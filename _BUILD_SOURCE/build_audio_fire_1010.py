from pathlib import Path
from PIL import Image
import json,hashlib,shutil
ROOT=Path(__file__).resolve().parents[1];RAW=ROOT/'_ART_SOURCES/audio_1010';DEST=ROOT/'assets/game/shared/combat/audio_1010'
GEN=Path(r'C:/Users/Mdogg/.codex/generated_images/01a0e3c8-265d-7731-8ffe-ee42ebb5ba3c')
banks={}
for name,file,count,rows,size in [('fire_shield','exec-75eda60b-d21b-489d-be8d-0b2b207db278.png',32,4,(256,256)),('chain','exec-83c57f7d-6210-411b-ab6c-38731ddb6ce7.png',16,2,(256,400))]:
 p=RAW/(name+'_raw.png');shutil.copy2(GEN/file,p)
 im=Image.open(p).convert('RGBA');W,H=im.size;bank=[]
 for i in range(count):
  c,r=i%8,i//8;box=[round(c*W/8),round(r*H/rows),round((c+1)*W/8),round((r+1)*H/rows)]
  cell=im.crop(box);ink=cell.getchannel('A').point(lambda a:255 if a>=96 else 0).getbbox()
  sx,sy=(ink[0]+ink[2])/2,(ink[1]+ink[3])/2
  pivot=[size[0]//2,size[1]//2];shift=[round(pivot[0]-sx),round(pivot[1]-sy)]
  out=Image.new('RGBA',size);out.alpha_composite(cell,tuple(shift));f=DEST/f'{name}_{i:02}.png';out.save(f,optimize=True)
  bank.append(dict(key=f'ap10_{name}_{i:02}',path=f.relative_to(ROOT).as_posix(),w=size[0],h=size[1],pivot=pivot,ink=ink,source_rect=box,source_pivot=[sx,sy],translation=shift,scale=1,sha256=hashlib.sha256(f.read_bytes()).hexdigest()))
 assert len({a['sha256'] for a in bank})==count
 banks[name]=bank;(RAW/(name+'_registration.json')).write_text(json.dumps(dict(raw_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bank=bank),indent=2),encoding='utf-8')
(ROOT/'assets/audio_fire_art_1010.js').write_text('"use strict";\nconst AP10_FIRE_ART='+json.dumps(banks)+';\n',encoding='utf-8',newline='\n')
print(json.dumps({k:len(v) for k,v in banks.items()}))
