#!/usr/bin/env python3
"""thruster_inventory_0907m.py - every defect on the 18 fleet thruster sheets, counted.

    python _BUILD_SOURCE/thruster_inventory_0907m.py
    python _BUILD_SOURCE/thruster_inventory_0907m.py juggernaut lizzie

Mike, 0907: "place where they are missing." The pack's README lists what to expect - "incorrect or
missing exhaust attachments, clipped/tight flame spacing, and rotation errors" - so this counts
each of those per cell rather than trusting or dismissing the warning.

WHAT IS COUNTED, AND WHY EACH ONE MATTERS
  DETACHED   a flame blob that does not touch the hull. Juggernaut's r1c2 long carries two of them
             floating clear above the aircraft. Baked in, they are debris that follows the ship.
  MISSING    a pose with no flame at all, which is what Mike is asking to have filled in. ⚠ A
             NOSE-ON VIEW HAS NO VISIBLE EXHAUST BY DESIGN and must not be counted as missing -
             that is the somersault frame where you are looking at the front of the aircraft.
  CLIPPED    ink touching the cell border, i.e. the flame runs out of its 221px cell. The long
             sheets do this constantly; a clipped plume ends in a straight cut across the flame.
  TRAPPED    key colour enclosed by artwork, which a border flood cannot reach (0906e).

⚠ THE FLAME IS FOUND BY BRIGHTNESS *AND* HUE *AND* SATURATION TOGETHER, AND EVEN THEN IT IS
CONFIRMED AGAINST A RENDER. 0907h caught a warm-pixel count reporting flame on Yuri (3,163 px) and
Falva (550) when neither had one - his aircraft is RED and hers is PINK, so the test was reading
their paint. Cole's green, Axel's blue and Juggernaut's copper cannot trip it, but Yuri and Falva
are checked by eye before any number about them is quoted.
"""
import os, sys, json
import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
THR = os.path.join(ROOT, '_ART_SOURCES_THRUSTERS')
COLS, ROWS = 8, 4
ROW_MEANING = ['barrel roll', 'somersault', 'banked turn', 'pivot(spin)']
PILOTS = ['axel', 'cole', 'decker', 'falva', 'freezer', 'juggernaut', 'lizzie', 'maverick', 'yuri']
# the somersault frames that look at the FRONT of the aircraft - no exhaust is correct there
NOSE_ON_OK = {(1, 2), (1, 6)}
MIN_BLOB = 30


def sheet(pilot, which):
    return os.path.join(THR, pilot.capitalize(), '%s-thrusters-%s-source.png' % (pilot, which))


def dekey_np(path):
    """returns (rgb uint8 HxWx3, alpha bool HxW, trapped bool HxW) for the whole sheet"""
    im = Image.open(path).convert('RGB')
    a = np.asarray(im).astype(np.int16)
    key = a[2, 2].copy()
    iskey = (np.abs(a - key).max(axis=2) <= 40)
    H, W = iskey.shape
    # border flood over the key mask, iteratively (never a colour sweep - 0906e)
    reach = np.zeros((H, W), bool)
    seed = np.zeros((H, W), bool)
    seed[0, :] = seed[-1, :] = True
    seed[:, 0] = seed[:, -1] = True
    cur = iskey & seed
    while cur.any():
        reach |= cur
        g = np.zeros((H, W), bool)
        g[1:, :] |= cur[:-1, :]
        g[:-1, :] |= cur[1:, :]
        g[:, 1:] |= cur[:, :-1]
        g[:, :-1] |= cur[:, 1:]
        cur = g & iskey & ~reach
    return a.astype(np.uint8), ~reach, (iskey & ~reach)


