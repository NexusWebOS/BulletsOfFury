"""Register the generated Warden rotary gun at one fixed mechanical pivot."""
from pathlib import Path
import hashlib,json,shutil
from collections import deque
import numpy as np
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'_ART_SOURCES/warden_center_1018';DST=ROOT/'assets/game/levels/stage_04/enemies/warden_center_1018'
OUT=ROOT/'_shots/stage4_engine_1018';SRC.mkdir(parents=True,exist_ok=True);DST.mkdir(parents=True,exist_ok=True);OUT.mkdir(parents=True,exist_ok=True)
raw=SRC/'warden_center_sheet.png'
if not raw.exists():shutil.copyfile(Path.home()/'.codex/generated_images/01a0e3c8-265d-7731-8ffe-ee42ebb5ba3c/exec-249ab428-5075-4308-a755-61d5372a3145.png',raw)
im=Image.open(raw).convert('RGBA');cuts=[round(i*im.width/4) for i in range(5)]
# The service returned a1254px sheet, so source cuts retain its odd measurements.
# Delivered cells are all256x256. A single0.70 scale, followed by integer shifts,
# registers the bronze mounting ring; no individual fitting or warped poses.
SCALE=.70;PIVOT=(128,104);records=[];frames=[]
anchor_y=[154,145,132,114];tip_y=[300,294,234,266]
for r in range(4):
 for c in range(4):
  i=r*4+c;rect=(cuts[c],cuts[r],cuts[c+1],cuts[r+1]);cell=im.crop(rect);p=np.array(cell)
  # Discard only isolated fragments of the NEXT grid cell touching this cut.
  # The generator's fractional cell grid leaked the following roof into row3.
  occupied=p[:,:,3]>0;seen=np.zeros_like(occupied);removed=0
  for xx in np.where(occupied[-1])[0]:
   if seen[-1,xx]:continue
   todo=deque([(int(xx),cell.height-1)]);component=[];seen[-1,xx]=True
   while todo:
    x0,y0=todo.popleft();component.append((x0,y0))
    for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)):
     x1,y1=x0+dx,y0+dy
     if 0<=x1<cell.width and 0<=y1<cell.height and occupied[y1,x1] and not seen[y1,x1]:seen[y1,x1]=True;todo.append((x1,y1))
   if cell.height-min(y for x,y in component)<20:
    for x0,y0 in component:p[y0,x0]=0
    removed+=len(component)
  cell=Image.fromarray(p)
  R,G,B=p[:,:,:3].astype(float).transpose(2,0,1)
  mask=(p[:,:,3]>200)&(R>65)&(G>45)&(B>25)&(R>G*1.12)&(G>B*1.12)&(R<G*1.9)&(R<210)
  y,x=np.where(mask);anchor=(round((int(x.min())+int(x.max()))/2),anchor_y[r])
  adjacent=None
  if r==2:
   # Measured next-row steel roof, beyond this row's flame tails. It overlaps
   # alpha halos, so connected-component trimming alone cannot separate it.
   adjacent=[anchor[0]-40,298,anchor[0]+40,cell.height]
   p[adjacent[1]:adjacent[3],adjacent[0]:adjacent[2]]=0;cell=Image.fromarray(p)
  scaled=cell.resize((round(cell.width*SCALE),round(cell.height*SCALE)),Image.Resampling.NEAREST)
  shift=(PIVOT[0]-round(anchor[0]*SCALE),PIVOT[1]-round(anchor[1]*SCALE))
  frame=Image.new('RGBA',(256,256));frame.alpha_composite(scaled,shift);assert frame.getbbox()[0]>0 and frame.getbbox()[1]>0 and frame.getbbox()[2]<256 and frame.getbbox()[3]<256
  path=DST/f'gun_{i:02}.png';frame.save(path,optimize=True);frames.append(frame)
  muzzles=[[PIVOT[0]+round(dx*SCALE),PIVOT[1]+round((tip_y[r]-anchor[1])*SCALE)] for dx in (-32,31)]
  records.append(dict(key=f'wc18_gun_{i:02}',path=path.relative_to(ROOT).as_posix(),w=256,h=256,pivot=list(PIVOT),sourceRect=list(rect),sourceAnchor=list(anchor),shift=list(shift),muzzles=muzzles,removedAdjacentCellPixels=removed,adjacentCellTrim=adjacent,ink=list(frame.getbbox()),sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
N=32;masks=[]
for frame,record in zip(frames,records):
 alpha=np.array(frame)[:,:,3];alpha[max(p[1] for p in record['muzzles'])+2:]=0;rows=[]
 for y in range(N):
  bits=0
  for x in range(N):bits=(bits<<1)|int(alpha[y*8:(y+1)*8,x*8:(x+1)*8].max()>120)
  rows.append(f'{bits:08x}')
 masks.append(dict(n=N,rows=rows))
art=dict(frames=records,pivot=list(PIVOT),size=[256,256],sourceScale=SCALE,masks=masks,banks=dict(idle=[0,4,8],charge=[4,4,10],fire=[8,4,20],cool=[12,4,10]))
(DST/'manifest.json').write_text(json.dumps(art,indent=2)+'\n',encoding='utf-8')
(ROOT/'assets/warden_center_art_1018.js').write_text('"use strict";\n// Owned by _BUILD_SOURCE/build_warden_center_1018.py.\nconst WC18_ART='+json.dumps(art,separators=(',',':'))+';\n',encoding='utf-8',newline='\n')
audit=dict(service='built-in image generator',reference='assets/game/shared/combat/modular_roster_0927/iron.png',frames=16,frameSize=[256,256],pivot=list(PIVOT),scale=SCALE,sourceSize=list(im.size),note='Single full-sheet generation; exact nearest-neighbour proportional normalization and transparent padding. Fixed mounting ring; authored barrel/recoil/glow/flash/smoke poses. No atlas edits.',registration=records)
(SRC/'generation.json').write_text(json.dumps(audit,indent=2)+'\n',encoding='utf-8')
sheet=Image.new('RGBA',(1024,1024),(8,17,28,255));d=ImageDraw.Draw(sheet)
for i,f in enumerate(frames):
 x=(i%4)*256;y=(i//4)*256;sheet.alpha_composite(f,(x,y));d.line((x+120,y+104,x+136,y+104),fill='#53c7ff');d.line((x+128,y+96,x+128,y+112),fill='#53c7ff');d.text((x+6,y+6),str(i),fill='white')
sheet.save(OUT/'turret-registration.png')
frames[0].save(OUT/'turret.gif',save_all=True,append_images=frames[1:],duration=100,loop=0,disposal=2)
tax=ROOT/'assets/data/ART_TAXONOMY.json';data=json.loads(tax.read_text(encoding='utf-8-sig'));data.pop('wc18_',None)
data={'wc18_':dict(role='stage4_iron_warden_modular_centre_rotary_cannon',sheet=None,note='16 generated gun poses256x256/pivot128,104:4 idle,4 charge,4 fire,4 cooldown. Actual Iron Warden armor reference; one0.70 proportional source scale and shared transparent padding. Own build_warden_center_1018.py registers pixels, muzzles and mask. Runtime warden_center_1018.js owns a damageable, flashing gunC; authored whole boss hull remains intact. No atlas edits.'),**data}
tax.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print('Exported16 fixed256x256 frames, pivot128,104, common scale0.70; registration sheet and manifest.')
