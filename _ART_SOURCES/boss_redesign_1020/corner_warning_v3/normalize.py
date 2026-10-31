from pathlib import Path
from PIL import Image
import json,hashlib
W=Path(__file__).parent
raw=W/'generated-master.png'
im=Image.open(raw).convert('RGBA')
# The selected generated triple-chevron sits in the lower-right of this1280px sheet.
# Preserve the raw sheet and crop only its arrow for the fixed-canvas export.
assert im.width==im.height,im.size
box=tuple(round(v*im.width/1280) for v in (520,700,1150,1140))
arrow=im.crop(box);arrow=arrow.crop(arrow.getbbox())
arrow.save(W/'generated-chevron-source.png')
arrow=arrow.resize((34,round(34*arrow.height/arrow.width)),Image.Resampling.NEAREST)
arrow=arrow.rotate(-45,resample=Image.Resampling.NEAREST,expand=True)
star=Image.open(W/'existing-asterisk.png').convert('RGBA');star=star.crop(star.getbbox());star=star.resize((28,28),Image.Resampling.NEAREST)
canvas=Image.new('RGBA',(64,64))
canvas.alpha_composite(star,(4,4));canvas.alpha_composite(arrow,(42-arrow.width//2,42-arrow.height//2))
assert canvas.getbbox()[2]<=62 and canvas.getbbox()[3]<=62,canvas.getbbox()
variants={'down_right':canvas,'down_left':canvas.transpose(Image.Transpose.ROTATE_270),'up_right':canvas.transpose(Image.Transpose.ROTATE_90),'up_left':canvas.transpose(Image.Transpose.ROTATE_180)}
for name,v in variants.items():v.save(W/('corner-warning-'+name+'.png'),optimize=True)
record=dict(provider='built-in image_gen',selected=str(raw),rejected='exec-888715f9-6798-4fa6-b9b3-2eff2638c0c7.png',sourceArrow='assets/game/shared/ui/ui/warn_0916/escape_arrow.png',sourceAsterisk='assets/bossmode/ui/alerts-yellow.png',asteriskRect=[424,0,384,384],normalization='Generated three-chevron arrow crop, single proportional nearest-neighbor scale and45-degree direction; original in-game hollow yellow asterisk reused unchanged apart from proportional scale; four whole-canvas quarter-turn variants. Fixed64x64 canvas,32,32 pivot.',sourceHash=hashlib.sha256(raw.read_bytes()).hexdigest())
(W/'generation.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(dict(sourceSize=im.size,arrowSize=arrow.size,export=canvas.getbbox(),variants=list(variants))))
