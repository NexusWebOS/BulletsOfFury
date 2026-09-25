"""Check all three Furious edge sweeps leave the displayed lower safe lane open."""
import base64
import json
from pathlib import Path

import shoot as sh
from playwright.sync_api import sync_playwright

out = Path('_shots/overlord_sweep_lane_0925')
out.mkdir(parents=True, exist_ok=True)
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
        for px in (100, 240, 380):
            page.evaluate(sh.SETUP, {'state': 'PLAY', 'stage': 1, 'pilot': 'cole', 'invuln': True})
            page.evaluate("""(px) => {
              diffKey='furious';DIFF=DIFFS.furious;stagePlan=[];waveIdx=999;spawnClock=9999;
              enemies=[];eBullets=[];pBullets=[];subBoss=null;subBossActive=false;
              boss=null;bossActive=false;spawnBoss('damkeeper');bossActive=true;
              boss.enter=false;if(boss._ovIntro)boss._ovIntro.done=true;
              player.invuln=1e9;player.x=px;player.y=VH*.84;
              ovStartSweep(boss);
              window.__ovSamples=[];window.__ovSeen=new WeakSet();window.__ovMaxPass=0;
              window.__qaTick=()=>{
                const S=boss&&boss._ovSweep;if(!S)return;
                window.__ovMaxPass=Math.max(window.__ovMaxPass,S.pass);
                for(const q of eBullets)if(q&&q.kind==='mg'&&!window.__ovSeen.has(q)){
                  window.__ovSeen.add(q);
                  const reach=S.safeY-q.y,impact=q.x+reach*q.vx/Math.max(.01,q.vy);
                  window.__ovSamples.push({pass:S.pass,x:q.x,y:q.y,impact:impact,
                    lane:S.safeX,radius:S.safeR});
                }
              };
            }""", px)
            for second in range(14):
                err = page.evaluate(sh.STEP, 60)
                if err:
                    errors.append(f'x={px} t={second}: {err}')
                    break
                if px == 240 and not (out/'middle_lane_pass.png').exists() and page.evaluate("() => boss._ovSweep&&boss._ovSweep.pass===1"):
                    raw = page.evaluate("() => document.querySelector('#screen').toDataURL('image/png')")
                    (out/'middle_lane_pass.png').write_bytes(base64.b64decode(raw.split(',',1)[1]))
                if page.evaluate("() => !boss._ovSweep"):
                    break
            row = page.evaluate("""() => {
              const list=window.__ovSamples;
              const intrusions=list.filter(q=>Math.abs(q.impact-q.lane)<q.radius-8);
              const byPass=[0,1,2].map(n=>list.filter(q=>q.pass===n).length);
              return {rounds:list.length,byPass:byPass,passes:window.__ovMaxPass+1,
                intrusions:intrusions.length,examples:intrusions.slice(0,4),
                safeX:list[0]&&list[0].lane,safeRadius:list[0]&&list[0].radius,
                nextState:boss._ovState};
            }""")
            rows.append({'playerX': px, **row})
        browser.close()
finally:
    stop()

report = {'rows': rows, 'errors': errors}
(out/'report.json').write_text(json.dumps(report, indent=2))
print(json.dumps(report, indent=2))
assert not errors
assert all(r['rounds']>0 and r['passes']==3 for r in rows)
