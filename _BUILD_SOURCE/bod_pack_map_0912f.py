#!/usr/bin/env python3
"""
bod_pack_map_0912f.py - cut maps for the Bullets of Debug! UI pack.

    python3 _BUILD_SOURCE/bod_pack_map_0912f.py [--check]

The generated sheets (buttons / cursors / icons) are grids of separate sprites. The Boss Mode editor
already has a loader for exactly this shape - loadAtlas/rectOf/cellRule in assets/bossmode/bossmode.js
read a <name>.json beside each <name>.png:

    { asset, frame_count, atlas:{columns, rows, cell, rects:[{frame,x,y,w,h}]},
      items:[{index, name, placement, visible_size}] }

rectOf() finds an item BY NAME and returns atlas.rects[i] at the same index, so the two arrays are
parallel and the rects do not have to be a uniform lattice. That matters here: generated grids are
never perfectly regular, and the START/SELECT-style wide cells in a pack like this sit outside any
lattice you would impose.

⚠ SLICED BY GRID, NOT BY ALPHA ISLAND - and the first cut got that wrong. Islands looked right for
the buttons (18 of 18) and fell apart on the other two: the cursor sheet returned 19 pieces for 16
cursors because the accent burst beside the active arrow, the I-beam's serifs and the rotate arrow's
plus are each their own island. That is precisely the "crosshairs split" failure the house rule
names, and I walked into it.

Both sheets are in fact perfectly regular - the cursors are 4x4, the icons 5x5 - so the grid IS the
slicer and each cell is then trimmed to its own ink for the rect. A count mismatch against the name
lists below (which are the order the art was PROMPTED in) is a loud failure rather than a silent
mislabel.

⚠ AND THE ICON SHEET CAME BACK 5x5, NOT THE 5x4 THAT WAS ASKED FOR. The generator added a fifth
column of variants - a second landscape, a cyan reload, a second path, a second gear. They are
useful rather than wrong, so they are named -alt and kept; the count in the list is what the art
actually is, not what the prompt requested.
"""
import os, sys, io, json, argparse
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
UI = os.path.join(ROOT, 'assets', 'bulletsofdebug', 'ui')

# the order the sheets were prompted in - row-major
BUTTON_LABELS = ['spawn', 'waves', 'enemy', 'stage', 'sprite', 'apply']
BUTTON_STATES = ['', '-hover', '-down']
NAMES = {
    'buttons': [L + S for L in BUTTON_LABELS for S in BUTTON_STATES],
    'cursors': ['pointer', 'pointer-active', 'link', 'text',
                'move', 'grab', 'grabbing', 'precision',
                'resize-horizontal', 'resize-vertical', 'resize-nwse', 'resize-nesw',
                'rotate', 'zoom-in', 'zoom-out', 'unavailable'],
    'icons':   ['enemy', 'waves', 'projectile', 'background', 'background-alt',
                'play', 'pause', 'stop', 'reload', 'reload-alt',
                'target', 'fov', 'select', 'path', 'path-alt',
                'save', 'open', 'export', 'import', 'delete',
                'brush', 'eyedropper', 'grid', 'settings', 'settings-alt'],
}
GRID = {'buttons': (6, 3), 'cursors': (4, 4), 'icons': (5, 5)}   # (rows, columns)
COLUMNS = {k: v[1] for k, v in GRID.items()}

# the hotspot for each cursor, as a fraction of its own cell - a pointer aims from its tip, a
# crosshair from its centre. Written here rather than guessed at use time.
HOTSPOT = {
    'pointer': (0.06, 0.04), 'pointer-active': (0.06, 0.04), 'link': (0.35, 0.10),
    'text': (0.50, 0.50), 'move': (0.50, 0.50), 'grab': (0.45, 0.45),
    'grabbing': (0.47, 0.47), 'precision': (0.50, 0.50),
    'resize-horizontal': (0.50, 0.50), 'resize-vertical': (0.50, 0.50),
    'resize-nwse': (0.50, 0.50), 'resize-nesw': (0.50, 0.50),
    'rotate': (0.50, 0.50), 'zoom-in': (0.42, 0.42), 'zoom-out': (0.42, 0.42),
    'unavailable': (0.50, 0.50),
}


