#!/usr/bin/env python3
"""thruster_pack_recon_0907l.py - what is on the 18 fleet thruster sheets, measured per cell.

    python _BUILD_SOURCE/thruster_pack_recon_0907l.py            # every pilot
    python _BUILD_SOURCE/thruster_pack_recon_0907l.py juggernaut

Mike, 0907: "heres the thruster frames, as always animatd thrusters our way with pixel glow per
frame and place where they are missing."

⚠ THE FLAME IS LIFTED BY DIFFING AGAINST THE FLAMELESS SHEET, NOT BY DETECTING A NOZZLE. 0906q
built a whole bell detector because there was nothing to diff against; this pack ships the same
8x4 pose grid twice, once with thrust and once without (`*-no-thrusters-source.png` in the
animation pack), so the flame IS the difference and its placement is the artist's, per pose, with
no mount table involved. That is the same geometric lift 0906q settled on for Juggernaut's own
plumes - "the footprint from where the two plates differ, then every inked pixel inside it" -
except the footprint is now exact rather than inferred.

⚠ WHICH ONLY WORKS IF THE HULLS LINE UP, AND THE PACK'S OWN README SAYS THEY MIGHT NOT: "Long and
short variants may differ in hull placement or pose details." So alignment is MEASURED per cell
before any diff is trusted - a hull one pixel off turns the whole silhouette into "difference" and
the lift would return the aircraft instead of its exhaust.

⚠ AND FREEZER AND MAVERICK HAVE NO FLAMELESS PARTNER. The animation pack shipped seven pilots;
this one ships nine. For those two the diff is unavailable and the sheet's own hull is used whole.
"""
import os, sys, json
from collections import deque
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
THR = os.path.join(ROOT, '_ART_SOURCES_THRUSTERS')
ANIM = os.path.join(ROOT, '_ART_SOURCES_SHIPANIM')
COLS, ROWS = 8, 4
ROW_MEANING = ['barrel roll', 'somersault', 'banked turn', 'pivot(spin)']

PILOTS = ['axel', 'cole', 'decker', 'falva', 'freezer', 'juggernaut', 'lizzie', 'maverick', 'yuri']
# the flameless partner sheet, where one exists
FLAMELESS = {
    'axel': 'Axel/axel-latest-source.png',
    'cole': 'Cole/cole-latest-source.png',
    'decker': 'Decker/decker-latest-source.png',
    'falva': 'Falva/falva-cyan-latest-source.png',
    'juggernaut': 'Juggernaut/juggernaut-no-thrusters-source.png',
    'lizzie': 'Lizzie/lizzie-golden-latest-source.png',
    'yuri': 'Yuri/yuri-latest-source.png',
}


def thr_sheet(pilot, which):
    d = pilot.capitalize()
    return os.path.join(THR, d, '%s-thrusters-%s-source.png' % (pilot, which))


def sheet_key(im):
    return im.convert('RGB').load()[2, 2][:3]


def dekey(cell, key, tol=40):
    """border flood - never a colour sweep (0906e); enclosed key is reported, not punched"""
    out = cell.convert('RGBA')
    W, H = out.size
    px = out.load()

    def isk(x, y):
        p = px[x, y]
        return (p[3] > 0 and abs(p[0] - key[0]) <= tol and abs(p[1] - key[1]) <= tol
                and abs(p[2] - key[2]) <= tol)

    q = deque()
    seen = [[False] * W for _ in range(H)]
    for x in range(W):
        for y in (0, H - 1):
            if not seen[y][x] and isk(x, y):
                seen[y][x] = True
                q.append((x, y))
    for y in range(H):
        for x in (0, W - 1):
            if not seen[y][x] and isk(x, y):
                seen[y][x] = True
                q.append((x, y))
    while q:
        x, y = q.popleft()
        px[x, y] = (0, 0, 0, 0)
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < W and 0 <= ny < H and not seen[ny][nx] and isk(nx, ny):
                seen[ny][nx] = True
                q.append((nx, ny))
    trapped = sum(1 for y in range(H) for x in range(W) if isk(x, y))
    return out, trapped


def cells_of(path):
    im = Image.open(path).convert('RGB')
    key = sheet_key(im)
    CW, CH = im.width // COLS, im.height // ROWS
    out = {}
    for r in range(ROWS):
        for c in range(COLS):
            raw = im.crop((c * CW, r * CH, (c + 1) * CW, (r + 1) * CH))
            out[(r, c)] = dekey(raw, key)
    return out, key


