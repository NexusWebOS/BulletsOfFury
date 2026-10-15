"""Render the level-2 solid rectangles (and optional spawn points) over the compound plate.
   python check_map.py [out.png]   - reads js/level2_map.js and js/level2.js through node."""
import json, subprocess, sys, os
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
js = r"""
globalThis.window=globalThis; require('./js/level2_map.js');
let spawns=[]; try{ require('./js/level2_data.js'); spawns=globalThis.TD.LEVEL2_DATA||{}; }catch(e){}
console.log(JSON.stringify({rects:globalThis.TD.LEVEL2_MAP.rects, data:spawns}));
"""
out = subprocess.run(['node', '-e', js], cwd=os.path.join(HERE, '..'), capture_output=True, text=True)
if out.returncode: print(out.stderr); sys.exit(1)
D = json.loads(out.stdout)
plate = Image.open(os.path.join(ROOT, 'assets/game/atlas/terrain_props_0.png')).convert('RGBA').crop((0, 0, 800, 3616))
bg = Image.new('RGBA', plate.size, (10, 10, 10, 255)); bg.alpha_composite(plate)
ov = Image.new('RGBA', plate.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
COL = {'b': (255, 40, 40, 90), 'h': (40, 255, 60, 90), 'v': (60, 120, 255, 110)}
for x0, y0, x1, y1, t in D['rects']:
    d.rectangle([x0, y0, x1, y1], fill=COL[t], outline=COL[t][:3] + (255,))
data = D['data'] or {}
for u in data.get('units', []):
    d.ellipse([u['x'] - 10, u['y'] - 10, u['x'] + 10, u['y'] + 10], outline=(255, 255, 0, 255), width=3)
    d.text((u['x'] + 12, u['y'] - 6), u['type'], fill=(255, 255, 0, 255))
    for w in u.get('wp') or []:
        d.line([u['x'], u['y'], w[0], w[1]], fill=(255, 255, 0, 120), width=1)
for q in data.get('props', []):
    d.rectangle([q['x'] - 6, q['y'] - 6, q['x'] + 6, q['y'] + 6], outline=(255, 140, 0, 255), width=2)
for c in data.get('checkpoints', []):
    d.line([0, c[1], 800, c[1]], fill=(0, 255, 255, 200), width=2)
bg.alpha_composite(ov)
small = bg.resize((400, 1808), Image.LANCZOS)
halves = [small.crop((0, 0, 400, 904)), small.crop((0, 904, 400, 1808))]
S = Image.new('RGBA', (820, 904), (0, 0, 0, 255)); S.paste(halves[0], (0, 0)); S.paste(halves[1], (420, 0))
dst = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'map_check.png')
S.save(dst); print(dst, len(D['rects']), 'rects')
