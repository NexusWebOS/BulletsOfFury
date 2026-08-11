#!/usr/bin/env python3
"""
probe_weapons.py — drive the pilot weapons through the game's own trigger and check what comes out.

    python3 _BUILD_SOURCE/probe_weapons.py

WHY THIS EXISTS
⚠ THE PLAYER NEVER FIRES IN shoot.py. Firing needs an input tap the capture harness does not
simulate, so pBullets stays empty and any weapon FX measures as dead. Every weapon in this game is
therefore invisible to the one tool that proves pixels — which is exactly how a muzzle flash could
be "missing" for a drop while drawing perfectly on the wrong frame of its reel.

So this calls pShoot() directly, the way CLAUDE.md says a weapon test must, and then asserts on
what actually landed in pBullets. It checks BEHAVIOUR, not just existence:

  DECKER   the reload is the whole design — "what makes it read as a shotgun rather than a spread
           gun is the CADENCE". So the test that matters is that the second pull produces NOTHING,
           and that the trigger comes back after DK_RELOAD. Pellet count alone would pass for a
           spread gun.
  LIZZIE   a MOUNTED gun: two barrels, heavy slugs, and it REPLACES the primary while docked. So
           check the pair, the cadence, and that no primary pellet sneaks out alongside them.

Art is checked too, because a correct bullet with no plate is still a bug.
"""
import http.server, socketserver, threading, os, sys, functools

ROOT = os.path.dirname(os.path.abspath(__file__))
GAME = os.path.abspath(os.path.join(ROOT, '..'))


def serve(directory, port=0):
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=directory)
    handler.log_message = lambda *a, **k: None
    httpd = socketserver.TCPServer(("127.0.0.1", port), handler)
    port = httpd.server_address[1]
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return port, httpd.shutdown


DECKER = r"""
() => {
  const R = {name:'DECKER — incendiary shotgun', checks:[]};
  const add = (ok, label, detail) => R.checks.push({ok:!!ok, label:label, detail:detail||''});
  try {
    ASSETS.ready = true; run.pilot = 'decker';
    curStage = STAGES[0]; beginStage(1); setState(GS.PLAY);
    player.reset(); player.invuln = 1e9;
    enemies.length = 0; pBullets.length = 0; dkShells.length = 0;

    add(!dkActive(), 'the shotgun is OFF until the pickup grants it');
    pBullets.length = 0; pShoot();
    const beforeGrant = pBullets.filter(b => b.kind === 'dkshot').length;
    add(beforeGrant === 0, 'and fires no pellets before that', 'got ' + beforeGrant);

    dkGrant();
    add(dkActive(), 'dkGrant arms it');

    // ---- BLAST ----
    pBullets.length = 0; dkShells.length = 0;
    pShoot();
    const blast = pBullets.filter(b => b.kind === 'dkshot');
    add(blast.length === DK_PELLETS, DK_PELLETS + ' pellets in one blast', 'got ' + blast.length);
    const angs = new Set(blast.map(b => b._ang));
    add(angs.size === DK_PELLETS,
        'each pellet indexes its OWN pre-angled plate (ndk_ang_0..6)',
        'distinct _ang: ' + angs.size);
    const vxs = blast.map(b => b.vx).sort((a,b) => a-b);
    add(vxs.length && vxs[0] < 0 && vxs[vxs.length-1] > 0,
        'the spread is symmetric about straight up',
        'vx ' + (vxs[0]||0).toFixed(2) + ' .. ' + (vxs[vxs.length-1]||0).toFixed(2));
    add(dkShells.length === 2, 'two shells eject, one per side',
        'got ' + dkShells.length);
    add(player._dkMuz != null, 'the muzzle blast reel is armed');

    // ---- RELOAD: the point of the whole weapon ----
    pBullets.length = 0;
    pShoot(); pShoot(); pShoot();
    const during = pBullets.filter(b => b.kind === 'dkshot').length;
    add(during === 0, 'RELOADING: the trigger is dead and nothing comes out',
        'got ' + during + ' pellets');
    const leaked = pBullets.length;
    add(leaked === 0, 'and no primary pellet leaks past it either', 'got ' + leaked);

    // ---- READY AGAIN ----
    for (let i = 0; i < 60; i++) dkTick(DK_RELOAD / 40);
    pBullets.length = 0; pShoot();
    const again = pBullets.filter(b => b.kind === 'dkshot').length;
    add(again === DK_PELLETS, 'after ' + DK_RELOAD + 's it fires again',
        'got ' + again);

    // ---- BURN ----
    enemies.length = 0;
    spawnEnemy('drone', player.x, player.y - 60, {});
    const e = enemies[0];
    if (e) {
      dkIgnite(e);
      add(e._burn > 0, 'a hit fodder enemy catches fire', '_burn=' + (e._burn||0).toFixed(2));
      const hpBefore = e.hp;
      for (let i = 0; i < 30; i++) dkBurnTick(e, 0.05);
      add(e.hp < hpBefore, 'and the fire keeps eating it',
          'hp ' + hpBefore + ' -> ' + e.hp);
    } else { add(false, 'could not spawn a fodder enemy to ignite'); }
    const bossy = {_boss:1, x:0, y:0, w:10, h:10};
    dkIgnite(bossy);
    add(!(bossy._burn > 0), 'but a boss does NOT — "except for mini bosses and bosses"');
    const mini = {mini:1, x:0, y:0, w:10, h:10};
    dkIgnite(mini);
    add(!(mini._burn > 0), 'and neither does a miniboss');

    // ---- ART ----
    for (let i = 0; i < DK_PELLETS; i++) XART.rdy('ndk_ang_' + i);
    R.artKeys = [];
    for (let i = 0; i < DK_PELLETS; i++) R.artKeys.push('ndk_ang_' + i);
  } catch (e) { R.err = String(e && e.message || e); }
  return R;
}
"""

