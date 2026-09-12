#!/usr/bin/env python3
"""
import_roll_pack_0909.py - THE RESOLUTION PACK'S BARREL ROLLS, ALL NINE PILOTS.

Mike, 0909: "here ye here ye. the resolution pack! use these for all pilots!" and, on the picks,
"You pick. palette swap lizzie's brown to be more Golden, the white remains."

Ship_All_Generations.zip is 105 unnamed PNGs - 93 ship sheets plus 12 FX. Nothing in it says which
pilot or which move, so every sheet was classified before anything was cut:

  PILOT   by palette against each pilot's in-game hull (hue+value histogram, L1 distance).
          WARNING: A SILHOUETTE CHECK WAS TRIED AND THROWN OUT. It disagreed with the palette on
          42 of 105 sheets, and it was the check that was wrong: these are REDESIGNED hulls, so
          matching them against the old outlines tests the one thing that is meant to have changed.

  MOVE    by the reel's own width/height profile. A barrel roll narrows to edge-on twice and keeps
          its height; a somersault keeps its width and loses height at nose-on and tail-on. The 26
          eight-frame sheets split cleanly: 20 rolls, 4 somersaults, 3 flat spins.

The pack holds a complete ROLL set for all nine pilots (each narrows to 22-37% of its width, so it
genuinely goes edge-on) but somersaults for only three and no five-frame lean reels, so only the
rolls are imported here. Picks are the deepest edge-on of each pilot's candidates.

FRAME ORDER IS NOT ASSUMED. Every sheet's measured width profile is wide/mid/NARROW/mid/wide/mid/
NARROW/mid in reading order, which is exactly br0..br7 with the edge-on twist frames landing on
br2 and br6 - where _shipFrameKey already looks for them. Asserted below, not trusted.

PLACEMENT. The old reels deliberately move the ship between frames (axel's centre swings 42px), so
frames are NOT centred. Each frame keeps its own offset from its source cell's centre, expressed as
a fraction of the cell and reapplied to the pilot's existing canvas. The canvas is fixed and the art
shrinks to fit it: growing canvasW/canvasH would change the unit the draw scales against and quietly
shrink the ship on screen. Size is safe to lose because every pilot is normalised on CONTENT height,
not canvas.

LIZZIE IS RECOLOURED, and the constants are solved rather than picked - see lizzie_goldify_0909.py.
"""
import io, json, os, re, sys
import numpy as np
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lizzie_goldify_0909 import goldify

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
MAN  = os.path.join(ROOT, 'assets/manifest.js')
PNG  = os.path.join(ROOT, 'assets/game/atlas/bof_player_ships_barrel_rolls.png')
PACK = sys.argv[1] if len(sys.argv) > 1 else None
if not PACK or not os.path.isdir(PACK):
    print('usage: import_roll_pack_0909.py <dir with the unzipped Generations pngs>')
    sys.exit(1)

PICK = {'axel': 'exec-47d817b5', 'cole': 'exec-e93fdc24', 'decker': 'exec-3ee96fc9',
        'falva': 'exec-5810d9cb', 'freezer': 'exec-b494429a', 'juggernaut': 'exec-1a5f04b6',
        'lizzie': 'exec-bc397a2e', 'maverick': 'exec-b31bea74', 'yuri': 'exec-df6338fd'}
COLS, ROWS = 4, 2

src = io.open(MAN, encoding='utf-8', newline='').read()
i = src.index('"ships"')
j = src.index('{', i)
d = 0
for k in range(j, len(src)):
    if src[k] == '{':
        d += 1
    elif src[k] == '}':
        d -= 1
        if d == 0:
            SPAN = (j, k + 1)
            SHIPS = json.loads(src[j:k + 1])
            break
atlas = Image.open(PNG).convert('RGBA')
AW, AH = atlas.size


