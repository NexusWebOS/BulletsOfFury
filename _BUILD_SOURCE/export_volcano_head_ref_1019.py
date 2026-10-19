"""One actual Stage 8 volcano head, at native pixel scale, for PixelLab."""
from pathlib import Path
import hashlib,json
from PIL import Image
R=Path(__file__).resolve().parents[1]
S=R/'_ART_SOURCES/volcano_head_1019';S.mkdir(exist_ok=True)
source=R/'assets/game/levels/stage_08/boss/identity_1018/v19_volcano_head.png'
im=Image.open(source).convert('RGBA')
# Preserve one proportional scale. The existing authored mount is (160,112).
# Shared transparent padding keeps every prospective rotation inside 128x128.
frame=im.crop((96,48,224,176))
frame.save(S/'reference.png',optimize=True)
# These are exact orientation bookends, not claimed generated animation poses.
# PixelLab supplies the intervening drawings. Every bookend has the same pivot.
for quarter in range(4):
 frame.rotate(-quarter*90,resample=Image.Resampling.NEAREST,center=(64,64)).save(S/f'bookend_{quarter}.png',optimize=True)
data=dict(source=source.relative_to(R).as_posix(),sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
          sourceCanvas=list(im.size),sourceMount=[160,112],frame=[128,128],pivot=[64,64],
          proportionalScale=1,bounds=frame.getbbox(),translation=[-96,-48])
(S/'reference-registration.json').write_text(json.dumps(data,indent=2)+'\n')
print(json.dumps(data))
