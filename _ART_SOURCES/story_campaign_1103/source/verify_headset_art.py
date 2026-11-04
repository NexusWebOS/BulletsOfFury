from pathlib import Path
import hashlib,json,sys
import numpy as np
from PIL import Image,ImageDraw,ImageFont
W=Path(__file__).resolve().parent;D=W.parent/'outputs/BOF-Cutscenes-1103'
A=D/'overlay/assets/game/shared/cinematics/story_1103'
revision=int(sys.argv[1]) if len(sys.argv)>1 else 3
V=D/('verification/revision'+str(revision));S=D/'source-art/headsets-16bit'
before=json.loads((V/'before-assets.json').read_text())
changed=[p.stem for p in A.glob('*.webp') if hashlib.sha256(p.read_bytes()).hexdigest()!=before[p.name]]
pilots=['cole','axel','decker','maverick','freezer','juggernaut','yuri','lizzie','falva']
expected={'headset-cole','comic-cole','comic-decker'} if revision==4 else {prefix+p for prefix in ['headset-','comic-'] for p in pilots}
assert set(changed)==expected,changed
board=Image.new('RGB',(864,960),'#15151c');draw=ImageDraw.Draw(board)
font=ImageFont.truetype(r'C:\Windows\Fonts\consolab.ttf',20)
facts=[]
for i,p in enumerate(pilots):
    im=Image.open(S/(p+'.png')).convert('RGBA');a=np.array(im)
    colors=len(np.unique(a[a[:,:,3]>0,:3],axis=0))
    assert im.size==(128,128) and colors<=32
    assert set(np.unique(a[:,:,3]))=={0,255},p
    # Individual exported portrait must consist of exactly 2x source pixels.
    bank=Image.open(A/('headset-'+p+'.webp')).convert('RGBA')
    crop=bank.crop((16,16,272,272))
    # Fully transparent RGB may be normalized by the WebP codec.
    expected_pixels=np.array(im.resize((256,256),Image.Resampling.NEAREST))
    actual=np.array(crop)
    assert np.array_equal(actual[:,:,3],expected_pixels[:,:,3])
    mask=actual[:,:,3]>0;assert np.array_equal(actual[mask],expected_pixels[mask]),p
    x=i%3*288+16;y=i//3*320+8
    board.paste(im.resize((256,256),Image.Resampling.NEAREST),(x,y),im.resize((256,256),Image.Resampling.NEAREST))
    draw.text((x,y+274),p.upper(),font=font,fill='#e4e4e8')
    facts.append({'pilot':p,'native':[128,128],'opaque_colors':colors,'alpha':[0,255],'standalone_integer_scale':2,'comic_integer_scale':3})
board.save(D/'Headsets-16bit.png')
report={'changed_banks':changed,'unchanged_other_banks':len(before)-len(changed),'headsets':facts}
(V/'art-report.json').write_text(json.dumps(report,indent=2))
print(json.dumps({'new_headsets':len(facts),'changed_banks':len(changed),'unchanged_other_banks':report['unchanged_other_banks']}))