LIZZIE = r"""
() => {
  const R = {name:'LIZZIE — heavy MG turret mount', checks:[]};
  const add = (ok, label, detail) => R.checks.push({ok:!!ok, label:label, detail:detail||''});
  try {
    ASSETS.ready = true; run.pilot = 'lizzie';
    curStage = STAGES[0]; beginStage(1); setState(GS.PLAY);
    player.reset(); player.invuln = 1e9;
    enemies.length = 0; pBullets.length = 0; lzMount = null;

    /* THE REGRESSION THIS PROBE ACTUALLY CAUGHT. The DECKER block above ran first and granted a
       24s incendiary shotgun. beginStage did not clear run.dkT, and dkActive() checked only the
       timer — so dkFire() claimed the trigger in pShoot ahead of the mount, for a pilot who is
       not Decker, and Lizzie fired nothing. Keep both halves asserted: the timer must not ride
       into the stage, and even if it somehow does, it must not be Lizzie's problem. */
    add(!(run.dkT > 0), "Decker's shotgun timer does not ride into the next stage",
        'run.dkT=' + (run.dkT || 0));
    add(!dkActive(), "and it never claims a non-Decker trigger");

    add(!lzMountActive(), 'the mount is absent until granted');
    lzMountGrant();
    add(!!lzMount && !lzMount.docked, 'it arrives UNDOCKED and flies in');

    const x0 = lzMount.x, y0 = lzMount.y;
    for (let i = 0; i < 40; i++) lzMountTick(LZM_DOCK_T / 30);
    add(lzMountActive(), 'and docks after LZM_DOCK_T (' + LZM_DOCK_T + 's)');
    add(lzMount.s < 1.0, 'shrinking as it closes, per "scale dow"',
        's=' + (lzMount.s||0).toFixed(2));
    add(Math.abs(lzMount.x - player.x) < 0.01,
        'then rides the hull exactly', 'dx=' + (lzMount.x - player.x).toFixed(3));

    // ---- VOLLEY ----
    run._lzCd = 0;
    pBullets.length = 0; pShoot();
    const slugs = pBullets.filter(b => b.kind === 'lzslug');
    add(slugs.length === 2, 'two barrels, two slugs', 'got ' + slugs.length);
    add(pBullets.length === slugs.length,
        'and it REPLACES the primary — nothing else comes out',
        'total bullets ' + pBullets.length);
    if (slugs.length === 2) {
      const dx = Math.abs(slugs[0].x - slugs[1].x);
      add(dx > 0, 'fired from the two barrels, not the hull centre', 'barrel gap ' + dx.toFixed(1));
      add(slugs[0].dmg === LZ_SLUG_DMG, 'heavy slug damage is ' + LZ_SLUG_DMG,
          'got ' + slugs[0].dmg);
      add(slugs[0].vy < 0, 'travelling up', 'vy=' + slugs[0].vy);
    }

    // ---- CADENCE ----
    pBullets.length = 0;
    pShoot();
    add(pBullets.filter(b => b.kind === 'lzslug').length === 0,
        'the cooldown holds the next volley', 'got ' + pBullets.length);

    // one-or-two-shot fodder, which is the brief the 7 dmg was measured for
    enemies.length = 0;
    spawnEnemy('drone', player.x, player.y - 60, {});
    const e = enemies[0];
    if (e) {
      const hp0 = e.hp;
      add(Math.ceil(hp0 / LZ_SLUG_DMG) <= 2,
          'stage-1 fodder dies in one or two slugs',
          'hp ' + hp0 + ' / ' + LZ_SLUG_DMG + ' = ' + Math.ceil(hp0 / LZ_SLUG_DMG) + ' shots');
    }
  } catch (e) { R.err = String(e && e.message || e); }
  return R;
}
"""


