#!/usr/bin/env python3
"""import_ship_rotsheet_0906.py - drop an 8x3 rotation sheet onto a pilot's ship slots.

    python _BUILD_SOURCE/import_ship_rotsheet_0906.py lizzie yuri cole
    python _BUILD_SOURCE/import_ship_rotsheet_0906.py lizzie yuri cole --write

The generalised form of import_maverick_v2_0906.py. Mike, 0906, replaced Lizzie's, Yuri's and
Cole's airframes and asked for SpriteCook to produce "her bank, barrel roll and pseudo-3d frames",
so all three sheets were generated to Maverick's own 8x3 layout and this reads any of them:

    row 0  BARREL ROLL   -> br0..br7   (in order; #2 and #6 come back edge-on, which is where
                                        the live twist pose reads from - see drop 0903y)
    row 1  SOMERSAULT    -> so0..so7   (the reel the 0906 double-tap-up move animates through)
    row 2  BANK sweep    -> pv0..pv4   (five picked from eight - see below)

⚠ THE FIVE BANK FRAMES ARE PICKED BY MEASUREMENT, NOT BY COLUMN NUMBER. Maverick's sheet happened
to put its level frame at column 4, and assuming that held for the others is exactly the kind of
guess this codebase punishes: a first pass at scoring these sheets compared each hero plate against
"column 4" and reported Lizzie at IoU 0.275 - "drifted" - when column 4 of HER sheet is simply a
banked frame. Nothing had drifted; the comparison had. So every frame in row 2 is measured for lean
(nose-vs-body ink centroid, normalised by hull width) and the five slots are filled from that:

    pv0 = the most nose-LEFT frame      pv4 = the most nose-RIGHT frame
    pv2 = the frame nearest to level
    pv1 / pv3 = the closest symmetric inner pair either side of level

⚠ AND THE SIGNS ARE CHECKED AGAINST THE PILOT'S EXISTING CONVENTION. A pilot in SHIP_BANK_FLIP has
their art authored mirrored; one not in it does not. Filling pv0 with a nose-RIGHT frame for an
unflipped pilot would silently invert their controls, which is the defect that was retracted for
lizzie earlier today. The script reports the resulting signs so the flip table can be checked
rather than assumed.

⚠ GEOMETRY MATCHES THE PILOT'S OWN OLD CANVAS. Each pilot's existing pv/br cells share one canvas
and their ink is CENTRED in it; the new frames are scaled by ONE uniform factor solved so the new
level frame's ink height matches the old pv2's, then centred the same way. That keeps the ship the
same size on screen as the other pilots, because the hull blits at a fixed SHIP_DRAW_H.

⚠ THE ATLAS IS APPENDED TO, NEVER OVERWRITTEN. Old pixels stay exactly where they are, so a revert
is the manifest rows alone - and pixels and manifest are written in the same pass.
"""
import os, re, sys, shutil, subprocess, json
from collections import deque
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ATLAS = os.path.join(ROOT, 'assets/game/atlas/bof_player_ships_barrel_rolls.png')
MANIFEST = os.path.join(ROOT, 'assets/manifest.js')
SHEETS = {'lizzie': os.path.join(ROOT, 'docs/spritecook_0906/lizzie_rotsheet.png'),
          'yuri':   os.path.join(ROOT, 'docs/spritecook_0906/yuri_rotsheet.png'),
          # ⚠ COLE IS THE v2 SHEET. The first generation drew his craft edge-to-edge in every cell
          # (frames measured 341-344 wide in a 344px cell - touching both walls), so the grid slice
          # cut the wings off and his banked frames imported as fragments. Regenerated with explicit
          # spacing rules - "at most 65% of the cell", "a WIDE EMPTY MARGIN", "no craft may touch" -
          # which also produced the even left-to-right bank progression the first sheet lacked.
          'cole':   os.path.join(ROOT, 'docs/spritecook_0906/cole_rotsheet_v2.png')}
