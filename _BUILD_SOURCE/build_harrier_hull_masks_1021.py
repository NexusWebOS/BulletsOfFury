"""32x40 fixed-pivot glow masks from the Harrier's actual authored gun pixels.
No hull replacement, generated turret, animation fit or source modification.
"""
from pathlib import Path
import json
from PIL import Image
R=Path(__file__).resolve().parents[1]
src=R/'assets/game/levels/stage_06/boss/bosses/skycarrier/carrier_closed_wells.png'
out=R/'assets/game/levels/stage_06/boss/harrier_hull_1021';out.mkdir(exist_ok=True)
im=Image.open(src).convert('RGBA');frames=[]
for i,(x,y,rect) in enumerate([(177,103,(168,86,18,32)),(211,94,(200,76,22,36)),(301,94,(290,76,22,36)),(335,103,(326,86,18,32))]):
 mask=Image.new('RGBA',(32,40));sx,sy,w,h=rect
 for yy in range(sy+1,sy+h-1):
  for xx in range(sx+1,sx+w-1):
   r,g,b,a=im.getpixel((xx,yy));lum=.2126*r+.7152*g+.0722*b
   alpha=round(a*max(0,min(1,(lum-72)/75)))
   if alpha:mask.putpixel((xx-x+16,yy-y+20),(255,255,255,alpha))
 assert mask.getbbox() and not any(mask.getpixel((xx,yy))[3] for xx,yy in [(0,0),(31,0),(0,39),(31,39)])
 path=out/f'gun_{i}.png';mask.save(path,optimize=True)
 frames.append(dict(key=f'hh21_gun_{i}',path=path.relative_to(R).as_posix(),w=32,h=40,pivot=[16,20],sourceRect=list(rect),sourcePivot=[x,y]))
data=dict(source=src.relative_to(R).as_posix(),frames=frames,method='Only actual authored metal highlight pixels; transparent low-luminance hull background. Uniform native-pixel scale.')
(R/'assets/harrier_hull_art_1021.js').write_text('"use strict";\n// Owned by build_harrier_hull_masks_1021.py. Fixed32x40; pivot16,20.\nconst HH21_ART='+json.dumps(data,separators=(',',':'))+';\n',encoding='utf-8')
print(json.dumps(dict(frames=len(frames),bytes=sum((R/f['path']).stat().st_size for f in frames))))
