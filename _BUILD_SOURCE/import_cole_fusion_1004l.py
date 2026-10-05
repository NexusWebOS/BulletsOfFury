from pathlib import Path
import json,hashlib,shutil
from PIL import Image
R=Path('.');a=R/'_ART_SOURCES/cole_fusion_1004l';dst=R/'assets/game/cole_fusion_1004l'
manifest={'generator':'builtin imagegen','normalization':'registration and measured source rectangles only; original RGBA bytes retained','sheets':{},'reels':{}}
for name,rows in [('weapons',['yellow','black','fusion','charge','impact','fragment','muzzle']),('cloak',['cloak'])]:
 src=a/(name+'-source.png');im=Image.open(src).convert('RGBA');cw=im.width//4;ch=im.height//len(rows)
 manifest['sheets'][name]={'key':'cf1004_'+name,'path':str(dst/(name+'.png')).replace('\\','/'),'size':list(im.size),'sha256':hashlib.sha256(src.read_bytes()).hexdigest()}
 for row,label in enumerate(rows):
  bounds=[]
  for col in range(4):
   cell=im.crop((col*cw,row*ch,(col+1)*cw,(row+1)*ch));bounds.append(cell.getchannel('A').point(lambda x:255 if x>80 else 0).getbbox())
  x0=min(b[0] for b in bounds);y0=min(b[1] for b in bounds);x1=max(b[2] for b in bounds);y1=max(b[3] for b in bounds)
  manifest['reels'][label]={'sheet':name,'fps':24 if label=='fusion' else 18,'frames':[[col*cw+x0,row*ch+y0,x1-x0,y1-y0] for col in range(4)]}
 dst.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst/(name+'.png'))
for d in [a,dst]:(d/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
(R/'assets/cole_fusion_art_1004l.js').write_text("'use strict';\nconst CF1004_ART="+json.dumps(manifest,separators=(',',':'))+';\n',encoding='utf-8',newline='\n')
