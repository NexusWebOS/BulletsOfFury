"""Register built-in generated FX on even, fixed canvases; never per-cell fit."""
from pathlib import Path
from PIL import Image
import json, hashlib, shutil

ROOT=Path(__file__).resolve().parents[1]
ARCHIVE=ROOT/'_ART_SOURCES/audio_1010'
DEST=ROOT/'assets/game/shared/combat/audio_1010'
ARCHIVE.mkdir(parents=True,exist_ok=True);DEST.mkdir(parents=True,exist_ok=True)
manifest={}

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def ice():
    source=Path(r'C:/Users/Mdogg/.codex/generated_images/01a0e3c8-265d-7731-8ffe-ee42ebb5ba3c/exec-f3c6adeb-38c8-48b5-9ee3-3a2b092e276b.png')
    raw=ARCHIVE/'ice_laser_raw.png'
    if not raw.exists():shutil.copy2(source,raw)
    im=Image.open(raw).convert('RGBA')
    # The raw image has odd dimensions. Measured equal grid cuts and a single
    # physical source throat align it using padding, not individual scaling.
    xs=[0,222,444,665,887];ys=[0,444,888,1332,1774]
    pivots=[(111,396),(111,396),(109,396),(111,396),
            (111,396),(111,396),(110,396),(111,396),
            (111,396),(111,396),(110,396),(111,396),
            (111,396),(111,396),(110,396),(111,396)]
    bank=[]
    for i in range(16):
        c,r=i%4,i//4;rect=[xs[c],ys[r],xs[c+1],ys[r+1]]
        cell=im.crop(rect);canvas=Image.new('RGBA',(224,448))
        shift=[112-pivots[i][0],396-pivots[i][1]]
        canvas.alpha_composite(cell,tuple(shift))
        file=DEST/f'ice_laser_{i:02}.png';canvas.save(file,optimize=True)
        bank.append(dict(key=f'ap10_ice_laser_{i:02}',path=file.relative_to(ROOT).as_posix(),
                         w=224,h=448,pivot=[112,396],source_rect=rect,source_pivot=list(pivots[i]),
                         translation=shift,scale=1,sha256=sha(file)))
    assert len({q['sha256'] for q in bank})==16
    manifest['ice_laser']=bank
    (ARCHIVE/'ice_laser_registration.json').write_text(json.dumps(dict(raw_sha256=sha(raw),bank=bank),indent=2),encoding='utf-8')

def icons():
    source=Path(r'C:/Users/Mdogg/.codex/generated_images/01a0e3c8-265d-7731-8ffe-ee42ebb5ba3c/exec-fa6b35b9-e747-43da-b5e5-cf0b9a6895dc.png')
    raw=ARCHIVE/'wind_icons_raw.png'
    if not raw.exists():shutil.copy2(source,raw)
    im=Image.open(raw).convert('RGBA');bank=[]
    assert im.size==(1254,1254)
    for i,w in enumerate([0,1,2,3,4,5,6,7,8]):
        c,r=i%3,i//3;rect=[c*418,r*418,(c+1)*418,(r+1)*418]
        canvas=Image.new('RGBA',(432,432));canvas.alpha_composite(im.crop(rect),(7,7))
        file=DEST/f'wind_icon_{w}.png';canvas.save(file,optimize=True)
        bank.append(dict(key=f'ap10_wind_icon_{w}',path=file.relative_to(ROOT).as_posix(),
                         w=432,h=432,pivot=[216,216],source_rect=rect,translation=[7,7],scale=1,sha256=sha(file)))
    manifest['wind_icons']=bank
    (ARCHIVE/'wind_icons_registration.json').write_text(json.dumps(dict(raw_sha256=sha(raw),bank=bank),indent=2),encoding='utf-8')

def effect(name,source_name,cols,rows,canvas_size,pivots,row_cuts=None):
    source=Path(r'C:/Users/Mdogg/.codex/generated_images/01a0e3c8-265d-7731-8ffe-ee42ebb5ba3c')/source_name
    raw=ARCHIVE/(name+'_raw.png')
    if not raw.exists():shutil.copy2(source,raw)
    im=Image.open(raw).convert('RGBA');W,H=im.size;bank=[]
    for i in range(cols*rows):
        c,r=i%cols,i//cols
        rect=[round(c*W/cols),row_cuts[r] if row_cuts else round(r*H/rows),
              round((c+1)*W/cols),row_cuts[r+1] if row_cuts else round((r+1)*H/rows)]
        cell=im.crop(rect);source_pivot,pivot=pivots(i)
        shift=[round(pivot[0]-source_pivot[0]),round(pivot[1]-source_pivot[1])]
        canvas=Image.new('RGBA',canvas_size);canvas.alpha_composite(cell,tuple(shift))
        file=DEST/f'{name}_{i:02}.png';canvas.save(file,optimize=True)
        bank.append(dict(key=f'ap10_{name}_{i:02}',path=file.relative_to(ROOT).as_posix(),
                         w=canvas_size[0],h=canvas_size[1],pivot=pivot,source_rect=rect,
                         source_pivot=source_pivot,translation=shift,scale=1,sha256=sha(file)))
    assert len({q['sha256'] for q in bank})==len(bank)
    if name=='wind':
        for i,a in enumerate(bank):
            a['clip']=['charge','gust','tornado','impact'][i//4]
    manifest[name]=bank
    (ARCHIVE/(name+'_registration.json')).write_text(json.dumps(dict(raw_sha256=sha(raw),bank=bank),indent=2),encoding='utf-8')

ice();icons()
effect('wind','exec-90711558-b9a0-4061-ac54-644f5d948e72.png',4,4,(320,336),
       lambda i:([155,304],[160,320]) if i<8 else ([155,158],[160,168]))
# The accepted generator left unequal vertical spacing. Measured blank gutters
# separate the four rows; charge cells must not contain the next held beam.
# Each real chrome muzzle is registered to the same (136,328) source point.
fusion_rows=[0,344,736,1128,1536]
fusion_muzzles=[312,706,1100,1487]
effect('fusion','exec-ac70704c-1850-47a7-8a13-444903f303ed.png',4,4,(272,400),
       lambda i:([128,fusion_muzzles[i//4]-fusion_rows[i//4]],[136,328]),fusion_rows)
from wind_icon_art_1011 import add_wind_icons
add_wind_icons(manifest)
from wind_projectile_art_1011 import add_wind_projectiles
add_wind_projectiles(manifest)
(ROOT/'assets/audio_fx_art_1010.js').write_text('"use strict";\nconst AP10_FX_ART='+json.dumps(manifest)+';\n',encoding='utf-8',newline='\n')
print(json.dumps({k:len(v) for k,v in manifest.items()}))
