"""Check live Stage-5 giant-strike missile, bullet and roll response routes."""
import json
from pathlib import Path

import shoot as sh
from playwright.sync_api import sync_playwright

out = Path('_shots/hammer_orbital_counters_0925')
out.mkdir(parents=True, exist_ok=True)
port, stop = sh.serve(sh.GAME)
errors = []
try:
    with sync_playwright() as pw:
        browser = pw.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
        page = browser.new_page(viewport={'width': 1100, 'height': 1200})
        page.on('pageerror', lambda e: errors.append(str(e)))
        page.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
        page.goto(f'http://127.0.0.1:{port}/index.html', wait_until='load')
        page.wait_for_function('() => (window.__bofFrames|0)>4')
        page.evaluate(sh.TRAP_RAF)
        page.evaluate(sh.SETUP, {'state': 'PLAY', 'stage': 5, 'pilot': 'cole', 'invuln': True})
        result = page.evaluate("""() => {
          diffKey='furious';DIFF=DIFFS.furious;stagePlan=[];waveIdx=999;spawnClock=9999;
          enemies=[];eBullets=[];pBullets=[];subBoss=null;subBossActive=false;
          boss=null;bossActive=false;spawnBoss('chromehammer');bossActive=true;
          const b=boss,h=b._hammer;
          b.enter=false;b._noHit=false;b.x=worldWidth()*.5;b.y=VH*.35;
          player.invuln=0;player.dead=false;player.alive=true;player.x=b.x;player.y=VH*.77;
          run.shield=0;
          hammerState(b,'giant_dive');h.giantLeft=2;h.giantFromX=b.x;h.giantFromY=b.y;
          h.tx=player.x;h.ty=player.y;
          const bullet={kind:'mg',x:b.x,y:b.y,vx:0,vy:-6,_hit:[]};
          const reflected=hammerDiveReflect(b,bullet);
          const reflectedRound={reflected,flag:bullet._enemyReflected,vx:bullet.vx,vy:bullet.vy,
            headsTowardPilot:bullet.vy>0};
          const hitbox=bossHitTest(b.x,b.y);
          _lastHitX=b.x;_lastHitY=b.y;_dmgBullet={kind:'gmiss',x:b.x,y:b.y,vx:0,vy:-7};
          const oldHp=b.hp;hitBoss(10);
          const missile={hitbox,oldHp,newHp:b.hp,state:h.state,countered:h.countered};
          player.invuln=0;startRoll(1);
          const roll={started:!!player.roll,invuln:player.invuln};
          playerHit();roll.survived=!player.dead;
          return {reflectedRound,missile,roll};
        }""")
        err = page.evaluate(sh.STEP, 1)
        if err: errors.append(err)
        browser.close()
finally:
    stop()

report = {'result': result, 'errors': errors}
(out/'report.json').write_text(json.dumps(report, indent=2))
print(json.dumps(report, indent=2))
assert not errors
assert result['reflectedRound']['reflected'] and result['reflectedRound']['headsTowardPilot']
assert result['missile']['hitbox'] and result['missile']['countered']
assert result['missile']['state'] == 'giant_knockback'
assert result['roll']['started'] and result['roll']['survived']
