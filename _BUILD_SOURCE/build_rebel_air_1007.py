"""Preserve the generated RGBA sprite sheet byte-for-byte and verify its cells."""
from pathlib import Path
from PIL import Image
import argparse, hashlib, json, shutil
root=Path(__file__).resolve().parents[1]
src=root/'_ART_SOURCES/rebel_air_1007/rebel_air.png'
dst=root/'assets/game/rebel_air_1007'
raw=src.read_bytes(); sha=hashlib.sha256(raw).hexdigest()
im=Image.open(src)
assert im.mode=='RGBA' and im.size==(1448,1086)
assert im.getchannel('A').getextrema()==(0,255)
names=['winch','hook_open','chain_link','hook_closed']+[f'nyx_spiral_{i}' for i in range(8)]
cells={}
for n,name in enumerate(names):
    x,y=n%4*362,n//4*362
    alpha=im.crop((x,y,x+362,y+362)).getchannel('A')
    bbox=alpha.point(lambda a:255 if a>32 else 0).getbbox()
    assert bbox and bbox[2]-bbox[0]>40 and bbox[3]-bbox[1]>60
    cells[name]={'rect':[x,y,362,362],'alphaBounds':list(bbox),'pivot':[181,181]}
manifest={'key':'ra7_air','path':'assets/game/rebel_air_1007/rebel_air.png','nativeSize':[1448,1086],
 'grid':[4,3],'cellSize':[362,362],'sha256':sha,'cells':cells,'processing':'Exact source byte copy, no raster editing',
 'source':'_ART_SOURCES/rebel_air_1007/rebel_air.png','prompt':'_ART_SOURCES/rebel_air_1007/prompt.txt',
 'notes':'Hook modules articulate independently. Nyx uses the same eight ribbon cells for clipped back/front depth passes.'}
ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');a=ap.parse_args()
if a.write:
    dst.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst/'rebel_air.png')
    (dst/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
else:
    assert hashlib.sha256((dst/'rebel_air.png').read_bytes()).hexdigest()==sha
    assert json.loads((dst/'manifest.json').read_text())==manifest
print(json.dumps({'verified':True,'cells':len(cells),'sha256':sha,'bytes':len(raw),'pixelsEdited':False}))
