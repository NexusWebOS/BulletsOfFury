"""
clean_hull_edges_0904h.py - strip the white/grey rim off the stage 5-9 hull plates and give every
one of them a real black edge.

Mike, 0904: "some of these idle enemies in general need edge cleanup or given 1px black edges.
thres some white/graying going out that looks bad. in both variants."

("both variants" is free: the enraged plate is derived from the source plate at runtime, so
cleaning the source fixes the normal hull and the enraged hull in one pass.)

MEASURED ACROSS ALL 48 IDLE PLATES BEFORE WRITING ANYTHING:

  - bright desaturated rim pixels: 2,141 of 36,299 silhouette-edge pixels (5.9%), but very
    unevenly spread - lightning_mine 32.1%, salvage_tug 23.3%, shield_leech 16.5%, gravity_orb
    14.2%, while most of stage 7 is under 1%.
  - already-dark edge pixels: only 37.4% overall. Stage 7 was authored with proper outlines
    (57-69%); stage 9 largely was not (10-30%). So "give them 1px black edges" is the bigger half
    of this job - most hulls simply have no outline.

⚠ A 1px OUTLINE WOULD BE INVISIBLE. These plates are 256px drawn at 93-141px, a 1.8x-2.8x
   minification (drop 0904d). One source pixel is ~0.43 screen pixels, so a 1px source outline
   disappears into the resampling. The outline is therefore OUTLINE_PX=2 at source, which lands
   at roughly one pixel on screen - which is what Mike is actually asking to see.

⚠ THE RIM STRIP ONLY TAKES PIXELS THAT ARE BRIGHTER THAN THE ART BEHIND THEM. A flat "delete
   bright edge pixels" rule would eat legitimate art - cockpit glass, lit engine bells, the white
   hot core of a thruster - any time it happened to sit on the silhouette. A rim pixel is bright,
   desaturated AND clearly brighter than the pixel inward of it; a lit engine is bright but its
   neighbours are bright too, so it survives.
"""
import io, os, sys, math
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STAGE_DIRS = ['stage5_enemy_attacks', 'stage6_enemy_attacks',
              'stage7_enemy_attacks', 'stage9_enemy_attacks']
OUTLINE_PX = 2
OUTLINE_RGB = (12, 7, 9)          # matches ENRAGE_RAMP band 0, so the enraged plate keeps it black
RIM_LUM = 105.0                   # "bright"
RIM_SAT = 0.34                    # "desaturated"
RIM_DELTA = 14.0                  # and this much brighter than the art behind it
RING_MIX  = 0.5                   # how far the outermost surviving ring is pulled toward black
LABEL_Y   = 0.68                  # a detached blob centred below this is a baked-in caption
LABEL_MAX = 0.06                  # ...and no bigger than this share of the plate
# ⚠ CAPTION STRIPPING IS ALLOWLISTED, AND IT HAS TO BE. The geometric rule alone (detached + low
#   in the plate + small) fired on 21 units and deleted 13,313 pixels - but only 6,861 of those
#   were text. The rest were on frames 03-06, which are ATTACK frames: the muzzle flashes, ejected
#   shells and launched ordnance that sit low and detached exactly like a caption does.
#   sampling_drone lost 1,518px of its own gunfire, piston_pump_walker 1,167px. Rendered the two
#   real offenders and confirmed them by eye; nothing else is touched.
LABEL_UNITS = ('salvage_tug', 'shield_leech')
N4 = ((1, 0), (-1, 0), (0, 1), (0, -1))


def lum(r, g, b):
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def sat(r, g, b):
    mx = max(r, g, b)
    return 0.0 if mx == 0 else (mx - min(r, g, b)) / float(mx)


def _components(px, w, h):
    from collections import deque
    seen = [[False] * h for _ in range(w)]
    out = []
    for y in range(h):
        for x in range(w):
            if px[x, y][3] == 0 or seen[x][y]:
                continue
            q = deque([(x, y)]); seen[x][y] = True; cur = []
            while q:
                cx, cy = q.popleft(); cur.append((cx, cy))
                for dx in (-1, 0, 1):
                    for dy in (-1, 0, 1):
                        i, j = cx + dx, cy + dy
                        if 0 <= i < w and 0 <= j < h and not seen[i][j] and px[i, j][3] > 0:
                            seen[i][j] = True; q.append((i, j))
            out.append(cur)
    out.sort(key=len, reverse=True)
    return out


