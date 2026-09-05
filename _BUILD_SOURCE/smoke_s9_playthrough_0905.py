#!/usr/bin/env python3
"""smoke_s9_playthrough_0905.py - can Mike actually SIT DOWN AND PLAY this build?

Everything else verified today answers "does it draw" or "does the state look right". Neither
catches the thing that would actually ruin a test session: a crash, or a stall, somewhere in the
middle of a real stage-9 run. The Event Horizon in particular has been verified to DRAW and to
take damage from all three space weapons - but nobody has fought it: entered, broken it to the
50% skin swap, killed it, and watched the stage carry on to the boss.

So this plays the stage. Fire held, horizontal tracking, real chunked stepping, and it records
every page error plus the order the encounters actually fire in.

⚠ IT IS NOT A SKILL TEST AND MUST NOT BE READ AS ONE. The autopilot cannot dodge; `invuln` is on
so it cannot die. What it proves is that the run REACHES its beats and nothing throws - not that
the fight is fair, fun, or the right length. Only Mike at the controls answers that.

⚠ STEP IN CHUNKS WITH A REAL PAUSE. STEP advances a synthetic clock in one tight loop, so a run
that never yields gives the browser no wall time to decode the stage-9 plates - and this build's
whole point is that an undecoded plate now draws NOTHING rather than a ground tank, which would
make a non-yielding run look empty and "pass" for the wrong reason.
"""
import sys, os, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shoot as sh
from playwright.sync_api import sync_playwright

WARM = """() => { const hit=k=>k.indexOf('ns9')===0||k.indexOf('s9atk_')===0;
  const w=[]; if(window.BOFX&&BOFX.cells) for(const k in BOFX.cells) if(hit(k)) w.push(k);
  if(XART._src) for(const k in XART._src) if(hit(k)) w.push(k);
  window.__w=Array.from(new Set(w)); for(const k of window.__w){try{XART._touch(k);}catch(e){}}
  return window.__w.length; }"""
READY = """() => { const ks=window.__w||[]; let n=0; for(const k of ks) if(XART.rdy(k)) n++;
  return ks.length?n/ks.length:1; }"""

QA = r"""
() => {
  window.__s = {log:[], err:null, seen:{}, maxT:0, minibossSkin:null};
  const S = window.__s;
  if (typeof run !== 'undefined') { run.spaceLevels=[5,5,5]; run.spaceWeapon=0; run.wlevel=5; }
  const K=(k,d)=>window.dispatchEvent(new KeyboardEvent(d?'keydown':'keyup',{key:k,bubbles:true}));
  K('j',true);
  let held=null;
  const note=(m)=>{ if(!S.seen[m]){ S.seen[m]=1;
    S.log.push(((typeof stageTimer!=='undefined')?stageTimer.toFixed(1):'?')+'s  '+m); } };
  window.__qaTick=function(){
    try{
      const t=(typeof stageTimer!=='undefined')?stageTimer:0;
      if(t>S.maxT) S.maxT=t;
      let best=null,bd=1e9;
      for(const e of enemies){ if(!e||e.dead||e._prop) continue;
        const d=Math.abs(e.x-player.x)+Math.max(0,e.y)*0.35; if(d<bd){bd=d;best=e;} }
      if(typeof subBoss!=='undefined'&&subBoss&&!subBoss.dead&&subBossActive) best=subBoss;
      if(typeof boss!=='undefined'&&boss&&!boss.dead&&bossActive) best=boss;
      const want=best?(best.x<player.x-8?'a':(best.x>player.x+8?'d':null)):null;
      if(want!==held){ if(held)K(held,false); if(want)K(want,true); held=want; }

      if(typeof subBossTriggered!=='undefined'&&subBossTriggered) note('miniboss WARNED');
      if(typeof subBossActive!=='undefined'&&subBossActive&&subBoss){
        note('miniboss ON SCREEN: '+subBoss.kind+' "'+subBoss.name+'"');
        const F=subBoss._s9rift;
        if(F&&F.core){
          if(F.core.hp<=F.core.maxhp*0.5){ note('miniboss BLACK PHASE (<=50% hp)'); S.minibossSkin='black'; }
          if(F.core.hp<=F.core.maxhp*0.2) note('miniboss under 20% hp');
        }
      }
      if(typeof subBossDone!=='undefined'&&subBossDone) note('miniboss DEFEATED, stage resumed');
      if(typeof bossWarned!=='undefined'&&bossWarned) note('BOSS warned');
      if(typeof bossActive!=='undefined'&&bossActive&&boss) note('BOSS on screen: '+(boss.kind||'?'));
      if(typeof bossDefeated!=='undefined'&&bossDefeated) note('BOSS defeated');
    }catch(e){ S.err=String(e&&e.message||e); }
  };
  return true;
}
"""
STATE = """() => ({t:(typeof stageTimer!=='undefined')?stageTimer:-1,
  sub:(typeof subBossActive!=='undefined'&&subBossActive),
  done:(typeof subBossDone!=='undefined'&&subBossDone),
  boss:(typeof bossActive!=='undefined'&&bossActive),
  bd:(typeof bossDefeated!=='undefined'&&bossDefeated),
  n:(typeof enemies!=='undefined')?enemies.length:-1})"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--seconds', type=float, default=240)
    a = ap.parse_args()
    port, stop = sh.serve(sh.GAME)
    try:
        with sync_playwright() as pw:
            b = pw.chromium.launch(args=['--autoplay-policy=no-user-gesture-required'])
            pg = b.new_page(viewport={'width': 480, 'height': 512})
            errs = []
            pg.on('pageerror', lambda e: errs.append(str(e)))
            pg.goto('http://127.0.0.1:%d/index.html' % port)
            pg.wait_for_function('typeof ASSETS!=="undefined" && typeof loop==="function"', timeout=30000)
            pg.wait_for_timeout(2500)
            r = pg.evaluate(sh.SETUP, {'state': 'PLAY', 'stage': 9, 'pilot': 'cole', 'invuln': True})
            if not r.get('ok'):
                raise SystemExit('setup failed: %s' % r)
            n = pg.evaluate(WARM)
            try:
                pg.wait_for_function('(' + READY + ')() >= 0.90', timeout=25000)
            except Exception:
                pass
            print('warmed %d stage-9 keys, %.0f%% ready' % (n, pg.evaluate(READY) * 100))
            pg.evaluate(sh.TRAP_RAF)
            pg.evaluate(QA)
            total, done, chunk = int(a.seconds * 60), 0, 240
            last = None
            while done < total:
                err = pg.evaluate(sh.STEP, min(chunk, total - done))
                if err:
                    print('\n** STEP THREW at frame %d: %s' % (done, err))
                    break
                done += chunk
                pg.wait_for_timeout(35)
                st = pg.evaluate(STATE)
                if st['bd']:
                    print('\nstage completed (boss defeated) at %.1fs of stage clock' % st['t'])
                    break
                last = st
            s = pg.evaluate('() => window.__s')
            b.close()
    finally:
        stop()

    print('\n--- WHAT ACTUALLY HAPPENED IN THE RUN -----------------------------------')
    if not s['log']:
        print('  (no encounter beat was reached at all)')
    for line in s['log']:
        print('  ' + line)
    print('\n  furthest stage clock reached: %.1fs' % s['maxT'])
    if last:
        print('  final state: %s' % last)
    if s.get('err'):
        print('\n  ** qaTick threw: %s' % s['err'])
    if errs:
        print('\n  ** %d PAGE ERRORS. first three:' % len(errs))
        for e in errs[:3]:
            print('     %s' % e[:200])
    else:
        print('\n  no page errors in the whole run.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
