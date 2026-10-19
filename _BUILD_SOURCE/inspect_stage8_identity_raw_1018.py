from pathlib import Path
import hashlib,json,math
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[1];S=R/'_ART_SOURCES/stage8_identity_1018/returned';Q=R/'_shots/stage8_identity_1018'
for bank in S.iterdir():
 paths=sorted(bank.glob('*.png'));frames=[Image.open(p).convert('RGBA') for p in paths];hashes=[hashlib.sha256(im.tobytes()).hexdigest() for im in frames]
 print(json.dumps(dict(bank=bank.name,count=len(frames),unique=len(set(hashes)),blank=sum(im.getbbox() is None for im in frames))))
 out=Image.new('RGB',(1024,274*math.ceil(len(frames)/4)),'#101722');d=ImageDraw.Draw(out)
 for i,im in enumerate(frames):
  x=i%4*256;y=i//4*274;out.paste(im,(x,y),im);d.text((x+3,y+256),str(i),fill='white')
 out.save(Q/(bank.name+'-raw.png'))
