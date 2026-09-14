#!/usr/bin/env python3
"""
tempest_grayswap_0912v.py - THE TEMPEST LEVIATHAN'S BROTHER: THE SAME HULL IN LIGHT GRAY.

    python3 _BUILD_SOURCE/tempest_grayswap_0912v.py --src <red_originals dir> --black <black assets dir> \
            --out <dir> --proof <png> [--field <stage capture png>] [--write]

Mike, 0912: "add another levithan ship in there, but palette swap that one ot be more light gray then black.
this will be its brother ship".

Built from the RED ORIGINALS, never from the black plates (0906o: re-run from the backup, not a result).

WHAT MOVES, MEASURED ON THE ORIGINALS (see tempest_blackswap_0912u.py for the full census):
  wing paint     hue 350..15, sat p50 0.79, val p50 0.42   -> desaturated, lifted to LIGHT gray
  hull body      near-neutral, val p50 0.13 (black titanium) -> lifted to mid/light gray
  outline ring   the outer OUTLINE_PX of ink                  -> KEPT DARK (the black-edge rule)
  energy         violet reactor, cyan apertures, blue engines -> untouched
  damage glow    orange scorch on the damaged plate           -> untouched (feathered band, as 0912u)

⚠ LIFTING DARK METAL TO LIGHT GRAY IS A RANGE STRETCH, AND 0906o IS WHAT A CARELESS ONE DOES. Decker's
swap stretched a 0.00-0.25 band across 0.02-0.95 (x3.7) and every one-step dither became a four-step
speckle. So the lift here is an OFFSET plus a GENTLE GAIN - v' = LIFT + GAIN*v with GAIN ~1.3 - which moves
the whole band up while keeping neighbouring shades within ~1.3 steps of each other. The shading depth is
kept in absolute terms; the ship simply sits higher on the value scale.

⚠ THE OUTLINE STAYS DARK. Lifting every neutral pixel would lift the plate's dark edge with the body and
leave a light-gray ship with a light-gray rim on a light sky - the silhouette dissolves. Ink within
OUTLINE_PX of transparency is left exactly as authored.

Guards (the 0912u reasoning, since chroma is removed from the paint): alpha delta 0; the touched band keeps
at least VLEVEL_MIN of its distinct value levels; no saturated red left; the RGB palette ratio is reported.
"""
import os, sys, argparse
import numpy as np
from PIL import Image, ImageDraw

PLATES = ['interceptor.png', 'interceptor-damaged.png']
FULL_DEG, FADE_DEG = 10.0, 24.0        # the paint band, feathered exactly as the black swap's
PAINT_SAT = 0.12                       # paint chroma kept - a whisper of warmth, reads gray
PAINT_LIFT, PAINT_GAIN = 0.36, 1.20    # paint v p50 0.42 -> ~0.86 would be white; see clamp below
PAINT_CAP = 0.80                       # light gray, never paper white
BODY_SAT = 0.80                        # body chroma multiplier (it is nearly neutral already)
BODY_LIFT, BODY_GAIN = 0.30, 1.30      # body v p50 0.13 -> ~0.47, p95 0.33 -> ~0.73
BODY_CAP = 0.86
NEUTRAL_S = 0.18                       # at or below this saturation a pixel counts as hull metal
OUTLINE_PX = 2                         # the dark edge that stays dark
VLEVEL_MIN = 0.60


def hsv(a):
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    mx = a.max(-1); mn = a.min(-1); d = mx - mn
    h = np.zeros_like(mx); m = d > 1e-9
    rm = m & (mx == r); gm = m & (mx == g) & ~rm; bm = m & ~rm & ~gm
    h[rm] = ((g[rm] - b[rm]) / d[rm]) % 6
    h[gm] = (b[gm] - r[gm]) / d[gm] + 2
    h[bm] = (r[bm] - g[bm]) / d[bm] + 4
    return h * 60.0, np.where(mx > 0, d / np.maximum(mx, 1e-9), 0.0), mx


