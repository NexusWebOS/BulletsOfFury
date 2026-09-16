#!/usr/bin/env python3
"""probe_awards_0916.py - ACH-02: the awards gallery and the unlock toast.

The achievement registry has been complete since 0915 - 66 definitions, the awards, the points, the
persistence - and nothing drew any of it: `achievementUnlock` set a variable and dispatched a window
event nothing listened to. A player could earn 1,630 points and never be told once.

Driven in real Chromium:
  * the title carries a SEVENTH button and its plate decodes;
  * ACHIEVEMENTS opens the gallery, which lists all 66 with their points and a locked/unlocked state;
  * the list scrolls and clamps, and BACK returns to the title with the cursor on ACHIEVEMENTS;
  * an unlock draws a toast at the bottom that RISES, holds and leaves - measured as ink in the
    bottom band across frames, not as a flag;
  * several unlocks at once QUEUE rather than replacing one another (a stage clear can award seven).

⚠ THE ACHIEVEMENT STORE IS localStorage AND IT PERSISTS. Every arm clears it first, or the second
run of this probe measures a build where everything is already unlocked and nothing can fire.
"""
import os, sys, base64
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shoot

OUT = 'docs/proofs/awards_0916'

STEP = r"""async ([n]) => {
  for (let i = 0; i < n; i++) { window.__bofStepNow = (window.__bofStepNow || performance.now()) + 1000/60; loop(window.__bofStepNow); }
  return state;
}"""

# the bottom band, where the toast lives: how much lit ink is in it this frame
INK = r"""([y0, y1]) => {
  try {
    const m = ctx.getTransform();
    const dy0 = Math.round(m.d * y0 + m.f), dy1 = Math.round(m.d * y1 + m.f);
    const d = ctx.getImageData(0, dy0, ctx.canvas.width, Math.max(1, dy1 - dy0));
    let n = 0, top = 1e9;
    for (let i = 0; i < d.data.length; i += 4) {
      const r = d.data[i], g = d.data[i+1], b = d.data[i+2];
      if ((r * 299 + g * 587 + b * 114) / 1000 > 95) { n++; const row = Math.floor((i / 4) / ctx.canvas.width); if (row < top) top = row; }
    }
    return {n: n, top: n ? top : -1};
  } catch (e) { return {n: -1, top: -1, err: String(e && e.message || e)}; }
}"""


