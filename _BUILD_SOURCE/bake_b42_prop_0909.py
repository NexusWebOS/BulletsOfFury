#!/usr/bin/env python3
"""
bake_b42_prop_0909.py - THE B-42'S PROPELLER, ANIMATED BY ALTERNATING TWO BLADES AND THREE.

Mike, 0909: "just make it switch from the dual to the triple really fast and it'll look like a
propeller."

That is a better effect than what I built first. A small rotation of the same two blades reads as
a wobble; swapping the BLADE COUNT reads as a disc you cannot resolve, which is what a turning prop
actually looks like. shipGlowKey already cycles ['', 'g1', '', 'g2'] every 70ms - the machinery
that flickers a jet's flame - so with the base plate as the DUAL and both phases as TRIPLES the
sequence is dual, triple, dual, triple at ~14Hz, and no new draw code exists anywhere.

FINDING THE PROP, AND WHY THE FIRST TWO ATTEMPTS DID NOT.
  1. "Farthest ink from the tail" lands on a blade TIP, not the hub. Rotating about it swung the
     whole propeller around its own end.
  2. "Midpoint between the two extreme points" reported a span of exactly 40.0 on all nine frames,
     which is the search radius, not a measurement - the cap was binding and the second point was
     hull, not the opposite tip.
  3. The dark-pixel blobs are dominated by the canopy and panel shading at 2,800-5,000 px; the
     blades are a few hundred.
  The hub is the SILVER SPINNER: bright, desaturated metal, unlike the gold everywhere else.
  Its centroid within 30px of the nose reproduces all nine hubs read by eye off a 5x gridded
  render to within 0.2-5.0 px - under 1.4 px at the 60px the game draws a hull. A detector that
  has not reproduced the known-correct cases is not evidence about anything, so that check came
  first.

ISOLATING A BLADE WITHOUT KEYING ON COLOUR. The blades are ~3px thick and the cowling behind them
is not, so a morphological opening at r=3 deletes the blades and keeps the hull: blade = ink minus
opened(ink), inside the prop disc. One blade is then the half of that on one side of the line
through the hub perpendicular to the blades' own principal axis, and the triple is that half
stamped at 0, 120 and 240 degrees.

⚠ ROTATION IS LICENSED HERE. CLAUDE.md bans deriving a BANK by rotating a sprite and allows it for
the spin-out because that genuinely is an image-plane rotation. A propeller is the same case: it
turns in its own plane about a fixed hub, so a stamped copy is exact rather than an approximation.
"""
import io, json, os, re, shutil, sys
import numpy as np
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
GAME = os.path.join(ROOT, 'assets/game.js')
B42 = os.path.join(ROOT, 'assets/game/atlas/ships/ship_lizzie_b42.png')
# the backup lives with the build tooling, NOT in assets/ - anything under assets ships, and a
# 0.7 MB .preprop riding along in the download is exactly the dead weight this drop removed.
BAK = os.path.join(ROOT, '_BUILD_SOURCE', '_backups', 'ship_lizzie_b42.png.preprop')
LEVELISH = ['', '_nf', '_l', '_r', '_pv0', '_pv1', '_pv2', '_pv3', '_pv4']
PHASES = [('_g1', 0.0), ('_g2', 60.0)]     # both TRIPLE; the second offset so they are not identical
PROP_R = 34          # the blade TIPS reach r~30; at 26 they fell outside the disc and
                     # survived the clear as detached yellow crumbs beside the prop
PAD = 2

if '--revert' in sys.argv:
    if os.path.exists(BAK):
        shutil.copyfile(BAK, B42)
        print('restored ' + B42)
    else:
        print('no backup at ' + BAK)
    sys.exit(0)

g = io.open(GAME, encoding='utf-8', newline='').read()
gst = g.index('const LIZZIE_B42_RECTS={')
gen = g.index('};', gst) + 2
R = {m.group(1): [int(v) for v in m.group(2).split(',')]
     for m in re.finditer(r'"([^"]*)":\[([0-9,\s]+)\]', g[gst:gen])}
R = {k: v for k, v in R.items() if not re.search(r'_g[12]$', k)}   # drop any earlier phase rows

if not os.path.exists(BAK):
    shutil.copyfile(B42, BAK)
base = Image.open(BAK).convert('RGBA')


def dilate(m, r):
    out = m.copy()
    for _ in range(r):
        p = np.pad(out, 1, constant_values=False)
        out = p[1:-1, 1:-1] | p[:-2, 1:-1] | p[2:, 1:-1] | p[1:-1, :-2] | p[1:-1, 2:]
    return out


