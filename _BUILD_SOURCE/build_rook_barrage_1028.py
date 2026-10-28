from pathlib import Path
import numpy as np
from PIL import Image
from pixel_glow_1015 import emissive,used_mask,rings,RING_A
R=Path(__file__).resolve().parents[1];D=R/'assets/game/levels/stage_06/boss/rook_barrage_1028';D.mkdir(parents=True,exist_ok=True)
Image.open(R/'_ART_SOURCES/rook_barrage_1028/spin_symbol.png').save(D/'spin_symbol.png')
sheet=Image.new('RGBA',(384,384))
for phase in range(2):
 im=Image.open(R/f'assets/game/levels/stage_05/boss/stage5_archmage_0916/blaster_0922/fx_{4+phase}.png').convert('RGBA').crop((88,16,136,240));im.thumbnail((12,30));base=Image.new('RGBA',(48,48));base.paste(im,((48-im.width)//2,(48-im.height)//2))
 for f in range(32):
  i=phase*32+f;sheet.paste(base.rotate(-f*360/32,resample=Image.Resampling.BICUBIC),((i%8)*48,(i//8)*48))
sheet.save(D/'slugs.png')
a=np.array(Image.open(R/'assets/game/levels/stage_06/boss/rough_riders_1028/flight_rook.png').convert('RGBA'));h,w=a.shape[:2];mask=emissive(a,used_mask(h,w,[[0,0,w,h]]),1);g=rings(mask,a[:,:,:3].astype(np.float32),RING_A,1,.48);Image.fromarray(g.clip(0,255).astype(np.uint8)).save(D/'hull_glow.png')
print('64 slug cells and source-aligned Rook glow')

import json
(D/'manifest.json').write_text(json.dumps(dict(slugs=dict(cell=[48,48],pivot=[24,24],columns=8,headings=32,phases=2,sourceCrop=[88,16,48,224]),spinSymbol=dict(cell=[64,64],pivot=[32,32],job='7ecfa71c-5e04-478e-b98c-ca60e138ff6b'),hullGlow=dict(source='rr33_flight_rook',cell=[192,192],pivot=[96,96])),indent=2))
