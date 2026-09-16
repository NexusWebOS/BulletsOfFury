#!/usr/bin/env python3
"""probe_unlocks_0916.py - the NEW WEAPONS UNLOCKED page announces where the engine GRANTS.

Mike, 0916: "announcement should be after stage 4 victory yes. The same should apply if you unlock
the laser mist on stage 9 if you beat the level."

So two claims, and both are checked against the ENGINE's own grant sites rather than against the
table that describes them:

  * `yuriLightningOrbGrantStage4` is called from `bossDie` at `run.stage===4`, so stage 2 must no
    longer promise Yuri the LIGHTNING ORB and stage 4 must announce it.
  * `laserMistUnlock` is called from `bossDie` at `run.stage===9` (the BONUS stage), so clearing
    stage 9 must announce LASER MIST.

The page is then driven the real way - the real debrief, a real key tap on its CONTINUE - and the
icon is identified by the KEY iconBlit was asked for AND by the sheet the blit came from:

  the LASER MIST icon is NOT on nia_icons. iconBlit routes micon_lasermist_* to
  laserMistAtlasBlit, which reads bof_laser_mist_weapon_atlas, and XART.rdy is false on its first
  call - so an unwarmed page draws the name beside a hole and nothing errors. The blit is matched
  on that sheet's own dimensions (XART.get returns a fresh canvas, so identity and .src catch
  nothing - CLAUDE.md 0905h and the .src note above it).

A BUSTED ARM runs first: with the warm suppressed the atlas is not ready and the icon does not
blit, so the pass below can fail.

Writes docs/proofs/unlocks_0916/ (stage 4 Yuri, stage 9 laser mist).
"""
import os, sys, base64
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shoot

OUT = 'docs/proofs/unlocks_0916'

# Wrap iconBlit (a top-level declaration, so its binding is reassignable) to record the KEY each
# row asked for, and the game context's OWN drawImage to record what that call actually blitted.
TRAP = r"""() => {
  if (window.__utrap) return true;
  window.__utrap = 1;
  window.__icons = [];      // [key, drewFromSheetWxH]
  window.__inIcon = 0;
  window.__lastBlit = null;
  window.__blits = []; window.__rec = 0;
  const c = ctx, od = c.drawImage;
  c.drawImage = function (im) {
    try {
      if (window.__inIcon && im) window.__lastBlit = {W: im.width || im.naturalWidth, H: im.height || im.naturalHeight};
      if (window.__rec && im) {
        const a = arguments;
        let dx = 0, dy = 0, dw = 0, dh = 0;
        if (a.length >= 9) { dx = a[5]; dy = a[6]; dw = a[7]; dh = a[8]; }
        else if (a.length >= 5) { dx = a[1]; dy = a[2]; dw = a[3]; dh = a[4]; }
        const m = c.getTransform();
        window.__blits.push({W: im.width || im.naturalWidth, H: im.height || im.naturalHeight,
                             x: m.a * dx + m.e, y: m.d * dy + m.f, w: dw * m.a, h: dh * m.d});
      }
    } catch (e) {}
    return od.apply(this, arguments);
  };
  const oi = iconBlit;
  iconBlit = function (g, key, x, y, h, centred) {
    window.__inIcon = 1; window.__lastBlit = null;
    let r = null;
    try { r = oi.apply(this, arguments); } finally {
      window.__inIcon = 0;
      window.__icons.push({key: key, ret: r, blit: window.__lastBlit});
    }
    return r;
  };
  return true;
}"""

# The real debrief for a cleared stage, then its own CONTINUE, then the unlock page's CONTINUE.
RUN = r"""async ([stage, pilot]) => {
  const step = async (n) => { for (let i = 0; i < n; i++) { window.__bofStepNow = (window.__bofStepNow || performance.now()) + 1000 / 60; loop(window.__bofStepNow); } };
  const tap = async () => { Input.keys['enter'] = false; Input.injectTap('enter'); await step(1); };
  run.stage = stage; run.pilot = pilot;
  curStage = STAGES[stage - 1];
  drawStageClear._init = false; drawStageClear._res = null; drawStageClear._unShown = false;
  unlocks = null;
  setState(GS.STAGECLEAR);
  await step(20);
  const onDebrief = (state === GS.STAGECLEAR);
  await tap();                      // skip the flourish
  await step(4);
  await tap();                      // leave the debrief
  await step(2);
  return {onDebrief: onDebrief, state: state, isUnlocks: (state === GS.UNLOCKS),
          rows: unlocks ? unlocks.rows.map(r => r[0]) : null,
          keys: unlocks ? unlocks.rows.map(r => r[1]) : null};
}"""

