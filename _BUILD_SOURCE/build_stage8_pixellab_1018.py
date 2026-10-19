"""Own Stage 8 PixelLab loose cells, module masks, registration and preview.

No per-frame fitting, rotations or interpolated animation frames. Each source
pixel belongs to exactly one module and their reconstruction is RGBA exact.
"""
from pathlib import Path
import json,hashlib,math,sys
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,distance_transform_edt
R=Path(__file__).resolve().parents[1];S=R/'_ART_SOURCES/stage8_pixellab_1018'
O=R/'assets/game/levels/stage_08/boss/pixellab_1018';Q=R/'_shots/stage8_pixellab_1018/export'
O.mkdir(parents=True,exist_ok=True);Q.mkdir(parents=True,exist_ok=True)
NAMES=['infused','ghost','colossus','hammer','helicopter','harrier','volcano']
# Anatomical lasso masks for attached armor. Transparent socket gaps in the
# three exploded kits are segmented using their actual connected components.
POLYS={
 'ghost': [[(0,94),(99,94),(103,133),(97,183),(100,256),(0,256)],[(157,94),(256,94),(256,256),(155,256),(160,183),(153,133)]],
 'harrier': [[(0,98),(85,98),(88,146),(83,256),(0,256)],[(171,98),(256,98),(256,256),(173,256),(168,146)]],
 'hammer': [[(0,65),(66,65),(69,136),(64,203),(0,203)],[(168,88),(256,72),(256,256),(202,234),(185,209),(181,178),(185,148),(168,124),(162,105)]],
 'volcano': [[(0,72),(83,72),(89,123),(88,188),(77,217),(0,217)],[(174,72),(256,72),(256,218),(183,218),(168,188),(166,123)]]
}
def masters(name):
 if name=='volcano' and (S/'returned/volcano-standard').exists():return Image.open(S/'references/volcano_176.png').convert('RGBA').resize((256,256),Image.Resampling.NEAREST)
 return Image.open(S/'masters'/f'{name}.png').convert('RGBA')
def masks(name):
 im=masters(name);a=np.asarray(im);m=np.zeros((256,256),np.uint8)
 if name in POLYS:
  for i,poly in enumerate(POLYS[name]):
   z=Image.new('L',(256,256));ImageDraw.Draw(z).polygon(poly,fill=255);m[np.asarray(z)>0]=i+1
  if name=='hammer':
   L,n=label(a[:,:,3]>20);ids=[i for i in range(1,n+1) if (L==i).sum()>1000]
   left=min(ids,key=lambda i:np.where(L==i)[1].mean());rest=[i for i in ids if i!=left]
   near=distance_transform_edt(L!=left)<distance_transform_edt(~np.isin(L,rest))
   m[(m==1)&~near]=0;m[near]=1
 else:
  L,n=label(a[:,:,3]>20);parts=sorted([(int((L==i).sum()),i) for i in range(1,n+1)],reverse=True)[:3]
  assert len(parts)==3,name
  centers={i:np.column_stack(np.where(L==i)).mean(0) for _,i in parts}
  order=sorted(centers,key=lambda i:centers[i][1]);roles={order[0]:1,order[1]:0,order[2]:2}
  # Distance to real artwork labels assigns tiny isolated sparks to the
  # correct anatomical neighbor; no rectangular wing slicing.
  distances=np.stack([distance_transform_edt(L!=i) for _,i in parts]);nearest=distances.argmin(0)
  for j,(_,i) in enumerate(parts):m[nearest==j]=roles[i]
 return m
def centroid(im,name):
 a=np.asarray(im).astype(float);h,w=a.shape[:2];y,x=np.indices((h,w));rgb=a[:,:,:3];hi=rgb.max(2)
 # A tight physical reactor/eye window ignores wandering fingertips and FX.
 cx,cy={'infused':(128,134),'ghost':(128,132),'colossus':(128,109),'hammer':(129,131),'helicopter':(129,135),'harrier':(128,137),'volcano':(128,128)}[name]
 roi=(abs(x-cx)<18)&(abs(y-cy)<16)&(a[:,:,3]>160)
 if name=='infused':weight=np.maximum(0,rgb[:,:,1]-rgb[:,:,0]*.7-rgb[:,:,2]*.25)*roi
 else:weight=np.maximum(0,hi-100)*roi
 if weight.sum()<10:return cx,cy
 return float((weight*x).sum()/weight.sum()),float((weight*y).sum()/weight.sum())
def register(im,name):
 # Register stationary head/mast detail, never a pulsing energy centroid.
 # A chest flare grows asymmetrically and must not drag the whole skull.
 box={'infused':(106,85,150,122),'ghost':(107,34,150,91),'colossus':(103,24,152,70),
      'hammer':(104,67,151,108),'helicopter':(111,69,145,104),'harrier':(110,80,146,111),'volcano':(105,46,151,93)}[name]
 a=np.asarray(masters(name)).astype(float);b=np.asarray(im).astype(float);x0,y0,x1,y1=box
 target=a[y0:y1,x0:x1,:3];weight=np.where(a[y0:y1,x0:x1,3]>150,1.,.2)[:,:,None]
 scores=[]
 for sy in range(-10,11):
  for sx in range(-10,11):
   sample=b[y0+sy:y1+sy,x0+sx:x1+sx,:3];err=float((np.minimum(abs(target-sample),80)*weight).mean());scores.append((err+(.04*(abs(sx)+abs(sy))),sx,sy))
 best,sx,sy=min(scores);zero=next(v[0] for v in scores if v[1:]==(0,0))
 dx,dy=(-sx,-sy) if zero>best*1.25 and zero-best>2 else (0,0)
 # Never fit changing alpha bounds or resize a pose independently.
 assert abs(dx)<=14 and abs(dy)<=14,(name,'reactor left its mount',dx,dy)
 out=Image.new('RGBA',(320,320));out.paste(im,(32+dx,32+dy));return out,dict(translation=[dx,dy],scale=1,pivot=[160,160])
