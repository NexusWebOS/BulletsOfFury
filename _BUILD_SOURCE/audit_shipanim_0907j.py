#!/usr/bin/env python3
"""audit_shipanim_0907j.py - is a pack frame a BANK or a YAW, and clean the de-key fringe.

    python _BUILD_SOURCE/audit_shipanim_0907j.py juggernaut
    python _BUILD_SOURCE/audit_shipanim_0907j.py juggernaut --write

TWO THINGS, BOTH FOUND BY LOOKING AT THE SLICED SHEET RATHER THAN BY TRUSTING ITS ROW LABELS.

⚠ THE PRINCIPAL-AXIS YAW TEST FROM 0906y DOES NOT TRANSFER TO THIS PACK, AND ITS FIRST RUN HERE
FLAGGED HALF THE SHEET. That test asks "does the ink's long axis point north", which is the right
question for a hull plate and the WRONG one for a somersault: a nose-on or tail-on aircraft is
WIDE AND SHORT, so its long axis is horizontal BY DESIGN and the metric reads it as 90 degrees of
yaw. Every one of row 1's eight frames failed a test that cannot apply to them.

⚠ THE TEST THAT DOES SEPARATE THEM IS WHERE THE NOSE SITS ABOVE THE TAIL. Take the ink centroid of
the top 15% of rows and of the bottom 15%, and subtract:
    a BANK rolls about the nose-tail axis, so the nose stays over the tail   -> offset ~0
    a YAW rotates the whole aircraft in the image plane                      -> offset grows
It is scale-free (reported as a share of the frame's own width), it does not care about aspect, so
it reads a somersault frame and a bank frame on the same scale, and it answers the only question
that matters for mapping onto `_l`/`_r`/`_pv*`: does this frame still point where the game draws it.

⚠ AND THE DE-KEY LEAVES A FRINGE, WHICH IS CONVERTED TO A BLACK EDGE AND NEVER DELETED. The border
flood punches pixels that MATCH the key; it cannot touch the 1-2px of hull that was blended with it
by the source's own antialiasing, so every sliced cell came out ringed in magenta. This repo's
standing rule covers exactly that case, and the classifier is 0906t's channel-pattern test
(`r > g and b > g`), not a saturation gate - dark violets sit under any saturation threshold.
Juggernaut's copper is r > g > b, so his paint cannot match it.
"""
import os, sys, json, math
from collections import deque
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SLICED = os.path.join(ROOT, 'assets/game/ships_sliced')
ROW_MEANING = ['barrel roll', 'somersault', 'banked turn', 'pivot']
END_F = 0.15          # the share of rows counted as "nose" and as "tail"
UPRIGHT = 0.06        # nose-over-tail offset below this is a bank, not a yaw
FRINGE_DEPTH = 6      # see the note on defringe() - the spill sits INSIDE the ship's black outline


def is_key_cast(p):
    """0906t's channel-pattern test: violet is r and b both above g. NOT a saturation gate."""
    r, g, b = p[0], p[1], p[2]
    return r > g and b > g and min(r, b) - g >= 5


def defringe(im):
    """convert the de-key's residual key cast to a BLACK EDGE (never delete it).

    ⚠ THE SPILL IS NOT ON THE BOUNDARY, IT IS ONE BLACK LINE IN - 0906u's finding, reproduced
    exactly on this pack. Depth-from-transparency over Juggernaut's 32 cells: 940 / 450 / 149 /
    **3293** / 813 / 303 / 158 / 90 / 59. A halo decays; this SPIKES at depth 3, because the art is
    drawn with its own 2-3px black outline - the flood punches the key, the outline occupies depths
    0-2, and the contaminated hull pixels land just inside it. A depth-2 cap (0906t's number, taken
    from plates with no drawn outline) converted 26,955 px and left 6,587 tracing the silhouette,
    which is what the highlight render showed as a green outline of the whole aircraft.

    ⚠ AND A PIXEL ON THE CROP BORDER HAS NO TRANSPARENT NEIGHBOUR, so it can never be reached
    from inside. The cells are cropped to their own ink bbox, so the outermost wingtip column IS
    ink - and it was blended against the key on the sheet. 940 px, and they read as a bright magenta
    line down each wingtip. The BFS seeds from the frame border as well as from alpha.

    ⚠ THIS IS SAFE ON JUGGERNAUT AND MUST BE RE-CHECKED PER SHIP. The classifier is a channel
    pattern, so it cannot fire on copper (r > g > b), on Cole's green or on Lizzie's gold, and
    Falva's sheet keys on CYAN so her pink hull is r-dominant against a g/b test. **Axel is the one
    to look at** - a violet-leaning blue satisfies r > g and b > g the same way a halo does, which
    is 0906t's falva/freezer case. Render the highlight before trusting the count.
    """
    im = im.copy()
    W, H = im.size
    px = im.load()
    # depth from transparency, by BFS out of the alpha-0 region
    depth = [[999] * W for _ in range(H)]
    q = deque()
    for y in range(H):
        for x in range(W):
            if px[x, y][3] < 40 or x in (0, W - 1) or y in (0, H - 1):
                depth[y][x] = 0
                q.append((x, y))
    while q:
        x, y = q.popleft()
        d = depth[y][x]
        if d >= FRINGE_DEPTH:
            continue
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < W and 0 <= ny < H and depth[ny][nx] > d + 1:
                depth[ny][nx] = d + 1
                q.append((nx, ny))
    n = deep = 0
    for y in range(H):
        for x in range(W):
            p = px[x, y]
            if p[3] < 40 or not is_key_cast(p):
                continue
            if depth[y][x] > FRINGE_DEPTH:
                deep += 1          # too far in to be spill - reported, never converted
                continue
            px[x, y] = (0, 0, 0, p[3])
            n += 1
    return im, n, deep


