from pathlib import Path
from PIL import Image
import json, shutil, hashlib

R=Path(__file__).resolve().parents[1]
if R.name=='New project': R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury')
S=R/'_ART_SOURCES/finale_motion_1006'; O=R/'assets/game/finale_motion_1006'
S.mkdir(parents=True,exist_ok=True);O.mkdir(parents=True,exist_ok=True)
source=S/'hammer-motion.png'
if not source.exists(): shutil.copy2(Path(r'C:/Users/Mike/.codex/generated_images/01a0c9fd-a6cc-73a3-8dca-3e0f7a90a956/exec-c228eff5-1b25-4a54-b546-a26f15c03034.png'),source)
im=Image.open(source).convert('RGBA')
# Measured native connected bodies; cells follow the authored sheet, not a guessed grid.
boxes=[(101,40,288,246),(481,47,666,246),(841,66,1038,258),(1195,35,1479,256),
 (73,267,314,537),(476,257,674,521),(804,336,1071,543),(1180,327,1465,541),
 (61,546,393,769),(458,543,734,772),(841,546,1123,772),(1193,544,1461,770),
 (71,799,318,996),(448,775,696,995),(821,791,1118,993),(1170,787,1478,995)]
cores=[(201,153),(579,151),(943,178),(1310,137),(200,424),(602,414),(944,434),(1316,411),
 (196,651),(571,650),(955,657),(1315,643),(216,908),(575,867),(967,900),(1310,876)]
heads=[(218,148),(605,150),None,(1435,222),(222,303),(532,299),(940,507),(1415,493),
 (354,637),(691,715),(1080,699),(1416,665),None,None,None,None]
names=['curlStart','curlMid','ball','uncurl','giantLift','giantDive','giantImpact','giantRecover',
 'whirlFront','whirlRight','whirlBack','whirlLeft','kneel','stun','rise','emptyThrow']
art=[];cells=[]
for i,(box,core,head,name) in enumerate(zip(boxes,cores,heads,names)):
 x,y,ex,ey=box;rect=(max(0,x-3),max(0,y-3),min(im.width,ex+3),min(im.height,ey+3))
 cell=im.crop(rect);pad=12
 out=Image.new('RGBA',(cell.width+pad*2,cell.height+pad*2));out.alpha_composite(cell,(pad,pad))
 path=O/f'hammer_motion_{i}.png';out.save(path,optimize=True)
 a={'key':f'f6_hammer_motion_{i}','path':f'assets/game/finale_motion_1006/hammer_motion_{i}.png',
  'w':out.width,'h':out.height,'px':(core[0]-rect[0]+pad)/out.width,'py':(core[1]-rect[1]+pad)/out.height,'name':name,
  'head':None if head is None else [head[0]-rect[0]+pad,head[1]-rect[1]+pad]}
 art.append(a);cells.append({**a,'sourceRect':rect,'alphaBounds':out.getbbox(),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
(R/'assets/finale_motion_art_1006.js').write_text('"use strict";\nconst F6_MOTION='+json.dumps(art,separators=(',',':'))+';\n',encoding='utf-8')
(S/'manifest.json').write_text(json.dumps({'tool':'built-in image_gen','source':'hammer-motion.png','reference':'../hammer_knight_1005/hammer.png','processing':'Measured native extraction and transparent padding only. No repaint, palette change, resizing or atlas reallocation.','cells':cells},indent=2),encoding='utf-8')
print('Extracted 16 native motion cells; alpha and original colors preserved')