def save(key,im):
 assert im.width%2==im.height%2==0
 path=O/(key+'.png');im.save(path,optimize=True)
 box=im.getbbox() or (0,0,0,0)
 return dict(key=key,path=path.relative_to(R).as_posix(),w=im.width,h=im.height,pivot=[im.width//2,im.height//2],bounds=list(box),sha256=hashlib.sha256(path.read_bytes()).hexdigest())
def preview(name,frames):
 w,h=frames[0].size;sheet=Image.new('RGB',(w*4,(h+20)*math.ceil(len(frames)/4)),'#101722');d=ImageDraw.Draw(sheet)
 for i,im in enumerate(frames):
  x=i%4*w;y=i//4*(h+20);sheet.paste(im,(x,y),im);d.text((x+8,y+h+3),str(i),fill='white')
 sheet.save(Q/(name+'-sheet.png'))
 onion=Image.new('RGBA',(w,h))
 for i in sorted({0,len(frames)//4,len(frames)//2,3*len(frames)//4,len(frames)-1}):
  layer=frames[i].copy();layer.putalpha(layer.getchannel('A').point(lambda a:round(a*.22)));onion=Image.alpha_composite(onion,layer)
 bg=Image.new('RGBA',(w,h),'#101722');Image.alpha_composite(bg,onion).convert('RGB').save(Q/(name+'-onion.png'))
 frames[0].save(Q/(name+'.gif'),save_all=True,append_images=frames[1:],duration=80,loop=0,disposal=2)
def read(name):
 folder=S/'returned'/(name+'-standard' if (S/'returned'/(name+'-standard')).exists() else name)
 paths=sorted(folder.glob('frame_*.png'));assert paths,name
 images=[Image.open(p).convert('RGBA') for p in paths];assert len({im.size for im in images})==1
 assert images[0].size in [(256,256),(176,176)],(name,images[0].size)
 if images[0].size==(176,176):images=[im.resize((256,256),Image.Resampling.NEAREST) for im in images]
 for i,im in enumerate(images[1:],1):
  a=np.asarray(im);assert (a[:,:,3]>200).sum()<256*256*.85,(name,i,'opaque blank/scenery rejected')
 return images
def build():
 data=dict(models={},clips={});audit={}
 for name in NAMES:
  images=read(name)
  if len(images)==17:images=images[1:]
  assert len(images)==16,(name,len(images))
  # The neutral seed is a single join point, replacing one generated idle
  # frame, never counted as extra motion or interpolated into a fake pose.
  images[0]=masters(name);mask=masks(name);model=dict(frames=[],size=320,fps=12);records=[];frames=[]
  for i,im in enumerate(images):
   full,info=register(im,name);arr=np.asarray(full);dx,dy=info['translation'];M=Image.new('L',(320,320));M.paste(Image.fromarray(mask),(32+dx,32+dy));M=np.asarray(M)
   layers={};rebuild=np.zeros(arr.shape,np.uint8)
   for n,part in enumerate(['core','left','right']):
    a=np.zeros_like(arr);a[M==n]=arr[M==n];rebuild[M==n]=a[M==n]
    layers[part]=save(f'v18_{name}_{part}_{i:02}',Image.fromarray(a))
   assert np.array_equal(rebuild,arr),(name,i,'module pixel loss')
   model['frames'].append(layers);frames.append(full);records.append(info)
  assert len({im.tobytes() for im in frames})>=15,(name,'duplicate poses')
  data['models'][name]=model;audit[name]=records;preview(name,frames)
 for name in ['conversion','ghost_emerge','colossus_emerge','morph_hammer','morph_helicopter','morph_harrier','morph_volcano']:
  if '--available' in sys.argv and not list((S/'returned'/name).glob('frame_*.png')):continue
  images=read(name);expected=32 if name=='conversion' else 24 if name.endswith('emerge') else 16
  if len(images)==expected+1:images=images[1:]
  assert len(images)==expected,(name,len(images))
  frames=[];rows=[]
  for i,im in enumerate(images):
   # Conversion changes silhouette on purpose. The shared source canvas is
   # its physical mount. Translating by alpha centroid would undo the acting.
   out=Image.new('RGBA',(320,320));out.paste(im,(32,32));frames.append(out);rows.append(save(f'v18_{name}_{i:02}',out))
  assert len({im.tobytes() for im in frames})==expected,(name,'not genuine distinct poses')
  data['clips'][name]=dict(frames=rows,fps=12);preview(name,frames)
 data['drone']=save('v18_drone',Image.open(S/'references/drone.png').convert('RGBA'))
 (R/'assets/stage8_pixellab_art_1018.js').write_text('"use strict";\nconst V18_ART='+json.dumps(data,separators=(',',':'))+';\n',encoding='utf-8',newline='\n')
 (S/'registration.json').write_text(json.dumps(dict(frame=[320,320],pivot=[160,160],scale=1,registration=audit,models=list(data['models']),clips={k:len(v['frames']) for k,v in data['clips'].items()}),indent=2))
 print(json.dumps(dict(models=7,moduleCells=sum(len(v['frames'])*3 for v in data['models'].values()),clipCells=sum(len(v['frames']) for v in data['clips'].values()),bytes=sum(p.stat().st_size for p in O.glob('*.png')))))
if __name__=='__main__':build()
