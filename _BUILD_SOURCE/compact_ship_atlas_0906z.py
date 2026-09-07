#!/usr/bin/env python3
"""compact_ship_atlas_0906z.py - reclaim the strips that repeated appends orphaned.

    python _BUILD_SOURCE/compact_ship_atlas_0906z.py            # measure + verify only
    python _BUILD_SOURCE/compact_ship_atlas_0906z.py --write

The standing rule in this repo is *append a strip, repoint the rects, pixels and manifest in ONE
write* - and it has earned its keep twice (Lizzie's B-42 costume cost no art at all because the
0906b import appended rather than replaced). But every append leaves the previous strip in the
file, and this drop appended six times. Measured: **28.6 Mpx of atlas, 11.9 referenced - 59% is
dead**, and the PNG is 21.1 MB against 11.7 before the run.

⚠ SAFE HERE FOR ONE SPECIFIC REASON, WHICH IS WORTH CHECKING BEFORE REUSING THIS. `BOFX.cells` has
**zero** rows pointing at this sheet, so the ONLY consumers are the 329 `BOFX.ships` rects, and
they can all be enumerated. On any other sheet the note in CLAUDE.md applies - "a key does not own
its file, ~750 cells are aliased" - and a repack that only walks one table would silently drop the
other's art.

⚠ ALIASES ARE PRESERVED BY GROUPING ON THE RECT, NOT BY KEY. Two keys that share one rectangle are
one picture; packing them twice would work but would waste exactly what this is trying to reclaim,
and packing them independently would break the invariant that they stay identical.

⚠ AND IT VERIFIES BY PIXELS, NOT BY COUNTS. Every key's cell is compared byte for byte between the
old atlas and the new one before anything is written; a repack that moves a rect one pixel is
invisible to any count-based check and obvious to this one.
"""
import os, re, sys, json, shutil, subprocess
from PIL import Image, ImageChops

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ATLAS = os.path.join(ROOT, 'assets/game/atlas/bof_player_ships_barrel_rolls.png')
MANIFEST = os.path.join(ROOT, 'assets/manifest.js')
SHEET = 'bof_player_ships_barrel_rolls'
GUT = 2


def main():
    write = '--write' in sys.argv
    data = json.loads(subprocess.run(['node', '-e',
        "global.window=global;eval(require('fs').readFileSync('assets/manifest.js','utf8'));"
        "process.stdout.write(JSON.stringify({ships:BOFX.ships,cells:BOFX.cells}));"],
        capture_output=True, cwd=ROOT).stdout.decode())
    ships = data['ships']

    other = [k for k, v in data['cells'].items() if isinstance(v, list) and v and v[0] == SHEET]
    if other:
        print('%d BOFX.cells rows also live on this sheet - refusing, they would be dropped' % len(other))
        return 1
    print('BOFX.cells rows on this sheet: 0 (so the ship rects are the only consumers)')

    A = Image.open(ATLAS).convert('RGBA')
    print('atlas %dx%d = %.1f Mpx, %.1f MB' % (A.width, A.height, A.width * A.height / 1e6,
                                               os.path.getsize(ATLAS) / 1e6))

    # group keys that share a rectangle - those are aliases and must stay one picture
    groups = {}
    for k, r in ships.items():
        groups.setdefault((r[0], r[1], r[2], r[3]), []).append(k)
    print('%d ship rows -> %d distinct rectangles (%d aliased)'
          % (len(ships), len(groups), len(ships) - len(groups)))

    # shelf-pack the distinct rects, tallest first
    order = sorted(groups, key=lambda t: -t[3])
    W = A.width
    x = y = rowh = 0
    place = {}
    for rect in order:
        w, h = rect[2], rect[3]
        if x + w + GUT > W:
            x = 0
            y += rowh + GUT
            rowh = 0
        place[rect] = (x, y)
        x += w + GUT
        rowh = max(rowh, h)
    H = y + rowh + GUT
    print('packed into %dx%d = %.1f Mpx  (%.0f%% of the old area)'
          % (W, H, W * H / 1e6, 100.0 * W * H / (A.width * A.height)))

    out = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    for rect, (nx, ny) in place.items():
        ox, oy, w, h = rect
        out.paste(A.crop((ox, oy, ox + w, oy + h)), (nx, ny))

    # ---- verify every key by PIXELS before writing anything
    bad = 0
    for k, r in ships.items():
        ox, oy, w, h = r[0], r[1], r[2], r[3]
        nx, ny = place[(ox, oy, w, h)]
        a = A.crop((ox, oy, ox + w, oy + h))
        b = out.crop((nx, ny, nx + w, ny + h))
        if ImageChops.difference(a.convert('RGBA'), b.convert('RGBA')).getbbox() is not None:
            print('  MISMATCH %s' % k)
            bad += 1
    print('pixel verification: %d of %d cells differ' % (bad, len(ships)))
    if bad:
        return 1

    src = open(MANIFEST, encoding='utf-8').read()
    n = 0
    for k, r in sorted(ships.items()):
        nx, ny = place[(r[0], r[1], r[2], r[3])]
        row = '"%s":[%d,%d,%d,%d,%d,%d,%d,%d]' % (k, nx, ny, r[2], r[3], r[4], r[5], r[6], r[7])
        pat = re.compile(r'"' + re.escape(k) + r'":\[[^\]]*\]')
        if not pat.search(src):
            print('  %s missing from the manifest - refusing' % k)
            return 1
        src = pat.sub(row, src, count=1)
        n += 1

    if not write:
        print('DRY RUN - nothing written (%d rows would be repointed).' % n)
        return 0
    bak = ATLAS + '.0906z.bak'
    if not os.path.exists(bak):
        shutil.copy2(ATLAS, bak)
    if not os.path.exists(MANIFEST + '.0906z.bak'):
        shutil.copy2(MANIFEST, MANIFEST + '.0906z.bak')
    out.save(ATLAS)
    open(MANIFEST, 'w', encoding='utf-8', newline=chr(10)).write(src)
    print('wrote the atlas (%dx%d, %.1f MB) and %d repointed rects, in one write'
          % (W, H, os.path.getsize(ATLAS) / 1e6, n))
    return 0


if __name__ == '__main__':
    sys.exit(main())