def grid_cells(im, rows, cols, floor=24):
    """Divide the sheet into a rows x cols lattice, then trim each cell to its own ink.
       A cell with no ink at all is reported as-is so the count mismatch is visible."""
    W, H = im.size
    a = im.split()[3].load()
    cw, ch = W / cols, H / rows
    out = []
    for r in range(rows):
        for c in range(cols):
            x0, y0 = int(c * cw), int(r * ch)
            x1, y1 = int((c + 1) * cw), int((r + 1) * ch)
            mnx, mny, mxx, mxy = x1, y1, x0, y0
            for y in range(y0, y1):
                for x in range(x0, x1):
                    if a[x, y] > floor:
                        if x < mnx: mnx = x
                        if x > mxx: mxx = x
                        if y < mny: mny = y
                        if y > mxy: mxy = y
            if mxx < mnx:
                out.append([x0, y0, max(1, x1 - x0), max(1, y1 - y0)])
            else:
                out.append([mnx, mny, mxx - mnx + 1, mxy - mny + 1])
    return out, rows


def islands(im, amin, floor=24):
    w, h = im.size
    a = im.split()[3].load()
    seen = bytearray(w * h)
    out = []
    for sy in range(h):
        base = sy * w
        for sx in range(w):
            if seen[base + sx] or a[sx, sy] <= floor:
                continue
            stack = [(sx, sy)]; seen[base + sx] = 1
            x0 = x1 = sx; y0 = y1 = sy; n = 0
            while stack:
                x, y = stack.pop(); n += 1
                if x < x0: x0 = x
                if x > x1: x1 = x
                if y < y0: y0 = y
                if y > y1: y1 = y
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < w and 0 <= ny < h and not seen[ny * w + nx] and a[nx, ny] > floor:
                        seen[ny * w + nx] = 1; stack.append((nx, ny))
            if n >= amin:
                out.append([x0, y0, x1 - x0 + 1, y1 - y0 + 1])
    # reading order: band into rows by vertical overlap, then left to right
    out.sort(key=lambda b: (b[1], b[0]))
    rows, cur = [], []
    for b in out:
        if cur and b[1] > cur[-1][1] + cur[-1][3] * 0.55:
            rows.append(sorted(cur, key=lambda q: q[0])); cur = []
        cur.append(b)
    if cur: rows.append(sorted(cur, key=lambda q: q[0]))
    return [b for r in rows for b in r], len(rows)


def build(name, check):
    png = os.path.join(UI, name + '.png')
    im = Image.open(png).convert('RGBA')
    want = NAMES[name]
    rects, nrows = grid_cells(im, *GRID[name])
    status = 'OK' if len(rects) == len(want) else 'MISMATCH'
    print('%-9s %-11s %d cells in %d rows, expected %d' % (name, status, len(rects), nrows, len(want)))
    if len(rects) != len(want):
        for i, r in enumerate(rects):
            print('    %2d %s %s' % (i, r, want[i] if i < len(want) else '??'))
        if not check:
            raise SystemExit('%s: refusing to write a map whose cell count does not match its name list' % name)
        return None
    m = {
        'asset': name,
        'frame_count': len(rects),
        'alpha': 'binary',
        'atlas': {'columns': COLUMNS[name], 'rows': nrows,
                  'cell': [max(r[2] for r in rects), max(r[3] for r in rects)],
                  'rects': [{'frame': i + 1, 'x': r[0], 'y': r[1], 'w': r[2], 'h': r[3]}
                            for i, r in enumerate(rects)]},
        'items': [{'index': i + 1, 'name': want[i],
                   'source_rect': [rects[i][0], rects[i][1],
                                   rects[i][0] + rects[i][2], rects[i][1] + rects[i][3]],
                   'placement': [0, 0], 'visible_size': [rects[i][2], rects[i][3]]}
                  for i in range(len(rects))],
        'notes': 'Generated by _BUILD_SOURCE/bod_pack_map_0912f.py. Cells found by GRID slice, '
                 'then sorted into reading order and named from the prompt order. rectOf() pairs '
                 'items[i] with atlas.rects[i], so the rects are per-sprite and need not be a lattice.',
    }
    if name == 'cursors':
        for it in m['items']:
            fx, fy = HOTSPOT.get(it['name'], (0.5, 0.5))
            it['hotspot'] = [round(it['visible_size'][0] * fx), round(it['visible_size'][1] * fy)]
    if not check:
        io.open(os.path.join(UI, name + '.json'), 'w', encoding='utf-8').write(json.dumps(m, indent=1))
    return m


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--check', action='store_true'); a = ap.parse_args()
    for n in ('buttons', 'cursors', 'icons'):
        build(n, a.check)
    if a.check:
        print('\n--check: nothing written')
    else:
        print('\nmaps written to', os.path.relpath(UI, ROOT))


if __name__ == '__main__':
    main()
