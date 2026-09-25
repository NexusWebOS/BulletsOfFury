"""Measure Frost Cruiser's real attack mix beyond the short opening sample."""
import base64
import json
from pathlib import Path

import shoot as sh
from playwright.sync_api import sync_playwright

out = Path('_shots/frost_cruiser_timeline_0925')
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
            page.evaluate(sh.SETUP, {'state': 'PLAY', 'stage': 3, 'pilot': 'cole', 'invuln': True})
            page.evaluate("""(diff) => {
              diffKey=diff;DIFF=DIFFS[diff];stagePlan=[];waveIdx=999;spawnClock=9999;
              enemies=[];eBullets=[];pBullets=[];boss=null;bossActive=false;
              subBoss=null;subBossActive=false;spawnSubBoss('frostcruiser');
              player.invuln=1e9;player.x=worldWidth()*.33;player.y=VH*.77;
              window.__fcTime=0;window.__fcSeen=new WeakSet();window.__fcShots={};
              window.__fcTransitions=[];window.__fcLast='';window.__fcBeamFrames=0;
              window.__qaTick=()=>{
                const b=subBoss,J=b&&b._jc;if(!J)return;
                window.__fcTime+=1/60;
                if(J.state!==window.__fcLast){window.__fcLast=J.state;
                  window.__fcTransitions.push({time:+window.__fcTime.toFixed(2),state:J.state});}
                if(J.beamActive)window.__fcBeamFrames++;
                for(const q of eBullets)if(q&&!window.__fcSeen.has(q)){
                  window.__fcSeen.add(q);const k=String(q.kind||'unknown');
                  window.__fcShots[k]=(window.__fcShots[k]||0)+1;}
              };
            }""", diff)
            captured = set()
            # Furious intentionally nukes this hull and replaces it with Thermocloud.
            # Capture that handoff instead of treating it as a 35-second cruiser duel.
            for half_sec in range(12 if diff == 'furious' else 70):
                err = page.evaluate(sh.STEP, 30)
                if err:
                    errors.append(f'{diff} {half_sec/2:.1f}s: {err}')
                    break
                state = page.evaluate("() => subBoss&&subBoss._jc&&subBoss._jc.state")
                if state in ('iceOrbCharge', 'frostRocketCharge', 'gunSlide', 'beamSweep',
                             'furyChargeWarn', 'furyDash') and state not in captured:
                    captured.add(state)
                    raw = page.evaluate("() => document.querySelector('#screen').toDataURL('image/png')")
                    (out/f'{diff}_{state}.png').write_bytes(base64.b64decode(raw.split(',',1)[1]))
                if half_sec % 8 == 0:
                    page.wait_for_timeout(15)
            row = page.evaluate("""() => ({transitions:window.__fcTransitions,
              shots:window.__fcShots,beamFrames:window.__fcBeamFrames,
              lastState:subBoss&&subBoss._jc?subBoss._jc.state:null,
              currentKind:subBoss&&subBoss.kind,
              hardVariant:subBoss&&subBoss._jc?subBoss._jc.hardVariant:null,
              width:subBoss&&subBoss.w})""")
            rows.append({'difficulty': diff, 'captured': sorted(captured), **row})
        browser.close()
finally:
    stop()

report = {'rows': rows, 'errors': errors}
(out/'report.json').write_text(json.dumps(report, indent=2))
print(json.dumps(report, indent=2))
assert not errors
assert all(r['transitions'] for r in rows)
