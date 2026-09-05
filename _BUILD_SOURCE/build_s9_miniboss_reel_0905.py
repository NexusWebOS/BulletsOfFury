#!/usr/bin/env python3
"""build_s9_miniboss_reel_0905.py - give the new stage-9 miniboss a reel without spending credits.

    python _BUILD_SOURCE/build_s9_miniboss_reel_0905.py --write

The SpriteCook generation came back as ONE still plate, and the Event Horizon it replaces had a
seven-frame reel that `drawS9VoidEnemy` already drives:

    if(e._s9==='event') key='ns9x_horizon_'+(Math.floor(e.t*10)%7);

A miniboss at 164x199 that never moves a pixel reads as a cardboard cutout. But the thing that
sells "powered" on a dark hull is the LIGHT, not the geometry - and the light is already isolated,
because the recolour pass has to flood-label it anyway to keep it out of the hue swap. So the reel
is derived from the still: the lens breathes, and at the top of the breath it bleeds one pixel of
glow into the surrounding plating.

That is a real seven-frame animation for zero credits, and it keeps the silhouette byte-identical
across every frame - which matters, because the hitbox is read off the alpha.

⚠ THE HULL MUST NOT MOVE. Only pixels in (or adjacent to) the core mask are touched. A reel that
also jittered the plating would change `alphaBounds` frame to frame and make the collision box
breathe with the light.

⚠ SEVEN FRAMES, NOT EIGHT. The draw site above takes `% 7`. Writing eight would silently drop the
last one and make the loop stutter at the wrap.
"""
import math, os, sys, shutil
import colorsys
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from s9_palette_variants_0905 import core_mask, recolour, quantize, colours

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'docs/spritecook_briefs/s9miniboss/pixB.png')
OUT_PURPLE = os.path.join(ROOT, 'assets/game/stage9_void_rift/enemies/event_horizon_%d.png')
OUT_BLACK = os.path.join(ROOT, 'assets/game/stage9_void_rift/enemies/event_horizon_blk_%d.png')
N = 7                     # drawS9VoidEnemy indexes % 7
PAL = 96


def neighbours(core, w, h):
    """one-pixel ring just outside the core, for the bloom bleed"""
    ring = set()
    for (x, y) in core:
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                p = (x + dx, y + dy)
                if p not in core and 0 <= p[0] < w and 0 <= p[1] < h:
                    ring.add(p)
    return ring


def frame(base, core, ring, k):
    """frame k of N: the lens breathes, and blooms into the ring at the top of the breath."""
    pulse = 0.5 + 0.5 * math.sin(2 * math.pi * k / N)
    im = base.copy()
    px = im.load()
    for (x, y) in core:
        r, g, b, a = px[x, y]
        if a == 0:
            continue
        hh, ss, vv = colorsys.rgb_to_hsv(r / 255., g / 255., b / 255.)
        vv = min(1.0, vv * (0.80 + 0.24 * pulse))
        ss = max(0.0, ss * (1.06 - 0.16 * pulse))          # hotter reads whiter
        nr, ng, nb = colorsys.hsv_to_rgb(hh, ss, vv)
        px[x, y] = (int(nr * 255 + .5), int(ng * 255 + .5), int(nb * 255 + .5), a)
    bleed = max(0.0, (pulse - 0.55) / 0.45) * 0.50
    if bleed > 0:
        for (x, y) in ring:
            r, g, b, a = px[x, y]
            if a == 0:
                continue                                    # never paint outside the silhouette
            px[x, y] = (int(r + (110 - r) * bleed), int(g + (226 - g) * bleed),
                        int(b + (255 - b) * bleed), a)
    return im


def build(base, out_pattern, label, write):
    px = base.load()
    core = core_mask(base)
    ring = neighbours(core, base.width, base.height)
    ring = {p for p in ring if px[p][3] > 0}
    print('  %-18s core %d px, bloom ring %d px' % (label, len(core), len(ring)))
    sig = None
    for k in range(N):
        f = quantize(frame(base, core, ring, k), PAL)
        a = {(x, y) for y in range(f.height) for x in range(f.width) if f.load()[x, y][3] > 0}
        if sig is None:
            sig = a
        elif a != sig:
            raise SystemExit('SILHOUETTE MOVED on frame %d of %s' % (k, label))
        if write:
            p = out_pattern % k
            if not os.path.exists(p + '.bak-0905'):
                if os.path.exists(p):
                    shutil.copy(p, p + '.bak-0905')
            f.save(p)
        if k == 0:
            print('    %dx%d, %d colours/frame, silhouette locked across all %d frames'
                  % (f.width, f.height, colours(f), N))
    return True


def main():
    write = '--write' in sys.argv
    gen = Image.open(SRC).convert('RGBA')
    gen = gen.crop(gen.getbbox())
    print('source %s' % (gen.size,))
    build(recolour(gen, 'asis', rim=False), OUT_PURPLE, 'dark purple/blue', write)
    build(recolour(gen, 'black', rim=False), OUT_BLACK, 'black variant', write)
    print('\n%s' % ('wrote 14 frames (7 purple + 7 black)' if write
                    else 'DRY RUN - nothing written. Re-run with --write.'))


if __name__ == '__main__':
    main()