# let the typewriter finish before a proof frame is taken - the first cut caught "LASER" mid-reveal
SETTLE = r"""async ([n]) => {
  for (let i = 0; i < n; i++) { window.__bofStepNow = (window.__bofStepNow || performance.now()) + 1000 / 60; loop(window.__bofStepNow); }
  return unlocks ? unlocks.t : -1;
}"""

DRAW = r"""async ([n]) => {
  const step = async (k) => { for (let i = 0; i < k; i++) { window.__bofStepNow = (window.__bofStepNow || performance.now()) + 1000 / 60; loop(window.__bofStepNow); } };
  window.__icons = [];
  for (let i = 0; i < n; i++) { await step(6); await new Promise(r => setTimeout(r, 20)); }
  const A = (typeof XART !== 'undefined' && XART.rdy('bof_laser_mist_weapon_atlas')) ? XART.get('bof_laser_mist_weapon_atlas') : null;
  return {icons: window.__icons, mistSheet: A ? {W: A.width, H: A.height} : null,
          mistReady: !!A, state: state};
}"""



# n rows through the page's own entry point, then one recorded frame: the panels are read back from
# the blits the draw actually made (chunks of four - box, then the strip's three slices), and the
# name's ink is read out of the canvas inside the strip it belongs to.
LAYOUT = r"""async ([n, presses]) => {
  const step = async (k) => { for (let i = 0; i < k; i++) { window.__bofStepNow = (window.__bofStepNow || performance.now()) + 1000/60; loop(window.__bofStepNow); } };
  const briefBelow = () => {
    try {
      const R = scPanelRect(), S = SC_SLOTS_FULL.brief, m = ctx.getTransform();
      const bx = R[0] + R[2] * S[0], by = R[1] + R[3] * S[1], bw = R[2] * S[2], bh = R[3] * S[3];
      const dx0 = Math.round(m.a * bx + m.e), dy1 = Math.round(m.d * (by + bh) + m.f);
      const dw0 = Math.round(bw * m.a), band = Math.max(3, Math.round(bh * m.d * 0.5));
      const q = ctx.getImageData(dx0, dy1 + 1, dw0, band);
      let nn = 0;
      for (let i = 0; i < q.data.length; i += 4) {
        const r = q.data[i], g = q.data[i + 1], b2 = q.data[i + 2];
        if (r > 190 && g > 140 && g < 240 && b2 < 130 && (r - b2) > 90) nn++;   // the brief's gold
      }
      return nn;
    } catch (e) { return -1; }
  };
  const NM = ['FIRE ORB','ICE BREATH','THERMOSHOCK BALL','LASER MIST','CHAINGUN','LIGHTNING ORB','FIRE ORB','ICE BREATH'];
  const KY = ['micon_fireorb_3','micon_icebreath_3','micon_thermoshock_3','micon_lasermist_3','micon_chaingun_3','micon_lightningorb_3','micon_fireorb_3','micon_icebreath_3'];
  const rows = []; for (let i = 0; i < n; i++) rows.push([NM[i], KY[i]]);
  run.stage = 2;
  unlocksStart(rows, null);
  /* ⚠ A CONTROL FOR THE BRIEF. The band under its bay contains the plate's OWN warm metal, so a
     raw gold count there is not evidence of anything - the first cut reported 948px on a frame
     where the message plainly fits. This is the same band at t~0, before the brief has faded in
     at all, so the live count is compared against what the ART puts there. */
  await step(2);
  const base = briefBelow();
  await step(200);
  /* ⚠ menuDown() is tapAny(keybind.down) - a LIST of bound names - and CLAUDE.md records that an
     injected tap is invisible to tapAny until Input.keys[k] EXISTS. So the probe injects the
     engine's OWN first binding for that action, with the key seeded false first. */
  const DK = (typeof keybind !== 'undefined' && keybind.down && keybind.down[0]) || 'down';
  for (let p = 0; p < (presses || 0); p++) { Input.keys[DK] = false; Input.injectTap(DK); await step(2); }
  await step(30);
  const pl = XART.rdy('statpanel_full_0916') ? XART.get('statpanel_full_0916') : null;
  const PW = pl ? (pl.naturalWidth || pl.width) : -1, PH = pl ? (pl.naturalHeight || pl.height) : -1;
  window.__blits = []; window.__icons = []; window.__rec = 1;
  await step(1);                       /* NOT requestAnimationFrame: this probe traps rAF */
  window.__rec = 0;
  /* the first plate blit of the frame is the PAGE BACKGROUND - the whole plate, full width. It has
     the same source dimensions as every panel cut out of it, so chunking without excluding it put
     every row's box and strip one slot out and reported a constant 222px "off centre" on text that
     is dead centre. Exclude anything as wide as the page. */
  const full = ctx.canvas.width * 0.9;
  const panels = window.__blits.filter(b => b.W === PW && b.H === PH && b.w > 4 && b.h > 4 && b.w < full);
  const out = [];
  for (let i = 0; i + 3 < panels.length; i += 4) {
    const box = panels[i], sl = panels.slice(i + 1, i + 4);
    const x0 = Math.min.apply(null, sl.map(q => q.x)), x1 = Math.max.apply(null, sl.map(q => q.x + q.w));
    const sx = Math.round(x0), sy = Math.round(box.y), sw = Math.round(x1 - x0), sh = Math.round(box.h);
    let d = null; try { d = ctx.getImageData(sx, sy, sw, sh); } catch (e) {}
    let a0 = 1e9, a1 = -1, cnt = 0;
    if (d) for (let y = 0; y < sh; y++) for (let x = 0; x < sw; x++) {
      const q = (y * sw + x) * 4, r = d.data[q], g = d.data[q + 1], b2 = d.data[q + 2];
      if (g > 110 && g > r * 1.25 && g > b2 * 1.25) { cnt++; if (x < a0) a0 = x; if (x > a1) a1 = x; }
    }
    out.push({box: {x: Math.round(box.x), w: Math.round(box.w), h: Math.round(box.h)},
              strip: {x: sx, w: sw}, ink: cnt,
              off: cnt ? (((a0 + a1) / 2) - (sw - 1) / 2) : null});
  }
  return {rows: out, scroll: unlocks ? unlocks.scroll : -1, n: n,
          keys: window.__icons.map(o => o.key),
          briefBelow: briefBelow(), briefBase: base, downKey: DK,
          shot: (document.getElementById('screen') || {toDataURL: () => null}).toDataURL('image/png')};
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
        pg.evaluate(TRAP)

        # ---- 1. the table answers where the engine grants -------------------------------------
        T = pg.evaluate("""() => ({
          s2yuri: unlockRowsFor(2,'yuri').map(r=>r[0]),
          s2all:  unlockRowsFor(2,'cole').map(r=>r[0]),
          s2frz:  unlockRowsFor(2,'freezer').map(r=>r[0]),
          s3:     unlockRowsFor(3,'cole').map(r=>r[0]),
          s4yuri: unlockRowsFor(4,'yuri').map(r=>r[0]),
          s4cole: unlockRowsFor(4,'cole').map(r=>r[0]),
          s9:     unlockRowsFor(9,'cole').map(r=>r[0]),
          s9yuri: unlockRowsFor(9,'yuri').map(r=>r[0]),
          s9key:  unlockRowsFor(9,'cole').map(r=>r[1]),
          grantsMist: /run\\.stage===9[^;]*laserMistUnlock/.test(bossDie.toString()),
          grantsOrb:  /run\\.stage===4[^;]*yuriLightningOrbGrantStage4/.test(bossDie.toString()),
          bonus9: !!(STAGES[8] && STAGES[8].bonus)
        })""")
        ok(T['grantsOrb'], 'the engine grants the lightning orb at stage 4 (bossDie)')
        ok(T['grantsMist'], 'the engine grants laser mist at stage 9 (bossDie)')
        ok(T['bonus9'], 'stage 9 is the bonus stage, so this page is not the campaign end')
        ok(T['s2yuri'] == ['FIRE ORB'], 'stage 2 no longer promises Yuri the lightning orb (%s)' % T['s2yuri'])
        ok(T['s2all'] == ['FIRE ORB'], 'stage 2 still announces the fire orb for everyone else (%s)' % T['s2all'])
        ok(T['s2frz'] == ['ICE BREATH', 'THERMOSHOCK BALL'], "Freezer's stage-2 row is untouched (%s)" % T['s2frz'])
        ok(T['s4yuri'] == ['LIGHTNING ORB'], 'stage 4 announces the lightning orb to Yuri (%s)' % T['s4yuri'])
        ok(T['s4cole'] == [], 'a pilot who is not Yuri gets no stage-4 page (%s)' % T['s4cole'])
        ok(T['s9'] == ['LASER MIST'], 'stage 9 announces laser mist (%s)' % T['s9'])
        ok(T['s9yuri'] == ['LASER MIST'], 'stage 9 announces it to every pilot (%s)' % T['s9yuri'])
        ok(T['s9key'] == ['micon_lasermist_3'], 'it uses the laser mist icon family (%s)' % T['s9key'])
        ok(T['s3'] == [], 'stage 3 still has no row, so no page appears (%s)' % T['s3'])

        # ---- 2. BUSTED ARM: without the atlas warm the icon cannot blit ------------------------
        pg.evaluate("""() => { window.__realWarm = laserMistWarm; laserMistWarm = function(){};
                               if (XART && XART.img) delete XART.img['bof_laser_mist_weapon_atlas'];
                               if (XART && XART._dec) delete XART._dec['bof_laser_mist_weapon_atlas']; }""")
        R = pg.evaluate(RUN, [9, 'cole'])
        bust = pg.evaluate(DRAW, [6])
        bust_icons = [i for i in bust['icons'] if i['key'] == 'micon_lasermist_3' and i['blit']]
        ok(not bust_icons, 'busted arm: with the warm suppressed the laser mist icon never blits (%d)' % len(bust_icons))
        pg.evaluate("() => { laserMistWarm = window.__realWarm; }")

        # ---- 3. the real stage-9 debrief -> the unlock page ------------------------------------
        R = pg.evaluate(RUN, [9, 'cole'])
        ok(R['onDebrief'], 'stage 9 reaches the debrief')
        ok(R['isUnlocks'], 'its CONTINUE lands on NEW WEAPONS UNLOCKED (state %s)' % R['state'])
        ok(R['rows'] == ['LASER MIST'], 'the page carries the laser mist row (%s)' % R['rows'])

        for _ in range(40):
            if pg.evaluate("() => XART.rdy('bof_laser_mist_weapon_atlas')"):
                break
            pg.wait_for_timeout(80)
        D = pg.evaluate(DRAW, [8])
        ok(D['mistReady'], 'the laser mist atlas decoded (the page warmed it)')
        mist = [i for i in D['icons'] if i['key'] == 'micon_lasermist_3']
        drew = [i for i in mist if i['blit'] and D['mistSheet'] and i['blit']['W'] == D['mistSheet']['W'] and i['blit']['H'] == D['mistSheet']['H']]
        ok(len(mist) > 0, 'the page asked iconBlit for micon_lasermist_3 (%d frames)' % len(mist))
        ok(len(drew) > 0, 'and it blitted from the laser mist atlas, not the icon sheet (%d of %d)' % (len(drew), len(mist)))
        ok(all(i['ret'] for i in drew), 'iconBlit reported a drawn width every time')
        pg.evaluate(SETTLE, [45])
        shot(pg, '02_stage9_lasermist.png')

        # CONTINUE off the unlock page still reaches the bonus stage's own exit
        st = pg.evaluate("""async () => {
          const step = async (n) => { for (let i=0;i<n;i++){ window.__bofStepNow=(window.__bofStepNow||performance.now())+1000/60; loop(window.__bofStepNow); } };
          // the exit gates on the reveal being in (0.55 + rows*0.45 + 0.2 seconds of page time),
          // so this runs AFTER the settle above - a tap before that measures the probe's own
          // impatience and not the page
          const t0 = unlocks ? unlocks.t : -1;
          Input.keys['enter']=false; Input.injectTap('enter'); await step(1); await step(3);
          return {state: state, left: state !== GS.UNLOCKS, t0: t0};
        }""")
        ok(st['left'], 'its CONTINUE leaves the page through scLeaveStage at page t %.2f (state %s)' % (st['t0'], st['state']))

        # ---- 4. the stage-4 control, Yuri -----------------------------------------------------
        R4 = pg.evaluate(RUN, [4, 'yuri'])
        ok(R4['isUnlocks'] and R4['rows'] == ['LIGHTNING ORB'],
           'stage 4 as Yuri shows LIGHTNING ORB (%s, state %s)' % (R4['rows'], R4['state']))
        D4 = pg.evaluate(DRAW, [8])
        orb = [i for i in D4['icons'] if i['key'] == 'micon_lightningorb_3' and i['blit']]
        ok(len(orb) > 0, 'the lightning orb icon blits (%d frames)' % len(orb))
        pg.evaluate(SETTLE, [45])
        shot(pg, '01_stage4_lightningorb.png')

        # ---- 5. stage 2 as Yuri no longer opens on the lightning orb ---------------------------
        R2 = pg.evaluate(RUN, [2, 'yuri'])
        ok(R2['isUnlocks'] and R2['rows'] == ['FIRE ORB'],
           'stage 2 as Yuri announces the fire orb alone (%s)' % R2['rows'])

        # ---- 6. the layout Mike asked for: four rows, one column, a square box each ------------
        # four is the cap, so the four-row case is the one that has to be looked at. Driven through
        # the page's own entry point with real icon keys.
        L = pg.evaluate("""async () => {
          const step = async (n) => { for (let i=0;i<n;i++){ window.__bofStepNow=(window.__bofStepNow||performance.now())+1000/60; loop(window.__bofStepNow); } };
          run.stage = 2;
          window.__icons = [];
          unlocksStart([['FIRE ORB','micon_fireorb_3'],['ICE BREATH','micon_icebreath_3'],
                        ['THERMOSHOCK BALL','micon_thermoshock_3'],['LASER MIST','micon_lasermist_3']], null);
          await step(160);
          const keys = window.__icons.slice(-8).map(o => o.key);
          return {state: state, rows: unlocks ? unlocks.rows.length : 0, keys: keys,
                  shot: (document.getElementById('screen')||{toDataURL:()=>null}).toDataURL('image/png')};
        }""")
        ok(L['rows'] == 4, 'the page carries four rows (%s)' % L['rows'])
        ok(len(set(L['keys'])) == 4, 'and four distinct icons are asked for on one frame (%s)' % sorted(set(L['keys'])))
        ok(pg.evaluate("() => UNLOCK_VIEW === 4"), 'four rows are visible at once (UNLOCK_VIEW)')
        ok(pg.evaluate("() => unlockRowsFor(2,'freezer').length <= UNLOCK_MAX"), "Freezer's row set is within the cap")

        # ---- 7. the section is flexible: 1, 2, 3 rows, and it SCROLLS past four ---------------
        for n in (1, 2, 3, 4):
            Z = pg.evaluate(LAYOUT, [n, 0])
            ok(len(Z['rows']) == n, 'a list of %d draws %d row%s (%d)' % (n, n, '' if n == 1 else 's', len(Z['rows'])))
            offs = [r['off'] for r in Z['rows'] if r['off'] is not None]
            ok(len(offs) == n, 'every row of %d carries its name (%d inked)' % (n, len(offs)))
            # the measure is the INK bounding box and the draw centres the ADVANCE box, so a few
            # device px of glyph side-bearing is expected and is not a placement error (measured
            # 1.5-8.0 across these cases, on names whose first and last letters differ). The bar is
            # set well inside one glyph: a left-aligned name in this strip measures ~500px off.
            ok(offs and max(abs(o) for o in offs) <= 14.0,
               'and every name is CENTRED in its strip (worst %.1f px off, n=%d)' % (max(abs(o) for o in offs) if offs else -1, n))
            ok(Z['briefBelow'] <= Z['briefBase'],
               'the stage-clear message fits its bay with n=%d (%d gold px below it against the plate\'s own %d)'
               % (n, Z['briefBelow'], Z['briefBase']))
            if n == 1 and Z.get('shot'):
                open(os.path.join(OUT, '04_one_row.png'), 'wb').write(base64.b64decode(Z['shot'].split(',', 1)[1]))

        Z6 = pg.evaluate(LAYOUT, [6, 0])
        ok(len(Z6['rows']) == 4, 'a list of six shows four at a time (%d)' % len(Z6['rows']))
        ok(Z6['scroll'] == 0, 'starting at the top (scroll %s)' % Z6['scroll'])
        first = Z6['keys'][:1]
        Z6b = pg.evaluate(LAYOUT, [6, 2])
        ok(Z6b['scroll'] == 2, 'DOWN scrolls the section (scroll %s)' % Z6b['scroll'])
        ok(len(Z6b['rows']) == 4, 'still four rows after scrolling (%d)' % len(Z6b['rows']))
        ok(Z6b['keys'][:1] != first, 'and the top row changed (%s -> %s)' % (first, Z6b['keys'][:1]))
        Z6c = pg.evaluate(LAYOUT, [6, 9])
        ok(Z6c['scroll'] == 2, 'the scroll clamps at the end (%s)' % Z6c['scroll'])
        if Z6b.get('shot'):
            open(os.path.join(OUT, '05_scrolled.png'), 'wb').write(base64.b64decode(Z6b['shot'].split(',', 1)[1]))
        # the four-row shot is re-taken last so the proof matches the shipped look
        L2 = pg.evaluate(LAYOUT, [4, 0])
        if L2.get('shot'):
            open(os.path.join(OUT, '03_four_rows.png'), 'wb').write(base64.b64decode(L2['shot'].split(',', 1)[1]))

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
