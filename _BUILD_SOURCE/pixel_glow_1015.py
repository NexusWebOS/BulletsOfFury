"""PIXEL GLOW baker (1015, usage-driven since 1015b).

Mike: "pixel glow should occur instead of overlayed graphics like our stage 5 boss's middle core." Then:
"only do this for enemies and frames we're actually using please. Do a pass for levels 1-9."

A glow that is a second sprite pasted over the hull (a radial disc, an effect cell, a blurred halo) reads as a
sticker: it has its own silhouette, it does not follow the art's panels, and it sits on a different pixel grid.
Pixel glow lights the art's OWN emissive pixels - the core ring, the cockpit, the panel lights, the engine
cans - and lets that light spill past them in hard steps, the way a 16-bit palette cycle does.

WHAT IS BAKED: only what the stage-1..9 survey saw drawn. probe_glow_usage_1015.py plays each stage (waves,
miniboss, boss, Normal and Furious) and records every image drawn inside drawEnemy / drawSubBoss / drawBoss by
the XART key it came from and the key-space rectangle actually shown. Effects drawn in those windows (warning
cones, alerts, gauges, explosions, debris, dust, wakes, exhaust plumes, shields, muzzle flashes, fire) are left
out by name - they are already light. export_glow_sources_1015.py saves each key's exact pixels.

For each surviving key a GLOW companion the same size and layout as the source:
  * every emissive pixel at about half its own colour (it is ADDED light, drawn under 'lighter' - pushing it
    toward white floods the art into a flat disc, the very sticker look being removed);
  * three hard rings past the emissive pixels in the colour of the nearest one, each ring one screen pixel
    wide at the size the key is actually drawn (a 512 px plate drawn at 90 px gets 6-px source rings);
  * nothing outside the rectangles the survey saw drawn: a sheet's unused frames carry no light.
"Emissive" = opaque, bright, and brighter than its surroundings: saturated light (v>.70, s>.45) or a white-hot
core (v>.93, s<.30), at least .12 above the local mean brightness, in clusters small enough to be lights -
a large evenly bright area is paint (Yuri-red armour, orange furnace plating), not a lamp.
The Stage 5 Hammer's sheets also get a CORE companion: each pose's chest core (the lit cluster nearest a torso
guess), which his driver can push harder than the panel lights while he charges.
Nothing is read from pixels at runtime (file:// taints the canvas), and the source art is never modified.

Usage: python _BUILD_SOURCE/pixel_glow_1015.py --survey     aggregate the survey JSONs -> glow_usage_1015.json
       python _BUILD_SOURCE/export_glow_sources_1015.py      export the source pixels (real Chromium)
       python _BUILD_SOURCE/pixel_glow_1015.py [--check]     bake + registry (+ contact sheets)
"""
import glob, json, re, shutil, sys
from collections import Counter, defaultdict
from pathlib import Path
import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = Path(__file__).resolve().parents[1]
OUTD = ROOT / 'assets/game/shared/combat/pixel_glow_1015'
USAGE = ROOT / '_BUILD_SOURCE/glow_usage_1015.json'
SRCD = ROOT / '_shots/glow_usage_1015/src'

# Drawn inside an enemy/boss window but not a unit's body: effects, telegraphs and HUD are already light.
FX = re.compile(r'(^bmfx_|^bmbar_|fov|alert|_dust|debris|_wake|exhaust|wreck|sonic_|muzzle|^nxp_|explosion|shield|smoke|'
                r'damage_fire|^p2_fire|_charge(_\d+)?$|cannon_flash|fireball|impact|chain_|^eh7_|_shadow|^ovrotor|^rzb_rotor|'
                r'tread|^nsd_|^ntr_|^on5_fragments|^ap10_void|^ap10_ice_laser|^dr5_effects|^cwd_wall|laser_beams|laserbeam|'
                r'lightning_ball|chain_lightning|^nchg_orb|_beams?$|red_beams|_flash|^lz_bomb|^fzt_debris|^fzt_boss_expl|'
                r'^arch_leap_shock|^hm10_shield|^pl11_black_void|^nbret_|thermal_jet|heat_disc|^fb1002_firejet|_spark|_ring$|'
                r'^cfx_|^weapon_|^mwfx_|^fb2_stealth_.*_trail|^s6cargo13_front_lights|^d27_|^bof_player_|^nca_player_|_reticle|^nca_fx_|^nca_ui_|'
                r'^retm|^nbret|^arch_hammer_lightning|^arch_spiked_ball|^hm10_core_|^nca_misc$|^arch_storm_charge|_projectile|_bolt|_missile_?\d*$|^nca_)')
