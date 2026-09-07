#!/usr/bin/env python3
"""build_ship_atlas_0907u.py - rebuild the player ship sheet from the thruster pack.

    python _BUILD_SOURCE/build_ship_atlas_0907u.py            # geometry + proof, writes nothing
    python _BUILD_SOURCE/build_ship_atlas_0907u.py --write

Replaces all 329 `BOFX.ships` rows with 369: nine pilots x (25 frames + 16 glow phases). Five
pilots gain a somersault reel they never had (0906z: "axel, decker, falva, freezer, juggernaut
have no `so` frames whatsoever").

⚠⚠ AND IT CARRIES THE B-42, WHICH IS ALREADY BROKEN ON HEAD. `LIZZIE_B42_RECTS` is seventeen
hard-coded rects in **game.js**, deliberately placed there so a manifest regeneration could not
lose them - and 0906z's compaction repacked every ship rect without updating them. Resolved against
the current atlas they render as fragments of Cole's, Freezer's and Maverick's aircraft; resolved
against any pre-compaction backup they are the intact yellow bomber. So the costume behind the
BOMBER password has been showing chopped-up pieces of other pilots' ships since 0906z.
0906z's own safety note said the repack was safe because "BOFX.cells has ZERO rows on it, so the
ship rects are the only consumers and can all be enumerated" - true of the manifest, and there was
a SECOND consumer, in the file the note was written in. This build lifts those seventeen frames out
of the last pre-compaction backup, packs them into the new sheet, and rewrites the table.
⚠ WHICH IS THIS FILE'S OWN "a key does not own its file" RULE, one level out: enumerate the
consumers of a SHEET, not the rows of one table that happens to point at it.

⚠ THE HULL IS FITTED TO 0.79 OF THE CANVAS AND THE EXHAUST LIVES IN WHAT IS LEFT. `drawPlayer`
blits the canvas at a fixed `SHIP_DRAW_H` of 60, so a hull drawn at 0.79 of canvas height is 47.4
screen px for every pilot, and the flame gets the remaining 0.21. Measured, every pilot's tallest
frame is 1.112-1.198x his hull, so all nine fit with room to spare. Two ships move a long way:
FALVA +33% and YURI +32%, because they have been drawing at 0.593 and 0.598 against a fleet that
sits at 0.72-0.84 - the outlier this repo has had open since 0906x. Nobody else moves more than 9%.

⚠ AND THE HULL/EXHAUST SPLIT IS TAKEN FROM THE INK WIDTH PROFILE, NOT FROM A FLAME DETECTOR. A
hull row spans the wingspan; a plume row does not. The boundary was drawn on all nine level frames
and checked by eye before it was used for anything (docs/HULL_BOUNDARY_0907T.png). The throttle-
response map was tried first and returned total/hull = 1.000 on seven of nine, because scanning for
"the last row that is not mostly flame" runs straight to the bottom of the ink.

⚠ ONE AFFINE PER PILOT, APPLIED TO ALL 41 PLATES. Centring each frame's own bbox would slide a
banked ship sideways relative to the level one - the pack draws every pose in place inside its
221px cell, and that relative placement IS the animation. Scale and offset are solved once from the
level frame and every other frame rides the same transform.

⚠ THE SHEET IS REBUILT, NOT APPENDED TO, AND THAT IS ONLY SAFE BECAUSE EVERY CONSUMER IS KNOWN:
`BOFX.cells` has zero rows on it (checked, not assumed), all 329 `BOFX.ships` rows are replaced,
and the B-42 table is the third consumer, handled above. 0906y's note about six appends orphaning
59% of the atlas is why this rebuilds instead.
"""
import os, re, sys, json, shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
THRUST = os.path.join(ROOT, 'assets/game/ships_thrust')
ATLAS = os.path.join(ROOT, 'assets/game/atlas/bof_player_ships_barrel_rolls.png')
PRE = ATLAS + '.0906z.bak'          # the last atlas before the compaction that broke the B-42
MANIFEST = os.path.join(ROOT, 'assets/manifest.js')
GAMEJS = os.path.join(ROOT, 'assets/game.js')
TARGET_INK = 0.79
PAD = 2
STEADY = ['', '_l', '_r', '_pv0', '_pv1', '_pv2', '_pv3', '_pv4']   # the suffixes that carry phases


