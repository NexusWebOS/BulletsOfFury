"""campaign_map_v2_0912v.py - bake the SpriteCook campaign-map pieces into game-ready sprites.

    python _BUILD_SOURCE/campaign_map_v2_0912v.py <src_dir>          # bake into assets/game/campaign_map_v2/
    python _BUILD_SOURCE/campaign_map_v2_0912v.py <src_dir> --check  # report only, write nothing

Mike (0912v): "Use spritecook, regenerate the entire map but this time as seperate pieces, a parallax
background you can amke scrolll and animate, a better UI, instead of the pause menu you can put the
buttons up top like a menu..."

SOURCES are SpriteCook `pixel_url` downloads (CLAUDE.md SpriteCook section: cut from pixel_url, never
raw_url - raw comes back opaque / checkerboarded). Asset ids are recorded in spritecook-assets.json.

EVERY SIZE HERE IS A BACKING-STORE SIZE. The map draws these at SS=2 one backing pixel per sprite
pixel, so a 380px island is 190 logical px on the 480x512 screen. Baking to the exact drawn size keeps
the resample offline and one-time (CLAUDE.md 1903-1914: a 4.5x downscale at draw time dissolved the
black edges).

Per island:
  1. resize the 512px plate to its backing size (LANCZOS) and re-threshold alpha at 50% -> hard alpha
  2. palette lock to <=128 colours taken from the island's own opaque pixels, NO dither
     (CLAUDE.md 1087-1091: pixel:true is not pixel art - 91,175 colours came back on the test plate)
  3. a 1px black edge on the OUTER boundary (CLAUDE.md 195: black edges, never halos)
  4. _lock  - a luminance swap of the same pixels to cold slate for locked stages
              (CLAUDE.md 196: palette/luminance swaps, not overlays)
  5. _glow  - an amber ring just outside the silhouette, graded alpha, drawn pulsing under the
              selected island
  6. _shadow - the silhouette in black, softened, drawn offset to seat the island in the sea
Ocean:   the texture tile at 512 backing, wrap-offset seam fix, palette lock.
Clouds:  clouds2_pixel.png (four large clouds) sliced by its empty gutters, x2 nearest, palette-locked,
         three mirrored for seven shapes, plus flat black silhouettes. The first sheet
         (clouds_pixel.png, seven small clouds at x3) is the fallback; rendered beside the islands its
         3px grain read chunky against their 1px detail, which is why the second plate exists.
Buttons: the AUTHORED btn_save / btn_load / btn_exit plates, shrunk once offline to 52px tall.
Bar:     the generated top-bar plate, trimmed and doubled with NEAREST.
"""
import os, sys, json
import numpy as np
from PIL import Image, ImageFilter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'assets', 'game', 'campaign_map_v2')

ISLANDS = {                      # out name: (source file, backing size)
    'isl_1': ('s1_jungle.png', 380), 'isl_2': ('s2_volcano.png', 380), 'isl_3': ('s3_ice.png', 380),
    'isl_4': ('s4_airbase.png', 380), 'isl_5': ('s5_launch.png', 380), 'isl_6': ('s6_storm.png', 380),
    'isl_7': ('s7_sewer.png', 380), 'isl_8': ('s8_crimson.png', 380), 'isl_9': ('s9_portal.png', 260),
    'isl_hub': ('hub_citadel.png', 480),
}
BUTTONS = {'btn_save': 'ui_menu_1', 'btn_load': 'ui_menu_1', 'btn_exit': 'ui_menu_1'}
BTN_H = 52                       # 26 logical: the three plates side by side fit the bar's 345px channel
EDGE = (9, 9, 13)                # the project's black edge colour (halo_to_black_0906t)
GLOW = (255, 210, 74)            # the menus' selection amber (#ffd24a, drawMenuButtons)
CLOUD_SHAPES = 7                 # the map draws cloud_0..6


def hard_alpha(im):
    a = np.array(im)
    a[..., 3] = np.where(a[..., 3] >= 128, 255, 0)
    a[a[..., 3] == 0, :3] = 0
    return a