# Hammer sheets whose chest core gets its own companion (the convergence/charge driver pushes it harder).
CORE_KEYS = re.compile(r'^(arch_|pt11_hammer_core_)')
RING_A = (0.58, 0.34, 0.16)        # alpha of the 1st/2nd/3rd hard ring
CORE_RING_A = (0.70, 0.46, 0.26, 0.12)


def survey():
    agg = defaultdict(lambda: {'n': 0, 'st': set(), 'scope': set(), 'rects': Counter(), 'sc': 0.0, 'tints': Counter()})
    seen = []
    for f in sorted(glob.glob(str(ROOT / '_shots/glow_usage_1015/s*_*.json'))):
        d = json.load(open(f)); seen.append((d['stage'], d['diff'], d.get('boss_kind')))
        for v in d['phases'].values():
            for k, r in v['rec'].items():
                a = agg[k]; a['n'] += r['n']; a['st'].add(d['stage']); a['scope'] |= set(r['scope'])
                a['rects'].update(r['rects']); a['sc'] += r.get('sc', 0); a['tints'].update(r.get('tints', {}))
    keys, dropped = {}, {}
    for k, a in agg.items():
        if FX.search(k):
            dropped[k] = sorted(a['st']); continue
        rects = [[int(x) for x in rk.split(',')] for rk in a['rects']]
        rects = [r for r in rects if r[2] - r[0] >= 2 and r[3] - r[1] >= 2]
        if not rects:
            continue
        keys[k] = {'n': a['n'], 'st': sorted(a['st']), 'scope': sorted(a['scope']), 'rects': rects,
                   'scale': a['sc'] / max(1, a['n']), 'tints': dict(a['tints'])}
    USAGE.write_text(json.dumps({'runs': seen, 'keys': keys, 'dropped_fx': dropped}, indent=0))
    print('survey runs', len(seen), '| unit keys', len(keys), '| fx dropped', len(dropped))


def hsv(rgba):
    rgb = rgba[..., :3].astype(np.float32) / 255
    mx, mn = rgb.max(-1), rgb.min(-1)
    s = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0)
    return mx, s


def hue(rgba):
    rgb = rgba[..., :3].astype(np.float32) / 255
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    mx, mn = rgb.max(-1), rgb.min(-1); d = np.maximum(mx - mn, 1e-6)
    h = np.where(mx == r, ((g - b) / d) % 6, np.where(mx == g, (b - r) / d + 2, (r - g) / d + 4))
    return h / 6


def emissive(src, used, step):
    a = (src[..., 3] > 200) & used
    v, s = hsv(src); h = hue(src)
    # the unit's own paint: hue bins that hold a large share of its coloured pixels are armour, not lamps
    # (tan desert buggies, green camo tanks, Yuri-red hulls) - a lamp in that same hue must be far brighter
    col = a & (s > 0.28) & (v > 0.25)
    paint = np.zeros(24, bool)
    if col.sum() > 50:
        hist = np.bincount((h[col] * 24).astype(int) % 24, minlength=24) / col.sum()
        paint = hist > 0.12
        paint = paint | np.roll(paint, 1) | np.roll(paint, -1)
    in_paint = paint[(h * 24).astype(int) % 24]
    sat = (v > 0.72) & (s > 0.50) & (~in_paint | ((v > 0.92) & (s > 0.70)))
    # brighter than its surroundings: mean brightness of the opaque pixels in a window ~8 screen px wide
    r = max(4, int(round(4 * step)))
    k = 2 * r + 1
    vs = ndimage.uniform_filter(np.where(a, v, 0), k)
    cs = ndimage.uniform_filter(a.astype(np.float32), k)
    local = vs / np.maximum(cs, 1e-3)
    sat = a & sat & (v - local > 0.16)
    # a white-hot pixel is light only as the centre of a coloured light, never a specular glint on armour
    hot = a & (v > 0.95) & (s < 0.20) & ndimage.binary_dilation(sat, iterations=2 * step) & (v - local > 0.16)
    m = sat | hot
    lab, n = ndimage.label(m)
    if not n:
        return m
    sizes = ndimage.sum(m, lab, range(1, n + 1))
    # a light, not a painted panel: drop specks under one screen pixel and blobs larger than a lamp can be
    opaque_frame = np.median([((src[y0:y1, x0:x1, 3] > 200).sum()) for (x0, y0, x1, y1) in used.rects]) if hasattr(used, 'rects') else a.sum()
    cap = max(12, 0.025 * opaque_frame)
    keep = np.zeros(n + 1, bool)
    keep[1:] = (sizes >= max(3, step * step)) & (sizes <= cap)
    return keep[lab]


