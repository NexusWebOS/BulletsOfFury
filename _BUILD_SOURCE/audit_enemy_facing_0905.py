#!/usr/bin/env python3
"""audit_enemy_facing_0905.py - is every enemy sprite facing vertically SOUTH, at the player?

Mike, 0905: "make sure all enemy sprites are facing vertically south to the player."

This is not a taste question, it is measurable, and he has already cut hulls over it by name -
the gate carrier ("the ONE hull my own silhouette audit flagged as genuinely turned, principal
axis 145.7 degrees", 0904r) and the chronal crawler ("its a 45 degree titled tank"). So rather
than eyeball 200 sprites, three numbers per plate:

  MIRROR-LR   reflect the alpha mask left-to-right about its own ink centre, take IoU.
              A top-down craft pointing straight up or straight down is bilaterally symmetric,
              so this is high. A hull drawn turned, banked or in 3/4 view is not.
  MIRROR-UD   the same flip top-to-bottom. If BOTH are high the sprite is radially symmetric -
              a mine, a ring, a turret, an orb - and "facing" does not apply to it at all.
              Reporting those as failures is how an audit like this becomes noise nobody reads.
  MASS-Y      where the ink actually sits, as a fraction of hull height: 0 = all at the top,
              1 = all at the bottom. A craft facing SOUTH carries its bulk high - wings, engines,
              shoulders - and tapers to a nose at the BOTTOM, so this sits BELOW 0.5. Facing
              NORTH is the same hull upside down and pushes it above 0.5. This is the only one of
              the three that separates "vertical but correct" from "vertical but backwards".

              ⚠ MEASURE INK, NOT SPAN. The first version of this took each row's leftmost-to-
              rightmost distance, and a hull with two spread tail fins has an enormous SPAN across
              a row holding almost no pixels - so 97 of 132 hulls came back "possibly upside
              down", including several Mike had just approved. Span describes the bounding box;
              mass describes the ship.

⚠ THE ROSTER IS ENUMERATED FROM THE GAME, NOT FROM THE DIRECTORY TREE. ENEMY_ART is assembled at
runtime - the stage-9 loop at game.js 34490 builds it by walking BOFX.img, and other families are
added by hand - so a `find` over assets/game would both miss registered art and sweep up hundreds
of backgrounds, icons and FX frames that are not enemies. The browser is asked what it actually
believes the enemy roster is, and each key is resolved to its real source: a BOFX.cells rect on an
atlas, or an X._src file path.

⚠ AND IT REPORTS, IT DOES NOT ROTATE. Auto-rotating a plate to satisfy a metric would bake a
resample into approved pixel art and silently change every silhouette the collision reads. The
output is a ranked list plus a contact sheet, for Mike.
"""
import sys, os, json, math, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shoot as sh
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont

ROOT = sh.GAME

DUMP = r"""
() => {
  const out = {};
  if (typeof ENEMY_ART === 'undefined') return {err:'no ENEMY_ART'};
  const bases = new Set();
  for (const k in ENEMY_ART) { const v = ENEMY_ART[k]; if (v) bases.add(v); }
  for (const base of bases) {
    // prefer the idle plate; fall back to frame 0, then the bare key
    let key = null;
    for (const cand of [base + '_idle', base + '_0', base]) {
      if ((window.BOFX && BOFX.cells && BOFX.cells[cand]) || (XART._src && XART._src[cand])) { key = cand; break; }
    }
    if (!key) continue;
    const cell = (window.BOFX && BOFX.cells) ? BOFX.cells[key] : null;
    const src = XART._src ? XART._src[key] : null;
    const sheet = cell ? ((window.BOFX && BOFX.img) ? BOFX.img[cell[0]] : null) : null;
    out[base] = {key: key,
                 cell: cell || null,
                 sheet: sheet || (cell ? ('assets/game/atlas/' + cell[0] + '.png') : null),
                 src: src || null};
  }
  return out;
}
"""


