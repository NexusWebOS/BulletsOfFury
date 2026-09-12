#!/usr/bin/env python3
"""
split_ship_atlas_per_pilot_0909.py - ONE SHIP SHEET PER PILOT.

Mike, 0909: "you need to make seperate atlas sheets for all nine pilots ships, with their
thrusters ... this will cut down on memory loading drastically as you load whichever atlas needed
into the memory and no need to have the other 8 or 7 if co-op when not in use."

Today every pilot's ship lives in ONE 4096x3502 sheet, bof_player_ships_barrel_rolls.png, 11 MB,
and it is in PRELOAD - so booting the game downloads and decodes all nine aircraft before the
player can act, whichever one they end up flying. Measured ink, by pilot:

    axel 1.33 Mp   cole 1.43   decker 1.33   falva 1.50   freezer 1.09
    juggernaut 1.47   lizzie 1.58   maverick 1.26   yuri 1.35      total 11.72 Mp

so a single-player run needs about a ninth of what it loads.

WHAT IS IN EACH SHEET. Everything that pilot owns: the flight frames and their baked thruster
phases, the pivot/bank ladder, the barrel roll, the somersault and the spin-out. Nothing is
dropped. Measured share of the fleet total, if the reels are ever worth splitting out again:

    flight 18%   bank 34%   roll 13%   somersault 17%   spin 18%

⚠ LIZZIE'S SHEET CARRIES 66 CELLS, NOT 49, AND MISSING THAT WOULD HAVE BROKEN HER COSTUME.
`LIZZIE_B42_RECTS` in game.js is a SECOND consumer of this sheet - seventeen hardcoded rects for
the B-42 bomber behind the BOMBER password - and `applyLizzieSkin` swaps them into `BOFX.ships`
at runtime. 0906z's compaction moved every ship rect without touching them and left the costume
resolving to fragments of Cole's, Freezer's and Maverick's aircraft for a whole drop, with
nothing failing. Both rect sets are packed here and both are rewritten.

⚠ AND THE SOURCE OF TRUTH IS THE TABLE IN game.js, NOT THE JSON BESIDE IT. The first run of this
script trusted assets/data/lizzie_b42_source_rects.json on 0907u's word. The two DISAGREE, and
the json is the stale one - see the note at the parse below. It is rewritten as a derived record
so they stop disagreeing, and this build refuses to run twice because the rects it writes name a
per-pilot sheet rather than the combined atlas it reads.

⚠ AND THE SHEET IS NOT NAMED IN THE ROW. `BOFX.ships` rows stay 8 wide - [x,y,w,h,offX,offY,
canvasW,canvasH] - and the sheet is derived from the KEY, because every ship key is
ship_<pilot> or ship_<pilot>_<suffix>. Adding a ninth element would have meant finding every
consumer of the row shape, and there is provably more than one of those.

Verification is a byte compare: every cell is cropped from the OLD sheet and from the NEW one and
the two must be identical. A count cannot see a rect that moved by a pixel.
"""
import io, json, os, re, sys
import numpy as np
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
MAN = os.path.join(ROOT, 'assets/manifest.js')
GAME = os.path.join(ROOT, 'assets/game.js')
OLD = os.path.join(ROOT, 'assets/game/atlas/bof_player_ships_barrel_rolls.png')
B42 = os.path.join(ROOT, 'assets/data/lizzie_b42_source_rects.json')
OUTDIR = os.path.join(ROOT, 'assets/game/atlas/ships')
PILOTS = ['axel', 'cole', 'decker', 'falva', 'freezer', 'juggernaut', 'lizzie', 'maverick', 'yuri']
PAD = 2

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

# WARNING: THE SOURCE OF TRUTH IS THE TABLE IN game.js, NOT THE JSON BESIDE IT.
# The first run of this script trusted assets/data/lizzie_b42_source_rects.json because 0907u
# called it the source of truth. The two DISAGREE: rendered side by side out of the same atlas,
# the game.js table gives an intact yellow warbird on 15 of 17 frames and the json gives
# fragments of Axel's, Falva's, Yuri's and Cole's aircraft on almost all of them. The json is
# stale. game.js is what the game reads, so game.js is what gets packed; the json is rewritten
# as a DERIVED record afterwards so the two stop disagreeing.
b42 = {}
_g0 = io.open(GAME, encoding='utf-8', newline='').read()
_st0 = _g0.index('const LIZZIE_B42_RECTS={')
for _m in re.finditer(r'"([^"]*)":\[([0-9,\s]+)\]', _g0[_st0:_g0.index('};', _st0) + 2]):
    b42[_m.group(1)] = [int(v) for v in _m.group(2).split(',')]
if len(b42) != 17:
    print('expected 17 B-42 rects in game.js, parsed %d' % len(b42))
    sys.exit(1)

# and refuse to run twice: after a split those rects name a PER-PILOT sheet, so a second pass
# would crop the new coordinates out of the old atlas - 0907u's "a script that consumes its own
# output is not idempotent", which cost that drop two silently worse runs.
if os.path.isdir(OUTDIR) and '--force' not in sys.argv:
    print('ABORT - %s already exists. This build is not idempotent: rerun it only from a tree' % OUTDIR)
    print('        whose LIZZIE_B42_RECTS still name the combined atlas. --force to override.')
    sys.exit(1)

atlas = Image.open(OLD).convert('RGBA')