class Used(np.ndarray):
    pass


def used_mask(H, W, rects):
    u = np.zeros((H, W), bool)
    for x0, y0, x1, y1 in rects:
        u[max(0, y0):min(H, y1), max(0, x0):min(W, x1)] = True
    u = u.view(Used); u.rects = [[max(0, x0), max(0, y0), min(W, x1), min(H, y1)] for x0, y0, x1, y1 in rects]
    return u


def rings(mask, rgb, alphas, step, scale_col):
    dist, idx = ndimage.distance_transform_edt(~mask, return_indices=True)
    near = rgb[idx[0], idx[1]]
    out = np.zeros(mask.shape + (4,), np.float32)
    out[mask, :3] = rgb[mask] * scale_col; out[mask, 3] = 255
    for i, al in enumerate(alphas, start=1):
        ring = (dist > (i - 1) * step) & (dist <= i * step) & ~mask
        out[ring, :3] = near[ring]; out[ring, 3] = 255 * al
    return out


def chest_core(src, m, rects):
    """per drawn frame: the lit cluster nearest the torso (ink centre, 30% down) - not the hammer head"""
    core = np.zeros_like(m)
    for x0, y0, x1, y1 in rects:
        sub = m[y0:y1, x0:x1]; al = src[y0:y1, x0:x1, 3] > 200
        lab, n = ndimage.label(sub); ys, xs = np.nonzero(al)
        if not n or not len(ys):
            continue
        gx0, gy0 = (xs.min() + xs.max()) / 2, ys.min() + (ys.max() - ys.min()) * 0.30
        sizes = ndimage.sum(sub, lab, range(1, n + 1)); cents = ndimage.center_of_mass(sub, lab, range(1, n + 1))
        best, bd = None, 1e9
        for k, (sz, (cy, cx)) in enumerate(zip(sizes, cents), start=1):
            if sz < 12:
                continue
            d = ((cx - gx0) ** 2 + (cy - gy0) ** 2) ** 0.5 - sz ** 0.5 * 0.8
            if d < bd:
                best, bd = k, d
        if best is not None:
            core[y0:y1, x0:x1] |= lab == best
    return core


def bake(key, info):
    p = SRCD / (key + '.png')
    if not p.exists():
        return None, 'no source'
    src = np.array(Image.open(p).convert('RGBA'))
    H, W = src.shape[:2]
    scale = max(1e-3, info['scale'])
    step = int(np.clip(round(2.0 / scale), 1, 8))          # source px per ring (1 game pixel = 2 canvas px)
    used = used_mask(H, W, info['rects'])
    m = emissive(src, used, step)
    if m.sum() < max(6, 2 * step * step):
        return None, 'no lights'
    rgb = src[..., :3].astype(np.float32)
    opaque = int(sum((src[y0:y1, x0:x1, 3] > 200).sum() for x0, y0, x1, y1 in used.rects))
    # a unit that is mostly light already (ice crystal jets, water swirls) gets nothing more - an extra wash
    # over its whole body would read as a halo sticker, the thing this pass removes
    if m.sum() > 0.14 * opaque:
        return None, 'self-lit'
    glow = rings(m, rgb, RING_A, step, 0.48)
    # many small lamps on one hull: keep the spill to a single ring so it never merges into one halo
    if (glow[..., 3] > 0).sum() > 0.30 * opaque:
        glow = rings(m, rgb, RING_A[:1], step, 0.48)
    glow[~ndimage.binary_dilation(used, iterations=3 * step + 1)] = 0     # light never reaches an unused frame
    OUTD.mkdir(parents=True, exist_ok=True)
    # stored pre-reduced to the size it is drawn at (n source px per stored px), so the runtime blit is close
    # to 1:1 - a full-size companion smooth-downscaled every frame cost several ms on the big boss sheets
    n = max(1, int(1.0 / (scale * 1.25)))
    gp = OUTD / (key + '_glow.png')
    save_reduced(glow, n, gp)
    rec = {'glow': str(gp.relative_to(ROOT)), 'size': [W, H], 'n': n, 'st': info['st'], 'step': step, 'emissive_px': int(m.sum())}
    if CORE_KEYS.search(key):
        cm = chest_core(src, m, used.rects)
        if cm.sum() >= 12:
            core = rings(cm, rgb, CORE_RING_A, step, 0.42)
            cp = OUTD / (key + '_core.png')
            save_reduced(core, n, cp)
            rec['core'] = str(cp.relative_to(ROOT))
    return rec, 'ok'


