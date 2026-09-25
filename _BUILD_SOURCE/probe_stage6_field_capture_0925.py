"""Check a real Stage 6 combat sample after its long scripted opening."""
import base64
import json
from pathlib import Path

import shoot as sh
from playwright.sync_api import sync_playwright

out = Path('_shots/stage6_field_capture_0925')
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
        page.evaluate(sh.SETUP, {'state': 'PLAY', 'stage': 6, 'pilot': 'cole', 'invuln': True})
        page.evaluate("""() => {diffKey='normal';DIFF=difficultyForRun(run.mode,'normal');
          s6Opening=null;playerLocks=[];stageTimer=10;mapScroll=Math.max(mapScroll,360);
          player.invuln=1e9;run.lives=9;}""")
        for sec in range(1, 13):
            err = page.evaluate(sh.STEP, 60)
            if err: errors.append(f'second {sec}: {err}')
            row = page.evaluate("""() => ({stage:run.stage,opening:!!s6Opening,
              timer:+stageTimer.toFixed(2),enemies:enemies.length,
              bullets:eBullets.length,types:[...new Set(enemies.map(e=>e.kind))],
              state})""")
            row['second'] = sec
            rows.append(row)
            if sec in (3, 6, 9, 12):
                raw = page.evaluate("() => document.querySelector('#screen').toDataURL('image/png')")
                (out / f'{sec:02}.png').write_bytes(base64.b64decode(raw.split(',', 1)[1]))
        browser.close()
finally:
    stop()

report = {'rows': rows, 'errors': errors}
(out / 'report.json').write_text(json.dumps(report, indent=2))
print(json.dumps(report, indent=2))
assert not errors
assert any(r['bullets'] > 0 for r in rows)
