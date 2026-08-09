#!/usr/bin/env python3
"""
DROP 0801je - ONE LINK, MANY ANGLES

Mike: "you will have to make rotational frame pieces or rotate and make the chain
dangle somehow if possible. I've seen this in symphony of the night with Richter
Belmont's whip. you cut each chain link into it's own frame, and then your able to
flex the chain Im pretty sure thats how they did it"

That is exactly how it was done. A whip or chain is ONE link sprite drawn N times
along a curve, each copy rotated to the local tangent. The chain then bends, dangles
and swings for free, because nothing about it is baked.

CUTTING THE LINK
The kit's chains are single connected runs - the links overlap, so there is no blob
to separate. The repeat period comes out of an autocorrelation of the alpha profile
instead: 40px horizontally, 45px vertically. One period, cut from the middle of the
run where both neighbours are present, is a complete link with its own shading.

DOUBLED, per Mike
The link is scaled 2x so the boss can be hauled on chains that read at his size.
NEAREST, so the pixels stay hard.

  nchx_link        the doubled link, upright
  nchx_r00..r15    16 rotations, 22.5 degrees apart

Sixteen is enough that a chain following any curve never shows a visible step, and
few enough that the set stays small.
"""
import os
import re
import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
OUT = 'assets/enemies/boss/magma/chainkit'
ROTS = 16
SCALE = 2


def main():
    man_path = os.path.join(ROOT, 'assets/manifest.js')
    man = open(man_path, encoding='utf-8').read()
    m = re.search(r'"nch_v_0":"([^"]+)"', man)
    a = np.array(Image.open(os.path.join(ROOT, m.group(1))).convert('RGBA')).astype(float)
    H, W = a.shape[:2]

    # the vertical run gives an upright link, which is the natural rest pose for
    # something hanging
    # THE AUTOCORRELATION PERIOD WAS NOT THE LINK (drop 0801je). It reported 45px,
    # and cutting that from the middle took the WAIST of one link plus the ends of
    # the two beside it - a chunky block, not a link. The profile repeats at 45
    # because the link's two side rails cross the row that often; the link itself is
    # the full oval.
    #
    # nch_v_0 is 78x181 and holds about two and a half links, so the real pitch is
    # near 72. Taking one whole oval from the middle gives a link that can rotate.
    PERIOD = 72
    y0 = (H - PERIOD) // 2
    link = a[y0:y0 + PERIOD].copy()

    # trim to the link's own art
    op = link[..., 3] > 16
    ys, xs = np.where(op)
    link = link[ys.min():ys.max() + 1, xs.min():xs.max() + 1]

    # clean anything the cut exposed
    op = link[..., 3] > 16
    r, g, b = link[..., 0], link[..., 1], link[..., 2]
    bad = op & (((r > g + 55) & (b > g + 35)) | ((b > g + 22) & (r > g + 14)))
    if bad.any():
        good = op & ~bad
        idx = ndimage.distance_transform_edt(~good, return_distances=False, return_indices=True)
        ys2, xs2 = np.where(bad)
        for c in range(3):
            link[..., c][ys2, xs2] = link[..., c][idx[0][ys2, xs2], idx[1][ys2, xs2]]

    im = Image.fromarray(np.clip(link, 0, 255).astype(np.uint8), 'RGBA')
    im = im.resize((im.width * SCALE, im.height * SCALE), Image.NEAREST)
    print('  single link cut at period %d, doubled -> %dx%d' % (PERIOD, im.width, im.height))

    os.makedirs(os.path.join(ROOT, OUT), exist_ok=True)
    add = {}
    rel = '%s/nchx_link.png' % OUT
    im.save(os.path.join(ROOT, rel))
    add['nchx_link'] = rel

    # a square canvas so every rotation lands on the same centre - a chain built
    # from frames of differing size would wander as it bends
    side = int(np.hypot(im.width, im.height)) + 2
    for i in range(ROTS):
        ang = i * (360.0 / ROTS)
        pad = Image.new('RGBA', (side, side), (0, 0, 0, 0))
        pad.alpha_composite(im, ((side - im.width) // 2, (side - im.height) // 2))
        rot = pad.rotate(-ang, resample=Image.NEAREST, expand=False)
        k = 'nchx_r%02d' % i
        rel = '%s/%s.png' % (OUT, k)
        rot.save(os.path.join(ROOT, rel))
        add[k] = rel

    new = ''.join('"%s":"%s",' % (k, v) for k, v in sorted(add.items())
                  if ('"%s":' % k) not in man)
    if new:
        i = man.index('window.BOFX={"img":{') + len('window.BOFX={"img":{')
        open(man_path, 'w', encoding='utf-8').write(man[:i] + new + man[i:])
    print('  %d rotations at %.1f degrees, all on a %dx%d canvas'
          % (ROTS, 360.0 / ROTS, side, side))
    print('  a chain is now N links along a curve, each at the nearest angle')


if __name__ == '__main__':
    main()
