#!/usr/bin/env python3
"""bake_pack_thrusters_0907p.py - the pack's own thrust, animated as pixel glow. No flame mask.

    python _BUILD_SOURCE/bake_pack_thrusters_0907p.py juggernaut
    python _BUILD_SOURCE/bake_pack_thrusters_0907p.py --all --write

Mike, 0907: "animatd thrusters our way with pixel glow per frame and place where they are missing."

⚠⚠ THERE IS NO FLAME MASK IN THIS SCRIPT, AND THAT IS THE POINT. Four detectors were built and
every one broke a ship the last one had right - warm pixels fired on Yuri's red hull and Falva's
pink (0907h); adding `r - b > 40` erased Falva's pale exhaust on 30 of 32 cells (0907m); a
white-hot-core count strict enough to reject Lizzie's gold wing streaks erased five pilots
entirely (0907n); and a seeded region grow ran down Lizzie's gold wings to 11,424 px of a 16,000 px
hull (0907o). Nine hulls span red, pink, gold, green, blue, copper, teal and violet: no window in
colour space holds every flame and excludes every hull, because some of these hulls ARE flame-
coloured. A fifth threshold was not going to be the answer.

⚠ 0906s ALREADY SOLVED THIS SHAPE, BY WEIGHTING RATHER THAN BY MASKING. Its note reads: "'did this
pixel change' pulsed the whole airframe... Weight the modulation by the SIZE of the change - the
flame core moved 100+ levels and takes the full effect, the haze moved 2-5 and takes almost none."
There the change was bake-versus-prebake. Here the pack ships **the same pose at two thrust
settings**, so the change is literally the aircraft's response to throttle, per pixel, measured by
the artist. Weighting by |long - short| needs no threshold, no components, and no opinion about
what fire looks like - a hull pixel is excluded because it did not move, not because of its colour.

⚠ AND THE SILHOUETTE STILL MAY NOT MOVE - 0906s's hard rule. "An outline that jitters reads as a
sprite glitch rather than combustion", and 0906q/r spent two rounds seating each plume. So the
SHORT plate is the base and the alpha is never touched: the glow runs in colour only, between just
under short thrust and just under long thrust, and `_g1`/`_g2` are the same size and offsets as the
base frame. Where long has ink that short does not - the extra plume length - it is IGNORED.

⚠ THE SHORT SHEET IS THE BASE BECAUSE THE LONG ONE DOES NOT FIT ITS CELL. Measured across all 18
sheets: 117 of the long cells have the flame cut by the 221px cell boundary against 54 of the
short, and the worst is Lizzie's r0c4 losing 59 px. Short also clips, but by 3-16 px at the plume
tip, which is under a screen pixel at the 60px the game draws a hull.
"""
import os, sys, json
import numpy as np
from collections import deque
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from thruster_inventory_0907m import dekey_np, sheet, label, PILOTS, ROWS, COLS

OUT = os.path.join(ROOT, 'assets/game/ships_thrust')
# ⚠ THE WEIGHT'S RANGE IS MEASURED, NOT PICKED, AND THE FIRST GUESS PULSED THE WHOLE AIRFRAME.
# Summed-RGB |long - short| inside the ink, over all nine pilots' frame 0:
#     p50  11-28      p75  23-64      p90  41-132     p95  60-214
#     p99  158-757    max  589-765
# So the hull's own redraw drift between the two generations fills everything up to about p90, and
# the exhaust lives in the top one percent. RESP_D=120 put w near 1 on drift and made the response
# map solid white across the wings - 0906s's "modulating all of them equally made the entire ship
# brighten and dim", reproduced exactly. 180..430 sits in the empty band between the two
# populations, so the hull weighs ~0 and the flame weighs 1 without a mask being drawn anywhere.
RESP_LO, RESP_HI = 180.0, 430.0
PEAK_LIFT = 58.0  # ⚠ AND THE GAIN IS NORMALISED PER PILOT, because the pack's own long/short
                  # gap is not the same on every ship: Axel has 138 px above 450 and Decker has 9,
                  # Yuri 6. Riding the raw delta would give Juggernaut a strong flicker and leave
                  # Decker's invisible - which is the complaint 0906t already answered once ("the
                  # animation should be as visible as juggernauts"). Each pilot is scaled so his
                  # brightest flame pixel lifts by the same amount.
G2 = 0.75         # _g2 dips this share of the distance _g1 rises
DEAD = 40         # fewer than this many strongly-responsive px = no working thruster on that cell
FRINGE_DEPTH = 6  # 0907j: the key spill sits INSIDE the ship's own black outline
MIN_BLOB = 30


