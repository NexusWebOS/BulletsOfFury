#!/usr/bin/env python3
"""
ice_swap_0912s.py - THE JUNGLE CRUISER, PALETTE-SWAPPED TO ICE, FOR STAGE 3.

    python3 _BUILD_SOURCE/ice_swap_0912s.py --proof <png>          # render only
    python3 _BUILD_SOURCE/ice_swap_0912s.py --proof <png> --write  # also writes the plate

Mike, 0912: "Take THAT stage 1 miniboss, palette swap to an icey combination, and use as the new
stage 3 mini boss."

MEASURED FIRST (nsb_jungle_cruiser.png, 256x256, 18,360 opaque px, 60 colours): there is almost no
GREEN on it at all - the hull is OLIVE DRAB, hue 55-75 at low value, 11,183 saturated pixels, with
RUST accents at hue 18-30 (5,949 px). So "the green goes blue" is the wrong model, and ONE hue
rotation is wrong too: a rotation that carries olive to ice blue carries rust to TEAL-GREEN, which is
neither ice nor an accent.

TWO BANDS, EACH A ROTATION WITH GENTLE GAINS:
  olive  (hue 36..100)  -> steel ice blue: rotate to ~205, saturation down a little, value UP with a
                           gain (ice reads light; the olive plate is authored very dark)
  rust   (hue 0..36)    -> frost cyan-white accents: rotate to ~188, saturation well down, value up
  near-neutral pixels (S < 0.12) and the black outline keep their value and pick up only a faint
  cool cast, so the 2px outline and the panel lines survive.

⚠ ROTATE, DO NOT SET (0906t) - each band keeps its internal hue spread by rotating by the band's own
offset rather than writing one hue. ⚠ GENTLE GAINS, NOT A RANGE REMAP (0906o) - one multiply plus a
floor, so one-step dithers stay one step. ⚠ COUNT THE COLOURS BEFORE AND AFTER on opaque pixels only,
and refuse the write on a loss past a fifth. ⚠ ALPHA IS NEVER WRITTEN.
"""
import os, sys, argparse, colorsys
import numpy as np
from PIL import Image, ImageDraw

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
SRC = os.path.join(ROOT, 'assets', 'game', 'nsb_jungle_cruiser.png')
OUT = os.path.join(ROOT, 'assets', 'game', 'nsb_frost_cruiser.png')

OLIVE = dict(lo=36, hi=100, to=205, sat=0.78, val=1.55, floor=0.020)
RUST = dict(lo=0, hi=36, to=188, sat=0.34, val=1.70, floor=0.030)
NEUTRAL_S = 0.12
NEUTRAL_CAST = dict(to=205, sat=0.10, val=1.12)


def rgb_to_hsv_arr(a):
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    mx = a.max(axis=-1); mn = a.min(axis=-1); d = mx - mn
    h = np.zeros_like(mx)
    m = d > 1e-9
    rm = m & (mx == r); gm = m & (mx == g) & ~rm; bm = m & (mx == b) & ~rm & ~gm
    h[rm] = ((g[rm] - b[rm]) / d[rm]) % 6
    h[gm] = ((b[gm] - r[gm]) / d[gm]) + 2
    h[bm] = ((r[bm] - g[bm]) / d[bm]) + 4
    h = (h / 6.0) * 360.0
    s = np.where(mx > 0, d / np.maximum(mx, 1e-9), 0.0)
    return h, s, mx


def hsv_to_rgb_arr(h, s, v):
    h = (h % 360.0) / 60.0
    i = np.floor(h); f = h - i
    p = v * (1 - s); q = v * (1 - f * s); t = v * (1 - (1 - f) * s)
    i = i.astype(int) % 6
    out = np.zeros(h.shape + (3,))
    for k, (R, G, B) in enumerate([(v, t, p), (q, v, p), (p, v, t), (p, q, v), (t, p, v), (v, p, q)]):
        mk = i == k
        out[mk, 0] = R[mk]; out[mk, 1] = G[mk]; out[mk, 2] = B[mk]
    return out


