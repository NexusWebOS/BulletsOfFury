"""Inspect the Stage 8 symbiote takeover with the red/charcoal portal sheet."""
import base64
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import shoot as sh
from playwright.sync_api import sync_playwright

out = Path('_shots/dark_portal_intro_0925')
out.mkdir(parents=True, exist_ok=True)
port, stop = sh.serve(sh.GAME)
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
        page.evaluate(sh.SETUP, {'state': 'PLAY', 'stage': 8, 'pilot': 'cole', 'invuln': True})
        page.evaluate("""() => {stagePlan=[];waveIdx=999;spawnClock=9999;enemies=[];eBullets=[];
          boss=null;bossActive=false;spawnBoss('vileexistence');boss._scene=null;boss.x=worldWidth()/2;boss.y=boss.ty;}""")
        page.wait_for_function("() => XART.rdy('vile24_portal_sheet') && XART.rdy('vile24_robot_takeover_sheet')", timeout=30000)
        report = {'source': page.evaluate("() => XART._src.vile24_portal_sheet"), 'frames': [], 'errors': errors}
        for i in range(4):
            for j in range(35):
                err = page.evaluate(sh.STEP, 1)
                if err:
                    errors.append(err)
                    break
            frame = page.evaluate("""() => ({stage:run.stage,form:boss._vForm,
                entry:boss._symEntry&&boss._symEntry.t,enter:boss.enter})""")
            report['frames'].append(frame)
            png = page.evaluate("() => document.querySelector('#screen').toDataURL('image/png')")
            (out / f'intro_{i+1}.png').write_bytes(base64.b64decode(png.split(',', 1)[1]))
        (out / 'report.json').write_text(json.dumps(report, indent=2))
        print(json.dumps(report, indent=2))
        assert not errors and report['source'].endswith('portal_sheet_0925.png')
        browser.close()
finally:
    stop()
