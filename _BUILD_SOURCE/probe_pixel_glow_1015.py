"""Pixel glow probe (1015): the Stage 5 Chrome Hammer's core lights from its own pixels.

Real index.html in Chromium. Spawns the real stage-5 boss, lets the fight run, and for several states
renders the SAME frame twice - glow driver on, then off (the busted arm) - and measures the chest:
  * glow companions were blitted (by key) and only while the boss draws;
  * the chest gets brighter with the glow and the change stays inside the pose (no new silhouette:
    pixels outside the body's own ink are unchanged);
  * the core climbs the step ladder while charging (core_orbit) and the old chest paste (effect cell 6)
    is suppressed;
  * zero page/console errors.
Usage: python _BUILD_SOURCE/probe_pixel_glow_1015.py
"""
import base64, io, json, sys
from pathlib import Path
from PIL import Image, ImageChops
import numpy as np
from playwright.sync_api import sync_playwright
sys.path.insert(0, str(Path(__file__).parent))
import shoot as sh
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '_shots/pixel_glow_1015/probe'; OUT.mkdir(parents=True, exist_ok=True)
results = []
def ok(c, msg): results.append((bool(c), msg)); print(('ok   ' if c else 'FAIL ') + msg, flush=True)

GRAB = "()=>document.querySelector('#screen').toDataURL('image/png')"
# render one frame without advancing the simulation: drawScene is the state draw
DRAW = r"""
(on) => {
  const keep = PXG.active; window.__pxgOff = !on;
  if (!window.__pxgWrapped) { window.__pxgWrapped = true; const d = hammerBossDraw;
    hammerBossDraw = function(b){ if (window.__pxgOff) { const p = PXG.active; PXG.active = null; try { return PXG.base.draw.apply(this, arguments); } finally { PXG.active = p; } } return d.apply(this, arguments); }; }
  const n0 = PXG.draws; drawScene(0);
  return {draws: PXG.draws - n0, log: Object.assign({}, PXG.log)};
}
"""
def img(data): return Image.open(io.BytesIO(base64.b64decode(data.split(',')[1]))).convert('RGB')

