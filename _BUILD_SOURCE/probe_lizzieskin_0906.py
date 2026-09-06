#!/usr/bin/env python3
"""probe_lizzieskin_0906.py - does the B-42 costume actually reach the screen?

    python _BUILD_SOURCE/probe_lizzieskin_0906.py

Mike, 0906: "store lizzie's old b-42 bomber sprites as an alternate costume pick if we use the
password bomber."

WHAT THIS HAS TO PROVE, AND WHY A FLAG CHECK WOULD NOT.  The costume works by repointing
`BOFX.ships` rects and flushing XART's ship-cell cache. Both halves can look right while the screen
shows the old aircraft: the table is correct the instant it is written, and the CACHE is what the
draw reads. `lizzieSkinOn===true` therefore proves nothing at all - it is set by the same function
that does the repoint, so it is true even if the flush is removed. This measures the PIXELS: the
canvas XART hands back for `ship_lizzie` is captured before and after the toggle and compared.

It also checks the toggle both ways. A one-way test passes on a build that can turn the costume on
and never off, which is the state a player would actually be stuck in.
"""
import os, sys, base64
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shoot as sh

OUT = os.path.join(sh.GAME, 'docs/proofs/lizzieskin_0906')

# a cheap fingerprint of what XART is actually handing to drawImage for a key
SIG = r"""
(k) => {
  if (typeof XART === 'undefined' || !XART.rdy(k)) return null;
  const im = XART.get(k);
  if (!im) return null;
  const c = document.createElement('canvas');
  c.width = im.naturalWidth || im.width; c.height = im.naturalHeight || im.height;
  c.getContext('2d').drawImage(im, 0, 0);
  const d = c.getContext('2d').getImageData(0, 0, c.width, c.height).data;
  let h = 0, ink = 0;
  for (let i = 0; i < d.length; i += 4) {
    if (d[i+3] > 8) { ink++; h = (h * 31 + d[i] + d[i+1] * 3 + d[i+2] * 7) >>> 0; }
  }
  return {w: c.width, h: c.height, ink: ink, sig: h, rect: (BOFX.ships[k]||[]).join(',')};
}
"""


