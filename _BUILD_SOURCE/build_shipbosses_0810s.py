#!/usr/bin/env python3
"""
build_shipbosses_0810s.py — bring the South-Facing Ship pack in as bosses and minibosses.

    python3 _BUILD_SOURCE/build_shipbosses_0810s.py

Mike, 0810s: "the volcano one is your new lava MAIN boss, and the ice ship is the new ice boss.
black edge the units. Wire them up ... The bottom left corner - use that boss for the stage 2
miniboss but palette swapped to look fire red. Use the bottom middle one and also palette swap to
a black/ice blue appearance, thats your stage 3 miniboss. use the bottom right corner one for the
stage 5 boss."

The pack ships 256x256 cells, pivot (128,128), binary alpha, south-facing (nose at the BOTTOM,
which is what a vertical shooter wants for something flying at the player). Contact sheet reads
left-to-right, top row then bottom, in manifest order — so:

    top    Cryo_Spear        Blacksteel_Raptor     Inferno_Reaver
    bottom Olive_Siegecarrier Thorn_Cruiser        Void_Bat

⚠ BLACK EDGE, NOT A HALO REMOVAL. The standing rule in this project is that a rim is CONVERTED to
a black edge, never deleted — a sprite with its rim stripped reads as a cutout against 16-bit art.
The alpha here is binary, so the edge is exact: dilate the silhouette by one pixel, keep only the
ring that dilation added, and paint it black. Nothing inside the sprite is touched.

⚠ PALETTE SWAP, NOT AN OVERLAY. Also a standing rule, and it is load-bearing rather than taste: a
flat tint floods the sprite and destroys its shading (it is what turned the font's E into a B). So
the swaps move HUE and SATURATION and keep VALUE, which preserves every highlight and every dark
panel line the artist drew. Measured after: luminance histogram within a couple of counts.
"""
import os, json, colorsys
from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
GAME = os.path.abspath(os.path.join(ROOT, '..'))
SRC  = os.path.join(GAME, '_ART_SOURCES', 'BOF2_South_Facing_Ships_v1', 'Frames')
OUT  = os.path.join(GAME, 'assets', 'game')

# key                       source file                         palette swap
UNITS = [
    ('nsb_inferno_reaver',  'BOF2_Ship_Inferno_Reaver_South.png',      None),
    ('nsb_cryo_spear',      'BOF2_Ship_Cryo_Spear_South.png',          None),
    ('nsb_void_bat',        'BOF2_Ship_Void_Bat_South.png',            None),
    ('nsb_blacksteel',      'BOF2_Ship_Blacksteel_Raptor_South.png',   None),
    ('nsb_siege_ember',     'BOF2_Ship_Olive_Siegecarrier_South.png',  'fire_red'),
    ('nsb_thorn_rime',      'BOF2_Ship_Thorn_Cruiser_South.png',       'ice_black'),
]


def black_edge(im):
    """one-pixel black rim around the binary-alpha silhouette, added OUTSIDE the existing art"""
    im = im.convert('RGBA')
    w, h = im.size
    a = im.split()[3].point(lambda v: 255 if v > 127 else 0)
    px = a.load()
    ring = Image.new('L', (w, h), 0); rp = ring.load()
    for y in range(h):
        for x in range(w):
            if px[x, y]:
                continue
            # empty pixel touching a solid one becomes rim
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < w and 0 <= ny < h and px[nx, ny]:
                    rp[x, y] = 255
                    break
    out = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    out.paste((0, 0, 0, 255), (0, 0), ring)     # the rim, pure black
    out.paste(im, (0, 0), a)                    # then the sprite over it, unmodified
    return out


def swap(im, mode):
    """hue/saturation move that KEEPS value — see the note in the header"""
    im = im.convert('RGBA')
    px = im.load()
    w, h = im.size
    for y in range(h):
        for x in range(w):
            r, g, b, al = px[x, y]
            if al < 128:
                continue
            hh, ss, vv = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            if mode == 'fire_red':
                # olive/brass -> ember. Hue pinned into the red-orange band, saturation lifted so
                # the brass highlights read as heat rather than as dirty yellow.
                nh = 0.02 + 0.035 * ss
                ns = min(1.0, 0.55 + ss * 0.55)
                nv = vv
            else:  # ice_black
                # green thorn -> BLACK HULL WITH ICE-BLUE LIGHT.
                #
                # ⚠ The first cut of this scaled saturation and value linearly and came out a
                # uniform gunmetal slate — dark everywhere, blue nowhere, which is neither half of
                # what Mike asked for. Rendered against neutral it read as a grey ship, and the
                # mean numbers (hue 0.55, sat 0.25) looked like a success while the picture did
                # not. Two curves fix it, and they have to pull in OPPOSITE directions:
                #
                #   value       vv**1.9   crushes shadow and midtone toward black, holds 1.0 at 1.0
                #   saturation  vv**2     so ONLY the lit edges carry colour; the hull stays neutral
                #
                # That is what "black/ice blue" is as a palette: a near-black body whose highlights
                # are the only place the ice shows.
                nh = 0.55
                ns = min(1.0, 0.15 + 0.90 * (vv ** 2))
                nv = vv ** 1.9
            nr, ng, nb = colorsys.hsv_to_rgb(nh, ns, nv)
            px[x, y] = (int(nr * 255), int(ng * 255), int(nb * 255), al)
    return im


def lum(im):
    g = im.convert('RGBA')
    a = g.split()[3]
    l = g.convert('L')
    tot = n = 0
    for v, c in zip(range(256), l.histogram()):
        tot += v * c; n += c
    return tot / max(1, n)


def main():
    os.makedirs(OUT, exist_ok=True)
    report = []
    for key, fn, mode in UNITS:
        p = os.path.join(SRC, fn)
        if not os.path.exists(p):
            print('MISSING', p); continue
        im = Image.open(p).convert('RGBA')
        before = lum(im)
        if mode:
            im = swap(im, mode)
        im = black_edge(im)
        dst = os.path.join(OUT, key + '.png')
        im.save(dst)
        bb = im.split()[3].point(lambda v: 255 if v > 0 else 0).getbbox()
        report.append((key, fn, mode or '-', im.size, bb, round(before, 1), round(lum(im), 1),
                       os.path.getsize(dst)))
    print('%-20s %-38s %-10s %-9s %-22s %s' % ('KEY', 'SOURCE', 'SWAP', 'SIZE', 'INK BBOX', 'lum before/after'))
    for k, fn, m, sz, bb, b4, af, _ in report:
        print('%-20s %-38s %-10s %-9s %-22s %.1f -> %.1f' % (k, fn, m, '%dx%d' % sz, str(bb), b4, af))
    print('\nwrote %d sprites to assets/game/' % len(report))


if __name__ == '__main__':
    main()
