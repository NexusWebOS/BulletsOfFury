#!/usr/bin/env python3
"""s9_palette_variants_0905.py - the stage-9 recolour pass.

Mike, 0905, on the two approved rosters: "they all have these purple halo's on their edge of the
units, and they all look too similar with color. we need to do some palette swaps to black, blue,
pink, green, dark gray, light gray and neon red."

Two separate defects, and they need different fixes:

1. THE HALO IS A 1px OPAQUE RIM BAKED INTO THE PLATE, NOT ANTI-ALIASING. Measured: semi-alpha
   pixels = 0 on every prototype cell and every in-game hull, so there is no soft fringe to
   threshold away. Eroding the alpha mask one shell at a time, the OUTERMOST shell of the
   prototype units comes back dark and violently saturated (value 0.27-0.38, sat 0.68-0.78) while
   the shell behind it is brighter - a saturated violet outline that reads as a glow against the
   near-black void. The in-game cast already does the right thing: `s9ring` shells 0-1 measure
   value 0.047, i.e. an almost pure black outline. So the fix is not to delete the rim - deleting
   it would leave the hull with no edge at all against the background - it is to RESTATE the rim
   in the stage's own house style, near-black, tinted a little toward the unit's new colour.

2. "TOO SIMILAR WITH COLOR" is true and measurable: every prototype cell sits at 38-51% purple
   and 30-36% blue by hue, and every in-game hull at 73-78% blue. The whole stage is one hue.

⚠ THE SWAP MUST PRESERVE LUMINANCE, NOT FLOOD THE SPRITE. This is the rule CLAUDE.md already
carries for xartPalette vs xartTint: a source-atop flood repaints every pixel one colour and
destroys the shading that makes the hull read as metal. Here each pixel keeps its own VALUE and
gets the variant's hue and saturation, so plating, panel lines and specular highlights survive.

⚠ AND THE GLOWING CORE IS EXEMPT. Every one of these hulls has a hot cyan-white core. Rolled
through a hue swap it turns into a hot green or hot pink blob and the unit stops reading as
"powered", so the lens is held out of the swap and a green Prism Mine keeps a cyan eye. See
core_mask below for why that exemption has to be a REGION and not a per-pixel threshold - the
first attempt used one and Mike caught the result immediately.

Three of Mike's seven are not hues at all - black, dark gray, light gray - so they are handled as
value curves at zero saturation rather than as hue rotations, which is why VARIANTS carries `sat`
and `curve` alongside `hue`.
"""
import colorsys, json, os, sys
from PIL import Image, ImageFilter

# name -> (hue 0..1 or None for greyscale, saturation, value curve (gain, lift))
VARIANTS = {
    'black':     (None,  0.00, (0.42, 0.00)),
    'blue':      (0.605, 0.72, (1.00, 0.00)),
    'pink':      (0.905, 0.62, (1.06, 0.04)),
    'green':     (0.345, 0.66, (1.00, 0.02)),
    'darkgray':  (None,  0.00, (0.66, 0.02)),
    'lightgray': (None,  0.00, (0.92, 0.26)),
    'neonred':   (0.985, 0.88, (1.10, 0.03)),
    # the miniboss keeps its generated colour; listed so the same code can pass it through
    'asis':      (-1.0,  0.00, (1.00, 0.00)),
}

# ---- THE CORE GLOW IS A REGION, NOT A PER-PIXEL TEST ---------------------------------------
# ⚠ Mike, 0905, on the first black variant: "fix the internal light". The per-pixel test this
# replaces was `v >= 0.62 and cyan-hued and s >= 0.10`, and the `s >= 0.10` clause is what broke
# it: the CENTRE of every core is a near-WHITE hotspot with saturation below 0.10, so the hottest
# pixels in the sprite failed the "is this the core" test, fell through to the black value curve
# (gain 0.42) and came back as dark speckles INSIDE the light. Measured on the first pass: the
# black variant's core carried mottled grey noise the dark-purple one did not.
# The mid-value cyan ramp around the lens failed it too, for a different reason - it sits below
# 0.62 - which is what made the ring ragged.
# So the core is now FLOOD-LABELLED. A generous candidate set (the cyan ramp, plus anything
# near-white regardless of hue) is split into connected components, and a component is kept only
# if it contains a genuinely bright, genuinely cyan SEED pixel. That keeps a lens whole - hotspot,
# ramp and all - without letting every stray pale highlight on the hull escape the swap.
H_LO, H_HI = 150.0 / 360.0, 235.0 / 360.0
SEED_V, SEED_S = 0.70, 0.15        # "this is definitely a light"
CAND_V = 0.45                      # the cyan ramp around it
WHITE_V = 0.78                     # a near-white hotspot counts whatever its hue
RIM_V, RIM_S = 0.16, 0.35          # what the restated outline is forced to


