"""Compose the review from both cast manifests; embed WebP previews for file://."""
from pathlib import Path
from PIL import Image
import json,base64,io
R=Path(__file__).resolve().parents[1];P=R/'docs/previews/cast_cinematics_1102'
old=json.loads((R/'assets/game/shared/cinematics/cast_1102/manifest.json').read_text())
new=json.loads((R/'assets/game/shared/cinematics/cast_performance_1102/manifest.json').read_text())
data={'pilots':{},'chronos':[new['chronos'],*old['chronos']['frames']]}
for pilot,bank in old['pilots'].items():
    data['pilots'][pilot]={'classic':bank['frames'],**{g:b['frames'] for g,b in new['pilots'][pilot].items()},'ship':[new['ship_scenes'][pilot]]}
template=(P/'gallery-template.html').read_text(encoding='utf-8')
(P/'index.html').write_text(template.replace('/*CAST_DATA*/',json.dumps(data,separators=(',',':'))),encoding='utf-8')
embedded=json.loads(json.dumps(data));total=0
frames=embedded['chronos']+[f for p in embedded['pilots'].values() for group in p.values() for f in group]
for frame in frames:
    im=Image.open(R/frame['file'])
    # Embedded actor previews fit the review cards; full PNGs remain in the
    # runtime/source package. Keep wide ship artwork and portrait at full size.
    if im.height==1024 and im.width in [512,768]:im=im.resize((im.width//2,512),Image.Resampling.NEAREST)
    # Only embedded review thumbnails use perceptual compression. The runtime
    # PNGs, source PNGs and lossless animation sheets remain unchanged.
    buf=io.BytesIO();im.save(buf,format='WEBP',lossless=im.size==(512,512),quality=92,method=4)
    encoded=base64.b64encode(buf.getvalue()).decode('ascii');frame['preview']='data:image/webp;base64,'+encoded;total+=len(encoded)
standalone=template.replace('/*CAST_DATA*/',json.dumps(embedded,separators=(',',':')))
(P/'standalone.html').write_text(standalone,encoding='utf-8')
print(json.dumps({'images':len(frames),'embedded_bytes':total,'standalone_bytes':(P/'standalone.html').stat().st_size}))
