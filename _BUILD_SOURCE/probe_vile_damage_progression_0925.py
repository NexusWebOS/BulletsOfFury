"""Damage-gate all four live Stage 8 forms in Chromium and inspect each morph."""
import base64
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import shoot as sh
from playwright.sync_api import sync_playwright

out = Path('_shots/vile_damage_progression_0925')
out.mkdir(parents=True, exist_ok=True)
port, stop = sh.serve(sh.GAME)
errors = []
report = {'forms': []}
try:
    with sync_playwright() as pw:
        browser = pw.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
        page = browser.new_page(viewport={'width': 1100, 'height': 1200})
        page.on('pageerror', lambda e: errors.append(str(e)))
        page.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
        page.goto(f'http://127.0.0.1:{port}/index.html', wait_until='load')
        page.wait_for_function('() => (window.__bofFrames|0)>4')
        page.evaluate(sh.TRAP_RAF)
        page.evaluate(sh.SETUP, {'state': 'PLAY', 'stage': 8, 'pilot': 'cole', 'invuln': True})
        page.evaluate("""() => {stagePlan=[];waveIdx=999;spawnClock=9999;enemies=[];eBullets=[];
          boss=null;bossActive=false;spawnBoss('vileexistence');boss._scene=null;boss._symEntry=null;
          boss.enter=false;boss.x=worldWidth()/2;boss.y=boss.ty;boss._mcd=.05;boss.flash=0;}""")
        page.wait_for_function("() => XART.rdy('vile24_form1_body') && XART.rdy('vile24_shield_sheet')", timeout=30000)
        for form in range(4):
            seen = set()
            for i in range(75):
                err = page.evaluate(sh.STEP, 8)
                if err:
                    errors.append(err)
                    break
                if i % 5 == 0:
                    seen.update(page.evaluate("() => eBullets.map(q => q.kind)"))
            before = page.evaluate("""() => ({form:boss._vForm,name:boss.name,
              parts:boss.parts.filter(p=>p.dmg&&!p.destroyed).length,
              shield:boss._v24&&boss._v24.shield,
              attack:boss._v24&&boss._v24.pattern&&boss._v24.pattern.type,
              music:bossMusPhase(run.stage,boss._vForm)})""")
            png = page.evaluate("() => document.querySelector('#screen').toDataURL('image/png')")
            (out / f'form_{form+1}.png').write_bytes(base64.b64decode(png.split(',', 1)[1]))
            row = {'before': before, 'seen': sorted(seen)}
            if form < 3:
                row['hit'] = page.evaluate("""() => {const original=boss._vForm,
                  pieces=boss.parts.filter(p=>p.dmg&&!p.destroyed).slice();
                  for(const part of pieces){
                    boss._lastPart=part;modularHit(part.hp*8);
                    if(!part.destroyed){boss._lastPart=part;modularHit(part.hp*8);}
                  }
                  return {from:original,to:boss._vForm,morph:boss._morphT,enter:boss.enter,
                    parts:boss.parts.filter(p=>p.dmg&&!p.destroyed).length};}""")
                for i in range(60):
                    err = page.evaluate(sh.STEP, 1)
                    if err:
                        errors.append(err)
                        break
                row['after'] = page.evaluate("""() => ({form:boss._vForm,enter:boss.enter,
                    morph:boss._morphT,parts:boss.parts.filter(p=>p.dmg&&!p.destroyed).length})""")
            report['forms'].append(row)
        report['errors'] = errors
        (out / 'report.json').write_text(json.dumps(report, indent=2))
        print(json.dumps(report, indent=2))
        assert not errors
        assert [r['before']['form'] for r in report['forms']] == list(range(4))
        assert all(r['seen'] for r in report['forms'])
        assert all(r['hit']['to'] == i+1 for i, r in enumerate(report['forms'][:3]))
        browser.close()
finally:
    stop()
