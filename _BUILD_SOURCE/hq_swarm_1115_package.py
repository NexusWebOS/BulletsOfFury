from pathlib import Path
import json,subprocess,re,hashlib,html
from PIL import Image,ImageDraw
import imageio_ffmpeg
R=Path('D:/BOF-Downloads/2026-11-14/RevG-source');O=R/'_shots/hq_swarm_1115';FF=imageio_ffmpeg.get_ffmpeg_exe()
q=json.loads((O/'recording.json').read_text(encoding='utf8'))
assert q['coreBefore']==q['coreAfter']and not q['errors']and len(q['clips'])==2
def run(args):
 p=subprocess.run([FF,'-hide_banner','-loglevel','error','-y',*args],capture_output=True,text=True)
 assert p.returncode==0 and not p.stderr,p.stderr
def duration(path):
 p=subprocess.run([FF,'-hide_banner','-i',str(path)],capture_output=True,text=True)
 m=re.search(r'Duration: (\d+):(\d+):([\d.]+)',p.stderr)
 return int(m[1])*3600+int(m[2])*60+float(m[3])
movies=[]
for c in q['clips']:
 part=c['part'];event=lambda text:next(s['at']for s in c['stages']if text in s['tag'])
 if part=='hq5':
  name='hq-fast-swarm';title='Fast evacuation, stealth missiles and guard escape'
  chapters=[(0,'Faster individual departures'),(event(':HQ19-QUIET:'),'Five quiet seconds'),(event(':HQ19-ATTACK:'),'Stealth fighters launch missiles'),(event(':HQ19-DECKER:'),'Rapid ten-ship counterattack'),(event(':HQ19-SWARM:'),'Reinforcements overwhelm the base'),(event(':HQ19-AXEL:')+.1,'Decker somersault and southeast boost'),(event(':HQ19-AXEL:')+1.0,'Axel somersault and southwest boost'),(event('intro:'),'Native Stage6 opening')]
  points=[(2.4,'Fast frame-by-frame departure'),(event(':HQ19-SWARM:')+.9,'Missile-firing stealth swarm'),(event(':HQ19-AXEL:')+.28,'Decker somersault'),(event(':HQ19-AXEL:')+1.25,'Axel somersault')]
  scope='Cole / Hard. Native checkpoint from HQ evacuation through the retained five-second pause, faster assault, ten guard takedowns, reinforcement swarm and somersault escapes into Stage6. Earlier homecoming is outside this clip.'
 else:
  name='stage6-to7-full';title='Stage6 to7 - Harrier aftermath and sewer entry'
  chapters=[(0,'Harrier aftermath'),(event(':POST6-06:'),'Signal below the city'),(event(':POST6-08:'),'The drains'),(event(':POST6-11:'),'Keep talking all the way in'),(event('intro:'),'Stage7 card'),(event(':stage7-approach:'),'Riverbank and sewer approach'),(event('launch:::run:') ,'Native underground entry'),(event('play:'),'Stage7 gameplay handoff')]
  points=[(event(':POST6-06:')+1.6,'Underground signal briefing'),(event(':POST6-08:')+1.4,'The sewer entrance'),(event(':stage7-approach:')+1.6,'Native riverbank approach'),(event('play:')+1.0,'Stage7 handoff')]
  scope='Cole / Hard, Harrier branch. Full current post-Stage6 dialogue, Stage7 card, riverbank/sewer approach and native launch to gameplay. The prepared cleared-stage checkpoint connects directly to Stage7, omitting the results, map and gear-menu pauses. No dialogue is skipped.'
 chapters=sorted([{'start':t,'title':title}for t,title in chapters],key=lambda v:v['start'])
 encoded=O/(name+'-encoded.mp4')
 if not encoded.exists():run(['-i',str(O/('films/'+part+'.webm')),'-vf','fps=30','-fps_mode','cfr','-c:v','libx264','-preset','fast','-crf','21','-pix_fmt','yuv420p','-threads','2','-af','aresample=async=1:first_pts=0','-c:a','aac','-b:a','160k',str(encoded)])
 total=duration(encoded);meta=';FFMETADATA1\ntitle=BOF - '+title+'\n'
 for i,ch in enumerate(chapters):
  end=chapters[i+1]['start']if i+1<len(chapters)else total
  assert ch['start']<end<=total+.15
  meta+='[CHAPTER]\nTIMEBASE=1/1000\nSTART='+str(round(ch['start']*1000))+'\nEND='+str(round(end*1000))+'\ntitle='+ch['title']+'\n'
 mf=O/(name+'.ffmeta');mf.write_text(meta,encoding='utf8');movie=O/(name+'.mp4')
 run(['-i',str(encoded),'-f','ffmetadata','-i',str(mf),'-map','0:v:0','-map','0:a:0','-map_metadata','1','-map_chapters','1','-c','copy','-movflags','+faststart',str(movie)])
 run(['-i',str(movie),'-f','null','-'])
 p=subprocess.run([FF,'-hide_banner','-i',str(movie),'-af','volumedetect','-vn','-f','null','-'],capture_output=True,text=True)
 audio=[v.strip()for v in p.stderr.splitlines()if'mean_volume:'in v or'max_volume:'in v]
 assert len(audio)==2 and not any('-inf'in v for v in audio)
 contact=Image.new('RGB',(1280,768),'#102030');d=ImageDraw.Draw(contact)
 for i,(t,label)in enumerate(points):
  path=O/(part+'-frame-'+str(i)+'.png');run(['-ss',str(t),'-i',str(movie),'-frames:v','1',str(path)])
  im=Image.open(path).convert('RGB');im.thumbnail((640,360));x=i%2*640;y=i//2*384
  contact.paste(im,(x,y));d.text((x+10,y+362),label,fill='white')
 contact.save(O/(part+'-contact.jpg'),quality=95)
 movies.append({'part':part,'title':title,'file':movie.name,'duration':duration(movie),'chapters':chapters,'decodeErrors':[],'audio':audio,'sha256':hashlib.sha256(movie.read_bytes()).hexdigest(),'scope':scope,'poster':part+'-frame-0.png'})
 print(json.dumps(movies[-1]),flush=True)