def main():
    from playwright.sync_api import sync_playwright
    port, stop = serve(GAME)
    url = 'http://127.0.0.1:%d/index.html' % port
    errs, results = [], []
    with sync_playwright() as p:
        b = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
        pg = b.new_page(viewport={'width': 1100, 'height': 1200}, device_scale_factor=1)
        pg.on('pageerror', lambda e: errs.append(str(e)[:200]))
        pg.goto(url, wait_until='load', timeout=60000)
        pg.wait_for_function("() => typeof ASSETS!=='undefined' && typeof pShoot==='function'",
                             timeout=45000)
        pg.wait_for_function("() => (window.__bofFrames|0) > 4", timeout=45000)

        dk = pg.evaluate(DECKER)
        # XART.rdy is false on its FIRST call — poll rather than one-shot
        keys = dk.get('artKeys') or []
        if keys:
            try:
                pg.wait_for_function("(ks) => ks.every(k => XART.rdy(k))", arg=keys, timeout=20000)
                dk['checks'].append({'ok': True, 'label': 'all 7 angled pellet plates resolve',
                                     'detail': ', '.join(keys)})
            except Exception:
                missing = pg.evaluate("(ks) => ks.filter(k => !XART.rdy(k))", keys)
                dk['checks'].append({'ok': False, 'label': 'all 7 angled pellet plates resolve',
                                     'detail': 'missing: ' + ', '.join(missing)})
        results.append(dk)
        results.append(pg.evaluate(LIZZIE))
        b.close()
    stop()

    bad = 0
    for R in results:
        print('\n=== %s ===' % R.get('name'))
        if R.get('err'):
            print('  THREW: %s' % R['err']); bad += 1; continue
        for c in R.get('checks', []):
            mark = 'ok  ' if c['ok'] else 'FAIL'
            print('  %s %s%s' % (mark, c['label'], ('   [' + c['detail'] + ']') if c['detail'] else ''))
            if not c['ok']:
                bad += 1
    if errs:
        print('\npage errors:')
        for e in errs[:5]:
            print('   ', e)
    print('\n%s' % ('ALL WEAPON CHECKS PASSED' if bad == 0 else '%d CHECK(S) FAILED' % bad))
    sys.exit(0 if bad == 0 else 1)


if __name__ == '__main__':
    main()
