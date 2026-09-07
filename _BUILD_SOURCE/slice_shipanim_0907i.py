#!/usr/bin/env python3
"""slice_shipanim_0907i.py - cut a pack sheet into frames and work out what each one IS.

    python _BUILD_SOURCE/slice_shipanim_0907i.py juggernaut
    python _BUILD_SOURCE/slice_shipanim_0907i.py juggernaut --write

⚠ THE PACK'S OWN README SAYS NOT TO TRUST THE LAYOUT: "known issues include repeated angles,
underside/design drift, and inconsistent rotation order." So the 8x4 grid is where the cells are,
not what they contain. Every cell is MEASURED and identified from its own pixels, and the row
labels are only used to break ties.

WHAT IDENTIFIES A FRAME
  roll magnitude   ink width / the level frame's width = |cos(roll)|, which inverts to an angle.
                   That is the same geometry the deriver used, run backwards on authored art.
  roll direction   the fuselage's bright side. Rolling right shows the right side-wall, so the
                   ink's brightness centroid sits right of its own bbox centre. THIS IS THE WHOLE
                   REASON THE PACK EXISTS - a derived frame has no such asymmetry (0907b).
  top or belly     a somersault/roll past 90 degrees shows the underside. Scored against the
                   ship's own top view by silhouette IoU after normalising width.

⚠ AND THE KEY COLOUR IS READ FROM EACH SHEET'S OWN CORNER, NOT ASSUMED. Six sheets key on magenta
and FALVA'S KEYS ON CYAN, because her aircraft is pink and magenta would collide with her hull
(0907h). Hardcoding either one silently ruins the other.
"""
import os, sys, json, math, colorsys
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, '_ART_SOURCES_SHIPANIM')
OUT = os.path.join(ROOT, 'assets/game/ships_sliced')
COLS, ROWS = 8, 4
ROW_MEANING = ['barrel roll', 'somersault', 'banked turn', 'pivot']

SHEETS = {
    'axel': 'Axel/axel-latest-source.png',
    'cole': 'Cole/cole-latest-source.png',
    'decker': 'Decker/decker-latest-source.png',
    'falva': 'Falva/falva-cyan-latest-source.png',
    'juggernaut': 'Juggernaut/juggernaut-no-thrusters-source.png',
    'lizzie': 'Lizzie/lizzie-golden-latest-source.png',
    'yuri': 'Yuri/yuri-latest-source.png',
}


def sheet_key(im):
    """the background colour, taken from this sheet's own corners"""
    px = im.load()
    c = px[2, 2]
    return c[:3]


def dekey(cell, key, tol=40):
    """punch the key to alpha. ⚠ a BORDER FLOOD, not a colour sweep - enclosed background inside
    the airframe (between a wing and the fuselage) must go too, and a sweep would also eat any
    hull pixel that happens to match."""
    out = cell.convert('RGBA')
    W, H = out.size
    px = out.load()

    def isk(x, y):
        p = px[x, y]
        return (abs(p[0] - key[0]) <= tol and abs(p[1] - key[1]) <= tol and abs(p[2] - key[2]) <= tol)

    from collections import deque
    q = deque()
    seen = [[False] * W for _ in range(H)]
    for x in range(W):
        for y in (0, H - 1):
            if not seen[y][x] and isk(x, y):
                seen[y][x] = True; q.append((x, y))
    for y in range(H):
        for x in (0, W - 1):
            if not seen[y][x] and isk(x, y):
                seen[y][x] = True; q.append((x, y))
    while q:
        x, y = q.popleft()
        px[x, y] = (0, 0, 0, 0)
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < W and 0 <= ny < H and not seen[ny][nx] and isk(nx, ny):
                seen[ny][nx] = True; q.append((nx, ny))
    return out


def ink(im):
    b = im.getbbox()
    return im.crop(b) if b else im


