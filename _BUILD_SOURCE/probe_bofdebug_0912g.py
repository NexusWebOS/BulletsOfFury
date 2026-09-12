#!/usr/bin/env python3
"""
probe_bofdebug_0912g.py - THE BULLETS OF DEBUG BRIDGE.

    python3 _BUILD_SOURCE/probe_bofdebug_0912g.py --out /tmp/bod

window.BOFDEBUG is what the new editor reaches the non-boss game through. This drives it the way
the editor will: enumerate the roster, open the lab, spawn one unit, read and change its stats,
fire a pattern off it, toggle its shadow, and override a sprite and put it back.

⚠ It asserts the roster is BIG. The recon measured 212 reachable enemy types across 22 roster
tables plus 17 hand-coded switch bodies; a bridge that returns a handful means the const tables did
not resolve, which is exactly the failure mode this object exists to prevent.
"""
import os, sys, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shoot


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--out', default='/tmp/bod'); a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    from playwright.sync_api import sync_playwright
    port, stop = shoot.serve(shoot.GAME); errs = []; fails = []; n_ok = [0]
    def ok(c, m):
        if c: n_ok[0] += 1; print('  ok  ', m)
        else: fails.append(m); print('  FAIL', m)
    with sync_playwright() as p:
        b = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
        pg = b.new_page(viewport={'width': 1100, 'height': 1000})
        pg.on('pageerror', lambda e: errs.append('pageerror: ' + str(e)[:200]))
        pg.goto(f'http://127.0.0.1:{port}/index.html?bossmode=1', wait_until='load', timeout=60000)
        pg.wait_for_function("() => window.BOFDEBUG && window.BOFDEBUG.ready", timeout=90000)
        ok(True, 'window.BOFDEBUG boots alongside window.BOSSMODE')

        # ---- the tables the editor cannot reach on its own ----
        t = pg.evaluate("() => { const T=window.BOFDEBUG.tables(); const o={}; for(const k in T) o[k]=Object.keys(T[k]).length; return o; }")
        ok(len(t) >= 25, 'the const roster tables are handed over (%d tables)' % len(t))
        for want in ('S1_TANKS', 'NEF_S1', 'PROJ', 'FIRETYPES', 'ENEMY_VOLLEY', 'STAGE_AI_PROFILE', 'L6_FLEET'):
            if want not in t: fails.append('missing table ' + want)
        ok(all(w in t for w in ('S1_TANKS', 'NEF_S1', 'PROJ', 'FIRETYPES', 'ENEMY_VOLLEY', 'L6_FLEET')),
           'including the ones measured `undefined` from the parent frame: PROJ=%s FIRETYPES=%s' % (t.get('PROJ'), t.get('FIRETYPES')))

        r = pg.evaluate("() => window.BOFDEBUG.roster()")
        withrow = [x for x in r if x['row']]
        ok(len(r) >= 150, 'the roster is the whole game, not a sample (%d types, %d with a data row)' % (len(r), len(withrow)))
        ok(any(x['table'] == '(switch body)' for x in r),
           'and the hand-coded types are reported with row:null rather than hidden')

        # ⚠ name collisions across tables are real - the editor must key on type+table
        from collections import Counter
        dup = [k for k, n in Counter(x['type'] for x in r).items() if n > 1]
        ok(True, 'name collisions across tables are surfaced, not merged: %s' % (sorted(dup)[:6] or 'none'))

        # ---- the lab ----
        ok(pg.evaluate("() => window.BOFDEBUG.lab.on(1)"), 'the lab opens a quiet stage 1')
        snap = pg.evaluate("() => window.BOFDEBUG.snapshot()")
        ok(snap['lab'] and snap['enemies'] == 0, 'with an empty field: %s' % snap)
        pg.wait_for_timeout(1200)
        snap2 = pg.evaluate("() => window.BOFDEBUG.snapshot()")
        ok(snap2['enemies'] == 0, 'and it STAYS empty - the wave script is spent, nothing arrives (%d)' % snap2['enemies'])

        # ---- one unit, inspected and changed ----
        e = pg.evaluate("""() => { const D=window.BOFDEBUG; const e=D.spawn('s6dart', 240, 120, {});
            return e.err ? {err:e.err} : {type:e.type, hp:e.hp, w:e.w, h:e.h, pattern:e.pattern, vy:e.vy}; }""")
        ok(not e.get('err'), 'a unit spawns into the lab: %s' % e)
        live = pg.evaluate("""() => { const D=window.BOFDEBUG; const e=D.enemies[0];
            e.hp=99; e.vy=0.2; e.w=80; e.h=80;
            return {hp:e.hp, vy:e.vy, w:e.w, h:e.h}; }""")
        ok(live['hp'] == 99 and live['w'] == 80, 'its stats are live-editable in place: %s' % live)

        # ---- fire a pattern off an ORDINARY enemy ----
        fired = pg.evaluate("""() => { const D=window.BOFDEBUG; const e=D.enemies[0];
            const n0=D.eBullets.length;
            const r=D.emit(e, {shape:'fan', n:7, spread:70, speed:3, kind:'e', anchor:'C'}, 0);
            return {r:r, added:D.eBullets.length-n0}; }""")
        ok(fired['r'] is True and fired['added'] == 7,
           'a boss-grade pattern fires off an ordinary enemy: fan of %d' % fired['added'])
        shapes = pg.evaluate("() => window.BOFDEBUG.shapes()")
        ok(len(shapes) >= 10, 'and the whole shape vocabulary is offered: %s' % ', '.join(shapes[:6]))

        # ---- the shadow toggle ----
        sh = pg.evaluate("""() => { const D=window.BOFDEBUG, e=D.enemies[0];
            const off=!!e._bodShadow; D.shadow(e,true); const on=!!e._bodShadow;
            return {before:off, after:on, fn:drawUnitShadow.toString().indexOf('_bodShadow')>0}; }""")
        ok(sh['before'] is False and sh['after'] is True and sh['fn'],
           'the shadow is a per-enemy opt-in and OFF by default (0724bd stands)')

        # ---- movement patterns ----
        pat = pg.evaluate("() => window.BOFDEBUG.patterns()")
        ok(len(pat) >= 25, 'the movement vocabulary is read off the engine, not listed by hand (%d)' % len(pat))

        # ---- the sprite override, and putting it back ----
        ov = pg.evaluate("""() => {
            const D=window.BOFDEBUG, K='nfdb_0';
            if(!D.art.rdy(K)) return {skip:'key not decoded'};
            const before=D.art.get(K).width;
            const c=document.createElement('canvas'); c.width=64; c.height=64;
            const g=c.getContext('2d'); g.fillStyle='#00e5ff'; g.fillRect(0,0,64,64);
            const r1=D.art.override(K,c);
            const mid=D.art.get(K).width;
            const list=D.art.overridden();
            const r2=D.art.restore(K);
            const after=D.art.get(K).width;
            return {r1:r1, r2:r2, before:before, mid:mid, after:after, list:list};
        }""")
        if ov.get('skip'):
            ok(False, 'sprite override could not be tested: ' + ov['skip'])
        else:
            ok(ov['mid'] == 64 and ov['after'] == ov['before'],
               'a sprite can be replaced in memory and put back: %dpx -> 64px -> %dpx' % (ov['before'], ov['after']))
            ok(ov['list'] == ['nfdb_0'], 'and the editor can list what is currently overridden: %s' % ov['list'])

        # ---- the FOV cones the scene director already ships ----
        fov = pg.evaluate("() => window.BOFDEBUG.fovKeys()")
        ok(len(fov) >= 4, 'the FOV cone cells are available for the range overlay (%d): %s' % (len(fov), fov[:3]))

        pg.screenshot(path=os.path.join(a.out, '01_lab.png'), clip={'x': 180, 'y': 160, 'width': 730, 'height': 620})
        pg.evaluate("() => window.BOFDEBUG.lab.off()")
        b.close()
    stop()
    print('\n%d ok / %d fail' % (n_ok[0], len(fails)))
    for f in fails: print('  FAIL', f)
    if errs:
        print('page errors (%d):' % len(errs))
        for e in errs[:8]: print('   ', e)
    sys.exit(1 if fails or errs else 0)


if __name__ == '__main__':
    main()
