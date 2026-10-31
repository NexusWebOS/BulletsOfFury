"""PH83 Order of the Phoenix. Fixed authored motion, charge and coded-fire banks.
No live sprite transforms, glow construction, alpha tween or generated decoration.
"""
from pathlib import Path
import json,math,hashlib,shutil
import numpy as np
from PIL import Image,ImageFilter
R=Path(__file__).resolve().parents[1] if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury')
W=R/'_shots/order_phoenix_1030' if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(__file__).parent;W.mkdir(exist_ok=True,parents=True)
O=R/'assets/game/levels/stage_08/boss/order_phoenix_1030';D=R/'_ART_SOURCES/order_phoenix_1030';O.mkdir(exist_ok=True,parents=True);D.mkdir(exist_ok=True,parents=True)
def meta(n):
 s=(R/'assets'/n).read_text(encoding='utf8');return json.JSONDecoder().raw_decode(s[s.index('=')+1:])[0]
B=meta('phoenix_turbo_core_art_1030.js');E=meta('neural_optics_art_1030.js');V=meta('arena_download_art_1020.js');F=meta('dracodia_phoenix_art_1020.js');sources={};cache={}
A={'banks':{},'pages':{},'ids':B['ids'],'diveAngles':[45,135,315,225],'diveDepths':[round(.82+i*.18/7,5)for i in range(8)],'echoDepths':[round(.36+i*.38/15,5)for i in range(16)],'windSizes':[160,190,210,230,250],'logical':[512,512],'pivot':[256,256],'source':'Approved PH82 body; reference-generated8-view turntable; source-authored coded fire.'}
def read(path):
 p=R/path
 if path not in cache:sources[path]=hashlib.sha256(p.read_bytes()).hexdigest();cache[path]=Image.open(p).convert('RGBA')
 return cache[path]
