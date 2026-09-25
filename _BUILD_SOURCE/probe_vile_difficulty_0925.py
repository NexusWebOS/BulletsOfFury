"""Compare live Stage 8 Form 1 sequencing and tracking across difficulties."""
import base64
import json
from pathlib import Path

import shoot as sh
from playwright.sync_api import sync_playwright

out = Path('_shots/vile_difficulty_0925')
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
        for diff in ('normal', 'hard', 'furious'):
            page.evaluate(sh.SETUP, {'state': 'PLAY', 'stage': 8, 'pilot': 'cole', 'invuln': True})
            page.evaluate("""(diff) => {
              diffKey=diff;DIFF=DIFFS[diff];stagePlan=[];waveIdx=999;spawnClock=9999;
              enemies=[];eBullets=[];pBullets=[];subBoss=null;subBossActive=false;
              boss=null;bossActive=false;spawnBoss('vileexistence');
              boss._scene=null;boss._symEntry=null;boss.enter=false;bossActive=true;
              boss.x=worldWidth()/2;boss.y=boss.ty;boss._mcd=.05;boss.flash=0;
              player.x=worldWidth()*.2;player.y=VH*.72;
              window.__vLog=[];window.__vSeen=new WeakSet();window.__vRockets=0;
              window.__qaTick=()=>{
                const S=boss&&boss._v24,P=S&&S.pattern;
                if(P&&!window.__vLog.some(q=>q.seq===S.seq))
                  window.__vLog.push({seq:S.seq,type:P.type,t:boss.t});
                for(const q of eBullets)if(q&&q._v24Kind==='rocket'&&!window.__vSeen.has(q)){
                  window.__vSeen.add(q);window.__vRockets++;
                }
              };
            }""", diff)
            for i in range(80):
                err = page.evaluate(sh.STEP, 1)
                if err:
                    errors.append(f'{diff}: {err}')
                    break
                if page.evaluate('() => !!(boss&&boss._v24&&boss._v24.pattern)'):
                    break
            first = page.evaluate("""() => ({
              type:boss._v24.pattern&&boss._v24.pattern.type,
              tx:boss._v24.pattern&&boss._v24.pattern.tx,
              px:player.x,t:boss._v24.pattern&&boss._v24.pattern.t})""")
            page.evaluate('() => {player.x=worldWidth()*.8;}')
            err = page.evaluate(sh.STEP, 16)
            if err: errors.append(f'{diff} follow: {err}')
            follow = page.evaluate("""() => ({tx:boss._v24.pattern&&boss._v24.pattern.tx,
              px:player.x,t:boss._v24.pattern&&boss._v24.pattern.t,
              locked:!!(boss._v24.pattern&&boss._v24.pattern.locked)})""")
            err = page.evaluate(sh.STEP, 18)
            if err: errors.append(f'{diff} commit: {err}')
            commit = page.evaluate("""() => ({tx:boss._v24.pattern&&boss._v24.pattern.tx,
              px:player.x,t:boss._v24.pattern&&boss._v24.pattern.t,
              locked:!!(boss._v24.pattern&&boss._v24.pattern.locked)})""")
            for i in range(24):
                err = page.evaluate(sh.STEP, 30)
                if err:
                    errors.append(f'{diff} combat {i}: {err}')
                    break
                if i % 5 == 0: page.wait_for_timeout(15)
            summary = page.evaluate("""() => ({sequence:window.__vLog,
              rockets:window.__vRockets,shots:boss._v24&&boss._v24.seq,
              liveBullets:eBullets.length})""")
            raw = page.evaluate("() => document.querySelector('#screen').toDataURL('image/png')")
            (out / f'{diff}.png').write_bytes(base64.b64decode(raw.split(',', 1)[1]))
            rows.append({'difficulty': diff, 'first': first,
                         'follow': follow, 'commit': commit, **summary})
        browser.close()
finally:
    stop()

report = {'rows': rows, 'errors': errors}
(out / 'report.json').write_text(json.dumps(report, indent=2))
print(json.dumps(report, indent=2))
assert not errors
assert [r['first']['type'] for r in rows] == ['rockets', 'rockets', 'laser']
assert rows[0]['follow']['tx'] == rows[0]['first']['tx']
assert rows[1]['follow']['tx'] > rows[1]['first']['tx']
assert rows[2]['follow']['tx'] > rows[2]['first']['tx']
