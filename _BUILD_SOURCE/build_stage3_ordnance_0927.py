"""Normalize generated Stage3 RGBA frames; no recoloring or background removal."""
from pathlib import Path
from PIL import Image
import json,shutil
OUT=Path('assets/game/projectiles_0927');OUT.mkdir(parents=True,exist_ok=True)
raw=OUT/'stage3_ordnance_source.png'
if not raw.exists():shutil.copyfile(r'C:\Users\Mdogg\.codex\generated_images\01a0d568-40a4-7b70-97c0-acc501f39d5b\exec-e788d324-4de6-4e53-ad83-96504ac9869b.png',raw)
im=Image.open(raw).convert('RGBA');assert im.size==(1024,1536)
alpha=im.getchannel('A').histogram();assert sum(alpha[:5])/sum(alpha)>.65
sheet=Image.new('RGBA',(1024,1920));frames=[];bands=[0,246,510,758,1000,1280,1536]
for row,role in enumerate(['shard','lance','tracer','mortar','shell','wave']):
 for col in range(4):
  cell=im.crop((col*256,bands[row],(col+1)*256,bands[row+1]));box=cell.getchannel('A').point(lambda x:255 if x>32 else 0).getbbox();assert box
  dx=round(128-(box[0]+box[2])/2);dy=300-box[3]
  assert box[1]+dy>=0 and box[3]+dy<320
  frame=Image.new('RGBA',(256,320));frame.paste(cell,(dx,dy));sheet.paste(frame,(col*256,row*320))
  frames.append({'role':role,'frame':col,'sourceCell':[col*256,bands[row],256,bands[row+1]-bands[row]],'translation':[dx,dy]})
sheet.save(OUT/'stage3_ordnance.png')
Path('docs/stage3_ordnance_art_0927.json').write_text(json.dumps({'generator':'Built-in image generation; no SpriteCook','source':raw.as_posix(),'output':(OUT/'stage3_ordnance.png').as_posix(),'spec':'Six ice ordnance families, four frames each: shard, lance, tracer, mortar, shell, crescent wave. South-facing cyan/white/violet with dark outlines, genuine alpha. Stable bodies with animated energy.','normalization':'Measured row gutters, shared scale1, bottom-center nose at128,300 in256x320 cell. Runtime center128,230; no recoloring, alpha removal or repainting.','frames':frames},indent=2)+'\n',encoding='utf-8')
print('transparent fraction',sum(alpha[:5])/sum(alpha))
