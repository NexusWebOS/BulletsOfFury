"""Exercise the actual Stage-5 miniboss director in Chromium, including one full attack cycle."""
from pathlib import Path
from playwright.sync_api import sync_playwright
from shoot import serve, SETUP, STEP, TRAP_RAF

ROOT = Path(__file__).resolve().parents[1]
port, stop = serve(str(ROOT))
errors = []
try:
    with sync_playwright() as pw:
        browser = pw.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
        page = browser.new_page(viewport={'width': 1100, 'height': 1200})
        page.on('pageerror', lambda e: errors.append(str(e)))
        page.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
        page.goto(f'http://127.0.0.1:{port}/index.html', wait_until='load', timeout=60000)
        page.wait_for_function("() => typeof ASSETS !== 'undefined' && (window.__bofFrames|0)>4", timeout=45000)
        page.evaluate(TRAP_RAF)
        page.wait_for_timeout(50)
        assert page.evaluate(SETUP, {'state':'PLAY','stage':5,'pilot':'cole','invuln':True})['ok']
        page.evaluate((ROOT / '_BUILD_SOURCE/scenario_chaosharrier.js').read_text())
        page.evaluate("""() => {
          window.__chTrace=[]; window.__chSeen=new Set(); window.__chShots=[]; window.__chHistory=[]; window.__chLastState=null;
          window.__qaTick=() => {
            if(!subBoss)return;
            const s=subBoss._chState;
            if(s!==window.__chLastState){window.__chHistory.push(s);window.__chLastState=s;}
            if(!window.__chSeen.has(s)){window.__chSeen.add(s);window.__chTrace.push(s);}
            for(const q of eBullets)if(q._chKind==='missile'&&!window.__chShots.includes(q))
              window.__chShots.push(q);
          };
        }""")
        for _ in range(30):
            assert page.evaluate(STEP, 60) is None
            page.wait_for_timeout(25)
        result = page.evaluate("""() => ({
          trace:window.__chTrace,
          history:window.__chHistory,
          shots:window.__chShots.map(q=>({x:q.x,lane:q._chLaneX,vx:q.vx,ang:q.ang})),
          art:['ch_ship_0','ch_ship_2','ch_plasma_0','ch_missile_0','ch_beam_0','chrift_3']
            .map(k=>[k,XART.rdy(k)])
        })""")
        browser.close()
finally:
    stop()

print(result)
assert not errors, errors[:6]
assert {'warpout','warpin','plasma','missile','side','beam'} <= set(result['trace'])
assert len(result['shots']) >= 2
first_beam=result['history'].index('beam')
assert result['history'][first_beam:first_beam+5]==['beam','idle','side','idle','beam'],result['history']
assert all(abs(q['x']-q['lane']) < 1e-6 and q['vx'] == 0 for q in result['shots'])
assert all(ready for _,ready in result['art'])
print('PASS Chaos Harrier complete attack cycle and art readiness; no browser errors')
