#!/usr/bin/env python3
"""
DROP 0801ir - LASSO THE MAGMA HEAD OFF ITS SHOULDERS

Mike: "with careful sprite manipulation, you can actually take his head piece, erase
the shoulders and purple halos. lasso his head instead of a square frame and it'll
seat perfectly on that slot on the torso. I just did it in ms-paint"

WHY A BOX WILL NOT DO
Measured down the head plate, the silhouette holds around 106-108px wide through
the skull and then jumps: 125 at y=84, 140 at y=90, 142 by y=96. Those last rows
are the shoulder yoke. A horizontal crop at the waist would take the shoulder
corners with it, because the skull's own jaw still overhangs there - which is
exactly the square-frame problem Mike is describing.

THE LASSO, DONE BY SHAPE
Erode the silhouette until the skull separates from the yoke, keep whichever piece
contains the head's centre of mass, then dilate that piece back INSIDE the original
alpha. The result follows the skull's real contour - the outline it was drawn with -
instead of a rectangle. Same thing a lasso does by hand, decided by the art.

Then the purple halo goes black rather than being deleted, per the standing rule.
"""
import os
import glob
import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
OUT = 'assets/enemies/boss/magma'


def main():
    src = glob.glob('/tmp/gbm/**/magma-colossus-modular-head.png', recursive=True)
    if not src:
        print('  no head plate'); return
    a = np.array(Image.open(src[0]).convert('RGBA')).astype(float)
    op = a[..., 3] > 16
    H, W = op.shape
    print('  head plate %dx%d, %d lit px' % (W, H, int(op.sum())))

    # EROSION WILL NOT SPLIT THIS ONE (drop 0801ir). Tried 2..25 iterations and the
    # skull never parted from the yoke - the neck is too thick relative to the head,
    # so the whole thing erodes away as one lump.
    #
    # The width profile does separate them cleanly though. Measured by row:
    #   y 36..78   holds 83..108 px      the skull
    #   y 84       jumps to 125          the yoke starts
    #   y 96+      142, the full plate   shoulders
    #
    # So: find the row where the silhouette widens sharply, take the skull's own
    # x-span at that row, and below it keep only what falls INSIDE that span. The
    # cut then follows the skull's vertical contour rather than a straight edge -
    # which is what a lasso does, and why a box crop takes the shoulder corners.
    widths = []
    for y in range(H):
        xs = np.where(op[y])[0]
        widths.append((xs.min(), xs.max(), len(xs)) if len(xs) else (0, 0, 0))

    waist = None
    for y in range(H // 3, H - 4):
        w_here = widths[y][1] - widths[y][0] + 1
        w_next = widths[y + 3][1] - widths[y + 3][0] + 1
        if w_here > 20 and w_next > w_here * 1.14:      # a sharp flare = the yoke
            waist = y
            break
    if waist is None:
        waist = int(H * 0.66)
    lx, rx = widths[waist][0], widths[waist][1]
    print('  waist at y=%d, skull spans x %d..%d there' % (waist, lx, rx))

    keep = op.copy()
    yy, xx = np.mgrid[0:H, 0:W]
    below = yy > waist
    # below the waist only the skull's own column range survives, and it tapers in
    # slightly so the jawline closes instead of running straight down
    taper = np.clip((yy - waist) * 0.55, 0, (rx - lx) * 0.34)
    keep &= ~(below & ((xx < lx + taper) | (xx > rx - taper)))
    # and nothing at all past a short chin
    keep &= ~(yy > waist + int((rx - lx) * 0.42))

    lab2, n2 = ndimage.label(keep)
    if n2 > 1:
        sz2 = ndimage.sum(keep, lab2, range(1, n2 + 1))
        keep = (lab2 == int(np.argmax(sz2)) + 1)
    grown = keep
    print('  kept %d px  (dropped %d px of shoulder yoke)'
          % (int(grown.sum()), int(op.sum() - grown.sum())))

    out = a.copy()
    out[..., 3] = np.where(grown, out[..., 3], 0)

    # 4. purple halo -> black, never deleted
    op2 = out[..., 3] > 16
    r, g, b = out[..., 0], out[..., 1], out[..., 2]
    pur = op2 & (b > g + 22) & (r > g + 14)
    for c in range(3):
        out[..., c] = np.where(pur, out[..., c] * 0.10, out[..., c])
    print('  purple darkened: %d px' % int(pur.sum()))

    ys, xs = np.where(out[..., 3] > 16)
    out = out[ys.min():ys.max() + 1, xs.min():xs.max() + 1]

    os.makedirs(os.path.join(ROOT, OUT), exist_ok=True)
    rel = '%s/mgx_head_lasso.png' % OUT
    Image.fromarray(np.clip(out, 0, 255).astype(np.uint8), 'RGBA').save(os.path.join(ROOT, rel))

    man_path = os.path.join(ROOT, 'assets/manifest.js')
    man = open(man_path, encoding='utf-8').read()
    if '"mgx_head_lasso"' not in man:
        i = man.index('window.BOFX={"img":{') + len('window.BOFX={"img":{')
        open(man_path, 'w', encoding='utf-8').write(
            man[:i] + '"mgx_head_lasso":"%s",' % rel + man[i:])
    print('  wrote mgx_head_lasso  %dx%d' % (out.shape[1], out.shape[0]))


if __name__ == '__main__':
    main()
