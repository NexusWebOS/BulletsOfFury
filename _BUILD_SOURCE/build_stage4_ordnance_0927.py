"""Normalize generated RGBA frames without repainting or recoloring the source."""
from pathlib import Path
from PIL import Image
import json,shutil
OUT=Path('assets/game/projectiles_0927');OUT.mkdir(parents=True,exist_ok=True)
SOURCE=Path(r'C:\Users\Mdogg\.codex\generated_images\01a0d568-40a4-7b70-97c0-acc501f39d5b\exec-96b6c39d-b174-490b-a0f9-ea427d3ff3c3.png')
raw=OUT/'stage4_ordnance_source.png'
if not raw.exists():shutil.copyfile(SOURCE,raw)
im=Image.open(raw).convert('RGBA');assert im.size==(1024,1536)
sheet=Image.new('RGBA',(1024,1920));frames=[]
# Generated rows have uneven vertical spacing. Cut at the clear gutters, rather
# than through a neighboring rocket flame; retain every frame at shared scale 1.
bands=[0,240,484,746,1034,1256,1536]
for row,role in enumerate(['steel','brass','rocket','missile','bomb','rail']):
 for col in range(4):
  cell=im.crop((col*256,bands[row],(col+1)*256,bands[row+1]))
  box=cell.getchannel('A').point(lambda x:255 if x>32 else 0).getbbox();assert box
  # All frames share scale=1. Align centerline and downward nose, preserving alpha.
  dx=round(128-(box[0]+box[2])/2);dy=300-box[3]
  assert box[1]+dy>=0 and box[3]+dy<320
  frame=Image.new('RGBA',(256,320));frame.paste(cell,(dx,dy))
  sheet.paste(frame,(col*256,row*320))
  frames.append({'role':role,'frame':col,'sourceCell':[col*256,bands[row],256,bands[row+1]-bands[row]],'translation':[dx,dy]})
sheet.save(OUT/'stage4_ordnance.png')
Path('docs/stage4_ordnance_art_0927.json').write_text(json.dumps({'generator':'Built-in image generation, no SpriteCook','source':str(raw).replace('\\','/'),'output':str(OUT/'stage4_ordnance.png').replace('\\','/'),'spec':'4 columns x6 rows, 256x320 cells, four animated south-facing frames each: steel cyan shell, brass tracer, red rocket, cyan-band precision missile, amber armored bomb, cobalt rail bolt. Genuine alpha; no background, labels, polygons or muzzle hardware. Stable metal bodies, varying flame/energy.','normalization':'Measured row gutters; shared scale1; translate each intact RGBA frame to centerline128 and nose300. No recoloring/background removal. Runtime anchor128,230.','frames':frames},indent=2)+'\n',encoding='utf-8')
print(OUT/'stage4_ordnance.png')
