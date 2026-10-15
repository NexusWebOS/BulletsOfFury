from pathlib import Path
from PIL import Image
import json,hashlib,shutil
import numpy as np
ROOT=Path(__file__).resolve().parents[1];RAW=ROOT/'_ART_SOURCES/audio_1010';DEST=ROOT/'assets/game/shared/combat/audio_1010'
GEN=Path(r'C:/Users/Mdogg/.codex/generated_images/01a0e3c8-265d-7731-8ffe-ee42ebb5ba3c');banks={}
for name,file,count,cols,rows,size in [
 ('turbo','exec-19bd48a4-3689-4200-b541-754ecb08e0a5.png',16,4,4,(336,336)),
 ('assembly','exec-4749699a-71d3-496c-bf38-450003681fd7.png',16,4,4,(352,384)),
 ('ending','exec-e50c6ca2-5be7-45ca-8418-7bd55e9f44bb.png',4,2,2,(840,472))]:
 p=RAW/(name+'_raw.png');shutil.copy2(GEN/file,p);im=Image.open(p).convert('RGBA');W,H=im.size;bank=[]
 for i in range(count):
  c,r=i%cols,i//cols;box=[round(c*W/cols),round(r*H/rows),round((c+1)*W/cols),round((r+1)*H/rows)]
  if name=='ending':
   # The generated montage divider is outside each cinematic plate.
   box=[box[0]+(3 if c else 0),box[1]+(3 if r else 0),box[2]-(3 if c==0 else 0),box[3]-(3 if r==0 else 0)]
  cell=im.crop(box);sx,sy=cell.width/2,cell.height/2;pivot=[size[0]//2,size[1]//2]
  if name=='turbo':
   # Seat the bright central laser diamond, excluding the trailing secondary
   # flash below it. Sheet-cell centers made the diamond drift as it charged.
   pixels=np.asarray(cell);yy,xx=np.nonzero((pixels[:,:,3]>180)&(pixels[:,:,0]>200)&(pixels[:,:,1]>175)&(pixels[:,:,2]>190))
   keep=(yy>cell.height*.04)&(yy<cell.height*.83)
   assert keep.any();sx=float(np.median(xx[keep]));sy=float(np.median(yy[keep]))
  if name=='assembly':
   green=[(x,y) for y in range(round(cell.height*.40),round(cell.height*.74)) for x in range(round(cell.width*.44),round(cell.width*.56))
          if (lambda p:p[3]>180 and p[1]>70 and p[1]>p[0]*1.4 and p[1]>p[2]*1.6)(cell.getpixel((x,y)))]
   assert green;sx=sum(x for x,y in green)/len(green);sy=sum(y for x,y in green)/len(green);pivot=[176,224]
  shift=[round(pivot[0]-sx),round(pivot[1]-sy)]
  out=Image.new('RGBA',size,(0,0,0,255) if name=='ending' else (0,0,0,0));out.alpha_composite(cell,tuple(shift))
  f=DEST/f'{name}_{i:02}.png';out.save(f,optimize=True)
  bank.append(dict(key=f'ap10_{name}_{i:02}',path=f.relative_to(ROOT).as_posix(),w=size[0],h=size[1],pivot=pivot,source_rect=box,source_pivot=[sx,sy],translation=shift,scale=1,sha256=hashlib.sha256(f.read_bytes()).hexdigest()))
 assert len({a['sha256'] for a in bank})==count
 banks[name]=bank;(RAW/(name+'_registration.json')).write_text(json.dumps(dict(raw_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bank=bank),indent=2),encoding='utf-8')
(ROOT/'assets/audio_extra_art_1010.js').write_text('"use strict";\nconst AP10_EXTRA_ART='+json.dumps(banks)+';\n',encoding='utf-8',newline='\n')
print(json.dumps({k:len(v) for k,v in banks.items()}))
