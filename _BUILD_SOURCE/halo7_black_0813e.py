#!/usr/bin/env python3
"""
DROP 0813E - LEVEL 7'S PURPLE HALOS BECOME A BLACK EDGE

Mike: "theres still purple halo's left on level 7."

Standing rule: purple halos are CONVERTED TO A BLACK EDGE, never deleted. Alpha is untouched, so the
silhouette is identical afterwards - only the RGB under the rim changes.

WHAT IS THERE (measured by probe_halo7.py)
2,175 halo pixels across 19 nsw_ plates. The heavy ones are the level-7 shock effects:
    nsw_ring_0..3   the damaging front
    nsw_circ_0..3   the muzzle compression pulse
    nsw_dist_0..3   the trailing distortion, drawn at 50% on 'lighter'
plus two single pixels on nsw_exca_atk_0 and nsw_maw_0.

Black is the right answer here and especially for nsw_dist: on an ADDITIVE layer black contributes
nothing, so the purple fringe stops glowing without a single pixel being removed.

WHAT IS NOT TOUCHED
  - INTERIOR magenta. nsw_barge_0 (7px) and nsw_sentry_0 (8px) carry magenta inside the silhouette,
    which may be authored colour. Only pixels on the OUTER BOUNDARY are converted.
  - The RC2 masters. Their magenta is punched to ALPHA on purpose as liquid openings (game.js:2439,
    8,412px on stage 7) and nlq_sludgeF shows through it. Terrain, not a halo. Sprites only.

⚠ A KEY DOES NOT OWN ITS FILE. These are atlas CELLS: nsw_circ_0 and nsw_circ_1 both live in
nca_74.png, and nsw_dist_N / nsw_distr_N are the SAME cell under two names (identical pixel counts,
175/175, 109/109, 54/54, 50/50). Work is therefore grouped by (file, rect) and each rect is edited
exactly ONCE, and only inside its own bounds, so nothing outside these cells can be disturbed.

Writes a .bak beside every sheet it modifies. Re-running is a no-op once the purple is gone.
"""
import os, re, io, json, shutil, sys
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
MAN  = os.path.join(ROOT, 'assets', 'manifest.js')

# the plates probe_halo7.py found carrying BOUNDARY purple
KEYS = ['nsw_circ_0','nsw_circ_1','nsw_circ_2','nsw_circ_3',
        'nsw_ring_0','nsw_ring_1','nsw_ring_2','nsw_ring_3',
        'nsw_dist_0','nsw_dist_1','nsw_dist_2','nsw_dist_3',
        'nsw_distr_0','nsw_distr_1','nsw_distr_2','nsw_distr_3',
        'nsw_exca_atk_0','nsw_maw_0']

man = io.open(MAN, encoding='utf-8', errors='ignore').read()

def src_of(k):
    m = re.search(r'"%s"\s*:\s*"([^"]+\.png)"' % re.escape(k), man)
    return m.group(1) if m else None

def rect_of(k):
    """⚠ FIVE elements, not four: [sheetIndex, x, y, w, h].
       e.g. nsw_circ_0 -> [74,1170,1300,128,128] = sheet nca_74, cell at 1170,1300, 128x128.
       Reading it as [x,y,w,h] resolved every rect to None, which is the only reason the first run
       edited nothing - it refused rather than writing to a wrong rectangle of a shared sheet."""
    m = re.search(r'"%s"\s*:\s*\[(\d+),(\d+),(\d+),(\d+),(\d+)\]' % re.escape(k), man)
    if not m: return None
    g = [int(v) for v in m.groups()]
    return (g[1], g[2], g[3], g[4])

def is_purple(r, g, b, a):
    return a >= 40 and r > 90 and b > 90 and g < min(r, b) * 0.62

groups = {}          # (file, rect) -> [keys]
missing = []
for k in KEYS:
    f, r = src_of(k), rect_of(k)
    if not f or not r:
        missing.append((k, f, r)); continue
    groups.setdefault((f, r), []).append(k)

if missing:
    print('could not resolve file+rect for:')
    for k, f, r in missing: print('   %-18s file=%s rect=%s' % (k, f, r))

print('%d key(s) -> %d unique cell(s)' % (len(KEYS) - len(missing), len(groups)))

by_file = {}
for (f, r), ks in groups.items():
    by_file.setdefault(f, []).append((r, ks))

total = 0
for f, cells in sorted(by_file.items()):
    path = os.path.join(ROOT, f.replace('/', os.sep))
    if not os.path.isfile(path):
        print('*** missing sheet %s' % f); continue
    im = Image.open(path).convert('RGBA')
    px = im.load()
    W, H = im.size
    changed_here = 0
    for (x0, y0, cw, ch), ks in cells:
        x1, y1 = min(x0 + cw, W), min(y0 + ch, H)
        n = 0
        for y in range(y0, y1):
            for x in range(x0, x1):
                r, g, b, a = px[x, y]
                if not is_purple(r, g, b, a): continue
                # boundary = touches transparency, or the edge of its OWN cell
                edge = False
                for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
                    nx, ny = x + dx, y + dy
                    if nx < x0 or ny < y0 or nx >= x1 or ny >= y1 or px[nx, ny][3] < 40:
                        edge = True; break
                if edge:
                    px[x, y] = (0, 0, 0, a)      # black EDGE - alpha preserved, nothing deleted
                    n += 1
        if n:
            print('   %-28s %4d px  (%s)' % (f.split('/')[-1] + ' @%d,%d' % (x0, y0), n, ','.join(ks)))
        changed_here += n
    if changed_here:
        bak = path + '.bak'
        if not os.path.exists(bak): shutil.copy2(path, bak)
        im.save(path)
        print('%-30s %d px -> black   (backup %s)' % (f, changed_here, os.path.basename(bak)))
    total += changed_here

print('\n%d halo pixel(s) converted to a black edge' % total)
if total == 0:
    print('(nothing to do - already converted, or the selector no longer matches)')
