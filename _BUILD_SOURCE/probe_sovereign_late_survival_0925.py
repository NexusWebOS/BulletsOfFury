"""Measure Stage 4 final-gun pressure against a moving, shielded pilot."""
import json
import sys
from pathlib import Path

import shoot as sh
from playwright.sync_api import sync_playwright

out = Path('_shots/sovereign_late_survival_0925')
out.mkdir(parents=True, exist_ok=True)
port, stop = sh.serve(sh.GAME)
rows = []
try:
    with sync_playwright() as pw:
        browser = pw.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
        modes = ('still_left', 'still_center', 'still_right', 'cross', 'zigzag',
                 'still_center_no_guns', 'cross_no_guns', 'zigzag_no_guns')
        if len(sys.argv)>1:
            modes = tuple(m for m in modes if m.endswith('_no_guns'))
        for mode in modes:
            page = browser.new_page(viewport={'width': 1100, 'height': 1200})
            errors = []
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
            page.goto(f'http://127.0.0.1:{port}/index.html', wait_until='load')
            page.wait_for_function('() => (window.__bofFrames|0)>4')
            page.evaluate(sh.TRAP_RAF)
            page.evaluate(sh.SETUP, {'state':'PLAY','stage':4,'pilot':'cole','invuln':True})
            page.evaluate("""() => {
              diffKey='furious';DIFF=DIFFS.furious;stagePlan=[];waveIdx=999;spawnClock=9999;
              enemies=[];eBullets=[];pBullets=[];subBoss=null;subBossActive=false;
              boss=null;bossActive=false;spawnBoss('stormsovereign');bossActive=true;
              player.invuln=1e9;player.y=VH*.78;
            }""")
            err = page.evaluate(sh.STEP, 180)
            if err: errors.append(str(err))
            for gate in (75, 50, 25):
                page.evaluate("""() => {
                  const b=boss,H=b._s4war.shield;
                  for(const n of H.nodes)stage4ShieldDestroyNode(b,n);
                  b._noHit=false;b._phaseInvuln=0;
                  _lastHitX=b.x;_lastHitY=b.y;
                  _dmgBullet={kind:'mg',x:b.x,y:b.y};hitBoss(b.maxhp*.35);
                }""")
                err = page.evaluate(sh.STEP, 84)
                if err: errors.append(str(err))
            page.evaluate("""(mode) => {
              eBullets.length=0;run.shield=99;player.invuln=0;
              if(mode.endsWith('_no_guns'))boss._s4war.finalGuns='off';
              player.x=worldWidth()*(mode==='still_left'?.18:mode==='still_right'?.82:
                                   mode.startsWith('still_center')?.5:.18);
            }""", mode)
            for f in range(240):
                page.evaluate("""({mode,f}) => {
                  const W=worldWidth();
                  if(mode.startsWith('cross'))player.x=W*(.18+.64*Math.min(1,f/160));
                  if(mode.startsWith('zigzag'))player.x=W*(.5+.28*Math.sin(f/38));
                  player.y=VH*.78;
                }""", {'mode':mode,'f':f})
                err = page.evaluate(sh.STEP, 1)
                if err:
                    errors.append(str(err))
                    break
            data = page.evaluate("""() => ({
              hits:stageStats.dmgTaken,shield:run.shield,dead:player.dead,
              shots:boss._s4war.finalGunWave,helpers:boss._s4war.coreShots,
              bullets:eBullets.length,width:worldWidth(),playerX:player.x
            })""")
            rows.append({'mode':mode,**data,'errors':errors})
            page.close()
        browser.close()
finally:
    stop()

(out/('report_no_guns.json' if len(sys.argv)>1 else 'report.json')).write_text(json.dumps(rows,indent=2))
print(json.dumps(rows,indent=2))
assert all(not row['errors'] for row in rows)
