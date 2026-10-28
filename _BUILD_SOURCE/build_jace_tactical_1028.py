"""Build fixed 64-cell Jace roller spin and 1015 own-ring light from PixelLab source frames."""
from pathlib import Path
import json
import numpy as np
from PIL import Image
from pixel_glow_1015 import rings, RING_A
R=Path(__file__).resolve().parents[1]
S=R/'_ART_SOURCES/jace_tactical_1028'
D=R/'assets/game/levels/stage_06/boss/jace_tactical_1028'
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
(D/'manifest.json').write_text(json.dumps(dict(cell=[64,64],pivot=[32,32],frames=16,columns=4,fps=24,source_job='31f5eecb-3fa3-4612-97c0-2374a9db84d0',source='Jace nhxsb_g_2',builder='_BUILD_SOURCE/build_jace_tactical_1028.py'),indent=2))
print('16 fixed 64x64 cells with matched 1015 glow')

# Whole authored hull edge light, aligned to the existing idle/attack cells.
from scipy import ndimage
for kind in ['idle','attack']:
 im=Image.open(R/f'assets/game/levels/stage_06/boss/air_refit_1021/jace/{kind}.webp').convert('RGBA');a=np.array(im)
 opaque=a[:,:,3]>100
 mask=opaque&(ndimage.distance_transform_edt(opaque)<=2)
 rgb=np.zeros(a.shape[:2]+(3,),np.float32);rgb[:]=[255,110,35]
 glow=rings(mask,rgb,RING_A,1,.48)
 Image.fromarray(glow.clip(0,255).astype(np.uint8)).save(D/f'{kind}_glow.png')