def clean(im, allow_label=False):
    """returns (image, rim_pixels_removed, outline_pixels_added, label_pixels_removed)"""
    im = im.convert('RGBA').copy()
    px = im.load()
    w, h = im.size

    def opaque(x, y):
        return 0 <= x < w and 0 <= y < h and px[x, y][3] > 0

    # ---- 0. the vendor left CAPTIONS baked into two of the plates -------------------------
    # ⚠ salvage_tug reads "OSTER SALVAGE TUG" across the bottom of the sheet and shield_leech
    #   carries its own name the same way - 426 and 431 pixels of text that would render in the
    #   game underneath the enemy. Scanned all 48: only those two. A caption is DETACHED from the
    #   hull, sits low in the plate and is small, so all three conditions have to hold - a
    #   legitimately detached part (a drone, a dropped turret) fails at least one.
    label_removed = 0
    comps = _components(px, w, h) if allow_label else []
    if allow_label and len(comps) > 1:
        total = sum(len(c) for c in comps)
        for c in comps[1:]:
            cy = sum(y for _, y in c) / float(len(c))
            if cy > h * LABEL_Y and len(c) <= total * LABEL_MAX:
                for q in c:
                    px[q] = (0, 0, 0, 0)
                label_removed += len(c)

    # ---- 1. strip the rim, up to two rings deep -------------------------------------------
    removed = 0
    for _ring in range(2):
        kill = []
        for y in range(h):
            for x in range(w):
                r, g, b, a = px[x, y]
                if a == 0:
                    continue
                if all(opaque(x + dx, y + dy) for dx, dy in N4):
                    continue                       # interior, not an edge
                L = lum(r, g, b)
                if L <= RIM_LUM or sat(r, g, b) >= RIM_SAT:
                    continue
                # the art immediately inward of this pixel
                inward = [px[x + dx, y + dy] for dx, dy in N4 if opaque(x + dx, y + dy)]
                if not inward:
                    kill.append((x, y)); continue  # a loose speck
                best = max(lum(*p[:3]) for p in inward)
                if L - best >= RIM_DELTA:
                    kill.append((x, y))
        if not kill:
            break
        for p in kill:
            px[p] = (0, 0, 0, 0)
        removed += len(kill)

    # ---- 1b. pull the outermost surviving ring toward black --------------------------------
    # ⚠ STRIPPING ALONE LEFT A LIGHT FRINGE. The rim rule only fires on pixels clearly brighter
    #   than the art behind them; a hull whose edge is uniformly pale keeps its pale edge and
    #   still reads as "white/graying going out". Darkening the outermost ring 50% toward the
    #   outline colour removes that without DELETING art - the silhouette does not shrink, it
    #   just stops glowing at the boundary.
    ring0 = []
    for y in range(h):
        for x in range(w):
            if px[x, y][3] == 0:
                continue
            if not all(opaque(x + dx, y + dy) for dx, dy in N4):
                ring0.append((x, y))
    for (x, y) in ring0:
        r, g, b, a = px[x, y]
        px[x, y] = (int(r + (OUTLINE_RGB[0] - r) * RING_MIX),
                    int(g + (OUTLINE_RGB[1] - g) * RING_MIX),
                    int(b + (OUTLINE_RGB[2] - b) * RING_MIX), a)

    # ---- 2. lay a black edge OUTSIDE the cleaned silhouette --------------------------------
    added = 0
    for _ring in range(OUTLINE_PX):
        ring = []
        for y in range(h):
            for x in range(w):
                if px[x, y][3] != 0:
                    continue
                touch = False
                for dx in (-1, 0, 1):
                    for dy in (-1, 0, 1):
                        if dx == 0 and dy == 0:
                            continue
                        if opaque(x + dx, y + dy):
                            touch = True; break
                    if touch:
                        break
                if touch:
                    ring.append((x, y))
        if not ring:
            break
        for p in ring:
            px[p] = (OUTLINE_RGB[0], OUTLINE_RGB[1], OUTLINE_RGB[2], 255)
        added += len(ring)
    return im, removed, added, label_removed


def room_check(im):
    """the outline grows the silhouette, so there has to be transparent margin to grow into"""
    b = im.convert('RGBA').getbbox()
    if not b:
        return 0
    w, h = im.size
    return min(b[0], b[1], w - b[2], h - b[3])


def main():
    apply = '--apply' in sys.argv
    only = None
    for a in sys.argv[1:]:
        if a.startswith('--only='):
            only = a.split('=', 1)[1].split(',')
    tot_r = tot_a = tot_l = files = tight = 0
    for d in STAGE_DIRS:
        base = os.path.join(ROOT, 'assets', 'game', d)
        if not os.path.isdir(base):
            continue
        for u in sorted(os.listdir(base)):
            if only and u not in only:
                continue
            udir = os.path.join(base, u)
            if not os.path.isdir(udir):
                continue
            for fn in sorted(os.listdir(udir)):
                if not fn.lower().endswith('.png'):
                    continue
                p = os.path.join(udir, fn)
                im = Image.open(p)
                margin = room_check(im)
                if margin < OUTLINE_PX:
                    tight += 1
                    print('  SKIP (no margin to outline into): %s/%s/%s  margin=%d' % (d, u, fn, margin))
                    continue
                out, rem, add, lab = clean(im, allow_label=(u in LABEL_UNITS))
                tot_r += rem; tot_a += add; tot_l += lab; files += 1
                if apply:
                    out.save(p)
    print('%s  files=%d  rim=-%d  caption=-%d  outline=+%d  skipped(no margin)=%d'
          % ('APPLIED' if apply else 'DRY RUN (pass --apply)', files, tot_r, tot_l, tot_a, tight))


if __name__ == '__main__':
    main()
