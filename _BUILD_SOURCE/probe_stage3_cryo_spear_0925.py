"""Verify the alternate Stage 3 Cryo Spear's shorter beam reel in Chromium."""
import base64
import json
from pathlib import Path

import shoot as sh
from playwright.sync_api import sync_playwright

out = Path('_shots/stage3_cryo_spear_0925')
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
            page.evaluate(sh.SETUP, {'state': 'PLAY', 'stage': 3, 'pilot': 'cole', 'invuln': True})
            init = page.evaluate("""(diff) => {
              diffKey=diff;DIFF=DIFFS[diff];stagePlan=[];waveIdx=999;spawnClock=9999;
              enemies=[];eBullets=[];pBullets=[];subBoss=null;subBossActive=false;
              boss=null;bossActive=false;spawnSubBoss__inner('rimewall');
              subBoss.enter=false;subBoss.t=3;subBoss.x=worldWidth()/2;
              subBoss.y=subBoss.ty;subBoss.fireCd=.05;subBossActive=true;
              player.x=worldWidth()*.3;player.y=VH*.72;
              return {kind:subBoss.kind,role:subBoss._s3boss.role};
            }""", diff)
            snapshots = []
            for i in range(30):
                err = page.evaluate(sh.STEP, 30)
                if err:
                    errors.append(f'{diff} frame {i*30}: {err}')
                    break
                if i in (5, 14, 23, 29):
                    data = page.evaluate("""() => ({t:+subBoss.t.toFixed(2),
                      patterns:subBoss._s3boss.patternsSeen,
                      cannons:subBoss._s3boss.cannonSeq&&subBoss._s3boss.cannonSeq.i,
                      beam:!!subBoss._l23Beam,shots:subBoss._s3boss.shots,
                      locks:playerLocks.length})""")
                    snapshots.append(data)
                    raw = page.evaluate("() => document.querySelector('#screen').toDataURL('image/png')")
                    (out / f'{diff}_{i:02}.png').write_bytes(base64.b64decode(raw.split(',', 1)[1]))
            rows.append({'difficulty': diff, 'init': init, 'snapshots': snapshots})
            if init != {'kind': 'rimewall', 'role': 'spear'}:
                errors.append(f'alternate spawn failed: {init}')
        browser.close()
finally:
    stop()

report = {'rows': rows, 'errors': errors}
(out / 'report.json').write_text(json.dumps(report, indent=2))
print(json.dumps(report, indent=2))
assert not errors
