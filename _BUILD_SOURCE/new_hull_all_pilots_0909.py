#!/usr/bin/env python3
"""
new_hull_all_pilots_0909.py - THE OTHER EIGHT PILOTS FLY THE PACK HULL TOO.

Mike, 0909: "use these for all pilots! they are clean and fixed boss!", and on Lizzie's frames:
"those should be the commited final versions and look of Lizzie's ship."

The resolution pack gave every pilot a barrel ROLL and nothing else, so eight of the nine have been
flying the OLD airframe in level flight and the NEW one the instant they roll - the ship changes
design mid-manoeuvre. Lizzie was converted first, on his explicit call; this does the same for the
rest, by the same route that needed no new art:

  FLIGHT  idle / _nf / _l / _r   -> the roll reel's own frames. br0 IS the level view, br1 and br7
                                    the shallow banks either side.
  BANK    _pv0.._pv4             -> aliased onto the roll: pv2=br0 level, pv1/pv3 the shallow leans,
                                    pv0/pv4 the edge-on ends. Which of br1/br7 is LEFT depends on
                                    the pilot: SHIP_TWIST_FLIP names axel, decker and juggernaut as
                                    authored the other way round, so their mapping is mirrored.
                                    Getting that backwards banks a pilot into the wrong lean, which
                                    0903y already records as a real shipped bug.
  SPIN    _sp0.._sp7             -> rebuilt by rotating the new level plate 45 degrees a step.
                                    CLAUDE.md licenses image-plane rotation for the spin-out only.
  GLOW    _g1/_g2 on the above   -> deleted; the pack has no phase art, and shipGlowKey falls back
                                    to the base frame when a phase is absent.

⚠ THE SOMERSAULT IS KEPT, UNLIKE LIZZIE'S. Hers went because Mike asked for the old-hull variants
to be deleted outright. Nobody has asked that for the other eight, and deleting so0..so7 would take
the move away from all of them - somersaultAvailable() gates on the art. So they keep an old-hull
somersault: a mismatch that shows only during a triggered move, which is strictly better than
losing the move. It is the one place these eight still differ from her.

⚠ THE pv KEYS ARE ALIASED, NOT DELETED. On Lizzie that was load-bearing because applyLizzieSkin
skips a missing stock rect and would have stranded her costume's pv rects. The other eight have no
costume, but the same shape of bug is one feature away, and an alias costs nothing.

Every surviving cell is byte-compared after the repack, and each pilot's sheet is rebuilt from
scratch so the retired art does not sit in the download.
"""
import io, json, os, re, sys
import numpy as np
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
MAN = os.path.join(ROOT, 'assets/manifest.js')
GAME = os.path.join(ROOT, 'assets/game.js')
SHIPS_DIR = os.path.join(ROOT, 'assets/game/atlas/ships')
PILOTS = ['axel', 'cole', 'decker', 'falva', 'freezer', 'juggernaut', 'maverick', 'yuri']
PAD = 2

g = io.open(GAME, encoding='utf-8', newline='').read()
# WARNING: THERE ARE TWO FLIP TABLES AND USING ONE FOR BOTH JOBS IS A REAL SHIPPED BUG.
# game.js says it outright: "`right` is for the LEAN reel and `rightBr` for the TWIST reel - they
# agree for six of the nine pilots and must not be collapsed back into one flag."
#   SHIP_TWIST_FLIP {axel, decker, juggernaut}  - which br frames are that pilot's right-hand pair
#   SHIP_BANK_FLIP  {axel, decker, freezer}     - which pv SLOTS the right-hand art belongs in
# They differ on FREEZER and JUGGERNAUT. The first cut of this script used the twist table for
# both and put those two pilots' leans backwards - caught by driving _shipFrameKey across the bank
# range and seeing axel answer pv4 for NEGATIVE bank, which is the opposite of the slot names.
def _flip(name):
    mm = re.search(r'const ' + name + r'=\{([^}]*)\}', g)
    if not mm:
        print(name + ' not found')
        sys.exit(1)
    return set(re.findall(r'(\w+)\s*:\s*1', mm.group(1)))
TWIST = _flip('SHIP_TWIST_FLIP')
BANK = _flip('SHIP_BANK_FLIP')
print('SHIP_TWIST_FLIP:', ', '.join(sorted(TWIST)))
print('SHIP_BANK_FLIP :', ', '.join(sorted(BANK)))
print('they differ on :', ', '.join(sorted(TWIST ^ BANK)) or 'nothing')

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

