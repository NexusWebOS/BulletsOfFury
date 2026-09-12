#!/usr/bin/env python3
"""fit_new_hulls_0906x.py - size Decker's and Axel's new plates to the fleet's proportions.

    python _BUILD_SOURCE/fit_new_hulls_0906x.py            # measure + proof
    python _BUILD_SOURCE/fit_new_hulls_0906x.py --write

Mike, 0906: "lets use v1 for decker, v2 for axel. this is perfect."

⚠ THE GAME NORMALISES A SHIP ON ITS CONTENT HEIGHT, SO THAT IS WHAT HAS TO MATCH. `drawPlayer`
blits at a fixed `SHIP_DRAW_H` against the CANVAS, and 0724cm records why: the hulls were once
scaled to a fixed WIDTH, and because their content heights are near-identical while their widths
run 143 to 222, the narrow airframes drew far taller than the wide ones - Falva came out a third
bigger than Cole. The fleet therefore sits at an ink-height / canvas-height ratio of 0.79-0.84
(the `_CF` table in game.js), and a new hull that misses that draws the wrong size no matter how
good the art is. Both plates are scaled so their INK HEIGHT lands on 0.79 of the canvas.

⚠ AND WIDTH IS ALLOWED TO FOLLOW THE DESIGN, BY MOVING THE CANVAS. Drawn width is
`SHIP_DRAW_H * canvasW/canvasH`, so a wider aircraft needs a wider canvas rather than a squeezed
plate - squeezing is how you get a ship that is the right size and the wrong shape. Axel's new
hull is squarer than his old one, so his canvas widens from 203 to 236 and he draws ~15% wider.
That is the design Mike picked, rendered honestly.

⚠ AXEL'S BASE FRAME HAS A DIFFERENT CANVAS FROM HIS OTHER SIXTEEN - 90x120 against 203x271 - and
the append tool takes its canvas from the BASE row, so it would have packed the new reel into the
small one and drawn him at a third of the fleet's size. Pre-existing, and it is fixed here by
giving every frame in the reel one canvas.
"""
import os, sys, json, subprocess
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, '_BUILD_SOURCE/sc_out_0906w')
OUT = os.path.join(ROOT, '_BUILD_SOURCE/sc_hero_0906x')
ATLAS = os.path.join(ROOT, 'assets/game/atlas/bof_player_ships_barrel_rolls.png')

INK_F = 0.79                      # ink height as a share of canvas height - the fleet's own ratio
PICK = {'decker': ('decker_v1.png', 203, 276),     # pilot -> (plate, canvasW hint, canvasH)
        'axel':   ('axel_v2.png',   236, 271)}


def flat(rgba, bg=(22, 22, 28)):
    """⚠ COMPOSITE, never .convert('RGB') - that discards alpha and paints the old key back (0906v)"""
    o = Image.new('RGB', rgba.size, bg)
    o.paste(rgba, (0, 0), rgba)
    return o


def main():
    write = '--write' in sys.argv
    rows = json.loads(subprocess.run(['node', '-e',
        "global.window=global;eval(require('fs').readFileSync('assets/manifest.js','utf8'));"
        "process.stdout.write(JSON.stringify(BOFX.ships));"], capture_output=True, cwd=ROOT).stdout.decode())
    A = Image.open(ATLAS).convert('RGBA')
    os.makedirs(OUT, exist_ok=True)
    shots = []
    for p, (fn, cw_hint, ch) in sorted(PICK.items()):
        old = rows['ship_' + p]
        oc = A.crop((old[0], old[1], old[0] + old[2], old[1] + old[3]))
        ob = oc.getbbox()
        print('%s  OLD canvas %dx%d  ink %dx%d  (ink/canvas h = %.3f)'
              % (p, old[6], old[7], ob[2] - ob[0], ob[3] - ob[1], (ob[3] - ob[1]) / float(old[7])))

        im = Image.open(os.path.join(SRC, fn)).convert('RGBA')
        b = im.getbbox()
        im = im.crop(b)
        target_h = int(round(ch * INK_F))
        sc = target_h / float(im.height)
        nw, nh = max(1, int(round(im.width * sc))), target_h
        im = im.resize((nw, nh), Image.LANCZOS)
        cw = max(cw_hint, nw + 24)                       # keep a margin like the rest of the fleet
        print('   NEW plate %dx%d -> ink %dx%d in a %dx%d canvas  (ink/canvas h = %.3f)'
              % (Image.open(os.path.join(SRC, fn)).width, Image.open(os.path.join(SRC, fn)).height,
                 nw, nh, cw, ch, nh / float(ch)))
        print('   drawn on screen: %.1f x %.1f px  (was %.1f x %.1f)'
              % (60.0 * cw / ch * nw / cw, 60.0 * nh / ch,
                 60.0 * old[6] / old[7] * (ob[2] - ob[0]) / old[6], 60.0 * (ob[3] - ob[1]) / old[7]))
        shots.append((p, oc.crop(ob), im, cw, ch, old[7]))
        if write:
            im.save(os.path.join(OUT, '%s_hero.png' % p))
            json.dump({'canvasW': cw, 'canvasH': ch},
                      open(os.path.join(OUT, '%s_canvas.json' % p), 'w'))

    try:
        F = ImageFont.truetype('C:/Windows/Fonts/consolab.ttf', 15)
    except Exception:
        F = ImageFont.load_default()
    T = 260
    proof = Image.new('RGB', (T * 4, T + 26), (18, 18, 24))
    d = ImageDraw.Draw(proof)
    col = 0
    for (p, oldi, newi, cw, ch, old_ch) in shots:
        # ⚠ EACH SHIP IS SCALED BY ITS OWN CANVAS. Using the new canvas height for the old plate
        # too drew Axel at half size and made the comparison meaningless - his old canvas is 120
        # tall against the new 271. A proof that mis-scales one side is not a comparison.
        for lbl, im, cch in (('%s OLD' % p, oldi, old_ch), ('%s NEW' % p, newi, ch)):
            dh = 60.0 * im.height / cch
            dw = 60.0 * im.width / cch
            t = im.resize((max(1, int(dw * 3)), max(1, int(dh * 3))), Image.NEAREST)
            proof.paste(flat(t), (col * T + (T - t.width) // 2, 26 + (T - 26 - t.height) // 2))
            d.text((col * T + 6, 4), lbl, font=F, fill=(238, 238, 248))
            col += 1
    proof.save(os.path.join(ROOT, 'docs/NEW_HULL_FIT_0906X.png'))
    print('wrote docs/NEW_HULL_FIT_0906X.png  (both drawn at the size the game uses, then 3x)')
    if not write:
        print('DRY RUN - nothing written.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
