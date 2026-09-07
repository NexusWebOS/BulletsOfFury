#!/usr/bin/env python3
"""map_pack_frames_0907s.py - the 25 game frames of all nine pilots, DERIVED from the pack.

    python _BUILD_SOURCE/map_pack_frames_0907s.py            # table for all nine
    python _BUILD_SOURCE/map_pack_frames_0907s.py juggernaut --proof

⚠ THE ROW ORDER IS NOT THE SAME ON EVERY SHEET, WHICH THE PACK README SAYS AND THIS MEASURES.
"known issues include repeated angles, underside/design drift, and inconsistent rotation order."
Measured on row 2 (the bank ladder) with the nose-over-tail lean from 0907j:
    six pilots  c0 c1 c2 bank LEFT, c3 and c7 are level, c4 c5 c6 bank RIGHT
    COLE and LIZZIE have **c2 and c5 SWAPPED** - cole c2 reads +0.099 and c5 -0.099, lizzie
                c2 +0.179 and c5 -0.190, i.e. one frame from each side sits in the other's block
    FALVA hardly banks at all - her whole row runs -0.068..+0.057 where everyone else reaches
                +/-0.3 - so her frames are near-pure ROLLS and her ladder is ordered by width
So the map is derived per pilot from that pilot's own pixels and the swap corrects itself. Hand-
listing it would have shipped Cole and Lizzie banking the wrong way on two frames each, on a
screen where nothing fails.

⚠ AND THE SOMERSAULT IS TAKEN AS AUTHORED, WHICH IS WHAT MAKES ALL NINE MATCH. Mike, 0907: "they
all must somersalt the same way." Measured on all nine (0907q) by which quarter frame shows lit
engine bells: **c2 is TAIL-ON and c6 is NOSE-ON, unanimously**. The pack is already internally
consistent, so row 1 goes straight across and every pilot loops the same way. This does flip
Maverick's and Lizzie's OLD authored direction - their reels had nose-on at so2 (0906z) - but
those reels are being replaced wholesale, so matching the pack costs nothing and reversing all
nine to chase one legacy reel would be the harder, worse answer.

⚠ ROW 3 IS A 360-DEGREE IN-PLANE SPIN AND NOTHING IN THE GAME USES IT. Verified on Juggernaut by
matching each cell against the level frame turned by each eighth of a circle: 0/315/270/225/180/
135/90/45, monotone, fit 0.76-0.90. It is not `_pv*`; it is a ready-made spin-out reel.
"""
import os, sys, json
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
THRUST = os.path.join(ROOT, 'assets/game/ships_thrust')
LEVEL_LEAN = 0.030     # below this a frame is level, not banked
SWAP_LEAN = 0.085      # ⚠ above this the lean is decisive enough to move a frame between blocks.
                       # 0.050 was too loose: FALVA's whole row runs -0.068..+0.057, which is her
                       # noise floor rather than a lean, and it tripped the Cole/Lizzie swap on her
                       # by accident. Cole reads +/-0.099 and Lizzie +/-0.190, so 0.085 keeps the
                       # two real transpositions and leaves her positional order alone.
CANON_L, CANON_R, CANON_0 = [0, 1, 2], [4, 5, 6], [3, 7]


def ink(pilot, cell):
    a = np.asarray(Image.open(os.path.join(THRUST, pilot, cell + '.png')).convert('RGBA'))
    al = a[:, :, 3] > 40
    ys, xs = np.nonzero(al)
    return al, int(ys.min()), int(ys.max()), int(xs.min()), int(xs.max())


def lean(al, y0, y1, x0, x1):
    rows = []
    for y in range(y0, y1 + 1):
        xr = np.nonzero(al[y])[0]
        rows.append((xr.mean(), len(xr)) if len(xr) else (0.0, 0))
    live = [i for i, (_, n) in enumerate(rows) if n]
    if len(live) < 6:
        return 0.0
    k = max(1, int(round(len(live) * 0.15)))

    def band(idx):
        tw = sum(rows[i][1] for i in idx)
        return sum(rows[i][0] * rows[i][1] for i in idx) / tw if tw else 0.0

    return (band(live[:k]) - band(live[-k:])) / max(1.0, (x1 - x0 + 1))


