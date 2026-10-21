"""Bright Stage1 blue palette of the approved PixelLab ocean. No new generation."""
from pathlib import Path
from PIL import Image,ImageDraw
import numpy as np,json,hashlib
R=Path(__file__).resolve().parents[1]
D=R/'assets/game/levels/stage_01/terrain/water_pixellab_1020'
Q=R/'_shots/stage1_water_1020'
A=R/'_ART_SOURCES/stage1_water_palette_1020'
for p in [D,Q,A]:p.mkdir(parents=True,exist_ok=True)
source=R/'assets/game/levels/tutorial/stormglass_1020/water/ocean.json'
m=json.loads(source.read_text(encoding='utf-8'))
src=R/m['path'];pixels=np.array(Image.open(src).convert('RGBA'))
# One fixed monotone brightness ramp for every pixel, frame and extruded gutter.
# Matches the original Stage1 royal-blue depths/cyan-white crests; no temporal
# normalization or changes to geometry, source-phase order, alpha, or motion.
knots=[29,46,52,60,80,110,150,200,244]
ramp=[[0,20,110],[0,34,190],[0,62,235],[6,100,251],[36,150,255],
      [92,196,255],[155,226,255],[214,247,255],[246,255,255]]
value=pixels[:,:,:3].mean(axis=2)
for channel in range(3):pixels[:,:,channel]=np.rint(np.interp(value,knots,[p[channel] for p in ramp])).astype(np.uint8)
sheet=Image.fromarray(pixels);sheet.save(D/'ocean.webp',lossless=True,method=6)
m.update(key='s1w20_ocean',path='assets/game/levels/stage_01/terrain/water_pixellab_1020/ocean.webp',
         revision='stage1-blue-water-1020',palette='Stage1 royal blue / cyan-white crest',
         source_atlas=str(src.relative_to(R)).replace('\\','/'),palette_knots=knots,palette_rgb=ramp)
(D/'ocean.json').write_text(json.dumps(m,indent=2),encoding='utf-8')
registration="'use strict';\n/* Generated together with atlas/cells by build_stage1_water_1020.py. */\nconst S1W20_ART="+json.dumps(m,separators=(',',':'))+";\nXART._src[S1W20_ART.key]=S1W20_ART.path;\nwindow.BOF_STAGE1_WATER_ART=S1W20_ART;\n"
(R/'assets/stage1_water_art_1020.js').write_text(registration,encoding='utf-8',newline='\n')
frames=[sheet.crop((x,y,x+w,y+h)).convert('RGB') for x,y,w,h in m['cells']]
frames[0].save(Q/'water-loop.gif',save_all=True,append_images=frames[1:],duration=83,loop=0,optimize=False)
grid=Image.new('RGB',(448,448))
for x in range(2):
 for y in range(2):grid.paste(frames[0],(x*224,y*224))
grid.save(Q/'tile-seams.png')
contact=Image.new('RGB',(1024,584),'#071322');g=ImageDraw.Draw(contact)
for i,im in enumerate(frames):
 x=i%8*128;y=i//8*146;contact.paste(im.resize((128,128),Image.Resampling.NEAREST),(x,y));g.text((x+4,y+130),str(i),fill='white')
contact.save(Q/'all-frames.png')
audit={'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),
       'output_sha256':hashlib.sha256((D/'ocean.webp').read_bytes()).hexdigest(),
       'frames':len(frames),'distinct_frames':len({hashlib.sha256(im.tobytes()).hexdigest() for im in frames}),
       'geometry_unchanged':m['cells']==json.loads(source.read_text(encoding='utf-8'))['cells'],
       'alpha_unchanged':bool(np.array_equal(pixels[:,:,3],np.array(Image.open(src).convert('RGBA'))[:,:,3])),
       'palette_knots':knots,'palette_rgb':ramp,'runtime_bytes':(D/'ocean.webp').stat().st_size+len(registration.encode()),
       'new_generation_cost':0,'source_jobs':[m['seed_job'],m['animation_job']]}
(A/'audit.json').write_text(json.dumps(audit,indent=2),encoding='utf-8')
(D/'README.md').write_text('Stage1 bright-blue palette of the approved PixelLab Stormglass ocean.\n32 real generated phases,12fps,224x224 cells,2px edge extrusion. Geometry, alpha and phase order unchanged.\nRebuild atlas/cells/registry together with _BUILD_SOURCE/build_stage1_water_1020.py.\nRuntime stage1_water_1020.js replaces water only; jungle land/masks/boats are native.\n',encoding='utf-8')
print(json.dumps(audit))
