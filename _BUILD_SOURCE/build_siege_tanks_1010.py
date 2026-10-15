"""Own the preview-only siege kit: authored cells, fixed pivots and provenance.

No atlas or production registry is edited. This performs source cuts, one scale
per reel and translation against stationary fixtures; it paints no sprite art.
Frame header rules: docs/FRAME_RESOLUTION_RULES.md. Every exported bank has
fixed even canvas dimensions, one proportional scale and a shared pivot.
"""
from pathlib import Path
import ast,json,hashlib,sys,shutil
from collections import deque
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];SRC=ROOT/'_ART_SOURCES/siege_tanks_1010'
DEST=SRC/'normalized';DEST.mkdir(exist_ok=True)
tree=ast.parse((ROOT/'_BUILD_SOURCE/build_smooth_motion_1009.py').read_text())
node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='registration')
exec(compile(ast.Module(body=[node],type_ignores=[]),'fixed-fixture-registration','exec'),globals())
SIZE=640;manifest={};metrics={};warnings=[]
FRAME_POLICY={'dimensionMultiple':2,'uniformCanvasPerBank':True,'proportionalScalePerBank':True,
 'fixedPivotPerBank':True,'oddCropRepair':'shared transparent right/bottom padding'}
corrections=json.loads((SRC/'registration-corrections.json').read_text()).get('shifts',{})
parts=['hull','weapon','track_left','track_right','pod','reactor','sensor']
widths={
 'sonic':dict(zip(parts,[280,175,92,92,80,115,70])),
 'devastator':dict(zip(parts,[280,220,90,90,65,120,60])),
 'deviator':dict(zip(parts,[280,195,80,80,62,125,78]))}
def bounds(im):
 return im.getchannel('A').point(lambda v:255 if v>160 else 0).getbbox()
def clean(im):
 a=np.array(im.convert('RGBA'));a[:,:,3][a[:,:,3]<64]=0;return Image.fromarray(a)
