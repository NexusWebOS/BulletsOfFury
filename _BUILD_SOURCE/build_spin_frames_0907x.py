#!/usr/bin/env python3
"""build_spin_frames_0907x.py - `ship_<pilot>_sp0..sp7`, the death spin-out reel.

    python _BUILD_SOURCE/build_spin_frames_0907x.py
    python _BUILD_SOURCE/build_spin_frames_0907x.py --write

Mike, 0907, making it a header rule: "when we get hit, we spin while explosions anchor and fire
anchor on us and animate as we spin about 540-900 degrees and -crash- and die."

⚠ ROTATION IS THE CORRECT TRANSFORM HERE, AND ONLY HERE. This repo forbids making a bank by
rotating a sprite (0906y: asked for a 27-degree bank the generator yawed the whole aircraft to
-49.1) and forbids making one by mirroring (0907b: a cosine roll is left-right symmetric, so `_l`
and `_r` come out pixel-identical and the frame reads as "banking" but never as WHICH WAY). A
SPIN-OUT is different in kind: it IS an image-plane rotation, so turning the pilot's own level
plate by 45k degrees is exact, loses no information, and carries its direction for free.

⚠ AND THE PACK'S OWN SPIN ROW IS BROKEN ON FIVE OF NINE, WHICH SILHOUETTE IoU CANNOT SEE. Matching
each cell against the level frame turned by 45k gives 0.86 on the cardinals and 0.70 on the
diagonals - respectable, and blind, because a silhouette does not record which way an engine
faces. That is 0906k's "mirror-LR IoU is blind to vertical facing" in a new coat. Measuring the
EXHAUST vector instead - from the ink centroid to the throttle-responsive centroid - the reel
should step by a constant 45 degrees, and:
    juggernaut 29   freezer 31   yuri 48   cole 64        <- clean enough to keep
    decker 115   maverick 167   falva 175   axel 180   lizzie 180
A 180 means the flame points the OPPOSITE way from travel. Lizzie's c2 and c6 are the same pose
drawn twice, so one of them thrusts forward into her own direction of flight.

⚠ THE REPAIR IS PER FRAME, NOT PER PILOT, BECAUSE MOST OF THE REEL IS GOOD. Deriving a whole reel
whenever one frame is bad would throw away authored art on eight pilots to fix one or two cells.
Every frame is measured and only the ones that fail are replaced - and the mixed result is
rendered before it is trusted, because 0907c's warning is that drift BETWEEN frames of one ship is
the thing that cannot be absorbed.

⚠ NO GLOW PHASES FOR THIS FAMILY. 0906s: "a barrel roll or spin-out is over before a flicker could
show, and phasing all 185 would have cost 320 cells for nothing." 72 rows, not 216.
"""
import os, sys, math, json
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from thruster_inventory_0907m import dekey_np, sheet, ROWS, COLS
from bake_pack_thrusters_0907p import defringe, drop_detached, RESP_LO, RESP_HI

THRUST = os.path.join(ROOT, 'assets/game/ships_thrust')
PILOTS = ['axel', 'cole', 'decker', 'falva', 'freezer', 'juggernaut', 'lizzie', 'maverick', 'yuri']
MAX_ERR = 40.0     # degrees of exhaust-direction error a frame may carry and still be kept
SP_BOX = 320       # the padded box every sp frame is stored in - see the note at its use


def exhaust_angle(rgbS, bS, rgbL, bL):
    """the direction the exhaust points, in degrees, or None if this frame has no measurable one"""
    resp = np.abs(rgbL.astype(np.int16) - rgbS.astype(np.int16)).sum(axis=2)
    resp[~(bS & bL)] = 0
    w = np.clip((resp - RESP_LO) / (RESP_HI - RESP_LO), 0.0, 1.0)
    m = w > 0.35
    if m.sum() < 8:
        return None
    ys, xs = np.nonzero(bS)
    hy, hx = ys.mean(), xs.mean()
    fy, fx = np.nonzero(m)
    wt = w[m]
    cy, cx = (fy * wt).sum() / wt.sum(), (fx * wt).sum() / wt.sum()
    return math.degrees(math.atan2(-(cy - hy), cx - hx)) % 360


