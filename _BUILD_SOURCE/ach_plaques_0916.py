#!/usr/bin/env python3
"""
ach_plaques_0916.py - THE ACHIEVEMENT PLAQUES: nine medals, generated as one sheet, sliced apart.

    python3 _BUILD_SOURCE/ach_plaques_0916.py <sheet.png> [--check]

Mike, 0916, on the toast's empty socket: "now get us the proper icons for each achievement
unlocked."

Generated as ONE 3x3 sheet rather than nine jobs - the medals then share a light source, a bevel
weight and a laurel treatment by construction, which nine separate jobs would only approximate.

⚠ AND THE FIRST SHEET CAME BACK WITH MY OWN COLOUR WORDS BAKED INTO THE MEDALS. The prompt named
each medal by colour ("a GOLD medal with a fighter jet"), and one of the two variations lettered
GOLD, BRONZE, BLUE, GREEN, RED, DEEP RED, SILVER, PLATINUM across the discs and ribbons. Read the
sheet before slicing it: a colour word in a prompt is a label the model may choose to draw.

⚠ SLICED ON THE SHEET'S OWN ALPHA GUTTERS, NOT ON AN ASSUMED GRID. CLAUDE.md records the 0907h
trap - "the 8x4 grid is a starting assumption, not a fact" - and the 0906k slicer that wrote ONE
height for every frame. Here the medals are found as connected alpha islands and then ordered by
row and column, so a sheet that comes back 3x3 at slightly different spacing still slices correctly
and a sheet that does NOT hold nine islands fails loudly instead of quietly cutting one in half.
"""
import os, sys, argparse
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
DST = os.path.join(ROOT, 'assets', 'game', 'ui', 'awards_0916')
OUT = os.path.join(ROOT, 'docs', 'proofs', 'awards_0916')

# reading order on the sheet -> what each medal is for
NAMES = ['campaign_clear', 'stage_clear', 'stage_nodeath',
         'stage_nomissile', 'boss_hard', 'boss_furious',
         'boss_speed', 'weapon_max', 'run_no_continue']


def islands(im, min_px=400):
    w, h = im.size
    px = im.load()
    seen = [[False] * h for _ in range(w)]
    out = []
    for sy in range(h):
        for sx in range(w):
            if seen[sx][sy] or px[sx, sy][3] <= 16:
                continue
            st = [(sx, sy)]
            n = 0
            x0 = x1 = sx
            y0 = y1 = sy
            while st:
                x, y = st.pop()
                if x < 0 or y < 0 or x >= w or y >= h or seen[x][y] or px[x, y][3] <= 16:
                    continue
                seen[x][y] = True
                n += 1
                x0, x1 = min(x0, x), max(x1, x)
                y0, y1 = min(y0, y), max(y1, y)
                st += [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1),
                       (x + 1, y + 1), (x - 1, y - 1), (x + 1, y - 1), (x - 1, y + 1)]
            if n >= min_px:
                out.append((x0, y0, x1 + 1, y1 + 1, n))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('sheet')
    ap.add_argument('--check', action='store_true')
    a = ap.parse_args()
    im = Image.open(a.sheet).convert('RGBA')
    isl = islands(im)
    print('%s: %d islands' % (os.path.basename(a.sheet), len(isl)))
    assert len(isl) == 9, 'expected nine medals, found %d - read the sheet before slicing it' % len(isl)

    # order by row then column, from the islands' own centres
    cent = [((b[1] + b[3]) / 2.0, (b[0] + b[2]) / 2.0, b) for b in isl]
    cent.sort(key=lambda q: q[0])
    rows = [cent[0:3], cent[3:6], cent[6:9]]
    ordered = []
    for r in rows:
        r.sort(key=lambda q: q[1])
        ordered += [q[2] for q in r]

    cuts = []
    for name, b in zip(NAMES, ordered):
        cuts.append((name, im.crop((b[0], b[1], b[2], b[3]))))
        print('  %-16s %dx%d  %d px' % (name, b[2] - b[0], b[3] - b[1], b[4]))

    os.makedirs(OUT, exist_ok=True)
    if a.check:
        Z = 3; pad = 8
        W = pad + len(cuts) * (max(c.width for _, c in cuts) * Z + pad)
        H = max(c.height for _, c in cuts) * Z + pad * 2 + 14
        card = Image.new('RGBA', (W, H), (28, 30, 38, 255))
        from PIL import ImageDraw
        d = ImageDraw.Draw(card); x = pad
        for n, c in cuts:
            card.alpha_composite(c.resize((c.width * Z, c.height * Z), Image.NEAREST), (x, pad))
            d.text((x + 2, pad + c.height * Z + 2), n[:14], fill=(255, 220, 150, 255))
            x += max(c.width for _, c in cuts) * Z + pad
        p = os.path.join(OUT, '10_plaques.png')
        card.save(p); print('--check: wrote', os.path.relpath(p, ROOT))
        return

    os.makedirs(DST, exist_ok=True)
    for n, c in cuts:
        p = os.path.join(DST, 'ach_%s.png' % n)
        c.save(p)
        print('wrote', os.path.relpath(p, ROOT))


if __name__ == '__main__':
    main()
