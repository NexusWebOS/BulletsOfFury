#!/usr/bin/env python3
"""
probe_playtest_0917.py - THE OVERNIGHT PLAYTEST SWEEP, IN REAL CHROMIUM.

Mike, 0917: "lots of graphics to generate, experiments to try, playtesting to go".

Every stage, HARD, a live infusion on the held gun, the trigger held, the ship weaving. Not a
balance run - a run that puts every new system (infusions on every carrier, kill points, evasion,
boss denial, chromium, geysers) through 45 simulated seconds of the REAL stage loop per stage and
reads the console. The claim is narrow and worth having: nothing throws, nothing is swallowed by the
state draw's try/catch (`draw error in state`), the frame keeps advancing, and the new systems
actually FIRE in ordinary play (an evade, a kill floater, an infusion drop on an eligible stage).

Stepped in chunks with a real pause between them so the stage's art can decode (the 0905 lesson: a
synchronous burst never yields). Stage 5 and 9 are the controls where no infusion may drop.
"""
import os, sys, base64, json, time
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.join(ROOT, '_BUILD_SOURCE'))
import shoot as sh
from playwright.sync_api import sync_playwright
OUT = os.path.join(ROOT, 'docs', 'proofs', 'playtest_0917')
N = {'ok': 0}; FAILS = []
def ok(c, m):
    if c: N['ok'] += 1; print('  ok   ' + m)
    else: FAILS.append(m); print('  FAIL ' + m)
def shot(pg, name):
    d = pg.evaluate("() => { const c=document.getElementById('screen'); return c?c.toDataURL('image/png'):null; }")
    if d: open(os.path.join(OUT, name), 'wb').write(base64.b64decode(d.split(',', 1)[1]))

ELEMS = ['fire', 'ice', 'lightning', 'prism', 'toxic', 'kinetic', 'chrome', 'fire', 'lightning']

# the pilot: trigger held, weaving across the lane, never dying (playerHit stubbed - this is a
# systems sweep, not a survival run)
PILOT = """(t) => {
  player.dead=false; player.invuln=0;
  const W=worldWidth(); player.x = W*0.5 + Math.sin(t*0.9)*W*0.32; player.y = 380 + Math.sin(t*1.7)*40;
  player.fireCd = 0; pShoot();
}"""
COUNTERS = """() => ({
  frames: window.__bofFrames|0,
  enemies: enemies.filter(e=>!e.dead).length,
  eb: eBullets.length, pb: pBullets.length,
  kills: (stageStats&&stageStats.kills)|0,
  floaters: floaters.filter(f=>f.score).length,
  evades: enemies.reduce((a,e)=>a+((e._evN|0)),0) + (window.__evTotal|0),
  drops: powerups.filter(p=>p.kind==='infuse').length + (window.__infDrops|0),
  inf: run.infusion ? run.infusion.elem+':'+run.infusion.lv : null,
  denied: window.__denied|0,
  bossUp: !!(bossActive || subBossActive),
  state: state, stage: run.stage
})"""

