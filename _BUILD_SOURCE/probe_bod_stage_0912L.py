#!/usr/bin/env python3
"""
probe_bod_stage_0912L.py - THE STAGE TAB, DRIVEN LIKE A USER.

    python3 _BUILD_SOURCE/probe_bod_stage_0912L.py --out /tmp/bodstage

Mike's Bullets of Debug brief opens with "level backgrounds, waves". Both are reachable; only one
of them is EDITABLE, and this asserts the panel is honest about which.

⚠ THE LOAD-BEARING ASSERTION IS THAT READING THE PLAN LEAVES NOTHING BEHIND. A wave is a FUNCTION
that spawns, so the only way to know what it contains is to run it - and running 28 of them while
the user is looking at a different stage would leave that stage's units standing in this one, and
move `run.stage` out from under everything else. The dry run saves and restores; this measures it.
"""
import os, sys, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shoot


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--out', default='/tmp/bodstage'); a = ap.parse_args()
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

        pg.goto(f'http://127.0.0.1:{port}/bulletsofdebug.html', wait_until='load', timeout=60000)
        pg.wait_for_function("() => window.BOD && window.BOD.api() && window.BOD.api().ready", timeout=90000)
        pg.evaluate("() => window.BOD.labOpen()")
        pg.wait_for_function("() => window.BOD.api().snapshot().lab", timeout=60000)
        ok(True, 'the editor boots with a stage open')

        pg.evaluate("() => window.BOD.selectTab('stage')")
        pg.wait_for_timeout(400)
        built = pg.evaluate("""() => ({
            stages: document.querySelector('#s-stage') ? document.querySelector('#s-stage').options.length : 0,
            secs: [...document.querySelectorAll('#insp .sec')].map(s=>s.dataset.sec),
            ai: document.querySelectorAll('#insp input[data-ai]').length,
            bgRows: document.querySelectorAll('#insp .sec[data-sec=sb] .f').length
        })""")
        ok(built['stages'] == 9, 'the stage picker lists all nine (%d)' % built['stages'])
        ok(all(k in built['secs'] for k in ('sg', 'sb', 'ss', 'sa', 'sw')),
           'stage / background / scroll / AI / waves are all present: %s' % built['secs'])
        ok(built['ai'] >= 5, 'the AI profile exposes its %d live fields' % built['ai'])
        ok(built['bgRows'] >= 5, 'the background is shown (%d fields)' % built['bgRows'])

        # ---- the background must be READ-ONLY and say so ----
        ro = pg.evaluate("""() => {
            const sec=document.querySelector('#insp .sec[data-sec=sb]');
            return {inputs: sec.querySelectorAll('input,select').length,
                    warns: /READ ONLY/.test(sec.textContent)}; }""")
        ok(ro['inputs'] == 0 and ro['warns'],
           'and it is read-only with the reason attached (%d inputs) - _levelCfg returns a fresh '
           'literal, so editable-looking fields there would be a placebo' % ro['inputs'])

        # ---- the AI profile IS live ----
        ai = pg.evaluate("""() => { const d=window.BOD.api();
            const before=d.aiProfile(1).cap;
            const r=document.querySelector('#insp input[data-ai=cap]');
            r.value=17; r.dispatchEvent(new Event('input',{bubbles:true}));
            return {before:before, after:d.aiProfile(1).cap}; }""")
        ok(ai['after'] == 17, 'the AI profile writes straight to the live table: cap %s -> %s '
                              '(read every frame by the wave pump)' % (ai['before'], ai['after']))

        # ---- READ THE PLAN, and leave nothing behind ----
        state = pg.evaluate("""() => { const W=document.querySelector('#host').contentWindow;
            return {stage:W.run.stage, enemies:window.BOD.api().enemies.length}; }""")
        pg.evaluate("""() => { const s=document.querySelector('#s-stage'); s.value='6';
            s.dispatchEvent(new Event('change',{bubbles:true})); }""")
        pg.wait_for_timeout(250)
        pg.evaluate("() => document.querySelector('#s-plan').click()")
        pg.wait_for_timeout(900)
        plan = pg.evaluate("""() => { const W=document.querySelector('#host').contentWindow;
            const rows=document.querySelectorAll('#insp .wv');
            return {rows:rows.length,
                    stageAfter:W.run.stage,
                    enemiesAfter:window.BOD.api().enemies.length,
                    txt:[...rows].slice(0,3).map(e=>e.textContent.trim())}; }""")
        ok(plan['rows'] >= 20, 'reading the plan dry-runs every wave and lists them (%d waves): %s'
           % (plan['rows'], plan['txt'][:2]))
        ok(plan['stageAfter'] == state['stage'] and plan['enemiesAfter'] == state['enemies'],
           'AND IT LEAVES NOTHING BEHIND - run.stage %s->%s, field %s->%s. A wave is a function '
           'that spawns, so reading 28 of them while the user looks at another stage would strand '
           'that stage units here' % (state['stage'], plan['stageAfter'],
                                      state['enemies'], plan['enemiesAfter']))

        # ---- the L6 fleet shows up in stage 6's plan, which is the 0912d fix, seen from the editor
        l6 = pg.evaluate("""() => { const p=window.BOD.api().stagePlan(6);
            const t={}; p.forEach(w=>(w.types||[]).forEach(k=>t[k]=1));
            return Object.keys(t).filter(k=>/^l6v_/.test(k)); }""")
        ok(len(l6) >= 6, 'and the L6 fleet is visible in stage 6 from the editor (%d types: %s) - '
                         'the config block that fields them was unreachable until 0912d'
           % (len(l6), sorted(l6)[:4]))

        # ---- clicking a wave fires it ----
        fired = pg.evaluate("""() => { const d=window.BOD.api(); d.clear();
            const n0=d.enemies.length;
            document.querySelector('#insp .wv').click();
            return {added:d.enemies.length-n0}; }""")
        ok(fired['added'] > 0, 'clicking a wave row fires that wave for real (%d spawned)' % fired['added'])

        # ---- the scroll scrubs ----
        scrub = pg.evaluate("""() => { const d=window.BOD.api();
            const r=document.querySelector('#s-scroll');
            r.value=0.5; r.dispatchEvent(new Event('input',{bubbles:true}));
            return d.scroll; }""")
        ok(scrub and scrub['range'] > 100 and scrub['at'] > scrub['range'] * 0.3,
           'the scroll scrubs the level plate: %s of %s' % (scrub['at'], scrub['range']))

        pg.wait_for_timeout(400)
        pg.screenshot(path=os.path.join(a.out, '01_stage_tab.png'))
        b.close()
    stop()
    print('\n%d ok / %d fail' % (n_ok[0], len(fails)))
    for f in fails: print('  FAIL', f)
    if errs:
        print('page errors (%d):' % len(errs))
        for e in errs[:6]: print('   ', e)
    sys.exit(1 if fails or errs else 0)


if __name__ == '__main__':
    main()
