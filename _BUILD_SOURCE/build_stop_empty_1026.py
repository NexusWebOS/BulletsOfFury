"""The Hammer Time raised-palm STOP frames (ht27 boss 12-15) with the hammer lifted out of his
left hand: Chronos has just thrown it when he does this pose in the rage forming.
Output: assets/game/levels/stage_05/boss/chronos_rageform_1026/stop_empty.png
(4 cells of 314x314 side by side, same pivots as the source frames)."""
from pathlib import Path
import json, re
from PIL import Image, ImageDraw
R = Path(__file__).resolve().parents[1]
s = (R/'assets/hammer_time_art_0927.js').read_text(encoding='utf-8')
d = json.loads(re.search(r'"boss":(\{.*?\]\][^}]*\})', s).group(1))
src = Image.open(R/d['path']).convert('RGBA')
# hammer head and handle, native cell px (measured on frame 12 at 3x; the hammer is static across 12-15)
POLY = [(10, 145), (86, 150), (100, 156), (99, 200), (97, 212), (97, 252), (10, 252)]
PIV0 = d['frames'][12][4]   # each frame draws the figure at its own pivot: shift the mask with it
out = Image.new('RGBA', (314 * 4, 314), (0, 0, 0, 0))
for i, f in enumerate(d['frames'][12:16]):
    c = src.crop((f[0], f[1], f[0] + 314, f[1] + 314))
    dx = f[4] - PIV0
    m = Image.new('L', c.size, 0); ImageDraw.Draw(m).polygon([(x + dx, y) for x, y in POLY], fill=255)
    a = c.split()[3]; a.paste(0, mask=m); c.putalpha(a)
    out.paste(c, (i * 314, 0))
dst = R/'assets/game/levels/stage_05/boss/chronos_rageform_1026/stop_empty.png'
out.save(dst)
print('wrote', dst, out.getbbox())
