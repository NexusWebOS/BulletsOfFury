from pathlib import Path
import numpy as np
from PIL import Image
from pixel_glow_1015 import emissive, used_mask, rings, RING_A
R=Path(__file__).resolve().parents[1];D=R/'assets/game/levels/stage_06/boss/rebel_revision_1026'
src=np.array(Image.open(D/'wall.png').convert('RGBA'));h,w=src.shape[:2]
mask=emissive(src,used_mask(h,w,[[0,0,w,h]]),1)
# The requested wall is self-lit: explicitly include its authored cyan grid.
mask |= (src[:,:,3]>150)&(src[:,:,1]>150)&(src[:,:,2]>145)&(src[:,:,1]>src[:,:,0]*1.18)&(src[:,:,2]>src[:,:,0]*1.15)
glow=rings(mask,src[:,:,:3].astype(np.float32),RING_A,1,.48)
Image.fromarray(glow.clip(0,255).astype(np.uint8)).save(D/'wall_glow.png')
print('1015 emissive pixels',int(mask.sum()),'size',w,h)

