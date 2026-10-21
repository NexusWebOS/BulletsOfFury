from pathlib import Path
import argparse, json, shutil
from PIL import Image

R=Path(__file__).resolve().parents[1]
ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path);ap.add_argument('--architecture',type=Path);a=ap.parse_args()
A=R/'_ART_SOURCES/stormglass_1020';A.mkdir(parents=True,exist_ok=True)
source=A/'generated-terrain.png'
if a.source and not source.exists():shutil.copy2(a.source,source)
layer=A/'generated-architecture.png'
if a.architecture and not layer.exists():shutil.copy2(a.architecture,layer)
im=Image.open(layer if layer.exists() else source).convert('RGBA')
size=(680,round(im.height*680/im.width/2)*2)
terrain=im.resize(size,Image.Resampling.NEAREST)
D=R/'assets/game/levels/tutorial/stormglass_1020';D.mkdir(parents=True,exist_ok=True)
target=D/('architecture.webp' if layer.exists() else 'terrain.webp')
terrain.save(target,lossless=True,method=6)
if layer.exists() and (D/'terrain.webp').exists():
 shutil.move(str(D/'terrain.webp'),str(A/'superseded-flat-terrain.webp'))
audit={'source':str(source.relative_to(R)),'source_size':list(im.size),'canvas':list(size),
 'proportional_scale':680/im.width,'normalization':'nearest; even canvas; no per-frame resizing',
 'registration':'sg20_stormglass in assets/stormglass_tutorial_1020.js',
 'runtime_bytes':target.stat().st_size,'generator':'built-in image generation',
 'layers':{'ocean':'native authored nlq2_water / nwl_water animation, 6fps,10px/s','far_clouds':'native 6-pose low rolling bank,15px/s','academy':'generated transparent architecture,28px/s','near_clouds':'native 6-pose low rolling bank,39px/s; all layers below gameplay'},
 'ship_references':'none required: terrain has no ships; actual native aircraft render in game'}
(A/'audit.json').write_text(json.dumps(audit,indent=2),encoding='utf-8')
(D/'README.md').write_text('# Stormglass Academy\n\nTutorial-only authored scrolling terrain. '+
 'Generated with the built-in image tool; source and exact prompt in `_ART_SOURCES/stormglass_1020`. '+
 'Rebuild with `_BUILD_SOURCE/build_stormglass_1020.py`. '+
 '680px wide, proportional nearest sampling, even canvas. Transparent architecture sits between independently animated native ocean and cloud layers. '+
 'Registered lazily by `stormglass_tutorial_1020.js`; not on campaign boot preload.\n',encoding='utf-8')
print(json.dumps(audit))
