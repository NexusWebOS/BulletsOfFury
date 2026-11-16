from pathlib import Path
from playwright.sync_api import sync_playwright
from urllib.request import urlopen,Request
import imageio_ffmpeg,json,subprocess,re,hashlib,html
R=Path(__file__).resolve().parents[1];O=R/'_shots/stage9_pilot_1115';V=O/'final-recording';FF=imageio_ffmpeg.get_ffmpeg_exe();q=json.loads((V/'recording.json').read_text(encoding='utf8'));checks=[];errors=[]
def ck(n,v,data=None):checks.append(dict(name=n,ok=bool(v),data=data));print(('PASS 'if v else'FAIL ')+n,flush=True)
def ff(args):
 p=subprocess.run([FF,'-hide_banner','-loglevel','error','-y',*map(str,args)],capture_output=True,text=True);assert p.returncode==0 and not p.stderr,p.stderr
def duration(path):
 p=subprocess.run([FF,'-hide_banner','-i',str(path)],capture_output=True,text=True);m=re.search(r'Duration: (\d+):(\d+):([\d.]+)',p.stderr);assert m,p.stderr;return int(m[1])*3600+int(m[2])*60+float(m[3])
ck('both recordings complete with native audio',len(q['clips'])==2 and all(c['completed']and c['peak']>.001 and not c['errors']for c in q['clips']))
ck('capture preserved shipping hashes',q['sourceBefore']==q['sourceAfter'])
movies={}
for c in q['clips']:
 mode=c['mode'];dst=O/('stage9-ship-to-pilot.mp4'if mode=='fight'else'freezer-text-scroll.mp4');tmp=V/(mode+'-encoded.mp4');print('ENCODING '+mode,flush=True)
 raw=V/'films'/(mode+'.webm')
 if not tmp.exists()or tmp.stat().st_mtime<raw.stat().st_mtime:ff(['-i',raw,'-vf','fps=30','-fps_mode','cfr','-c:v','libx264','-preset','fast','-crf','20','-pix_fmt','yuv420p','-threads','2','-af','aresample=async=1:first_pts=0','-c:a','aac','-b:a','160k',tmp])
 d=duration(tmp)
 if mode=='fight':
  stages=c['stages'];spec=[('', 'Tidal Sovereign — terminal vehicle checkpoint'),(':eject:', 'Ship destruction and ejection'),(':pilot:grenades','Current Breaker — alternating grenades'),(':pilot:flight-warn-n','Warned flight pass'),('play:pilot:marble','Liquid orb and radial grenades'),('play:pilot:tidal','Hand-shoved tidal waves'),('play:pilot:depth-spin','Background water rollers'),(':defeat:','Final pilot defeat'),('stageclear:','Native stage clear')]
  chapters=[{'start':0,'title':spec[0][1]}]
  for needle,title in spec[1:]:
   hit=next((s for s in stages if (s['tag']==needle if needle.startswith('play:pilot:')else needle in s['tag'])),None);ck('recorded '+title,hit is not None)
   if hit:chapters.append({'start':hit['at'],'title':title})
  ck('actual boss9 music progressed during combat',any(m.get('time',0)>2 and not m.get('paused',True)and m.get('src')for m in c['music']),c['music'][:3])
  ck('pilot health gauge and native side HUD captured',any(h['phase']=='pilot'and h['visible']and h['painted']and 'siege-left'in h['layers']and 'siege-right'in h['layers']for h in c['hud']),c['hud'][:4])
 else:
  changed=next((s['t']for s in c['scroll']if s['offset']>0),1);chapters=[{'start':0,'title':'Freezer — original full dialogue'},{'start':changed,'title':'Overflow scrolls upward'}]
  ck('recorded long dialogue scroll advances with text',max(s['offset']for s in c['scroll'])>0 and max(s['budget']for s in c['scroll'])>200,{'maxOffset':max(s['offset']for s in c['scroll'])})
 meta=';FFMETADATA1\ntitle=Bullets of Fury - '+mode+'\n'
 for i,ch in enumerate(chapters):meta+='[CHAPTER]\nTIMEBASE=1/1000\nSTART='+str(round(ch['start']*1000))+'\nEND='+str(round((chapters[i+1]['start']if i+1<len(chapters)else d)*1000))+'\ntitle='+ch['title']+'\n'
 mp=V/(mode+'.ffmeta');mp.write_text(meta,encoding='utf8');ff(['-i',tmp,'-f','ffmetadata','-i',mp,'-map','0:v:0','-map','0:a:0','-map_metadata','1','-map_chapters','1','-c','copy','-movflags','+faststart',dst]);ff(['-i',dst,'-f','null','-']);ck(mode+' full movie decode',True)
 p=subprocess.run([FF,'-hide_banner','-i',str(dst),'-af','volumedetect','-vn','-f','null','-'],capture_output=True,text=True);audio=[s.strip()for s in p.stderr.splitlines()if 'mean_volume:'in s or 'max_volume:'in s];ck(mode+' audible decoded native audio',len(audio)==2 and not any('-inf'in s for s in audio),audio)
 movies[mode]={'file':dst.name,'duration':d,'chapters':chapters,'sha256':hashlib.sha256(dst.read_bytes()).hexdigest(),'audio':audio};ff(['-ss',6 if mode=='fight'else 9,'-i',dst,'-frames:v','1',O/(mode+'-poster.png')])
