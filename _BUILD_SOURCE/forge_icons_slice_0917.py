#!/usr/bin/env python3
"""
forge_icons_slice_0917.py - cut a generated 3x3 forge-icon sheet into nine badges the game can use.

Mike, 0917: "I wanted weapon icons of each type after being upgraded with our element type,
generate those."

Each sheet is one weapon x nine elements, generated against ref_mg.png (the authored badge plus
the nine element badges) so the frame, ring and tag come back in the family's own language. The
RAW render is what gets cut - the pixel_url is a 200px downscale, far too small for nine badges -
and the raw is rendered on WHITE, so:

  1. cells are found from the sheet's own column/row gutters (the white gaps), never assumed thirds;
  2. each cell's white is punched to alpha by a FLOOD FROM ITS BORDER - the standing rule; a global
     white sweep would open pinholes in the chrome and ice badges, which carry near-white paint;
  3. what survives the flood at the rim (the anti-aliased white fringe) is converted to a dark
     edge, never deleted - halos become black edges (standing rule);
  4. the badge is trimmed and normalised to the FAMILY height (112, the chaingun badges' own),
     keeping its aspect - size is a hint and every sheet came back a different size.

    python _BUILD_SOURCE/forge_icons_slice_0917.py <sheet.png> <slot> [--check]
"""
import os, sys
from PIL import Image, ImageDraw
from collections import deque

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
OUT = os.path.join(ROOT, 'assets', 'game', 'ui', 'forge_0917')
ELEMS = ['fire', 'ice', 'lightning', 'prism', 'toxic', 'kinetic', 'chrome', 'water', 'dark']
FAMILY_H = 112
WHITE = 236          # a raw-render background pixel is >= this on all three channels

def runs(mask_line):
    """contiguous runs of True in a 1-D bool list -> [(start, end)]"""
    out, start = [], None
    for i, v in enumerate(mask_line + [False]):
        if v and start is None: start = i
        elif not v and start is not None: out.append((start, i)); start = None
    return out

def find_cells(im, thr=WHITE):
    """the nine content boxes, from the sheet's own gutters. `thr` is the background floor: the tier-V
    sheets carry a faint glow around every frame that tints the gutters, so their rows only separate
    at a lower floor (the glow is near-white, the ink is not)."""
    W, H = im.size
    px = im.load()
    def is_bg(x, y):
        r, g, b = px[x, y][:3]; return r >= thr and g >= thr and b >= thr
    colInk = [any(not is_bg(x, y) for y in range(0, H, 2)) for x in range(W)]
    rowInk = [any(not is_bg(x, y) for x in range(0, W, 2)) for y in range(H)]
    cols = [r for r in runs(colInk) if r[1] - r[0] > W * 0.12]
    rows = [r for r in runs(rowInk) if r[1] - r[0] > H * 0.12]
    return cols, rows

def punch(cell):
    """flood the background from the cell's border; convert the surviving rim fringe to a dark edge"""
    cell = cell.convert('RGBA'); W, H = cell.size; px = cell.load()
    def bg(x, y):
        r, g, b, a = px[x, y]; return a > 0 and r >= WHITE - 8 and g >= WHITE - 8 and b >= WHITE - 8
    seen = bytearray(W * H); q = deque()
    for x in range(W):
        for y in (0, H - 1):
            if bg(x, y) and not seen[y * W + x]: seen[y * W + x] = 1; q.append((x, y))
    for y in range(H):
        for x in (0, W - 1):
            if bg(x, y) and not seen[y * W + x]: seen[y * W + x] = 1; q.append((x, y))
    while q:
        x, y = q.popleft(); px[x, y] = (0, 0, 0, 0)
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < W and 0 <= ny < H and not seen[ny * W + nx] and bg(nx, ny):
                seen[ny * W + nx] = 1; q.append((nx, ny))
    # the rim: opaque pixels touching transparency that are still near-white are fringe, not paint
    fringe = 0
    for y in range(H):
        for x in range(W):
            r, g, b, a = px[x, y]
            if a == 0 or r < 200 or g < 200 or b < 200: continue
            if any(0 <= nx < W and 0 <= ny < H and px[nx, ny][3] == 0 for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1))):
                px[x, y] = (24, 22, 28, 255); fringe += 1
    return cell, fringe

def main():
    if len(sys.argv) < 3:
        print(__doc__); sys.exit(2)
    sheet, slot = sys.argv[1], int(sys.argv[2])
    check = '--check' in sys.argv
    im = Image.open(sheet).convert('RGB')
    cols, rows = find_cells(im)
    print('  gutters -> %d cols, %d rows' % (len(cols), len(rows)))
    if len(cols) != 3 or len(rows) != 3:
        print('  REFUSED: expected a 3x3 sheet, found %dx%d content runs' % (len(cols), len(rows))); sys.exit(1)
    os.makedirs(OUT, exist_ok=True)
    tiles = []
    k = 0
    for (y0, y1) in rows:
        for (x0, x1) in cols:
            cell = im.crop((max(0, x0 - 2), max(0, y0 - 2), min(im.width, x1 + 2), min(im.height, y1 + 2)))
            cell, fringe = punch(cell)
            bb = cell.getbbox()
            if not bb: print('  REFUSED: empty cell', k); sys.exit(1)
            cell = cell.crop(bb)
            s = FAMILY_H / cell.height
            cell = cell.resize((max(1, round(cell.width * s)), FAMILY_H), Image.LANCZOS)
            opaque = sum(1 for p in cell.getdata() if p[3] > 8)
            name = 'micon_forge_%s_%d.png' % (ELEMS[k], slot)
            cell.save(os.path.join(OUT, name))
            print('  %-28s %3dx%-3d opaque %5d fringe->edge %4d' % (name, cell.width, cell.height, opaque, fringe))
            tiles.append((cell, ELEMS[k])); k += 1
    if check:
        pad = 10; W = sum(t[0].width for t in tiles) + pad * 10; H = FAMILY_H + 34
        card = Image.new('RGB', (W, H), (16, 16, 22)); d = ImageDraw.Draw(card); x = pad
        for t, e in tiles:
            card.paste(t.convert('RGB'), (x, 24), t); d.text((x, 6), e, fill=(235, 220, 150)); x += t.width + pad
        p = os.path.join(ROOT, 'docs', 'proofs', 'forge_icons_0917', 'slot%d_check.png' % slot)
        card.save(p); print('  check ->', p)

if __name__ == '__main__':
    main()
