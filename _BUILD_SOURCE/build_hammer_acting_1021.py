"""Export accepted PixelLab acting at fixed pivots; owning sheet/cell/taxonomy build."""
from pathlib import Path
import json,re,hashlib
import numpy as np
from PIL import Image,ImageDraw,ImageOps
from scipy.ndimage import label,uniform_filter
R=Path(__file__).resolve().parents[1];S=R/'_ART_SOURCES/hammer_acting_1021';O=R/'_shots/hammer_acting_1021';D=R/'assets/game/shared/combat/hammer_acting_1021'
D.mkdir(parents=True,exist_ok=True);O.mkdir(exist_ok=True)
art=dict(banks={},sheets={},pivot=[128,112],format='Fixed256x256 chest128,112; ship transforms320x320 with shared32px padding/chest160,144; counters640x640 chest320,280/common2.5 scale. No per-frame silhouette fit.')
audit=[]
def anchor(im,variant):
 a=np.asarray(im);r,g,b,al=[a[:,:,i].astype(float) for i in range(4)];yy,xx=np.indices(al.shape)
 m=(al>120)&(((r>110)&(r>g*1.4)&(r>b*1.3)) if variant=='corrupt' else ((b>120)&(g>110)&(r<g*.85)))&((xx-128)**2+(yy-112)**2<48**2)
 groups,n=label(m);best=None
 for i in range(1,n+1):
  ys,xs=np.where(groups==i)
  if len(xs)<7:continue
  x,y=xs.mean(),ys.mean();score=(x-128)**2+(y-112)**2-len(xs)*.2
  if best is None or score<best[0]:best=(score,x,y)
 if best is None:return (0,0)
 dx,dy=round(128-best[1]),round(112-best[2]);return (dx,dy) if abs(dx)<32 and abs(dy)<32 else (0,0)
def tip(im,variant):
 a=np.asarray(im).astype(float);r,g,b,al=[a[:,:,i] for i in range(4)];yy,xx=np.indices(al.shape)
 m=((b>100)&(b>r*1.3)&(g>65)) if variant=='blue' else ((b>80)&(r>75)&(g<r*.8)&(b>g*1.2))
 px=im.width/2;py=112+(im.height-256)/2
 m&=(al>120)&((xx-px)**2+(yy-py)**2>42**2)
 dense=uniform_filter(m.astype(float),size=10);y,x=np.unravel_index(dense.argmax(),dense.shape)
 return [int(x),int(y)] if dense[y,x]>.08 else [128,180]
def mirror(im):
 c=Image.new('RGBA',im.size);c.alpha_composite(ImageOps.mirror(im),(1,0));return c
def chromium(im):
 a=np.array(im);rgb=a[:,:,:3].astype(float);hi=rgb.max(2);lo=rgb.min(2);m=(a[:,:,3]>0)&(hi-lo<28)&(hi>27)&(hi<235)
 lum=rgb@np.array([.2126,.7152,.0722]);shine=np.minimum(245,130+lum*.85)
 for c,f in enumerate([.96,1,1.04]):a[:,:,c][m]=np.clip(shine[m]*f,0,255).astype('uint8')
 return Image.fromarray(a)
