#!/usr/bin/env python3
"""
flame_mask_0912n.py - FIND THE PAINTED FLAME IN THE CURRENT SHIP PLATES.

    python3 _BUILD_SOURCE/flame_mask_0912n.py --proof /tmp/flamemask.png

Mike, 0912: "re-bake against the current plates."

⚠ THE OLD ROUTE IS GONE, AND SO IS THE ONE THIS FILE'S HISTORY RECOMMENDS.
0906s recovered the flame by DIFFING the baked plate against a pre-bake backup. 0907u used the
source pack's THROTTLE PAIR - each pose shipped twice, and the hull is registered between them.
Neither is available here:

  - ship_<pilot>_nf is an ALIAS OF THE BASE on all nine (identical rects, measured), so
    base - _nf is zero. That is 0907u's "_nf MUST ACTUALLY BE FLAMELESS" bug, reintroduced by
    the 0909 per-pilot re-pack.
  - the 0909 pack has no phase art and no throttle pair; its own build script says so and
    deliberately deleted _g1/_g2 rather than faking them.

⚠ AND 0907u PROVED A COLOUR DETECTOR CANNOT DO THIS. Five were tried and each broke a ship the
previous one fixed: Cole's exhaust is GREEN, Freezer's and Maverick's CYAN, while Yuri's hull is
RED and Falva's PINK. No window in colour space holds every flame and excludes every hull.

SO THE SIGNAL HERE IS GEOMETRY FIRST, BRIGHTNESS SECOND - and that ordering is the whole idea.
Rendering the nine tails at 3x (rule 1, before writing a line of this) shows the plumes plainly:
they are the ink that PROTRUDES BELOW THE METAL, they are the lowest ink on the fuselage, and
inside that small region the flame is unambiguously the bright part whatever its hue. The hull
colours that defeated every previous detector are elsewhere on the airframe and never get
considered.

    1. find the BELL COLUMNS - the 0906r detector, columns whose ink reaches within a few px of
       the hull's lowest row. Validated there against Juggernaut's authored flames to 0.2px.
    2. in those columns only, walk UP from the lowest ink while the pixel stays bright.
       The dark lip of the bell stops the walk by itself.

⚠ VALIDATE ON JUGGERNAUT BEFORE TRUSTING IT ANYWHERE. He is the one pilot whose exhaust was
painted into open bells and measured by 0906r (centres at ink x 73.0 / 129.5, width 18). A metric
that has not reproduced the known case is not evidence about the unknown ones.
"""
import os, sys, io, re, json, argparse
import numpy as np
from PIL import Image, ImageDraw

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
SHEETS = os.path.join(ROOT, 'assets', 'game', 'atlas', 'ships')
PILOTS = ['axel', 'cole', 'decker', 'falva', 'freezer', 'juggernaut', 'lizzie', 'maverick', 'yuri']

DEEP_PX = 6        # a bell column's ink must reach within this of the hull's lowest row
V_FLOOR = 0.42     # the walk up the plume stops below this value
S_OR_V = 0.30      # ...unless the pixel is near-white (a plume core is desaturated AND bright)


def ships_table():
    s = io.open(os.path.join(ROOT, 'assets', 'manifest.js'), encoding='utf-8', newline='').read()
    return json.loads(re.search(r'window\.BOFX=(\{.*?\});', s, re.S).group(1))['ships']


def cell(pilot, key, tab=None):
    tab = tab or ships_table()
    x, y, w, h, ox, oy, cw, ch = tab[key]
    im = Image.open(os.path.join(SHEETS, 'ship_%s.png' % pilot)).convert('RGBA')
    return im.crop((x, y, x + w, y + h))


def hsv(arr):
    """arr float RGB 0..1 -> H,S,V planes."""
    r, g, b = arr[..., 0], arr[..., 1], arr[..., 2]
    mx = arr[..., :3].max(axis=-1); mn = arr[..., :3].min(axis=-1)
    v = mx
    s = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0)
    return s, v


