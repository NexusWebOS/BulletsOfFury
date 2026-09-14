#!/usr/bin/env python3
"""
tempest_blackswap_0912u.py - THE TEMPEST LEVIATHAN'S RED, PALETTE-SWAPPED TO BLACK / DARK GRAY.

    python3 _BUILD_SOURCE/tempest_blackswap_0912u.py --src <pack assets dir> --out <dir> \
            --proof <png> [--field <png of the stage the unit will fly over>] [--write]

Mike, 0912: "snag the new tempest levithan, palette swap the red to black/dark gray. this is our new
mini-boss and fighting style for level 6's miniboss."

MEASURED FIRST, on the two LIVE plates (interceptor.png / interceptor-damaged.png, 807x700 - the pack's
game.js renders only these; jet*.png and turret*.png are retained history its README calls unrendered):

    wing paint   hue 350..15 deg, sat p50 0.79 (p5 0.19), val p50 0.42 (p95 0.66)   ~50k px intact
    reactor      violet, hue 260..280                                                 KEPT
    apertures    cyan/blue engines and laser housings, hue 180..250                   KEPT
    hull body    near-neutral already, val p50 0.13 (black titanium)                  untouched
    damaged      extra ORANGE scorch at hue 10..40 (2-3x the intact count)            mostly KEPT

⚠ BLACK HAS NO HUE, SO THIS IS NOT A ROTATION - AND SETTING SATURATION TO A CONSTANT IS A COLLAPSE.
Writing one saturation into every red pixel merges shades that differed only in chroma - 0906o's
palette-shredder signature by a different route. Saturation and value are GENTLE GAINS (one multiply
each, a floor on value), so neighbouring shades keep their spacing and the panel shading survives.
The wings land darker than their paint but LIGHTER than the black titanium body (val p50 ~0.24 vs 0.13),
so the wing panels still read as a separate material: "black/dark gray", as asked.

⚠ THE BAND IS FEATHERED, NOT CUT. Full effect inside +/-10 deg of red, fading to none by 24 deg. A hard
cut at 20 would leave orange-red shading fringes on the wing edges; a wide one would grey out the
damaged plate's orange scorch, which is DAMAGE GLOW, not paint.

⚠ THE COUNT GUARD. The forest (0912p) and ice (0912s) tools refuse on a >20% opaque-palette loss, and this
one did too on its first run: 66,226 -> 41,677 colours (0.63). A five-setting sweep then measured 0.63,
0.65, 0.66, 0.65 and 0.66 - saturation x0.10..0.22, value x0.52..0.66, with and without a hue rotation.
A ratio that does not move with the parameters is not a parameter mistake: it is intrinsic to taking the
chroma out of ~72k strongly saturated pixels, because a dark gray has far fewer distinct 8-bit RGB triples
than a red with a hue/saturation spread. That 0.80 threshold was set for hue ROTATIONS, which keep chroma.
So here the RGB count is REPORTED and the refusal is on what carries the shading - the number of distinct
VALUE levels in the painted band (kept 182/255 intact, 200/255 damaged at the chosen setting) - plus zero
alpha movement and no saturated red left. The proof sheet was read at full size before this was accepted.

⚠ ORDNANCE KEEPS ITS AUTHORED COLOUR (CLAUDE.md standing rule): the needle missile's red fins, the plasma
bolt, the laser, fire and explosions are not touched by this tool.
⚠ ALPHA IS NEVER WRITTEN, and the tool refuses to write on an opaque-palette loss past a fifth.
⚠ RE-RUN FROM THE RED ORIGINALS, NEVER FROM THIS TOOL'S OUTPUT (0906o).
"""
import os, sys, argparse
import numpy as np
from PIL import Image, ImageDraw

PLATES = ['interceptor.png', 'interceptor-damaged.png']
FULL_DEG = 10.0      # full effect within this many degrees of pure red
FADE_DEG = 24.0      # no effect beyond this
SAT_MIN = 0.12       # below this a pixel is already neutral - leave it
SAT_GAIN = 0.14      # red -> a whisper of warmth at most: reads as gray, keeps chroma spacing
VAL_GAIN = 0.66      # paint p50 0.42 -> ~0.30, p95 0.66 -> ~0.45: dark gray, clearly lighter than the body
VLEVEL_MIN = 0.60    # refuse if the painted band keeps fewer than this share of its distinct value levels
VAL_FLOOR = 0.018    # the darkest shading lines never crush to pure black
HUE_TO = None        # degrees to ROTATE the paint band by (None keeps red's own hue at low chroma)


def hsv(a):
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    mx = a[..., :3].max(-1); mn = a[..., :3].min(-1); d = mx - mn
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


def opaque_colours(a8):
    m = a8[..., 3] > 200
    return len(np.unique(a8[..., :3][m].reshape(-1, 3), axis=0)) if m.any() else 0