class Pack:
 def __init__(self,name,hit=False):self.name=name;self.hit=hit;self.n=0;self.x=self.y=self.rh=self.usedx=0;self.im=Image.new('RGBA',(1024,1024))
 def flush(self):
  if not self.usedx:return
  key='ph83_'+self.name+'_'+str(self.n);w=max(2,(self.usedx+1)//2*2);h=min(1024,(self.y+self.rh+3)//2*2);im=self.im.crop((0,0,w,h));p=O/(key+'.webp');im.save(p,lossless=True,method=3);a={'path':p.relative_to(R).as_posix(),'w':w,'h':h}
  if self.hit:
   v=np.array(im);v[:,:,:3]=255;hp=O/(key+'_hit.webp');Image.fromarray(v).save(hp,lossless=True,method=3);a.update(hitKey=key+'_hit',hitPath=hp.relative_to(R).as_posix())
  A['pages'][key]=a;self.n+=1;self.x=self.y=self.rh=self.usedx=0;self.im=Image.new('RGBA',(1024,1024))
 def emit(self,name,im,extra=None):
  pixels=np.array(im);pixels[pixels[:,:,3]==0,:3]=0;im=Image.fromarray(pixels);b=im.getbbox()or(256,256,258,258);x0=b[0]//2*2;y0=b[1]//2*2;x1=min(im.width,(b[2]+1)//2*2);y1=min(im.height,(b[3]+1)//2*2);crop=im.crop((x0,y0,x1,y1));w,h=crop.size;assert w%2==h%2==0 and w<=1024 and h<=1024
  if self.x+w+2>1024:self.x=0;self.y+=self.rh+2;self.rh=0
  if self.y+h+2>1024:self.flush()
  self.im.paste(crop,(self.x,self.y));a={'key':'ph83_'+self.name+'_'+str(self.n),'rect':[self.x,self.y,w,h],'offset':[x0-256,y0-256],'w':w,'h':h,'logical':[512,512]}
  if extra:a.update(extra)
  A['banks'].setdefault(name,[]).append(a);self.x+=w+2;self.usedx=max(self.usedx,self.x);self.rh=max(self.rh,h);return a
combat=Pack('combat',True);motion=Pack('motion');fx=Pack('effects')
def restore(a,pages,pivot=256,logical=512):
 im=read(pages[a['key']]['path']);x,y,w,h=a['rect'];out=Image.new('RGBA',(logical,logical));out.paste(im.crop((x,y,x+w,y+h)),(pivot+a['offset'][0],pivot+a['offset'][1]));return out
def transform(im,depth=1,angle=0):
 size=max(2,round(512*depth/2)*2);q=im.resize((size,size),Image.Resampling.NEAREST);out=Image.new(im.mode,(512,512));out.paste(q,(256-size//2,256-size//2));return out.rotate(-angle,Image.Resampling.NEAREST,center=(256,256))if angle else out
def span_rows(mask):
 out=[]
 for row in mask:
  d=np.diff(np.pad(row.astype(np.int8),(1,1)));out.append([int(v)for pair in zip(np.flatnonzero(d==1),np.flatnonzero(d==-1))for v in pair])
 return out
def tag_data(tags):
 v=np.array(tags);hit=[];parts={}
 for row in v:
  d=np.flatnonzero(np.diff(np.pad(row.astype(np.int16),(1,1))));runs=[]
  for x0,x1 in zip(d,d[1:]):
   if row[x0]:runs.extend([int(x0),int(x1),int(row[x0])-1])
  hit.append(runs)
 for i,id in enumerate(A['ids']):
  yy,xx=np.nonzero(v==i+1);parts[id]=[round((int(xx.min())+int(xx.max()))/2-256),round((int(yy.min())+int(yy.max()))/2-256),int(xx.max()-xx.min()+1),int(yy.max()-yy.min()+1)]if len(xx)else[0,0,0,0]
 return{'hitRows':hit,'parts':parts}
wing_indices=[0,1,2,3,4,5,6,7,8,7,6,5,4,3,2,1];bodies=[];labels=[]
for f in wing_indices:
 a=B['banks']['body_wind_3'][f];im=restore(a,B['pages']);tag=np.zeros((512,512),np.uint8)
 for y,row in enumerate(B['poses']['wind_'+str(f)]['hitRows']):
  for i in range(0,len(row),3):tag[y,row[i]:row[i+1]]=row[i+2]+1
 bodies.append(im);labels.append(Image.fromarray(tag))
def combat_frame(name,im,tags,depth):
 combat.emit(name,im,{'depth':depth,**tag_data(tags)});v=np.zeros((512,512,4),np.uint8);v[:,:,3]=(np.array(im)[:,:,3].astype(float)*.35).astype(np.uint8);v[346:,:,3]=0;short=Image.fromarray(v).resize((512,164),Image.Resampling.NEAREST);out=Image.new('RGBA',(512,512));out.paste(short,(0,174));fx.emit(name+'_shadow',out)
for f in range(16):combat_frame('idle',bodies[f],labels[f],1)
for d,angle in enumerate(A['diveAngles']):
 for depth in A['diveDepths']:
  for f in [2,6]:combat_frame('dive_'+str(d),transform(bodies[f],depth,angle-90),transform(labels[f],depth,angle-90),depth)
combat.flush()
# Approaches and returns use authored sizes. No arbitrary runtime scaling.
for i in range(18):
 u=i/17;motion.emit('recede',transform(bodies[(i*2)%16],1-.6*u),{'depth':1-.6*u})
for d in range(16):motion.emit('cruise',transform(bodies[4],.4,d*22.5-90),{'depth':.4})
# True front/quarter/profile/rear volumes; no cross-faded duplicate wings.
turns=[bodies[0]]
for f in range(1,8):
 src=(D if(D/('isolated-turn-'+str(f)+'.png')).exists()else W)/('isolated-turn-'+str(f)+'.png');im=Image.open(src).convert('RGBA');v=np.array(im);yy,xx=np.indices(v.shape[:2]);m=(yy>im.height*.68)&(v[:,:,0]>180)&(v[:,:,1]>65)&(v[:,:,2]<120)&(v[:,:,3]>48);cx=float(xx[m].mean())if m.any()else im.width/2;cy=im.height*.47;scale=.70;sz=(max(2,round(im.width*scale/2)*2),max(2,round(im.height*scale/2)*2));out=Image.new('RGBA',(512,512));out.paste(im.resize(sz,Image.Resampling.NEAREST),(round(256-cx*scale),round(256-cy*scale)));turns.append(out);sources['turn-source-'+str(f)]=hashlib.sha256(src.read_bytes()).hexdigest()
for side,startAngle in [('north',180),('south',0)]:
 for name,count in [('twist',24),('return',32)]:
  for i in range(count):
   u=i/(count-1);view=min(8,round(u*8));src=turns[view%8];depth=.4 if name=='twist'else .4+.6*(u*u*(3-2*u));rot=startAngle*(1-u)+360*u;motion.emit(name+'_'+side,transform(src,depth,rot),{'depth':depth,'view':view%8})
# Source-authored1015 material and actual-outline light at fixed background depth.
for level in range(6):
 for f in range(16):
  src=bodies[f];v=np.array(src);alpha=v[:,:,3];rgb=v[:,:,:3].astype(float);u=level/5
  warm=(rgb[:,:,0]>rgb[:,:,2]*1.12)|(rgb[:,:,0]>rgb[:,:,1]*1.15);rgb[warm]=rgb[warm]*(1-u*.55)+np.array([255,237,135])*(u*.55);rgb[~warm]=rgb[~warm]*(1-u*.4)+np.array([255,95,25])*(u*.4);v[:,:,:3]=rgb.clip(0,255).astype(np.uint8)
  out=Image.new('RGBA',(512,512))
  if level:
   glow=np.zeros_like(v);glow[:,:,:3]=[255,75,8];ga=np.array(src.getchannel('A').filter(ImageFilter.MaxFilter(13)));glow[:,:,3]=np.where((ga>0)&(alpha==0),80+level*30,0).astype(np.uint8);out.alpha_composite(Image.fromarray(glow))
  out.alpha_composite(Image.fromarray(v));motion.emit('charge_'+str(level),transform(out,.4),{'depth':.4})
motion.flush()
# Current approved source fire/coded curtain fill inside the exact body silhouette.
cur=V['curtain'];curim=read(cur['path']);flames=[];codes=[]
for f in range(8):
 a=F['plume']['frames'][f*2];fire=read(a['path']).crop((34,60,100,128)).resize((264,272),Image.Resampling.NEAREST);flames.append(np.array(fire));x,y,w,h=cur['cells'][f*4];codes.append(np.array(curim.crop((x,y,x+w,y+h))))
echoes=[];echoMasks=[];yy,xx=np.indices((512,512))
for f in range(8):
 src=bodies[f*2];sv=np.array(src);mask=sv[:,:,3]>48;tex=flames[f][(yy-f*17)%272,(xx+f*13)%264];code=codes[f][(yy+f*21)%256,(xx-f*7)%256];light=sv[:,:,:3].max(2).astype(float)/255;rgb=np.stack([195+60*light,32+105*light,5+24*light],2);k=tex[:,:,3:4]/255;rgb=rgb*(1-k)+tex[:,:,:3]*k;marks=(code[:,:,3]>65)&mask;rgb[marks]=[255,230,90]
 inner=mask&~(np.array(Image.fromarray(mask.astype(np.uint8)*255).filter(ImageFilter.MinFilter(5)))>0);rgb[inner]=[255,244,159];body=np.zeros((512,512,4),np.uint8);body[:,:,:3]=rgb.clip(0,255).astype(np.uint8);body[:,:,3]=mask*255;halo=np.zeros_like(body);outer=(np.array(Image.fromarray(mask.astype(np.uint8)*255).filter(ImageFilter.MaxFilter(9)))>0)&~mask;halo[:,:,:3]=[255,69,7];halo[:,:,3]=outer*210;out=Image.alpha_composite(Image.fromarray(halo),Image.fromarray(body));echoes.append(out);echoMasks.append(Image.fromarray(mask.astype(np.uint8)*255))
for depth in A['echoDepths']:
 for f in range(8):
  im=transform(echoes[f],depth);mask=transform(echoMasks[f],depth);a=fx.emit('echo',im,{'depth':depth});x0=256+a['offset'][0];y0=256+a['offset'][1];a['spans']=span_rows(np.array(mask.crop((x0,y0,x0+a['w'],y0+a['h'])))>48)
for i in range(4):
 for f in range(8):
  im=transform(echoes[f],.36);v=np.array(im);v[:,:,3]=(v[:,:,3].astype(float)*(i+1)/4).astype(np.uint8);fx.emit('echo_birth',Image.fromarray(v),{'depth':.36})
# Improved Nightwing source wind arcs, converted offline to fire colours.
windPaths={s:'assets/game/levels/stage_06/boss/nightwing_teal_charge_1030/wind_'+s+'.png'for s in ['rear','front']}
windFrames={s:[]for s in windPaths}
for s,path in windPaths.items():
 sheet=read(path)
 for f in range(0,24,2):
  im=sheet.crop((f%8*336,f//8*336,f%8*336+336,f//8*336+336));v=np.array(im);light=v[:,:,:3].max(2).astype(float)/255;v[:,:,0]=(140+115*light).clip(0,255);v[:,:,1]=(20+205*light**1.7).clip(0,255);v[:,:,2]=(4+100*light**3).clip(0,255);windFrames[s].append(Image.fromarray(v))
for n,size in enumerate(A['windSizes']):
 for s in windFrames:
  for im in windFrames[s]:
   out=Image.new('RGBA',(512,512));out.paste(im.resize((size,size),Image.Resampling.NEAREST),(256-size//2,256-size//2));fx.emit('wind_'+s+'_'+str(n),out)
for f in range(8):
 out=Image.new('RGBA',(512,512))
 for s in windFrames:out.alpha_composite(windFrames[s][f].resize((250,250),Image.Resampling.NEAREST),(131,131))
 v=np.array(out);v[:,:,3]=(v[:,:,3].astype(float)*(1-f/7)).astype(np.uint8);fx.emit('wind_out',Image.fromarray(v))
# Three repeated fixed warning segments cover each committed diagonal corridor.
for colour in ['green','yellow','red']:
 src=restore(E['banks']['warning_'+colour][0],E['pages'],640,1280).crop((600,640,680,1264));src=src.resize((274,2138),Image.Resampling.NEAREST).crop((0,0,274,480));base=Image.new('RGBA',(512,512));base.paste(src,(119,16))
 for angle in A['diveAngles']:fx.emit('warning_'+colour,base.rotate(90-angle,Image.Resampling.NEAREST,center=(256,256)))
fx.flush()
strip=Image.new('RGBA',(512*8,512))
for f,im in enumerate(turns):strip.paste(im,(f*512,0))
strip.save(D/'normalized-turns.png');bg=Image.new('RGBA',(512,512),(12,8,16,255));bg.alpha_composite(echoes[3]);bg.save(W/'echo-art-preview.png');im=Image.new('RGBA',(512,512));im.alpha_composite(windFrames['rear'][3].resize((280,280),Image.Resampling.NEAREST),(116,116));im.alpha_composite(transform(bodies[6],.4));im.alpha_composite(windFrames['front'][3].resize((280,280),Image.Resampling.NEAREST),(116,116));im.save(W/'charge-art-preview.png')
(R/'assets/order_phoenix_art_1030.js').write_text("'use strict';\nconst PH83_ART="+json.dumps(A,separators=(',',':'))+';\n',encoding='utf8',newline='\n');(D/'manifest.json').write_text(json.dumps(A,separators=(',',':')));(D/'provenance.json').write_text(json.dumps({'sources':sources,'generation':'Built-in GPT local-reference8-view turntable; exact prompt/raw source retained.','body':'Approved PH82 disabled-pod body, source-locked labels and original wing cycle.','effects':'Exact body outline, PixelLab fire fill, coded curtain glyphs and improved wind arcs.','runtime':'Fixed unrotated crops, source alpha, frame selection and movement only.','newPaidCredits':0},indent=2));print(json.dumps({'frames':sum(map(len,A['banks'].values())),'pages':len(A['pages']),'bodyBanks':len(A['banks'])}))
