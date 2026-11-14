from pathlib import Path
from PIL import Image
import json,math,hashlib,shutil,numpy as np
from scipy.ndimage import label
W=Path(__file__).resolve().parent;ARCHIVED=W.parent.name=='_BUILD_SOURCE';R=W.parent.parent if ARCHIVED else Path('C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');O=W/'export'if ARCHIVED else W.parents[1]/'outputs/dracodia-helicopter';O.mkdir(parents=True,exist_ok=True);C=W/'candidate';D=C/'art';D.mkdir(parents=True,exist_ok=True)
BASE=Path('C:/Users/Mike/.codex/generated_images/01a1c263-6df7-7072-a76a-4b41ccbb8b8a');sources={'muzzle':'exec-f239de2b-23f2-4408-96e0-febf6048e55e.png','missile':'exec-666a05de-df08-48e5-9fb2-e369e33dad63.png','tracer':'exec-7e854112-2ce4-4992-b8ac-9172b5bac7f7.png','explosion':'exec-cdc5d3ae-6a2c-4186-a4cb-b85474f63aeb.png'}
A={'version':'H125','banks':{},'pages':{},'sources':{},'directions':64,'direction_zero':'south; positive index clockwise in canvas coordinates','frames':{'muzzle':8,'launch':8,'tracer':8,'missile':8,'burst72':16,'burst112':16,'burst160':16},'timing':{'muzzle':.16,'launch':.20,'missile_fps':24,'tracer_fps':30,'explosion_fps':20},'contract':'Decorative source pixels; native projectile movement, damage, interception, HP and warnings retained.'}
class Pack:
 def __init__(self):self.im=Image.new('RGBA',(1024,1024));self.x=self.y=self.rh=self.n=0
 def flush(self):
  if not(self.y or self.rh):return
  key='h125_'+str(self.n);im=self.im.crop((0,0,1024,min(1024,(self.y+self.rh+1)//2*2)));im.save(D/(key+'.png'),optimize=True);A['pages'][key]={'path':'assets/game/levels/stage_08/effects/helicopter_1111/'+key+'.png','size':list(im.size)};self.n+=1;self.x=self.y=self.rh=0;self.im=Image.new('RGBA',(1024,1024))
 def emit(self,name,im,pivot):
  bbox=im.getbbox()or(0,0,2,2);x=bbox[0]//2*2;y=bbox[1]//2*2;r=min(im.width,(bbox[2]+1)//2*2);b=min(im.height,(bbox[3]+1)//2*2);q=im.crop((x,y,r,b));w,h=q.size;assert w%2==h%2==0
  if self.x+w>1024:self.x=0;self.y+=self.rh+2;self.rh=0
  if self.y+h>1024:self.flush()
  self.im.paste(q,(self.x,self.y));A['banks'].setdefault(name,[]).append({'key':'h125_'+str(self.n),'rect':[self.x,self.y,w,h],'offset':[x-pivot[0],y-pivot[1]],'w':w,'h':h,'logical':list(im.size),'pivot':pivot});self.x+=w+2;self.rh=max(self.rh,h)
pack=Pack()
def master(name,rows):
 p=W/(name+'-master.png')if(W/(name+'-master.png')).exists()else BASE/sources[name];raw=Image.open(p).convert('RGBA');shutil.copy2(p,O/(name+'-master.png'));A['sources'][name]={'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'size':list(raw.size),'grid':[4,rows]};cw=2*math.ceil(raw.width/4/2);ch=2*math.ceil(raw.height/rows/2);frames=[]
 for f in range(4*rows):
  x=round(f%4*raw.width/4);y=round(f//4*raw.height/rows);xx=round((f%4+1)*raw.width/4);yy=round((f//4+1)*raw.height/rows);im=Image.new('RGBA',(cw,ch));im.paste(raw.crop((x,y,xx,yy)),(0,0));v=np.array(im);keep=v[:,:,3]>=144;labs,n=label(keep);counts=np.bincount(labs.ravel());keep&=np.isin(labs,np.flatnonzero(counts>=5));v[:,:,3]=np.where(keep,255,0);v[~keep]=0;frames.append(Image.fromarray(v))
 return frames
def palette(frames):
 sample=np.concatenate([np.array(q)[np.array(q)[:,:,3]>0,:3]for q in frames])[::3];q=Image.fromarray(sample.reshape(1,-1,3)).quantize(colors=32,method=Image.Quantize.MEDIANCUT);pal=Image.new('P',(1,1));pal.putpalette(q.getpalette());out=[]
 for im in frames:rgb=im.convert('RGB').quantize(palette=pal,dither=Image.Dither.NONE).convert('RGBA');rgb.putalpha(im.getchannel('A'));out.append(rgb)
 return out
def sized(frames,w):
 h=2*math.ceil(frames[0].height/frames[0].width*w/2);return palette([im.resize((w,h),Image.Resampling.NEAREST)for im in frames])
def directions(name,frames,pivot,cell):
 for f,im in enumerate(frames):
  base=Image.new('RGBA',(cell,cell));base.paste(im,(cell//2-pivot[0],cell//2-pivot[1]));
  for d in range(64):pack.emit(name,base.rotate(-d*360/64,resample=Image.Resampling.NEAREST,center=(cell//2,cell//2)),[cell//2,cell//2])
m=master('muzzle',2);m[-1]=Image.new('RGBA',m[0].size);directions('muzzle',sized(m,64),[32,22],112);directions('launch',sized(m,88),[44,30],160)
t=master('tracer',2);directions('tracer',sized(t,18),[9,48],128)
missile=master('missile',2);body=np.array(missile[0]);
for i,im in enumerate(missile):
 v=np.array(im);v[230:]=body[230:];missile[i]=Image.fromarray(v)
directions('missile',sized(missile,88),[44,62],176)
explosion=master('explosion',4);explosion[-1]=Image.new('RGBA',explosion[0].size)
for size in [72,112,160]:
 for im in sized(explosion,size):pack.emit('burst'+str(size),im,[size//2,size//2])
pack.flush();(O/'art.json').write_text(json.dumps(A,separators=(',',':')));(C/'helicopter_effects_art_1111.js').write_text("'use strict';\nconst H125_ART="+json.dumps(A,separators=(',',':'))+';\n',encoding='utf-8',newline='\n');print(json.dumps({'banks':len(A['banks']),'frames':sum(map(len,A['banks'].values())),'pages':len(A['pages']),'sources':A['sources']}),flush=True)
