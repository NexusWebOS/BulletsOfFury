"""Confirm the composed Pilot Select reveal and clean GOOD LUCK card in Chromium."""
import base64
import json
from pathlib import Path

from playwright.sync_api import sync_playwright
from shoot import serve, STEP, TRAP_RAF


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '_shots/pilot_reveal_0920'
OUT.mkdir(parents=True, exist_ok=True)


def main():
    port, stop = serve(str(ROOT))
    errors, states = [], {}
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(args=['--no-sandbox', '--mute-audio'])
            page = browser.new_page(viewport={'width': 1280, 'height': 720})
            page.on('pageerror', lambda e: errors.append('page ' + str(e)))
            page.on('console', lambda m: errors.append('console ' + m.text) if m.type == 'error' else None)
            page.goto(f'http://127.0.0.1:{port}/index.html', wait_until='load', timeout=120000)
            page.wait_for_function('() => (window.__bofFrames|0)>4', timeout=120000)
            page.evaluate(TRAP_RAF)
            page.evaluate("() => {run.mode='arcade'; pilotIndex=PILOTS.findIndex(x=>x.key==='yuri'); setState('pilot');}")
            for _ in range(240):
                if page.evaluate("() => XART.rdy('pav_yuri') && XART.rdy('ship_yuri_pv2')"):
                    break
                page.wait_for_timeout(30)

            def shot(name):
                uri = page.evaluate("() => document.querySelector('#screen').toDataURL('image/png')")
                (OUT / (name + '.png')).write_bytes(base64.b64decode(uri.split(',', 1)[1]))
                states[name] = page.evaluate("""() => ({phase:pcard&&pcard.phase,typed:pcard&&pcard.typed,
                  bar:pcard&&pcard.bar,seg:pcard&&pcard.seg,done:pcard&&pcard.done,
                  pilot:PILOTS[pilotIndex].key,pending:pilotPending})""")

            found = set()
            for _ in range(350):
                assert page.evaluate(STEP, 1) is None
                s = page.evaluate("() => pcard&&({phase:pcard.phase,typed:pcard.typed,bar:pcard.bar,seg:pcard.seg})")
                if s and s['phase'] == 'type' and s['typed'] > 5 and 'type' not in found:
                    shot('identity_typing'); found.add('type')
                if s and s['phase'] == 'bars' and s['bar'] == 0 and s['seg'] > 2 and 'bar0' not in found:
                    shot('first_bar_filling'); found.add('bar0')
                if s and s['phase'] == 'bars' and s['bar'] == 1 and s['seg'] > 2 and 'bar1' not in found:
                    shot('second_bar_filling'); found.add('bar1')
                if s and s['phase'] == 'hold' and 'hold' not in found:
                    shot('fully_revealed'); found.add('hold')
                if len(found) == 4:
                    break
            assert found == {'type', 'bar0', 'bar1', 'hold'}, found
            page.evaluate("() => {pilotPending=pilotIndex;pilotSlide=.04;}")
            assert page.evaluate(STEP, 1) is None
            shot('good_luck_clean')
            assert not errors, errors
            browser.close()
    finally:
        stop()
    (OUT / 'results.json').write_text(json.dumps({'states': states, 'errors': errors}, indent=2), encoding='utf-8')
    print('PASS typewriter, separate stat bars, completed special and GOOD LUCK; no browser errors')


if __name__ == '__main__':
    main()
