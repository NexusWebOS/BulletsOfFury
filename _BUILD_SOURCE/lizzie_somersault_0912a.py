#!/usr/bin/env python3
"""
lizzie_somersault_0912a.py - THE NINTH SOMERSAULT REEL.

    python3 _BUILD_SOURCE/lizzie_somersault_0912a.py [--check]

Mike (0912): "All pilots should get somersalt and properly use their graphics to make them
somersalt."

Measured first, per CLAUDE.md. SOMER_PILOTS already lists all nine and somersaultAvailable()
already widened in 0908 - but it ALSO gates on `ship_<pk>_so0`, and the manifest carries 64 `so`
cells, not 72:

    axel 8  cole 8  decker 8  falva 8  freezer 8  juggernaut 8  maverick 8  yuri 8   LIZZIE 0

So eight pilots somersault today and Lizzie silently cannot. Her reel is the whole feature.

⚠ THE `so` REEL IS NOT THE `br` REEL. Checked cell-by-cell, not by eye: maverick so2 is 196x78
and br2 is 39x184 - a pitch rotation presents the SPAN and loses height, a roll presents the
CHORD and keeps it. Aliasing her roll frames onto `so` would have shipped a barrel roll wearing
a somersault's name, which is exactly the bug Mike is pointing at with "properly use their
graphics".

⚠ SO THE REEL IS DERIVED FROM HER OWN PLATE, NOT GENERATED. "properly use THEIR graphics" -
her authored gold delta is the source, put through the pitch transform the engine already uses
for a somersault when there is no authored reel (see RAP_MAN / blacksteelManoeuvre: "A
somersault does the same on scale.y and adds a vertical arc"). The profile is not invented
either - it is measured off Maverick's authored eight and applied to her:

    frame       so0   so1   so2   so3   so4   so5   so6   so7
    height/so0  1.00  0.81  0.44  0.89  0.96  0.88  0.54  0.81
    width /so0  1.00  1.08  1.12  1.07  0.99  1.04  1.12  1.08
    surface     top   top   EDGE  belly belly belly EDGE  top

Height collapses and span widens together, which is what a pitching airframe does; the floor at
0.44 rather than 0 is the fuselage's own depth, which is why the authored frames never vanish.
so3/so4/so5 are the UNDERSIDE and keep the nose up-screen (Maverick's do), so they are darkened
and desaturated rather than mirrored - a mirror of a near-symmetric delta is invisible.

⚠ BOTH OF HER SHEETS, OR THE COSTUME DRAWS GARBAGE. She is the one pilot whose sheet is chosen
by a live flag rather than by the key (_shipSheetOf), and applyLizzieSkin only walks
Object.keys(LIZZIE_B42_RECTS). Registering `so` on the stock sheet alone would leave
ship_lizzie_so0 holding a STOCK rect while _shipSheetOf returned the B-42 page - her own note
in game.js calls this out as what breaks a two-way swap. So the reel is built onto ship_lizzie
AND ship_lizzie_b42, and `_so0.._so7` are added to LIZZIE_B42_RECTS.
"""
import os, sys, io, json, re, argparse
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
SHIPS = os.path.join(ROOT, 'assets', 'game', 'atlas', 'ships')
MANIFEST = os.path.join(ROOT, 'assets', 'manifest.js')
GAMEJS = os.path.join(ROOT, 'assets', 'game.js')

# measured off ship_maverick_so0..so7 (see the header)
VSC  = [1.00, 0.81, 0.44, 0.89, 0.96, 0.88, 0.54, 0.81]
HSC  = [1.00, 1.08, 1.12, 1.07, 0.99, 1.04, 1.12, 1.08]
BELLY= [0,    0,    0,    1,    1,    1,    0,    0   ]
EDGE = [0,    0,    1,    0,    0,    0,    1,    0   ]

CANVAS = (224, 243)          # every ship_lizzie_* row is authored on this canvas
STOCK_BASE = [246, 2, 158, 202, 44, 17, 224, 243]     # ship_lizzie_nf  (her level plate)
B42_BASE   = [191, 242, 151, 213, 40, 45, 224, 243]   # LIZZIE_B42_RECTS["_nf"]


def plate_from(sheet, rect):
    """Rebuild the full authored canvas for one cell, exactly as _shipCell does."""
    x, y, w, h, ox, oy, cw, ch = rect
    c = Image.new('RGBA', (cw, ch), (0, 0, 0, 0))
    c.paste(sheet.crop((x, y, x + w, y + h)), (ox, oy))
    return c


def belly(im):
    """The underside: no canopy glass, no top-surface specular. Darken and desaturate the
       painted hull while leaving the engine plume alone - the plume is the one thing that is
       BRIGHTER from below, and killing it would read as the ship switching off mid-flip."""
    px = im.load()
    w, h = im.size
    for j in range(h):
        for i in range(w):
            r, g, b, a = px[i, j]
            if not a:
                continue
            lum = (r * 299 + g * 587 + b * 114) // 1000
            if lum > 205 and (r > 150 and g > 110):     # hot plume / muzzle white: keep it
                continue
            # 62% value, pulled 45% toward its own luminance = shadowed, unpainted underside
            r = int((r * 0.55 + lum * 0.45) * 0.62)
            g = int((g * 0.55 + lum * 0.45) * 0.62)
            b = int((b * 0.55 + lum * 0.45) * 0.66)     # a hair cool, like sky-shadow
            px[i, j] = (r, g, b, a)
    return im