def main():
    port, stop = sh.serve(sh.GAME)
    from playwright.sync_api import sync_playwright
    os.makedirs(OUT, exist_ok=True)
    rows, errs, ok = [], [], True
    KEYS = ['ship_lizzie', 'ship_lizzie_pv0', 'ship_lizzie_br0', 'ship_lizzie_l']
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        pg = br.new_page(viewport={'width': 900, 'height': 900})
        pg.on('pageerror', lambda e: errs.append('pageerror: ' + str(e)))
        pg.on('console', lambda m: errs.append('console.error: ' + m.text) if m.type == 'error' else None)
        pg.goto('http://127.0.0.1:%d/index.html' % port)
        pg.wait_for_function("() => typeof XART !== 'undefined' && typeof GS !== 'undefined'",
                             timeout=30000)
        pg.wait_for_timeout(400)
        pg.evaluate(sh.TRAP_RAF)
        st = pg.evaluate(sh.SETUP, {'state': 'PILOT', 'pilot': 'lizzie'})
        if not st.get('ok'):
            print('SETUP FAILED: %s' % st.get('err')); br.close(); stop(); return 1
        for k in KEYS:
            pg.evaluate("(k) => XART.rdy(k)", k)
        pg.wait_for_function("() => XART.rdy('ship_lizzie') && XART.rdy('ship_lizzie_br0')",
                             timeout=15000)

        print('the password gate:')
        print('   unlocked before BOMBER: %s'
              % pg.evaluate("() => lizzieSkinUnlocked"))
        # the toggle must be INERT until the password is entered
        pg.evaluate("() => { pilotIndex = PILOTS.findIndex(p=>p&&p.key==='lizzie');"
                    " pilotRot = 0; pilotFrom = pilotIndex; }")
        stock = {k: pg.evaluate(SIG, k) for k in KEYS}

        pg.evaluate("() => { pwInput='BOMBER'; submitPassword(); }")
        unlocked = pg.evaluate("() => lizzieSkinUnlocked")
        print('   unlocked after  BOMBER: %s' % unlocked)
        if not unlocked:
            ok = False; errs.append('BOMBER did not set lizzieSkinUnlocked')

        pg.evaluate("() => applyLizzieSkin(true)")
        b42 = {k: pg.evaluate(SIG, k) for k in KEYS}
        pg.evaluate("() => applyLizzieSkin(false)")
        back = {k: pg.evaluate(SIG, k) for k in KEYS}

        print()
        print('%-18s %-26s %-26s %s' % ('key', 'stock', 'B-42', 'restored'))
        print('-' * 92)
        for k in KEYS:
            s, b, r = stock[k], b42[k], back[k]
            if not (s and b and r):
                rows.append((k, 'UNRESOLVED')); ok = False; continue
            changed = (s['sig'] != b['sig'])
            restored = (s['sig'] == r['sig'])
            if not changed or not restored:
                ok = False
            print('%-18s %-26s %-26s %s%s' % (
                k,
                '%dx%d ink %d' % (s['w'], s['h'], s['ink']),
                '%dx%d ink %d' % (b['w'], b['h'], b['ink']),
                '%dx%d ink %d' % (r['w'], r['h'], r['ink']),
                '' if (changed and restored) else
                ('   <-- NO CHANGE' if not changed else '   <-- DID NOT RESTORE')))

        # and a picture of each state, because a hash is not a bomber
        pg.evaluate("() => applyLizzieSkin(true)")
        pg.evaluate(sh.STEP, 6)
        png = pg.evaluate("() => { const g=document.querySelector('#screen-area canvas')"
                          "||document.querySelector('canvas'); return g?g.toDataURL('image/png'):null; }")
        if png:
            open(os.path.join(OUT, 'lizzie_b42.png'), 'wb').write(base64.b64decode(png.split(',', 1)[1]))
        pg.evaluate("() => applyLizzieSkin(false)")
        pg.evaluate(sh.STEP, 6)
        png = pg.evaluate("() => { const g=document.querySelector('#screen-area canvas')"
                          "||document.querySelector('canvas'); return g?g.toDataURL('image/png'):null; }")
        if png:
            open(os.path.join(OUT, 'lizzie_stock.png'), 'wb').write(base64.b64decode(png.split(',', 1)[1]))
        # ---- AND IT MUST SURVIVE THE STAGE, NOT JUST THE MENU. The rect swap is global so this
        # ought to follow structurally - but 'ought to' is what CLAUDE.md keeps recording as the
        # step where a correct state and a wrong picture part company. beginStage warms art and
        # could plausibly re-resolve, so drive real PLAY with the skin on and read the hull.
        pg.evaluate("() => applyLizzieSkin(true)")
        st2 = pg.evaluate(sh.SETUP, {'state': 'PLAY', 'stage': 1, 'pilot': 'lizzie', 'invuln': True})
        if not st2.get('ok'):
            errs.append('PLAY setup: %s' % st2.get('err'))
        for _ in range(4):
            pg.evaluate(sh.STEP, 30); pg.wait_for_timeout(60)
        inplay = pg.evaluate(SIG, 'ship_lizzie')
        same = bool(inplay and b42['ship_lizzie'] and inplay['sig'] == b42['ship_lizzie']['sig'])
        print()
        print('in PLAY on stage 1, the hull XART serves for ship_lizzie is %s'
              % ('the B-42' if same else 'NOT the B-42 -- the skin did not survive beginStage'))
        if not same:
            ok = False
        png = pg.evaluate("() => { const g=document.querySelector('#screen-area canvas')"
                          "||document.querySelector('canvas'); return g?g.toDataURL('image/png'):null; }")
        if png:
            open(os.path.join(OUT, 'lizzie_b42_inplay.png'), 'wb').write(
                base64.b64decode(png.split(',', 1)[1]))
        br.close()
    stop()

    print()
    print('the swap reaches the drawn canvas and reverses cleanly' if ok
          else '!! the costume did not change or did not restore what the game DRAWS')
    print('shots -> docs/proofs/lizzieskin_0906/')
    if errs:
        print()
        print('%d errors:' % len(errs))
        for e in errs[:8]:
            print('   ' + e)
    else:
        print('0 console errors, 0 page errors')
    return 0 if (ok and not errs) else 1


if __name__ == '__main__':
    sys.exit(main())
