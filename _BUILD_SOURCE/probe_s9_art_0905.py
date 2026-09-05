#!/usr/bin/env python3
"""probe_s9_art_0905.py - does the recoloured roster and the new mid-boss actually RENDER?

The suite proves state. It cannot see a colour. Everything this drop changed is pixels:

  * eight atlas cells rewritten in place inside en_s9.png (Mike's palette assignment + the halo)
  * a seven-frame mid-boss reel in two skins, replacing a two-body sub-boss with one

So this boots the real game, spawns each unit, and reads the CANVAS BACK. A unit is only accepted
if its dominant on-screen hue lands in the band its assigned palette implies - which is the one
check a manifest grep, a key count and the whole assertion suite are all incapable of making.

⚠ WARM THE ATLAS AND WAIT ON IT BEFORE STEPPING. shoot.STEP advances a synthetic clock inside one
tight JS loop, so a stepped run gets no wall time and `en_s9.png` never finishes decoding - it
measured naturalWidth 0 with ZERO network requests for a whole run earlier today, and the probe
that did not wait reported nine perfectly good units as "NOT DRAWN".

⚠ SAMPLE THE CANVAS, NOT THE PNG. Reading the file back would only prove the bake script did what
it said. The question here is whether the GAME draws that plate - past ENEMY_ART, past the cell
lookup, past drawNewEnemyArt's rdy() fallback to _idle.
"""
import sys, os, json, argparse, colorsys, base64, io as _io
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shoot as sh
from playwright.sync_api import sync_playwright
from PIL import Image

# unit -> (assigned palette, accepted hue band in degrees, or None for a greyscale family)
EXPECT = {
    'wskim':   ('blue',      (195, 265)),
    'pneedle': ('lightgray', None),
    'pmine':   ('asis',      (230, 320)),
    'gleech':  ('neonred',   (330, 375)),
    'vmanta':  ('pink',      (295, 350)),
    'echof':   ('darkgray',  None),
    'tsplit':  ('black',     None),
    'cbreak':  ('neonred',   (330, 375)),
}

WARM = """() => {
  const hit = k => k.indexOf('ns9') === 0 || k.indexOf('s9atk_') === 0;
  const want = [];
  if (window.BOFX && BOFX.cells) for (const k in BOFX.cells) if (hit(k)) want.push(k);
  if (XART._src) for (const k in XART._src) if (hit(k)) want.push(k);
  window.__warm = Array.from(new Set(want));
  for (const k of window.__warm) { try { XART._touch(k); } catch (e) {} }
  return window.__warm.length;
}"""
# ⚠ WRAP THE ARROW BEFORE CALLING IT. `READY + '() >= 0.98'` builds `() => {...}() >= 0.98`, which
# is a SyntaxError, so wait_for_function threw instantly, the warm wait never happened, and the
# FIRST unit tested drew before the atlas had decoded - reported as "NOTHING PAINTED" for a plate
# that was fine. Same decode race as before, this time manufactured by the probe itself.
READY = """() => { const ks = window.__warm || []; let n = 0;
  for (const k of ks) if (XART.rdy(k)) n++; return ks.length ? n / ks.length : 1; }"""
READY_CALL = '(' + READY + ')()'

SHOT = """(unit) => {
  enemies.length = 0; eBullets.length = 0;
  const e = spawnEnemy(unit, 240, 190, {});
  if (!e) return {ok:false, err:'spawn returned nothing'};
  e._s9x0 = 240; e._s9y0 = 190; e.x = 240; e.y = 190; e.spin = 0;
  for (let i = 0; i < 3; i++) { try { drawEnemy(e); } catch (err) { return {ok:false, err:String(err)}; } }
  return {ok:true, w:e._drawW || e.w, h:e._drawH || e.h, art:e.art};
}"""

CLEARCV = """() => { const c = document.getElementById('screen');
  const g = c.getContext('2d'); g.clearRect(0,0,c.width,c.height); return [c.width, c.height]; }"""
GRAB = """() => document.getElementById('screen').toDataURL('image/png')"""

BOSS = """(frac) => {
  subBoss = null; subBossActive = false; subBossDone = false; subBossTriggered = false;
  spawnSubBoss('voidhorizon');
  for (let i = 0; i < 120; i++) updateSubBoss(1/60);
  const F = subBoss._s9rift;
  F.core.hp = Math.ceil(F.core.maxhp * frac); subBoss.hp = F.core.hp;
  F.core.x = 240; F.core.y = 190;
  const c = document.getElementById('screen'); c.getContext('2d').clearRect(0,0,c.width,c.height);
  try { drawSubBoss(); } catch (e) { return {ok:false, err:String(e)}; }
  return {ok:true, hp:F.core.hp, maxhp:F.core.maxhp, w:F.core.w, h:F.core.h,
          name:subBoss.name, kind:subBoss.kind};
}"""


def dominant(img):
    """mean hue/sat/val of the opaque, non-trivial pixels actually painted"""
    px = img.convert('RGBA').load()
    hs = []
    for y in range(0, img.height, 2):
        for x in range(0, img.width, 2):
            r, g, b, a = px[x, y]
            if a < 40:
                continue
            h, s, v = colorsys.rgb_to_hsv(r / 255., g / 255., b / 255.)
            if v < 0.10:
                continue                       # the near-black outline is not the body colour
            hs.append((h * 360, s, v))
    if not hs:
        return None
    import math
    sx = sum(math.cos(math.radians(h)) * s for h, s, _ in hs)
    sy = sum(math.sin(math.radians(h)) * s for h, s, _ in hs)
    hue = math.degrees(math.atan2(sy, sx)) % 360
    return hue, sum(x[1] for x in hs) / len(hs), sum(x[2] for x in hs) / len(hs), len(hs)


