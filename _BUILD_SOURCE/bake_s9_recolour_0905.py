#!/usr/bin/env python3
"""bake_s9_recolour_0905.py - write Mike's approved stage-9 palette assignment into the atlas.

    python _BUILD_SOURCE/bake_s9_recolour_0905.py            # dry run, reports only
    python _BUILD_SOURCE/bake_s9_recolour_0905.py --write

Mike approved, 0905: wskim blue, pneedle light gray, pmine ORIGINAL purple/blue, gleech neon red,
vmanta pink, echof dark gray, tsplit black, cbreak neon red - plus the halo fix on all eight and
the stray removal on echof.

⚠ THE PIXELS GO BACK INTO THE ATLAS, NOT INTO NEW LOOSE PNGs. `XART._touch` checks BOFX.cells
BEFORE X._src (game.js 2553, and the comment there says the order "matters more than it looks"),
so registering recoloured loose files under the same keys would lose to the atlas cell every time
and the game would keep drawing the purple originals. Measured first: all 32 ns9e_ cells live on
`en_s9`, every one of their rects is exclusive to the roster, and no NON-ns9e cell overlaps any of
them - so rewriting that region in place cannot touch another unit's art.

⚠ AND EACH UNIT HAS ONLY TWO DISTINCT RECTS, NOT FOUR. `_idle` and `_0` alias the same rectangle,
as do `_fire` and `_1`. Processing all four keys would recolour each rect twice - and a second
pass over an already-swapped plate would roll the hue a second time and darken the rim again.
Rects are de-duplicated before any work happens.

⚠ ALPHA IS ASSERTED UNCHANGED. Silhouette is collision: `alphaBounds` and the draw footprint both
read it. The only permitted difference is echof's 60 stray pixels, which Mike asked to be removed
by name, and the script fails loudly if anything else moved.
"""
import json, os, sys, shutil
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from s9_palette_variants_0905 import recolour, drop_strays, colours

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ATLAS = os.path.join(ROOT, 'assets/game/atlas/en_s9.png')
BACKUP = ATLAS + '.bak-0905recolour'

ASSIGN = {'wskim': 'blue', 'pneedle': 'lightgray', 'pmine': 'asis', 'gleech': 'neonred',
          'vmanta': 'pink', 'echof': 'darkgray', 'tsplit': 'black', 'cbreak': 'neonred'}


def alpha_sig(im):
    px = im.load()
    return {(x, y) for y in range(im.height) for x in range(im.width) if px[x, y][3] > 0}


def main():
    write = '--write' in sys.argv
    cells = json.load(open('/tmp/ns9e_cells.json'))
    atlas = Image.open(ATLAS).convert('RGBA')

    # de-duplicate: idle/0 and fire/1 alias one rect each
    todo = {}
    for k, (_a, x, y, w, h) in cells.items():
        unit = k.split('_')[1]
        if unit not in ASSIGN:
            continue
        todo.setdefault((unit, x, y, w, h), []).append(k)
    print('%d ns9e keys -> %d distinct rects to process\n' % (len(cells), len(todo)))

    total_stray = 0
    for (unit, x, y, w, h), keys in sorted(todo.items()):
        var = ASSIGN[unit]
        src = atlas.crop((x, y, x + w, y + h))
        before_a = alpha_sig(src)
        before_c = colours(src)
        cleaned, n = drop_strays(src)
        total_stray += n
        out = recolour(cleaned, var)
        after_a = alpha_sig(out)
        # the ONLY permitted alpha change is the strays we deliberately deleted
        lost, gained = before_a - after_a, after_a - before_a
        if gained or len(lost) != n:
            raise SystemExit('ALPHA MOVED on %s (%s): lost %d (expected %d), gained %d'
                             % (unit, var, len(lost), n, len(gained)))
        print('  %-9s %-10s rect %4d,%-4d %3dx%-3d  colours %5d -> %-5d  strays %2d  keys: %s'
              % (unit, var, x, y, w, h, before_c, colours(out), n, ','.join(sorted(keys))))
        if write:
            atlas.paste(out, (x, y))

    print('\nstray pixels removed in total: %d' % total_stray)
    if not write:
        print('DRY RUN - nothing written. Re-run with --write.')
        return
    if not os.path.exists(BACKUP):
        shutil.copy(ATLAS, BACKUP)
        print('backed up -> %s' % os.path.basename(BACKUP))
    atlas.save(ATLAS)
    print('wrote %s' % ATLAS)


if __name__ == '__main__':
    main()
