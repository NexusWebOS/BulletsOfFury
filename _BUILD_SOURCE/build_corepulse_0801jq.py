#!/usr/bin/env python3
"""
DROP 0801jq - THE CORE PULSES FROM ITS CENTRE LINE, AND THE ARMOUR POWERS ON

Mike: "dont forget to make the core itself pulsate and spread inside. especialy the
line in the middle bright. and dont forget the that when he activates, the armor
powers on so his torso pulsates."

TWO THINGS, SEPARATE

  nqm_corepulse_0..7   the core pulsing OUTWARD FROM ITS CENTRE LINE. Measured, the
                       core is 1726 px in a column at x 92..182 with a bright spine
                       of 242 px running down x=136. The pulse starts on that spine
                       and spreads sideways, so the line is always the hottest part
                       and the glow blooms off it - rather than the whole column
                       brightening as one lump.

  nqm_armor_0..7       the ARMOUR coming online. This is the plating, not the core:
                       every non-vein, non-core pixel of the torso, breathing on a
                       slower clock so it reads as the shell energising underneath
                       the lights rather than competing with them.

Both are dithered before a 12-step quantise, so they band.
"""
import os
import re
import numpy as np
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
OUT = 'assets/enemies/boss/magma'
N = 8
BAYER = np.array([[0, 8, 2, 10], [12, 4, 14, 6],
                  [3, 11, 1, 9], [15, 7, 13, 5]], dtype=float) / 16.0


def main():
    man_path = os.path.join(ROOT, 'assets/manifest.js')
    man = open(man_path, encoding='utf-8').read()
    a0 = np.array(Image.open(os.path.join(ROOT, re.search(r'"mbg2_m_torso":"([^"]+)"', man).group(1))).convert('RGBA')).astype(float)
    H, W = a0.shape[:2]
    op = a0[..., 3] > 16
    r, g, b = a0[..., 0], a0[..., 1], a0[..., 2]
    yy, xx = np.mgrid[0:H, 0:W]
    bay = np.tile(BAYER, (H // 4 + 1, W // 4 + 1))[:H, :W]

    core = op & (r > 190) & (g > 120) & (b < 140) & (r > b + 80) & (np.abs(xx - W // 2) < 46)
    lum = 0.299 * r + 0.587 * g + 0.114 * b
    spine = core & (lum > np.percentile(lum[core], 86))
    sx = int(np.where(spine)[1].mean())
    print('  core %d px, spine %d px on x=%d' % (int(core.sum()), int(spine.sum()), sx))

    def quant(a, m):
        step = 255.0 / 11
        for c in range(3):
            ch = a[..., c] + (bay - 0.5) * step * 0.9
            a[..., c] = np.where(m, np.clip(np.round(ch / step) * step, 0, 255), a[..., c])
        return a

    add = {}
    os.makedirs(os.path.join(ROOT, OUT), exist_ok=True)

    # ---- 1. THE CORE PULSES OUT FROM ITS SPINE ----
    dx = np.abs(xx - sx)
    maxd = float(dx[core].max()) or 1.0
    for i in range(N):
        t = i / float(N)
        a = a0.copy()
        # the wave leaves the spine and travels sideways; the spine itself never
        # drops below full brightness, so the line stays the hottest thing
        # A SINE REPEATS ITS VALUES (drop 0801jq). sin(t*2pi) returns the same number
        # twice per cycle, so frames came out byte-identical - the fourth time this
        # pattern has bitten me today. A rising ramp with a soft ease gives eight
        # distinct steps and still loops, because the wave leaving the spine is a
        # travelling front, not a breath.
        reach = maxd * (0.14 + 0.94 * (t ** 0.85))
        wave = np.clip(1.0 - np.abs(dx - reach) / 13.0, 0, 1)
        near = np.clip(1.0 - dx / max(1.0, reach), 0, 1) ** 1.4
        amt = np.clip(wave * 0.9 + near * 0.55, 0, 1) * core
        for c, tgt in zip(range(3), (255, 214, 140)):
            a[..., c] = np.clip(a[..., c] * (1 - amt) + tgt * amt, 0, 255)
        # the spine, always hottest
        for c, tgt in zip(range(3), (255, 250, 224)):
            a[..., c] = np.where(spine, np.clip(a[..., c] * 0.22 + tgt * 0.78, 0, 255), a[..., c])
        a = quant(a, op)
        k = 'nqm_corepulse_%d' % i
        rel = '%s/%s.png' % (OUT, k)
        Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA').save(os.path.join(ROOT, rel))
        add[k] = rel

    # ---- 2. THE ARMOUR POWERS ON ----
    vein = op & (r > 150) & (r > g + 60) & (r > b + 90)
    plate = op & ~core & ~vein
    print('  armour plating: %d px' % int(plate.sum()))
    for i in range(N):
        t = i / float(N)
        a = a0.copy()
        # a slow breath, brightest at the rim so the shell reads as charged rather
        # than the sprite being turned up
        from scipy import ndimage
        rim = ndimage.binary_dilation(op, iterations=2) & ~ndimage.binary_erosion(op, iterations=2)
        # same fix: a ramp, not a sine
        pulse = t ** 0.9
        amt = (0.16 + 0.34 * pulse) * plate + (0.22 * pulse) * (plate & rim)
        for c, tgt in zip(range(3), (255, 196, 122)):
            a[..., c] = np.clip(a[..., c] * (1 - amt) + tgt * amt, 0, 255)
        a = quant(a, op)
        k = 'nqm_armor_%d' % i
        rel = '%s/%s.png' % (OUT, k)
        Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA').save(os.path.join(ROOT, rel))
        add[k] = rel

    new = ''.join('"%s":"%s",' % (k, v) for k, v in sorted(add.items())
                  if ('"%s":' % k) not in man)
    if new:
        i = man.index('window.BOFX={"img":{') + len('window.BOFX={"img":{')
        open(man_path, 'w', encoding='utf-8').write(man[:i] + new + man[i:])

    man2 = open(man_path, encoding='utf-8').read()
    for fam in ['nqm_corepulse', 'nqm_armor']:
        fr = [np.array(Image.open(os.path.join(ROOT, re.search(r'"%s_%d":"([^"]+)"' % (fam, i), man2).group(1))).convert('RGBA')).astype(int)
              for i in range(N)]
        d = [int((np.abs(fr[i][..., :3] - fr[0][..., :3]).sum(axis=2) > 18).sum()) for i in range(1, N)]
        print('  %-14s changing %d-%d   duplicate frame: %s' % (fam, min(d), max(d), 0 in d))


if __name__ == '__main__':
    main()
