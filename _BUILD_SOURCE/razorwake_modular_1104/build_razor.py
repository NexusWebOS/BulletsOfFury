"""Razorwake disjoint hull/wings/guns, native1:1 pages and exact collision bits.
All hinge projections, headings, spin, glow, shadows and VFX lifecycle baked offline.
"""
from pathlib import Path
from collections import deque
import math,json,hashlib,subprocess
import numpy as np
from PIL import Image,ImageDraw,ImageFilter
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');O=W/'authored';O.mkdir(exist_ok=True)
REL='assets/game/levels/stage_06/miniboss/razorwake_modular_1104/'
M={'banks':{},'pages':{},'masks':{},'format':'Native1:1 fixed even cells,32 baked headings; trimmed pages restore exact original pivots; separate hull/wing/gun ownership; authored FX/light/shadows.'};bitdata=bytearray();frames={};pageid=0
def cutout(im,kind='ship'):
 a=np.array(im.convert('RGBA'));rgb=a[:,:,:3].astype(int);lo=rgb.min(2);ch=rgb.max(2)-lo
 # Remove only the exterior connected matte; closed silver armor highlights remain intact.
 bg=((lo>164)&(ch<65))|(a[:,:,3]<16)
 h,w=bg.shape;outside=np.zeros((h,w),bool);todo=deque()
 for x in range(w):
  for y in[0,h-1]:
   if bg[y,x]and not outside[y,x]:outside[y,x]=1;todo.append((x,y))
 for y in range(h):
  for x in[0,w-1]:
   if bg[y,x]and not outside[y,x]:outside[y,x]=1;todo.append((x,y))
 while todo:
  x,y=todo.popleft()
  for xx,yy in[(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
   if 0<=xx<w and 0<=yy<h and bg[yy,xx]and not outside[yy,xx]:outside[yy,xx]=1;todo.append((xx,yy))
 a[outside]=0;a[~outside,3]=255
 return Image.fromarray(a)
def remove_strips(im):
 a=np.array(im);fg=a[:,:,3]>0;seen=np.zeros(fg.shape,bool);hh,ww=fg.shape
 for yy,xx in zip(*np.where(fg)):
  if seen[yy,xx]:continue
  todo=deque([(int(xx),int(yy))]);seen[yy,xx]=1;pts=[]
  while todo:
   x,y=todo.popleft();pts.append((x,y))
   for nx,ny in[(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
    if 0<=nx<ww and 0<=ny<hh and fg[ny,nx]and not seen[ny,nx]:seen[ny,nx]=1;todo.append((nx,ny))
  xs=[p[0]for p in pts];ys=[p[1]for p in pts];w=max(xs)-min(xs)+1;h=max(ys)-min(ys)+1
  if (h<9 and w>24 and min(ys)>hh*.85)or(len(pts)<14 and(min(xs)==0 or max(xs)==ww-1 or min(ys)==0 or max(ys)==hh-1)):
   for x,y in pts:a[y,x]=0
 return Image.fromarray(a)
def light(im,level=0,mode='normal'):
 a=np.array(im);alpha=a[:,:,3].copy();rgb=a[:,:,:3].astype(float)
 if mode=='hit':rgb[:]=255
 elif mode=='shadow':rgb[:]=[2,9,13];a[:,:,3]=(alpha.astype(float)*.43).astype('uint8')
 elif mode=='wreck':rgb[:]=rgb.max(2)[:,:,None]*np.array([.16,.21,.22])
 elif level:
  c=rgb.max(2)-rgb.min(2);energy=(rgb[:,:,1]>rgb[:,:,0]*1.08)&(rgb[:,:,2]>rgb[:,:,0]*1.02)&(c>20)&(alpha>0)
  rgb[energy]=np.minimum(255,rgb[energy]*(1+level*.07)+np.array([level*13,level*17,level*12]));steel=(alpha>0)&~energy;rgb[steel]=np.minimum(255,rgb[steel]+np.array([0,level*3,level*2]))
 a[:,:,:3]=rgb.astype('uint8');out=Image.fromarray(a)
 if level:
  aa=out.getchannel('A');rim=aa.filter(ImageFilter.MaxFilter(3+2*(level>=4)));ring=Image.new('RGBA',out.size,(64+level*19,206+level*8,164+level*14,0));ring.putalpha(Image.fromarray(np.maximum(0,np.array(rim).astype(int)-np.array(aa).astype(int)).astype('uint8')));ring.alpha_composite(out);out=ring
 return out
def native(im,cell,k,root):
 out=Image.new('RGBA',(cell,cell));s=im.resize((round(im.width*k),round(im.height*k)),Image.Resampling.NEAREST);out.alpha_composite(s,(round(cell/2-root[0]*k),round(cell/2-root[1]*k)));return out
def heading(im,n):return im.rotate(-n*360/32,resample=Image.Resampling.NEAREST,center=(im.width//2,im.height//2))
def bank(name,images,pivot=None,masks=False):
 global pageid
 cw,ch=images[0].size;assert cw%2==ch%2==0 and all(im.size==(cw,ch)for im in images)
 B={'w':cw,'h':ch,'pivot':pivot or[cw//2,ch//2],'frames':len(images),'cells':[]};masklist=[]
 page=Image.new('RGBA',(1024,1024));x=y=rowh=0;pending=[]
 def save():
  global pageid
  if not pending:return
  key='rw117_page_'+str(pageid);filename='page_'+str(pageid)+'.png';page.save(O/filename);M['pages'][key]={'path':REL+filename,'w':1024,'h':1024}
  for row in pending:row[0]=key
  pageid+=1
 for i,im in enumerate(images):
  bb=im.getbbox()or(0,0,2,2);l,t,r,b=bb;sw=r-l;sh=b-t
  if x+sw+2>1024:x=0;y+=rowh+2;rowh=0
  if y+sh+2>1024:save();page=Image.new('RGBA',(1024,1024));x=y=rowh=0;pending=[]
  page.alpha_composite(im.crop(bb),(x,y));cell=[None,x,y,sw,sh,l,t];pending.append(cell);B['cells'].append(cell);x+=sw+2;rowh=max(rowh,sh)
  if masks:
   aa=np.array(im.getchannel('A'));ys,xs=np.where(aa>80)
   if len(xs):l2=int(xs.min());t2=int(ys.min());w2=int(xs.max())-l2+1;h2=int(ys.max())-t2+1;mask=aa[t2:t2+h2,l2:l2+w2]>80
   else:l2=t2=0;w2=h2=2;mask=np.zeros((2,2),bool)
   off=len(bitdata);bitdata.extend(np.packbits(mask.ravel(),bitorder='little').tobytes());masklist.append([l2,t2,w2,h2,off])
 save();M['banks'][name]=B;frames[name]=images
 if masks:M['masks'][name]=masklist
 # Editable untrimmed strip is the source; packed runtime pages restore this canvas.
 strip=Image.new('RGBA',(cw*min(8,len(images)),ch*math.ceil(len(images)/8)))
 for i,im in enumerate(images):strip.alpha_composite(im,(i%8*cw,i//8*ch))
 (O/'strips').mkdir(exist_ok=True);strip.save(O/'strips'/(name+'.png'))

raw=Image.open(W/'razorwake-modular-generated.png').convert('RGBA');parts=[]
for i in range(6):parts.append(cutout(raw.crop((i%3*512,i//3*512,i%3*512+512,i//3*512+512))))
for i,im in enumerate(parts):im.save(W/('piece-'+str(i)+'.png'))
ship=parts[0];central=parts[1];K=.43;CELL=384;ROOT=(256,250)
leftmask=Image.new('L',(512,512));d=ImageDraw.Draw(leftmask);d.polygon([(14,371),(18,226),(51,180),(115,144),(168,146),(219,215),(175,260),(127,267),(82,295),(44,340)],fill=255)
rightmask=leftmask.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
def masked(im,mask):
 out=im.copy();out.putalpha(Image.fromarray(np.minimum(np.array(im.getchannel('A')),np.array(mask))));return out
lw=masked(ship,leftmask);rw=masked(ship,rightmask);hull=ship.copy();a=np.array(hull);a[:,:,3]=np.where(np.maximum(np.array(leftmask),np.array(rightmask))>0,0,a[:,:,3]);hull=Image.fromarray(a);base=central.copy();base.alpha_composite(hull);hull=base
baseh=native(hull,CELL,K,ROOT)
bank('hull',[heading(baseh,n)for n in range(32)],masks=True)
bank('hull_hit',[heading(light(baseh,mode='hit'),n)for n in range(32)])
bank('hull_charge',[light(baseh,level)for level in range(6)])
bank('hull_shadow',[heading(light(baseh,mode='shadow'),n)for n in range(32)])
for side,source,root,sign in [('left',lw,(190,200),-1),('right',rw,(322,200),1)]:
 poses=[]
 for i in range(24):
  ang=math.sin(i/24*math.tau)*.74;co=math.cos(ang);slope=sign*.25*math.sin(ang)
  f=source.transform((512,512),Image.Transform.AFFINE,(1/co,0,root[0]-root[0]/co,-slope/co,1,slope*root[0]/co),Image.Resampling.NEAREST)
  poses.append(native(f,CELL,K,ROOT))
 bank(side,[heading(poses[0],n)for n in range(32)]+poses,masks=True)
 bank(side+'_hit',[heading(light(poses[0],mode='hit'),n)for n in range(32)]+[light(f,mode='hit')for f in poses])
 bank(side+'_charge',[light(f,level)for level in range(6)for f in poses])
 bank(side+'_shadow',[heading(light(poses[0],mode='shadow'),n)for n in range(32)]+[light(f,mode='shadow')for f in poses])

gun=native(parts[4],128,.19,(256,147));gun.save(W/'gun-native.png');spins=[]
capbox=(56,92,73,110);cap=gun.crop(capbox)
for recoil in[0,-3]:
 for f in range(8):
  g=gun.copy();g.alpha_composite(cap.rotate(-f*45,resample=Image.Resampling.NEAREST),(capbox[0],capbox[1]));out=Image.new('RGBA',(128,128));out.alpha_composite(g,(0,recoil));spins.append(out)
bank('gun',[heading(f,n)for f in spins for n in range(32)],masks=True)
bank('gun_hit',[heading(light(f,mode='hit'),n)for f in spins for n in range(32)])
bank('gun_charge',[light(gun,level)for level in range(6)])
stump=gun.copy();stump.paste((0,0,0,0),(0,78,128,128));bank('gun_wreck',[heading(light(stump,mode='wreck'),n)for n in range(32)])
# One flame source; only authored six-step light levels and separate fixed cruise/throttle sizes.
plume=parts[5];bb=plume.getbbox();plume=plume.crop(bb);k=70/plume.height;flame=plume.resize((round(plume.width*k),70),Image.Resampling.NEAREST)
for label,height in [('cruise',70),('throttle',126)]:
 k=height/flame.height;f=flame.resize((round(flame.width*k),height),Image.Resampling.NEAREST);c=Image.new('RGBA',(288,288));c.alpha_composite(f,(144-f.width//2,144-height))
 bank('thrust_'+label,[heading(light(c,level),n)for level in range(6)for n in range(32)])
# Muzzle/slug use this same coherent authored energy source, not a storm-burst/lightning glyph.
slug=flame.resize((6,22),Image.Resampling.NEAREST).transpose(Image.Transpose.FLIP_TOP_BOTTOM);c=Image.new('RGBA',(48,48));c.alpha_composite(slug,(21,13));bank('slug',[heading(light(c,level),n)for level in range(6)for n in range(32)])
m=flame.resize((14,24),Image.Resampling.NEAREST).transpose(Image.Transpose.FLIP_TOP_BOTTOM);c=Image.new('RGBA',(80,80));c.alpha_composite(m,(33,38));bank('muzzle',[heading(light(c,level),n)for level in range(6)for n in range(32)])

t=Image.open(W/'wind-tornado-generated.png').convert('RGBA');tornado=[]
for i in range(16):
 l=round(i%4*t.width/4);rr=round((i%4+1)*t.width/4);top=round(i//4*t.height/4);bot=round((i//4+1)*t.height/4)
 f=cutout(t.crop((l,top,rr,bot)),'wind');f=remove_strips(f);fixed=Image.new('RGBA',(314,314));fixed.alpha_composite(f,(0,0));tornado.append(fixed)
# Common proportional scale and a fixed physical bottom tip; no per-cell fitting.
big=[];small=[];swirl=[]
for f in tornado:
 g=f.resize((214,214),Image.Resampling.NEAREST);c=Image.new('RGBA',(256,256));c.alpha_composite(g,(21,20));big.append(c)
 g=f.resize((92,92),Image.Resampling.NEAREST);c=Image.new('RGBA',(128,128));c.alpha_composite(g,(18,16));small.append(c)
 g=f.crop((0,0,314,130)).resize((220,92),Image.Resampling.NEAREST);c=Image.new('RGBA',(256,128));c.alpha_composite(g,(18,18));swirl.append(c)
bank('tornado',big,pivot=[128,154]);bank('cyclone',small)
bank('swirl',swirl)
grow=[];fade=[]
for i in range(8):
 k=(i+1)/8;g=big[i].resize((round(256*k),round(256*k)),Image.Resampling.NEAREST);c=Image.new('RGBA',(256,256));c.alpha_composite(g,(128-round(128*k),154-round(154*k)));grow.append(c)
 g=np.array(big[i]);g[:,:,3]=(g[:,:,3].astype(float)*(1-(i+1)/8)).astype('uint8');fade.append(Image.fromarray(g))
bank('tornado_grow',grow,pivot=[128,154]);bank('tornado_tail',fade,pivot=[128,154])
# Original source-derived real roll views stay available through FB112; no cropped wing masks.
M['model']={'cell':384,'world':250,'engines':[[178,107],[206,107]],'guns':[{'mount':[151,189],'bore':[0,40],'size':128,'recoilOffset':-3},{'mount':[233,189],'bore':[0,40],'size':128,'recoilOffset':-3}],'core':[192,210],'coreBox':[52,76],'bodyBox':[220,200],'shear':[[151,189],[233,189]],'clips':{'idle':0,'brake':2,'roll':[0,4,5,6,7,8,9,10]}}
M['maskBytes']=len(bitdata);M['maskPath']=REL+'opaque_masks.bin';(O/'opaque_masks.bin').write_bytes(bitdata)
M['sourceHashes']={p.name:hashlib.sha256(p.read_bytes()).hexdigest()for p in[W/'razorwake-modular-generated.png',W/'wind-tornado-generated.png']}
(O/'manifest.json').write_text(json.dumps(M,separators=(',',':')))
(W/'razorwake_modular_art_1104.js').write_text("'use strict';\nconst RW117_ART="+json.dumps(M,separators=(',',':'))+';\n',encoding='utf8')
lua="""local D=app.params['out'];local f=io.open(D..'/manifest.json','r');local M=json.decode(f:read('*a'));f:close()
for n,a in pairs(M.banks)do local im=Image{fromFile=D..'/strips/'..n..'.png'};local s=Sprite(a.w,a.h,ColorMode.RGB)
for i=0,a.frames-1 do if i>0 then s:newEmptyFrame()end;local c=Image(im,Rectangle(i%8*a.w,math.floor(i/8)*a.h,a.w,a.h));s:newCel(s.layers[1],i+1,c,Point(0,0));s.frames[i+1].duration=1/24 end;s:saveAs(D..'/'..n..'.aseprite');s:close()end"""
(O/'author.lua').write_text(lua);subprocess.run([r'C:/Users/Mike/Desktop/Retro Dev Tools/Graphics/Aseprite/aseprite.exe','--batch','--script-param','out='+O.as_posix(),'--script',str(O/'author.lua')],check=True)
preview=Image.new('RGBA',(1152,768),(7,17,24,255))
for i,pose in enumerate([0,6,18]):
 c=frames['hull'][0].copy();c.alpha_composite(frames['left'][32+pose]);c.alpha_composite(frames['right'][32+pose]);preview.alpha_composite(c,(i*384,0))
for i,name in enumerate(['gun','tornado','thrust_throttle']):preview.alpha_composite(frames[name][0],(i*384+80,420))
preview.save(W/'kit-review.png');print('AUTHORED',sum(b['frames']for b in M['banks'].values()),'frames',len(M['banks']),'banks',len(M['pages']),'pages',len(bitdata),'mask bytes')
