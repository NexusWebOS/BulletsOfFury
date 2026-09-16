#!/usr/bin/env python3
"""
bossbar_shield_0916.py - THE SHIELD GETS ITS OWN BAR, AND THE FILLS BECOME OURS.

    python3 _BUILD_SOURCE/bossbar_shield_0916.py [--check]

Mike, 0916: "Shield should get it's own shield like boss bar, not the same as the boss bar. our own
custom solid/shield fills too. and Shield should be colored Blue as text."

Builds four things and appends them to assets/game/atlas/ui_bossbar.png:

  bmbar_frame_shield   700x33  the shield's OWN bar
  bmbar_tab_shield     204x30  its tab, built from that frame's own bands
  bmbar_fill_solid     578x13  our own SOLID hp fill (the pack's is hazard stripes)
  bmbar_sf2_over/hex/plasma/low  578x13  our own shield fills, a hex field losing power

⚠ THE SHIELD FRAME IS A HUE ROTATION OF THE BOSS FRAME, NOT A NEW DRAWING AND NOT A FLAT REPAINT.
CLAUDE.md's standing rule is palette/luminance swaps, and 0906t's correction to it is ROTATE the
hue, never SET it - setting one hue flattens a gradient that is most of what makes metal read as
metal. The rails run gold (246,227,100) into orange (169,39,1); rotated they run pale cyan into
deep blue with every bevel, rivet and shadow intact. That also guarantees the two bars are the
same object in two liveries rather than two designs that can drift apart.

⚠ AND THE TAB IS BUILT FROM THE SHIELD FRAME'S OWN BANDS, by the same routine 0912e used on the
boss frame. A tab recoloured separately is a second chance to not match.

⚠ THE WELL CARRIES A FAINT HEX LATTICE so an EMPTY shield bar still reads as a field rather than as
an empty hp bar. It is drawn at low alpha INSIDE the measured well only, never over the rails.

⚠ THE FILLS ARE AUTHORED AT A LUMINANCE RAMP, NOT AT A COLOUR. `xartPalette` composites in 'color'
- hue and saturation from the fill, LUMINOSITY from the plate - so a fill with a flat interior
tints to a flat slab. Each of these carries the lit top row, the body and the shaded bottom two
rows the authored fills carry, which is what survives the swap and keeps the bar reading as a tube.
"""
import os, sys, io, json, re, math, argparse
from PIL import Image, ImageDraw
import colorsys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
ATLAS = os.path.join(ROOT, 'assets', 'game', 'atlas', 'ui_bossbar.png')
MANIFEST = os.path.join(ROOT, 'assets', 'manifest.js')
SHEET = 'ui_bossbar'

FRAME_BOSS = (2, 39, 700, 33)
FILL_W, FILL_H = 578, 13
TAB_W, TAB_H = 204, 30

# the well, measured off the boss frame's own pixels in 0910c and carried in game.js as BMBAR.boss
WELL = (61, 11, 578, 12)          # x, y, w, h inside the 700x33 frame

# gold -> ice. Measured on the frame: the lit rail sits at hue ~0.14 (gold) and the deep rail at
# ~0.02 (orange-red). The rotation is a constant ADDITION, so the two stay the same distance apart.
HUE_ROT = 0.42                    # +151 degrees: gold -> pale cyan, orange -> deep blue
SAT_K = 1.06                      # a touch more chroma, because blue reads flatter than gold


def rotate_hue(im, rot=HUE_ROT, sat_k=SAT_K):
    """Rotate hue, keep value. Never sets a hue; never touches alpha."""
    out = im.copy().convert('RGBA')
    px = out.load()
    for y in range(out.height):
        for x in range(out.width):
            r, g, b, a = px[x, y]
            if a == 0:
                continue
            h, s, v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
            h = (h + rot) % 1.0
            s = min(1.0, s * sat_k)
            r2, g2, b2 = colorsys.hsv_to_rgb(h, s, v)
            px[x, y] = (int(r2 * 255 + .5), int(g2 * 255 + .5), int(b2 * 255 + .5), a)
    return out


