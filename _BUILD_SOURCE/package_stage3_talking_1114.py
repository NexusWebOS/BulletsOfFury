from pathlib import Path
from PIL import Image,ImageDraw
import subprocess,json,re,hashlib
import imageio_ffmpeg
ROOT=Path('D:/BOF-Downloads/2026-11-14/RevG-source');OUT=ROOT/'_shots/stage3_talking_1114';FF=imageio_ffmpeg.get_ffmpeg_exe()
report=json.loads((OUT/'recording.json').read_text(encoding='utf-8'))
assert len(report['clips'])==3 and not report['errors']
assert all(c['peak']>.001 and not c['errors']for c in report['clips'])
ENC=OUT/'encoded';ENC.mkdir(exist_ok=True)
def run(args):
 r=subprocess.run([FF,'-hide_banner','-loglevel','error','-y',*args],capture_output=True,text=True)
 assert r.returncode==0 and not r.stderr,r.stderr
def info(path):
 r=subprocess.run([FF,'-hide_banner','-i',str(path)],capture_output=True,text=True)
 m=re.search(r'Duration: (\d+):(\d+):([\d.]+)',r.stderr);assert m,r.stderr
 return int(m[1])*3600+int(m[2])*60+float(m[3])
def event(c,needle):return next(s['at']for s in c['stages']if needle in s['tag'])
chapters=[];segments=[];offset=0
names={'lead-in':'Service data-link, charge-up and lift-off','arrival':'Stage 3 card and fly-in','hq':'Stage 3 aftermath — Fury HQ'}
codec=['-vf','fps=30','-fps_mode','cfr','-c:v','libx264','-preset','fast','-crf','21','-pix_fmt','yuv420p','-threads','2','-af','aresample=async=1:first_pts=0','-c:a','aac','-b:a','160k']
for c in report['clips']:
 part=c['part'];target=ENC/(part+'.mp4');print('Encoding '+part,flush=True)
 run(['-i',str(OUT/(part+'.webm')),*codec,str(target)])
 duration=info(target);segments.append({'part':part,'start':offset,'duration':duration,'title':names[part]})
 chapters.append({'start':round(offset,3),'title':names[part]})
 if part=='lead-in':
  for shot,title in [('SL2-06','Top-down heat charge'),('SL2-09','Lift-off'),('stagesel','Return to the campaign map')]:chapters.append({'start':round(offset+event(c,shot),3),'title':title})
 if part=='hq':chapters.append({'start':round(offset+event(c,'POST3-13'),3),'title':"Decker’s workshop and Photon Cannon prototype"})
 offset+=duration
chapters.sort(key=lambda q:q['start'])
(ENC/'concat.txt').write_text('\n'.join("file '"+c['part']+".mp4'"for c in report['clips']),encoding='utf-8')
meta=';FFMETADATA1\ntitle=Bullets of Fury - Stage 3 updated cinematic reel\n'
for i,ch in enumerate(chapters):
 end=chapters[i+1]['start']if i+1<len(chapters)else offset
 meta+='[CHAPTER]\nTIMEBASE=1/1000\nSTART='+str(round(ch['start']*1000))+'\nEND='+str(round(end*1000))+'\ntitle='+ch['title']+'\n'
