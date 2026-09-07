#!/usr/bin/env python3
"""recolour_juggernaut_brown_0906m.py - jugv2_b to shades of brown and brown-orange.

    python _BUILD_SOURCE/recolour_juggernaut_brown_0906m.py            # proof only
    python _BUILD_SOURCE/recolour_juggernaut_brown_0906m.py --write

Mike, 0906: "use jugv2b as the ship but palette swap to shades of brown and brown/orange."

MEASURED FIRST. jugv2_b is 62% desaturated grey (median value 0.27, p05 0.00, p95 0.65), 27.1%
already in hue 0-30 and 5.4% in 30-60. So the job is the GREY PLATING; the warm pixels are the
engine glow and the few lit copper edges, and those are left alone - recolouring them would flatten
the exhaust into the hull.

⚠ "SHADES OF BROWN" IS A RANGE, NOT A TINT, WHICH IS WHY THE HUE MOVES WITH VALUE. A single brown
hue applied at one saturation gives a flat brown silhouette - the same failure the Lizzie gold rule
avoided in 0906b, and the same reason CLAUDE.md's font bug happened: a flat fill destroys the
modelling underneath. Here the darkest plating takes a deep brown (16 deg) and the lit faces run up
to brown-orange (28 deg), with saturation riding value so near-black stays near-black. That is what
makes it read as brown PLATING rather than as a brown shape. (Those two angles were 18/34 in the
first cut and are named again below where they are set - a docstring quoting numbers the code no
longer holds is this repo's "comment describing a change the code never received".)

⚠ AND VALUE IS PRESERVED EXACTLY. This is a hue/saturation swap, per the standing rule. The one
deliberate exception this project has made to that was Decker's black/yellow exchange in 0906h,
where the two bands had to trade brightness or the swap would have been invisible; nothing like
that applies here, so V is untouched and every rivet, bevel and panel line survives.
"""
import os, sys, colorsys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, '_BUILD_SOURCE/sc_out_0906/jugv2_b.png')
OUT = os.path.join(ROOT, '_BUILD_SOURCE/sc_out_0906/jugv2_b_brown.png')

# ⚠ CHOSEN FROM A RENDERED SWEEP, NOT PICKED. Four treatments were generated and compared side by
# side (docs/JUGGERNAUT_BROWN_SWEEP_0906M.png): 18-34 at s.34-.64 came out khaki-olive rather than
# brown, 14-26 at s.55-.82 tipped over into rust-orange and stopped reading as brown at all, and
# 20-32 went pale tan. 16-28 at s.45-.72 is the one that reads as Mike asked - brown in the body
# with brown-orange where the light catches it.
BROWN_DARK = 16.0 / 360.0     # deep, slightly red brown in the shadows
BROWN_LIT = 28.0 / 360.0      # brown-orange on the lit faces


def rule(h, s, v):
    if s < 0.20:                                   # the grey plating - the 62% this is aimed at
        f = min(1.0, max(0.0, v / 0.70))           # how lit this pixel is, across the real spread
        nh = BROWN_DARK + (BROWN_LIT - BROWN_DARK) * f
        ns = 0.45 + 0.27 * f                       # deeper colour as it catches light
        return nh, ns, v                           # V UNTOUCHED
    if h * 360 <= 60 and s >= 0.20:                # already warm: engine glow, lit copper
        return h, s, v                             # left alone on purpose
    return h, min(1.0, s * 0.55), v                # anything else damped toward the scheme


def recolour(im):
    px = im.load(); n = 0
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            if a < 8:
                continue
            h, s, v = colorsys.rgb_to_hsv(r / 255., g / 255., b / 255.)
            nh, ns, nv = rule(h, s, v)
            if (nh, ns, nv) != (h, s, v):
                n += 1
                rr, gg, bb = colorsys.hsv_to_rgb(nh, max(0., min(1., ns)), max(0., min(1., nv)))
                px[x, y] = (int(rr * 255 + .5), int(gg * 255 + .5), int(bb * 255 + .5), a)
    return n


def main():
    write = '--write' in sys.argv
    src = Image.open(SRC).convert('RGBA')
    bb = src.getbbox()
    if bb:
        src = src.crop(bb)
    new = src.copy()
    n = recolour(new)
    print('jugv2_b %dx%d - %d pixels recoloured (value preserved on every one)' % (new.width, new.height, n))

    # the facing check again, on the plate that will actually be used
    px = new.load()
    gy = gw = iy = iw = 0.0
    for y in range(new.height):
        for x in range(new.width):
            r, g, b, a = px[x, y]
            if a < 32:
                continue
            iy += y; iw += 1
            h, s, v = colorsys.rgb_to_hsv(r / 255., g / 255., b / 255.)
            if v >= 0.80 and s >= 0.45 and (h < 0.12 or h > 0.92):
                gy += y * v; gw += v
    if gw > 0:
        a, b2 = gy / gw / (new.height - 1), iy / iw / (new.height - 1)
        print('exhaust y %.3f vs centroid %.3f -> %s' % (a, b2,
              'NORTH-facing' if a > b2 else 'SOUTH - DO NOT USE'))

    from PIL import ImageDraw, ImageFont
    try:
        F = ImageFont.truetype('C:/Windows/Fonts/consolab.ttf', 16)
    except Exception:
        F = ImageFont.load_default()
    T = 340
    proof = Image.new('RGB', (T * 2, T + 24), (22, 22, 28))
    d = ImageDraw.Draw(proof)
    for i, (lbl, im) in enumerate((('jugv2_b BEFORE', src), ('AFTER - browns', new))):
        s = min((T - 14) / im.width, (T - 14) / im.height)
        t = im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.LANCZOS)
        proof.paste(t, (i * T + (T - t.width) // 2, (T - t.height) // 2), t)
        d.text((i * T + 5, T + 5), lbl, font=F, fill=(240, 240, 250))
    proof.save(os.path.join(ROOT, 'docs/JUGGERNAUT_BROWN_0906M.png'))
    print('wrote docs/JUGGERNAUT_BROWN_0906M.png')

    if not write:
        print('DRY RUN - nothing written. Re-run with --write.')
        return 0
    new.save(OUT)
    print('wrote %s' % os.path.relpath(OUT, ROOT))
    return 0


if __name__ == '__main__':
    sys.exit(main())
