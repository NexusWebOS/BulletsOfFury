"""PIXEL GLOW baker (1015).

Mike: "pixel glow should occur instead of overlayed graphics like our stage 5 boss's middle core."

A glow that is a second sprite pasted over the hull (a radial disc, an effect cell, a blurred halo) reads as a
sticker: it has its own silhouette, it does not follow the art's panels, and it sits on a different pixel grid.
Pixel glow lights the art's OWN emissive pixels - the core ring, the panel lights, the energy seams - and lets
that light spill one, two, three pixels past them in hard steps, the way a 16-bit palette cycle does.

This script bakes, for each registered sheet, a companion GLOW sheet of the exact same size and layout:
  * every emissive source pixel, at its own hue pushed toward white (the hot core of the light);
  * three hard rings around the emissive regions (1, 2, 3 px at the sheet's native scale), at falling alpha,
    in the colour of the nearest emissive pixel - no blur, no new silhouette;
  * a CORE sheet holding only each cell's largest emissive cluster, so a charge can drive the core harder
    than the panel lights.
Because the companion shares the source's rectangles, the runtime redraws it with the exact source/dest
rectangles the body blit used, so it cannot drift off the art. Nothing is read from pixels at runtime
(file:// taints the canvas, CLAUDE.md 0917b), and the source art is never modified.

Emissive = opaque, bright and saturated in the sheet's light hue band, or near-white. The hue band and
thresholds are per sheet in SHEETS, measured on the art; --check writes a contact sheet to verify by eye.
Usage: python _BUILD_SOURCE/pixel_glow_1015.py [--check]
"""
import colorsys, json, sys
from pathlib import Path
import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = Path(__file__).resolve().parents[1]
OUTD = ROOT / 'assets/game/shared/combat/pixel_glow_1015'
A5 = 'assets/game/levels/stage_05/boss/stage5_archmage_0916/'
# key: XART key of the source sheet; cells: grid or explicit rects used to split CORE clusters per cell.
SHEETS = [
    {'key': 'arch_orbital_sweep_0926', 'src': A5 + 'combat_0926/hammer_strike_v2.png', 'hue': (0.50, 0.72), 'grid': (4, 3)},
    {'key': 'arch_chaingun_break_enrage', 'src': A5 + 'chaingun_break_enrage.png', 'hue': (0.0, 1.0), 'grid': (16, 1), 'v': 0.40, 's': 0.30, 'hot': 0.80, 'core_window': 0.52},
    {'key': 'arch_leap_strike_0922', 'src': A5 + 'leap_strike_0922.png', 'hue': (0.50, 0.72), 'grid': (8, 1)},
    {'key': 'arch_spell_raise', 'src': A5 + 'spell_raise.png', 'hue': (0.50, 0.72), 'grid': (12, 1)},
]
# LOOSE per-frame plates: every frame is its own PNG of one shared size, so the runtime recognises them by
# the key XART.get was asked for (tag), never by size. One row per frame.
PT = 'assets/game/shared/combat/playthrough_1011/'
SHEETS += [{'key': 'pt11_hammer_core_%d' % i, 'src': PT + 'hammer_core_%02d.png' % i, 'hue': (0.50, 0.72), 'grid': (1, 1), 'loose': True}
           for i in range(16)]
RING_A = (0.58, 0.34, 0.16)     # alpha of the 1st/2nd/3rd hard ring past the emissive pixels


def emissive_mask(rgba, hue, vmin=0.62, smin=0.42, hotv=0.92):
    a = rgba[..., 3] > 200
    rgb = rgba[..., :3].astype(np.float32) / 255
    mx, mn = rgb.max(-1), rgb.min(-1)
    v, s = mx, np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0)
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    h = np.zeros_like(v)
    d = np.maximum(mx - mn, 1e-6)
    h = np.where(mx == r, ((g - b) / d) % 6, h)
    h = np.where(mx == g, (b - r) / d + 2, h)
    h = np.where(mx == b, (r - g) / d + 4, h)
    h = h / 6
    lit = (v > vmin) & (s > smin) & (h >= hue[0]) & (h <= hue[1])
    hot = (v > hotv) & (s < 0.35)
    m = a & (lit | hot)
    # a lone lit pixel is a specular glint on the armour, not a light: keep clusters of 3+
    lab, n = ndimage.label(m)
    if n:
        sizes = ndimage.sum(m, lab, range(1, n + 1))
        keep = np.zeros(n + 1, bool); keep[1:] = sizes >= 3
        m = keep[lab]
    return m


