#!/usr/bin/env python3
"""
bossbar_tab_0912e.py - THE BOSS BAR GETS A CONNECTED NAME TAB, AND A SHIELD BAR.

    python3 _BUILD_SOURCE/bossbar_tab_0912e.py [--check]

Mike (0912): "we need our hud bars for the bosses regenerated but with BOSS embed into the center
above the above but within a tab connnected to the bar. you may use the same designs, same fills
just regenerated bars. Also, we will need an additional SHIELD hud bar for the bosses too with
forcefield/shield like fills too."

⚠ THE TAB IS BUILT FROM THE BAR'S OWN PIXELS, NOT DRAWN FRESH. "you may use the same designs" is
easiest to honour literally: the frame's rails ARE the tab's rails. Read down the frame body at
x=350 and it is three bands - a lit rail (rows 1..6, gold 246,227,100 into orange 169,39,1), a
near-black well (rows 7..23), and the mirrored bottom rail (rows 24..31). The tab reuses that exact
rail strip for its top edge, the same strip rotated for its sides, and the same well for its
interior, so it cannot drift from the bar it sits on.

⚠ AND IT IS A SEPARATE CELL, NOT A TALLER FRAME. BMBAR.mini/boss carry interior offsets measured
off each frame's own pixels in 0910c - the drop where Mike asked for the fill to be "centered inside
the black properly". Growing the frame plate would move every one of those numbers and put that
seating back at risk for nothing. The tab is its own plate drawn flush against the bar's top edge,
so the two read as one piece and the approved fill geometry is untouched.

⚠ THE WORD IS NOT BAKED IN. The plate is the socket; the game letters it at draw time with the
authored stage face - the same rule 0809r/0810z record for the attract cards and the aintro panels.
A baked "BOSS" would need a new plate the day anything about that lettering changes, and could not
say MINI BOSS or SHIELD from the same art.

The shield FILLS come from a generated forcefield texture, tiled into the bar's own fill geometry
(578x13) and given the same top highlight / bottom shade the authored fills carry, so a shield fill
seats in the well exactly like an HP fill.
"""
import os, sys, io, json, re, argparse
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
ATLAS = os.path.join(ROOT, 'assets', 'game', 'atlas', 'ui_bossbar.png')
MANIFEST = os.path.join(ROOT, 'assets', 'manifest.js')
SRC = os.path.join(os.environ.get('TEMP', '/tmp'), 'sc')
SHEET = 'ui_bossbar'

FRAME_BOSS = (2, 39, 700, 33)
FRAME_MINI = (2, 2, 700, 33)
FILL_W, FILL_H = 578, 13
# ⚠ SIZED BACKWARDS FROM THE LETTERING, not picked. The bar draws at VW*0.72 on a 480 field, so the
# frame's 700px cell renders at scale ~0.494. A tab of 21px would render 10px tall and leave about
# 8px for the word - and 0912b measured that BOTH stage faces lose their counters below 11px. 30px
# renders ~15 and carries an 11px word with air around it.
TAB_W, TAB_H = 204, 30


def frame(im, r):
    return im.crop((r[0], r[1], r[0] + r[2], r[1] + r[3]))


def build_tab(fr, flip_rail=False):
    """The tab, made of the frame's own three bands. Bottom edge left open so it merges with the
       bar's top rail and the two read as one connected piece."""
    RAIL_TOP, RAIL_BOT = 1, 7        # the lit rail band, measured off the row profile
    rail = fr.crop((300, RAIL_TOP, 360, RAIL_BOT))          # 60x6 of clean rail
    well = fr.crop((300, 12, 360, 20))                       # 60x8 of the near-black well
    rh = rail.height

    tab = Image.new('RGBA', (TAB_W, TAB_H), (0, 0, 0, 0))
    # interior first
    tab.paste(well.resize((TAB_W, TAB_H), Image.NEAREST), (0, 0))
    # top rail, full width
    tab.paste(rail.resize((TAB_W, rh), Image.NEAREST), (0, 0))
    # side rails: the same band stood on end, so the tab is framed in the bar's own trim
    side = rail.resize((TAB_H, rh), Image.NEAREST).rotate(90, expand=True)   # rh wide, TAB_H tall
    tab.paste(side, (0, 0))
    tab.paste(side.transpose(Image.FLIP_LEFT_RIGHT), (TAB_W - rh, 0))
    # re-lay the top rail over the corners so the miter reads clean
    tab.paste(rail.resize((TAB_W, rh), Image.NEAREST), (0, 0))
    # the bottom two rows are the frame's own dark seam, so the tab sits ON the bar rather than
    # floating above it
    seam = fr.crop((300, 0, 360, 1)).resize((TAB_W, 1), Image.NEAREST)
    tab.paste(seam, (0, TAB_H - 1))
    return tab