def mask_of(im):
    px = im.load()
    return {(x, y) for y in range(im.height) for x in range(im.width) if px[x, y][3] > 0}


def metrics(im):
    b = im.getbbox()
    if not b:
        return None
    im = im.crop(b)
    M = mask_of(im)
    if len(M) < 40:
        return None
    w, h = im.width, im.height
    lr = {(w - 1 - x, y) for (x, y) in M}
    ud = {(x, h - 1 - y) for (x, y) in M}
    iou = lambda A, B: len(A & B) / max(1, len(A | B))
    # width profile
    rows = {}
    for (x, y) in M:
        r = rows.setdefault(y, [w, 0])
        r[0] = min(r[0], x)
        r[1] = max(r[1], x)
    ink = {}
    for (x, y) in M:
        ink[y] = ink.get(y, 0) + 1
    def band(lo, hi):
        return sum(v for y, v in ink.items() if lo <= y < hi)
    top, bot = band(0, int(h * 0.35)), band(int(h * 0.65), h)
    massy = (cy0 := (sum(p[1] for p in M) / len(M))) / max(1, h - 1)
    # principal axis of the mask, measured off the vertical
    cx = sum(p[0] for p in M) / len(M)
    cy = sum(p[1] for p in M) / len(M)
    sxx = syy = sxy = 0.0
    for (x, y) in M:
        dx, dy = x - cx, y - cy
        sxx += dx * dx; syy += dy * dy; sxy += dx * dy
    n = len(M)
    sxx /= n; syy /= n; sxy /= n
    ang = 0.5 * math.atan2(2 * sxy, sxx - syy)          # long axis, radians from +x
    deg = (math.degrees(ang)) % 180
    off_vert = min(abs(deg - 90), 180 - abs(deg - 90))   # 0 = perfectly vertical long axis
    return {'lr': iou(M, lr), 'ud': iou(M, ud), 'top': top, 'bot': bot, 'massy': massy,
            'taper': (bot / top) if top else 1.0, 'axis_off_vert': off_vert,
            'w': w, 'h': h, 'n': len(M)}


