from pathlib import Path
import json
from PIL import Image
R=Path(__file__).resolve().parents[1];D=R/'assets/game/levels/stage_06/boss/nyx_ambush_1028';D.mkdir(parents=True,exist_ok=True)
m=json.loads((R/'_ART_SOURCES/nyx_ambush_1028/sources.json').read_text());v=m['eglaser_2'];c=v['cell'];im=Image.open(R/v['path']).convert('RGBA').crop((c[1],c[2],c[1]+c[3],c[2]+c[4]));im.thumbnail((10,42))
base=Image.new('RGBA',(64,64));base.paste(im,((64-im.width)//2,(64-im.height)//2));sheet=Image.new('RGBA',(512,256))
for i in range(32):sheet.paste(base.rotate(-i*360/32,resample=Image.Resampling.BICUBIC),((i%8)*64,(i//8)*64))
sheet.save(D/'lasers.png');(D/'manifest.json').write_text(json.dumps(dict(source='eglaser_2',cell=[64,64],pivot=[32,32],frames=32,columns=8),indent=2))
