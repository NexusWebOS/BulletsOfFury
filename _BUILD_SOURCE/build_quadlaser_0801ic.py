#!/usr/bin/env python3
"""
DROP 0801ic - THE QUAD LASER, ASSEMBLED

Mike's idea:
  "duplicate our body and damaged sprites. is there a way you can layer those
   cannons in place of the one on our sprite? make them seperate units you destroy
   as part of the miniboss. when you do destroy 1 of them, to cover the fact that
   we overlayed and anchored them on the sprite itself, swap and anchor/layer a
   smoke animation we have to cover each one."

IT WORKS, AND MORE EASILY THAN EXPECTED
Every part is already drawn on the SAME 384x384 canvas at its own final position:

  body          x  12..371   y  21..361
  cannon L out  x  22.. 67   y 159..239
  cannon L in   x  75..123   y 159..241
  cannon R in   x 260..309   y 159..241
  cannon R out  x 317..362   y 159..239

So the cannons do not need positioning at all - they composite straight on, and
their centres give the muzzle anchors for free:

  L out (44,199)   L in (99,200)   R in (284,200)   R out (339,199)

WHAT THIS BUILDS
  nqx_body_intact / nqx_body_damaged   the hull with NO cannons, so a destroyed
                                        cannon simply stops being drawn
  nqx_cannon_<slot>_<state>            each cannon as its own plate, still on the
                                        full canvas so it lines up when drawn
  nqx_glow_<n>                         the green glass sections, pulsing - Mike:
                                        "the green part at the glass sections needs
                                        to have green pixel glow"

The muzzle anchors are written to a JSON the game reads, so a laser leaves from the
barrel rather than the sprite centre.
"""
import json
import os
import re
import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
OUT = 'assets/enemies/miniboss/quadlaser'
GLOW_PHASES = 6

SLOTS = ['left_outer', 'left_inner', 'right_inner', 'right_outer']


def load(man, key):
    m = re.search(r'"%s":"([^"]+)"' % key, man)
    if not m:
        return None
    p = os.path.join(ROOT, m.group(1))
    if not os.path.exists(p):
        return None
    return np.array(Image.open(p).convert('RGBA')).astype(float)


def save(a, rel):
    Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGBA').save(os.path.join(ROOT, rel))


