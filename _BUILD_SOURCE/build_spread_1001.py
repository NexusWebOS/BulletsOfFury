"""Import generated Spreadfire frames. Preserve alpha and pixels; measure every row."""
from pathlib import Path
from PIL import Image
import shutil,json,hashlib
R=Path(__file__).resolve().parents[1]
src=R/'_ART_SOURCES/encounters_1001/spread.png'
out=R/'assets/game/encounters_1001';out.mkdir(parents=True,exist_ok=True)
im=Image.open(src).convert('RGBA')
# Measured transparent gutters, not an assumed uniform generator grid.
bounds=[0,176,356,532,700,879,1089,1315,1513,1718,1983]
names=['base','fire','ice','lightning','kinetic','chrome','dark','toxic','prism','water']
data={}
for row,name in enumerate(names):
 frames=[];regions=[]
 for col in range(4):
  x=round(col*im.width/4);end=round((col+1)*im.width/4)
  cell=im.crop((x,bounds[row],end,bounds[row+1]));regions.append(cell)
 boxes=[cell.getchannel('A').getbbox() for cell in regions]
 l=min(b[0] for b in boxes);t=min(b[1] for b in boxes);rr=max(b[2] for b in boxes);bb=max(b[3] for b in boxes)
 w,h=rr-l+8,bb-t+8;sheet=Image.new('RGBA',(w*4,h))
 for col,cell in enumerate(regions):
  crop=cell.crop((l,t,rr,bb));sheet.paste(crop,(col*w+4,4))
  frames.append([col*w,0,w,h])
 path=out/(name+'.png');sheet.save(path)
 data[name]={'key':'spread1001_'+name,'path':path.relative_to(R).as_posix(),'frames':frames,'fps':16,'size':[w,h]}
(R/'assets/spread_art_1001.js').write_text('"use strict";\nconst SPREAD1001_ART='+json.dumps(data,separators=(',',':'))+';\n',encoding='utf-8')
(out/'manifest.json').write_text(json.dumps({'source':src.relative_to(R).as_posix(),'rows':bounds,'art':data,'sha256':hashlib.sha256(src.read_bytes()).hexdigest()},indent=2)+'\n')
print('Imported 10 Spreadfire reels, 40 distinct generated frames.')
