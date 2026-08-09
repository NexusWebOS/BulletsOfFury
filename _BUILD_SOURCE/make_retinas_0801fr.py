#!/usr/bin/env python3
"""
DROP 0801fr - RETINA REELS

Mike: "retinas are not using the right graphic for each pilot. use the corrected
new retinas, the proper colors for them too" then "4 frame reels from each still
with the middle glow like its locked on."

WHAT EXISTS AND WHAT THE CODE WANTS
nbret_<pilot> is ONE 172x170 still per pilot. The reticle code asks for
retA_<pilot>_0..3 (sweeping) and retB_<pilot>_0..3 (locked) - 72 keys. Every one
was missing, which is why the reticle drew nothing at all rather than drawing the
wrong thing.

COLOUR
The shipped stills are not in Mike's colours either: Cole reads blue-teal and
should be black, Axel reads orange and should be blue. Hue rotation preserves
value and saturation, so the authored shading survives - the same rule used for
Axel's orb and Freezer's ice breath.

Cole is the exception. Black is not a hue, so his is desaturated and darkened
instead, with the rim left bright enough to read against dark terrain.

THE TWO REELS
  retA - SWEEPING. The reticle is hunting: it breathes in scale and its brightness
         rises and falls, but there is no core. Frames step 0..3 on a 80ms clock.

  retB - LOCKED. Same body plus a MIDDLE GLOW that pulses hard - a white-hot core
         drawn additively at the centre, peaking on frames 1 and 2. That pulse is
         the whole read: sweeping has no core, locked has one, so the player can
         tell at a glance without reading a colour change.
"""
import os
import re
import numpy as np
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
OUT = 'assets/ui/icons'

# Mike's list. hue in degrees, or None for the achromatic case.
PILOT_COL = {
    'cole':       (None, 'black'),
    'decker':     (52,   'yellow'),
    'lizzie':     (43,   'gold'),
    'falva':      (330,  'pink'),
    'freezer':    (280,  'purple'),
    'yuri':       (0,    'red'),
    'maverick':   (110,  'neon green'),
    'juggernaut': (25,   'orange'),
    'axel':       (215,  'blue'),
}


def to_hsv(rgb):
    mx = rgb.max(axis=2)
    mn = rgb.min(axis=2)
    v = mx
    s = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0)
    return s, v


def hsv_to_rgb(h, s, v):
    i = np.floor(h * 6.0)
    f = h * 6.0 - i
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    i = (i % 6).astype(int)
    out = np.zeros(h.shape + (3,))
    for k, (rr, gg, bb) in enumerate([(v, t, p), (q, v, p), (p, v, t),
                                      (p, q, v), (t, p, v), (v, p, q)]):
        m = (i == k)
        out[..., 0][m] = rr[m]
        out[..., 1][m] = gg[m]
        out[..., 2][m] = bb[m]
    return out


def recolour(a, hue, sat_mul=1.15, val_mul=1.0):
    """Rotate to a target hue, keeping the authored value and shading."""
    rgb = a[..., :3] / 255.0
    s, v = to_hsv(rgb)
    core = (v > 0.90) & (s < 0.25)              # white-hot detail stays white
    if hue is None:
        # BLACK: drop the colour and crush the value, but keep the rim readable
        g = 0.299 * rgb[..., 0] + 0.587 * rgb[..., 1] + 0.114 * rgb[..., 2]
        g2 = np.clip(g * 0.42, 0, 1)
        g2 = np.where(g > 0.72, np.clip(g * 0.85, 0, 1), g2)   # highlights survive
        out = np.dstack([g2, g2, g2])
    else:
        h = np.full_like(v, hue / 360.0)
        # SATURATION FLOOR. Juggernaut's still is near-grey (140,140,147), and
        # rotating the hue of a desaturated pixel leaves it grey - he came out
        # RGB(145,142,141) instead of orange. Lifting low-saturation pixels toward
        # a floor gives the rotation something to work with, while pixels that are
        # already colourful keep their own relationship.
        s2 = np.clip(s * sat_mul, 0, 1)
        s2 = np.where(v > 0.06, np.maximum(s2, 0.55 * np.clip(v * 1.3, 0, 1)), s2)
        out = hsv_to_rgb(h, s2, np.clip(v * val_mul, 0, 1))
    for c in range(3):
        out[..., c] = np.where(core, rgb[..., c], out[..., c])
    res = a.copy()
    res[..., :3] = np.clip(out * 255, 0, 255)
    return res


def radial(shape, cx, cy, r):
    yy, xx = np.mgrid[0:shape[0], 0:shape[1]]
    d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    return np.clip(1.0 - d / max(1.0, r), 0, 1)


def main():
    man_path = os.path.join(ROOT, 'assets/manifest.js')
    man = open(man_path, encoding='utf-8').read()
    os.makedirs(os.path.join(ROOT, OUT), exist_ok=True)
    add = {}

    for pilot, (hue, name) in PILOT_COL.items():
        m = re.search(r'"nbret_%s":"([^"]+)"' % pilot, man)
        if not m:
            print('  %-11s no still registered' % pilot)
            continue
        src = os.path.join(ROOT, m.group(1))
        base = np.array(Image.open(src).convert('RGBA')).astype(float)
        col = recolour(base, hue)
        H, W = col.shape[:2]
        cx, cy = W / 2.0, H / 2.0
        glow = radial((H, W), cx, cy, W * 0.20)

        for f in range(4):
            # SWEEPING: breathes, no core
            a = col.copy()
            pulse = 0.80 + 0.20 * np.sin(f / 4.0 * 2 * np.pi)
            a[..., :3] = np.clip(a[..., :3] * pulse, 0, 255)
            a[..., 3] = np.clip(base[..., 3] * (0.82 + 0.18 * pulse), 0, 255)
            p = '%s/retA_%s_%d.png' % (OUT, pilot, f)
            Image.fromarray(a.astype(np.uint8), 'RGBA').save(os.path.join(ROOT, p))
            add['retA_%s_%d' % (pilot, f)] = p

            # LOCKED: same body plus a hot middle glow, peaking mid-reel
            b = col.copy()
            gp = [0.35, 1.0, 0.85, 0.5][f]
            add_glow = (glow ** 1.6) * gp * 235.0
            for c in range(3):
                b[..., c] = np.clip(b[..., c] + add_glow, 0, 255)
            # the core also pushes alpha up so it reads even over bright terrain
            b[..., 3] = np.clip(np.maximum(base[..., 3], add_glow * 1.1), 0, 255)
            p = '%s/retB_%s_%d.png' % (OUT, pilot, f)
            Image.fromarray(b.astype(np.uint8), 'RGBA').save(os.path.join(ROOT, p))
            add['retB_%s_%d' % (pilot, f)] = p

        px = col[..., :3][base[..., 3] > 16]
        print('  %-11s %-11s RGB(%3.0f,%3.0f,%3.0f)  8 frames' %
              (pilot, name, px[:, 0].mean(), px[:, 1].mean(), px[:, 2].mean()))

    new = ''.join('"%s":"%s",' % (k, v) for k, v in sorted(add.items())
                  if ('"%s":' % k) not in man)
    if new:
        i = man.index('window.BOFX={"img":{') + len('window.BOFX={"img":{')
        open(man_path, 'w', encoding='utf-8').write(man[:i] + new + man[i:])
    print('  registered %d retina keys' % new.count('":"'))


if __name__ == '__main__':
    main()
