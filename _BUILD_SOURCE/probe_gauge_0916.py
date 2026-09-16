#!/usr/bin/env python3
"""probe_gauge_0916.py - the boss gauges: a centred label, the shield's own bar, our own fills.

Mike, 0916: "text in boss bars and min boss bars shold centered all around including vertically.
Shield should get it's own shield like boss bar, not the same as the boss bar. our own custom
solid/shield fills too. and Shield should be colored Blue as text."

Driven on the Stage-2 Furnace Tyrant, which carries a real barrier, so the HP bar and the SHIELD
bar are both on screen in a live fight.

⚠ THE PLATES CANNOT BE TOLD APART BY SIZE. bmbar_frame_boss and bmbar_frame_shield are both
700x33; all three tabs are 204x30; every fill is 578x13. CLAUDE.md's rule applies at full force -
identify a blit by the KEY it was asked for. XART.get is wrapped to record keys, and the game
context's own drawImage (never the prototype) to record where each blit landed.

⚠ AND THE CENTRING IS MEASURED IN PIXELS, NOT ASSERTED FROM THE SOURCE. The tab's drawn rect comes
from the live CTM; the socket inside it is BMTAB.in; the label's ink bounding box is read back out
of the canvas with getImageData and its centre compared to the socket's. A source assertion that
the code passes a centre would pass on a build where the text was drawn somewhere else entirely.
"""
import os, sys, base64
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shoot

OUT = 'docs/proofs/bossbar_0916'

TRAP = r"""() => {
  if (window.__gtrap) return true;
  window.__gtrap = 1;
  window.__keys = []; window.__blits = []; window.__rec = 0;
  const og = XART.get;
  XART.get = function (k) { try { if (window.__rec) window.__keys.push(k); } catch (e) {} return og.apply(this, arguments); };
  const c = ctx, od = c.drawImage;
  c.drawImage = function (im) {
    try {
      if (window.__rec && im) {
        const a = arguments, W = im.width || im.naturalWidth, H = im.height || im.naturalHeight;
        let dx = 0, dy = 0, dw = W, dh = H;
        if (a.length >= 9) { dx = a[5]; dy = a[6]; dw = a[7]; dh = a[8]; }
        else if (a.length >= 5) { dx = a[1]; dy = a[2]; dw = a[3]; dh = a[4]; }
        else if (a.length >= 3) { dx = a[1]; dy = a[2]; }
        const m = c.getTransform();
        window.__blits.push({W: W, H: H, x: m.a * dx + m.e, y: m.d * dy + m.f, w: dw * m.a, h: dh * m.d});
      }
    } catch (e) {}
    return od.apply(this, arguments);
  };
  return true;
}"""

FRAME = r"""async () => {
  window.__keys = []; window.__blits = []; window.__rec = 1;
  await new Promise(r => requestAnimationFrame(r));
  window.__rec = 0;
  const tabs = window.__blits.filter(b => b.W === 204 && b.H === 30);
  /* the label ink, read back out of the canvas inside each tab's own socket */
  const I = BMTAB.in, out = [];
  for (const t of tabs) {
    const s = t.w / BMTAB.w;
    const sx = Math.round(t.x + I.dx * s), sy = Math.round(t.y + I.dy * s);
    const sw = Math.max(2, Math.round(I.w * s)), sh = Math.max(2, Math.round(I.h * s));
    let d = null;
    try { d = ctx.getImageData(sx, sy, sw, sh); } catch (e) { }
    if (!d) { out.push({err: 'no pixels'}); continue; }
    let x0 = 1e9, y0 = 1e9, x1 = -1, y1 = -1, n = 0, sr = 0, sg = 0, sb = 0;
    for (let y = 0; y < sh; y++) for (let x = 0; x < sw; x++) {
      const i = (y * sw + x) * 4, r = d.data[i], g = d.data[i + 1], b = d.data[i + 2];
      const lum = (r * 299 + g * 587 + b * 114) / 1000;
      if (lum > 95) { n++; sr += r; sg += g; sb += b; if (x < x0) x0 = x; if (x > x1) x1 = x; if (y < y0) y0 = y; if (y > y1) y1 = y; }
    }
    out.push(n ? {n: n, sw: sw, sh: sh,
                  cx: ((x0 + x1) / 2) - (sw - 1) / 2,        // ink centre relative to the socket centre
                  cy: ((y0 + y1) / 2) - (sh - 1) / 2,
                  ih: (y1 - y0 + 1), iw: (x1 - x0 + 1),
                  r: sr / n, g: sg / n, b: sb / n} : {n: 0, sw: sw, sh: sh});
  }
  return {keys: window.__keys.slice(), tabs: tabs.length, labels: out,
          frames: window.__blits.filter(b => b.W === 700 && b.H === 33).length,
          fills: window.__blits.filter(b => b.W === 578 && b.H === 13).length};
}"""

