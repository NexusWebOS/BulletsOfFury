#!/usr/bin/env python3
"""flip_juggernaut_0906k.py - Juggernaut's new hull was upside down. Turn it over.

    python _BUILD_SOURCE/flip_juggernaut_0906k.py            # proof only
    python _BUILD_SOURCE/flip_juggernaut_0906k.py --write

Mike, 0906: "Is juggernauts ship facing vertically north or south I cant see it?" ... "yeah its
upside down, flip his shp graphic vertically now."

He is right. Rendered at 3x: the two orange engine nozzles sit at the TOP of the fuselage, the four
wing cannons point DOWN, and the heavy armoured prow wedge is at the BOTTOM. That is a ship flying
south in a game where the player flies north.

⚠ AND MY OWN CHECK COULD NOT HAVE CAUGHT IT, WHICH IS THE POINT WORTH KEEPING. 0906h picked this
hull partly on **mirror-LR IoU 1.000** - and that metric is completely blind to vertical facing,
because a sprite rotated 180 degrees has exactly the same left-right symmetry as the original. I
measured the one axis the defect was not on and reported it as clean. Bilateral symmetry answers
"is this a tidy top-down?", never "which way is it pointing."

⚠ A GLOW-POSITION TEST WAS TRIED AS A REPLACEMENT AND IS NOT TRUSTWORTHY EITHER. Scoring "bright
saturated pixels above or below the ink centroid" across the fleet flagged juggernaut correctly but
ALSO flagged maverick and yuri, whose ships are fine - it catches a bright canopy as readily as an
exhaust. It is recorded here as a WEAK hint, not as the check. The reliable test for facing is a
human looking at the hull at size, which is how this was actually found.

⚠ THE FLIP IS IN PLACE, SO THE RECTS DO NOT MOVE - BUT `offY` MUST STILL BE RECOMPUTED. A ship row
is [x, y, w, h, offX, offY, canvasW, canvasH] and the cell is built at canvas size with the trim
blitted at (offX, offY). Flipping the trimmed pixels without flipping that offset would hold the
hull at the old vertical position inside its canvas - the art turns over and the ship jumps up or
down the screen by however far it sat off centre. New offset is canvasH - offY - h.
"""
import os, re, sys, json, shutil, subprocess
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ATLAS = os.path.join(ROOT, 'assets/game/atlas/bof_player_ships_barrel_rolls.png')
MANIFEST = os.path.join(ROOT, 'assets/manifest.js')
PILOT = 'juggernaut'


def main():
    write = '--write' in sys.argv
    js = subprocess.run(['node', '-e',
        "global.window=global;eval(require('fs').readFileSync('assets/manifest.js','utf8'));"
        "const o={};for(const k in BOFX.ships)"
        "if(k==='ship_" + PILOT + "'||k.indexOf('ship_" + PILOT + "_')===0)o[k]=BOFX.ships[k];"
        "process.stdout.write(JSON.stringify(o));"], capture_output=True, cwd=ROOT)
    rows = json.loads(js.stdout.decode())
    A = Image.open(ATLAS).convert('RGBA')
    print('%d %s frames, atlas %dx%d' % (len(rows), PILOT, A.width, A.height))

    before = None
    src = open(MANIFEST, encoding='utf-8').read()
    for k, r in sorted(rows.items()):
        x, y, w, h, ox, oy, cw, ch = r
        cell = A.crop((x, y, x + w, y + h))
        if k == 'ship_' + PILOT:
            before = cell.copy()
        A.paste(cell.transpose(Image.FLIP_TOP_BOTTOM), (x, y))
        noy = ch - oy - h                     # the offset turns over with the pixels
        row = '"%s":[%d,%d,%d,%d,%d,%d,%d,%d]' % (k, x, y, w, h, ox, noy, cw, ch)
        pat = re.compile(r'"' + re.escape(k) + r'":\[[^\]]*\]')
        if not pat.search(src):
            print('  %s missing from the manifest - refusing' % k); return 1
        src = pat.sub(row, src, count=1)
    print('flipped %d frames in place; offY recomputed on every row (rects unmoved)' % len(rows))

    after = A.crop((rows['ship_' + PILOT][0], rows['ship_' + PILOT][1],
                    rows['ship_' + PILOT][0] + rows['ship_' + PILOT][2],
                    rows['ship_' + PILOT][1] + rows['ship_' + PILOT][3]))
    from PIL import ImageDraw, ImageFont
    try:
        F = ImageFont.truetype('C:/Windows/Fonts/consolab.ttf', 16)
    except Exception:
        F = ImageFont.load_default()
    T = 340
    proof = Image.new('RGB', (T * 2, T + 24), (22, 22, 28))
    d = ImageDraw.Draw(proof)
    for i, (lbl, im) in enumerate((('BEFORE (flying south)', before), ('AFTER (flying north)', after))):
        bb = im.getbbox(); c = im.crop(bb) if bb else im
        s = min((T - 14) / c.width, (T - 14) / c.height)
        t = c.resize((max(1, int(c.width * s)), max(1, int(c.height * s))), Image.LANCZOS)
        proof.paste(t, (i * T + (T - t.width) // 2, (T - t.height) // 2), t)
        d.text((i * T + 5, T + 5), lbl, font=F, fill=(240, 240, 250))
    proof.save(os.path.join(ROOT, 'docs/JUGGERNAUT_FLIP_0906K.png'))
    print('wrote docs/JUGGERNAUT_FLIP_0906K.png')

    if not write:
        print('DRY RUN - neither the atlas nor the manifest was touched.')
        return 0
    for f in (ATLAS, MANIFEST):
        bak = f + '.0906k.bak'
        if not os.path.exists(bak):
            shutil.copy2(f, bak)
    A.save(ATLAS)
    open(MANIFEST, 'w', encoding='utf-8', newline='\n').write(src)
    print('wrote the atlas and the manifest together')
    return 0


if __name__ == '__main__':
    sys.exit(main())
