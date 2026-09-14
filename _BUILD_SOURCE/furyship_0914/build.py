"""Normalize generated Furyship candidate sheets; never modify the shipping atlas.

Only extraction, matte removal, shared scaling and frame registration happen here.
The artwork itself is produced by image_gen; prompts and masters are preserved.
"""
from pathlib import Path
import hashlib
import json
import ast
import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / '_ART_SOURCES/furyship_0914'
OUT = ROOT / 'assets/game/furyship_0914'
PROOF = ROOT / '_shots/furyship_0914'
OUT.mkdir(exist_ok=True)
PROOF.mkdir(exist_ok=True)
frames = {}
views = ['top', 'front', 'left', 'back', 'right']
# Reuse only the existing owner's pure mask function. Importing that whole script
# would rebuild the shipping atlas because its build runs at module scope.
owner = ast.parse((ROOT/'_BUILD_SOURCE/build_gravity_mode_v2.py').read_text(encoding='utf-8'))
mask_fn = next(n for n in owner.body if isinstance(n,ast.FunctionDef) and n.name=='blue_mask')
exec(compile(ast.Module(body=[mask_fn],type_ignores=[]),'<existing blue_mask>','exec'),globals())

def source(name):
    im = Image.open(SRC / (name + '.png')).convert('RGBA')
    if name in ['core', 'somersault']:
        a = np.array(im)
        rgb = a[:, :, :3].astype(int)
        matte = (rgb[:, :, 0] - rgb[:, :, 1] > 70) & (rgb[:, :, 2] - rgb[:, :, 1] > 70)
        a[matte] = 0
        im = Image.fromarray(a)
    return im

def bounds(im):
    return im.getchannel('A').point(lambda v: 255 if v > 16 else 0).getbbox()

def save(key, im, meta):
    assert im.mode == 'RGBA' and bounds(im), key
    im.save(OUT / (key + '.png'))
    frames[key] = dict(path=key + '.png', size=list(im.size), alphaBounds=list(bounds(im)), **meta)

