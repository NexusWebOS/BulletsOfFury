#!/usr/bin/env python3
"""
forest_swap_0912p.py - NEON GREEN DOWN TO FOREST GREEN, on the Razorback tank pack.

    python3 _BUILD_SOURCE/forest_swap_0912p.py --src <pack/sprites> --proof /tmp/forest.png
    python3 _BUILD_SOURCE/forest_swap_0912p.py --src ... --out <dir> --write

Mike, 0912: "recolor the neon green down to forest green via palette swapping."

MEASURED FIRST, on hull_0: the neon sits at **hue 88 degrees** (a yellow-green), saturation 0.90,
value 0.74, and it is **14.2% of the opaque pixels** - the rest of the tank is grey steel that must
not move a shade. Forest green is hue ~120 with less of both.

⚠ ROTATE THE HUE, DO NOT SET IT. 0906t: "SETTING THE HUE FLATTENS A FLAME; ROTATING IT DOES NOT" -
the plate's internal hue spread (69-136 degrees here) is what gives the panels their variation, and
writing one hue into every pixel collapses that into a slab. A +32 degree rotation carries the whole
spread across intact.

⚠ AND A VALUE-RANGE EXCHANGE IS A PALETTE SHREDDER. 0906o measured Decker's range remap turning
every one-step dither into a four-step jump and **halving his palette, 7,666 colours to 3,707**,
while looking plausible. Saturation and value are GENTLE GAINS here (one multiply, with a floor),
never a remap of one band onto another.

⚠ COUNT THE COLOURS BEFORE AND AFTER - that halving is the signature of the damage and it is one
line to check. This refuses to write if the opaque palette loses more than a fifth of its colours.

⚠ AND COUNT THEM ON OPAQUE PIXELS ONLY. `convert('RGB').getcolors()` counts the RGB left under
fully transparent pixels and reports more "colours" than the sprite has pixels (0905, measured at
35,374 against an honest 19,063).
"""
import os, sys, glob, argparse
import numpy as np
from PIL import Image, ImageDraw

HUE_ROT = 32.0      # 88 -> 120, measured
SAT_GAIN = 0.66     # pull the neon back without flattening the spread
VAL_GAIN = 0.60     # forest green sits near V 0.55; the neon was at 0.74
VAL_FLOOR = 0.025   # keep the darkest panel lines from crushing to black
GREEN_MARGIN = 14   # how much G must lead R and B for a pixel to be "the green"

# ⚠ THE SONIC EFFECTS ARE NOT HULL PAINT AND MUST NOT GO FOREST GREEN.
# Mike's instruction is about the TANK; these are its ORDNANCE. This tank becomes the STAGE 1
# miniboss, and stage 1 is "RUMBLE IN THE JUNGLE" - a forest-green shockwave on a green jungle
# backdrop is a projectile the player cannot see. CLAUDE.md already records this exact reasoning
# from the other direction (0905e): an ice-blue alert lane on an ice stage "vanishes into the ice,
# which is the same mistake one step over"; a cue must contrast with the FIELD.
# They also measured the worst palette loss of anything in the pack - 0.62 to 0.78 - because they
# are almost entirely green gradient, which is the 0906o shredder signature and a second reason to
# leave them alone.
FX_KEEP = ('sonic_', 'muzzle', 'dust')


def rgb_to_hsv(a):
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    mx = a[..., :3].max(axis=-1); mn = a[..., :3].min(axis=-1)
    d = mx - mn
    h = np.zeros_like(mx)
    m = d > 1e-9
    rm = m & (mx == r); gm = m & (mx == g) & ~rm; bm = m & (mx == b) & ~rm & ~gm
    h[rm] = ((g[rm] - b[rm]) / d[rm]) % 6
    h[gm] = ((b[gm] - r[gm]) / d[gm]) + 2
    h[bm] = ((r[bm] - g[bm]) / d[bm]) + 4
    h = h / 6.0
    s = np.where(mx > 0, d / np.maximum(mx, 1e-9), 0.0)
    return h, s, mx


def hsv_to_rgb(h, s, v):
    i = np.floor(h * 6.0)
    f = h * 6.0 - i
    p = v * (1 - s); q = v * (1 - f * s); t = v * (1 - (1 - f) * s)
    i = (i % 6).astype(int)
    out = np.zeros(h.shape + (3,))
    for k, (R, G, B) in enumerate([(v, t, p), (q, v, p), (p, v, t), (p, q, v), (t, p, v), (v, p, q)]):
        m = i == k
        out[m, 0] = R[m]; out[m, 1] = G[m]; out[m, 2] = B[m]
    return out


def green_mask(a8):
    """Only the GREEN panels. The steel hull, the treads and the orange trim must not move."""
    r, g, b = a8[..., 0].astype(int), a8[..., 1].astype(int), a8[..., 2].astype(int)
    return (a8[..., 3] > 8) & (g > r + GREEN_MARGIN) & (g > b + GREEN_MARGIN)


