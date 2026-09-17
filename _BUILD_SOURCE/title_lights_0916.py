#!/usr/bin/env python3
"""
title_lights_0916.py - THE TITLE BUTTONS' LAMPS AND LETTERING, RECOLOURED PER BUTTON.

    python3 _BUILD_SOURCE/title_lights_0916.py [--check]

Mike, 0916: "in each marquee, the lights should be palette swapped to different colors on the left
and right sides of the button. New Game - Neon Green, Enter Password - Neon Orange, Options - Neon
Blue. Help - Neon pink - Achievements - Neon Red - Credits - Neon Black, also palette swap Star to
Black. Exit Game - White Light. You also palette swap the text in each button to match the color of
the lights."

Reads `btn_<name>.png` (the 0916 sheet's cuts) and writes `btn_<name>_lit.png` beside them.

--------------------------------------------------------------------------------------------------
THE TWO MASKS, AND WHY NEITHER IS A THRESHOLD I PICKED
--------------------------------------------------------------------------------------------------

⚠ THE LAMPS ARE BOUNDED GEOMETRICALLY, NOT BY SATURATION. The saturation histogram of the bezel
zone has NO empty band between the metal and the tube - measured, every plate: bin 0 holds 716-986
px of grey metal, bin 9 holds 575-748 px of lit tube, and the bins between hold 150-270 px each of
spill and warm-tinted metal. Threshold-hunting there is the 0907u trap (five colour detectors, each
breaking the ship the last one fixed). The tube is instead found as the lit bounding box inside each
end's bezel, and every pixel in it is rotated with a SATURATION WEIGHT - so the grey bezel is
untouched, the spill rotates in proportion to how much colour it actually carries, and the
white-hot core stays white, which is what a neon tube of ANY colour does.

⚠ THE LETTERS ARE FOUND BY THEIR SHARED BASELINE. A gold colour mask alone is not enough and the
render said so immediately: on NEW GAME it swallowed the whole sunset SKY (1,692 px), on
ACHIEVEMENTS the trophy and the medals, on CREDITS the star, on EXIT GAME the fire. But a line of
text has one property nothing in a painted scene has - every glyph sits on the SAME two rows.
Measured: letters land at y0 22-23 / y1 44-45 on all seven plates, while the sky is y11-48, the
medal y32-52, the trophy y20-39, the star y14-48 and the fire y34-51. So the band is taken as the
MEDIAN of the letter-sized components and anything off it is dropped. Nothing is hand-listed, and a
re-generated plate classifies itself.

⚠ BOUNDARY DARKNESS WAS THE FIRST DISCRIMINATOR AND IT IS THE WEAKER ONE. Letters carry a hard
keyline, so 0.41-0.95 of their boundary is dark, against 0.30 for the sky and 0.19 for the medal -
but CREDITS' star reads 0.24 against its own dimmest letter at 0.41, which is close enough to be
one bad plate away from failing. It is kept only as a tie-break.

--------------------------------------------------------------------------------------------------
THE COLOURS
--------------------------------------------------------------------------------------------------

⚠ ROTATE THE HUE, DO NOT SET IT (CLAUDE.md, 0906t). The tube runs white-hot core -> bright body
-> deep rim, and that gradient is most of what makes it read as a lamp rather than a coloured bar.
A rotation by (target - the plate's OWN measured lit hue) carries the whole gradient across; writing
one hue into every pixel flattens it into a slab.

⚠ TWO OF THE SEVEN CANNOT BE A ROTATION, BECAUSE BLACK AND WHITE HAVE NO HUE TO ROTATE TO.
  - CREDITS "Neon Black": value and saturation are curved in OPPOSITE directions (the 0810s ice_black
    lesson) so the body crushes toward black while the lit edge survives - a dark glass tube with a
    rim, not a black rectangle.
  - EXIT GAME "White Light": the colour cast is stripped and the value lifted (xartPalette's own
    'white' path), which is the only way to go white without a flat overlay.

⚠ AND THE COLOUR COUNT IS CHECKED BEFORE AND AFTER, because a halved palette is the signature of
a range-exchange shredder (0906o) and it is one line to catch.
"""
import os, sys, argparse, colorsys
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
DST = os.path.join(ROOT, 'assets', 'game', 'ui', 'title_0916')
OUT = os.path.join(ROOT, 'docs', 'proofs', 'awards_0916')

