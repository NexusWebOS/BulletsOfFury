"""Check the installed additive guide and actual decoded video/audio playback."""
from pathlib import Path
import json,urllib.request,subprocess,array
import imageio_ffmpeg
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];W=R/'_shots/cloud_carrier_1101';base='http://127.0.0.1:8805';checks=[];errors=[]
def ck(n,v,d=None):checks.append(dict(name=n,passed=bool(v),data=d));print('PASS'if v else'FAIL',n,flush=True)
old=json.loads((W/'before-guide.json').read_text());now=json.load(urllib.request.urlopen(base+'/enemy-showcase-1031/manifest.json'));ck('All160 previous enemy cards unchanged;161 current cards',len(now['items'])==161 and all(next(q for q in now['items']if q['id']==p['id'])==p for p in old['items']))
ff=imageio_ffmpeg.get_ffmpeg_exe();r=subprocess.run([ff,'-v','error','-i',str(W/'video/cloud-carriers.mp4'),'-vn','-ac','1','-ar','22050','-f','f32le','-'],capture_output=True,check=True);a=array.array('f');a.frombytes(r.stdout);peak=max(abs(v)for v in a);ck('Decoded AAC is audible and stays below digital full scale',.005<peak<1,dict(peak=peak,samples=len(a)))
with sync_playwright()as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1280,'height':900});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:350])if m.type=='error'else None)
 p.goto(base+'/current/stage6-cloud-carriers-1101.html',wait_until='load');p.wait_for_function('document.querySelector("video").readyState>=2');q=p.evaluate('()=>{const v=document.querySelector("video");return{duration:v.duration,width:v.videoWidth,height:v.videoHeight}}');ck('Installed player loads1280x800 decoded movie',q['width']==1280 and q['height']==800 and q['duration']>23,q)
 for t in[1,7,15,22]:
  p.evaluate('t=>{document.querySelector("video").currentTime=t}',t);p.wait_for_function('()=>{const v=document.querySelector("video");return !v.seeking&&v.readyState>=2}');ck('Browser decoded seek '+str(t)+'s',p.evaluate('t=>Math.abs(document.querySelector("video").currentTime-t)<.15',t))
 p.evaluate('''async()=>{const v=document.querySelector('video');v.currentTime=14;window.qaAudio=new AudioContext();const s=qaAudio.createMediaElementSource(v);window.qaAnalyser=qaAudio.createAnalyser();s.connect(qaAnalyser);qaAnalyser.connect(qaAudio.destination);await qaAudio.resume();await v.play();}''');peak=0
 for i in range(12):
  p.wait_for_timeout(150);peak=max(peak,p.evaluate('()=>{const a=new Float32Array(qaAnalyser.fftSize);qaAnalyser.getFloatTimeDomainData(a);return Math.max(...a.map(Math.abs))}'))
 ck('Actual browser playback has decoded audio',peak>.005,peak);p.evaluate('document.querySelector("video").pause()');p.screenshot(path=str(W/'installed-preview.png'));ck('No installed preview page/console errors',not errors,errors);b.close()
(W/'preview-checks.json').write_text(json.dumps(checks,indent=2));print('SUMMARY',sum(q['passed']for q in checks),'/',len(checks));assert all(q['passed']for q in checks)
