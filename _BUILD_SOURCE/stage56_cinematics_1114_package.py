from pathlib import Path
import json,subprocess,re,hashlib
from PIL import Image,ImageDraw
import imageio_ffmpeg
ROOT=Path('D:/BOF-Downloads/2026-11-14/RevG-source');OUT=ROOT/'_shots/stage56_cinematics_1114';ENC=OUT/'encoded';ENC.mkdir(exist_ok=True);FF=imageio_ffmpeg.get_ffmpeg_exe()
q=json.loads((OUT/'recording.json').read_text(encoding='utf8'));assert len(q['clips'])==2 and not q['errors'];assert q['coreBefore']==q['coreAfter'];a,b=q['clips'];c=b;assert[a['part'],b['part']]==['chronos','hq5']
def run(args):
 r=subprocess.run([FF,'-hide_banner','-loglevel','error','-y',*args],capture_output=True,text=True);assert r.returncode==0 and not r.stderr,r.stderr

def duration(path):
 r=subprocess.run([FF,'-hide_banner','-i',str(path)],capture_output=True,text=True);m=re.search(r'Duration: (\d+):(\d+):([\d.]+)',r.stderr);assert m,r.stderr;return int(m[1])*3600+int(m[2])*60+float(m[3])
def event(clip,needle,default=None):
 v=next((x['at']for x in clip['stages']if needle in x['tag']),default)
 if v is None:raise ValueError('Missing native chapter event '+needle)
 return v
codec=['-vf','fps=30','-fps_mode','cfr','-c:v','libx264','-preset','fast','-crf','21','-pix_fmt','yuv420p','-threads','2','-af','aresample=async=1:first_pts=0','-c:a','aac','-b:a','160k']
for clip in q['clips']:
 print('Encoding '+clip['part'],flush=True);run(['-i',str(OUT/'films'/(clip['part']+'.webm')),*(['-t',str(clip['presentationEnd'])]if clip.get('presentationEnd')else[]),*codec,str(ENC/(clip['part']+'.mp4'))])
off1=duration(ENC/'chronos.mp4');off2=off1;total=off1+duration(ENC/'hq5.mp4')
chapters=[{'start':0,'title':'Chronos — last words'},{'start':event(a,':lock:'),'title':'Core lock and final missile'},{'start':event(a,':engulf:'),'title':'Chromium ignition and breakup'},{'start':event(a,':overhead:'),'title':'Orbital aftermath'},{'start':event(a,':welcome:'),'title':'Team radio and return to Earth'},{'start':off1,'title':'Fury HQ — bringing the chaingun home'},{'start':off1+event(b,':B505:'),'title':'Incoming contacts — emergency scramble'},{'start':off2+event(c,'intro:'),'title':'Stage 6 — card and flight in'},{'start':off2+event(c,':cloak:1'),'title':'Stage 6 — stealth ambush'}]
chapters=sorted(chapters,key=lambda x:x['start']);meta=';FFMETADATA1\ntitle=Bullets of Fury - Full Stage 5 to 6 cinematics\n'
for i,ch in enumerate(chapters):meta+='[CHAPTER]\nTIMEBASE=1/1000\nSTART='+str(round(ch['start']*1000))+'\nEND='+str(round((chapters[i+1]['start']if i+1<len(chapters)else total)*1000))+'\ntitle='+ch['title']+'\n'
(OUT/'chapters.ffmeta').write_text(meta,encoding='utf8');(ENC/'concat.txt').write_text("file 'chronos.mp4'\nfile 'hq5.mp4'\n",encoding='utf8')
movie=OUT/'stage5-to-6-full-cinematics.mp4';run(['-f','concat','-safe','0','-i',str(ENC/'concat.txt'),'-f','ffmetadata','-i',str(OUT/'chapters.ffmeta'),'-map','0:v:0','-map','0:a:0','-map_metadata','1','-map_chapters','1','-c','copy','-movflags','+faststart',str(movie)]);run(['-i',str(movie),'-f','null','-'])
v=subprocess.run([FF,'-hide_banner','-i',str(movie),'-af','volumedetect','-vn','-f','null','-'],capture_output=True,text=True);audio=[x.strip()for x in v.stderr.splitlines()if'mean_volume:'in x or'max_volume:'in x]
points=[(event(a,':drain:')+1.8,'Chronos last words'),(event(a,':engulf:')+3.2,'Chromium breakup'),(event(a,':aftermath:')+2,'Monochrome aftermath'),(off1+3,'Fury HQ'),(off1+event(b,':B505:')+2,'Emergency contacts'),(off2+event(c,':cloak:1')+3.5,'Stage6 approach')]
contact=Image.new('RGB',(1440,588),'#0b1420');d=ImageDraw.Draw(contact)
for i,(t,label)in enumerate(points):
 f=OUT/('frame-'+str(i)+'.png');run(['-ss',str(t),'-i',str(movie),'-frames:v','1',str(f)]);im=Image.open(f).convert('RGB');im.thumbnail((480,270));x=i%3*480;y=i//3*294;contact.paste(im,(x+(480-im.width)//2,y));d.text((x+8,y+272),label,fill='#eee4c7')
contact.save(OUT/'contact-sheet.jpg',quality=94)
q['combined']={'file':movie.name,'duration':duration(movie),'chapters':chapters,'sha256':hashlib.sha256(movie.read_bytes()).hexdigest(),'decodeErrors':[],'audio':audio};(OUT/'recording.json').write_text(json.dumps(q,indent=2),encoding='utf8')
buttons=''.join('<button data-time="'+str(ch['start'])+'">'+ch['title']+'</button>'for ch in chapters)
html='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>BOF — Full Stage5 to6 cinematics</title><style>body{max-width:1200px;margin:30px auto;padding:0 20px;background:#09131f;color:#f1e8ce;font:17px/1.55 system-ui}p{color:#b7c8db}video,img{width:100%;background:#02060b;border:1px solid #405c73;border-radius:7px}button{padding:9px 13px;margin:4px;background:#20374b;color:#f4eacb;border:1px solid #52778f;border-radius:5px;font:inherit;cursor:pointer}a{color:#72ddce}small{color:#9fb4ca}</style><h1>Stage 5 → 6 — the full cinematic sequence</h1><p>Chronos’s native last words, core shot and breakup; orbital aftermath and return to Earth; the complete Fury HQ homecoming and emergency scramble; Stage6’s card, flight in and stealth ambush.</p><video id="movie" controls preload="metadata" src="stage5-to-6-full-cinematics.mp4" poster="frame-0.png"></video><p>__BUTTONS__</p><p><small>Cole / Hard, with native game audio. Full cinematic checkpoints with no dialogue skipped. The result/equipment menus between the two checkpoints are omitted; HQ to Stage6 is one continuous native capture. Ends at the first interactive missile interception in Stage6. This is not a campaign playthrough. Hard uses the Stage6 continuation story branch.</small></p><p><a download href="stage5-to-6-full-cinematics.mp4">Download recording</a> · <a href="../../docs/STAGE56_CINEMATICS_1114.md">Recording notes</a></p><img src="contact-sheet.jpg" alt="Verified native frames from Chronos farewell through Stage6"><script>const v=document.getElementById('movie');document.querySelectorAll('button').forEach(b=>b.onclick=async()=>{v.currentTime=Number(b.dataset.time);try{await v.play()}catch(e){if(e.name!=='AbortError')throw e}});</script></html>'''
(OUT/'review.html').write_text(html.replace('__BUTTONS__',buttons),encoding='utf8');print(json.dumps(q['combined'],indent=2),flush=True)
