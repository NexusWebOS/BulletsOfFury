#!/usr/bin/env python3
"""
chaingun_barrel_0916.py - THE CHAINGUN'S EMBLEM IS A CHAIN BARREL, IN FIVE TIER COLOURS.

    python3 _BUILD_SOURCE/chaingun_barrel_0916.py <generated_barrel.png> [--check]

Mike, 0916, with a reference photo of a six-barrel minigun: "chaingun icon should be a chain barrel
icon with lvl1-5 upgrade color variants like our current scheme" / "something ike, generate it
please."

The barrel is GENERATED (SpriteCook, gemini-3.1-flash-image, three variations; the one with the
muzzle face square to the viewer reads best at icon size, the same way the MG badge's own emblem
does). Everything after that is this file:

⚠ PALETTE-LOCKED FIRST, BECAUSE `pixel:true` DOES NOT GIVE PIXEL ART. Measured on OPAQUE PIXELS
ONLY - counting the RGB under transparent pixels is how this gets waved through - the generated
barrel is **656 colours** against an authored badge's few dozen. Dropped in as-is it is a
continuous-tone render sitting inside hand-authored pixel art. It is snapped to the palette of
`micon_mg_4`, the SILVER tier, which is the family's own neutral metal and carries no hue of its
own to inject.

⚠ THEN THE TIER COLOUR IS A HUE ROTATION, NOT A PAINT. Each tier's hue is measured off THAT
BADGE'S OWN RING (the family is colour-coded per tier: orange, blue, green, silver, red) and the
barrel is rotated onto it with its value untouched, so every bevel, muzzle shadow and rim light
survives. 0906t: rotate the hue, never set it - setting one hue flattens the gradient that makes
metal read as metal. Tier 4 is SILVER: its ring has no hue to measure, so the barrel is left
neutral there rather than being rotated onto noise.
"""
import os, sys, argparse, colorsys, collections
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
ATLAS = os.path.join(ROOT, 'assets', 'game', 'atlas', 'bof_player_weapon_special_icons.png')
OUT = os.path.join(ROOT, 'docs', 'proofs', 'chaingun_icons_0916')
DST = os.path.join(ROOT, 'assets', 'game', 'stage5_archmage_0916')

# the SPECIAL family's badges (micon_icebreath_1..5) - the frame donor
BADGE = {1: (144, 520, 96, 112), 2: (271, 520, 97, 112), 3: (399, 520, 98, 112),
         4: (527, 520, 97, 112), 5: (654, 520, 99, 112)}
# the gun family's own badges (micon_mg_1..5) - where each tier's colour is measured
MGB = {1: (35, 31, 58, 66), 2: (162, 31, 60, 66), 3: (280, 16, 79, 96), 4: (408, 16, 79, 96), 5: (536, 16, 80, 96)}


def opaque_colours(im):
    px = im.convert('RGBA').load()
    return len({px[x, y][:3] for y in range(im.height) for x in range(im.width) if px[x, y][3] > 8})


def palette_of(im):
    px = im.convert('RGBA').load()
    c = collections.Counter()
    for y in range(im.height):
        for x in range(im.width):
            p = px[x, y]
            if p[3] > 8:
                c[p[:3]] += 1
    return [k for k, _ in c.most_common()]


def snap(im, pal):
    """nearest-neighbour palette lock, DITHER OFF (dithering a small target sprays checkerboard
       noise through flat metal and reads as JPEG rot at 2x)"""
    out = im.copy().convert('RGBA')
    px = out.load()
    cache = {}
    for y in range(out.height):
        for x in range(out.width):
            r, g, b, a = px[x, y]
            if a <= 8:
                px[x, y] = (0, 0, 0, 0)
                continue
            k = (r, g, b)
            if k not in cache:
                cache[k] = min(pal, key=lambda c: (c[0] - r) ** 2 + (c[1] - g) ** 2 + (c[2] - b) ** 2)
            c = cache[k]
            px[x, y] = (c[0], c[1], c[2], 255 if a > 128 else 0)
    return out