(OUT/'chapters.ffmeta').write_text(meta,encoding='utf-8')
movie=OUT/'stage3-full-cinematics.mp4'
run(['-f','concat','-safe','0','-i',str(ENC/'concat.txt'),'-f','ffmetadata','-i',str(OUT/'chapters.ffmeta'),'-map','0:v:0','-map','0:a:0','-map_metadata','1','-map_chapters','1','-c','copy','-movflags','+faststart',str(movie)])
run(['-i',str(movie),'-f','null','-'])
levels=subprocess.run([FF,'-hide_banner','-i',str(movie),'-af','volumedetect','-vn','-f','null','-'],capture_output=True,text=True)
audio=[q.strip()for q in levels.stderr.splitlines()if 'mean_volume:'in q or 'max_volume:'in q]
frames=[]
lead=report['clips'][0]
for needle,label,delay in [('SL2-01','Cole talking in his cockpit',1.2),('SL2-02','Decker restores the service data-link',1.4),('SL2-06','Top-down heat charge',2.6),('SL2-09','Lift-off and animated thrusters',1.3),('stagesel','Campaign map handoff',.7)]:frames.append({'time':event(lead,needle)+delay,'label':label})
frames.extend([{'time':segments[1]['start']+segments[1]['duration']*.65,'label':'Stage 3 fly-in'},{'time':segments[2]['start']+5,'label':'Fury HQ briefing'},{'time':next(q['start']for q in chapters if 'workshop'in q['title'])+7,'label':'Decker’s workshop'},{'time':segments[2]['start']+event(report['clips'][2],'POST3-16')+1.6,'label':'Photon Cannon prototype'}])
contact=Image.new('RGB',(1440,882),'#0c1520');draw=ImageDraw.Draw(contact)
for i,q in enumerate(frames):
 file=OUT/('frame-'+str(i)+'.png');run(['-ss',str(q['time']),'-i',str(movie),'-frames:v','1',str(file)])
 im=Image.open(file).convert('RGB');im.thumbnail((480,270));x=i%3*480;y=i//3*294
 contact.paste(im,(x+(480-im.width)//2,y));draw.text((x+8,y+272),q['label'],fill='#f2e7c8');q['file']=file.name
contact.save(OUT/'contact-sheet.jpg',quality=94)
report.update({'chapters':chapters,'segments':segments,'inspectionFrames':frames,'combined':{'file':movie.name,'duration':info(movie),'sha256':hashlib.sha256(movie.read_bytes()).hexdigest(),'bytes':movie.stat().st_size,'decodeErrors':[],'audio':audio},'nativeDialogueSkipped':False,'gameSourceChanged':False})
(OUT/'recording.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
buttons=''.join('<button data-time="'+str(c['start'])+'">'+c['title']+'</button>'for c in chapters)
html='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>BOF — Stage 3 complete cinematic reel</title><style>body{max-width:1200px;margin:30px auto;padding:0 20px;background:#0a111b;color:#f1e8ce;font:17px/1.55 system-ui}h1{margin-bottom:5px}p{color:#b9c9db}video{width:100%;background:#000;border:1px solid #3d586f;border-radius:6px}button{cursor:pointer;padding:10px 14px;margin:4px;border:1px solid #54718a;border-radius:5px;background:#203248;color:#fff2cf;font:inherit}a{color:#72ddd1}small{color:#a9bacd}img{width:100%}</style><h1>Stage 3 — the complete updated cinematic reel</h1><p>Cole / Normal. Fresh recordings with the new talking cockpit frames and native game audio. Includes the complete service data-link conversation, top-down heat charge, lift-off, map handoff, Stage 3 arrival and the full HQ/prototype scenes afterward.</p><video id="movie" controls preload="metadata" src="stage3-full-cinematics.mp4" poster="frame-0.png"></video><p>__BUTTONS__</p><p><small>Complete cinematic checkpoints played at native speed, without skipping dialogue. Gameplay between the arrival and HQ scenes is omitted; this is not a campaign playthrough.</small></p><p><a href="stage3-full-cinematics.mp4" download>Download the complete recording</a> · <a href="../cockpit_talk_1114/review.html">All nine talking pilots</a></p><img src="contact-sheet.jpg" alt="Nine checked frames from the new cinematic reel"><script>const v=document.getElementById('movie');document.querySelectorAll('button').forEach(b=>b.onclick=async()=>{v.currentTime=Number(b.dataset.time);try{await v.play()}catch(e){if(e.name!=='AbortError')throw e}});</script></html>'''
(OUT/'review.html').write_text(html.replace('__BUTTONS__',buttons),encoding='utf-8')
print(json.dumps({'combined':report['combined'],'chapters':chapters,'errors':report['errors']},indent=2),flush=True)
