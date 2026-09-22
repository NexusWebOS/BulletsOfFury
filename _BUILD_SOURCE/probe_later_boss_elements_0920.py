"""Check Stage 2–6 actual boss-death reward routes in Chromium."""
from pathlib import Path
from playwright.sync_api import sync_playwright
from shoot import serve, SETUP, STEP, TRAP_RAF

ROOT = Path(__file__).resolve().parents[1]
port, stop = serve(str(ROOT))
errors = []
results = []
try:
    with sync_playwright() as pw:
        browser = pw.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
        page = browser.new_page(viewport={'width': 1100, 'height': 1200})
        page.on('pageerror', lambda e: errors.append(str(e)))
        page.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
        page.goto(f'http://127.0.0.1:{port}/index.html', wait_until='load', timeout=60000)
        page.wait_for_function("() => typeof bossDie === 'function' && (window.__bofFrames|0)>4", timeout=45000)
        page.evaluate(TRAP_RAF)
        for stage in range(2, 7):
            assert page.evaluate(SETUP, {'state':'PLAY','stage':stage,'pilot':'cole','invuln':True})['ok']
            data = page.evaluate("""() => {
              run.mode='arcade';run.forgeElems={};run._stageElements=[];
              enemies.length=0;eBullets.length=0;powerups.length=0;
              stagePlan=[{t:9999,fn:function(){}}];waveIdx=0;spawnClock=9999;
              spawnBoss(curStage.boss);
              boss.enter=false;
              const name=boss.name;
              bossDie();
              return {stage:run.stage,name,dead:boss.dead,defeated:bossDefeated,
                drops:powerups.filter(p=>p.kind==='forgecombo').map(p=>p.elem)};
            }""")
            results.append(data)
            assert page.evaluate(STEP, 2) is None
        browser.close()
finally:
    stop()

print(results)
expect = {2:'fire',3:'ice',4:'lightning',5:'chrome',6:'dark'}
assert all(r['dead'] and r['defeated'] and r['drops']==[expect[r['stage']]] for r in results), results
assert not errors, errors[:8]
print('PASS Stage 2–6 bosses each drop exactly one stage element; no browser errors')
