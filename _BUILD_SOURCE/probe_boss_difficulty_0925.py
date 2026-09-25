#!/usr/bin/env python3
"""Sample every campaign miniboss/boss in real Chromium on three difficulties.

This is a timed attack observation, not a claim of complete unassisted clears.
It keeps the player invulnerable and does not fire so each encounter can reveal
its normal attack selection without health gates being skipped.
"""
import base64
import json
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(ROOT, '_BUILD_SOURCE'))
import shoot as sh
from playwright.sync_api import sync_playwright

OUT = os.path.join(ROOT, '_shots', 'boss_difficulty_0925')

SET_BATTLE = """([stage,diff,role]) => {
  beginStage(stage);setState(GS.PLAY);diffKey=diff;
  DIFF=difficultyForRun(run.mode,diff);run.stage=stage;run.lives=9;
  player.invuln=1e9;player.dead=false;
  enemies.length=0;eBullets.length=0;pBullets.length=0;
  subBoss=null;subBossActive=false;boss=null;bossActive=false;
  stageTimer=curStage.length*.55;
  if(role==='mini')spawnSubBoss(SUBBOSS[stage].kind);
  else spawnBoss(curStage.boss);
  window.__reviewSeen=new WeakSet();window.__reviewShots=0;
  window.__reviewKinds={};window.__reviewPeak=0;window.__reviewRetina=0;
  return {stage,diff,role,kind:role==='mini'?subBoss&&subBoss.kind:boss&&boss.kind};
}"""
SAMPLE = """() => {
  const b=eBullets||[];window.__reviewPeak=Math.max(window.__reviewPeak,b.length);
  for(const q of b)if(q&&!window.__reviewSeen.has(q)){
    window.__reviewSeen.add(q);window.__reviewShots++;
    const k=String(q.kind||q._bfam||'unknown');
    window.__reviewKinds[k]=(window.__reviewKinds[k]||0)+1;
  }
  if(typeof groundTargetingFx!=='undefined')
    window.__reviewRetina=Math.max(window.__reviewRetina,groundTargetingFx.length);
}"""
RESULT = """() => ({
  state,shots:window.__reviewShots,peakBullets:window.__reviewPeak,
  bulletKinds:window.__reviewKinds,peakGroundWarnings:window.__reviewRetina,
  bossActive,subBossActive,
  hp:bossActive&&boss?boss.hp:subBossActive&&subBoss?subBoss.hp:null,
  phase:bossActive&&boss?(boss.phase||boss._phase||boss.state||null):
        subBossActive&&subBoss?(subBoss.phase||subBoss._phase||subBoss.state||null):null
})"""


def main():
    os.makedirs(OUT,exist_ok=True)
    port, stop = sh.serve(sh.GAME)
    rows=[]
    try:
        with sync_playwright() as pw:
            browser=pw.chromium.launch(args=['--disable-gpu','--no-sandbox','--mute-audio'])
            for stage in range(1,9):
                page=browser.new_page(viewport={'width':1100,'height':1200})
                errors=[]
                page.on('pageerror',lambda e:errors.append(str(e)))
                page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
                page.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load',timeout=60000)
                page.wait_for_function("() => typeof ASSETS!=='undefined' && (window.__bofFrames|0)>4",timeout=60000)
                page.evaluate(sh.TRAP_RAF)
                page.wait_for_timeout(50)
                page.evaluate(sh.SETUP,{'state':'PLAY','stage':stage,'pilot':'cole','invuln':True})
                for diff in ('normal','hard','furious'):
                    for role in ('mini','boss'):
                        if role=='mini' and not page.evaluate(f"() => !!SUBBOSS[{stage}]"):
                            continue
                        start=page.evaluate(SET_BATTLE,[stage,diff,role])
                        # The same simulator/draw path as normal play. Yield so
                        # lazy authored art has a chance to decode.
                        for i in range(18 if role=='mini' else 24):
                            err=page.evaluate(sh.STEP,30)
                            if err: raise RuntimeError(f'{start}: {err}')
                            page.evaluate(SAMPLE)
                            if i%3==0:page.wait_for_timeout(18)
                        row={**start,**page.evaluate(RESULT),'errors':errors[-4:]}
                        if diff=='furious':
                            raw=page.evaluate("() => document.querySelector('#screen').toDataURL('image/png')")
                            if raw:
                                with open(os.path.join(OUT,f'stage{stage}_{role}.png'),'wb') as f:
                                    f.write(base64.b64decode(raw.split(',',1)[1]))
                        rows.append(row)
                        print(json.dumps(row),flush=True)
                page.close()
            browser.close()
    finally:
        stop()
        with open(os.path.join(OUT,'results.json'),'w',encoding='utf-8') as f:
            json.dump(rows,f,indent=2)
        print('Observed',len(rows),'encounter samples',flush=True)


if __name__=='__main__': main()
