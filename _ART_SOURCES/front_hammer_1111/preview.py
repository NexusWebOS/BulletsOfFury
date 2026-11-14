from pathlib import Path
import json,base64,io
from PIL import Image,ImageDraw
W=Path(__file__).resolve().parent;E=W/'exports';OLD=W.parent/'heavy_hammer_1111';O=W.parents[1]/'outputs/Front-facing-hammer';C=512
M=json.loads((W/'manifest.json').read_text())
for move in ['overhead','sides','right']:
 fs=[];count=M['blue-'+move]['count']
 for i in range(count):
  out=Image.new('RGBA',(1024,1056),'#101820');d=ImageDraw.Draw(out)
  for col,n,label in [(0,'blue','CHRONOS'),(1,'corrupt','DRACODIA')]:
   for row,mat in [(0,'regular'),(1,'chrome')]:
    sheet=Image.open(E/(n+'-'+move+'_'+mat+'.webp')).convert('RGBA');f=sheet.crop((i%4*C,i//4*C,(i%4+1)*C,(i//4+1)*C));out.alpha_composite(f,(col*C,32+row*C));d.text((col*C+12,row*C+12),label+' / '+('CHROMIUM'if mat=='chrome'else'NORMAL'),fill='white')
  fs.append(out.convert('RGB'))
 durations=([30]*8+[55]*8+[60,55,45,40,35,30,100,65]+[50]*8)if move=='overhead'else[55]*16
 fs[0].save(O/('both-forms-'+('front'if move=='overhead'else move)+'.gif'),save_all=True,append_images=fs[1:],duration=durations,loop=0,disposal=2)
 fs[22 if move=='overhead'else 6].save(O/('normal-chromium-'+move+'.png'))
data={}
for n,a in M.items():
 data[n]=dict(count=a['count'],sheets={})
 for mat in ['regular','chrome','red']:
  path=(OLD if n.endswith('whirl')else W)/'exports'/(n+'_'+mat+'.webp');data[n]['sheets'][mat]='data:image/webp;base64,'+base64.b64encode(path.read_bytes()).decode()
page='''<!doctype html><meta charset="utf-8"><title>Forward-facing hammer attacks</title><style>body{margin:0;background:#101820;color:#eaf5ff;font:17px system-ui}main{max-width:1100px;margin:auto;padding:24px}h1{font-size:25px}button,select,input{font:inherit;margin:6px;padding:8px}.grid{display:grid;grid-template-columns:1fr 1fr}figure{margin:0;text-align:center}canvas{width:100%;image-rendering:pixelated}p{color:#abc3d1}</style><main><h1>Forward-facing hammer attacks — both forms</h1><select id="move"><option value="overhead">Overhead strike</option><option value="sides">Left side strike</option><option value="right">Right side strike</option><option value="whirl">Whirlwind</option></select><select id="mat"><option value="both">Normal + Chromium</option><option value="red">Red hammer state</option></select><button id="play">Pause</button><select id="speed"><option value="1">Normal speed</option><option value="0.5">Half speed</option><option value="0.25">Quarter speed</option></select><input id="scrub" type="range" min="0" max="31"><span id="counter"></span><div class="grid"><figure>CHRONOS — NORMAL<canvas id="b0" width="512" height="512"></canvas></figure><figure>DRACODIA — NORMAL<canvas id="d0" width="512" height="512"></canvas></figure><figure>CHRONOS — CHROMIUM<canvas id="b1" width="512" height="512"></canvas></figure><figure>DRACODIA — CHROMIUM<canvas id="d1" width="512" height="512"></canvas></figure></div><p>Pause or scrub to inspect the complete drawings. In-game recordings include the actual armor states, hits and recovery.</p></main><script>const data=DATA,ims={};let f=0,last=0,playing=true;const move=document.querySelector('#move'),mat=document.querySelector('#mat'),speed=document.querySelector('#speed'),slider=document.querySelector('#scrub'),play=document.querySelector('#play');for(const[n,a]of Object.entries(data)){ims[n]={};for(const[m,src]of Object.entries(a.sheets)){const im=new Image();ims[n][m]=im;im.onload=()=>render();im.src=src;}}function render(){const n=data['blue-'+move.value].count;f=Math.min(f,n-1);slider.max=n-1;slider.value=f;document.querySelector('#counter').textContent=(f+1)+' / '+n;for(const[id,unit,m]of[['b0','blue','regular'],['d0','corrupt','regular'],['b1','blue','chrome'],['d1','corrupt','chrome']]){const c=document.getElementById(id),g=c.getContext('2d');g.imageSmoothingEnabled=false;g.clearRect(0,0,512,512);const image=ims[unit+'-'+move.value]?.[mat.value==='red'?'red':m];if(image?.complete&&image.naturalWidth)g.drawImage(image,f%4*512,Math.floor(f/4)*512,512,512,0,0,512,512);}}move.onchange=()=>{f=0;render()};mat.onchange=render;slider.oninput=()=>{f=+slider.value;render()};play.onclick=()=>{playing=!playing;play.textContent=playing?'Pause':'Play'};function tick(t){const d=move.value==='overhead'?[...Array(8).fill(30),...Array(8).fill(55),60,55,45,40,35,30,100,65,...Array(8).fill(50)]:Array(16).fill(55);if(playing&&t-last>d[f]/+speed.value){f=(f+1)%d.length;render();last=t}requestAnimationFrame(tick)}render();requestAnimationFrame(tick);</script>'''.replace('DATA',json.dumps(data,separators=(',',':')))
(O/'playback.html').write_text(page,encoding='utf8')
print('Saved normal/Chromium paired previews and interactive frame player.',flush=True)
