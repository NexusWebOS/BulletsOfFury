"""Export a molten-lava palette from the approved32-phase PixelLab surface."""
from pathlib import Path
from PIL import Image
import numpy as np,json,hashlib
R=Path(__file__).resolve().parents[1];D=R/'assets/game/levels/stage_02/terrain/lava_pixellab_1020'
Q=R/'_shots/arena_download_1020';A=R/'_ART_SOURCES/arena_download_1020'
for p in [D,Q,A]:p.mkdir(exist_ok=True,parents=True)
m=json.loads((R/'assets/game/levels/tutorial/stormglass_1020/water/ocean.json').read_text(encoding='utf-8'))
source=R/m['path'];a=np.array(Image.open(source).convert('RGBA'));value=a[:,:,:3].mean(2)
knots=[29,46,52,60,80,110,150,200,244]
ramp=[[25,4,11],[93,14,11],[158,30,8],[217,51,8],[246,98,15],[255,154,32],[255,209,85],[255,241,160],[255,252,215]]
for ch in range(3):a[:,:,ch]=np.rint(np.interp(value,knots,[p[ch] for p in ramp])).astype(np.uint8)
atlas=Image.fromarray(a);atlas.save(D/'lava.webp',lossless=True,method=6)
m.update(key='s2l20_lava',path='assets/game/levels/stage_02/terrain/lava_pixellab_1020/lava.webp',revision='stage2-lava-1020',
 palette='Molten basalt / crimson / orange / gold',source_atlas=str(source.relative_to(R)).replace('\\','/'),palette_knots=knots,palette_rgb=ramp)
(D/'lava.json').write_text(json.dumps(m,indent=2),encoding='utf-8')
s="'use strict';\n/* Atlas/cells generated together by build_stage2_lava_1020.py. */\nconst S2L20_ART="+json.dumps(m,separators=(',',':'))+";\nXART._src[S2L20_ART.key]=S2L20_ART.path;\nwindow.BOF_STAGE2_LAVA_ART=S2L20_ART;\n"
(R/'assets/stage2_lava_art_1020.js').write_text(s,encoding='utf-8',newline='\n')
frames=[atlas.crop((x,y,x+w,y+h)).convert('RGB') for x,y,w,h in m['cells']]
frames[0].save(Q/'lava-loop.gif',save_all=True,append_images=frames[1:],duration=83,loop=0,optimize=False)
audit={'frames':32,'distinct':len({hashlib.sha256(f.tobytes()).hexdigest() for f in frames}),'atlas':list(atlas.size),'cell':[224,224],
 'bytes':(D/'lava.webp').stat().st_size+len(s.encode()),'new_generation_cost':0,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'palette_knots':knots,'palette_rgb':ramp}
(A/'lava-audit.json').write_text(json.dumps(audit,indent=2),encoding='utf-8');print(json.dumps(audit))