def bake(sheet):
    im = Image.open(ROOT / sheet['src']).convert('RGBA')
    src = np.array(im)
    H, W = src.shape[:2]
    m = emissive_mask(src, sheet['hue'], sheet.get('v', 0.62), sheet.get('s', 0.42), sheet.get('hot', 0.92))
    # the light's own pixels, pushed toward white by how bright they already are
    rgb = src[..., :3].astype(np.float32)
    # ADDED light, not a replacement colour: the companion is drawn under 'lighter', so a lit pixel only
    # takes back about half its own colour. Pushing it toward white flooded the authored core ring into a
    # flat white disc - the very sticker look this pass removes (seen in the first preview, 1015).
    hotc = rgb * 0.48
    glow = np.zeros((H, W, 4), np.float32)
    glow[m, :3] = hotc[m]; glow[m, 3] = 255
    # hard rings: distance (in pixels) from the emissive set, coloured by the nearest emissive pixel
    dist, idx = ndimage.distance_transform_edt(~m, return_indices=True)
    near = rgb[idx[0], idx[1]]
    for k, al in enumerate(RING_A, start=1):
        ring = (dist > k - 1) & (dist <= k) & ~m
        glow[ring, :3] = near[ring]; glow[ring, 3] = 255 * al
    # CORE: per cell, only the largest emissive cluster (the chest core on every authored pose)
    core_m = np.zeros_like(m)
    gx, gy = sheet['grid']; cw, ch = W // gx, H // gy
    for j in range(gy):
        for i in range(gx):
            sub = m[j * ch:(j + 1) * ch, i * cw:(i + 1) * cw]
            if sheet.get('core_window'):
                # this reel paints its chest ring in the same pale steel as the armour highlights, so colour
                # cannot find it: look only inside a torso window (pose ink centre, 15-45% down) for bright pixels
                cell = src[j * ch:(j + 1) * ch, i * cw:(i + 1) * cw].astype(np.float32)
                al = cell[..., 3] > 200
                ys, xs = np.nonzero(al)
                if len(ys):
                    vv = cell[..., :3].max(-1) / 255
                    cx0, top, hh = (xs.min() + xs.max()) / 2, ys.min(), ys.max() - ys.min()
                    yy, xx = np.mgrid[0:ch, 0:cw]
                    win = (np.abs(xx - cx0) < hh * 0.16) & (yy > top + hh * 0.13) & (yy < top + hh * 0.45)
                    sub = sub | (al & win & (vv > sheet['core_window']))
            lab, n = ndimage.label(sub)
            if not n:
                continue
            # the chest core, not the hammer head: of the clusters big enough to be a light, take the one
            # nearest the torso guess (centre of the pose's ink, 30% down from its top)
            al = src[j * ch:(j + 1) * ch, i * cw:(i + 1) * cw, 3] > 200
            ys, xs = np.nonzero(al)
            if not len(ys):
                continue
            gx0, gy0 = (xs.min() + xs.max()) / 2, ys.min() + (ys.max() - ys.min()) * 0.30
            sizes = ndimage.sum(sub, lab, range(1, n + 1))
            cents = ndimage.center_of_mass(sub, lab, range(1, n + 1))
            best, bd = None, 1e9
            for k, (sz, (cy, cx)) in enumerate(zip(sizes, cents), start=1):
                if sz < 12:
                    continue
                d = ((cx - gx0) ** 2 + (cy - gy0) ** 2) ** 0.5 - sz ** 0.5 * 0.8
                if d < bd:
                    best, bd = k, d
            if best is not None:
                core_m[j * ch:(j + 1) * ch, i * cw:(i + 1) * cw] = lab == best
    cd, cidx = ndimage.distance_transform_edt(~core_m, return_indices=True)
    cnear = rgb[cidx[0], cidx[1]]
    core = np.zeros((H, W, 4), np.float32)
    core[core_m, :3] = rgb[core_m] * 0.42; core[core_m, 3] = 255
    for k, al in enumerate((0.70, 0.46, 0.26, 0.12), start=1):
        ring = (cd > k - 1) & (cd <= k) & ~core_m
        core[ring, :3] = cnear[ring]; core[ring, 3] = 255 * al
    OUTD.mkdir(parents=True, exist_ok=True)
    gp = OUTD / (sheet['key'] + '_glow.png'); cp = OUTD / (sheet['key'] + '_core.png')
    Image.fromarray(glow.clip(0, 255).astype(np.uint8), 'RGBA').save(gp, optimize=True)
    Image.fromarray(core.clip(0, 255).astype(np.uint8), 'RGBA').save(cp, optimize=True)
    return {'key': sheet['key'], 'loose': bool(sheet.get('loose')), 'glow': str(gp.relative_to(ROOT)), 'core': str(cp.relative_to(ROOT)),
            'size': [W, H], 'emissive_px': int(m.sum()), 'core_px': int(core_m.sum()),
            'opaque_px': int((src[..., 3] > 200).sum())}