def bank_map(pilot):
    """-> {frame suffix: cell}, plus the measurements it was derived from"""
    al0, ay0, ay1, ax0, ax1 = ink(pilot, 'r0c0')
    LW = ax1 - ax0 + 1
    L, W = {}, {}
    for c in range(8):
        al, y0, y1, x0, x1 = ink(pilot, 'r2c%d' % c)
        L[c] = lean(al, y0, y1, x0, x1)
        W[c] = (x1 - x0 + 1) / LW

    left, right, level = list(CANON_L), list(CANON_R), list(CANON_0)
    swapped = False
    # correct the cole/lizzie transposition from the pixels rather than from a hand-written list
    for a in list(left):
        if L[a] > SWAP_LEAN:
            for b in list(right):
                if L[b] < -SWAP_LEAN:
                    left.remove(a); right.remove(b); left.append(b); right.append(a)
                    swapped = True
                    break
    # a frame sitting in a bank block but measuring level belongs with the level frames
    for blk in (left, right):
        for c in list(blk):
            if abs(L[c]) < LEVEL_LEAN and W[c] > 0.97:
                blk.remove(c); level.append(c)

    # ⚠ SHALLOW FIRST, AND THE FIRST CUT HAD IT BACKWARDS. The names are consumed in the order
    # `_pv1` (17 deg), `_l` (20), `_pv0` (27), so the list must run shallow -> deep. Sorting by
    # -abs(lean) put the DEEPEST frame on `_pv1` and the shallowest on `_pv0`, i.e. the pivot ladder
    # ran backwards on all nine pilots - the ship would have leaned hardest at its smallest input.
    # Ascending abs(lean); and where the leans are noise, ascending narrowness (widest = shallowest).
    flat = max(abs(L[c]) for c in left + right) < SWAP_LEAN if (left or right) else True
    key = (lambda c: -W[c]) if flat else (lambda c: abs(L[c]))
    left.sort(key=key)
    right.sort(key=key)
    level.sort(key=lambda c: -W[c])

    m = {'_pv2': level[0] if level else CANON_0[0]}
    for names, blk in (('_pv1 _l _pv0'.split(), left), ('_pv3 _r _pv4'.split(), right)):
        for i, nm in enumerate(names):
            m[nm] = blk[min(i, len(blk) - 1)] if blk else m['_pv2']
    return m, L, W, swapped, len(left), len(right)


def frames(pilot):
    m, L, W, swapped, nl, nr = bank_map(pilot)
    out = [('', 'r0c0'), ('_nf', 'r0c0')]
    for k in ('_pv0', '_pv1', '_pv2', '_pv3', '_pv4', '_l', '_r'):
        out.append((k, 'r2c%d' % m[k]))
    out += [('_br%d' % i, 'r0c%d' % i) for i in range(8)]
    out += [('_so%d' % i, 'r1c%d' % i) for i in range(8)]
    return out, (L, W, swapped, nl, nr)


def main():
    pilots = sorted(os.listdir(THRUST))
    want = [p for p in sys.argv[1:] if p in pilots] or pilots
    proof = '--proof' in sys.argv
    table = {}
    for pilot in want:
        fr, (L, W, swapped, nl, nr) = frames(pilot)
        table[pilot] = {k: v for k, v in fr}
        bank = ' '.join('%s<-%s' % (k, dict(fr)[k]) for k in
                        ('_pv0', '_pv1', '_pv2', '_pv3', '_pv4', '_l', '_r'))
        note = []
        if swapped:
            note.append('c2/c5 SWAP corrected')
        if nl < 3 or nr < 3:
            note.append('%d left / %d right authored - short side shares a cell' % (nl, nr))
        print('%-11s %s%s' % (pilot.upper(), bank, ('   [%s]' % '; '.join(note)) if note else ''))
        if proof:
            try:
                F = ImageFont.truetype('C:/Windows/Fonts/consolab.ttf', 15)
                FS = ImageFont.truetype('C:/Windows/Fonts/consola.ttf', 13)
            except Exception:
                F = FS = ImageFont.load_default()
            T = 200
            cols = 9
            rows = (len(fr) + cols - 1) // cols
            S = Image.new('RGB', (T * cols + 8, (T + 40) * rows + 26), (14, 14, 20))
            d = ImageDraw.Draw(S)
            d.text((6, 5), '%s  -  25 game frames from the thruster pack' % pilot.upper(),
                   font=F, fill=(255, 226, 140))
            for i, (suf, cellk) in enumerate(fr):
                im = Image.open(os.path.join(THRUST, pilot, cellk + '.png')).convert('RGBA')
                b = im.getbbox(); cr = im.crop(b)
                sc = min((T - 14) / cr.width, (T - 20) / cr.height)
                t = Image.new('RGB', (int(cr.width * sc), int(cr.height * sc)), (24, 24, 30))
                rs = cr.resize(t.size, Image.NEAREST)
                t.paste(rs, (0, 0), rs)
                x, y = 4 + (i % cols) * T, 26 + (i // cols) * (T + 40)
                S.paste(t, (x + (T - t.width) // 2, y + (T - t.height) // 2))
                d.text((x + 4, y + T + 2), 'ship_%s%s' % (pilot, suf), font=FS, fill=(238, 240, 250))
                d.text((x + 4, y + T + 18), cellk, font=FS, fill=(150, 160, 200))
            S.save(os.path.join(ROOT, 'docs/PACK_FRAMES_%s_0907S.png' % pilot.upper()))
            print('             wrote docs/PACK_FRAMES_%s_0907S.png' % pilot.upper())
    json.dump(table, open(os.path.join(ROOT, 'assets/data/pack_frame_map_0907s.json'), 'w'), indent=1)
    print()
    print('wrote assets/data/pack_frame_map_0907s.json  (%d pilots x 25 frames)' % len(table))
    return 0


if __name__ == '__main__':
    sys.exit(main())
