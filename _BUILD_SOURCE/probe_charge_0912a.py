#!/usr/bin/env python3
"""
probe_charge_0912a.py - JUGGERNAUT'S CHARGE, HIS WRECKING BALLS, AND THE NEW BINDS.

    python3 _BUILD_SOURCE/probe_charge_0912a.py --out /tmp/chg

Drives the real engine through the debug host:
  * the binds - space on RETINA (Mike asked; it was already true, so it is pinned), the two side
    mouse buttons on C and CHARGE, CHARGE rebindable in both control screens
  * the charge is HIS and only while the crate is live - no bar and no dash for anyone else
  * hold CHARGE+UP -> the wind-up climbs, pins him, and release rams him forward, with a LONGER
    hold buying a LONGER ram (measured twice at two hold times, not asserted once)
  * six wrecking balls, two rings, counter-rotating, anchored to the ship
  * they eat enemy fire and they damage a boss
  * the CHARGE bar is the bottom row with SOMERSAULT and ROLL lifted above it
"""
import os, sys, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shoot

# hold CHARGE+UP for `hold` seconds, release, and report how far the ram carried him
DASH = r"""
async ([hold]) => {
  const B=window.BOSSMODE;
  const p=B.player;
  p._chgT=0; p._chgOn=false; p._chgDash=null;
  // park him low so a long ram has room, and hold the two keys down for real
  p.y = B.snapshot().VH*0.78;
  const y0=p.y;
  B.hold('h',true); B.hold('w',true);
  const t0=performance.now();
  let peak=0, pinnedDrift=0, yWind=p.y;
  while(performance.now()-t0 < hold*1000){
    await new Promise(r=>requestAnimationFrame(r));
    peak=Math.max(peak, B.player._chgT||0);
    pinnedDrift=Math.max(pinnedDrift, Math.abs(B.player.y-yWind));
  }
  const lvlAtRelease = B.player._chgT||0;
  B.hold('h',false); B.hold('w',false);
  const yRelease=B.player.y;
  let dashed=false, invuln=0;
  for(let i=0;i<90;i++){
    await new Promise(r=>requestAnimationFrame(r));
    if(B.player._chgDash){ dashed=true; invuln=Math.max(invuln,B.player.invuln||0); }
    else if(dashed) break;
  }
  return {peak:+peak.toFixed(2), lvl:+lvlAtRelease.toFixed(2), dashed:dashed,
          travel:Math.round(yRelease-B.player.y), pinnedDrift:Math.round(pinnedDrift), invuln:invuln};
}
"""

