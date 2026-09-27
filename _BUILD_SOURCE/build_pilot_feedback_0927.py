"""Register the generated ice-breath sheet unchanged, with measured nozzle roots."""
from pathlib import Path
from PIL import Image
import json,shutil

ROOT=Path(__file__).resolve().parent.parent
info=json.loads((ROOT/'docs/pilot_feedback_art_0927.json').read_text(encoding='utf-8'))
source=Path('C:/Users/Mdogg/.codex/generated_images/01a0e3c8-265d-7731-8ffe-ee42ebb5ba3c')/info['source']
dest=ROOT/'assets/game/pilot_feedback_0927/ice_breath.png'
if source.exists():
 dest.parent.mkdir(parents=True,exist_ok=True)
 shutil.copyfile(source,dest)
im=Image.open(dest)
assert im.mode=='RGBA' and im.size==(1024,1536)
# Alpha-supported lower central roots measured once from the approved generation.
# Keep these per-cell anchors: centering the whole cell shifts the nozzle in motion.
roots=[(135,494),(131,494),(124,494),(118,494),(136,490),(131,490),
       (124,490),(118,490),(136,480),(131,479),(124,479),(118,479)]
meta={'path':dest.relative_to(ROOT).as_posix(),
      'frames':[[i%4*256,i//4*512,256,512,*r] for i,r in enumerate(roots)],
      'fps':18,'reachPixels':460,'widthPixels':214}
(ROOT/'assets/pilot_feedback_art_0927.js').write_text('"use strict";\nconst PILOT_FEEDBACK_ART='+json.dumps(meta,separators=(',',':'))+';\n',encoding='utf-8',newline='\n')
taxonomy=ROOT/'assets/data/ART_TAXONOMY.json'
data=json.loads(taxonomy.read_text(encoding='utf-8'))
data['ice_breath_0927']={'role':'effect','sheet':None,'note':'Built-in image generation September 27: twelve frames of rolling cold vapor and travelling ice shards. Original RGBA preserved, 4x3 cells of 256x512. Per-cell nozzle roots in assets/pilot_feedback_art_0927.js; owning build _BUILD_SOURCE/build_pilot_feedback_0927.py; source/prompt docs/pilot_feedback_art_0927.json. Sustained Freezer breath uses simulation time, 18fps, existing reach and damage envelope.'}
taxonomy.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
print('Registered twelve ice-breath frames; original alpha preserved.')
