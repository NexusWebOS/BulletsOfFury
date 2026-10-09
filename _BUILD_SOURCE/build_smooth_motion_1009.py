"""Own loose authored reels. Crop/normalize only; never synthesize sprite art."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];SRC=ROOT/'_ART_SOURCES/smooth_motion_1009'
DEST=ROOT/'assets/game/shared/combat/smooth_motion_1009';DEST.mkdir(parents=True,exist_ok=True)
OUT=ROOT/'_shots/smooth_motion_1009';OUT.mkdir(parents=True,exist_ok=True)
manifest={};targets=[]
def registration(cells,ink):
 # Register only the fixed central chassis; moving feet, wing tips and exhaust
 # are excluded. One scale serves the reel, never a per-frame silhouette fit.
 base=np.array(cells[0]);l,t,r,b=map(int,ink);x0=l+(r-l)//3;x1=r-(r-l)//3;y0=t+(b-t)//4;y1=t+(b-t)*3//4
 patch=base[y0:y1,x0:x1,:3].astype(float);mask=base[y0:y1,x0:x1,3]>160
 if not mask.any():return [(0,0)]*len(cells)
 shifts=[(0,0)]
 for cell in cells[1:]:
  a=np.array(cell);best=(float('inf'),0,0)
  for dy in range(-7,8):
   for dx in range(-7,8):
    if min(y0+dy,x0+dx)<0 or y1+dy>a.shape[0] or x1+dx>a.shape[1]:continue
    sample=a[y0+dy:y1+dy,x0+dx:x1+dx,:3].astype(float)
    cost=np.abs(sample-patch)[mask].mean()+.16*(abs(dx)+abs(dy))
    if cost<best[0]:best=(cost,dx,dy)
  shifts.append((-best[1],-best[2]))
 return shifts
im=Image.open(SRC/'returned/electric_rings.png').convert('RGBA')
# This reel's expansion is drawn across unequal widths, measured per-frame.
edges=[0,238,501,766,1103,1400,1666,1939,2172]
pivots=[(127,391.5),(138,384),(132.5,384),(168.5,379.5),(148.5,388),(133,388.5),(131.5,386.5),(116,384)]
frames=[]
for i in range(8):
 cell=im.crop((edges[i],140,edges[i+1],620));a=np.array(cell);a[:,:,3][a[:,:,3]<64]=0;cell=Image.fromarray(a)
 # Measured ring centers sit on the electrical burst. One common scale retains
 # the authored outward growth; transparent source margins do not shrink it.
 w,h=cell.size;canvas=Image.new('RGBA',(416,480));px,py=pivots[i];canvas.alpha_composite(cell,(round(208-px),round(240-(py-140))))
 path=DEST/f'electric_ring_{i}.png';canvas.save(path,optimize=True)
 frames.append({'key':f'sm10_electric_ring_{i}','path':path.relative_to(ROOT).as_posix(),'w':416,'h':480,'pivot':[208,240],'rect':[edges[i],140,edges[i+1],620],'sourcePivot':[edges[i]+px,py]})
manifest['electric_ring']=frames
config=SRC/'reels.json'
if config.exists():
 for name,spec in json.loads(config.read_text()).items():
  raw=Image.open(SRC/'returned'/spec['file']).convert('RGBA');cols=spec.get('cols',8);rows=spec.get('rows',1);frames=[]
  cuts=[]
  for i in range(spec['count']):
   j=i+spec.get('start',0)
   rect=spec.get('rects',[])[i] if spec.get('rects') else [round(j%cols*raw.width/cols),round(j//cols*raw.height/rows),round((j%cols+1)*raw.width/cols),round((j//cols+1)*raw.height/rows)]
   cuts.append(rect)
  ink=spec.get('ink')
  if not ink:
   boxes=[raw.crop(r).getchannel('A').point(lambda a:255 if a>160 else 0).getbbox() for r in cuts]
   boxes=[b for b in boxes if b];ink=[min(b[0] for b in boxes),min(b[1] for b in boxes),max(b[2] for b in boxes),max(b[3] for b in boxes)]
  cells=[]
  for rect in cuts:
   cell=raw.crop(rect);a=np.array(cell);a[:,:,3][a[:,:,3]<64]=0;cells.append(Image.fromarray(a))
  shifts=registration(cells,ink) if spec.get('align') else [(0,0)]*len(cells)
  native=Image.open(SRC/'reference'/spec['targetRef']).convert('RGBA') if spec.get('targetRef') else None
  if native:
   target=native.getchannel('A').point(lambda a:255 if a>160 else 0).getbbox();origin=cells[0].getchannel('A').point(lambda a:255 if a>160 else 0).getbbox()
   kx=(target[2]-target[0])/(origin[2]-origin[0]);ky=(target[3]-target[1])/(origin[3]-origin[1])
  for i,(rect,cell) in enumerate(zip(cuts,cells)):
   if native:
    cell=cell.resize((round(cell.width*kx),round(cell.height*ky)),Image.Resampling.NEAREST);canvas=Image.new('RGBA',native.size)
    canvas.alpha_composite(cell,(round(target[0]-origin[0]*kx+shifts[i][0]*kx),round(target[1]-origin[1]*ky+shifts[i][1]*ky)))
    path=DEST/f'{name}_{i}.png';canvas.save(path,optimize=True);frames.append({'key':f'sm10_{name}_{i}','path':path.relative_to(ROOT).as_posix(),'w':native.width,'h':native.height,'pivot':[native.width/2,native.height/2],'rect':rect,'inkW':target[2]-target[0],'inkH':target[3]-target[1],'registration':shifts[i]});continue
   size=spec.get('size',[512,512]);k=spec.get('scale',1);cell=cell.resize((round(cell.width*k),round(cell.height*k)),Image.Resampling.NEAREST)
   canvas=Image.new('RGBA',size);ox=(size[0]-cell.width)//2;oy=(size[1]-cell.height)//2;canvas.alpha_composite(cell,(ox+round(shifts[i][0]*k),oy+round(shifts[i][1]*k)))
   pivot=spec.get('pivot',[(ink[0]+ink[2])/2,(ink[1]+ink[3])/2]);pivot=[ox+pivot[0]*k,oy+pivot[1]*k]
   path=DEST/f'{name}_{i}.png';canvas.save(path,optimize=True);frames.append({'key':f'sm10_{name}_{i}','path':path.relative_to(ROOT).as_posix(),'w':size[0],'h':size[1],'pivot':pivot,'rect':rect,'inkW':(ink[2]-ink[0])*k,'inkH':(ink[3]-ink[1])*k,'registration':shifts[i]})
  manifest[name]=frames
  if spec.get('paletteMask'):
   masks=[]
   for i,f in enumerate(frames):
    im=Image.open(ROOT/f['path']).convert('RGBA');a=np.array(im);rgb=a[:,:,:3].astype(float);rr,gg,bb=rgb[:,:,0],rgb[:,:,1],rgb[:,:,2]
    # The authored cobalt hull panels alone. Neutral chrome, cyan windows,
    # engine glow and all ordnance retain their generated source colors.
    hull=(bb>rr*1.2)&(bb>gg*1.10)&(gg<bb*.76)&(a[:,:,3]>64)
    hull[round(im.height*.84):]=False
    # Neutral value mask matches the existing Furyship multiply palette owner.
    # Multiplying colored blue pixels by a red pilot palette would turn them black.
    value=np.max(a[:,:,:3],axis=2);a[:,:,:3]=value[:,:,None]
    a[:,:,3][~hull]=0;path=DEST/f'{name}_blue_{i}.png';Image.fromarray(a).save(path,optimize=True)
    masks.append({**f,'key':f'sm10_{name}_blue_{i}','path':path.relative_to(ROOT).as_posix()})
   manifest[name+'_blue']=masks
  for stage,unit in spec.get('actors',[]):
   ref=Image.open(SRC/'reference'/f'stage{stage}_{unit}.png');box=ref.getchannel('A').point(lambda a:255 if a>160 else 0).getbbox()
   rec=next(q for q in json.loads((SRC/'reference/roster.json').read_text())['actors'] if q['stage']==stage and q['reference']==f'stage{stage}_{unit}.png')
   targets.append({'stage':stage,'type':rec['type'],'bank':name,'hScale':(box[3]-box[1])/3/rec['h'],'baseH':rec['h'],'ox':((box[0]+box[2])/2-256)/3,'oy':((box[1]+box[3])/2-256)/3})
(SRC/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
(ROOT/'assets/smooth_motion_art_1009.js').write_text('"use strict";\n// Owned by _BUILD_SOURCE/build_smooth_motion_1009.py.\nconst SM10_ART='+json.dumps(manifest,separators=(',',':'))+';\nconst SM10_TARGETS='+json.dumps(targets,separators=(',',':'))+';\n',encoding='utf-8',newline='\n')
def hashes(paths):return {p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
proof={'tool':'image_gen.imagegen','creative_sources':hashes(sorted((SRC/'returned').glob('*.png'))),
 'references':hashes(sorted((SRC/'reference').glob('*.png'))),
 'outputs':hashes([ROOT/f['path'] for bank in manifest.values() for f in bank]),
 'registry_sha256':hashlib.sha256((ROOT/'assets/smooth_motion_art_1009.js').read_bytes()).hexdigest(),
 'cell_count':sum(map(len,manifest.values())),
 'normalization':'Alpha below 64 cleared; common reel scale; fixed-chassis translation registration only; native ship canvases and original nozzle rigs retained. Cobalt-only Furyship value masks support the existing pilot palette owner. No procedural sprite painting.'}
(SRC/'provenance.json').write_text(json.dumps(proof,indent=2)+'\n',encoding='utf-8')
print('Built',sum(map(len,manifest.values())),'authored cells')