def key_bg(a):
    """magenta or cyan sheet background -> alpha. Whichever covers more of the plate wins."""
    rgb = a[:, :, :3].astype(int)
    if a.shape[2] == 4 and a[:, :, 3].min() < 10:
        return a.copy()
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    mag = (r > 150) & (b > 150) & (g < 130)
    cya = (g > 150) & (b > 150) & (r < 130)
    bg = mag if mag.mean() > cya.mean() else cya
    return np.dstack([rgb, np.where(bg, 0, 255)]).astype(np.uint8)


def find(prefix):
    for f in sorted(os.listdir(PACK)):
        if f.startswith(prefix):
            return os.path.join(PACK, f)
    raise SystemExit('missing sheet ' + prefix)


# occupancy of everything the ships table claims, minus the reels we are replacing
occ = np.zeros((AH, AW), bool)
for key, e in SHIPS.items():
    x, y, w, h = e[:4]
    occ[y:y + h, x:x + w] = True

# WARNING: BOFX.ships IS NOT THE ONLY CONSUMER OF THIS SHEET, AND THE FIRST RUN OF THIS SCRIPT
# LEARNED THAT THE EXPENSIVE WAY. LIZZIE_B42_RECTS in game.js is seventeen hardcoded rects for
# the B-42 bomber behind the BOMBER password - art that was APPENDED to this atlas and is
# referenced from nowhere in the manifest. Building occupancy from the ships table alone left
# that strip flagged free, find_slot handed its pixels to the new reels, and TEN OF THE
# SEVENTEEN frames were written over: her costume became fragments of Juggernaut's, Freezer's
# and Maverick's aircraft, with nothing failing and no manifest key to notice it.
# This is CLAUDE.md's own rule, self-inflicted: enumerate the consumers of a SHEET, not the rows
# of one table that points at it. The check at the end of this file now refuses the write if any
# B-42 pixel moves.
B42_RECTS = {}
_g = io.open(os.path.join(ROOT, 'assets/game.js'), encoding='utf-8', newline='').read()
_st = _g.index('const LIZZIE_B42_RECTS={')
for _m in re.finditer(r'"([^"]*)":\[([0-9,\s]+)\]', _g[_st:_g.index('};', _st) + 2]):
    B42_RECTS[_m.group(1)] = [int(v) for v in _m.group(2).split(',')]
if len(B42_RECTS) != 17:
    print('expected 17 B-42 rects, parsed %d' % len(B42_RECTS))
    sys.exit(1)
for e in B42_RECTS.values():
    x, y, w, h = e[:4]
    occ[y:y + h, x:x + w] = True

for p in PICK:
    for q in range(8):
        x, y, w, h = SHIPS['ship_%s_br%d' % (p, q)][:4]
        occ[y:y + h, x:x + w] = False


def find_slot(w, h, pad=2):
    ww, hh = w + pad * 2, h + pad * 2
    integ = np.cumsum(np.cumsum(occ.astype(np.int32), 0), 1)

    def blocked(x, y):
        x2, y2 = x + ww, y + hh
        t = integ[y2 - 1, x2 - 1]
        if x:
            t -= integ[y2 - 1, x - 1]
        if y:
            t -= integ[y - 1, x2 - 1]
        if x and y:
            t += integ[y - 1, x - 1]
        return t > 0

    for y in range(0, AH - hh, 2):
        for x in range(0, AW - ww, 2):
            if not blocked(x, y):
                return x + pad, y + pad
    return None


def grow(rows_needed):
    """Append blank rows. Reserving the B-42 strip correctly makes the sheet too tight for one
    frame, and squeezing is what caused the damage in the first place - so the sheet grows
    instead. It is temporary either way: the per-pilot split repacks all of this from scratch."""
    global atlas, occ, AH
    bigger = Image.new('RGBA', (AW, AH + rows_needed), (0, 0, 0, 0))
    bigger.paste(atlas, (0, 0))
    atlas = bigger
    occ = np.vstack([occ, np.zeros((rows_needed, AW), bool)])
    AH += rows_needed
    print('grew the sheet to %dx%d to place the last frames' % (AW, AH))