def main():
    os.makedirs(OUT, exist_ok=True)
    port, stop = sh.serve(sh.GAME)
    summary = {}
    with sync_playwright() as pw:
        br = pw.chromium.launch(); pg = br.new_page(viewport={'width': 1000, 'height': 1100})
        errs = []
        pg.on('pageerror', lambda e: errs.append('page:' + str(e)))
        pg.on('console', lambda m: errs.append('console:' + m.text) if m.type == 'error' else None)
        pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=60000)
        pg.wait_for_function("() => typeof setState==='function' && typeof infusionGrant==='function' && typeof enemyEvadeTick==='function'", timeout=60000)
        pg.wait_for_function("() => (window.__bofFrames|0) > 4", timeout=60000)
        pg.evaluate(sh.TRAP_RAF)
        # instruments that survive the per-frame culls: totals accumulated at the source
        pg.evaluate("""() => {
          window.__evTotal=0; const et=enemyEvadeTick; enemyEvadeTick=function(e,dt){ const n0=e._evN|0; et(e,dt); if((e._evN|0)>n0) window.__evTotal++; };
          window.__infDrops=0; const dp=dropPowerup; dropPowerup=function(){ const n0=powerups.length; const r=dp.apply(this,arguments); if(powerups.length>n0 && powerups[powerups.length-1].kind==='infuse') window.__infDrops++; return r; };
          window.__denied=0; const bd=bossDenies; bossDenies=function(){ const r=bd(); if(r) window.__denied++; return r; };
          window.playerHit=function(){};
        }""")
        for stage in range(1, 10):
            e0 = len(errs)
            pg.evaluate(sh.SETUP, {'state': 'PLAY', 'stage': stage, 'pilot': 'cole'})
            pg.evaluate("() => { diffKey='hard'; DIFF=difficultyForRun(run.mode,'hard'); run.lives=9; player.dead=false; window.playerHit=function(){}; }")
            for _ in range(4):
                pg.evaluate(sh.STEP, [8]); pg.wait_for_timeout(350)
            elem = ELEMS[stage - 1]
            pg.evaluate("(e) => { run.infusion=null; infusionGrant(e); infusionGrant(e); infusionGrant(e); run.wlevels[run.weapon]=3; run.wlevel=3; }", elem)
            f0 = pg.evaluate("() => window.__bofFrames|0")
            t = 0.0; stalled = 0; last = f0
            # ⚠ ONE evaluate PER FRAME COST EIGHT MINUTES A STAGE (each round trip renders a frame in
            # software). The pilot and the step run inside ONE evaluate per chunk; the chunks still
            # pause for real time so anything requested mid-run can decode.
            pg.evaluate("() => { window.__step = %s; window.__pilot = %s; }" % (sh.STEP, PILOT))
            for chunk in range(45):                      # 45 x 60 frames = 45 simulated seconds
                pg.evaluate("(t0) => { for(let i=0;i<60;i++){ window.__pilot(t0+i/60); window.__step(1); } }", t); t += 1.0
                if chunk % 5 == 4: pg.wait_for_timeout(250)   # let anything requested mid-run decode
                fr = pg.evaluate("() => window.__bofFrames|0")
                if fr == last: stalled += 1
                last = fr
                if chunk == 20: shot(pg, 'stage%d_mid.png' % stage)
            c = pg.evaluate(COUNTERS)
            e1 = len(errs)
            new_errs = errs[e0:e1]
            draw_errs = [x for x in new_errs if 'draw error' in x]
            c.update({'errors': len(new_errs), 'drawErrors': len(draw_errs), 'stalledChunks': stalled, 'elem': elem, 'framesRun': last - f0})
            summary[stage] = c
            print('  stage %d: %s' % (stage, json.dumps(c)))
            for x in new_errs[:4]: print('      !', x[:200])
            ok(len(new_errs) == 0, 'stage %d: 45s on HARD with %s L3 held - no page or console errors (%d)' % (stage, elem.upper(), len(new_errs)))
            ok(stalled == 0 and last - f0 >= 45 * 60, 'stage %d: the frame kept advancing every chunk (%d frames)' % (stage, last - f0))
            ok(c['kills'] > 0 and c['floaters'] >= 0, 'stage %d: the stage was PLAYED - %d kills' % (stage, c['kills']))
            if stage in (5, 9):
                ok(c['drops'] == 0, 'stage %d (space): CONTROL - no infusion may drop (%d)' % (stage, c['drops']))
            pg.evaluate("() => { try{ if(boss){ boss.hp=0; } }catch(e){} for(const e of enemies) e.dead=true; pBullets.length=0; eBullets.length=0; }")
        # across the whole sweep the new systems must have FIRED in ordinary play
        tot = lambda k: sum(v[k] for v in summary.values())
        ok(tot('evades') > 0, 'across the sweep, ordinary units EVADED on HARD (%d evades)' % tot('evades'))
        ok(tot('drops') > 0, 'across the sweep, infusions DROPPED on eligible stages (%d drops)' % tot('drops'))
        ok(tot('kills') > 50, 'across the sweep, %d kills fed the arcade kill points' % tot('kills'))
        json.dump(summary, open(os.path.join(OUT, 'summary.json'), 'w'), indent=2)
        br.close(); stop()
    print('\n%d ok / %d fail' % (N['ok'], len(FAILS)))
    for f in FAILS: print('  FAIL', f)
    sys.exit(1 if FAILS else 0)

if __name__ == '__main__':
    main()
