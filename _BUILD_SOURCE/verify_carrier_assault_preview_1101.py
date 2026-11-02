"""Installed player/guide verification, full movie decoding and actual AAC playback."""
from pathlib import Path
import json,urllib.request,subprocess,array
import imageio_ffmpeg
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];W=R/'_shots/carrier_assault_1101';base='http://127.0.0.1:8805';checks=[];errors=[];ff=imageio_ffmpeg.get_ffmpeg_exe()
def ck(n,v,d=None):checks.append(dict(name=n,passed=bool(v),data=d));print('PASS'if v else'FAIL',n,flush=True)
receipt=json.loads((W/'publication.json').read_text());before=json.loads((W/'before-guide.json').read_text());current=json.load(urllib.request.urlopen(base+'/enemy-showcase-1031/manifest.json'));ids={q['id']for q in receipt['films']};others=[q for q in before['items']if q['id']not in ids];ck('Four current cards and all unrelated guide cards preserved',len(current['items'])==164 and all(next(q for q in current['items']if q['id']==v['id'])==v for v in others))
with sync_playwright()as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1280,'height':900});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:350])if m.type=='error'else None)
 p.goto(base+'/current/stage6-cloud-carriers-1101.html?revision=carrier-assault-polish-1101',wait_until='load');ck('Original carrier URL now presents all four updated players',p.locator('video').count()==4)
 p.evaluate('''()=>{window.qaAudio=new AudioContext();window.qaGain=qaAudio.createGain();qaGain.gain.value=.01;qaGain.connect(qaAudio.destination);window.qaAnalysers={};}''')
 for film in receipt['films']:
  kind=film['kind'];selector='#v-'+kind;p.evaluate('s=>{const v=document.querySelector(s);v.preload="auto";v.load()}',selector);p.wait_for_function('s=>document.querySelector(s).readyState>=2',arg=selector)
  q=p.evaluate('s=>{const v=document.querySelector(s);return{duration:v.duration,width:v.videoWidth,height:v.videoHeight}}',selector);ck(kind+' full1280x800 movie metadata',q['width']==1280 and q['height']==800 and abs(q['duration']-film['duration'])<.2,q)
  for label,t in film['chapters'][1:3]:
   p.evaluate('q=>{document.querySelector(q[0]).currentTime=q[1]}',[selector,t]);p.wait_for_function('s=>{const v=document.querySelector(s);return !v.seeking&&v.readyState>=2}',arg=selector);ck(kind+' decoded chapter '+label,p.evaluate('q=>Math.abs(document.querySelector(q[0]).currentTime-q[1])<.2',[selector,t]))
  # Actual media-element decoding/playing; inspect samples from this film alone.
  p.evaluate('''async q=>{const v=document.querySelector(q[0]);v.currentTime=q[1];const source=qaAudio.createMediaElementSource(v),a=qaAudio.createAnalyser();source.connect(a);a.connect(qaGain);qaAnalysers[q[0]]=a;await qaAudio.resume();await v.play()}''',[selector,film['chapters'][1][1]])
  peak=0
  for i in range(10):p.wait_for_timeout(120);peak=max(peak,p.evaluate('s=>{const a=qaAnalysers[s],q=new Float32Array(a.fftSize);a.getFloatTimeDomainData(q);return Math.max(...q.map(Math.abs))}',selector))
  ck(kind+' browser has decoded audible playback',peak>.004,peak);p.evaluate('s=>document.querySelector(s).pause()',selector)
  raw=subprocess.run([ff,'-v','error','-i',str(W/'video'/(kind+'.mp4')),'-vn','-ac','1','-ar','22050','-f','f32le','-'],capture_output=True,check=True).stdout;a=array.array('f');a.frombytes(raw);peak=max(abs(v)for v in a);ck(kind+' AAC stream is audible without clipping',.005<peak<1,peak)
 # Chapter controls should work as controls, not only through direct JS seeking.
 p.locator('button[data-video="v-laser"]').nth(2).click();p.wait_for_function('()=>!document.querySelector("#v-laser").paused');ck('Timed detonation chapter button starts the selected film',p.evaluate('document.querySelector("#v-laser").currentTime>10'));p.evaluate('document.querySelector("#v-laser").pause()');p.screenshot(path=str(W/'installed-preview.png'));ck('No page/console playback errors',not errors,errors);b.close()
(W/'preview-checks.json').write_text(json.dumps(checks,indent=2));print('SUMMARY',sum(q['passed']for q in checks),'/',len(checks));assert all(q['passed']for q in checks)
