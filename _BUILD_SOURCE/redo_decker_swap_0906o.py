#!/usr/bin/env python3
"""redo_decker_swap_0906o.py - redo Decker's yellow/black swap without destroying his shading.

    python _BUILD_SOURCE/redo_decker_swap_0906o.py            # proof only
    python _BUILD_SOURCE/redo_decker_swap_0906o.py --write

Mike, 0906: "and deckers also looks bad."

⚠ HE IS RIGHT AND IT IS MY 0906h RECOLOUR, NOT HIS SHIP. Measured on the hull frame:
7,666 colours before the swap, 3,707 after - the recolour DESTROYED HALF HIS PALETTE - and
saturation went 0.11 to 0.60, so the result is simultaneously flatter and noisier. Rendered at 3x
it is visibly speckled, and the panel structure that reads clearly on the original is mush.

⚠ THE CAUSE IS THE EXACT THING THE LUMINANCE RULE EXISTS TO PREVENT, AND I OVERRODE IT ON PURPOSE.
0906h mapped his black band (value 0.00..0.25) onto the gold band's range (0.02..0.95) - a 3.7x
STRETCH of a narrow band across a wide one. Every one-step dither in the near-black hull became a
four-step jump, which is what the speckle is, and the quantisation is what halved the colour count.
The argument for breaking the rule was sound (black and yellow must trade brightness or the swap is
invisible); the IMPLEMENTATION was not. A range exchange is not the only way to trade brightness.

WHAT THIS DOES INSTEAD: a gentle gain, not a range remap. The grey takes the gold hue at its own
value multiplied by 1.7 with a small floor, so the hull lifts into gold while the SPACING between
neighbouring values is nearly preserved - dither stays dither instead of becoming banding. The gold
accents drop to 0.22 of their value. Mike's brief still holds: the ship reads yellow-dominant with
black where the yellow used to be.

⚠ AND IT RE-RUNS FROM THE PRE-SWAP BACKUP, NOT FROM THE CURRENT ATLAS. Recolouring the already
recoloured plate would compound the damage - the lost palette cannot be recovered by a second pass
over the lossy result. `bof_player_ships_barrel_rolls.png.0906g.bak` is the plate as it stood before
0906h, and Decker's rects have not moved since (the appends that grew the atlas were all below him),
so the same rectangles read the original pixels.
"""
import os, sys, json, shutil, subprocess, colorsys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ATLAS = os.path.join(ROOT, 'assets/game/atlas/bof_player_ships_barrel_rolls.png')
BACKUP = ATLAS + '.0906g.bak'
GOLD = 47.0 / 360.0          # the hue his own accents already used - his colour, not a new one


def rule(h, s, v):
    d = h * 360
    if s < 0.20:                                  # the gunmetal hull -> GOLD
        return GOLD, 0.62 + 0.20 * min(1.0, v / 0.30), min(1.0, 0.16 + v * 1.7)
    if 30 <= d <= 62 and s >= 0.25:               # the gold accents -> dark
        return h, s * 0.12, v * 0.22
    return h, s, v


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


def colours(im):
    px = im.load(); s = set()
    for y in range(im.height):
        for x in range(im.width):
            if px[x, y][3] > 8:
                s.add(px[x, y][:3])
    return len(s)


def main():
    write = '--write' in sys.argv
    if not os.path.exists(BACKUP):
        print('the pre-swap backup is missing - refusing rather than compounding the damage')
        return 1
    js = subprocess.run(['node', '-e',
        "global.window=global;eval(require('fs').readFileSync('assets/manifest.js','utf8'));"
        "const o={};for(const k in BOFX.ships)"
        "if(k==='ship_decker'||k.indexOf('ship_decker_')===0)o[k]=BOFX.ships[k];"
        "process.stdout.write(JSON.stringify(o));"], capture_output=True, cwd=ROOT)
    R = json.loads(js.stdout.decode())
    A = Image.open(ATLAS).convert('RGBA')
    P = Image.open(BACKUP).convert('RGBA')
    print('%d decker frames; atlas %dx%d, backup %dx%d' % (len(R), A.width, A.height, P.width, P.height))

    shots = {}
    total = 0
    for k, r in sorted(R.items()):
        x, y, w, h = r[0], r[1], r[2], r[3]
        if x + w > P.width or y + h > P.height:
            print('  %s lies outside the backup - refusing' % k); return 1
        cell = P.crop((x, y, x + w, y + h))          # ORIGINAL pixels, not the recoloured ones
        if k == 'ship_decker':
            shots['before the 0906h swap'] = cell.copy()
            shots['0906h (the bad one)'] = A.crop((x, y, x + w, y + h)).copy()
        total += recolour(cell)
        A.paste(cell, (x, y))
        if k == 'ship_decker':
            shots['0906o (redone)'] = cell.copy()
    print('recoloured %d pixels across %d frames, sourced from the pre-swap plate' % (total, len(R)))
    for lbl, im in shots.items():
        print('   %-24s %d colours' % (lbl, colours(im)))

    from PIL import ImageDraw, ImageFont
    try:
        F = ImageFont.truetype('C:/Windows/Fonts/consolab.ttf', 15)
    except Exception:
        F = ImageFont.load_default()
    T = 300
    proof = Image.new('RGB', (T * len(shots), T + 24), (22, 22, 28))
    d = ImageDraw.Draw(proof)
    for i, (lbl, im) in enumerate(shots.items()):
        bb = im.getbbox(); c = im.crop(bb) if bb else im
        s = min((T - 14) / c.width, (T - 14) / c.height)
        t = c.resize((max(1, int(c.width * s)), max(1, int(c.height * s))), Image.LANCZOS)
        proof.paste(t, (i * T + (T - t.width) // 2, (T - t.height) // 2), t)
        d.text((i * T + 4, T + 5), lbl, font=F, fill=(240, 240, 250))
    proof.save(os.path.join(ROOT, 'docs/DECKER_REDONE_0906O.png'))
    print('wrote docs/DECKER_REDONE_0906O.png')

    if not write:
        print('DRY RUN - the atlas was not touched.')
        return 0
    bak2 = ATLAS + '.0906o.bak'
    if not os.path.exists(bak2):
        shutil.copy2(ATLAS, bak2)
    A.save(ATLAS)
    print('wrote the atlas (rects unchanged, so no manifest edit)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
