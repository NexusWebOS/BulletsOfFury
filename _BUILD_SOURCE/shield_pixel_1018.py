#!/usr/bin/env python3
"""shield_pixel_1018.py - bake every pilot's shield as a PIXEL-ANIMATED, PIXEL-GLOWING reel.

Mike, 1018: "the shields arent very pixel animated and I meant make it pixel glow. not a rotating glow around body."

The first 1018 pass lit the shell with a blurred halo and a sector that circled the ship. That is the overlay look
he rejected; pixel glow here means what docs/PIXEL_GLOW_1015.md built for the Stage 5 Hammer core: light from the
art's OWN pixels, spilling past them in HARD one-pixel rings, stepped on a fixed ladder like a 16-bit palette cycle -
no blur, no smooth fade, nothing rotating.

For each pilot this bakes, at the EXACT size the shell is drawn in game (so every frame lands 1:1 on the game's
pixel grid and nothing is resampled at runtime):
  shield_<pk>.png       12 frames: the authored crystal shell, with light FLOWING nose -> tail through its own
                        tonal bands (a palette cycle: each band brightens in turn, in hard steps) and pixel
                        sparkles (1 px star, 3 frames) on its brightest facets
  shield_<pk>_glow.png  12 frames: added light - the shell's emissive pixels at half strength plus two hard rings
                        outside the rim, their brightness walking a six-step ladder
and assets/shield_pixel_1018.js (SHIELD_PX_1018[pk] = {key, glow, frames, fps, w, h, hole:[cx,cy]}).

Sizing reproduces the runtime fit exactly: the shell's ship-shaped hole (SHIELD_FIT_1018) encloses the hull's ink
box from its manifest row x PS18_CLEAR, uniform scale, and the hole centre goes on the hull centre.

    python _BUILD_SOURCE/shield_pixel_1018.py [--check]
"""
import os, sys, re, json, math
import numpy as np
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'assets', 'game', 'shared', 'combat', 'part2_1010')
OUTD = os.path.join(ROOT, 'assets', 'game', 'shared', 'combat', 'shield_1018')
OUTJS = os.path.join(ROOT, 'assets', 'shield_pixel_1018.js')
PILOTS = ['cole', 'maverick', 'lizzie', 'juggernaut', 'yuri', 'freezer', 'falva', 'decker', 'axel']
SHIP_DRAW_H = 60
CLEAR = 1.16                       # must equal PS18_CLEAR in player_shield_1018.js
FRAMES, FPS = 12, 10
LADDER = (0.30, 0.40, 0.52, 0.62, 0.52, 0.40)      # glow ring strength, stepped (a 16-bit palette cycle)
RING_A = (0.62, 0.30)              # 1st / 2nd hard ring alpha at full ladder
CYCLE = (0.0, 0.18, 0.34, 0.18, 0.0, -0.16)   # per-tone brightness ladder (positive: toward white, negative: darker)

def fit_data():
    s = open(os.path.join(ROOT, 'assets', 'shield_fit_1018.js'), encoding='utf-8').read()
    return json.loads(re.search(r'const SHIELD_FIT_1018=(\{.*\});', s, re.S).group(1))

def ship_row(pk, man):
    m = re.search(r'"ship_%s":\s*(\[[^\]]*\])' % pk, man)
    return json.loads(m.group(1))

def reduce_plate(im, W, H):
    """Area-average down in premultiplied space, then make alpha HARD (pixel art: a pixel is in or out)."""
    a = np.asarray(im, dtype=np.float64) / 255.0
    pm = a.copy(); pm[..., :3] *= pm[..., 3:4]
    small = np.asarray(Image.fromarray((pm * 255).astype(np.uint8), 'RGBA').resize((W, H), Image.Resampling.BOX), dtype=np.float64) / 255.0
    al = small[..., 3]
    rgb = np.where(al[..., None] > 1e-4, small[..., :3] / np.maximum(al[..., None], 1e-4), 0)
    keep = al >= 0.42
    out = np.zeros((H, W, 4)); out[..., :3] = np.clip(rgb, 0, 1); out[..., 3] = keep
    return out

def lum(rgb): return 0.2126 * rgb[..., 0] + 0.7152 * rgb[..., 1] + 0.0722 * rgb[..., 2]

