"""Inspect the live Rime Wall's Normal/Hard warning and tracking cadence."""
import base64
import json
from pathlib import Path

import shoot as sh
from playwright.sync_api import sync_playwright

out = Path('_shots/stage3_wall_targeting_0925')
out.mkdir(parents=True, exist_ok=True)
port, stop = sh.serve(sh.GAME)
rows = []
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
        for diff in ('normal', 'hard'):
            for health in ('full', 'half'):
                page.evaluate(sh.SETUP, {'state': 'PLAY', 'stage': 3, 'pilot': 'cole', 'invuln': True})
                page.evaluate("""([diff, health]) => {
                  diffKey=diff;DIFF=DIFFS[diff];stagePlan=[];waveIdx=999;spawnClock=9999;
                  enemies=[];eBullets=[];pBullets=[];subBoss=null;subBossActive=false;
                  boss=null;bossActive=false;spawnBoss('cryospear');
                  boss.enter=false;boss.t=3;boss.x=worldWidth()/2;boss.y=boss.ty;
                  boss.fireCd=.05;bossActive=true;
                  if(health==='half')boss.hp=boss.maxhp*.46;
                  player.x=worldWidth()*.28;player.y=VH*.72;
                }""", [diff, health])
                seen = []
                previous = ''
                peak_locks = 0
                for i in range(35):  # 17.5 seconds
                    err = page.evaluate(sh.STEP, 30)
                    if err:
                        errors.append(f'{diff}/{health} frame {i*30}: {err}')
                        break
                    sample = page.evaluate("""() => ({
                      t:+boss.t.toFixed(2),pat:boss._s3boss.lastPattern||null,
                      phase:shipBossPhase(boss),shots:boss._s3boss.shots,
                      lock:playerLocks.length,
                      activeLock:playerLocks.some(q=>q.state==='arming'||q.state==='locked'),
                      beam:!!boss._l23Beam,charge:!!boss._s3boss.charge,
                      volley:!!boss._s3boss.volley,cannons:!!boss._s3boss.cannonSeq,
                      warnings:groundTargetingFx.length,
                      bulletKinds:Object.keys(boss._s3boss.kinds),
                      patterns:boss._s3boss.patternsSeen
                    })""")
                    peak_locks = max(peak_locks, sample['lock'])
                    signature = (sample['pat'], sample['phase'], sample['beam'], sample['activeLock'])
                    if signature != previous:
                        seen.append(sample)
                        previous = signature
                    if i in (8, 16, 27):
                        raw = page.evaluate("() => document.querySelector('#screen').toDataURL('image/png')")
                        (out / f'{diff}_{health}_{i:02}.png').write_bytes(base64.b64decode(raw.split(',', 1)[1]))
                rows.append({'difficulty': diff, 'health': health,
                             'transitions': seen, 'peakLocks': peak_locks,
                             'final': sample})
        browser.close()
finally:
    stop()

report = {'rows': rows, 'errors': errors}
(out / 'report.json').write_text(json.dumps(report, indent=2))
print(json.dumps(report, indent=2))
assert not errors