def emit(name,ims,variant,source,mirror=False):
 cw,ch=ims[0].size;pivot=[128+(cw-256)//2,112+(ch-256)//2];cells=[];sheet=Image.new('RGBA',(cw*6,ch*((len(ims)+5)//6)));rows=[]
 for i,im in enumerate(ims):
  box=im.getbbox();assert im.size==(cw,ch) and box,(name,i)
  assert min(box[:2])>0 and box[2]<cw and box[3]<ch,(name,i,'clipped',box)
  rect=[i%6*cw,i//6*ch,cw,ch];sheet.alpha_composite(im,rect[:2]);rows.append(dict(key=f'ha21_{name}_{i}',sheet='ha21_'+name,cell=rect,w=cw,h=ch,pivot=pivot,bounds=list(box),tip=tip(im,variant)))
 sheet.save(D/(name+'.webp'),lossless=True,exact=True,method=6);art['sheets']['ha21_'+name]=dict(key='nca_ha21_'+name,path=(D/(name+'.webp')).relative_to(R).as_posix(),w=sheet.width,h=sheet.height);art['banks'][name]=rows
 audit.append(dict(bank=name,frames=len(ims),source=source,bytes=(D/(name+'.webp')).stat().st_size))
folders=list((S/'raw').glob('*'))
folders=sorted(set(folders+[p.with_name(p.name.replace('_clean','_empty')) for p in folders if p.name.endswith('_clean')]))
for folder in folders:
 name=folder.name;variant=name.split('_')[0];ims=[];offsets=[]
 files=sorted(folder.glob('*.png'))
 if name in ['blue_beam','corrupt_beam'] or name.endswith('_clean'):continue
 if name.startswith('blue_') and name.endswith('_empty'):
  replacement=S/'raw'/name.replace('_empty','_clean')
  if not (replacement/'16.png').exists():continue
  files=sorted(replacement.glob('*.png'))
 if len(files)!=17:continue
 if name in ['blue_release_pose','blue_throw_follow','blue_throw_release']:continue # consumed as corrected release tail below
 if name=='blue_throw' and (S/'raw/blue_throw_follow/08.png').exists():
  follow=sorted((S/'raw/blue_throw_follow').glob('*.png'));files=files[:7]+[follow[0]]+follow
 if name=='blue_chromium':files=[files[6] if i==7 else files[9] if i==8 else p for i,p in enumerate(files)]
 if name=='corrupt_chromium':files=[files[10] if i in [11,12,13] else p for i,p in enumerate(files)]
 for file in files:
  im=Image.open(file).convert('RGBA');assert im.size==(256,256)
  # Register the real luminous chest, never independently fit a frame silhouette.
  dx,dy=(0,0) if name=='corrupt_stun' else anchor(im,variant);pad=32 if name.endswith('from_ship') else 0;c=Image.new('RGBA',(256+pad*2,256+pad*2));c.alpha_composite(im,(dx+pad,dy+pad));ims.append(c);offsets.append([dx,dy])
 emit(name,ims,variant,name)
 if name.endswith('_slam'):emit(variant+'_idle',[ims[0]],variant,name)
 if name.endswith('_side'):emit(name+'_left',[mirror(im) for im in ims],variant,name)
 if variant=='blue' and not name.endswith(('chromium','from_ship','to_ball')):emit(name+'_armor',[chromium(im) for im in ims],variant,name)
 audit[-1]['registrationTranslations']=offsets
 if name=='blue_side':
  # Existing committed counter reads sixteen pose/tip rows at native scale.70.
  # One bank-wide x2.5 export gives the same1.75 world scale as the new body.
  order=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,15,16]
  for side,flip in [('right',False),('left',True)]:
   name2='blue_counter_'+side;sheet=Image.new('RGBA',(640*4,640*4));rows=[]
   for j,f in enumerate(order):
    im=mirror(ims[f]) if flip else ims[f];im=im.resize((640,640),Image.Resampling.NEAREST);box=im.getbbox();rect=[j%4*640,j//4*640,640,640];sheet.alpha_composite(im,rect[:2]);head=tip(mirror(ims[f]) if flip else ims[f],variant)
    rows.append(dict(key=f'ha21_{name2}_{j}',sheet='ha21_'+name2,cell=rect,w=640,h=640,pivot=[320,280],bounds=list(box),tip=[round(x*2.5) for x in head]))
   sheet.save(D/(name2+'.webp'),lossless=True,exact=True,method=6);art['sheets']['ha21_'+name2]=dict(key='nca_ha21_'+name2,path=(D/(name2+'.webp')).relative_to(R).as_posix(),w=2560,h=2560);art['banks'][name2]=rows
   audit.append(dict(bank=name2,frames=16,source='blue_side',scale=2.5,bytes=(D/(name2+'.webp')).stat().st_size))
   armored=name2+'_armor';chrome_sheet=chromium(sheet);chrome_sheet.save(D/(armored+'.webp'),lossless=True,exact=True,method=6)
   art['sheets']['ha21_'+armored]=dict(key='nca_ha21_'+armored,path=(D/(armored+'.webp')).relative_to(R).as_posix(),w=2560,h=2560)
   art['banks'][armored]=[{**a,'key':f'ha21_{armored}_{i}','sheet':'ha21_'+armored} for i,a in enumerate(rows)]
   audit.append(dict(bank=armored,frames=16,source='blue_side',scale=2.5,bytes=(D/(armored+'.webp')).stat().st_size))
 for bank in [name]:
  sheet=Image.new('RGB',(6*256,3*280),'#111b24');dr=ImageDraw.Draw(sheet)
  for i,im in enumerate(ims):
   x=i%6*256;y=i//6*280;small=im.resize((256,256),Image.Resampling.NEAREST);sheet.paste(small,(x,y),small);dr.text((x+6,y+258),f'{name} {i}',fill='white')
   tx,ty=art['banks'][bank][i]['tip'];tx*=256/im.width;ty*=256/im.height;dr.ellipse((x+tx-3,y+ty-3,x+tx+3,y+ty+3),outline='#30ff80')
  sheet.save(O/(name+'-registered.png'))
(S/'export-audit.json').write_text(json.dumps(dict(banks=audit,geometry=art['format'],outputs=[dict(path=a['path'],sha256=hashlib.sha256((R/a['path']).read_bytes()).hexdigest()) for a in art['sheets'].values()]),indent=2)+'\n')
(D/'manifest.json').write_text(json.dumps(art,indent=2)+'\n')
(R/'assets/hammer_acting_art_1021.js').write_text('"use strict";\nconst HA21_ART='+json.dumps(art,separators=(',',':'))+';\n',newline='\n')
taxonomy=R/'assets/data/ART_TAXONOMY.json';tax=json.loads(taxonomy.read_text(encoding='utf-8'))
tax['ha21_']=dict(role='whole_authored_hammer_acting',sheet=None,owner='_BUILD_SOURCE/build_hammer_acting_1021.py',note='PixelLab standard black-steel/cyan and corrupted violet/orange Hammerboss acting. Whole body, two arms, one hammer, physical Chromium takeover. Native encounter clocks, damage, HP and visible part/owner flash retain ownership. Fixed256px frames, ship320px padded frames, counter640px at common2.5 scale. Source/selection/export audit in _ART_SOURCES/hammer_acting_1021; Stage5 retains approved native kneeling/death acting.')
taxonomy.write_text(json.dumps(tax,indent=2,ensure_ascii=True)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(dict(banks=len(art['banks']),frames=sum(len(a) for a in art['banks'].values()),bytes=sum(a['bytes'] for a in audit))))
