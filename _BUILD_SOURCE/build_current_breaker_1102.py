"""Current Breaker: registered liquid actions/yaw, source-water flow and rollers.
All sheets have fixed even cells and common chest pivots. Other roster banks
are read only. Actual yaw views come from the selected ImageGen sheet.
"""
from pathlib import Path
import json,math,hashlib,sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'_shots/current_breaker_1102/deps'))
import numpy as np
import cv2
from PIL import Image,ImageDraw
from scipy.ndimage import label,maximum_filter
from pixel_glow_1015 import rings,RING_A
R=Path(__file__).resolve().parents[1];S=R/'_BUILD_SOURCE/current_breaker_1102';O=R/'assets/game/levels/stage_09/enemies/current_breaker_1102';Q=R/'_shots/current_breaker_1102'
for p in [S,O,Q]:p.mkdir(parents=True,exist_ok=True)
OLD=json.loads((R/'assets/game/levels/stage_09/enemies/amplify_1101/manifest.json').read_text());M={'owner':'_BUILD_SOURCE/build_current_breaker_1102.py','banks':{},'sources':{},'pivot':[192,192],'cell':384}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def clean(im):
 a=np.array(im.convert('RGBA'));ids,_=label(a[:,:,3]>55);counts=np.bincount(ids.ravel());keep=counts>=max(10,counts[1:].max()*.002);keep[0]=False;a[:,:,3]=np.where(keep[ids],255,0);a[:,:,:3][a[:,:,3]==0]=0;return Image.fromarray(a)
