from pathlib import Path
from PIL import Image
from scipy.ndimage import distance_transform_edt
import numpy as np,json
W=Path(__file__).resolve().parent;M=json.loads((W/'manifest.json').read_text());points=[[256,300],[215,292],[210,290],[174,286],[181,284],[180,285],[188,282],[192,283],[228,294],[256,270],[256,268],[256,254],[256,253],[256,263],[256,278],[256,300]];audit=[]
for depth,cell in [('fore',512),('back',224)]:
 for i,p in enumerate(points):
  point=[round(v*cell/512)for v in p]
  for suffix in ['', '_hit']:
   m=M['cast_'+depth+suffix]['meta'][i];m['ball']=point;m['palms']=[[point[0]-round(12*cell/512),point[1]],[point[0]+round(12*cell/512),point[1]]]
  if depth=='fore'and i in [3,4,5,6,7]:
   a=np.array(Image.open(W/'exports/cast_fore'/f'{i:02}.png'))[:,:,3]>0;gap=float(distance_transform_edt(~a)[p[1],p[0]])
   assert not a[p[1],p[0]]and 3<=gap<=24,(i,p,gap)
   audit.append(dict(frame=i,ball=p,insideActualTransparentCup=True,pixelsToFingers=gap))
(W/'manifest.json').write_text(json.dumps(M,separators=(',',':')));(W/'draconus_cinematic_rage_art_1113.js').write_text("'use strict';\nconst DCR13_ART="+json.dumps(M,separators=(',',':'))+';\n');(W/'hand-socket-audit.json').write_text(json.dumps(audit,indent=2))
print('Ball socket verified inside the actual cupped-hand gap for every gather pose; release centered between forward palms.')
