from pathlib import Path
import json,math,hashlib,shutil
import numpy as np
from PIL import Image,ImageFilter
R=Path(__file__).resolve().parents[1] if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury');W=R/'_ART_SOURCES/dracodia_terminal_1030' if Path(__file__).parent.name=='_BUILD_SOURCE' else Path(__file__).parent
O=R/'assets/game/levels/stage_08/ending/terminal_1030';D=R/'_ART_SOURCES/dracodia_terminal_1030';O.mkdir(parents=True,exist_ok=True);D.mkdir(parents=True,exist_ok=True)
def meta(n):
 s=(R/'assets'/n).read_text(encoding='utf8');return json.JSONDecoder().raw_decode(s[s.index('=')+1:])[0]
V=meta('stage8_pixellab_art_1018.js');I=meta('stage8_identity_art_1018.js');F=meta('final_effects_art_1021.js');L=meta('stage78_review_art_1025.js');K=meta('lightning_art_1018.js');P=meta('phoenix_turbo_core_art_1030.js');C=meta('coastal_city_art_1021.js');A={'banks':{},'pages':{},'sources':{},'timing':{'lightning':6,'explosions':9.2,'downloads':13.2,'shatter':16.4,'portal':18.4},'source':'Current complete colossus idle/roar, actual formation lightning, ColeForge explosion packs, actual gated toxic portal recoloured blue, exact current aircraft.'}
def read(path):
 p=R/path;A['sources'][path]=hashlib.sha256(p.read_bytes()).hexdigest();return Image.open(p).convert('RGBA')