def defringe(rgb, alpha):
    """convert the de-key's residual key cast to a BLACK EDGE, never delete it (0907j).

    ⚠ THE CLASSIFIER IS READ FROM THE SHEET'S OWN KEY, NOT HARDCODED. Six sheets key on magenta and
    FALVA'S ON CYAN (0907h), so a magenta-shaped test would leave her fringe untouched and a cyan
    one would eat six coppery hulls. Cast toward magenta is r and b above g; toward cyan is g and b
    above r. Both are read off the corner pixel rather than assumed."""
    H, W = alpha.shape
    r = rgb[:, :, 0].astype(np.int16)
    g = rgb[:, :, 1].astype(np.int16)
    b = rgb[:, :, 2].astype(np.int16)
    cast = ((r > g) & (b > g) & (np.minimum(r, b) - g >= 5)) | \
           ((g > r) & (b > r) & (np.minimum(g, b) - r >= 5))
    # depth from transparency OR from the frame border (a cropped wingtip has no transparent side)
    depth = np.full((H, W), 255, np.int16)
    cur = ~alpha.copy()
    cur[0, :] = cur[-1, :] = True
    cur[:, 0] = cur[:, -1] = True
    depth[cur] = 0
    for d in range(1, FRINGE_DEPTH + 1):
        g2 = np.zeros((H, W), bool)
        g2[1:, :] |= cur[:-1, :]
        g2[:-1, :] |= cur[1:, :]
        g2[:, 1:] |= cur[:, :-1]
        g2[:, :-1] |= cur[:, 1:]
        cur = g2 & (depth > d)
        depth[cur] = d
    hit = alpha & cast & (depth <= FRINGE_DEPTH)
    out = rgb.copy()
    out[hit] = 0
    return out, int(hit.sum()), int((alpha & cast & ~hit).sum())


def drop_detached(alpha):
    """⚠ THE PACK DRAWS FLAMES THAT ARE NOT ATTACHED TO ANYTHING, AND THE README SAYS SO:
    "incorrect or missing exhaust attachments". Juggernaut's r1c2 long carries two plumes floating
    clear above the aircraft. Baked in they are debris that follows the ship around the screen."""
    lab, n = label(alpha)
    if n <= 1:
        return alpha, 0
    sz = np.bincount(lab.ravel())[1:]
    big = int(np.argmax(sz)) + 1
    out = alpha.copy()
    dropped = 0
    for i in range(1, n + 1):
        if i != big:
            out[lab == i] = False
            dropped += int(sz[i - 1])
    return out, dropped


def build(pilot):
    rgbL, alL, trapL = dekey_np(sheet(pilot, 'long'))
    rgbS, alS, trapS = dekey_np(sheet(pilot, 'short'))
    CH, CW = rgbS.shape[0] // ROWS, rgbS.shape[1] // COLS

    # pass 1 - de-fringe BOTH plates, then measure the response
    # ⚠ DE-FRINGING ONLY THE BASE PUTS THE HALO STRAIGHT BACK ON `_g1`. The lift is
    # `base + w*(long - short)`, so a magenta pixel still present in the LONG plate becomes a
    # large positive delta exactly where the base was blacked - and the first proof render came
    # out with a magenta outline traced round the wings on the bright phase only. Both plates go
    # through the same cleanup before anything is subtracted.
    prep = {}
    gmax = 1.0
    for r in range(ROWS):
        for c in range(COLS):
            sl = (slice(r * CH, (r + 1) * CH), slice(c * CW, (c + 1) * CW))
            bS, det = drop_detached(alS[sl].copy())
            bL, _ = drop_detached(alL[sl].copy())
            aS, fixed, deep = defringe(rgbS[sl].copy(), bS)
            aL, _, _ = defringe(rgbL[sl].copy(), bL)
            both = bS & bL
            delta = aL.astype(np.int16) - aS.astype(np.int16)
            resp = np.abs(delta).sum(axis=2)
            resp[~both] = 0
            w = np.clip((resp - RESP_LO) / (RESP_HI - RESP_LO), 0.0, 1.0)
            lift = float((np.abs(delta).max(axis=2) * w).max())
            gmax = max(gmax, lift)
            prep[(r, c)] = (aS, bS, delta, resp, w, det, fixed, deep)

    gain = PEAK_LIFT / gmax
    cells, rep = {}, {}
    for k, (aS, bS, delta, resp, w, det, fixed, deep) in prep.items():
        w3 = w[:, :, None]
        base = aS.astype(np.float32)
        g1 = np.clip(base + w3 * delta * gain, 0, 255).astype(np.uint8)
        g2 = np.clip(base - w3 * delta * (gain * G2), 0, 255).astype(np.uint8)
        peak = int(resp.max()) if resp.size else 0
        cells[k] = dict(rgb=aS, alpha=bS, g1=g1, g2=g2, w=w)
        rep['r%dc%d' % k] = dict(peak=peak, responsive=int((w > 0.35).sum()), detached=det,
                                 fringe=fixed, deep=deep, dead=bool((w > 0.35).sum() < DEAD))
    rep['_gain'] = round(gain, 4)
    return cells, rep


