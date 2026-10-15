"""Own the authored Overdrive dossier exports, pivots and registration together."""
from pathlib import Path
import hashlib, json
from PIL import Image

ROOT = Path(__file__).resolve().parents[3]
DEST = ROOT / 'expansion/topdown/art/boss_intro_1011'
SRC = DEST / 'source'
PREFIX = DEST.relative_to(ROOT).as_posix()
assets, frames, crops = {}, [], []


def export(image, key, size, scale, pivot, source_pivot):
    # One affine factor for both axes; integer output canvases add transparent
    # padding without stretching art or fitting poses independently.
    px, py = pivot
    cx, cy = source_pivot
    tx, ty = px - scale * cx, py - scale * cy
    out = image.transform(size, Image.Transform.AFFINE,
        (1/scale, 0, -tx/scale, 0, 1/scale, -ty/scale),
        resample=Image.Resampling.NEAREST)
    out.save(DEST / (key + '.png'))
    assets[key] = {'file': PREFIX + '/' + key + '.png', 'size': list(size),
        'anchor': list(pivot), 'bounds': list(out.getbbox()), 'scale': scale}
    assert all(n % 2 == 0 for n in out.size)
    assert out.getbbox()[0] > 0 and out.getbbox()[2] < size[0]
    return out


card = Image.open(SRC / 'card_generated.png').convert('RGBA')
factor = min(1196/card.width, 844/card.height)
export(card, 'od_warrior_card', (1200,848), factor, (600,424), (card.width/2,card.height/2))
master = Image.open(SRC / 'turntable_generated_v2.png').convert('RGBA')
slots = []
for i in range(16):
    x, y = i % 4, i // 4
    rect = [round(x*master.width/4),round(y*master.height/4),
        round((x+1)*master.width/4),round((y+1)*master.height/4)]
    im = master.crop(rect)
    bounds = im.getbbox()
    assert bounds, f'Empty pose {i}'
    slots.append((im,bounds))
    crops.append({'frame':i,'sourceRect':rect,'sourceBounds':list(bounds)})
factor = min(472/max(b[2]-b[0] for _,b in slots),402/max(b[3]-b[1] for _,b in slots))
sheet = Image.new('RGBA',(2048,2048))
preview = Image.new('RGBA',(1024,1024),(6,14,23,255))
for i,(im,bounds) in enumerate(slots):
    key = 'od_warrior_view_' + str(i)
    frame = export(im,key,(512,512),factor,(256,454),((bounds[0]+bounds[2])/2,bounds[3]))
    assets[key]['sourceRect'] = crops[i]['sourceRect']
    frames.append(key)
    sheet.alpha_composite(frame,((i%4)*512,(i//4)*512))
    preview.alpha_composite(frame.resize((256,256),Image.Resampling.NEAREST),((i%4)*256,(i//4)*256))
sheet.save(DEST/'turntable_sheet.png')
shots=ROOT/'_shots/overdrive_intro_1011';shots.mkdir(parents=True,exist_ok=True)
preview.save(shots/'turntable_preview.png')
manifest={'tool':'built-in image_gen','role':'Overdrive enemy introduction card and 360-degree rendered turntable',
    'framePolicy':'1200x848 card; sixteen 512x512 poses, one scale and ground pivot256,454',
    'assets':assets,'turntable':frames,'sourceCrops':crops,
    'sourceSHA256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in SRC.glob('*.png')}}
(DEST/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
(DEST/'manifest.js').write_text('window.TD_BOSS_INTRO_ART='+json.dumps(manifest,separators=(',',':'))+';\nObject.assign(window.TD_UI_ART.assets,window.TD_BOSS_INTRO_ART.assets);\n',encoding='utf-8')
print(f'{len(assets)} even frames registered; common turntable scale {factor:.6f}.')
