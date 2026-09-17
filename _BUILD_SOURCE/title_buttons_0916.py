#!/usr/bin/env python3
"""
title_buttons_0916.py - THE TITLE BUTTONS, REGENERATED AS ONE SHEET.

    python3 _BUILD_SOURCE/title_buttons_0916.py <sheet.png> [--check]

Mike, 0916: "Regenerate all my other buttons here to match the current style of Bullets of Fury and
proper reference of ships and pilots please. The help button also is too large compared to the rest."

⚠ "TOO LARGE" WAS AN ASPECT PROBLEM, NOT A SIZE ONE. `titleMenuLayout` measures ONE w x h from the
first ready plate and draws every button at it, so a plate whose native aspect differs is stretched
into that box. Measured: the authored bars are 1090x222-233, i.e. **4.7-4.9:1**, and `btn_help` is
**446x112 = 3.98:1** - 20% squatter, so it was drawn 20% taller than every bar around it. Nothing
about it was "big"; it was the wrong shape. All six are now cut from one sheet and share an aspect
by construction.

Generated as ONE sheet for the same reason the medals were: six separate jobs can only approximate
a shared frame, light source and lettering weight. Two references were passed - the authored buttons
for the frame language, and a sheet of the game's own PILOT SHIPS so the NEW GAME emblem is our
aircraft rather than a stock jet.

⚠ THE ACHIEVEMENTS BAR IS CUT FROM THE SAME SHEET. It was generated on its own first, at 5.17:1,
and the moment the other six landed at 6.1:1 it became the odd one out - the same fault, one button
over. Seven bars from one job share the aspect by construction.

⚠ SLICED ON THE SHEET'S OWN ALPHA GUTTERS, and it refuses unless it finds exactly seven islands whose
aspects agree - the 0907h trap ("the grid is a starting assumption, not a fact") and the 0906k
slicer that wrote one height for every frame.

⚠ THEY SHIP UNDER NEW KEYS. `btn_newgame` and friends are ATLAS CELLS, and CLAUDE.md records that
cells are checked before the loose-file cache (0912m), so registering a loose file under the same
key would be ignored. The new plates are `btn_<name>_0916` and MENU_KEYS points at them; the atlas
rows stay for the pause menu, which uses its own.
"""
import os, sys, argparse
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
DST = os.path.join(ROOT, 'assets', 'game', 'ui', 'title_0916')
OUT = os.path.join(ROOT, 'docs', 'proofs', 'awards_0916')
NAMES = ['newgame', 'password', 'options', 'help', 'achievements', 'credits', 'exit']


def islands(im, min_px=2000):
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
    isl = sorted(islands(im), key=lambda b: b[1])
    print('%s: %d islands' % (os.path.basename(a.sheet), len(isl)))
    assert len(isl) == len(NAMES), 'expected %d bars, found %d' % (len(NAMES), len(isl))
    asp = [(b[2] - b[0]) / float(b[3] - b[1]) for b in isl]
    print('  aspects: %s' % ' '.join('%.2f' % q for q in asp))
    assert max(asp) - min(asp) < 0.6, 'the bars do not share an aspect: %s' % asp

    cuts = [(n, im.crop((b[0], b[1], b[2], b[3]))) for n, b in zip(NAMES, isl)]
    for n, c in cuts:
        print('  %-9s %dx%d  aspect %.2f' % (n, c.width, c.height, c.width / c.height))

    os.makedirs(OUT, exist_ok=True)
    if a.check:
        Z = 2; pad = 8
        W = max(c.width for _, c in cuts) * Z + pad * 2
        H = sum(c.height * Z + pad + 12 for _, c in cuts) + pad
        card = Image.new('RGBA', (W, H), (28, 30, 38, 255))
        from PIL import ImageDraw
        d = ImageDraw.Draw(card); y = pad
        for n, c in cuts:
            card.alpha_composite(c.resize((c.width * Z, c.height * Z), Image.NEAREST), (pad, y))
            d.text((pad + 4, y + c.height * Z + 1), '%s %dx%d %.2f' % (n, c.width, c.height, c.width / c.height),
                   fill=(255, 220, 150, 255))
            y += c.height * Z + pad + 12
        p = os.path.join(OUT, '13_title_buttons.png')
        card.save(p); print('--check: wrote', os.path.relpath(p, ROOT))
        return

    os.makedirs(DST, exist_ok=True)
    for n, c in cuts:
        p = os.path.join(DST, 'btn_%s.png' % n)
        c.save(p)
        print('wrote', os.path.relpath(p, ROOT))


if __name__ == '__main__':
    main()
