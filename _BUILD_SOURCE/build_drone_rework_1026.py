"""Bake drone-native magenta emission and hard pixel-glow rings, 1015 method."""
from pathlib import Path
from PIL import Image, ImageFilter
import hashlib
import json
import numpy as np

R = Path(__file__).resolve().parents[1]
O = R / 'assets/game/levels/stage_08/boss/drone_rework_1026'
O.mkdir(exist_ok=True)
t = (R / 'assets/stage8_pixellab_art_1018.js').read_text()
a = json.JSONDecoder().raw_decode(t[t.index('{'):])[0]['drone']
im = Image.open(R / a['path']).convert('RGBA')
raw = np.array(im); rgb = raw[:,:,:3].astype(float)
lum = rgb @ np.array([.2126,.7152,.0722])
lit = ((lum > 130) | ((rgb[:,:,1] > rgb[:,:,0]*1.12) & (rgb[:,:,1] > rgb[:,:,2]*1.08) & (lum > 28))) & (raw[:,:,3] > 24)
alpha = np.where(lit, np.minimum(raw[:,:,3], 70+lum*.5), 0).astype(np.uint8)
mask = Image.fromarray(alpha)
out = np.zeros_like(raw); out[:,:,:3] = [195,52,215]; out[:,:,3] = alpha
glow = Image.fromarray(out)
for size, opacity in [(3, .24),(5, .13),(7, .065)]:
    outer = np.array(mask.filter(ImageFilter.MaxFilter(size))).astype(float)
    ring = np.zeros_like(raw); ring[:,:,:3] = [195,52,215]
    ring[:,:,3] = np.maximum(0, outer-alpha)*opacity
    glow = Image.alpha_composite(Image.fromarray(ring), glow)
dest = O / 'drone-pixel-glow.webp'; glow.save(dest, lossless=True, method=6)
art = {'key': 'rd29_drone_glow', 'path': dest.relative_to(R).as_posix(), 'w': 256, 'h': 256, 'pivot': [128,128],
       'source': a, 'sourceSha256': hashlib.sha256((R/a['path']).read_bytes()).hexdigest(), 'owner': '_BUILD_SOURCE/build_drone_rework_1026.py', 'sha256': hashlib.sha256(dest.read_bytes()).hexdigest(), 'method': 'Own emissive pixels and 1-3px hard rings; PXG_STEPS driver, no radial overlay or blur.'}
(O / 'manifest.json').write_text(json.dumps(art, indent=2), encoding='utf8')
(R / 'assets/drone_rework_art_1026.js').write_text("'use strict';\nconst RD29_ART="+json.dumps(art,separators=(',',':'))+';\n',encoding='utf8')
print(json.dumps({'size': list(im.size), 'emissivePixels': int(lit.sum()), 'path': str(dest)}))

taxonomy=R/'assets/data/ART_TAXONOMY.json'
raw=taxonomy.read_bytes()
if 'rd29_' not in json.loads(raw.decode('utf8')):
    entry={'rd29_':{'role':'drone_native_magenta_pixel_glow','owner':'_BUILD_SOURCE/build_drone_rework_1026.py','manifest':'assets/game/levels/stage_08/boss/drone_rework_1026/manifest.json','note':'Mike Oct26: source-derived 256x256 own-pixel emission with fixed pivot and hard rings; six stepped 1015 charge levels, original drone unchanged.'}}
    fragment=json.dumps(entry,indent=2)[1:-2]+','
    if b'\r\n' in raw:fragment=fragment.replace('\n','\r\n')
    pos=raw.index(b'{')+1;updated=raw[:pos]+fragment.encode()+raw[pos:];json.loads(updated);taxonomy.write_bytes(updated)
