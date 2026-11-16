from pathlib import Path
from PIL import Image,ImageDraw
import json,subprocess,re,hashlib
import imageio_ffmpeg
ROOT=Path('D:/BOF-Downloads/2026-11-14/RevG-source');OUT=ROOT/'_shots/kit_dialogue_1114';ENC=OUT/'encoded';ENC.mkdir(exist_ok=True);FF=imageio_ffmpeg.get_ffmpeg_exe()
q=json.loads((OUT/'recording.json').read_text(encoding='utf-8'));assert len(q['clips'])==2 and not q['errors'];a,b=q['clips'];assert a['part']=='post4'and b['part']=='arrival5'and b['end']['gravityReady']
assert all(any(':'+phase+':'in e['tag']for e in b['stages'])for phase in ['assembly','countdown'])
def run(args):
 r=subprocess.run([FF,'-hide_banner','-loglevel','error','-y',*args],capture_output=True,text=True);assert r.returncode==0 and not r.stderr,r.stderr
def duration(path):
 r=subprocess.run([FF,'-hide_banner','-i',str(path)],capture_output=True,text=True);m=re.search(r'Duration: (\d+):(\d+):([\d.]+)',r.stderr);assert m,r.stderr;return int(m[1])*3600+int(m[2])*60+float(m[3])
def event(c,needle):return next(e['at']for e in c['stages']if needle in e['tag'])
codec=['-vf','fps=30','-fps_mode','cfr','-c:v','libx264','-preset','fast','-crf','21','-pix_fmt','yuv420p','-threads','2','-af','aresample=async=1:first_pts=0','-c:a','aac','-b:a','160k']
for c in q['clips']:
 print('Encoding '+c['part'],flush=True);run(['-i',str(OUT/'films'/(c['part']+'.webm')),*codec,str(ENC/(c['part']+'.mp4'))])
split=duration(ENC/'post4.mp4');total=split+duration(ENC/'arrival5.mp4')
chapters=[{'start':0,'title':'The prototype kit is in separate pieces'},{'start':event(a,'POST4-02'),'title':'How the pieces bind during ascent'},{'start':event(a,'B403'),'title':'Animated code-only satellite corruption'},{'start':event(a,'POST4-07'),'title':'Awaiting your orders'},{'start':event(a,'POST4-10'),'title':'Original aircraft departure'},{'start':split,'title':'Stage 5 ascent'},{'start':split+event(b,':assembly:'),'title':'Cole’s twelve-piece kit assembly'},{'start':split+event(b,':countdown:'),'title':'Space launch'}]
chapters.sort(key=lambda c:c['start']);meta=';FFMETADATA1\ntitle=Bullets of Fury - Prototype dispatch and Stage 4 to 5\n'
for i,c in enumerate(chapters):meta+='[CHAPTER]\nTIMEBASE=1/1000\nSTART='+str(round(c['start']*1000))+'\nEND='+str(round((chapters[i+1]['start']if i+1<len(chapters)else total)*1000))+'\ntitle='+c['title']+'\n'
(OUT/'chapters.ffmeta').write_text(meta,encoding='utf-8');(ENC/'concat.txt').write_text("file 'post4.mp4'\nfile 'arrival5.mp4'\n",encoding='utf-8')
movie=OUT/'stage4-to-5-code-and-kit.mp4';run(['-f','concat','-safe','0','-i',str(ENC/'concat.txt'),'-f','ffmetadata','-i',str(OUT/'chapters.ffmeta'),'-map','0:v:0','-map','0:a:0','-map_metadata','1','-map_chapters','1','-c','copy','-movflags','+faststart',str(movie)]);run(['-i',str(movie),'-f','null','-'])
v=subprocess.run([FF,'-hide_banner','-i',str(movie),'-af','volumedetect','-vn','-f','null','-'],capture_output=True,text=True);audio=[s.strip()for s in v.stderr.splitlines()if 'mean_volume:'in s or 'max_volume:'in s]
points=[(2,'Kit discovery'),(event(a,'POST4-02')+2,'The binding technology'),(event(a,'B403')+2,'Code-only satellite animation'),(event(a,'POST4-07')+2,'Awaiting orders'),(event(a,'POST4-10')+2,'Original unconverted aircraft'),(split+event(b,':assembly:')+2,'Native kit assembly')]
contact=Image.new('RGB',(1440,588),'#0b1420');d=ImageDraw.Draw(contact)
for i,(t,label)in enumerate(points):
 file=OUT/('frame-'+str(i)+'.png');run(['-ss',str(t),'-i',str(movie),'-frames:v','1',str(file)]);im=Image.open(file).convert('RGB');im.thumbnail((480,270));x=i%3*480;y=i//3*294;contact.paste(im,(x+(480-im.width)//2,y));d.text((x+8,y+272),label,fill='#eee4c7')
contact.save(OUT/'contact-sheet.jpg',quality=94)
q['combined']={'file':movie.name,'duration':duration(movie),'chapters':chapters,'sha256':hashlib.sha256(movie.read_bytes()).hexdigest(),'decodeErrors':[],'audio':audio};(OUT/'recording.json').write_text(json.dumps(q,indent=2),encoding='utf-8')
buttons=''.join('<button data-time="'+str(c['start'])+'">'+c['title']+'</button>'for c in chapters)
html='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>BOF — Prototype dispatch</title><style>body{max-width:1200px;margin:30px auto;padding:0 20px;background:#09131f;color:#f1e8ce;font:17px/1.55 system-ui}p{color:#b7c8db}video,img{width:100%;background:#02060b;border:1px solid #405c73;border-radius:7px}button{padding:9px 13px;margin:4px;background:#20374b;color:#f4eacb;border:1px solid #52778f;border-radius:5px;font:inherit;cursor:pointer}a{color:#72ddce}small{color:#9fb4ca}</style><h1>Stage 4 → 5 — prototype dispatch</h1><p>The kit is discovered in separate pieces. Decker explains its binding technology; Cole fills in when Decker is the flying pilot. The satellite corrupts through sixteen frames of purple alien code, with no creature form. Departure uses the actual unconverted aircraft with animated exhaust. Metal dialogue uses fixed-ratio plates and framed selection avatars.</p><video id="movie" controls preload="metadata" src="stage4-to-5-code-and-kit.mp4" poster="frame-4.png"></video><p>__BUTTONS__</p><p><small>Cole / Normal. Native cinematic checkpoints, without dialogue skips, through the full original Stage 5 kit assembly and gameplay handoff. Gameplay between scenes is omitted; this is not a campaign playthrough.</small></p><p><a download href="stage4-to-5-code-and-kit.mp4">Download recording</a> · <a href="../../docs/KIT_DIALOGUE_1114.md">Change notes</a> · <a href="../../docs/KIT_DIALOGUE_ART_1114.json">Generated art and prompt</a></p><img src="contact-sheet.jpg" alt="Checked frames from the updated kit discovery and ascent"><script>const v=document.getElementById('movie');document.querySelectorAll('button').forEach(b=>b.onclick=async()=>{v.currentTime=Number(b.dataset.time);try{await v.play()}catch(e){if(e.name!=='AbortError')throw e}});</script></html>'''
(OUT/'review.html').write_text(html.replace('__BUTTONS__',buttons),encoding='utf-8');print(json.dumps(q['combined'],indent=2),flush=True)