def ring_hue(badge):
    """the tier's own colour, measured off its ring: the median hue of its saturated pixels, and
       the saturation that goes with it. A tier whose ring is metal (silver) reports None."""
    px = badge.convert('RGBA').load()
    hs, ss = [], []
    for y in range(badge.height):
        for x in range(badge.width):
            p = px[x, y]
            if p[3] < 8:
                continue
            h, s, v = colorsys.rgb_to_hsv(p[0] / 255.0, p[1] / 255.0, p[2] / 255.0)
            if s > 0.45 and v > 0.25:
                hs.append(h); ss.append(s)
    if len(hs) < 40:
        return None
    hs.sort(); ss.sort()
    return (hs[len(hs) // 2], ss[len(ss) // 2])


def tint_to(im, hue, sat):
    """rotate the barrel's hue onto the tier's, keeping VALUE - the bevels and muzzle shadows are
       what make it read as a barrel and they live in value"""
    out = im.copy().convert('RGBA')
    px = out.load()
    for y in range(out.height):
        for x in range(out.width):
            r, g, b, a = px[x, y]
            if a <= 8:
                continue
            h, s, v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
            # the metal is nearly neutral, so its own hue carries no information: the tier's hue is
            # applied and the saturation is raised toward the ring's, scaled by how lit the pixel is
            ns = min(1.0, max(s, sat * (0.35 + 0.45 * v)))
            r2, g2, b2 = colorsys.hsv_to_rgb(hue, ns, v)
            px[x, y] = (int(r2 * 255 + .5), int(g2 * 255 + .5), int(b2 * 255 + .5), a)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('src')
    ap.add_argument('--check', action='store_true')
    a = ap.parse_args()
    atlas = Image.open(ATLAS).convert('RGBA')
    gen = Image.open(a.src).convert('RGBA')

    mg4 = atlas.crop((MGB[4][0], MGB[4][1], MGB[4][0] + MGB[4][2], MGB[4][1] + MGB[4][3]))
    pal = palette_of(mg4)
    base = snap(gen, pal)
    print('barrel %dx%d  colours %d -> %d  (locked to micon_mg_4, %d colours)'
          % (gen.width, gen.height, opaque_colours(gen), opaque_colours(base), len(pal)))

    made = []
    for t in (1, 2, 3, 4, 5):
        r = MGB[t]
        hs = ring_hue(atlas.crop((r[0], r[1], r[0] + r[2], r[1] + r[3])))
        if hs is None:
            made.append((t, base.copy(), None))
            print('  tier %d: no hue in its ring (silver) - the barrel stays neutral' % t)
        else:
            made.append((t, tint_to(base, hs[0], hs[1]), hs))
            print('  tier %d: ring hue %.3f sat %.2f' % (t, hs[0], hs[1]))

    os.makedirs(OUT, exist_ok=True)
    if a.check:
        Z = 3; pad = 10
        W = pad + len(made) * (base.width * Z + pad)
        H = base.height * Z + pad * 2 + 16
        card = Image.new('RGBA', (W, H), (28, 30, 38, 255))
        from PIL import ImageDraw
        d = ImageDraw.Draw(card); x = pad
        for t, im, hs in made:
            card.alpha_composite(im.resize((im.width * Z, im.height * Z), Image.NEAREST), (x, pad))
            d.text((x + 4, pad + im.height * Z + 2), 'tier %d' % t, fill=(255, 220, 150, 255))
            x += im.width * Z + pad
        p = os.path.join(OUT, '04_barrel_tiers.png')
        card.save(p); print('--check: wrote', os.path.relpath(p, ROOT))
        return

    for t, im, _ in made:
        p = os.path.join(DST, 'chaingun_barrel_%d.png' % t)
        im.save(p)
        print('wrote', os.path.relpath(p, ROOT))


if __name__ == '__main__':
    main()