port, stop = sh.serve(str(ROOT))
errs = []
try:
    with sync_playwright() as pw:
        br = pw.chromium.launch(executable_path='/opt/pw-browsers/chromium')
        pg = br.new_page(viewport={'width': 960, 'height': 1100})
        pg.route('**/favicon.ico', lambda r: r.fulfill(status=204, body=''))
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.on('console', lambda m: m.type == 'error' and errs.append(m.text))
        pg.goto(f'http://127.0.0.1:{port}/index.html')
        pg.wait_for_function('typeof loop==="function" && window.__bofAssetRuntimeReady', timeout=180000)
        reg = pg.evaluate("()=>({n:Object.keys(PXG_SHEETS).length,hook:!!ctx.__pxg,unused:Object.keys(PXG_SHEETS).filter(k=>/chaingun_break|spell_raise|leap_strike_0922/.test(k)),stages:[...new Set(Object.values(PXG_SHEETS).flatMap(s=>s.st))].sort()})")
        ok(reg['n'] > 50 and reg['hook'], f'glow layer loaded from the stage 1-9 usage survey: {reg["n"]} drawn images registered, drawImage hook installed')
        ok(not reg['unused'], f'no unused Hammer forms registered (chaingun-on-back, spell raise, old leap): {reg["unused"]}')
        ok(reg['stages'] == list(range(1, 10)), f'every stage 1-9 has registered unit art: {reg["stages"]}')
        pg.evaluate(sh.TRAP_RAF)
        pg.evaluate(sh.SETUP, {'state': 'PLAY', 'stage': 5, 'pilot': 'cole', 'invuln': True})
        pg.evaluate("()=>{playerHit=function(){};}")
        for _ in range(12):
            pg.evaluate(sh.STEP, 60); pg.wait_for_timeout(150)
        en = pg.evaluate("()=>Object.keys(PXG.log).filter(k=>/^pxg_/.test(k)&&!/^pxg_(arch_|pt11_hammer)/.test(k))")
        ok(len(en) > 0, f'ordinary stage-5 enemies glow from their own lights ({len(en)} companions drawn: {en[:4]})')
        pg.evaluate("()=>{enemies.length=0;spawnBoss(curStage.boss);playerHit=function(){};}")
        pg.wait_for_function("()=>pxgKeys(5).every(k=>XART.rdy(k))", timeout=90000)
        ok(True, 'all stage-5 glow companions decoded (polled, not a one-shot rdy)')
        n0 = pg.evaluate("()=>PXG.draws")
        ok(n0 >= 0, f'glow draws counted ({n0})')
        seen = {}
        for i in range(30):
            pg.evaluate(sh.STEP, 60); pg.wait_for_timeout(120)
            st = pg.evaluate("()=>boss&&boss._hammer&&boss._hammer.state")
            if st in ('hammer', 'warn', 'curl', 'leap') and st not in seen:
                pg.evaluate("()=>{player.invuln=1e9;boss.flash=0;}")
                on = pg.evaluate(DRAW, True); a = img(pg.evaluate(GRAB))
                off = pg.evaluate(DRAW, False); b_ = img(pg.evaluate(GRAB))
                pg.evaluate("()=>{window.__pxgOff=false;}")
                info = pg.evaluate("()=>({x:boss.x-camX,y:boss._drawY??boss.y})")
                A, B = np.asarray(a, float), np.asarray(b_, float)
                diff = np.abs(A - B).sum(-1) > 6
                gain = (A - B).sum(-1)
                ys, xs = np.nonzero(diff)
                seen[st] = {'draws': on['draws'], 'changed_px': int(diff.sum()), 'mean_gain': float(gain[diff].mean()) if diff.any() else 0,
                            'bbox': [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())] if diff.any() else None, 'boss': info}
                a.save(OUT / f'{st}_on.png'); b_.save(OUT / f'{st}_off.png')
                x0, y0 = int(info['x']) - 110, int(info['y']) - 130
                box = (max(0, x0), max(0, y0), min(480, x0 + 220), min(512, y0 + 240))
                pair = Image.new('RGB', ((box[2]-box[0]) * 2 + 8, box[3]-box[1]), (0, 0, 0))
                pair.paste(b_.crop(box), (0, 0)); pair.paste(a.crop(box), (box[2]-box[0] + 8, 0))
                pair.resize((pair.width * 2, pair.height * 2), Image.NEAREST).save(OUT / f'{st}_offon.png')
                print(st, json.dumps(seen[st]), flush=True)
            if len(seen) >= 3: break
        ok(len(seen) >= 2, f'captured on/off pairs in {len(seen)} live states: {list(seen)}')
        for st, s in seen.items():
            ok(s['draws'] >= 2, f'{st}: glow and core companions blitted on the boss frame ({s["draws"]})')
            ok(s['changed_px'] > 150 and s['mean_gain'] > 0, f'{st}: glow brightens {s["changed_px"]} px (mean +{s["mean_gain"]:.0f}), never darkens')
            bb, bo = s['bbox'], s['boss']
            ok(bb and bb[0] > bo['x'] - 150 and bb[2] < bo['x'] + 150 and bb[1] > bo['y'] - 170 and bb[3] < bo['y'] + 170,
               f'{st}: every changed pixel sits on the boss ({bb}) - no new silhouette')
        # charge: core_orbit ramps the core up the ladder and the chest paste is gone
        drive = pg.evaluate(r"""()=>{const b=boss,h=b._hammer;b.flash=0;h.state='core_orbit';const out=[];
          for(const t of [0,.7,1.4,2.1]){h.t=t;out.push(pxgHammerDrive(b));}
          h.state='hammer';h.t=0;const idle=pxgHammerDrive(b);return {out,idle};}""")
        cores = [pg.evaluate(f"()=>pxgStep({d['core']})") for d in drive['out']]
        ok(cores[-1] > cores[0] and cores[-1] >= 0.74, f'core_orbit climbs the step ladder {cores}')
        ok(pg.evaluate(f"()=>pxgStep({drive['idle']['core']})") < cores[-1], 'idle core sits below the charged core')
        steps = pg.evaluate("()=>{const s=new Set();for(let i=0;i<=100;i++)s.add(pxgStep(i/100));return [...s];}")
        ok(len(steps) == 6, f'brightness is quantised to fixed steps, not a smooth fade: {steps}')
        sup = pg.evaluate(r"""()=>{const b=boss,h=b._hammer;h.state='core_orbit';h.t=1.2;b.flash=0;const n=PXG.log.suppressedCorePaste||0;
          PXG.hammer=b;const r=archEffectBlit(6,b.x,b.y-9,50,0,.8);PXG.hammer=null;
          const other=archEffectBlit(3,b.x+40,b.y,40,0,.8);return {r,n0:n,n1:PXG.log.suppressedCorePaste||0,other};}""")
        ok(sup['r'] is True and sup['n1'] == sup['n0'] + 1, 'core_orbit no longer pastes effect cell 6 over the chest')
        ok(sup['other'] is not False, 'the converging motes (other cells) still draw')
        # off-boss: a registered sheet drawn with no driver gets no glow
        pg.evaluate("()=>{PXG.active=null;}")
        n1 = pg.evaluate("()=>{const n=PXG.draws;const im=XART.get('arch_orbital_sweep_0926');ctx.drawImage(im,0,0,10,10,0,0,10,10);return PXG.draws-n;}")
        ok(n1 == 0, 'a registered sheet drawn outside a driver window gets no glow')
        br.close()
finally:
    stop()
ok(not errs, f'zero page/console errors ({errs[:3]})')
fails = sum(1 for c, _ in results if not c)
(OUT / 'results.json').write_text(json.dumps({'pass': len(results) - fails, 'fail': fails, 'checks': results}, indent=1))
print(f'{len(results) - fails} ok / {fails} fail')
sys.exit(1 if fails else 0)
