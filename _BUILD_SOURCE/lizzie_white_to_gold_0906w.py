#!/usr/bin/env python3
"""lizzie_white_to_gold_0906w.py - Lizzie is GOLD, so her white becomes shaded gold.

    python _BUILD_SOURCE/lizzie_white_to_gold_0906w.py            # sweep + proof
    python _BUILD_SOURCE/lizzie_white_to_gold_0906w.py --write

Mike, 0906: "Lizzie, shes supposed to be GOLD, no white, the white should be shaded gold/yellow."

Measured on her hull frame: 27,131 opaque px, of which **1,529 are white** (s < 0.12, v >= 0.55)
and a further 1,044 are pale (s < 0.22, v >= 0.40) - 9.4% between them. That is her canopy and the
two nozzle caps, which is exactly what reads as white against an otherwise gold-brown aircraft.

⚠ SATURATION IS ADDED ON A RAMP, NOT AS A FLAT FILL. A single gold written into every white pixel
destroys the modelling underneath - the same failure as the font tint (a flat `source-atop` flood
turned E into B) and the first Juggernaut brown pass. The nozzle caps and the canopy are SHADED
white: they carry a highlight, a midtone and a shadow, and if all three become one gold the parts
stop reading as metal. Here the hue is fixed and the SATURATION rides value, so a bright highlight
takes a pale gold and a shadowed fold takes a deep one. **Value is untouched on every pixel**, per
the standing palette/luminance rule.

⚠ AND IT IS BOUNDED AT s < 0.30 SO HER GOLD DOES NOT MOVE. Her hull is already gold-brown at
s 0.35-0.6; sweeping every low-saturation pixel would also catch her grey-brown panels and flatten
the two-tone the airframe is built from. Only what actually reads as white or near-white converts.
"""
import os, sys, json, shutil, colorsys, subprocess
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ATLAS = os.path.join(ROOT, 'assets/game/atlas/bof_player_ships_barrel_rolls.png')
MANIFEST = os.path.join(ROOT, 'assets/manifest.js')

GOLD_H = 44.0 / 360.0        # her own accent hue, taken off her hull rather than picked
S_MAX = 0.30                 # above this she is already gold; leave it alone


def rows():
    out = subprocess.run(['node', '-e',
        "global.window=global;eval(require('fs').readFileSync('assets/manifest.js','utf8'));"
        "const o={};for(const k in BOFX.ships)if(/^ship_lizzie(_|$)/.test(k))o[k]=BOFX.ships[k];"
        "process.stdout.write(JSON.stringify(o));"], capture_output=True, cwd=ROOT)
    return json.loads(out.stdout.decode())


def convert(cell, lo, hi):
    """white -> gold, saturation riding value, V untouched"""
    px = cell.load()
    n = 0
    for y in range(cell.height):
        for x in range(cell.width):
            r, g, b, a = px[x, y]
            if a <= 16:
                continue
            h, s, v = colorsys.rgb_to_hsv(r / 255., g / 255., b / 255.)
            if s >= S_MAX or v < 0.30:
                continue
            # how "white" is it: 1 at fully desaturated, 0 at the S_MAX boundary
            wf = 1.0 - min(1.0, s / S_MAX)
            ns = (lo + (hi - lo) * (1.0 - min(1.0, max(0.0, (v - 0.30) / 0.70)))) * wf
            rr, gg, bb = colorsys.hsv_to_rgb(GOLD_H, max(0.0, min(1.0, ns)), v)
            px[x, y] = (int(rr * 255 + .5), int(gg * 255 + .5), int(bb * 255 + .5), a)
            n += 1
    return n


def flat(rgba, bg=(20, 20, 26)):
    """⚠ COMPOSITE, NEVER .convert('RGB') - that discards alpha and paints the old chroma key
    back on (0906v). Every proof render in this repo goes through here."""
    out = Image.new('RGB', rgba.size, bg)
    out.paste(rgba, (0, 0), rgba)
    return out


def main():
    write = '--write' in sys.argv
    R = rows()
    A = Image.open(ATLAS).convert('RGBA')
    r = R['ship_lizzie']
    base = A.crop((r[0], r[1], r[0] + r[2], r[1] + r[3]))

    # ---- a rendered sweep, because "how gold" is a look and not a number
    try:
        F = ImageFont.truetype('C:/Windows/Fonts/consolab.ttf', 15)
    except Exception:
        F = ImageFont.load_default()
    opts = [('now', None), ('0.20-0.45', (0.20, 0.45)), ('0.30-0.60', (0.30, 0.60)),
            ('0.42-0.78', (0.42, 0.78))]
    T = 300
    sheet = Image.new('RGB', (T * len(opts), T + 24), (18, 18, 24))
    d = ImageDraw.Draw(sheet)
    for i, (lbl, band) in enumerate(opts):
        c = base.copy()
        if band:
            convert(c, band[0], band[1])
        sc = min((T - 16) / c.width, (T - 30) / c.height)
        t = flat(c.resize((max(1, int(c.width * sc)), max(1, int(c.height * sc))), Image.NEAREST))
        sheet.paste(t, (i * T + (T - t.width) // 2, (T - 24 - t.height) // 2 + 12))
        d.text((i * T + 6, T + 4), lbl, font=F, fill=(238, 238, 248))
    sheet.save(os.path.join(ROOT, 'docs/LIZZIE_GOLD_SWEEP_0906W.png'))
    print('wrote docs/LIZZIE_GOLD_SWEEP_0906W.png')

    lo, hi = 0.30, 0.60
    n = 0
    for k, rr in sorted(R.items()):
        x, y, w, h = rr[0], rr[1], rr[2], rr[3]
        c = A.crop((x, y, x + w, y + h))
        n += convert(c, lo, hi)
        A.paste(c, (x, y))
    print('converted %d white/pale pixels across %d lizzie frames (value untouched)' % (n, len(R)))

    if not write:
        print('DRY RUN - nothing written.')
        return 0
    bak = ATLAS + '.0906w.bak'
    if not os.path.exists(bak):
        shutil.copy2(ATLAS, bak)
    A.save(ATLAS)
    print('wrote the atlas (rects unchanged - only pixels moved)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