START = r"""async ([stage, pilot]) => {
  const B = window.BOSSMODE;
  B.start(stage, 'boss', pilot, false);
  for (let i = 0; i < 1500 && !(B.snapshot().bossActive && B.player && !B.player.dead); i++)
    await new Promise(r => requestAnimationFrame(r));
  if (B.player) B.player.invuln = 1e9;
  playerHit = function () {};
  const b = B.boss || boss;
  return {boss: !!b, shield: (typeof bossShieldFrac === 'function') ? bossShieldFrac(b) : null};
}"""


def main():
    os.makedirs(OUT, exist_ok=True)
    from playwright.sync_api import sync_playwright
    port, stop = shoot.serve(shoot.GAME)
    errs, fails, n_ok = [], [], [0]

    def ok(c, m):
        if c:
            n_ok[0] += 1; print('  ok  ', m)
        else:
            fails.append(m); print('  FAIL', m)

    with sync_playwright() as p:
        b = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
        pg = b.new_page(viewport={'width': 1100, 'height': 1000}, device_scale_factor=1)
        pg.on('pageerror', lambda e: errs.append('pageerror: ' + str(e)[:200]))
        pg.on('console', lambda m: errs.append('console: ' + m.text[:200]) if m.type == 'error' else None)
        pg.goto('http://127.0.0.1:%d/index.html?bossmode=1' % port, wait_until='load', timeout=60000)
        pg.wait_for_function("() => window.BOSSMODE && window.BOSSMODE.ready", timeout=90000)

        S = pg.evaluate(START, [2, 'cole'])
        ok(S.get('boss'), 'the Stage-2 boss is up')
        ok(S.get('shield') is not None, 'and it carries a shield, so both bars are on screen (%s)' % S.get('shield'))

        # every new plate, warmed then waited for - rdy is false on its first call
        KEYS = ['bmbar_frame_shield', 'bmbar_tab_shield', 'bmbar_fill_solid',
                'bmbar_sf2_over', 'bmbar_sf2_hex', 'bmbar_sf2_plasma', 'bmbar_sf2_low']
        for _ in range(50):
            pg.evaluate("(ks) => ks.forEach(k => XART.rdy(k))", KEYS)
            if pg.evaluate("(ks) => ks.every(k => XART.rdy(k))", KEYS):
                break
            pg.wait_for_timeout(80)
        ok(pg.evaluate("(ks) => ks.every(k => XART.rdy(k))", KEYS), 'every new gauge plate decoded')

        pg.evaluate(TRAP)
        F = pg.evaluate(FRAME)

        ok('bmbar_frame_shield' in F['keys'], 'the SHIELD bar draws its own frame, not the boss frame')
        ok('bmbar_tab_shield' in F['keys'], 'and its own tab')
        ok('bmbar_frame_boss' in F['keys'], 'while the HP bar still draws the boss frame (both are on screen)')
        ok('bmbar_fill_solid' in F['keys'] or any(k == 'bmbar_fill_solid' for k in F['keys']),
           'the HP bar uses our own SOLID fill (%s)' % [k for k in F['keys'] if k.startswith('bmbar_fill')])
        ok(any(k.startswith('bmbar_sf2_') for k in F['keys']),
           'the shield uses our own shield fill (%s)' % [k for k in F['keys'] if k.startswith('bmbar_sf')])
        ok('bmbar_fill_seg' not in F['keys'], 'and the hazard-stripe plate is no longer the boss fill')

        # ---- the centring, measured off the canvas ----
        labs = [l for l in F['labels'] if l.get('n')]
        ok(len(labs) >= 2, 'both tabs carry lettering (%d of %d tabs)' % (len(labs), F['tabs']))
        for i, l in enumerate(labs):
            ok(abs(l['cy']) <= 1.5, 'label %d is vertically centred in its socket (%.2f px off centre, socket %dpx)' % (i, l['cy'], l['sh']))
            ok(abs(l['cx']) <= 2.5, 'label %d is horizontally centred (%.2f px off centre)' % (i, l['cx']))
            ok(l['ih'] < l['sh'], 'label %d fits inside the socket (%dpx ink in %dpx)' % (i, l['ih'], l['sh']))

        # ---- SHIELD is blue, BOSS is not ----
        blue = [l for l in labs if l['b'] > l['r'] * 1.25]
        gold = [l for l in labs if l['r'] > l['b'] * 1.25]
        ok(len(blue) >= 1, 'the SHIELD label is blue (%s)' % [(round(l['r']), round(l['g']), round(l['b'])) for l in labs])
        ok(len(gold) >= 1, 'and the BOSS label is not')

        d = pg.evaluate("() => { const c=document.getElementById('screen'); return c?c.toDataURL('image/png'):null; }")
        if d:
            open(os.path.join(OUT, '03_gauges_live.png'), 'wb').write(base64.b64decode(d.split(',', 1)[1]))

        # ---- the MINI BOSS bar: he named those too, and its label is the long one ----

        M = pg.evaluate("""async ([stage, pilot]) => {
          const B = window.BOSSMODE;
          B.start(stage, 'mini', pilot, false);
          for (let i = 0; i < 1500 && !(B.snapshot().subBossActive); i++) await new Promise(r => requestAnimationFrame(r));
          if (B.player) B.player.invuln = 1e9;
          return {mini: !!B.snapshot().subBossActive};
        }""", [1, 'cole'])
        ok(M.get('mini'), 'a miniboss is up (stage 1)')
        F2 = pg.evaluate(FRAME)
        ok('bmbar_tab_mini' in F2['keys'], 'it draws the mini tab')
        labs2 = [l for l in F2['labels'] if l.get('n')]
        ok(len(labs2) >= 1, 'the mini tab carries lettering')
        for i, l in enumerate(labs2):
            ok(abs(l['cy']) <= 1.5, 'MINI BOSS label %d is vertically centred (%.2f px off, socket %dpx)' % (i, l['cy'], l['sh']))
            ok(abs(l['cx']) <= 2.5, 'MINI BOSS label %d is horizontally centred (%.2f px off)' % (i, l['cx']))
            ok(l['iw'] < l['sw'], 'MINI BOSS fits its socket without touching the rails (%dpx ink in %dpx)' % (l['iw'], l['sw']))
        d2 = pg.evaluate("() => { const c=document.getElementById('screen'); return c?c.toDataURL('image/png'):null; }")
        if d2:
            open(os.path.join(OUT, '04_mini_live.png'), 'wb').write(base64.b64decode(d2.split(',', 1)[1]))

        ok(not errs, 'no page or console errors (%d)' % len(errs))
        for e in errs[:6]:
            print('    !', e)
        b.close(); stop()

    print('\n%d ok / %d fail' % (n_ok[0], len(fails)))
    for f in fails:
        print('  FAIL', f)
    sys.exit(1 if fails else 0)


if __name__ == '__main__':
    main()
