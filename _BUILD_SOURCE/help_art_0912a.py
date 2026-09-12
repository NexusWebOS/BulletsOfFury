#!/usr/bin/env python3
"""
help_art_0912a.py - THE HELP BUTTON AND THE CONTROLLER GLYPHS.

    python3 _BUILD_SOURCE/help_art_0912a.py [--check]

Mike (0912): "generate a matching button in the main menu to our current ones titled Help ...
generated directonal pad and buttons like A B C X Y Z START SELECT in our unique signature
ColeForge graphical style."

⚠ BOTH WERE GENERATED AGAINST THE GAME'S OWN BUTTONS AS A REFERENCE ASSET, not from a description
of them. btn_newgame / btn_options / btn_credits were uploaded as one strip and passed as
`reference_asset_id`, which is the one lever that keeps a generation on-model (see the SpriteCook
note in memory). "Matching our current ones" is a promise that can be checked by eye, and the
frame, the end-cap indicator lights, the teal circuit interior and the orange 3D lettering all came
back the same family.

⚠ BOTH ARE CUT FROM `pixel_url`, NOT `raw_url` - the same trap the charge rings fell into earlier
in this drop. raw_url is a full-resolution render with NO alpha: sampled along its top edge it is
(224,224,224)..(255,255,255), i.e. the transparency CHECKERBOARD flattened into the picture. Taking
the detail and keying it would have shipped buttons on a grey chessboard.

⚠ THE GLYPH SHEET IS SLICED BY ALPHA ISLAND, and that is the right call HERE specifically. The
usual rule is the opposite - slice by cell, because a crosshair or a burst splits into fragments -
but every one of these twelve is a single solid button with clear air round it, and the model laid
them out on an IRREGULAR grid (the START and SELECT pills are wider than a face cap and do not sit
in a 4x3 lattice). A fixed grid would have cut two of them in half. The islands are then sorted
into reading order and named.
"""
import os, sys, io, json, argparse
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
SRC = os.path.join(os.environ.get('TEMP', '/tmp'), 'sc')
OUT = os.path.join(ROOT, 'assets', 'game', 'atlas', 'ui_help.png')
MANIFEST = os.path.join(ROOT, 'assets', 'manifest.js')
SHEET = 'ui_help'

# reading order, after the islands are sorted by row then column
GLYPHS = ['pad_a', 'pad_b', 'pad_c', 'pad_x',
          'pad_y', 'pad_z', 'pad_start',
          'pad_dpad', 'pad_dpad_up', 'pad_select',
          'pad_dpad2', 'pad_dpad_up2', 'pad_stick', 'pad_l']


def trim(im):
    bb = im.getbbox()
    return im.crop(bb) if bb else im


def islands(im, amin=140, floor=24):
    """Flood-fill every connected run of opaque pixels; return their bounding boxes."""
    w, h = im.size
    a = im.split()[3].load()
    seen = bytearray(w * h)
    out = []
    for sy in range(h):
        for sx in range(w):
            if seen[sy * w + sx] or a[sx, sy] <= floor:
                continue
            stack = [(sx, sy)]
            seen[sy * w + sx] = 1
            x0 = x1 = sx; y0 = y1 = sy; n = 0
            while stack:
                x, y = stack.pop()
                n += 1
                if x < x0: x0 = x
                if x > x1: x1 = x
                if y < y0: y0 = y
                if y > y1: y1 = y
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < w and 0 <= ny < h and not seen[ny * w + nx] and a[nx, ny] > floor:
                        seen[ny * w + nx] = 1
                        stack.append((nx, ny))
            if n >= amin:
                out.append((x0, y0, x1 + 1, y1 + 1))
    # reading order: group into rows by vertical overlap, then left to right
    out.sort(key=lambda b: (b[1], b[0]))
    rows, cur = [], []
    for b in out:
        if cur and b[1] > cur[-1][1] + (cur[-1][3] - cur[-1][1]) * 0.55:
            rows.append(sorted(cur, key=lambda q: q[0])); cur = []
        cur.append(b)
    if cur: rows.append(sorted(cur, key=lambda q: q[0]))
    return [b for r in rows for b in r]


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--check', action='store_true'); a = ap.parse_args()
    btn = trim(Image.open(os.path.join(SRC, 'help_btn.png')).convert('RGBA'))
    pad = Image.open(os.path.join(SRC, 'pad.png')).convert('RGBA')
    # 4x, so a 45px cap is not mush at the 30-40px the help screen draws it
    pad = pad.resize((pad.width * 4, pad.height * 4), Image.LANCZOS)
    boxes = islands(pad, amin=1200)
    print('%d glyph islands found' % len(boxes))
    cells = [('btn_help', btn)]
    for i, b in enumerate(boxes):
        name = GLYPHS[i] if i < len(GLYPHS) else 'pad_extra%d' % i
        cells.append((name, pad.crop(b)))

    if a.check:
        H = 150
        W = sum(int(im.width * H / im.height) + 8 for _, im in cells) + 8
        card = Image.new('RGBA', (W, H + 20), (60, 64, 74, 255))
        from PIL import ImageDraw
        d = ImageDraw.Draw(card); x = 4
        for n, im in cells:
            w = max(1, int(im.width * H / im.height))
            card.alpha_composite(im.resize((w, H), Image.LANCZOS), (x, 18))
            d.text((x + 2, 3), n, fill=(255, 210, 90, 255)); x += w + 8
        p = os.path.join(os.environ.get('TEMP', '/tmp'), 'help_cells.png')
        card.save(p); print('--check: wrote', p)
        for n, im in cells: print('   %-14s %dx%d' % (n, im.width, im.height))
        return

    PAD = 2; W = 2048
    x = y = PAD; rowh = 0; placed = []
    for name, im in cells:
        if x + im.width + PAD > W:
            x = PAD; y += rowh + PAD; rowh = 0
        placed.append((name, im, x, y)); x += im.width + PAD; rowh = max(rowh, im.height)
    H = y + rowh + PAD
    sheet = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    rows = {}
    for name, im, px, py in placed:
        sheet.paste(im, (px, py)); rows[name] = [SHEET, px, py, im.width, im.height]
    sheet.save(OUT)
    print('%s  %dx%d' % (os.path.relpath(OUT, ROOT), W, H))

    s = io.open(MANIFEST, encoding='utf-8').read()
    import re
    for n in rows:
        s = re.sub(r'"%s":\[[^\]]*\],?' % re.escape(n), '', s)
    s = s.replace('"nca_%s":"assets/game/atlas/%s.png",' % (SHEET, SHEET), '')
    s = s.replace('"img":{', '"img":{"nca_%s":"assets/game/atlas/%s.png",' % (SHEET, SHEET), 1)
    add = ''.join('"%s":%s,' % (n, json.dumps(rows[n], separators=(',', ':'))) for n, _, _, _ in placed)
    s = s.replace('"cells":{', '"cells":{' + add, 1)
    io.open(MANIFEST, 'w', encoding='utf-8', newline='').write(s)
    print('manifest.js: +1 img, +%d cells' % len(rows))
    for n in rows: print('  %-14s %s' % (n, rows[n]))


if __name__ == '__main__':
    main()