# ⚠ AND THAT REGENERATION DREW THIN BLACK GRID LINES between the cells, which the magenta border
# flood cannot touch and which would be trimmed INTO every frame as ink. Each cell is inset before
# slicing. The margin the new prompt bought is what makes an inset safe: there is nothing but
# background out there to throw away.
INSET = 6
COLS, ROWS = 8, 3


def is_key(p):
    r, g, b = p[0], p[1], p[2]
    return r > 150 and b > 150 and g < 95 and abs(r - b) < 80


def is_fringe(p):
    r, g, b, a = p
    return a > 0 and r > 90 and b > 90 and g < min(r, b) - 28


def cut(im, r, c):
    W, H = im.size
    cw, ch = W / COLS, H / ROWS
    cell = im.crop((int(c * cw) + INSET, int(r * ch) + INSET,
                    int((c + 1) * cw) - INSET, int((r + 1) * ch) - INSET)).convert('RGBA')
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
    # halo -> black edge, within 2px of the silhouette (the standing rule)
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
    for y in range(h):
        for x in range(w):
            p = px[x, y]
            if p[3] and dist[y][x] <= RING and is_fringe(p):
                px[x, y] = (16, 18, 16, p[3])
    bb = cell.getbbox()
    return cell.crop(bb) if bb else cell


def lean(img):
    px = img.load()
    M = [(x, y) for y in range(img.height) for x in range(img.width) if px[x, y][3] > 32]
    if len(M) < 60:
        return None
    x0 = min(p[0] for p in M); x1 = max(p[0] for p in M)
    y0 = min(p[1] for p in M); y1 = max(p[1] for p in M)
    W = max(1, x1 - x0); H = max(1, y1 - y0)
    body = sum(p[0] for p in M) / len(M)
    N = [p for p in M if p[1] <= y0 + H * 0.22]
    if len(N) < 12:
        return None
    return (sum(p[0] for p in N) / len(N) - body) / W


def old_cells(pilot):
    js = subprocess.run(['node', '-e',
        "const fs=require('fs');global.window=global;eval(fs.readFileSync('assets/manifest.js','utf8'));"
        "const S=BOFX.ships,o={};for(const k in S) if(k.indexOf('ship_%s_')===0) o[k]=S[k];"
        "process.stdout.write(JSON.stringify(o));" % pilot],
        capture_output=True, cwd=ROOT)
    return json.loads(js.stdout.decode())


