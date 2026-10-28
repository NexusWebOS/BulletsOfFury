"""Build fixed 64-cell Kaia roller spin and 1015 own-ring light from PixelLab source frames."""
from pathlib import Path
import json
import numpy as np
from PIL import Image
from pixel_glow_1015 import rings, RING_A
R=Path(__file__).resolve().parents[1]
S=R/'_ART_SOURCES/kaia_roller_1028'
D=R/'assets/game/levels/stage_06/boss/kaia_roller_1028'
D.mkdir(parents=True,exist_ok=True)
sheet=Image.new('RGBA',(256,256));glow=Image.new('RGBA',(256,256))
for i in range(16):
 im=Image.open(S/f'frame_{i+1:02}.png').convert('RGBA')
 assert im.size==(64,64),im.size
 a=np.array(im);yy,xx=np.indices((64,64));radius=np.hypot(xx-31.5,yy-31.5)
 # Only the authored bright rim, plus its three hard pixel rings; no pasted halo.
 mask=(a[:,:,3]>100)&(a[:,:,:3].max(2)>160)&(radius>19)
 g=rings(mask,a[:,:,:3].astype(np.float32),RING_A,1,.48)
 light=Image.fromarray(g.clip(0,255).astype(np.uint8))
 sheet.paste(im,((i%4)*64,(i//4)*64));glow.paste(light,((i%4)*64,(i//4)*64))
sheet.save(D/'spin.png');glow.save(D/'spin_glow.png')
(D/'manifest.json').write_text(json.dumps(dict(cell=[64,64],pivot=[32,32],frames=16,columns=4,fps=24,source_job='844ae6ba-7005-4880-99be-dbe891009d3b',source='Falva nfrb_3',builder='_BUILD_SOURCE/build_kaia_rollers_1028.py'),indent=2))
print('16 fixed 64x64 cells with matched 1015 glow')
