from pathlib import Path
import numpy as np,json
from PIL import Image
from scipy.ndimage import label,find_objects
W=Path(__file__).parent;im=Image.open(W/'phoenix-turntable-generated.png').convert('RGBA');v=np.array(im);lab,n=label(v[:,:,3]>48);areas=np.bincount(lab.ravel());objects=find_objects(lab);major=sorted(range(1,n+1),key=lambda i:areas[i],reverse=True)[:8];boxes=[]
for i in major:
 yy,xx=objects[i-1];boxes.append((i,xx.start,yy.start,xx.stop,yy.stop,int(areas[i])))
boxes.sort(key=lambda b:(0 if (b[2]+b[4])/2<im.height/2 else 1,b[1]));print(json.dumps(boxes))
for f,(i,x0,y0,x1,y1,area)in enumerate(boxes):
 # Keep detached source sparks nearest this complete actor, never cut on a grid line.
 out=np.zeros_like(v);keep=lab==i
 for j in range(1,n+1):
  if j in major:continue
  yy,xx=objects[j-1];cx=(xx.start+xx.stop)/2;cy=(yy.start+yy.stop)/2
  dist=lambda b:max(b[1]-cx,0,cx-b[3])**2+max(b[2]-cy,0,cy-b[4])**2
  if min(boxes,key=dist)[0]==i:keep|=lab==j
 out[keep]=v[keep];bbox=Image.fromarray(out).getbbox();crop=Image.fromarray(out).crop(bbox);crop.save(W/('isolated-turn-'+str(f)+'.png'))
(W/'turn-boxes.json').write_text(json.dumps(boxes,indent=2))