def to_rgb(h, s, v):
    h = (h % 360.0) / 60.0
    i = np.floor(h); f = h - i
    p = v * (1 - s); q = v * (1 - f * s); t = v * (1 - (1 - f) * s)
    i = i.astype(int) % 6
    out = np.zeros(h.shape + (3,))
    for k, (R, G, B) in enumerate([(v, t, p), (q, v, p), (p, v, t), (p, q, v), (t, p, v), (v, p, q)]):
        mk = i == k
        out[mk, 0] = R[mk]; out[mk, 1] = G[mk]; out[mk, 2] = B[mk]
    return out


def outline_ring(alpha, px):
    """Ink within px pixels (4-neighbour steps) of transparency."""
    solid = alpha > 8
    ring = np.zeros_like(solid)
    cur = ~solid
    for _ in range(px):
        grow = cur.copy()
        grow[1:, :] |= cur[:-1, :]; grow[:-1, :] |= cur[1:, :]
        grow[:, 1:] |= cur[:, :-1]; grow[:, :-1] |= cur[:, 1:]
        ring |= grow & solid
        cur = grow
    return ring


def opaque_colours(a8):
    m = a8[..., 3] > 200
    return len(np.unique(a8[..., :3][m].reshape(-1, 3), axis=0)) if m.any() else 0


