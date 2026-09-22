"""Package the generated 4x2 burn reel; preserve generated alpha and shared anchors."""
import json, shutil, sys
from pathlib import Path
from PIL import Image

root=Path(__file__).resolve().parents[1]
out=root/'assets/game/fx_burn_0922'
out.mkdir(exist_ok=True)
source=Path(sys.argv[1]) if len(sys.argv)>1 else out/'source.png'
if source.resolve()!=(out/'source.png').resolve(): shutil.copyfile(source,out/'source.png')
im=Image.open(out/'source.png').convert('RGBA')
w,h=im.size
assert abs(w/h-2)<.1
assert im.getchannel('A').getextrema()==(0,255),'Generated transparency required'
cells=[]
for i in range(8):
 x,y=round((i%4)*w/4),round((i//4)*h/2)
 right,bottom=round((i%4+1)*w/4),round((i//4+1)*h/2)
 cell=im.crop((x,y,right,bottom))
 assert cell.getbbox(),'Empty frame'
 cell.resize((128,128),Image.Resampling.NEAREST).save(out/f'burn_{i}.png')
 cells.append([x,y,right-x,bottom-y])
print(json.dumps({'source':im.size,'cells':cells,'alpha':im.getchannel('A').getextrema()}))
