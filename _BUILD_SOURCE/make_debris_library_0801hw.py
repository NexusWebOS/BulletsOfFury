#!/usr/bin/env python3
"""
DROP 0801hx - DEBRIS, PALETTE-SWAPPED ONTO THE REAL ROSTER COLOURS

Mike: "make sure your palette swapping not color overlaying these, and to match the
exact colors of our enemy roster please. it might be tedious, but well worth it."

WHAT WAS WRONG
My first pass did `target_rgb * luminance`. That is an OVERLAY: it forces every
pixel onto one hue and one saturation, so a shaded metal chunk comes out as a flat
colour sticker. It also used invented primaries - cartoon red, blue, green - that
match nothing in the game.

WHAT THIS DOES
The ramps below are MEASURED off the real sprite folders, three tones each:

  tanks   assets/enemies/tanks      olive/khaki   RGB(57,56,36) .. (122,122,67)
  jets    assets/enemies/aircraft   grey-steel    RGB(46,48,51) .. (130,129,132)
  boats   assets/enemies/boats      navy          RGB(27,52,95) .. (89,107,134)
  bosses  assets/enemies/bosses     steel + blue  RGB(61,59,58) .. (73,120,169)

Each chunk's pixels are sorted into shadow / midtone / highlight by luminance
quantile, and each band is REPLACED by the matching tone from the target ramp. A
pixel's position within its own band survives as a small local shade, so the metal
keeps its modelling instead of going flat.
"""
import os
import glob
import numpy as np
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
OUT = 'assets/fx/debris'
PACK = '/tmp/dfx'

RAMPS = {
    'olive':  [(41, 40, 25), (57, 56, 36), (122, 122, 67)],
    'khaki':  [(48, 48, 28), (65, 63, 41), (140, 138, 84)],
    'steel':  [(46, 48, 51), (90, 93, 98), (130, 129, 132)],
    'slate':  [(45, 49, 54), (77, 84, 93), (118, 124, 132)],
    'navy':   [(27, 52, 95), (42, 82, 132), (89, 107, 134)],
    'gunmet': [(56, 60, 72), (61, 79, 110), (110, 126, 152)],
    'bossbl': [(56, 100, 150), (66, 112, 163), (128, 168, 210)],
    'bossgr': [(61, 59, 58), (68, 68, 67), (120, 122, 124)],
}
TYPES = {
    'tank': ['olive', 'khaki'],
    'jet':  ['steel', 'slate'],
    'boat': ['navy', 'gunmet'],
    'boss': ['bossbl', 'bossgr'],
}
SIZES = {'medium': 24, 'small': 17, 'tiny': 12, 'micro': 8}
ROLE = {1: 'general', 2: 'small piece', 3: 'small piece', 4: 'small piece',
        5: 'WHEEL', 6: 'TANK ROLLER', 7: 'fragment', 8: 'fragment'}


def swap(a, ramp):
    """Replace tonal bands with the target ramp - a swap, not a tint."""
    out = a.copy()
    op = a[..., 3] > 16
    if not op.any():
        return out
    lum = 0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2]
    lo, hi = np.percentile(lum[op], 22), np.percentile(lum[op], 74)
    bands = ((op & (lum <= lo), ramp[0]),
             (op & (lum > lo) & (lum <= hi), ramp[1]),
             (op & (lum > hi), ramp[2]))
    for band, target in bands:
        if not band.any():
            continue
        b = lum[band]
        span = max(1.0, float(b.max() - b.min()))
        local = ((b - b.min()) / span - 0.5) * 26.0
        for c in range(3):
            out[..., c][band] = np.clip(target[c] + local, 0, 255)
    return out


def main():
    os.makedirs(os.path.join(ROOT, OUT), exist_ok=True)
    srcs = sorted(x for x in glob.glob('%s/**/nchunk_*.png' % PACK, recursive=True)
                  if 'atlas' not in x)
    man_path = os.path.join(ROOT, 'assets/manifest.js')
    man = open(man_path, encoding='utf-8').read()
    add = {}
    for idx, p in enumerate(srcs, start=1):
        base = np.array(Image.open(p).convert('RGBA')).astype(float)
        op = base[..., 3] > 16
        ys, xs = np.where(op)
        base = base[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
        for typ, cols in TYPES.items():
            for col in cols:
                tinted = swap(base, RAMPS[col])
                for rot in range(4):
                    r = np.rot90(tinted, k=rot).copy()
                    im = Image.fromarray(np.clip(r, 0, 255).astype(np.uint8), 'RGBA')
                    for sname, px in SIZES.items():
                        w, h = im.size
                        sc = px / float(max(w, h))
                        t = im.resize((max(1, int(w * sc)), max(1, int(h * sc))), Image.NEAREST)
                        k = '%s%s%d_r%d_%s' % (col, typ, idx, rot, sname)
                        rel = '%s/%s.png' % (OUT, k)
                        t.save(os.path.join(ROOT, rel))
                        add[k] = rel
    new = ''.join('"%s":"%s",' % (k, v) for k, v in sorted(add.items())
                  if ('"%s":' % k) not in man)
    if new:
        i = man.index('window.BOFX={"img":{') + len('window.BOFX={"img":{')
        open(man_path, 'w', encoding='utf-8').write(man[:i] + new + man[i:])
    print('  built %d debris keys on ROSTER-SAMPLED ramps' % len(add))
    print('   ' + ', '.join('%s=%s' % (t, '/'.join(c)) for t, c in TYPES.items()))


if __name__ == '__main__':
    main()