buttons=''.join('<button data-player="fight" data-time="'+str(c['start'])+'">'+html.escape(c['title'])+'</button>'for c in movies['fight']['chapters'])
page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>BOF — Stage 9 pilot boss and dialogue scrolling</title><style>body{max-width:1200px;margin:24px auto;padding:0 18px;background:#091621;color:#e8eef1;font:17px/1.55 system-ui}video{width:100%;height:auto;background:#000}button{padding:8px;margin:4px;background:#234153;color:#fff;border:1px solid #5d90a4;cursor:pointer}a{color:#94e0df}.scope{font-size:15px;color:#abc5d2}h2{margin-top:36px}</style><h1>Stage 9 — the pilot behind the water ship</h1><p>Destroy the Tidal Sovereign and Current Breaker ejects, settles into his humanoid form, and fights as the real boss. His own health pool, water arsenal, Retina targets and physical-missile roller counters remain live. Stage clear and rewards wait for his defeat.</p><video id="fight" controls preload="metadata" poster="fight-poster.png" src="stage9-ship-to-pilot.mp4"></video><div>__BUTTONS__</div><p class="scope">Prepared terminal ship-health checkpoint. Both terminal defeats use scripted native damage; the entire pilot attack book runs on native clocks with brief real primary input. Player invulnerable. Includes native final destruction, flyover, stage clear and boss9 music. This is not an unassisted campaign win or full loadout balance certification.</p><h2>Freezer — dialogue scrolls inside the same box</h2><p>Long dialogue retains its readable font and fixed panel. The column moves upward as the next line types in, revealing the full ending rather than clipping it.</p><video id="freezer" controls preload="metadata" poster="freezer-poster.png" src="freezer-text-scroll.mp4"></video><p class="scope">Exact retained Freezer line rehearsed with the current cockpit art and native letter sounds. Archived openings remain inactive; none were restored or removed by this fix.</p><p><a href="../../docs/STAGE9_PILOT_1115.md">Implementation and verification</a></p><script>document.querySelectorAll('[data-time]').forEach(b=>b.onclick=async()=>{const v=document.getElementById(b.dataset.player);v.currentTime=Number(b.dataset.time);try{await v.play()}catch(e){if(e.name!=='AbortError')throw e}});document.querySelectorAll('video').forEach(v=>v.addEventListener('play',()=>document.querySelectorAll('video').forEach(other=>{if(other!==v)other.pause()})));</script></html>'''
(O/'review.html').write_text(page.replace('__BUTTONS__',buttons),encoding='utf8')
url='http://127.0.0.1:8766/_shots/stage9_pilot_1115/'
with sync_playwright()as pw:
 b=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1440,'height':1000});p.set_default_timeout(30000);p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None);p.on('response',lambda r:errors.append(str(r.status)+' '+r.url)if r.status>=400 else None)
 p.goto(url+'review.html');p.wait_for_function('[...document.querySelectorAll("video")].every(v=>v.readyState>=1)')
 for mode,m in movies.items():
  info=p.evaluate('id=>{const v=document.getElementById(id);return{w:v.videoWidth,h:v.videoHeight,d:v.duration}}',mode);ck(mode+' browser geometry/duration',info['w']==1824 and info['h']==1024 and abs(info['d']-m['duration'])<.3,info)
  p.evaluate('async id=>{const ac=new AudioContext();await ac.resume();const a=ac.createAnalyser();ac.createMediaElementSource(document.getElementById(id)).connect(a);a.connect(ac.destination);window["qa_"+id]={ac,a};}',mode);peak=0
  for ch in m['chapters']:
   p.evaluate('async o=>{const v=document.getElementById(o.id);v.currentTime=o.t;await v.play()}',{'id':mode,'t':ch['start']});p.wait_for_function('o=>{const v=document.getElementById(o.id);return !v.seeking&&!v.paused&&Math.abs(v.currentTime-o.t)<1.5}',arg={'id':mode,'t':ch['start']});t=p.evaluate('async id=>await new Promise(r=>document.getElementById(id).requestVideoFrameCallback((_,m)=>r(m.mediaTime)))',mode);ck('browser chapter '+ch['title'],abs(t-ch['start'])<1.6,t)
   a=p.evaluate('async id=>{const a=window["qa_"+id].a,s=new Float32Array(a.fftSize);let pk=0;for(let i=0;i<8;i++){await new Promise(r=>setTimeout(r,25));a.getFloatTimeDomainData(s);for(const v of s)pk=Math.max(pk,Math.abs(v))}return pk}',mode);peak=max(peak,a)
  ck(mode+' browser decoded audio',peak>.001,peak);p.evaluate('id=>document.getElementById(id).pause()',mode)
  with urlopen(Request(url+m['file'],headers={'Range':'bytes=0-255'}))as res:ck(mode+' HTTP206 seek',res.status==206 and len(res.read())==256)
 p.locator('[data-time]').nth(2).click();p.wait_for_timeout(500);p.evaluate('document.getElementById("fight").pause();scrollTo(0,0)');p.screenshot(path=str(O/'browser-review.png'));ck('review page has no overflow',p.evaluate('document.documentElement.scrollWidth<=innerWidth'));b.close()
ck('no recording/review page console or HTTP errors',not errors and not q['errors'],errors)
old=(R/'_shots/stage_frame_1115/full-suite.log').read_text(encoding='utf8').splitlines();now=(O/'full-suite.log').read_text(encoding='utf8').splitlines();fails=lambda rows:[s for s in rows if 'ASSERT FAIL:'in s or 'FAILED —'in s];suite={'passed':sum(s.startswith('  ok  ')for s in now),'beforeFailures':fails(old),'afterFailures':fails(now),'summary':now[-1]};ck('full8969 suite and failing-name comparison',suite['passed']==8969 and not suite['afterFailures']and suite['beforeFailures']==suite['afterFailures'],suite)
ck('shipping source still matches capture',all(hashlib.sha256((R/n).read_bytes()).hexdigest()==h for n,h in q['sourceBefore'].items()))
result={'checks':checks,'errors':errors,'movies':movies,'suite':suite,'scope':q['scope']};(O/'media-qa.json').write_text(json.dumps(result,indent=2),encoding='utf8');print(str(sum(c['ok']for c in checks))+'/'+str(len(checks))+' media/packaging checks passed');assert all(c['ok']for c in checks)
