#!/usr/bin/env python3
"""
probe_bod_editor_0912g.py - BULLETS OF DEBUG!, DRIVEN LIKE A USER.

    python3 _BUILD_SOURCE/probe_bod_editor_0912g.py --out /tmp/bodui

Real Chromium on bulletsofdebug.html: the pack loads, the roster fills from the engine, a unit is
picked and spawned into the lab, its stats are moved with the actual sliders, a pattern is fired off
it, the FOV overlay paints, and the layout keys work. Screens at every step.
"""
import os, sys, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shoot


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--out', default='/tmp/bodui'); a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    from playwright.sync_api import sync_playwright
    port, stop = shoot.serve(shoot.GAME); errs = []; fails = []; n_ok = [0]
    def ok(c, m):
        if c: n_ok[0] += 1; print('  ok  ', m)
        else: fails.append(m); print('  FAIL', m)
    with sync_playwright() as p:
        b = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
        pg = b.new_page(viewport={'width': 1600, 'height': 1000})
        pg.on('pageerror', lambda e: errs.append('pageerror: ' + str(e)[:220]))
        pg.on('console', lambda m: errs.append('console.error: ' + m.text[:200]) if m.type == 'error' else None)
        missing = []
        pg.on('response', lambda r: missing.append(r.url.split(f':{port}/')[-1]) if r.status == 404 else None)

        pg.goto(f'http://127.0.0.1:{port}/bulletsofdebug.html', wait_until='load', timeout=60000)
        pg.wait_for_function("() => window.BOD", timeout=30000)
        ok(True, 'the page boots and exposes window.BOD')

        # the pack: atlas-backed CSS rules must have real rects
        packed = pg.evaluate("""() => {
            const b=getComputedStyle(document.querySelector('.pb[data-btn=spawn]'));
            const i=getComputedStyle(document.querySelector('.ico[data-icon=enemy]'));
            return {btnW:parseInt(b.width), btnBg:b.backgroundImage.indexOf('buttons.png')>0,
                    icoW:parseInt(i.width), icoBg:i.backgroundImage.indexOf('icons.png')>0};
        }""")
        ok(packed['btnW'] > 40 and packed['btnBg'], 'the generated button rules point at the pack (%dpx wide)' % packed['btnW'])
        ok(packed['icoW'] > 10 and packed['icoBg'], 'and so do the icon rules (%dpx)' % packed['icoW'])

        # the engine
        pg.wait_for_function("() => window.BOD.api() && window.BOD.api().ready", timeout=90000)
        ok(pg.evaluate("() => document.querySelector('#host-led').classList.contains('on')"),
           'the host LED turns green when BOFDEBUG is reachable')

        n = pg.evaluate("() => window.BOD.S.roster.length")
        ok(n > 150, 'the roster fills from the live engine (%d types)' % n)
        pg.wait_for_timeout(300)
        groups = pg.evaluate("() => document.querySelectorAll('#roster .rg').length")
        rows = pg.evaluate("() => document.querySelectorAll('#roster .ri').length")
        ok(groups >= 15 and rows == n, 'and renders grouped by table (%d tables, %d rows)' % (groups, rows))

        # the drawer
        pg.keyboard.press('l'); pg.wait_for_timeout(300)
        ok(pg.evaluate("() => document.body.classList.contains('drawer')"), 'L opens the roster drawer')
        pg.screenshot(path=os.path.join(a.out, '01_roster.png'))

        # filter, then pick a real unit
        pg.fill('#roster-filter', 's6')
        pg.wait_for_timeout(250)
        vis = pg.evaluate("() => document.querySelectorAll('#roster .ri').length")
        ok(0 < vis < n, 'the filter narrows the roster (%d of %d)' % (vis, n))
        pg.evaluate("""() => { const el=[...document.querySelectorAll('#roster .ri')]
            .find(e=>e.textContent.trim().startsWith('s6dart')); el.click(); }""")
        pg.wait_for_timeout(300)
        ok(pg.evaluate("() => window.BOD.S.sel && window.BOD.S.sel.type==='s6dart'"), 'picking a unit selects it')
        ok(not pg.evaluate("() => document.body.classList.contains('drawer')"),
           'and closes the drawer, the way the boss list does')

        # spawn into the lab
        pg.keyboard.press('s')
        pg.wait_for_function("() => window.BOD.unit()", timeout=30000)
        u = pg.evaluate("() => { const u=window.BOD.unit(); return {type:u.type, hp:u.hp, w:u.w, pattern:u.pattern}; }")
        ok(u['type'] == 's6dart', 'S spawns it into the lab: %s' % u)
        pg.wait_for_timeout(900)
        ok(pg.evaluate("() => window.BOD.api().snapshot().enemies===1"),
           'and the lab stays quiet - exactly one unit, no waves arriving')
        pg.screenshot(path=os.path.join(a.out, '02_spawned.png'))

        # the inspector sliders actually move the live unit
        moved = pg.evaluate("""() => {
            const before=window.BOD.unit().hp;
            const r=document.querySelector('#insp input[type=range][data-k=hp]');
            r.value=222; r.dispatchEvent(new Event('input',{bubbles:true}));
            return {before:before, after:window.BOD.unit().hp,
                    shown:document.querySelector('#insp [data-v=hp]').textContent};
        }""")
        ok(moved['after'] == 222, 'the HP slider writes straight to the live unit: %s -> %s (readout %s)'
           % (moved['before'], moved['after'], moved['shown']))
        wm = pg.evaluate("""() => { const r=document.querySelector('#insp input[type=range][data-k=w]');
            r.value=120; r.dispatchEvent(new Event('input',{bubbles:true})); return window.BOD.unit().w; }""")
        ok(wm == 120, 'and so does WIDTH, which is hull and draw at once (%s)' % wm)

        # movement pattern
        pat = pg.evaluate("""() => { const s=document.querySelector('#i-pattern');
            const opts=[...s.options].map(o=>o.value); s.value=opts.includes('sine')?'sine':opts[1];
            s.dispatchEvent(new Event('change',{bubbles:true}));
            return {n:opts.length, now:window.BOD.unit().pattern}; }""")
        ok(pat['n'] >= 25 and pat['now'], 'the movement pattern can be swapped live (%d options, now %s)' % (pat['n'], pat['now']))

        # shadow opt-in
        shd = pg.evaluate("""() => { const c=document.querySelector('#i-shadow');
            c.checked=true; c.dispatchEvent(new Event('change',{bubbles:true}));
            return !!window.BOD.unit()._bodShadow; }""")
        ok(shd, 'the per-unit shadow can be switched on from the inspector')

        # fire a pattern off it
        fired = pg.evaluate("""() => { const d=window.BOD.api(); const n0=d.eBullets.length;
            window.BOD.fireOnce(); return d.eBullets.length-n0; }""")
        ok(fired > 0, 'FIRE ONCE emits a boss-grade pattern off the ordinary enemy (%d rounds)' % fired)
        pg.wait_for_timeout(500)
        pg.screenshot(path=os.path.join(a.out, '03_firing.png'))

        # the FOV overlay paints
        ink = pg.evaluate("""() => { const c=document.querySelector('#overlay');
            if(!c.width) return 0;
            const d=c.getContext('2d').getImageData(0,0,c.width,c.height).data;
            let n=0; for(let i=3;i<d.length;i+=16) if(d[i]>8) n++; return n; }""")
        ok(ink > 300, 'the FOV cone and anchors paint over the live field (%d px)' % ink)

        # layout keys
        pg.keyboard.press('Tab'); pg.wait_for_timeout(300)
        ok(pg.evaluate("() => document.body.classList.contains('nodock')"), 'Tab folds the inspector dock')
        pg.keyboard.press('t'); pg.wait_for_timeout(300)
        ok(pg.evaluate("() => document.body.classList.contains('theater')"), 'T goes theater')
        pg.screenshot(path=os.path.join(a.out, '04_theater.png'))
        pg.keyboard.press('t'); pg.keyboard.press('Tab'); pg.wait_for_timeout(300)

        # clear
        pg.keyboard.press('c'); pg.wait_for_timeout(400)
        ok(pg.evaluate("() => window.BOD.api().snapshot().enemies===0"), 'C clears the field')
        pg.screenshot(path=os.path.join(a.out, '05_final.png'))
        b.close()
    stop()
    if missing:
        from collections import Counter
        print('404s:'); [print('   %3d  %s' % (n, u)) for u, n in Counter(missing).most_common(8)]
    print('\n%d ok / %d fail' % (n_ok[0], len(fails)))
    for f in fails: print('  FAIL', f)
    if errs:
        print('page errors (%d):' % len(errs))
        for e in errs[:8]: print('   ', e)
    sys.exit(1 if fails or errs else 0)


if __name__ == '__main__':
    main()
