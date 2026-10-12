"""Own nine jet reels and the physical infestation: native crop/pad/registration."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
RAW=ROOT/'_ART_SOURCES/homecoming_1010'
DEST=ROOT/'assets/game/shared/cinematics/homecoming_1010';DEST.mkdir(parents=True,exist_ok=True)
PILOTS=['cole','axel','freezer','yuri','maverick','falva','lizzie','decker','juggernaut']
banks={};sources=[];metrics={}

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def visible(im):return im.getchannel('A').point(lambda a:255 if a>80 else 0).getbbox()
def seams(im,n,axis):
 # Measure clear gutters instead of cutting through a wing or exhaust where
 # the generator's row/column pitch differs by a few source pixels.
 counts=(np.asarray(im)[:,:,3]>80).sum(axis=axis);step=len(counts)/n;out=[0]
 for i in range(1,n):
  nominal=round(i*step);lo=max(0,nominal-32);hi=min(len(counts),nominal+33)
  candidates=np.flatnonzero(counts[lo:hi]==counts[lo:hi].min())+lo
  at=int(min(candidates,key=lambda x:abs(int(x)-nominal)))
  assert counts[at]==0,('No clear gutter',i,axis,int(counts[at]))
  out.append(at)
 return out+[len(counts)]

def jet_station(cell):
 # Fixed airframe centreline fixture, excluding luminous moving exhaust.
 # Only measure pixels; the full source RGBA is exported without repainting.
 ar=np.asarray(cell);rgb=ar[:,:,:3];h,w=ar.shape[:2]
 mask=(ar[:,:,3]>=200)&(rgb.min(axis=2)>16)&(rgb.max(axis=2)<238)
 mask[:,:round(w*.30)]=False;mask[:,round(w*.70):]=False;mask[round(h*.65):]=False
 rows=np.flatnonzero(mask.sum(axis=1)>=3)
 assert len(rows)>15,'No readable airframe fixture'
 top=next(int(y) for y in rows if sum(mask[y:min(h,y+6)].sum(axis=1)>=3)>=5)
 ys,xs=np.nonzero(mask[top:top+24]);assert len(xs)>15
 return [round(float(np.median(xs))),top+64]

def infection_station(cell):
 ar=np.asarray(cell).astype(float);rgb=ar[:,:,:3]*ar[:,:,3:4]/255
 score=rgb[:,:,1]-rgb[:,:,0]-rgb[:,:,2]*.45;score[rgb[:,:,1]<180]=-1000
 remaining=set(map(tuple,np.argwhere(score>max(80,score.max()*.72))));groups=[]
 while remaining:
  seed=remaining.pop();todo=[seed];group=[seed]
  while todo:
   y,x=todo.pop()
   for dy,dx in [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]:
    p=(y+dy,x+dx)
    if p in remaining:remaining.remove(p);todo.append(p);group.append(p)
  groups.append(group)
 assert groups,'Missing infection root'
 pts=np.array(max(groups,key=lambda g:sum(score[y,x] for y,x in g)))
 weights=np.array([score[y,x] for y,x in pts]);centre=np.average(pts,axis=0,weights=weights)
 return [round(float(centre[1])),round(float(centre[0]))]

def landing_station(cell):
 # The canopy can rise above the nose. Register the two rigid wing tips,
 # excluding centreline exhaust, the moving canopy and lower landing gear.
 ar=np.asarray(cell).astype(float);rgb=ar[:,:,:3]*ar[:,:,3:4]/255
 mask=np.rint(rgb).max(axis=2)>48;h,w=mask.shape
 spans=[]
 for y in range(h):
  xs=np.flatnonzero(mask[y])
  if len(xs):spans.append((int(xs[-1]-xs[0]),y,int(xs[0]),int(xs[-1])))
 widest=max(q[0] for q in spans)
 tips=[q for q in spans if q[0]>=widest-3]
 assert len(tips)>0 and widest>w*.50,'Missing rigid wing fixture'
 return [round(float(np.median([(q[2]+q[3])/2 for q in tips]))),round(float(np.median([q[1] for q in tips])))]

def reel(name,source,jet=False,landing=False):
 p=RAW/source;im=Image.open(p).convert('RGBA');assert im.getchannel('A').getextrema()[0]==0
 columns=4 if landing else 8;count=16 if landing else 32
 xs=seams(im,columns,0);ys=seams(im,4,1);cells=[]
 for i in range(count):
  c,r=i%columns,i//columns;rect=[xs[c],ys[r],min(im.width,xs[c+1]+1),min(im.height,ys[r+1]+1)];cell=im.crop(rect);b=visible(cell);assert b
  assert b[0]>0 and b[1]>0 and b[2]<cell.width and b[3]<cell.height,(name,i,'Clipped source',b,cell.size)
  anchor=landing_station(cell) if landing else jet_station(cell) if jet else infection_station(cell);size=448 if landing else 384
  pivot=[size//2,size//2];shift=[pivot[0]-anchor[0],pivot[1]-anchor[1]]
  out=Image.new('RGBA',(size,size));out.alpha_composite(cell,tuple(shift))
  expected=[b[0]+shift[0],b[1]+shift[1],b[2]+shift[0],b[3]+shift[1]]
  assert list(visible(out))==expected,(name,i,'Clipped delivered frame',expected,visible(out))
  clip=name+('_front' if i<16 else '_rear') if jet else name
  f=i%16 if jet else i;path=DEST/(clip+'_'+str(f).zfill(2)+'.png');out.save(path,optimize=True)
  a=dict(key='hc10_'+clip+'_'+str(f).zfill(2),path=path.relative_to(ROOT).as_posix(),clip=clip,w=size,h=size,pivot=pivot,
   source_rect=rect,source_pivot=anchor,translation=shift,opaque_bounds=list(visible(out)),scale=1,sha256=sha(path),
   registration='Rigid left/right wing-tip fixture; excludes canopy, gear and exhaust' if landing else 'Airframe centreline fixture; excludes exhaust' if jet else 'Emerald infection root')
  banks.setdefault(clip,[]).append(a);cells.append(a)
 assert len({a['sha256'] for a in cells})==count,(name,'Duplicate poses')
 for clip in {a['clip'] for a in cells}:
  widths=[a['opaque_bounds'][2]-a['opaque_bounds'][0] for a in banks[clip]]
  metrics[clip]=dict(body_width=round(float(np.median(widths))),source_scale=1)
 sources.append(dict(bank=name,path=p.relative_to(ROOT).as_posix(),size=list(im.size),sha256=sha(p),grid=[columns,4],x_seams=xs,y_seams=ys,frames=count))

def plate(name):
 p=RAW/(name+'_raw.png');im=Image.open(p).convert('RGBA');w,h=im.size;size=[w+w%2,h+h%2]
 out=Image.new('RGBA',tuple(size));out.alpha_composite(im);path=DEST/(name+'.png');out.save(path,optimize=True)
 banks[name]=[dict(key='hc10_'+name,path=path.relative_to(ROOT).as_posix(),clip=name,w=size[0],h=size[1],pivot=[size[0]//2,size[1]//2],content_rect=[0,0,w,h],scale=1,sha256=sha(path))]
 sources.append(dict(bank=name,path=p.relative_to(ROOT).as_posix(),size=[w,h],sha256=sha(p),frames=1))

for pk in PILOTS:reel(pk,pk+'_flight_'+('clean' if pk in ['lizzie','decker','juggernaut'] else 'raw')+'.png',True)
for pk in PILOTS:reel(pk+'_landing',pk+'_landing_raw.png',landing=True)
reel('infection','infection_raw.png')
for name in ['space','earth','infected_detail']:plate(name)
(ROOT/'assets/homecoming_art_1010.js').write_text('"use strict";\nconst HC10_ART='+json.dumps(banks,separators=(',',':'))+';\nconst HC10_METRICS='+json.dumps(metrics,separators=(',',':'))+';\n',encoding='utf-8',newline='\n')
manifest=dict(tool='built-in image_gen',sources=sources,shipping_assets=[a for b in banks.values() for a in b],
 native_references='references/native-manifest.json',prompts=['prompts.json','landing_prompts.json'],generation_ids=['accepted_generations.json','landing_generations.json'],
 normalization='Measured clear source gutters; unchanged RGBA crop and integer translation to the flight centreline, rigid landing wing tips or emerald root. Fixed 384x384 flight/infection cells (pivot192,192); 448x448 landing cells (pivot224,224) accommodate open canopies and full gear. Source scale1, no per-frame resampling, painting, rotation or width/height fitting. Plates receive only even transparent padding.')
(RAW/'generation_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:len(v) for k,v in banks.items()}))
