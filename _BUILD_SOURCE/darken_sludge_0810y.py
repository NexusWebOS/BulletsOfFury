#!/usr/bin/env python3
"""
darken_sludge_0810y.py — Mike: "darken the toxic sludge".

    python3 _BUILD_SOURCE/darken_sludge_0810y.py            # darken
    python3 _BUILD_SOURCE/darken_sludge_0810y.py --restore  # put nca_17.png back

Stage 7's bed came out as neon green at full brightness, which is both wrong for a sewer and the
reason the enemy fire added in 0810x reads as washed out over it.

⚠ WHICH KEY IS ACTUALLY DRAWN IS NOT THE ONE THE STAGE NAMES. _levelCfg gives stage 7
`liquid:'nlq_sludgeF'`, but stage 7 is `wide:true` and _liquidFrames swaps a wide stage onto
WIDE_FLAT[key] — so what the player sees is `nwl_sludge_*`, not `nlq_sludgeF_*`. Darkening only the
named family would have changed nothing on screen. Both families are done here.

⚠ THE CELLS ARE EDITED IN PLACE INSIDE nca_17.png, which is only safe because it was checked
first: all ten sludge rects are unaliased — no other key resolves to any of them (a key does not own
its file, and ~750 cells in this project are shared). Verified before writing, and re-verified here
at build time against the manifest.

⚠ VALUE MULTIPLY, HUE AND SATURATION UNTOUCHED. The standing rule is palette/luminance swaps, not
overlays — a flat dark overlay would flatten the bubbling highlights that give the sludge its
motion, the same way the source-atop tint flattened the font's drop shadow into the E→B bug. Only
V moves, so every bubble and swirl the artist drew survives at the new brightness.
"""
import io, json, os, re, shutil, sys, colorsys
from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
GAME = os.path.abspath(os.path.join(ROOT, '..'))
SHEET = os.path.join(GAME, 'assets', 'game', 'atlas', 'nca_17.png')
BACKUP = SHEET + '.presludge'

VALUE = 0.50          # how much of the original brightness survives


def load_cells():
    src = io.open(os.path.join(GAME, 'assets', 'manifest.js'), encoding='utf-8', errors='replace').read()
    m = re.search(r'window\.BOFX\s*=\s*', src)
    st = m.end(); d = 0; i = st
    while i < len(src):
        if src[i] == '{': d += 1
        elif src[i] == '}':
            d -= 1
            if d == 0: break
        i += 1
    return json.loads(src[st:i + 1])['cells']


def main():
    if '--restore' in sys.argv:
        if os.path.exists(BACKUP):
            shutil.copy(BACKUP, SHEET); print('restored nca_17.png from backup')
        else:
            print('no backup to restore')
        return

    cells = load_cells()
    targets = {k: v for k, v in cells.items() if re.match(r'^(nwl_sludge|nlq_sludgeF)_\d+$', k)}

    # re-verify the rects are unaliased before editing a shared sheet in place
    inv = {}
    for k, v in cells.items():
        inv.setdefault(tuple(v), []).append(k)
    for k, v in targets.items():
        others = [x for x in inv[tuple(v)] if x != k]
        if others:
            raise SystemExit('REFUSING: %s shares its rect with %s — editing in place would change '
                             'them too.' % (k, ', '.join(others)))
    print('%d sludge cells, all unaliased' % len(targets))

    if not os.path.exists(BACKUP):
        shutil.copy(SHEET, BACKUP); print('backup -> %s' % os.path.basename(BACKUP))

    im = Image.open(SHEET).convert('RGBA')
    px = im.load()
    touched = 0
    for k, c in sorted(targets.items()):
        _, sx, sy, w, h = c
        for y in range(sy, sy + h):
            for x in range(sx, sx + w):
                r, g, b, a = px[x, y]
                if a == 0:
                    continue
                hh, ss, vv = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
                nr, ng, nb = colorsys.hsv_to_rgb(hh, ss, vv * VALUE)
                px[x, y] = (int(nr * 255), int(ng * 255), int(nb * 255), a)
                touched += 1
        print('   %-16s %dx%d at (%d,%d)' % (k, w, h, sx, sy))
    im.save(SHEET)
    print('\ndarkened %d px to %.0f%% value, hue and saturation untouched' % (touched, VALUE * 100))
    print('wrote %s' % os.path.basename(SHEET))


if __name__ == '__main__':
    main()
