"""Own the landing PNGs and registration. Crop, pad, translate; no repainting.

Frames are registered by fixed aircraft engine mounts and pilot hip centres.
Bounding boxes are recorded for QA, never used to fit each frame to a new size.
"""
from pathlib import Path
from PIL import Image
import numpy as np
import json,hashlib,math
ROOT=Path(__file__).resolve().parents[1]
RAW=ROOT/'_ART_SOURCES/hq_landing_1010'
DEST=ROOT/'assets/game/shared/cinematics/hq_landing_1010';DEST.mkdir(parents=True,exist_ok=True)
PILOTS=['cole','axel','freezer','yuri','maverick','falva','lizzie','decker','juggernaut']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def row_edges(im,rows):
 counts=(np.asarray(im)[:,:,3]>96).sum(axis=1)
 step=im.height/rows;edges=[0]
 for i in range(1,rows):
  lo,hi=round(step*(i-.29)),round(step*(i+.29))
  sample=counts[lo:hi];limit=int(sample.min())+3
  gap=np.flatnonzero(sample<=limit)+lo
  edges.append(round(float(np.median(gap))))
 return edges+[im.height]
def bounds(cell):return cell.getchannel('A').point(lambda a:255 if a>96 else 0).getbbox()
def body_anchor(cell):
 box=bounds(cell);assert box
 band=round(cell.height*.54);coords=[]
 for y in range(band-5,band+6):
  for x in range(cell.width):
   if cell.getpixel((x,y))[3]>220:coords.append(x)
 centre=(box[0]+box[2])//2
 nearby=[x for x in coords if abs(x-centre)<cell.width*.13]
 return [round(sum(nearby)/len(nearby)) if nearby else centre,band]
def rect(im,i,cols,rows,edges=None):
 c,r=i%cols,i//cols
 return [round(c*im.width/cols),edges[r] if edges else round(r*im.height/rows),round((c+1)*im.width/cols),edges[r+1] if edges else round((r+1)*im.height/rows)]
def engine_anchor(cell):
 # Twin round engine mouths, excluding the moving cyan exhaust underneath.
 points=[];w,h=cell.size
 for y in range(round(h*.47),round(h*.77)):
  for x in range(round(w*.20),round(w*.62)):
   r,g,b,a=cell.getpixel((x,y))
   if a>180 and r>145 and g>210 and b>210 and b-r>20:points.append((x,y))
 if not points:return None
 return [round(sum(x for x,y in points)/len(points)),round(sum(y for x,y in points)/len(points))]