q['movies']=movies;(O/'recording.json').write_text(json.dumps(q,indent=2),encoding='utf8')
sections=[]
for m in movies:
 buttons=''.join('<button data-player="'+m['part']+'" data-time="'+str(ch['start'])+'">'+html.escape(ch['title'])+'</button>'for ch in m['chapters'])
 sections.append('<section><h2>'+html.escape(m['title'])+'</h2><video id="'+m['part']+'" controls preload="metadata" poster="'+m['poster']+'" src="'+m['file']+'"></video><p>'+buttons+'</p><p>'+m['scope']+'</p></section>')
page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>BOF - Evacuation and Stage6-7 cinematics</title><style>body{max-width:1200px;margin:24px auto;padding:0 20px;background:#0c1723;color:#f1e9d7;font:17px/1.6 system-ui}video{width:100%;background:#000}button{padding:9px;margin:4px;background:#253d51;color:#fff;border:1px solid #668ba5;border-radius:4px;cursor:pointer}a{color:#8fe3d0}section{margin-bottom:45px}.gallery{display:flex;gap:15px}.gallery img{width:256px}small{color:#a9bfd0}</style><h1>BOF - Faster evacuation and the road underground</h1><p>Two real Chromium recordings with native game audio. Cinematic checkpoints, not campaign wins.</p>__SECTIONS__<details><summary>Actual guard somersault frames</summary><div class="gallery"><figure><figcaption>Decker</figcaption><img src="decker-somersault.gif" alt="Decker native eight-frame somersault"></figure><figure><figcaption>Axel</figcaption><img src="axel-somersault.gif" alt="Axel native eight-frame somersault"></figure></div></details><p><a href="../../docs/HQ_SWARM_1115.md">Changes and verification</a> | <a href="../../docs/STAGE67_CINEMATICS_1115.md">Stage6-7 recording scope</a></p><script>document.querySelectorAll('button').forEach(b=>b.onclick=async()=>{const v=document.getElementById(b.dataset.player);document.querySelectorAll('video').forEach(o=>{if(o!==v)o.pause()});v.currentTime=Number(b.dataset.time);try{await v.play()}catch(e){if(e.name!=='AbortError')throw e}});</script></html>'''
(O/'review.html').write_text(page.replace('__SECTIONS__',''.join(sections)),encoding='utf8')
