#!/usr/bin/env python3
"""
DROP 0801if - THE QUAD LASER'S CHARGE ATTACK

Mike:
  "Make it where you have go destroy the lasers first on this miniboss, then his
   hull is attackable. From the nose, when his lasers are gone, he should begin
   shooting charge lasers. Make a traced outline of him 3x, do different shades of
   green and make them pixel animate and hull glow green until he releases it. You
   can use his green projectile not laser but scaled much larger. It should form at
   his nose and scale up till he releases it as. This would be a large plasma burst
   ... then some of our older explosions palette swapped to this plasma energy, and
   make it like a plasma nuclear ball."

WHAT GETS BUILT

1. THREE TRACED OUTLINES, nqx_trace_<0..2>
   Each is the hull's silhouette expanded by a different amount and filled with a
   different shade of green - near, mid, far. Drawn stacked and cycled, they read as
   energy crawling outward from the machine while it winds up.

2. HULL GLOW, nqx_charge_<0..5>
   The whole hull lifted toward green, ramping with the charge rather than pulsing,
   so it visibly builds to the release instead of idling.

3. THE FORMING ORB, nqx_orb_<0..7>
   nql_rupture_01 - his green projectile, not the laser - scaled from small to very
   large across eight steps. It forms at the nose (x=191, y=361 on the 384 canvas)
   and grows until he lets go.

4. THE PLASMA BURST, nqx_plasma_<0..7>
   The existing explosion reel palette-swapped from fire to plasma: deep green rim,
   acid-green body, white-hot core. Same three-band swap used on the debris, so the
   blast keeps its authored shading and only changes element.

Nothing here is procedural - every frame comes from art that already exists.
"""
import os
import re
import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
OUT = 'assets/enemies/miniboss/quadlaser'

# near / mid / far, brightest closest to the hull
TRACE = [((6), (196, 255, 128)), ((14), (96, 214, 72)), ((24), (28, 128, 44))]
PLASMA_RAMP = [(10, 62, 18), (74, 196, 58), (226, 255, 214)]


def load(man, key):
    m = re.search(r'"%s":"([^"]+)"' % key, man)
    if not m:
        return None
    p = os.path.join(ROOT, m.group(1))
    return np.array(Image.open(p).convert('RGBA')).astype(float) if os.path.exists(p) else None


def save(a, rel):
    Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA').save(os.path.join(ROOT, rel))


def band_swap(a, ramp):
    """Three tonal bands replaced by the ramp - the same swap used on the debris."""
    out = a.copy()
    op = a[..., 3] > 16
    if not op.any():
        return out
    lum = 0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2]
    lo, hi = np.percentile(lum[op], 26), np.percentile(lum[op], 72)
    for band, target in ((op & (lum <= lo), ramp[0]),
                         (op & (lum > lo) & (lum <= hi), ramp[1]),
                         (op & (lum > hi), ramp[2])):
        if not band.any():
            continue
        b = lum[band]
        span = max(1.0, float(b.max() - b.min()))
        local = ((b - b.min()) / span - 0.5) * 24.0
        for c in range(3):
            out[..., c][band] = np.clip(target[c] + local, 0, 255)
    return out


