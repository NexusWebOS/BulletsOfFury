from pathlib import Path
from PIL import Image,ImageDraw
import json,subprocess,re,hashlib,html
import imageio_ffmpeg
R=Path(__file__).resolve().parents[1];O=R/'_shots/crossed_fate_1115';FF=imageio_ffmpeg.get_ffmpeg_exe()
q=json.loads((O/'recording.json').read_text(encoding='utf8'))
assert q['coreBefore']==q['coreAfter']and not q['errors']and len(q['clips'])==3
def run(args):
 p=subprocess.run([FF,'-hide_banner','-loglevel','error','-y',*args],capture_output=True,text=True)
 assert p.returncode==0 and not p.stderr,p.stderr
def duration(path):
 p=subprocess.run([FF,'-hide_banner','-i',str(path)],capture_output=True,text=True);m=re.search(r'Duration: (\d+):(\d+):([\d.]+)',p.stderr)
 return int(m[1])*3600+int(m[2])*60+float(m[3])
movies=[]
for c in q['clips']:
 part=c['part'];event=lambda text:next(s['at']for s in c['stages']if text in s['tag'])
 if part=='split':
  title='Furious split - Harrier leads, Storm Cannon follows'
  chapters=[(0,'Two overhead aircraft'),(4.0,'Retained Rough Riders interception dialogue'),(event('route-choice'),'Storm Cannon or Rough Riders'),(event(':route-left:'),'Storm Cannon pursuit briefing')]
  points=[(1.3,'Harrier overtakes the Fury wing'),(2.3,'Storm Cannon follows with shadow'),(8,'Retained Rough Riders interception'),(event('route-choice')+.75,'Furious pursuit choice')]
  scope='Prepared Cole / Furious native Stage6 split after the carrier prelude. Both real aircraft, retained Rebel dialogue, pursuit choice and full Storm Cannon briefing. The native left route is selected automatically for this cinematic checkpoint; no fight or campaign win is claimed.'
 else:
  storm=part=='storm';title='Storm Cannon defeated - Crossed Fate'if storm else'Rough Riders defeated - Road Not Taken'
  mt=event(':::transit:');chapters=[(0,'The skies are clearing'),(event(':POST6-04:'),'Who escaped toward the city'),(event(':POST6-11:'),'Regroup and choose the next route'),(mt,'Harrier and Fury Fighters reach the city'if storm else'Storm Cannon escapes west'),(event(':::password:'),'Alternate-route password'),(event(':::achievement:'),'Crossed Fate unlocked'if storm else'Road Not Taken unlocked'),(event(':::choice:'),'Campaign map choices restored')]
  points=[(event(':POST6-04:')+3,'Remaining threat report'),(mt+(6.1 if storm else 2.2),'Harrier crash'if storm else'Storm Cannon westward escape'),(event(':::password:')+2.9,'Password route message'),(event(':::achievement:')+1.1,'Generated achievement medal')]
  scope='Cole / Furious. Scripted damage goes through the actual native module/core or five-Rebel/Retina/death owners. The verified result then plays every post6 dialogue beat and the map event without skips. This is a cinematic checkpoint, not an unassisted campaign win.'
 chapters=[{'start':t,'title':n}for t,n in sorted(chapters)]
 encoded=O/(part+'-encoded.mp4');source=O/'films'/(part+'.webm')
 # Always encode the current recording, so a prior checkpoint can never be reused silently.
 run(['-i',str(source),'-vf','fps=30','-fps_mode','cfr','-c:v','libx264','-preset','fast','-crf','21','-pix_fmt','yuv420p','-threads','2','-af','aresample=async=1:first_pts=0','-c:a','aac','-b:a','160k',str(encoded)])
 total=duration(encoded);meta=';FFMETADATA1\ntitle=BOF - '+title+'\n'
 for i,ch in enumerate(chapters):
  end=chapters[i+1]['start']if i+1<len(chapters)else total
  assert ch['start']<end<=total+.2
  meta+='[CHAPTER]\nTIMEBASE=1/1000\nSTART='+str(round(ch['start']*1000))+'\nEND='+str(round(end*1000))+'\ntitle='+ch['title']+'\n'
 mf=O/(part+'.ffmeta');mf.write_text(meta,encoding='utf8');movie=O/(part+'.mp4')
 run(['-i',str(encoded),'-f','ffmetadata','-i',str(mf),'-map','0:v:0','-map','0:a:0','-map_metadata','1','-map_chapters','1','-c','copy','-movflags','+faststart',str(movie)])
 run(['-i',str(movie),'-f','null','-'])
 p=subprocess.run([FF,'-hide_banner','-i',str(movie),'-af','volumedetect','-vn','-f','null','-'],capture_output=True,text=True)
 audio=[v.strip()for v in p.stderr.splitlines()if'mean_volume:'in v or'max_volume:'in v];assert len(audio)==2 and not any('-inf'in v for v in audio)
 contact=Image.new('RGB',(1280,768),'#102030');d=ImageDraw.Draw(contact)
 for i,(t,label)in enumerate(points):
  path=O/(part+'-frame-'+str(i)+'.png');run(['-ss',str(t),'-i',str(movie),'-frames:v','1',str(path)])
  im=Image.open(path).convert('RGB');im.thumbnail((640,360));x=i%2*640;y=i//2*384;contact.paste(im,(x,y));d.text((x+10,y+362),label,fill='white')
 contact.save(O/(part+'-contact.jpg'),quality=95)
 movies.append({'part':part,'title':title,'file':movie.name,'duration':total,'chapters':chapters,'decodeErrors':[],'audio':audio,'sha256':hashlib.sha256(movie.read_bytes()).hexdigest(),'scope':scope,'poster':part+'-frame-0.png'})
 print(json.dumps(movies[-1]),flush=True)
