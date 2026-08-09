#!/usr/bin/env python3
"""
DROP 0801jb - THE CANNON PLATES COME OFF

Mike: "try to delete those plates on his cannons, and texture them with metal
sections from his cannon if possible, or use one of his magma sections to make it
look like it extends. but if so, the arm has to remain anchored where it is and just
make horizontal turns 45 degrees max."

WHAT THE PLATE IS
The pale tan block across the top of each cannon - the same low-saturation beige as
the disc at the torso's waist. It reads as a mounting flange, and with the cannon now
dangling below the shoulder pod it just gets in the way.

HOW IT IS REPLACED
Not erased - erased leaves a hole. The plate's rows are rebuilt from the cannon's OWN
barrel texture immediately below it, tiled upward. So the barrel appears to extend
through where the flange was, which is what Mike asked for, and every pixel comes from
the same sprite so the metal matches exactly.

THE 45 DEGREE NOTE
Mike's constraint is recorded in the anchors file: the arm stays where it is and the
cannon may only swing horizontally, 45 degrees maximum either side. That belongs to
the behaviour code, but the limit is written down next to the art so it is not lost.
"""
import os
import re
import json
import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
OUT = 'assets/enemies/boss/magma'
MAX_SWING = 45


def strip_plate(a):
    """Find the pale flange and rebuild it from the barrel below."""
    op = a[..., 3] > 16
    H, W = op.shape
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    mx = np.maximum(np.maximum(r, g), b)
    mn = np.minimum(np.minimum(r, g), b)
    sat = mx - mn

    # the flange: light, low-saturation, warm-neutral - and only in the top third,
    # because the barrel's own highlights look similar further down
    band = np.zeros_like(op)
    band[:int(H * 0.34)] = True
    # THE FLANGE IS DARKER THAN I ASSUMED (drop 0801jb). Sampled, it is RGB(105,87,66)
    # - value 105, saturation 39. My first test wanted mx > 118, so it caught 126 px
    # of highlight and left the whole plate standing. Tuned to what is actually there:
    # a warm mid-value neutral, red above blue but never far above it.
    plate = op & band & (mx > 74) & (mx < 168) & (sat < 58) & (r > b) & ((r - b) < 58)
    if plate.sum() < 40:
        return a, 0, 0

    # take the whole connected flange, not just the pixels that passed the colour
    # test, or the edges of it survive as a rim
    lab, n = ndimage.label(plate)
    if n:
        sizes = ndimage.sum(plate, lab, range(1, n + 1))
        keep = np.zeros_like(plate)
        for j in range(1, n + 1):
            if sizes[j - 1] > 30:
                keep |= (lab == j)
        plate = ndimage.binary_dilation(keep, iterations=2) & op

    ys, xs = np.where(plate)
    y0, y1 = ys.min(), ys.max()
    # the donor strip is the barrel immediately below the flange
    dh = max(6, (y1 - y0) + 4)
    d0, d1 = y1 + 2, min(H, y1 + 2 + dh)
    if d1 - d0 < 4:
        return a, 0, 0
    donor = a[d0:d1].copy()

    out = a.copy()
    for y in range(y0, y1 + 1):
        # tile the donor upward, mirroring alternate passes so the seam does not
        # repeat visibly
        k = (y1 - y) % (2 * donor.shape[0])
        if k < donor.shape[0]:
            src = donor[donor.shape[0] - 1 - k]
        else:
            src = donor[k - donor.shape[0]]
        m = plate[y]
        if not m.any():
            continue
        for c in range(4):
            out[y, m, c] = src[m, c]
    # keep the original silhouette: the flange sat inside it
    out[..., 3] = np.where(plate, a[..., 3], out[..., 3])
    return out, int(plate.sum()), (y1 - y0 + 1)


def main():
    man_path = os.path.join(ROOT, 'assets/manifest.js')
    man = open(man_path, encoding='utf-8').read()
    tot = 0
    for side in ['left', 'right']:
        k = 'mbg2_m_%s-cannon-forearm' % side
        m = re.search(r'"%s":"([^"]+)"' % k, man)
        if not m:
            continue
        p = os.path.join(ROOT, m.group(1))
        a = np.array(Image.open(p).convert('RGBA')).astype(float)
        out, n, rows = strip_plate(a)
        if n:
            Image.fromarray(np.clip(out, 0, 255).astype(np.uint8), 'RGBA').save(p)
            print('   %-30s plate %4d px over %d rows, rebuilt from the barrel'
                  % (side, n, rows))
            tot += n
        else:
            print('   %-30s no flange found' % side)
    print('  %d plate pixels replaced with the cannon\'s own metal' % tot)

    ap = os.path.join(ROOT, OUT, 'assembled_anchors.json')
    if os.path.exists(ap):
        d = json.load(open(ap))
        d['cannon_swing_deg'] = MAX_SWING
        d['cannon_note'] = ('arm stays anchored; the cannon may swing HORIZONTALLY '
                            'only, %d degrees maximum either side (Mike, 0801jb)' % MAX_SWING)
        json.dump(d, open(ap, 'w'), indent=1)
        print('  recorded the %d-degree horizontal swing limit in the anchors' % MAX_SWING)


if __name__ == '__main__':
    main()
