"""Own 32-frame authored effect reels; equal-cell crops and alpha cleanup only."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];SRC=ROOT/'_ART_SOURCES/arcade_finish_1010';DEST=ROOT/'assets/game/shared/combat/arcade_finish_1010';DEST.mkdir(parents=True,exist_ok=True)
FILES={'electric_ring':'electric_ring_32_clean.png','plasma_blast':'plasma_blast_32_padded.png','fire_ring':'fire_ring_32_clean.png'}
manifest={};proof={}
for name,file in FILES.items():
 raw=Image.open(SRC/'returned'/file).convert('RGBA');frames=[];hashes=[]
 for i in range(32):
  rect=[round(i%4*raw.width/4),round(i//4*raw.height/8),round((i%4+1)*raw.width/4),round((i//4+1)*raw.height/8)]
  cell=raw.crop(rect);a=np.array(cell);a[:,:,3][a[:,:,3]<64]=0;cell=Image.fromarray(a)
  if any(np.any(v) for v in [a[0,:,3],a[-1,:,3],a[:,0,3],a[:,-1,3]]):raise ValueError(name+' cell '+str(i)+' touches a source boundary')
  if name=='plasma_blast':cell=cell.resize((round(cell.width*1.15),round(cell.height*1.15)),Image.Resampling.NEAREST)
  # Identical canvas, common scale, fixed source cell centre: expansion remains
  # authored. Never fit each silhouette to the cell, duplicate or blend frames.
  canvas=Image.new('RGBA',(256,256));canvas.alpha_composite(cell,(round(128-cell.width/2),round(128-cell.height/2)))
  path=DEST/f'{name}_{i:02d}.png';canvas.save(path,optimize=True);h=hashlib.sha256(canvas.tobytes()).hexdigest();hashes.append(h)
  frames.append({'key':f'af10_{name}_{i}','path':path.relative_to(ROOT).as_posix(),'w':256,'h':256,'pivot':[128,128],'rect':rect})
 if len(set(hashes))!=32:raise ValueError(name+' has repeated frames')
 manifest[name]=frames;proof[name]={'source':file,'source_sha256':hashlib.sha256((SRC/'returned'/file).read_bytes()).hexdigest(),'frames':32,'unique':len(set(hashes))}
(SRC/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
(ROOT/'assets/arcade_finish_art_1010.js').write_text('"use strict";\n// Owned by _BUILD_SOURCE/build_arcade_finish_1010.py.\nconst AF10_ART='+json.dumps(manifest,separators=(',',':'))+';\n',encoding='utf-8',newline='\n')
(SRC/'provenance.json').write_text(json.dumps({'tool':'image_gen.imagegen','banks':proof,'normalization':'Alpha below64 removed; equal-cell crop; common scale and fixed center;32 distinct authored cells per reel.','outputs':{f['path']:hashlib.sha256((ROOT/f['path']).read_bytes()).hexdigest() for bank in manifest.values() for f in bank}},indent=2)+'\n',encoding='utf-8')
print('Built96 unique authored effect cells',flush=True)
