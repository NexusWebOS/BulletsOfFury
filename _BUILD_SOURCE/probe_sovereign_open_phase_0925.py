"""Observe Stage-4 boss attacks after its four shield nodes are destroyed."""
import base64
import json
from pathlib import Path

import shoot as sh
from playwright.sync_api import sync_playwright

out = Path('_shots/sovereign_open_phase_0925')
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
        for diff in ('normal', 'hard', 'furious'):
            page.evaluate(sh.SETUP, {'state': 'PLAY', 'stage': 4, 'pilot': 'cole', 'invuln': True})
            page.evaluate("""(diff) => {
              diffKey=diff;DIFF=DIFFS[diff];stagePlan=[];waveIdx=999;spawnClock=9999;
              enemies=[];eBullets=[];pBullets=[];subBoss=null;subBossActive=false;
              boss=null;bossActive=false;spawnBoss('stormsovereign');bossActive=true;
              player.invuln=1e9;player.x=worldWidth()*.31;player.y=VH*.78;
            }""", diff)
            err = page.evaluate(sh.STEP, 60*3)
            if err: errors.append(f'{diff} entry: {err}')
            opened = page.evaluate("""() => {
              const S=boss&&boss._s4war,H=S&&S.shield;
              if(!H||!H.active)throw Error('shield missing');
              const n=H.nodes.length;
              for(const q of H.nodes)stage4ShieldDestroyNode(boss,q);
              window.__soTime=0;window.__soSeen=new WeakSet();window.__soShots={};
              window.__soTransitions=[];window.__soLast='';window.__soGiant=0;
              window.__qaTick=()=>{
                const S=boss&&boss._s4war;if(!S)return;
                window.__soTime+=1/60;
                if(S.mode!==window.__soLast){window.__soLast=S.mode;
                  window.__soTransitions.push({time:+window.__soTime.toFixed(2),mode:S.mode});}
                if(S.giantStrike)window.__soGiant++;
                for(const q of eBullets)if(q&&!window.__soSeen.has(q)){
                  window.__soSeen.add(q);const k=String(q.kind||'unknown');
                  window.__soShots[k]=(window.__soShots[k]||0)+1;}
              };
              return {nodes:n,shieldActive:H.active,mode:S.mode};
            }""")
            captured = set()
            for half_sec in range(70):
                err = page.evaluate(sh.STEP, 30)
                if err:
                    errors.append(f'{diff} {half_sec/2:.1f}s: {err}')
                    break
                mode = page.evaluate("() => boss&&boss._s4war&&boss._s4war.mode")
                if mode in ('burst','flyaway','lightning','giantStrike') and mode not in captured:
                    captured.add(mode)
                    raw = page.evaluate("() => document.querySelector('#screen').toDataURL('image/png')")
                    (out/f'{diff}_{mode}.png').write_bytes(base64.b64decode(raw.split(',',1)[1]))
                if half_sec % 8 == 0: page.wait_for_timeout(15)
            row = page.evaluate("""() => ({transitions:window.__soTransitions,
              shots:window.__soShots,giantFrames:window.__soGiant,
              chainCycles:boss._s4war.chainCycles,chainBolts:boss._s4war.chainBolts,
              chainOrbs:boss._s4war.chainOrbs,giantCount:boss._s4war.giantStrikeCount,
              finalMode:boss._s4war.mode})""")
            rows.append({'difficulty': diff, 'opened': opened, 'captured': sorted(captured), **row})
        browser.close()
finally:
    stop()

report = {'rows': rows, 'errors': errors}
(out/'report.json').write_text(json.dumps(report, indent=2))
print(json.dumps(report, indent=2))
assert not errors
assert all(not r['opened']['shieldActive'] for r in rows)