def main():
    man_path = os.path.join(ROOT, 'assets/manifest.js')
    man = open(man_path, encoding='utf-8').read()
    os.makedirs(os.path.join(ROOT, OUT), exist_ok=True)
    add = {}

    body = load(man, 'nqx_body_intact')
    if body is None:
        print('  no hull'); return
    op = body[..., 3] > 16

    # ---- 1. three traced outlines, PIXEL-SHADED ----
    # Mike: "Now shade those traced things with pixel shading to get that proper
    # 16-bit effect."
    #
    # The first pass filled each ring with ONE flat colour - measured, 1 distinct
    # colour per trace. That reads as vector line art, not 16-bit. Three things fix
    # it, and all three are what a Mega Drive artist would actually do:
    #
    #   1. a TONAL RAMP across the ring's width, hot at the inner edge where the
    #      energy leaves the hull and cooling outward
    #   2. ORDERED DITHER between adjacent steps, using a 4x4 Bayer matrix, so the
    #      transition is stippled instead of smoothly blended
    #   3. QUANTISED to a handful of steps, because a 16-bit palette had few slots
    #      and the banding is the look
    BAYER = np.array([[0, 8, 2, 10], [12, 4, 14, 6],
                      [3, 11, 1, 9], [15, 7, 13, 5]], dtype=float) / 16.0
    for i, (grow, rgb) in enumerate(TRACE):
        inner = ndimage.binary_dilation(op, iterations=max(1, grow - 5))
        outer = ndimage.binary_dilation(op, iterations=grow)
        ring = outer & ~inner
        if not ring.any():
            continue
        # distance across the ring: 1 at the inner edge, 0 at the outer
        dIn = ndimage.distance_transform_edt(~inner)
        span = float(dIn[ring].max() - dIn[ring].min()) or 1.0
        t = 1.0 - (dIn - dIn[ring].min()) / span
        t = np.clip(t, 0, 1)

        H, W = t.shape
        bay = np.tile(BAYER, (H // 4 + 1, W // 4 + 1))[:H, :W]

        STEPS = 5
        # dither BEFORE quantising - that is what turns a smooth ramp into stipple
        q = np.clip(np.floor(t * (STEPS - 1) + bay * 0.9) / (STEPS - 1), 0, 1)

        a = np.zeros_like(body)
        # each step is a real palette entry, brightest at the hull
        for sIdx in range(STEPS):
            lvl = sIdx / (STEPS - 1.0)
            m = ring & (np.abs(q - lvl) < 1e-6)
            if not m.any():
                continue
            k = 0.42 + 0.58 * lvl          # value ramp across the band
            for c in range(3):
                a[..., c][m] = np.clip(rgb[c] * k, 0, 255)
            a[..., 3][m] = int(120 + 118 * lvl)

        cols = len(set(map(tuple, a[..., :3][a[..., 3] > 0])))
        print('   trace %d: %d px, %d shade steps' % (i, int((a[..., 3] > 0).sum()), cols))
        k = 'nqx_trace_%d' % i
        rel = '%s/%s.png' % (OUT, k)
        save(a, rel); add[k] = rel

    # ---- 2. hull glow, RAMPING to the release ----
    for ph in range(6):
        t = ph / 5.0
        a = body.copy()
        # push toward green in proportion to the charge, brightest at the end
        a[..., 0] = np.where(op, np.clip(body[..., 0] * (1 - t * 0.55), 0, 255), a[..., 0])
        a[..., 1] = np.where(op, np.clip(body[..., 1] * (1 + t * 0.95) + t * 40, 0, 255), a[..., 1])
        a[..., 2] = np.where(op, np.clip(body[..., 2] * (1 - t * 0.35), 0, 255), a[..., 2])
        k = 'nqx_charge_%d' % ph
        rel = '%s/%s.png' % (OUT, k)
        save(a, rel); add[k] = rel
    print('  6 hull-glow steps, ramping not pulsing')

    # ---- 3. the forming orb, from his own green projectile ----
    orb = load(man, 'nql_rupture_01')
    if orb is not None:
        src = Image.fromarray(np.clip(orb, 0, 255).astype(np.uint8), 'RGBA')
        for i in range(8):
            px = int(18 + (150 - 18) * (i / 7.0) ** 1.35)   # slow start, fast finish
            t = src.resize((px, px), Image.LANCZOS)
            k = 'nqx_orb_%d' % i
            rel = '%s/%s.png' % (OUT, k)
            t.save(os.path.join(ROOT, rel)); add[k] = rel
        print('  8 orb steps, 18px -> 150px, forming at the nose')

    # ---- 4. the plasma burst ----
    made = 0
    for i in range(8):
        e = load(man, 'nxp_dense_%d' % i)
        if e is None:
            continue
        save(band_swap(e, PLASMA_RAMP), '%s/nqx_plasma_%d.png' % (OUT, i))
        add['nqx_plasma_%d' % i] = '%s/nqx_plasma_%d.png' % (OUT, i)
        made += 1
    print('  %d plasma blast frames, fire -> plasma' % made)

    new = ''.join('"%s":"%s",' % (k, v) for k, v in sorted(add.items())
                  if ('"%s":' % k) not in man)
    if new:
        i = man.index('window.BOFX={"img":{') + len('window.BOFX={"img":{')
        open(man_path, 'w', encoding='utf-8').write(man[:i] + new + man[i:])
    print('  registered %d keys' % len(add))


if __name__ == '__main__':
    main()
