from pathlib import Path
from PIL import Image
import json,hashlib
ROOT=Path('D:/BOF-Downloads/2026-11-14/RevG-source');SRC=ROOT/'_ART_SOURCES/hq_swarm_1115';OUT=ROOT/'_shots/hq_swarm_1115';INSTALL=OUT/'reproduced';checks=[]
meta=json.loads((SRC/'manifest.json').read_text(encoding='utf8'))
for pk,a in meta['flips'].items():
 sheet=Image.new('RGBA',(1024,512))
 for f in range(8):
  cell=Image.open(SRC/(pk+'-flip-%02d.png'%f)).convert('RGBA');assert cell.size==(256,256)
  sheet.alpha_composite(cell,((f%4)*256,(f//4)*256))
  if f in [0,7]:assert cell.tobytes()==Image.open(ROOT/('_ART_SOURCES/hq_turns_1115/'+pk+'/00.png')).convert('RGBA').tobytes()
 dest=INSTALL/a['path'];dest.parent.mkdir(parents=True,exist_ok=True);sheet.save(dest,lossless=True)
 digest=hashlib.sha256(dest.read_bytes()).hexdigest();assert digest==a['sha256'];checks.append({'pilot':pk,'sha256':digest,'exact':True,'evenCells':True,'fixedPivot':[128,128],'seamlessExitPose':True})
(INSTALL/'assets/hq_swarm_art_1115.js').write_text('"use strict";\nconst HQ22_ART='+json.dumps(meta,separators=(',',':'))+';\n',encoding='utf8',newline='\n')
assert (INSTALL/'assets/hq_swarm_art_1115.js').read_bytes()==(ROOT/'assets/hq_swarm_art_1115.js').read_bytes()
(OUT/'reproduction-qa.json').write_text(json.dumps({'checks':checks,'registryExact':True},indent=2),encoding='utf8')
print('Both somersault pages and registry reproduced exactly from retained cells; exit endpoints pixel-exact.')
