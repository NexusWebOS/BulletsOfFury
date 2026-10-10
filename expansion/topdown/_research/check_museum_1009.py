"""Draw Level 5's solid map, ring, curtains and placements over the plate (re-run after any edit).
Placements come from TD_LEVEL5 (level5_data.js) and the museum.js PLACE table, read through node."""
import json, subprocess, sys, math
from pathlib import Path
from PIL import Image, ImageDraw
ROOT = Path(__file__).resolve().parents[3]
JS = r"""
global.window={};require('%s/expansion/topdown/js/level5_data.js');
const L=window.TD_LEVEL5;let P={};try{global.window.TD={};require('%s/expansion/topdown/js/museum_place.js');P=window.TD_LEVEL5_PLACE||{};}catch(e){}
console.log(JSON.stringify({L,P}));""" % (ROOT, ROOT)
d = json.loads(subprocess.check_output(['node', '-e', JS]).decode())
L, P = d['L'], d['P']
im = Image.open(ROOT / 'expansion/topdown/art/museum_1009/museum_ground.png').convert('RGBA')
ov = Image.new('RGBA', im.size, (0, 0, 0, 0)); g = ImageDraw.Draw(ov)
col = {'b': (255, 40, 40, 90), 'd': (40, 120, 255, 110), 'h': (40, 200, 60, 90), 'v': (0, 0, 0, 120)}
for x0, y0, x1, y1, t in L['rects']:
    g.rectangle([x0, y0, x1, y1], fill=col[t], outline=(255, 255, 0, 200))
R = L['ring']
for i in range(64):
    a = i / 64 * math.tau
    if any(abs((a - c + math.pi) % math.tau - math.pi) < w for c, w in R['doors']): continue
    x, y = R['x'] + math.cos(a) * R['r'], R['y'] + math.sin(a) * R['r']; h = R['t'] / 2
    g.rectangle([x - h, y - h, x + h, y + h], fill=(255, 40, 40, 90), outline=(255, 160, 0, 200))
for c in L['curtains']: g.line(c, fill=(255, 0, 255, 255), width=3)
for k in ('units', 'props', 'hostages', 'lasers'):
    items = P.get(k, [])
    for it in items:
        x, y = it['x'], it['y']
        c = {'units': (255, 255, 255), 'props': (0, 255, 200), 'hostages': (255, 220, 0), 'lasers': (255, 0, 0)}.get(k, (200, 200, 200))
        g.ellipse([x - 6, y - 6, x + 6, y + 6], outline=c + (255,), width=2)
        g.text((x + 7, y - 6), it.get('type', it.get('kind', k[:3])), fill=c + (255,))
        for w in it.get('wp') or []: g.line([x, y, w[0], w[1]], fill=c + (160,))
        if k == 'lasers': g.line([it['x'], it['y'], it['x2'], it['y2']], fill=(255, 0, 0, 255), width=2)
if P.get('vehicle'): v = P['vehicle']; g.rectangle([v['x'] - 20, v['y'] - 20, v['x'] + 20, v['y'] + 20], outline=(80, 160, 255, 255), width=2)
for w in P.get('waves', []):
    for t, x, y in w: g.rectangle([x - 4, y - 4, x + 4, y + 4], outline=(255, 120, 0, 255))
out = Image.alpha_composite(im, ov)
out.save(sys.argv[1] if len(sys.argv) > 1 else str(ROOT / '_shots/museum_1009/map_check.png'))
print('rects', len(L['rects']))