def label(mask):
    """connected components, 4-connected. no scipy here, so this is a scanline union-find."""
    H, W = mask.shape
    lab = np.zeros((H, W), np.int32)
    parent = [0]

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[max(ra, rb)] = min(ra, rb)

    nxt = 1
    for y in range(H):
        row = mask[y]
        for x in np.nonzero(row)[0]:
            up = lab[y - 1, x] if y else 0
            lf = lab[y, x - 1] if x else 0
            if up and lf:
                lab[y, x] = min(up, lf)
                union(up, lf)
            elif up or lf:
                lab[y, x] = up or lf
            else:
                lab[y, x] = nxt
                parent.append(nxt)
                nxt += 1
    if nxt == 1:
        return lab, 0
    roots = np.array([find(i) for i in range(nxt)], np.int32)
    remap = {r: i + 1 for i, r in enumerate(sorted(set(roots[1:].tolist())))}
    out = np.zeros_like(lab)
    nz = lab > 0
    out[nz] = [remap[roots[v]] for v in lab[nz]]
    return out, len(remap)


def flame_mask(rgb, alpha):
    """bright AND warm AND saturated - all three, per the 0907h trap"""
    r = rgb[:, :, 0].astype(np.int16)
    g = rgb[:, :, 1].astype(np.int16)
    b = rgb[:, :, 2].astype(np.int16)
    mx = np.maximum(np.maximum(r, g), b)
    mn = np.minimum(np.minimum(r, g), b)
    sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1), 0.0)
    warm = (r >= g) & (g >= b - 12) & (r - b > 40)
    return alpha & (mx > 205) & (sat > 0.55) & warm


def main():
    want = [p for p in (sys.argv[1:] or PILOTS) if p in PILOTS]
    report, tot = {}, dict(detached=0, missing=0, clipped=0, trapped=0)
    for pilot in want:
        report[pilot] = {}
        for which in ('long', 'short'):
            rgb, alpha, trap = dekey_np(sheet(pilot, which))
            CH, CW = rgb.shape[0] // ROWS, rgb.shape[1] // COLS
            hits = []
            for r in range(ROWS):
                for c in range(COLS):
                    sl = (slice(r * CH, (r + 1) * CH), slice(c * CW, (c + 1) * CW))
                    A, T = alpha[sl], trap[sl]
                    F = flame_mask(rgb[sl], A)
                    hull = A & ~F
                    lab, n = label(A)
                    # the body is the largest component; anything else is detached
                    det = 0
                    if n > 1:
                        sizes = np.bincount(lab.ravel())[1:]
                        big = int(np.argmax(sizes)) + 1
                        for i in range(1, n + 1):
                            if i != big and sizes[i - 1] >= MIN_BLOB:
                                det += int(sizes[i - 1])
                    edge = int(A[0, :].sum() + A[-1, :].sum() + A[:, 0].sum() + A[:, -1].sum())
                    flame = int(F.sum())
                    d = dict(flame=flame, detached=det, clipped=edge, trapped=int(T.sum()),
                             hull=int(hull.sum()))
                    report[pilot]['%s r%dc%d' % (which, r, c)] = d
                    tags = []
                    if det:
                        tags.append('DETACHED %d px' % det); tot['detached'] += 1
                    if flame < 60 and (r, c) not in NOSE_ON_OK:
                        tags.append('NO FLAME'); tot['missing'] += 1
                    if edge:
                        tags.append('clipped %d px on the cell border' % edge); tot['clipped'] += 1
                    if T.sum():
                        tags.append('%d px key trapped' % int(T.sum())); tot['trapped'] += 1
                    if tags:
                        hits.append('   %-6s r%dc%d %-13s %s'
                                    % (which, r, c, ROW_MEANING[r], '; '.join(tags)))
            if hits:
                print('%s %s' % (pilot.upper(), which))
                for h in hits:
                    print(h)
        print()
    print('=' * 92)
    print('across %d sheets: %d cells with DETACHED flame, %d with NO FLAME, %d CLIPPED, %d with TRAPPED key'
          % (len(want) * 2, tot['detached'], tot['missing'], tot['clipped'], tot['trapped']))
    json.dump(report, open(os.path.join(ROOT, 'docs/THRUSTER_INVENTORY_0907M.json'), 'w'), indent=1)
    print('wrote docs/THRUSTER_INVENTORY_0907M.json')
    return 0


if __name__ == '__main__':
    sys.exit(main())
