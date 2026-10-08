"""Import generated art as isolated, cropped RGBA modules; no synthetic artwork."""
from pathlib import Path
from PIL import Image
import numpy as np, scipy.ndimage as nd, json, shutil
R=Path(__file__).resolve().parents[1]
SRC=R/'_ART_SOURCES/realm_0930';DST=R/'assets/game/realm_0930'
SRC.mkdir(exist_ok=True,parents=True);DST.mkdir(exist_ok=True,parents=True)
FILES={'possessed':'5330d3db-f83a-4bf6-9a64-11f168e13d2a','colossus':'2856c950-8e2b-41c3-8f8e-64b68827ad95','furnace':'4ca0c3e3-db18-4d37-af47-34da0c510757','chopper':'c33e0ff2-fb0c-4c7f-8ca7-f7c73e97248b','fx':'464178c9-b1ac-412b-84bb-021a65eda0c7','walls':'cbbfa5d0-8b64-4da0-827d-aead035a7dd9'}
meta={}
def save(key,im,limit=384,grid=False):
 a=np.array(im.convert('RGBA'));a[:,:,3]=np.where(a[:,:,3]>=96,255,0).astype('uint8');im=Image.fromarray(a);box=im.getbbox();assert box,key
 if not grid:im=im.crop(box)
 scale=min(1,limit/max(im.size));im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.NEAREST)
 # Fixed transparent padding avoids loss of tip pixels at a transformed edge.
 out=Image.new('RGBA',(im.width+8,im.height+8));out.paste(im,(4,4));out.save(DST/(key+'.png'),optimize=True)
 meta[key]={'path':'assets/game/shared/combat/realm_0930/'+key+'.png','w':out.width,'h':out.height,'sourceBox':list(box)}
for name,file in FILES.items():
 src=SRC/(name+'.png');im=Image.open(src).convert('RGBA')
 if name in ('fx','walls'):
  cols,rows=(4,4) if name=='fx' else (3,2)
  cells=[im.crop((j%cols*im.width//cols,j//cols*im.height//rows,(j%cols+1)*im.width//cols,(j//cols+1)*im.height//rows)) for j in range(cols*rows)]
  if name=='walls':
   for row in range(rows):
    boxes=[]
    for cell in cells[row*cols:(row+1)*cols]:
     a=np.array(cell);a[:,:,3]=np.where(a[:,:,3]>=96,255,0).astype('uint8');boxes.append(Image.fromarray(a).getbbox())
    union=(min(b[0] for b in boxes),min(b[1] for b in boxes),max(b[2] for b in boxes),max(b[3] for b in boxes))
    for j in range(row*cols,(row+1)*cols):cells[j]=cells[j].crop(union)
  for j,cell in enumerate(cells):save(name+'_'+str(j),cell,256,True)
 elif name=='furnace':save(name,im)
 else:
  a=np.array(im);lab,n=nd.label(a[:,:,3]>=128);sizes=np.bincount(lab.ravel());sizes[0]=0
  ids=sorted(np.argsort(sizes)[-({'possessed':3,'colossus':3,'chopper':2}[name]):],key=lambda i:np.mean(np.where(lab==i)[1]))
  labels={'possessed':['possessed_armL','possessed_body','possessed_armR'],'colossus':['colossus_body','colossus_armL','colossus_armR'],'chopper':['chopper_body','chopper_rotor']}[name]
  for key,idx in zip(labels,ids):
   mask=nd.binary_dilation(lab==idx,iterations=3);out=a.copy();out[:,:,3]=np.where(mask,out[:,:,3],0);save(key,Image.fromarray(out))
(DST/'manifest.json').write_text(json.dumps(meta,indent=2))
(R/'assets/realm_art_0930.js').write_text('/* Generated authored modules; see _ART_SOURCES/realm_0930. */\nconst REALM30_ART='+json.dumps(meta,separators=(',',':'))+';\n',newline='\n')
print('Imported',len(meta),'isolated authored modules/effect cells.')
