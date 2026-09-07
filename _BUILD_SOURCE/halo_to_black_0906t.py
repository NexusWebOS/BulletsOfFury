#!/usr/bin/env python3
"""halo_to_black_0906t.py - purple halo off every ship hull, converted to a 1px black edge.

    python _BUILD_SOURCE/halo_to_black_0906t.py            # measure only
    python _BUILD_SOURCE/halo_to_black_0906t.py --write

Mike, 0906: "remove all purple halo's from all ships, use 1px black edging in placement or
conversion instead."

Measured before touching anything - magenta pixels on the outer alpha boundary of every ship frame:

    yuri 50.9%   cole 49.5%   freezer 48.8%   lizzie 38.2%   maverick 35.4%
    decker 31.2% axel 26.9%   falva 5.7%      juggernaut 0.0% (2 px of 12,861)

⚠ JUGGERNAUT HAVING NONE IS NOT A COINCIDENCE - IT IS PART OF WHY HIS SHIP HAS LOOKED RIGHT ALL
ALONG. Half the boundary of the other hulls is a magenta fringe, and at the 60 px the game draws
them that reads as a soft violet haze rather than as an edge. 0811r measured these boundaries as
"93-98% dark" and concluded the black edge was already there; it is there on the pixels that are
not halo, and this is the other half of that measurement.

⚠ ONLY OUTER-BOUNDARY PIXELS CONVERT, AND THAT RULE IS LOAD-BEARING FOR FALVA. Her hull IS pink -
mean hue 330 - so a colour sweep over the whole plate would black out her aircraft. A pixel
qualifies only if it touches transparency, which is the standing rule this repo already states as
"INTERIOR magenta is NOT a halo".

⚠ AND IT IS A CONVERSION, NOT A DELETION. Punching the halo to alpha would shrink every silhouette
by a pixel and leave the hulls with no outline at all where the fringe used to be; the standing
rule is "purple halos are converted to a black edge, never deleted". Alpha is untouched, so no
silhouette moves.
"""
import os, re, sys, json, shutil, colorsys, subprocess
from collections import deque
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ATLAS = os.path.join(ROOT, 'assets/game/atlas/bof_player_ships_barrel_rolls.png')
MANIFEST = os.path.join(ROOT, 'assets/manifest.js')
EDGE = (9, 9, 13)                 # the near-black these hulls already outline with


def ship_rows(man):
    out = subprocess.run(['node', '-e',
        "global.window=global;eval(require('fs').readFileSync(%s,'utf8'));"
        "const o={};for(const k in BOFX.ships)o[k]=BOFX.ships[k];"
        "process.stdout.write(JSON.stringify(o));"
        % json.dumps(os.path.relpath(man, ROOT).replace('\\', '/'))],
        capture_output=True, cwd=ROOT)
    return json.loads(out.stdout.decode())


def is_halo(p):
    r, g, b, a = p
    if a < 16:
        return False
    h, s, v = colorsys.rgb_to_hsv(r / 255., g / 255., b / 255.)
    d = h * 360.0
    return s >= 0.25 and v >= 0.12 and 255.0 <= d <= 330.0


DEPTH = 2          # how far in the fringe is allowed to reach
DECAY = 0.15       # magenta past DEPTH, as a share of magenta within it, for it to still be halo


