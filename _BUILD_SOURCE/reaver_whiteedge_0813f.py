#!/usr/bin/env python3
"""
DROP 0813F - THE STAGE-2 BOSS'S WHITE EDGE BECOMES A BLACK EDGE

Mike: "convert stage 2 boss white edges to black and white pixels ty."

Read as: the white RIM becomes black; white pixels that are part of the artwork stay white. Same
treatment the purple halos got in 0813e - outer boundary only, alpha untouched, nothing deleted.
If he meant a black/white dithered rim instead, the ramp is one edit away (see DITHER below).

Runs a DRY SCAN first and prints what it would touch, so the split between rim-white and
interior-white is visible BEFORE anything is written.

⚠ BOFFI rects are [sheetIndex, x, y, w, h] - FIVE elements. Reading them as four resolved every
rect to None in 0813e and the script correctly edited nothing rather than writing to a wrong
rectangle of a shared sheet.

⚠ A key does not own its file. Work is grouped by (file, rect) and each rect is edited once.
"""
import os, re, io, shutil, sys
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
MAN  = os.path.join(ROOT, 'assets', 'manifest.js')
KEYS = ['nsb_inferno_reaver']
DRY  = ('--write' not in sys.argv)
DITHER = False        # True -> alternate black/white along the rim instead of solid black

man = io.open(MAN, encoding='utf-8', errors='ignore').read()

def src_of(k):
    m = re.search(r'"%s"\s*:\s*"([^"]+\.png)"' % re.escape(k), man)
    return m.group(1) if m else None

def rect_of(k):
    m = re.search(r'"%s"\s*:\s*\[(\d+),(\d+),(\d+),(\d+),(\d+)\]' % re.escape(k), man)
    if not m: return None
    g = [int(v) for v in m.groups()]
    return (g[1], g[2], g[3], g[4])

def is_white(r, g, b, a):
    # near-white: bright and close to neutral
    return a >= 40 and r > 185 and g > 185 and b > 185 and (max(r,g,b) - min(r,g,b)) < 40

groups = {}
for k in KEYS:
    f, r = src_of(k), rect_of(k)
    if not f:
        print('*** no source file for %s' % k); continue
    if not r:
        # A LOOSE FILE, not an atlas cell - it has no BOFFI rect because the whole PNG is the
        # sprite. nsb_inferno_reaver is assets/game/nsb_inferno_reaver.png. Use the full bounds.
        p = os.path.join(ROOT, f.replace('/', os.sep))
        if not os.path.isfile(p):
            print('*** %s: no rect and no file at %s' % (k, f)); continue
        with Image.open(p) as _im: r = (0, 0, _im.width, _im.height)
        print('%s is a loose file (%dx%d) - whole image is the cell' % (k, r[2], r[3]))
    groups.setdefault((f, r), []).append(k)

total_edge = total_interior = 0
for (f, rect), ks in groups.items():
    path = os.path.join(ROOT, f.replace('/', os.sep))
    if not os.path.isfile(path):
        print('*** missing sheet %s' % f); continue
    im = Image.open(path).convert('RGBA')
    px = im.load()
    W, H = im.size
    x0, y0, cw, ch = rect
    x1, y1 = min(x0 + cw, W), min(y0 + ch, H)
    edge_px, interior_px = [], 0
    for y in range(y0, y1):
        for x in range(x0, x1):
            r, g, b, a = px[x, y]
            if not is_white(r, g, b, a): continue
            boundary = False
            for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
                nx, ny = x + dx, y + dy
                if nx < x0 or ny < y0 or nx >= x1 or ny >= y1 or px[nx, ny][3] < 40:
                    boundary = True; break
            if boundary: edge_px.append((x, y))
            else: interior_px += 1
    total_edge += len(edge_px); total_interior += interior_px
    print('%s  cell %dx%d @%d,%d' % (','.join(ks), cw, ch, x0, y0))
    print('   rim white      %5d px   <- becomes black' % len(edge_px))
    print('   interior white %5d px   <- kept as-is' % interior_px)
    if DRY:
        continue
    for i, (x, y) in enumerate(edge_px):
        a = px[x, y][3]
        if DITHER and ((x + y) & 1):
            px[x, y] = (255, 255, 255, a)
        else:
            px[x, y] = (0, 0, 0, a)
    bak = path + '.bak'
    if not os.path.exists(bak): shutil.copy2(path, bak)
    im.save(path)
    print('   written to %s (backup %s)' % (f, os.path.basename(bak)))

print('\n%d rim px%s;  %d interior white px untouched'
      % (total_edge, ' WOULD BE converted (dry run - pass --write)' if DRY else ' converted to black',
         total_interior))
