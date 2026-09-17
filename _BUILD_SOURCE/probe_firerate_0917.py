#!/usr/bin/env python3
"""
probe_firerate_0917.py - IS THE GUN TOO FAST, OR WAS THE CAMERA?

Mike, on the infusion reel: "the bullets are firing too fast."

The reel's autopilot did `player.fireCd = 0; pShoot();` every frame - it called the muzzle
DIRECTLY and zeroed the cooldown, so it fired once per frame at 60 Hz whatever the weapon's
cadence says. The shipping game fires through `updatePlay`'s trigger block, which sets
`player.fireCd = _weaponCadence() * (1 - PILOTMOD.fire)` and will not fire again until it drains.

So this measures the SAME weapon two ways over the same simulated seconds:

  HELD   - BOSSMODE.hold(<fire bind>, true), i.e. the real input path, cadence and all
  FORCED - what the reel did

and reports rounds per second for each. If HELD matches the table and FORCED is ~60, the reel was
lying about the gun and the fix is in the harness, not in the balance.

⚠ ROUNDS ARE COUNTED AT THE MUZZLE, NOT IN pBullets. A bullet pool is drained by culls and by
pierce/expiry every frame, so its length measures what is ALIVE, never what was fired. `pShoot` is
wrapped and the pushes it makes are counted.
"""
import os, sys, json
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.join(ROOT, '_BUILD_SOURCE'))
import shoot as sh
from playwright.sync_api import sync_playwright

N = {'ok': 0}; FAILS = []
def ok(c, m):
    if c: N['ok'] += 1; print('  ok   ' + m)
    else: FAILS.append(m); print('  FAIL ' + m)

# (slot, name, level, counts?) - `counts` is whether the weapon PUSHES INTO pBullets once per
# beat, which is the only thing a rounds/sec counter can see. Two do not and are reported
# rather than asserted on: the LASER holds ONE reused 'beam' entry for as long as it burns,
# and the LIGHTNING ORB fires through `yuriLightningOrbFire` into its own pool. Neither is a
# defect - measuring them with this metric is (CLAUDE.md: a quantity that is consumed cannot
# be measured after it is gone, and its sibling: a pool you do not push into cannot be counted).
WEAPONS = [(0, 'MACHINE GUN', 2, True), (1, 'SPREAD', 2, True),
           (3, 'LASER', 2, False), (7, 'CHAINGUN', 2, True), (8, 'LIGHTNING ORB', 2, False)]
SECONDS = 4.0

COUNT = """() => {
  window.__fired = 0;
  const f = pShoot;
  pShoot = function(){ const n0 = pBullets.length; const r = f.apply(this, arguments);
                       window.__fired += Math.max(0, pBullets.length - n0); return r; };
}"""

