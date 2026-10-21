"""Rebuild selected UI textures and the corrected complete Cole bank from saved masters."""
from pathlib import Path
from PIL import Image
import json
R=Path(__file__).resolve().parents[1];S=R/'_ART_SOURCES/ui_production_1020';D=R/'assets/game/shared/ui/command_1020';P=R/'assets/game/pilots/cole/body_frames/front_identity_1020'
D.mkdir(parents=True,exist_ok=True);P.mkdir(parents=True,exist_ok=True)
for side,x in [('left',0),('right',1160)]:
 im=Image.open(S/'masters/hud-a.png').convert('RGBA');im.crop((x,0,x+376,1024)).save(D/('hud-a-'+side+'.webp'),lossless=True)
im=Image.open(S/'masters/dialogue-a.png').convert('RGBA');r=im.getchannel('A').point(lambda v:255 if v>128 else 0).getbbox();r=(r[0]-4,r[1]-4,r[2]+4,r[3]+4);r=(r[0],r[1],r[2]+(r[2]-r[0])%2,r[3]+(r[3]-r[1])%2);im.crop(r).save(D/'dialogue-a.webp',lossless=True)
for pose in ['neutral','report','horror','talk']:
 im=Image.open(S/'masters'/('cole-corrected-'+pose+'.png')).convert('RGBA');assert im.width<=888 and im.height<=1776
 canvas=Image.new('RGBA',(888,1776));canvas.alpha_composite(im,(0,0));canvas.resize((512,1024),Image.Resampling.NEAREST).save(P/('cole-'+pose+'.webp'),lossless=True)
for f in [*D.glob('*.webp'),*P.glob('*.webp')]:
 im=Image.open(f);assert im.width%2==0 and im.height%2==0
print('Selected UI and corrected complete Cole frames rebuilt; no atlases or combat changed.')
