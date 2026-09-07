#!/usr/bin/env python3
"""flame_seed_0907o.py - the exhaust, found by what THRUST does rather than by what fire looks like.

    python _BUILD_SOURCE/flame_seed_0907o.py           # proof sheet, 9 pilots
    python _BUILD_SOURCE/flame_seed_0907o.py lizzie    # every cell of one pilot

⚠⚠ THREE COLOUR-WINDOW DETECTORS FAILED HERE, EACH ON A DIFFERENT SHIP, AND THE FOURTH IS NOT
ANOTHER COLOUR WINDOW. The history is worth keeping because the pattern is the lesson:
    0907h  warm pixels          -> fired on Yuri's RED hull (3,163 px) and Falva's PINK (550)
    0907m  warm, with r-b > 40  -> reported FALVA with NO FLAME on 30 of 32 cells; her exhaust is
                                   pale pink-white, and pink carries a high blue channel
    0907n  + white-hot core     -> the core count that keeps Lizzie's gold wing streaks out (6)
                                   also erases Axel, Cole, Falva, Freezer and Maverick entirely
Each fix broke a ship the previous one had right, which is this file's own "when a model fits one
case and explodes on another, check whether the cases are the same thing". Nine hulls span red,
pink, gold, green, blue, copper, teal and violet; no window in colour space contains every flame
and excludes every hull, because some hulls ARE flame-coloured.

⚠ THE PACK ANSWERS IT DEFINITIONALLY. It ships each pose TWICE - long thrust and short thrust -
and the hull is REGISTERED between the pair: measured on frame 0 of all nine, only 72 to 543 px of
~15,000 differ, and 76-94% of those sit in the aircraft's bottom quarter. So the pixels that gain
ink when thrust goes up ARE the exhaust, whatever colour that pilot's fire or paint happens to be.
That is a seed no hull can trip, on any palette, present or future.

The seed is then grown through connected BRIGHT ink to recover the whole plume, including the part
that is lit in both plates. Region growing from a certain seed is safe where thresholding from
scratch was not: the threshold only has to keep the flame connected, not to tell fire from paint.
"""
import os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from thruster_inventory_0907m import dekey_np, sheet, label, PILOTS, ROWS, COLS

GROW_V = 170      # "bright ink" the grow is allowed to spread through
GROW_K = 9        # ⚠ AND IT MUST BE A BOUNDED DILATION, NOT A CONNECTED COMPONENT. Growing the
                  # seed through every connected bright pixel took Lizzie's flame to 11,424 px of a
                  # ~16,000 px hull and Falva's to 9,007: a gold aircraft and a pink one are bright
                  # ALL OVER, and the exhaust touches them, so "connected and bright" is the whole
                  # ship. Nine dilations reach about as far as a plume is wide and no further, so
                  # the bound is geometric and needs no opinion about colour.
SEED_D = 44       # per-pixel RGB distance that counts as "this pixel changed with thrust"
MIN_SEED = 12     # a component needs this many seed px to be called an exhaust


def cell(rgb, alpha, r, c):
    CH, CW = rgb.shape[0] // ROWS, rgb.shape[1] // COLS
    sl = (slice(r * CH, (r + 1) * CH), slice(c * CW, (c + 1) * CW))
    return rgb[sl], alpha[sl]


def flames(rgbL, alL, rgbS, alS):
    """(flame in the long plate, flame in the short plate) for one cell"""
    d = np.abs(rgbL.astype(np.int16) - rgbS.astype(np.int16)).sum(axis=2)
    seed = (alL & ~alS) | (alL & alS & (d > SEED_D))
    if not seed.any():
        z = np.zeros_like(alL)
        return z, z
    # drop stray seed specks: a real exhaust seed is a blob, a mismatched rivet is not
    slab, sn = label(seed)
    if sn:
        sz = np.bincount(slab.ravel())
        for i in range(1, sn + 1):
            if sz[i] < MIN_SEED:
                seed[slab == i] = False
    if not seed.any():
        z = np.zeros_like(alL)
        return z, z

    out = []
    for rgb, al in ((rgbL, alL), (rgbS, alS)):
        bright = al & (rgb.max(axis=2) > GROW_V)
        cur = seed & al
        keep = cur.copy()
        for _ in range(GROW_K):
            g = np.zeros_like(keep)
            g[1:, :] |= keep[:-1, :]
            g[:-1, :] |= keep[1:, :]
            g[:, 1:] |= keep[:, :-1]
            g[:, :-1] |= keep[:, 1:]
            nxt = g & bright & ~keep
            if not nxt.any():
                break
            keep |= nxt
        out.append(keep)
    return out[0], out[1]


def main():
    args = [a for a in sys.argv[1:] if a in PILOTS]
    try:
        F = ImageFont.truetype('C:/Windows/Fonts/consolab.ttf', 15)
    except Exception:
        F = ImageFont.load_default()

    if args:
        pilot = args[0]
        rgbL, alL, _ = dekey_np(sheet(pilot, 'long'))
        rgbS, alS, _ = dekey_np(sheet(pilot, 'short'))
        T = 221
        S = Image.new('RGB', (T * COLS + 8, (T + 22) * ROWS + 26), (14, 14, 20))
        d = ImageDraw.Draw(S)
        d.text((6, 5), '%s  -  LONG plate, exhaust masked GREEN' % pilot.upper(),
               font=F, fill=(255, 226, 140))
        tot = 0
        for r in range(ROWS):
            for c in range(COLS):
                aL, bL = cell(rgbL, alL, r, c)
                aS, bS = cell(rgbS, alS, r, c)
                fL, _ = flames(aL, bL, aS, bS)
                tot += int(fL.sum())
                o = np.full(aL.shape, (24, 24, 30), np.uint8)
                o[bL] = aL[bL]
                o[fL] = (0, 255, 90)
                S.paste(Image.fromarray(o), (4 + c * T, 26 + r * (T + 22)))
                d.text((6 + c * T, 26 + r * (T + 22) + T + 3), 'r%dc%d  %d px' % (r, c, int(fL.sum())),
                       font=F, fill=(150, 160, 200) if fL.any() else (255, 110, 110))
        out = os.path.join(ROOT, 'docs/FLAME_SEED_%s_0907O.png' % pilot.upper())
        S.save(out)
        print('wrote docs/FLAME_SEED_%s_0907O.png   %d flame px over 32 cells' % (pilot.upper(), tot))
        return 0

    print('%-11s %s' % ('pilot', 'flame px per cell, LONG plate, row 0 then row 1'))
    for pilot in PILOTS:
        rgbL, alL, _ = dekey_np(sheet(pilot, 'long'))
        rgbS, alS, _ = dekey_np(sheet(pilot, 'short'))
        for r in (0, 1):
            v = []
            for c in range(COLS):
                aL, bL = cell(rgbL, alL, r, c)
                aS, bS = cell(rgbS, alS, r, c)
                fL, _ = flames(aL, bL, aS, bS)
                v.append(int(fL.sum()))
            print('%-11s row%d  %s' % (pilot if r == 0 else '', r, '  '.join('%5d' % x for x in v)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
