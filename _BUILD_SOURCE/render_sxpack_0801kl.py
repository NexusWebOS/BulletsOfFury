#!/usr/bin/env python3
"""
render_sxpack_0801kl.py — replay probe_sxpack_0801kl.js's recorded draw calls.

The probe records (key, x, y, w, h, alpha) from the SHIPPING sxPackDraw. This
replays them with the real PNGs, so the picture below is what the game's own
draw path produces, not an offline reimplementation of it.
"""
import json, os, re, sys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAN = json.loads(re.search(r'window\.BOFX=([\s\S]*?\});',
                           open(os.path.join(ROOT, 'assets/manifest.js')).read()).group(1))['img']
BG = (22, 26, 36, 255)


def render(calls, W=480, H=330, ox=-115, oy=-25):
    cv = Image.new('RGBA', (W, H), BG)
    for c in calls:
        k = c.get('key')
        if not k or k not in MAN:
            continue
        p = os.path.join(ROOT, MAN[k])
        if not os.path.exists(p):
            continue
        im = Image.open(p).convert('RGBA')
        w, h = max(1, int(round(c['w']))), max(1, int(round(c['h'])))
        im = im.resize((w, h), Image.NEAREST)
        a = float(c.get('alpha', 1))
        if a < 1:
            al = im.split()[3].point(lambda v: int(v * a))
            im.putalpha(al)
        cv.alpha_composite(im, (int(round(c['x'] + ox)), int(round(c['y'] + oy))))
    return cv


def main():
    data = json.load(open(sys.argv[1] if len(sys.argv) > 1 else '/tmp/sxpack.json'))
    frames = data['frames']
    order = ['intact', 'damaged_all', 'critical_all', 'turrets_blown']
    labels = ['intact', 'damaged + smoke', 'critical + smoke', 'turrets blown off']
    S = 2
    tiles = [render(frames[k]) for k in order if k in frames]
    W, H = tiles[0].size
    sheet = Image.new('RGBA', (W * len(tiles) * S, H * S), BG)
    for i, t in enumerate(tiles):
        sheet.paste(t.resize((W * S, H * S), Image.NEAREST), (i * W * S, 0))
    out = '/tmp/sxpack_proof.png'
    sheet.save(out)
    print('wrote', out, sheet.size, '|', ' · '.join(labels))


if __name__ == '__main__':
    main()
