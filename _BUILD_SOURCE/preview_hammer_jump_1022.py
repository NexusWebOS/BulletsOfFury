from pathlib import Path
from PIL import Image,ImageDraw
import json
W=Path(__file__).resolve().parents[1]/'_ART_SOURCES/hammer_jump_1022' if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(__file__).parent/'BOF-Hammer-Jump-1022';A=json.loads((W/'hammer_jump_art_1022.js').read_text(encoding='utf-8').split('const HJ22_ART=')[1].rstrip(';\n'))
cache={}
def frame(a):
 p=W/'shipping'/Path(A['sheets'][a['sheet']]['path']).name
 if str(p) not in cache:cache[str(p)]=Image.open(p).convert('RGBA')
 x,y,w,h=a['cell'];return cache[str(p)].crop((x,y,x+w,y+h))
for bank in ['blue_jump','corrupt_jump']:
 rows=A['banks'][bank];out=[];contact=Image.new('RGB',(512*5,560*((len(rows)+4)//5)),'#14202d');g=ImageDraw.Draw(contact)
 for i,a in enumerate(rows):
  im=frame(a);c=Image.new('RGB',(640,640),'#111b29');at=(320-a['pivot'][0],280-a['pivot'][1]);c.paste(im,at,im);out.append(c)
  x=i%5*512;y=i//5*560;contact.paste(im,(x,y),im);g.text((x+5,y+520),str(i),fill='white');px=x+a['tip'][0];py=y+a['tip'][1];g.ellipse((px-4,py-4,px+4,py+4),outline='red',width=2);px=x+a['glow'][0];py=y+a['glow'][1];g.ellipse((px-4,py-4,px+4,py+4),outline='lime',width=2)
 durations=[90]*len(rows)
 if bank.endswith('jump'):
  M=A['phases']['blue' if bank.startswith('blue') else 'corrupt'];durations[M['windEnd']]=250;durations[M['strikeEnd']]=300
 out[0].save(W/(bank+'.gif'),save_all=True,append_images=out[1:],duration=durations,loop=0,disposal=2);contact.save(W/(bank+'-contact.png'))
html='''<!doctype html><meta charset="utf-8"><title>Hammer jumping windups and double swings</title><style>body{background:#101821;color:#def;font:17px system-ui;margin:24px}canvas{image-rendering:pixelated;max-width:95vw}button,input,select{font:inherit;margin:8px}</style><h1>Hammer jumping windups / Hama double</h1><p>Fixed authored frames. Red = contact; green = hammer light socket. Onion overlays are review tools.</p><select id="bank"></select><button id="play">Pause</button><input id="frame" type="range" min="0" value="0"><label><input id="onion" type="checkbox">Onion</label><span id="label"></span><br><canvas id="cv" width="640" height="640"></canvas><script src="hammer_jump_art_1022.js"></script><script>
const bank=document.querySelector('#bank'),slider=document.querySelector('#frame'),ctx=document.querySelector('canvas').getContext('2d'),cache={};let playing=true;
for(const k of Object.keys(HJ22_ART.banks)){const o=document.createElement('option');o.value=o.textContent=k;bank.append(o)}
function draw(){const rows=HJ22_ART.banks[bank.value],i=+slider.value,a=rows[i];slider.max=rows.length-1;ctx.fillStyle='#111b29';ctx.fillRect(0,0,640,640);ctx.imageSmoothingEnabled=false;
function cell(n,alpha){const a=rows[(n+rows.length)%rows.length],s=HJ22_ART.sheets[a.sheet];let im=cache[a.sheet];if(!im){im=cache[a.sheet]=new Image();im.src='shipping/'+s.path.split('/').pop();im.onload=draw}if(!im.complete||!im.naturalWidth)return;ctx.globalAlpha=alpha;ctx.drawImage(im,...a.cell,320-a.pivot[0],280-a.pivot[1],a.w,a.h)}
if(document.querySelector('#onion').checked){cell(i-1,.18);cell(i+1,.18)}cell(i,1);ctx.globalAlpha=1;for(const[p,color]of [[a.tip,'red'],[a.glow,'lime']])if(p){ctx.strokeStyle=color;ctx.beginPath();ctx.arc(320-a.pivot[0]+p[0],280-a.pivot[1]+p[1],5,0,Math.PI*2);ctx.stroke()}document.querySelector('#label').textContent=i+' / '+(rows.length-1)}
bank.onchange=()=>{slider.value=0;draw()};slider.oninput=draw;document.querySelector('#onion').onchange=draw;document.querySelector('#play').onclick=e=>{playing=!playing;e.target.textContent=playing?'Pause':'Play'};setInterval(()=>{if(playing){slider.value=(+slider.value+1)%HJ22_ART.banks[bank.value].length;draw()}},100);draw();</script>'''
(W/'review.html').write_text(html,encoding='utf-8');print('Saved motion GIFs, socket contact sheets and interactive onion review.')
