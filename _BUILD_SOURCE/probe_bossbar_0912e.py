#!/usr/bin/env python3
"""
probe_bossbar_0912e.py - THE NAME TAB AND THE SHIELD BAR.

    python3 _BUILD_SOURCE/probe_bossbar_0912e.py --out /tmp/bar

Mike (0912): "hud bars for the bosses regenerated but with BOSS embed into the center above the
above but within a tab connnected to the bar ... Also, we will need an additional SHIELD hud bar
for the bosses too with forcefield/shield like fills too."

Drives real fights and captures them: a BOSS tab on a boss bar, a MINI BOSS tab on a miniboss bar,
and on the Magma Ward - which carries a real hp/maxhp barrier - the SHIELD bar under the HP bar
with its forcefield fill. Also checks the shield bar is ABSENT on a boss that has no shield, since
a bar that is always there says nothing.
"""
import os, sys, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shoot

START = r"""
async ([stage, role]) => {
  const B=window.BOSSMODE;
  B.start(stage, role, 'yuri', false);
  for(let i=0;i<900 && !(B.snapshot().bossActive||B.snapshot().subBossActive); i++)
    await new Promise(r=>requestAnimationFrame(r));
  B.setInvuln(true);
  for(let i=0;i<50;i++) await new Promise(r=>requestAnimationFrame(r));
  return B.snapshot().boss ? B.snapshot().boss.name : null;
}
"""

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--out', default='/tmp/bar'); a=ap.parse_args()
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
        miss=[]; pg.on('response', lambda r: miss.append(r.url.split(f':{port}/')[-1]) if r.status==404 else None)
        pg.goto(f'http://127.0.0.1:{port}/index.html?bossmode=1', wait_until='load', timeout=60000)
        pg.wait_for_function("() => window.BOSSMODE && window.BOSSMODE.ready", timeout=90000)

        # ---- the art ----
        keys=['bmbar_tab_boss','bmbar_tab_mini','bmbar_sfill_hex','bmbar_sfill_plasma',
              'bmbar_sfill_over','bmbar_sfill_low']
        pg.evaluate("(ks)=>ks.forEach(k=>{try{XART.rdy(k);}catch(e){}})", keys)
        pg.wait_for_timeout(2500)
        gone=pg.evaluate("(ks)=>ks.filter(k=>!XART.rdy(k))", keys)
        ok(not gone, 'the two tabs and four shield fills decode - missing: %s' % (gone or 'none'))
        ok(pg.evaluate("() => bmbarTabLabel('boss')==='BOSS' && bmbarTabLabel('mini')==='MINI BOSS' && bmbarTabLabel('shield')==='SHIELD'"),
           'the tab is lettered at draw time, so one plate serves BOSS / MINI BOSS / SHIELD')

        # ---- the miniboss bar gets the MINI BOSS tab ----
        # ⚠ THE ROLE IS 'mini', NOT 'sub'. debugFightList() builds rows with role:'boss' and
        # role:'mini'; debugFightFor(stage,'sub') finds nothing, debugStartFight(null) returns
        # false, and the wait times out against a fight that was never asked for. Reordering the
        # probe did not help because the order was never the problem.
        pg.evaluate(START, [2, 'mini'])
        pg.wait_for_function("() => { const s=window.BOSSMODE.snapshot(); return s.subBossActive||s.bossActive; }", timeout=30000)
        pg.wait_for_timeout(500)
        pg.screenshot(path=os.path.join(a.out,'03_mini.png'), clip={'x':180,'y':160,'width':730,'height':190})
        ok(pg.evaluate("() => window.BOSSMODE.snapshot().subBossActive || window.BOSSMODE.snapshot().bossActive"),
           'the miniboss fight is live for its capture')

        # ---- the shield resolver only fires where a shield exists ----
        pg.evaluate(START, [2, 'boss'])
        hasB=pg.evaluate("() => !!(window.BOSSMODE.boss && window.BOSSMODE.boss._mwBarrier)")
        ok(hasB, 'the Magma Ward carries a real barrier to drive the bar')
        f=pg.evaluate("() => bossShieldFrac(window.BOSSMODE.boss)")
        ok(f is not None and f > 0, 'bossShieldFrac reads it: %.2f' % (f or 0))
        pg.screenshot(path=os.path.join(a.out,'01_boss_with_shield.png'), clip={'x':180,'y':160,'width':730,'height':190})

        # drain the barrier and confirm the fill escalates down through its states
        st=pg.evaluate("""() => {
            const b=window.BOSSMODE.boss, H=b._mwBarrier, seen=[];
            for(const fr of [1.0,0.7,0.4,0.1]){
                H.hp=Math.max(1,Math.round(H.maxhp*fr));
                seen.push(bmbarShieldFillKey(bossShieldFrac(b)).replace('bmbar_sfill_',''));
            }
            H.hp=H.maxhp; return seen;
        }""")
        ok(st==['over','hex','plasma','low'],
           'the fill escalates as the field drains: %s' % ' -> '.join(st))
        pg.evaluate("() => window.BOSSMODE.stop()"); pg.wait_for_timeout(300)

        # ---- a boss with NO shield must not get the bar ----
        pg.evaluate(START, [1, 'boss'])
        f2=pg.evaluate("() => bossShieldFrac(window.BOSSMODE.boss)")
        ok(f2 is None, 'a boss with no shield returns null, so no bar is drawn (%s)' % f2)
        pg.screenshot(path=os.path.join(a.out,'02_boss_no_shield.png'), clip={'x':180,'y':160,'width':730,'height':190})
        pg.evaluate("() => window.BOSSMODE.stop()"); pg.wait_for_timeout(300)

        b.close()
    stop()
    if miss:
        from collections import Counter
        print('404s:'); [print('   %3d %s'%(n,u)) for u,n in Counter(miss).most_common(5)]
    print('\n%d ok / %d fail' % (n_ok[0], len(fails)))
    for f in fails: print('  FAIL', f)
    if errs:
        print('page errors (%d):' % len(errs))
        for e in errs[:8]: print('   ', e)
    sys.exit(1 if fails or errs else 0)

if __name__=='__main__':
    main()
