#!/usr/bin/env python3
"""
build_weaponicons_0810s.py — Mike's refreshed FIRE ORB and ICE SHARD tier icons.

    python3 _BUILD_SOURCE/build_weaponicons_0810s.py

Mike, 0810r/0810s: "I see your using a basic graphic for fireball icon, Im assuming yuo lost the
icons. Not good." ... "And ill have to get you to the fireball icons again" — then supplied the
sheet.

⚠ NOTHING WAS EVER LOST, AND THE OLD ICONS ARE GOOD. Rendered before touching anything
(docs/proofs/icons_existing_0810s.png): micon_fireorb_1..5 are hexagon-framed tier icons in the
same house style as this new sheet, and so are iceorb, icebreath, thermoshock, firewall and laser.
So this is a REFRESH of art that already worked, not a recovery — which matters, because it means
the thing Mike is calling "basic" is a SURFACE, not a missing file, and swapping the art would not
have fixed it on its own. See the HUD note at the bottom.

⚠ THE GRID IS MEASURED, NOT ASSUMED. Ink runs on the de-keyed sheet, gap-joined at 6px:
    cols (73,309) (359,598) (645,885) (930,1168) (1222,1465)
    rows (125,400) (568,843)
Five tiers across, two families down — fire orb on top, ice shards beneath.

⚠ THE KEY IS FLOODED FROM THE BORDER, never colour-matched across the whole image. A sweep for
"magenta" eats the magenta INSIDE the art (these icons have hot pink-white cores at tier IV/V);
flooding from the outside can only ever reach background. Standing rule in this project, and the
reason unit 12's wing survived its slice.

⚠ HALO -> BLACK EDGE, never deleted. Also standing. The rim is what keeps a sprite from reading as
a cutout against 16-bit art.
"""
import os
from collections import deque
from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
GAME = os.path.abspath(os.path.join(ROOT, '..'))
SRC = os.path.join(GAME, '_ART_SOURCES', 'BOF2_WeaponIcons_0810s',
                   'icons_fireorb_icebreath_tiers.png')
OUT_SHEET = os.path.join(GAME, 'assets', 'game', 'nia_icons2.png')

COLS = [(73, 309), (359, 598), (645, 885), (930, 1168), (1222, 1465)]
ROWS = [(125, 400), (568, 843)]
# Mike named the bottom row himself on the resend: "heres your fireball and ice breath icoNS".
# It is ICE BREATH - Freezer's weapon, and a family that already existed - not the "ice shards"
# this script guessed at on the first pass. weaponIconKey already routes w===4 to icebreath for
# him, so naming the row correctly is the whole wiring.
FAMILIES = ['micon_fireorb', 'micon_icebreath']      # row order, top to bottom
PAD = 2                                              # gutter in the packed sheet

# ⚠ DOWNSCALED, and it is a FILTERED resize on purpose. The obvious assumption with pixel-art-
# styled source is that it is a clean N-times upscale you can decimate losslessly with NEAREST —
# measured, it is not: re-expanding a NEAREST decimation mismatches the source by 16% at block 2
# and 19% at block 3, so there is no pixel grid to preserve. It is continuous-tone art at high
# resolution, and LANCZOS is the correct reducer for that.
#
# 192 is deliberate headroom: the existing micon_ family is 78x96 and the HUD draws around that,
# so this is 2x the largest size anything asks for and stays crisp when scaled down. At source
# size the ten icons packed to 1,025 KB, which is a lot of atlas for ten icons in a project whose
# atlas sprawl Mike has already called out.
TARGET_H = 192


def is_key(p):
    r, g, b = p[0], p[1], p[2]
    return r > 165 and g < 100 and b > 165


