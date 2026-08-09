#!/usr/bin/env python3
"""
DROP 0801jj - THE PLATE OPENS AND THE HEAD RISES

Mike: "the head piece, maybe instead of that, where the plate is on the torso. make
an animation set that makes that circular piece 'open up' blacken, the head rises,
then as its rising we do the flash from bottom to top so that as the head connects
we get a white flash so we can make it look just right after the flash stops"

MUCH BETTER THAN THE CHAIN DROP
The head coming down on a chain from off-screen is generic. The head rising OUT OF
THE MACHINE ITSELF says the thing assembled itself, which is what the whole intro is
about.

THE PLATE
Measured on the torso: the pale disc at x 84..191, y 292..330 - 108 x 39. That is
the piece that opens.

THE SEQUENCE
  nqm_plate_0..7    the disc irises open and BLACKENS, so it reads as a hatch with
                    depth behind it rather than a lid sliding off
  nqm_rise_0..11    the head climbing out, with the bottom-to-top flash running up
                    the body underneath it as it goes
  nqm_seat_0..5     the white flash on connection, decaying back to normal so the
                    machine settles into its finished look
"""
import os
import re
import numpy as np
from PIL import Image, ImageDraw

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
OUT = 'assets/enemies/boss/magma'
BAYER = np.array([[0, 8, 2, 10], [12, 4, 14, 6],
                  [3, 11, 1, 9], [15, 7, 13, 5]], dtype=float) / 16.0


def quant(a, op, bay, levels=12):
    step = 255.0 / (levels - 1)
    for c in range(3):
        ch = a[..., c] + (bay - 0.5) * step * 0.9
        a[..., c] = np.where(op, np.clip(np.round(ch / step) * step, 0, 255), a[..., c])
    return a


def main():
    man_path = os.path.join(ROOT, 'assets/manifest.js')
    man = open(man_path, encoding='utf-8').read()
    torso = np.array(Image.open(os.path.join(ROOT, re.search(r'"mbg2_m_torso":"([^"]+)"', man).group(1))).convert('RGBA')).astype(float)
    headIm = Image.open(os.path.join(ROOT, re.search(r'"mgx_head":"([^"]+)"', man).group(1))).convert('RGBA')
    H, W = torso.shape[:2]
    op = torso[..., 3] > 16
    yy, xx = np.mgrid[0:H, 0:W]
    bay = np.tile(BAYER, (H // 4 + 1, W // 4 + 1))[:H, :W]

    # the measured disc
    PX0, PX1, PY0, PY1 = 84, 191, 292, 330
    pcx, pcy = (PX0 + PX1) // 2, (PY0 + PY1) // 2
    prx, pry = (PX1 - PX0) / 2.0, (PY1 - PY0) / 2.0
    disc = op & (((xx - pcx) / prx) ** 2 + ((yy - pcy) / pry) ** 2 < 1.0)
    print('  the disc: %d px at (%d,%d), %dx%d' % (int(disc.sum()), pcx, pcy, PX1 - PX0, PY1 - PY0))

    add = {}
    os.makedirs(os.path.join(ROOT, OUT), exist_ok=True)

    # ---- 1. the plate irises open and blackens ----
    for i in range(8):
        t = i / 7.0
        a = torso.copy()
        # the aperture grows from the centre outward
        ap = (((xx - pcx) / max(1.0, prx * t + 0.001)) ** 2 +
              ((yy - pcy) / max(1.0, pry * t + 0.001)) ** 2) < 1.0
        hole = disc & ap
        for c in range(3):
            a[..., c] = np.where(hole, a[..., c] * 0.06, a[..., c])
        # a hot rim where the hatch edge glows as it parts
        rim = disc & ap & ~((((xx - pcx) / max(1.0, prx * t * 0.82 + 0.001)) ** 2 +
                             ((yy - pcy) / max(1.0, pry * t * 0.82 + 0.001)) ** 2) < 1.0)
        for c, tgt in zip(range(3), (255, 176, 72)):
            a[..., c] = np.where(rim, np.clip(a[..., c] * 0.3 + tgt * 0.7, 0, 255), a[..., c])
        a = quant(a, op, bay)
        k = 'nqm_plate_%d' % i
        rel = '%s/%s.png' % (OUT, k)
        Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA').save(os.path.join(ROOT, rel))
        add[k] = rel

    # the fully open plate is the base for everything after
    openPlate = np.array(Image.open(os.path.join(ROOT, add['nqm_plate_7'])).convert('RGBA')).astype(float)

    # ---- 2. the head rises, flash running up beneath it ----
    RISE = pcy - 6                       # from the hatch up to the socket
    for i in range(12):
        t = i / 11.0
        base = openPlate.copy()
        # THE FLASH CLIMBS WITH THE HEAD. Mike wants bottom-to-top while it rises,
        # so the band tracks the head rather than running on its own clock.
        headY = pcy - (pcy + 8) * t
        band = np.abs(yy - headY) / 46.0
        lift = np.clip(1.5 - band, 0, 1.5)
        below = (yy > headY)
        amt = np.clip(lift * 0.8 + below * 0.22, 0, 1) * op
        for c, tgt in zip(range(3), (255, 208, 130)):
            base[..., c] = np.clip(base[..., c] * (1 - amt) + tgt * amt, 0, 255)
        base = quant(base, op, bay)
        im = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8), 'RGBA')
        # the head climbing out of the hatch
        hh = headIm.copy()
        canvas = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        canvas.alpha_composite(im)
        hy = int(pcy - (pcy + 10) * t) - hh.height // 2
        canvas.alpha_composite(hh, ((W - hh.width) // 2, hy))
        k = 'nqm_rise_%d' % i
        rel = '%s/%s.png' % (OUT, k)
        canvas.save(os.path.join(ROOT, rel))
        add[k] = rel

    # ---- 3. the white flash on connection, decaying to normal ----
    seated = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    seated.alpha_composite(Image.fromarray(np.clip(openPlate, 0, 255).astype(np.uint8), 'RGBA'))
    seated.alpha_composite(headIm, ((W - headIm.width) // 2, -10))
    sarr = np.array(seated).astype(float)
    sop = sarr[..., 3] > 16
    for i in range(6):
        t = i / 5.0
        a = sarr.copy()
        # full white at the moment of contact, falling away fast
        amt = (1.0 - t) ** 1.6
        for c in range(3):
            a[..., c] = np.clip(sarr[..., c] * (1 - amt) + 255 * amt, 0, 255)
        a = quant(a, sop, bay)
        k = 'nqm_seat_%d' % i
        rel = '%s/%s.png' % (OUT, k)
        Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA').save(os.path.join(ROOT, rel))
        add[k] = rel

    new = ''.join('"%s":"%s",' % (k, v) for k, v in sorted(add.items())
                  if ('"%s":' % k) not in man)
    if new:
        i = man.index('window.BOFX={"img":{') + len('window.BOFX={"img":{')
        open(man_path, 'w', encoding='utf-8').write(man[:i] + new + man[i:])
    print('  8 plate + 12 rise + 6 seat = %d frames' % len(add))


if __name__ == '__main__':
    main()