def hex_lattice(w, h, cell, colour, alpha, phase=0.0):
    """A flat-topped hex lattice as a standalone RGBA layer. Drawn at 4x and reduced, because a
       one-pixel hex outline drawn directly at 13px tall comes out as dashes."""
    Z = 4
    lay = Image.new('RGBA', (w * Z, h * Z), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    R = cell * Z / 2.0
    dx = R * 1.5
    dy = R * math.sqrt(3)
    col = colour + (alpha,)
    j = 0
    x = -R + phase * dx
    while x < w * Z + R * 2:
        off = (dy / 2.0) if (j % 2) else 0.0
        y = -R + off
        while y < h * Z + R * 2:
            pts = [(x + R * math.cos(math.radians(60 * k)), y + R * math.sin(math.radians(60 * k))) for k in range(6)]
            d.line(pts + [pts[0]], fill=col, width=max(1, int(Z * 0.9)))
            y += dy
        x += dx
        j += 1
    return lay.resize((w, h), Image.LANCZOS)


def shade(strip):
    """The profile every authored fill in this sheet carries: a lit top row, a bright second row,
       the body, and two shaded rows at the bottom. It is what makes a flat strip read as a tube,
       and it is the part that SURVIVES an xartPalette swap (which keeps luminosity)."""
    px = strip.load()
    for x in range(strip.width):
        for y in range(strip.height):
            r, g, b, a = px[x, y]
            if a == 0:
                continue
            if y == 0:
                k = 1.52
            elif y == 1:
                k = 1.22
            elif y == strip.height - 1:
                k = 0.46
            elif y == strip.height - 2:
                k = 0.62
            else:
                k = 1.0
            px[x, y] = (min(255, int(r * k)), min(255, int(g * k)), min(255, int(b * k)), a)
    return strip


def solid_fill():
    """OUR OWN SOLID FILL. The pack's boss fill is hazard stripes; Mike asked for a solid one.
       Authored in the sheet's own gold-orange so stage 2 uses it untouched and every other stage
       swaps it by hue, exactly as bmbarFill already does for the striped plate."""
    s = Image.new('RGBA', (FILL_W, FILL_H), (0, 0, 0, 0))
    px = s.load()
    top, bot = (255, 196, 64), (196, 96, 10)
    for y in range(FILL_H):
        f = y / max(1, FILL_H - 1)
        c = tuple(int(top[i] + (bot[i] - top[i]) * f) for i in range(3))
        for x in range(FILL_W):
            px[x, y] = c + (255,)
    # a slow travelling sheen, so a long bar is not one dead colour across 578px
    for x in range(FILL_W):
        k = 1.0 + 0.055 * math.sin(x / FILL_W * math.pi * 6)
        for y in range(FILL_H):
            r, g, b, a = px[x, y]
            px[x, y] = (min(255, int(r * k)), min(255, int(g * k)), min(255, int(b * k)), a)
    return shade(s)


SHIELD_STATES = [
    # name,            base rgb,           lattice rgb,       lattice alpha, cell
    ('bmbar_sf2_over',   (150, 236, 255), (255, 255, 255), 210, 9),
    ('bmbar_sf2_hex',    ( 64, 186, 255), (196, 244, 255), 180, 9),
    ('bmbar_sf2_plasma', ( 38, 126, 226), (150, 206, 255), 150, 9),
    ('bmbar_sf2_low',    ( 28,  76, 146), (110, 156, 210), 110, 9),
]


def shield_fill(base, lat, alpha, cell, phase):
    """OUR OWN SHIELD FILL: a hex field, blue, losing power as it drains. Four states, ONE
       construction - so a shield at 90% and a shield at 10% are visibly the same field with
       different energy in it, not two different materials. (0912e's generated 'failing shield'
       quadrant was dropped for exactly that reason: at 13px it read as television static.)"""
    s = Image.new('RGBA', (FILL_W, FILL_H), (0, 0, 0, 0))
    px = s.load()
    for y in range(FILL_H):
        f = abs((y / max(1, FILL_H - 1)) - 0.42) * 2.0      # brightest just above the middle
        k = 1.0 - 0.34 * f
        c = tuple(min(255, int(base[i] * k)) for i in range(3))
        for x in range(FILL_W):
            px[x, y] = c + (255,)
    s.alpha_composite(hex_lattice(FILL_W, FILL_H, cell, lat, alpha, phase))
    return shade(s)


def build_tab(fr):
    """0912e's construction, verbatim in shape: the frame's own rail band for the top and sides and
       its own well for the interior, so the tab cannot drift from the bar it sits on."""
    RAIL_TOP, RAIL_BOT = 1, 7
    rail = fr.crop((300, RAIL_TOP, 360, RAIL_BOT))
    well = fr.crop((300, 12, 360, 20))
    rh = rail.height
    tab = Image.new('RGBA', (TAB_W, TAB_H), (0, 0, 0, 0))
    tab.paste(well.resize((TAB_W, TAB_H), Image.NEAREST), (0, 0))
    tab.paste(rail.resize((TAB_W, rh), Image.NEAREST), (0, 0))
    side = rail.resize((TAB_H, rh), Image.NEAREST).rotate(90, expand=True)
    tab.paste(side, (0, 0))
    tab.paste(side.transpose(Image.FLIP_LEFT_RIGHT), (TAB_W - rh, 0))
    tab.paste(rail.resize((TAB_W, rh), Image.NEAREST), (0, 0))
    seam = fr.crop((300, 0, 360, 1)).resize((TAB_W, 1), Image.NEAREST)
    tab.paste(seam, (0, TAB_H - 1))
    return tab


def opaque_colours(im):
    px = im.convert('RGBA').load()
    seen = set()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            if a > 8:
                seen.add((r, g, b))
    return len(seen)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--check', action='store_true'); a = ap.parse_args()
    im = Image.open(ATLAS).convert('RGBA')
    fb = im.crop((FRAME_BOSS[0], FRAME_BOSS[1], FRAME_BOSS[0] + FRAME_BOSS[2], FRAME_BOSS[1] + FRAME_BOSS[3]))

    # ---- the shield frame -----------------------------------------------------------------
    sf = rotate_hue(fb)
    # ⚠ COUNT THE COLOURS BEFORE AND AFTER (0906o). A halved opaque-colour count is the signature of
    # a shredded palette, and it is one line to check.
    c0, c1 = opaque_colours(fb), opaque_colours(sf)
    print('frame colours %d -> %d (%.2f)' % (c0, c1, c1 / max(1, c0)))
    assert c1 >= c0 * 0.80, 'the hue rotation shredded the palette: %d -> %d' % (c0, c1)
    # ⚠ THE TAB IS BUILT FROM THE CLEAN FRAME, BEFORE THE LATTICE GOES INTO THE WELL. build_tab
    # samples a 60x8 patch of the well and stretches it to 204x30 - which is harmless on flat black
    # and catastrophic on a texture: the first cut latticed the frame first and the tab came back
    # with five stretched hexes the height of the whole tab. Rendered at 2x it was obvious and no
    # number in the build said a word about it. The tab gets its own lattice, at its own scale,
    # inside its own measured socket (rows 5..29, cols 5..198 of the 204x30 plate).
    tab = build_tab(sf)
    TW = (5, 5, 194, 24)
    tl = Image.new('RGBA', (TW[2], TW[3]), (0, 0, 0, 0))
    tl.alpha_composite(hex_lattice(TW[2], TW[3], 9, (90, 170, 230), 52, 0.0))
    tab.alpha_composite(tl, (TW[0], TW[1]))

    # the faint hex lattice, inside the measured well ONLY - so an EMPTY shield bar still reads as
    # a field rather than as an empty hp bar
    well = Image.new('RGBA', (WELL[2], WELL[3]), (0, 0, 0, 0))
    well.alpha_composite(hex_lattice(WELL[2], WELL[3], 9, (90, 170, 230), 58, 0.0))
    sf.alpha_composite(well, (WELL[0], WELL[1]))

    cells = [('bmbar_frame_shield', sf), ('bmbar_tab_shield', tab), ('bmbar_fill_solid', solid_fill())]
    for i, (n, base, lat, alpha, cell) in enumerate(SHIELD_STATES):
        cells.append((n, shield_fill(base, lat, alpha, cell, i * 0.33)))

    if a.check:
        Z = 2; pad = 8
        W = max(c.width for _, c in cells) * Z + 240
        H = sum(c.height * Z + pad for _, c in cells) + pad
        card = Image.new('RGBA', (W, H), (30, 33, 40, 255))
        d = ImageDraw.Draw(card); y = pad
        for n, c in cells:
            card.alpha_composite(c.resize((c.width * Z, c.height * Z), Image.NEAREST), (230, y))
            d.text((8, y + c.height * Z // 2 - 4), n, fill=(180, 226, 255, 255))
            y += c.height * Z + pad
        p = os.path.join(ROOT, 'docs', 'proofs', 'bossbar_0916', '01_new_art.png')
        os.makedirs(os.path.dirname(p), exist_ok=True)
        card.save(p); print('--check: wrote', os.path.relpath(p, ROOT))
        for n, c in cells: print('   %-22s %dx%d  %d colours' % (n, c.width, c.height, opaque_colours(c)))
        return

    PAD = 2
    x, y, rowh = PAD, im.height + PAD, 0
    W = max(im.width, max(c[1].width for c in cells) + PAD * 2)
    placed = []
    for n, c in cells:
        if x + c.width + PAD > W:
            x = PAD; y += rowh + PAD; rowh = 0
        placed.append((n, c, x, y)); x += c.width + PAD; rowh = max(rowh, c.height)
    out = Image.new('RGBA', (W, y + rowh + PAD), (0, 0, 0, 0))
    out.paste(im, (0, 0))
    rows = {}
    for n, c, px_, py in placed:
        out.paste(c, (px_, py)); rows[n] = [SHEET, px_, py, c.width, c.height]
    out.save(ATLAS)
    print('%s -> %dx%d' % (os.path.relpath(ATLAS, ROOT), out.width, out.height))

    s = io.open(MANIFEST, encoding='utf-8').read()
    for n in rows:
        s = re.sub(r'"%s":\[[^\]]*\],?' % re.escape(n), '', s)
    add = ''.join('"%s":%s,' % (n, json.dumps(rows[n], separators=(',', ':'))) for n, _, _, _ in placed)
    s = s.replace('"cells":{', '"cells":{' + add, 1)
    io.open(MANIFEST, 'w', encoding='utf-8', newline='').write(s)
    print('manifest.js: +%d cells' % len(rows))
    for n in rows: print('  %-22s %s' % (n, rows[n]))


if __name__ == '__main__':
    main()
