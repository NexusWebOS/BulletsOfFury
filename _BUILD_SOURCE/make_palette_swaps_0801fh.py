#!/usr/bin/env python3
"""
DROP 0801fh - PALETTE SWAPS FOR AXEL AND FREEZER

Mike:
  Axel    - "duplicate falva's ball helper, palette swap it to royal blue, get th
             falva laser, palette swap it to roayl blue as well"
  Freezer - "turn it into ice breath instead. palette swap it to ice blue" and
             "explode with ice blue epxlosions that are palette swapped from our
             explosions, and use some debris we got palette swap it to a ice
             version"

WHY HUE ROTATION AND NOT A TINT
A tint multiplies, so it darkens everything it touches and flattens the authored
shading - the white-hot cores go grey and the piece stops reading as energy.
Rotating HUE in HSV moves the colour while leaving VALUE and SATURATION exactly
where the artist put them, so every highlight, every falloff and every core
survives. It is the same rule already used for the pilot thrusters in this build.

Near-white pixels are left alone on purpose. A plasma core is white because it is
the hottest part; recolouring it makes the whole sprite read as flat plastic.

TARGETS
  royal blue  hue 225 deg   for Axel, off Falva's magenta kit
  ice blue    hue 195 deg   for Freezer, colder and cyan-leaning
"""
import os
import re
import numpy as np
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


def hue_shift(src, dst, target_hue, sat_mul=1.0, val_mul=1.0, keep_white=0.90):
    """Rotate every pixel to a target hue, preserving value and shading."""
    a = np.array(Image.open(src).convert('RGBA')).astype(float)
    rgb = a[..., :3] / 255.0
    alpha = a[..., 3]
    mx = rgb.max(axis=2)
    mn = rgb.min(axis=2)
    v = mx
    s = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0)

    # a near-white, low-saturation pixel is a hot core: leave it
    core = (v > keep_white) & (s < 0.25)

    h = np.full_like(v, target_hue / 360.0)
    s2 = np.clip(s * sat_mul, 0, 1)
    v2 = np.clip(v * val_mul, 0, 1)

    i = np.floor(h * 6.0)
    f = h * 6.0 - i
    p = v2 * (1 - s2)
    q = v2 * (1 - f * s2)
    t = v2 * (1 - (1 - f) * s2)
    i = (i % 6).astype(int)

    out = np.zeros_like(rgb)
    for k, (rr, gg, bb) in enumerate([(v2, t, p), (q, v2, p), (p, v2, t),
                                      (p, q, v2), (t, p, v2), (v2, p, q)]):
        m = (i == k)
        out[..., 0][m] = rr[m]
        out[..., 1][m] = gg[m]
        out[..., 2][m] = bb[m]

    for c in range(3):
        out[..., c] = np.where(core, rgb[..., c], out[..., c])

    res = np.dstack([np.clip(out * 255, 0, 255), alpha])
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    Image.fromarray(res.astype(np.uint8), 'RGBA').save(dst)
    return True


def family(man, prefix):
    """Every registered key in a numbered family, in order."""
    out = []
    for k, p in re.findall(r'"([a-zA-Z0-9_]+)":"(assets/[^"]+)"', man):
        if re.match(r'^' + prefix + r'\d+$', k):
            out.append((k, p))
    return sorted(out, key=lambda kv: int(re.sub(r'\D', '', kv[0][len(prefix):]) or 0))


def main():
    man_path = os.path.join(ROOT, 'assets/manifest.js')
    man = open(man_path, encoding='utf-8').read()
    add = {}

    JOBS = [
        # (source prefix, new prefix, out dir, hue, sat, val, label)
        ('forb_',   'aorb_',   'assets/fx/axel',    225, 1.05, 1.00, "Axel's orbiting ball"),
        ('nfdb_',   'nadb_',   'assets/fx/axel',    225, 1.05, 1.00, "Axel's beam"),
        ('fshard_', 'ashard_', 'assets/fx/axel',    225, 1.05, 1.00, "Axel's shards"),
    ]
    for pre, newpre, outdir, hue, sm, vm, label in JOBS:
        fam = family(man, pre)
        n = 0
        for k, p in fam:
            src = os.path.join(ROOT, p)
            if not os.path.exists(src):
                continue
            newk = newpre + k[len(pre):]
            rel = '%s/%s.png' % (outdir, newk)
            if hue_shift(src, os.path.join(ROOT, rel), hue, sm, vm):
                add[newk] = rel
                n += 1
        print('  %-24s %2d frames  %s -> %s' % (label, n, pre + '*', newpre + '*'))

    new = ''.join('"%s":"%s",' % (k, v) for k, v in sorted(add.items())
                  if ('"%s":' % k) not in man)
    if new:
        i = man.index('window.BOFX={"img":{') + len('window.BOFX={"img":{')
        man = man[:i] + new + man[i:]
        open(man_path, 'w', encoding='utf-8').write(man)
    print('  registered %d new keys' % new.count('":"'))


if __name__ == '__main__':
    main()