# ⚠ THE TOAST'S MOTION CANNOT BE READ AS "the lowest lit row in the bottom band": the title screen
# fills that band with its own ink, so the minimum row is 0 on every frame whatever the toast does.
# The toast's own panel is blitted from statpanel_full_0916 - trap that blit and read its dest y.
TRAP = r"""() => {
  if (window.__atrap) return true;
  window.__atrap = 1;
  window.__panels = []; window.__rec = 0;
  const c = ctx, od = c.drawImage;
  c.drawImage = function (im) {
    try {
      if (window.__rec && im) {
        const pl = XART.rdy('statpanel_full_0916') ? XART.get('statpanel_full_0916') : null;
        const W = im.width || im.naturalWidth, H = im.height || im.naturalHeight;
        if (pl && W === (pl.naturalWidth || pl.width) && H === (pl.naturalHeight || pl.height)) {
          const a = arguments;
          let dx = 0, dy = 0, dw = 0, dh = 0;
          if (a.length >= 9) { dx = a[5]; dy = a[6]; dw = a[7]; dh = a[8]; }
          else if (a.length >= 5) { dx = a[1]; dy = a[2]; dw = a[3]; dh = a[4]; }
          window.__panels.push({x: dx, y: dy, w: dw, h: dh});
        }
      }
    } catch (e) {}
    return od.apply(this, arguments);
  };
  return true;
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

    def shot(pg, name):
        d = pg.evaluate("() => { const c=document.getElementById('screen'); return c?c.toDataURL('image/png'):null; }")
        if d:
            open(os.path.join(OUT, name), 'wb').write(base64.b64decode(d.split(',', 1)[1]))

    with sync_playwright() as p:
        b = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
        pg = b.new_page(viewport={'width': 1100, 'height': 1000}, device_scale_factor=1)
        pg.on('pageerror', lambda e: errs.append('pageerror: ' + str(e)[:200]))
        pg.on('console', lambda m: errs.append('console: ' + m.text[:200]) if m.type == 'error' else None)
        pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=60000)
        pg.wait_for_function("() => typeof ASSETS!=='undefined' && typeof setState==='function'", timeout=60000)
        pg.wait_for_function("() => (window.__bofFrames|0) > 4", timeout=60000)
        pg.evaluate("() => { ASSETS.ready = true; }")
        pg.evaluate(shoot.TRAP_RAF)
        pg.wait_for_timeout(60)

        # ---- 1. the seventh button ----
        T = pg.evaluate("""() => ({items: TITLE_ITEMS.slice(), keys: MENU_KEYS.slice(),
                                   acts: Object.keys(TITLE_ACTION),
                                   idx: TITLE_ITEMS.indexOf('ACHIEVEMENTS')})""")
        ok(len(T['items']) == 7 and 'ACHIEVEMENTS' in T['items'], 'the title carries a seventh button (%s)' % T['items'])
        ok(len(T['keys']) == len(T['items']), 'every item has a plate (%d keys for %d items)' % (len(T['keys']), len(T['items'])))
        ok(sorted(T['acts']) == sorted(T['items']), 'and every item has its OWN action - the dispatch is keyed by name')
        for _ in range(40):
            pg.evaluate("() => XART.rdy('btn_achievements')")
            if pg.evaluate("() => XART.rdy('btn_achievements')"):
                break
            pg.wait_for_timeout(80)
        ok(pg.evaluate("() => XART.rdy('btn_achievements')"), 'the AWARDS plate decoded')
        pg.evaluate(STEP, [6])
        shot(pg, '01_title.png')

        # ---- 2. the gallery ----
        pg.evaluate("""([i]) => { setState(GS.TITLE); menuIndex = i; titlePending = null; menuFlash = 0; chooseTitle(); }""", [T['idx']])
        st = pg.evaluate(STEP, [40])
        ok(st == 'achievements', 'choosing ACHIEVEMENTS opens the gallery (state %s)' % st)
        G = pg.evaluate("""() => ({rows: awards.rows.length, view: AWARDS_VIEW, scroll: awards.scroll,
                                   first: awards.rows.slice(0,3).map(r => r.title),
                                   locked: awards.rows.filter(r => !r.unlocked).length,
                                   pts: achievementPoints(),
                                   fams: awards.rows.slice(0, 12).map(r => r.family)})""")
        ok(G['rows'] == 66, 'it lists every definition (%d)' % G['rows'])
        ok(G['view'] == 8, 'eight at a time (%d)' % G['view'])
        ok(G['fams'][0] == 'campaign_clear', 'sorted by family, the big ones first (%s)' % G['fams'][0])
        ok(G['locked'] > 0, 'locked rows are listed, not hidden (%d locked)' % G['locked'])
        shot(pg, '02_gallery.png')

        # the list scrolls and clamps
        pg.evaluate("""() => { const k = (keybind.down && keybind.down[0]) || 'down'; Input.keys[k] = false; Input.injectTap(k); }""")
        pg.evaluate(STEP, [2])
        s1 = pg.evaluate("() => awards.scroll")
        ok(s1 == 1, 'DOWN scrolls the gallery (%s)' % s1)
        for _ in range(80):
            pg.evaluate("""() => { const k = (keybind.down && keybind.down[0]) || 'down'; Input.keys[k] = false; Input.injectTap(k); }""")
            pg.evaluate(STEP, [2])
        s2 = pg.evaluate("() => ({s: awards.scroll, max: awards.rows.length - AWARDS_VIEW})")
        ok(s2['s'] == s2['max'], 'and clamps at the end (%s of %s)' % (s2['s'], s2['max']))
        shot(pg, '03_gallery_end.png')

        # BACK returns to the title, with the cursor on ACHIEVEMENTS
        pg.evaluate("""() => { const k = (keybind.back && keybind.back[0]) || 'escape'; Input.keys[k] = false; Input.injectTap(k); }""")
        st = pg.evaluate(STEP, [4])
        ok(st == 'title', 'BACK returns to the title (%s)' % st)
        ok(pg.evaluate("() => menuIndex === TITLE_ITEMS.indexOf('ACHIEVEMENTS')"), 'with the cursor left on ACHIEVEMENTS')

        # ---- 3. the toast ----
        # ⚠ the store persists: clear it or nothing can unlock on a second run
        pg.evaluate("""() => { try { localStorage.removeItem(ACHIEVEMENT_STORE_KEY); } catch(e) {}
                               achievementReload(); achToasts.length = 0; }""")
        base = pg.evaluate(INK, [shoot and 0 or 0, 0]) if False else None
        idle = pg.evaluate(INK, [460, 512])
        pg.evaluate(TRAP)
        pg.evaluate("() => achievementUnlock('stage_clear_1')")
        ok(pg.evaluate("() => achToasts.length === 1"), 'an unlock queues a toast')
        # \u26a0 REPOINTED: the card is a LOWER-LEFT corner card now (Mike, 0916: "should pop up in the
        # lower left corner ... like a steam/xbox 360 achievement system"), so it travels in X from
        # off the left edge. The old assertions measured a bottom strip rising in Y and reported
        # "0.0 px of travel" on a build that moves its full width.
        fr = []
        for i in range(7):
            pg.evaluate("() => { window.__panels = []; window.__rec = 1; }")
            pg.evaluate(STEP, [3])
            pg.evaluate("() => { window.__rec = 0; }")
            got = pg.evaluate("() => window.__panels.slice()")
            if got:
                q = min(got, key=lambda r: r['x'])
                fr.append((round(q['x'], 1), round(q['y'], 1), round(q['w'], 1), round(q['h'], 1)))
        xs = [f[0] for f in fr]
        ok(len(fr) >= 4, 'the toast panel is blitted every frame it is up (%d frames)' % len(fr))
        ok(xs and xs[0] < xs[-1], 'and it SLIDES IN from the left edge (panel x %s -> %s)' % (xs[0] if xs else None, xs[-1] if xs else None))
        ok(xs and xs[0] < 0, 'starting off-screen (%s)' % (xs[0] if xs else None))
        vh = pg.evaluate("() => VH")
        last = fr[-1] if fr else None
        ok(last and abs(last[0] - 8) <= 2, 'and resting in the LEFT corner (x %s)' % (last[0] if last else None))
        ok(last and abs((last[1] + last[3]) - (vh - 8)) <= 2,
           'at the BOTTOM of the screen (bottom %s of %s)' % ((last[1] + last[3]) if last else None, vh - 8))
        shot(pg, '04_toast.png')
        pg.evaluate(STEP, [260])
        ok(pg.evaluate("() => achToasts.length === 0"), 'it leaves on its own')
        pg.evaluate("() => { window.__panels = []; window.__rec = 1; }")
        pg.evaluate(STEP, [3])
        pg.evaluate("() => { window.__rec = 0; }")
        ok(pg.evaluate("() => window.__panels.length === 0"), 'and stops drawing entirely once it has')

        # several at once QUEUE
        pg.evaluate("""() => { try { localStorage.removeItem(ACHIEVEMENT_STORE_KEY); } catch(e) {}
                               achievementReload(); achToasts.length = 0;
                               ['stage_clear_1','stage_clear_2','stage_clear_3'].forEach(id => achievementUnlock(id)); }""")
        ok(pg.evaluate("() => achToasts.length === 3"), 'three unlocks at once queue three toasts')
        # one card lives slide+hold+out = ~3.95s, so 200 frames (3.3s) is not enough to retire one -
        # the first cut asserted against its own impatience
        pg.evaluate(STEP, [260])
        ok(pg.evaluate("() => achToasts.length < 3"), 'and they play through in order')

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
