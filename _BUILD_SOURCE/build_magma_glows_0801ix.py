#!/usr/bin/env python3
"""
DROP 0801ix - THREE SEPARATE GLOW LAYERS

Mike: "uhh, still need the split armor glow, a seperate eye glow for him thats
red/white, and the core needs to glow on its own."

Three layers, each independent, so the fight can run them in any combination:

  nqm_split_0..7    THE ARMOUR SPLIT - a bright orange/white flash opening LEFT and
                    RIGHT from the machine's midline, across the whole body. This is
                    the beat Mike described after the core charges.

  nqm_eyes_0..7     THE EYES - red into white, on the head only. Separate from the
                    shield so the eyes can burn while the body does something else,
                    which the intro needs at step 12 ("the eyes turn on").

  nqm_corelit_0..7  THE CORE ON ITS OWN - the fusion column pulsing by itself with
                    no shield and no body flash, for the intro's power-on.

All three are 16-bit: ordered dither applied BEFORE a 12-step quantise, which is
what gives banding rather than a smooth modern bloom.
"""
import os
import re
import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
OUT = 'assets/enemies/boss/magma'
N = 8
BAYER = np.array([[0, 8, 2, 10], [12, 4, 14, 6],
                  [3, 11, 1, 9], [15, 7, 13, 5]], dtype=float) / 16.0
LEVELS = 12


def quantise(a, op, bay):
    """Dither, then snap. The order is the whole point."""
    step = 255.0 / (LEVELS - 1)
    for c in range(3):
        ch = a[..., c] + (bay - 0.5) * step * 0.9
        a[..., c] = np.where(op, np.clip(np.round(ch / step) * step, 0, 255), a[..., c])
    return a


def main():
    man_path = os.path.join(ROOT, 'assets/manifest.js')
    man = open(man_path, encoding='utf-8').read()
    seat = np.array(Image.open(os.path.join(ROOT, re.search(r'"mgx_torso_head":"([^"]+)"', man).group(1))).convert('RGBA')).astype(float)
    head = np.array(Image.open(os.path.join(ROOT, re.search(r'"mgx_head":"([^"]+)"', man).group(1))).convert('RGBA')).astype(float)
    H, W = seat.shape[:2]
    op = seat[..., 3] > 16
    yy, xx = np.mgrid[0:H, 0:W]
    bay = np.tile(BAYER, (H // 4 + 1, W // 4 + 1))[:H, :W]
    add = {}

    # ---------- 1. ARMOUR SPLIT ----------
    cx = W // 2
    for i in range(N):
        t = i / float(N - 1)
        a = seat.copy()
        reach = 4 + (W * 0.58) * t
        d = np.abs(xx - cx)
        edge = np.clip(1.0 - np.abs(d - reach) / 22.0, 0, 1)     # the travelling rim
        inside = (d < reach) * np.clip(1.0 - t * 0.5, 0, 1)
        amt = np.clip(inside * 0.55 + edge * 1.0, 0, 1) * op
        for c, tgt in zip(range(3), (255, 208, 132)):
            a[..., c] = np.clip(seat[..., c] * (1 - amt) + tgt * amt, 0, 255)
        # the leading rim goes white-hot
        hot = op & (edge > 0.72)
        for c, tgt in zip(range(3), (255, 250, 232)):
            a[..., c] = np.where(hot, tgt, a[..., c])
        a = quantise(a, op, bay)
        k = 'nqm_split_%d' % i
        rel = '%s/%s.png' % (OUT, k)
        Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA').save(os.path.join(ROOT, rel))
        add[k] = rel

    # ---------- 2. THE EYES, red into white ----------
    hh, hw = head.shape[:2]
    hop = head[..., 3] > 16
    hyy, hxx = np.mgrid[0:hh, 0:hw]
    hbay = np.tile(BAYER, (hh // 4 + 1, hw // 4 + 1))[:hh, :hw]
    # two sockets either side of centre, in the upper-middle of the face
    exL, exR, ey = int(hw * 0.36), int(hw * 0.64), int(hh * 0.45)
    rad = max(5.0, hw * 0.115)
    dL = np.hypot(hxx - exL, (hyy - ey) * 1.35)
    dR = np.hypot(hxx - exR, (hyy - ey) * 1.35)
    socket = hop & ((dL < rad) | (dR < rad))
    print('  eye sockets: %d px, centres (%d,%d) and (%d,%d) r=%.0f'
          % (int(socket.sum()), exL, ey, exR, ey, rad))
    for i in range(N):
        t = i / float(N - 1)
        a = head.copy()
        core = np.clip(1.0 - np.minimum(dL, dR) / rad, 0, 1) ** 1.5
        lit = np.clip(core * (0.35 + 0.85 * t), 0, 1) * hop
        # RED at the rim, WHITE at the centre - Mike asked for red/white
        for c, (rim, mid) in enumerate([(232, 255), (28, 244), (24, 226)]):
            tgt = rim + (mid - rim) * np.clip(core * 1.25, 0, 1)
            a[..., c] = np.clip(head[..., c] * (1 - lit) + tgt * lit, 0, 255)
        a = quantise(a, hop, hbay)
        k = 'nqm_eyes_%d' % i
        rel = '%s/%s.png' % (OUT, k)
        Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA').save(os.path.join(ROOT, rel))
        add[k] = rel

    # ---------- 3. THE CORE, alone ----------
    r, g, b = seat[..., 0], seat[..., 1], seat[..., 2]
    warm = op & (r > 190) & (g > 120) & (b < 140) & (r > b + 80)
    core = warm & (np.abs(xx - cx) < 46)
    for i in range(N):
        t = i / float(N)
        a = seat.copy()
        pulse = (t ** 0.8) * 0.88 + 0.12
        lit = np.clip(pulse, 0, 1) * core
        for c, tgt in zip(range(3), (255, 216, 128)):
            a[..., c] = np.clip(seat[..., c] * (1 - lit * 0.9) + tgt * lit * 0.9, 0, 255)
        hot = core & (pulse > 0.72)
        for c, tgt in zip(range(3), (255, 252, 226)):
            a[..., c] = np.where(hot, np.clip(a[..., c] * 0.3 + tgt * 0.7, 0, 255), a[..., c])
        a = quantise(a, op, bay)
        k = 'nqm_corelit_%d' % i
        rel = '%s/%s.png' % (OUT, k)
        Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA').save(os.path.join(ROOT, rel))
        add[k] = rel

    new = ''.join('"%s":"%s",' % (k, v) for k, v in sorted(add.items())
                  if ('"%s":' % k) not in man)
    if new:
        i = man.index('window.BOFX={"img":{') + len('window.BOFX={"img":{')
        open(man_path, 'w', encoding='utf-8').write(man[:i] + new + man[i:])
    print('  %d keys: split, eyes, corelit - 8 frames each' % len(add))

    man2 = open(man_path, encoding='utf-8').read()
    import collections
    for fam in ['nqm_split_3', 'nqm_eyes_6', 'nqm_corelit_5']:
        p = os.path.join(ROOT, re.search(r'"%s":"([^"]+)"' % fam, man2).group(1))
        a = np.array(Image.open(p).convert('RGBA'))
        px = a[..., :3][a[..., 3] > 16]
        print('   %-16s %d distinct colours' % (fam, len(collections.Counter(map(tuple, px)))))


if __name__ == '__main__':
    main()
