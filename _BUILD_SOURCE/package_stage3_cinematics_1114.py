from pathlib import Path
import json,subprocess,re,hashlib
import imageio_ffmpeg
from PIL import Image,ImageDraw
OUT=Path('D:/BOF-Downloads/2026-11-14/RevG-source/_shots/stage3_cinematics_1114')
report=json.loads((OUT/'recording.json').read_text());assert not report['errors'] and len(report['clips'])==3
assert all(c['peak']>.001 and not c['errors'] for c in report['clips'])
ff=imageio_ffmpeg.get_ffmpeg_exe();chapters=[];total=0;thumbs=[]
names={'lead-in':'Radio lead-in to Stage 3','arrival':'Stage 3 card and fly-in','hq':'After Stage 3: HQ and prototypes'}
for c in report['clips']:
 part=c['part'];src=OUT/(part+'.webm')
 p=subprocess.run([ff,'-i',str(src)],capture_output=True,text=True)
 m=re.search(r'Duration: (\d+):(\d+):([\d.]+)',p.stderr);assert m,p.stderr
 duration=int(m[1])*3600+int(m[2])*60+float(m[3])
 chapters.append({'part':part,'title':names[part],'start':round(total,2),'duration':duration});total+=duration
 if c['expectedBeats']:
  seen=[s['tag'].rsplit(':',1)[-1] for s in c['stages']]
  assert all(q['id'] in seen for q in c['expectedBeats']),[q['id'] for q in c['expectedBeats'] if q['id'] not in seen]
 for i,f in enumerate([.20,.50,.82]):
  dst=OUT/(part+'-frame-'+str(i)+'.png')
  subprocess.run([ff,'-v','error','-y','-ss',str(duration*f),'-i',str(src),'-frames:v','1',str(dst)],check=True)
  thumbs.append((dst,names[part]+' / '+str(round(duration*f,1))+'s'))
contact=Image.new('RGB',(1440,870),'#10151d');g=ImageDraw.Draw(contact)
for i,(path,label) in enumerate(thumbs):
 im=Image.open(path).convert('RGB');im.thumbnail((480,270));x=i%3*480;y=i//3*290
 contact.paste(im,(x+(480-im.width)//2,y));g.text((x+8,y+272),label,fill='#fff0cf')
contact.save(OUT/'contact-sheet.jpg',quality=93)
(OUT/'concat.txt').write_text('\n'.join("file '"+(OUT/(c['part']+'.webm')).as_posix()+"'" for c in report['clips'])+'\n',encoding='utf-8')
meta=';FFMETADATA1\ntitle=Bullets of Fury - Stage 3 cinematics\n'
for ch in chapters:
 meta+='[CHAPTER]\nTIMEBASE=1/1000\nSTART='+str(round(ch['start']*1000))+'\nEND='+str(round((ch['start']+ch['duration'])*1000))+'\ntitle='+ch['title']+'\n'
(OUT/'chapters.ffmeta').write_text(meta,encoding='utf-8')
cmd=[ff,'-v','warning','-y','-f','concat','-safe','0','-i',str(OUT/'concat.txt'),'-f','ffmetadata','-i',str(OUT/'chapters.ffmeta'),'-map','0:v:0','-map','0:a:0','-map_metadata','1','-map_chapters','1','-c:v','libx264','-preset','fast','-crf','21','-pix_fmt','yuv420p','-r','30','-af','aresample=async=1:first_pts=0','-c:a','aac','-b:a','160k','-movflags','+faststart',str(OUT/'stage3-cinematics.mp4')]
with (OUT/'encode.log').open('w') as log:subprocess.run(cmd,stderr=log,stdout=log,check=True)
report['chapters']=chapters;report['combined']={'file':'stage3-cinematics.mp4','duration':round(total,2),'sha256':hashlib.sha256((OUT/'stage3-cinematics.mp4').read_bytes()).hexdigest()}
(OUT/'recording.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
buttons=' '.join('<button onclick="v.currentTime='+str(c['start'])+';v.play()">'+c['title']+'</button>' for c in chapters)
(OUT/'review.html').write_text('''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>BOF Stage 3 cinematics</title><style>body{max-width:1100px;margin:32px auto;padding:0 18px;background:#10151d;color:#ecdfbd;font:17px/1.5 system-ui}video{width:100%;background:#000}button{background:#27333e;border:1px solid #82744f;color:#fff0cf;padding:10px;margin:4px;cursor:pointer}a{color:#8dd9ef}img{max-width:100%}</style><h1>Stage 3 â€” current cinematics</h1><p>Cole / Normal. Recorded from the running D: BOF build with game audio, without skipping dialogue. Includes the lead-in radio scene, Stage 3 card and fly-in, and the full HQ/prototype sequence after Stage 3.</p><video id="v" controls preload="metadata" src="stage3-cinematics.mp4" poster="hq-frame-1.png"></video><p>'''+buttons+'''</p><p>These are native cinematic checkpoints. No game code was changed and this is not a campaign playthrough.</p><p><a href="stage3-cinematics.mp4">Open the complete recording</a></p></html>''',encoding='utf-8')
print(json.dumps({'combined':report['combined'],'chapters':chapters,'errors':report['errors']},indent=2),flush=True)
