"""Copy authored UI reference pixels into an even comparison sheet."""
from pathlib import Path
from PIL import Image
import json, hashlib
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'_ART_SOURCES/wind_icons_1011';OUT.mkdir(parents=True,exist_ok=True)
ref=Image.new('RGBA',(768,768));rows=[]
for i in range(9):
    f=ROOT/f'assets/game/shared/ui/ui/forge_0917/micon_forge_fire_{i}.png'
    im=Image.open(f).convert('RGBA');x=(i%3)*256+(256-im.width)//2;y=(i//3)*256+(256-im.height)//2
    ref.alpha_composite(im,(x,y));rows.append(dict(slot=i,file=f.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(f.read_bytes()).hexdigest(),native_size=list(im.size)))
ref.save(OUT/'weapon_badge_reference.png')
ref=Image.new('RGBA',(768,256))
for i,elem in enumerate(['fire','ice','prism']):
    f=ROOT/f'assets/game/shared/ui/ui/infusion_0917/inf_{elem}.png';im=Image.open(f).convert('RGBA')
    ref.alpha_composite(im,(i*256+(256-im.width)//2,(256-im.height)//2))
    rows.append(dict(element=elem,file=f.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(f.read_bytes()).hexdigest(),native_size=list(im.size)))
ref.save(OUT/'element_badge_reference.png')
(OUT/'references.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
print('Prepared original nine projectile badges and three element symbols without redrawing them.')
