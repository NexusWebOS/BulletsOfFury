"""Source-derived weapon contact reels. Never edits/re-packs the source atlases.

FRAME FORMAT: 96x96, centre48, shared proportional scale per bank, even grid.
Existing authored sparks, energy contacts and Decker scorch pixels supply all art.
Cooling/expiry is baked into frames; runtime does not rotate, stretch or fade them.
"""
from pathlib import Path
import colorsys, hashlib, json
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/game/shared/combat/weapon_contacts_1031'
QA=ROOT/'_shots/weapon_contacts_1031'
OUT.mkdir(parents=True,exist_ok=True);QA.mkdir(parents=True,exist_ok=True)
BANKS={}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def hue(im,degrees,saturation=None):
    im=im.copy();a=im.load()
    for y in range(im.height):
        for x in range(im.width):
            r,g,b,alpha=a[x,y]
            if not alpha or max(r,g,b)<36 or max(r,g,b)-min(r,g,b)<18:continue
            _,s,v=colorsys.rgb_to_hsv(r/255,g/255,b/255)
            r,g,b=colorsys.hsv_to_rgb(degrees/360,s if saturation is None else s*saturation,v)
            a[x,y]=(round(r*255),round(g*255),round(b*255),alpha)
    return im
def bank(name,path,rects,fps=24,tint=None,fade=False):
    source=ROOT/path;im=Image.open(source).convert('RGBA');frames=[]
    # A shared padded canvas and one scale for every pose in the bank.
    pw=max(r[2] for r in rects);ph=max(r[3] for r in rects);pw+=pw%2;ph+=ph%2
    scale=min(88/pw,88/ph);dw=round(pw*scale);dh=round(ph*scale)
    for i,(x,y,w,h) in enumerate(rects):
        src=Image.new('RGBA',(pw,ph));src.alpha_composite(im.crop((x,y,x+w,y+h)),((pw-w)//2,(ph-h)//2))
        if tint is not None:src=hue(src,*tint)
        if fade:src.putalpha(src.getchannel('A').point(lambda a:round(a*(1-i/len(rects)))))
        src=src.resize((dw,dh),Image.Resampling.NEAREST)
        f=Image.new('RGBA',(96,96));f.alpha_composite(src,((96-dw)//2,(96-dh)//2));frames.append(f)
    cols=min(8,len(frames));rows=(len(frames)+cols-1)//cols;sheet=Image.new('RGBA',(96*cols,96*rows))
    for i,f in enumerate(frames):sheet.alpha_composite(f,(i%cols*96,i//cols*96))
    dest=OUT/(name+'.png');sheet.save(dest,optimize=True)
    BANKS[name]=dict(key='wc1031_'+name,path=dest.relative_to(ROOT).as_posix(),cw=96,ch=96,cols=cols,frames=len(frames),fps=fps,pivot=[48,48],source=path,sourceSha256=sha(source),sourceRects=rects,sourcePadding=[pw,ph],unitScale=scale,sha256=sha(dest))
def reel(name,source,tint=None):
    p=Path('assets/game/shared/player_weapons/weapon_animation_0928')/source
    r=json.loads((ROOT/p/'reel.json').read_text())
    bank(name,(p/'atlas.png').as_posix(),[f['rect'] for f in r['frames']],r['fps'],tint)

reel('ballistic','chaingun_impact')
for el in ['fire','ice','lightning','kinetic','chrome','dark','toxic','prism','water']:reel('orb_'+el,'orb_hit_'+el)
reel('orb_wind','orb_hit_water',(174,1))
base='assets/game/shared/player_weapons/laser_mist/bof_laser_mist_weapon_atlas.png'
for name,h,s in [('blue',212,1),('orange',30,1),('green',136,1),('white',0,0),('red',3,1),('violet',280,1)]:
    bank('energy_'+name,base,[[i*112,648,104,104]for i in range(8)],32,(h,s))
    bank('residue_'+name,base,[[i*112,760,104,104]for i in range(8)],10,(h,s))
space=Path('assets/game/shared/atlases/bof_gravity_mode_space_weapons.json')
meta=json.loads((ROOT/space).read_text())
for tier in range(1,6):
    rects=[]
    for i in range(4):
        r=meta['frames'][f'laser_{tier}_impact_{i}'];rects.append([r[k]for k in ('x','y','w','h')])
    bank('cannon_'+str(tier),space.with_suffix('.png').as_posix(),rects,24)
index=json.loads((ROOT/'assets/game/shared/asset_index.json').read_text())
for a in index['assets']:
    if not isinstance(a,dict)or not a.get('key','').startswith('ndk_scorch_'):continue
    _,x,y,w,h=a['cell']
    bank('singe_'+a['key'].split('_')[-1],a['path'],[[x,y,w,h]]*8,10,fade=True)

(OUT/'manifest.json').write_text(json.dumps(dict(owner='_BUILD_SOURCE/build_weapon_contacts_1031.py',format='96x96; fixed centre48; source-derived only',banks=BANKS),indent=2)+'\n')
(ROOT/'assets/weapon_contacts_art_1031.js').write_text('"use strict";\nconst WC1031_ART='+json.dumps(BANKS,separators=(',',':'))+';\n',encoding='utf-8',newline='\n')
preview=Image.new('RGB',(880,len(BANKS)*110),(7,19,29));d=ImageDraw.Draw(preview)
for row,(name,a)in enumerate(BANKS.items()):
    d.text((4,row*110+3),name,fill='white');im=Image.open(ROOT/a['path'])
    for i in range(a['frames']):
        f=im.crop((i%a['cols']*96,i//a['cols']*96,i%a['cols']*96+96,i//a['cols']*96+96));preview.paste(f,(100+i*96,row*110+13),f)
preview.save(QA/'contact-reels.png')
print('Built',len(BANKS),'banks,',sum(a['frames']for a in BANKS.values()),'fixed frames')
