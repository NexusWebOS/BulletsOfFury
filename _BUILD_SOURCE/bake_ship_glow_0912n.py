#!/usr/bin/env python3
"""
bake_ship_glow_0912n.py - RE-BAKE THE FLAME FLICKER AGAINST THE CURRENT PLATES.

    python3 _BUILD_SOURCE/bake_ship_glow_0912n.py --dry
    python3 _BUILD_SOURCE/bake_ship_glow_0912n.py --proof /tmp/glow.png
    python3 _BUILD_SOURCE/bake_ship_glow_0912n.py --write

Mike, 0912: "re-bake against the current plates."

WHAT THIS RESTORES. 0906s replaced the deleted star-thruster overlay with per-frame PHASE cells -
`ship_<pilot><suffix>_g1` and `_g2`, the same plate with only the flame's INTERIOR brightness
changed - and `shipGlowKey()` cycles base -> g1 -> g2. The 0909 per-pilot re-pack deleted them, and
its own build script says why: "the pack has no phase art, and shipGlowKey falls back to the base
frame when a phase is absent." It fails soft, so nothing threw, nothing logged, and every flame in
the game has been STATIC since - measured in Chromium as one distinct key over a 300ms cycle.

⚠ AN ANIMATION MUST NOT MOVE THE SILHOUETTE (0906s). Only RGB inside the flame mask is touched;
ALPHA IS NEVER WRITTEN. A phase is byte-identical in size and offsets to its base frame, so it
drops into the same rect and the ship cannot jitter.

⚠ THE MODULATION IS WEIGHTED, NOT FLAT. 0906s's own lesson: modulating every changed pixel equally
made the whole airframe brighten and dim. The weight here is the pixel's own value within the mask,
so the white-hot core takes the full effect and the dim rim takes almost none.

⚠ AND THIS IS A LUMINANCE CHANGE, WHICH IS THE RULE RATHER THAN AN EXCEPTION TO IT. CLAUDE.md's
"palette/luminance swaps, not overlays" is exactly what a flame phase is: hue and saturation are
carried through untouched and only V moves.

⚠ 45 DISTINCT RECTS, NOT 72. The 0909 pack aliases `_pv2` onto the base and `_pv1`/`_pv3` onto
`_l`/`_r`, so eight phase-bearing keys per pilot resolve to five distinct frames. Baking per KEY
would write the same pixels four times and orphan half the strip. Baked per RECT, aliases follow.

⚠ APPEND, NEVER REPACK. One strip per sheet, rects repointed, pixels and manifest in ONE write -
the standing rule. 0906y records six appends orphaning 59% of a sheet, so this appends exactly once
and refuses to run twice (it checks for existing _g1 rows first).
"""
import os, sys, io, re, json, argparse
import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from flame_mask_0912n import flame_mask, ships_table, PILOTS, SHEETS, ROOT

MANIFEST = os.path.join(ROOT, 'assets', 'manifest.js')
PHASE_KEYS = ['', '_l', '_r', '_pv0', '_pv1', '_pv2', '_pv3', '_pv4']
AMP_UP = 0.30      # the flare, applied to the HEADROOM (see modulate)
AMP_DN = 0.30      # and drops on _g2
PAD = 2


