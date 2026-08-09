#!/usr/bin/env python3
"""
DROP 0801ih - THE QUAD LASER'S PURPLE HALO BECOMES GREEN SHADING

Mike: "Clean up all purple halos on this ship. Make them 16-bit green shaded"

WHAT IS THERE
790 purple pixels across the hull and four cannons, mean RGB(72,13,74) - the dark
magenta the alpha key leaves on an anti-aliased rim. Every one sits on an edge.

WHY NOT JUST DARKEN THEM
That is what I did on the boss projectiles, and it is right when the sprite wants a
black outline. This ship is the GREEN machine - it glows green, charges green,
fires green - so its rim should read as part of that, not as a black sticker.

THE SHADING
Each halo pixel takes a green from a FIVE-STEP ramp chosen by how deep into the
sprite it sits: pixels touching open space get the darkest green, pixels tucked
against solid hull get the brightest. Depth comes from a distance transform, so the
shading follows the silhouette instead of being uniform.

Then the same ordered dither used on the traces breaks the boundary between steps,
so the rim bands rather than gradients - which is the 16-bit part.
"""
import os
import re
import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

PARTS = ['nqx_body_intact', 'nqx_body_damaged',
         'nqx_cannon_left_outer_intact', 'nqx_cannon_left_outer_damaged',
         'nqx_cannon_left_inner_intact', 'nqx_cannon_left_inner_damaged',
         'nqx_cannon_right_inner_intact', 'nqx_cannon_right_inner_damaged',
         'nqx_cannon_right_outer_intact', 'nqx_cannon_right_outer_damaged']

# darkest at the outside edge, brightest tucked against the hull
RAMP = [(14, 40, 18), (26, 70, 30), (44, 104, 44), (66, 142, 60), (96, 184, 82)]
BAYER = np.array([[0, 8, 2, 10], [12, 4, 14, 6],
                  [3, 11, 1, 9], [15, 7, 13, 5]], dtype=float) / 16.0


def main():
    man = open(os.path.join(ROOT, 'assets/manifest.js'), encoding='utf-8').read()
    total = 0
    for key in PARTS:
        m = re.search(r'"%s":"([^"]+)"' % key, man)
        if not m:
            continue
        p = os.path.join(ROOT, m.group(1))
        if not os.path.exists(p):
            continue
        a = np.array(Image.open(p).convert('RGBA')).astype(float)
        op = a[..., 3] > 16
        r, g, b = a[..., 0], a[..., 1], a[..., 2]
        halo = op & (b > g + 18) & (r > g + 10)
        if not halo.any():
            continue

        # DEPTH DOES NOT DISCRIMINATE HERE (drop 0801ih). Every halo pixel sits on
        # the edge at essentially the same depth, so a distance ramp put 335 of 350
        # on one step - flat again, just green instead of purple.
        #
        # Rim light does vary, and in a predictable way: a 16-bit artist lights from
        # ABOVE, so the top of a silhouette catches the most and the underside falls
        # to shadow. Driving the ramp off the local surface NORMAL gives that, and it
        # follows the shape rather than being a vertical wash.
        ys, xs = np.where(halo)
        # the outward normal is the gradient of the alpha field
        gy, gx = np.gradient(ndimage.gaussian_filter(op.astype(float), 1.6))
        n = np.hypot(gx, gy) + 1e-6
        # dot with a light coming from up and slightly left
        lit = ((-gy / n) * 0.86 + (-gx / n) * 0.34)
        t = np.clip((lit + 1.0) * 0.5, 0, 1)
        # a touch of the pixel's own value so the rim is not perfectly uniform
        own = (0.299 * r + 0.587 * g + 0.114 * b) / 255.0
        t = np.clip(t * 0.78 + own * 0.44, 0, 1)

        H, W = a.shape[:2]
        bay = np.tile(BAYER, (H // 4 + 1, W // 4 + 1))[:H, :W]
        # dither BEFORE quantising, or the stipple never appears
        q = np.clip(np.floor(t * (len(RAMP) - 1) + bay * 0.85), 0, len(RAMP) - 1).astype(int)

        for i, rgb in enumerate(RAMP):
            m2 = halo & (q == i)
            if not m2.any():
                continue
            for c in range(3):
                a[..., c][m2] = rgb[c]
        Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA').save(p)
        total += int(halo.sum())
        print('   %-34s %4d px shaded' % (key.replace('nqx_', ''), int(halo.sum())))
    print('  %d purple pixels are now 16-bit green shading' % total)


if __name__ == '__main__':
    main()