def nose_over_tail(im):
    """the nose's horizontal offset from the tail, as a share of the ink's own width.

    ~0 means the fuselage still runs north-south (a BANK, or a level frame); a large value means
    the whole aircraft has been rotated in the image plane (a YAW), whatever its aspect."""
    W, H = im.size
    px = im.load()
    rows = []
    for y in range(H):
        tw = tx = 0
        for x in range(W):
            if px[x, y][3] >= 40:
                tw += 1
                tx += x
        rows.append((tx / tw, tw) if tw else (None, 0))
    live = [y for y in range(H) if rows[y][1]]
    if len(live) < 6:
        return 0.0
    k = max(1, int(round(len(live) * END_F)))

    def band(ys):
        tw = sum(rows[y][1] for y in ys)
        return sum(rows[y][0] * rows[y][1] for y in ys) / tw if tw else 0.0

    return (band(live[:k]) - band(live[-k:])) / float(W)


def best_rot(im, lvl):
    """which IN-PLANE ROTATION of the level frame this cell most is, and how well it fits.

    ⚠ NOSE-OVER-TAIL IS BLIND TO 90 AND 180 DEGREES, WHICH IS THE 0906k TRAP IN A NEW COAT.
    A ship yawed a quarter turn has one wing at the top of the frame and the other at the bottom,
    both centred, so the offset reads 0.000 - and a ship yawed a HALF turn (flying south, guns
    down) reads 0.000 as well. Row 3 is visibly a full 360 spin and every one of its eight frames
    passed the offset test. So the offset finds a LEAN and this finds a TURN; both are needed.

    Matching the level frame turned by each eighth of a circle answers it directly and needs no
    model of where a nose is."""
    b = im.getbbox()
    tgt = im.crop(b) if b else im
    out = []
    for k in range(8):
        r = lvl.rotate(-k * 45.0, resample=Image.BICUBIC, expand=True)
        bb = r.getbbox()
        if bb:
            r = r.crop(bb)
        out.append((iou_a(tgt, r), k * 45))
    out.sort(reverse=True)
    return out[0][1], out[0][0]


def iou_a(a, b):
    if a.size != b.size:
        b = b.resize(a.size, Image.NEAREST)
    pa, pb = a.load(), b.load()
    inter = union = 0
    for y in range(a.height):
        for x in range(a.width):
            A = pa[x, y][3] > 40
            B = pb[x, y][3] > 40
            if A or B:
                union += 1
                if A and B:
                    inter += 1
    return inter / float(union) if union else 0.0


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    pilot = sys.argv[1]
    write = '--write' in sys.argv
    d = os.path.join(SLICED, pilot)
    if not os.path.isdir(d):
        print('no sliced cells for %r - run slice_shipanim_0907i.py %s --write first' % (pilot, pilot))
        return 1

    cells = {}
    fringe = deep = 0
    for r in range(4):
        for c in range(8):
            f = os.path.join(d, 'r%dc%d.png' % (r, c))
            im = Image.open(f).convert('RGBA')
            im, n, dp = defringe(im)
            fringe += n
            deep += dp
            cells[(r, c)] = im
    print('%s  de-key fringe converted to black: %d px across 32 cells  '
          '(%d left deeper than %d px in, untouched)' % (pilot, fringe, deep, FRINGE_DEPTH))
    print()

    lvl = cells[(0, 0)]
    LW = lvl.width
    print('%-5s %-13s %-10s %-7s %-9s %-13s %s'
          % ('cell', 'row means', 'ink', 'w/lvl', 'nose-tail', 'turned by', 'reads as'))
    info = {}
    for r in range(4):
        for c in range(8):
            im = cells[(r, c)]
            nt = nose_over_tail(im)
            rot, rq = best_rot(im, lvl)
            wr = im.width / float(LW)
            asp = im.width / float(im.height)
            if abs(nt) < UPRIGHT:
                verdict = 'UPRIGHT - nose is over the tail'
                if asp > 1.15:
                    verdict = 'UPRIGHT, pitched (wide+short: a nose-on/belly/tail-on view)'
            else:
                verdict = 'YAWED %+.0f%% - the whole aircraft is turned in-plane' % (nt * 100)
            if rot and rq >= 0.62:
                verdict = 'TURNED %d deg in-plane (fit %.2f)' % (rot, rq)
            info['%d,%d' % (r, c)] = dict(w=im.width, h=im.height, wr=wr, nt=nt, asp=asp,
                                          rot=rot, rq=rq)
            print('%-5s %-13s %-10s %-7.3f %+9.3f %-13s %s'
                  % ('r%dc%d' % (r, c), ROW_MEANING[r], '%dx%d' % (im.width, im.height), wr, nt,
                     '%d deg %.2f' % (rot, rq), verdict))
        print()

    if write:
        for (r, c), im in cells.items():
            im.save(os.path.join(d, 'r%dc%d.png' % (r, c)))
        json.dump(info, open(os.path.join(d, '_audit.json'), 'w'), indent=1)
        print('rewrote 32 de-fringed cells + _audit.json in assets/game/ships_sliced/%s/' % pilot)
    else:
        print('DRY RUN - the sliced cells were not modified.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
