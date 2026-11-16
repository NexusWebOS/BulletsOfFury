from pathlib import Path
from PIL import Image,ImageDraw
import json,subprocess,re,hashlib
import imageio_ffmpeg
ROOT=Path('D:/BOF-Downloads/2026-11-14/RevG-source');OUT=ROOT/'_shots/cinematic_rework_1114';FILMS=OUT/'films';ENC=OUT/'encoded';ENC.mkdir(exist_ok=True);FF=imageio_ffmpeg.get_ffmpeg_exe()
report=json.loads((OUT/'recording.json').read_text(encoding='utf-8'));assert len(report['clips'])==5 and not report['errors'];clips={q['part']:q for q in report['clips']}
s5=clips['arrival5'];assert s5['end']['gravityReady']and all(any(':'+phase+':'in q['tag']for q in s5['stages'])for phase in ['assembly','countdown'])
def run(args):
 r=subprocess.run([FF,'-hide_banner','-loglevel','error','-y',*args],capture_output=True,text=True);assert r.returncode==0 and not r.stderr,r.stderr
def duration(file):
 r=subprocess.run([FF,'-hide_banner','-i',str(file)],capture_output=True,text=True);m=re.search(r'Duration: (\d+):(\d+):([\d.]+)',r.stderr);assert m,r.stderr;return int(m[1])*3600+int(m[2])*60+float(m[3])
def event(part,needle):return next(e['at']for e in clips[part]['stages']if needle in e['tag'])
codec=['-vf','fps=30','-fps_mode','cfr','-c:v','libx264','-preset','fast','-crf','21','-pix_fmt','yuv420p','-threads','2','-af','aresample=async=1:first_pts=0','-c:a','aac','-b:a','160k']
for part in clips:
 print('Encoding '+part,flush=True);run(['-i',str(FILMS/(part+'.webm')),*codec,str(ENC/(part+'.mp4'))])
