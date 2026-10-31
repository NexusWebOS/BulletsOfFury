"""Extract original authored sheets, register roots, preserve one scale per bank.

No drawing or synthetic inbetweens: exports only crop/nearest-scale/pad authored
pixels. Sources, exact rectangles, anchors, alpha audits and review contacts stay.
"""
from pathlib import Path
import json,hashlib,statistics
import numpy as np
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'expansion/topdown/art/bastion_1013';SRC=OUT/'source';FR=OUT/'frames'
REVIEW=ROOT/'_shots/bastion_1013';FR.mkdir(parents=True,exist_ok=True);REVIEW.mkdir(parents=True,exist_ok=True)
D={'version':'1013-bastion-r1','assets':{},'sequences':{},'audit':[],'sources':{}}
def save(key,im,anchor,src,rect,scale):
 a=im.getchannel('A');box=a.getbbox();assert box,(key,'empty')
 assert all(n%2==0 for n in im.size),(key,im.size)
 if key!='pb_stage':assert box[0]>0 and box[1]>0 and box[2]<im.width and box[3]<im.height,(key,box,im.size)
 path=FR/(key+'.png');im.save(path,optimize=True)
 D['assets'][key]={'file':path.relative_to(ROOT).as_posix(),'size':list(im.size),'anchor':anchor,'bounds':box}
 D['audit'].append({'key':key,'source':src,'crop':rect,'scale':scale,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
def row(src,prefix,n,y0,y1,kind='actor',scale=1,cellsize=(320,320),baseline=284):
 sheet=Image.open(SRC/src).convert('RGBA');cells=[];rects=[]
 for j in range(n):
  rect=(round(j*sheet.width/n),y0,round((j+1)*sheet.width/n),y1);im=sheet.crop(rect)
  im.putalpha(im.getchannel('A').point(lambda a:255 if a>=128 else 0));cells.append(im);rects.append(rect)
 boxes=[im.getchannel('A').getbbox() for im in cells]
 base=statistics.median(b[3] for b in boxes);keys=[]
 for j,(im,b,rect) in enumerate(zip(cells,boxes,rects)):
  a=np.asarray(im);cx=im.width/2
  if kind=='yuri':
   mask=(a[:,:,0]>60)&(a[:,:,0]>a[:,:,1]*1.5)&(a[:,:,0]>a[:,:,2]*1.3)&(a[:,:,3]>128)
   mask[round(b[1]+(b[3]-b[1])*.58):]=False;yy,xx=np.where(mask)
   if len(xx)>20:cx=float(np.median(xx))
  elif kind=='enemy':
   mask=a[:,:,3]>128;mask[round(b[1]+(b[3]-b[1])*.3):]=False;yy,xx=np.where(mask)
   if len(xx)>20:cx=float(np.median(xx))
  elif kind in ('center','wall'):cx=statistics.median((q[0]+q[2])/2 for q in boxes)
  if kind=='center':cy=statistics.median((q[1]+q[3])/2 for q in boxes);anchor=[cellsize[0]//2,cellsize[1]//2]
  else:cy=base;anchor=[cellsize[0]//2,baseline]
  cut=im.crop(b);size=(round(cut.width*scale),round(cut.height*scale));offset=(round(anchor[0]+(b[0]-cx)*scale),round(anchor[1]+(b[1]-cy)*scale))
  assert offset[0]>0 and offset[1]>0 and offset[0]+size[0]<cellsize[0] and offset[1]+size[1]<cellsize[1],(prefix,j,offset,size)
  frame=Image.new('RGBA',cellsize);frame.alpha_composite(cut.resize(size,Image.Resampling.NEAREST),offset)
  key=f'{prefix}_{j}';save(key,frame,anchor,src,rect,scale);keys.append(key)
  if prefix.startswith('pb_yuri_') and prefix!='pb_yuri_death':
   # Barrel socket uses actual dark gun pixels beside the head, not feet.
   px=np.asarray(frame).astype('int16');bb=D['assets'][key]['bounds'];yy,xx=np.indices(px.shape[:2]);rgb=px[:,:,:3]
   gun=(px[:,:,3]>0)&(xx>anchor[0]+16)&(yy>=bb[1]+8)&(yy<bb[1]+65)&((rgb.max(2)-rgb.min(2))<28)&(rgb.max(2)<150)&(rgb.max(2)>14)
   gy,gx=np.where(gun);tip=int(np.percentile(gx,99)) if len(gx)>8 else anchor[0]+44
   ys=gy[gx>=tip-3];D['assets'][key]['muzzle']=[tip,float(np.median(ys)) if len(ys) else bb[1]+35]
   if prefix=='pb_yuri_fire':
    # Pixel-reviewed metal barrel endpoints. In flash frames the bright cone
    # fools a dark-color search into choosing the trigger hand below it.
    D['assets'][key]['muzzle']=[[211,102],[197,97],[211,100],[195,97],[209,100],[194,97],[209,103],[196,98]][j]
 D['sequences'][prefix]={'frames':keys,'fps':12,'scale':scale,'rootContract':{'cell':cellsize,'anchor':anchor,'method':'fixed proportional bank scale, chest/head root registration; original authored feet baseline'},'contacts':[0,n//2]}
 # Side-by-side contact and previous/current/next alpha overlay, real pixels.
 thumb=Image.new('RGBA',(n*cellsize[0],cellsize[1]),(12,22,29,255))
 for j,k in enumerate(keys):thumb.alpha_composite(Image.open(FR/(k+'.png')),(j*cellsize[0],0))
 thumb.convert('RGB').save(REVIEW/(prefix+'_contact.png'))
 onion=Image.new('RGBA',(cellsize[0]*n,cellsize[1]),(12,22,29,255))
 for j,k in enumerate(keys):
  for idx,alpha in [((j-1)%n,80),((j+1)%n,80),(j,210)]:
   q=Image.open(FR/(keys[idx]+'.png'));q.putalpha(q.getchannel('A').point(lambda a:a*alpha//255));onion.alpha_composite(q,(j*cellsize[0],0))
  d=ImageDraw.Draw(onion);d.line((j*cellsize[0]+anchor[0],0,j*cellsize[0]+anchor[0],cellsize[1]),fill=(70,180,255,255));d.line((j*cellsize[0],anchor[1],(j+1)*cellsize[0],anchor[1]),fill=(70,180,255,255))
 onion.convert('RGB').save(REVIEW/(prefix+'_onion.png'))
plate=Image.open(SRC/'stage.png').convert('RGBA').resize((640,480),Image.Resampling.NEAREST);save('pb_stage',plate,[320,240],'stage.png',[0,0,1448,1086],640/1448)
for i,name in enumerate(['strafe','rise','fire','death']):row('yuri.png','pb_yuri_'+name,8,i*256,(i+1)*256,'actor' if name=='death' else 'yuri')
for i,name in enumerate(['heavy','rifle','rocket','laser']):row('enemies.png','pb_'+name,6,i*256,(i+1)*256,'enemy')
row('props.png','pb_core',4,0,448,'center',.78,(384,384))
row('props.png','pb_turret',4,448,772,'center',.95,(384,384))
row('props.png','pb_wall',4,772,1086,'wall',.95,(384,384),350)
for i,name in enumerate(['run','throw','jump','lightning']):row('helios.png','pb_helios_'+name,6,i*256,(i+1)*256,'actor',1,(384,384),340)
row('fx.png','pb_orb',6,0,286,'center',.92,(384,384))
for i in range(2):row('lightning.png','pb_lightning_part'+str(i),3,i*512,(i+1)*512,'center',.68,(384,384))
light=[]
for i in range(6):
 old='pb_lightning_part'+str(i//3)+'_'+str(i%3);new='pb_lightning_'+str(i);(FR/(new+'.png')).write_bytes((FR/(old+'.png')).read_bytes());D['assets'][new]=dict(D['assets'][old],file=(FR/(new+'.png')).relative_to(ROOT).as_posix());light.append(new)
D['sequences']['pb_lightning']={'frames':light,'fps':12,'scale':.68}
# Geyser was regenerated separately so the tall apex is never cropped by a bolt row.
im=Image.open(SRC/'geyser.png');half=im.height//2
for i in range(2):row('geyser.png','pb_geyser_part'+str(i),3,i*half,(i+1)*half,'actor',.65,(384,384),356)
g=[]
for i in range(6):
 old='pb_geyser_part'+str(i//3)+'_'+str(i%3);new='pb_geyser_'+str(i);(FR/(new+'.png')).write_bytes((FR/(old+'.png')).read_bytes());D['assets'][new]=dict(D['assets'][old],file=(FR/(new+'.png')).relative_to(ROOT).as_posix());g.append(new)
D['sequences']['pb_geyser']={'frames':g,'fps':12,'scale':.65}
for path in SRC.glob('*.png'):D['sources'][path.name]=hashlib.sha256(path.read_bytes()).hexdigest()
(OUT/'manifest.js').write_text('window.TD_BASTION_ART='+json.dumps(D,separators=(',',':'))+';\n',encoding='utf-8')
(OUT/'manifest.json').write_text(json.dumps(D,indent=2),encoding='utf-8')
print(json.dumps({'assets':len(D['assets']),'sequences':len(D['sequences']),'sources':len(D['sources'])}))