def main():
    write = '--write' in sys.argv
    report = {}
    print('%-11s %s' % ('pilot', 'per-frame exhaust error, and what each sp frame is made of'))
    kept = derived = 0
    for p in PILOTS:
        rgbL, alL, _ = dekey_np(sheet(p, 'long'))
        rgbS, alS, _ = dekey_np(sheet(p, 'short'))
        CH, CW = rgbS.shape[0] // ROWS, rgbS.shape[1] // COLS
        cells, angs = {}, {}
        for c in range(COLS):
            sl = (slice(3 * CH, 4 * CH), slice(c * CW, (c + 1) * CW))
            bS, _ = drop_detached(alS[sl].copy())
            bL, _ = drop_detached(alL[sl].copy())
            aS, _, _ = defringe(rgbS[sl].copy(), bS)
            aL, _, _ = defringe(rgbL[sl].copy(), bL)
            cells[c] = (aS, bS)
            angs[c] = exhaust_angle(aS, bS, aL, bL)

        # the level frame, already cleaned by 0907p, is the source for any derived frame
        lvl = Image.open(os.path.join(THRUST, p, 'r0c0.png')).convert('RGBA')
        base = angs[0]
        row, marks = {}, []
        for c in range(COLS):
            err = None
            if base is not None and angs[c] is not None:
                step = (angs[c] - base) % 360
                exp = (c * 45) % 360
                err = min(abs(step - exp), 360 - abs(step - exp))
            ok = (c == 0) or (err is not None and err <= MAX_ERR)
            if ok:
                a, b = cells[c]
                out = np.dstack([a, np.where(b, 255, 0).astype(np.uint8)])
                out[~b] = 0
                img = Image.fromarray(out, 'RGBA')      # already the full 221 cell
                kept += 1
                marks.append('c%d keep %s' % (c, ('%2.0f' % err) if err is not None else ' 0'))
            else:
                # ⚠ ROTATE COUNTER-CLOCKWISE BY 45k, WHICH IS THE DIRECTION THE PACK'S OWN GOOD
                # FRAMES TURN (measured on juggernaut: c2 matches the level frame turned +90).
                pad = Image.new('RGBA', (SP_BOX, SP_BOX), (0, 0, 0, 0))
                pad.alpha_composite(lvl, ((SP_BOX - lvl.width) // 2, (SP_BOX - lvl.height) // 2))
                img = pad.rotate(c * 45.0, resample=Image.BICUBIC, expand=False)
                derived += 1
                marks.append('c%d DERIVE %s' % (c, ('%3.0f' % err) if err is not None else ' --'))
            # ⚠ EVERY SPIN FRAME IS STORED IN A 320px BOX CENTRED ON THE 221px CELL'S CENTRE.
            # The atlas builder solves ONE affine per pilot in the pack's 221-cell coordinates and
            # applies it to all his plates (0907u) - so a frame cropped to its own bbox, or one
            # rotated with expand=True into a bigger box, no longer shares that coordinate system
            # and would be placed by however much its bbox happened to move. A rotation of a ~200px
            # aircraft needs ~285px of room, so the box has to grow: it grows SYMMETRICALLY, and
            # the builder subtracts the known pad, which keeps the affine exactly as it was.
            box = Image.new('RGBA', (SP_BOX, SP_BOX), (0, 0, 0, 0))
            box.alpha_composite(img, ((SP_BOX - img.width) // 2, (SP_BOX - img.height) // 2))
            row[c] = box
        report[p] = marks
        print('%-11s %s' % (p, '  '.join(marks)))
        if write:
            for c, img in row.items():
                img.save(os.path.join(THRUST, p, 'sp%d.png' % c))

    print()
    print('%d authored frames kept, %d derived by rotation (of %d)' % (kept, derived, kept + derived))

    # proof: every reel, with the derived frames marked
    try:
        F = ImageFont.truetype('C:/Windows/Fonts/consolab.ttf', 16)
        FS = ImageFont.truetype('C:/Windows/Fonts/consola.ttf', 12)
    except Exception:
        F = FS = ImageFont.load_default()
    T = 150
    S = Image.new('RGB', (T * 8 + 16, (T + 30) * len(PILOTS) + 30), (14, 14, 20))
    d = ImageDraw.Draw(S)
    d.text((10, 7), 'DEATH SPIN REEL  sp0..sp7   ORANGE = derived by rotating that pilot\'s own level plate',
           font=F, fill=(255, 226, 140))
    for i, p in enumerate(PILOTS):
        y = 30 + i * (T + 30)
        for c in range(8):
            f = os.path.join(THRUST, p, 'sp%d.png' % c)
            if not os.path.exists(f):
                continue
            im = Image.open(f).convert('RGBA')
            sc = min((T - 10) / im.width, (T - 10) / im.height)
            t = Image.new('RGB', (max(1, int(im.width * sc)), max(1, int(im.height * sc))), (22, 22, 28))
            rs = im.resize(t.size, Image.NEAREST)
            t.paste(rs, (0, 0), rs)
            S.paste(t, (8 + c * T + (T - t.width) // 2, y + (T - t.height) // 2))
            lab = report[p][c]
            d.text((10 + c * T, y + T + 2), lab, font=FS,
                   fill=(255, 176, 96) if 'DERIVE' in lab else (140, 150, 180))
        d.text((10, y - 2), p.upper(), font=FS, fill=(200, 205, 225))
    S.save(os.path.join(ROOT, 'docs/SPIN_REPAIRED_0907X.png'))
    print('wrote docs/SPIN_REPAIRED_0907X.png')
    if not write:
        print('DRY RUN - no sp*.png written.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