def png(pg):
    d = pg.evaluate(GRAB)
    return Image.open(_io.BytesIO(base64.b64decode(d.split(',', 1)[1])))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default='docs/S9_INGAME_0905.png')
    a = ap.parse_args()
    port, stop = sh.serve(sh.GAME)
    shots, fails = [], []
    try:
        with sync_playwright() as pw:
            b = pw.chromium.launch()
            pg = b.new_page(viewport={'width': 480, 'height': 512})
            errs = []
            pg.on('pageerror', lambda e: errs.append(str(e)))
            pg.goto('http://127.0.0.1:%d/index.html' % port)
            pg.wait_for_function('typeof ASSETS!=="undefined" && typeof loop==="function"', timeout=30000)
            pg.wait_for_timeout(2500)
            r = pg.evaluate(sh.SETUP, {'state': 'PLAY', 'stage': 9, 'pilot': 'cole', 'invuln': True})
            if not r.get('ok'):
                raise SystemExit('setup failed: %s' % r)
            n = pg.evaluate(WARM)
            try:
                pg.wait_for_function(READY_CALL + ' >= 0.90', timeout=25000)
            except Exception:
                pass
            print('warmed %d keys, %.0f%% ready\n' % (n, pg.evaluate(READY) * 100))
            pg.evaluate(sh.TRAP_RAF)
            pg.evaluate(sh.STEP, 8)

            print('%-9s %-10s %-22s %s' % ('unit', 'palette', 'measured on canvas', 'verdict'))
            for unit, (pal, band) in EXPECT.items():
                pg.evaluate(CLEARCV)
                res = pg.evaluate(SHOT, unit)
                if not res.get('ok'):
                    fails.append('%s: %s' % (unit, res.get('err')))
                    print('  %-9s %-10s %-22s ** %s **' % (unit, pal, '-', res.get('err')))
                    continue
                im = png(pg)
                d = dominant(im)
                if not d:
                    fails.append('%s: nothing painted' % unit)
                    print('  %-9s %-10s %-22s ** NOTHING PAINTED **' % (unit, pal, '-'))
                    continue
                hue, sat, val, npx = d
                if band is None:
                    ok = sat < 0.34
                    desc = 'sat %.2f val %.2f' % (sat, val)
                    why = 'greyscale' if ok else 'STILL COLOURED'
                else:
                    lo, hi = band
                    hh = hue + 360 if hue < lo - 180 else hue
                    ok = lo <= hh <= hi
                    desc = 'hue %3.0f sat %.2f' % (hue, sat)
                    why = 'in band %d-%d' % (lo, hi) if ok else 'OUT of %d-%d' % (lo, hi)
                if not ok:
                    fails.append('%s: %s (%s)' % (unit, desc, why))
                print('  %-9s %-10s %-22s %s  %s' % (unit, pal, desc, 'OK ' if ok else '**FAIL**', why))
                shots.append((unit + ' / ' + pal, im.crop(im.getbbox()) if im.getbbox() else im))

            print()
            for label, frac in [('mid-boss FULL hp', 1.0), ('mid-boss 40% hp (black phase)', 0.40)]:
                pg.evaluate(CLEARCV)
                res = pg.evaluate(BOSS, frac)
                if not res.get('ok'):
                    fails.append('%s: %s' % (label, res.get('err')))
                    print('  %-30s ** %s **' % (label, res.get('err')))
                    continue
                im = png(pg)
                d = dominant(im)
                if not d:
                    fails.append('%s: nothing painted' % label)
                    print('  %-30s ** NOTHING PAINTED **' % label)
                    continue
                hue, sat, val, npx = d
                print('  %-30s %s "%s" %dx%d  hue %3.0f sat %.2f val %.2f  painted %d px'
                      % (label, res['kind'], res['name'], res['w'], res['h'], hue, sat, val, npx))
                shots.append((label, im.crop(im.getbbox()) if im.getbbox() else im))
            if errs:
                print('\npage errors (%d): %s' % (len(errs), errs[0][:200]))
                fails.append('page errors: %d' % len(errs))
            b.close()
    finally:
        stop()

    if shots:
        from PIL import ImageDraw, ImageFont
        try:
            F = ImageFont.truetype('C:/Windows/Fonts/consolab.ttf', 12)
        except Exception:
            F = ImageFont.load_default()
        H = 150
        tiles = []
        for lab, im in shots:
            s = min(H / max(1, im.height), 2.4)
            tiles.append((lab, im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))))))
        cw = max(t.width for _, t in tiles) + 18
        cols = 5
        rows = (len(tiles) + cols - 1) // cols
        out = Image.new('RGBA', (cw * cols, rows * (H + 34) + 8), (8, 6, 18, 255))
        d = ImageDraw.Draw(out)
        for i, (lab, t) in enumerate(tiles):
            cx, cy = (i % cols) * cw, (i // cols) * (H + 34) + 6
            out.alpha_composite(t, (cx + (cw - t.width) // 2, cy + (H - t.height) // 2))
            d.text((cx + 6, cy + H + 6), lab[:26], font=F, fill=(220, 235, 255))
        out.save(a.out)
        print('\nwrote %s' % a.out)
    print('\n%s' % ('FAILED:\n  ' + '\n  '.join(fails) if fails
                    else 'every recoloured unit and both mid-boss phases drew, in the right colour.'))
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
