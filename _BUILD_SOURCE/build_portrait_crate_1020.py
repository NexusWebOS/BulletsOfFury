"""Re-export the approved framed portrait and exclusive Hammer pickup art."""
from pathlib import Path
from PIL import Image
R=Path(__file__).resolve().parents[1];S=R/'_ART_SOURCES/portrait_crate_1020/masters'
for name,size,dst in [('portrait',512,'assets/game/levels/stage_08/cinematics/dracodia_portrait_box_1020/portrait.webp'),('crate',128,'assets/game/shared/pickups/hammer_chaingun_1020/crate.webp'),('icon',128,'assets/game/shared/pickups/hammer_chaingun_1020/icon.webp')]:
 im=Image.open(S/(name+'.png')).convert('RGBA');assert im.width==im.height
 out=R/dst;out.parent.mkdir(parents=True,exist_ok=True);im.resize((size,size),Image.Resampling.NEAREST).save(out,lossless=True)
print('Re-exported three even-sized assets; game code/atlases unchanged.')