def main():
    port, stop = sh.serve(sh.GAME)
    rows = []
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        pg = br.new_page(viewport={'width': 1000, 'height': 1200})
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=60000)
        pg.wait_for_function("() => typeof setState==='function' && typeof _weaponCadence==='function'", timeout=60000)
        pg.wait_for_function("() => (window.__bofFrames|0) > 4", timeout=60000)
        pg.evaluate(sh.TRAP_RAF)
        pg.evaluate(sh.SETUP, {'state': 'PLAY', 'stage': 1, 'pilot': 'cole'})
        pg.evaluate("() => { window.playerHit=function(){}; run.lives=9; enemies.length=0; }")
        for _ in range(4):
            pg.evaluate(sh.STEP, [8]); pg.wait_for_timeout(300)
        pg.evaluate(COUNT)

        fire_key = pg.evaluate("() => { const b=BOSSMODE.binds(); return (b&&b.fire&&b.fire[0])||'j'; }")
        print('  fire bind:', fire_key)

        for w, name, lv, counts in WEAPONS:
            pg.evaluate("([w,lv]) => { run.weapon=w; run.wlevels[w]=lv; run.wlevel=lv;"
                        " player.fireCd=0; run._chainRev=0; for(const b of pBullets) b.dead=true; pBullets.length=0; }", [w, lv])
            # the table's own number, before the pilot's fire-rate stat
            table_cd = pg.evaluate("() => _weaponCadence()")

            # --- HELD: the real input path -----------------------------------------
            pg.evaluate("() => { window.__step = %s; }" % sh.STEP)
            # record the cooldown the ENGINE writes on each firing frame - the real interval,
            # pilot stat included, with nothing recomputed probe-side (CLAUDE.md: a probe that
            # recomputes the thing under test cannot find the bug)
            pg.evaluate("([k]) => { window.__fired=0; window.__cds=[];"
                        " const f=pShoot; pShoot=function(){ const r=f.apply(this,arguments);"
                        "   window.__cds.push(player.fireCd); return r; };"
                        " BOSSMODE.hold(k,true); }", [fire_key])
            pg.evaluate("(n) => { for(let i=0;i<n;i++) window.__step(1); }", int(SECONDS * 60))
            held = pg.evaluate("() => window.__fired|0")
            cds = pg.evaluate("() => (window.__cds||[]).filter(v=>v>0)")
            pg.evaluate("([k]) => { BOSSMODE.hold(k,false); }", [fire_key])
            real_cd = (sum(cds) / len(cds)) if cds else None

            # --- FORCED: what the reel's autopilot did ------------------------------
            pg.evaluate("() => { window.__fired=0; for(const b of pBullets) b.dead=true; pBullets.length=0; }")
            pg.evaluate("(n) => { for(let i=0;i<n;i++){ player.fireCd=0; pShoot(); window.__step(1); } }", int(SECONDS * 60))
            forced = pg.evaluate("() => window.__fired|0")

            # rounds/sec is what a player feels; a spread gun emits several rounds per BEAT, so
            # report the beats too - otherwise SPREAD looks five times faster than the MG
            beats = (1.0 / real_cd) if real_cd else 0.0
            # how many rounds ONE beat emits, read off the engine rather than assumed - the MG
            # fires _cl+1 pellets at level 2, so "rounds per second / 2" is wrong above level 1
            per_beat = pg.evaluate("() => { const n0=pBullets.length; const cd=player.fireCd;"
                                   " player.fireCd=0; pShoot(); player.fireCd=cd;"
                                   " return Math.max(0, pBullets.length-n0); }")
            rows.append({'w': w, 'name': name, 'counts': counts, 'rounds_per_beat': per_beat,
                         'table_cadence': round(table_cd, 4),
                         'engine_cadence': round(real_cd, 4) if real_cd else None,
                         'beats_per_sec': round(beats, 2),
                         'held_rounds_per_sec': round(held / SECONDS, 1),
                         'forced_rounds_per_sec': round(forced / SECONDS, 1)})
            print('  %-14s table %.3fs | engine %s -> %5.2f beats/s x %d rounds | HELD %6.1f rounds/s | FORCED %6.1f rounds/s%s'
                  % (name, table_cd, ('%.3fs' % real_cd) if real_cd else '  n/a ', beats, per_beat,
                     held / SECONDS, forced / SECONDS, '' if counts else '   (own pool - not countable)'))

        print('  errors:', len(errs))
        for e in errs[:4]: print('   !', e)

        mg = [r for r in rows if r['w'] == 0][0]
        shot = [r for r in rows if r['counts']]
        ok(mg['rounds_per_beat'] > 0 and
           abs(mg['beats_per_sec'] - mg['held_rounds_per_sec'] / mg['rounds_per_beat']) < 0.8,
           'HELD machine gun fires exactly ONE beat of %d pellets per engine cooldown (%.1f beats/s, %.1f rounds/s)'
           % (mg['rounds_per_beat'], mg['beats_per_sec'], mg['held_rounds_per_sec']))
        ok(mg['engine_cadence'] <= mg['table_cadence'] + 1e-6,
           "the engine's own cooldown never EXCEEDS the table (engine %.3fs vs table %.3fs; the pilot's"
           " fire-rate stat can only shorten it, and is 0 for this pilot in this harness)"
           % (mg['engine_cadence'], mg['table_cadence']))
        ok(mg['forced_rounds_per_sec'] > mg['held_rounds_per_sec'] * 4,
           'the reel autopilot fired %.0fx faster than the real trigger (%.1f vs %.1f rounds/s)'
           % (mg['forced_rounds_per_sec'] / max(1e-9, mg['held_rounds_per_sec']),
              mg['forced_rounds_per_sec'], mg['held_rounds_per_sec']))
        ok(all(r['held_rounds_per_sec'] < r['forced_rounds_per_sec'] for r in shot),
           'every ROUND-firing weapon is slower through the real trigger than through the forced one')
        ok(all(r['engine_cadence'] and r['engine_cadence'] > 1 / 30.0 for r in shot),
           'no weapon beats faster than 30 times a second through the real trigger')
        ok(len(errs) == 0, 'no page errors (%d)' % len(errs))
        br.close()
    stop()
    qa = os.path.join(ROOT, 'docs', 'qa', 'firerate_0917.json')
    os.makedirs(os.path.dirname(qa), exist_ok=True)
    json.dump({'seconds': SECONDS, 'rows': rows}, open(qa, 'w'), indent=2)
    print('  ->', qa)
    print('\n%d ok / %d fail' % (N['ok'], len(FAILS)))
    for f in FAILS: print('  FAIL', f)
    sys.exit(1 if FAILS else 0)

if __name__ == '__main__':
    main()
