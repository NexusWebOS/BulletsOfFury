#!/usr/bin/env python3
"""
DROP 0801iu - THE FUSION CORE ANIMATION

Mike: "see his fusion core? part of the animation for the torso only - the middle
yellow light part, you make it light up from bottom to top, then the whole core
spreads a bright orange/white flash left and right lke a split from that middle
line."

TWO BEATS, IN ORDER

  1. CHARGE   nqm_core_up_0..7
     the middle column lights from the BOTTOM UP - a band of brightness climbing
     the core, so it reads as power gathering rather than a lamp switching on

  2. SPLIT    nqm_core_split_0..7
     the whole core then throws a bright orange/white flash LEFT and RIGHT, opening
     outward from that same centre line

FINDING THE CORE
Selected by colour, not by a box: the fusion column is the only strongly warm,
bright matter in the torso - r above 190, g above 120, b below 140. Measured, that
is 1726 px in a column at x 92..182, dead centre. Everything outside that column is
left alone, so the armour never lights up with it.

The split flash is masked to the core's own rows so it opens along the machine's
midline rather than washing the whole sprite.
"""
import os
import re
import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
OUT = 'assets/enemies/boss/magma'
N = 8


def main():
    man_path = os.path.join(ROOT, 'assets/manifest.js')
    man = open(man_path, encoding='utf-8').read()
    m = re.search(r'"mbg2_m_torso":"([^"]+)"', man)
    base = np.array(Image.open(os.path.join(ROOT, m.group(1))).convert('RGBA')).astype(float)
    H, W = base.shape[:2]
    op = base[..., 3] > 16
    r, g, b = base[..., 0], base[..., 1], base[..., 2]

    warm = op & (r > 190) & (g > 120) & (b < 140) & (r > b + 80)
    yy, xx = np.mgrid[0:H, 0:W]
    core = warm & (np.abs(xx - W // 2) < 46)
    if not core.any():
        print('  no core found'); return
    cys, cxs = np.where(core)
    y0, y1 = cys.min(), cys.max()
    print('  core: %d px, x %d..%d, y %d..%d' % (int(core.sum()), cxs.min(), cxs.max(), y0, y1))

    os.makedirs(os.path.join(ROOT, OUT), exist_ok=True)
    add = {}

    # ---- 1. CHARGE: a band climbing from the bottom ----
    span = float(y1 - y0) or 1.0
    for i in range(N):
        t = i / float(N - 1)
        a = base.copy()
        # the band sits at (1-t) down the core and is brightest at its centre
        headY = y1 - span * t
        dist = np.abs(yy - headY) / max(1.0, span * 0.30)
        lift = np.clip(1.8 - dist, 0, 1.8)
        # below the band the core is already lit; above it is still cold
        lit = np.where(yy > headY, 1.25, 0.55) + lift
        for c in range(3):
            a[..., c] = np.where(core, np.clip(base[..., c] * lit, 0, 255), base[..., c])
        # the leading edge blows out toward white
        hot = core & (lift > 1.1)
        for c, tgt in zip(range(3), (255, 246, 208)):
            a[..., c] = np.where(hot, np.clip(a[..., c] * 0.35 + tgt * 0.65, 0, 255), a[..., c])
        k = 'nqm_core_up_%d' % i
        rel = '%s/%s.png' % (OUT, k)
        Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA').save(os.path.join(ROOT, rel))
        add[k] = rel

    # ---- 2. SPLIT: the flash opening left and right ----
    coreRows = np.zeros(H, dtype=bool)
    coreRows[y0:y1 + 1] = True
    rowMask = op & coreRows[:, None]
    cx = W // 2
    for i in range(N):
        t = i / float(N - 1)
        a = base.copy()
        reach = 6 + (W * 0.52) * t                 # opens outward from the midline
        d = np.abs(xx - cx)
        edge = np.clip(1.0 - np.abs(d - reach) / 26.0, 0, 1)   # a moving bright rim
        inside = (d < reach)
        fade = np.clip(1.0 - t * 0.55, 0, 1)
        amt = (inside * 0.62 * fade + edge * 0.95) * rowMask
        for c, tgt in zip(range(3), (255, 214, 150)):
            a[..., c] = np.clip(base[..., c] * (1 - amt) + tgt * amt, 0, 255)
        # the core itself stays hottest through the whole split
        for c, tgt in zip(range(3), (255, 250, 226)):
            a[..., c] = np.where(core, np.clip(a[..., c] * 0.30 + tgt * 0.70, 0, 255), a[..., c])
        k = 'nqm_core_split_%d' % i
        rel = '%s/%s.png' % (OUT, k)
        Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA').save(os.path.join(ROOT, rel))
        add[k] = rel

    new = ''.join('"%s":"%s",' % (k, v) for k, v in sorted(add.items())
                  if ('"%s":' % k) not in man)
    if new:
        i = man.index('window.BOFX={"img":{') + len('window.BOFX={"img":{')
        open(man_path, 'w', encoding='utf-8').write(man[:i] + new + man[i:])
    print('  %d charge frames + %d split frames' % (N, N))

    # prove the charge actually climbs
    man2 = open(man_path, encoding='utf-8').read()
    cent = []
    for i in range(N):
        p = os.path.join(ROOT, re.search(r'"nqm_core_up_%d":"([^"]+)"' % i, man2).group(1))
        a = np.array(Image.open(p).convert('RGBA')).astype(float)
        d = np.clip((a[..., :3] - base[..., :3]).sum(axis=2), 0, None)
        cent.append(round(float((d * yy).sum() / max(1.0, d.sum())) / H, 3) if d.sum() else None)
    print('  charge centroid per frame (falling = climbing UP): %s' % cent)


if __name__ == '__main__':
    main()
