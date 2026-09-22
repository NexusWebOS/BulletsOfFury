"""Inspect the authored incoming-lock HUD and distance-based warning cadence in Chromium."""
from pathlib import Path
from playwright.sync_api import sync_playwright
from shoot import serve, SETUP, STEP, TRAP_RAF

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '_shots/lock_hud_0920'
OUT.mkdir(exist_ok=True)
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
        assert page.evaluate(SETUP, {'state': 'PLAY', 'stage': 5, 'pilot': 'cole', 'invuln': True})['ok']
        page.wait_for_function("() => XART.rdy('retm_0') && XART.rdy('nequipbox')", timeout=30000)
        page.evaluate(STEP, 3)
        page.screenshot(path=str(OUT / 'idle.png'))
        result = page.evaluate("""() => {
          const m={x:player.x,y:player.y-400,vx:0,vy:0,dead:false,kind:'emissile',_shootable:true};
          eBullets.push(m);
          playerLocks=[{id:999,src:{x:player.x,y:player.y-430,dead:false},t:.1,dur:0,
            launches:[],missiles:[m],state:'locked',endT:0,spin:0,ev0:false}];
          updatePlayerLocks(1/60);
          const far=_lockHudGap;
          m.y=player.y-90;updatePlayerLocks(1/60);
          const near=_lockHudGap,next=_lockBeepT;
          m.y=player.y-210;
          return {far,near,next,art:XART.rdy('retm_0')};
        }""")
        page.evaluate(STEP, 2)
        page.screenshot(path=str(OUT / 'incoming.png'))
        page.evaluate("""() => {playerLocks=[];_lockHudGap=Infinity;}""")
        page.evaluate(STEP, 2)
        browser.close()
finally:
    stop()

print(result)
assert result['art'] and .40 < result['far'] < .50, result
assert .095 < result['near'] < .105 and result['next'] <= result['near'], result
assert not errors, errors[:8]
print('PASS incoming lock HUD art, distance cadence, and browser errors')
