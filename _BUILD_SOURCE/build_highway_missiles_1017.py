"""Own the two PixelLab highway-emplacement plates and their source-pixel lamp layer."""
from pathlib import Path
import hashlib,json,shutil
from PIL import Image
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'_ART_SOURCES/highway_missiles_1017'
RAW=ROOT/'_shots/highway_missiles_1017/raw'
DST=ROOT/'assets/game/levels/stage_04/enemies/highway_missiles_1017'
SRC.mkdir(parents=True,exist_ok=True);DST.mkdir(parents=True,exist_ok=True)
art={}
jobs={'pad':'281b17a5-654a-4c71-aefb-5e7d2b3cb548','missile':'d943d051-f15a-47ee-979f-16a0f29df1e7'}
for name,size,pivot in [('pad',(128,128),(64,80)),('missile',(64,192),(32,96))]:
    source=SRC/(name+'.png')
    if not source.exists():shutil.copyfile(RAW/(name+'.png'),source)
    im=Image.open(source).convert('RGBA');assert im.size==size and all(n%2==0 for n in size)
    path=DST/(name+'.png');im.save(path,optimize=True)
    art[name]={'key':'hm17_'+name,'path':path.relative_to(ROOT).as_posix(),'w':size[0],'h':size[1],'pivot':list(pivot),'scale':.55 if name=='pad' else .64,'ink':list(im.getbbox()),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
    if name=='pad':
        p=np.array(im);r,g,b=p[:,:,:3].astype(float).transpose(2,0,1)
        keep=(p[:,:,3]>0)&(r>175)&(g>70)&(r>g*1.12)&(g>b*1.6)
        p[:,:,3]=np.where(keep,p[:,:,3],0);lamp=Image.fromarray(p)
        lamp.save(DST/'lamps.png',optimize=True)
        art['lamps']={**art[name],'key':'hm17_lamps','path':(DST/'lamps.png').relative_to(ROOT).as_posix(),'sha256':hashlib.sha256((DST/'lamps.png').read_bytes()).hexdigest()}
(SRC/'generation.json').write_text(json.dumps({'service':'PixelLab Pixen','date':'2026-10-17','jobs':jobs,'referencesUploaded':False,'frames':{'pad':[128,128],'missile':[64,192]},'export':'Exact generated pixels, no rescaling/cropping/warping. Lamp companion contains only existing amber pixels. Runtime uses one proportional scale per plate. No atlas edits.'},indent=2)+'\n',encoding='utf-8')
(DST/'manifest.json').write_text(json.dumps(art,indent=2)+'\n',encoding='utf-8')
(ROOT/'assets/highway_missile_art_1017.js').write_text('"use strict";\n// Owned by _BUILD_SOURCE/build_highway_missiles_1017.py.\nconst HM17_ART='+json.dumps(art,separators=(',',':'))+';\n',encoding='utf-8',newline='\n')
print('Exported3 even-canvas PNGs; fixed pivots and source-pixel warning lamps.')
