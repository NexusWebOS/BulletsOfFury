"""Source-preserving red electrical impact export: 16 fixed128x128 frames.

The original electrical strip is retained. Pad its321px crop to322 square,
then apply one common proportional scale. Preserve source alpha and luminance;
neutral outlines/white cores stay neutral. No generated/procedural silhouettes.
"""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image

R=Path(__file__).resolve().parents[1]
D=R/'assets/game/levels/stage_08/miniboss/herald_electric_1031'
D.mkdir(parents=True,exist_ok=True)
s=(R/'assets/feedback_art_1002.js').read_text(encoding='utf-8')
a=json.JSONDecoder().raw_decode(s[s.index('{'):])[0]['electrical']
source=R/a['path'];strip=Image.open(source).convert('RGBA')
sheet=Image.new('RGBA',(512,512));source_alpha=[]
for f,(x,y,w,h)in enumerate(a['frames']):
    assert(w,h)==(322,321)
    padded=Image.new('RGBA',(322,322));padded.paste(strip.crop((x,y,x+w,y+h)),(0,0))
    cell=padded.resize((128,128),Image.Resampling.NEAREST)
    v=np.array(cell);rgb=v[:,:,:3].astype(np.float64)/255
    lum=rgb@np.array([.2126,.7152,.0722])
    # Red/white hue at the source's luminance, leaving dark/neutral source ink.
    hue=np.array([1.,.015,.075]);base=float(hue@np.array([.2126,.7152,.0722]))
    t=np.clip((lum-base)/(1-base),0,1)
    red=np.where((lum<=base)[:,:,None],lum[:,:,None]/base*hue,hue+(1-hue)*t[:,:,None])
    coloured=(rgb.max(2)-rgb.min(2)>.04)&(v[:,:,3]>0)
    v[:,:,:3]=np.where(coloured[:,:,None],np.rint(red*255),v[:,:,:3]).clip(0,255).astype(np.uint8)
    assert np.array_equal(v[:,:,3],np.array(cell)[:,:,3])
    source_alpha.append(hashlib.sha256(v[:,:,3].tobytes()).hexdigest())
    sheet.paste(Image.fromarray(v),(f%4*128,f//4*128))
path=D/'electric_red.png';sheet.save(path)
meta={'key':'hh101_electric_red','path':path.relative_to(R).as_posix(),'cw':128,'ch':128,'cols':4,'frames':16,'pivot':[64,64],
      'source':a['path'],'sourceSha256':hashlib.sha256(source.read_bytes()).hexdigest(),'sourceRects':a['frames'],
      'sourcePadding':[322,322],'unitScale':128/322,'fps':32,'alphaSha256':source_alpha,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
      'recipe':'Pad then normalize authored FB1002 electrical strip; luminance-preserving red/white hue, unchanged alpha and neutral ink.'}
(D/'manifest.json').write_text(json.dumps(meta,indent=2),encoding='utf-8')
(R/'assets/herald_electric_art_1031.js').write_text('"use strict";\nconst HH101_ART='+json.dumps(meta,separators=(',',':'))+';\n',encoding='utf-8')
print('Exported16 source-authored128x128 red electric impact frames')