def ring_bands(mask, n):
    """Chebyshev distance bands outside the mask, 1..n pixels (hard, square-cornered: pixel art rings)."""
    H, W = mask.shape; d = np.full((H, W), 99, np.int16); d[mask] = 0
    cur = mask.copy()
    for i in range(1, n + 1):
        grow = cur.copy()
        grow[1:, :] |= cur[:-1, :]; grow[:-1, :] |= cur[1:, :]; grow[:, 1:] |= cur[:, :-1]; grow[:, :-1] |= cur[:, 1:]
        grow[1:, 1:] |= cur[:-1, :-1]; grow[:-1, :-1] |= cur[1:, 1:]; grow[1:, :-1] |= cur[:-1, 1:]; grow[:-1, 1:] |= cur[1:, :-1]
        d[grow & ~cur] = i; cur = grow
    return d

def nearest_colour(rgb, mask, n):
    """Spread the shell colour outward n pixels so a ring takes the colour of the crystal beside it."""
    col = rgb.copy(); have = mask.copy()
    for _ in range(n):
        g = have.copy(); c = col.copy()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            src = np.roll(np.roll(have, dy, 0), dx, 1); sc = np.roll(np.roll(col, dy, 0), dx, 1)
            take = src & ~g
            c[take] = sc[take]; g |= take
        col, have = c, g
    return col

def bake(pk, fit, man):
    F = fit[pk]; r = ship_row(pk, man); k = SHIP_DRAW_H / r[7]
    hw, hh = F['hole'][2] - F['hole'][0], F['hole'][3] - F['hole'][1]
    s = max(r[2] * k * CLEAR / hw, r[3] * k * CLEAR / hh)
    W, H = max(8, round(F['plate'][0] * s)), max(8, round(F['plate'][1] * s))
    sx, sy = W / F['plate'][0], H / F['plate'][1]
    hole = ((F['hole'][0] + F['hole'][2]) / 2 * sx, (F['hole'][1] + F['hole'][3]) / 2 * sy)
    PAD = 3                                                      # room for the hard rings
    base = reduce_plate(Image.open(os.path.join(SRC, 'shield_%s.png' % pk)).convert('RGBA'), W, H)
    b = np.zeros((H + PAD * 2, W + PAD * 2, 4)); b[PAD:PAD + H, PAD:PAD + W] = base
    Hh, Ww = b.shape[:2]; mask = b[..., 3] > 0; rgb = b[..., :3]; L = lum(rgb)
    mx = rgb.max(-1); mn = rgb.min(-1); sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0)
    # tonal bands of the crystal (the palette the cycle walks), and a nose->tail coordinate for the flow
    lv = np.where(mask, L, np.nan); q = np.nanpercentile(lv, [35, 60, 80])
    band = np.digitize(L, q)                                     # 0 dark .. 3 brightest facets
    ys, xs = np.nonzero(mask); y0, y1 = ys.min(), ys.max()
    flow = ((np.arange(Hh)[:, None] - y0) / max(1, (y1 - y0)) * FRAMES).astype(int) + np.zeros((1, Ww), int)
    # sparkle sites: brightest facet pixels, spread out
    cand = sorted(zip(*np.nonzero(mask & (band >= 3))), key=lambda p: -L[p])
    sites = []
    for p in cand:
        if all(abs(p[0] - q2[0]) + abs(p[1] - q2[1]) > 7 for q2 in sites): sites.append(p)
        if len(sites) >= 10: break
    emissive = mask & (((L > 0.50) & (sat > 0.30)) | (L > 0.80))
    dist = ring_bands(mask, 2); near = nearest_colour(rgb, mask, 3)
    shell = np.zeros((Hh, Ww * FRAMES, 4), np.uint8); glow = np.zeros_like(shell)
    for f in range(FRAMES):
        o = b.copy()
        # PALETTE CYCLE: every crystal tone steps up and down a fixed ladder, each tone a beat behind the last, so
        # the whole shell shimmers in hard steps (the 16-bit way) without a single pixel moving or changing shape
        for tb in (1, 2, 3):
            stepv = CYCLE[(f + tb * 2) % len(CYCLE)]
            sel = mask & (band == tb)
            o[..., :3] = np.where(sel[..., None], np.clip(o[..., :3] * (1 + stepv), 0, 1) if stepv < 0 else o[..., :3] + (1 - o[..., :3]) * stepv, o[..., :3])
        # FLOW: a two-band wave of light runs nose -> tail through the crystal's lit tones in hard steps; the
        # outline and dark facets keep their pixels, so the silhouette never changes
        ph = (flow - f) % FRAMES
        lead = mask & ((ph == 0) | (ph == 1)) & (band >= 1)
        trail = mask & (ph == 2) & (band >= 1)
        o[..., :3] = np.where(lead[..., None], o[..., :3] + (1 - o[..., :3]) * 0.70, o[..., :3])
        o[..., :3] = np.where(trail[..., None], o[..., :3] + (1 - o[..., :3]) * 0.35, o[..., :3])
        # SPARKLES: a 1-px star on a bright facet, three frames (white core, cross, fade), staggered per site
        for i, (py, px) in enumerate(sites):
            age = (f - (i * 5) % FRAMES) % FRAMES
            if age == 0: o[py, px, :3] = 1.0
            elif age in (1, 2):
                o[py, px, :3] = 1.0
                for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    yy, xx = py + dy, px + dx
                    if 0 <= yy < Hh and 0 <= xx < Ww and mask[yy, xx]: o[yy, xx, :3] = o[yy, xx, :3] + (1 - o[yy, xx, :3]) * 0.7
            elif age == 3: o[py, px, :3] = o[py, px, :3] + (1 - o[py, px, :3]) * 0.6
        shell[:, f * Ww:(f + 1) * Ww] = (np.clip(o, 0, 1) * 255).round().astype(np.uint8)
        # GLOW (added light): emissive pixels at half their colour + two hard rings, strength on the ladder
        st = LADDER[f % len(LADDER)] / max(LADDER)
        g = np.zeros((Hh, Ww, 4))
        e = emissive | lead
        g[e, :3] = o[e, :3] * 0.5; g[e, 3] = 1.0 * st
        for i, al in enumerate(RING_A, 1):
            ring = dist == i
            g[ring, :3] = near[ring]; g[ring, 3] = al * st
        glow[:, f * Ww:(f + 1) * Ww] = (np.clip(g, 0, 1) * 255).round().astype(np.uint8)
    os.makedirs(OUTD, exist_ok=True)
    Image.fromarray(shell, 'RGBA').save(os.path.join(OUTD, 'shield_%s.png' % pk))
    Image.fromarray(glow, 'RGBA').save(os.path.join(OUTD, 'shield_%s_glow.png' % pk))
    return {'key': 'spx_shield_' + pk, 'glow': 'spx_shield_glow_' + pk,
            'path': 'assets/game/shared/combat/shield_1018/shield_%s.png' % pk,
            'glowPath': 'assets/game/shared/combat/shield_1018/shield_%s_glow.png' % pk,
            'frames': FRAMES, 'fps': FPS, 'w': Ww, 'h': Hh, 'hole': [round(hole[0] + PAD, 2), round(hole[1] + PAD, 2)],
            'sites': len(sites), 'scale': round(s, 5)}

