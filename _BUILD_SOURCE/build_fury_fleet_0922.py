"""Normalize generated Fury fleet frames. Real alpha; component-aware extraction avoids grid-edge clipping."""
from pathlib import Path
from PIL import Image
from scipy.ndimage import label,find_objects
import numpy as np,json,shutil
ROOT=Path(__file__).resolve().parents[1]
SRC=Path(r'C:\Users\Mike\.codex\generated_images\01a0c9fd-a6cc-73a3-8dca-3e0f7a90a956')
OUT=ROOT/'assets/game/fury_fleet_0922'
OUT.mkdir(parents=True,exist_ok=True)
FILES={
'bank':('02ad67c0-0175-41ae-aa44-db89d8bbe322',3,4),
'boats':('4cc0ca46-b816-418d-90ca-a0cbe1c9511b',3,2),
'roll':('3b1babb9-6a7d-4973-b9ae-ab484fa07242',4,8),
'pitch':('d22c80b7-3da7-400e-b5f1-f1b84fb16893',4,8),
'turn':('96186f1e-2f9a-4ece-a994-9f40b18a88c7',4,8),
'interceptor':('11e4e611-3816-4c63-bd5f-265699c74ef8',4,8),
'bomber':('b586e009-bcc2-46d3-bb2b-710720c37a86',4,8),
'northturn':('3b638029-844f-441c-b346-58833490d93f',4,2)}
sheets={}
manifest={'cell':[128,128],'anchor':[64,64],'mode':'built-in image_gen','frames':{}}
for kind,(uid,rows,cols) in FILES.items():
 dest=OUT/(kind+'_source.png')
 if not dest.exists():shutil.copy2(SRC/('exec-'+uid+'.png'),dest)
 im=Image.open(dest).convert('RGBA')
 labs,_=label(np.array(im)[:,:,3]>64)
 boxes=[]
 for sl in find_objects(labs):
  if sl is not None and (sl[0].stop-sl[0].start)*(sl[1].stop-sl[1].start)>1400:
   boxes.append((sl[1].start,sl[0].start,sl[1].stop,sl[0].stop))
 assert len(boxes)==rows*cols,(kind,len(boxes))
 boxes.sort(key=lambda b:(b[1]+b[3])/2)
 grid=[sorted(boxes[r*cols:(r+1)*cols],key=lambda b:(b[0]+b[2])/2) for r in range(rows)]
 sheets[kind]=(im,grid)
def save(name,kind,row,col,scale):
 im,grid=sheets[kind];b=grid[row][col]
 # Two pixels retain antialiased outer edges without borrowing adjacent hulls.
 b=(max(0,b[0]-2),max(0,b[1]-2),min(im.width,b[2]+2),min(im.height,b[3]+2))
 frame=im.crop(b);frame=frame.resize((max(1,round(frame.width*scale)),max(1,round(frame.height*scale))),Image.Resampling.NEAREST)
 assert max(frame.size)<=124,(name,frame.size)
 canvas=Image.new('RGBA',(128,128));canvas.alpha_composite(frame,((128-frame.width)//2,(128-frame.height)//2))
 canvas.save(OUT/(name+'.png'),optimize=True)
 manifest['frames'][name]={'source':kind+'_source.png','box':b,'scale':round(scale,5)}
def scale_for(kind,cells):
 boxes=[sheets[kind][1][r][c] for r,c in cells]
 return 116/max(max(b[2]-b[0]+4,b[3]-b[1]+4) for b in boxes)
for v in range(4):
 sc=scale_for('bank',[(r,v) for r in range(3)])
 for f in range(3):save(f'jet_{v}_bank_{f}','bank',f,v,sc)
 for pose in ['roll','pitch','turn']:
  kind=pose;row=v
  if v in (0,2) and pose!='turn':
   kind='interceptor';row=(0 if v==0 else 2)+(pose=='pitch')
  elif v in (1,3) and pose!='turn':
   kind='bomber';row=(0 if v==1 else 2)+(pose=='pitch')
  sc=scale_for(kind,[(row,c) for c in range(8)])
  for f in range(8):save(f'jet_{v}_{pose}_{f}',kind,row,f,sc)
# Correct northward diagonals, authored separately rather than mirroring south poses.
for v in range(4):
 sc=scale_for('northturn',[(v,c) for c in range(2)])
 for f,c in [(3,0),(5,1)]:save(f'jet_{v}_turn_{f}','northturn',v,c,sc)
for v in range(2):
 sc=scale_for('boats',[(r,v) for r in range(3)])
 for f in range(3):save(f'boat_{v}_{f}','boats',f,v,sc)
(OUT/'manifest.json').write_text(json.dumps(manifest,indent=2))
print('Saved',len(manifest['frames']),'RGBA frames to',OUT)
