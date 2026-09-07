#!/usr/bin/env python3
"""missing_exhaust_0907r.py - which of the 288 pack cells have no lit exhaust, per pilot palette.

    python _BUILD_SOURCE/missing_exhaust_0907r.py
    python _BUILD_SOURCE/missing_exhaust_0907r.py juggernaut --proof

Mike, 0907: "place where they are missing."

⚠ THE FLAME PALETTE IS LEARNED FROM THE PILOT'S OWN SHIP, NOT ASSUMED TO BE FIRE-COLOURED. Rendering
the fleet settled what four failed detectors had been hinting at: **Cole's exhaust is GREEN, Freezer's
and Maverick's are CYAN, Falva's is white-pink, Axel's white** - only Juggernaut, Lizzie, Decker and
Yuri burn orange. So every "warm pixel" test in 0907h/m/n was looking for a colour that five of the
nine ships do not have, while the hulls it was tripping on (Yuri red, Falva pink) genuinely are
flame-coloured. There is no fleet-wide flame colour to test for.

⚠ SO THE PALETTE IS TAKEN FROM r0c0, WHERE THE THRUST-RESPONSE WEIGHT ALREADY IDENTIFIES THE FLAME
WITH NO COLOUR TEST AT ALL. That weight (0907p) is |long - short| per pixel: the level top view has
a big, unambiguous plume and the response map is black across the hull and white on the flame, which
was confirmed by eye before this was built on it. The bright core of those pixels IS that pilot's
flame palette, measured off his own aircraft, and any cell is then scored by how much of it it
carries. A repainted ship re-learns its own palette; nothing is hand-listed.

⚠ AND THE CORE IS THE TOP OF THE FLAME'S OWN VALUE RANGE, WHICH IS WHAT KEEPS COLE'S GREEN FLAME
APART FROM COLE'S GREEN HULL. The plume's core is far brighter than any paint on the airframe -
that is what makes it read as combustion - so matching on the core colours separates them where
matching on hue alone could not.
"""
import os, sys, json
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from thruster_inventory_0907m import dekey_np, sheet, label, PILOTS, ROWS, COLS
from bake_pack_thrusters_0907p import defringe, drop_detached, RESP_LO, RESP_HI

CORE_Q = 70        # the flame's own brightest 30% is its core
PAL_D = 46         # RGB distance at which a pixel counts as "this pilot's flame colour"
MIN_BLOB = 22      # a lit exhaust is a blob, not a speck
NOSE_ON = (1, 6)   # ⚠ measured on all nine (0907q): c2 is TAIL-ON, c6 is NOSE-ON, unanimously.
                   # A nose-on aircraft correctly shows no exhaust and must not count as missing.


def cells(pilot):
    rgbL, alL, _ = dekey_np(sheet(pilot, 'long'))
    rgbS, alS, _ = dekey_np(sheet(pilot, 'short'))
    CH, CW = rgbS.shape[0] // ROWS, rgbS.shape[1] // COLS
    out = {}
    for r in range(ROWS):
        for c in range(COLS):
            sl = (slice(r * CH, (r + 1) * CH), slice(c * CW, (c + 1) * CW))
            bS, _ = drop_detached(alS[sl].copy())
            bL, _ = drop_detached(alL[sl].copy())
            aS, _, _ = defringe(rgbS[sl].copy(), bS)
            aL, _, _ = defringe(rgbL[sl].copy(), bL)
            resp = np.abs(aL.astype(np.int16) - aS.astype(np.int16)).sum(axis=2)
            resp[~(bS & bL)] = 0
            w = np.clip((resp - RESP_LO) / (RESP_HI - RESP_LO), 0.0, 1.0)
            out[(r, c)] = (aS, bS, w)
    return out


