from pathlib import Path
from PIL import Image
from scipy import ndimage
import numpy as np,json
W=Path(__file__).resolve().parent;E=W/'exports';M=json.loads((W/'manifest.json').read_text());im=Image.open(W/'generated/energy-ball.png').convert('RGBA');order=list(range(12))+[10,11,10,9];audit=[]
for name,cell,size in [('ball',128,84),('ball_back',96,60)]:
 d=E/name;d.mkdir(exist_ok=True);sheet=Image.new('RGBA',(cell*4,cell*4))
 for i,source in enumerate(order):
  cx=round((source%4+.5)*im.width/4);cy=round((source//4+.5)*im.height/4);crop=im.crop((cx-120,cy-120,cx+120,cy+120));a=np.array(crop);lab,n=ndimage.label(a[:,:,3]>=32,np.ones((3,3)));sizes=np.bincount(lab.ravel());sizes[0]=0;mask=lab==sizes.argmax();a[~mask]=0
  f=Image.new('RGBA',(cell,cell));f.paste(Image.fromarray(a).resize((size,size),Image.Resampling.NEAREST),((cell-size)//2,(cell-size)//2));f.save(d/f'{i:02}.png');sheet.paste(f,(i%4*cell,i//4*cell))
  audit.append(dict(bank=name,frame=i,source=source,masterCrop=[cx-120,cy-120,cx+120,cy+120],targetFromMaster=size))
 sheet.save(E/(name+'.webp'),lossless=True,method=1);M[name]=dict(cw=cell,ch=cell,cols=4,count=16,pivot=[cell//2,cell//2],meta=[])
# New actor/effect banks cannot contain an opaque background rectangle.
for name,a in M.items():
 if a['meta']:continue
 p=E/(name+'.webp');img=np.array(Image.open(p).convert('RGBA'))
 assert img[0,0,3]==0,(name,'opaque corner')
 assert (img[:,:,3]==0).mean()>.30,(name,'opaque effect background')
(W/'manifest.json').write_text(json.dumps(M,separators=(',',':')));(W/'draconus_cinematic_rage_art_1113.js').write_text("'use strict';\nconst DCR13_ART="+json.dumps(M,separators=(',',':'))+';\n')
(W/'ball-export-audit.json').write_text(json.dumps(dict(sourceImageSize=im.size,rejectedClippedSourceFrames=[12,13,14,15],frames=audit,transparentEffectBackgrounds=True),indent=2))
print('Prepared genuinely round growing energy ball, direct master depth exports and transparent effect checks.')
