#!/usr/bin/env python3
"""import_bolts_0906.py - Mike's three enemy bolt families and their impacts.

    python _BUILD_SOURCE/import_bolts_0906.py            # dry run: geometry + key survey
    python _BUILD_SOURCE/import_bolts_0906.py --write    # + the cut frames

Mike, 0906: "I have much better projectiles to use for enemies, orbs, lightning, shadow bolts."

THE THREE PLATES SHARE THE FLAMETHROWER PLATE'S LAYOUT - 4x2 on magenta, row 0 the projectile in
flight and row 1 an impact that DECAYS - so this is import_flame_v2_0906.py's structure with one
rule deliberately NOT carried over. See the despill note below; it is the whole reason this is a
separate script rather than another SHEETS entry.

    caae65e2   cyan/white lightning lance   -> nbolt_cyan_*  / nboltx_cyan_*
    6aaf06e7   purple-black shadow bolt     -> nbolt_void_*  / nboltx_void_*
    b275c2d4   yellow bead bolt             -> nbolt_bead_*  / nboltx_bead_*

An impact reel is a ONE-SHOT and must be driven off the hit's own clock, never a wall clock, or it
is caught mid-decay at whatever point the frame lands on - the correction 0811y made to the pellet
and 0812g made to the muzzle flash. Nothing here drives it; that is the wiring job.

WARNING - THE FLAME'S DESPILL RULE WOULD DESTROY TWO OF THESE THREE.

`despill_fire` clamps BLUE down to GREEN wherever blue runs high, and it is sound for FIRE because
fire's ramp is red -> orange -> yellow -> white, along which blue never exceeds green. Cyan is b>g
by definition and purple is r-high/g-low/b-high, which is the KEY'S OWN SIGNATURE. Applying it
would grey the lightning out and eat the shadow bolt whole.

AND THE SURVIVING KEY INK IS TWO DIFFERENT THINGS, WHICH IS WHY ONE RULE COULD NOT DO IT.
Measured: cyan 4.13% of opaque, void 2.29%, bead 0.06%. My first pass called all of it halo and
converted the ink's rim to a black edge - it moved 28 pixels on the cyan plate and left 10,397,
because the cyan lance's branching arms ENCLOSE large pools of background the border flood cannot
reach, and those are nowhere near an edge. A rim-only rule cannot see them.

Scoring every unreachable blob by how far its mean colour sits from THE PLATE'S OWN background
pixel separates the two populations without a per-family list: 28 blobs (9,528 px) within 31 of it,
967 blobs (5,180 px) at 48 or more, 9 in between. So:

    still the background colour, and big     -> PUNCH to alpha. It is a hole the sprite has.
    anything else                            -> BLACK EDGE, never deleted (the standing halo rule).

That is what makes it safe for the VOID family, whose art genuinely is purple: its own ink scores
67..90 and not one pixel of it is punched. A hand-written "which families may contain magenta"
table would have had to get exactly that family right, on nothing but my say-so.
"""
import os, sys
from collections import deque
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DESK = 'C:/Users/Mdogg/Desktop/'
OUT = os.path.join(ROOT, 'assets/game/bolts_v1')
COLS, ROWS = 4, 2

PLATES = {
    'cyan': 'caae65e2-b13f-41de-a4a9-81bdfaf3c71c.png',
    'void': '6aaf06e7-0833-40f0-9803-640fd0769d28.png',
    'bead': 'b275c2d4-0403-47b9-906b-8207d1749726.png',
}
# (the old HALO_RING approach is gone: a rim-only rule could not reach the cyan lance's enclosed pockets)
# ⚠ THE THRESHOLDS BELOW ARE MEASURED, NOT PICKED. Every key-coloured blob the border flood could
# not reach was scored across all 24 frames by how far its mean colour sits from THE PLATE'S OWN
# background pixel: 28 blobs (9,528 px) land within 31 of it, 967 blobs (5,180 px) sit at 48 or
# more, and only 9 fall in between. So a pocket that is still literally the background colour is
# separable from ink WITHOUT a per-family list - which matters, because the family whose art is
# genuinely purple is the one a hand-written rule would have got wrong.
BG_TOL = 32        # max channel distance from the plate background to call a blob "still background"
MIN_POCKET = 20    # px: below this it is a spec, and 0810t's stage-7 lesson applies - punching a
                   # spec opens a pinhole through the middle of the sprite. Specs are darkened.


