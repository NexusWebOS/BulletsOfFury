#!/usr/bin/env python3
"""recolour_ships_0906g.py - Decker's yellow/black exchange and Maverick's move off Cole's green.

    python _BUILD_SOURCE/recolour_ships_0906g.py            # measure + proof, writes nothing
    python _BUILD_SOURCE/recolour_ships_0906g.py --write    # edits the ship atlas in place

Mike, 0906:
  DECKER    "palette swap decker's vehicle to be more yellow than black, and where the yellow
             was becomes black instead."
  MAVERICK  "palette swap ... his ship's green colors to a more teal color so were not confused
             with him or Cole."

MEASURED FIRST, ON THE HULL FRAME. Decker is 47% grey at v<=0.25 (the "black") and 18.4% in hue
30-60 (the yellow). Maverick is 23.4% in 120-150 and 17.8% in 90-120 - and COLE measures 13.0% in
90-120, which is the collision Mike is pointing at. Teal at 177 clears Cole's band entirely.

⚠ THIS IS THE ONE PLACE THE LUMINANCE RULE IS DELIBERATELY BROKEN, AND ONLY FOR DECKER.
"Palette/luminance swaps, not overlays" exists because a flat tint destroys authored shading - it
is why the font's drop shadow got flooded and E became B. But Mike asked for black and yellow to
TRADE PLACES, and they sit at opposite ends of the value range: preserving luminance would give a
hull that is still dark everywhere the black was, i.e. the swap would be invisible. So the two
bands exchange their value RANGES rather than being flat-filled - each pixel keeps its position
within its own band, so every panel line and bevel survives, and the bands swap brightness.
Maverick's rule is a pure hue rotation and touches neither S nor V.

⚠ AND IT IS ONE PASS OVER THE ORIGINAL PIXEL. Converting black->yellow and then yellow->black in
two passes would undo the first with the second, and the ship would come out unchanged - a
"nothing happened" that looks like the script not running rather than like a logic error.

⚠ THE RECTS WERE CHECKED FOR ALIASING BEFORE ANY WRITE. 42 Decker/Maverick frames, zero exact
aliases and zero partial overlaps with any other key. This repo has ~750 aliased cells and a
shared rect would have silently recoloured somebody else's ship.
"""
import os, sys, json, shutil, subprocess, colorsys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ATLAS = os.path.join(ROOT, 'assets/game/atlas/bof_player_ships_barrel_rolls.png')

TEAL = 177.0 / 360.0          # clear of Cole's 90-120 band by a wide margin
DECKER_GOLD = 47.0 / 360.0    # the hue his own accents already use, so it is his colour, not a new one


def ship_rects(pilots):
    js = subprocess.run(['node', '-e',
        "global.window=global;eval(require('fs').readFileSync('assets/manifest.js','utf8'));"
        "const P=" + json.dumps(pilots) + ";const o={};"
        "for(const k in BOFX.ships){for(const p of P){"
        "  if(k==='ship_'+p || k.indexOf('ship_'+p+'_')===0){o[k]=BOFX.ships[k];break;}}}"
        "process.stdout.write(JSON.stringify(o));"], capture_output=True, cwd=ROOT)
    return json.loads(js.stdout.decode())


def band_stats(im, lo, hi, greyband):
    """value range actually occupied by a band, so the exchange maps real range onto real range"""
    px = im.load()
    vs = []
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            if a < 8:
                continue
            h, s, v = colorsys.rgb_to_hsv(r / 255., g / 255., b / 255.)
            d = h * 360
            if greyband:
                if s < 0.20 and v <= 0.30:
                    vs.append(v)
            elif lo <= d <= hi and s >= 0.25:
                vs.append(v)
    if not vs:
        return (0.0, 1.0)
    vs.sort()
    return (vs[int(len(vs) * 0.05)], vs[int(len(vs) * 0.95)])


def make_decker_rule(blk, yel):
    """black -> gold and gold -> black, each keeping its position inside its own band"""
    b0, b1 = blk
    y0, y1 = yel

    def rescale(v, src, dst):
        s0, s1 = src; d0, d1 = dst
        f = 0.0 if s1 <= s0 else (v - s0) / (s1 - s0)
        return max(0.0, min(1.0, d0 + max(0.0, min(1.0, f)) * (d1 - d0)))

    def rule(h, s, v):
        d = h * 360
        if s < 0.20 and v <= 0.30:                    # the near-black hull -> GOLD, lifted
            nv = rescale(v, (b0, b1), (y0, y1))
            return DECKER_GOLD, 0.62 + 0.22 * nv, nv
        if 30 <= d <= 62 and s >= 0.25:               # the gold accents -> BLACK, dropped
            nv = rescale(v, (y0, y1), (b0, b1))
            return h, s * 0.12, nv
        return h, s, v
    return rule


