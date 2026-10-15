"""Normalize candidate modules; shipping jets and preview bosses have separate registries."""
from pathlib import Path
import ast,json,hashlib
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];SRC=ROOT/'_ART_SOURCES/arcade_candidates_1010';DEST=SRC/'normalized';DEST.mkdir(exist_ok=True)
# Reuse the owner's registration function without executing its build workflow.
tree=ast.parse((ROOT/'_BUILD_SOURCE/build_smooth_motion_1009.py').read_text());node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='registration')
exec(compile(ast.Module(body=[node],type_ignores=[]),'registration-owner','exec'),globals())
manifest={}
for name in ['razorback_hull','furious_razorback_hull','overlord_hull','razorback_kit','furious_razorback_kit','overlord_kit','fire_jet','ice_jet']:
 raw=Image.open(SRC/'returned'/(name+'.png')).convert('RGBA');groups=4 if name.endswith('_kit') else 1
 for group in range(groups):
  bank=name+('_'+str(group) if groups>1 else '');n=4 if groups>1 else 16;cells=[];rects=[]
  for f in range(n):
   i=group*4+f;rect=[round(i%4*raw.width/4),round(i//4*raw.height/4),round((i%4+1)*raw.width/4),round((i//4+1)*raw.height/4)];rects.append(rect)
   a=np.array(raw.crop(rect));a[:,:,3][a[:,:,3]<64]=0;cells.append(Image.fromarray(a))
  boxes=[c.getchannel('A').point(lambda a:255 if a>160 else 0).getbbox() for c in cells]
  ink=[min(b[0] for b in boxes),min(b[1] for b in boxes),max(b[2] for b in boxes),max(b[3] for b in boxes)]
  # Generated grids drift by more than one small correlation search. First
  # translate the complete fixed chassis into the first cell's bounds, then
  # correlate its unchanged core. Scale remains common throughout the reel.
  initial=[(round((boxes[0][0]+boxes[0][2]-b[0]-b[2])/2),round((boxes[0][1]+boxes[0][3]-b[1]-b[3])/2)) for b in boxes]
  if groups>1:
   # Recoil, doors and rotor blades change the silhouette; match only the
   # stationary mounting fixture, never the muzzle flame or changing blades.
   if group==3 or (group==0 and name=='overlord_kit'):shifts=initial
   else:
    fixture=[ink[0],ink[1],ink[2],ink[1]+(ink[3]-ink[1])*.35]
    shifts=registration(cells,fixture)
  else:
   aligned=[]
   for c,(dx,dy) in zip(cells,initial):
    out=Image.new('RGBA',(c.width+192,c.height+192));out.alpha_composite(c,(96+dx,96+dy));aligned.append(out)
   residual=registration(aligned,[v+96 for v in boxes[0]])
   shifts=[(dx+rx,dy+ry) for (dx,dy),(rx,ry) in zip(initial,residual)]
  pivot=[(boxes[0][0]+boxes[0][2])/2,(boxes[0][1]+boxes[0][3])/2];k=.85
  # Physical weapon sockets are the assembly anchors, independent of barrel
  # length and the silhouette of a firing frame.
  if name=='razorback_hull':pivot=[192,174]
  if name=='furious_razorback_hull':pivot=[195,174]
  if name=='overlord_hull':pivot=[130,170]
  if groups>1:
   if group==0 and name!='overlord_kit':pivot[1]=raw.height/4*.44
   if group in [1,2]:pivot[1]=ink[1]+(ink[3]-ink[1])*.25
  frames=[]
  for f,c in enumerate(cells):
   c=c.resize((round(c.width*k),round(c.height*k)),Image.Resampling.NEAREST);im=Image.new('RGBA',(384,384));dx=round(192-pivot[0]*k+shifts[f][0]*k);dy=round(192-pivot[1]*k+shifts[f][1]*k);im.alpha_composite(c,(dx,dy))
   target=ROOT/'assets/game/shared/combat/arcade_jets_1010' if name in ['fire_jet','ice_jet'] else DEST;target.mkdir(parents=True,exist_ok=True)
   path=target/f'{bank}_{f:02d}.png';im.save(path,optimize=True);frames.append({'key':f'ac10_{bank}_{f}','path':path.relative_to(ROOT).as_posix(),'w':384,'h':384,'pivot':[192,192],'rect':rects[f],'registration':shifts[f]})
  manifest[bank]=frames
(SRC/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
jets={'fire':manifest['fire_jet'],'ice':manifest['ice_jet']}
(ROOT/'assets/arcade_jets_art_1010.js').write_text('"use strict";\n// Owned by _BUILD_SOURCE/build_arcade_candidates_1010.py.\nconst AC10_JET_ART='+json.dumps(jets,separators=(',',':'))+';\n',encoding='utf-8',newline='\n')
preview=ROOT/'docs/previews/neo_geo_stage1_1010';preview.mkdir(parents=True,exist_ok=True)
(preview/'candidate_art.js').write_text('"use strict";\n// Preview only. Owned by _BUILD_SOURCE/build_arcade_candidates_1010.py.\nconst PV10_ART='+json.dumps(manifest,separators=(',',':'))+';\n',encoding='utf-8',newline='\n')
(SRC/'provenance.json').write_text(json.dumps({'tool':'image_gen.imagegen','normalization':'Common scale; masked fixed-chassis translation; shared module mount anchors; no per-frame fit; alpha below64 removed. Rotor keeps hub orientation.','source_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((SRC/'returned').glob('*.png'))},'outputs':{f['path']:hashlib.sha256((ROOT/f['path']).read_bytes()).hexdigest() for bank in manifest.values() for f in bank}},indent=2)+'\n')
print('Built',sum(map(len,manifest.values())),'candidate/jet cells',flush=True)