def core_mask(im):
    """Set of (x,y) belonging to a glowing light: flood-labelled, seeded by bright cyan."""
    px = im.load()
    w, h = im.size
    cand, seed = set(), set()
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a == 0:
                continue
            hh, ss, vv = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
            cyan = H_LO <= hh <= H_HI
            if (cyan and vv >= CAND_V) or vv >= WHITE_V:
                cand.add((x, y))
                if cyan and vv >= SEED_V and ss >= SEED_S:
                    seed.add((x, y))
    out, seen = set(), set()
    for p in cand:
        if p in seen:
            continue
        stack, comp = [p], []
        seen.add(p)
        while stack:
            cx, cy = stack.pop()
            comp.append((cx, cy))
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    q = (cx + dx, cy + dy)
                    if q in cand and q not in seen:
                        seen.add(q)
                        stack.append(q)
        if any(q in seed for q in comp):
            out.update(comp)
    return out


def drop_strays(im):
    """Delete every alpha component that is not the main body.

    ⚠ Mike, 0905: "remove that out of the echoof sprite". Measured across the whole prototype
    roster, `echof` is the ONLY unit with detached geometry - a 59px sliver at x11-13,y80-102 plus
    one orphan pixel at (11,77), identical in all four of its frames. Every other unit is a single
    component, so this pass is a no-op for them and cannot quietly amputate an intentionally
    detached part."""
    px = im.load()
    w, h = im.size
    seen = [[False] * w for _ in range(h)]
    comps = []
    for y in range(h):
        for x in range(w):
            if px[x, y][3] == 0 or seen[y][x]:
                continue
            stack, comp = [(x, y)], []
            seen[y][x] = True
            while stack:
                cx, cy = stack.pop()
                comp.append((cx, cy))
                for dx in (-1, 0, 1):
                    for dy in (-1, 0, 1):
                        nx, ny = cx + dx, cy + dy
                        if 0 <= nx < w and 0 <= ny < h and not seen[ny][nx] and px[nx, ny][3] > 0:
                            seen[ny][nx] = True
                            stack.append((nx, ny))
            comps.append(comp)
    if len(comps) <= 1:
        return im, 0
    comps.sort(key=len, reverse=True)
    out = im.copy()
    op = out.load()
    n = 0
    for c in comps[1:]:
        for (x, y) in c:
            op[x, y] = (0, 0, 0, 0)
            n += 1
    return out, n


def recolour(im, variant, rim=True):
    """Return a new RGBA plate in `variant`, luminance preserved, core glow held out, and the
    outermost 1px shell restated as a near-black outline."""
    hue, sat, (gain, lift) = VARIANTS[variant]
    im = im.convert('RGBA')
    core = core_mask(im)
    out = im.copy()
    px, op = im.load(), out.load()
    w, h = im.size

    # the outermost shell: opaque pixels that vanish under a single erosion of the alpha mask
    mask = im.split()[3].point(lambda v: 255 if v > 0 else 0)
    inner = mask.filter(ImageFilter.MinFilter(3))
    mk, ik = mask.load(), inner.load()

    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            if a == 0:
                op[x, y] = (0, 0, 0, 0)
                continue
            hh, ss, vv = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
            edge = mk[x, y] and not ik[x, y]
            if (x, y) in core and not edge:
                continue                                   # the powered core is never swapped
            if hue is not None and hue < 0:                # 'asis' - body untouched
                nh, ns, nv = hh, ss, vv
            elif hue is None:                              # greyscale families
                nh, ns, nv = 0.0, 0.0, vv
            else:
                nh, ns, nv = hue, min(1.0, ss * 0.35 + sat), vv
            nv = max(0.0, min(1.0, nv * gain + lift))
            if edge and rim:
                # restate the outline: the stage's own near-black edge, faintly tinted
                nv, ns = min(nv, RIM_V), (0.0 if hue is None else min(ns, RIM_S))
            nr, ng, nb = colorsys.hsv_to_rgb(nh, ns, nv)
            op[x, y] = (int(nr * 255 + .5), int(ng * 255 + .5), int(nb * 255 + .5), a)
    return out


def quantize(im, n):
    """Snap to n colours, dither OFF. SpriteCook returns 3,800+ colours on a plate whose in-game
    neighbours carry 362-414; dithering a target this small sprays checkerboard noise across flat
    armour and reads as JPEG rot at 2x."""
    a = im.split()[3]
    q = im.convert('RGB').quantize(colors=n, method=Image.MEDIANCUT, dither=Image.Dither.NONE)
    o = q.convert('RGB').convert('RGBA')
    o.putalpha(a)
    p = o.load()
    for y in range(o.height):
        for x in range(o.width):
            if p[x, y][3] == 0:
                p[x, y] = (0, 0, 0, 0)
    return o


def colours(im):
    px = im.load()
    return len({px[x, y][:3] for y in range(im.height) for x in range(im.width) if px[x, y][3] > 0})


if __name__ == '__main__':
    print(__doc__)
    print('variants: %s' % ', '.join(k for k in VARIANTS if k != 'asis'))
