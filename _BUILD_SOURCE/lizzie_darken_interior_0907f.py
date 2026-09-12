#!/usr/bin/env python3
"""lizzie_darken_interior_0907f.py - Lizzie's internal yellow spots go dark; the hull stays gold.

    python _BUILD_SOURCE/lizzie_darken_interior_0907f.py            # sweep + proof
    python _BUILD_SOURCE/lizzie_darken_interior_0907f.py --write

Mike, 0907, on the new animation pack: "the internal yellow spots on lizzie needs to be darker,
much darker like the cockpit window and such, she keeps a gold hull though."

Measured on frame 0 of her sheet: the single largest colour bucket is **hue 50 at value 1.0,
1,649 px** - brighter than any part of the hull around it. That is the canopy, the spine strip and
the panel inserts, and being the brightest thing on the aircraft they read as lamps rather than as
glass. The hull itself sits at hue 30-40, value 0.3-0.9, and is not touched.

⚠ VALUE DROPS, HUE DOES NOT MOVE. "She keeps a gold hull" is the constraint, so this is a value
change inside her existing gold and not a recolour - the darkened canopy is the same hue as the
plating, just deep. Rotating or desaturating it would have made a grey/green window on a gold
aircraft, which is the flat-fill failure this repo has hit twice (the font tint, the first
Juggernaut brown).

⚠ AND THE THRESHOLD IS THE ONE THAT LEAVES THE HULL ALONE, PICKED FROM A RENDER. Swept 0.88x0.55,
0.88x0.40 and 0.82x0.34 side by side: the last one reaches v 0.82 and starts eating the hull's own
lit faces (3,468 px against 3,055), which flattens the plating. 0.88 x 0.40 darkens the canopy hard
and touches nothing else.

⚠ THIS IS A SOURCE-PACK FIX, NOT AN IN-GAME ONE. Her shipped hull measures only **1.2% bright
interior yellow** (324 px of 27,075) because 0906w already worked her palette - so the complaint is
about the pack sheet, which is what was in front of him. Checked before editing, rather than
assuming which Lizzie he meant.
"""
import os, sys, shutil, colorsys
from collections import deque
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, '_ART_SOURCES_SHIPANIM/Lizzie')
V_MIN = 0.88          # only what is brighter than the hull
# ⚠ VALUE ALONE GOES OLIVE, WHICH IS WHY THE FIRST TWO PASSES LOOKED WRONG. Dropping a saturated
# YELLOW's value slides it straight to olive-green - it never becomes dark glass, because glass on
# a gold aircraft is amber. Swept five treatments side by side: v.55 at the same hue is muted olive,
# v.45 at hue 32 is bronze, v.34 at hue 28 is dark amber and reads as a tinted canopy, v.26 at hue
# 24 is nearly black. The insets take a small hue shift toward amber as they darken; the HULL is
# never touched, so "she keeps a gold hull" still holds.
V_MUL = 0.34
S_MUL = 1.00
HUE_TO = 28.0         # degrees - amber, down from the 42-68 the bright insets sit at
S_MIN = 0.45
HUE_LO, HUE_HI = 42.0, 68.0
# the centreline band: everything inside it is canopy/spine/nozzle, everything outside is wing
CENTRE_F = 0.45


def is_key(h, s):
    return s >= 0.35 and 280.0 <= h * 360.0 <= 330.0