def palette_lock(a, colours):
    """quantise the opaque pixels to `colours` entries chosen from those pixels alone, no dither"""
    op = a[..., 3] > 0
    if not op.any():
        return a
    rgb = a[..., :3].copy()
    mean = rgb[op].mean(axis=0).astype(np.uint8)
    rgb[~op] = mean                                   # transparent pixels must not claim palette slots
    q = Image.fromarray(rgb).quantize(colors=colours, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    out = a.copy()
    out[..., :3] = np.array(q.convert('RGB'))
    out[~op, :3] = 0
    return out


def dilate(mask, r):
    m = Image.fromarray((mask * 255).astype(np.uint8))
    for _ in range(r):
        m = m.filter(ImageFilter.MaxFilter(3))
    return np.array(m) > 0


def black_edge(a):
    op = a[..., 3] > 0
    ring = dilate(op, 1) & ~op
    out = a.copy()
    out[ring] = EDGE + (255,)
    return out


def lock_variant(a):
    """cold slate: each pixel's own luminance mapped into a dark blue-grey ramp"""
    out = a.copy()
    rgb = a[..., :3].astype(np.float32)
    lum = rgb[..., 0] * 0.299 + rgb[..., 1] * 0.587 + rgb[..., 2] * 0.114
    lum = 18 + lum * 0.52
    ramp = np.stack([lum * 0.78, lum * 0.86, lum * 1.02], axis=-1)
    out[..., :3] = np.clip(ramp, 0, 255).astype(np.uint8)
    out[a[..., 3] == 0, :3] = 0
    return out


def glow_variant(a, width=5):
    op = a[..., 3] > 0
    out = np.zeros_like(a)
    prev = op
    for k in range(1, width + 1):
        grown = dilate(prev, 1)
        ring = grown & ~prev
        alpha = int(255 * (1.0 - (k - 1) / float(width)) ** 1.4)
        out[ring] = GLOW + (alpha,)
        prev = grown
    return out


def shadow_variant(a):
    op = (a[..., 3] > 0).astype(np.uint8) * 255
    m = Image.fromarray(op).filter(ImageFilter.GaussianBlur(6))
    out = np.zeros_like(a)
    out[..., 3] = (np.array(m).astype(np.float32) * 0.62).astype(np.uint8)
    return out


def colours(a):
    op = a[a[..., 3] > 0][:, :3]
    return len(np.unique(op.view([('', op.dtype)] * 3))) if len(op) else 0


def bake_island(src, size):
    im = Image.open(src).convert('RGBA').resize((size, size), Image.LANCZOS)
    a = hard_alpha(im)
    a = palette_lock(a, 128)
    a = black_edge(a)
    return {'': a, '_lock': lock_variant(a), '_glow': glow_variant(a), '_shadow': shadow_variant(a)}


def bake_ocean(src, size=512):
    im = Image.open(src).convert('RGB').resize((size, size), Image.LANCZOS)
    t1 = np.array(im).astype(np.float32)
    t2 = np.roll(t1, (size // 2, size // 2), axis=(0, 1))
    ramp = np.clip(np.minimum(np.arange(size), size - 1 - np.arange(size)) / 96.0, 0, 1)
    mask = np.minimum(ramp[None, :], ramp[:, None])[..., None]
    t = t1 * mask + t2 * (1 - mask)
    a = np.dstack([np.clip(t, 0, 255).astype(np.uint8), np.full((size, size), 255, np.uint8)])
    return palette_lock(a, 56)


def slice_islands(a, min_px=40):
    """connected alpha islands (8-neighbour), returned as (x0, y0, x1, y1) boxes"""
    op = a[..., 3] > 0
    seen = np.zeros_like(op)
    h, w = op.shape
    boxes = []
    for y in range(h):
        for x in range(w):
            if op[y, x] and not seen[y, x]:
                stack, px = [(y, x)], []
                seen[y, x] = True
                while stack:
                    cy, cx = stack.pop()
                    px.append((cy, cx))
                    for dy in (-1, 0, 1):
                        for dx in (-1, 0, 1):
                            ny, nx = cy + dy, cx + dx
                            if 0 <= ny < h and 0 <= nx < w and op[ny, nx] and not seen[ny, nx]:
                                seen[ny, nx] = True
                                stack.append((ny, nx))
                if len(px) >= min_px:
                    ys, xs = zip(*px)
                    boxes.append((min(xs), min(ys), max(xs) + 1, max(ys) + 1))
    return sorted(boxes, key=lambda b: (b[1] // 40, b[0]))


def cloud_shadow(big):
    sh = np.zeros_like(big)
    sh[..., 3] = np.where(big[..., 3] > 0, 255, 0)
    return sh


def bake_clouds(src, scale=3):
    """the first sheet: seven small clouds, x3 nearest (kept as the fallback)"""
    a = np.array(Image.open(src).convert('RGBA'))
    a[..., 3] = np.where(a[..., 3] >= 128, 255, 0)
    out = []
    for (x0, y0, x1, y1) in slice_islands(a):
        c = a[y0:y1, x0:x1]
        big = np.array(Image.fromarray(c).resize(((x1 - x0) * scale, (y1 - y0) * scale), Image.NEAREST))
        out.append((big, cloud_shadow(big)))
    return out


def widest_gap(profile, lo, hi):
    """the centre of the widest run of empty rows/columns inside [lo, hi)"""
    best, run0, best_c = 0, None, None
    for i in range(lo, hi + 1):
        empty = i < hi and profile[i] == 0
        if empty and run0 is None:
            run0 = i
        if not empty and run0 is not None:
            if i - run0 > best:
                best, best_c = i - run0, (run0 + i) // 2
            run0 = None
    return best_c


def bake_clouds_v2(src, scale=2):
    """four large clouds laid out two by two. Sliced by the EMPTY GUTTERS between them, not by
    connected alpha: a cloud's loose puffs are separate alpha islands and a component slice would
    either drop them or hand each one its own sprite. Doubled with NEAREST - 2 backing px per art px
    where the first sheet needed 3 - then palette-locked (it returns ~7,300 opaque colours)."""
    a = np.array(Image.open(src).convert('RGBA'))
    a[..., 3] = np.where(a[..., 3] >= 128, 255, 0)
    a[a[..., 3] == 0, :3] = 0
    op = a[..., 3] > 0
    h, w = op.shape
    gx = widest_gap(op.sum(axis=0), w // 3, 2 * w // 3)
    gy = widest_gap(op.sum(axis=1), h // 3, 2 * h // 3)
    if gx is None or gy is None:
        raise SystemExit('clouds2: no empty gutter between the four clouds (gx=%s gy=%s)' % (gx, gy))
    base = []
    for (qx0, qy0, qx1, qy1) in [(0, 0, gx, gy), (gx, 0, w, gy), (0, gy, gx, h), (gx, gy, w, h)]:
        q = a[qy0:qy1, qx0:qx1]
        ys, xs = np.where(q[..., 3] > 0)
        if not len(xs):
            continue
        c = q[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
        big = np.array(Image.fromarray(c).resize((c.shape[1] * scale, c.shape[0] * scale), Image.NEAREST))
        base.append(palette_lock(big, 96))
    if len(base) != 4:
        raise SystemExit('clouds2: expected four clouds, sliced %d' % len(base))
    shapes = base + [np.ascontiguousarray(b[:, ::-1]) for b in base[:CLOUD_SHAPES - len(base)]]
    return [(big, cloud_shadow(big)) for big in shapes]


def cell_image(key):
    src = open(os.path.join(ROOT, 'assets', 'manifest.js'), encoding='utf-8').read()
    import re
    m = re.search(r'"%s"\s*:\s*\[\s*"([A-Za-z0-9_]+)"\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)' % re.escape(key), src)
    if not m:
        raise SystemExit('no cell for %s' % key)
    sheet, x, y, w, h = m.group(1), int(m.group(2)), int(m.group(3)), int(m.group(4)), int(m.group(5))
    atlas = Image.open(os.path.join(ROOT, 'assets', 'game', 'atlas', sheet + '.png')).convert('RGBA')
    return atlas.crop((x, y, x + w, y + h))


def bake_button(key):
    im = cell_image(key)
    w = int(round(im.width * BTN_H / float(im.height)))
    return np.array(im.resize((w, BTN_H), Image.LANCZOS))


def bake_bar(src):
    """the strip comes back as a 430x43 ink band inside a square canvas: crop it and double it with
    NEAREST, which is exactly 2 backing px per art px at SS=2 - a fractional fit to 960 wide would
    resample pixel art the generator already quantised"""
    im = Image.open(src).convert('RGBA')
    bb = im.getbbox()
    if bb:
        im = im.crop(bb)
    im = im.resize((im.width * 2, im.height * 2), Image.NEAREST)
    a = hard_alpha(im)
    return black_edge(palette_lock(a, 96))


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    src_dir, check = sys.argv[1], '--check' in sys.argv
    results = {}
    for name, (f, size) in ISLANDS.items():
        p = os.path.join(src_dir, f)
        if not os.path.exists(p):
            print('MISSING source %s' % p)
            continue
        for suffix, arr in bake_island(p, size).items():
            results[name + suffix + '.png'] = arr
    if os.path.exists(os.path.join(src_dir, 'ocean_raw.png')):
        results['ocean.png'] = bake_ocean(os.path.join(src_dir, 'ocean_raw.png'))
    clouds = None
    if os.path.exists(os.path.join(src_dir, 'clouds2_pixel.png')):
        clouds = bake_clouds_v2(os.path.join(src_dir, 'clouds2_pixel.png'))
    elif os.path.exists(os.path.join(src_dir, 'clouds_pixel.png')):
        clouds = bake_clouds(os.path.join(src_dir, 'clouds_pixel.png'))
    for i, (c, sh) in enumerate(clouds or []):
        results['cloud_%d.png' % i] = c
        results['cloud_%d_shadow.png' % i] = sh
    for key in BUTTONS:
        results[key + '.png'] = bake_button(key)
    if os.path.exists(os.path.join(src_dir, 'bar_pixel.png')):
        results['bar.png'] = bake_bar(os.path.join(src_dir, 'bar_pixel.png'))

    report = {}
    for name, arr in sorted(results.items()):
        report[name] = {'w': int(arr.shape[1]), 'h': int(arr.shape[0]), 'colours': colours(arr),
                        'opaque': round(float((arr[..., 3] > 0).mean()), 3)}
        print('%-24s %4dx%-4d colours %5d  opaque %.2f' % (name, arr.shape[1], arr.shape[0], report[name]['colours'],
                                                          report[name]['opaque']))
    if check:
        print('--check: nothing written')
        return
    os.makedirs(OUT, exist_ok=True)
    for name, arr in results.items():
        Image.fromarray(arr, 'RGBA').save(os.path.join(OUT, name), optimize=True)
    json.dump(report, open(os.path.join(OUT, 'bake_report.json'), 'w'), indent=1)
    print('wrote %d files to %s' % (len(results), OUT))


if __name__ == '__main__':
    main()
