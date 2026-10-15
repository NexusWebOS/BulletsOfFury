"""Owned loose frames; fixed even cells, genuine alpha and shared pivots."""
from pathlib import Path
from PIL import Image
import json,hashlib,shutil
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'_ART_SOURCES/part2_1010';SOURCE.mkdir(parents=True,exist_ok=True)
OUT=ROOT/'assets/game/shared/combat/part2_1010';OUT.mkdir(parents=True,exist_ok=True)
GEN=Path('C:/Users/Mdogg/.codex/generated_images/01a0e3c8-265d-7731-8ffe-ee42ebb5ba3c')
SPECS=[('shield','exec-ce8dd050-425e-4d45-b607-f163be24d371.png',3,3,432),
       ('jace','exec-509bd973-fa3e-4d64-aa18-8d9ceb3436db.png',4,8,256)]
bank={};pilots=['yuri','falva','cole','maverick','axel','juggernaut','lizzie','decker','freezer']
for name,fn,cols,rows,size in SPECS:
 raw=SOURCE/(name+'_raw.png')
 if not raw.exists():shutil.copyfile(GEN/fn,raw)
 im=Image.open(raw).convert('RGBA')
 bank[name]=[];cw,ch=im.width/cols,im.height/rows
 # One common physical scale throughout each bank. Odd crops receive padding.
 factor=min(1,(size-12)/max(cw,ch))
 for i in range(cols*rows):
  r=[round((i%cols)*cw),round((i//cols)*ch),round((i%cols+1)*cw),round((i//cols+1)*ch)]
  cell=im.crop(r);normalization=None
  if name=='jace':
   # Register the physical sphere, ignoring the few trailing electric sparks.
   # Only translation/uniform scale change; no painted pixels or generated tween.
   yy,xx=np.nonzero(np.asarray(cell)[:,:,3]>=192)
   cx,cy=float(np.median(xx)),float(np.median(yy))
   diameter=max(float(np.quantile(xx,.95)-np.quantile(xx,.05)),float(np.quantile(yy,.95)-np.quantile(yy,.05)))
   k=178/diameter
   c=cell.transform((size,size),Image.Transform.AFFINE,(1/k,0,cx-size/(2*k),0,1/k,cy-size/(2*k)),Image.Resampling.NEAREST)
   offset=(0,0);normalization=dict(center=[cx,cy],scale=k,diameter=diameter)
  else:
   cell=cell.resize((round(cell.width*factor),round(cell.height*factor)),Image.Resampling.NEAREST)
   c=Image.new('RGBA',(size,size),(0,0,0,0));offset=((size-cell.width)//2,(size-cell.height)//2);c.alpha_composite(cell,offset)
  label=pilots[i] if name=='shield' else f'{i:02d}';file=OUT/(name+'_'+label+'.png');c.save(file,optimize=True)
  data=file.read_bytes();bank[name].append(dict(key='p2_'+name+'_'+label,path=file.relative_to(ROOT).as_posix(),w=size,h=size,
   pivot=[size//2,size//2],source_rect=r,scale=factor,normalization=normalization,
   sha256=hashlib.sha256(data).hexdigest(),opaque_bounds=c.getbbox()))
 assert len(set(a['sha256'] for a in bank[name]))==cols*rows
from repair_part2_art_1011 import add_repaired_banks
add_repaired_banks(bank)
from part2_motion_art_1011 import add_motion_banks
add_motion_banks(bank)
(ROOT/'assets/part2_art_1010.js').write_text('"use strict";\n// Owned by _BUILD_SOURCE/build_part2_art_1010.py.\nconst P2_ART='+json.dumps(bank,separators=(',',':'))+';\n',encoding='utf-8',newline='\n')
(SOURCE/'provenance.json').write_text(json.dumps(dict(tool='built-in image_gen',references=['_shots/part2_1010/diagnostic/shield_references.png','assets/game/shared/combat/arcade_finish_1010/plasma_blast_14.png','assets/game/levels/stage_06/boss/rebel_arsenal_1004c/jace_nhxsb_g_2.png','assets/game/levels/stage_02/boss/bosses/furnace/fzt_fire_laser_0920.png'],banks=bank),indent=2),encoding='utf-8')
print(json.dumps({k:len(v) for k,v in bank.items()}))
