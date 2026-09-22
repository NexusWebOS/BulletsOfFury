"""Exercise B/Back through mode setup and render right-facing dialogue portraits."""
import base64
import json
from pathlib import Path

from playwright.sync_api import sync_playwright
from shoot import serve, STEP, TRAP_RAF

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '_shots' / 'dialogue_back_0920'
OUT.mkdir(parents=True, exist_ok=True)
port, stop = serve(str(ROOT))
errors = []
steps = []

try:
    with sync_playwright() as pw:
        browser = pw.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
        page = browser.new_page(viewport={'width': 1280, 'height': 720})
        page.on('pageerror', lambda e: errors.append('page ' + str(e)))
        page.on('console', lambda m: errors.append('console ' + m.text) if m.type == 'error' else None)
        page.goto(f'http://127.0.0.1:{port}/index.html', wait_until='load', timeout=60000)
        page.wait_for_function("() => typeof drawModeSelect==='function' && (window.__bofFrames|0)>4", timeout=45000)
        page.evaluate(TRAP_RAF)

        def tick(n=1):
            err = page.evaluate(STEP, n)
            assert err is None, err

        def state():
            return page.evaluate('() => state')

        def back(expect, input_name='k'):
            if input_name == 'pad_b1':
                page.evaluate("() => Input.injectTap('pad_b1')")
            else:
                page.keyboard.press(input_name)
            tick()
            got = state()
            assert got == expect, {'back': input_name, 'expected': expect, 'got': got}
            steps.append({'back': input_name, 'state': got})

        def select_mode(index, expect):
            page.evaluate('(i) => {setState(GS.MODESEL);modeIndex=i;}', index)
            tick(26)
            page.keyboard.press('Enter')
            tick(38)
            got = state()
            assert got == expect, {'modeIndex': index, 'expected': expect, 'got': got}
            steps.append({'modeIndex': index, 'state': got})

        select_mode(0, 'camphub')
        back('modesel', 'pad_b1')
        select_mode(0, 'camphub')
        page.evaluate("() => {campHubIndex=0;campPick=null;}")
        tick(26)
        page.keyboard.press('Enter')
        tick(38)
        assert state() == 'diff', state()
        back('camphub')
        page.evaluate("() => {campPick='load';campHubIndex=0;}")
        tick(26)
        back('camphub', 'pad_b1')
        assert page.evaluate('() => campPick') is None
        page.evaluate('() => setState(GS.PILOT)')
        tick(26)
        back('diff')
        back('camphub')
        back('modesel')

        for index in (1, 2):
            select_mode(index, 'diff')
            back('modesel', 'pad_b1')
        select_mode(1, 'diff')
        page.evaluate('() => setState(GS.PILOT)')
        tick(26)
        back('diff', 'pad_b1')
        back('modesel')

        page.evaluate("() => {coopOn=false;run.mode='campaign';run.stage=1;openStageSelect(1,{});}")
        tick(26)
        page.evaluate("() => {if(typeof cmap2On==='function' && cmap2On()) cmap2.focus='bar';}")
        back('stagesel', 'pad_b1')
        assert page.evaluate("() => !cmap2On() || cmap2.focus==='map'")
        back('camphub')

        # The shared dialogue panel uses the same sprite treatment for all pilot keys.
        for pilot in ('cole', 'yuri'):
            page.evaluate("p => {run.mode='campaign';run.pilot=p;pilotIndex=PILOTS.findIndex(x=>x.key===p);campaignBridgeStart(()=>setState(GS.CAMPHUB));}", pilot)
            page.wait_for_function("() => XART.rdy('cinbg_stage1_route') && bmfReady('dialogue')", timeout=20000)
            tick(80)
            uri = page.evaluate("() => document.querySelector('#screen').toDataURL('image/png')")
            (OUT / (pilot + '_portrait.png')).write_bytes(base64.b64decode(uri.split(',', 1)[1]))

        assert not errors, errors[:10]
        (OUT / 'results.json').write_text(json.dumps({'steps': steps, 'errors': errors}, indent=2), encoding='utf-8')
        browser.close()
finally:
    stop()
print('PASS Back through Campaign/Arcade/Co-op setup and right-facing dialogue portraits; no browser errors')
