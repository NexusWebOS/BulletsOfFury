"""Fixed-camera cinematic plates and registered 32-frame void animation."""
from pathlib import Path
from PIL import Image
import hashlib,json,shutil
ROOT=Path(__file__).resolve().parents[1]
RAW=ROOT/'_ART_SOURCES/audio_1010'
DEST=ROOT/'assets/game/shared/combat/audio_1010'
GEN=Path(r'C:/Users/Mdogg/.codex/generated_images/01a0e3c8-265d-7731-8ffe-ee42ebb5ba3c')
RAW.mkdir(parents=True,exist_ok=True);DEST.mkdir(parents=True,exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def archive(name,file):
 p=RAW/(name+'_raw.png')
 if not p.exists():shutil.copy2(GEN/file,p)
 return p,Image.open(p).convert('RGBA')
banks={}
p,im=archive('hq_story','exec-4e0a62e9-7390-4f92-abf6-9b74daf8dc06.png')
bank=[];xs=[0,836,1672];ys=[0,471,941]
for i in range(4):
 c,r=i%2,i//2;box=[xs[c],ys[r],xs[c+1],ys[r+1]]
 cell=im.crop(box);out=Image.new('RGBA',(840,472),(0,0,0,255));out.alpha_composite(cell,(2,0))
 f=DEST/f'hq_story_{i}.png';out.save(f,optimize=True)
 bank.append(dict(key=f'ap10_hq_story_{i}',path=f.relative_to(ROOT).as_posix(),w=840,h=472,pivot=[420,236],source_rect=box,translation=[2,0],scale=1,sha256=sha(f)))
banks['hq_story']=bank
(RAW/'hq_story_registration.json').write_text(json.dumps(dict(raw_sha256=sha(p),bank=bank),indent=2),encoding='utf-8')
p,im=archive('void','exec-5d361b88-9952-4f73-8c5f-b0a4547300a6.png')
bank=[];W,H=im.size
for i in range(32):
 c,r=i%8,i//8;box=[round(c*W/8),round(r*H/4),round((c+1)*W/8),round((r+1)*H/4)]
 cell=im.crop(box)
 # Center the effect's physical opening without changing scale or drawing pixels.
 bbox=cell.getchannel('A').point(lambda a:255 if a>=64 else 0).getbbox()
 sx,sy=(bbox[0]+bbox[2])/2,(bbox[1]+bbox[3])/2
 shift=[round(128-sx),round(128-sy)]
 out=Image.new('RGBA',(256,256));out.alpha_composite(cell,tuple(shift))
 f=DEST/f'void_{i:02}.png';out.save(f,optimize=True)
 bank.append(dict(key=f'ap10_void_{i:02}',path=f.relative_to(ROOT).as_posix(),w=256,h=256,pivot=[128,128],source_rect=box,source_pivot=[sx,sy],translation=shift,scale=1,sha256=sha(f)))
assert len({a['sha256'] for a in bank})==32
banks['void']=bank
(RAW/'void_registration.json').write_text(json.dumps(dict(raw_sha256=sha(p),bank=bank),indent=2),encoding='utf-8')
p,im=archive('consumption','exec-be7c1f5d-822a-42d7-9849-5bc959c6bc55.png')
bank=[];W,H=im.size
for i in range(16):
 c,r=i%4,i//4;box=[round(c*W/4),round(r*H/4),round((c+1)*W/4),round((r+1)*H/4)]
 cell=im.crop(box)
 # The green optical core is the fixed physical anchor throughout consumption.
 green=[(x,y) for y in range(cell.height) for x in range(cell.width)
        if (lambda p:p[3]>128 and p[1]>100 and p[1]>p[0]*1.8 and p[1]>p[2]*1.35)(cell.getpixel((x,y)))]
 assert green, 'Optical core must stay visible in every mutation frame'
 sx=(min(x for x,y in green)+max(x for x,y in green))/2
 sy=(min(y for x,y in green)+max(y for x,y in green))/2
 shift=[round(192-sx),round(236-sy)]
 out=Image.new('RGBA',(384,384));out.alpha_composite(cell,tuple(shift))
 f=DEST/f'consumption_{i:02}.png';out.save(f,optimize=True)
 bank.append(dict(key=f'ap10_consumption_{i:02}',path=f.relative_to(ROOT).as_posix(),w=384,h=384,pivot=[192,236],source_rect=box,source_pivot=[sx,sy],translation=shift,scale=1,sha256=sha(f)))
assert len({a['sha256'] for a in bank})==16
banks['consumption']=bank
(RAW/'consumption_registration.json').write_text(json.dumps(dict(raw_sha256=sha(p),bank=bank),indent=2),encoding='utf-8')
(ROOT/'assets/audio_cinematic_art_1010.js').write_text('"use strict";\nconst AP10_CIN_ART='+json.dumps(banks)+';\n',encoding='utf-8',newline='\n')
print(json.dumps({k:len(v) for k,v in banks.items()}))
