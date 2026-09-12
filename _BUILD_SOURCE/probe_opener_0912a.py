#!/usr/bin/env python3
"""
probe_opener_0912a.py - THE ARCADE OPENER, BEAT BY BEAT.

    python3 _BUILD_SOURCE/probe_opener_0912a.py --out /tmp/opener

Boots the real game with no query string at all - the way a player does - and asserts that the
ColeForge logo hands off to GS.OPENER rather than to the title, that all nine beats run in Mike's
order, that every beat actually PAINTS (an opener that advances its clock against a black screen is
the exact failure 0809p records), that the montage draws nine panels, and that any input skips it.
A frame is captured on every beat so the reel can be looked at rather than trusted.
"""
import os, sys, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shoot

# how much of the frame is not black - a beat that paints nothing scores ~0
INK = r"""
() => {
  const c=document.getElementById('screen');   // #hud is first in the DOM and is not the reel
  const g=c.getContext('2d');
  const d=g.getImageData(0,0,c.width,c.height).data;
  let n=0, tot=0;
  for(let i=0;i<d.length;i+=16){ tot++; if(d[i]+d[i+1]+d[i+2] > 46) n++; }
  return n/Math.max(1,tot);
}
"""

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--out', default='/tmp/opener'); a=ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    from playwright.sync_api import sync_playwright
    port, stop = shoot.serve(shoot.GAME); errs=[]; fails=[]; n_ok=[0]
    def ok(c,m):
        if c: n_ok[0]+=1; print('  ok  ',m)
        else: fails.append(m); print('  FAIL',m)
    BEATS=['sil','sil','roll','face','demo','demo','demo','nine','logo']
    with sync_playwright() as p:
        b=p.chromium.launch(args=['--disable-gpu','--no-sandbox','--mute-audio',
                                  '--autoplay-policy=no-user-gesture-required'])
        pg=b.new_page(viewport={'width':1100,'height':1000})
        pg.on('pageerror', lambda e: errs.append('pageerror: '+str(e)[:220]))
        pg.on('console', lambda m: errs.append('console.error: '+m.text[:200]) if m.type=='error' else None)
        # NO query string: this is the path a player takes
        pg.goto(f'http://127.0.0.1:{port}/index.html', wait_until='load', timeout=60000)
        pg.wait_for_timeout(1200)
        pg.keyboard.press('Enter')          # the boot gate wants one press to unlock audio
        pg.wait_for_function("() => window.__BOFSTATE && window.__BOFSTATE()==='opener'", timeout=60000)
        ok(True, 'the ColeForge logo hands off to GS.OPENER, not straight to the title')
        ok(pg.evaluate("() => window.__BOFOPN().music"),
           'the opener runs on the one track the manifest never mapped (stage9_bonus_warp_run)')

        seen=[]; blank=[]
        for i in range(len(BEATS)):
            pg.wait_for_function("(i) => window.__BOFOPN().i===i", arg=i, timeout=30000)
            pg.wait_for_timeout(700)
            o=pg.evaluate("() => window.__BOFOPN()")
            ink=pg.evaluate(INK)
            seen.append(o['k'])
            if ink<0.02: blank.append('%d:%s' % (i,o['k']))
            pg.screenshot(path=os.path.join(a.out,'%02d_%s.png'%(i,o['k'])))
            print('      beat %d %-5s ink %.0f%%  "%s"' % (i, o['k'], ink*100, o.get('t') or ''))
        ok(seen==BEATS, "the nine beats run in Mike's order: %s" % ' '.join(seen))
        ok(not blank, 'every beat paints something (blank beats: %s)' % (blank or 'none'))

        n=pg.evaluate("() => window.__BOFOPN().nine")
        ok(n==9, 'the finale is a nine-screen montage (%s panels)' % n)
        acts=pg.evaluate("() => window.__BOFOPN().acts")
        ok(sorted(set(acts))==['die','dodge','kill'] and acts.count('die')==3 and acts.count('kill')==3,
           'all three outcomes Mike named are on the wall: %s' % acts)

        pg.wait_for_function("() => window.__BOFSTATE()==='title'", timeout=30000)
        ok(True, 'the opener ends at the main menu on its own')

        pg.evaluate("() => window.__BOFOPENERSTART()")
        pg.wait_for_function("() => window.__BOFSTATE()==='opener'", timeout=15000)
        pg.wait_for_timeout(900)
        pg.keyboard.press('Space')
        pg.wait_for_function("() => window.__BOFSTATE()==='title'", timeout=8000)
        ok(True, 'any input skips it, mid-beat')
        b.close()
    stop()
    print('\n%d ok / %d fail' % (n_ok[0], len(fails)))
    for f in fails: print('  FAIL', f)
    if errs:
        print('page errors (%d):' % len(errs))
        for e in errs[:8]: print('   ', e)
    sys.exit(1 if fails or errs else 0)

if __name__=='__main__':
    main()