# what goes in each sheet: (unique id, source rect, pilot)
items = {p: [] for p in PILOTS}
for key, e in SHIPS.items():
    m = re.match(r'ship_([a-z]+)(?:_.+)?$', key)
    if not m or m.group(1) not in items:
        print('UNPLACEABLE KEY ' + key)
        sys.exit(1)
    items[m.group(1)].append(('ships:' + key, e))
for suf, e in b42.items():
    items['lizzie'].append(('b42:' + suf, e))


def pack(rects, pad=PAD):
    """shelf pack, tallest first, into a width chosen from the total area"""
    area = sum((w + pad * 2) * (h + pad * 2) for _, w, h in rects)
    W = max(256, int((area * 1.18) ** 0.5))
    W = 1 << (W - 1).bit_length() if W <= 4096 else 4096
    order = sorted(rects, key=lambda r: -r[2])
    placed = {}
    x = y = rowh = 0
    for name, w, h in order:
        ww, hh = w + pad * 2, h + pad * 2
        if x + ww > W:
            x = 0
            y += rowh
            rowh = 0
        placed[name] = (x + pad, y + pad)
        x += ww
        rowh = max(rowh, hh)
    H = y + rowh
    return W, H, placed


os.makedirs(OUTDIR, exist_ok=True)
newships = dict(SHIPS)
newb42 = {}
report = []
for p in PILOTS:
    rects = [(nm, e[2], e[3]) for nm, e in items[p]]
    W, H, placed = pack(rects)
    sheet = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    for nm, e in items[p]:
        sx, sy, w, h = e[0], e[1], e[2], e[3]
        nx, ny = placed[nm]
        sheet.paste(atlas.crop((sx, sy, sx + w, sy + h)), (nx, ny))
        row = [nx, ny, w, h, e[4], e[5], e[6], e[7]]
        if nm.startswith('ships:'):
            newships[nm[6:]] = row
        else:
            newb42[nm[4:]] = row
    out = os.path.join(OUTDIR, 'ship_%s.png' % p)
    sheet.save(out)
    report.append((p, len(items[p]), '%dx%d' % (W, H), os.path.getsize(out) / 1e6))

print('%-12s %-7s %-12s %s' % ('pilot', 'cells', 'sheet', 'MB'))
for r in report:
    print('%-12s %-7d %-12s %.2f' % r)
print('%-12s %-7d %-12s %.2f' % ('TOTAL', sum(r[1] for r in report), '', sum(r[3] for r in report)))
print('was: one sheet, %d cells, 4096x3502, %.2f MB' % (len(SHIPS), os.path.getsize(OLD) / 1e6))

# ---- verify every cell byte for byte before anything is written back ----
bad = []
sheets = {p: Image.open(os.path.join(OUTDIR, 'ship_%s.png' % p)).convert('RGBA') for p in PILOTS}
for key, e in SHIPS.items():
    p = re.match(r'ship_([a-z]+)', key).group(1)
    n = newships[key]
    a = np.array(atlas.crop((e[0], e[1], e[0] + e[2], e[1] + e[3])))
    b = np.array(sheets[p].crop((n[0], n[1], n[0] + n[2], n[1] + n[3])))
    if a.shape != b.shape or not np.array_equal(a, b):
        bad.append(key)
for suf, e in b42.items():
    n = newb42[suf]
    a = np.array(atlas.crop((e[0], e[1], e[0] + e[2], e[1] + e[3])))
    b = np.array(sheets['lizzie'].crop((n[0], n[1], n[0] + n[2], n[1] + n[3])))
    if a.shape != b.shape or not np.array_equal(a, b):
        bad.append('b42' + suf)
if bad:
    print('ABORT - %d cells did not survive the repack: %s' % (len(bad), ', '.join(bad[:10])))
    sys.exit(1)
print('verify: all %d cells byte-identical to the old sheet' % (len(SHIPS) + len(b42)))

if '--dry' in sys.argv:
    print('dry run, nothing written back')
    sys.exit(0)

# ---- manifest: new rects, and register the nine sheets ----
body = json.dumps(newships, separators=(',', ':'), sort_keys=False)
src2 = src[:SPAN[0]] + body + src[SPAN[1]:]
reg = ''.join('"nsa_ship_%s":"assets/game/atlas/ships/ship_%s.png",' % (p, p) for p in PILOTS)
anchor = '"nsa_ships":"assets/game/atlas/bof_player_ships_barrel_rolls.png",'
assert src2.count(anchor) == 1, src2.count(anchor)
src2 = src2.replace(anchor, reg + anchor)
io.open(MAN, 'w', encoding='utf-8', newline='').write(src2)
print('wrote ' + MAN)

# ---- game.js: the B-42 table, and the json it comes from ----
io.open(B42, 'w', encoding='utf-8', newline='\n').write(json.dumps(newb42, indent=1) + '\n')
g = io.open(GAME, encoding='utf-8', newline='').read()
nl = '\r\n' if '\r\n' in g[:20000] else '\n'
st = g.index('const LIZZIE_B42_RECTS={')
en = g.index('};', st) + 2
lines = ['const LIZZIE_B42_RECTS={']
for suf, r in newb42.items():
    lines.append('  %s:%s,' % (json.dumps(suf), json.dumps(r, separators=(',', ','))))
lines.append('};')
g = g[:st] + nl.join(lines) + g[en:]
io.open(GAME, 'w', encoding='utf-8', newline='').write(g)
print('wrote ' + GAME + '  (LIZZIE_B42_RECTS, %d rects)' % len(newb42))
print('wrote ' + B42)
