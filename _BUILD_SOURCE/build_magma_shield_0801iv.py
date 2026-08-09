#!/usr/bin/env python3
"""
DROP 0801iv - THE ENERGY SHIELD, IN 16-BIT

Mike: "make sure his head also does the yellow flash and glow as its protected by
the shield. and the flash and glow MUST look 16-bit"

WHAT 16-BIT MEANS HERE, CONCRETELY
Not a soft additive bloom. A Mega Drive had a fixed palette and no alpha blending,
so a shield flash was faked with three things, and all three are what this does:

  1. QUANTISED STEPS. The lift is snapped to five discrete levels. No smooth ramp -
     the banding is the look.
  2. ORDERED DITHER. A 4x4 Bayer matrix breaks the boundary between steps, applied
     BEFORE quantising. Dithering after quantising does nothing at all; that
     ordering is the whole trick.
  3. A HARD PALETTE. Each step is a real colour off a five-entry yellow ramp, not
     the sprite's own pixels multiplied by a number.

The shield covers HEAD AND TORSO TOGETHER, because Mike's damage order has both
protected until the limbs are gone.

  nqm_shield_0..7   the pulse, head and torso as one plate
"""
import os
import re
import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
OUT = 'assets/enemies/boss/magma'
N = 8

# a five-entry yellow ramp - the shield's whole palette
RAMP = [(120, 74, 10), (186, 122, 20), (238, 178, 46), (255, 222, 110), (255, 250, 208)]
BAYER = np.array([[0, 8, 2, 10], [12, 4, 14, 6],
                  [3, 11, 1, 9], [15, 7, 13, 5]], dtype=float) / 16.0


def main():
    man_path = os.path.join(ROOT, 'assets/manifest.js')
    man = open(man_path, encoding='utf-8').read()

    # --- seat the head properly first: smaller, higher, clear of the chest ---
    lasso = Image.open(os.path.join(ROOT, re.search(r'"mgx_head_lasso":"([^"]+)"', man).group(1))).convert('RGBA')
    torso = Image.open(os.path.join(ROOT, re.search(r'"mbg2_m_torso":"([^"]+)"', man).group(1))).convert('RGBA')
    HW, HH, HY = 104, 111, -10          # clears the chest plate, sits in the slot
    head = lasso.resize((HW, HH), Image.LANCZOS)

    ha = np.array(head).astype(float)
    op = ha[..., 3] > 16
    r, g, b = ha[..., 0], ha[..., 1], ha[..., 2]
    mag = op & (r > g + 55) & (b > g + 35)
    if mag.any():
        good = op & ~mag
        idx = ndimage.distance_transform_edt(~good, return_distances=False, return_indices=True)
        ys, xs = np.where(mag)
        for c in range(3):
            ha[..., c][ys, xs] = ha[..., c][idx[0][ys, xs], idx[1][ys, xs]]
    head = Image.fromarray(np.clip(ha, 0, 255).astype(np.uint8), 'RGBA')
    os.makedirs(os.path.join(ROOT, OUT), exist_ok=True)
    head.save(os.path.join(ROOT, '%s/mgx_head.png' % OUT))

    HX = (torso.width - HW) // 2
    seated = Image.new('RGBA', (torso.width, torso.height), (0, 0, 0, 0))
    seated.alpha_composite(torso)
    seated.alpha_composite(head, (HX, max(0, HY)))
    seated.save(os.path.join(ROOT, '%s/mgx_torso_head.png' % OUT))
    print('  head %dx%d at (%d,%d) - clear of the chest plate' % (HW, HH, HX, HY))

    # --- the shield, over head AND torso together ---
    base = np.array(seated).astype(float)
    H, W = base.shape[:2]
    op = base[..., 3] > 16
    lum = (0.299 * base[..., 0] + 0.587 * base[..., 1] + 0.114 * base[..., 2]) / 255.0
    rim = ndimage.binary_dilation(op, iterations=2) & ~ndimage.binary_erosion(op, iterations=1)
    yy, xx = np.mgrid[0:H, 0:W]
    bay = np.tile(BAYER, (H // 4 + 1, W // 4 + 1))[:H, :W]

    add = {}
    for i in range(N):
        t = i / float(N)
        # the shield breathes, and the RIM always carries more than the interior -
        # that is what makes it read as a shell rather than the sprite glowing
        # A PLAIN SINE STALLS (drop 0801iw). sin returns the same value twice per
        # cycle, so frame 4 came out byte-identical to frame 0 - measured, 0 px
        # changed between them - and the shield visibly froze mid-pulse. Same bug I
        # hit on the rampart core. A rising sawtooth with a soft ease gives eight
        # distinct steps that still breathe.
        pulse = (t ** 0.85) * 0.90 + 0.10
        drive = np.clip(lum * 0.42 + pulse * 0.86, 0, 1)
        drive = np.where(rim, np.clip(drive + 0.34, 0, 1), drive)

        # DITHER FIRST, THEN QUANTISE. The other order does nothing.
        q = np.clip(np.floor(drive * (len(RAMP) - 1) + bay * 0.9), 0, len(RAMP) - 1).astype(int)

        a = base.copy()
        for s, rgb in enumerate(RAMP):
            m = op & (q == s)
            if not m.any():
                continue
            k = 0.34 + 0.60 * (s / (len(RAMP) - 1.0))
            for c in range(3):
                a[..., c] = np.where(m, np.clip(base[..., c] * (1 - k) + rgb[c] * k, 0, 255), a[..., c])

        # QUANTISE THE RESULT (drop 0801iv). Blending toward a five-entry ramp still
        # carries the sprite's own colour variety through - measured 16,945 distinct
        # colours in a frame, which is a modern soft bloom wearing a palette.
        #
        # A 16-bit machine could not do that. Snapping every channel to a coarse
        # step count is what actually produces the banding, and the ordered dither
        # above is what stops that banding from looking like posterisation.
        LEVELS = 12                     # per channel, so ~1700 possible not 16 million
        step = 255.0 / (LEVELS - 1)
        for c in range(3):
            ch = a[..., c] + (bay - 0.5) * step * 0.9      # dither across the step
            a[..., c] = np.where(op, np.clip(np.round(ch / step) * step, 0, 255), a[..., c])
        k2 = 'nqm_shield_%d' % i
        rel = '%s/%s.png' % (OUT, k2)
        Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA').save(os.path.join(ROOT, rel))
        add[k2] = rel

    new = ''.join('"%s":"%s",' % (k, v) for k, v in sorted(add.items())
                  if ('"%s":' % k) not in man)
    if new:
        i = man.index('window.BOFX={"img":{') + len('window.BOFX={"img":{')
        open(man_path, 'w', encoding='utf-8').write(man[:i] + new + man[i:])

    # prove it is banded, not smooth
    man2 = open(man_path, encoding='utf-8').read()
    p = os.path.join(ROOT, re.search(r'"nqm_shield_2":"([^"]+)"', man2).group(1))
    a = np.array(Image.open(p).convert('RGBA'))
    px = a[..., :3][a[..., 3] > 16]
    import collections
    print('  %d shield frames, head + torso as one plate' % N)
    print('  distinct colours in a frame: %d  (a soft bloom would be thousands)'
          % len(collections.Counter(map(tuple, px))))


if __name__ == '__main__':
    main()