def rule_maverick(h, s, v):
    """green -> teal. Hue only: S and V are left exactly as authored."""
    d = h * 360
    if 80 <= d <= 160 and s >= 0.15:
        return TEAL, s, v
    return h, s, v


def recolour(im, fn):
    px = im.load(); n = 0
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            if a < 8:
                continue
            h, s, v = colorsys.rgb_to_hsv(r / 255., g / 255., b / 255.)
            nh, ns, nv = fn(h, s, v)
            if (nh, ns, nv) != (h, s, v):
                n += 1
            rr, gg, bb = colorsys.hsv_to_rgb(nh, max(0., min(1., ns)), max(0., min(1., nv)))
            px[x, y] = (int(rr * 255 + .5), int(gg * 255 + .5), int(bb * 255 + .5), a)
    return n


def main():
    write = '--write' in sys.argv
    R = ship_rects(['decker', 'maverick'])
    A = Image.open(ATLAS).convert('RGBA')
    print('atlas %dx%d, %d Decker/Maverick frames' % (A.width, A.height, len(R)))

    hull = A.crop(tuple(R['ship_decker'][:2]) +
                  (R['ship_decker'][0] + R['ship_decker'][2], R['ship_decker'][1] + R['ship_decker'][3]))
    blk = band_stats(hull, 0, 0, True)
    yel = band_stats(hull, 30, 62, False)
    print('decker  black band v %.2f..%.2f   gold band v %.2f..%.2f  -> they exchange these ranges'
          % (blk[0], blk[1], yel[0], yel[1]))
    dr = make_decker_rule(blk, yel)

    before = {p: None for p in ('decker', 'maverick')}
    for p in before:
        r = R['ship_' + p]
        before[p] = A.crop((r[0], r[1], r[0] + r[2], r[1] + r[3])).copy()

    total = 0
    for k, r in sorted(R.items()):
        fn = dr if k.startswith('ship_decker') else rule_maverick
        x, y, w, h = r[0], r[1], r[2], r[3]
        cell = A.crop((x, y, x + w, y + h))
        n = recolour(cell, fn)
        A.paste(cell, (x, y))
        total += n
    print('recoloured %d pixels across %d frames' % (total, len(R)))

    from PIL import ImageDraw, ImageFont
    try:
        F = ImageFont.truetype('C:/Windows/Fonts/consolab.ttf', 15)
    except Exception:
        F = ImageFont.load_default()
    T = 240
    proof = Image.new('RGB', (T * 4, T + 24), (22, 22, 28))
    d = ImageDraw.Draw(proof)
    cells = []
    for p in ('decker', 'maverick'):
        r = R['ship_' + p]
        cells.append((p + ' BEFORE', before[p]))
        cells.append((p + ' AFTER', A.crop((r[0], r[1], r[0] + r[2], r[1] + r[3]))))
    for i, (lbl, im) in enumerate(cells):
        bb = im.getbbox(); c = im.crop(bb) if bb else im
        s = min((T - 12) / c.width, (T - 12) / c.height)
        t = c.resize((max(1, int(c.width * s)), max(1, int(c.height * s))), Image.LANCZOS)
        proof.paste(t, (i * T + (T - t.width) // 2, (T - t.height) // 2), t)
        d.text((i * T + 5, T + 4), lbl, font=F, fill=(240, 240, 250))
    proof.save(os.path.join(ROOT, 'docs/SHIPS_RECOLOUR_0906G.png'))
    print('wrote docs/SHIPS_RECOLOUR_0906G.png')

    if not write:
        print('DRY RUN - the atlas is untouched. Re-run with --write.')
        return 0
    bak = ATLAS + '.0906g.bak'
    if not os.path.exists(bak):
        shutil.copy2(ATLAS, bak)
        print('backed up the atlas to %s' % os.path.basename(bak))
    A.save(ATLAS)
    print('wrote the ship atlas in place (rects unchanged, so no manifest edit)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
