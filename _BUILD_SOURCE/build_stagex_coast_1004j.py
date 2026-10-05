"""Normalize generated Stage X terrain without changing its native RGBA alpha."""
from pathlib import Path
from PIL import Image
import json, hashlib

R = Path(__file__).resolve().parents[1]
S = R / '_ART_SOURCES/stagex_coast_1004j/terrain-source.png'
O = R / 'assets/game/stagex_coast_1004j'
O.mkdir(exist_ok=True)
im = Image.open(S).convert('RGBA')
size = (680, round(im.height * 680 / im.width))
terrain = im.resize(size, Image.Resampling.NEAREST)
terrain.save(O / 'terrain.png')
record = {'mode': 'builtin-imagegen-edit', 'source': str(S.relative_to(R)).replace('\\','/'),
          'source_sha256': hashlib.sha256(S.read_bytes()).hexdigest(),
          'source_size': list(im.size), 'runtime_size': list(size),
          'normalization': 'nearest-neighbor only; generated alpha preserved',
          'terrain_key': 'sx1001_arena', 'water_keys': ['nwl_water_'+str(i) for i in range(4)],
          'transparent_pixels': sum(a == 0 for a in terrain.getchannel('A').getdata()),
          'partial_alpha_pixels': sum(0 < a < 255 for a in terrain.getchannel('A').getdata())}
(O / 'manifest.json').write_text(json.dumps(record, indent=2)+'\n', encoding='utf-8')
print(json.dumps(record, indent=2))
