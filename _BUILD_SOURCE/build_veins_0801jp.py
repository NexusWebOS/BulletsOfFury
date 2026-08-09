#!/usr/bin/env python3
"""
DROP 0801jp - THE MAGMA VEINS, ON EVERY PIECE

Mike: "theres also magma in his shoulders/arms"

He is right, and it is not only the arms. Measured across the whole rig:

  torso                4692 px   7.2%
  left-upper-arm       1630 px   4.2%
  right-upper-arm      1654 px   4.2%
  left-cannon-forearm  2577 px   9.6%     <- the richest
  right-cannon-forearm 2448 px   9.1%
  left-leg              929 px   3.0%
  right-leg            1009 px   3.2%
                      -------
                      14939 px total

My earlier pass lit the torso only, and even there it was masked to the outboard
shoulders. Every piece gets the treatment now.

ONE CLOCK, MANY PIECES
The light front is driven by a shared phase rather than each piece running its own,
so the current appears to travel THROUGH the machine - shoulder into arm into
cannon - instead of seven parts blinking independently. Each piece maps its own
vertical extent onto that shared front, which is what keeps them in step when they
are different heights.
"""
import os
import re
import numpy as np
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
OUT = 'assets/enemies/boss/magma/veins'
N = 8
BAYER = np.array([[0, 8, 2, 10], [12, 4, 14, 6],
                  [3, 11, 1, 9], [15, 7, 13, 5]], dtype=float) / 16.0

PIECES = {
    'torso': 'mbg2_m_torso',
    'arml': 'mbg2_m_left-upper-arm',
    'armr': 'mbg2_m_right-upper-arm',
    'canl': 'mbg2_m_left-cannon-forearm',
    'canr': 'mbg2_m_right-cannon-forearm',
    'legl': 'mbg2_m_left-leg',
    'legr': 'mbg2_m_right-leg',
}


def main():
    man_path = os.path.join(ROOT, 'assets/manifest.js')
    man = open(man_path, encoding='utf-8').read()
    os.makedirs(os.path.join(ROOT, OUT), exist_ok=True)
    add = {}
    total = 0

    for tag, key in PIECES.items():
        m = re.search(r'"%s":"([^"]+)"' % key, man)
        if not m:
            print('   %s missing' % key); continue
        a0 = np.array(Image.open(os.path.join(ROOT, m.group(1))).convert('RGBA')).astype(float)
        H, W = a0.shape[:2]
        op = a0[..., 3] > 16
        r, g, b = a0[..., 0], a0[..., 1], a0[..., 2]
        vein = op & (r > 150) & (r > g + 60) & (r > b + 90)
        if vein.sum() < 40:
            print('   %-6s no veins' % tag); continue
        total += int(vein.sum())

        yy, xx = np.mgrid[0:H, 0:W]
        bay = np.tile(BAYER, (H // 4 + 1, W // 4 + 1))[:H, :W]
        vy, _ = np.where(vein)
        # bound the travel to this piece's OWN veins, so no frame comes out dark -
        # a shared absolute range left short pieces unlit for half the reel
        Y0, Y1 = vy.max() + 34, vy.min() - 34

        for i in range(N):
            t = i / float(N - 1)
            a = a0.copy()
            front = Y0 + (Y1 - Y0) * t
            amt = np.clip(np.clip(1.4 - np.abs(yy - front) / 54.0, 0, 1.4), 0, 1) * vein
            for c, tgt in zip(range(3), (255, 226, 150)):
                a[..., c] = np.clip(a[..., c] * (1 - amt) + tgt * amt, 0, 255)
            step = 255.0 / 11
            for c in range(3):
                ch = a[..., c] + (bay - 0.5) * step * 0.9
                a[..., c] = np.where(op, np.clip(np.round(ch / step) * step, 0, 255), a[..., c])
            k = 'nqv_%s_%d' % (tag, i)
            rel = '%s/%s.png' % (OUT, k)
            Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA').save(os.path.join(ROOT, rel))
            add[k] = rel

        # prove no frame duplicates
        fr = [np.array(Image.open(os.path.join(ROOT, add['nqv_%s_%d' % (tag, i)])).convert('RGBA')).astype(int)
              for i in range(N)]
        d = [int((np.abs(fr[i][..., :3] - fr[0][..., :3]).sum(axis=2) > 18).sum()) for i in range(1, N)]
        print('   %-6s %5d veins   changing %s   dup:%s'
              % (tag, int(vein.sum()), '%d-%d' % (min(d), max(d)), 0 in d))

    new = ''.join('"%s":"%s",' % (k, v) for k, v in sorted(add.items())
                  if ('"%s":' % k) not in man)
    if new:
        i = man.index('window.BOFX={"img":{') + len('window.BOFX={"img":{')
        open(man_path, 'w', encoding='utf-8').write(man[:i] + new + man[i:])
    print('  %d frames across %d pieces, %d vein px lit in total'
          % (len(add), len(PIECES), total))


if __name__ == '__main__':
    main()