rows = []
pend = []
for p, pref in PICK.items():
    a = np.array(Image.open(find(pref)).convert('RGBA'))
    kk = key_bg(a)
    H, W = kk.shape[:2]
    cw, chh = W / COLS, H / ROWS
    # WARNING: AN EQUAL 4x2 GRID DOES NOT CUT THESE SHEETS. The generator did not centre every
    # ship in its cell, so axel's edge-on frame straddles a boundary and a fixed grid sliced it
    # into a 242px lump of two neighbours instead of a 79px sliver - which the edge-on assertion
    # below caught. Frames are cut on DETECTED ink runs, which is reliable, and the regular grid
    # is kept only as the reference the per-frame offset is measured against: each run is assigned
    # to the cell whose centre it is nearest, and fx/fy is its deviation from that centre. That
    # keeps the inter-frame motion the artist drew instead of flattening it to centre.
    m = kk[:, :, 3] > 40

    def runs(v, minlen=18):
        out, on = [], None
        for i2, x in enumerate(v):
            if x and on is None:
                on = i2
            elif not x and on is not None:
                if i2 - on > minlen:
                    out.append((on, i2 - 1))
                on = None
        if on is not None and len(v) - on > minlen:
            out.append((on, len(v) - 1))
        return out

    cruns, rruns = runs(m.any(axis=0)), runs(m.any(axis=1))
    assert len(cruns) == COLS and len(rruns) == ROWS, \
        '%s: found a %dx%d layout, expected %dx%d' % (p, len(cruns), len(rruns), COLS, ROWS)
    frames = []
    for ri, (y0, y1) in enumerate(rruns):
        for ci, (x0, x1) in enumerate(cruns):
            cell = kk[y0:y1 + 1, x0:x1 + 1]
            ys, xs = np.where(cell[:, :, 3] > 40)
            if len(xs) < 40:
                continue
            ink = cell[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
            cx = x0 + (xs.min() + xs.max() + 1) / 2.0
            cy = y0 + (ys.min() + ys.max() + 1) / 2.0
            fx = (cx - (ci + 0.5) * cw) / cw
            fy = (cy - (ri + 0.5) * chh) / chh
            frames.append((ink, fx, fy))
    assert len(frames) == 8, '%s cut %d frames, expected 8' % (p, len(frames))
    ws = [f[0].shape[1] for f in frames]
    assert ws[2] < ws[0] * 0.45 and ws[6] < ws[4] * 0.45, \
        '%s: frames 2 and 6 are not the edge-on pair (%s)' % (p, ws)
    if p == 'lizzie':
        frames = [(goldify(f)[0], fx, fy) for f, fx, fy in frames]

    old0 = SHIPS['ship_%s_br0' % p]
    CW, CH = old0[6], old0[7]

    def layout(sc):
        out = []
        for ink, fx, fy in frames:
            w2 = max(1, int(round(ink.shape[1] * sc)))
            h2 = max(1, int(round(ink.shape[0] * sc)))
            out.append((w2, h2,
                        int(round(CW / 2.0 + fx * CW - w2 / 2.0)),
                        int(round(CH / 2.0 + fy * CH - h2 / 2.0))))
        return out

    def fits(L):
        return all(ox >= 0 and oy >= 0 and ox + w <= CW and oy + h <= CH for w, h, ox, oy in L)

    scale = old0[3] / float(frames[0][0].shape[0])
    while scale > 0.05 and not fits(layout(scale)):
        scale -= 0.002
    L = layout(scale)

    for q in range(8):
        w2, h2, ox, oy = L[q]
        pend.append(['ship_%s_br%d' % (p, q), frames[q][0], w2, h2, ox, oy, CW, CH])
    rows.append((p, pref[5:13], '%.3f' % scale, '%dx%d' % (L[0][0], L[0][1]),
                 '%dx%d' % (old0[2], old0[3]), '%dx%d' % (CW, CH)))

# WARNING: RESERVE EVERYTHING BEFORE ALLOCATING ANYTHING.
# The first two runs decided placement pilot by pilot, and both handed the same pixels out twice.
# Run one never marked the in-place case at all - a frame that fitted its old rect stayed flagged
# FREE, all 72 having been freed up front - so in game Lizzie rolled through Maverick's teal hull
# and Yuri's red one. Run two marked it, but too late: yuri's br0 sat in-place on a rect that
# lizzie's br7 had already been handed by find_slot, because lizzie is processed first.
# Both are the same mistake, so both passes are now separated: every frame that can stay in its
# own rect claims it FIRST, and only then does find_slot look for space for the rest.
# A per-key content hash does NOT catch this - both keys read as "changed", which is exactly what
# is expected of them. The disjointness check at the end of this file is what catches it.
for it in pend:
    key, _, w2, h2 = it[0], it[1], it[2], it[3]
    ex, ey, ew, eh = SHIPS[key][:4]
    if w2 <= ew and h2 <= eh:
        it.append((ex, ey))
        occ[ey:ey + h2, ex:ex + w2] = True
    else:
        it.append(None)
for it in pend:
    if it[-1] is None:
        got = find_slot(it[2], it[3])
        if not got:
            grow(it[3] + 8)
            got = find_slot(it[2], it[3])
        if not got:
            print('NO ROOM for ' + it[0])
            sys.exit(1)
        it[-1] = got
        occ[got[1]:got[1] + it[3], got[0]:got[0] + it[2]] = True

# clear every old rect BEFORE pasting, or a frame placed inside a rect still to be cleared is erased
for it in pend:
    ex, ey, ew, eh = SHIPS[it[0]][:4]
    atlas.paste((0, 0, 0, 0), (ex, ey, ex + ew, ey + eh))
for key, ink, w2, h2, ox, oy, CW, CH, (nx, ny) in pend:
    atlas.paste(Image.fromarray(ink, 'RGBA').resize((w2, h2), Image.LANCZOS), (nx, ny))
    SHIPS[key] = [nx, ny, w2, h2, ox, oy, CW, CH]

print('%-12s %-10s %-7s %-12s %-12s %s' % ('pilot', 'sheet', 'scale', 'new br0', 'old br0', 'canvas'))
for r in rows:
    print('%-12s %-10s %-7s %-12s %-12s %s' % r)

# NOT ONE B-42 PIXEL MAY MOVE. The bomber has no manifest key, so nothing else in the pipeline
# can notice it being overwritten - this is the only thing standing between a reel import and
# Lizzie's costume becoming other pilots' wreckage again.
_before = Image.open(PNG).convert('RGBA')
_hurt = []
for _k, _e in B42_RECTS.items():
    _box = (_e[0], _e[1], _e[0] + _e[2], _e[1] + _e[3])
    if not np.array_equal(np.array(_before.crop(_box)), np.array(atlas.crop(_box))):
        _hurt.append(_k or '(base)')
if _hurt:
    print('ABORT - the pack overwrote %d B-42 frames: %s' % (len(_hurt), ', '.join(_hurt)))
    sys.exit(1)
print('B-42 check: all 17 costume frames untouched')

# NO TWO SHIP CELLS MAY SHARE A PIXEL. Cheap, and it is the check that would have caught the
# in-place occupancy bug above on the first run instead of in a screenshot.
stamp = np.zeros((AH, AW), np.int32)
clash = []
for idx, (key, e) in enumerate(sorted(SHIPS.items()), start=1):
    x, y, w, h = e[:4]
    reg = stamp[y:y + h, x:x + w]
    hit = np.unique(reg[reg > 0])
    if hit.size:
        clash.append(key)
    reg[:] = idx
if clash:
    print('ABORT - %d ship cells overlap another: %s' % (len(clash), ', '.join(sorted(clash)[:12])))
    sys.exit(1)
print('overlap check: all %d ship cells are disjoint' % len(SHIPS))

body = json.dumps(SHIPS, separators=(',', ':'), sort_keys=False)
io.open(MAN, 'w', encoding='utf-8', newline='').write(src[:SPAN[0]] + body + src[SPAN[1]:])
atlas.save(PNG)
print('')
print('wrote ' + PNG)
print('wrote ' + MAN)
