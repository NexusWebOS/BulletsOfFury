"""Measure/crop generated RGBA poses and normalize them for the map effect."""
from pathlib import Path
import json,hashlib
from PIL import Image
R=Path(__file__).resolve().parents[1];S=R/'_ART_SOURCES/campaign_0930';O=R/'assets/game/campaign_0930'
source=Image.open(S/'east_coast_front_v4.png').convert('RGBA')
assert source.size==(887,1774),source.size
xs=[0,222,444,665,887];ys=[0,887,1774]
# The generated tall panels are normalized to broad map-weather poses.
# Keep all pixels and genuine alpha; no synthetic flames, recoloring or keying.
sheet=Image.new('RGBA',(1024,1024));cells=[]
for i in range(8):
 # Trim 3 right-edge pixels: the generated next panel's opaque left edge
 # intrudes into fractional grid boundaries. Never include that vertical seam.
 col,row=i%4,i//4;box=(xs[col],ys[row],xs[col+1]-3,ys[row+1])
 frame=source.crop(box).resize((256,512),Image.Resampling.NEAREST)
 lo,hi=frame.getchannel('A').getextrema()
 assert lo==0 and hi>=250,(i,lo,hi)
 sheet.paste(frame,(col*256,row*512))
 cells.append({'index':i,'source_box':box,'rect':[col*256,row*512,256,512],
  'sha256':hashlib.sha256(frame.tobytes()).hexdigest()})
assert len({q['sha256'] for q in cells})==8
sheet.save(O/'east_coast_front_v4.png',optimize=True)
(O/'east_coast_front_v4.json').write_text(json.dumps({'image':'east_coast_front_v4.png','columns':4,'rows':2,'fps':6,'frame_width':256,'frame_height':512,'count':8,'direction':'left','transparent_edge':True,'motion':'fixed-position authored flame and smoke poses','frames':cells},indent=2)+'\n',encoding='utf-8')
print('Built eight RGBA map-front frames; original transparency preserved.')
