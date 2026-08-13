#!/usr/bin/env python3
"""
probe_volley.py — did the positional volley layer actually reach the game, and is it downward?

    python3 _BUILD_SOURCE/probe_volley.py

Mike: "Make the enemies shoot more projectiles and give our shmup patterns where I have to keep
myself at certain spots to survive."

Four questions, in the order they can invalidate each other:

  1. IS THE TABLE EVEN IN SCOPE? `spawnEnemy`'s `if(base.art===undefined){` is never closed, so
     declarations below it are function-scoped and read as undefined from outside. That trap made
     DEAD_SUBBOSS inert for two drops while its commit said the unit was retired, and ARSENAL_DRONES
     before it. ENEMY_VOLLEY sits below spawnEnemy in the file, so this is asked FIRST and at
     RUNTIME — `typeof` at global scope, the same check that caught DEAD_SUBBOSS.

  2. DO VOLLEYS FIRE? enemyVolley is wrapped and counted, per pattern.

  3. IS EVERYTHING STILL DOWNWARD? "theres sideway bullets going across the screen instead of
     machine gun like attacks" is a complaint this file already fixed once (0801kn). Any enemy
     bullet with |vx| >= vy is travelling more sideways than down and is a regression. Counted
     across every stage, and reported per kind so a pre-existing offender is not blamed on this.

  4. HOW MUCH MORE IS ON SCREEN? Bullets born per 12s of real play, per stage.
"""
import http.server, socketserver, threading, os, functools, json, sys

GAME = r'C:/Users/Mdogg/Desktop/BOF-CODE/BulletsOfFury'
OUT = os.path.join(GAME, 'docs', 'proofs')


def serve(d):
    h = functools.partial(http.server.SimpleHTTPRequestHandler, directory=d)
    h.log_message = lambda *a, **k: None
    s = socketserver.TCPServer(("127.0.0.1", 0), h)
    threading.Thread(target=s.serve_forever, daemon=True).start()
    return s.server_address[1]


SCOPE = r"""
() => ({
  tableType: typeof ENEMY_VOLLEY,
  fnType:    typeof enemyVolley,
  keys:      (typeof ENEMY_VOLLEY==='object' && ENEMY_VOLLEY) ? Object.keys(ENEMY_VOLLEY) : null,
  /* the fire dispatch lives in updatePlay. There is no updateEnemies function at all, and
     checking for one reported the layer as never called while it was correctly wired. */
  hooked:    typeof updatePlay==='function'
               ? /enemyVolley\(/.test(updatePlay.toString()) : 'no updatePlay'
})
"""

RUN = r"""
([stage, seconds, volleyOn]) => {
  ASSETS.ready=true; run.pilot='cole'; run.mode='arcade';
  beginStage(stage); setState(GS.PLAY);
  player.invuln = 1e9;                    // survive long enough to measure
  eBullets.length = 0;

  // count volleys by pattern, and DISABLE the layer entirely for the baseline run
  const realVolley = window.__realVolley || enemyVolley;
  window.__realVolley = realVolley;
  const byPat = {};
  let volleyShots = 0, volleySideways = 0;
  enemyVolley = function(e){
    if(!volleyOn) return false;
    const V = ENEMY_VOLLEY[e && e.type];
    const before = eBullets.length;
    const r = realVolley(e);
    if(r && V){
      const made = eBullets.slice(before);
      byPat[V.pat] = (byPat[V.pat]||0) + made.length;
      /* ⚠ ATTRIBUTED, NOT DIFFED. Comparing total sideways counts between a baseline run and a
         volley run measures WAVE RANDOMNESS, not this layer: the two runs spawn different
         enemies, and the first cut of this probe duly reported "2 new sideways bullets" that
         were all kind 'dart' — a kind no volley fires — while stage 6 went DOWN by 8. These are
         the rounds this layer actually created. */
      for(const b of made){
        volleyShots++;
        if(Math.abs(b.vx||0) >= Math.max(0.001, b.vy||0)) volleySideways++;
      }
    }
    return r;
  };

  /* ⚠ TWO WRONG INSTRUMENTS BEFORE THIS ONE, and both reported a confident zero.

     A WeakSet re-scanned over 1,800 frames crashed the renderer outright ("Target crashed").
     Wrapping eBullets.push then reported 0 bullets on EVERY stage including the baseline, which
     enemies obviously do not manage - eShoot does call eBullets.push, but the pools in this file
     are REASSIGNED rather than mutated (`enemies = enemies.filter(...)` and the same for bullets),
     so the wrapper was thrown away on the first cull and the native push took over silently.

     Tagging each bullet the first time it is seen survives reassignment, because the tag rides on
     the bullet rather than on the array. */
  let born = 0, sideways = 0;
  const sideKinds = {};
  const t0 = performance.now();
  const frames = Math.round(seconds * 60);
  for (let i=0; i<frames; i++){
    loop(t0 + i*16.7);
    for (const b of eBullets){
      if (b.__vseen) continue;
      b.__vseen = 1; born++;
      const vx = Math.abs(b.vx||0), vy = (b.vy||0);
      if (vx >= Math.max(0.001, vy)) { sideways++; sideKinds[b.kind||'?'] = (sideKinds[b.kind||'?']||0)+1; }
    }
  }
  enemyVolley = realVolley;
  return {stage, born, sideways, sideKinds, byPat, volleyShots, volleySideways};
}
"""


