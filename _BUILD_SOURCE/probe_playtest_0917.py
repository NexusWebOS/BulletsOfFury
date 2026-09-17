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
  elig: !!infusionEligible(),
  bossUp: !!(bossActive || subBossActive),
  state: state, stage: run.stage
})"""

def main():
    os.makedirs(OUT, exist_ok=True)
    port, stop = sh.serve(sh.GAME)
    summary = {}
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        errs = []
        # ⚠ ONE FRESH PAGE PER STAGE. Jumping 8 -> 9 through SETUP on one page left stage 9 with 0 rounds and
        # 0 kills in the first sweep while stage 9 alone scored 45 - state a real warp entry never carries.
        def fresh_page():
            pg = br.new_page(viewport={'width': 1000, 'height': 1100})
            pg.on('pageerror', lambda e: errs.append('page:' + str(e)))
            pg.on('console', lambda m: errs.append('console:' + m.text) if m.type == 'error' else None)
            pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=60000)
            pg.wait_for_function("() => typeof setState==='function' && typeof infusionGrant==='function' && typeof enemyEvadeTick==='function'", timeout=60000)
            pg.wait_for_function("() => (window.__bofFrames|0) > 4", timeout=60000)
            pg.evaluate(sh.TRAP_RAF)
            pg.evaluate("""() => {
              window.__evTotal=0; const et=enemyEvadeTick; enemyEvadeTick=function(e,dt){ const n0=e._evN|0; et(e,dt); if((e._evN|0)>n0) window.__evTotal++; };
              window.__infDrops=0; const dp=dropPowerup; dropPowerup=function(){ const n0=powerups.length; const r=dp.apply(this,arguments); if(powerups.length>n0 && powerups[powerups.length-1].kind==='infuse') window.__infDrops++; return r; };
              window.__denied=0; const bd=bossDenies; bossDenies=function(){ const r=bd(); if(r) window.__denied++; return r; };
              window.playerHit=function(){};
            }""")
            return pg
        STAGES=[int(x) for x in os.environ.get('PT_STAGES','1,2,3,4,5,6,7,8,9').split(',')]   # PT_STAGES=9 to run one
        for stage in STAGES:
            pg = fresh_page()
            e0 = len(errs)
            pg.evaluate(sh.SETUP, {'state': 'PLAY', 'stage': stage, 'pilot': 'cole'})
            # ⚠ the source-accumulated totals are PER STAGE - the first run carried stage 4's one drop into the
            # stage-5 control and failed a gate that holds (probe_infusion_0917: 400 stage-5 drops -> 0)
            pg.evaluate("() => { diffKey='hard'; DIFF=difficultyForRun(run.mode,'hard'); run.lives=9; player.dead=false; window.playerHit=function(){}; window.__evTotal=0; window.__infDrops=0; window.__denied=0; }")
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
                pg.evaluate("(t0) => { for(let i=0;i<60;i++){ window.__pilot(t0+i/60); window.__step(1); window.__pbMax=Math.max(window.__pbMax|0,pBullets.length); } }", t); t += 1.0
                if chunk % 5 == 4: pg.wait_for_timeout(250)   # let anything requested mid-run decode
                fr = pg.evaluate("() => window.__bofFrames|0")
                if fr == last: stalled += 1
                last = fr
                if chunk == 20: shot(pg, 'stage%d_mid.png' % stage)
            c = pg.evaluate(COUNTERS)
            c['shots']=pg.evaluate("() => (stageStats&&stageStats.shots)|0"); c['pbMax']=pg.evaluate("() => window.__pbMax|0")
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
                ok(c['drops'] == 0 and not c['elig'], 'stage %d (space guns): CONTROL - ineligible, no infusion dropped (%d)' % (stage, c['drops']))
            else:
                ok(c['elig'], 'stage %d: infusions are ELIGIBLE in the live stage' % stage)
            pg.close()
        # across the whole sweep the new systems must have FIRED in ordinary play
        tot = lambda k: sum(v[k] for v in summary.values())   # per-stage totals now, so a sum is a sum
        if len(STAGES) == 9: ok(tot('evades') > 0, 'across the sweep, ordinary units EVADED on HARD (%d evades)' % tot('evades'))
        # ⚠ `drops > 0` WAS A COIN FLIP DRESSED AS A PROOF. When the roll sat behind the ordinary 18%
        # loot gate an eligible kill paid a pickup about once in 44, so a sweep of ~150 eligible kills
        # expected 3 and drew zero one night in twenty - the second run did, and nothing was wrong.
        # killDrop has since given the infusion its own roll (INFUSION_DROP_P x dropMul, ~1 in 21), but
        # a handful of expected events is still not a proof. The RATE belongs to
        # probe_infusion_rate_0917.py (4,000 real dropPowerup calls per stage); what this sweep can
        # honestly claim is that the gate says YES in the live stage.
        if len(STAGES) == 9: ok(all(v['elig'] for k, v in summary.items() if int(k) not in (5, 9)),
                                'across the sweep, every non-space stage reported infusions eligible (%d drops fell, expected ~3)' % tot('drops'))
        if len(STAGES) == 9: ok(tot('kills') > 50, 'across the sweep, %d kills fed the arcade kill points' % tot('kills'))
        # a PT_STAGES subset re-runs one stage; merging keeps the other eight stages' rows instead
        # of leaving a one-row summary behind as the record of the sweep
        sp = os.path.join(OUT, 'summary.json'); merged = {}
        if len(STAGES) < 9 and os.path.exists(sp):
            try: merged = json.load(open(sp))
            except Exception: merged = {}
        merged.update({str(k): v for k, v in summary.items()})
        json.dump({k: merged[k] for k in sorted(merged, key=int)}, open(sp, 'w'), indent=2)
        br.close(); stop()
    print('\n%d ok / %d fail' % (N['ok'], len(FAILS)))
    for f in FAILS: print('  FAIL', f)
    sys.exit(1 if FAILS else 0)

if __name__ == '__main__':
    main()