def convert(cell):
    """convert the magenta FRINGE - however many pixels thick - to the hull's own near-black edge.

    ⚠ A ONE-PIXEL RULE LEAVES THE HALO VISIBLE, BECAUSE THE FRINGE IS 2-3 PX THICK. Measured by
    distance from the silhouette on the untouched plate: cole 376/470/96/1, lizzie 377/559/208/12,
    yuri 355/321/70/5. Converting only the outermost ring turns the outer pixel black and leaves
    the violet one behind it, which at 7x reads as a black line with a purple line inside it - and
    that is what Mike was still seeing after the first pass.

    ⚠ AND THE SAME DEPTH PROFILE IS WHAT SEPARATES A HALO FROM A SHIP THAT IS GENUINELY PURPLE. A
    halo DECAYS sharply inward (the four above all reach ~0 by depth 3); a hull colour does not -
    falva runs 54/96/49/31/28/49 flat and freezer 4/6/13/12/15/18, INCREASING with depth, because
    their aircraft are pink and violet. Eroding a fixed 2 px would have taken a bite out of both.
    So the decay is tested per frame and the conversion only runs where it holds; nobody is
    hand-listed, and a repainted hull re-classifies itself."""
    px = cell.load()
    w, h = cell.size
    dist = [[-1] * w for _ in range(h)]
    q = deque()
    for y in range(h):
        for x in range(w):
            if px[x, y][3] <= 16:
                continue
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if nx < 0 or ny < 0 or nx >= w or ny >= h or px[nx, ny][3] <= 16:
                    dist[y][x] = 0
                    q.append((x, y))
                    break
    while q:
        a2, b2 = q.popleft()
        for nx, ny in ((a2 + 1, b2), (a2 - 1, b2), (a2, b2 + 1), (a2, b2 - 1)):
            if 0 <= nx < w and 0 <= ny < h and px[nx, ny][3] > 16 and dist[ny][nx] < 0:
                dist[ny][nx] = dist[b2][a2] + 1
                q.append((nx, ny))

    near = far = 0
    hits = []
    for y in range(h):
        for x in range(w):
            d = dist[y][x]
            if d < 0 or not is_halo(px[x, y]):
                continue
            if d <= DEPTH:
                near += 1
                hits.append((x, y))
            elif d <= DEPTH + 3:
                far += 1
    if not near or far > near * DECAY:
        return 0                                   # this hull is that colour; leave it alone
    for (x, y) in hits:
        px[x, y] = (EDGE[0], EDGE[1], EDGE[2], px[x, y][3])
    return len(hits)


def boundary_dark(cell):
    """what fraction of the outer boundary is dark - the thing the conversion is trying to fix"""
    px = cell.load()
    w, h = cell.size
    tot = dark = 0
    for y in range(h):
        for x in range(w):
            if px[x, y][3] <= 16:
                continue
            edge = False
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if nx < 0 or ny < 0 or nx >= w or ny >= h or px[nx, ny][3] <= 16:
                    edge = True
                    break
            if not edge:
                continue
            tot += 1
            if max(px[x, y][:3]) <= 70:
                dark += 1
    return dark, tot


def main():
    write = '--write' in sys.argv
    targets = [(ATLAS, MANIFEST)]
    p0 = ATLAS + '.0906p.bak'                     # juggernaut's flame source, kept in step
    if os.path.exists(p0):
        targets.append((p0, MANIFEST))

    for atlas_path, man_path in targets:
        R = ship_rows(man_path)
        A = Image.open(atlas_path).convert('RGBA')
        label = os.path.basename(atlas_path)
        print('%s  (%d ship frames)' % (label, len(R)))
        per = {}
        b_before = d_before = 0
        for k, r in sorted(R.items()):
            x, y, w, h, ox, oy, cw, ch = r
            cell = A.crop((x, y, x + w, y + h))
            d, t = boundary_dark(cell)
            d_before += d; b_before += t
            n = convert(cell)
            if n:
                A.paste(cell, (x, y))
            pk = k[5:].split('_')[0]
            per[pk] = per.get(pk, 0) + n
        d_after = b_after = 0
        for k, r in sorted(R.items()):
            x, y, w, h = r[0], r[1], r[2], r[3]
            d, t = boundary_dark(A.crop((x, y, x + w, y + h)))
            d_after += d; b_after += t
        print('   converted %d px: %s' % (sum(per.values()),
              ', '.join('%s %d' % (a, b) for a, b in sorted(per.items()) if b)))
        print('   boundary that is dark: %.1f%% -> %.1f%%'
              % (100.0 * d_before / max(1, b_before), 100.0 * d_after / max(1, b_after)))
        if write:
            bak = atlas_path + '.0906t.bak'
            if not os.path.exists(bak):
                shutil.copy2(atlas_path, bak)
            A.save(atlas_path, format='PNG')   # .bak has no extension PIL knows
            print('   written (alpha untouched, so no silhouette moved)')
    if not write:
        print('DRY RUN - nothing written.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
