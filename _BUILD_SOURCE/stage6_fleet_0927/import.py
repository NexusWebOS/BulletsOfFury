"""Normalize the approved generated source; do not redraw or recolor the hulls."""
from pathlib import Path
from PIL import Image
HERE=Path(__file__).resolve().parent
OUT=HERE.parent.parent/'assets/game/stage6_fleet_0927'
OUT.mkdir(parents=True,exist_ok=True)
with Image.open(HERE/'source.png') as im:
 im=im.convert('RGBA')
 for name,box in [('interceptor',(0,0,800,im.height)),('bomber',(800,0,im.width,im.height))]:
  q=im.crop(box);q=q.crop(q.getbbox());q.thumbnail((256,256),Image.Resampling.NEAREST)
  q.save(OUT/(name+'.png'))
