#!/usr/bin/env python3
"""
DROP 0801ka - ONE SLOT AT A TIME

Mike: "use the plates. but slice out | pieces to you can fill up the bar 1 slot at
a time in-game."

WHAT IS THERE
nmb_fill_<st>_<f> is 326x33 and already contains TEN discrete cells - measured as
solid runs at (8,36) (40,68) (72,100) (104,131) ... on a 32px pitch. Those are the
slots. They only ever read as one bar because the plate was drawn whole and clipped.

WHAT THIS BUILDS
  nbs_slot_<st>_<f>    a single cell, cut from the run the artist drew
  nbs_gap_<st>         the dark inter-cell gap, for drawing empty slots

The game then draws N slots for N units of health, so the gauge steps rather than
sliding - which is what a slot bar should do, and what the art was made for.

The BOSS plate has no cells - one unbroken run from x 108..403 - so its slots are
derived from the miniboss pitch scaled to the boss bar's fill span, keeping the
same rhythm across both.
"""
import os
import re
import numpy as np
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
OUT = 'assets/ui/bars'
SLOTS = 10


def runs_of(op_cols):
    out, cur, st = [], False, 0
    for x, v in enumerate(op_cols > 0):
        if v != cur:
            if cur:
                out.append((st, x - 1))
            cur, st = v, x
    if cur:
        out.append((st, len(op_cols) - 1))
    return out


def main():
    man_path = os.path.join(ROOT, 'assets/manifest.js')
    man = open(man_path, encoding='utf-8').read()
    os.makedirs(os.path.join(ROOT, OUT), exist_ok=True)
    add = {}
    meta = {}

    for st in range(1, 9):
        for f in range(8):
            k = 'nmb_fill_%d_%d' % (st, f)
            m = re.search(r'"%s":"([^"]+)"' % k, man)
            if not m:
                continue
            p = os.path.join(ROOT, m.group(1))
            if not os.path.exists(p):
                continue
            a = np.array(Image.open(p).convert('RGBA'))
            op = (a[..., 3] > 16).astype(float)
            rr = runs_of(op.sum(axis=0))
            if len(rr) < 4:
                continue
            # take a MIDDLE cell - the first and last can carry end-cap shaping
            x0, x1 = rr[len(rr) // 2]
            cell = a[:, x0:x1 + 1]
            # trim vertically to the cell's own art
            ys = np.where((cell[..., 3] > 16).any(axis=1))[0]
            if len(ys):
                cell = cell[ys.min():ys.max() + 1]
            kk = 'nbs_slot_%d_%d' % (st, f)
            rel = '%s/%s.png' % (OUT, kk)
            Image.fromarray(cell, 'RGBA').save(os.path.join(ROOT, rel))
            add[kk] = rel
            if f == 0:
                pitch = (rr[1][0] - rr[0][0]) if len(rr) > 1 else (x1 - x0 + 1)
                meta[st] = {'cells': len(rr), 'pitch': int(pitch),
                            'w': int(cell.shape[1]), 'h': int(cell.shape[0]),
                            'first': int(rr[0][0]), 'plate': int(a.shape[1])}

    new = ''.join('"%s":"%s",' % (k, v) for k, v in sorted(add.items())
                  if ('"%s":' % k) not in man)
    if new:
        i = man.index('window.BOFX={"img":{') + len('window.BOFX={"img":{')
        open(man_path, 'w', encoding='utf-8').write(man[:i] + new + man[i:])

    print('  cut %d slot plates' % len(add))
    for st in sorted(meta):
        d = meta[st]
        print('   stage %d  %2d cells  pitch %2dpx  slot %dx%d  first at x=%d of %d'
              % (st, d['cells'], d['pitch'], d['w'], d['h'], d['first'], d['plate']))


if __name__ == '__main__':
    main()