groups=[('stage3-corrected',['escape','arrival3','hq3']),('stage4-to-5',['post4','arrival5'])];movies=[];thumbs=[]
for key,parts in groups:
 starts={};total=0
 for part in parts:starts[part]=total;total+=duration(ENC/(part+'.mp4'))
 if key=='stage3-corrected':
  chapterSpec=[('escape',None,'Service data-link'),('escape','SL2-08','Ground rumble and approaching fire wave'),('escape','SL2-09','Lift-off'),('arrival3',None,'Stage 3 fly-in with scrolling water'),('hq3',None,'Fury HQ — satellite signal discovery'),('hq3','CW3-09','The team discusses the trip to space'),('hq3','CW3-W01','Six-panel workshop comic'),('hq3','CW3-DEMO','Top-down Photon Cannon test'),('hq3','CW3-W04','Cole and Decker — the hug')]
  thumbSpec=[('escape','SL2-09',1.3,'Escape over the fire wave'),('arrival3',None,9,'Scrolling water approach'),('hq3','CW3-03',2,'The alien satellite signal'),('hq3','CW3-DEMO',4,'Overhead Photon Cannon'),('hq3','CW3-W04',2,'The hug'),('hq3','CW3-W08',2,'Trust and departure')]
 else:
  chapterSpec=[('post4',None,'The Federation prototype aircraft attachments'),('post4','B403','The satellite camera feed'),('post4','POST4-07','Space kits ready'),('arrival5',None,'Stage 5 card and space ascent'),('arrival5',':assembly:','Aircraft attachment and assembly'),('arrival5',':countdown:','Launch into Stage 5')]
  thumbSpec=[('post4',None,2,'The Federation kits'),('post4','B403',2,'The satellite feed'),('arrival5',':assembly:',2,'Prototype kit assembly')]
 chapters=[]
 for part,needle,title in chapterSpec:
  try:t=starts[part]+(event(part,needle)if needle else 0)
  except StopIteration:continue
  chapters.append({'start':round(t,3),'title':title})
 chapters.sort(key=lambda q:q['start']);meta=';FFMETADATA1\ntitle=Bullets of Fury - '+key+'\n'
 for i,c in enumerate(chapters):meta+='[CHAPTER]\nTIMEBASE=1/1000\nSTART='+str(round(c['start']*1000))+'\nEND='+str(round((chapters[i+1]['start']if i+1<len(chapters)else total)*1000))+'\ntitle='+c['title']+'\n'
 (OUT/(key+'.ffmeta')).write_text(meta,encoding='utf-8');(ENC/(key+'.txt')).write_text('\n'.join("file '"+part+".mp4'"for part in parts),encoding='utf-8')
 target=OUT/(key+'.mp4');run(['-f','concat','-safe','0','-i',str(ENC/(key+'.txt')),'-f','ffmetadata','-i',str(OUT/(key+'.ffmeta')),'-map','0:v:0','-map','0:a:0','-map_metadata','1','-map_chapters','1','-c','copy','-movflags','+faststart',str(target)]);run(['-i',str(target),'-f','null','-'])
 level=subprocess.run([FF,'-hide_banner','-i',str(target),'-af','volumedetect','-vn','-f','null','-'],capture_output=True,text=True)
 audio=[s.strip()for s in level.stderr.splitlines()if 'mean_volume:'in s or 'max_volume:'in s]
 movies.append({'key':key,'file':target.name,'duration':duration(target),'chapters':chapters,'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'decodeErrors':[],'audio':audio})
 for j,(part,needle,delay,label)in enumerate(thumbSpec):
  try:t=starts[part]+(event(part,needle)if needle else 0)+delay
  except StopIteration:continue
  file=OUT/(key+'-'+str(j)+'.png');run(['-ss',str(t),'-i',str(target),'-frames:v','1',str(file)]);thumbs.append((file,label))
 print(json.dumps(movies[-1]),flush=True)
contact=Image.new('RGB',(1440,294*((len(thumbs)+2)//3)),'#0a111b');d=ImageDraw.Draw(contact)
for i,(file,label)in enumerate(thumbs):
 im=Image.open(file).convert('RGB');im.thumbnail((480,270));x=i%3*480;y=i//3*294;contact.paste(im,(x+(480-im.width)//2,y));d.text((x+8,y+272),label,fill='#f0e6c5')
contact.save(OUT/'contact-sheet.jpg',quality=94)
(OUT/'movies.json').write_text(json.dumps({'movies':movies},indent=2),encoding='utf-8')
def player(m,title,poster):
 buttons=''.join('<button data-player="'+m['key']+'" data-time="'+str(c['start'])+'">'+c['title']+'</button>'for c in m['chapters'])
 return '<section><h2>'+title+'</h2><video id="'+m['key']+'" controls preload="metadata" src="'+m['file']+'" poster="'+poster+'"></video><div class="chapters">'+buttons+'</div><p><a download href="'+m['file']+'">Download recording</a></p></section>'
html='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>BOF — revised cinematic sequence</title><style>body{max-width:1200px;margin:30px auto;padding:0 20px;background:#09121c;color:#eee7d2;font:17px/1.55 system-ui}h1{margin-bottom:6px}p{color:#bccbdc}section{margin:30px 0}video,img{width:100%;border:1px solid #3c5369;border-radius:7px;background:#02060c}button{padding:9px 12px;margin:4px;color:#f4ecd4;background:#20364c;border:1px solid #52738d;border-radius:5px;cursor:pointer;font:inherit}a{color:#75dfd1}small{color:#9fb6cb}</style><h1>Fury Division — revised cinematics</h1><p>The satellite discovery now leads to the Federation's prototype aircraft attachments. The revised Stage 3 reel includes ground rumble, a continuous fire wave, moving water, a six-panel workshop comic and the overhead Photon Cannon test.</p>__PLAYERS__<section><h2>The six workshop panels</h2><img src="workshop-preview.png" alt="Cole and Decker's workshop comic, six illustrated panels"></section><p><small>Fresh native Chromium cinematic checkpoints with game audio. Dialogue plays at native speed without skips. Gameplay between scenes is omitted; these are not campaign playthroughs.</small></p><p><a href="../../docs/CINEMATIC_REWORK_1114.md">Change notes and verification</a> · <a href="../../docs/CINEMATIC_REWORK_ART_1114.json">Generated art sources and prompts</a></p><script>const all=[...document.querySelectorAll('video')];document.querySelectorAll('button').forEach(b=>b.onclick=async()=>{const v=document.getElementById(b.dataset.player);all.forEach(o=>{if(o!==v)o.pause()});v.currentTime=Number(b.dataset.time);try{await v.play()}catch(e){if(e.name!=='AbortError')throw e}});</script></html>'''
html=html.replace('__PLAYERS__',player(movies[1],'Stage 4 → 5: the trip to space','stage4-to-5-0.png')+player(movies[0],'Stage 3: corrected escape, discovery and workshop','stage3-corrected-3.png'))
(OUT/'review.html').write_text(html,encoding='utf-8');print('Both complete movie reels are packaged.',flush=True)