def main():
    write = '--write' in sys.argv
    who = [a for a in sys.argv[1:] if not a.startswith('--')] or list(SHEETS)
    atlas = Image.open(ATLAS).convert('RGBA')
    all_rects, strip_items, sx, x, rowh = {}, [], 0, 2, 0
    PAD, MAXW = 2, atlas.width

    for pilot in who:
        src = SHEETS.get(pilot)
        if not src or not os.path.exists(src):
            print('%-8s NO SHEET at %s' % (pilot, src)); continue
        im = Image.open(src).convert('RGBA')
        old = old_cells(pilot)
        if 'ship_%s_pv2' % pilot not in old:
            print('%-8s has no existing pv2 to match against' % pilot); continue
        CW, CH = old['ship_%s_pv2' % pilot][6], old['ship_%s_pv2' % pilot][7]
        old_h = old['ship_%s_pv2' % pilot][3]

        roll = [cut(im, 0, c) for c in range(8)]
        somer = [cut(im, 1, c) for c in range(8)]
        bankf = [cut(im, 2, c) for c in range(8)]
        leans = [lean(f) for f in bankf]
        print('\n%s  sheet %dx%d  canvas %dx%d' % (pilot.upper(), im.width, im.height, CW, CH))
        print('  bank row lean: %s' % ' '.join('%+0.3f' % (v if v is not None else 0) for v in leans))

        # ⚠ THE GENERATED BANK ROWS ARE NOT MONOTONIC SWEEPS, so the five slots cannot just be
        # read off in order. Measured: lizzie +.046 +.177 -.431 +.004 +.015 +.494 +.115 +.034,
        # yuri +.303 -.184 -.138 +.046 +.020 +.010 -.234 -.328, cole mostly within +/-0.09 with
        # one +.311 outlier. Taking "the most left" and "the most right" straight off that gave
        # lizzie the SAME column for pv0 and pv1, and gave yuri a set drawn from columns 7,2,5,4,0
        # whose leans do not step evenly. A lopsided bank is worse than no bank: the ship would
        # lean harder one way than the other and the two halves of the control would not match.
        #
        # So the LEFT half is measured and the RIGHT half is MIRRORED from it. That is Mike's own
        # method - for Falva's spread he asked to "make 45 degree angle laser frames via flip/turn,
        # flip for the other side" - and it is sound here because a top-down aircraft is bilaterally
        # symmetric, so a mirrored left-bank IS the right-bank. It guarantees pv0..pv4 step evenly
        # and that the two directions are exact opposites, which the flip tables assume.
        #
        # Candidates are drawn from the WHOLE sheet, not just row 2, and edge-on/tail-on frames are
        # excluded by ink width - a 55px sliver is a roll frame, not a bank pose.
        cand = []
        for src_row, lst in (('bank', bankf), ('roll', roll)):
            for i, f in enumerate(lst):
                v = lean(f)
                if v is None:
                    continue
                cand.append((v, f, '%s%d' % (src_row, i), f.width))
        wmax = max(c[3] for c in cand)
        cand = [c for c in cand if c[3] >= wmax * 0.60]        # drop edge-on and tail-on poses
        # ⚠ AND WHICH SIDE IS THE GOOD ONE VARIES BY SHEET. The first cut always measured the LEFT
        # and mirrored to the right, which collapsed Cole: his sheet leans RIGHT (+0.329, +0.313,
        # +0.311) and has nothing stronger than -0.090 to the left, so pv0 and pv1 came back as the
        # SAME frame and his bank had no progression at all. Take the strongest pose of EITHER sign
        # and mirror to the opposite side; the symmetry is then guaranteed whichever way the
        # generator happened to lean.
        # ⚠ THE LEVEL FRAME IS THE WIDEST NEAR-ZERO-LEAN POSE, NOT SIMPLY THE FLATTEST NUMBER. A
        # ship rolled fully over also measures ~0 lean, and Lizzie's first import picked exactly
        # that - her idle hull came out as a narrow inverted sliver instead of the wide gold delta.
        # A true top-down delta is the WIDEST pose the craft has, so among everything within 0.06 of
        # level, take the widest; and prefer the bank row, which is the one authored top-down.
        flat = [c for c in cand if abs(c[0]) < 0.06] or cand
        bankflat = [c for c in flat if c[2].startswith('bank')]
        lvlf = max(bankflat or flat, key=lambda c: c[3])
        strong = max(cand, key=lambda c: abs(c[0]))
        side = 1 if strong[0] > 0 else -1
        same = [c for c in cand if (c[0] * side) > 0.04]
        mild = min(same, key=lambda c: abs(abs(c[0]) - abs(strong[0]) * 0.45)) if same else strong
        mir = lambda im: im.transpose(Image.FLIP_LEFT_RIGHT)
        frames = {}
        for i in range(8):
            frames['br%d' % i] = roll[i]
            frames['so%d' % i] = somer[i]
        frames['pv2'] = lvlf[1]
        if side > 0:                      # the sheet's strong poses are nose-RIGHT
            frames['pv4'] = strong[1]; frames['pv3'] = mild[1]
            frames['pv0'] = mir(strong[1]); frames['pv1'] = mir(mild[1])
        else:                             # nose-LEFT
            frames['pv0'] = strong[1]; frames['pv1'] = mild[1]
            frames['pv4'] = mir(strong[1]); frames['pv3'] = mir(mild[1])
        print('  bank built from %s (%+0.3f) / %s (%+0.3f) / level %s (%+0.3f); the %s side is MIRRORED'
              % (strong[2], strong[0], mild[2], mild[0], lvlf[2], lvlf[0],
                 'left' if side > 0 else 'right'))
        print('  -> pv0..pv4 leans %s'
              % ' '.join('%+0.3f' % (lean(frames['pv%d' % i]) or 0) for i in range(5)))

        s = old_h / max(1, frames['pv2'].height)
        print('  uniform scale %.4f (new level ink %dx%d -> matches old pv2 h=%d)'
              % (s, frames['pv2'].width, frames['pv2'].height, old_h))
        for slot, img in frames.items():
            nw, nh = max(1, round(img.width * s)), max(1, round(img.height * s))
            sm = img.resize((nw, nh), Image.LANCZOS)
            canvas = Image.new('RGBA', (CW, CH), (0, 0, 0, 0))
            canvas.alpha_composite(sm, ((CW - nw) // 2, (CH - nh) // 2))
            bb = canvas.getbbox()
            sub = canvas.crop(bb)
            if x + sub.width + PAD > MAXW:
                x = PAD; sx += rowh + PAD; rowh = 0
            strip_items.append((pilot, slot, x, sx, sub, bb, CW, CH))
            x += sub.width + PAD
            rowh = max(rowh, sub.height)

    if not strip_items:
        print('\nnothing to do'); return 1
    strip_h = sx + rowh + PAD
    y0 = atlas.height
    out = Image.new('RGBA', (atlas.width, atlas.height + strip_h), (0, 0, 0, 0))
    out.alpha_composite(atlas, (0, 0))
    for pilot, slot, px_, py_, sub, bb, CW, CH in strip_items:
        out.alpha_composite(sub, (px_, y0 + py_))
        all_rects['ship_%s_%s' % (pilot, slot)] = [px_, y0 + py_, sub.width, sub.height,
                                                   bb[0], bb[1], CW, CH]
    print('\natlas %dx%d -> %dx%d  (+%d rows, %d frames)'
          % (atlas.width, atlas.height, out.width, out.height, strip_h, len(strip_items)))

    if not write:
        print('DRY RUN - nothing written. Re-run with --write.')
        return 0
    for f in (ATLAS, MANIFEST):
        if not os.path.exists(f + '.bak-0906ships'):
            shutil.copy(f, f + '.bak-0906ships')
    out.save(ATLAS)
    src = open(MANIFEST, 'rb').read()
    n = 0
    for key, r in all_rects.items():
        new = ('"%s":[%s]' % (key, ','.join(str(v) for v in r))).encode()
        hit = 0
        for q in (b'"', b"'"):
            pat = re.compile(re.escape(q + key.encode() + q) + rb'\s*:\s*\[[^\]]*\]')
            src, k = pat.subn(new, src)
            hit += k
        if not hit:
            pilot = key.split('_')[1]
            anchor = re.search(('"ship_%s_pv2"' % pilot).encode() + rb'\s*:\s*\[[^\]]*\]', src) or \
                     re.search(("'ship_%s_pv2'" % pilot).encode() + rb'\s*:\s*\[[^\]]*\]', src)
            if not anchor:
                raise SystemExit('no anchor for %s' % key)
            src = src[:anchor.end()] + b',' + new + src[anchor.end():]
            hit = 1
        n += hit
    open(MANIFEST, 'wb').write(src)
    print('manifest: %d rows written' % n)
    r = subprocess.run(['node', '--check', MANIFEST], capture_output=True, cwd=ROOT)
    print('node --check manifest: %s' % ('OK' if r.returncode == 0 else r.stderr.decode()[:200]))
    return 0


if __name__ == '__main__':
    sys.exit(main())
