from pathlib import Path
import json,hashlib,zipfile,subprocess,shutil,html
import numpy as np
from PIL import Image,ImageDraw
import imageio_ffmpeg
W=Path(__file__).resolve().parent;O=W.parents[1]/'outputs/Heavy-hammer-motion';E=W/'exports';C=512
manifest=json.loads((W/'manifest.json').read_text())
for family in ['overhead','sides','whirl']:
 frames=[];count=manifest['blue-'+family]['count']
 for i in range(count):
  board=Image.new('RGB',(C*2,C+32),'#101820');d=ImageDraw.Draw(board)
  for j,(n,label)in enumerate([('blue','CHRONOS'),('corrupt','DRACODIA / CHRONOS FORM')]):
   f=Image.open(E/(n+'-'+family)/f'{i:02}.png').convert('RGBA');board.paste(f,(j*C,32),f);d.text((j*C+20,12),label,fill='white')
  frames.append(board)
 duration=([30]*8+[55]*8+[60,55,45,40,35,30,100,65]+[50]*8)if family=='overhead'else[55]*count
 frames[0].save(O/('both-'+family+'.gif'),save_all=True,append_images=frames[1:],duration=duration,loop=0,disposal=2)
# A lossless, self-contained playback page uses whole exported source frames.
assets={n:[Image.open(E/n/f'{i:02}.png')for i in range(a['count'])]for n,a in manifest.items()}
import base64,io
encoded={}
for n,frames in assets.items():
 encoded[n]=[]
 for f in frames:
  b=io.BytesIO();f.save(b,format='PNG');encoded[n].append('data:image/png;base64,'+base64.b64encode(b.getvalue()).decode())
page='''<!doctype html><meta charset="utf-8"><title>Heavy hammer motion — both forms</title><style>body{margin:0;background:#101820;color:#eef8ff;font:18px system-ui}main{max-width:1100px;margin:auto;padding:24px}h1{font-size:26px}button,select,input{font:inherit;margin:8px;padding:8px}section{display:flex;gap:12px}article{width:50%;text-align:center}img{width:100%;image-rendering:pixelated}p{color:#aac4d2}</style><main><h1>Heavy hammer motion — both forms</h1><select id="move"><option value="overhead">Overhead strike</option><option value="sides">Left side strike</option><option value="right">Right side strike</option><option value="whirl">Whirlwind turn</option></select><button id="play">Pause</button><select id="speed"><option value="1">Normal speed</option><option value="0.5">Half speed</option><option value="0.25">Quarter speed</option></select><input type="range" id="scrub" min="0" max="31" value="0"><span id="counter"></span><section><article>CHRONOS<img id="blue"></article><article>DRACODIA / CHRONOS FORM<img id="corrupt"></article></section><p>Complete exported drawings. The overhead cycle includes a planted impact hold. Side swings include a contact hold; right swings mirror the complete drawing. Native game recordings are supplied separately.</p></main><script>const assets=ASSETS;let f=0,playing=true,last=0;const move=document.querySelector('#move'),speed=document.querySelector('#speed'),slider=document.querySelector('#scrub'),play=document.querySelector('#play');function render(){const n=assets['blue-'+move.value].length;f=Math.min(f,n-1);slider.max=n-1;slider.value=f;document.querySelector('#blue').src=assets['blue-'+move.value][f];document.querySelector('#corrupt').src=assets['corrupt-'+move.value][f];document.querySelector('#counter').textContent=(f+1)+' / '+n;}move.onchange=()=>{f=0;render()};slider.oninput=()=>{f=+slider.value;render()};play.onclick=()=>{playing=!playing;play.textContent=playing?'Pause':'Play'};function tick(t){const durations=move.value==='overhead'?[...Array(8).fill(30),...Array(8).fill(55),60,55,45,40,35,30,100,65,...Array(8).fill(50)]:Array(16).fill(55);if(playing&&t-last>durations[f]/+speed.value){f=(f+1)%durations.length;render();last=t}requestAnimationFrame(tick)}render();requestAnimationFrame(tick);</script>'''.replace('ASSETS',json.dumps(encoded,separators=(',',':')))
(O/'playback.html').write_text(page,encoding='utf8')
accepted={
 'guided-drac-o0':list(range(8)),'guided-drac-o1-alpha':list(range(8)),'guided-drac-o2':list(range(7)),
 'guided-drac-o3':list(range(5)),'guided-drac-o3-grip':[5,6,7],
 'guided-blue-o0':list(range(8)),'guided-blue-o1':list(range(8)),'guided-blue-o2':list(range(7)),
 'guided-blue-o3-right':list(range(5)),'guided-blue-o3-rejected':[5,6,7],
 'drac-side-T':[i for i in range(16)if i!=8],'blue-side-T':[i for i in range(16)if i!=8],
 'drac-whirl':list(range(16)),'blue-whirl':list(range(16))}
for name,cells in accepted.items():
 p=W/'jobs'/(name+'.json');j=json.loads(p.read_text());j.update(accepted=True,status='accepted-selected-complete-cells',selectedCells=cells);p.write_text(json.dumps(j,indent=2))
# Native film review: contact, sides and actual turning at several engine times.
ff=imageio_ffmpeg.get_ffmpeg_exe()
for unit in ['chronos','dracodia']:
 board=Image.new('RGB',(640*4,400*3),'#101820');d=ImageDraw.Draw(board)
 times=[.3,.8,1.2,1.6,2.0,2.4,2.8,3.2,17.8,18.1,18.4,18.7]
 for j,t in enumerate(times):
  p=W/'reviews'/f'{unit}-live-{j:02}.png';subprocess.run([ff,'-v','error','-y','-ss',str(t),'-i',str(O/(unit+'-hammer.mp4')),'-frames:v','1','-vf','scale=640:422:flags=neighbor',str(p)],check=True)
  im=Image.open(p).convert('RGB');board.paste(im.crop((0,0,640,400)),(j%4*640,j//4*400));d.text((j%4*640+8,j//4*400+8),str(t)+'s',fill='white')
 board.save(O/(unit+'-native-review.png'))
print('Created paired GIFs, frame playback, selected-source provenance and native film review boards.')
