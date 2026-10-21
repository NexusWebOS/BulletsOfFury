"""Whole connected anatomical modules; no partitioning moving whole-body clips."""
from pathlib import Path
from PIL import Image,ImageDraw
from collections import deque
import numpy as np,json
R=Path(__file__).resolve().parents[1];S=R/'_ART_SOURCES/boss_redesign_1020';D=R/'assets/game/levels/stage_08/boss/phoenix_swoon_1020';O=R/'_shots/boss_redesign_1020';D.mkdir(parents=True,exist_ok=True);O.mkdir(parents=True,exist_ok=True)
im=Image.open(R/'_ART_SOURCES/dracodia_phoenix_1020/master.png').convert('RGBA');raw=np.array(im);claimed=np.zeros((256,256),bool);pieces={}
def region(poly):
 m=Image.new('1',(256,256));ImageDraw.Draw(m).polygon(poly,fill=1);return np.asarray(m).astype(bool)
def connected(arr):
 mask=arr[:,:,3]>16;seen=np.zeros(mask.shape,bool);components=[]
 for y,x in zip(*np.where(mask)):
  if seen[y,x]:continue
  todo=[(y,x)];seen[y,x]=True;group=[]
  while todo:
   cy,cx=todo.pop();group.append((cy,cx))
   for dy in [-1,0,1]:
    for dx in [-1,0,1]:
     ny,nx=cy+dy,cx+dx
     if 0<=ny<256 and 0<=nx<256 and mask[ny,nx] and not seen[ny,nx]:seen[ny,nx]=True;todo.append((ny,nx))
  components.append(group)
 if not components:return arr,0
 keep=max(components,key=len);out=np.zeros_like(arr)
 for y,x in keep:out[y,x]=arr[y,x]
 return out,len(components)
def cut(name,mask):
 global claimed
 selected=mask&~claimed;claimed|=selected;arr=np.zeros_like(raw);arr[selected]=raw[selected];arr,count=connected(arr);pieces[name]=(arr,count)
cut('head',region([(109,51),(148,51),(148,100),(109,100)]))
left=region([(1,1),(104,1),(104,77),(111,85),(110,112),(94,118),(1,118)])
cut('wingL',left);cut('wingR',np.fliplr(left))
leg=region([(100,146),(124,146),(124,172),(118,200),(82,200),(82,169)])
cut('clawL',leg);cut('clawR',np.fliplr(leg));cut('tail',region([(118,168),(138,168),(141,249),(115,249)]))
body=np.zeros_like(raw);body[~claimed]=raw[~claimed]
# Original authored collar material underlaps each whole hinge; these are
# intentional identical-pixel overlaps, not invented replacement surfaces.
for box in [(91,91,112,115),(144,91,165,115),(108,144,123,156),(133,144,148,156),(119,93,138,103)]:
 x0,y0,x1,y1=box;body[y0:y1,x0:x1]=raw[y0:y1,x0:x1]
body,count=connected(body);pieces['core']=(body,count)
anchors={'head':[128,94],'wingL':[103,99],'wingR':[153,99],'clawL':[113,152],'clawR':[143,152],'tail':[128,178],'core':[128,128]}
art={'parts':{},'source':'a3ed4f8a-edd3-49c0-8ba3-479f887a287f','version':2};sheet=Image.new('RGB',(1280,700),'#10131d');draw=ImageDraw.Draw(sheet);audit=[]
for i,(name,(arr,removed)) in enumerate(pieces.items()):
 c=Image.new('RGBA',(320,320));c.alpha_composite(Image.fromarray(arr),(32,32));assert c.getbbox(),name;p=D/(name+'.png');c.save(p,optimize=True)
 art['parts'][name]=dict(key='ph21_'+name,path=p.relative_to(R).as_posix(),w=320,h=320,pivot=[160,160],anchor=[v+32 for v in anchors[name]],bounds=list(c.getbbox()))
 at=(i%4*320,i//4*350);sheet.paste(c,at,c);draw.text((at[0]+8,at[1]+322),name+' / ONE connected anatomy',fill='white');audit.append(dict(module=name,sourceComponents=removed,exportedComponents=1))
if (S/'phoenix-cannon.png').exists():
 c=Image.open(S/'phoenix-cannon.png').convert('RGBA');assert c.size==(128,128);p=D/'cannon_attachment.png';c.save(p,optimize=True);art['cannon']=dict(key='ph21_cannon',path=p.relative_to(R).as_posix(),w=128,h=128,pivot=[64,36],anchor=[64,36],bounds=list(c.getbbox()))
if (S/'corner-warning.png').exists():
 c=Image.open(S/'corner-warning.png').convert('RGBA');assert c.size==(64,64);p=D/'corner_warning_v3.png';c.save(p,optimize=True);art['warning']=dict(key='ph21_corner_warning',path=p.relative_to(R).as_posix(),w=64,h=64,pivot=[32,32],bounds=list(c.getbbox()))
sheet.save(O/'phoenix-whole-modules.png');(D/'manifest.json').write_text(json.dumps(art,indent=2)+'\n');(S/'phoenix-module-audit.json').write_text(json.dumps(audit,indent=2)+'\n');(R/'assets/phoenix_swoon_art_1020.js').write_text('"use strict";\n// Owned by build_phoenix_swoon_1020.py. Whole connected authored anatomy.\nconst PH21_ART='+json.dumps(art,separators=(',',':'))+';\n',encoding='utf-8',newline='\n');print(json.dumps({'modules':len(pieces),'allConnected':True,'cannon':bool(art.get('cannon'))}))
