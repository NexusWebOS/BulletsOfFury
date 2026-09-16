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
  const c = ctx, od = c.drawImage;
  c.drawImage = function (im) {
    try {
      if (window.__inIcon && im) window.__lastBlit = {W: im.width || im.naturalWidth, H: im.height || im.naturalHeight};
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
        if L.get('shot'):
            open(os.path.join(OUT, '03_four_rows.png'), 'wb').write(base64.b64decode(L['shot'].split(',', 1)[1]))
        ok(pg.evaluate("() => UNLOCK_MAX === 4"), 'the cap and the layout are one number (UNLOCK_MAX)')
        ok(pg.evaluate("() => unlockRowsFor(2,'freezer').length <= UNLOCK_MAX"), "Freezer's row set is within the cap")

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