def main():
    from playwright.sync_api import sync_playwright
    os.makedirs(OUT, exist_ok=True)
    port = serve(GAME)
    url = 'http://127.0.0.1:%d/index.html' % port
    stages = [1, 2, 3, 4, 6, 7]
    rows = []
    with sync_playwright() as p:
        b = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
        pg = b.new_page(viewport={'width': 620, 'height': 900}, device_scale_factor=1)
        pg.goto(url, wait_until='load', timeout=60000)
        pg.wait_for_function("()=>typeof setState==='function'", timeout=45000)
        pg.wait_for_function("()=>(window.__bofFrames|0)>4", timeout=45000)

        sc = pg.evaluate(SCOPE)
        print('SCOPE CHECK (the spawnEnemy swallow trap)')
        print('   typeof ENEMY_VOLLEY : %s' % sc['tableType'])
        print('   typeof enemyVolley  : %s' % sc['fnType'])
        print('   hooked into updateEnemies: %s' % sc['hooked'])
        print('   types covered       : %s' % (', '.join(sc['keys']) if sc['keys'] else 'NONE'))
        if sc['tableType'] != 'object' or sc['fnType'] != 'function':
            print('\n*** THE LAYER IS OUT OF SCOPE. It is function-scoped inside spawnEnemy and the game '
                  'never sees it. Hoist it. ***')
            b.close(); sys.exit(1)
        if sc['hooked'] is not True:
            print('\n*** DECLARED BUT NEVER CALLED from updatePlay. ***')
            b.close(); sys.exit(1)
        print('   -> in scope and called\n')

        b.close()

        # one browser per stage: six stage masters plus twelve 12s runs exhausted a shared one
        for st in stages:
            sb = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
            sp = sb.new_page(viewport={'width': 620, 'height': 900}, device_scale_factor=1)
            try:
                sp.goto(url, wait_until='load', timeout=60000)
                sp.wait_for_function("()=>typeof setState==='function'", timeout=45000)
                sp.wait_for_function("()=>(window.__bofFrames|0)>4", timeout=45000)
                off = sp.evaluate(RUN, [st, 12, False])
                on = sp.evaluate(RUN, [st, 12, True])
                rows.append((st, off, on))
                print('   stage %d  baseline %4d bullets  ->  with volleys %4d  (%+d, %+.0f%%)'
                      % (st, off['born'], on['born'], on['born'] - off['born'],
                         100.0 * (on['born'] - off['born']) / max(1, off['born'])))
            except Exception as ex:
                print('   stage %d  FAILED %s' % (st, str(ex)[:70]))
            finally:
                sp.close(); sb.close()

    print('\nPER-PATTERN BULLETS (12s per stage, volleys on)')
    agg = {}
    for st, off, on in rows:
        for k, v in (on['byPat'] or {}).items():
            agg[k] = agg.get(k, 0) + v
    for k in sorted(agg, key=lambda z: -agg[z]):
        print('   %-9s %5d' % (k, agg[k]))
    if not agg:
        print('   NONE — the layer is in scope but never fired. Do the covered types spawn on these stages?')

    print('\nSIDEWAYS CHECK — rounds THIS LAYER created (|vx| >= vy is more across than down)')
    shots = sum(on['volleyShots'] for _, _, on in rows)
    side = sum(on['volleySideways'] for _, _, on in rows)
    for st, off, on in rows:
        print('   stage %d  volley rounds %4d   sideways %d' % (st, on['volleyShots'], on['volleySideways']))
    print('   TOTAL     volley rounds %4d   sideways %d' % (shots, side))
    print('\n   (whole-run totals are NOT a before/after: the two runs spawn different waves.')
    print('    stage 4 read -56% on one pass purely from that. byPat and the numbers above are')
    print('    attributed to the layer and are the ones to trust.)')
    print('\nVERDICT:', ('%d volley rounds, none sideways' % shots) if side == 0 and shots
          else ('*** %d of %d volley rounds travel sideways ***' % (side, shots)) if shots
          else '*** THE LAYER FIRED NOTHING ***')
    json.dump([{'stage': r[0], 'off': r[1], 'on': r[2]} for r in rows],
              open(os.path.join(OUT, 'volley_0810u.json'), 'w'), indent=1)


if __name__ == '__main__':
    main()