def load(rec):
    if rec.get('cell'):
        name, x, y, w, h = rec['cell']
        p = os.path.join(ROOT, rec['sheet'] or ('assets/game/atlas/%s.png' % name))
        if not os.path.exists(p):
            return None
        return Image.open(p).convert('RGBA').crop((x, y, x + w, y + h))
    if rec.get('src'):
        p = os.path.join(ROOT, rec['src'])
        if not os.path.exists(p):
            return None
        return Image.open(p).convert('RGBA')
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default='docs/S9_FACING_AUDIT_0905.png')
    ap.add_argument('--stage9only', action='store_true')
    a = ap.parse_args()

    port, stop = sh.serve(ROOT)
    try:
        with sync_playwright() as pw:
            b = pw.chromium.launch()
            pg = b.new_page(viewport={'width': 480, 'height': 512})
            pg.goto('http://127.0.0.1:%d/index.html' % port)
            pg.wait_for_function('typeof ASSETS!=="undefined" && typeof loop==="function"', timeout=30000)
            pg.wait_for_timeout(2500)
            pg.evaluate(sh.SETUP, {'state': 'PLAY', 'stage': 9, 'pilot': 'cole'})
            roster = pg.evaluate(DUMP)
            b.close()
    finally:
        stop()
    if roster.get('err'):
        raise SystemExit(roster['err'])
    print('ENEMY_ART advertises %d distinct art families\n' % len(roster))

    rows = []
    missing = 0
    for base, rec in sorted(roster.items()):
        if a.stage9only and not (base.startswith('ns9') or base.startswith('s9')):
            continue
        im = load(rec)
        if im is None:
            missing += 1
            continue
        m = metrics(im)
        if not m:
            continue
        m['base'] = base
        m['rec'] = rec
        m['im'] = im
        rows.append(m)
    print('measured %d plates (%d could not be resolved to a file)\n' % (len(rows), missing))

    RADIAL = 0.82        # both mirrors this high -> orientation does not apply
    TURNED = 0.72        # LR mirror below this -> the hull is drawn turned
    radial = [r for r in rows if r['lr'] >= RADIAL and r['ud'] >= RADIAL]
    rest = [r for r in rows if r not in radial]
    turned = sorted([r for r in rest if r['lr'] < TURNED], key=lambda r: r['lr'])
    # mass sitting materially BELOW the middle means the bulk is at the bottom: nose up = NORTH
    northish = sorted([r for r in rest if r['lr'] >= TURNED and r['massy'] > 0.545],
                      key=lambda r: -r['massy'])
    ok = [r for r in rest if r not in turned and r not in northish]

    print('  %-4d radially symmetric (mines, rings, turrets, orbs) - facing not applicable' % len(radial))
    print('  %-4d face vertically with their mass HIGH (nose low)   = SOUTH, correct' % len(ok))
    print('  %-4d vertical but mass sits LOW (nose high)             = may be facing NORTH' % len(northish))
    print('  %-4d drawn TURNED (low left-right mirror symmetry)' % len(turned))

    if turned:
        print('\n--- TURNED HULLS, worst first --------------------------------------------------')
        print('  %-26s %-7s %-7s %-9s %s' % ('family', 'mirrorLR', 'axis', 'taper', 'source'))
        for r in turned[:24]:
            src = r['rec'].get('src') or ('%s cell' % (r['rec']['cell'][0] if r['rec'].get('cell') else '?'))
            print('  %-26s %6.2f  %5.1f deg %7.2f  %s' % (r['base'][:26], r['lr'], r['axis_off_vert'],
                                                          r['taper'], str(src)[:44]))
    if northish:
        print('\n--- VERTICAL BUT POSSIBLY UPSIDE DOWN (wide at the bottom) ---------------------')
        print('  %-28s %-9s %-8s %s' % ('family', 'mirrorLR', 'mass-Y', 'source'))
        for r in northish[:30]:
            src = r['rec'].get('src') or ('%s cell' % (r['rec']['cell'][0] if r['rec'].get('cell') else '?'))
            print('  %-28s %6.2f    %6.3f   %s' % (r['base'][:28], r['lr'], r['massy'], str(src)[:40]))

    # contact sheet of everything that is not clean
    bad = turned[:12] + northish[:8]
    if bad:
        try:
            F = ImageFont.truetype('C:/Windows/Fonts/consolab.ttf', 11)
        except Exception:
            F = ImageFont.load_default()
        H, cols = 118, 5
        tiles = []
        for r in bad:
            im = r['im'].crop(r['im'].getbbox())
            s = min(H / im.height, H / im.width)
            tiles.append((r, im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.NEAREST)))
        cw = H + 74
        rws = (len(tiles) + cols - 1) // cols
        out = Image.new('RGBA', (cw * cols, rws * (H + 40) + 30), (8, 6, 18, 255))
        d = ImageDraw.Draw(out)
        d.text((8, 8), 'ENEMY FACING AUDIT - hulls that are not cleanly south-facing', font=F, fill=(255, 190, 74))
        for i, (r, t) in enumerate(tiles):
            cx, cy = (i % cols) * cw, (i // cols) * (H + 40) + 26
            out.alpha_composite(t, (cx + (cw - t.width) // 2, cy + (H - t.height) // 2))
            tag = 'TURNED' if r in turned else 'mass-Y %.2f' % r['massy']
            d.text((cx + 4, cy + H + 4), r['base'][:22], font=F, fill=(225, 238, 255))
            d.text((cx + 4, cy + H + 19), '%s  LR %.2f' % (tag, r['lr']), font=F, fill=(255, 140, 140))
        out.save(os.path.join(ROOT, a.out))
        print('\nwrote %s' % a.out)
    return 0


if __name__ == '__main__':
    sys.exit(main())
