#!/usr/bin/env python3
"""fix_yuri_rects_0906k.py - Yuri's ship rects straddle a strip seam and carry a neighbour's tail.

    python _BUILD_SOURCE/fix_yuri_rects_0906k.py            # proof only
    python _BUILD_SOURCE/fix_yuri_rects_0906k.py --write

Mike, 0906, with a screenshot of the roster thumbnail: "fix yuri's ship graphic here as shown."

WHAT IS ACTUALLY WRONG. Rendered at 3x, `ship_yuri` is not one aircraft: it is the ENGINE END of
the frame above, a 3px separator line, and then Yuri's real hull. Measured by counting contiguous
inked rows inside each declared rect, **19 of his 25 frames carry a second fragment** - every one of
them declared at y=2180 with h=219, which spans a row boundary in the appended strip. The six that
are clean are the ones that happen to sit on rows of their own.

⚠ THIS IS A PRE-EXISTING DEFECT FROM THE 0906b ROTSHEET IMPORT, NOT FROM THE 0906h/i/j work. His
ship was replaced in 0906b and the slicer wrote one height for every frame instead of each frame's
own. It has been shipping since then and nobody caught it, because at the 60px the game draws a
hull the junk reads as "some extra red bits" rather than as a second aircraft. Mike caught it on
the pilot-select ROSTER, where the thumbnail is small but the whole cell is visible.

⚠ AND THE FIX IS PER FRAME, NOT ONE OFFSET FOR ALL OF THEM. The fragment is ABOVE the ship on the
hull frames (runs 0-51 junk, 57-218 ship) and BELOW it on the barrel-roll frames (0-161 ship,
185-218 junk). A single "shift everything down by 57" would have repaired nine frames and destroyed
eight. Each rect is re-derived from its own largest contiguous ink run.

⚠ `offY` MOVES WITH `y`, OR THE SHIP JUMPS ON SCREEN. The row is [x,y,w,h,offX,offY,canvasW,canvasH]
and the cell is built at canvas size with the trim blitted at (offX,offY). Trimming rows off the TOP
of the source means the same pixels now start lower in the atlas, so the offset has to grow by
exactly what was removed to leave the hull where it was in its canvas.
"""
import os, re, sys, json, shutil, subprocess
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ATLAS = os.path.join(ROOT, 'assets/game/atlas/bof_player_ships_barrel_rolls.png')
MANIFEST = os.path.join(ROOT, 'assets/manifest.js')


def runs_of_ink(cell):
    px = cell.load()
    w, h = cell.size
    rows = [any(px[x, y][3] > 16 for x in range(w)) for y in range(h)]
    out, s = [], None
    for i, v in enumerate(rows):
        if v and s is None:
            s = i
        if not v and s is not None:
            out.append((s, i - 1)); s = None
    if s is not None:
        out.append((s, h - 1))
    return out


def main():
    write = '--write' in sys.argv
    js = subprocess.run(['node', '-e',
        "global.window=global;eval(require('fs').readFileSync('assets/manifest.js','utf8'));"
        "const o={};for(const k in BOFX.ships)if(/^ship_yuri(_|$)/.test(k))o[k]=BOFX.ships[k];"
        "process.stdout.write(JSON.stringify(o));"], capture_output=True, cwd=ROOT)
    R = json.loads(js.stdout.decode())
    A = Image.open(ATLAS).convert('RGBA')
    src = open(MANIFEST, encoding='utf-8').read()

    print('%-18s %-22s %-22s %s' % ('key', 'was', 'now', 'note'))
    print('-' * 78)
    fixed = 0
    shots = {}
    for k in sorted(R):
        x, y, w, h, ox, oy, cw, ch = R[k]
        cell = A.crop((x, y, x + w, y + h))
        rr = runs_of_ink(cell)
        if len(rr) <= 1:
            print('%-18s %-22s %-22s already clean' % (k, str([x, y, w, h]), '-'))
            continue
        # the ship is the LARGEST run; the others are a neighbour's tail and the separator line
        best = max(rr, key=lambda t: t[1] - t[0])
        top, bot = best
        ny, nh, noy = y + top, bot - top + 1, oy + top
        row = '"%s":[%d,%d,%d,%d,%d,%d,%d,%d]' % (k, x, ny, w, nh, ox, noy, cw, ch)
        pat = re.compile(r'"' + re.escape(k) + r'":\[[^\]]*\]')
        if not pat.search(src):
            print('  %s missing from the manifest - refusing' % k); return 1
        src = pat.sub(row, src, count=1)
        dropped = sum((b - a + 1) for a, b in rr if (a, b) != best)
        print('%-18s %-22s %-22s dropped %d rows in %d fragment(s)'
              % (k, str([x, y, w, h]), str([x, ny, w, nh]), dropped, len(rr) - 1))
        fixed += 1
        if k in ('ship_yuri', 'ship_yuri_br0'):
            shots[k] = (cell.copy(), A.crop((x, ny, x + w, ny + nh)))
    print()
    print('%d of %d frames repaired' % (fixed, len(R)))

    if shots:
        from PIL import ImageDraw, ImageFont
        try:
            F = ImageFont.truetype('C:/Windows/Fonts/consolab.ttf', 15)
        except Exception:
            F = ImageFont.load_default()
        T = 300
        items = []
        for k, (b, a) in shots.items():
            items.append((k + ' BEFORE', b)); items.append((k + ' AFTER', a))
        proof = Image.new('RGB', (T * len(items), T + 22), (22, 22, 28))
        d = ImageDraw.Draw(proof)
        for i, (lbl, im) in enumerate(items):
            bb = im.getbbox(); c = im.crop(bb) if bb else im
            s = min((T - 12) / c.width, (T - 12) / c.height)
            t = c.resize((max(1, int(c.width * s)), max(1, int(c.height * s))), Image.LANCZOS)
            proof.paste(t, (i * T + (T - t.width) // 2, (T - t.height) // 2), t)
            d.text((i * T + 4, T + 4), lbl, font=F, fill=(240, 240, 250))
        proof.save(os.path.join(ROOT, 'docs/YURI_RECTS_0906K.png'))
        print('wrote docs/YURI_RECTS_0906K.png')

    if not write:
        print('DRY RUN - the manifest was not touched.')
        return 0
    bak = MANIFEST + '.0906k2.bak'
    if not os.path.exists(bak):
        shutil.copy2(MANIFEST, bak)
    open(MANIFEST, 'w', encoding='utf-8', newline='\n').write(src)
    print('wrote the manifest (atlas pixels untouched - only the rects were wrong)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