def is_key(p):
    r, g, b = p[0], p[1], p[2]
    return r > 150 and b > 150 and g < 95 and abs(r - b) < 80


def dekey(cell):
    """flood the key inward from the border; anything enclosed by ink is ART and survives"""
    w, h = cell.size
    px = cell.load()
    seen = [[False] * w for _ in range(h)]
    q = deque()
    for x in range(w):
        for y in (0, h - 1):
            if is_key(px[x, y]) and not seen[y][x]:
                seen[y][x] = True; q.append((x, y))
    for y in range(h):
        for x in (0, w - 1):
            if is_key(px[x, y]) and not seen[y][x]:
                seen[y][x] = True; q.append((x, y))
    while q:
        x, y = q.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h and not seen[ny][nx] and is_key(px[nx, ny]):
                seen[ny][nx] = True; q.append((nx, ny))
    for y in range(h):
        for x in range(w):
            if seen[y][x]:
                px[x, y] = (0, 0, 0, 0)
    return cell


def key_survivors(im):
    """opaque pixels still sitting in the key's colour bucket, and the opaque total"""
    px = im.load()
    n = op = 0
    for y in range(im.height):
        for x in range(im.width):
            p = px[x, y]
            if p[3] < 8:
                continue
            op += 1
            if is_key(p):
                n += 1
    return n, op


def clean_key(im, bg):
    """Every key-coloured blob the border flood could not reach, judged on its own evidence.

    A blob is POCKET (untouched background enclosed by the sprite - the cyan lightning's branching
    arms trap several hundred pixels of it) when its mean colour is still within BG_TOL of the
    plate's own background AND it is at least MIN_POCKET across. Those are punched to alpha,
    because they are holes the sprite is supposed to have.

    Everything else is HALO or spill, and takes this repo's standing treatment: converted to a
    BLACK EDGE, never deleted. That is what protects the VOID family - its shadow bolt's own purple
    scores 67..90 from the background and is nowhere near BG_TOL, so not one pixel of it is punched.

    The size floor is 0810t's stage-7 lesson: below it, a blob inside the structure is a spec, and
    punching a spec opens a pinhole straight through the sprite. Nine blobs of 1,004 land between
    the two populations; they go the CONVERT way, because a wrongly darkened pixel is invisible and
    a wrongly punched one is a hole.
    """
    w, h = im.size
    px = im.load()
    seen = [[False] * w for _ in range(h)]
    punched = darkened = 0
    for y0 in range(h):
        for x0 in range(w):
            if seen[y0][x0] or px[x0, y0][3] < 8 or not is_key(px[x0, y0]):
                continue
            q = deque([(x0, y0)]); seen[y0][x0] = True; pts = []
            while q:
                x, y = q.popleft(); pts.append((x, y))
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < w and 0 <= ny < h and not seen[ny][nx] \
                       and px[nx, ny][3] >= 8 and is_key(px[nx, ny]):
                        seen[ny][nx] = True; q.append((nx, ny))
            m = [sum(px[a, b][i] for a, b in pts) / len(pts) for i in range(3)]
            d = max(abs(m[i] - bg[i]) for i in range(3))
            if d <= BG_TOL and len(pts) >= MIN_POCKET:
                for a, b in pts:
                    px[a, b] = (0, 0, 0, 0)
                punched += len(pts)
            else:
                for a, b in pts:
                    px[a, b] = (0, 0, 0, px[a, b][3])
                darkened += len(pts)
    return punched, darkened


def mask(im):
    px = im.load()
    return {(x, y) for y in range(im.height) for x in range(im.width) if px[x, y][3] > 32}


