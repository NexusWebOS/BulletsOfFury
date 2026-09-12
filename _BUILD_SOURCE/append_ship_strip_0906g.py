#!/usr/bin/env python3
"""append_ship_strip_0906g.py - put a derived ship reel into the atlas and repoint its rects.

    python _BUILD_SOURCE/append_ship_strip_0906g.py juggernaut falva
    python _BUILD_SOURCE/append_ship_strip_0906g.py juggernaut falva --write

⚠ PIXELS AND MANIFEST IN ONE WRITE. CLAUDE.md records the 0903 repack landing 451 repointed cells
minutes before the sheets they pointed at were registered, and Mike was playing during the window:
every one of those keys resolved to nothing. This writes the PNG and the manifest rows in the same
run or it writes neither, and it refuses outright if it cannot do both.

⚠ AND IT APPENDS RATHER THAN PACKING OVER THE OLD ROWS. That is not tidiness - it is what made
Lizzie's B-42 recoverable as a costume in 0906g, three drops after her ship was replaced. Old rects
left alone are old art still on disk. The atlas grows by one strip; the cost is a few hundred KB
and the benefit is that every replacement stays reversible.

⚠ THE ROW FORMAT IS EIGHT NUMBERS, NOT FOUR: [x, y, w, h, offX, offY, canvasW, canvasH]. The last
two are the ORIGINAL canvas the frame was composed on, and _shipCell builds its cell at that size
and blits the trim into it at (offX, offY). Writing a four-element row would not throw - it would
give `undefined` canvas dimensions and a zero-size cell, i.e. an invisible ship.
"""
import os, re, sys, json, shutil, subprocess
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ATLAS = os.path.join(ROOT, 'assets/game/atlas/bof_player_ships_barrel_rolls.png')
MANIFEST = os.path.join(ROOT, 'assets/manifest.js')
DERIVED = os.path.join(ROOT, 'assets/game/ships_derived')
SUF = ['', '_nf', '_l', '_r', '_pv0', '_pv1', '_pv2', '_pv3', '_pv4'] + ['_br%d' % i for i in range(8)]
PAD = 2


def current_rows(pilots):
    js = subprocess.run(['node', '-e',
        "global.window=global;eval(require('fs').readFileSync('assets/manifest.js','utf8'));"
        "process.stdout.write(JSON.stringify(BOFX.ships));"], capture_output=True, cwd=ROOT)
    return json.loads(js.stdout.decode())


def main():
    pilots = [a for a in sys.argv[1:] if not a.startswith('--')]
    write = '--write' in sys.argv
    if not pilots:
        print(__doc__); return 2

    ships = current_rows(pilots)
    A = Image.open(ATLAS).convert('RGBA')
    print('atlas %dx%d' % A.size)

    # keep each pilot's ORIGINAL canvas size, so the ship keeps the on-screen scale it had
    plan = []
    for p in pilots:
        base = ships.get('ship_' + p)
        if not base:
            print('  %s has no existing rows - refusing' % p); return 1
        cw, ch = base[6], base[7]
        # ⚠ AN OVERRIDE WINS, BECAUSE THE BASE ROW IS NOT ALWAYS THE RIGHT CANVAS. Axel's base
        # frame sits on 90x120 while his other sixteen use 203x271, so taking the canvas from the
        # base row would have packed a whole new reel into the small one and drawn him at a third
        # of the fleet's size. fit_new_hulls writes the intended canvas beside the hero plate.
        ov = os.path.join(ROOT, '_BUILD_SOURCE/sc_hero_0906x/%s_canvas.json' % p)
        if os.path.exists(ov):
            j = json.load(open(ov))
            cw, ch = j['canvasW'], j['canvasH']
            print('  %s: canvas override %dx%d (base row says %dx%d)' % (p, cw, ch, base[6], base[7]))
        for s in SUF:
            f = os.path.join(DERIVED, p, 'ship_%s%s.png' % (p, s))
            if not os.path.exists(f):
                print('  MISSING %s - refusing' % f); return 1
            plan.append((p, s, f, cw, ch))
    print('%d frames to append across %d pilots' % (len(plan), len(pilots)))

    # lay the strip out as rows that fit the atlas width
    imgs = []
    for p, s, f, cw, ch in plan:
        im = Image.open(f).convert('RGBA')
        bb = im.getbbox()
        trim = im.crop(bb) if bb else im
        offx, offy = (bb[0], bb[1]) if bb else (0, 0)
        # the derived frame is drawn on the HERO plate's canvas; rescale so its canvas matches the
        # pilot's authored canvas, or the ship changes size the moment the new rows go live
        # ⚠ AND A FRAME THAT ALREADY FITS IS NOT RESCALED. The hero plate was fitted to this
        # canvas on purpose (ink height = 0.79 of it, the fleet's own ratio); scaling it again to
        # fill the canvas would undo that and draw the ship 15% oversize.
        s2 = 1.0 if (im.width <= cw and im.height <= ch) else min(cw / im.width, ch / im.height)
        trim = trim.resize((max(1, round(trim.width * s2)), max(1, round(trim.height * s2))), Image.LANCZOS)
        offx = int(round(offx * s2 + (cw - im.width * s2) / 2))
        offy = int(round(offy * s2 + (ch - im.height * s2) / 2))
        imgs.append((p, s, trim, offx, offy, cw, ch))

    W = A.width
    x, y, rowh, placed = PAD, A.height + PAD, 0, {}
    for p, s, trim, offx, offy, cw, ch in imgs:
        if x + trim.width + PAD > W:
            x = PAD; y += rowh + PAD; rowh = 0
        placed['ship_%s%s' % (p, s)] = (x, y, trim.width, trim.height, offx, offy, cw, ch, trim)
        x += trim.width + PAD
        rowh = max(rowh, trim.height)
    newH = y + rowh + PAD
    print('strip occupies y %d..%d (atlas grows %d -> %d)' % (A.height, newH, A.height, newH))

    B = Image.new('RGBA', (W, newH), (0, 0, 0, 0))
    B.paste(A, (0, 0))
    for k, v in placed.items():
        B.alpha_composite(v[8], (v[0], v[1]))

    src = open(MANIFEST, encoding='utf-8').read()
    n = 0
    for k, v in placed.items():
        row = '"%s":[%s]' % (k, ','.join(str(int(t)) for t in v[:8]))
        pat = re.compile(r'"' + re.escape(k) + r'":\[[^\]]*\]')
        if not pat.search(src):
            print('  %s not in the manifest - refusing' % k); return 1
        src = pat.sub(row, src, count=1)
        n += 1
    print('%d manifest rows repointed' % n)

    if not write:
        print('DRY RUN - neither the atlas nor the manifest was touched.')
        return 0
    for f in (ATLAS, MANIFEST):
        bak = f + '.0906g2.bak'
        if not os.path.exists(bak):
            shutil.copy2(f, bak)
    B.save(ATLAS)
    open(MANIFEST, 'w', encoding='utf-8', newline='\n').write(src)
    print('wrote the atlas and the manifest together')
    return 0


if __name__ == '__main__':
    sys.exit(main())