def modulate(img, mask, amp, up=True):
    """Move V inside the mask. H, S and ALPHA are untouched; the silhouette cannot move.

    ⚠ THE FLARE AND THE SETTLE WEIGHT DIFFERENT PIXELS, AND THE FIRST CUT DID NOT.
    SHIP_GLOW_SEQ is ['', 'g1', '', 'g2'] - "0 -> flare -> 0 -> settle" - so g1 has to read BRIGHTER.
    Weighting the lift by the pixel's own value put the whole effect on the white-hot core, which is
    already at 1.0 and simply CLIPS: measured, g1 moved 7,282 against g2's 24,511 on Axel, a flare
    a third the size of the settle. The plate is authored at full brightness, so there is no headroom
    where it is brightest.

      flare   weight by HEADROOM (1-v): the saturated mid-tones brighten, the core stays put, and
              the plume reads hotter without a single clipped pixel.
      settle  weight by VALUE: the core dims most, which is what a flame losing energy does.

    Same total energy either way, and neither touches alpha.
    """
    a = np.asarray(img).astype(np.float64) / 255.0
    out = a.copy()
    if not mask.any():
        return Image.fromarray((np.clip(out, 0, 1) * 255).astype(np.uint8), 'RGBA')
    rgb = a[..., :3]
    v = rgb.max(axis=-1)
    mv = v[mask]
    lo, hi = float(mv.min()), float(mv.max())
    norm = np.zeros_like(v)
    norm[mask] = (mv - lo) / max(1e-6, hi - lo)   # 0 at the dim rim, 1 at the core
    if up:
        # ⚠ A HOTTER FLAME DOES NOT GET BRIGHTER, IT GOES WHITER - and that is not a stylistic
        # choice, it is the only axis with room left. Two attempts at a brightness lift measured
        # 7,282 and then 501 against the settle's 24,511, because the plume core is authored at
        # V=1.0 and every gain simply clips. SATURATION is where the headroom is: pulling the core
        # toward white is what a flame gaining energy actually does, and it costs no hue - the
        # gradient 0906t established as the thing that makes a plume read as fire is untouched.
        w = norm
        white = v[..., None]                       # pure-white at this pixel's own brightness
        t = (amp * 1.25 * w)[..., None]
        scaled = rgb * (1.0 - t) + white * t
    else:
        # ⚠ A COOLING FLAME DOES NOT GO GREY, IT GOES DEEPER IN ITS OWN COLOUR - and a flat value
        # scale gets that exactly wrong. Rendered at 7x, scaling RGB down turned Cole's white-green
        # core ASHEN and Yuri's white-red core to grey, because darkening a near-white pixel walks
        # it toward neutral. The settle is the true inverse of the flare: pull the core toward the
        # FULLY SATURATED version of its own hue, then dim slightly. Hue is untouched either way,
        # so the gradient that makes a plume read as fire (0906t) survives both phases.
        w = norm
        mn = rgb.min(axis=-1, keepdims=True)
        vv = v[..., None]
        span = np.maximum(vv - mn, 1e-6)
        sat_full = (rgb - mn) / span * vv          # same brightness, full saturation
        t = (amp * 1.15 * w)[..., None]
        scaled = (rgb * (1.0 - t) + sat_full * t) * (1.0 - 0.42 * amp * w)[..., None]
    out[..., :3] = np.where(mask[..., None], np.clip(scaled, 0, 1), rgb)
    # ⚠ alpha is copied through untouched - the silhouette must not move
    out[..., 3] = a[..., 3]
    return Image.fromarray((np.clip(out, 0, 1) * 255).astype(np.uint8), 'RGBA')


def distinct_rects(tab, pilot):
    """The 5 distinct frames behind the 8 phase-bearing keys, with every key that aliases each."""
    groups = {}
    for suf in PHASE_KEYS:
        k = 'ship_' + pilot + suf
        r = tab.get(k)
        if not r:
            continue
        groups.setdefault(tuple(r), []).append(k)
    return groups


def plan():
    tab = ships_table()
    out = []
    for p in PILOTS:
        for rect, keys in distinct_rects(tab, p).items():
            out.append({'pilot': p, 'rect': list(rect), 'keys': keys})
    return out, tab


