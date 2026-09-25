"""Measure Chrome Hammer's real entry, leap, ball and nova cadence by difficulty."""
import base64
import json
from pathlib import Path

import shoot as sh
from playwright.sync_api import sync_playwright

out = Path('_shots/hammer_difficulty_timeline_0925')
out.mkdir(parents=True, exist_ok=True)
port, stop = sh.serve(sh.GAME)
errors = []
rows = []
try:
    with sync_playwright() as pw:
        browser = pw.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
        page = browser.new_page(viewport={'width': 1100, 'height': 1200})
        page.on('pageerror', lambda e: errors.append(str(e)))
        page.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
        page.goto(f'http://127.0.0.1:{port}/index.html', wait_until='load')
        page.wait_for_function('() => (window.__bofFrames|0)>4')
        page.evaluate(sh.TRAP_RAF)
        for diff in ('normal', 'hard', 'furious'):
            page.evaluate(sh.SETUP, {'state': 'PLAY', 'stage': 5, 'pilot': 'cole', 'invuln': True})
            page.evaluate("""(diff) => {
              diffKey=diff;DIFF=DIFFS[diff];stagePlan=[];waveIdx=999;spawnClock=9999;
              enemies=[];eBullets=[];pBullets=[];subBoss=null;subBossActive=false;
              boss=null;bossActive=false;spawnBoss('chromehammer');bossActive=true;
              player.invuln=1e9;player.x=worldWidth()*.55;player.y=VH*.76;
              window.__hTransitions=[];window.__hLast='';window.__hTime=0;
              window.__qaTick=()=>{if(!boss||!boss._hammer)return;
                window.__hTime+=1/60;
                const h=boss._hammer,s=h.state;
                if(s!==window.__hLast){window.__hLast=s;
                  window.__hTransitions.push({time:+window.__hTime.toFixed(2),
                    state:s,cycle:h.attackCycle||0,follow:h.followCount||0,
                    bounces:h.ballBounces||0});}
              };
            }""", diff)
            peak_bounces = 0
            captured = set()
            for half in range(100):
                err = page.evaluate(sh.STEP, 30)
                if err:
                    errors.append(f'{diff} half-second {half}: {err}')
                    break
                state = page.evaluate("""() => ({state:boss._hammer.state,
                  bounces:boss._hammer.ballBounces||0,
                  nova:boss._hammer.novaShots||0,
                  shots:eBullets.length})""")
                peak_bounces = max(peak_bounces, state['bounces'])
                if state['state'] in ('ball', 'nova_release', 'whirlwind') and state['state'] not in captured:
                    captured.add(state['state'])
                    raw = page.evaluate("() => document.querySelector('#screen').toDataURL('image/png')")
                    (out / f'{diff}_{state["state"]}.png').write_bytes(base64.b64decode(raw.split(',', 1)[1]))
                if half % 8 == 0: page.wait_for_timeout(12)
            row = page.evaluate("""() => ({transitions:window.__hTransitions,
              hp:boss.hp,maxhp:boss.maxhp,finalState:boss._hammer.state,
              finalBounces:boss._hammer.ballBounces||0})""")
            row.update({'difficulty': diff, 'peakBounces': peak_bounces,
                        'captured': sorted(captured)})
            rows.append(row)
        browser.close()
finally:
    stop()

report = {'rows': rows, 'errors': errors}
(out / 'report.json').write_text(json.dumps(report, indent=2))
print(json.dumps(report, indent=2))
assert not errors
assert all(any(q['state'] == 'ball' for q in r['transitions']) for r in rows)
assert rows[1]['peakBounces'] > 0 and rows[2]['peakBounces'] > 0
