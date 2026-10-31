"""PH82: approved Phoenix plates, source-exact sockets, core optics and lava edges.
Offline exports only; runtime selects fixed frames and ordinary positions.
"""
from pathlib import Path
import json,math,hashlib
import numpy as np
from PIL import Image,ImageFilter
R=Path(__file__).resolve().parents[1] if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury')
W=R/'_shots/phoenix_turbo_core_1030' if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(__file__).parent;W.mkdir(parents=True,exist_ok=True)
O=R/'assets/game/levels/stage_08/boss/phoenix_turbo_core_1030';D=R/'_ART_SOURCES/phoenix_turbo_core_1030';O.mkdir(parents=True,exist_ok=True);D.mkdir(parents=True,exist_ok=True)
def meta(n):
 s=(R/'assets'/n).read_text(encoding='utf8');return json.JSONDecoder().raw_decode(s[s.index('=')+1:])[0]
B=meta('boss_integrity_art_1024.js');E=meta('neural_optics_art_1030.js');V=meta('arena_download_art_1020.js');ms=(R/'assets/manifest.js').read_text(encoding='utf8');M=json.JSONDecoder().raw_decode(ms.split('window.BOFX=',1)[1])[0];PATHS=meta('asset_paths_1007.js')
A={'banks':{},'pages':{},'poses':{},'arena':{},'ids':['core','head','wingL','wingR','clawL','clawR','cannonL','cannonR'],'directions':[45+i*7.5 for i in range(13)],'bodyLogical':[512,512],'bodyPivot':[256,256]};sources={}
def read(path):
 p=R/PATHS.get(path,path);sources[p.relative_to(R).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest();return Image.open(p).convert('RGBA')
class Pack:
 def __init__(self,prefix,hit=False):self.prefix=prefix;self.hit=hit;self.n=0;self.x=self.y=self.rh=0;self.im=Image.new('RGBA',(1024,1024))
 def flush(self):
  if not(self.rh or self.y):return
  key='ph82_'+self.prefix+'_'+str(self.n);h=min(1024,(self.y+self.rh+3)//2*2);im=self.im.crop((0,0,1024,h));p=O/(key+'.webp');im.save(p,lossless=True,method=3);a={'path':p.relative_to(R).as_posix(),'w':1024,'h':h}
  if self.hit:
   v=np.array(im);v[:,:,:3]=255;hp=O/(key+'_hit.webp');Image.fromarray(v).save(hp,lossless=True,method=3);a.update(hitKey=key+'_hit',hitPath=hp.relative_to(R).as_posix())
  A['pages'][key]=a;self.n+=1;self.x=self.y=self.rh=0;self.im=Image.new('RGBA',(1024,1024))
 def emit(self,name,im,pivot,extra=None):
  b=im.getbbox()or(pivot[0],pivot[1],pivot[0]+2,pivot[1]+2);xx=b[0]//2*2;yy=b[1]//2*2;rr=min(im.width,(b[2]+1)//2*2);bb=min(im.height,(b[3]+1)//2*2);crop=im.crop((xx,yy,rr,bb));w,h=crop.size;assert w%2==h%2==0 and w<=1024 and h<=1024
  if self.x+w+2>1024:self.x=0;self.y+=self.rh+2;self.rh=0
  if self.y+h+2>1024:self.flush()
  self.im.paste(crop,(self.x,self.y));a={'key':'ph82_'+self.prefix+'_'+str(self.n),'rect':[self.x,self.y,w,h],'offset':[xx-pivot[0],yy-pivot[1]],'w':w,'h':h,'logical':list(im.size)}
  if extra:a.update(extra)
  A['banks'].setdefault(name,[]).append(a);self.x+=w+2;self.rh=max(self.rh,h);return a
body=Pack('body',True);fx=Pack('fx')
def rows(mask):
 out=[]
 for row in mask:
  padded=np.pad(row.astype(np.int8),(1,1));d=np.diff(padded);out.append([int(n)for pair in zip(np.flatnonzero(d==1),np.flatnonzero(d==-1))for n in pair])
 return out
def image_frame(a,f):
 sh=next(s for s in B['sheets'].values()if s['key']==a['key']);im=read(sh['path']);x=f%a['cols']*a['w'];y=f//a['cols']*a['h'];return im.crop((x,y,x+a['w'],y+a['h']))
def centres(v,cx,cy):
 # Detect the two visible hot barrel mouths near the original measured pair.
 out=[]
 for sign in [-1,1]:
  px=cx+sign*16;py=cy;yy,xx=np.indices(v.shape[:2]);m=(abs(xx-px)<12)&(abs(yy-py)<16)&(v[:,:,0]>180)&(v[:,:,1]>60)&(v[:,:,2]<150)&(v[:,:,3]>48)
  if m.any():out.append([float(xx[m].mean()),float(yy[m].mean())])
  else:out.append([px,py])
 return out
preview=[]
for phase in ['recover','wind','strike']:
 bank=B['banks']['phoenix_'+phase]
 for f in range(bank['count']):
  src=image_frame(bank,f);v=np.array(src);yy,xx=np.indices((512,512));warm=(v[:,:,0]>180)&(v[:,:,1]>70)&(v[:,:,2]<120)&(abs(xx-256)<26)&(abs(yy-255)<40)&(v[:,:,3]>48);cx=float(xx[warm].mean())if warm.any()else 256;cy=float(yy[warm].mean())if warm.any()else 255
  # One common proportional360px scale, centred on the original512px pivot.
  native=src.resize((360,360),Image.Resampling.NEAREST);full=Image.new('RGBA',(512,512));full.paste(native,(76,76));base=np.array(full);pose=phase+'_'+str(f);sockets={};original={}
  for tag,side in [('cannonL','left'),('cannonR','right')]:
   sx,sy=bank['sockets'][f][side];original[tag]=centres(v,sx*2,sy*2);sockets[tag]=[[round((x-256)*360/512),round((y-256)*360/512)]for x,y in original[tag]]
  core=[round((cx-256)*360/512),round((cy-256)*360/512)]
  # Pixel classification mirrors the native intact-part ownership, baked once.
  X=(xx-76)*512/360/2;Y=(yy-76)*512/360/2;ids=np.zeros((512,512),np.uint8)
  ids[(Y<117)&(X>115)&(X<141)]=1;ids[(X<112)&(Y<145)]=2;ids[(X>144)&(Y<145)]=3;low=(Y>150)&(Y<185);ids[low&(X<128)]=4;ids[low&(X>=128)]=5
  for num,side in [(6,'left'),(7,'right')]:
   sx,sy=bank['sockets'][f][side];ids[(abs(X-sx)<13)&(Y>sy-34)&(Y<sy+3)]=num
  hit=[];parts={};opaque=base[:,:,3]>48
  for row,m in zip(ids,opaque):
   runs=[];start=None;last=-1
   for x in range(513):
    value=int(row[x])if x<512 and m[x]else-1
    if value!=last:
     if last>=0:runs.extend([start,x,last])
     start=x;last=value
   hit.append(runs)
  for i,id in enumerate(A['ids']):
   by,bx=np.nonzero(opaque&(ids==i));parts[id]=[round((int(bx.min())+int(bx.max()))/2-256),round((int(by.min())+int(by.max()))/2-256),int(bx.max()-bx.min()+1),int(by.max()-by.min()+1)]if len(bx)else[0,0,0,0]
  A['poses'][pose]={'phase':phase,'f':f,'sockets':sockets,'core':core,'hitRows':hit,'parts':parts}
  for dead in range(4):
   q=base.copy()
   for i,num in enumerate([6,7]):
    if dead&(1<<i):
     mask=(ids==num)&opaque;lum=q[:,:,:3].astype(float).mean(2)*.35;q[:,:,:3][mask]=np.stack([lum,lum,lum*1.08],2)[mask].astype(np.uint8)
   body.emit('body_'+phase+'_'+str(dead),Image.fromarray(q),[256,256],{'pose':pose})
  # Core-only1015 ring/material pixels remain source-locked, including hit flash.
  for strength in range(1,6):
   lum=np.zeros((512,512,4),np.uint8);radius=16+strength;ccx=256+core[0];ccy=256+core[1];mask=((xx-ccx)**2+(yy-ccy)**2<radius**2)&opaque;hot=base.copy();hot[:,:,:3]=(hot[:,:,:3].astype(float)*(1-strength*.13)+np.array([255,230,130])*strength*.13).clip(0,255).astype(np.uint8);lum[mask]=hot[mask];seed=Image.fromarray(lum);halo=seed.getchannel('A').filter(ImageFilter.MaxFilter(5));hv=np.zeros_like(lum);hv[:,:,:3]=[255,81,13];hv[:,:,3]=np.array(halo)//2;out=Image.alpha_composite(Image.fromarray(hv),seed);fx.emit('core_'+phase+'_'+str(strength),out,[256,256])
  if phase=='wind':preview.append(full)
body.flush()
def optic(bank,f):
 a=E['banks'][bank][f];im=read(E['pages'][a['key']]['path']);x,y,w,h=a['rect'];crop=im.crop((x,y,x+w,y+h));full=Image.new('RGBA',(1280,1280));full.paste(crop,(640+a['offset'][0],640+a['offset'][1]));return full
for i,angle in enumerate(A['directions']):
 for name,source,frames in [('beam','beam_0',list(range(0,16,2))),('launch','start_0',list(range(5))),('recover','recover',[0,5,10,15]),('green','warning_green',[0]),('yellow','warning_yellow',[0]),('red','warning_red',[0])]:
  for f in frames:
   im=optic(source,f).rotate(90-angle,resample=Image.Resampling.NEAREST,center=(640,640));a=fx.emit(name+'_'+str(i),im,[640,640]);x,y,w,h=a['rect'];crop=im.crop((640+a['offset'][0],640+a['offset'][1],640+a['offset'][0]+w,640+a['offset'][1]+h));a['spans']=rows(np.array(crop)[:,:,3]>48)if name in ['beam','launch']else[]
fx.flush()
# The original animated lava floor retains its drawing, with a darker palette.
terrain=read(V['arenas']['lava']['terrain']['path']);wallSources=[terrain.crop((0,0,48,256)),terrain.crop((464,0,512,256))]
for f in range(8):
 path=M['img']['nlq3_lava_'+str(f)];im=read(path).resize((256,256),Image.Resampling.NEAREST);v=np.array(im);v[:,:,:3]=(v[:,:,:3].astype(float)*.50).astype(np.uint8);v[:,:,3]=255
 for name,pixels in [('lava',v),('wire',np.concatenate([(v[:,:,:3]*.45).astype(np.uint8),v[:,:,3:]],2))]:
  file=name+'_'+str(f)+'.png';Image.fromarray(pixels).save(O/file);A['arena'].setdefault(name,[]).append({'key':'ph82_'+name+'_'+str(f),'path':(O/file).relative_to(R).as_posix(),'w':256,'h':256})
 for side,src in zip(['left','right'],wallSources):
  v=np.array(src);rgb=v[:,:,:3].astype(float);mask=(rgb[:,:,0]>rgb[:,:,1]*1.5)&(rgb[:,:,0]>80);factor=[.65,.8,1,1.15,1,.85,.72,.78][f];rgb[mask]*=factor;v[:,:,:3]=rgb.clip(0,255).astype(np.uint8);file='wall_'+side+'_'+str(f)+'.png';Image.fromarray(v).save(O/file);A['arena'].setdefault(side,[]).append({'key':'ph82_wall_'+side+'_'+str(f),'path':(O/file).relative_to(R).as_posix(),'w':48,'h':256})
strip=Image.new('RGBA',(512*len(preview),512))
for i,im in enumerate(preview):strip.paste(im,(i*512,0))
strip.save(D/'wind-source-strip.png');preview[0].save(W/'body-preview.png');Image.open(O/'lava_0.png').save(W/'lava-preview.png')
(R/'assets/phoenix_turbo_core_art_1030.js').write_text("'use strict';\nconst PH82_ART="+json.dumps(A,separators=(',',':'))+';\n',encoding='utf8',newline='\n');(D/'manifest.json').write_text(json.dumps(A,separators=(',',':')));(D/'provenance.json').write_text(json.dumps({'sources':sources,'mode':'Offline authored conversion of existing approved Phoenix, NB80 optics and lava/metal-edge artwork; no paid generation.','bodyFrames':92,'coreFrames':115,'beamDirections':13,'beamOrigin':'Measured orange chest-core pixel cluster','render':'Fixed blits and current source alpha; no new runtime transformations or generated decoration.'},indent=2));print(json.dumps({'pages':len(A['pages']),'frames':sum(map(len,A['banks'].values())),'poses':len(A['poses'])}))