def norm(name,n,rows,anchors):
 p=S/(name+'_source.png');M['sources'][name]={'path':p.relative_to(R).as_posix(),'sha256':sha(p),'tool':'built-in image_gen','prompt':'_BUILD_SOURCE/current_breaker_1102/prompts.md'};im=Image.open(p);cols=n//rows
 ts=[clean(im.crop((round(i%cols*im.width/cols),round(i//cols*im.height/rows),round((i%cols+1)*im.width/cols),round((i//cols+1)*im.height/rows))))for i in range(n)]
 # One physical body unit for the entire bank; no per-pose silhouette fitting.
 k=236/max(t.getbbox()[3]-t.getbbox()[1] for t in ts);out=[]
 for t,p in zip(ts,anchors):
  v=t.resize((round(t.width*k),round(t.height*k)),Image.Resampling.NEAREST);z=Image.new('RGBA',(384,384));z.alpha_composite(v,(round(192-p[0]*t.width*k),round(192-p[1]*t.height*k)));out.append(z)
 M.setdefault('normalization',{})[name]={'scale':k,'sizes':[list(t.size)for t in ts],'anchors':anchors};return out
def bank(name,fs,dirs=1):
 c=fs[0].width;assert c%2==0 and all(f.size==(c,c)for f in fs);im=Image.new('RGBA',(c*dirs,c*len(fs)))
 for f,t in enumerate(fs):
  for d in range(dirs):im.alpha_composite(t.rotate(-360*d/dirs,Image.Resampling.NEAREST),(d*c,f*c))
 p=O/(name+'.webp');im.save(p,format='WEBP',lossless=True,method=3);b={'key':'cb112_'+name,'path':p.relative_to(R).as_posix(),'cell':c,'frames':len(fs),'dirs':dirs,'cols':dirs,'dirRows':1,'sha256':sha(p)};M['banks'][name]=b;return b
def frames(B):
 im=Image.open(R/B['path']).convert('RGBA');c=B['cell'];return[im.crop((0,f*B.get('dirRows',1)*c,c,(f*B.get('dirRows',1)+1)*c))for f in range(B['frames'])]
def flow(fs,name):
 # Four source-masked moving light phases, 192px glow cells preserve a common
 # proportional canvas. Energy exists inside actual water pixels and its edge.
 c=192;im=Image.new('RGBA',(c*4,c*len(fs)))
 for i,f in enumerate(fs):
  a=np.array(f.resize((c,c),Image.Resampling.NEAREST));yy,xx=np.indices((c,c));lum=a[:,:,:3]@np.array([.2126,.7152,.0722]);mask=a[:,:,3]>0;energy=mask&(lum>65);edge=maximum_filter(mask,5)&~mask
  for phase in range(4):
   wave=np.sin(xx*.12+yy*.075-phase*math.pi/2)+np.sin(np.hypot(xx-96,yy-96)*.16-phase*math.pi/2)
   selected=energy&(wave>0);z=rings(selected,a[:,:,:3].astype(np.float32)*.55,RING_A,1,.48).clip(0,255).astype('uint8');im.alpha_composite(Image.fromarray(z),(phase*c,i*c))
 p=O/(name+'.webp');im.save(p,format='WEBP',lossless=True,method=3);M['banks'][name]={'key':'cb112_'+name,'path':p.relative_to(R).as_posix(),'cell':c,'frames':len(fs),'dirs':4,'cols':4,'dirRows':1,'sha256':sha(p),'flowPhases':4}
def tween(fs,steps,loop=True,solid=False):
 out=[];yy,xx=np.indices(fs[0].size[::-1],dtype=np.float32)
 for i,a in enumerate(fs):
  if i==len(fs)-1 and not loop:out.append(a);break
  b=fs[(i+1)%len(fs)];aa=np.array(a);bb=np.array(b);ga=cv2.cvtColor(aa,cv2.COLOR_RGBA2GRAY);gb=cv2.cvtColor(bb,cv2.COLOR_RGBA2GRAY)
  f=cv2.calcOpticalFlowFarneback(ga,gb,None,.5,3,23,4,5,1.2,0);r=cv2.calcOpticalFlowFarneback(gb,ga,None,.5,3,23,4,5,1.2,0)
  for n in range(steps):
   t=n/steps
   if not n:out.append(a.copy());continue
   av=cv2.remap(aa,xx-f[:,:,0]*t,yy-f[:,:,1]*t,cv2.INTER_NEAREST,borderMode=cv2.BORDER_CONSTANT);bv=cv2.remap(bb,xx-r[:,:,0]*(1-t),yy-r[:,:,1]*(1-t),cv2.INTER_NEAREST,borderMode=cv2.BORDER_CONSTANT)
   z=np.round(av*(1-t)+bv*t).astype('uint8')
   if solid:
    selected=av if t<.5 else bv;both=(av[:,:,3]>0)&(bv[:,:,3]>0);z[~both]=selected[~both];z[:,:,3]=selected[:,:,3]
   z[:,:,3][z[:,:,3]<25]=0;out.append(Image.fromarray(z))
 return out
def preview(name,fs):
 out=Image.new('RGB',(192*8,210*math.ceil(len(fs)/8)),(5,13,24));d=ImageDraw.Draw(out)
 for i,t in enumerate(fs):
  z=t.copy();z.thumbnail((192,192),Image.Resampling.NEAREST);x=i%8*192;y=i//8*210;out.paste(z,(x+(192-z.width)//2,y+18),z);d.text((x+4,y),str(i),fill='white')
 out.save(Q/(name+'-frames.jpg'),quality=94)
anchors=[(.5,.35),(.52,.35),(.5,.35),(.5,.35),(.5,.35),(.48,.35),(.5,.35),(.5,.35),(.5,.39),(.5,.37),(.5,.38),(.5,.38),(.5,.39),(.5,.39),(.5,.36),(.5,.37)]
actions=norm('actions',16,4,anchors);actions[1],actions[5]=actions[5],actions[1]
bank('actions',actions);flow(actions,'actions_flow');preview('actions',actions)
raw=[[[.28,.42],[.75,.60]],[[.30,.52],[.78,.18]],[[.25,.54],[.72,.39]],[[.25,.53],[.86,.45]],[[.25,.60],[.72,.42]],[[.22,.18],[.70,.52]],[[.28,.39],[.75,.54]],[[.14,.45],[.75,.53]],[[.12,.51],[.88,.51]],[[.42,.55],[.58,.55]],[[.43,.49],[.57,.49]],[[.43,.49],[.57,.49]],[[.35,.34],[.65,.34]],[[.36,.34],[.64,.34]],[[.40,.50],[.60,.50]],[[.16,.49],[.84,.49]]]
N=M['normalization']['actions'];order=[0,5,2,3,4,1,6,7,8,9,10,11,12,13,14,15]
M['hands']=[[[192+(p[a]-N['anchors'][order[i]][a])*N['sizes'][order[i]][a]*N['scale'] for a in [0,1]]for p in ports]for i,ports in enumerate(raw)]
# Snap candidate palm sockets to actual opaque water pixels, then inspect the
# socket contact sheets. Coordinates are in the normalized384px chest space.
for i,ports in enumerate(M['hands']):
 a=np.array(actions[i]);yy,xx=np.nonzero(a[:,:,3]>200)
 for j,p in enumerate(ports):
  k=np.argmin((xx-p[0])**2+(yy-p[1])**2);M['hands'][i][j]=[int(xx[k]),int(yy[k])]
yaw=norm('yaw',8,2,[(.5,.34),(.5,.34),(.55,.34),(.5,.34),(.5,.34),(.5,.34),(.45,.34),(.5,.34)])
turn=tween(yaw,4,solid=True);bank('yaw',turn);flow(turn,'yaw_flow');preview('yaw',turn)
N=M['normalization']['yaw'];raw=[[[.12,.49],[.88,.49]],[[.13,.49],[.88,.49]],[[.52,.49],[.78,.47]],[[.13,.49],[.90,.50]],[[.13,.49],[.88,.49]],[[.12,.49],[.88,.49]],[[.22,.47],[.48,.49]],[[.12,.49],[.87,.49]]]
pts=[[[192+(p[a]-N['anchors'][i][a])*N['sizes'][i][a]*N['scale'] for a in [0,1]]for p in ports]for i,ports in enumerate(raw)];M['yawHands']=[]
for i,t in enumerate(turn):
 a=i//4;b=(a+1)%8;u=i%4/4;ports=[];yy,xx=np.nonzero(np.array(t)[:,:,3]>180)
 for j in range(2):
  p=np.array(pts[a][j])*(1-u)+np.array(pts[b][j])*u;k=np.argmin((xx-p[0])**2+(yy-p[1])**2);ports.append([int(xx[k]),int(yy[k])])
 M['yawHands'].append(ports)
orb=frames(OLD['models']['current']['orb'])[0];spins=[orb.rotate(-i*360/32,Image.Resampling.NEAREST)for i in range(32)];bank('orb',spins);flow(spins,'orb_flow');preview('orb',spins[::4])
morph=frames(OLD['models']['current']['morph']);flow(morph,'morph_flow')
wave=frames(OLD['banks']['tidal_wave']);waves=tween(wave,4);bank('wave',waves,4);preview('wave',waves)
# The approved Falva-derived 16-frame roller spins are recolored in water hues.
p=R/'assets/game/levels/stage_06/boss/kaia_roller_1028/spin.png';im=Image.open(p).convert('RGBA');rollers=[]
M['sources']['roller']={'path':p.relative_to(R).as_posix(),'sha256':sha(p),'origin':'Falva authored roller / build_kaia_rollers_1028.py'}
for i in range(16):
 a=np.array(im.crop((i%4*64,i//4*64,(i%4+1)*64,(i//4+1)*64)));rgb=a[:,:,:3].astype(float);lum=rgb@np.array([.2126,.7152,.0722]);hue=np.array([20,177,255]);hy=hue@np.array([.2126,.7152,.0722]);z=np.where((lum<=hy)[:,:,None],hue*lum[:,:,None]/hy,hue+(255-hue)*(lum-hy)[:,:,None]/(255-hy));a[:,:,:3]=np.clip(z,0,255).astype('uint8');rollers.append(Image.fromarray(a))
bank('roller',rollers);flow(rollers,'roller_flow');preview('roller',rollers)
(O/'manifest.json').write_text(json.dumps(M,indent=2)+'\n',encoding='utf-8');(R/'assets/current_breaker_art_1102.js').write_text('"use strict";\nconst CB112_ART='+json.dumps(M,separators=(',',':'))+';\n',encoding='utf-8',newline='\n');print('Registered',len(M['banks']),'Current Breaker banks')
