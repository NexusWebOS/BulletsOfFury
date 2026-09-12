#!/usr/bin/env python3
"""
bake_mirror_frames_0908b.py — SIX SHIP FRAMES THAT WERE NEVER DRAWN.

Every pilot's br/so/pv reel is authored MIRROR-SYMMETRIC: frame 7 is the mirror of frame 1,
frame 5 the mirror of frame 3, pv3 the mirror of pv1. Measured across all nine pilots, frame 7
sits 0.03-0.08 from mirror(frame 1) -- except on five frames, where it sits 0.018-0.029 from
frame 0 instead, i.e. it is a straight copy of the LEVEL frame and the pose never happens:

    ship_decker_br7      f7~f0 0.028   f7~mir(f1) 0.127
    ship_maverick_br7    f7~f0 0.023   f7~mir(f1) 0.289
    ship_freezer_so7     f7~f0 0.029   f7~mir(f1) 0.291
    ship_juggernaut_so7  f7~f0 0.018   f7~mir(f1) 0.231
    ship_maverick_so7    f7~f0 0.022   f7~mir(f1) 0.172

and Falva's pv3 -- the shallow RIGHT bank the picker resolves on every rightward nudge -- is a
mirror of her LEVEL pv2 rather than of her pv1, so she banks left and not right.

⚠ MIRRORING IS THE CORRECT FIX HERE AND THAT IS NOT AN ASSUMPTION. It is what the other seven
pilots' own frames already are. Rendered all six mirrors before baking and checked each hull for
one-sided decals or a light direction a flip would reverse; there are none.

Placement: four of the six mirrors are SMALLER than the slot they replace, so they are cleared
and rewritten in place. Two are wider (juggernaut_so7 186->194, maverick_so7 175->189) and get a
fresh slot found by scanning the atlas for space no ships entry claims. Nothing else in the
manifest references this sheet -- checked every `cells` row -- so the ships table is the only
occupancy source that matters.

The entry is [x, y, w, h, offX, offY, canvasW, canvasH]. A horizontal flip keeps offY and turns
offX into (canvasW - offX - w); getting that wrong slides the ship sideways mid-reel.
"""
import io, json, os, sys
import numpy as np
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
MAN  = os.path.join(ROOT, 'assets/manifest.js')
PNG  = os.path.join(ROOT, 'assets/game/atlas/bof_player_ships_barrel_rolls.png')

# frame to fix  ->  the sibling whose mirror it should be
JOBS = [('ship_decker_br7',     'ship_decker_br1'),
        ('ship_maverick_br7',   'ship_maverick_br1'),
        ('ship_freezer_so7',    'ship_freezer_so1'),
        ('ship_juggernaut_so7', 'ship_juggernaut_so1'),
        ('ship_maverick_so7',   'ship_maverick_so1'),
        ('ship_falva_pv3',      'ship_falva_pv1')]

src = io.open(MAN, encoding='utf-8', newline='').read()
i = src.index('"ships"'); j = src.index('{', i); d = 0
for k in range(j, len(src)):
    if src[k] == '{': d += 1
    elif src[k] == '}':
        d -= 1
        if d == 0:
            SPAN = (j, k + 1); SHIPS = json.loads(src[j:k + 1]); break

atlas = Image.open(PNG).convert('RGBA')
AW, AH = atlas.size
print('atlas %dx%d, %d ship frames' % (AW, AH, len(SHIPS)))

# occupancy: every rect any ships entry claims, minus the six slots we are about to vacate
occ = np.zeros((AH, AW), bool)
for key, e in SHIPS.items():
    x, y, w, h = e[:4]
    occ[y:y + h, x:x + w] = True
for key, _ in JOBS:
    x, y, w, h = SHIPS[key][:4]
    occ[y:y + h, x:x + w] = False

def find_slot(w, h, pad=2):
    """topmost-leftmost free box. coarse stride first, then exact."""
    ww, hh = w + pad * 2, h + pad * 2
    integral = np.cumsum(np.cumsum(occ.astype(np.int32), 0), 1)
    def blocked(x, y):
        x2, y2 = x + ww, y + hh
        t = integral[y2 - 1, x2 - 1]
        if x: t -= integral[y2 - 1, x - 1]
        if y: t -= integral[y - 1, x2 - 1]
        if x and y: t += integral[y - 1, x - 1]
        return t > 0
    for y in range(0, AH - hh, 2):
        for x in range(0, AW - ww, 2):
            if not blocked(x, y):
                return x + pad, y + pad
    return None

changes = []
for key, ref in JOBS:
    ex, ey, ew, eh, eox, eoy, ecw, ech = SHIPS[key]
    rx, ry, rw, rh, rox, roy, rcw, rch = SHIPS[ref]
    assert (ecw, ech) == (rcw, rch), '%s and %s disagree on canvas size' % (key, ref)
    mir = atlas.crop((rx, ry, rx + rw, ry + rh)).transpose(Image.FLIP_LEFT_RIGHT)
    nox = rcw - rox - rw            # the flip moves the ink to the other side of the canvas
    if rw <= ew and rh <= eh:
        nx, ny, how = ex, ey, 'in place'
        atlas.paste((0, 0, 0, 0), (ex, ey, ex + ew, ey + eh))   # clear the whole old slot
    else:
        got = find_slot(rw, rh)
        if not got:
            print('NO ROOM for %s (%dx%d)' % (key, rw, rh)); sys.exit(1)
        nx, ny = got; how = 'new slot'
        occ[ny:ny + rh, nx:nx + rw] = True
        atlas.paste((0, 0, 0, 0), (ex, ey, ex + ew, ey + eh))
    atlas.paste(mir, (nx, ny))
    SHIPS[key] = [nx, ny, rw, rh, nox, roy, rcw, rch]
    changes.append((key, ref, '%dx%d@%d,%d' % (ew, eh, ex, ey), '%dx%d@%d,%d' % (rw, rh, nx, ny),
                    eox, nox, how))

print('%-22s %-22s %-18s %-18s %-9s %s' % ('frame', 'mirror of', 'was', 'now', 'offX', 'where'))
for k, r, a, b, o1, o2, how in changes:
    print('%-22s %-22s %-18s %-18s %3d->%-4d %s' % (k, r, a, b, o1, o2, how))

# rewrite both files, compact json exactly as the manifest already stores it
body = json.dumps(SHIPS, separators=(',', ':'), sort_keys=False)
io.open(MAN, 'w', encoding='utf-8', newline='').write(src[:SPAN[0]] + body + src[SPAN[1]:])
atlas.save(PNG)
print('wrote', PNG, 'and', MAN)
