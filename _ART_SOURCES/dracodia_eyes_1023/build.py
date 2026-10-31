from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,math,hashlib
from scipy.ndimage import label
R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');B=R/'_ART_SOURCES/dracodia_brain_1023';W=Path(__file__).resolve().parent;O=W/'shipping';O.mkdir(exist_ok=True)
A={'owner':'_BUILD_SOURCE/build_dracodia_brain_1023.py','banks':{},'sheets':{},'pivot':[192,192],'eyes':[[158,228],[216,228]],'beamWidths':[8,16,26,38,52,64],'beamLength':600,'geyserHalf':26,'geyserHeight':154,'jobs':{**json.loads((B/'jobs.json').read_text()),**json.loads((W/'jobs.json').read_text())}};audit=[]
def hard(im):
 a=np.array(im.convert('RGBA'));a[:,:,3]=np.where(a[:,:,3]>127,255,0);return Image.fromarray(a)
def raw(name,i=0):
 p=W/'raw'/name/f'{i:02}.png'
 if not p.exists():p=B/'raw'/name/f'{i:02}.png'
 return hard(Image.open(p))
def eyes(im):
 a=np.array(im);yy,xx=np.indices(a.shape[:2]);out=[]
 for cx in [105,143]:
  roi=(abs(xx-cx)<=13)&(abs(yy-152)<=9)&(a[:,:,3]>0)
  warm=roi&(a[:,:,0]>150)&(a[:,:,0]>a[:,:,1]*1.3)&(a[:,:,0]>a[:,:,2]*1.1)
  # Match the white pupil within its warm socket, excluding the chrome brow.
  from scipy.ndimage import binary_dilation,center_of_mass
  hot=roi&binary_dilation(warm,iterations=2)&(a[:,:,:3].min(2)>190)
  mask=hot if hot.sum()>=2 else warm
  if not mask.any():raise ValueError('No visible eye at '+str(cx))
  y,x=center_of_mass(mask);out.append([round(x*1.5),round(y*1.5)])
 return out
def white(im):
 c=Image.new('RGBA',im.size,'white');c.putalpha(im.getchannel('A'));return c
