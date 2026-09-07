#!/usr/bin/env python3
"""flame_mask_0907n.py - find the exhaust on a pack cell, on nine differently-coloured aircraft.

    python _BUILD_SOURCE/flame_mask_0907n.py            # proof sheet, all 9 pilots, both lengths
    python _BUILD_SOURCE/flame_mask_0907n.py --cells    # every cell of one sheet

⚠ A WARM-PIXEL TEST CANNOT FIND A FLAME ON THIS FLEET AND IT FAILED IN BOTH DIRECTIONS. 0907h
recorded it firing on paint - Yuri's aircraft is RED (3,163 px) and Falva's PINK (550) - and 0907m
found the opposite half: tightened with `r - b > 40` to keep Yuri's hull out, it reported FALVA AS
HAVING NO FLAME ON 30 OF HER 32 CELLS, because her exhaust is pale pink-white and pink carries a
high blue channel. A colour window that excludes a red hull also excludes a white flame.

⚠ THE PROPERTY THAT SEPARATES THEM IS A WHITE-HOT CORE, NOT A HUE. Every flame in this pack ramps
white -> yellow -> orange -> red, so it always contains near-achromatic pixels at full brightness.
No hull in the fleet does: Yuri's red and Falva's pink are saturated at every value, and her white
wing flashes are up at the canopy, not down at the tail. So a component qualifies only if it is
bright, warm-or-white, HOLDS A NEAR-WHITE CORE, and sits below the aircraft's own centroid - four
conditions, of which the core is the one doing the work.

⚠ AND IT IS CONFIRMED BY RENDERING THE MASK, ON ALL NINE, BEFORE ANY COUNT IS QUOTED. That is the
whole of 0907h's lesson: "Confirm with the picture; a colour count cannot tell a red ship from a
lit engine."
"""
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from thruster_inventory_0907m import dekey_np, sheet, label, PILOTS, ROWS, COLS

MIN_BLOB = 24
CORE_V = 186      # a pixel this bright in ALL THREE channels is a white-hot core pixel
CORE_N = 6        # a real flame carries at least this many of them


def flame_mask(rgb, alpha):
    """the exhaust, as a boolean mask. see the module docstring for why each term is here."""
    r = rgb[:, :, 0].astype(np.int16)
    g = rgb[:, :, 1].astype(np.int16)
    b = rgb[:, :, 2].astype(np.int16)
    mx = np.maximum(np.maximum(r, g), b)
    mn = np.minimum(np.minimum(r, g), b)
    # bright, and on the warm-to-white ramp: red >= green >= blue, with slack for dithering
    hot = alpha & (mx > 200) & (r >= g - 12) & (g >= b - 24)
    if not hot.any():
        return np.zeros_like(alpha)
    core = alpha & (mn > CORE_V)
    if not alpha.any():
        return np.zeros_like(alpha)
    # ⚠ "BELOW THE AIRCRAFT'S CENTROID" WAS WRONG AND IT COST FOUR REELS. An INVERTED frame -
    # the belly, halfway through a somersault - has its nose DOWN and its exhaust pointing UP, so
    # the rule rejected the flame on exactly the frames where the ship is upside down: decker r1c4
    # and yuri r1c4 both measured 0 px on a plate that plainly has two lit engines, and Maverick
    # came out "reversed against Maverick", which is the contradiction that gave it away.
    # An exhaust PROTRUDES instead: it is the bright warm ink that reaches open space.
    edge = np.zeros_like(alpha)
    edge[1:, :] |= ~alpha[:-1, :]
    edge[:-1, :] |= ~alpha[1:, :]
    edge[:, 1:] |= ~alpha[:, :-1]
    edge[:, :-1] |= ~alpha[:, 1:]
    edge &= alpha
    lab, n = label(hot)
    out = np.zeros_like(alpha)
    for i in range(1, n + 1):
        m = lab == i
        sz = int(m.sum())
        if sz < MIN_BLOB:
            continue
        if int((m & core).sum()) < CORE_N:
            continue                        # no white-hot core -> it is paint, not fire
        if not (m & edge).any():
            continue                        # sealed inside the airframe -> a highlight, not fire
        out |= m
    return out


def cell_of(rgb, alpha, r, c):
    CH, CW = rgb.shape[0] // ROWS, rgb.shape[1] // COLS
    sl = (slice(r * CH, (r + 1) * CH), slice(c * CW, (c + 1) * CW))
    return rgb[sl], alpha[sl]


def render(a, al, m, bg=(24, 24, 30), hi=(0, 255, 90)):
    out = np.full(a.shape, bg, np.uint8)
    out[al] = a[al]
    out[m] = hi
    return Image.fromarray(out)


def main():
    try:
        F = ImageFont.truetype('C:/Windows/Fonts/consolab.ttf', 15)
    except Exception:
        F = ImageFont.load_default()
    Z = 1
    T = 221 * Z
    cols = 6
    tiles = []
    for pilot in PILOTS:
        for which in ('short', 'long'):
            rgb, alpha, _ = dekey_np(sheet(pilot, which))
            a, al = cell_of(rgb, alpha, 0, 0)
            m = flame_mask(a, al)
            tiles.append(('%s %s' % (pilot, which), int(m.sum()),
                          render(a, al, al & ~m, hi=(30, 30, 38)),
                          render(a, al, m)))
    rows = (len(tiles) + cols - 1) // cols
    CW, CH = T * 2 + 16, T + 26
    S = Image.new('RGB', (CW * cols, CH * rows), (14, 14, 20))
    d = ImageDraw.Draw(S)
    for i, (lab, n, plain, hl) in enumerate(tiles):
        x, y = (i % cols) * CW, (i // cols) * CH
        S.paste(plain.resize((T, T), Image.NEAREST), (x + 4, y + 22))
        S.paste(hl.resize((T, T), Image.NEAREST), (x + T + 10, y + 22))
        d.text((x + 4, y + 3), '%s   flame %d px  (hull greyed | mask green)' % (lab, n),
               font=F, fill=(255, 214, 110) if n else (255, 110, 110))
    out = os.path.join(ROOT, 'docs/FLAME_MASK_0907N.png')
    S.save(out)
    print('wrote docs/FLAME_MASK_0907N.png  (%dx%d)' % S.size)
    for lab, n, _, _ in tiles:
        print('   %-18s %6d px' % (lab, n))
    return 0


if __name__ == '__main__':
    sys.exit(main())