banks={};sources=[]
def export(name,im,indices,cols,rows,size,anchors=None,clip=None,pivot=None,edges=None):
 bank=[];pivot=pivot or [size[0]//2,size[1]//2]
 for f,i in enumerate(indices):
  box=rect(im,i,cols,rows,edges)
  if name in ['background','space']:
   # The white montage divider belongs to neither cinematic environment.
   if i%cols:box[0]+=3
   else:box[2]-=3
   if i//cols:box[1]+=3
   else:box[3]-=3
  cell=im.crop(box)
  point=anchors[f] if anchors else [cell.width//2,cell.height//2]
  shift=[pivot[0]-point[0],pivot[1]-point[1]]
  out=Image.new('RGBA',size);out.alpha_composite(cell,tuple(shift))
  dest=DEST/(name+'_'+str(f).zfill(2)+'.png');out.save(dest,optimize=True)
  source_bounds=bounds(cell);out_bounds=bounds(out)
  if source_bounds:
   expected=[source_bounds[0]+shift[0],source_bounds[1]+shift[1],source_bounds[2]+shift[0],source_bounds[3]+shift[1]]
   assert expected==list(out_bounds),(name,f,'Visible artwork clipped',expected,out_bounds)
   if name.endswith(('_walk','_exit')):
    assert source_bounds[0]>3 and source_bounds[2]<cell.width-3,(name,f,'Body crosses source column boundary',source_bounds)
  bank.append(dict(key='hl10_'+name+'_'+str(f).zfill(2),path=dest.relative_to(ROOT).as_posix(),source=im.info.get('source_path'),w=size[0],h=size[1],pivot=pivot,source_rect=box,source_pivot=point,translation=shift,scale=1,clip=clip or name,opaque_bounds=list(out_bounds or (0,0,0,0)),sha256=sha(dest)))
 assert len({a['sha256'] for a in bank})==len(bank),(name,'Duplicate cells')
 banks[name]=bank
 return bank

def export_door(im,edges):
 # Onion registration uses the building, never the uneven sheet-cell centre.
 # One authored open frame owns the stationary lintel, pillars and threshold.
 # The two authored closed panels translate behind that frame's aperture;
 # regenerating the masonry on every frame caused the visible building wobble.
 size=(384,384);pivot=[192,288];registered=[];origins=[]
 for i in range(16):
  box=rect(im,i,4,4,edges);cell=im.crop(box);b=bounds(cell);assert b
  point=[round((b[0]+b[2])/2),b[3]-4]
  shift=[pivot[0]-point[0],pivot[1]-point[1]]
  plate=Image.new('RGBA',size);plate.alpha_composite(cell,tuple(shift))
  registered.append(plate)
  origins.append(dict(source_rect=box,source_pivot=point,translation=shift))
 fixed=registered[15];closed=registered[0]
 aperture=[138,124,246,278];centre=192
 panel_boxes=[[aperture[0],aperture[1],centre,aperture[3]],
              [centre,aperture[1],aperture[2],aperture[3]]]
 panels=[closed.crop(tuple(box)) for box in panel_boxes]
 bank=[]
 outside=np.ones((size[1],size[0]),dtype=bool)
 outside[aperture[1]:aperture[3],aperture[0]:aperture[2]]=False
 fixed_pixels=np.asarray(fixed)
 for f in range(16):
  travel=round((centre-aperture[0])*f/15)
  layer=Image.new('RGBA',size)
  for side,box,panel in zip([-1,1],panel_boxes,panels):
   layer.alpha_composite(panel,(box[0]+side*travel,box[1]))
  # Only the doorway aperture reveals the sliding panels. The jambs stay fixed.
  clipped=Image.new('RGBA',size)
  clipped.alpha_composite(layer.crop(tuple(aperture)),tuple(aperture[:2]))
  out=Image.alpha_composite(fixed,clipped)
  assert np.array_equal(np.asarray(out)[outside],fixed_pixels[outside]),'Stationary door pixels changed'
  dest=DEST/('door_'+str(f).zfill(2)+'.png');out.save(dest,optimize=True)
  bank.append(dict(key='hl10_door_'+str(f).zfill(2),path=dest.relative_to(ROOT).as_posix(),
   source=im.info['source_path'],w=size[0],h=size[1],pivot=pivot,clip='door',scale=1,
   source_rect=origins[15]['source_rect'],source_pivot=origins[15]['source_pivot'],
   translation=origins[15]['translation'],opaque_bounds=list(bounds(out)),sha256=sha(dest),
   fixed_frame=15,aperture=aperture,sliding_panels=dict(source_frame=0,
    source_rect=origins[0]['source_rect'],source_pivot=origins[0]['source_pivot'],
    translation=origins[0]['translation'],panel_rects=panel_boxes,offsets=[-travel,travel]),
   registration='One fixed authored frame; closed panels translate 1:1 within its fixed aperture.'))
 assert len({a['sha256'] for a in bank})==16,'Door poses must be distinct'
 banks['door']=bank
 return dict(fixed_frame=15,closed_frame=0,aperture=aperture,source_registration=origins,
  normalization='Native 1:1 crop/translate/composite. Stationary architecture is identical in all sixteen frames; no resampling or repainting.')
for name,indices in [('background',[0,2]),('space',[0,1])]:
 p=RAW/(name+'_raw.png');im=Image.open(p).convert('RGBA')
 im.info['source_path']=p.relative_to(ROOT).as_posix()
 export(name,im,indices,2,2,(840,472))
 sources.append(dict(name=name,path=p.relative_to(ROOT).as_posix(),size=list(im.size),sha256=sha(p)))
for pilot in PILOTS:
 p=RAW/(pilot+'_raw.png');im=Image.open(p).convert('RGBA')
 im.info['source_path']=p.relative_to(ROOT).as_posix()
 edges=row_edges(im,4);cells=[im.crop(rect(im,i,8,4,edges)) for i in range(32)]
 engines=[engine_anchor(cell) for cell in cells[:16]]
 assert all(engines[:10]),(pilot,'Missing engine mouth origin')
 # Engine shutdown hides the cyan; retain the measured bank origin for those
 # poses rather than letting visible landing gear/ladder redefine the mount.
 stable=[round(sum(v[j] for v in engines[7:10])/3) for j in (0,1)]
 engines=[v if v and i<11 else stable for i,v in enumerate(engines)]
 export(pilot+'_landing',im,range(16),8,4,(288,288),engines,pilot+'_landing',[144,190],edges)
 # Hips, not each heel, anchor both body clips. One measured station per row:
 # regular gaits may raise a heel, but that must not shove the torso around.
 body=[body_anchor(cell) for cell in cells[16:]]
 if pilot!='juggernaut':export(pilot+'_exit',im,range(16,24),8,4,(288,288),body[:8],pilot+'_exit',[144,144],edges)
 if pilot!='axel':export(pilot+'_walk',im,range(24,32),8,4,(288,288),body[8:],pilot+'_walk',[144,144],edges)
 sources.append(dict(name=pilot,path=p.relative_to(ROOT).as_posix(),size=list(im.size),sha256=sha(p),stable_engine_origin=stable,row_edges=edges,used_clips=['landing']+([] if pilot=='juggernaut' else ['exit'])+([] if pilot=='axel' else ['walk'])))
for name,row in [('axel_walk',3),('juggernaut_exit',2)]:
 p=RAW/(name+'_fixed_raw.png');im=Image.open(p).convert('RGBA');im.info['source_path']=p.relative_to(ROOT).as_posix()
 edges=row_edges(im,4);indices=range(row*8,(row+1)*8)
 anchors=[body_anchor(im.crop(rect(im,i,8,4,edges))) for i in indices]
 export(name,im,indices,8,4,(288,288),anchors,name,[144,144],edges)
 sources.append(dict(name=name,path=p.relative_to(ROOT).as_posix(),size=list(im.size),sha256=sha(p),row_edges=edges,used_frames=list(indices)))
for name in ['fx','door','dust']:
 p=RAW/(name+'_raw.png')
 if not p.exists():continue
 im=Image.open(p).convert('RGBA')
 im.info['source_path']=p.relative_to(ROOT).as_posix()
 edges=row_edges(im,4)
 if name=='fx':
  size=(math.ceil(im.width/4/2)*2+8,math.ceil(im.height/4/2)*2+8)
  # The sheet's transparent top margin is not the ground contact station.
  # Centre each authored silhouette on the common pavement anchor.
  anchors=[]
  for i in range(4):
   cell=im.crop(rect(im,i,4,4));alpha=cell.getchannel('A');peak=alpha.getextrema()[1]
   b=alpha.point(lambda a:255 if a>max(4,peak*.5) else 0).getbbox();assert b,(name,i)
   # The two aft lobes sit underneath the landing wheels. Register that rear
   # axle, not the nose-heavy silhouette's visual centre, to the pavement.
   anchors.append([(b[0]+b[2])//2,round(b[1]+(b[3]-b[1])*.80)])
  export('shadow',im,range(4),4,4,size,anchors)
 elif name=='door':
  door_registration=export_door(im,edges)
 else:
  anchors=[]
  for i in range(16):
   cell=im.crop(rect(im,i,4,4,edges));b=bounds(cell);assert b,(name,i)
   anchors.append([cell.width//2,b[3]-4])
  export('door' if name=='door' else 'downwash',im,range(16),4,4,(384,384),anchors,pivot=[192,288],edges=edges)
 sources.append(dict(name=name,path=p.relative_to(ROOT).as_posix(),size=list(im.size),sha256=sha(p),row_edges=edges,used_frames=list(range(4)) if name=='fx' else [0,15] if name=='door' else list(range(16))))
registry=ROOT/'assets/hq_landing_art_1010.js'
registry.write_text('"use strict";\nconst HL10_ART='+json.dumps(banks,separators=(',',':'))+';\n',encoding='utf-8',newline='\n')
user_refs=[]
for name in ['approved-runway.png','approved-hq.png']:
 p=RAW/'references'/name
 if p.exists():user_refs.append(dict(path=p.relative_to(ROOT).as_posix(),size=list(Image.open(p).size),sha256=sha(p),role='User supplied sunset edit target/reference'))
manifest=dict(tool='built-in image_gen',sources=sources,shipping_assets=[a for b in banks.values() for a in b],reference_manifest='references/manifest.json',user_references=user_refs,prompts='final_prompts.json',correction_prompts='correction_prompts.json',generation_ids='accepted_generation_ids.json',normalization='Native 1:1 crop/pad/translation. Fixed engine mouths and torso anchor; no repaint, per-frame fit or independent axis scale.',pilots=PILOTS,door_registration=door_registration)
(RAW/'generation_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:len(b) for k,b in banks.items()}))
