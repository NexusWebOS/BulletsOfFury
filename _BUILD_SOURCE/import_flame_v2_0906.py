#!/usr/bin/env python3
"""import_flame_v2_0906.py - Mike's new flamethrower plume and its impact burst.

    python _BUILD_SOURCE/import_flame_v2_0906.py --write

Mike, 0906: "I want to use this for flamethrower instead of what we have ... this should be our
flamethrower projectile, not what were using currently. good replacement here."

SOURCE. ~/Desktop/8a8a434d-....png, 1536x1024, a 4x2 grid of 384x512 cells:

    row 0   FOUR frames of a vertical flame column - ink 127..145 x 428..444, aspect ~0.29-0.34.
            This is the plume. Wide flare at the bottom (the nozzle) tapering up to the tip.
    row 1   FOUR frames of an impact star that DECAYS - full cross, bigger burst, ring, sparks.
            That is a one-shot, not a loop: it must be driven off the hit's own clock, never a
            wall clock, or it will be caught mid-decay at a random point.

WRITTEN AS A NEW FAMILY, NOT OVER THE OLD ONE. `nfw_wall_0..7` stays exactly where it is and
stays registered; `nfw2_0..3` and `nfx2_0..3` are new loose files and flameDraw prefers them with
the old reel as the fallback. So this is reversible by one predicate, the ICE path is untouched
(it is a different reel and a different weapon - see flameIsIce), and a cold boot that has not
decoded the new art yet still draws fire rather than nothing.

⚠ THE MAGENTA IS FLOOD-KEYED FROM THE BORDER, NOT SWEPT. The background samples (230,3,224) and
drifts, and - the reason a colour sweep is actually dangerous here rather than merely sloppy -
this plume's own hot core is white and its mid-tones run through orange into near-magenta reds.
A threshold key eats the middle of the fire. That is the same lesson the firewall plate taught in
drop 0801ch, where 62% of the image was near-white and connectivity was the only thing that
separated background from core.

⚠ AND THE SILHOUETTE IS CHECKED FOR CRAWL. Four frames that do not share an outline make the jet
shimmer at the edges when it is held down, which is what the eight-frame `nfw_wall` reel avoids by
being palette-cycled off ONE plate. These four are independently drawn, so the script reports the
frame-to-frame silhouette IoU rather than assuming; anything low is a note for Mike, not something
to quietly "fix" by overwriting his art.
"""
import os, sys, shutil
from collections import deque
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = 'C:/Users/Mdogg/Desktop/8a8a434d-5077-4b69-904e-a534e82a6189.png'
OUT = os.path.join(ROOT, 'assets/game/flame_v2')
COLS, ROWS = 4, 2


def is_key(p):
    r, g, b, a = p
    return r > 150 and b > 150 and g < 95 and abs(r - b) < 80


def dekey(cell):
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


def despill_fire(im):
    """kill the key bleed that survives INSIDE the flame.

    The border flood cannot reach a magenta pixel that is enclosed by fire, and 1.87% of the
    plume's opaque pixels came out hot pink - (246,51,140), (236,27,155) and friends. Fire does
    not contain pink: its ramp runs red -> orange -> yellow -> white, along which BLUE never
    exceeds GREEN. So the rule is exactly that, applied only where it is violated - blue is
    clamped down to green. It leaves the white-hot core untouched (there b == g == r), and it
    cannot invent a colour that is not already on the plate's own ramp.
    """
    px = im.load()
    n = 0
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            if a < 8 or r < 60:
                continue
            if b > r * 0.55 and g < r * 0.75:
                px[x, y] = (r, g, min(b, g), a); n += 1
    return n


def mask(im):
    px = im.load()
    return {(x, y) for y in range(im.height) for x in range(im.width) if px[x, y][3] > 32}


def main():
    write = '--write' in sys.argv
    im = Image.open(SRC).convert('RGBA')
    W, H = im.size
    cw, ch = W / COLS, H / ROWS
    print('source %dx%d, %dx%d grid' % (W, H, COLS, ROWS))

    fam = {'nfw2': [], 'nfx2': []}
    for r in range(ROWS):
        name = 'nfw2' if r == 0 else 'nfx2'
        for c in range(COLS):
            cell = dekey(im.crop((int(c * cw), int(r * ch), int((c + 1) * cw), int((r + 1) * ch))).convert('RGBA'))
            despill_fire(cell)
            bb = cell.getbbox()
            fam[name].append(cell.crop(bb) if bb else cell)

    # the plume frames must share a silhouette or the held jet shimmers at its edges
    pl = fam['nfw2']
    SZ = (max(f.width for f in pl), max(f.height for f in pl))
    padded = []
    for f in pl:
        c = Image.new('RGBA', SZ, (0, 0, 0, 0))
        c.alpha_composite(f, ((SZ[0] - f.width) // 2, SZ[1] - f.height))   # bottom-aligned: the nozzle
        padded.append(c)
    ms = [mask(p) for p in padded]
    print('\nplume frames padded to %dx%d, bottom-aligned on the nozzle' % SZ)
    print('frame-to-frame silhouette IoU (1.00 = no edge crawl):')
    ious = []
    for i in range(len(ms)):
        a, b = ms[i], ms[(i + 1) % len(ms)]
        v = len(a & b) / max(1, len(a | b))
        ious.append(v)
        print('   %d->%d  %.3f' % (i, (i + 1) % len(ms), v))
    print('   mean %.3f  min %.3f' % (sum(ious) / len(ious), min(ious)))
    if min(ious) < 0.80:
        print('   \u26a0 the outline moves between frames; the jet will breathe at its edges.')
        print('     That is the ART, not a bug to paper over - flagging it for Mike.')
    fam['nfw2'] = padded

    for name, frames in fam.items():
        for i, f in enumerate(frames):
            print('%s_%d  %dx%d' % (name, i, f.width, f.height))

    if not write:
        print('\nDRY RUN - nothing written. Re-run with --write.')
        return 0
    os.makedirs(OUT, exist_ok=True)
    n = 0
    for name, frames in fam.items():
        for i, f in enumerate(frames):
            f.save(os.path.join(OUT, '%s_%d.png' % (name, i))); n += 1
    print('\nwrote %d files to assets/game/flame_v2/' % n)
    return 0


if __name__ == '__main__':
    sys.exit(main())
