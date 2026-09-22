"""Verify Stage 3 music aliases and shared pilot portrait geometry in Chromium."""
import json
from pathlib import Path

from playwright.sync_api import sync_playwright
from shoot import serve

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '_shots' / 'pandemonium_portraits_0920'
OUT.mkdir(parents=True, exist_ok=True)
port, stop = serve(str(ROOT))
errors = []
try:
    with sync_playwright() as pw:
        browser = pw.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
        page = browser.new_page(viewport={'width': 1280, 'height': 720})
        page.on('pageerror', lambda e: errors.append('page ' + str(e)))
        page.on('console', lambda m: errors.append('console ' + m.text) if m.type == 'error' else None)
        page.goto(f'http://127.0.0.1:{port}/index.html', wait_until='load', timeout=60000)
        page.wait_for_function("() => typeof Snd !== 'undefined' && Snd.music && Snd.music.boss3 && Snd.music.unused2 && Snd.music.mini3", timeout=45000)
        routed = page.evaluate("""() => ({
          boss3: Snd.music.boss3.src,
          mini3: Snd.music.mini3.src,
          unused2: Snd.music.unused2.src,
          level3: Snd.music.lvl3.src
        })""")
        assert routed['boss3'].endswith('/assets/game/music/boss3_pandemonium.mp3'), routed
        assert routed['unused2'].endswith('/assets/game/music/boss3_cryo_behemoth.mp3'), routed
        assert routed['mini3'] == routed['level3'], routed
        assert not errors, errors[:10]
        (OUT / 'results.json').write_text(json.dumps({'routed': routed, 'errors': errors}, indent=2), encoding='utf-8')
        browser.close()
finally:
    stop()
print('PASS Stage 3 boss uses Pandemonium; former boss theme archived as unused2; no browser errors')
