#!/usr/bin/env python3
"""import_maverick_v2_0906.py - Mike's new green Maverick airframe, into the ship atlas.

    python _BUILD_SOURCE/import_maverick_v2_0906.py            # dry run, writes proofs only
    python _BUILD_SOURCE/import_maverick_v2_0906.py --write     # atlas + manifest, one write

Mike, 0906: "I want to change Maverick's entire ship design to this."

SOURCE. ~/Desktop/maverick.png, 2046x768, an 8x3 grid of 256px cells. Rendered and measured
(docs/MAV_FRAMES_0906.png) the three rows are three different rotations:

    row 0   a full 360 BARREL ROLL about the nose axis. #2 and #6 are edge-on at 54px wide.
    row 1   pitch / tumble, nose-on through tail-on. NOT USED here - no slot wants it.
    row 2   a BANK sweep, monotonic left to right: -.220 -.148 -.070 .000 +.003 +.073 +.154

⚠ ROW 0 MAPS ONTO br0..br7 IN ORDER, AND THAT IS NOT A COINCIDENCE WORTH LOSING. The live rig
uses br2 and br6 as the TWIST pose (drop 0903y), and in this sheet #2 and #6 are exactly the two
edge-on frames - the same semantics the existing art already has (old br2/br5/br6 measure 68-69px
against their neighbours' 124-173). A straight in-order map preserves the twist for free.

⚠ THE BANK ROW IS EIGHT FRAMES AND THE GAME WANTS FIVE, so the pick is stated rather than
implied: the two extremes (#16 / #22) plus the symmetric inner pair (#18 / #21, -.070 / +.073)
and the centre (#20). Picking #17 for pv1 would have paired -.148 against +.073 and made the
ship lean harder one way than the other.

⚠ AND THE SIGNS MATCH THE UNFLIPPED CONVENTION, so Maverick STAYS OUT of SHIP_BANK_FLIP. His old
art measures pv0 -0.197 / pv4 +0.213 and the new art gives -0.220 / +0.154 - same sign, same
slots. This is checked rather than assumed because a transposed pair is exactly what caused the
retracted lizzie change earlier today; see the note at SHIP_BANK_FLIP.

GEOMETRY. Every existing maverick pv/br frame is INK-CENTRED in a 220x271 canvas - measured, all
thirteen, centre (109.5, 135.5) against a canvas centre of (110, 135.5). So the rule is: centre
the ink. One UNIFORM scale is applied to all thirteen frames, solved so the new centre frame's ink
HEIGHT matches the old pv2's 196px. Per-frame scaling would make the hull pulse as it banks, and
matching height rather than width is what keeps the ship the same size on screen as the other
eight pilots, because the hull blits at a fixed SHIP_DRAW_H.

⚠ THE MAGENTA IS NOISY AND MUST BE FLOOD-KEYED, NOT SWEPT. Sampled background runs (250,3,249),
(251,4,250), with corners drifting to (240,12,241) - a compressed magenta, not a clean #FF00FF.
A border flood with tolerance handles that and, per this repo's standing rule, cannot eat an
interior colour that happens to be magenta-ish.

⚠ AND THE FRINGE BECOMES A BLACK EDGE, NEVER A DELETION. That is a standing creative rule here
("Purple halos are converted to a black edge, never deleted"). Leftover magenta-dominant pixels on
the silhouette boundary are darkened to the hull's own outline colour instead of being punched to
alpha, which would gnaw a pixel off the ship all the way round.

⚠ THE ATLAS IS FULL. 3530x1605 with a used extent of 3524x1599, so the frames go into a strip
APPENDED at the bottom and the thirteen rects are repointed at it. The old pixels are left exactly
where they are, so reverting is thirteen manifest rows and nothing else - and the pixels and the
manifest are written in the SAME pass, which is the one rule an atlas edit here must not break.
"""
import os, sys, json, shutil, subprocess
from collections import deque
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = 'C:/Users/Mdogg/Desktop/maverick.png'
ATLAS = os.path.join(ROOT, 'assets/game/atlas/bof_player_ships_barrel_rolls.png')
MANIFEST = os.path.join(ROOT, 'assets/manifest.js')
CANVAS_W, CANVAS_H = 220, 271
COLS, ROWS = 8, 3

