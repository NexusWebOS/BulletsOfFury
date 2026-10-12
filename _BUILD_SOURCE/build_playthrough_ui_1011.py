"""Proportional, even exports of October 11's generated interface plaques."""
from pathlib import Path
from PIL import Image
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'_ART_SOURCES/playthrough_1011/returned'
OUT=ROOT/'assets/game/shared/ui/playthrough_1011';OUT.mkdir(parents=True,exist_ok=True)
rows={}
for name in ['brand-plaque','author-plaque','fullscreen-button']:
    im=Image.open(SRC/(name+'.png')).convert('RGBA')
    # Crop only empty gutters, preserve authored proportions, then pad even.
    box=im.getchannel('A').point(lambda a:255 if a>8 else 0).getbbox()
    plate=im.crop(box);scale=min(1,(128 if name=='fullscreen-button' else 640)/max(plate.size))
    size=tuple(round(n*scale) for n in plate.size);plate=plate.resize(size,Image.Resampling.LANCZOS)
    w,h=((n+1)//2*2 for n in size);out=Image.new('RGBA',(w,h));out.alpha_composite(plate,((w-size[0])//2,(h-size[1])//2))
    path=OUT/(name+'.png');out.save(path,optimize=True)
    rows[name]=dict(path=path.relative_to(ROOT).as_posix(),w=w,h=h,sourceRect=box,scale=scale,sha256=hashlib.sha256(path.read_bytes()).hexdigest())
(OUT/'registration.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
print(json.dumps(rows,indent=2))
