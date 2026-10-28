from pathlib import Path
from PIL import Image,ImageDraw
from scipy.ndimage import label,binary_dilation
import numpy as np,json,math,hashlib,shutil
R=Path(__file__).resolve().parents[1];W=R/'_ART_SOURCES/hammer_tactical_1023';O=W/'shipping';O.mkdir(exist_ok=True)
A={'banks':{},'sheets':{},'pivot':[192,230],'cell':[384,512],'unit':1.75,'muzzle':[211,400],'heldHammer':[[-58,153],[-143,106],[-153,-91],[-75,-172]],'jobs':json.loads((W/'jobs.json').read_text()),'owner':'_BUILD_SOURCE/build_hammer_tactical_1023.py'}
def clean(im):
 a=np.array(im);a[:,:,3]=np.where(a[:,:,3]>127,255,0);L,n=label(a[:,:,3]>0);sizes=np.bincount(L.ravel());a[:,:,3][sizes[L]<10]=0
 # Cyan/blue energy uses the established cobalt + cyan family in every frame.
 rgb=a[:,:,:3].astype(float);hi=rgb.max(2);lo=rgb.min(2);m=(a[:,:,3]>0)&(rgb[:,:,2]>100)&(rgb[:,:,1]>rgb[:,:,0]*1.35)&(hi-lo>45)
 value=hi; a[:,:,0][m]=(value[m]*.18).astype('uint8');a[:,:,1][m]=(value[m]*.64).astype('uint8');a[:,:,2][m]=value[m].astype('uint8')
 return Image.fromarray(a)
def chrome(im):
 from scipy.ndimage import binary_erosion
 a=np.array(im);v=a[:,:,:3].astype(float);lum=v@np.array([.2126,.7152,.0722]);m=binary_erosion(a[:,:,3]>0)&(v.max(2)-v.min(2)<34)&(lum>56)&(lum<236);shine=np.interp(lum,[0,56,80,110,145,190,236,255],[0,56,105,145,181,222,247,255])
 for c,f in enumerate([.94,.98,1.]):a[:,:,c][m]=np.clip(shine[m]*f,0,255).astype('uint8')
 return Image.fromarray(a)
def red(im):
 a=np.array(im);v=a[:,:,:3].astype(float);m=(a[:,:,3]>0)&(v[:,:,2]>v[:,:,0]*1.3)&(v[:,:,2]>75)
 val=v.max(2)
 for c,f in enumerate([1,.20,.26]):a[:,:,c][m]=np.clip(val[m]*f,0,255).astype('uint8')
 return Image.fromarray(a)
