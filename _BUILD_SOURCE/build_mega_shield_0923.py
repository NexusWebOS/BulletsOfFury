from pathlib import Path
from PIL import Image
import json,hashlib
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'assets/game/axel_mega_shield_0923'
im=Image.open(OUT/'source.png').convert('RGBA');frames=[]
for i in range(8):
 x,y=i%4*512,i//4*576;cell=im.crop((x,y,x+512,y+576))
 # One scale for the whole reel. Use the solid bubble boundary, excluding faint outer sparks.
 bb=cell.getchannel('A').point(lambda a:255 if a>180 else 0).getbbox();assert bb
 cx,cy=(bb[0]+bb[2])/2,(bb[1]+bb[3])/2
 frame=Image.new('RGBA',(256,256));frame.alpha_composite(cell.resize((230,259),Image.Resampling.NEAREST),(round(128-cx*.45),round(128-cy*.45)))
 name=f'shield_{i}.png';frame.save(OUT/name);frames.append({'file':name,'anchor':[128,128],'sha12':hashlib.sha256((OUT/name).read_bytes()).hexdigest()[:12]})
(OUT/'frames.json').write_bytes((json.dumps({'size':[256,256],'scale':.45,'frames':frames},indent=2)+'\n').encode())
print('Eight normalized shield frames.')