def bright_bias(im):
    """where the LIT side is, as a fraction of half-width from the ink's own centre.
    positive = the right side is brighter = rolled right."""
    px = im.load()
    W, H = im.size
    tw = tx = 0.0
    for y in range(H):
        for x in range(W):
            p = px[x, y]
            if p[3] < 40:
                continue
            v = max(p[0], p[1], p[2]) / 255.0
            w = v ** 3
            tw += w; tx += w * x
    if tw <= 0:
        return 0.0
    return ((tx / tw) - (W - 1) / 2.0) / max(1.0, W / 2.0)


def iou(a, b):
    """silhouette overlap after fitting b to a's box - is this the same face of the ship?"""
    if a.size != b.size:
        b = b.resize(a.size, Image.NEAREST)
    pa, pb = a.load(), b.load()
    inter = union = 0
    for y in range(a.height):
        for x in range(a.width):
            A = pa[x, y][3] > 40
            B = pb[x, y][3] > 40
            if A or B:
                union += 1
                if A and B:
                    inter += 1
    return inter / float(union) if union else 0.0


def main():
    if len(sys.argv) < 2:
        print(__doc__); return 2
    pilot = sys.argv[1]
    write = '--write' in sys.argv
    if pilot not in SHEETS:
        print('unknown ship %r' % pilot); return 1
    im = Image.open(os.path.join(SRC, SHEETS[pilot])).convert('RGB')
    key = sheet_key(im)
    CW, CH = im.width // COLS, im.height // ROWS
    print('%s  sheet %dx%d  cell %dx%d  key rgb%s' % (pilot, im.width, im.height, CW, CH, key))

    cells = {}
    for r in range(ROWS):
        for c in range(COLS):
            raw = im.crop((c * CW, r * CH, (c + 1) * CW, (r + 1) * CH))
            cells[(r, c)] = ink(dekey(raw, key))

    level = cells[(0, 0)]
    LW, LH = level.width, level.height
    print('level frame (row0 col0) ink %dx%d' % (LW, LH))
    print()
    print('%-4s %-13s %-10s %-8s %-8s %-7s %s'
          % ('cell', 'row means', 'ink', 'w/level', 'roll deg', 'lit side', 'same face as level (IoU)'))
    info = {}
    for r in range(ROWS):
        for c in range(COLS):
            im2 = cells[(r, c)]
            wr = im2.width / float(LW)
            ang = math.degrees(math.acos(max(0.0, min(1.0, wr))))
            bias = bright_bias(im2)
            ov = iou(level, im2)
            info[(r, c)] = dict(w=im2.width, h=im2.height, wr=wr, ang=ang, bias=bias, iou=ov)
            print('%-4s %-13s %-10s %-8.3f %-8.1f %-7s %.3f'
                  % ('r%dc%d' % (r, c), ROW_MEANING[r], '%dx%d' % (im2.width, im2.height),
                     wr, ang, ('right' if bias > 0.012 else ('left' if bias < -0.012 else '-')), ov))
        print()

    # repeated frames, which the README warns about
    print('REPEATS - cells whose ink is the same size AND overlaps above 0.99:')
    keys = sorted(info)
    dup = 0
    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            a, b = keys[i], keys[j]
            if info[a]['w'] == info[b]['w'] and info[a]['h'] == info[b]['h']:
                if iou(cells[a], cells[b]) > 0.99:
                    print('   r%dc%d == r%dc%d' % (a[0], a[1], b[0], b[1])); dup += 1
    if not dup:
        print('   none')

    if write:
        d = os.path.join(OUT, pilot)
        os.makedirs(d, exist_ok=True)
        for (r, c), im2 in cells.items():
            im2.save(os.path.join(d, 'r%dc%d.png' % (r, c)))
        json.dump({'%d,%d' % k: v for k, v in info.items()},
                  open(os.path.join(d, '_measured.json'), 'w'), indent=1)
        print()
        print('wrote 32 de-keyed cells to assets/game/ships_sliced/%s/' % pilot)
    return 0


if __name__ == '__main__':
    sys.exit(main())
