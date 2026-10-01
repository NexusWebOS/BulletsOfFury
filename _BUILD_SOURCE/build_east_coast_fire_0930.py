"""Extract the eight generated poses. No procedural flames or texture scrolling."""
from pathlib import Path
import json, hashlib
from PIL import Image

R=Path(__file__).resolve().parents[1]
S=R/'_ART_SOURCES/campaign_0930'
O=R/'assets/game/campaign_0930'
source=Image.open(S/'east_coast_flames_v3.png').convert('RGB')
# Measured 4-column, 2-row sheet, no gutters. Original is 1254 square.
assert source.size==(1254,1254), source.size
xs=[0,314,627,940,1254];ys=[0,627,1254]
sheet=Image.new('RGB',(1024,1024))
cells=[]
for i in range(8):
 col,row=i%4,i//4
 box=(xs[col],ys[row],xs[col+1],ys[row+1])
 frame=source.crop(box).resize((256,512),Image.Resampling.NEAREST)
 sheet.paste(frame,(col*256,row*512))
 cells.append({'index':i,'source_box':box,'rect':[col*256,row*512,256,512],
  'sha256':hashlib.sha256(frame.tobytes()).hexdigest()})
assert len({c['sha256'] for c in cells})==8
sheet.save(O/'east_coast_flames_v3.png',optimize=True)
(O/'east_coast_flames_v3.json').write_text(json.dumps({
 'image':'east_coast_flames_v3.png','columns':4,'rows':2,'fps':12,
 'frame_width':256,'frame_height':512,'count':8,'direction':'left',
 'motion':'authored frames; fixed destination; no texture offsets',
 'opaque':True,'frames':cells},indent=2)+'\n',encoding='utf-8')
print('Built eight distinct opaque frames, 256x512, 4x2 sheet.')