def load_json(p):
    return json.load(open(os.path.join(ROOT, p)))


def _components(mask):
    """(number of blobs >= 40 px, size of the biggest) - a whole aircraft is ONE blob"""
    H, W = mask.shape
    seen = np.zeros((H, W), bool)
    big = cnt = 0
    idx = np.argwhere(mask)
    for y0, x0 in idx:
        if seen[y0, x0]:
            continue
        st = [(y0, x0)]
        seen[y0, x0] = True
        n = 0
        while st:
            y, x = st.pop()
            n += 1
            for ny, nx in ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)):
                if 0 <= ny < H and 0 <= nx < W and mask[ny, nx] and not seen[ny, nx]:
                    seen[ny, nx] = True
                    st.append((ny, nx))
        if n >= 40:
            cnt += 1
            big = max(big, n)
    return cnt, big


def ink_box(a):
    ys, xs = np.nonzero(a[:, :, 3] > 40)
    if not len(ys):
        return None
    return int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1


def plates(pilot, fmap):
    """every plate this pilot needs -> {suffix: cell file stem}"""
    out = {}
    for suf, cell in fmap.items():
        out[suf] = cell
        if suf in STEADY:
            out[suf + '_g1'] = cell + '_g1'
            out[suf + '_g2'] = cell + '_g2'
    return out


def solve(pilot, cur, geom, fmap):
    """one scale + offset for this pilot, from his level frame

    ⚠ THE CANVAS IS SIZED TO THE ART, NOT THE ART TO THE OLD CANVAS. Keeping each pilot's existing
    canvas height made `s = TARGET_INK * canvasH / hull` come out at 1.15-1.40 on every single
    pilot, i.e. every one of the 386 plates was being UPSCALED from 221px source and stored at
    250-310px. That is resolution the art does not have, it cost the sheet 13.6 MB against the 6.6
    MB it replaced, and it puts an extra resample in front of a sprite the game then reduces to
    47px - on a hull whose black edges this repo has already lost once to smoothing (0811r).

    Nothing depends on the canvas's absolute size. `drawPlayer` blits at a fixed `SHIP_DRAW_H` and
    takes its width from `naturalWidth/naturalHeight`, so only the RATIOS matter: the hull draws at
    `TARGET_INK * 60` px whatever the canvas is. Setting `canvasH = hull / TARGET_INK` therefore
    gives s = 1.000, native pixels, and a much smaller sheet, with the drawn size unchanged.
    The vertical anchor is carried across in the same proportion so nothing moves on screen."""
    nf = cur['ship_%s_nf' % pilot]
    oldH = nf[7]
    hull = geom[pilot]['hull']
    canvasH = int(round(hull / TARGET_INK))
    s = TARGET_INK * canvasH / float(hull)          # 1.000 by construction, up to the rounding

    lvl = np.asarray(Image.open(os.path.join(THRUST, pilot, fmap[pilot]['_nf'] + '.png')).convert('RGBA'))
    b = ink_box(lvl)
    hb = geom[pilot]['hull_bot']
    # the level frame's hull centre, in cell coordinates
    cx = (b[0] + b[2]) / 2.0
    cy = (b[1] + hb + 1) / 2.0
    # ...must land where the CURRENT flameless hull's centre sits PROPORTIONALLY, so nothing jumps
    ty = (nf[5] + nf[3] / 2.0) * (canvasH / float(oldH))
    return dict(s=s, cx=cx, cy=cy, canvasH=canvasH, ty=ty, canvasW_old=nf[6], oldH=oldH)