def main():
    write = '--write' in sys.argv
    made = {}
    for fam, fn in PLATES.items():
        path = DESK + fn
        if not os.path.exists(path):
            print('%-6s MISSING %s' % (fam, fn)); continue
        im = Image.open(path).convert('RGBA')
        W, H = im.size
        cw, ch = W / COLS, H / ROWS
        # the plate's OWN background, sampled rather than assumed - the three plates measure
        # (246,3,250) (248,3,251) (247,3,249), close but not identical, and the pocket test is a
        # distance FROM this value
        bg = im.convert('RGB').getpixel((2, 2))
        print('%s  %s  %dx%d  cells %dx%d  bg %s'
              % (fam.upper(), fn[:12], W, H, int(cw), int(ch), bg))

        bolt, impact = [], []
        for r in range(ROWS):
            for c in range(COLS):
                cell = dekey(im.crop((int(c * cw), int(r * ch),
                                      int((c + 1) * cw), int((r + 1) * ch))).convert('RGBA'))
                bb = cell.getbbox()
                cell = cell.crop(bb) if bb else cell
                (bolt if r == 0 else impact).append(cell)

        kn, kop = 0, 0
        for f in bolt + impact:
            a, b = key_survivors(f)
            kn += a; kop += b
        pu = da = 0
        for f in bolt + impact:
            a, b = clean_key(f, bg)
            pu += a; da += b
        # and re-crop: punching an enclosed pocket cannot change the bbox, but punching one that
        # touched the frame edge can, and a stale bbox would leave dead margin on the sprite
        bolt = [(f.crop(f.getbbox()) if f.getbbox() else f) for f in bolt]
        impact = [(f.crop(f.getbbox()) if f.getbbox() else f) for f in impact]
        print('   key ink %.2f%% of opaque -> %d px punched as enclosed background, %d px darkened '
              'to a black edge' % (100.0 * kn / max(1, kop), pu, da))

        # ⚠ SIZE FIRST, THEN IoU. A low IoU means two different things and they want opposite
        # treatment: frames that are the SAME size with different detail are a loop (electricity
        # crackling - draw it as one), and frames that CHANGE size are a sequence (draw it off the
        # round's own clock, monotonically, or it stutters). Reporting the IoU alone cannot tell
        # them apart, and calling a growth sequence "edge crawl" would be 0811y's mistake exactly.
        hs = [f.height for f in bolt]
        span = (max(hs) - min(hs)) / max(1, max(hs))
        print('   bolt frames %s  (height spread %.0f%%)'
              % (' '.join('%dx%d' % (f.width, f.height) for f in bolt), span * 100))
        SZ = (max(f.width for f in bolt), max(f.height for f in bolt))
        padded = []
        for f in bolt:
            cvs = Image.new('RGBA', SZ, (0, 0, 0, 0))
            cvs.alpha_composite(f, ((SZ[0] - f.width) // 2, (SZ[1] - f.height) // 2))
            padded.append(cvs)
        ms = [mask(x) for x in padded]
        ious = [len(ms[i] & ms[(i + 1) % len(ms)]) / max(1, len(ms[i] | ms[(i + 1) % len(ms)]))
                for i in range(len(ms))]
        print('   silhouette IoU mean %.3f min %.3f -> %s'
              % (sum(ious) / len(ious), min(ious),
                 'A SEQUENCE: drive it off the round\'s own clock, do not loop it' if span > 0.15
                 else ('a loop with real motion in it' if min(ious) >= 0.80
                       else 'a loop whose outline moves - it will breathe in flight')))
        print('   impact %s' % ' '.join('%dx%d' % (f.width, f.height) for f in impact))
        made[fam] = (padded, impact)

    if not write:
        print(os.linesep + 'DRY RUN - nothing written. Re-run with --write.')
        return 0
    os.makedirs(OUT, exist_ok=True)
    n = 0
    for fam, (bolt, impact) in made.items():
        for i, f in enumerate(bolt):
            f.save(os.path.join(OUT, 'nbolt_%s_%d.png' % (fam, i))); n += 1
        for i, f in enumerate(impact):
            f.save(os.path.join(OUT, 'nboltx_%s_%d.png' % (fam, i))); n += 1
    print(os.linesep + 'wrote %d files to assets/game/bolts_v1/' % n)
    return 0


if __name__ == '__main__':
    sys.exit(main())
