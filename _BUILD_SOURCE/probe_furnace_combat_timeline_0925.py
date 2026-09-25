"""Measure the Furnace Tyrant's intro and first real attack reels on N/H/F."""
import base64
import json
from pathlib import Path

import shoot as sh
from playwright.sync_api import sync_playwright

out = Path('_shots/furnace_combat_timeline_0925')
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
            page.evaluate(sh.SETUP, {'state': 'PLAY', 'stage': 2, 'pilot': 'cole', 'invuln': True})
            page.evaluate("""(diff) => {
              diffKey=diff;DIFF=DIFFS[diff];stagePlan=[];waveIdx=999;spawnClock=9999;
              enemies=[];eBullets=[];pBullets=[];subBoss=null;subBossActive=false;
              boss=null;bossActive=false;spawnBoss('infernoreaver');bossActive=true;
              player.invuln=1e9;player.x=worldWidth()*.32;player.y=VH*.76;
              window.__fSeen=new WeakSet();window.__fShots=0;
              window.__fTransitions=[];window.__fLast='';window.__fBeamFrames=0;
              window.__fTime=0;
              window.__qaTick=()=>{
                const F=boss&&boss._fz;if(!F)return;
                window.__fTime+=1/60;
                const signature=F.phase+':'+F.attack;
                if(signature!==window.__fLast){window.__fLast=signature;
                  window.__fTransitions.push({time:+window.__fTime.toFixed(2),
                    phase:F.phase,attack:F.attack});}
                if(F.beams&&F.beams.length)window.__fBeamFrames++;
                for(const q of eBullets)if(q&&!window.__fSeen.has(q)){
                  window.__fSeen.add(q);window.__fShots++;}
              };
            }""", diff)
            captured = set()
            for sec in range(1, 40):
                err = page.evaluate(sh.STEP, 60)
                if err:
                    errors.append(f'{diff} second {sec}: {err}')
                    break
                current = page.evaluate("""() => ({phase:boss._fz.phase,
                  attack:boss._fz.attack,beams:boss._fz.beams.length,
                  shots:window.__fShots})""")
                if current['phase'] == 'arms' and current['attack'] not in captured:
                    captured.add(current['attack'])
                    raw = page.evaluate("() => document.querySelector('#screen').toDataURL('image/png')")
                    (out / f'{diff}_{current["attack"]}.png').write_bytes(base64.b64decode(raw.split(',', 1)[1]))
                if sec % 5 == 0: page.wait_for_timeout(15)
            summary = page.evaluate("""() => ({transitions:window.__fTransitions,
              shots:window.__fShots,beamFrames:window.__fBeamFrames,
              phase:boss._fz.phase,attack:boss._fz.attack})""")
            rows.append({'difficulty': diff, 'captured': sorted(captured), **summary})
        browser.close()
finally:
    stop()

report = {'rows': rows, 'errors': errors}
(out / 'report.json').write_text(json.dumps(report, indent=2))
print(json.dumps(report, indent=2))
assert not errors
assert all(any(q['phase'] == 'arms' for q in r['transitions']) for r in rows)