def flame_mask(img):
    """Boolean mask of the painted plume. See the module note for why it is geometry-first."""
    a = np.asarray(img).astype(np.float64) / 255.0
    al = a[..., 3]
    ink = al > 0.35
    H, W = ink.shape
    if not ink.any():
        return np.zeros_like(ink), {}

    sat, val = hsv(a)

    # --- 1. the bell columns: ink that reaches near the hull's lowest row -------------------
    low = np.full(W, -1)
    for x in range(W):
        col = np.where(ink[:, x])[0]
        if len(col):
            low[x] = col[-1]
    deepest = low.max()
    bell = (low >= deepest - DEEP_PX) & (low >= 0)

    # --- 2. walk UP from the lowest ink while the pixel stays bright ------------------------
    m = np.zeros_like(ink)
    for x in np.where(bell)[0]:
        y = low[x]
        while y >= 0 and ink[y, x]:
            bright = val[y, x] >= V_FLOOR and (sat[y, x] >= S_OR_V or val[y, x] >= 0.80)
            if not bright:
                break
            m[y, x] = True
            y -= 1

    info = {'cols': int(bell.sum()), 'px': int(m.sum()), 'ink': int(ink.sum()),
            'share': round(float(m.sum()) / max(1, int(ink.sum())), 4)}
    if m.any():
        xs = np.where(m.any(axis=0))[0]
        info['x0'], info['x1'] = int(xs[0]), int(xs[-1])
        # centroids of each connected run of marked columns - the bell CENTRES, for validation
        runs, cur = [], []
        for x in range(W):
            if m[:, x].any():
                cur.append(x)
            elif cur:
                runs.append(cur); cur = []
        if cur:
            runs.append(cur)
        info['centres'] = [round(float(np.mean(r)), 1) for r in runs]
        info['widths'] = [len(r) for r in runs]
    return m, info


def proof(path):
    tab = ships_table()
    tiles = []
    for p in PILOTS:
        img = cell(p, 'ship_' + p, tab)
        m, info = flame_mask(img)
        Z = 3
        base = Image.new('RGBA', img.size, (10, 14, 20, 255))
        base.paste(img, (0, 0), img)           # ⚠ composite, never convert('RGB') - 0906v
        over = base.copy()
        px = np.asarray(over).copy()
        px[m] = [255, 40, 120, 255]            # the mask, in a colour no ship wears
        over = Image.fromarray(px)
        strip = Image.new('RGBA', (img.width * 2 + 6, img.height), (10, 14, 20, 255))
        strip.paste(base, (0, 0)); strip.paste(over, (img.width + 6, 0))
        strip = strip.resize((strip.width * Z, strip.height * Z), Image.NEAREST)
        tiles.append((p, strip, info))

    W = max(t.width for _, t, _ in tiles); H = max(t.height for _, t, _ in tiles)
    sheet = Image.new('RGBA', (W * 3 + 40, (H + 34) * 3 + 30), (7, 12, 18, 255))
    d = ImageDraw.Draw(sheet)
    for i, (p, t, info) in enumerate(tiles):
        cx = (i % 3) * (W + 14) + 8; cy = (i // 3) * (H + 34) + 24
        sheet.paste(t, (cx, cy))
        d.text((cx, cy - 20), '%s   %d px  (%.1f%% of ink)  centres %s  widths %s'
               % (p, info.get('px', 0), info.get('share', 0) * 100,
                  info.get('centres'), info.get('widths')), fill=(124, 245, 255, 255))
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    sheet.save(path)
    print('wrote %s' % path)
    for p, _, info in tiles:
        print('  %-11s %s' % (p, info))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--proof', default='/tmp/flamemask.png')
    a = ap.parse_args()
    proof(a.proof)
    return 0


if __name__ == '__main__':
    sys.exit(main())
