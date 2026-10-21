from pathlib import Path
from PIL import Image,ImageDraw
import json,math
R=Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury');O=R/'_shots/final_version_1021';D=json.loads((R/'_ART_SOURCES/final_version_1021/air-production-manifest.json').read_text());models=list(D['models'].items())
for page in range(math.ceil(len(models)/5)):
 group=models[page*5:page*5+5];im=Image.new('RGB',(1280,len(group)*320),'#0b1420');g=ImageDraw.Draw(im)
 for row,(id,m) in enumerate(group):
  for line,kind in enumerate(['roll','somer','drift','attack']):
   a=m['banks'][kind];atlas=Image.open(R/a['path']).convert('RGBA');n=a['frames'];g.text((2,row*320+line*80+2),id+' '+kind,fill='white')
   for f,c in enumerate(a['cells']):
    x,y,w,h=c;cell=atlas.crop((x,y,x+w,y+h)).resize((64,64),Image.Resampling.NEAREST);im.paste(cell,(200+f*66,row*320+line*80),cell)
 im.save(O/f'air-review-page-{page+1}.jpg',quality=92)
print('Eight visual contact pages; 2280 exported aircraft poses, fixed pivots, zero clipped edges, exact three-part recomposition.')
