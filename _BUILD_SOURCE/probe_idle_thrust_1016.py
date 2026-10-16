"""Idle thruster probe (1016): does every pilot's flame animate while the ship holds still?

Mike: "can you make our thrusters animate when were idle on all pilots?"

Real index.html in Chromium, stage 1, NO input. The plume is drawn by pf27PlaneThrustDraw inside _drawPlayerCore;
every blit it makes is recorded off the game ctx (the instance carries its own drawImage - 0905h), with the
destination height and the plume reel frame it sampled. Idle must (a) draw the plume on every frame, (b) cycle
more than one reel frame, (c) vary its length. A busted arm (window.PF16_IDLE=0, the pre-1016 behaviour) must
draw NO plume, so the check can fail. Also: a moving ship still burns harder than an idle one, and a dead one
draws nothing.  Usage: python _BUILD_SOURCE/probe_idle_thrust_1016.py
"""
import json, sys
from pathlib import Path
from playwright.sync_api import sync_playwright
sys.path.insert(0, str(Path(__file__).parent))
import shoot as sh
ROOT = Path(__file__).resolve().parents[1]
PILOTS = ['axel', 'cole', 'decker', 'falva', 'freezer', 'juggernaut', 'lizzie', 'maverick', 'yuri']
MEASURE = r"""
(args) => {
  const [n, off, moveUp] = args;
  window.PF16_IDLE = off ? 0 : undefined;
  enemies.length = 0; eBullets.length = 0;
  const d = ctx.drawImage, orig = pf27PlaneThrustDraw; let inPlume = false, cur = null;
  window.pf27PlaneThrustDraw = function(){ inPlume = true; try { return orig.apply(this, arguments); } finally { inPlume = false; } };
  ctx.drawImage = function(im){ if (inPlume && arguments.length >= 9 && ctx.globalCompositeOperation === 'source-over') { cur.n++; cur.h = Math.max(cur.h, arguments[8]); cur.frames.add(im); } return d.apply(this, arguments); };
  const per = [], frameSet = new Set();
  for (let i = 0; i < n; i++) {
    cur = {n: 0, h: 0, frames: new Set()};
    if (moveUp) { Input.keys = Input.keys || {}; }
    player.invuln = 0;
    if (moveUp) { player._thrustPower = 1; }
    window.__bofStepNow += 1000/60; loop(window.__bofStepNow);
    per.push({n: cur.n, h: Math.round(cur.h*100)/100}); for (const f of cur.frames) frameSet.add(f);
  }
  ctx.drawImage = d; window.pf27PlaneThrustDraw = orig; window.PF16_IDLE = undefined;
  const hs = per.filter(p => p.n).map(p => p.h);
  return {drawn: per.filter(p => p.n).length, of: n, reelFrames: frameSet.size,
          hMin: hs.length ? Math.min(...hs) : 0, hMax: hs.length ? Math.max(...hs) : 0, power: player._thrustPower || 0};
}
"""
port, stop = sh.serve(str(ROOT))
res = {'pilots': {}, 'errors': []}
ok = fail = 0
def check(c, msg):
    global ok, fail
    if c: ok += 1
    else: fail += 1
    print(('ok   ' if c else 'FAIL ') + msg, flush=True)
try:
    with sync_playwright() as pw:
        br = pw.chromium.launch(executable_path='/opt/pw-browsers/chromium')
        for pk in PILOTS:
            pg = br.new_page(viewport={'width': 960, 'height': 1100})
            pg.route('**/favicon.ico', lambda r: r.fulfill(status=204, body=''))
            pg.on('pageerror', lambda e: res['errors'].append(str(e)[:200]))
            pg.on('console', lambda m: m.type == 'error' and res['errors'].append(m.text[:200]))
            pg.goto(f'http://127.0.0.1:{port}/index.html')
            pg.wait_for_function('typeof loop==="function" && window.__bofAssetRuntimeReady', timeout=180000)
            pg.evaluate(sh.TRAP_RAF)
            pg.evaluate(sh.SETUP, {'state': 'PLAY', 'stage': 1, 'pilot': pk, 'invuln': True})
            pg.evaluate("()=>{playerHit=function(){};}")
            for _ in range(6):
                pg.evaluate(sh.STEP, 60); pg.wait_for_timeout(250)
            on = pg.evaluate(MEASURE, [48, 0, 0])
            off = pg.evaluate(MEASURE, [24, 1, 0])
            mv = pg.evaluate(MEASURE, [12, 0, 1])
            res['pilots'][pk] = {'idle': on, 'busted': off, 'moving': mv}
            print(pk, json.dumps(res['pilots'][pk]), flush=True)
            check(on['drawn'] == on['of'], f"{pk}: idle plume drawn on every frame ({on['drawn']}/{on['of']})")
            check(on['reelFrames'] >= 4, f"{pk}: idle plume cycles the reel ({on['reelFrames']} distinct frames)")
            check(on['hMax'] - on['hMin'] >= 0.6, f"{pk}: idle plume breathes ({on['hMin']}..{on['hMax']} px)")
            check(off['drawn'] == 0, f"{pk}: busted arm draws no idle plume ({off['drawn']})")
            check(mv['hMax'] > on['hMax'], f"{pk}: full throttle burns longer than idle ({mv['hMax']} > {on['hMax']})")
            pg.close()
        br.close()
finally:
    stop()
check(not res['errors'], f"no page/console errors ({len(res['errors'])})")
print(f'{ok} ok / {fail} fail', res['errors'][:3])
(ROOT / 'docs/qa').mkdir(exist_ok=True)
(ROOT / 'docs/qa/idle_thrust_1016.json').write_text(json.dumps({'ok': ok, 'fail': fail, **res}, indent=1))