def main():
    fit = fit_data(); man = open(os.path.join(ROOT, 'assets', 'manifest.js'), encoding='utf-8').read(); out = {}
    for pk in PILOTS:
        out[pk] = bake(pk, fit, man)
        print('%-10s %dx%d x%d frames  scale %.4f  hole centre %s  sparkle sites %d' % (pk, out[pk]['w'], out[pk]['h'], FRAMES, out[pk]['scale'], out[pk]['hole'], out[pk]['sites']))
    js = ('"use strict";\n/* Generated by _BUILD_SOURCE/shield_pixel_1018.py - do not edit by hand. Per-pilot pixel-animated\n'
          '   shield reels and their pixel-glow companions, baked at draw size (drawn 1:1). */\n'
          'const SHIELD_PX_1018=%s;\nfor(const v of Object.values(SHIELD_PX_1018)){XART._src[v.key]=v.path;XART._src[v.glow]=v.glowPath;}\n') % json.dumps(out, separators=(',', ':'))
    open(OUTJS, 'w', encoding='utf-8', newline='\n').write(js); print('wrote', OUTJS)
    if '--check' in sys.argv:
        rows = []
        for pk in PILOTS:
            sh = Image.open(os.path.join(OUTD, 'shield_%s.png' % pk)); gl = Image.open(os.path.join(OUTD, 'shield_%s_glow.png' % pk))
            bg = Image.new('RGBA', sh.size, (24, 26, 30, 255)); bg.alpha_composite(sh)
            a = np.asarray(bg).astype(np.int32); gg = np.asarray(gl).astype(np.int32)
            add = a.copy(); add[..., :3] = np.clip(a[..., :3] + gg[..., :3] * gg[..., 3:4] // 255, 0, 255)
            rows.append(Image.fromarray(add.astype(np.uint8), 'RGBA').resize((sh.width * 4, sh.height * 4), Image.Resampling.NEAREST))
        W = max(r.width for r in rows); sheet = Image.new('RGBA', (W, sum(r.height for r in rows)), (0, 0, 0, 255)); y = 0
        for r in rows: sheet.paste(r, (0, y)); y += r.height
        d = os.path.join(ROOT, '_shots', 'shield_1018'); os.makedirs(d, exist_ok=True); sheet.save(os.path.join(d, 'pixel_reels.png'))

if __name__ == '__main__':
    main()
