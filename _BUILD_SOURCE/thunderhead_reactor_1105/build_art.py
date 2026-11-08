"""TC119: author the approved Thunderhead's connectors, chamber, depth and debris.
All resizing, turning, emission and alpha changes occur here, before export.
"""
from pathlib import Path
import math,json,hashlib,subprocess
import numpy as np
from PIL import Image,ImageDraw,ImageFilter
W=Path(__file__).resolve().parent
R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury')
O=W/'authored';O.mkdir(exist_ok=True)
REL='assets/game/levels/stage_06/boss/thunderhead_reactor_1105/'
M={'banks':{},'pages':{},'masks':{},'depths':[round(1-i*.04,2)for i in range(16)],
   'contract':'Fixed even source-over cells; approved TM115/THS114 pixels; all depth/turn/glow/debris frames authored offline.'}
bits=bytearray();frames={};pageid=0;cache={}
OLD=json.loads((R/'assets/game/levels/stage_06/boss/thunderhead_modular_1104/manifest.json').read_text())
ST=json.loads((R/'assets/game/levels/stage_06/boss/thunderhead_storm_1104/manifest.json').read_text())
RW=json.loads((R/'assets/game/levels/stage_06/miniboss/razorwake_modular_1104/manifest.json').read_text())
def source(meta,name,i=0):
 b=meta['banks'][name];c=b['cells'][i];key=c[0]
 if key not in cache:
  p=meta.get('pages',{}).get(key)
  if p:path=p['path']
  else:path=next(p['path']for p in b['pages']if p['key']==key)
  cache[key]=Image.open(R/path).convert('RGBA')
 cw=b.get('cw',b.get('w'));ch=b.get('ch',b.get('h'))
 if len(c)>3:
  out=Image.new('RGBA',(cw,ch));out.alpha_composite(cache[key].crop((c[1],c[2],c[1]+c[3],c[2]+c[4])),(c[5],c[6]));return out
 return cache[key].crop((c[1],c[2],c[1]+cw,c[2]+ch))