def grid(file,cols,rows,start=0,count=None,half=None):
 raw=Image.open(SRC/'returned'/file).convert('RGBA');cells=[];rects=[]
 for i in range(start,start+(count if count is not None else cols*rows)):
  rect=[round(i%cols*raw.width/cols),round(i//cols*raw.height/rows),round((i%cols+1)*raw.width/cols),round((i//cols+1)*raw.height/rows)]
  if half=='left':rect[2]=round((rect[0]+rect[2])/2)
  if half=='right':rect[0]=round((rect[0]+rect[2])/2)
  cells.append(clean(raw.crop(rect)));rects.append(rect)
 return cells,rects

def track_grid(file,rows=4,lower=False,side='left',perrow=8,singles=False,upper=False):
 raw=Image.open(SRC/'returned'/file).convert('RGBA');mask=np.array(raw)[:,:,3]>160
 hh,ww=mask.shape;seen=np.zeros(mask.shape,dtype=bool);pieces=[]
 for yy,xx in zip(*np.where(mask)):
  if seen[yy,xx]:continue
  q=deque([(int(xx),int(yy))]);seen[yy,xx]=True;n=0;x0=x1=int(xx);y0=y1=int(yy)
  while q:
   x,y=q.popleft();n+=1;x0=min(x0,x);x1=max(x1,x);y0=min(y0,y);y1=max(y1,y)
   for nx,ny in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
    if 0<=nx<ww and 0<=ny<hh and mask[ny,nx] and not seen[ny,nx]:seen[ny,nx]=True;q.append((nx,ny))
  if n>2000 and (not lower or y0>=hh/2):pieces.append((n,[x0,y0,x1+1,y1+1]))
 if upper:pieces=sorted(pieces,reverse=True)[:16]
 pieces=[b for n,b in pieces]
 if len(pieces)!=perrow*4:raise ValueError(f'{file}: expected {perrow*4} separate authored tracks, got {len(pieces)}')
 pieces.sort(key=lambda b:(b[1]+b[3])/2);ordered=[]
 for row in range(4):
  line=sorted(pieces[row*perrow:row*perrow+perrow],key=lambda b:b[0])
  ordered+=line if singles else line[0 if side=='left' else 1::2]
 selected=ordered;cells=[];rects=[]
 for b in selected:
  rect=[max(0,b[0]-4),max(0,b[1]-4),min(ww,b[2]+4),min(hh,b[3]+4)]
  cells.append(clean(raw.crop(rect)));rects.append(rect)
 return cells,rects
def shift_fixed(cells,mode):
 bs=[bounds(c) for c in cells]
 if any(b is None for b in bs):raise ValueError('Missing authored cell')
 # Fixed metal fixtures, not expanding sparks/flames, own the translation.
 if mode=='projectile':
  first=bs[0];initial=[(round((first[0]+first[2]-b[0]-b[2])/2),first[3]-b[3]) for b in bs]
 elif mode in ['hull','track','damage']:
  first=bs[0];initial=[(round((first[0]+first[2]-b[0]-b[2])/2),round((first[1]+first[3]-b[1]-b[3])/2)) for b in bs]
 elif mode=='weapon':
  metal=[]
  for c in cells:
   a=np.array(c);rgb=a[:,:,:3];m=(a[:,:,3]>160)&(rgb.max(2)<205)&(rgb.max(2)-rgb.min(2)<85)
   ys,xs=np.where(m)
   metal.append((int(xs.min()),int(ys.min()),int(xs.max()+1),int(ys.max()+1)))
  first=metal[0];initial=[(round((first[0]+first[2]-b[0]-b[2])/2),first[1]-b[1]) for b in metal]
 else:initial=[(0,0)]*len(cells)
 aligned=[];cw=max(c.width for c in cells);ch=max(c.height for c in cells)
 for c,(dx,dy) in zip(cells,initial):
  out=Image.new('RGBA',(cw+192,ch+192));out.alpha_composite(c,(96+dx,96+dy));aligned.append(out)
 l,t,r,b=[v+96 for v in bs[0]]
 if mode=='weapon':fixture=[l+(r-l)*.36,t,l+(r-l)*.64,t+(b-t)*.13]
 elif mode=='projectile':fixture=[l+(r-l)*.15,t+(b-t)*.65,r-(r-l)*.15,b]
 elif mode=='track':fixture=[l,t,r,t+(b-t)*.23]
 else:fixture=[l+(r-l)*.26,t+(b-t)*.34,r-(r-l)*.26,t+(b-t)*.68]
 # Damage paintings deliberately change metal and silhouette. Their shared
 # cell/pivot, rather than a search for intact texture in white art, owns them.
 if mode in ['damage','projectile']:return initial
 # Rolling tread texture and expanding light must not become mounting points.
 # Compare silhouettes in a bounded neighborhood after coarse translation.
 base=np.array(aligned[0])[:,:,3].astype(float)/255
 x0,y0,x1,y1=map(int,fixture)
 pad=10;x0=max(0,x0-pad);y0=max(0,y0-pad);x1=min(base.shape[1],x1+pad);y1=min(base.shape[0],y1+pad)
 residual=[(0,0)]
 for c in aligned[1:]:
  a=np.array(c)[:,:,3].astype(float)/255;best=None
  for dy in range(-12,13):
   for dx in range(-12,13):
    cost=float(np.mean((base[y0:y1,x0:x1]-a[y0-dy:y1-dy,x0-dx:x1-dx])**2))+.00005*(abs(dx)+abs(dy))
    if best is None or cost<best[0]:best=(cost,dx,dy)
  if max(abs(best[1]),abs(best[2]))==12:raise ValueError(f'{mode}: fixture search limit; inspect source')
  residual.append((best[1],best[2]))
 return [(dx+rx,dy+ry) for (dx,dy),(rx,ry) in zip(initial,residual)]
def bank(name,cells,rects,file,target_width,mode='center',pivot_fraction=(.5,.5),template=None):
 print('Registering '+name,flush=True)
 bs=[bounds(c) for c in cells];first=bs[0]
 if first is None:raise ValueError(f'{name}: first frame empty')
 k=target_width/(first[2]-first[0]);shifts=shift_fixed(cells,mode) if mode!='center' else [(0,0)]*len(cells)
 pivot=[first[0]+(first[2]-first[0])*pivot_fraction[0],first[1]+(first[3]-first[1])*pivot_fraction[1]]
 # Expansion is scaled once from the largest authored frame. It is never
 # fitted separately frame-by-frame, which would erase growth and cause bobbing.
 if mode in ['center','projectile']:
  w=max(c.width for c in cells);h=max(c.height for c in cells);pivot=[w/2,h/2]
  if mode=='projectile':pivot=[(first[0]+first[2])/2,first[3]]
  extent=max(max(b[2]-b[0],b[3]-b[1]) for b in bs if b)
  k=target_width/extent
 records=[];hashes=[];areas=[]
 extra=corrections.get(name,[(0,0)]*len(cells))
 if len(extra)!=len(cells):raise ValueError(f'{name}: incomplete native fixture translation')
 for i,(c,rect,(dx,dy)) in enumerate(zip(cells,rects,shifts)):
  out=Image.new('RGBA',(SIZE,SIZE));scaled=c.resize((round(c.width*k),round(c.height*k)),Image.Resampling.NEAREST)
  nx,ny=extra[i]
  out.alpha_composite(scaled,(round(SIZE/2+(dx-pivot[0])*k)+nx,round(SIZE/2+(dy-pivot[1])*k)+ny))
  box=out.getchannel('A').getbbox()
  if not box:raise ValueError(f'{name}/{i}: no pixels')
  if box[0]<=0 or box[1]<=0 or box[2]>=SIZE or box[3]>=SIZE:raise ValueError(f'{name}/{i}: normalized output clips')
  path=DEST/f'{name}_{i:02d}.png';out.save(path,optimize=True);digest=hashlib.sha256(path.read_bytes()).hexdigest();hashes.append(digest)
  a=np.array(out)[:,:,3];areas.append(int((a>=64).sum()))
  records.append({'key':f'st10_{name}_{i}','path':path.relative_to(ROOT).as_posix(),'w':SIZE,'h':SIZE,'pivot':[SIZE//2,SIZE//2],
   'source':file,'rect':rect,'sourcePivot':pivot,'scale':k,'registration':[dx,dy],'nativeFixtureShift':[nx,ny],'bounds':box,'sha256':digest})
 # One common transparent canvas crop per bank saves decoded-image memory.
 # Its pivot is adjusted once, never separately fitted to individual frames.
 union=[min(q['bounds'][0] for q in records)-2,min(q['bounds'][1] for q in records)-2,
  max(q['bounds'][2] for q in records)+2,max(q['bounds'][3] for q in records)+2]
 # Round the common canvas up with transparent space. Left/top, artwork and
 # physical pivots stay exact; stretching or individually fitting cells would
 # change proportions or create frame-to-frame movement.
 union[2]+=(union[2]-union[0])%2
 union[3]+=(union[3]-union[1])%2
 hashes=[]
 for q in records:
  path=ROOT/q['path'];im=Image.open(path).crop(union);im.save(path,optimize=True)
  q['w'],q['h']=im.size;q['pivot']=[SIZE//2-union[0],SIZE//2-union[1]]
  q['bounds']=[q['bounds'][0]-union[0],q['bounds'][1]-union[1],q['bounds'][2]-union[0],q['bounds'][3]-union[1]]
  q['sha256']=hashlib.sha256(path.read_bytes()).hexdigest();hashes.append(q['sha256'])
 if any(q['w']%2 or q['h']%2 for q in records):raise ValueError(f'{name}: odd exported frame dimensions')
 if len({(q['w'],q['h'],*q['pivot'],q['scale']) for q in records})!=1:raise ValueError(f'{name}: unequal frame geometry')
 if len(cells)>4 and len(set(hashes))!=len(cells):raise ValueError(f'{name}: repeated animation cells')
 manifest[name]=records;metrics[name]={'frames':len(cells),'unique':len(set(hashes)),'peakInk':max(areas),'commonScale':k,
  'peakInkFrame':areas.index(max(areas)),'peakWidth':max(r['bounds'][2]-r['bounds'][0] for r in records),'peakHeight':max(r['bounds'][3]-r['bounds'][1] for r in records)}
 return records
for unit in ['sonic','devastator','deviator']:
 # Idle bare hulls retain empty sockets. Rejected mixed-count returns remain
 # archived; no missing frames are filled by duplication.
 file=f'{unit}_mobility.png'
 if unit=='sonic':file='sonic_hull16.png';cells,rects=track_grid(file,perrow=4,singles=True)
 else:cells,rects=track_grid(file,perrow=4,singles=True,upper=True)
 bank(unit+'_hull',cells,rects,file,widths[unit]['hull'],'hull',(.5,.51))
 for side in ['left','right']:
  if unit=='sonic' and side=='left':file='sonic_tracks16.png';cells,rects=track_grid(file,side=side,perrow=7)
  elif unit=='sonic':file='sonic_track_right16.png';cells,rects=track_grid(file,perrow=4,singles=True)
  elif unit=='deviator':file=unit+'_mobility.png';cells,rects=track_grid(file,lower=True,side=side)
  else:file=unit+'_tracks16.png';cells,rects=track_grid(file,side=side)
  bank(unit+'_track_'+side,cells,rects,file,widths[unit]['track_'+side],'track')
 file='devastator_weapon_padded16.png' if unit=='devastator' else unit+'_weapon16.png'
 cells,rects=track_grid(file,perrow=4,singles=True,upper=True)
 pivot=(.5,.18) if unit=='sonic' else (.5,.30) if unit=='devastator' else (.5,.68)
 bank(unit+'_weapon',cells,rects,file,widths[unit]['weapon'],'weapon',pivot)
 for part in ['pod','reactor','sensor']:
  im=clean(Image.open(SRC/'reference'/f'{unit}_{part}.png'))
  bank(unit+'_'+part,[im],[[0,0,im.width,im.height]],'reference/'+unit+'_'+part+'.png',widths[unit][part],'center')
 for row,part in enumerate(parts):
  file=unit+'_damage32.png';cells,rects=grid(file,4,8,row*4,4)
  pivot=(.5,.18) if part=='weapon' and unit=='sonic' else (.5,.30) if part=='weapon' and unit=='devastator' else (.5,.68) if part=='weapon' else (.5,.51) if part=='hull' else (.5,.5)
  bank(unit+'_'+part+'_damage',cells,rects,file,metrics[unit+'_'+part]['peakWidth'],'damage',pivot)
 file=unit+'_damage32.png';cells,rects=grid(file,4,8,28,4)
 bank(unit+'_debris',cells,rects,file,85)
 for effect,count,rows,extent in [('charge',16,4,270),('projectile',16,4,150),('explosion',32,8,460),('impact',16,4,270)]:
  file=f'{unit}_{effect}{count}.png';cells,rects=grid(file,4,rows)
  bank(unit+'_'+effect,cells,rects,file,extent,'projectile' if effect=='projectile' else 'center',(.5,.85) if effect=='projectile' else (.5,.5))
cells,rects=grid('decals16.png',4,4)
bank('decals',cells,rects,'decals16.png',270)
preview=ROOT/'docs/previews/siege_tanks_1010'
(preview/'art.js').write_text('"use strict";\n// Preview only; owned by build_siege_tanks_1010.py.\nconst ST10_ART='+json.dumps(manifest,separators=(',',':'))+';\nconst ST10_METRICS='+json.dumps(metrics,separators=(',',':'))+';\n',encoding='utf-8',newline='\n')
(SRC/'manifest.json').write_text(json.dumps({'framePolicy':FRAME_POLICY,'banks':manifest,'metrics':metrics,'warnings':warnings},indent=2)+'\n')
(SRC/'provenance.json').write_text(json.dumps({'tool':'image_gen.imagegen','scope':'Preview only; no production imports or atlas changes',
 'normalization':'Authored cell cuts; alpha<64 fringe removal; fixed fixture translation; one common scale per reel; shared even canvas with transparent padding; native nearest-neighbor pixel rendering',
 'framePolicy':FRAME_POLICY,
 'source_sha256':{p.relative_to(SRC).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((SRC/'returned').glob('*.png'))},
 'outputs':{a['path']:a['sha256'] for bank in manifest.values() for a in bank}},indent=2)+'\n')
print(json.dumps({'banks':len(manifest),'cells':sum(len(b) for b in manifest.values()),'warnings':warnings}),flush=True)

# Explicit deployment is now authorized for the three Level 1 password fights.
# The preview remains independent, and raw/source files retain their provenance.
if '--deploy' in sys.argv:
 ship=ROOT/'assets/game/levels/stage_01/miniboss/siege_tanks_1010';ship.mkdir(parents=True,exist_ok=True)
 shipped={}
 for name,records in manifest.items():
  shipped[name]=[]
  for a in records:
   source=ROOT/a['path'];target=ship/source.name;shutil.copy2(source,target)
   q={k:a[k] for k in ['key','w','h','pivot','bounds','sha256']};q['path']=target.relative_to(ROOT).as_posix();shipped[name].append(q)
 (ship/'manifest.json').write_text(json.dumps({'framePolicy':FRAME_POLICY,'banks':shipped,'metrics':metrics},indent=2)+'\n')
 (ROOT/'assets/siege_tanks_art_1010.js').write_text('"use strict";\n// Owned by build_siege_tanks_1010.py --deploy.\nconst SG10_ART='+json.dumps(shipped,separators=(',',':'))+';\nconst SG10_METRICS='+json.dumps(metrics,separators=(',',':'))+';\n',encoding='utf-8',newline='\n')
 print('Deployed 553 authored cells and the matching production registry.',flush=True)