def emit(name,ims,pivot=(192,230),muzzle=None):
 w,h=ims[0].size;sheet=Image.new('RGBA',(w*3,h*math.ceil(len(ims)/3)));rows=[]
 for i,im in enumerate(ims):
  assert im.size==(w,h);box=im.getbbox();assert box and box[0]>0 and box[1]>0 and box[2]<w and box[3]<h,(name,i,box)
  rect=[i%3*w,i//3*h,w,h];sheet.alpha_composite(im,rect[:2]);key='ht23_'+name+'_'+str(i);rows.append({'key':key,'sheet':'ht23_'+name,'cell':rect,'w':w,'h':h,'pivot':list(pivot),'bounds':list(box),'muzzle':muzzle or A['muzzle']})
 path=O/(name+'.webp');sheet.save(path,lossless=True,exact=True);A['sheets']['ht23_'+name]={'key':'nca_ht23_'+name,'path':'assets/game/shared/combat/hammer_tactical_1023/'+path.name,'w':sheet.width,'h':sheet.height,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()};A['banks'][name]=rows
 return rows
for bank in ['toss','catch','fire']:
 ims=[]
 files=sorted((W/'raw'/bank).glob('*.png'))
 if bank=='catch':files=[files[i]for i in [0,0,0,3,4,5,6,7,8]] # two clipped arrival frames are rejected
 for p in files:
  raw=clean(Image.open(p).convert('RGBA'))
  if bank=='fire':
   # Reject generated effect pixels; retain the articulated recoil body. Lock the
   # approved head/core/muzzle identity so native muzzle FX remain the only flash.
   ref=clean(Image.open(W/'gun_seed.png').convert('RGBA'));a=np.array(raw);mask=binary_dilation(np.array(ref)[:,:,3]>0,iterations=4);L,n=label(a[:,:,3]>0);sizes=np.bincount(L.ravel());sizes[0]=0;mask&=L==sizes.argmax();a[:,:,3][~mask]=0;raw=Image.fromarray(a)
   for rect in [(106,70,151,104),(119,103,139,122),(120,191,158,224)]:
    raw.paste((0,0,0,0),rect);raw.alpha_composite(ref.crop(rect),(rect[0],rect[1]))
  cw=512 if bank=='toss'else 384;c=Image.new('RGBA',(cw,512));c.alpha_composite(raw.resize((448,448),Image.Resampling.NEAREST),(cw//2-224,34));ims.append(c)
 assert len(ims)==9,(bank,len(ims))
 # Stable weapon identity: the first four toss poses carry the existing canonical prop.
 if bank=='toss':
  tool=Image.open(W/'tool.png').convert('RGBA');tool.putalpha(tool.getchannel('A').point(lambda v:255 if v>127 else 0));grip=(256,350)
  for i,(hx,hy,angle)in enumerate([(-58,59,180),(-66,52,125),(-72,-44,60),(-75,-78,0)]):
   # Rotation is baked into these exported pixels; runtime never rotates a sprite.
   c=Image.new('RGBA',(1024,1024));c.alpha_composite(tool,(512-grip[0],512-grip[1]));c=c.rotate(angle,resample=Image.Resampling.NEAREST,center=(512,512));ims[i].alpha_composite(c,(256+hx-512,230+hy-512))
 for suffix,frames in [('',ims),('_armor',[chrome(im)for im in ims]),('_red',[red(im)for im in ims])]:
  rows=emit(bank+suffix,frames,pivot=(256 if bank=='toss'else 192,230))
  for i,a in enumerate(rows):a['white']='ht23_'+bank+'_hit_'+str(i)
 whites=[]
 for im in ims:c=Image.new('RGBA',im.size,'white');c.putalpha(im.getchannel('A'));whites.append(c)
 emit(bank+'_hit',whites,pivot=(256 if bank=='toss'else 192,230))
# Exact Stage6 sign, pre-sized once. Game-wide boss prompt owner uses this graphic.
shutil.copy2(W/'shoot_fixed.png',O/'shoot.png');A['shoot']={'key':'ht23_shoot','path':'assets/game/shared/ui/shoot_prompt_1023.png','w':80,'h':70,'source':'nwarn_shoot'}
# Existing canonical prop used for detached upward flight, no icon substitute.
tool=Image.open(W/'tool.png').convert('RGBA');tool.putalpha(tool.getchannel('A').point(lambda v:255 if v>127 else 0));emit('tool',[tool],pivot=(256,256));emit('tool_red',[red(tool)],pivot=(256,256))
crate=[clean(Image.open(p).convert('RGBA')).resize((80,80),Image.Resampling.NEAREST)for p in sorted((W/'raw/crate').glob('*.png'))];assert len(crate)==9
crate[0]=Image.open(R/'assets/game/shared/pickups/hammer_chaingun_1020/crate.webp').convert('RGBA').resize((80,80),Image.Resampling.NEAREST);crate[0].putalpha(crate[0].getchannel('A').point(lambda v:255 if v>127 else 0));emit('crate',crate,pivot=(40,40))
gun=clean(Image.open(W/'raw/gun_prop/00.png').convert('RGBA'));box=gun.getbbox();g=gun.crop(box);g=g.resize((round(g.width*1.75),round(g.height*1.75)),Image.Resampling.NEAREST);c=Image.new('RGBA',(128,192));c.alpha_composite(g,((128-g.width)//2,20));emit('gun_prop',[c],pivot=(64,96))
emit('gun_prop_red',[red(c)],pivot=(64,96))
(O/'manifest.json').write_text(json.dumps(A,indent=2));(W/'tactical_art.js').write_text("'use strict';\nconst HT23_ART="+json.dumps(A,separators=(',',':'))+';\n')
print(json.dumps({'banks':len(A['banks']),'frames':sum(len(r)for r in A['banks'].values()),'bytes':sum((O/Path(s['path']).name).stat().st_size for s in A['sheets'].values())}))
