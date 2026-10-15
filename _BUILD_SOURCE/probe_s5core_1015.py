"""Stage-5 boss core survey (1015): what is drawn ON the Chrome Hammer's chest, and by whom.

Spawns the real stage-5 boss, forces each body state that has a lit core, and records every
additive ('lighter') blit landing inside the boss's chest box together with the XART key that
fed it, then grabs a frame per state. Usage: python _BUILD_SOURCE/probe_s5core_1015.py [label]
"""
import base64, json, sys
from pathlib import Path
from playwright.sync_api import sync_playwright
sys.path.insert(0, str(Path(__file__).parent))
import shoot as sh
ROOT = Path(__file__).resolve().parents[1]
LABEL = sys.argv[1] if len(sys.argv) > 1 else 'before'
OUT = ROOT / '_shots/pixel_glow_1015' / LABEL; OUT.mkdir(parents=True, exist_ok=True)

TRACE = r"""
() => {
  if (window.__s5trace) return;
  window.__s5trace = {on:false, log:[]};
  const T = window.__s5trace, g = XART.get.bind(XART), keyOf = new WeakMap();
  XART.get = function(k){ const im = g(k); try{ if(im && typeof im==='object') keyOf.set(im,k); }catch(e){} return im; };
  const d = ctx.drawImage;
  ctx.drawImage = function(im){
    if (T.on && ctx.globalCompositeOperation === 'lighter' && typeof boss !== 'undefined' && boss) {
      const m = ctx.getTransform(), a = arguments, n = a.length;
      const dx = n >= 9 ? a[5] : a[1], dy = n >= 9 ? a[6] : a[2], dw = n >= 9 ? a[7] : (a[3] || im.width), dh = n >= 9 ? a[8] : (a[4] || im.height);
      const cx = m.a*(dx+dw/2)+m.c*(dy+dh/2)+m.e, cy = m.b*(dx+dw/2)+m.d*(dy+dh/2)+m.f;
      T.log.push({key: keyOf.get(im) || ('?'+im.width+'x'+im.height), cx: Math.round(cx), cy: Math.round(cy), w: Math.round(dw*Math.hypot(m.a,m.b)), alpha: +ctx.globalAlpha.toFixed(2), st: boss._hammer && boss._hammer.state});
    }
    return d.apply(this, arguments);
  };
}
"""
FORCE = r"""
(st) => {
  const b = boss, h = b._hammer;
  b.enter = false; b._noHit = false; b.y = b.ty = VH*.34; b.x = worldWidth()/2;
  h.state = st; h.t = st === 'core_orbit' ? 1.2 : 0.4; h.coreAngle = 0.6;
  return {state: h.state, x: b.x, y: b.y, w: b.w, h: b.h};
}
"""
port, stop = sh.serve(str(ROOT))
res = {'label': LABEL, 'states': {}}
try:
    with sync_playwright() as pw:
        br = pw.chromium.launch(executable_path='/opt/pw-browsers/chromium')
        pg = br.new_page(viewport={'width': 960, 'height': 1100})
        pg.route('**/favicon.ico', lambda r: r.fulfill(status=204, body=''))
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.on('console', lambda m: m.type == 'error' and errs.append(m.text))
        pg.goto(f'http://127.0.0.1:{port}/index.html')
        pg.wait_for_function('typeof loop==="function" && window.__bofAssetRuntimeReady', timeout=180000)
        pg.evaluate(sh.TRAP_RAF)
        print(pg.evaluate(sh.SETUP, {'state': 'PLAY', 'stage': 5, 'pilot': 'cole', 'invuln': True}))
        pg.evaluate(sh.STEP, 30)
        pg.evaluate("()=>{enemies.length=0;eBullets.length=0;spawnBoss(curStage.boss);playerHit=function(){};}")
        for _ in range(12):
            pg.evaluate(sh.STEP, 20); pg.wait_for_timeout(400)
        pg.evaluate(TRACE)
        for st in ['core_orbit', 'idle', 'mega_charge', 'enrage']:
            info = pg.evaluate(FORCE, st)
            pg.evaluate("()=>{window.__s5trace.log.length=0;window.__s5trace.on=true;}")
            pg.evaluate(sh.STEP, 1); pg.wait_for_timeout(300)
            pg.evaluate(FORCE, st)
            pg.evaluate(sh.STEP, 1)
            log = pg.evaluate("()=>{const T=window.__s5trace;T.on=false;return T.log.slice(0,60);}")
            png = pg.evaluate("()=>document.querySelector('#screen').toDataURL('image/png')")
            (OUT / f'{st}.png').write_bytes(base64.b64decode(png.split(',')[1]))
            chest = [q for q in log if abs(q['cx'] - info['x']) < 60 and abs(q['cy'] - info['y']) < 70]
            res['states'][st] = {'boss': info, 'lighter_blits': len(log), 'chest_blits': chest[:20]}
            print(st, json.dumps({'lighter': len(log), 'chest': chest[:6]}), flush=True)
        res['errors'] = errs[:8]
        br.close()
finally:
    stop()
(OUT / 'survey.json').write_text(json.dumps(res, indent=1))
print('errors', res['errors'])