def edge_shade(im):
    """Edge-on: almost all of what you see is the fuselage side, which catches less light."""
    px = im.load()
    w, h = im.size
    for j in range(h):
        for i in range(w):
            r, g, b, a = px[i, j]
            if not a:
                continue
            px[i, j] = (int(r * 0.84), int(g * 0.84), int(b * 0.88), a)
    return im


def build_reel(plate):
    """Eight pitch frames on the authored canvas, centred on the plate's own centre."""
    cw, ch = CANVAS
    bb = plate.getbbox()
    body = plate.crop(bb)
    bw, bh = body.size
    cx = (bb[0] + bb[2]) / 2.0
    cy = (bb[1] + bb[3]) / 2.0
    out = []
    for i in range(8):
        nw = max(1, int(round(bw * HSC[i])))
        nh = max(1, int(round(bh * VSC[i])))
        f = body.resize((nw, nh), Image.LANCZOS)
        if BELLY[i]:
            f = belly(f)
        elif EDGE[i]:
            f = edge_shade(f)
        c = Image.new('RGBA', (cw, ch), (0, 0, 0, 0))
        c.paste(f, (int(round(cx - nw / 2.0)), int(round(cy - nh / 2.0))))
        out.append(c)
    return out


def pack(sheet_path, base_rect, dry=False):
    """Append the reel to the pilot's own sheet in a fresh strip and return the eight rows."""
    sheet = Image.open(sheet_path).convert('RGBA')
    reel = build_reel(plate_from(sheet, base_rect))
    cw, ch = CANVAS
    PAD = 2
    per_row = max(1, (sheet.width - PAD) // (cw + PAD))
    rows_n = (8 + per_row - 1) // per_row
    strip_h = rows_n * (ch + PAD) + PAD
    y0 = sheet.height
    out = Image.new('RGBA', (sheet.width, sheet.height + strip_h), (0, 0, 0, 0))
    out.paste(sheet, (0, 0))
    rects = []
    for i, f in enumerate(reel):
        r, c = divmod(i, per_row)
        ox, oy = PAD + c * (cw + PAD), y0 + PAD + r * (ch + PAD)
        bb = f.getbbox() or (0, 0, 1, 1)          # trim like every other row in this atlas
        trim = f.crop(bb)
        out.paste(trim, (ox, oy))
        rects.append([ox, oy, trim.width, trim.height, bb[0], bb[1], cw, ch])
    if not dry:
        out.save(sheet_path)
    return rects, out.size


def patch_manifest(rows, dry=False):
    s = io.open(MANIFEST, encoding='utf-8').read()
    if '"ship_lizzie_so0"' in s:
        raise SystemExit('manifest already carries ship_lizzie_so0 - rerun on a clean tree')
    anchor = '"ship_lizzie_sp0":'
    if s.count(anchor) != 1:
        raise SystemExit('anchor %s appears %d times' % (anchor, s.count(anchor)))
    add = ''.join('"ship_lizzie_so%d":%s,' % (i, json.dumps(rows[i], separators=(',', ':')))
                  for i in range(8))
    s = s.replace(anchor, add + anchor, 1)
    if not dry:
        io.open(MANIFEST, 'w', encoding='utf-8', newline='').write(s)
    return len(add)


def patch_gamejs(rows_b42, dry=False):
    """LIZZIE_B42_RECTS is keyed by SUFFIX and applyLizzieSkin only walks its keys."""
    s = io.open(GAMEJS, encoding='utf-8').read()
    nl = '\r\n' if '\r\n' in s else '\n'
    if '"_so0"' in s:
        raise SystemExit('game.js already carries _so0 - rerun on a clean tree')
    anchor = 'const LIZZIE_B42_RECTS={'
    if s.count(anchor) != 1:
        raise SystemExit('LIZZIE_B42_RECTS anchor appears %d times' % s.count(anchor))
    note = (anchor + nl +
            '  /* ⚠ THE SOMERSAULT REEL IS IN HERE BECAUSE applyLizzieSkin WALKS THESE KEYS (0912a).' + nl +
            '     She is the one pilot whose SHEET is chosen by a live flag rather than by the key' + nl +
            '     (_shipSheetOf), so a `so` row registered on the stock atlas alone would keep its stock' + nl +
            '     rect while the costume was on and crop the B-42 page at stock coordinates. Her own' + nl +
            '     note below already calls an asymmetric key set out as what breaks a two-way swap. */' + nl)
    add = ''.join('  "_so%d":%s,%s' % (i, json.dumps(rows_b42[i], separators=(',', ':')), nl)
                  for i in range(8))
    s = s.replace(anchor, note + add, 1)
    if not dry:
        io.open(GAMEJS, 'w', encoding='utf-8', newline='').write(s)
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true', help='build and report, write nothing')
    a = ap.parse_args()
    dry = a.check

    stock_rows, stock_size = pack(os.path.join(SHIPS, 'ship_lizzie.png'), STOCK_BASE, dry)
    b42_rows, b42_size = pack(os.path.join(SHIPS, 'ship_lizzie_b42.png'), B42_BASE, dry)
    print('ship_lizzie.png     ->', stock_size)
    print('ship_lizzie_b42.png ->', b42_size)
    for i in range(8):
        print('  so%d stock %-28s b42 %s' % (i, stock_rows[i], b42_rows[i]))
    if dry:
        print('\n--check: nothing written')
        return
    n = patch_manifest(stock_rows)
    patch_gamejs(b42_rows)
    print('\nmanifest.js +%d bytes (8 rows), game.js LIZZIE_B42_RECTS +8 rows' % n)


if __name__ == '__main__':
    main()
