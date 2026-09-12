#!/usr/bin/env python3
"""
probe_theater_0911b.py - THE THEATER LAYOUT (drop 0911b).

    python3 _BUILD_SOURCE/probe_theater_0911b.py --out /tmp/theater

Mike: "a more theater and full screen for 75% screen like approach and a more modern editor style".
Real Chromium on bossmode.html at 1600x1000 and 1920x1080: the viewport's share of the width with
the dock open (~75%), with the dock folded (Tab), in THEATER (T), the drawer (L) sliding over and
closing on a pick, the layout remembered across a reload, and the scene inspector living in the
dock while the field takes the theater. Screenshots of every state.
"""
import os, sys, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shoot

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--out', default='/tmp/theater'); a=ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    from playwright.sync_api import sync_playwright
    port, stop = shoot.serve(shoot.GAME); errs=[]; fails=[]; n_ok=[0]
    def ok(c,m):
        if c: n_ok[0]+=1; print('  ok  ',m)
        else: fails.append(m); print('  FAIL',m)
    W_VIEW="() => { const r=document.getElementById('w-view').getBoundingClientRect(); return r.width/innerWidth; }"
    with sync_playwright() as p:
        b=p.chromium.launch(args=['--disable-gpu','--no-sandbox','--mute-audio'])
        ctx=b.new_context(viewport={'width':1600,'height':1000}); pg=ctx.new_page()
        pg.on('pageerror', lambda e: errs.append('pageerror: '+str(e)[:200]))
        pg.on('console', lambda m: errs.append('console.error: '+m.text[:200]) if m.type=='error' else None)
        missing=[]; pg.on('response', lambda r: missing.append(r.url.split(f':{port}/')[-1]) if r.status==404 else None)
        pg.goto(f'http://127.0.0.1:{port}/bossmode.html', wait_until='load', timeout=60000)
        pg.evaluate("() => localStorage.removeItem('bof_bm_layout')")
        pg.wait_for_function("() => document.getElementById('boot').classList.contains('gone')", timeout=60000)
        pg.wait_for_timeout(600)
        share=pg.evaluate(W_VIEW)
        ok(0.72<=share<=0.80, 'dock open: the viewport is %.0f%% of the width at 1600' % (share*100))
        ok(pg.evaluate("() => getComputedStyle(document.getElementById('drawer')).transform!=='none'"), 'the boss list starts as a closed drawer')
        ok(pg.evaluate("() => document.getElementById('host').getBoundingClientRect().height>600"), 'the engine iframe fills the theater (>600px tall)')
        pg.screenshot(path=os.path.join(a.out,'01_default_1600.png'))
        # L opens the drawer over the theater; picking a boss closes it
        pg.keyboard.press('l'); pg.wait_for_timeout(300)
        ok(pg.evaluate("() => document.body.classList.contains('drawer') && document.getElementById('drawer').getBoundingClientRect().left>=40"), 'L slides the drawer in over the theater')
        pg.screenshot(path=os.path.join(a.out,'02_drawer.png'))
        pg.evaluate("() => { const li=[...document.querySelectorAll('#list-groups .li')].find(e=>e.textContent.includes('MAGMA WARD')); li.click(); }"); pg.wait_for_timeout(300)
        ok(pg.evaluate("() => !document.body.classList.contains('drawer') && document.getElementById('vt-name').textContent==='MAGMA WARD'"), 'picking a boss closes the drawer and names the view')
        ok(pg.evaluate("() => document.getElementById('dock-sub').textContent==='BOSS · S2'"), 'the dock header reads the role and stage')
        # Tab folds the dock; the viewport widens; the pull tab appears
        pg.keyboard.press('Tab'); pg.wait_for_timeout(400)
        share2=pg.evaluate(W_VIEW)
        ok(share2>0.93 and pg.evaluate("() => getComputedStyle(document.getElementById('dock-open')).display==='block'"), 'Tab folds the dock: viewport %.0f%%, pull tab shown' % (share2*100))
        pg.click('#dock-open'); pg.wait_for_timeout(400)
        ok(abs(pg.evaluate(W_VIEW)-share)<0.01, 'the pull tab brings the dock back')
        # T = theater
        pg.keyboard.press('t'); pg.wait_for_timeout(400)
        share3=pg.evaluate(W_VIEW)
        ok(pg.evaluate("() => document.body.classList.contains('theater')") and share3>0.93, 'T: theater, the view has %.0f%% of the width' % (share3*100))
        pg.screenshot(path=os.path.join(a.out,'03_theater.png'))
        pg.keyboard.press('F11'); pg.wait_for_timeout(400)
        ok(not pg.evaluate("() => document.body.classList.contains('theater')") and abs(pg.evaluate(W_VIEW)-share)<0.01, 'F11 toggles theater off again')
        # the SCENE tab: inspector in the dock, the field in the theater
        pg.click('#tabs .tab[data-tab=scene]'); pg.wait_for_timeout(500)
        ok(pg.evaluate("() => document.body.dataset.tab==='scene' && document.querySelector('#dock-scene #sc-insp')!==null && getComputedStyle(document.getElementById('dock-main')).display==='none'"), 'SCENE: the scene inspector is in the dock, the fight inspector hidden')
        cvw=pg.evaluate("() => document.getElementById('sc-cv').getBoundingClientRect().width"); wrapw=pg.evaluate("() => document.getElementById('sc-wrap').clientWidth")
        ok(cvw>500 and cvw<=wrapw, 'the field canvas is fitted into the theater (%dpx of %dpx)' % (cvw, wrapw))
        pg.screenshot(path=os.path.join(a.out,'04_scene.png'))
        pg.keyboard.press('Tab'); pg.wait_for_timeout(500)
        cvw2=pg.evaluate("() => document.getElementById('sc-cv').getBoundingClientRect().width")
        ok(cvw2>=cvw, 'folding the dock refits the field (%dpx -> %dpx)' % (cvw, cvw2))
        # the layout is remembered
        pg.reload(wait_until='load'); pg.wait_for_function("() => document.getElementById('boot').classList.contains('gone')", timeout=60000); pg.wait_for_timeout(400)
        ok(pg.evaluate("() => document.body.classList.contains('nodock')"), 'the folded dock is remembered across a reload')
        pg.keyboard.press('Tab'); pg.wait_for_timeout(300)
        # the file bar + PLAY TEST still work in the new chrome
        pg.click('#tabs .tab[data-tab=stage]'); pg.wait_for_timeout(200)
        pg.click('#b-play'); pg.wait_for_function("() => { const s=document.getElementById('host').contentWindow.BOSSMODE.snapshot(); return s.bossActive; }", timeout=25000)
        pg.wait_for_timeout(800); pg.screenshot(path=os.path.join(a.out,'05_playtest_1600.png'))
        ok(True, 'PLAY TEST runs in the theater')
        pg.click('#b-stop'); pg.wait_for_function("() => document.getElementById('host').contentWindow.BOSSMODE.state==='bmhost'", timeout=15000)
        # 1920x1080
        pg.set_viewport_size({'width':1920,'height':1080}); pg.wait_for_timeout(500)
        share4=pg.evaluate(W_VIEW)
        ok(0.76<=share4<=0.82, 'at 1920 the viewport is %.0f%% of the width' % (share4*100))
        pg.screenshot(path=os.path.join(a.out,'06_default_1920.png'))
        b.close()
    stop()
    if missing:
        from collections import Counter
        print('404s:'); [print('   %3d  %s' % (n,u)) for u,n in Counter(missing).most_common(10)]
    print('\n%d ok / %d fail' % (n_ok[0], len(fails)))
    for f in fails: print('  FAIL', f)
    if errs:
        print('page errors (%d):' % len(errs))
        for e in errs[:10]: print('   ', e)
    sys.exit(1 if fails or errs else 0)

if __name__=='__main__':
    main()