rows = []
newships = dict(SHIPS)
for p in PILOTS:
    K = lambda s: 'ship_%s%s' % (p, s)
    # which br frames depict a RIGHT-hand bank, from the TWIST table
    if p in TWIST:
        Rs, Rd, Ls, Ld = '_br1', '_br2', '_br7', '_br6'
    else:
        Rs, Rd, Ls, Ld = '_br7', '_br6', '_br1', '_br2'
    # which pv SLOTS the right-hand art goes in, from the BANK table. Holding the right key gives
    # a positive bank; `right` is (bank>0) normally and (bank<0) for a BANK_FLIP pilot, and the
    # picker reads pv3/pv4 when `right` is true - so on a flipped pilot the right-hand art has to
    # live in pv1/pv0 instead, or they lean the wrong way.
    if p in BANK:
        pv_shallow_R, pv_deep_R, pv_shallow_L, pv_deep_L = '_pv1', '_pv0', '_pv3', '_pv4'
    else:
        pv_shallow_R, pv_deep_R, pv_shallow_L, pv_deep_L = '_pv3', '_pv4', '_pv1', '_pv0'
    ALIAS = {'': '_br0', '_nf': '_br0', '_l': Ls, '_r': Rs, '_pv2': '_br0',
             pv_shallow_R: Rs, pv_deep_R: Rd, pv_shallow_L: Ls, pv_deep_L: Ld}
    DROP = [s + q for s in ['', '_l', '_r', '_pv0', '_pv1', '_pv2', '_pv3', '_pv4']
            for q in ('_g1', '_g2')]
    REGEN = ['_sp%d' % q for q in range(8)]

    sheet_path = os.path.join(SHIPS_DIR, 'ship_%s.png' % p)
    old = Image.open(sheet_path).convert('RGBA')
    lvl = SHIPS[K('_br0')]
    lvlimg = old.crop((lvl[0], lvl[1], lvl[0] + lvl[2], lvl[1] + lvl[3]))
    CW, CH = lvl[6], lvl[7]

    spin = []
    for q in range(8):
        rot = lvlimg.rotate(-45 * q, resample=Image.NEAREST, expand=True)
        aa = np.array(rot)
        ys, xs = np.where(aa[:, :, 3] > 40)
        rot = rot.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
        if rot.width > CW or rot.height > CH:
            f = min(CW / rot.width, CH / rot.height)
            rot = rot.resize((max(1, int(rot.width * f)), max(1, int(rot.height * f))), Image.LANCZOS)
        spin.append(rot)

    suffixes = [k.replace('ship_%s' % p, '') for k in SHIPS if k.startswith('ship_%s' % p)]
    keep = [s for s in suffixes if s not in DROP and s not in ALIAS and s not in REGEN]
    items = []
    for s in sorted(keep):
        e = SHIPS[K(s)]
        items.append(('ships:' + K(s), old.crop((e[0], e[1], e[0] + e[2], e[1] + e[3])), e[4], e[5]))
    for q, im in enumerate(spin):
        items.append(('ships:' + K('_sp%d' % q), im, (CW - im.width) // 2, (CH - im.height) // 2))

    area = sum((im.width + PAD * 2) * (im.height + PAD * 2) for _, im, _, _ in items)
    W = 1 << (max(256, int((area * 1.18) ** 0.5)) - 1).bit_length()
    placed, x, y, rowh = {}, 0, 0, 0
    for nm, im, _, _ in sorted(items, key=lambda t: -t[1].height):
        ww, hh = im.width + PAD * 2, im.height + PAD * 2
        if x + ww > W:
            x, y, rowh = 0, y + rowh, 0
        placed[nm] = (x + PAD, y + PAD)
        x += ww
        rowh = max(rowh, hh)
    H = y + rowh

    out = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    for s in DROP:
        newships.pop(K(s), None)
    for nm, im, ox, oy in items:
        nx, ny = placed[nm]
        out.paste(im, (nx, ny))
        newships[nm[6:]] = [nx, ny, im.width, im.height, ox, oy, CW, CH]
    for s, tgt in ALIAS.items():
        newships[K(s)] = list(newships[K(tgt)])
    out.save(sheet_path)

    chk = Image.open(sheet_path).convert('RGBA')
    bad = []
    for s in sorted(keep):
        o, n = SHIPS[K(s)], newships[K(s)]
        a1 = np.array(old.crop((o[0], o[1], o[0] + o[2], o[1] + o[3])))
        b1 = np.array(chk.crop((n[0], n[1], n[0] + n[2], n[1] + n[3])))
        if a1.shape != b1.shape or not np.array_equal(a1, b1):
            bad.append(K(s))
    for s, tgt in ALIAS.items():
        if newships[K(s)] != newships[K(tgt)]:
            bad.append('alias ' + p + s)
    if bad:
        print('ABORT on %s - %d cells wrong: %s' % (p, len(bad), ', '.join(bad[:6])))
        sys.exit(1)
    rows.append((p, ('twist' if p in TWIST else '-')+'/'+('bank' if p in BANK else '-'), len(suffixes),
                 len([k for k in newships if k.startswith('ship_%s' % p)]),
                 '%dx%d' % (W, H), os.path.getsize(sheet_path) / 1e6))

print()
print('%-12s %-10s %-12s %-12s %s' % ('pilot', 'flips', 'keys before', 'keys after', 'sheet / MB'))
for r in rows:
    print('%-12s %-10s %-12d %-12d %s  %.2f' % r)
print()
print('verify: every surviving cell byte-identical, every alias resolves to its target')
print('kept:   each pilot keeps their old-hull somersault - nobody asked for those to go')

io.open(MAN, 'w', encoding='utf-8', newline='').write(
    src[:SPAN[0]] + json.dumps(newships, separators=(',', ':'), sort_keys=False) + src[SPAN[1]:])
print('wrote ' + MAN)