def emit(name,ims,pivot,cols=4,hit=False):
 w,h=ims[0].size;assert w%2==h%2==0;sheet=Image.new('RGBA',(cols*w,math.ceil(len(ims)/cols)*h));rows=[]
 for i,im in enumerate(ims):
  assert im.size==(w,h);b=im.getbbox();assert b and b[0]>0 and b[1]>0 and b[2]<w and b[3]<h,(name,i,b)
  rect=[i%cols*w,i//cols*h,w,h];sheet.alpha_composite(im,rect[:2]);rows.append({'key':f'nb23_{name}_{i}','sheet':'nb23_'+name,'cell':rect,'w':w,'h':h,'pivot':list(pivot),'bounds':list(b)})
  audit.append({'key':rows[-1]['key'],'size':[w,h],'bounds':list(b),'even':True,'noClip':True,'binary':set(np.unique(np.asarray(im)[:,:,3])).issubset({0,255})})
 path=O/(name+'.webp');sheet.save(path,lossless=True,exact=True);A['sheets']['nb23_'+name]={'key':'nca_nb23_'+name,'path':'assets/game/levels/stage_08/boss/neural_archon_1023/'+path.name,'w':sheet.width,'h':sheet.height,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()};A['banks'][name]=rows
 return rows
seed=raw('brain');brain=[raw('brain_anim',i).resize((384,384),Image.Resampling.NEAREST)for i in range(9)]
# Eyes/brow remain original pixels in EVERY whole-body frame. Never paste a
# stationary face rectangle onto the live lobes. Origins follow measured eyes.
for name,source_ids,raw_name in [('brain',list(range(9)),'brain_anim'),('charge',list(range(8)),'charge'),('focus',[5,6,7,6],'charge')]:
 frames=[raw(raw_name,i).resize((384,384),Image.Resampling.NEAREST)for i in source_ids]
 rows=emit(name,frames,(192,192));emit(name+'_hit',[white(im)for im in frames],(192,192))
 for i,(a,source)in enumerate(zip(rows,source_ids)):
  a['white']=f'nb23_{name}_hit_{i}';a['eyes']=eyes(raw(raw_name,source));a['sourceFrame']=source
charge=[raw('charge',i).resize((384,384),Image.Resampling.NEAREST)for i in range(8)]
cloud=[raw('cloud_anim',i).resize((384,384),Image.Resampling.NEAREST)for i in range(9)]
emit('cloud',cloud,(192,192))
# A short non-protective startup/break bank uses the generated sparser smoke
# lobes as authored source pixels, with no runtime fading or tint.
opened=[]
for im in cloud:
 a=np.array(im);yy,xx=np.indices(a.shape[:2]);a[((xx-192)**2+(yy-192)**2)<122**2,3]=0;opened.append(Image.fromarray(a))
emit('cloud_open',opened,(192,192))
geyser=[]
# Reject source7/8: they re-ignite after the eruption has already subsided.
for i in [6,0,1,2,3,4,5,6]:
 im=raw('geyser_anim',i);v=np.array(im);rgb=v[:,:,:3].astype(float);m=(rgb[:,:,1]>rgb[:,:,0]*1.2)&(rgb[:,:,2]>rgb[:,:,0]*1.2)&(v[:,:,3]>0);bright=rgb.max(2)
 for channel,f in enumerate([.78,.28,1]):v[:,:,channel][m]=np.clip(bright[m]*f,0,255).astype('uint8')
 im=Image.fromarray(v);c=Image.new('RGBA',(144,208));c.alpha_composite(im,(8,8));geyser.append(c)
emit('geyser',geyser,(72,178))
# Exact generated dissolve is played backward to build the form and forward
# to remove it. One proportional actor scale, same pivot across both paths.
morph=[raw('morph_anim',i).resize((384,384),Image.Resampling.NEAREST)for i in range(9)]
morph[0]=brain[0]
# PixelLab left a persistent face. Author a fixed12px digital breakup map
# into the intact connected pixels, retaining its detached generated sparks.
# These are saved RGBA poses; there is no runtime fade, mask or new particle rig.
order=np.array([[0,8,2,10],[12,4,14,6],[3,11,1,9],[15,7,13,5]])
for i in range(3,9):
 a=np.array(morph[i]);lab,n=label(a[:,:,3]>0);yy,xx=np.indices(lab.shape);rank=order[(yy//12)%4,(xx//12)%4];threshold=[0,0,0,2,5,8,11,14,16][i]
 for k in range(1,n+1):
  m=lab==k
  if m.sum()>220 and np.any(m&(xx>130)&(xx<250)&(yy>120)&(yy<300)):a[m&(rank<threshold),3]=0
 rgb=a[:,:,:3].astype(float);m=(rgb[:,:,2]>rgb[:,:,0]*1.25)&(rgb[:,:,1]>rgb[:,:,0]*1.1)&(a[:,:,3]>0);bright=rgb.max(2)
 for channel,f in enumerate([.78,.28,1]):a[:,:,channel][m]=np.clip(bright[m]*f,0,255).astype('uint8')
 morph[i]=Image.fromarray(a)
emit('morph',list(reversed(morph)),(192,192))
# Generated straight beam, six fully baked expansion levels and two flicker
# phases. No live transform/rotation/alpha enhancement of the new attack.
for step,width in enumerate(A['beamWidths']):
 ims=[]
 for i in range(1,17):
  im=raw('laser_new',i).crop((20,24,44,172));v=np.array(im)
  # PixelLab periodically dimmed the entire core. Preserve a small white-hot
  # authored core within its actual red energy pixels in each generated row;
  # the16 different flowing packet/edge shapes and alpha remain intact.
  for y in range(v.shape[0]):
   candidates=np.where((v[y,:,0]>180)&(v[y,:,0]>v[y,:,1]*1.2)&(v[y,:,3]>0))[0]
   candidates=[int(x)for x in candidates if 5<=x<=18]
   if candidates:
    mid=sum(candidates)/len(candidates)
    for x in sorted(candidates,key=lambda x:abs(x-mid))[:2]:v[y,x,:3]=[255,240,255]
  im=Image.fromarray(v);out=im.resize((width,600),Image.Resampling.NEAREST);c=Image.new('RGBA',(104,624));c.alpha_composite(out,((104-out.width)//2,12));ims.append(c)
 emit('beam_'+str(step),ims,(52,12))
for color,file in [('green','fov-light-green.png'),('yellow','fov-yellow.png'),('red','fov-neon-red.png')]:
 source=Image.open(R/'assets/bossmode/ui'/file).convert('RGBA').crop((0,0,640,640));source=source.crop(source.getbbox())
 # The center of the existing authored FOV plate supplies flat parallel lanes.
 band=source.crop((source.width//2-24,source.height//3,source.width//2+24,source.height-12))
 for name,size,pivot,pos in [('laser',(128,624),(64,12),(8,12)),('geyser',(80,192),(40,174),(8,12))]:
  c=Image.new('RGBA',size);material=band.resize((112,600)if name=='laser'else(64,162),Image.Resampling.NEAREST);c.alpha_composite(material,pos);emit('warn_'+name+'_'+color,[c],pivot,cols=1)
(O/'manifest.json').write_text(json.dumps(A,indent=2));(W/'brain_art.js').write_text("'use strict';\nconst NB23_ART="+json.dumps(A,separators=(',',':'))+';\n',encoding='utf-8');(W/'asset-audit.json').write_text(json.dumps(audit,indent=2))
for name,frames in [('brain',brain),('charge',charge),('cloud',cloud),('geyser',geyser),('morph',morph)]:
 c=Image.new('RGB',(384*3,414*3),(18,26,40));d=ImageDraw.Draw(c)
 for i,im in enumerate(frames):
  q=im.copy();q.thumbnail((370,380),Image.Resampling.NEAREST);x=i%3*384;y=i//3*414;c.paste(q,(x+(384-q.width)//2,y+24),q);d.text((x+10,y+5),f'{name} {i}',fill='white')
 c.save(W/(name+'-review.png'))
print(json.dumps({'cells':len(audit),'sheets':len(A['sheets']),'evenNoClip':all(a['even']and a['noClip']for a in audit)}))
