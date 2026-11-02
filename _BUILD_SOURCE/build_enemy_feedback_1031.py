"""Matching short muzzle/exhaust reels, all from existing authored sources."""
from pathlib import Path
import json,math,sys,base64,hashlib
import numpy as np
from PIL import Image
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import serve,TRAP_RAF
O=R/'assets/game/shared/combat/enemy_flight_1031/feedback';O.mkdir(exist_ok=True);S=R/'_BUILD_SOURCE/enemy_flight_1031/feedback_sources';S.mkdir(exist_ok=True)
def data(f,n):return json.JSONDecoder().raw_decode((R/f).read_text(encoding='utf-8').split('const '+n+'=',1)[1])[0]
AF=data('assets/stage1_amplify_art_1031.js','S1A_ART');BF=data('assets/biome_fleet_art_1022.js','BF22_ART');CP=data('assets/pressure_art_1022.js','CP22_ART');meta={'owner':'_BUILD_SOURCE/build_enemy_feedback_1031.py','banks':{}}
port,stop=serve(str(R))
try:
 with sync_playwright()as pw:
  b=pw.chromium.launch(channel='msedge',headless=True);p=b.new_page();p.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load',timeout=180000);p.evaluate(TRAP_RAF);keys=['bpfx_muzzle_void_'+str(i)for i in range(8)];p.evaluate('(keys)=>keys.forEach(k=>XART.rdy(k))',keys);p.wait_for_function('(keys)=>keys.every(k=>XART.rdy(k))',arg=keys)
  for key in keys:
   s=p.evaluate('(k)=>{const im=XART.get(k),c=document.createElement("canvas");c.width=im.naturalWidth||im.width;c.height=im.naturalHeight||im.height;c.getContext("2d").drawImage(im,0,0);return c.toDataURL().split(",")[1]}',key);(S/(key+'.png')).write_bytes(base64.b64decode(s))
  b.close()
finally:stop()
def bank(name,frames):
 cell=96;side=max(max(t.size)for t in frames);k=76/side;fs=[]
 for t in frames:
  t=t.resize((round(t.width*k),round(t.height*k)),Image.Resampling.NEAREST);p=Image.new('RGBA',(cell,cell));p.alpha_composite(t,((cell-t.width)//2,(cell-t.height)//2));fs.append(p)
 out=Image.new('RGBA',(cell*32,cell*len(fs)))
 for f,t in enumerate(fs):
  for d in range(32):out.alpha_composite(t.rotate(-d*360/32,Image.Resampling.NEAREST),(d*cell,f*cell))
 p=O/(name+'.webp');out.save(p,format='WEBP',lossless=True,method=4);meta['banks'][name]={'key':'r46_fx_'+name,'path':p.relative_to(R).as_posix(),'cell':cell,'dirs':32,'frames':len(fs),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
bank('void_muzzle',[Image.open(S/('bpfx_muzzle_void_'+str(i)+'.png')).convert('RGBA')for i in range(8)])
for name,B in [('sky_muzzle',BF['effects']['sky_muzzle']),('water_muzzle',BF['effects']['water_muzzle']),('toxic_muzzle',CP['effects']['toxic_muzzle'])]:
 im=Image.open(R/B['path']).convert('RGBA');bank(name,[im.crop((x,y,x+w,y+h))for x,y,w,h in B['cells']])
B=AF['thruster'];im=Image.open(R/B['path']).convert('RGBA');frames=[im.crop((0,f*B['cell'],B['cell'],(f+1)*B['cell']))for f in range(B['frames'])]
for stage,color in [(4,[88,177,255]),(5,[166,92,242]),(6,[74,229,194]),(7,[108,230,50]),(8,[235,65,180]),(9,[72,204,255])]:
 fs=[];target=np.array(color,dtype=float);target/=target@[.2126,.7152,.0722]
 for t in frames:
  a=np.array(t);rgb=a[:,:,:3].astype(float);hi=rgb.max(2);lo=rgb.min(2);l=rgb@[.2126,.7152,.0722];mask=(hi-lo>30)&(a[:,:,3]>0);a[:,:,:3][mask]=np.minimum(255,l[:,:,None]*target)[mask].astype('uint8');fs.append(Image.fromarray(a))
 bank('exhaust'+str(stage),fs)
(O/'manifest.json').write_text(json.dumps(meta,indent=2)+'\n',encoding='utf-8');(R/'assets/enemy_feedback_art_1031.js').write_text('"use strict";\nconst R46_FEEDBACK='+json.dumps(meta,separators=(',',':'))+';\n',encoding='utf-8',newline='\n');print('Exported',len(meta['banks']),'matching feedback banks')
