#!/usr/bin/env python3
"""
build_stage7_0810t.py — Mike's corrected stage 7 plate, keyed so the SLUDGE shows through.

    python3 _BUILD_SOURCE/build_stage7_0810t.py

Mike, 0810r: "replace stage 7 with that sheet as an overlay, clean up all purple and white specs
and halos, and use the sludge for the background."

HOW THIS ENGINE DOES AN "OVERLAY" — it does not need a new draw path.
`_levelCfg()` already gives stage 7 `liquid:'nlq_sludgeF'`, and the liquid bed is drawn UNDERNEATH
the master, showing through wherever the master is TRANSPARENT. So "overlay with sludge behind" is:
punch this plate's white background to alpha and point the stage at it. No new code.

⚠ THE CHANNEL IS ALPHA, NOT MAGENTA, AND I BUILT IT WRONG ONCE. The first cut of this script wrote
literal #FF00FF, on a reading that drawStageBG keys magenta at runtime. It does not — the magenta in
these RC2 plates is punched to alpha OFFLINE and the liquid simply shows through the holes
(game.js: "8,412 magenta px were punched to alpha, and nlq_sludgeF is what shows THROUGH those
holes"). Rendered, stage 7 came back as a screen of raw magenta with pipes on it.

⚠ AND THE SLUDGE WAS NOT "NEVER DRAWN" EITHER. I measured the outgoing master by converting it to
RGB — which DISCARDS ALPHA — got 0.00% magenta, and read that as "no channel". It has 8,412 alpha-0
px, 0.21%, exactly the figure game.js already records. The sludge drew; there was just almost
nowhere for it to show. This plate takes that to 68%.

⚠ WHITE IS SAFE TO SWEEP GLOBALLY HERE, AND THAT IS MEASURED, NOT ASSUMED. The standing rule is to
flood a key from the BORDER because a colour sweep eats matching pixels inside the art. It cannot
be used here: the enclosed gaps (inside the frame, between the catwalks) must become channel too,
and a border flood would leave them opaque. A sweep is only correct if white is cleanly separated —
and it is, by a wide margin:

    luminance 255      2,223,584 px   68.43%     <- the background
    luminance 235-254          1 px    0.00%     <- nothing lives in the gap
    luminance <= 229                            <- the entire structure

A 25-level empty band between the key and the art. Re-checked here at build time, and the script
REFUSES to run if that gap ever closes.

⚠ h:4062 IS NOT OPTIONAL. Every reader of `cfg.h` falls back to 4800 when it is absent, and this
plate is 4062 — leaving it off mismaps the whole stage. The same note is already on stage 1 for the
same reason.
"""
import os
from collections import deque
from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
GAME = os.path.abspath(os.path.join(ROOT, '..'))
SRC = r'C:/Users/Mdogg/Desktop/level7corrected.png'
DST = os.path.join(GAME, 'assets', 'game', 'nst7_master_v2.png')

WHITE_MIN = 240          # everything at/above this, and neutral, is background
SPEC_MAX = 24            # a white blob smaller than this is a SPEC, not a gap


def main():
    im = Image.open(SRC).convert('RGBA')
    W, H = im.size
    px = im.load()
    print('source %dx%d' % (W, H))

    # ---- guard: the key must still be cleanly separated from the art ----
    hist = im.convert('L').histogram()
    gap = sum(hist[WHITE_MIN - 5:255])
    if gap > W * H * 0.001:
        raise SystemExit('REFUSING: %d px sit between the art and the key (%.3f%%). White is no '
                         'longer cleanly separable and a global sweep would eat the art.'
                         % (gap, 100.0 * gap / (W * H)))
    print('separation guard OK: %d px in the 235-254 band' % gap)

    def is_bg(p):
        return p[3] > 0 and min(p[0], p[1], p[2]) >= WHITE_MIN

    # ---- find white components so tiny ones can be filled instead of punched ----
    seen = bytearray(W * H)
    specs = filled = 0
    holes = 0
    for y0 in range(H):
        row = y0 * W
        for x0 in range(W):
            if seen[row + x0] or not is_bg(px[x0, y0]):
                continue
            comp = []
            q = deque([(x0, y0)])
            seen[row + x0] = 1
            while q:
                x, y = q.popleft()
                comp.append((x, y))
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < W and 0 <= ny < H and not seen[ny * W + nx] and is_bg(px[nx, ny]):
                        seen[ny * W + nx] = 1
                        q.append((nx, ny))
            if len(comp) <= SPEC_MAX:
                # a WHITE SPEC inside the structure. Punching it would open a pinhole of sludge in
                # the middle of a pipe. Fill it from its own darkest neighbour instead.
                specs += 1
                dark = None
                for (x, y) in comp:
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < W and 0 <= ny < H and not is_bg(px[nx, ny]):
                            p = px[nx, ny]
                            if p[3] > 0 and (dark is None or sum(p[:3]) < sum(dark[:3])):
                                dark = p
                for (x, y) in comp:
                    px[x, y] = dark or (35, 40, 24, 255)
                    filled += 1
            else:
                holes += 1
                for (x, y) in comp:
                    px[x, y] = (0, 0, 0, 0)          # ALPHA hole; the sludge shows through

    im.save(DST)
    keyed = sum(1 for y in range(0, H, 3) for x in range(0, W, 3) if px[x, y][3] == 0)
    tot = len(range(0, H, 3)) * len(range(0, W, 3))
    print('white specs filled : %d blobs, %d px (<= %d px each)' % (specs, filled, SPEC_MAX))
    print('sludge channel     : %d regions, %.1f%% of the plate (sampled)'
          % (holes, 100.0 * keyed / tot))
    print('wrote %s  (%.0f KB)' % (os.path.basename(DST), os.path.getsize(DST) / 1024))
    print('\nregister nst7_master_v2 and set _levelCfg case 7 to it, with h:%d' % H)


if __name__ == '__main__':
    main()