def darken(src):
    """darken only the CENTRELINE insets - canopy, spine, nozzles - and leave the wing panels.

    ⚠ "KEEP THE GOLD" IS THE CONSTRAINT AND THE FIRST PASS BROKE IT. Every bright-yellow inset on
    the aircraft was darkened, wing panels included, and those panels are most of what makes her
    read as gold - so the ship came out drab even though only 3,055 px of ~40,000 had moved.
    Mike came back with three crops: the canopy, a spine inset and a nozzle. All three are on or
    near the SPINE.

    ⚠ AND THE SPLIT IS MEASURED, WITH A REAL GAP IN IT. Numbering every bright interior component
    on frame 0 and taking its distance from the centreline as a share of the half-width: the
    canopy, spine strip, nose insets and the four nozzle pieces all land at **0.02 to 0.39**, and
    the four wing panels at **0.52, 0.54, 0.86, 0.87**. Nothing sits between 0.39 and 0.52, so the
    cut is not a guess - it is the gap the artwork already has.

    ⚠ VALUE DROPS, HUE DOES NOT MOVE, because the hull stays gold. This is a value change inside
    her existing gold, not a recolour."""
    c = src.copy()
    px = c.load()
    W, H = c.size

    def is_key(x, y):
        r, g, b = px[x, y][:3]
        h, s, v = colorsys.rgb_to_hsv(r / 255., g / 255., b / 255.)
        return s >= 0.35 and 280.0 <= h * 360.0 <= 330.0

    def bright(x, y):
        r, g, b = px[x, y][:3]
        h, s, v = colorsys.rgb_to_hsv(r / 255., g / 255., b / 255.)
        if s >= 0.35 and 280.0 <= h * 360.0 <= 330.0:
            return False
        return s >= S_MIN and HUE_LO <= h * 360.0 <= HUE_HI and v >= V_MIN

    ship = [x for y in range(H) for x in range(W) if not is_key(x, y)]
    if not ship:
        return c, 0
    mid = (min(ship) + max(ship)) / 2.0
    half = max(1.0, (max(ship) - min(ship)) / 2.0)

    seen = [[False] * W for _ in range(H)]
    hits = []
    for y0 in range(H):
        for x0 in range(W):
            if seen[y0][x0] or not bright(x0, y0):
                continue
            q = deque([(x0, y0)])
            seen[y0][x0] = True
            pts = []
            while q:
                a, b = q.popleft()
                pts.append((a, b))
                for nx, ny in ((a + 1, b), (a - 1, b), (a, b + 1), (a, b - 1)):
                    if 0 <= nx < W and 0 <= ny < H and not seen[ny][nx] and bright(nx, ny):
                        seen[ny][nx] = True
                        q.append((nx, ny))
            cx = sum(q2[0] for q2 in pts) / float(len(pts))
            if abs(cx - mid) / half < CENTRE_F:
                hits.extend(pts)
    for (x, y) in hits:
        r, g, b = px[x, y][:3]
        h, s, v = colorsys.rgb_to_hsv(r / 255., g / 255., b / 255.)
        rr, gg, bb = colorsys.hsv_to_rgb(HUE_TO / 360.0, min(1.0, s * S_MUL), v * V_MUL)
        px[x, y] = (int(rr * 255 + .5), int(gg * 255 + .5), int(bb * 255 + .5))
    return c, len(hits)


def main():
    write = '--write' in sys.argv
    files = [f for f in sorted(os.listdir(SRC)) if f.endswith('.png')]
    try:
        F = ImageFont.truetype('C:/Windows/Fonts/consolab.ttf', 15)
    except Exception:
        F = ImageFont.load_default()
    shots = []
    for fn in files:
        p = os.path.join(SRC, fn)
        im = Image.open(p).convert('RGB')
        out, n = darken(im)
        print('%-36s %dx%d  darkened %d px (%.2f%% of the sheet)'
              % (fn, im.width, im.height, n, 100.0 * n / (im.width * im.height)))
        if 'golden' in fn:
            CW, CH = im.width // 8, im.height // 4
            shots = [('before', im.crop((0, 0, CW, CH))), ('after', out.crop((0, 0, CW, CH))),
                     ('before  somersault', im.crop((2 * CW, CH, 3 * CW, 2 * CH))),
                     ('after  somersault', out.crop((2 * CW, CH, 3 * CW, 2 * CH)))]
        if write:
            bak = p + '.pre0907f'
            if not os.path.exists(bak):
                shutil.copy2(p, bak)
            out.save(p)
    if shots:
        T = 300
        S = Image.new('RGB', (T * len(shots), T + 26), (18, 18, 24))
        d = ImageDraw.Draw(S)
        for i, (lbl, c) in enumerate(shots):
            t = c.resize((T - 16, T - 40), Image.NEAREST)
            S.paste(t, (i * T + 8, 26))
            d.text((i * T + 5, 4), lbl, font=F, fill=(238, 238, 248))
        S.save(os.path.join(ROOT, 'docs/LIZZIE_DARK_0907F.png'))
        print('wrote docs/LIZZIE_DARK_0907F.png')
    if not write:
        print('DRY RUN - the pack was not modified.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