def bbox_of(im):
    b = im.getbbox()
    return b if b else (0, 0, 0, 0)


def warm_mask(im):
    """flame pixels: bright AND warm. ⚠ 0907h - a warm-pixel count alone fires on a RED hull
    (yuri 3,163) and a PINK one (falva 550), so this is only ever used against a DIFF, never on a
    plate by itself."""
    W, H = im.size
    px = im.load()
    n = 0
    for y in range(H):
        for x in range(W):
            p = px[x, y]
            if p[3] < 40:
                continue
            if max(p[0], p[1], p[2]) > 150 and p[0] > p[2] + 30:
                n += 1
    return n


def diff_mask(a, b, thr=26):
    """pixels where the thrust plate departs from the flameless one"""
    W, H = a.size
    pa, pb = a.load(), b.load()
    n = 0
    xs, ys = [], []
    for y in range(H):
        for x in range(W):
            A, B = pa[x, y], pb[x, y]
            if A[3] < 40 and B[3] < 40:
                continue
            d = abs(A[0] - B[0]) + abs(A[1] - B[1]) + abs(A[2] - B[2]) + abs(A[3] - B[3])
            if d > thr:
                n += 1
                xs.append(x)
                ys.append(y)
    if not n:
        return 0, None
    return n, (min(xs), min(ys), max(xs) + 1, max(ys) + 1)


def main():
    want = sys.argv[1:] or PILOTS
    want = [p for p in want if p in PILOTS]
    report = {}
    for pilot in want:
        print('=' * 100)
        lng, sht = thr_sheet(pilot, 'long'), thr_sheet(pilot, 'short')
        L, kl = cells_of(lng)
        S, ks = cells_of(sht)
        base = None
        if pilot in FLAMELESS:
            f = os.path.join(ANIM, FLAMELESS[pilot].replace('/', os.sep))
            if os.path.exists(f):
                base, _ = cells_of(f)
        print('%s   key long rgb%s / short rgb%s   flameless partner: %s'
              % (pilot.upper(), kl, ks, FLAMELESS.get(pilot, 'NONE - freezer/maverick')))
        print('%-5s %-13s %-15s %-15s %-9s %s'
              % ('cell', 'row means', 'hull bbox long', 'aligned?', 'flame px', 'notes'))
        rec = {}
        for r in range(ROWS):
            for c in range(COLS):
                li, ltrap = L[(r, c)]
                si, strap = S[(r, c)]
                lb, sb = bbox_of(li), bbox_of(si)
                notes = []
                if ltrap:
                    notes.append('%d px of KEY trapped inside the long plate' % ltrap)
                if strap:
                    notes.append('%d px of KEY trapped inside the short plate' % strap)
                if base:
                    bi, _ = base[(r, c)]
                    nl, boxl = diff_mask(li, bi)
                    ns, _ = diff_mask(si, bi)
                    # alignment: how much of the flameless hull the thrust plate reproduces exactly
                    bb = bbox_of(bi)
                    align = 'bbox %s' % ('SAME' if bb[:2] == lb[:2] else
                                         'off %+d,%+d' % (lb[0] - bb[0], lb[1] - bb[1]))
                    fl = nl
                    if nl and boxl:
                        notes.append('flame box %dx%d at y%d' % (boxl[2] - boxl[0], boxl[3] - boxl[1], boxl[1]))
                    if ns == 0:
                        notes.append('SHORT plate is identical to the flameless hull - NO FLAME')
                    elif nl == 0:
                        notes.append('LONG plate is identical to the flameless hull - NO FLAME')
                else:
                    align = '-'
                    fl = warm_mask(li)
                rec['%d,%d' % (r, c)] = dict(long_bbox=lb, short_bbox=sb, flame=fl,
                                             trap_long=ltrap, trap_short=strap)
                print('%-5s %-13s %-15s %-15s %-9d %s'
                      % ('r%dc%d' % (r, c), ROW_MEANING[r],
                         '%d,%d %dx%d' % (lb[0], lb[1], lb[2] - lb[0], lb[3] - lb[1]),
                         align, fl, '; '.join(notes)))
            print()
        report[pilot] = rec
    out = os.path.join(ROOT, 'docs/THRUSTER_PACK_RECON_0907L.json')
    json.dump(report, open(out, 'w'), indent=1)
    print('wrote docs/THRUSTER_PACK_RECON_0907L.json')
    return 0


if __name__ == '__main__':
    sys.exit(main())