def run(a):
    jobs, tab = plan()
    already = [k for k in tab if re.search(r'_g[12]$', k)]
    if already and not a.force:
        sys.exit('%d _g1/_g2 rows already exist - this appends and must not run twice. --force to override.'
                 % len(already))

    print('%d distinct frames -> %d phase cells' % (len(jobs), len(jobs) * 2))
    if a.dry:
        for j in jobs[:12]:
            print('  %-11s %-34s %s' % (j['pilot'], j['rect'], ','.join(j['keys'])))
        print('  ... (%d total)' % len(jobs))
        return 0

    tiles = []
    newrects = {}
    for p in PILOTS:
        sheet_path = os.path.join(SHEETS, 'ship_%s.png' % p)
        sh = Image.open(sheet_path).convert('RGBA')
        mine = [j for j in jobs if j['pilot'] == p]
        # lay the new cells in a strip UNDER the existing sheet
        cells = []
        for j in mine:
            x, y, w, h, ox, oy, cw, ch = j['rect']
            src = sh.crop((x, y, x + w, y + h))
            m, info = flame_mask(src)
            g1 = modulate(src, m, AMP_UP, up=True)
            g2 = modulate(src, m, AMP_DN, up=False)
            cells.append((j, src, g1, g2, m, info))
        stripH = max(c[1].height for c in cells) + PAD * 2
        stripW = sum(c[1].width * 2 + PAD * 2 for c in cells) + PAD
        big = Image.new('RGBA', (max(sh.width, stripW), sh.height + stripH), (0, 0, 0, 0))
        big.paste(sh, (0, 0))
        cx = PAD
        y0 = sh.height + PAD
        for j, src, g1, g2, m, info in cells:
            x, y, w, h, ox, oy, cw, ch = j['rect']
            big.paste(g1, (cx, y0)); r1 = [cx, y0, w, h, ox, oy, cw, ch]; cx += w + PAD
            big.paste(g2, (cx, y0)); r2 = [cx, y0, w, h, ox, oy, cw, ch]; cx += w + PAD
            for k in j['keys']:
                newrects[k + '_g1'] = r1
                newrects[k + '_g2'] = r2
            if j['rect'] == tab['ship_' + p]:
                tiles.append((p, src, g1, g2, m, info))
        if a.write:
            big.save(sheet_path)
            print('  %-11s sheet %dx%d -> %dx%d, +%d cells'
                  % (p, sh.width, sh.height, big.width, big.height, len(cells) * 2))

    if a.proof:
        proof(a.proof, tiles)

    if a.write:
        s = io.open(MANIFEST, encoding='utf-8', newline='').read()
        mm = re.search(r'window\.BOFX=(\{.*?\});', s, re.S)
        o = json.loads(mm.group(1))
        o['ships'].update(newrects)
        s2 = s[:mm.start(1)] + json.dumps(o, separators=(',', ':')) + s[mm.end(1):]
        io.open(MANIFEST, 'w', encoding='utf-8', newline='').write(s2)
        print('\nmanifest: +%d rows (BOFX.ships %d -> %d)'
              % (len(newrects), len(o['ships']) - len(newrects), len(o['ships'])))
    else:
        print('\n(no --write: nothing on disk changed; %d rows would be added)' % len(newrects))
    return 0


def proof(path, tiles):
    Z = 3
    rows = []
    for p, src, g1, g2, m, info in tiles:
        # crop to the tail so the flicker is actually visible at this scale
        h0 = int(src.height * 0.58)
        cuts = [src.crop((0, h0, src.width, src.height)),
                g1.crop((0, h0, src.width, src.height)),
                g2.crop((0, h0, src.width, src.height))]
        w = cuts[0].width; hh = cuts[0].height
        strip = Image.new('RGBA', (w * 3 + 12, hh), (10, 14, 20, 255))
        for i, c in enumerate(cuts):
            bg = Image.new('RGBA', c.size, (10, 14, 20, 255)); bg.paste(c, (0, 0), c)
            strip.paste(bg, (i * (w + 6), 0))
        strip = strip.resize((strip.width * Z, strip.height * Z), Image.NEAREST)
        d1 = int(np.abs(np.asarray(g1).astype(int) - np.asarray(src).astype(int))[..., :3].sum())
        d2 = int(np.abs(np.asarray(g2).astype(int) - np.asarray(src).astype(int))[..., :3].sum())
        da = int(np.abs(np.asarray(g1).astype(int) - np.asarray(src).astype(int))[..., 3].sum())
        rows.append((p, strip, info, d1, d2, da))
    W = max(r[1].width for r in rows); H = max(r[1].height for r in rows)
    sheet = Image.new('RGBA', (W * 3 + 40, (H + 30) * 3 + 30), (7, 12, 18, 255))
    d = ImageDraw.Draw(sheet)
    for i, (p, t, info, d1, d2, da) in enumerate(rows):
        cx = (i % 3) * (W + 14) + 8; cy = (i // 3) * (H + 30) + 22
        sheet.paste(t, (cx, cy))
        d.text((cx, cy - 18), '%s   base | g1 | g2    mask %d px   RGB moved %d / %d   ALPHA moved %d'
               % (p, info.get('px', 0), d1, d2, da), fill=(124, 245, 255, 255))
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    sheet.save(path)
    print('proof -> %s' % path)
    for p, _, info, d1, d2, da in rows:
        print('  %-11s mask %4d px   g1 %8d   g2 %8d   alpha %d %s'
              % (p, info.get('px', 0), d1, d2, da, '' if da == 0 else '  <-- ALPHA MOVED, silhouette at risk'))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry', action='store_true')
    ap.add_argument('--write', action='store_true')
    ap.add_argument('--force', action='store_true')
    ap.add_argument('--proof', default='')
    return run(ap.parse_args())


if __name__ == '__main__':
    sys.exit(main())