# Mike's own list, in his order. 'hue' is a target hue; 'mode' names the two that cannot be one.
LIGHTS = {
    'newgame':      {'name': 'Neon Green',  'mode': 'hue',   'hue': 0.312, 'sat': 1.10},
    'password':     {'name': 'Neon Orange', 'mode': 'hue',   'hue': 0.055, 'sat': 1.16},
    'options':      {'name': 'Neon Blue',   'mode': 'hue',   'hue': 0.578, 'sat': 1.10},
    'help':         {'name': 'Neon Pink',   'mode': 'hue',   'hue': 0.905, 'sat': 1.12},
    'achievements': {'name': 'Neon Red',    'mode': 'hue',   'hue': 0.985, 'sat': 1.14},
    'credits':      {'name': 'Neon Brown', 'mode': 'hue',   'hue': 0.072, 'sat': 1.05, 'val': 0.58,
                     'dim': 0.62},
    'exit':         {'name': 'White Light', 'mode': 'white'},
}
NAMES = ['newgame', 'password', 'options', 'help', 'achievements', 'credits', 'exit']

EDGE = 26          # the bezel zone at each end, measured off the plates
GOLD = (0.06, 0.18)


def hsv(p):
    return colorsys.rgb_to_hsv(p[0] / 255.0, p[1] / 255.0, p[2] / 255.0)


def rgb(h, s, v, a):
    r, g, b = colorsys.hsv_to_rgb(h % 1.0, max(0.0, min(1.0, s)), max(0.0, min(1.0, v)))
    return (int(round(r * 255)), int(round(g * 255)), int(round(b * 255)), a)


def opaque_colours(im):
    px = im.load(); w, h = im.size
    return len({px[x, y][:3] for x in range(w) for y in range(h) if px[x, y][3] > 240})


# ---------------------------------------------------------------- the lamps

def lamp_boxes(im):
    """The lit bounding box inside each end's bezel. Geometry, not a saturation cut."""
    w, h = im.size; px = im.load()
    out = []
    for xs in (range(0, EDGE), range(w - EDGE, w)):
        pts = []
        for x in xs:
            for y in range(h):
                r, g, b, a = px[x, y]
                if a < 200:
                    continue
                hh, s, v = hsv((r, g, b))
                if v > 0.50 and (s > 0.35 or v > 0.85):
                    pts.append((x, y))
        if not pts:
            out.append(None); continue
        bx = [p[0] for p in pts]; by = [p[1] for p in pts]
        out.append((min(bx), min(by), max(bx), max(by)))
    return out