def save_reduced(rgba, n, path):
    """box-reduce by n with premultiplied alpha (so a light's colour does not darken toward its transparent edge)"""
    a = rgba.clip(0, 255)
    if n > 1:
        H, W = a.shape[:2]; H2, W2 = -(-H // n) * n, -(-W // n) * n
        pad = np.zeros((H2, W2, 4), np.float32); pad[:H, :W] = a
        al = pad[..., 3:4] / 255; pm = pad[..., :3] * al
        pm = pm.reshape(H2 // n, n, W2 // n, n, 3).mean((1, 3)); al = al.reshape(H2 // n, n, W2 // n, n, 1).mean((1, 3))
        a = np.concatenate([pm / np.maximum(al, 1e-6), al * 255], -1)
    Image.fromarray(a.clip(0, 255).astype(np.uint8), 'RGBA').save(path, optimize=True)


def check(res):
    """per stage contact sheet: source | source + glow, one cell per drawn frame (first frame of each key)"""
    by_st = defaultdict(list)
    for k, r in res.items():
        by_st[r['st'][0]].append(k)
    usage = json.loads(USAGE.read_text())['keys']
    for st, ks in sorted(by_st.items()):
        tiles = []
        for k in sorted(ks):
            src = Image.open(SRCD / (k + '.png')).convert('RGBA'); g = Image.open(ROOT / res[k]['glow']).convert('RGBA').resize(src.size, Image.BILINEAR)
            x0, y0, x1, y1 = usage[k]['rects'][0]
            pad = 3 * res[k]['step']
            box = (max(0, x0 - pad), max(0, y0 - pad), min(src.width, x1 + pad), min(src.height, y1 + pad))
            s, gg = src.crop(box), g.crop(box)
            t = 120 / max(s.width, s.height)
            sz = (max(1, int(s.width * t)), max(1, int(s.height * t)))
            bg = Image.new('RGBA', s.size, (22, 24, 32, 255)); bg.alpha_composite(s)
            a = np.array(bg).astype(np.float32); l = np.array(gg).astype(np.float32)
            lit = a.copy(); lit[..., :3] = np.minimum(255, a[..., :3] + l[..., :3] * (l[..., 3:4] / 255) * 0.95)
            pair = Image.new('RGBA', (sz[0] * 2 + 4, sz[1]), (10, 10, 14, 255))
            pair.paste(bg.resize(sz, Image.LANCZOS), (0, 0)); pair.paste(Image.fromarray(lit.astype(np.uint8)).resize(sz, Image.LANCZOS), (sz[0] + 4, 0))
            tiles.append(pair)
        cols = 6; cw = max(t.width for t in tiles) + 6; ch = max(t.height for t in tiles) + 6
        rows = (len(tiles) + cols - 1) // cols
        out = Image.new('RGBA', (cols * cw, rows * ch), (10, 10, 14, 255))
        for i, t in enumerate(tiles):
            out.paste(t, ((i % cols) * cw, (i // cols) * ch))
        p = ROOT / f'_shots/glow_usage_1015/check_stage{st}.png'; out.save(p)
        print('check ->', p, len(tiles))


if __name__ == '__main__':
    if '--survey' in sys.argv:
        survey(); sys.exit(0)
    keys = json.loads(USAGE.read_text())['keys']
    if OUTD.exists():
        shutil.rmtree(OUTD)
    res, skipped = {}, Counter()
    for k, info in sorted(keys.items()):
        r, why = bake(k, info)
        if r:
            res[k] = r
        else:
            skipped[why] += 1
    (OUTD / 'pixel_glow_1015.json').write_text(json.dumps(res, indent=1))
    js = 'const PXG_SHEETS=' + json.dumps({k: {kk: r[kk] for kk in ('glow', 'core', 'size', 'n', 'st') if kk in r} for k, r in res.items()}, separators=(',', ':')) + ';\n'
    (ROOT / 'assets/pixel_glow_art_1015.js').write_text('"use strict";\n/* generated by _BUILD_SOURCE/pixel_glow_1015.py from the stage 1-9 usage survey - do not hand-edit */\n' + js)
    tot = sum((OUTD / Path(r['glow']).name).stat().st_size + ((OUTD / Path(r['core']).name).stat().st_size if 'core' in r else 0) for r in res.values())
    print('baked', len(res), 'keys,', sum('core' in r for r in res.values()), 'with core;', dict(skipped), f'{tot / 1e6:.1f} MB')
    if '--check' in sys.argv:
        check(res)
