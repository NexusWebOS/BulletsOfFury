"""Register generated HUD concept frames without touching the shipping HUD.

Measured source windows are padded to even coordinates. The browser uses one
uniform scale per banner and overlays the existing authored font and icons.
"""
from pathlib import Path
from PIL import Image
import hashlib, json, shutil

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / '_ART_SOURCES/hud_concepts_1011'
OUT = ROOT / 'docs/previews/hud_concepts_1011'
OUT.mkdir(parents=True, exist_ok=True)

# Source-space display recesses, measured from each generated plate.
DATA = [
 dict(key='fury-classic', name='Fury Classic', accent='#ffb345',
      note='Closest to the current cockpit. Bigger counters above; maneuver bars on the left and lock status on the right.',
      bands=[[16,60,1520,344],[22,546,1512,918]],
      wells=dict(score=[123,107,596,61],high=[819,107,593,61],lives=[106,202,612,88],missiles=[818,202,612,88],
                 weapon=[451,602,155,259],special=[679,602,463,116],lock=[1216,602,209,259],
                 roll=[111,603,268,104],somer=[111,739,268,122],speed=[678,775,202,90],shield=[940,775,203,90])),
 dict(key='bold-cabinet', name='Bold Cabinet', accent='#ff6659',
      note='The boldest stock readouts. Red cabinet armor, a wide special panel, and maneuver bars in the right bay.',
      bands=[[8,86,1526,368],[10,530,1524,904]],
      wells=dict(score=[116,132,592,49],high=[828,132,591,49],lives=[107,219,607,105],missiles=[822,219,607,105],
                 weapon=[106,577,192,146],special=[398,577,739,118],roll=[1235,577,195,142],
                 speed=[399,740,322,121],shield=[815,740,321,121],somer=[1235,759,195,100],lock=[106,762,192,97])),
 dict(key='white-interceptor', name='White Interceptor', accent='#78e7ff',
      note='Bright alloy edges with dark display wells. A long special bar sits above the two maneuver bars.',
      bands=[[38,74,1498,366],[26,562,1510,926]],
      wells=dict(score=[157,112,546,69],high=[833,113,546,68],lives=[118,219,596,100],missiles=[821,219,597,100],
                 weapon=[80,603,192,278],special=[350,603,836,76],lock=[1252,636,198,217],
                 roll=[367,727,367,98],somer=[813,727,354,98],speed=[359,868,362,33],shield=[816,868,361,33])),
 dict(key='armored-command', name='Armored Command', accent='#ffd16a',
      note='A centered weapon bay with two wide wings. Left: maneuvers. Right: special and retina lock. Brass and olive armor.',
      bands=[[18,60,1518,344],[18,534,1518,904]],
      wells=dict(score=[114,118,597,59],high=[826,118,596,58],lives=[109,203,602,81],missiles=[825,203,602,81],
                 special=[939,583,480,84],roll=[118,584,481,83],weapon=[696,584,144,228],
                 somer=[110,698,497,91],lock=[930,698,496,91],speed=[189,829,406,35],shield=[942,829,405,35])),
 dict(key='neon-fury', name='Neon Fury', accent='#46f4e5',
      note='Thin cyan rails and long horizontal meters. Weapon left; special, maneuvers, speed and shield read across the lower panel.',
      bands=[[16,106,1518,376],[18,538,1516,920]],
      wells=dict(score=[108,153,621,57],high=[809,154,621,57],lives=[99,248,638,77],missiles=[802,248,637,77],
                 weapon=[107,588,238,283],special=[417,589,1010,86],roll=[416,714,465,70],
                 somer=[926,714,502,71],lock=[1082,823,352,48],speed=[414,824,265,47],shield=[731,824,300,48])),
]

def even_rect(r):
    x,y,w,h=r
    lo_x,lo_y=x//2*2,y//2*2
    hi_x,hi_y=(x+w+1)//2*2,(y+h+1)//2*2
    return [lo_x,lo_y,hi_x-lo_x,hi_y-lo_y]

for index, v in enumerate(DATA, 1):
    source=SRC/(v['key']+'.png')
    im=Image.open(source)
    assert all(n%2==0 for n in im.size), (source, im.size)
    assert im.size==(1536,1024), (source, im.size)
    assert len(v['wells'])==11
    v['number']=index
    v['wells']={k:even_rect(r) for k,r in v['wells'].items()}
    v['size']=list(im.size)
    v['sha256']=hashlib.sha256(source.read_bytes()).hexdigest()
    v['image']=v['key']+'-frame.png'
    shutil.copyfile(source,OUT/v['image'])
    for x,y,x1,y1 in v['bands']:
        assert all(n%2==0 for n in [x,y,x1,y1])
        assert 0<=x<x1<=im.width and 0<=y<y1<=im.height
    for x,y,w,h in v['wells'].values():
        assert all(n%2==0 for n in [x,y,w,h])
        assert 0<=x<x+w<=im.width and 0<=y<y+h<=im.height

shutil.copyfile(ROOT/'assets/game/levels/stage_01/ui/player_hud_1008.png',OUT/'authored-meter-source.png')
review=dict(title='Bullets of Fury — five HUD concepts', date='2026-10-11',
            scope='Concept review only. Shipping HUD and radar unchanged pending Mike\'s selection.',
            generatedWith='built-in image_gen', logicalSize=[576,784],
            topHeight=112, playfieldSize=[480,512], bottomHeight=160,
            layouts=DATA, imagePrompts='../../../_ART_SOURCES/hud_concepts_1011/prompts.json',
            references='references.json', registration='Uniform banner fit; no nonuniform sprite scaling.')
(OUT/'concepts.json').write_text(json.dumps(review,indent=2),encoding='utf-8')
(SRC/'registration.json').write_text(json.dumps(review,indent=2),encoding='utf-8')
print('Registered five generated plates, 55 measured even display windows and unchanged authored references.',flush=True)