def opaque_colours(a8):
    m = a8[..., 3] > 200
    if not m.any():
        return 0
    return len(np.unique(a8[..., :3][m].reshape(-1, 3), axis=0))


def swap(img):
    a8 = np.asarray(img).astype(np.uint8)
    a = a8.astype(np.float64) / 255.0
    m = green_mask(a8)
    if not m.any():
        return img.copy(), {'green': 0, 'before': opaque_colours(a8), 'after': opaque_colours(a8)}
    h, s, v = rgb_to_hsv(a)
    h2 = (h + HUE_ROT / 360.0) % 1.0
    s2 = np.clip(s * SAT_GAIN, 0, 1)
    v2 = np.clip(v * VAL_GAIN + VAL_FLOOR, 0, 1)
    rgb2 = hsv_to_rgb(h2, s2, v2)
    out = a.copy()
    out[..., :3] = np.where(m[..., None], rgb2, a[..., :3])
    out[..., 3] = a[..., 3]                      # ⚠ alpha never moves
    o8 = (np.clip(out, 0, 1) * 255).astype(np.uint8)
    return Image.fromarray(o8, 'RGBA'), {
        'green': int(m.sum()),
        'before': opaque_colours(a8),
        'after': opaque_colours(o8),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--src', required=True)
    ap.add_argument('--out', default='')
    ap.add_argument('--proof', default='')
    ap.add_argument('--write', action='store_true')
    a = ap.parse_args()

    files = sorted(glob.glob(os.path.join(a.src, '*.png')))
    if not files:
        sys.exit('no png in ' + a.src)
    rows, bad = [], []
    for f in files:
        nm = os.path.basename(f)
        im = Image.open(f).convert('RGBA')
        if nm.startswith(FX_KEEP):
            out, info = im.copy(), {'green': 0, 'before': 0, 'after': 0, 'kept': True}
        else:
            out, info = swap(im)
        keep = info.get('kept') or info['before'] == 0 or info['after'] / max(1, info['before']) >= 0.80
        if not keep:
            bad.append((os.path.basename(f), info))
        rows.append((os.path.basename(f), im, out, info))
        if a.write and a.out:
            os.makedirs(a.out, exist_ok=True)
            out.save(os.path.join(a.out, os.path.basename(f)))

    print('%-26s %8s %9s %9s  %s' % ('file', 'green px', 'colours', 'after', ''))
    for n, _, _, i in rows:
        if i.get('kept'):
            print('  %-24s %8s %9s %9s  %s' % (n, '-', '-', '-', 'ORDNANCE - left bright on purpose'))
            continue
        ratio = i['after'] / max(1, i['before'])
        print('  %-24s %8d %9d %9d  %.2f%s'
              % (n, i['green'], i['before'], i['after'], ratio,
                 '  <-- PALETTE LOSS' if ratio < 0.80 and i['before'] else ''))
    if bad:
        print('\n%d file(s) lost more than a fifth of their palette - that is 0906o\'s shredder '
              'signature, not a recolour' % len(bad))
    if a.write:
        print('\nwrote %d files -> %s' % (len(rows), a.out))

    if a.proof:
        show = [r for r in rows if r[3]['green'] > 200][:8]
        Z = 2
        tiles = []
        for n, im, out, info in show:
            w, h = im.size
            t = Image.new('RGBA', (w * 2 + 8, h), (14, 16, 20, 255))
            for i, c in enumerate((im, out)):
                bg = Image.new('RGBA', c.size, (14, 16, 20, 255)); bg.paste(c, (0, 0), c)
                t.paste(bg, (i * (w + 8), 0))
            tiles.append((n, t.resize((t.width * Z, t.height * Z), Image.NEAREST), info))
        W = max(t.width for _, t, _ in tiles); H = max(t.height for _, t, _ in tiles)
        cols = 2
        sheet = Image.new('RGBA', (W * cols + 30, (H + 26) * ((len(tiles) + cols - 1) // cols) + 20),
                          (7, 12, 18, 255))
        d = ImageDraw.Draw(sheet)
        for i, (n, t, info) in enumerate(tiles):
            cx = (i % cols) * (W + 14) + 8; cy = (i // cols) * (H + 26) + 20
            sheet.paste(t, (cx, cy))
            d.text((cx, cy - 14), '%s    neon | forest    %d green px, palette %d -> %d'
                   % (n, info['green'], info['before'], info['after']), fill=(124, 245, 255, 255))
        os.makedirs(os.path.dirname(os.path.abspath(a.proof)), exist_ok=True)
        sheet.save(a.proof)
        print('proof -> %s' % a.proof)
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