def bank(name,images,pivot=None,mask=False):
 global pageid
 cw,ch=images[0].size;assert cw%2==ch%2==0 and all(im.size==(cw,ch)for im in images)
 b={'w':cw,'h':ch,'pivot':pivot or[cw//2,ch//2],'frames':len(images),'cells':[]}
 page=Image.new('RGBA',(1024,1024));x=y=rowh=0;pending=[];ms=[]
 def save():
  global pageid
  if not pending:return
  bb=page.getbbox()or(0,0,2,2);pw=math.ceil(bb[2]/2)*2;ph=math.ceil(bb[3]/2)*2
  key='tc119_page_'+str(pageid);file='page_'+str(pageid)+'.png';page.crop((0,0,pw,ph)).save(O/file)
  M['pages'][key]={'path':REL+file,'w':pw,'h':ph}
  for c in pending:c[0]=key
  pageid+=1
 for im in images:
  l,t,r,bottom=im.getbbox()or(0,0,2,2);sw=r-l;sh=bottom-t
  if x+sw+2>1024:x=0;y+=rowh+2;rowh=0
  if y+sh+2>1024:save();page=Image.new('RGBA',(1024,1024));x=y=rowh=0;pending=[]
  page.alpha_composite(im.crop((l,t,r,bottom)),(x,y));c=[None,x,y,sw,sh,l,t];b['cells'].append(c);pending.append(c);x+=sw+2;rowh=max(rowh,sh)
  if mask:
   a=np.array(im.getchannel('A'))>80;yy,xx=np.where(a);l2=int(xx.min());t2=int(yy.min());w2=int(xx.max())-l2+1;h2=int(yy.max())-t2+1
   off=len(bits);bits.extend(np.packbits(a[t2:t2+h2,l2:l2+w2].ravel(),bitorder='little').tobytes());ms.append([l2,t2,w2,h2,off])
 save();M['banks'][name]=b;frames[name]=images
 if mask:M['masks'][name]=ms
 (O/'strips').mkdir(exist_ok=True);strip=Image.new('RGBA',(cw*min(8,len(images)),ch*math.ceil(len(images)/8)))
 for i,im in enumerate(images):strip.alpha_composite(im,(i%8*cw,i//8*ch))
 strip.save(O/'strips'/(name+'.png'));print('BANK',name,len(images),flush=True)
def turn(im,d,dirs=32):return im.rotate(-d*360/dirs,Image.Resampling.NEAREST,center=(im.width//2,im.height//2))
def depth(im,s):
 w=math.ceil(im.width*s/2)*2;h=math.ceil(im.height*s/2)*2
 # Uniform proportional scale, centred in a shared padded even canvas.
 out=Image.new('RGBA',(w+4,h+4));f=im.resize((round(im.width*s),round(im.height*s)),Image.Resampling.NEAREST);out.alpha_composite(f,((out.width-f.width)//2,(out.height-f.height)//2));return out
def white(im):
 f=Image.new('RGBA',im.size,'white');f.putalpha(im.getchannel('A'));return f
def emit(im,l,phase):
 a=np.array(im);v=a[:,:,:3].astype(float);active=(a[:,:,1]>a[:,:,0]*1.13)&(a[:,:,2]>a[:,:,0]*1.05)&(a[:,:,3]>0)
 v[active]=np.minimum(255,v[active]*(1+l*.09)+np.array([l*13,l*19,l*17])*[.65,1,.8,1][phase%4]);a[:,:,:3]=v.astype('uint8');return Image.fromarray(a)

# The core uses the real cyclone texture inside the original glass, with all
# chrome, central brace and seams preserved. The texture rotates and rises north.
core=source(OLD,'core');a=np.array(core);v=a[:,:,:3].astype(int);glassmask=Image.new('L',core.size);gd=ImageDraw.Draw(glassmask);gd.polygon([(54,67),(88,58),(89,160),(54,168)],fill=255);gd.polygon([(104,58),(139,67),(139,168),(103,160)],fill=255);glass=(np.array(glassmask)>0)&(a[:,:,3]>0)
flows=[]
for level in range(4):
 for phase in range(24):
  tile=source(ST,'tempest',phase).resize((168,168),Image.Resampling.NEAREST)
  layer=Image.new('RGBA',core.size);shift=(phase*9)%168
  for y in range(-168,336,168):layer.alpha_composite(tile,(12,y-shift))
  wind=np.array(layer);out=a.copy();mix=.80+level*.05;rgb=out[:,:,:3].astype(float)
  rgb[glass]=np.minimum(255,v[glass]*(1-mix)+wind[:,:,:3][glass]*mix+np.array([4,level*7,level*7]));out[:,:,:3]=rgb.astype('uint8');flows.append(Image.fromarray(out))

# Foreground plus four actual depth sizes, with independently owned modules.
for di,s in enumerate(M['depths']):
 for n in ['hull','core','pod0','pod1']:
  original=flows if n=='core'else[source(OLD,n,i)for i in range(OLD['banks'][n]['frames'])]
  for face in ([0,1]if di in[0,len(M['depths'])-1]else[0]):
   used=original if face==0 and di in[0,len(M['depths'])-1]else original[:24 if n=='core'else 8 if n.startswith('pod')else 4]
   bank(n+'_d'+str(di)+'_'+str(face),[depth(turn(im,16*face),s)for im in used])
 # Neutral turn plates permit a visible turn north without instant sprite flips.
 for n in (['hull','core','pod0','pod1']if di in[0,len(M['depths'])-1]else[]):
  im=source(OLD,n);cell=math.ceil(math.hypot(*im.size)/2)*2+4;c=Image.new('RGBA',(cell,cell));c.alpha_composite(im,((cell-im.width)//2,(cell-im.height)//2))
  bank(n+'_turn_d'+str(di),[depth(turn(c,i,16),s)for i in range(16)])

# Full directional gun ownership, recoil and material emission; exact base masks.
g=source(OLD,'gun');guns=[]
for level in range(4):
 for phase in range(4):
  for recoil in[0,1]:
   f=emit(source(OLD,'gun',3 if recoil else 0),level,phase)
   for d in range(32):guns.append(turn(f,d))
bank('gun',guns)
bank('gun_mask',[turn(source(OLD,'gun',3 if r else 0),d)for r in[0,1]for d in range(32)],mask=True)
bank('gun_hit',[white(im)for im in frames['gun_mask']])
for di,s in enumerate(M['depths'][1:],1):bank('gun_d'+str(di),[depth(turn(g,d),s)for d in range(32 if di==len(M['depths'])-1 else 1)])

# The approved single-source exhaust remains anchored while the ship flies in depth.
XR=json.loads((R/'assets/game/levels/stage_06/miniboss/razorwake_tempest_1105/manifest.json').read_text())
for di,s in enumerate(M['depths']):
 for mode in ['cruise','throttle']:
  bank('thrust_'+mode+'_d'+str(di),[depth(source(XR,'thrust_'+mode,(1+phase)*32+d*2),s)for phase in range(4)for d in range(16 if di in[0,len(M['depths'])-1]else 1)])

# Authentic beam throat: wind texture narrows into the outlet and flares into
# the existing approved beam. A restored lower metal lip overlaps the root.
couplers=[]
for i in range(16):
 b=source(OLD,'wind_beam',6+i);out=Image.new('RGBA',(208,160))
 for y in range(112):
  width=round(82+min(y,90)*1.18);row=b.crop((0,min(110,y+3),288,min(110,y+3)+1)).resize((width,1),Image.Resampling.NEAREST);out.alpha_composite(row,((208-width)//2,26+y))
 # Source fan disc lights the physical opening instead of a floating flare.
 fan=source(OLD,'pod0').crop((51,220,141,253));fan=emit(fan,3,i%4);out.alpha_composite(fan,(59,8));couplers.append(out)
bank('beam_coupling',couplers,pivot=[104,25])
recovery=[]
for i in range(6):
 im=couplers[(i+8)%16].copy();ar=np.array(im);ar[:,:,3]=(ar[:,:,3].astype(float)*(5-i)/6).astype('uint8');recovery.append(Image.fromarray(ar))
bank('beam_coupling_tail',recovery,pivot=[104,25])
for i in[0,1]:
 p=source(OLD,'pod'+str(i));arr=np.array(p);yy,xx=np.indices(arr.shape[:2]);ellipse=((xx-96)/43)**2+((yy-237.28)/17)**2
 keep=(yy>=237)&(yy<261)&(ellipse>=.82)&(abs(xx-96)<60);arr[~keep]=0;bank('pod'+str(i)+'_lip',[Image.fromarray(arr)])

# Physical, coloured breakaway parts and smaller shards; no mounted wreck plate.
for n in ['gun','pod0','pod1']:
 im=source(OLD,n);side=math.ceil(math.hypot(*im.size)/2)*2+8;c=Image.new('RGBA',(side,side));c.alpha_composite(im,((side-im.width)//2,(side-im.height)//2))
 bank(n+'_detach',[turn(c,d)for d in range(32)])
 bb=im.getbbox();f=im.crop(bb);chunk=Image.new('RGBA',(80,80));piece=f.crop((0,0,max(2,f.width//2),max(2,f.height//3)));piece.thumbnail((44,48),Image.Resampling.NEAREST);chunk.alpha_composite(piece,((80-piece.width)//2,(80-piece.height)//2));bank(n+'_shard',[turn(chunk,d,16)for d in range(16)])
# A small exposed mechanical receiver sits on the hull after the complete gun leaves.
socket=source(OLD,'gun').crop((48,48,144,144));ar=np.array(socket);yy,xx=np.indices(ar.shape[:2]);inner=(xx-48)**2+(yy-48)**2<24**2;ar[inner,:3]=(ar[inner,:3].astype(float)*.35).astype('uint8');ar[:,:,3]=np.where((xx-48)**2+(yy-48)**2<43**2,ar[:,:,3],0);bank('socket',[Image.fromarray(ar)])

# The same approved large cyclone, now authored at successive perspective sizes.
M['cycloneSizes']=[64,80,96,112,128,144,160,176,192,208,224,240,256,288,320,352]
for j,d in enumerate(M['cycloneSizes']):
 images=[]
 for i in range(0,24,2):
  im=source(ST,'tempest',i).resize((d,d),Image.Resampling.NEAREST);out=Image.new('RGBA',(d+8,d+8));out.alpha_composite(im,(4,4));images.append(out)
 bank('cyclone_'+str(j),images)
bank('shade',[Image.new('RGBA',(340,256),(1,7,13,round(i/15*155)))for i in range(16)])
M['banks']['shade']['edgePolicy']='Intentional full-bleed background fading tile.'
M['model']=OLD['model'];M['maskPath']=REL+'opaque_masks.bin';M['maskBytes']=len(bits);(O/'opaque_masks.bin').write_bytes(bits)
M['sources']={n:hashlib.sha256((R/p).read_bytes()).hexdigest()for n,p in [('TM115','assets/game/levels/stage_06/boss/thunderhead_modular_1104/manifest.json'),('THS114','assets/game/levels/stage_06/boss/thunderhead_storm_1104/manifest.json')]}
(O/'manifest.json').write_text(json.dumps(M,separators=(',',':')));(W/'thunderhead_reactor_art_1105.js').write_text("'use strict';\nconst TC119_ART="+json.dumps(M,separators=(',',':'))+';\n')
lua="""local D=app.params.out;local f=io.open(D..'/manifest.json','r');local M=json.decode(f:read('*a'));f:close()
for n,a in pairs(M.banks)do local im=Image{fromFile=D..'/strips/'..n..'.png'};local s=Sprite(a.w,a.h,ColorMode.RGB)
for i=0,a.frames-1 do if i>0 then s:newEmptyFrame()end;s:newCel(s.layers[1],i+1,Image(im,Rectangle(i%8*a.w,math.floor(i/8)*a.h,a.w,a.h)),Point(0,0));s.frames[i+1].duration=1/24 end;s:saveAs(D..'/'..n..'.aseprite');s:close()end"""
(O/'author.lua').write_text(lua);subprocess.run([r'C:/Users/Mike/Desktop/Retro Dev Tools/Graphics/Aseprite/aseprite.exe','--batch','--script-param','out='+O.as_posix(),'--script',str(O/'author.lua')],check=True)
print('ART',sum(b['frames']for b in M['banks'].values()),len(M['banks']),len(M['pages']),round(sum(p['w']*p['h']*4 for p in M['pages'].values())/1048576,1),'MiB',flush=True)