def shield_fills(src):
    """Tile the generated forcefield texture into the bar's own 578x13 fill geometry, with the same
       top-highlight / bottom-shade profile the authored fills carry."""
    tex = Image.open(src).convert('RGBA')
    w, h = tex.size
    quads = [tex.crop((0, 0, w // 2, h // 2)), tex.crop((w // 2, 0, w, h // 2)),
             tex.crop((0, h // 2, w // 2, h)), tex.crop((w // 2, h // 2, w, h))]
    # ⚠ THE GENERATED "FAILING SHIELD" QUADRANT IS NOT USABLE AS A BAR FILL. Rendered, it is
    # mostly black with scattered white pixels - at 13px tall that reads as television static, not
    # as a field about to collapse. The depleted state is derived from the HEX fill instead:
    # same cells, dimmed and desaturated, so a draining shield visibly loses power rather than
    # changing into a different material. Only three of the four quadrants are used. 
    quads = quads[:3]
    out = []
    for q in quads:
        # square swatch -> a long thin strip: scale to the fill height, then tile across
        s = q.resize((FILL_H * 3, FILL_H), Image.LANCZOS)
        strip = Image.new('RGBA', (FILL_W, FILL_H))
        for x in range(0, FILL_W, s.width):
            strip.paste(s, (x, 0))
        px = strip.load()
        for x in range(FILL_W):
            for y in range(FILL_H):
                r, g, b, a = px[x, y]
                if y == 0:                      # the authored fills carry a lit top row
                    k = 1.45
                elif y == 1:
                    k = 1.18
                elif y >= FILL_H - 2:           # and a shaded bottom
                    k = 0.55
                else:
                    k = 1.0
                px[x, y] = (min(255, int(r * k)), min(255, int(g * k)), min(255, int(b * k)), 255)
        out.append(strip)
    # the depleted field: the hex cells with the power taken out of them
    dim = out[0].copy(); px = dim.load()
    for x in range(FILL_W):
        for y in range(FILL_H):
            r, g, b, al = px[x, y]
            lum = (r * 299 + g * 587 + b * 114) // 1000
            px[x, y] = (int((r * .35 + lum * .65) * .52),
                        int((g * .35 + lum * .65) * .55),
                        int((b * .35 + lum * .65) * .62), al)
    out.append(dim)
    return out


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--check', action='store_true'); a = ap.parse_args()
    im = Image.open(ATLAS).convert('RGBA')
    fb, fm = frame(im, FRAME_BOSS), frame(im, FRAME_MINI)

    cells = [('bmbar_tab_boss', build_tab(fb)), ('bmbar_tab_mini', build_tab(fm))]

    tex = os.path.join(SRC, 'shield_tex.png')
    if os.path.exists(tex):
        names = ['bmbar_sfill_hex', 'bmbar_sfill_plasma', 'bmbar_sfill_over', 'bmbar_sfill_low']
        for n, f in zip(names, shield_fills(tex)):
            cells.append((n, f))
    else:
        print('!! %s not present - tabs only this pass' % tex)

    if a.check:
        H = sum(c[1].height * 3 + 10 for c in cells) + 10
        W = max(c[1].width for c in cells) * 3 + 180
        card = Image.new('RGBA', (W, H), (44, 48, 58, 255))
        from PIL import ImageDraw
        d = ImageDraw.Draw(card); y = 6
        for n, c in cells:
            card.alpha_composite(c.resize((c.width * 3, c.height * 3), Image.NEAREST), (170, y))
            d.text((6, y + c.height * 3 // 2 - 4), n, fill=(255, 210, 90, 255))
            y += c.height * 3 + 10
        p = os.path.join(os.environ.get('TEMP', '/tmp'), 'bossbar_new.png')
        card.save(p); print('--check: wrote', p)
        for n, c in cells: print('   %-20s %dx%d' % (n, c.width, c.height))
        return

    # ---- append a strip to the existing atlas; the authored rows above are untouched ----
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
    for n, c, px, py in placed:
        out.paste(c, (px, py)); rows[n] = [SHEET, px, py, c.width, c.height]
    out.save(ATLAS)
    print('%s -> %dx%d' % (os.path.relpath(ATLAS, ROOT), out.width, out.height))

    s = io.open(MANIFEST, encoding='utf-8').read()
    for n in rows:
        s = re.sub(r'"%s":\[[^\]]*\],?' % re.escape(n), '', s)
    add = ''.join('"%s":%s,' % (n, json.dumps(rows[n], separators=(',', ':'))) for n, _, _, _ in placed)
    s = s.replace('"cells":{', '"cells":{' + add, 1)
    io.open(MANIFEST, 'w', encoding='utf-8', newline='').write(s)
    print('manifest.js: +%d cells' % len(rows))
    for n in rows: print('  %-20s %s' % (n, rows[n]))


if __name__ == '__main__':
    main()