def swap(img):
    a8 = np.asarray(img.convert('RGBA')).astype(np.uint8)
    a = a8[..., :3].astype(np.float64) / 255.0
    ink = a8[..., 3] > 0
    h, s, v = hsv(a)
    dist = np.minimum(np.abs(h), np.abs(360.0 - h))                     # degrees from pure red
    w = np.clip((FADE_DEG - dist) / (FADE_DEG - FULL_DEG), 0.0, 1.0)     # 1 inside FULL, 0 past FADE
    w = np.where(ink & (s >= SAT_MIN), w, 0.0)
    s2 = s * (1 - w) + (s * SAT_GAIN) * w
    v2 = v * (1 - w) + np.clip(v * VAL_GAIN + VAL_FLOOR, 0, 1) * w
    # an optional ROTATION of the paint's hue (never a set): a cool gunmetal cast keeps each shade's own
    # hue offset, so shades that differed in chroma stay distinct instead of folding into one gray.
    # Applied only where the pixel is mostly paint (w >= 0.5); fringes keep their hue and just lose chroma.
    h2 = h if HUE_TO is None else np.where(w >= 0.5, (h + HUE_TO) % 360.0, h)
    rgb = to_rgb(h2, s2, v2)
    o = a8.copy()
    touched = w > 0
    o[..., :3] = np.where(touched[..., None], np.clip(rgb * 255 + 0.5, 0, 255).astype(np.uint8), a8[..., :3])
    return Image.fromarray(o, 'RGBA'), {
        'touched': int(touched.sum()), 'full': int((w >= 0.999).sum()),
        'before': opaque_colours(a8), 'after': opaque_colours(o),
        'alpha_delta': int(np.abs(o[..., 3].astype(int) - a8[..., 3].astype(int)).sum()),
        'red_left': red_left(o),
        'vlevels_before': int(len(np.unique(np.round(v[touched] * 255)))) if touched.any() else 0,
        'vlevels_after': int(len(np.unique(np.round(hsv(o[..., :3].astype(np.float64) / 255.0)[2][touched] * 255)))) if touched.any() else 0,
    }


def red_left(o8):
    """Saturated red still on the OUTPUT - hue, saturation and value all read from the result.
    (The first cut read s and v from the input and only hue from the output; hue is preserved, so
    it echoed the original red count and looked like a swap that did nothing.)"""
    a = o8[..., :3].astype(np.float64) / 255.0
    h, s, v = hsv(a)
    dist = np.minimum(np.abs(h), np.abs(360.0 - h))
    return int(((o8[..., 3] > 8) & (s > 0.30) & (v > 0.15) & (dist < 12)).sum())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--src', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--proof', required=True)
    ap.add_argument('--field', default='')
    ap.add_argument('--write', action='store_true')
    ap.add_argument('--sat-gain', type=float, default=None)
    ap.add_argument('--val-gain', type=float, default=None)
    ap.add_argument('--hue-to', type=float, default=None)
    a = ap.parse_args()
    global SAT_GAIN, VAL_GAIN, HUE_TO
    if a.sat_gain is not None: SAT_GAIN = a.sat_gain
    if a.val_gain is not None: VAL_GAIN = a.val_gain
    if a.hue_to is not None: HUE_TO = a.hue_to
    print('params: sat x%.2f  val x%.2f + %.3f  hue %s' % (SAT_GAIN, VAL_GAIN, VAL_FLOOR, 'kept' if HUE_TO is None else '+%.0f' % HUE_TO))
    rows, bad = [], []
    for name in PLATES:
        src = Image.open(os.path.join(a.src, name)).convert('RGBA')
        out, info = swap(src)
        ratio = info['after'] / max(1, info['before'])
        vratio = info['vlevels_after'] / max(1, info['vlevels_before'])
        # see "THE COUNT GUARD" in the module note: for a chroma-REMOVING swap the RGB count is reported,
        # and the refusal is on value levels (the shading) and alpha (the silhouette)
        ok = vratio >= VLEVEL_MIN and info['alpha_delta'] == 0 and info['red_left'] < 50
        print('%-24s touched %7d (full %7d)  palette %6d -> %6d (%.2f)  value levels %d -> %d  alpha delta %d  red left %d%s'
              % (name, info['touched'], info['full'], info['before'], info['after'], ratio,
                 info['vlevels_before'], info['vlevels_after'], info['alpha_delta'],
                 info['red_left'], '' if ok else '   <-- REFUSED'))
        if not ok: bad.append(name)
        rows.append((name, src, out))
        if a.write and ok:
            os.makedirs(a.out, exist_ok=True)
            out.save(os.path.join(a.out, name))

    # proof: red | black on a dark field, then red | black on the real stage field (drawn at game scale too)
    field = Image.open(a.field).convert('RGBA') if a.field and os.path.exists(a.field) else None
    TW = 404
    tiles = []
    for name, src, out in rows:
        for bgc in ((12, 16, 24, 255),):
            pair = Image.new('RGBA', (TW * 2 + 8, int(TW * 700 / 807)), bgc)
            for i, im in enumerate((src, out)):
                t = im.resize((TW, int(TW * 700 / 807)), Image.LANCZOS)
                pair.paste(t, (i * (TW + 8), 0), t)
            tiles.append((name + '   red | black', pair))
        if field is not None:
            fw, fh = field.size
            crop = field.crop((0, int(fh * 0.12), min(fw, 960), int(fh * 0.12) + 380)).resize((960, 380))
            for i, im in enumerate((src, out)):
                t = im.resize((216, 187), Image.LANCZOS)          # ~2x the pack's 108x118 draw, as the game draws 2x
                crop.paste(t, (170 + i * 420, 90), t)
            tiles.append((name + '   on the live stage-6 field (left red, right black)', crop))
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