def main():
    man_path = os.path.join(ROOT, 'assets/manifest.js')
    man = open(man_path, encoding='utf-8').read()
    os.makedirs(os.path.join(ROOT, OUT), exist_ok=True)
    add = {}
    anchors = {}
    LIMB = {}   # slot -> the hull section that belongs to that gun

    for state in ['intact', 'damaged']:
        body = load(man, 'nql_%s_01' % state)
        if body is None:
            print('  no body for %s' % state)
            continue

        # THE HULL WITHOUT ITS GUNS. Subtracting each cannon's own footprint from
        # the body means a destroyed cannon can simply stop drawing - there is no
        # hole left behind, because the hull was never carrying it.
        hull = body.copy()

        # CUT THE WHOLE LIMB, NOT JUST THE GUN (drop 0801ie). Mike: "The 3 and hull
        # gone still have stubs left."
        #
        # Cutting only the cannon's own pixels left the PYLON behind, because the arm
        # each gun mounts to is drawn as part of the hull. Measured: in the cannon
        # band the hull is one unbroken run from x63 to x322, so removing a gun just
        # punched a hole in the middle of an arm that stayed put.
        #
        # The fix is to cut by SECTION. The body core sits between the two inner
        # cannons; everything outboard of that, inside the cannon band, belongs to
        # one of the four guns. Boundaries are derived from where the cannons
        # actually are, so this holds if the art moves.
        ext = {}
        for slot in SLOTS:
            c = load(man, 'nql_cannon_%s_intact' % slot)
            if c is None:
                continue
            ys, xs = np.where(c[..., 3] > 16)
            ext[slot] = (xs.min(), xs.max(), ys.min(), ys.max())
        if len(ext) == 4:
            # THE BAND HAS TO REACH THE SPAR TIPS (drop 0801ii). Mike: "when you
            # traced the hull, you have two stubs sticking out, those should be
            # destroyed with the last set of lasers."
            #
            # A +/-6px band around the cannons stopped at y247, and the outer wing
            # SPARS run on to y256 - so their last few rows survived the cut and
            # were left poking out of a hull with no wings. Widening the band below
            # the guns takes the whole spar with its gun. Above stays tight so the
            # canard is not eaten.
            bandY0 = min(v[2] for v in ext.values()) - 6
            bandY1 = max(v[3] for v in ext.values()) + 26
            # the inboard edge of each inner gun bounds the body core
            coreL = ext['left_inner'][1] + 4
            coreR = ext['right_inner'][0] - 4
            yy, xx = np.mgrid[0:body.shape[0], 0:body.shape[1]]
            inBand = (yy >= bandY0) & (yy <= bandY1)
            SECTION = {
                'left_outer':  inBand & (xx <= ext['left_outer'][1] + 4),
                'left_inner':  inBand & (xx > ext['left_outer'][1] + 4) & (xx <= coreL),
                'right_inner': inBand & (xx >= coreR) & (xx < ext['right_outer'][0] - 4),
                'right_outer': inBand & (xx >= ext['right_outer'][0] - 4),
            }
            for slot, sec in SECTION.items():
                piece = sec & (hull[..., 3] > 16)
                if piece.any():
                    LIMB.setdefault(slot, np.zeros(body.shape[:2], dtype=bool))
                    LIMB[slot] |= piece
                    hull[..., 3][piece] = 0
            print('   %s: cut %d px of limb into 4 sections'
                  % (state, int(sum(int((SECTION[k] & (body[..., 3] > 16)).sum()) for k in SECTION))))

        # anything still orphaned after the section cut goes to its nearest gun
        op = hull[..., 3] > 16
        lab, n = ndimage.label(op)
        if n > 1:
            sizes = ndimage.sum(op, lab, range(1, n + 1))
            main = int(np.argmax(sizes)) + 1
            for jj in range(1, n + 1):
                if jj == main:
                    continue
                piece = (lab == jj)
                ys, xs = np.where(piece)
                px, py = xs.mean(), ys.mean()
                best, bd = None, 1e9
                for slot in SLOTS:
                    if slot not in ext:
                        continue
                    cx = (ext[slot][0] + ext[slot][1]) / 2.0
                    cy = (ext[slot][2] + ext[slot][3]) / 2.0
                    d2 = (cx - px) ** 2 + (cy - py) ** 2
                    if d2 < bd:
                        bd, best = d2, slot
                if best:
                    LIMB.setdefault(best, np.zeros(body.shape[:2], dtype=bool))
                    LIMB[best] |= piece
                hull[..., 3][piece] = 0

        k = 'nqx_body_' + state
        rel = '%s/%s.png' % (OUT, k)
        save(hull, rel)
        add[k] = rel

    # each cannon kept on the FULL canvas, so drawing it needs no offset maths
    for slot in SLOTS:
        for st in ['intact', 'damaged']:
            c = load(man, 'nql_cannon_%s_%s' % (slot, st))
            if c is None:
                continue
            # draw the gun's own mount section onto its plate so they live and die
            # together
            if slot in LIMB:
                src = load(man, 'nql_%s_01' % ('intact' if st == 'intact' else 'damaged'))
                if src is not None:
                    m = LIMB[slot]
                    for ch in range(4):
                        c[..., ch] = np.where(m, src[..., ch], c[..., ch])
            k = 'nqx_cannon_%s_%s' % (slot, st)
            rel = '%s/%s.png' % (OUT, k)
            save(c, rel)
            add[k] = rel
        c = load(man, 'nql_cannon_%s_intact' % slot)
        if c is not None:
            ys, xs = np.where(c[..., 3] > 16)
            # the muzzle is the BOTTOM of the barrel - these fire downward at the
            # player, so the anchor is the low edge, not the centre
            anchors[slot] = [int((xs.min() + xs.max()) // 2), int(ys.max())]

    # ---- THE GREEN GLASS, PULSING ----
    body = load(man, 'nql_intact_01')
    if body is not None:
        op = body[..., 3] > 16
        r, g, b = body[..., 0], body[..., 1], body[..., 2]
        # the glass is the saturated green matter - not the olive hull, which is
        # green-ish but desaturated and much darker
        glass = op & (g > r + 26) & (g > b + 26) & (g > 120)
        print('  green glass pixels found: %d' % int(glass.sum()))
        for ph in range(GLOW_PHASES):
            a = np.zeros_like(body)
            t = ph / float(GLOW_PHASES)
            lift = 0.55 + 0.45 * (np.sin(t * 2 * np.pi) * 0.5 + 0.5)
            for c in range(3):
                a[..., c] = np.where(glass, np.clip(body[..., c] * lift * 1.35, 0, 255), 0)
            a[..., 3] = np.where(glass, 255, 0)
            k = 'nqx_glow_%d' % ph
            rel = '%s/%s.png' % (OUT, k)
            save(a, rel)
            add[k] = rel

    new = ''.join('"%s":"%s",' % (k, v) for k, v in sorted(add.items())
                  if ('"%s":' % k) not in man)
    if new:
        i = man.index('window.BOFX={"img":{') + len('window.BOFX={"img":{')
        man = man[:i] + new + man[i:]
        open(man_path, 'w', encoding='utf-8').write(man)

    with open(os.path.join(ROOT, 'assets/enemies/miniboss/quadlaser/anchors.json'), 'w') as f:
        json.dump(anchors, f, indent=1)

    print('  built %d keys' % len(add))
    print('  muzzle anchors (bottom of each barrel):')
    for s, xy in anchors.items():
        print('   %-13s %s' % (s, xy))


if __name__ == '__main__':
    main()
