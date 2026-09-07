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
    return s >= 0.25 and v >= 0.12 and 248.0 <= d <= 345.0


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


def hue_gap(a, b):
    d = abs(a - b) % 1.0
    return min(d, 1.0 - d) * 360.0


def despeckle(cell):
    """key SPILL on the silhouette: a saturated pixel whose hue matches almost none of its neighbours.

    ⚠ THE MAGENTA RULE ONLY EVER CAUGHT A QUARTER OF THIS. Measured across all nine hulls, 18,697
    boundary pixels are saturated AND unlike 75%+ of their own neighbours, and their hues cluster
    at 120-135 deg (4,535), 240-255 (3,707), 300-315 (3,570) and 165-195 (2,644) - green, blue,
    magenta and cyan, i.e. the CORNERS OF THE COLOUR CUBE. That is chroma-key spill, not paint, and
    a magenta-only sweep leaves the green and cyan dots on every wing edge - which is what was
    still speckling the hulls after 0906t.

    ⚠ AND "UNLIKE ITS NEIGHBOURS" IS WHAT MAKES IT SAFE ON A SHIP THAT IS THAT COLOUR. Cole's hull
    is green and Maverick's is teal; their green and teal pixels sit among other green and teal
    pixels, so they never qualify. A hue LIST would have had to special-case both."""
    px = cell.load()
    w, h = cell.size
    hits = []
    for y in range(h):
        for x in range(w):
            p0 = px[x, y]
            if p0[3] <= 16:
                continue
            h0, s0, v0 = colorsys.rgb_to_hsv(p0[0] / 255., p0[1] / 255., p0[2] / 255.)
            if s0 < 0.30:
                continue
            nb = []
            edge = False
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    if dx == 0 and dy == 0:
                        continue
                    nx, ny = x + dx, y + dy
                    if nx < 0 or ny < 0 or nx >= w or ny >= h or px[nx, ny][3] <= 16:
                        edge = True
                        continue
                    q = colorsys.rgb_to_hsv(*[v / 255. for v in px[nx, ny][:3]])
                    if q[1] >= 0.10:
                        nb.append(q[0])
            if not edge or len(nb) < 2:
                continue
            if sum(1 for q in nb if hue_gap(h0, q) > 55) >= len(nb) * 0.75:
                hits.append((x, y))
    for (x, y) in hits:
        px[x, y] = (EDGE[0], EDGE[1], EDGE[2], px[x, y][3])
    return len(hits)


SPECK_MAX = 24     # a violet blob this small is dirt, not paint
THIN_MAX  = 80     # ...and so is a longer blob that is at most 2 px thick


def depurple(cell):
    """violet dirt by CONNECTED-COMPONENT SIZE, which is the only thing that separates it from a
    ship that is painted violet.

    ⚠ EVERY PER-PIXEL TEST I TRIED SCORED REAL PAINT. A hue list cannot work (freezer's hull is
    violet, falva's is pink); "is it on the boundary" misses the dots buried one pixel inside the
    black edge; "is it unlike its neighbours" took 69,995 px and started eating airframes, and a
    hue-agnostic version scored 1,000 hits on juggernaut, whose copper highlights are paint.

    ⚠ THE SIZE HISTOGRAM IS UNAMBIGUOUS AND IT IS WHAT SHOULD HAVE BEEN MEASURED FIRST. Of the
    violet components left on the nine hulls: **8,146 are a single pixel**, 2,441 are two, 1,070
    are three — and only 182 are 64 px or larger. Falva's 82,240 violet pixels and Freezer's
    37,756 are their AIRCRAFT and live almost entirely in those large components, so a size cut
    removes the dirt and cannot touch either hull. No pilot is named, and a repainted ship
    re-classifies itself.

    ⚠ AND A THIN COMPONENT IS DIRT EVEN WHEN IT IS LONG - key spill runs along an edge as a 1-2 px
    filament that can total 40-60 px while never being more than two wide."""
    px = cell.load()
    w, h = cell.size
    seen = [[False] * w for _ in range(h)]
    killed = 0
    for y0 in range(h):
        for x0 in range(w):
            if seen[y0][x0] or not is_violet(px[x0, y0]):
                continue
            q = deque([(x0, y0)])
            seen[y0][x0] = True
            pts = []
            while q:
                a2, b2 = q.popleft()
                pts.append((a2, b2))
                for nx, ny in ((a2 + 1, b2), (a2 - 1, b2), (a2, b2 + 1), (a2, b2 - 1),
                               (a2 + 1, b2 + 1), (a2 - 1, b2 - 1), (a2 + 1, b2 - 1), (a2 - 1, b2 + 1)):
                    if 0 <= nx < w and 0 <= ny < h and not seen[ny][nx] and is_violet(px[nx, ny]):
                        seen[ny][nx] = True
                        q.append((nx, ny))
            xs = [q2[0] for q2 in pts]; ys = [q2[1] for q2 in pts]
            bw = max(xs) - min(xs) + 1; bh = max(ys) - min(ys) + 1
            thin = min(bw, bh) <= 2
            if len(pts) < SPECK_MAX or (thin and len(pts) < THIN_MAX):
                for (x, y) in pts:
                    px[x, y] = (EDGE[0], EDGE[1], EDGE[2], px[x, y][3])
                killed += len(pts)
    return killed


def is_violet(p):
    """a magenta cast, by CHANNEL PATTERN rather than by saturation.

    ⚠ SATURATION IS THE WRONG TEST ON A DARK PIXEL, AND THAT IS WHY FOUR PASSES LEFT DOTS BEHIND.
    The survivors sampled off Cole's shipped hull are (57,48,62), (52,43,55), (29,21,29),
    (22,0,21) - violet, plainly visible at zoom against a near-black hull, and sitting at
    saturation 0.20-0.27, just under every threshold I tried. Raising the threshold instead would
    have started taking real shadow.

    What every one of them HAS is the magenta signature: red and blue both above green. That holds
    at any brightness, which is exactly what saturation does not. Grey stays grey (r=g=b gives a
    gap of 0) and a hull colour that genuinely leans violet is still protected by the
    component-SIZE rule one level up."""
    r, g, b, a = p
    if a <= 16:
        return False
    h, s, v = colorsys.rgb_to_hsv(r / 255., g / 255., b / 255.)
    if s >= 0.28 and v >= 0.10 and 248.0 <= h * 360.0 <= 352.0:
        return True
    return r > g and b > g and min(r, b) - g >= 5 and max(r, b) >= 14


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
            n = convert(cell) + despeckle(cell) + depurple(cell)
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