def opaque_colours(a8):
    m = a8[..., 3] > 200
    return len(np.unique(a8[..., :3][m].reshape(-1, 3), axis=0)) if m.any() else 0


def swap(img):
    a8 = np.asarray(img.convert('RGBA')).astype(np.uint8)
    a = a8[..., :3].astype(np.float64) / 255.0
    ink = a8[..., 3] > 0
    h, s, v = rgb_to_hsv_arr(a)
    H, Sa, V = h.copy(), s.copy(), v.copy()

    neutral = ink & (s < NEUTRAL_S)
    olive = ink & ~neutral & (h >= OLIVE['lo']) & (h < OLIVE['hi'])
    rust = ink & ~neutral & ((h < RUST['hi']) | (h >= 340))
    other = ink & ~neutral & ~olive & ~rust

    for mask, B in ((olive, OLIVE), (rust, RUST)):
        centre = ((B['lo'] + B['hi']) / 2.0)
        H[mask] = h[mask] + (B['to'] - centre)                     # a ROTATION, spread kept
        Sa[mask] = np.clip(s[mask] * B['sat'], 0, 1)
        V[mask] = np.clip(v[mask] * B['val'] + B['floor'], 0, 1)
    H[neutral] = NEUTRAL_CAST['to']
    Sa[neutral] = np.clip(s[neutral] * 0 + NEUTRAL_CAST['sat'] * (v[neutral] > 0.08), 0, 1)
    V[neutral] = np.clip(v[neutral] * NEUTRAL_CAST['val'], 0, 1)

    rgb = hsv_to_rgb_arr(H, Sa, V)
    o = a8.copy()
    o[..., :3] = np.where(ink[..., None], np.clip(rgb * 255 + 0.5, 0, 255).astype(np.uint8), a8[..., :3])
    return Image.fromarray(o, 'RGBA'), {
        'olive': int(olive.sum()), 'rust': int(rust.sum()), 'neutral': int(neutral.sum()), 'other': int(other.sum()),
        'before': opaque_colours(a8), 'after': opaque_colours(o),
        'alpha_delta': int(np.abs(o[..., 3].astype(int) - a8[..., 3].astype(int)).sum()),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--proof', required=True)
    ap.add_argument('--write', action='store_true')
    a = ap.parse_args()
    src = Image.open(SRC).convert('RGBA')
    out, info = swap(src)
    print(info)
    ratio = info['after'] / max(1, info['before'])
    ok = ratio >= 0.80 and info['alpha_delta'] == 0
    Z = 3
    tiles = []
    for bgc in ((18, 24, 32), (196, 214, 226)):                  # a dark field AND a stage-3 ice field
        for im in (src, out):
            bg = Image.new('RGBA', im.size, bgc + (255,)); bg.paste(im, (0, 0), im)
            tiles.append(bg.resize((im.width * Z, im.height * Z), Image.NEAREST))
    W = tiles[0].width
    sheet = Image.new('RGBA', (W * 2 + 12, W * 2 + 40), (8, 12, 18, 255))
    for i, t in enumerate(tiles):
        sheet.paste(t, ((i % 2) * (W + 12), 30 + (i // 2) * (W + 10) if i < 2 else 30 + W + 10))
    d = ImageDraw.Draw(sheet)
    d.text((6, 8), 'jungle | frost    palette %d -> %d (%.2f)   olive %d  rust %d  neutral %d  alpha delta %d'
           % (info['before'], info['after'], ratio, info['olive'], info['rust'], info['neutral'], info['alpha_delta']),
           fill=(124, 245, 255, 255))
    os.makedirs(os.path.dirname(os.path.abspath(a.proof)), exist_ok=True)
    sheet.save(a.proof)
    print('proof ->', a.proof)
    if not ok:
        print('REFUSED: palette ratio %.2f or alpha moved' % ratio)
        return 1
    if a.write:
        out.save(OUT)
        print('wrote', OUT)
    return 0


if __name__ == '__main__':
    sys.exit(main())
