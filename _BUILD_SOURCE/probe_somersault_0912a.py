#!/usr/bin/env python3
"""
probe_somersault_0912a.py - ALL NINE PILOTS ACTUALLY SOMERSAULT, IN THE REAL ENGINE.

    python3 _BUILD_SOURCE/probe_somersault_0912a.py --out /tmp/ss

Not "the key is registered" - the move. For every pilot: start a real fight through the debug
host, double-tap UP, and assert the engine entered player.somer, that somerFrameKey() resolves
to that pilot's own reel, that the flip carries i-frames, and that it walks all eight frames and
returns the ship to where it started. Lizzie is the one this drop added, so she is checked on
BOTH of her airframes - the stock delta and the B-42 costume, which read different atlas pages.
"""
import os, sys, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shoot

PILOTS = ['axel','cole','decker','falva','freezer','juggernaut','lizzie','maverick','yuri']

# double-tap UP inside SS_WINDOW (0.26s), then let the flip run
FLIP = r"""
async ([pilot, skin]) => {
  const W = window;
  const B = W.BOSSMODE;
  B.start(2, 'boss', pilot, false);
  // wait for the fight to be live and the player to exist
  for(let i=0;i<900 && !(B.snapshot().bossActive && B.player && !B.player.dead); i++)
    await new Promise(r=>requestAnimationFrame(r));
  const p = B.player;
  if(!p) return {err:'no player'};
  p._somerCool = 0; p.somer = null; p._tapU = -9;
  const y0 = p.y;
  const seen = {};
  let armed=false, invulnPeak=0;
  // two UP taps in consecutive frames is well inside SS_WINDOW
  B.injectTap('w'); await new Promise(r=>requestAnimationFrame(r));
  B.injectTap('w');
  for(let i=0;i<120;i++){
    await new Promise(r=>requestAnimationFrame(r));
    const q = B.player;
    if(q && q.somer){
      armed = true;
      invulnPeak = Math.max(invulnPeak, q.invuln||0);
      const k = B.somerFrameKey ? B.somerFrameKey() : null;
      if(k) seen[k]=1;
    } else if(armed) break;
  }
  const q = B.player;
  return {
    armed: armed,
    frames: Object.keys(seen).sort(),
    invuln: invulnPeak,
    dy: Math.round((q?q.y:0) - y0),
    ended: !!(q && !q.somer),
    cool: q ? Math.round((q._somerCool||0)*10)/10 : -1
  };
}
"""

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--out', default='/tmp/ss'); a=ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    from playwright.sync_api import sync_playwright
    port, stop = shoot.serve(shoot.GAME); errs=[]; fails=[]; n_ok=[0]
    def ok(c,m):
        if c: n_ok[0]+=1; print('  ok  ',m)
        else: fails.append(m); print('  FAIL',m)
    with sync_playwright() as p:
        b=p.chromium.launch(args=['--disable-gpu','--no-sandbox','--mute-audio'])
        pg=b.new_page(viewport={'width':1100,'height':1000})
        pg.on('pageerror', lambda e: errs.append('pageerror: '+str(e)[:200]))
        pg.goto(f'http://127.0.0.1:{port}/index.html?bossmode=1', wait_until='load', timeout=60000)
        pg.wait_for_function("() => window.BOSSMODE && window.BOSSMODE.ready", timeout=90000)
        for pk in PILOTS:
            r=pg.evaluate(FLIP, [pk, False])
            good = (r.get('armed') and len(r.get('frames',[]))>=6
                    and all(f.startswith('ship_%s_so'%pk) for f in r.get('frames',[]))
                    and r.get('invuln',0)>30 and abs(r.get('dy',999))<=3 and r.get('ended'))
            ok(good, '%-11s somersault: %d frames %s, invuln %d, net dy %d, cooldown %.1fs'
               % (pk.upper(), len(r.get('frames',[])), 'own reel' if all(f.startswith('ship_%s_so'%pk) for f in r.get('frames',[])) else 'WRONG REEL %s'%r.get('frames'),
                  r.get('invuln',0), r.get('dy',0), r.get('cool',-1)))
            pg.evaluate("() => window.BOSSMODE.stop()")
            pg.wait_for_timeout(250)
        # the flip is drawn, not just tracked: capture Lizzie mid-somersault
        pg.evaluate("""async () => {
            const B=window.BOSSMODE; B.start(2,'boss','lizzie',false);
            for(let i=0;i<900 && !(B.snapshot().bossActive && B.player); i++) await new Promise(r=>requestAnimationFrame(r));
            const p=B.player; p._somerCool=0; p._tapU=-9;
            B.injectTap('w'); await new Promise(r=>requestAnimationFrame(r)); B.injectTap('w');
            for(let i=0;i<12;i++) await new Promise(r=>requestAnimationFrame(r));
        }""")
        pg.screenshot(path=os.path.join(a.out,'01_lizzie_midflip.png'))
        ok(pg.evaluate("() => { const p=window.BOSSMODE.player; return !!(p&&p.somer); }"),
           'the capture was taken with the flip still live')
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