def rgba(d, which='rgb'):
    a = d[which] if which != 'rgb' else d['rgb']
    out = np.dstack([a, np.where(d['alpha'], 255, 0).astype(np.uint8)])
    out[~d['alpha']] = 0
    return Image.fromarray(out, 'RGBA')


def main():
    want = [p for p in sys.argv[1:] if p in PILOTS] or (PILOTS if '--all' in sys.argv else ['juggernaut'])
    write = '--write' in sys.argv
    try:
        F = ImageFont.truetype('C:/Windows/Fonts/consolab.ttf', 15)
    except Exception:
        F = ImageFont.load_default()
    allrep = {}
    for pilot in want:
        cells, rep = build(pilot)
        allrep[pilot] = rep
        cellv = [v for k, v in rep.items() if k != '_gain']
        dead = [k for k, v in rep.items() if k != '_gain' and v['dead']]
        det = sum(1 for v in cellv if v['detached'])
        print('%-11s gain x%.2f   responsive px %d..%d   fringe blacked %d   detached blobs cut from %d cells'
              % (pilot, rep['_gain'], min(v['responsive'] for v in cellv),
                 max(v['responsive'] for v in cellv), sum(v['fringe'] for v in cellv), det))
        if dead:
            print('             NO WORKING THRUSTER on %d cells: %s' % (len(dead), ', '.join(dead)))
        if write:
            d = os.path.join(OUT, pilot)
            os.makedirs(d, exist_ok=True)
            for (r, c), v in cells.items():
                rgba(v).save(os.path.join(d, 'r%dc%d.png' % (r, c)))
                rgba(v, 'g1').save(os.path.join(d, 'r%dc%d_g1.png' % (r, c)))
                rgba(v, 'g2').save(os.path.join(d, 'r%dc%d_g2.png' % (r, c)))
            print('             wrote 96 plates to assets/game/ships_thrust/%s/' % pilot)

        # proof: the three phases of frame 0, zoomed on the tail, plus the response map
        v = cells[(0, 0)]
        ys, xs = np.nonzero(v['alpha'])
        y0, y1, x0, x1 = ys.min(), ys.max(), xs.min(), xs.max()
        cy = int(y0 + 0.52 * (y1 - y0))
        box = (x0, cy, x1 + 1, y1 + 1)
        Z = 4
        tiles = [('base (short thrust)', rgba(v)), ('_g1 bright', rgba(v, 'g1')),
                 ('base', rgba(v)), ('_g2 dim', rgba(v, 'g2'))]
        wimg = Image.fromarray((np.clip(v['w'], 0, 1) * 255).astype(np.uint8)).convert('RGBA')
        tiles.append(('thrust response (the weight)', wimg))
        cw = (box[2] - box[0]) * Z + 12
        ch = (box[3] - box[1]) * Z + 26
        S = Image.new('RGB', (cw * len(tiles), ch), (14, 14, 20))
        dr = ImageDraw.Draw(S)
        for i, (lab, im) in enumerate(tiles):
            cr = im.crop(box)
            t = Image.new('RGB', cr.size, (24, 24, 30))
            t.paste(cr, (0, 0), cr)
            S.paste(t.resize((cr.width * Z, cr.height * Z), Image.NEAREST), (i * cw + 6, 22))
            dr.text((i * cw + 6, 4), lab, font=F, fill=(255, 214, 110))
        S.save(os.path.join(ROOT, 'docs/THRUST_GLOW_%s_0907P.png' % pilot.upper()))
        print('             wrote docs/THRUST_GLOW_%s_0907P.png' % pilot.upper())
    json.dump(allrep, open(os.path.join(ROOT, 'docs/THRUST_GLOW_0907P.json'), 'w'), indent=1)
    return 0


if __name__ == '__main__':
    sys.exit(main())