for master, names, lengths in [
    ('core', ['nose', 'hull'], [58, 44]),
    ('wings', ['wing_left', 'wing_right'], [48, 48]),
    ('engines', ['engine_left', 'engine_right'], [65, 65]),
]:
    im = source(master)
    cuts = [round(i * im.width / 5) for i in range(6)]
    if master == 'engines':
        # This generated master did not obey an equal-column grid. Reviewed separators.
        cuts = [0, 320, 565, 1040, 1305, im.width]
    for row, name in enumerate(names):
        cells = [im.crop((cuts[c], round(row * im.height / 2), cuts[c+1], round((row+1)*im.height/2))) for c in range(5)]
        boxes = [bounds(c) for c in cells]
        assert all(boxes), name
        # One physical scale for every view, never expand edge-on poses to fill cells.
        scale = lengths[row] / max(max(b[2]-b[0], b[3]-b[1]) for b in boxes)
        for col, (cell, box) in enumerate(zip(cells, boxes)):
            crop = cell.crop(box)
            crop = crop.resize((max(1, round(crop.width*scale)), max(1, round(crop.height*scale))), Image.Resampling.NEAREST)
            canvas = Image.new('RGBA', (128, 128))
            canvas.alpha_composite(crop, ((128-crop.width)//2, (128-crop.height)//2))
            save(name+'_'+views[col], canvas, dict(family=name, view=views[col], pivot=[64,64], scale=scale, source=master+'.png', sourceCell=[cuts[col],round(row*im.height/2),cuts[col+1],round((row+1)*im.height/2)], sourceBounds=box))

for family in ['assembly', 'veil', 'speed', 'thrusters', 'roll', 'somersault']:
    im = source(family)
    rows = 3 if family == 'somersault' else 2
    cells = [im.crop((round(c*im.width/4),round(r*im.height/rows),round((c+1)*im.width/4),round((r+1)*im.height/rows))) for r in range(rows) for c in range(4)]
    boxes = [bounds(c) for c in cells]
    assert all(boxes), family
    scale = 114/max(b[3]-b[1] for b in boxes) if family in ['roll','somersault'] else None
    for i, cell in enumerate(cells):
        if family in ['roll','somersault']:
            crop = cell.crop(boxes[i])
            crop = crop.resize((round(crop.width*scale),round(crop.height*scale)),Image.Resampling.NEAREST)
            canvas = Image.new('RGBA',(128,128))
            canvas.alpha_composite(crop,((128-crop.width)//2,(128-crop.height)//2))
        else:
            # Preserve each complete cell and its fixed origin; do not center each effect's bounds.
            size = (192,256) if family in ['veil','speed'] else (256,256)
            canvas = cell.resize(size,Image.Resampling.NEAREST)
        save(family+'_'+str(i).zfill(2), canvas, dict(family=family,index=i,pivot=[canvas.width/2,canvas.height/2],source=family+'.png',scale=scale))

base = ROOT/'assets/game/gravity_mode/furyship_somersault_13.png'
(OUT/'runtime_base.png').write_bytes(base.read_bytes())
blue_mask(Image.open(base)).save(OUT/'runtime_base_blue.png')
pack = {'status':'candidate: generated and normalized, not installed in gameplay', 'reference':str(base.relative_to(ROOT)).replace('\\','/'), 'referenceSha256':hashlib.sha256(base.read_bytes()).hexdigest(), 'frameCount':len(frames), 'frames':frames,
        'sequences':{k:[f'{k}_{i:02}' for i in range(12 if k=='somersault' else 8)] for k in ['assembly','veil','speed','thrusters','roll','somersault']},
        'notes':['Component pivots are normalized local centers, not yet approved assembly sockets.','Generated top views are candidates; exact reassembly against frame 13 remains a release gate.','Roll frame 00 is generated and must be reconciled with the exact approved source before shipping.','Existing 16-frame somersault source is preserved unchanged.','Veil and speed are RGBA overlays; preserve alpha when compositing.']}
pack['playbackSuggestions']={'assembly':{'fps':12,'loop':False},'veil':{'fps':12,'loop':False},'speed':{'fps':12,'loop':True},'thrusters':{'fps':12,'ignition':[0,1,2,3],'sustain':[4,5],'release':[6,7]},'roll':{'fps':13,'loop':False}}
pack['playbackSuggestions']['somersault']={'fps':20,'loop':False,'axis':'pitch around the wing axis','anglesDegrees':[i*30 for i in range(12)],'nominalDurationSeconds':0.6}
pack['notes'].append('New 12-pose somersault candidate has rear/front end-on and underside views; frame width drift and the return to the exact source remain review items.')
pack['palettes']={
 'axel':{'color':'#348dff','lum':1,'model':'Aristotle'},'cole':{'color':'#7ad63a','lum':1.35,'model':'Collisto'},
 'maverick':{'color':'#3ad6c8','lum':1.20,'model':'Moonraker'},'decker':{'color':'#ffe030','lum':1.75,'model':'Draven'},
 'yuri':{'color':'#ff3030','lum':1.25,'model':'Yamado'},'freezer':{'color':'#a060ff','lum':1.25,'model':'Falcon'},
 'juggernaut':{'color':'#e0662a','lum':1.15,'model':'Janis'},'lizzie':{'color':'#b88a1c','lum':1.30,'model':'Lavender'},
 'falva':{'color':'#ff2a8f','lum':1.25,'model':'Foxtrout'}}
for key,frame in frames.items():
    if frame['family'] in ['assembly','veil','speed','thrusters']:
        continue
    mask=blue_mask(Image.open(OUT/frame['path']))
    name=key+'_blue.png'
    mask.save(OUT/name)
    frame['paletteMask']=name
pack['paletteMaskCount']=sum('paletteMask' in f for f in frames.values())
(OUT/'pack.json').write_text(json.dumps(pack,indent=2)+'\n',encoding='utf-8')
# File-openable preview data: same owning workflow as the JSON, no fetch required.
(OUT/'catalog.js').write_text('window.FURYSHIP_CANDIDATES='+json.dumps(pack,separators=(',',':'))+';\n',encoding='utf-8')
keys=list(frames)
sheet=Image.new('RGB',(640,((len(keys)+4)//5)*150),(23,28,37))
d=ImageDraw.Draw(sheet)
for n,key in enumerate(keys):
    im=Image.open(OUT/(key+'.png'));im.thumbnail((128,128),Image.Resampling.NEAREST)
    x=(n%5)*128;y=(n//5)*150
    sheet.paste(im,(x+(128-im.width)//2,y+(128-im.height)//2),im)
    d.text((x+3,y+132),key,fill='white')
sheet.save(PROOF/'normalized_contact.png')
print('Normalized',len(frames),'RGBA frames; original runtime and atlas untouched.')
