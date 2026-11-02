#!/usr/bin/env python3
"""build_brood_blood_1101.py - blood burst for the Brood Sentinel's robot flies.
Source: the authored radial splatter assets/game/shared/effects/fx_0918/efx_burst_toxic.png (8 frames, 128x128 cells).
Each pixel keeps its alpha and silhouette; its luminance is mapped onto a blood ramp (black-maroon -> crimson ->
wet highlight). Output: assets/game/levels/stage_07/enemies/brood_1101/blood_burst.png (same 1024x128 layout)."""
from pathlib import Path
import hashlib, json
from PIL import Image
R = Path(__file__).resolve().parents[1]
SRC = R / 'assets/game/shared/effects/fx_0918/efx_burst_toxic.png'
OUT = R / 'assets/game/levels/stage_07/enemies/brood_1101'; OUT.mkdir(parents=True, exist_ok=True)
RAMP = [(0.00, (26, 2, 6)), (0.28, (92, 6, 14)), (0.52, (152, 14, 22)), (0.74, (204, 32, 30)), (0.90, (236, 86, 70)), (1.00, (255, 182, 160))]

def ramp(l):
    for (a, ca), (b, cb) in zip(RAMP, RAMP[1:]):
        if l <= b:
            t = (l - a) / max(1e-6, b - a); return tuple(round(ca[i] + (cb[i] - ca[i]) * t) for i in range(3))
    return RAMP[-1][1]

im = Image.open(SRC).convert('RGBA'); W, H = im.size; assert (W, H) == (1024, 128)
px = im.load(); out = Image.new('RGBA', (W, H)); po = out.load()
lums = [(0.299 * r + 0.587 * g + 0.114 * b) / 255 for r, g, b, a in im.getdata() if a]
lo, hi = min(lums), max(lums)
for y in range(H):
    for x in range(W):
        r, g, b, a = px[x, y]
        if not a: continue
        l = ((0.299 * r + 0.587 * g + 0.114 * b) / 255 - lo) / max(1e-6, hi - lo)
        po[x, y] = (*ramp(l), a)
dst = OUT / 'blood_burst.png'; out.save(dst)
meta = {'source': str(SRC.relative_to(R)).replace('\\', '/'), 'sourceSha256': hashlib.sha256(SRC.read_bytes()).hexdigest(),
        'output': str(dst.relative_to(R)).replace('\\', '/'), 'sha256': hashlib.sha256(dst.read_bytes()).hexdigest(),
        'cell': 128, 'frames': 8, 'method': 'alpha and silhouette preserved; luminance mapped to a blood ramp', 'ramp': RAMP}
(OUT / 'manifest.json').write_text(json.dumps(meta, indent=1))
print('wrote', dst, out.size)
