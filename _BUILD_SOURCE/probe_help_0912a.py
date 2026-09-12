#!/usr/bin/env python3
"""
probe_help_0912a.py - THE HELP BUTTON AND THE HELP SCREEN.

    python3 _BUILD_SOURCE/probe_help_0912a.py --out /tmp/help

Six title buttons now, and a cursor that wrapped on a literal 5 would make the last one
unreachable - so the wrap is walked in BOTH directions rather than assumed. Then HELP is opened the
way a player opens it, all three pages are turned and captured, the labels are checked against the
LIVE bind table (not against typed strings), and BACK returns to the title the way every other
backable screen does.
"""
import os, sys, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shoot

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--out', default='/tmp/help'); a=ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    from playwright.sync_api import sync_playwright
    port, stop = shoot.serve(shoot.GAME); errs=[]; fails=[]; n_ok=[0]
    def ok(c,m):
        if c: n_ok[0]+=1; print('  ok  ',m)
        else: fails.append(m); print('  FAIL',m)
    INK = ("() => { const c=document.getElementById('screen'); const d=c.getContext('2d')"
           ".getImageData(0,0,c.width,c.height).data; let n=0,t=0;"
           " for(let i=0;i<d.length;i+=16){t++; if(d[i]+d[i+1]+d[i+2]>46) n++;} return n/t; }")
    with sync_playwright() as p:
        b=p.chromium.launch(args=['--disable-gpu','--no-sandbox','--mute-audio'])
        pg=b.new_page(viewport={'width':1100,'height':1000})
        pg.on('pageerror', lambda e: errs.append('pageerror: '+str(e)[:220]))
        pg.on('console', lambda m: errs.append('console.error: '+m.text[:200]) if m.type=='error' else None)
        missing=[]; pg.on('response', lambda r: missing.append(r.url.split(f':{port}/')[-1]) if r.status==404 else None)
        pg.goto(f'http://127.0.0.1:{port}/index.html?debug=1', wait_until='load', timeout=60000)
        pg.wait_for_timeout(1200); pg.keyboard.press('Enter')
        # skip the opener straight to the title
        pg.wait_for_function("() => window.__BOFSTATE && window.__BOFSTATE()==='opener'", timeout=60000)
        pg.wait_for_timeout(400); pg.keyboard.press('Space')
        pg.wait_for_function("() => window.__BOFSTATE()==='title'", timeout=20000)
        pg.wait_for_timeout(800)

        items=pg.evaluate("() => window.__BOFHELP().items")
        ok(items==['NEW GAME','PASSWORD','OPTIONS','HELP','CREDITS','EXIT GAME'],
           'HELP is the fourth title button: %s' % items)
        ok(pg.evaluate("() => window.__BOFHELP().btnArt"),
           'its plate (btn_help) is registered and decoded, matching the menu family')
        pg.screenshot(path=os.path.join(a.out,'00_title.png'))

        # ⚠ the wrap, both ways - a literal 5 would strand the sixth item
        n=len(items)
        idx=[]
        for i in range(n+1):
            idx.append(pg.evaluate("() => window.__BOFHELP().idx"))
            pg.keyboard.press('ArrowDown'); pg.wait_for_timeout(140)
        ok(idx[:n]==list(range(n)) and idx[n]==0,
           'the cursor steps through all six and wraps: %s' % idx)
        # ⚠ n presses from WHEREVER the cursor now sits must return it to the same row - the loop
        # above left it one step past the last read, so asserting a literal 0 here was the probe's
        # own arithmetic being wrong rather than the menu.
        before=pg.evaluate("() => window.__BOFHELP().idx")
        for _ in range(n): pg.keyboard.press('ArrowUp'); pg.wait_for_timeout(120)
        after=pg.evaluate("() => window.__BOFHELP().idx")
        ok(before==after, 'and wraps upward too (%d -> %d after %d steps)' % (before, after, n))

        # open it the way a player does: step down until HELP is lit, rather than counting presses
        for _ in range(n*2):
            if pg.evaluate("() => window.__BOFHELP().idx")==3: break
            pg.keyboard.press('ArrowDown'); pg.wait_for_timeout(140)
        ok(pg.evaluate("() => window.__BOFHELP().idx")==3, 'HELP is under the cursor')
        pg.keyboard.press('Enter')
        pg.wait_for_function("() => window.__BOFSTATE()==='help'", timeout=10000)
        ok(True, 'ENTER on HELP opens the help screen')

        pages=[]
        for i in range(3):
            pg.wait_for_timeout(700)
            h=pg.evaluate("() => window.__BOFHELP()")
            ink=pg.evaluate(INK)
            pages.append((h['page'], ink))
            pg.screenshot(path=os.path.join(a.out,'%02d_%s.png'%(i+1,h['pageName'].lower())))
            print('      page %d %-9s ink %.0f%%' % (i, h['pageName'], ink*100))
            pg.keyboard.press('ArrowRight')
        ok(all(p[1]>0.04 for p in pages), 'all three pages paint (%s)' % [round(p[1]*100) for p in pages])
        # ⚠ NOTHING MAY OVERFLOW THE FIELD AT THE FLOOR SIZE. helpLabel will not shrink a line below
        # HELP_MIN (11px) because both stage faces mush under that - which means an over-long string
        # runs off the edge instead of getting smaller. Measured with the engine's own stageWidth
        # across all three pages rather than eyeballed in a screenshot.
        wd=pg.evaluate("() => window.__BOFHELP()")
        ok(wd['widest']['w'] <= wd['field'],
           'the widest line on any page fits the field: %dpx of %dpx  [%s]'
           % (wd['widest']['w'], wd['field'], wd['widest']['s']))
        ok([p[0] for p in pages]==[0,1,2], 'RIGHT turns the pages in order')

        # the labels come from the live table, not from typed strings
        pg.wait_for_timeout(300)
        bl=pg.evaluate("() => window.__BOFHELP().labels")
        ok(bl['fire'] and 'L-CLICK' in bl['fire'], 'FIRE reads the live bind: %s' % bl['fire'])
        ok('SPACE' in bl['retina'] and 'MOUSE 4' in bl['retina'],
           'RETINA / C shows SPACE and the side button: %s' % bl['retina'])
        ok('MOUSE 5' in bl['charge'], 'CHARGE shows H and the other side button: %s' % bl['charge'])
        # and it follows a rebind rather than restating a literal
        pg.evaluate("() => window.__BOFHELP().rebind('fire','q')")
        pg.wait_for_timeout(200)
        ok(pg.evaluate("() => window.__BOFHELP().labels.fire").startswith('Q'),
           'rebinding FIRE changes what HELP says (no hard-coded key names)')
        pg.evaluate("() => window.__BOFHELP().restore()")

        pg.keyboard.press('Escape')
        pg.wait_for_function("() => window.__BOFSTATE()==='title'", timeout=8000)
        # ⚠ THE CURSOR RESETS, AND THAT IS THE HOUSE RULE, not a bug. menuBackTick sets menuIndex=0
        # for every backable screen on purpose - "a stray menu index following you back out is its
        # own bug". The first cut of this assertion demanded HELP stay lit, which would have made
        # HELP the one screen in the game that behaves differently on the way out.
        ok(pg.evaluate("() => window.__BOFHELP().idx")==0,
           'BACK returns to the title with the cursor reset, like every other menu')
        b.close()
    stop()
    if missing:
        from collections import Counter
        print('404s:'); [print('   %3d  %s'%(n,u)) for u,n in Counter(missing).most_common(6)]
    print('\n%d ok / %d fail' % (n_ok[0], len(fails)))
    for f in fails: print('  FAIL', f)
    if errs:
        print('page errors (%d):' % len(errs))
        for e in errs[:8]: print('   ', e)
    sys.exit(1 if fails or errs else 0)

if __name__=='__main__':
    main()
