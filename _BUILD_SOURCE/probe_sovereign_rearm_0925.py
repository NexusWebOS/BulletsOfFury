"""Follow Storm Sovereign's three health-gated shield rearms in Chromium."""
import base64
import json
import sys
from pathlib import Path

import shoot as sh
from playwright.sync_api import sync_playwright

out = Path('_shots/sovereign_rearm_0925')
out.mkdir(parents=True, exist_ok=True)
diff = sys.argv[1] if len(sys.argv)>1 else 'furious'
assert diff in ('normal','hard','furious')
port, stop = sh.serve(sh.GAME)
errors, rows = [], []
try:
    with sync_playwright() as pw:
        browser = pw.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
        page = browser.new_page(viewport={'width': 1100, 'height': 1200})
        page.on('pageerror', lambda e: errors.append(str(e)))
        page.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
        page.goto(f'http://127.0.0.1:{port}/index.html', wait_until='load')
        page.wait_for_function('() => (window.__bofFrames|0)>4')
        page.evaluate(sh.TRAP_RAF)
        page.evaluate(sh.SETUP, {'state': 'PLAY', 'stage': 4, 'pilot': 'cole', 'invuln': True})
        page.evaluate("""(diff) => {
          diffKey=diff;DIFF=DIFFS[diff];stagePlan=[];waveIdx=999;spawnClock=9999;
          enemies=[];eBullets=[];pBullets=[];subBoss=null;subBossActive=false;
          boss=null;bossActive=false;spawnBoss('stormsovereign');bossActive=true;
          player.invuln=1e9;player.x=worldWidth()*.30;player.y=VH*.78;
        }""", diff)
        err = page.evaluate(sh.STEP, 180)
        if err: errors.append(f'entry: {err}')
        for gate in (75, 50, 25):
            deploy = []
            before = page.evaluate("""() => {
              const b=boss,S=b._s4war,H=S.shield;
              if(!H.active)throw Error('shield did not rearm before next gate');
              for(const n of H.nodes)stage4ShieldDestroyNode(b,n);
              b._noHit=false;b._phaseInvuln=0;
              _lastHitX=b.x;_lastHitY=b.y;_dmgBullet={kind:'mg',x:b.x,y:b.y};
              hitBoss(b.maxhp*.35);
              return {ratio:b.hp/b.maxhp,index:S.shieldThresholdIndex,
                rearming:H.rearming,shieldActive:H.active,mode:S.mode,
                finalGuns:S.finalGuns,coreUnlocked:S.coreUnlocked,
                coreTurrets:S.coreTurrets.length};
            }""")
            if gate==25:
                for frame in (15,18,18):
                    err = page.evaluate(sh.STEP, frame)
                    if err: errors.append(f'{gate}% deploy: {err}')
                    point = page.evaluate("""() => ({t:+boss._s4war.finalGunT.toFixed(2),
                      aimL:+boss._s4war.finalGunAimL.toFixed(2),
                      aimR:+boss._s4war.finalGunAimR.toFixed(2),
                      waves:boss._s4war.finalGunWave})""")
                    deploy.append(point)
                    tick = point['t']
                    raw = page.evaluate("() => document.querySelector('#screen').toDataURL('image/png')")
                    (out/f'{diff}_deploy_{tick:.2f}.png').write_bytes(base64.b64decode(raw.split(',',1)[1]))
                remaining = 84-51
            else:
                remaining = 84
            err = page.evaluate(sh.STEP, remaining)
            if err: errors.append(f'{gate}% rearm: {err}')
            after = page.evaluate("""() => {
              const S=boss._s4war,H=S.shield;
              return {ratio:boss.hp/boss.maxhp,index:S.shieldThresholdIndex,
                rearming:H.rearming,shieldActive:H.active,mode:S.mode,
                finalGuns:S.finalGuns,finalGunWave:S.finalGunWave,
                coreUnlocked:S.coreUnlocked,coreTurrets:S.coreTurrets.length};
            }""")
            raw = page.evaluate("() => document.querySelector('#screen').toDataURL('image/png')")
            (out/f'{diff}_gate_{gate}.png').write_bytes(base64.b64decode(raw.split(',',1)[1]))
            rows.append({'gate': gate, 'before': before, 'deploy': deploy, 'after': after})
        err = page.evaluate(sh.STEP, 180)
        if err: errors.append(f'late phase: {err}')
        late = page.evaluate("""() => ({finalGuns:boss._s4war.finalGuns,
          finalGunWave:boss._s4war.finalGunWave,coreShots:boss._s4war.coreShots})""")
        raw = page.evaluate("() => document.querySelector('#screen').toDataURL('image/png')")
        (out/f'{diff}_late_phase.png').write_bytes(base64.b64decode(raw.split(',',1)[1]))
        browser.close()
finally:
    stop()

report = {'difficulty':diff,'rows': rows, 'late': late, 'errors': errors}
(out/f'report_{diff}.json').write_text(json.dumps(report, indent=2))
print(json.dumps(report, indent=2))
assert not errors
assert [round(r['before']['ratio'],2) for r in rows] == [.75,.50,.25]
assert all(r['after']['shieldActive'] for r in rows)
assert rows[-1]['after']['finalGuns']=='active' and late['finalGunWave']>0
assert all(p['waves']==0 for p in rows[-1]['deploy'])