# slot -> (row, col) in the source sheet
BANK = {'pv0': (2, 0), 'pv1': (2, 2), 'pv2': (2, 4), 'pv3': (2, 5), 'pv4': (2, 6)}
ROLL = {('br%d' % i): (0, i) for i in range(8)}
# ⚠ ROW 1 IS THE SOMERSAULT (Mike, 0906): "Maverick's got back and front pseudo-3d graphics, plus
# somersault graphics PLUS barrel roll graphics ... if we double tap up we'll do a literal
# somersalt like starfox 64."  The first pass wrote this row off as "NOT USED - no slot wants it".
# It is a PITCH tumble read in order: #8 flat top-down, #10 edge-on from the side (227x87 - the
# ship halfway through the flip), #12 tail-on (the BACK view he is naming), #14 edge-on again,
# #15 back to flat. That is one clean 360 in the vertical plane, so it maps straight onto so0..so7.
SOMER = {('so%d' % i): (1, i) for i in range(8)}
SLOTS = dict(BANK); SLOTS.update(ROLL); SLOTS.update(SOMER)


def is_key(p):
    r, g, b, a = p
    return r > 170 and b > 170 and g < 90 and abs(r - b) < 70


def is_fringe(p):
    """magenta-dominant but not saturated enough to be background - the halo"""
    r, g, b, a = p
    return a > 0 and r > 90 and b > 90 and g < min(r, b) - 28


def cut(im, r, c):
    W, H = im.size
    cw, ch = W / COLS, H / ROWS
    cell = im.crop((int(c * cw), int(r * ch), int((c + 1) * cw), int((r + 1) * ch))).convert('RGBA')
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
    # halo -> black edge (the standing rule), not a deletion
    #
    # ⚠ THE HALO IS UP TO 2px THICK, so a test that only looks at pixels TOUCHING transparency
    # leaves the second ring behind - visible as a pink tinge along the wing edges in the first
    # proof render. Distance-to-alpha is computed once (a BFS out from the transparent region)
    # and every magenta-dominant pixel within RING of the edge is converted.
    RING = 2
    dist = [[999] * w for _ in range(h)]
    q = deque()
    for y in range(h):
        for x in range(w):
            if px[x, y][3] == 0:
                dist[y][x] = 0; q.append((x, y))
    while q:
        x, y = q.popleft()
        if dist[y][x] >= RING:
            continue
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h and dist[ny][nx] > dist[y][x] + 1:
                dist[ny][nx] = dist[y][x] + 1; q.append((nx, ny))
    conv = 0
    for y in range(h):
        for x in range(w):
            p = px[x, y]
            if p[3] == 0 or dist[y][x] > RING or not is_fringe(p):
                continue
            px[x, y] = (16, 18, 16, p[3]); conv += 1
    return cell, conv


