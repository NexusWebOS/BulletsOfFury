#!/usr/bin/env python3
"""
probe_bod_fire_0912h.py - THE FIRE TAB, DRIVEN LIKE A USER.

    python3 _BUILD_SOURCE/probe_bod_fire_0912h.py --out /tmp/bodfire

Bullets of Debug's FIRE tab exists because Mike asked for "projectiles ... muzzle flashes, firing
speed, damage or damage per second, projectile patterning ... anchor points". Seven subsystems were
read before a control was drawn, and the finding that shaped the tab is that a literal reading of
that list produces sliders that READ BACK THE VALUE YOU WROTE AND CHANGE NOTHING.

So this probe asserts two things, and the second matters more than the first:

  1. every control that IS shipped moves something measurable in the engine
  2. the controls that CANNOT work are named rather than shipped

⚠ The pattern assertions are behavioural, not counts of buttons. A `fan` must produce n distinct
headings; a `spiral` burst must produce headings that ROTATE (a one-shot spiral is a single round by
design - that is what made the first FIRE panel look broken); a `wall` with a gap must leave a gap.
"""
import os, sys, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shoot


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--out', default='/tmp/bodfire'); a = ap.parse_args()
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
        ok(True, 'the editor boots and reaches the engine')

        # a live unit, through the editor's own path
        pg.evaluate("() => window.BOD.labOpen()")
        pg.wait_for_function("() => window.BOD.api().snapshot().lab", timeout=60000)
        pg.keyboard.press('l'); pg.wait_for_timeout(250)
        pg.fill('#roster-filter', 's1jetdelta'); pg.wait_for_timeout(250)
        pg.evaluate("""() => { const el=[...document.querySelectorAll('#roster .ri')]
            .find(e=>e.textContent.trim().startsWith('s1jetdelta')); if(el) el.click(); }""")
        pg.wait_for_timeout(200)
        pg.evaluate("() => window.BOD.spawn()")
        pg.wait_for_function("() => window.BOD.unit()", timeout=30000)
        ok(True, 'a unit is in the lab')

        # ---- the tab ----
        pg.evaluate("() => window.BOD.selectTab('fire')")
        pg.wait_for_timeout(400)
        built = pg.evaluate("""() => ({
            kinds: document.querySelector('#f-kind') ? document.querySelector('#f-kind').options.length : 0,
            shapes: document.querySelector('#f-shape') ? document.querySelector('#f-shape').options.length : 0,
            flashes: document.querySelector('#f-flash') ? document.querySelector('#f-flash').options.length : 0,
            inert: document.querySelectorAll('#insp .sec[data-sec=fi] .f').length,
            secs: [...document.querySelectorAll('#insp .sec')].map(s=>s.dataset.sec)
        })""")
        ok(built['kinds'] > 100, 'the projectile picker offers the whole registry (%d kinds)' % built['kinds'])
        ok(built['shapes'] >= 10, 'and the shape list comes from the scene director (%d)' % built['shapes'])
        ok(built['flashes'] >= 8, 'and real muzzle families, none + %d measured' % (built['flashes'] - 1))
        ok(built['inert'] >= 10,
           'the tab NAMES the dials that cannot work rather than shipping them (%d listed)' % built['inert'])
        ok('fa' in built['secs'] and 'fv' in built['secs'],
           'anchor and volley sections are present: %s' % built['secs'])
        pg.screenshot(path=os.path.join(a.out, '01_fire_tab.png'))

        # ---- FIRE ONCE with a fan: n distinct headings ----
        fan = pg.evaluate("""() => { const d=window.BOD.api();
            d.eBullets.length=0;
            const sh=document.querySelector('#f-shape'); sh.value='fan'; sh.dispatchEvent(new Event('change',{bubbles:true}));
            const n=document.querySelector('#f-n'); n.value=9; n.dispatchEvent(new Event('input',{bubbles:true}));
            document.querySelector('#f-once').click();
            const hs=d.eBullets.map(b=>Math.round(Math.atan2(b.vy,b.vx)*57.3));
            return {n:d.eBullets.length, distinct:new Set(hs).size, hs:hs}; }""")
        ok(fan['n'] == 9 and fan['distinct'] >= 8,
           'FIRE ONCE lays a real fan: %d rounds on %d distinct headings %s'
           % (fan['n'], fan['distinct'], fan['hs'][:5]))

        # ---- a one-shot shape disables ROUNDS and says why ----
        spiral_ui = pg.evaluate("""() => { const sh=document.querySelector('#f-shape');
            sh.value='spiral'; sh.dispatchEvent(new Event('change',{bubbles:true}));
            const n=document.querySelector('#f-n');
            const warn=[...document.querySelectorAll('#insp .sec[data-sec=fp] .hint.warn')].map(e=>e.textContent).join(' ');
            return {disabled:!!(n&&n.disabled), warns:warn.indexOf('ONE round per beat')>0}; }""")
        ok(spiral_ui['disabled'] and spiral_ui['warns'],
           'picking a one-round-per-beat shape disables ROUNDS and explains why, instead of leaving '
           'a slider that does nothing')

        # ---- the BURST is what makes a spiral a spiral ----
        spiral = pg.evaluate("""() => { const d=window.BOD.api();
            d.eBullets.length=0;
            const bn=document.querySelector('#f-burstn'); bn.value=12; bn.dispatchEvent(new Event('input',{bubbles:true}));
            const iv=document.querySelector('#f-interval'); iv.value=0.05; iv.dispatchEvent(new Event('input',{bubbles:true}));
            const st=document.querySelector('#f-step'); st.value=24; st.dispatchEvent(new Event('input',{bubbles:true}));
            document.querySelector('#f-burst').click(); return true; }""")
        pg.wait_for_timeout(1500)
        sp = pg.evaluate("""() => { const d=window.BOD.api();
            const hs=d.eBullets.map(b=>Math.round(Math.atan2(b.vy,b.vx)*57.3));
            return {n:hs.length, distinct:new Set(hs).size, hs:hs.slice(0,8)}; }""")
        ok(sp['n'] >= 8 and sp['distinct'] >= 6,
           'a BURST turns the spiral into a pattern: %d rounds on %d headings %s - a one-shot spiral '
           'is one round BY DESIGN, which is what made the first panel read as broken'
           % (sp['n'], sp['distinct'], sp['hs']))

        # ---- the wall's gap is a real lane ----
        wall = pg.evaluate("""() => { const d=window.BOD.api(); d.eBullets.length=0;
            const sh=document.querySelector('#f-shape'); sh.value='wall'; sh.dispatchEvent(new Event('change',{bubbles:true}));
            const n=document.querySelector('#f-n'); n.value=10; n.dispatchEvent(new Event('input',{bubbles:true}));
            const g=document.querySelector('#f-gap'); g.value=4; g.dispatchEvent(new Event('input',{bubbles:true}));
            document.querySelector('#f-once').click();
            const xs=d.eBullets.map(b=>Math.round(b.x)).sort((p,q)=>p-q);
            let biggest=0; for(let i=1;i<xs.length;i++) biggest=Math.max(biggest, xs[i]-xs[i-1]);
            const typical=xs.length>2?(xs[1]-xs[0]):0;
            return {n:xs.length, xs:xs, biggest:biggest, typical:typical}; }""")
        ok(wall['n'] == 9 and wall['biggest'] > wall['typical'] * 1.6,
           'the wall leaves the gap it is told to: %d of 10 columns, widest step %d against a '
           'typical %d' % (wall['n'], wall['biggest'], wall['typical']))

        # ---- the ANCHOR actually moves where rounds leave from ----
        anchor = pg.evaluate("""() => { const d=window.BOD.api(), u=window.BOD.unit();
            d.clearMounts(u);
            const before=d.mountPoint(u,'L');
            const sl=document.querySelector('#f-slot'); sl.value='L'; sl.dispatchEvent(new Event('change',{bubbles:true}));
            const mx=document.querySelector('#f-mx'); mx.value=-0.45; mx.dispatchEvent(new Event('input',{bubbles:true}));
            const after=d.mountPoint(u,'L');
            /* and a round must actually leave from there */
            d.eBullets.length=0;
            const sh=document.querySelector('#f-shape'); sh.value='fan'; sh.dispatchEvent(new Event('change',{bubbles:true}));
            document.querySelector('#f-once').click();
            const bx=d.eBullets.length?Math.round(d.eBullets[0].x):null;
            return {before:before, after:after, bulletX:bx, unitX:Math.round(u.x), w:u.w}; }""")
        moved = abs(anchor['after']['x'] - anchor['before']['x'])
        ok(moved > 20,
           'the ANCHOR slider moves the mount: x %d -> %d (%dpx) - it returned ONE point for all '
           'twelve slots before 0912h' % (anchor['before']['x'], anchor['after']['x'], moved))
        ok(anchor['bulletX'] is not None and abs(anchor['bulletX'] - anchor['after']['x']) < 3,
           'and the round leaves from the new mount, not the hull centre (bullet x %s, mount x %s, '
           'hull x %s)' % (anchor['bulletX'], round(anchor['after']['x']), anchor['unitX']))

        # ---- the muzzle flash is raised, and the default would NOT have been ----
        # ⚠ read the flash queue through the BRIDGE - `_navalFlashes` is a module-scope array and
        # is not a window property, so `host.contentWindow._navalFlashes` is undefined and
        # "no flash was raised" is indistinguishable from "I cannot see the queue".
        flash = pg.evaluate("""() => { const d=window.BOD.api();
            d.flashes.length=0;
            const fl=document.querySelector('#f-flash'); fl.value='bpfx_muzzle_kinetic';
            fl.dispatchEvent(new Event('change',{bubbles:true}));
            document.querySelector('#f-once').click();
            const named=d.flashes.length;
            /* the control: the engine default on an ordinary enemy */
            d.flashes.length=0;
            const u=window.BOD.unit();
            d.emit(u, {shape:'fan', n:5, kind:'e', anchor:'C'}, 0);
            return {named:named, withDefault:d.flashes.length}; }""")
        ok(flash['named'] > 0,
           'naming a muzzle family raises a real flash (%d queued)' % flash['named'])
        ok(flash['withDefault'] == 0,
           'and the engine DEFAULT raises none on an ordinary enemy (%d) - shipBossMuzzleStart '
           'returns unless the unit has _ship plus SHIPBOSS .proj and .mounts, silently, which is '
           'why the tab has no "default" option' % flash['withDefault'])

        # ---- the volley edits the table in BOTH spellings ----
        vol = pg.evaluate("""() => { const d=window.BOD.api();
            const ve=document.querySelector('#f-vevery');
            if(!ve) return {skip:'this unit has no volley row'};
            ve.value=7; ve.dispatchEvent(new Event('input',{bubbles:true}));
            return {upper:d.volleyFor('s1jetDelta').row.every, lower:d.volleyFor('s1jetdelta').row.every}; }""")
        if vol.get('skip'):
            ok(False, 'volley section: ' + vol['skip'])
        else:
            ok(vol['upper'] == 7 and vol['lower'] == 7,
               'the volley edit reaches BOTH spellings of the row (%s / %s) - writing one is how '
               'stages 4 and 6 fielded 26x26 one-hp jets for six drops' % (vol['upper'], vol['lower']))

        # ---- firing a volley ----
        vf = pg.evaluate("""() => { const d=window.BOD.api(); d.eBullets.length=0;
            const btn=document.querySelector('#f-vfire'); if(!btn) return {skip:1};
            btn.click(); return {n:d.eBullets.length}; }""")
        if not vf.get('skip'):
            ok(vf['n'] > 0, 'FIRE VOLLEY runs the unit\'s own authored volley (%d rounds)' % vf['n'])

        pg.wait_for_timeout(300)
        pg.screenshot(path=os.path.join(a.out, '02_fired.png'))

        # ---- the anchor is drawn on the overlay ----
        # ⚠ PIN THE SUBJECT FIRST. This assertion flaked 1 run in 3 at "0 px", and it is the SAME
        # probe fault probe_bod_overlay_0912h already records: s1jetdelta is a mover, the lab runs
        # real time, and by the time the ink is counted the unit can have drifted off and been
        # culled - at which point drawOverlay correctly returns early and the canvas is blank.
        # "the marker is not drawn" and "there is no longer a unit to mark" look identical from a
        # pixel count, so the probe says which.
        pinned = pg.evaluate("""() => { const W=document.querySelector('#host').contentWindow;
            const u=window.BOD.unit(); if(!u) return false;
            u.vx=0; u.vy=0; u._dyingT=null; u.x=Math.round(W.player.x-40); u.y=170; return true; }""")
        ok(pinned, 'the subject is still alive to mark (a culled unit and an unmarked one look the '
                   'same to a pixel count)')
        pg.wait_for_timeout(450)
        ink = pg.evaluate("""() => { const c=document.querySelector('#overlay');
            if(!c.width||c.width<2) return 0;
            const d=c.getContext('2d').getImageData(0,0,c.width,c.height).data;
            let gold=0; for(let i=0;i<d.length;i+=4){
              if(d[i+3]>40 && d[i]>200 && d[i+1]>140 && d[i+2]<110) gold++; }
            return gold; }""")
        ok(ink > 40, 'the mount is drawn on the field in gold so an offset is visible (%d px)' % ink)

        pg.screenshot(path=os.path.join(a.out, '03_final.png'))
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