def erode(m, r):
    return ~dilate(~m, r)


def find_hub(a, m):
    ys, xs = np.where(m)
    bot = ys.max()
    band = m[max(0, bot - 6):bot + 1]
    bxs = np.where(band.any(axis=0))[0]
    tail = np.array([(bxs.min() + bxs.max()) / 2.0, float(bot)])
    pts = np.stack([xs, ys], axis=1).astype(float)
    A = pts[int(np.argmax(((pts - tail) ** 2).sum(axis=1)))]
    H, W = m.shape
    yy, xx = np.mgrid[0:H, 0:W]
    near = ((xx - A[0]) ** 2 + (yy - A[1]) ** 2) <= 30 * 30
    mx = a[:, :, :3].max(axis=2)
    mn = a[:, :, :3].min(axis=2)
    sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1), 0)
    silver = m & near & (mx > 110) & (sat < 0.30)
    if silver.sum() < 8:
        return None
    sy, sx = np.where(silver)
    return np.array([sx.mean(), sy.mean()])


def triple(cell, extra_deg):
    """clear the two authored blades and stamp ONE of them at 0/120/240 about the hub"""
    a = np.array(cell).astype(int)
    m = a[:, :, 3] > 40
    hub = find_hub(a, m)
    if hub is None:
        return None, 0
    H, W = m.shape
    yy, xx = np.mgrid[0:H, 0:W]
    d = np.sqrt((xx - hub[0]) ** 2 + (yy - hub[1]) ** 2)
    ang = np.degrees(np.arctan2(yy - hub[1], xx - hub[0])) % 360

    # WARNING: FOUR ISOLATION ATTEMPTS FAILED BEFORE THIS ONE, ALL RECORDED SO NOBODY REPEATS THEM.
    # Morphological thinning does not work - the blades are 6-8px thick and survive an opening that
    # would delete them; it returned 26 px of blade on a prop that has ~200. A dark-pixel test finds
    # the canopy (2,800-5,000 px against the blades' few hundred). A yellow-tip test finds the gold
    # FUSELAGE, because the fuselage is the same gold. And "the two points farthest apart" reported
    # a span of exactly 40.0 on all nine frames, which was the search radius binding, not a length.
    #
    # What DOES separate them is that a propeller is the only thing here with a MATCHED OPPOSITE
    # PAIR at radius. In the 20-30px ring the fuselage is a broad lobe with empty space across from
    # it; the blades are two narrow lobes roughly 180 degrees apart. Scoring each angle by the
    # WEAKER of itself and its opposite therefore picks the blades and scores the fuselage at zero.
    ring = m & (d >= 20) & (d <= 30)
    if ring.sum() < 40:
        return None, 0
    best, bestsc = None, -1
    for th in range(0, 360, 5):
        lo = ((ang - th + 180) % 360) - 180
        hi = ((ang - th - 180 + 180) % 360) - 180
        n1 = int((ring & (np.abs(lo) <= 14)).sum())
        n2 = int((ring & (np.abs(hi) <= 14)).sum())
        sc = min(n1, n2)
        if sc > bestsc:
            bestsc, best = sc, th
    if bestsc < 6:
        return None, 0
    th = float(best)
    disc = m & (d <= PROP_R)
    near = ((ang - th + 180) % 360) - 180
    far = ((ang - th - 180 + 180) % 360) - 180
    # the wedge we CLEAR is wider than the one we STAMP: at 16 degrees the outer tip of a blade
    # falls outside the wedge and survives as a detached yellow crumb floating beside the prop,
    # which is plainly visible at 5x on _l_g2 and _pv4_g2.
    one = disc & (np.abs(near) <= 16)                 # the blade we keep and re-stamp
    both = disc & ((np.abs(near) <= 26) | (np.abs(far) <= 26))

    src = np.array(cell)
    blade = np.zeros_like(src)
    blade[one] = src[one]
    patch = Image.fromarray(blade, 'RGBA')

    out = np.array(cell)
    out[both] = [0, 0, 0, 0]
    res = Image.fromarray(out, 'RGBA')
    for k in range(3):
        rot = patch.rotate(-(extra_deg + 120.0 * k), resample=Image.NEAREST,
                           center=(float(hub[0]), float(hub[1])))
        res = Image.alpha_composite(res, rot)
    return res, int(one.sum())