def swap(img):
    a8 = np.asarray(img.convert('RGBA')).astype(np.uint8)
    a = a8[..., :3].astype(np.float64) / 255.0
    ink = a8[..., 3] > 8
    h, s, v = hsv(a)
    ring = outline_ring(a8[..., 3], OUTLINE_PX)
    dist = np.minimum(np.abs(h), np.abs(360.0 - h))
    wp = np.clip((FADE_DEG - dist) / (FADE_DEG - FULL_DEG), 0, 1)
    wp = np.where(ink & ~ring & (s > NEUTRAL_S), wp, 0.0)            # paint weight
    body = ink & ~ring & (s <= NEUTRAL_S)                            # hull metal
    s2 = s.copy(); v2 = v.copy()
    # paint -> light gray, blended by its feather weight
    ps = s * PAINT_SAT
    pv = np.minimum(PAINT_CAP, PAINT_LIFT + PAINT_GAIN * v * 0.62)
    s2 = s2 * (1 - wp) + ps * wp
    v2 = v2 * (1 - wp) + pv * wp
    # body metal -> mid/light gray
    s2 = np.where(body, s * BODY_SAT, s2)
    v2 = np.where(body, np.minimum(BODY_CAP, BODY_LIFT + BODY_GAIN * v), v2)
    # ⚠ THE OUTLINE RING KEEPS ITS VALUE, NOT ITS RED. The first run excluded the ring from the paint swap
    # entirely and left ~1,000 saturated red pixels per plate as a red rim along every wing edge. Paint in
    # the ring is desaturated like the rest of the paint, but its VALUE is left as authored - the edge
    # stays dark, which is what the ring exists to protect.
    wr = np.clip((FADE_DEG - dist) / (FADE_DEG - FULL_DEG), 0, 1)
    wr = np.where(ring & (s > NEUTRAL_S), wr, 0.0)
    s2 = s2 * (1 - wr) + (s * PAINT_SAT) * wr
    touched = (wp > 0) | body | (wr > 0)
    rgb = to_rgb(h, s2, v2)
    o = a8.copy()
    o[..., :3] = np.where(touched[..., None], np.clip(rgb * 255 + 0.5, 0, 255).astype(np.uint8), a8[..., :3])
    oh, os_, ov = hsv(o[..., :3].astype(np.float64) / 255.0)
    odist = np.minimum(np.abs(oh), np.abs(360.0 - oh))
    return Image.fromarray(o, 'RGBA'), {
        'touched': int(touched.sum()), 'paint': int((wp >= 0.999).sum()), 'body': int(body.sum()), 'ring': int(ring.sum()),
        'before': opaque_colours(a8), 'after': opaque_colours(o),
        'vlevels_before': int(len(np.unique(np.round(v[touched] * 255)))),
        'vlevels_after': int(len(np.unique(np.round(ov[touched] * 255)))),
        'body_v': (round(float(np.median(v[body])), 3), round(float(np.median(ov[body])), 3)),
        'ring_v_delta': round(float(np.abs(ov[ring] - v[ring]).max()) if ring.any() else 0.0, 4),
        'alpha_delta': int(np.abs(o[..., 3].astype(int) - a8[..., 3].astype(int)).sum()),
        'red_left': int((ink & (os_ > 0.30) & (ov > 0.15) & (odist < 12)).sum()),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--src', required=True, help='the RED originals')
    ap.add_argument('--black', default='', help='the black plates, for the side-by-side proof only')
    ap.add_argument('--out', required=True)
    ap.add_argument('--proof', required=True)
    ap.add_argument('--field', default='')
    ap.add_argument('--write', action='store_true')
    a = ap.parse_args()
    rows, bad = [], []
    for name in PLATES:
        src = Image.open(os.path.join(a.src, name)).convert('RGBA')
        out, info = swap(src)
        ratio = info['after'] / max(1, info['before'])
        vr = info['vlevels_after'] / max(1, info['vlevels_before'])
        ok = vr >= VLEVEL_MIN and info['alpha_delta'] == 0 and info['red_left'] < 50 and info['ring_v_delta'] < 0.01
        print('%-24s touched %7d (paint %6d body %6d, outline ring %5d kept)  palette %6d -> %6d (%.2f)  '
              'value levels %d -> %d  body v %.3f -> %.3f  alpha delta %d  red left %d%s'
              % (name, info['touched'], info['paint'], info['body'], info['ring'], info['before'], info['after'], ratio,
                 info['vlevels_before'], info['vlevels_after'], info['body_v'][0], info['body_v'][1],
                 info['alpha_delta'], info['red_left'], '' if ok else '   <-- REFUSED'))
        if not ok: bad.append(name)
        blk = Image.open(os.path.join(a.black, name)).convert('RGBA') if a.black and os.path.exists(os.path.join(a.black, name)) else None
        rows.append((name, src, blk, out))
        if a.write and ok:
            os.makedirs(a.out, exist_ok=True)
            out.save(os.path.join(a.out, name))
    field = Image.open(a.field).convert('RGBA') if a.field and os.path.exists(a.field) else None
    TW, TH = 300, int(300 * 700 / 807)
    tiles = []
    for name, src, blk, out in rows:
        seq = [('red', src)] + ([('black', blk)] if blk is not None else []) + [('light gray', out)]
        pair = Image.new('RGBA', (len(seq) * (TW + 8), TH), (12, 16, 24, 255))
        for i, (_, im) in enumerate(seq):
            t = im.resize((TW, TH), Image.LANCZOS); pair.paste(t, (i * (TW + 8), 0), t)
        tiles.append((name + '   ' + ' | '.join(l for l, _ in seq), pair))
        if field is not None:
            fw, fh = field.size
            crop = field.crop((0, int(fh * 0.12), min(fw, 960), int(fh * 0.12) + 380)).resize((960, 380))
            for i, (_, im) in enumerate(seq[1:] if blk is not None else seq):
                t = im.resize((216, 187), Image.LANCZOS); crop.paste(t, (560 + i * 200 - (200 if blk is None else 0), 90), t)
            tiles.append((name + '   on the live stage field (black, then light gray)', crop))
    H = sum(t.height + 26 for _, t in tiles) + 10
    W = max(t.width for _, t in tiles) + 20
    sheet = Image.new('RGBA', (W, H), (6, 8, 12, 255))
    d = ImageDraw.Draw(sheet); y = 6
    for label, t in tiles:
        d.text((10, y), label, fill=(124, 245, 255, 255)); sheet.paste(t, (10, y + 18)); y += t.height + 26
    os.makedirs(os.path.dirname(os.path.abspath(a.proof)), exist_ok=True)
    sheet.save(a.proof)
    print('proof ->', a.proof)
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main())