def check(results):
    from PIL import ImageDraw
    rows = []
    for r in results:
        src = Image.open(ROOT / next(s['src'] for s in SHEETS if s['key'] == r['key'])).convert('RGBA')
        W, H = src.size
        cell = (W // next(s['grid'] for s in SHEETS if s['key'] == r['key'])[0], H)
        cw = min(W, 420)
        crop = (0, 0, cw, min(H, 380))
        g = Image.open(ROOT / r['glow']).convert('RGBA'); c = Image.open(ROOT / r['core']).convert('RGBA')
        panes = []
        for lvl, lay in ((0, None), (1, g), (2, c)):
            bg = Image.new('RGBA', src.size, (24, 26, 34, 255)); bg.alpha_composite(src)
            if lay is not None:
                a = np.array(bg).astype(np.float32); l = np.array(lay).astype(np.float32)
                a[..., :3] = np.minimum(255, a[..., :3] + l[..., :3] * (l[..., 3:4] / 255) * 0.85)
                bg = Image.fromarray(a.astype(np.uint8))
            panes.append(bg.crop(crop))
        row = Image.new('RGBA', (cw * 3 + 20, crop[3]), (10, 10, 14, 255))
        for i, p in enumerate(panes):
            row.paste(p, (i * (cw + 10), 0))
        rows.append(row)
    out = Image.new('RGBA', (max(r.width for r in rows), sum(r.height for r in rows)), (10, 10, 14, 255))
    y = 0
    for r in rows:
        out.paste(r, (0, y)); y += r.height
    p = ROOT / '_shots/pixel_glow_1015/bake_check.png'; p.parent.mkdir(parents=True, exist_ok=True)
    out.resize((out.width * 2, out.height * 2), Image.NEAREST).save(p)
    print('check ->', p)


if __name__ == '__main__':
    res = [bake(s) for s in SHEETS]
    (OUTD / 'pixel_glow_1015.json').write_text(json.dumps(res, indent=1))
    js = 'const PXG_SHEETS=' + json.dumps({r['key']: {'glow': r['glow'], 'core': r['core'], 'size': r['size'], **({'loose': 1} if r['loose'] else {})} for r in res}) + ';\n'
    (ROOT / 'assets/pixel_glow_art_1015.js').write_text('"use strict";\n/* generated by _BUILD_SOURCE/pixel_glow_1015.py - do not hand-edit */\n' + js)
    for r in res:
        print(r['key'], 'emissive', r['emissive_px'], 'core', r['core_px'], 'of', r['opaque_px'])
    if '--check' in sys.argv:
        check([r for r in res if not r['loose']])