def palette(a, al, w):
    """this pilot's flame core colours, learned from the frame whose plume is unambiguous"""
    m = al & (w > 0.6)
    if m.sum() < 20:
        m = al & (w > 0.35)
    if m.sum() < 20:
        return None
    px = a[m].astype(np.int16)
    v = px.max(axis=1)
    keep = px[v >= np.percentile(v, CORE_Q)]
    # quantise to keep the match cheap and to tolerate dithering
    q = np.unique(keep // 12, axis=0) * 12 + 6
    return q


def lit(a, al, pal):
    """px of this cell that carry the pilot's own flame core colour, in blobs"""
    if pal is None:
        return 0, np.zeros_like(al)
    px = a.astype(np.int16)
    d = np.full(al.shape, 9999, np.int32)
    for cq in pal:
        d = np.minimum(d, np.abs(px - cq).sum(axis=2))
    m = al & (d <= PAL_D)
    lab, n = label(m)
    if not n:
        return 0, m
    sz = np.bincount(lab.ravel())
    keep = np.zeros_like(m)
    for i in range(1, n + 1):
        if sz[i] >= MIN_BLOB:
            keep |= (lab == i)
    return int(keep.sum()), keep


def main():
    want = [p for p in sys.argv[1:] if p in PILOTS] or PILOTS
    proof = '--proof' in sys.argv
    rep, missing_total = {}, 0
    for pilot in want:
        cs = cells(pilot)
        a0, al0, w0 = cs[(0, 0)]
        pal = palette(a0, al0, w0)
        base = lit(a0, al0, pal)[0]
        rows, miss = {}, []
        for r in range(ROWS):
            for c in range(COLS):
                a, al, _ = cs[(r, c)]
                n, _ = lit(a, al, pal)
                rows['r%dc%d' % (r, c)] = n
                if n < MIN_BLOB and (r, c) != NOSE_ON:
                    miss.append('r%dc%d' % (r, c))
        rep[pilot] = dict(palette=int(len(pal)) if pal is not None else 0,
                          base_flame=base, per_cell=rows, missing=miss)
        missing_total += len(miss)
        print('%-11s palette %2d colours   r0c0 flame %5d px   cells with NO LIT EXHAUST: %s'
              % (pilot, len(pal) if pal is not None else 0, base,
                 ('%d  -> %s' % (len(miss), ', '.join(miss))) if miss else '0'))
        if proof:
            try:
                F = ImageFont.truetype('C:/Windows/Fonts/consolab.ttf', 14)
            except Exception:
                F = ImageFont.load_default()
            T = 221
            S = Image.new('RGB', (T * COLS + 8, (T + 20) * ROWS + 24), (14, 14, 20))
            dr = ImageDraw.Draw(S)
            dr.text((6, 4), '%s  -  pixels carrying this pilot\'s own flame palette, in GREEN'
                    % pilot.upper(), font=F, fill=(255, 226, 140))
            for r in range(ROWS):
                for c in range(COLS):
                    a, al, _ = cs[(r, c)]
                    n, m = lit(a, al, pal)
                    o = np.full(a.shape, (24, 24, 30), np.uint8)
                    o[al] = a[al]
                    o[m] = (0, 255, 90)
                    S.paste(Image.fromarray(o), (4 + c * T, 24 + r * (T + 20)))
                    dr.text((6 + c * T, 24 + r * (T + 20) + T + 2), 'r%dc%d  %d px' % (r, c, n),
                            font=F, fill=(150, 160, 200) if n >= MIN_BLOB else (255, 110, 110))
            S.save(os.path.join(ROOT, 'docs/MISSING_EXHAUST_%s_0907R.png' % pilot.upper()))
            print('             wrote docs/MISSING_EXHAUST_%s_0907R.png' % pilot.upper())
    print()
    print('%d cells across %d pilots have no lit exhaust' % (missing_total, len(want)))
    json.dump(rep, open(os.path.join(ROOT, 'docs/MISSING_EXHAUST_0907R.json'), 'w'), indent=1)
    print('wrote docs/MISSING_EXHAUST_0907R.json')
    return 0


if __name__ == '__main__':
    sys.exit(main())
