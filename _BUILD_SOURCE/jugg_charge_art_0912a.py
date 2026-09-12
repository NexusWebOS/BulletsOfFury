#!/usr/bin/env python3
"""
jugg_charge_art_0912a.py - THE WRECKING BALLS AND THE CHARGE RINGS.

    python3 _BUILD_SOURCE/jugg_charge_art_0912a.py

Cuts two SpriteCook 2x2 grids into one atlas and registers eight cells:

    jwb_ball  jwb_ball_hot  jwb_link  jwb_burst      jchg_0  jchg_1  jchg_2  jchg_3

⚠ BOTH GRIDS COME OFF `pixel_url`, AND THE SECOND ONE LEARNED THAT THE HARD WAY. `pixel_url`
carries real alpha but is downscaled (the balls came back 200x200, the rings 90x90); `raw_url`
keeps the full 1K render. The first cut took the RINGS off raw_url on the theory that they are
drawn with globalCompositeOperation 'lighter', where black contributes nothing, so luminance could
stand in for alpha at four times the resolution.

That theory was wrong and it was visible the moment the rings were rendered in-engine: raw_url does
not draw transparency as BLACK, it draws it as a CHECKERBOARD, so the luminance key turned the
checker into a half-opaque grey square and Juggernaut charged inside a floating chessboard. The
photograph is the whole argument for the CLAUDE.md rule - the cells looked perfect on a
transparency-checkered contact sheet, because a checkerboard on a checkerboard is invisible.

So the rings are cut from pixel_url too and upscaled. A 45px cell taken to 180 is soft, and on an
additive glow that is worth far more than four times the detail with a chessboard in it.

⚠ SLICED BY CELL, NOT BY CONNECTED ALPHA. The burst throws debris chunks clear of its own body
and the rings are hollow - an alpha-island slicer would have returned about thirty fragments and
no whole sprite. The prompt asked for a 2x2 grid with wide gaps, so the grid is the slicer; each
quadrant is then trimmed to its own ink.
"""
import os, sys, io, json, re
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
SRC = os.path.join(os.environ.get('TEMP', '/tmp'), 'sc')
OUT_PNG = os.path.join(ROOT, 'assets', 'game', 'atlas', 'jugg_charge_wreck.png')
MANIFEST = os.path.join(ROOT, 'assets', 'manifest.js')
SHEET = 'jugg_charge_wreck'


def quads(im, inset=0.055):
    """⚠ INSET BEFORE CUTTING. The generator draws faint separator lines along its own grid, and a
       quadrant taken edge-to-edge keeps them - the first cut shipped a stray black hairline down
       the side of the ball, the link and the burst, visible the moment the cells were laid on a
       grey card. The prompt asked for "wide empty gaps", so a 5.5% inset costs no artwork and
       takes the ruling with it."""
    w, h = im.size
    hw, hh = w // 2, h // 2
    mx, my = int(hw * inset), int(hh * inset)
    return [im.crop((mx, my, hw - mx, hh - my)),
            im.crop((hw + mx, my, w - mx, hh - my)),
            im.crop((mx, hh + my, hw - mx, h - my)),
            im.crop((hw + mx, hh + my, w - mx, h - my))]


def trim(im, pad=0):
    bb = im.getbbox()
    if not bb:
        return im
    x0, y0, x1, y1 = bb
    x0 = max(0, x0 - pad); y0 = max(0, y0 - pad)
    x1 = min(im.width, x1 + pad); y1 = min(im.height, y1 + pad)
    return im.crop((x0, y0, x1, y1))


def clean_edge(im, floor=10):
    """Drop the smart-crop's faint halo so an upscaled ring has no grey ghost around it."""
    px = im.load()
    for j in range(im.height):
        for i in range(im.width):
            r, g, b, a = px[i, j]
            if a <= floor:
                px[i, j] = (0, 0, 0, 0)
    return im


def main():
    wreck = Image.open(os.path.join(SRC, 'wreck_px.png')).convert('RGBA')
    chg = Image.open(os.path.join(SRC, 'chg_px.png')).convert('RGBA')

    wq = [trim(q) for q in quads(wreck)]
    cq = [trim(clean_edge(q)) for q in quads(chg)]
    # 4x, because the ring is drawn at 54..120px and a 40px cell would be mush at the top of that
    cq = [q.resize((q.width * 4, q.height * 4), Image.LANCZOS) for q in cq]

    cells = [('jwb_ball', wq[0]), ('jwb_ball_hot', wq[1]), ('jwb_link', wq[2]), ('jwb_burst', wq[3]),
             ('jchg_0', cq[0]), ('jchg_1', cq[1]), ('jchg_2', cq[2]), ('jchg_3', cq[3])]

    PAD = 2
    W = 1024
    x = y = PAD
    rowh = 0
    placed = []
    for name, im in cells:
        if x + im.width + PAD > W:
            x = PAD; y += rowh + PAD; rowh = 0
        placed.append((name, im, x, y))
        x += im.width + PAD
        rowh = max(rowh, im.height)
    H = y + rowh + PAD

    sheet = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    rows = {}
    for name, im, px_, py in placed:
        sheet.paste(im, (px_, py))
        rows[name] = [SHEET, px_, py, im.width, im.height]
    sheet.save(OUT_PNG)
    print('%s  %dx%d' % (os.path.relpath(OUT_PNG, ROOT), W, H))
    for n in rows:
        print('  %-14s %s' % (n, rows[n]))

    s = io.open(MANIFEST, encoding='utf-8').read()
    # re-runnable: strip any rows a previous pass left before writing the new ones, so re-cutting
    # the art is one command rather than a git checkout first
    for n in rows:
        s = re.sub(r'"%s":\[[^\]]*\],?' % re.escape(n), '', s)
    s = s.replace('"nca_%s":"assets/game/atlas/%s.png",' % (SHEET, SHEET), '')
    a = '"img":{'
    assert s.count(a) == 1
    s = s.replace(a, a + '"nca_%s":"assets/game/atlas/%s.png",' % (SHEET, SHEET), 1)
    a = '"cells":{'
    assert s.count(a) == 1, 'cells block appears %d times' % s.count(a)
    add = ''.join('"%s":%s,' % (n, json.dumps(rows[n], separators=(',', ':'))) for n, _, _, _ in placed)
    s = s.replace(a, a + add, 1)
    io.open(MANIFEST, 'w', encoding='utf-8', newline='').write(s)
    print('\nmanifest.js: +1 img, +%d cells' % len(rows))


if __name__ == '__main__':
    main()
