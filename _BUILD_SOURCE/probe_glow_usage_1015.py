"""Pixel glow usage survey (1015b): which enemy / miniboss / boss frames does each stage ACTUALLY draw?

Mike: "only do this for enemies and frames we're actually using please. Do a pass for levels 1-9."

Real index.html in Chromium. For one stage: natural play (the stage's own waves), then its miniboss, then
its boss, with the player firing real rounds (pShoot) under the target so the fights advance through their
damage states and phases. Every drawImage that lands while drawEnemy / drawSubBoss / drawBoss is running is
recorded by the KEY the image was fetched under (XART._touch is wrapped - XART.get returns a fresh blank or
a cached cell canvas, never a stable identity, and a cell canvas carries no .src), plus the source rect, so
a sheet's frames are known individually. xartPalette / xartTint results are tagged with their source key.
Usage: python _BUILD_SOURCE/probe_glow_usage_1015.py STAGE [DIFF]   -> _shots/glow_usage_1015/sN_DIFF.json
"""
import json, sys, time
from pathlib import Path
from playwright.sync_api import sync_playwright
sys.path.insert(0, str(Path(__file__).parent))
import shoot as sh
ROOT = Path(__file__).resolve().parents[1]
STAGE = int(sys.argv[1]); DIFF = sys.argv[2] if len(sys.argv) > 2 else 'normal'
OUT = ROOT / '_shots/glow_usage_1015'; OUT.mkdir(parents=True, exist_ok=True)

TRACE = r"""
() => {
  if (window.__gu) return;
  const T = window.__gu = {scope: null, rec: {}, untagged: {}};
  const wrap = (name, scope) => { const f = window[name]; if (typeof f !== 'function') return;
    window[name] = function(){ const prev = T.scope; T.scope = scope; try { return f.apply(this, arguments); } finally { T.scope = prev; } }; };
  wrap('drawEnemy', 'enemy'); wrap('drawSubBoss', 'mini'); wrap('drawBoss', 'boss');
  const d = ctx.drawImage;
  ctx.drawImage = function(im){
    if (T.scope && im && !PXG.drawing) {
      const a = arguments, n = a.length, w = im.naturalWidth || im.width, h = im.naturalHeight || im.height;
      if (w > 2 && h > 2) {
        let sx=0,sy=0,sw=w,sh=h,dw,dh; if(n>=9){sx=a[1];sy=a[2];sw=a[3];sh=a[4];dw=a[7];dh=a[8];} else {dw=n>=5?a[3]:w;dh=n>=5?a[4]:h;}
        const t = PXG.tags.get(im);
        if (t && t.key) {
          const kx0=Math.max(t.ax*sx+t.bx,t.vx0),ky0=Math.max(t.ay*sy+t.by,t.vy0),kx1=Math.min(t.ax*(sx+sw)+t.bx,t.vx1),ky1=Math.min(t.ay*(sy+sh)+t.by,t.vy1);
          const m = this.getTransform(), sc = Math.hypot(m.a,m.b) * dw / Math.max(1e-6,(t.ax*sw));
          const r = T.rec[t.key] || (T.rec[t.key] = {n: 0, scope: {}, rects: {}, tints: {}, sc: 0});
          r.n++; r.scope[T.scope] = 1; r.sc += sc;
          const rk = [Math.round(kx0),Math.round(ky0),Math.round(kx1),Math.round(ky1)].join(','); r.rects[rk] = (r.rects[rk] || 0) + 1;
          if (t.tint) r.tints[t.tint] = (r.tints[t.tint]||0) + 1;
        } else { const uk = w + 'x' + h; const r = T.untagged[uk] || (T.untagged[uk] = {n: 0, scope: {}, stack: new Error().stack.split('\n').slice(2,5).map(s=>s.trim()).join(' | ')}); r.n++; r.scope[T.scope] = 1; }
      }
    }
    return d.apply(this, arguments);
  };
}
"""
# the player keeps under the target and fires real rounds, so fights advance through damage states
TICK = r"""
() => { window.__qaTick = function(i){
  try{
    const t = (typeof boss!=='undefined'&&bossActive&&boss&&!boss.dead) ? boss : (typeof subBoss!=='undefined'&&subBossActive&&subBoss&&!subBoss.dead) ? subBoss : null;
    if (t) { player.x += clamp((t.x||player.x) - player.x, -4, 4); }
    if (typeof pShoot === 'function') pShoot();
    if (t && i % 30 === 0) { const mh = t.maxhp || t.hp || 100; window.__qaDmg = (window.__qaDmg||0)+1;
      if (t === boss) { boss._lastHitX = boss.x; boss._lastHitY = boss.y; hitBoss(mh * 0.012); } else hitSubBoss(mh * 0.02, t.x, t.y); }
  }catch(e){}
}; }
"""
port, stop = sh.serve(str(ROOT))
res = {'stage': STAGE, 'diff': DIFF, 'phases': {}, 'errors': []}
t0 = time.time()
try:
    with sync_playwright() as pw:
        br = pw.chromium.launch(executable_path='/opt/pw-browsers/chromium')
        pg = br.new_page(viewport={'width': 960, 'height': 1100})
        pg.route('**/favicon.ico', lambda r: r.fulfill(status=204, body=''))
        pg.on('pageerror', lambda e: res['errors'].append(str(e)[:200]))
        pg.goto(f'http://127.0.0.1:{port}/index.html')
        pg.wait_for_function('typeof loop==="function" && window.__bofAssetRuntimeReady', timeout=180000)
        pg.evaluate(sh.TRAP_RAF)
        pg.evaluate("(d)=>{ if (typeof DIFFS!=='undefined' && DIFFS[d]) { diffKey=d; DIFF=DIFFS[d]; } }", DIFF)
        print(pg.evaluate(sh.SETUP, {'state': 'PLAY', 'stage': STAGE, 'pilot': 'cole', 'invuln': True}), flush=True)
        pg.evaluate("(d)=>{ if (typeof DIFFS!=='undefined' && DIFFS[d]) { diffKey=d; DIFF=DIFFS[d]; } playerHit=function(){}; }", DIFF)
        pg.evaluate(TRACE); pg.evaluate(TICK)

        def run(sec, phase):
            for _ in range(int(sec)):
                err = pg.evaluate(sh.STEP, 60)
                if err: res['errors'].append(err[:200])
                pg.evaluate("()=>{player.invuln=1e9;}")
                pg.wait_for_timeout(60)
            snap = pg.evaluate("()=>{const T=window.__gu;const o={rec:T.rec,untagged:T.untagged};T.rec={};T.untagged={};return o;}")
            res['phases'][phase] = snap
            print(phase, len(snap['rec']), 'keys', round(time.time() - t0), 's', flush=True)

        run(60, 'waves')
        pg.evaluate("()=>{enemies.length=0;eBullets.length=0;const SB=SUBBOSS[run.stage];if(SB&&SB.kind){spawnSubBoss(SB.kind);}}")
        has_sub = pg.evaluate("()=>!!(typeof subBoss!=='undefined'&&subBoss&&subBossActive)")
        res['has_sub'] = has_sub
        if has_sub: run(50, 'mini')
        pg.evaluate("()=>{try{if(subBoss){subBoss=null;subBossActive=false;}}catch(e){} enemies.length=0;eBullets.length=0;spawnBoss(curStage.boss);}")
        res['boss_kind'] = pg.evaluate("()=>boss&&boss.kind")
        run(80, 'boss')
        br.close()
finally:
    stop()
p = OUT / f's{STAGE}_{DIFF}.json'; p.write_text(json.dumps(res))
print('wrote', p, 'errors', res['errors'][:3])