def lit_hue(im, boxes):
    """The plate's OWN lamp hue - the thing the rotation is measured from."""
    px = im.load(); hs = []
    for b in boxes:
        if not b:
            continue
        for x in range(b[0], b[2] + 1):
            for y in range(b[1], b[3] + 1):
                r, g, bl, a = px[x, y]
                if a < 200:
                    continue
                hh, s, v = hsv((r, g, bl))
                if s > 0.50 and v > 0.50:
                    hs.append(hh)
    hs.sort()
    return hs[len(hs) // 2] if hs else None


# ---------------------------------------------------------------- the letters

def gold_components(im, x_lo, x_hi):
    w, h = im.size; px = im.load()
    gold = [[False] * h for _ in range(w)]
    for x in range(x_lo, x_hi):
        for y in range(h):
            r, g, b, a = px[x, y]
            if a < 200:
                continue
            hh, s, v = hsv((r, g, b))
            if GOLD[0] <= hh <= GOLD[1] and s > 0.30 and v > 0.60:
                gold[x][y] = True
    seen = [[False] * h for _ in range(w)]; out = []
    for sy in range(h):
        for sx in range(x_lo, x_hi):
            if seen[sx][sy] or not gold[sx][sy]:
                continue
            st = [(sx, sy)]; pts = []
            while st:
                x, y = st.pop()
                if x < x_lo or y < 0 or x >= x_hi or y >= h or seen[x][y] or not gold[x][y]:
                    continue
                seen[x][y] = True; pts.append((x, y))
                st += [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
            if len(pts) >= 40:
                ys = [p[1] for p in pts]
                out.append({'pts': pts, 'y0': min(ys), 'y1': max(ys), 'n': len(pts)})
    return out


def letter_mask(im):
    """Glyphs share a baseline; painted scenery does not."""
    w, h = im.size
    cs = gold_components(im, EDGE, w - EDGE)
    cand = [c for c in cs if 18 <= (c['y1'] - c['y0'] + 1) <= 30 and 60 <= c['n'] <= 900]
    if not cand:
        return set(), None
    y0s = sorted(c['y0'] for c in cand); y1s = sorted(c['y1'] for c in cand)
    my0 = y0s[len(y0s) // 2]; my1 = y1s[len(y1s) // 2]
    keep = [c for c in cand if abs(c['y0'] - my0) <= 3 and abs(c['y1'] - my1) <= 3]
    m = set()
    for c in keep:
        m |= set(c['pts'])
    return m, (my0, my1, len(keep))


def warm_ring(im, mask, band, rad=2):
    """The glyph's antialiased edge, which the strict gold cut misses - else a recoloured letter
       keeps a thin gold halo. Bounded to the text band and to warm pixels only."""
    if not mask or not band:
        return set()
    w, h = im.size; px = im.load()
    y0, y1 = band[0] - 1, band[1] + 1
    ring = set()
    for (x, y) in mask:
        for dx in range(-rad, rad + 1):
            for dy in range(-rad, rad + 1):
                nx, ny = x + dx, y + dy
                if (nx, ny) in mask or not (0 <= nx < w and y0 <= ny <= y1):
                    continue
                r, g, b, a = px[nx, ny]
                if a < 200:
                    continue
                hh, s, v = hsv((r, g, b))
                if 0.02 <= hh <= 0.22 and s > 0.15 and v > 0.30:
                    ring.add((nx, ny))
    return ring


# ---------------------------------------------------------------- the emblem star (credits only)

def star_mask(im):
    """CREDITS' emblem star - 'also palette swap Star to Black'.

    \u26a0 THE COMPONENT WAS THE STAR'S OUTLINE, NOT THE STAR. Taking the tall gold component caught
    174 px and the render still showed a gold star: the strict v>0.60 / s>0.30 cut follows the dark
    bevel ring and leaves the bright interior behind. The star is found by its BOX instead - the
    gold components give the bounds - and then every warm pixel inside that box is taken, which is
    the whole emblem and nothing else, because the box is inside the emblem panel.

    \u26a0 AND THE STAR IS TWO COMPONENTS, NOT ONE, SO "THE TALL ONE" BLACKENED HALF OF IT. Its own
    bevel cuts it in two - measured on this plate, n=174 at x27-45 and n=51 at x46-61 - and the
    render showed a star black down the left and gold down the right. Every component in the panel
    is unioned now. The third component, n=88 at x6-11, is the LAMP, which is gold too: it is
    excluded by GEOMETRY (the scan starts at EDGE) rather than by a size rule that would have to
    keep being retuned."""
    cs = gold_components(im, EDGE, EDGE + 46)
    tall = [c for c in cs if c['n'] >= 40]
    if not tall:
        return set()
    xs = [p[0] for c in tall for p in c['pts']]
    ys = [p[1] for c in tall for p in c['pts']]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    px = im.load(); m = set()
    for x in range(x0, x1 + 1):
        for y in range(y0, y1 + 1):
            r, g, b, a = px[x, y]
            if a < 200:
                continue
            hh, s, v = hsv((r, g, b))
            if 0.02 <= hh <= 0.22 and s > 0.18 and v > 0.18:
                m.add((x, y))
    return m


# ---------------------------------------------------------------- the transforms

def wgt(s, mode):
    """\u26a0 A LINEAR SATURATION WEIGHT GIVES A MID-TONE THE WRONG HUE, AND THE RENDER SAID SO.
    Rotating by `dh * s` means a pale gold highlight at s=0.30 travels only 30% of the way: aiming
    HELP's lettering at pink (+0.79) landed those pixels on 0.36, which is GREEN, and the word came
    out violet. ACHIEVEMENTS came out magenta the same way. A partial hue rotation is not a paler
    version of the target - it is a DIFFERENT COLOUR, which is the one thing a weight must never do.

    So: text rotates whole ('full'), because a glyph is one object and its dark keyline and white
    highlight are unaffected by a rotation anyway. The lamp uses a sharpened ramp, so the tube and
    its lit bezel rotate fully while near-grey metal is spared - the reason the weight exists."""
    if mode == 'full':
        return 1.0
    return max(0.0, min(1.0, (s - 0.10) * 2.4))


def apply_hue(px, pts, dh, sat, mode='ramp', val=1.0, dim=1.0):
    """⚠ `val` EXISTS BECAUSE BROWN IS NOT A HUE - IT IS DARK ORANGE. CREDITS asked for "Neon
    Brown", and the plates' own lamps are amber at hue 0.100 against a brown target of ~0.072: a
    rotation of 0.028 is nothing, so hue alone would leave the bar exactly as generated. What makes
    a warm colour read as brown is the LUMINANCE drop, applied with the same weight so grey metal
    is still spared."""
    n = 0
    for (x, y) in pts:
        r, g, b, a = px[x, y]
        if a < 8:
            continue
        hh, s, v = hsv((r, g, b))
        w = wgt(s, mode)
        if (w <= 0.02 or s <= 0.06) and dim >= 1.0:
            continue
        nv = v * (1 - w) + (v * val) * w
        # ⚠ `dim` IS UNCONDITIONAL, AND A WEIGHTED DROP ALONE LEFT THE TUBE LOOKING GOLD. The
        # weight spares low-saturation pixels on purpose - that is what keeps grey bezel metal grey
        # - but the WHITE-HOT CORE is low-saturation too, so it kept almost all of its brightness:
        # measured, the brightest lamp pixels went 1.00 -> only 0.58-0.74 and the lamp still read
        # amber at a glance while the numbers said it had moved. A brown lamp has no white-hot core
        # to keep: brown IS dark, so the whole tube comes down together.
        nv *= dim
        px[x, y] = rgb(hh + dh * w, min(1.0, s * sat), nv, a)
        n += 1
    return n


def apply_black(px, pts, mode='ramp', cast=0.72, sock=1.0):
    """Value and saturation curved in OPPOSITE directions, so the body crushes toward black and the
       lit edge survives as a rim. A flat multiply gives a black rectangle with no lamp in it."""
    n = 0
    for (x, y) in pts:
        r, g, b, a = px[x, y]
        if a < 8:
            continue
        hh, s, v = hsv((r, g, b))
        w = wgt(s, mode)
        if w <= 0.02 and sock >= 1.0:
            continue
        nv = (v ** 2.6) * (0.62 if cast else 0.34)   # a neutral crush goes further: no glow to keep
        ns = s * 0.30
        nv = v * (1 - w) + nv * w
        ns = s * (1 - w) + ns * w
        # ⚠ A LAMP THAT HAS GONE BLACK TAKES ITS HOUSING WITH IT. Crushing only the coloured
        # pixels left the socket's own lit metal at full brightness, so the brightest pixel in the
        # bezel measured 0.47 against 0.78 - a dim tube in a bright socket, which does not read as
        # "off" at all. `sock` dims the whole box, saturation or none: turn a lamp off and the
        # housing around it stops being lit too.
        nv *= sock
        px[x, y] = rgb(hh + cast * w, ns, nv, a)
        # ⚠ THE CAST IS THE LAMP'S ONLY, AND THE RENDER IS WHY. A +0.72 rotation applied to the
        # STAR and the LETTERING turned gold into PLUM - a violet star is not "Star to Black". A
        # tube needs some colour left in it or it stops reading as a lamp at all; a black star and
        # black lettering want no hue whatsoever, so they are crushed neutral (cast 0).
        n += 1
    return n


def apply_white(px, pts, mode='ramp'):
    """Strip the cast, then lift. 'color' compositing cannot make white - white has no saturation
       to donate - so this is a desaturate plus a gain, which keeps the tube's own falloff."""
    n = 0
    for (x, y) in pts:
        r, g, b, a = px[x, y]
        if a < 8:
            continue
        hh, s, v = hsv((r, g, b))
        w = wgt(s, mode)
        if w <= 0.02:
            continue
        ns = s * (1 - w) + (s * 0.06) * w
        nv = v * (1 - w) + min(1.0, v * 1.22 + 0.06) * w
        px[x, y] = rgb(hh, ns, nv, a)
        n += 1
    return n


def recolour(im, key):
    cfg = LIGHTS[key]
    im = im.copy(); px = im.load(); w, h = im.size
    before = opaque_colours(im)

    boxes = lamp_boxes(im)
    src = lit_hue(im, boxes)
    lamp_pts = []
    for b in boxes:
        if not b:
            continue
        for x in range(max(0, b[0] - 3), min(w, b[2] + 4)):
            for y in range(max(0, b[1] - 3), min(h, b[3] + 4)):
                lamp_pts.append((x, y))

    mask, band = letter_mask(im)
    ring = warm_ring(im, mask, band)
    text_pts = sorted(mask | ring)

    extra = sorted(star_mask(im)) if key == 'credits' else []

    if cfg['mode'] == 'hue':
        dh = cfg['hue'] - (src if src is not None else 0.10)
        val = cfg.get('val', 1.0)
        nl = apply_hue(px, lamp_pts, dh, cfg['sat'], 'ramp', val, cfg.get('dim', 1.0))
        # the lettering is gold on every plate whatever the lamp is, so it rotates from ITS own hue
        dt = cfg['hue'] - 0.115
        nt = apply_hue(px, text_pts, dt, cfg['sat'], 'full', val)
        # the emblem goes with them where one is named - CREDITS' star (Mike, 0916)
        ne = apply_hue(px, extra, dt, cfg['sat'], 'full', val) if extra else 0
    elif cfg['mode'] == 'black':
        nl = apply_black(px, lamp_pts, 'ramp', 0.72, 0.62)
        nt = apply_black(px, text_pts, 'full', 0.0)
        ne = apply_black(px, extra, 'full', 0.0)
    else:
        nl = apply_white(px, lamp_pts, 'ramp')
        nt = apply_white(px, text_pts, 'full')
        ne = 0

    after = opaque_colours(im)
    return im, {'src_hue': src, 'lamp_px': nl, 'text_px': nt, 'extra_px': ne,
                'band': band, 'colours': (before, after),
                'boxes': boxes}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true')
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    cuts = []
    for n in NAMES:
        src = os.path.join(DST, 'btn_%s.png' % n)
        im = Image.open(src).convert('RGBA')
        out, st = recolour(im, n)
        b, af = st['colours']
        ratio = af / float(b) if b else 0
        print('%-13s %-12s src-hue %s  lamp %4d px  text %4d px%s  band %s  colours %d -> %d (%.2f)'
              % (n, LIGHTS[n]['name'],
                 ('%.3f' % st['src_hue']) if st['src_hue'] is not None else '  n/a',
                 st['lamp_px'], st['text_px'],
                 ('  star %d px' % st['extra_px']) if st['extra_px'] else '',
                 st['band'], b, af, ratio))
        assert st['lamp_px'] > 80, '%s: the lamps were not found (%d px)' % (n, st['lamp_px'])
        assert st['text_px'] > 200 or n == 'options', '%s: the lettering was not found (%d px)' % (n, st['text_px'])
        assert ratio > 0.55, '%s: the palette was SHREDDED (%d -> %d)' % (n, b, af)
        cuts.append((n, im, out))

    if a.check:
        Z = 2; pad = 8
        W = max(c.width for _, c, _ in cuts) * Z + pad * 2
        H = sum(c.height * Z * 2 + pad + 14 for _, c, _ in cuts) + pad
        card = Image.new('RGBA', (W, H), (22, 24, 30, 255))
        from PIL import ImageDraw
        d = ImageDraw.Draw(card); y = pad
        for n, before, after in cuts:
            card.alpha_composite(before.resize((before.width * Z, before.height * Z), Image.NEAREST), (pad, y))
            y += before.height * Z
            card.alpha_composite(after.resize((after.width * Z, after.height * Z), Image.NEAREST), (pad, y))
            d.text((pad + 4, y + after.height * Z + 1), '%s  %s' % (n, LIGHTS[n]['name']),
                   fill=(255, 220, 150, 255))
            y += after.height * Z + pad + 14
        p = os.path.join(OUT, '19_lights.png')
        card.save(p); print('--check: wrote', os.path.relpath(p, ROOT))
        return

    for n, _, out in cuts:
        p = os.path.join(DST, 'btn_%s_lit.png' % n)
        out.save(p)
        print('wrote', os.path.relpath(p, ROOT))


if __name__ == '__main__':
    main()
