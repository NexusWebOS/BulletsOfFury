#!/usr/bin/env python3
"""recolour_maverick_teal_0906g.py - move Maverick's whole identity off Cole's green.

    python _BUILD_SOURCE/recolour_maverick_teal_0906g.py            # proof only
    python _BUILD_SOURCE/recolour_maverick_teal_0906g.py --write

Mike, 0906: "palette swap maverick's portrait light color and his ship's green colors to a more
teal color so were not confused with him or Cole."

The SHIP is done by recolour_ships_0906g.py. This is everything else that carries the same green,
because a pilot whose ship is teal and whose portrait, avatar, standing figure, card, HUD and stat
bars are all still Cole-green has not actually been separated from Cole - the ship is the smallest
of those surfaces.

    port_maverick_*        7 cells on ui_dialogue (idle and smile are ALIASED to one rect)
    pav_maverick           the bordered roster avatar and its accent bars
    maverick_body_0        the standing figure, including the shoulder patch
    PILOTS[].tint          the one table the card, HUD, roster ring and emblem accents read

⚠ THE ALIAS IS WHY THIS COUNTS RECTS AND NOT KEYS. port_maverick_idle and port_maverick_smile are
the SAME rect (0,2845,213,262). Recolouring per key would run the conversion over those pixels
twice - harmless for a pure hue rotation, but this repo has ~750 aliased cells and the habit of
iterating keys is how a two-pass rule silently double-applies. Deduped by rect.

⚠ AND THE HUE ROTATION IS THE SAME ONE THE SHIP GOT, DELIBERATELY. 80-160 -> 177, S and V
untouched. If the portrait used a different green-to-teal mapping than the hull, the pilot and his
aircraft would be two slightly different colours on the same card, which reads as a mistake rather
than as a scheme.
"""
import os, sys, json, shutil, subprocess, colorsys
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEAL = 177.0 / 360.0
TEAL_HEX = '#3ad6c8'          # the tint table's new value for him, measured off the recoloured hull


def rule(h, s, v):
    d = h * 360
    if 80 <= d <= 160 and s >= 0.15:
        return TEAL, s, v
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
                rr, gg, bb = colorsys.hsv_to_rgb(nh, ns, nv)
                px[x, y] = (int(rr * 255 + .5), int(gg * 255 + .5), int(bb * 255 + .5), a)
    return n


def main():
    write = '--write' in sys.argv
    js = subprocess.run(['node', '-e',
        "global.window=global;eval(require('fs').readFileSync('assets/manifest.js','utf8'));"
        "const o={};for(const k in BOFX.cells)if(/^port_maverick/.test(k))o[k]=BOFX.cells[k];"
        "process.stdout.write(JSON.stringify(o));"], capture_output=True, cwd=ROOT)
    cells = json.loads(js.stdout.decode())

    # DEDUPE BY RECT - idle and smile share one
    uniq = {}
    for k, c in cells.items():
        uniq.setdefault(tuple(c), []).append(k)
    print('%d portrait keys -> %d distinct rects' % (len(cells), len(uniq)))
    for r, ks in uniq.items():
        if len(ks) > 1:
            print('   aliased: %s share %s' % (' + '.join(sorted(ks)), list(r[1:])))

    sheet_name = list(uniq)[0][0]
    sheet = os.path.join(ROOT, 'assets/game/atlas/%s.png' % sheet_name)
    A = Image.open(sheet).convert('RGBA')
    total = 0
    for r in uniq:
        _, x, y, w, h = r
        cell = A.crop((x, y, x + w, y + h))
        total += recolour(cell)
        A.paste(cell, (x, y))
    print('portraits: %d px moved to teal on %s' % (total, sheet_name))

    loose = []
    for rel in ('assets/game/pilot_avatars/pav_maverick.png',
                'assets/game/pilot_bodies/maverick_body_0.png'):
        p = os.path.join(ROOT, rel)
        if not os.path.exists(p):
            print('   MISSING %s' % rel); continue
        im = Image.open(p).convert('RGBA')
        n = recolour(im)
        loose.append((rel, p, im, n))
        print('%-44s %d px' % (os.path.basename(rel), n))

    from PIL import ImageDraw, ImageFont
    try:
        F = ImageFont.truetype('C:/Windows/Fonts/consolab.ttf', 14)
    except Exception:
        F = ImageFont.load_default()
    T = 200
    shots = [('portrait', A.crop((uniq[list(uniq)[0]] and 0 or 0, 0, 1, 1)))]  # placeholder, replaced below
    shots = []
    idle = cells.get('port_maverick_idle')
    if idle:
        _, x, y, w, h = idle
        shots.append(('portrait', A.crop((x, y, x + w, y + h))))
    for rel, _p, im, _n in loose:
        shots.append((os.path.basename(rel).replace('.png', ''), im))
    proof = Image.new('RGB', (T * max(1, len(shots)), T + 22), (22, 22, 28))
    d = ImageDraw.Draw(proof)
    for i, (lbl, im) in enumerate(shots):
        bb = im.getbbox(); c = im.crop(bb) if bb else im
        s = min((T - 10) / c.width, (T - 10) / c.height)
        t = c.resize((max(1, int(c.width * s)), max(1, int(c.height * s))), Image.LANCZOS)
        proof.paste(t, (i * T + (T - t.width) // 2, (T - t.height) // 2), t)
        d.text((i * T + 4, T + 4), lbl, font=F, fill=(240, 240, 250))
    proof.save(os.path.join(ROOT, 'docs/MAVERICK_TEAL_0906G.png'))
    print(os.linesep + 'wrote docs/MAVERICK_TEAL_0906G.png')
    print('PILOTS tint for maverick should become %s (edit game.js separately)' % TEAL_HEX)

    if not write:
        print('DRY RUN - nothing written. Re-run with --write.')
        return 0
    bak = sheet + '.0906g.bak'
    if not os.path.exists(bak):
        shutil.copy2(sheet, bak)
    A.save(sheet)
    for rel, p, im, _n in loose:
        im.save(p)
    print('wrote %s and %d loose files' % (sheet_name, len(loose)))
    return 0


if __name__ == '__main__':
    sys.exit(main())
