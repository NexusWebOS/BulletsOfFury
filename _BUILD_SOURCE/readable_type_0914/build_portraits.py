"""Normalize authored portraits into compact comm cells; never invent a pilot likeness."""
from pathlib import Path
import json
from PIL import Image
R=Path(__file__).resolve().parents[2];O=R/'assets/game/comm_portraits_0914';O.mkdir(exist_ok=True)
pilots=['axel','cole','decker','falva','freezer','juggernaut','lizzie','maverick','yuri']
poses=['idle','happy','laugh','anger','sad','crash','victory','talk-closed','talk-small','talk-medium','talk-wide','talk-o']
sources={}
for p in pilots:
 frame=Image.open(R/f'assets/game/pilot_avatars/pav_{p}.png').convert('RGBA').resize((64,64),Image.Resampling.NEAREST)
 # Reuse the pilot's existing authored outer frame, including its colored corner lights.
 frame.paste((0,0,0,0),(4,4,60,60))
 for pose in poses:
  if p=='yuri':
   emotion='smile'if pose=='happy'else'idle'if pose.startswith('talk')else pose
   src=R/f'assets/game/yuri_v2/port_yuri_{emotion}.png'
  else:src=R/f'assets/game/pilot_portraits/{p}-{pose}.png'
  im=Image.open(src).convert('RGBA')
  if p!='yuri':im=im.crop((16,16,im.width-16,im.height-16))
  im.thumbnail((56,56),Image.Resampling.NEAREST)
  cv=Image.new('RGBA',(64,64),(6,9,15,255));cv.alpha_composite(im,((64-im.width)//2,(64-im.height)//2));cv.alpha_composite(frame)
  key=f'comm_{p}_{pose}';cv.save(O/(key+'.png'));sources[key]={'image':f'assets/game/comm_portraits_0914/{key}.png','source':src.relative_to(R).as_posix()}
(O/'sources.json').write_text(json.dumps(sources,indent=2)+'\n')
print('Normalized',len(sources),'compact portraits from authored assets; Yuri uses v2 only.')
