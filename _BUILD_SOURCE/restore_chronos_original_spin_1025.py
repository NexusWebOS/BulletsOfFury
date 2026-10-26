"""Restore the original HAMMER/HAMA two-handed whirlwind, as whole plates.

No arm/weapon extraction, replacement tool, mesh, or per-frame fitting. Source
rectangles and chest/head landmarks are the original HAMMER_WHIRL_REEL.
"""
from pathlib import Path
from PIL import Image, ImageDraw
import json, math, hashlib, ast
import numpy as np

R = Path(__file__).resolve().parents[1]
O = R / 'assets/game/shared/combat/chronos_motion_1025'
P = O / 'manifest.json'
art = json.loads(P.read_text(encoding='utf8'))
WORLD = art['worldScale']
SOURCE = R / 'assets/game/levels/stage_05/boss/stage5_archmage_0916/combat_0926/whirlwind_v2.png'
source = Image.open(SOURCE).convert('RGBA')
REEL = [
    [0,0,478,443,280,203,104,280], [478,0,412,443,698,204,534,280],
    [890,0,430,443,1125,204,972,278], [1320,0,454,443,1573,200,1420,278],
    [0,443,478,444,232,575,414,650], [478,443,412,444,642,575,808,650],
    [890,443,430,444,1072,575,1230,650], [1320,443,454,444,1516,580,1694,654],
]
# Same proportional scale for all views; source chest is the common pivot.
PIVOT = art['pixelPivot']

# Reuse the existing material and sheet exporters, never the modular tool bake.
tree = ast.parse((R / '_BUILD_SOURCE/build_chronos_final_1025.py').read_text(encoding='utf8'))
for n in tree.body:
    if isinstance(n, ast.FunctionDef) and n.name in ['steel', 'red', 'export']:
        exec(compile(ast.Module(body=[n], type_ignores=[]), 'whole-spin-export', 'exec'))

frames = []
weapon_palette_masks = []
for f, (x,y,w,h,cx,cy,hx,hy) in enumerate(REEL):
    # Uniform 512-square source padding retains the original odd-sized crops.
    pad = Image.new('RGBA', (512,512))
    pad.alpha_composite(source.crop((x,y,x+w,y+h)), (0,0))
    k = 308 / 512
    offset = [round(PIVOT[0]-(cx-x)*k), round(PIVOT[1]-(cy-y)*k)]
    body = Image.new('RGBA', (448,448))
    body.alpha_composite(pad.resize((308,308), Image.Resampling.NEAREST), tuple(offset))
    # Protect the original weapon colors during the armor palette swap. This
    # is only a color-selection mask on the complete plate, never another tool.
    yy, xx = np.indices((512,512))
    boundary = cx-x+(hx-cx)*.25
    side = xx<boundary if hx<cx else xx>boundary
    mask = Image.fromarray((side & (abs(yy-(hy-y))<60)).astype('uint8')*255)
    mapped = Image.new('L',(448,448))
    mapped.paste(mask.resize((308,308),Image.Resampling.NEAREST),tuple(offset))
    weapon_palette_masks.append(np.array(mapped)>0)
    tip = [(hx-x)*k+offset[0], (hy-y)*k+offset[1]]
    # The original head's full luminous barrel, not the chest or hand, is the
    # contact/Retina landmark. This is one plate including both gripping hands.
    grip = [PIVOT[0], PIVOT[1]+32*k]
    meta = dict(tip=[v*WORLD for v in tip], grip=[v*WORLD for v in grip],
                headBounds=[(tip[0]-32*k)*WORLD,(tip[1]-42*k)*WORLD,
                            (tip[0]+32*k)*WORLD,(tip[1]+42*k)*WORLD],
                bounds=[v*WORLD for v in body.getbbox()], angle=0, empty=False,
                sourceFrame=f, wholeAuthored=True, gripHands=2)
    frames.append((body, meta))

for mat in ['regular','chrome','red']:
    rows = []
    for i, (im, meta) in enumerate(frames):
        image = im.copy() if mat=='regular' else steel(im, True)
        if mat=='red': image=red(image)
        pixels=np.array(image);original=np.array(im)
        pixels[weapon_palette_masks[i]]=original[weapon_palette_masks[i]]
        image=Image.fromarray(pixels)
        rows.append((image, meta))
    export('spin_'+mat, rows)

art['originalSpin'] = dict(source=SOURCE.relative_to(R).as_posix(),
    sourceKey='arch_whirlwind_0926', sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
    sourceRects=REEL, sourceScale=308/512, frames=8, hands=2,
    note='Whole original two-handed body/hammer plates. No separate held hammer or limb assembly; palette-only armor variants.')
P.write_text(json.dumps(art,indent=2)+'\n',encoding='utf8')
(R/'assets/chronos_motion_art_1025.js').write_text('"use strict";\nconst C27_ART='+json.dumps(art,separators=(',',':'))+';\n',encoding='utf8',newline='\n')
out=R/'_shots/chronos_original_1025';out.mkdir(exist_ok=True)
contact=Image.new('RGBA',(448*4,472*2),(16,25,38,255));draw=ImageDraw.Draw(contact)
for i,(im,_) in enumerate(frames):
    x=i%4*448;y=i//4*472;contact.alpha_composite(im,(x,y+24));draw.text((x+10,y+6),f'Original complete frame {i+1}',fill='white')
contact.save(out/'restored-whole-spin.png')
print(json.dumps({'frames':24,'cells':[448,448],'originalTwoHands':True,'toolComposites':0}))