START = r"""
async ([pilot]) => {
  const B=window.BOSSMODE;
  B.start(2,'boss',pilot,false);
  for(let i=0;i<900 && !(B.snapshot().bossActive && B.player && !B.player.dead); i++)
    await new Promise(r=>requestAnimationFrame(r));
  return !!B.player;
}
"""

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--out', default='/tmp/chg'); a=ap.parse_args()
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

        # ---- the binds ----
        kb=pg.evaluate("() => JSON.parse(JSON.stringify(window.BOSSMODE.binds()))")
        ok(' ' in kb['retina'] and 'c' in kb['retina'],
           "SPACE is the C / retina button: retina = %s" % kb['retina'])
        ok('mouse3' in kb['retina'], "side mouse button 4 (e.button 3) is C: %s" % kb['retina'])
        ok(kb.get('charge') and 'h' in kb['charge'] and 'mouse4' in kb['charge'],
           "CHARGE is H + side mouse button 5 (e.button 4): %s" % kb.get('charge'))
        ok(pg.evaluate("() => window.BOSSMODE.ctrlActs().indexOf('charge')>=0"),
           'CHARGE is rebindable in the controls screen')

        # ---- it is Juggernaut's, and only with the crate ----
        pg.evaluate(START, ['yuri'])
        ok(not pg.evaluate("() => window.BOSSMODE.chargeAvailable()"), 'no charge for YURI')
        pg.evaluate("() => window.BOSSMODE.grantSpecial()")
        ok(not pg.evaluate("() => window.BOSSMODE.chargeAvailable()"),
           "and none for YURI even with a special up - it is Juggernaut's")
        pg.evaluate("() => window.BOSSMODE.stop()"); pg.wait_for_timeout(250)

        pg.evaluate(START, ['juggernaut'])
        ok(not pg.evaluate("() => window.BOSSMODE.chargeAvailable()"),
           'no charge for JUGGERNAUT before he picks the crate up')
        pg.evaluate("() => window.BOSSMODE.grantSpecial()")
        pg.wait_for_timeout(120)
        ok(pg.evaluate("() => window.BOSSMODE.chargeAvailable()"), 'the crate arms his charge')

        # ---- the wrecking balls ----
        pg.wait_for_timeout(400)
        wb=pg.evaluate("() => window.BOSSMODE.wreck().map(b=>({r:Math.round(Math.hypot(b.x-window.BOSSMODE.player.x,b.y-window.BOSSMODE.player.y)), spin:b.spin}))")
        radii=sorted(set(w['r'] for w in wb)); spins=sorted(set(w['spin'] for w in wb))
        ok(len(wb)==6 and len(radii)==2, 'six wrecking balls on two rings, radii %s' % radii)
        ok(len(spins)==2 and spins[0]<0<spins[1],
           'the two rings swing in OPPOSITE directions: %s rad/s' % spins)
        a1=pg.evaluate("() => window.BOSSMODE.wreck()[0].a")
        pg.wait_for_timeout(320)
        a2=pg.evaluate("() => window.BOSSMODE.wreck()[0].a")
        ok(abs(a2-a1)>0.3, 'they are actually swinging (%.2f rad in 0.32s)' % abs(a2-a1))
        anch=pg.evaluate("""() => { const B=window.BOSSMODE; B.player.x+=60;
            return B.wreck().every(b=>Math.hypot(b.x-B.player.x,b.y-B.player.y)<200); }""")
        pg.wait_for_timeout(120)
        ok(pg.evaluate("""() => { const B=window.BOSSMODE;
            return B.wreck().every(b=>Math.hypot(b.x-B.player.x,b.y-B.player.y)<130); }"""),
           'they re-anchor to the ship after it moves')
        # they eat enemy fire
        eaten=pg.evaluate("""async () => {
            const B=window.BOSSMODE, W=window;
            const before=B.eBullets.length;
            const b=B.wreck()[0];
            for(let i=0;i<8;i++) B.eBullets.push({x:b.x,y:b.y,vx:0,vy:0,r:3,dead:false,dmg:1});
            const seeded=B.eBullets.length;
            for(let i=0;i<6;i++) await new Promise(r=>requestAnimationFrame(r));
            return {seeded:seeded-before, alive:B.eBullets.filter(e=>!e.dead).length};
        }""")
        ok(eaten['alive']<=2, 'the balls cull enemy rounds: seeded %d on a ball, %d still alive'
           % (eaten['seeded'], eaten['alive']))
        # ---- and they damage a boss.
        # ⚠ NOT MEASURED AS HP. Stage 2's Magma Ward absorbs into barriers before the hull sees a
        # hit (hitBoss), so a real contact can legitimately move hp by zero - the first cut of this
        # assertion failed against working code. The BALL's own re-hit clock is the honest signal:
        # it is set by the boss branch and by nothing else on that frame.
        hit=pg.evaluate("""async () => {
            const B=window.BOSSMODE, s0=B.snapshot().boss.hp;
            const t=B.boss; B.player.x=t.x; B.player.y=t.y;
            let fired=0;
            for(let i=0;i<50;i++){ await new Promise(r=>requestAnimationFrame(r));
              if(B.wreck().some(b=>b.cd>0)) fired++; }
            return {fired:fired, dhp:s0-B.snapshot().boss.hp}; }""")
        ok(hit['fired']>0, 'a ring dragged through the boss lands hits (%d frames on the re-hit clock, %d hp through the barrier)'
           % (hit['fired'], hit['dhp']))
        pg.screenshot(path=os.path.join(a.out,'01_wrecking_balls.png'))

        # ---- the charge dash: a longer hold must buy a longer ram ----
        short=pg.evaluate(DASH, [0.30])
        pg.wait_for_timeout(200)
        long_=pg.evaluate(DASH, [1.45])
        ok(short['dashed'] and long_['dashed'], 'both a short and a full hold ram forward')
        ok(long_['lvl']>short['lvl']+0.4, 'the wind-up climbs with the hold: %.2fs vs %.2fs'
           % (short['lvl'], long_['lvl']))
        ok(long_['travel']>short['travel']+60,
           'and a longer charge projects him further: %dpx vs %dpx' % (long_['travel'], short['travel']))
        ok(long_['pinnedDrift']<=2, 'the wind-up pins him (drift %dpx while holding UP)' % long_['pinnedDrift'])
        ok(long_['invuln']>20, 'the ram carries i-frames (%d)' % long_['invuln'])
        ok(pg.evaluate("() => window.BOSSMODE.chargeLevel()===0 && !window.BOSSMODE.player._chgOn"),
           'and the wind-up resets after the ram')

        # ---- the bar ----
        pg.evaluate("""async () => { const B=window.BOSSMODE; B.hold('h',true); B.hold('w',true);
            for(let i=0;i<40;i++) await new Promise(r=>requestAnimationFrame(r)); }""")
        pg.screenshot(path=os.path.join(a.out,'02_charging.png'))
        rows=pg.evaluate("() => window.BOSSMODE.barRows()")
        ok(rows and rows['charge']==0 and rows['somersault']==1 and rows['roll']==2,
           'bar rows bottom-up: CHARGE 0, SOMERSAULT 1, ROLL 2 -> %s' % rows)
        pg.evaluate("() => { window.BOSSMODE.hold('h',false); window.BOSSMODE.hold('w',false); }")
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