def dekey(im):
    """flood the magenta from the BORDER inward — never a colour sweep over the whole image"""
    im = im.convert('RGBA')
    w, h = im.size
    px = im.load()
    seen = [[False] * w for _ in range(h)]
    q = deque()
    for x in range(w):
        for y in (0, h - 1):
            if is_key(px[x, y]) and not seen[y][x]:
                seen[y][x] = True; q.append((x, y))
    for y in range(h):
        for x in (0, w - 1):
            if is_key(px[x, y]) and not seen[y][x]:
                seen[y][x] = True; q.append((x, y))
    while q:
        x, y = q.popleft()
        px[x, y] = (0, 0, 0, 0)
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h and not seen[ny][nx] and is_key(px[nx, ny]):
                seen[ny][nx] = True; q.append((nx, ny))
    return im


def despill(im):
    """kill the magenta fringe left on the rim: where R and B both overshoot G, pull them back"""
    im = im.convert('RGBA')
    px = im.load()
    w, h = im.size
    n = 0
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a < 8:
                continue
            if r > g + 38 and b > g + 38:
                px[x, y] = (min(r, g + 26), g, min(b, g + 26), a); n += 1
    return im, n


def black_edge(im):
    """one-pixel black rim OUTSIDE the silhouette — converted, not deleted"""
    im = im.convert('RGBA')
    w, h = im.size
    a = im.split()[3].point(lambda v: 255 if v > 110 else 0)
    ap = a.load()
    ring = Image.new('L', (w, h), 0)
    rp = ring.load()
    for y in range(h):
        for x in range(w):
            if ap[x, y]:
                continue
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < w and 0 <= ny < h and ap[nx, ny]:
                    rp[x, y] = 255
                    break
    out = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    out.paste((0, 0, 0, 255), (0, 0), ring)
    out.paste(im, (0, 0), a)
    return out


def main():
    sheet = Image.open(SRC).convert('RGBA')
    print('source %s  %dx%d' % (os.path.basename(SRC), sheet.width, sheet.height))

    icons = []          # (key, image)
    spill_total = 0
    for ri, (y0, y1) in enumerate(ROWS):
        fam = FAMILIES[ri]
        for ci, (x0, x1) in enumerate(COLS):
            cell = sheet.crop((x0 - 3, y0 - 3, x1 + 4, y1 + 4))
            cell = dekey(cell)
            cell, sp = despill(cell)
            spill_total += sp
            bb = cell.split()[3].point(lambda v: 255 if v > 0 else 0).getbbox()
            cell = cell.crop(bb)
            cell = cell.resize((max(1, round(cell.width * TARGET_H / cell.height)), TARGET_H),
                               Image.LANCZOS)
            cell = black_edge(cell)
            icons.append(('%s_%d' % (fam, ci + 1), cell))

    # pack: one row per family, tiers left to right
    cw = max(i.width for _, i in icons)
    ch = max(i.height for _, i in icons)
    W = (cw + PAD) * len(COLS) + PAD
    H = (ch + PAD) * len(ROWS) + PAD
    out = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    rects = {}
    for n, (key, im) in enumerate(icons):
        r, c = divmod(n, len(COLS))
        x = PAD + c * (cw + PAD) + (cw - im.width) // 2
        y = PAD + r * (ch + PAD) + (ch - im.height) // 2
        out.alpha_composite(im, (x, y))
        rects[key] = [x, y, im.width, im.height]
    out.save(OUT_SHEET)

    print('de-keyed by border flood, %d spill pixels pulled back' % spill_total)
    print('packed %d icons into %s  (%dx%d, %.0f KB)'
          % (len(icons), os.path.basename(OUT_SHEET), W, H,
             os.path.getsize(OUT_SHEET) / 1024))
    for k in sorted(rects):
        print('   %-22s %s' % (k, rects[k]))

    import json
    json.dump(rects, open(os.path.join(GAME, 'assets', 'data', 'ICONS2_RECTS.json'),
                          'w', encoding='utf-8'), indent=1)
    print('\nrects -> assets/data/ICONS2_RECTS.json')


if __name__ == '__main__':
    main()
