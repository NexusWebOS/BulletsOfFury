#!/usr/bin/env python3
"""
DROP 0801jd - LONG CHAINS FROM THE FOUR LINK PIECES

Mike: "just use the chains and form long chain graphics. remove all purple halo's
and magenta. on the chain dialognial up, you have frame spill on the right side of
the frame. remove that. then, you will have your 4 pieces to make all chains. a long
chain should be about 6-10 of those link graphics carefully placed together"

THE SPILL
nch_du_0 carries a 1380px fragment at x=176 - the right edge of its source frame,
where the next cell of the sheet bled in. nch_du_1 has a smaller one at x=0.
Anything not part of the main link is dropped.

THE FOUR PIECES
  nch_h    horizontal   168 x  75
  nch_v    vertical      78 x 181
  nch_du   diagonal up  191 x 178
  nch_dd   diagonal dn  160 x 175

WHAT GETS BUILT
Each piece is tiled 6, 8 and 10 times along its own axis, with the overlap measured
from the link art rather than guessed - the pitch is found by sliding one copy over
another until the seam lines up, so the links interlock the way the artist drew them
instead of butting end to end.

  nchl_h_6 / _8 / _10        and the same for v, du, dd
"""
import os
import re
import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
OUT = 'assets/enemies/boss/magma/chainkit'
LENGTHS = [6, 8, 10]


def clean(a):
    """Drop frame spill, then any magenta or purple rim."""
    op = a[..., 3] > 16
    lab, n = ndimage.label(op)
    dropped = 0
    if n > 1:
        sizes = ndimage.sum(op, lab, range(1, n + 1))
        main = int(np.argmax(sizes)) + 1
        for j in range(1, n + 1):
            if j == main:
                continue
            m = (lab == j)
            a[..., 3][m] = 0
            dropped += int(m.sum())
    op = a[..., 3] > 16
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    bad = op & (((r > g + 55) & (b > g + 35)) | ((b > g + 22) & (r > g + 14)))
    healed = 0
    if bad.any():
        good = op & ~bad
        if good.any():
            idx = ndimage.distance_transform_edt(~good, return_distances=False, return_indices=True)
            ys, xs = np.where(bad)
            for c in range(3):
                a[..., c][ys, xs] = a[..., c][idx[0][ys, xs], idx[1][ys, xs]]
            healed = int(bad.sum())
    ys, xs = np.where(a[..., 3] > 16)
    if len(ys):
        a = a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    return a, dropped, healed


def find_pitch(im, axis):
    """Slide a copy over the original and take the offset where the overlap is
    tightest - that is the link pitch the artist drew, not a guess."""
    a = np.array(im)
    op = (a[..., 3] > 16).astype(float)
    n = op.shape[1] if axis == 'x' else op.shape[0]
    best, bestScore = int(n * 0.62), -1
    for off in range(int(n * 0.35), int(n * 0.95)):
        if axis == 'x':
            oa, ob = op[:, off:], op[:, :n - off]
        else:
            oa, ob = op[off:, :], op[:n - off, :]
        if oa.size == 0:
            continue
        # want the two edges to MEET: high overlap at the join, not a gap
        score = float((oa * ob).sum()) / max(1.0, oa.size)
        if score > bestScore:
            bestScore, best = score, off
    return best


def main():
    man_path = os.path.join(ROOT, 'assets/manifest.js')
    man = open(man_path, encoding='utf-8').read()
    os.makedirs(os.path.join(ROOT, OUT), exist_ok=True)
    add = {}
    totDrop = totHeal = 0

    PIECES = {'h': ('nch_h_0', 'x'), 'v': ('nch_v_0', 'y'),
              'du': ('nch_du_0', 'both-up'), 'dd': ('nch_dd_0', 'both-down')}

    for tag, (key, axis) in PIECES.items():
        m = re.search(r'"%s":"([^"]+)"' % key, man)
        if not m:
            print('   %s missing' % key); continue
        a = np.array(Image.open(os.path.join(ROOT, m.group(1))).convert('RGBA')).astype(float)
        a, dropped, healed = clean(a)
        totDrop += dropped; totHeal += healed
        link = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA')
        # write the cleaned single link back too
        Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA').save(
            os.path.join(ROOT, m.group(1)))
        print('   %-9s %3dx%-3d  spill dropped %4d  rim healed %4d'
              % (key, link.width, link.height, dropped, healed))

        for L in LENGTHS:
            if axis == 'x':
                pitch = find_pitch(link, 'x')
                W = pitch * (L - 1) + link.width
                H = link.height
                canvas = Image.new('RGBA', (W, H), (0, 0, 0, 0))
                for i in range(L):
                    canvas.alpha_composite(link, (i * pitch, 0))
            elif axis == 'y':
                pitch = find_pitch(link, 'y')
                W = link.width
                H = pitch * (L - 1) + link.height
                canvas = Image.new('RGBA', (W, H), (0, 0, 0, 0))
                for i in range(L):
                    canvas.alpha_composite(link, (0, i * pitch))
            else:
                px = find_pitch(link, 'x')
                py = find_pitch(link, 'y')
                up = axis.endswith('up')
                W = px * (L - 1) + link.width
                H = py * (L - 1) + link.height
                canvas = Image.new('RGBA', (W, H), (0, 0, 0, 0))
                for i in range(L):
                    y = (L - 1 - i) * py if up else i * py
                    canvas.alpha_composite(link, (i * px, y))
            k = 'nchl_%s_%d' % (tag, L)
            rel = '%s/%s.png' % (OUT, k)
            canvas.save(os.path.join(ROOT, rel))
            add[k] = rel

    new = ''.join('"%s":"%s",' % (k, v) for k, v in sorted(add.items())
                  if ('"%s":' % k) not in man)
    if new:
        i = man.index('window.BOFX={"img":{') + len('window.BOFX={"img":{')
        open(man_path, 'w', encoding='utf-8').write(man[:i] + new + man[i:])
    print('  %d long chains built (4 pieces x %s links)' % (len(add), LENGTHS))
    print('  total: %d px of frame spill dropped, %d px of rim healed' % (totDrop, totHeal))


if __name__ == '__main__':
    main()
