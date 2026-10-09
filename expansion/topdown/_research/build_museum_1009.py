"""Level 5 MUSEUM OF VIOLENCE: normalize the generated museum plate and slice the exhibit sheet.

Sources (SpriteCook, 2026-10-09) live untouched in art/museum_1009/source/:
  museum_raw.png        1152x2048 first plate (kept for provenance)
  museum_doors_raw.png  1152x2048 edit of it: two doorways cut through the rotunda ring (the plate we ship)
  props_raw.png         2048x2048 transparent 4x4 exhibit sheet, intact/broken pairs
Outputs: museum_ground.png (800x1422), mx_*.png, manifest.js / manifest.json.

Intact/broken pairs are cropped with ONE shared rectangle, so a state swap never moves the prop.
The laser post was drawn with its beam baked in; the beam is cut off the plate (the game draws the
live beam itself, from authored laser art), leaving only the emitter.
No base atlas, no pixel reads at runtime.
"""
from pathlib import Path
import json
from PIL import Image

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'expansion/topdown/art/museum_1009'
SRC = OUT / 'source'
REL = 'expansion/topdown/art/museum_1009/'

frames = {}
plate = Image.open(SRC / 'museum_doors_raw.png').convert('RGB').resize((800, 1422), Image.Resampling.LANCZOS)
plate.save(OUT / 'museum_ground.png')
frames['museum_ground'] = {'file': REL + 'museum_ground.png', 'size': [800, 1422], 'anchor': [400, 711]}

sheet = Image.open(SRC / 'props_raw.png').convert('RGBA')
C = sheet.width // 4
NAMES = [['statue', 'statue_broken', 'rifle_case', 'rifle_case_broken'],
         ['vase', 'vase_broken', 'painting', 'painting_broken'],
         ['alarm', 'alarm_broken', 'laser_post', 'laser_post_broken'],
         ['rope', 'rope_broken', 'plasma_case', 'plasma_case_broken']]
SCALE = 0.25          # 2048 sheet -> props about 70-100 px, drawn at ~0.5 in the world


def cell(r, c):
    im = sheet.crop((c * C, r * C, (c + 1) * C, (r + 1) * C))
    if NAMES[r][c] == 'laser_post':
        # the beam is a thin horizontal run to the right of the post: drop every column right of the post
        # whose ink is thinner than the post itself
        a = im.getchannel('A').load()
        cols = [sum(1 for y in range(C) if a[x, y] > 40) for x in range(C)]
        post = max(range(C), key=lambda x: cols[x])
        cut = next((x for x in range(post, C) if cols[x] < max(8, cols[post] * 0.12)), C)
        px = im.load()
        for x in range(cut + 6, C):
            for y in range(C):
                px[x, y] = (0, 0, 0, 0)
        print('laser beam cut at local x', cut + 6, 'post column', post)
    return im


for r in range(4):
    for c in (0, 2):
        a, b = cell(r, c), cell(r, c + 1)
        boxes = [im.getchannel('A').point(lambda v: 255 if v > 24 else 0).getbbox() for im in (a, b)]
        x0 = min(q[0] for q in boxes) - 4; y0 = min(q[1] for q in boxes) - 4
        x1 = max(q[2] for q in boxes) + 4; y1 = max(q[3] for q in boxes) + 4
        for im, name in ((a, NAMES[r][c]), (b, NAMES[r][c + 1])):
            out = im.crop((x0, y0, x1, y1))
            out = out.resize((max(1, round(out.width * SCALE)), max(1, round(out.height * SCALE))), Image.Resampling.LANCZOS)
            fn = 'mx_' + name + '.png'
            out.save(OUT / fn)
            # anchor: horizontal centre, the plinth base (82% down) - where the prop meets the floor
            frames['mx_' + name] = {'file': REL + fn, 'size': [out.width, out.height], 'anchor': [out.width / 2, round(out.height * 0.82)]}
            print(fn, out.size)

prompts = {
    'tool': 'SpriteCook generate_game_art',
    'plate': {'asset_id': '72fe11d1-edfe-4741-9292-4297e39e9a78', 'model': 'gpt-image-2', 'resolution': '2K', 'aspect': '9:16',
              'prompt': 'Full top-down orthographic museum-of-violence interior: lobby, Hall of Arms, west art-gallery maze and east '
                        'vehicle exhibit hall split by a central wall, rotunda atrium, grand hall boss arena (see manifest history).'},
    'plate_edit': {'asset_id': '5225c727-376a-4e37-a282-874ab3b3330a', 'edit_of': '72fe11d1-edfe-4741-9292-4297e39e9a78',
                   'prompt': 'Cut a left and a right doorway through the rotunda ring into the gallery and the vehicle hall; keep everything else.'},
    'props': {'asset_id': '72b109df-0c32-418f-8491-3d8d921e3d98', 'model': 'gpt-image-2.5-flare', 'resolution': '2K',
              'prompt': '4x4 top-down museum exhibit props, intact/broken pairs: statue, rifle case, vase, painting panel, alarm panel, '
                        'laser tripwire post, velvet rope, plasma weapon case.'},
}
(OUT / 'prompts.json').write_text(json.dumps(prompts, indent=1) + '\n')
(OUT / 'manifest.json').write_text(json.dumps(frames, indent=1) + '\n')
(OUT / 'manifest.js').write_text('window.TD_MUSEUM_ART=' + json.dumps(frames, separators=(',', ':')) + ';\n')
print(len(frames), 'frames')
