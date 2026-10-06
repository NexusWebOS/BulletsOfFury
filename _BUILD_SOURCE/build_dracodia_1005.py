"""Measured native alpha cuts. Original sheets retained; no repaint or shared atlas."""
from pathlib import Path
from PIL import Image, ImageDraw
import json,hashlib
R=Path(__file__).resolve().parents[1]
if not (R/'assets/game.js').exists():R=Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury')
S=R/'_ART_SOURCES/dracodia_1005';O=R/'assets/game/dracodia_1005';O.mkdir(parents=True,exist_ok=True)
CONFIG={
 'parts':{'source':'parts-v2.png','rows':[(0,370,[0,425,717,1056,1448]),(370,708,[0,391,720,1089,1448]),(708,1086,[0,375,712,1084,1448])]},
 'portrait':{'source':'portrait.png','xs':[0,427,829,1254],'ys':[0,397,797,1210]},
 'effects':{'source':'effects-v2.png','xs':[0,365,710,1055,1427],'ys':[0,289,553,827,1102]},
 'portal':{'source':'portal-v3.png','xs':[0,362,724,1086,1448],'ys':[0,362,724,1086]},
 'charred':{'source':'charred.png','xs':[0,548,1024,1536],'ys':[0,566,1024]}
}
art={};meta={'generator':'built-in image_gen','pixelPolicy':'Measured crops and transparent padding only. Native pixels/alpha unchanged.','sources':{},'cells':{}}
for name,cfg in CONFIG.items():
 src=S/cfg['source'];im=Image.open(src);assert im.mode=='RGBA';boxes=[]
 rows=cfg.get('rows') or [(cfg['ys'][i],cfg['ys'][i+1],cfg['xs']) for i in range(len(cfg['ys'])-1)]
 for y0,y1,xs in rows:
  for x0,x1 in zip(xs,xs[1:]):boxes.append([x0,y0,x1,y1])
 cells=[]
 for n,box in enumerate(boxes):
  cell=im.crop(box)
  if name=='parts':
   bb=cell.getbbox();assert bb;cell=cell.crop(bb)
   if n>=3:
    # Same native scale, crown/foot padding and mouth root for every head.
    assert cell.width<=420 and cell.height<=380
    c=Image.new('RGBA',(420,400));c.alpha_composite(cell,((420-cell.width)//2,380-cell.height));cell=c
  elif name=='portrait':
   # Runtime holds one fixed complete bezel; source expressions are unchanged.
   pass
  else:
   # Preserve growth/shrink within each reel; do not normalize each alpha silhouette.
   common=(400,400) if name=='portal' else (400,340) if name=='effects' else (560,570)
   c=Image.new('RGBA',common);c.alpha_composite(cell,((common[0]-cell.width)//2,(common[1]-cell.height)//2));cell=c
  dst=O/(name+'_'+str(n)+'.png');cell.save(dst,optimize=True)
  cells.append({'key':'dr5_'+name+'_'+str(n),'path':dst.relative_to(R).as_posix(),'w':cell.width,'h':cell.height,'sourceBox':box})
 art[name]=cells;meta['sources'][name]={'path':src.relative_to(R).as_posix(),'size':im.size,'sha256':hashlib.sha256(src.read_bytes()).hexdigest()};meta['cells'][name]=cells
(R/'assets/dracodia_art_1005.js').write_text('"use strict";\nconst DR5_ART='+json.dumps(art,separators=(',',':'))+';\n',encoding='utf-8',newline='\n')
(S/'manifest.json').write_text(json.dumps(meta,indent=2)+'\n',encoding='utf-8',newline='\n')
# Review every cell at native aspect; this is a review artifact, not runtime art.
contact=Image.new('RGB',(1000,((sum(map(len,art.values()))+4)//5)*230),'#11121a');d=ImageDraw.Draw(contact)
i=0
for name,cells in art.items():
 for a in cells:
  q=Image.open(R/a['path']);q.thumbnail((186,204),Image.Resampling.NEAREST);x=(i%5)*200;y=(i//5)*230;contact.paste(q,(x+(200-q.width)//2,y+18),q);d.text((x+4,y+3),a['key'],fill='white');i+=1
out=R/'_shots/dracodia_1005';out.mkdir(parents=True,exist_ok=True);contact.save(out/'asset-contact.png')
print('Registered',sum(map(len,art.values())),'native alpha cells')