def build(write=False):
    cur = load_json('docs/_ships_current.json')
    geom = load_json('docs/PACK_HULL_GEOM_0907T.json')
    fmap = load_json('assets/data/pack_frame_map_0907s.json')
    pilots = sorted(fmap)

    made = {}        # (pilot, suffix) -> (RGBA trim image, offX, offY, canvasW, canvasH)
    report = []
    for p in pilots:
        S = solve(p, cur, geom, fmap)
        s, canvasH = S['s'], S['canvasH']
        pl = plates(p, fmap[p])
        # first pass: scale every plate, find the widest ink so the canvas can be sized
        scaled = {}
        maxw = 0
        for suf, stem in pl.items():
            im = Image.open(os.path.join(THRUST, p, stem + '.png')).convert('RGBA')
            if suf == '_nf':
                # ⚠ `_nf` MUST ACTUALLY BE FLAMELESS, AND THE FIRST BUILD MADE IT A COPY OF THE
                # BASE. 0906q's note is explicit - "ship_*_nf stays flameless for any surface that
                # wants a cold airframe" - and the pack cell it maps to has a lit exhaust, so the
                # rebuild quietly turned the cold airframe into a second hot one. Nothing consumes
                # `_nf` today, which is exactly why it would have sat wrong until something did:
                # this file already records `ship_<pilot>_t` shipping under a comment calling it
                # "the flameless airframe" when it was the flame-BAKED one.
                # The exhaust is cut at the measured hull boundary (the ink-width profile drawn and
                # eyeballed on all nine in docs/HULL_BOUNDARY_0907T.png), not at a colour threshold.
                a = np.array(im)
                a[geom[p]['hull_bot'] + 1:, :, 3] = 0
                im = Image.fromarray(a, 'RGBA')
            n = im.resize((max(1, int(round(im.width * s))), max(1, int(round(im.height * s)))),
                          Image.LANCZOS)
            a = np.asarray(n)
            bb = ink_box(a)
            scaled[suf] = (n, bb)
            if bb:
                maxw = max(maxw, bb[2] - bb[0])
        canvasW = int(maxw + 2 * PAD)
        # x offset so the level hull's centre sits on the canvas centre line
        tx = canvasW / 2.0 - S['cx'] * s
        ty = S['ty'] - S['cy'] * s
        lo_y = min(bb[1] for _, bb in scaled.values() if bb)
        hi_y = max(bb[3] for _, bb in scaled.values() if bb)
        shift = 0.0
        if ty + lo_y < 0:
            shift = -(ty + lo_y)
        elif ty + hi_y > canvasH:
            shift = canvasH - (ty + hi_y)
        ty += shift
        for suf, (n, bb) in scaled.items():
            if not bb:
                continue
            trim = n.crop(bb)
            offX = int(round(tx + bb[0]))
            offY = int(round(ty + bb[1]))
            offX = max(0, min(canvasW - trim.width, offX))
            offY = max(0, min(canvasH - trim.height, offY))
            made[(p, suf)] = (trim, offX, offY, canvasW, canvasH)
        nf = cur['ship_%s_nf' % p]
        report.append((p, s, S['canvasW_old'], canvasW, canvasH,
                       nf[3] / nf[7] * 60, TARGET_INK * 60, shift))

    print('%-11s %-7s %-15s %-9s %-15s %s'
          % ('pilot', 'scale', 'canvas', 'plates', 'hull draws', 'anchor shift'))
    for p, s, cw0, cw, ch, was, now, sh in report:
        n = sum(1 for k in made if k[0] == p)
        print('%-11s %-7.3f %-15s %-9d %-15s %s'
              % (p, s, '%dx%d (was %dx%d)' % (cw, ch, cw0, ch), n,
                 '%.1f -> %.1f px' % (was, now), ('%+.1f px' % sh) if sh else '-'))

    # the B-42, lifted out of the last atlas that still has it
    #
    # ⚠⚠ THE SOURCE RECTS COME FROM A FIXED FILE, NOT FROM game.js - BECAUSE THIS SCRIPT REWRITES
    # game.js. The first cut read `LIZZIE_B42_RECTS` out of game.js, cropped those coordinates from
    # the PRE-COMPACTION atlas, then wrote NEW coordinates back into game.js. Run it a second time
    # and it cropped the NEW sheet's coordinates out of the OLD sheet: the bomber came back as four
    # disconnected fragments, and worse each run. A script that consumes its own output is not
    # idempotent and this one had no way to notice.
    #
    # ⚠ AND THE BYTE-COMPARE MEANT TO CATCH IT PASSED EVERY TIME, because it compared the packed
    # plate against the crop it had just taken - the same wrong pixels on both sides. That is this
    # repo's own "a probe that recomputes the thing under test cannot find the bug", self-inflicted.
    # What caught it was probe_shipframes_0907v's CONNECTIVITY check: an aeroplane is ONE body and
    # the broken version was four. That check runs here now, before the write, where it can refuse.
    b42 = {}
    old = load_json('assets/data/lizzie_b42_source_rects.json')
    pre = Image.open(PRE).convert('RGBA')
    frag = []
    for k, r in old.items():
        crop = pre.crop((r[0], r[1], r[0] + r[2], r[1] + r[3]))
        al = np.asarray(crop)[:, :, 3] > 40
        tot = int(al.sum())
        n, big = _components(al)
        if not tot or big / float(tot) < 0.80:
            frag.append('%s: %d parts, biggest holds %.0f%%'
                        % (k or '<base>', n, 100.0 * big / max(1, tot)))
        b42[k] = (crop, r[4], r[5], r[6], r[7])
    print('\ncarried %d B-42 frames out of %s' % (len(b42), os.path.basename(PRE)))
    if frag:
        print('REFUSING TO WRITE - these B-42 source crops are not a single body:')
        for f in frag:
            print('   ' + f)
        raise SystemExit(1)
    print('B-42 source check: all %d frames are one connected body' % len(b42))

    # ⚠ AND ITS CANVAS IS RE-SCALED ONTO THE FLEET'S HULL RATIO, OR THE COSTUME CHANGES SIZE.
    # The B-42 keeps its OWN canvas (222x280 and 208x271) because it is a different aeroplane, and
    # `applyLizzieSkin` swaps the rect wholesale - so its airframe drew at 0.843 of its canvas while
    # every stock hull now draws at 0.79 of a canvas sized to the art. Toggling the skin would have
    # changed the aircraft's size by ~7% on the same pilot. The PIXELS are untouched: only the
    # canvas grows, by one factor for all seventeen frames so the reel keeps its own internal
    # proportions, with the old canvas centred inside the new one so nothing shifts.
    bb = b42['']
    bal = np.asarray(bb[0])[:, :, 3] > 40
    _rows = np.nonzero(bal.any(axis=1))[0]
    bh = int(_rows.max() - _rows.min() + 1)
    K = (bh / TARGET_INK) / float(bb[4])
    for k, (im, ox, oy, cw, ch) in list(b42.items()):
        ncw, nch = int(round(cw * K)), int(round(ch * K))
        b42[k] = (im, ox + (ncw - cw) // 2, oy + (nch - ch) // 2, ncw, nch)
    print('B-42 canvas scaled x%.4f (%dx%d -> %dx%d) so it draws at the fleet hull ratio'
          % (K, bb[3], bb[4], b42[''][3], b42[''][4]))

    # ---- pack ----
    items = [('ship_%s%s' % (p, suf), v) for (p, suf), v in made.items()]
    items += [('B42%s' % k, v) for k, v in b42.items()]
    items.sort(key=lambda kv: -kv[1][0].height)
    # ⚠ 4096, NOT 2048. A 2048-wide shelf packs these 386 plates into a sheet 8,835 px TALL,
    # and 8192 is a real texture-size ceiling on plenty of hardware. Nothing in the 2D canvas path
    # would error - it would just fail to draw the ships on the machines that cap there, which is
    # the silent-on-one-device class of bug this repo can least afford (the fleet already runs on
    # two machines). 4096 gives a squarer sheet well inside the limit.
    SW = 4096
    x = y = rowh = 0
    place = {}
    for k, (im, ox, oy, cw, ch) in items:
        if x + im.width + PAD > SW:
            x = 0
            y += rowh + PAD
            rowh = 0
        place[k] = (x, y)
        x += im.width + PAD
        rowh = max(rowh, im.height)
    SH = y + rowh + PAD
    print('new sheet %dx%d for %d plates' % (SW, SH, len(items)))

    sheet = Image.new('RGBA', (SW, SH), (0, 0, 0, 0))
    rows = {}
    for k, (im, ox, oy, cw, ch) in items:
        px, py = place[k]
        sheet.paste(im, (px, py))
        rows[k] = [px, py, im.width, im.height, ox, oy, cw, ch]

    if not write:
        print('\nDRY RUN - nothing written.')
        return rows, sheet, b42

    # ---- one write: pixels, manifest rows and the B-42 table together ----
    for f, tag in ((ATLAS, '.0907u.bak'),):
        if not os.path.exists(f + tag):
            shutil.copy2(f, f + tag)
    sheet.save(ATLAS)
    print('wrote %s  (%.1f MB)' % (ATLAS, os.path.getsize(ATLAS) / 1e6))

    ships = {k: v for k, v in rows.items() if k.startswith('ship_')}
    man = open(MANIFEST, encoding='utf-8', errors='surrogateescape').read()
    old_json = re.search(r'"ships":\{.*?\},"cells"', man, re.S).group(0)
    new_json = '"ships":' + json.dumps(ships, separators=(',', ':')) + ',"cells"'
    assert old_json in man
    man = man.replace(old_json, new_json, 1)
    open(MANIFEST, 'w', encoding='utf-8', errors='surrogateescape', newline='').write(man)
    print('wrote manifest: %d ship rows (was %d)' % (len(ships), len(cur)))

    b42rows = {k[3:]: rows['B42' + k[3:]] for k in rows if k.startswith('B42')}
    # read game.js HERE, at write time - the table is only ever an OUTPUT of this script now
    src = open(GAMEJS, encoding='utf-8', errors='surrogateescape').read()
    m = re.search(r'const LIZZIE_B42_RECTS=\{(.*?)\n\};', src, re.S)
    assert m, 'LIZZIE_B42_RECTS not found in game.js'
    body = '\n'.join('  "%s":%s,' % (k, json.dumps(b42rows[k], separators=(',', ':')))
                     for k in old).rstrip(',')
    src2 = src[:m.start()] + 'const LIZZIE_B42_RECTS={\n' + body + '\n};' + src[m.end():]
    assert src2 != src, 'the B-42 table write made no change'
    open(GAMEJS, 'w', encoding='utf-8', errors='surrogateescape', newline='').write(src2)
    print('wrote game.js: LIZZIE_B42_RECTS repointed onto the new sheet')

    # ⚠ VERIFY BY PIXELS, NEVER BY COUNTS - 0906y, on the compaction that broke the B-42 in the
    # first place: "a rect moved one pixel is invisible to a count". Every carried B-42 frame is
    # compared byte for byte against the crop it came from.
    fresh = Image.open(ATLAS).convert('RGBA')
    bad = 0
    for k, (im, ox, oy, cw, ch) in b42.items():
        r = rows['B42' + k]
        got = fresh.crop((r[0], r[1], r[0] + r[2], r[1] + r[3]))
        if np.array_equal(np.asarray(got), np.asarray(im)):
            continue
        bad += 1
        print('   B-42 %-6s MISMATCH' % (k or '<base>'))
    print('B-42 verify: %d of %d frames byte-identical to the pre-compaction atlas'
          % (len(b42) - bad, len(b42)))
    oob = [k for k, r in rows.items()
           if r[0] < 0 or r[1] < 0 or r[0] + r[2] > fresh.width or r[1] + r[3] > fresh.height]
    print('rects outside the sheet: %d' % len(oob))
    off = [k for k, r in rows.items() if r[4] + r[2] > r[6] or r[5] + r[3] > r[7]]
    print('trims that overflow their own canvas: %d' % len(off))
    return rows, sheet, b42


if __name__ == '__main__':
    build('--write' in sys.argv)