class Pack:
 def __init__(self,name):self.name=name;self.n=0;self.x=self.y=self.rh=self.used=0;self.im=Image.new('RGBA',(1024,1024))
 def flush(self):
  if not self.used:return
  key='rd84_'+self.name+'_'+str(self.n);w=min(1024,(self.used+1)//2*2);h=min(1024,(self.y+self.rh+3)//2*2);p=O/(key+'.webp');self.im.crop((0,0,w,h)).save(p,lossless=True,method=3);A['pages'][key]={'path':p.relative_to(R).as_posix(),'w':w,'h':h};self.n+=1;self.x=self.y=self.rh=self.used=0;self.im=Image.new('RGBA',(1024,1024))
 def emit(self,name,im,pivot=None,extra=None):
  pivot=pivot or[im.width//2,im.height//2];v=np.array(im);v[v[:,:,3]==0,:3]=0;im=Image.fromarray(v);b=im.getbbox()or(pivot[0],pivot[1],pivot[0]+2,pivot[1]+2);l=b[0]//2*2;t=b[1]//2*2;r=min(im.width,(b[2]+1)//2*2);z=min(im.height,(b[3]+1)//2*2);crop=im.crop((l,t,r,z));w,h=crop.size;assert w%2==h%2==0 and w<=1024 and h<=1024
  if self.x+w+2>1024:self.x=0;self.y+=self.rh+2;self.rh=0
  if self.y+h+2>1024:self.flush()
  self.im.paste(crop,(self.x,self.y));a={'key':'rd84_'+self.name+'_'+str(self.n),'rect':[self.x,self.y,w,h],'offset':[l-pivot[0],t-pivot[1]],'w':w,'h':h,'logical':list(im.size),'pivot':pivot}
  if extra:a.update(extra)
  A['banks'].setdefault(name,[]).append(a);self.x+=w+2;self.used=max(self.used,self.x);self.rh=max(self.rh,h)
body=Pack('body');fx=Pack('effects');bits=Pack('shatter');ships=Pack('ships')
def centre(im,size,canvas=512):
 k=size/max(im.size);sz=tuple(max(2,round(n*k/2)*2)for n in im.size);out=Image.new('RGBA',(canvas,canvas));out.paste(im.resize(sz,Image.Resampling.NEAREST),(canvas//2-sz[0]//2,canvas//2-sz[1]//2));return out
def glow(im,power):
 v=np.array(im);mask=v[:,:,3];u=power/5;v[:,:,:3]=(v[:,:,:3]*(1-u)+255*u).astype(np.uint8);out=Image.new('RGBA',im.size)
 if power:
  edge=np.array(im.getchannel('A').filter(ImageFilter.MaxFilter(9)));g=np.zeros_like(v);g[:,:,:3]=[164,232,255];g[:,:,3]=np.where((edge>0)&(mask==0),60+power*30,0).astype(np.uint8);out.alpha_composite(Image.fromarray(g))
 out.alpha_composite(Image.fromarray(v));return out
poses={'idle':[],'roar':[]}
for a in V['models']['colossus']['frames']:
 im=Image.new('RGBA',(320,320))
 for name in ['left','right','core']:im.alpha_composite(read(a[name]['path']))
 poses['idle'].append(centre(im,410))
for a in I['clips']['colossus_roar']['frames']:poses['roar'].append(centre(read(a['path']),410))
for name,ims in poses.items():
 for level in range(6):
  for im in ims:body.emit(name+'_'+str(level),glow(im,level))
body.flush()
# Actual formation bolts, normalized offline to a full-height downward channel.
a=L['lightning'];sheet=read(L['sheets']['lightning']['path'])
for f in range(a['count']):
 im=sheet.crop((f%a['cols']*a['w'],f//a['cols']*a['h'],f%a['cols']*a['w']+a['w'],f//a['cols']*a['h']+a['h']));im=im.resize((256,544),Image.Resampling.NEAREST)
 for strength,alpha in [('strong',1),('tail',.40)]:
  v=np.array(im);v[:,:,3]=(v[:,:,3].astype(float)*alpha).astype(np.uint8);fx.emit('lightning_'+strength,Image.fromarray(v),[128,272])
# ColeForge's own dense fuel/chain explosions, electrified without altering alpha.
for name,source,size in [('electric_small','pack_fuel_tank_rupture',130),('electric_medium','pack_standard_eexplosions_04_smoke_core_blast',210),('electric_final','explosion_chain_burst',420)]:
 bank=F['banks'][source]
 for f,a in enumerate(bank['frames']):
  im=read(a['path']);x,y,w,h=a['cell'];im=im.crop((x,y,x+w,y+h));v=np.array(im);rgb=v[:,:,:3].astype(float);light=rgb.max(2)/255;warm=(rgb[:,:,0]>rgb[:,:,2]*1.2)&(rgb[:,:,0]>rgb[:,:,1]*.9);cold=np.stack([20+210*light**3,65+190*light**1.3,100+155*light],2);v[:,:,:3]=np.where(warm[:,:,None],cold,rgb).clip(0,255).astype(np.uint8)
  arc=read(K['banks']['wrap_front']['frames'][f%32]['path']).resize(im.size,Image.Resampling.NEAREST);av=np.array(arc);av[:,:,3]=np.minimum(av[:,:,3],v[:,:,3]);electrified=Image.alpha_composite(Image.fromarray(v),Image.fromarray(av));fx.emit(name,centre(electrified,size))
# The actual existing blue METAL-FRAMED lifecycle, not the energy-only variant.
gate={phase:[read('assets/game/shared/fx/portal_lifecycle_1011/blue_rift_'+phase+'_'+str(f).zfill(2)+'.png')for f in range(32)]for phase in ['form','loop','close']}
boxes=[im.getbbox()for ims in gate.values()for im in ims if im.getbbox()];bounds=(min(b[0]for b in boxes),min(b[1]for b in boxes),max(b[2]for b in boxes),max(b[3]for b in boxes));A['gateSource']='Existing blue_rift mechanical lifecycle; common union crop, one proportional size.';A['source']=A['source'].replace('actual gated toxic portal recoloured blue','actual existing blue metal-framed lifecycle')
for phase,count in [('loop',16),('form',12),('close',12)]:
 for f in range(count):
  source=gate[phase][round(f*(31 if phase!='loop'else 30)/(count-1))];fx.emit('gate_'+phase,centre(source.crop(bounds),320,384))
# Actual code curtain becomes finite pre-authored scan steps over the whole body.
cur=meta('arena_download_art_1020.js')['curtain'];sheet=read(cur['path']);base=poses['roar'][12]
for f in range(16):
 v=np.array(base);y0=round(f/15*512);mask=np.indices((512,512))[0]>=y0;v[mask,3]=0
 x,y,w,h=cur['cells'][f*2];code=sheet.crop((x,y,x+w,y+h)).resize((512,512),Image.Resampling.NEAREST);cv=np.array(code);cv[:,:,3]=np.where(np.abs(np.indices((512,512))[0]-y0)<24,cv[:,:,3],0);im=Image.alpha_composite(Image.fromarray(v),Image.fromarray(cv));fx.emit('download_erase',im)
# Exact source pixels split into irregular alpha-bearing armor chunks.
v=np.array(base);yy,xx=np.indices((512,512));coords=np.argwhere(v[:,:,3]>48);rng=np.random.default_rng(84030);samples=coords[rng.choice(len(coords),56,replace=False)];dist=(yy[:,:,None]-samples[:,0])**2+(xx[:,:,None]-samples[:,1])**2;labels=dist.argmin(2);pieces=[]
for n,(sy,sx)in enumerate(samples):
 mask=(labels==n)&(v[:,:,3]>0);q=v.copy();q[~mask]=0;im=Image.fromarray(q);box=im.getbbox()
 if not box:continue
 im=im.crop(box);cx=(box[0]+box[2])/2-256;cy=(box[1]+box[3])/2-256;angle=math.atan2(cy,cx);pieces.append((im,cx,cy,angle,n))
for f in range(64):
 t=f/20;u=max(0,t-.10);out=Image.new('RGBA',(1024,1024))
 for im,cx,cy,angle,n in pieces:
  speed=100+n%7*23;rot=im.rotate((n%2*2-1)*u*(80+n%5*31),Image.Resampling.NEAREST,expand=True);x=512+cx+math.cos(angle)*speed*u;y=512+cy+math.sin(angle)*speed*u-65*u+50*u*u
  if f%5==1 and f<18:rot=glow(rot,2)
  out.alpha_composite(rot,(round(x-rot.width/2),round(y-rot.height/2)))
 bits.emit('body_shatter',out,[512,512],{'pieces':len(pieces)})
bits.flush();A['shatterPieces']=len(pieces)
# Native stages1-9 plus the actual coastal cityX, all authored once for the rapid montage.
for n in range(1,11):
 if n==2:
  tile=read(P['arena']['lava'][0]['path']);im=Image.new('RGBA',(480,512))
  for y in [0,256]:
   for x in [0,256]:im.paste(tile,(x,y))
 elif n==10:
  source=read(C['path']);im=source.crop((144,800,624,1312))
 else:im=Image.open(W/('stage-'+str(n)+'.png')).convert('RGBA')
 p=O/('stage-'+str(n)+'.webp');im.save(p,lossless=True);A.setdefault('stages',[]).append({'key':'rd84_stage_'+str(n),'path':p.relative_to(R).as_posix(),'w':480,'h':512,'level':n})
# Generated riverfront, two environment layers and eight source-authored water phases.
scene=Image.open(W/'sewer-reunion-generated.png').convert('RGBA').resize((680,512),Image.Resampling.NEAREST);sv=np.array(scene);yy,xx=np.indices((512,680));water=(yy>76)&(yy<206)&(sv[:,:,2]>sv[:,:,0]*1.15)&(sv[:,:,1]>sv[:,:,0]*1.08);patch=sv[108:180,4:188].copy()
for f in range(8):
 im=sv.copy();tex=patch[(yy+f*2)%72,(xx+f*3)%184];im[water,:3]=((im[water,:3].astype(float)*.64)+(tex[water,:3].astype(float)*.36)).astype(np.uint8);p=O/('riverfront-'+str(f)+'.webp');Image.fromarray(im).save(p,lossless=True);A.setdefault('reunion',[]).append({'key':'rd84_riverfront_'+str(f),'path':p.relative_to(R).as_posix(),'w':680,'h':512})
# All current aircraft remain their exact authored designs; depth changes are baked.
pilots=['cole','axel','decker','falva','freezer','juggernaut','lizzie','maverick','yuri'];A['pilots']=pilots
for pk in pilots:
 src=Image.open(W/('ship-'+pk+'.png')).convert('RGBA');box=src.getbbox();src=src.crop(box)
 for f in range(32):
  size=max(2,round((2+f/31*52)/2)*2);ships.emit('ship_north_'+pk,centre(src,size,96));ships.emit('ship_south_'+pk,centre(src.transpose(Image.Transpose.FLIP_TOP_BOTTOM),size,96))
 ground=centre(src,54,96);shadow=np.zeros((96,96,4),np.uint8);shadow[:,:,3]=(np.array(ground)[:,:,3].astype(float)*.4).astype(np.uint8);ships.emit('shadow_'+pk,Image.fromarray(shadow))
ships.flush();fx.flush()
# Full-field flash frames are authored alpha, never generated at runtime.
for f,alpha in enumerate([0,24,48,80,128,190,255]):
 im=Image.new('RGBA',(480,512),(235,248,255,alpha));p=O/('flash-'+str(f)+'.webp');im.save(p,lossless=True);A.setdefault('flash',[]).append({'key':'rd84_flash_'+str(f),'path':p.relative_to(R).as_posix(),'w':480,'h':512})
(R/'assets/dracodia_terminal_art_1030.js').write_text("'use strict';\nconst RD84_ART="+json.dumps(A,separators=(',',':'))+';\n',encoding='utf8',newline='\n');(D/'manifest.json').write_text(json.dumps(A,separators=(',',':')));(D/'provenance.json').write_text(json.dumps({'sources':A['sources'],'newEnvironment':'Built-in GPT imagegen, exact prompt/source retained; no generated pilots or aircraft.','reference':'MKII arcade ending first1-25 seconds inspected for arena hopping and full-body rupture; no MK audiovisual material shipped.','render':'Authored unrotated crops, fixed logical canvases, source alpha; no runtime sprite transforms.','frames':sum(map(len,A['banks'].values()))},indent=2));print('Authored',sum(map(len,A['banks'].values())),'frames',len(A['pages']),'pages',len(pieces),'exact body shards',flush=True)