def main():
    write = '--write' in sys.argv
    im = Image.open(SRC).convert('RGBA')
    print('source %s %dx%d' % (os.path.basename(SRC), im.width, im.height))

    cells, halo = {}, 0
    for slot, (r, c) in SLOTS.items():
        cell, conv = cut(im, r, c)
        bb = cell.getbbox()
        cells[slot] = cell.crop(bb)
        halo += conv
    print('%d frames cut, %d halo pixels converted to a black edge' % (len(cells), halo))

    # ONE uniform scale, solved on the centre frame against the old pv2 ink height (196)
    OLD_PV2_H = 196
    s = OLD_PV2_H / cells['pv2'].height
    print('uniform scale %.4f  (centre ink %dx%d -> %dx%d, old pv2 was 195x196)'
          % (s, cells['pv2'].width, cells['pv2'].height,
             round(cells['pv2'].width * s), round(cells['pv2'].height * s)))

    packed = {}
    for slot, img in cells.items():
        nw, nh = max(1, round(img.width * s)), max(1, round(img.height * s))
        sm = img.resize((nw, nh), Image.LANCZOS)
        canvas = Image.new('RGBA', (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
        canvas.alpha_composite(sm, ((CANVAS_W - nw) // 2, (CANVAS_H - nh) // 2))
        bb = canvas.getbbox()
        packed[slot] = (canvas.crop(bb), bb)

    # lay the trimmed frames out in a strip
    PAD = 2
    x, rowh, sx, strip = PAD, 0, PAD, []
    MAXW = 3530
    for slot in sorted(packed):
        sub, bb = packed[slot]
        if x + sub.width + PAD > MAXW:
            x = PAD; sx += rowh + PAD; rowh = 0
        strip.append((slot, x, sx, sub, bb))
        x += sub.width + PAD
        rowh = max(rowh, sub.height)
    strip_h = sx + rowh + PAD

    atlas = Image.open(ATLAS).convert('RGBA')
    y0 = atlas.height
    out = Image.new('RGBA', (atlas.width, atlas.height + strip_h), (0, 0, 0, 0))
    out.alpha_composite(atlas, (0, 0))
    rects = {}
    for slot, px_, py_, sub, bb in strip:
        out.alpha_composite(sub, (px_, y0 + py_))
        rects['ship_maverick_' + slot] = [px_, y0 + py_, sub.width, sub.height,
                                          bb[0], bb[1], CANVAS_W, CANVAS_H]
    print('atlas %dx%d -> %dx%d  (+%d row strip)' % (atlas.width, atlas.height,
                                                     out.width, out.height, strip_h))

    os.makedirs(os.path.join(ROOT, 'docs'), exist_ok=True)
    proof = Image.new('RGBA', (CANVAS_W * 7, CANVAS_H * 3), (22, 20, 30, 255))
    for i, slot in enumerate(['pv0', 'pv1', 'pv2', 'pv3', 'pv4', 'br0', 'br1',
                              'br2', 'br3', 'br4', 'br5', 'br6', 'br7',
                              'so0', 'so1', 'so2', 'so3', 'so4', 'so5', 'so6', 'so7']):
        sub, bb = packed[slot]
        cx, cy = (i % 7) * CANVAS_W, (i // 7) * CANVAS_H
        proof.alpha_composite(sub, (cx + bb[0], cy + bb[1]))
    proof.save(os.path.join(ROOT, 'docs/MAV_V2_PACKED_0906.png'))
    print('wrote docs/MAV_V2_PACKED_0906.png')

    if not write:
        print('\nDRY RUN - nothing written. Re-run with --write.')
        return 0

    if not os.path.exists(ATLAS + '.bak-0906mav'):
        shutil.copy(ATLAS, ATLAS + '.bak-0906mav')
    if not os.path.exists(MANIFEST + '.bak-0906mav'):
        shutil.copy(MANIFEST, MANIFEST + '.bak-0906mav')
    out.save(ATLAS)

    # rewrite the thirteen rows in place - same write as the pixels above
    src = open(MANIFEST, 'rb').read()
    n = 0
    for key, r in rects.items():
        new = ('"%s":[%s]' % (key, ','.join(str(v) for v in r))).encode()
        hit = 0
        for q in (b'"', b"'"):
            import re
            pat = re.compile(re.escape(q + key.encode() + q) + rb'\s*:\s*\[[^\]]*\]')
            src, k = pat.subn(new, src)
            hit += k
        if not hit:
            # a NEW family (so0..so7) has no row to replace - insert it beside a sibling that does
            import re
            anchor = re.search(rb'"ship_maverick_pv2"\s*:\s*\[[^\]]*\]', src) or                      re.search(rb"'ship_maverick_pv2'\s*:\s*\[[^\]]*\]", src)
            if not anchor:
                raise SystemExit('no anchor row to insert %s beside' % key)
            src = src[:anchor.end()] + b',' + new + src[anchor.end():]
            hit = 1
        n += hit
    open(MANIFEST, 'wb').write(src)
    print('manifest: %d ship rows repointed' % n)
    if n != len(rects):
        print('** expected %d, patched %d - CHECK THIS **' % (len(rects), n))
        return 1
    r = subprocess.run(['node', '--check', MANIFEST], capture_output=True)
    print('node --check manifest: %s' % ('OK' if r.returncode == 0 else r.stderr.decode()[:200]))
    return 0


if __name__ == '__main__':
    sys.exit(main())