made = []
for suf in LEVELISH:
    r = R[suf]
    cell = base.crop((r[0], r[1], r[0] + r[2], r[1] + r[3]))
    for pname, deg in PHASES:
        im, n = triple(cell, deg)
        if im is None:
            print('no propeller found on ' + (suf or '(base)'))
            sys.exit(1)
        made.append((suf + pname, im, r, n))

W = base.width
x, y, rowh = 0, base.height + PAD, 0
placed = {}
for nm, im, r, n in sorted(made, key=lambda t: -t[1].height):
    ww, hh = im.width + PAD * 2, im.height + PAD * 2
    if x + ww > W:
        x, y, rowh = 0, y + rowh, 0
    placed[nm] = (x + PAD, y + PAD)
    x += ww
    rowh = max(rowh, hh)
H = y + rowh

sheet = Image.new('RGBA', (W, H), (0, 0, 0, 0))
sheet.paste(base, (0, 0))
newR = dict(R)
for nm, im, r, n in made:
    nx, ny = placed[nm]
    sheet.paste(im, (nx, ny))
    newR[nm] = [nx, ny, im.width, im.height, r[4], r[5], r[6], r[7]]
sheet.save(B42)

chk = Image.open(B42).convert('RGBA')
bad = [nm for nm, im, r, n in made if not np.array_equal(np.array(im), np.array(chk.crop(
    (newR[nm][0], newR[nm][1], newR[nm][0] + newR[nm][2], newR[nm][1] + newR[nm][3]))))]
for suf, r in R.items():
    box = (r[0], r[1], r[0] + r[2], r[1] + r[3])
    if not np.array_equal(np.array(base.crop(box)), np.array(chk.crop(box))):
        bad.append('original ' + (suf or '(base)'))
if bad:
    print('ABORT - %d cells wrong: %s' % (len(bad), ', '.join(bad[:8])))
    sys.exit(1)

print('%-10s %s' % ('frame', 'pixels in the one blade that gets stamped three times'))
for suf in LEVELISH:
    print('%-10s %d' % (suf or '(base)', [m[3] for m in made if m[0] == suf + '_g1'][0]))
print('')
print('sheet %dx%d, %.2f MB   %d cells (%d aircraft + %d propeller phases)'
      % (W, H, os.path.getsize(B42) / 1e6, len(newR), len(R), len(made)))
print('verify: every aircraft cell byte-identical, all %d phase cells land where the rects say' % len(made))

nl = '\r\n' if '\r\n' in g[:20000] else '\n'
lines = ['const LIZZIE_B42_RECTS={',
         "  /* ⚠ TWO OF THESE ARE ALIASES AND THAT IS A REPAIR, NOT THE AUTHORED LAYOUT (0909).",
         "     (base) and _pv2 - the costume's LEVEL frames, i.e. what you look at for almost the whole",
         "     run - cropped Juggernaut's and Maverick's aircraft, in the pre-0909 atlas too. Both now",
         "     name _nf, which IS a clean level bomber. _br1 and _br5 are still stubs and are left",
         "     alone: a roll frame has no obviously correct stand-in the way a level frame does.",
         "",
         "     ⚠ THE _g1/_g2 ROWS ARE THE PROPELLER AND THEY ARE TRIPLE-BLADED (Mike, 0909: \"just make",
         "     it switch from the dual to the triple really fast and it'll look like a propeller\").",
         "     The base plate is the authored two-blade prop; both phases are three blades, the second",
         "     offset 60 degrees. shipGlowKey cycles ['','g1','','g2'] every 70ms, so the aircraft",
         "     alternates dual/triple at about 14Hz. Only the nine level-ish frames carry phases; the",
         "     roll frames fall back to their base plate, which is what shipGlowKey does when a phase",
         "     is absent. */"]
for suf, r in newR.items():
    lines.append('  %s:%s,' % (json.dumps(suf), json.dumps(r, separators=(',', ','))))
lines.append('};')
io.open(GAME, 'w', encoding='utf-8', newline='').write(g[:gst] + nl.join(lines) + g[gen:])
io.open(os.path.join(ROOT, 'assets/data/lizzie_b42_source_rects.json'), 'w',
        encoding='utf-8', newline='\n').write(json.dumps(newR, indent=1) + '\n')
print('wrote the sheet, LIZZIE_B42_RECTS (%d rows) and the b42 json' % len(newR))
print('backup at ' + os.path.basename(BAK) + '   (--revert restores it)')