q['movies']=movies;(O/'recording.json').write_text(json.dumps(q,indent=2),encoding='utf8')
sections=[]
for m in movies:
 buttons=''.join('<button data-player="'+m['part']+'" data-time="'+str(ch['start'])+'">'+html.escape(ch['title'])+'</button>'for ch in m['chapters'])
 sections.append('<section><h2>'+html.escape(m['title'])+'</h2><video id="'+m['part']+'" controls preload="metadata" poster="'+m['poster']+'" src="'+m['file']+'"></video><p>'+buttons+'</p><p class="scope">'+m['scope']+'</p></section>')
page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>BOF - Crossed Fate branches</title><style>body{max-width:1200px;margin:24px auto;padding:0 20px;background:#0c1723;color:#f1e9d7;font:17px/1.6 system-ui}video{width:100%;background:#000}button{padding:9px;margin:4px;background:#253d51;color:#fff;border:1px solid #668ba5;border-radius:4px;cursor:pointer}a{color:#8fe3d0}section{margin-bottom:45px}.medals{display:flex;gap:24px}.medals img{width:128px;image-rendering:pixelated}.scope{color:#a9bfd0;font-size:15px}</style><h1>BOF - Crossed Fate</h1><p>The Furious split and both Stage6 outcomes. Real Chromium recordings with native game audio; prepared checkpoints, not campaign wins. Use the chapter buttons to jump straight to either map event.</p><div class="medals"><figure><img src="../../assets/game/shared/cinematics/crossed_fate_1115/crossed_fate.png" alt="Crossed Fate medal"><figcaption>Crossed Fate</figcaption></figure><figure><img src="../../assets/game/shared/cinematics/crossed_fate_1115/road_not_taken.png" alt="Road Not Taken medal"><figcaption>Road Not Taken</figcaption></figure></div>__SECTIONS__<p><a href="../../docs/CROSSED_FATE_1115.md">Changes and verification</a></p><script>document.querySelectorAll('button').forEach(b=>b.onclick=async()=>{const v=document.getElementById(b.dataset.player);document.querySelectorAll('video').forEach(o=>{if(o!==v)o.pause()});v.currentTime=Number(b.dataset.time);try{await v.play()}catch(e){if(e.name!=='AbortError')throw e}});</script></html>'''
(O/'review.html').write_text(page.replace('__SECTIONS__',''.join(sections)),encoding='utf8')
