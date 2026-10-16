"""Pixel glow live A/B (1015b): real stage play, the same frame drawn with the glow drivers on and off.
Saves side-by-side crops per stage and times drawScene both ways. Usage: python _BUILD_SOURCE/probe_glow_live_1015.py [stages]"""
import base64, io, json, sys, time
from pathlib import Path
from PIL import Image
import numpy as np
from playwright.sync_api import sync_playwright
sys.path.insert(0, str(Path(__file__).parent))
import shoot as sh
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '_shots/glow_usage_1015/live'; OUT.mkdir(parents=True, exist_ok=True)
STAGES = [int(x) for x in sys.argv[1].split(',')] if len(sys.argv) > 1 else [1, 2, 3, 4, 6, 7, 8, 9]
AB = r"""(on)=>{ if(!window.__pd){window.__pd=[pxgUnitDrive,pxgHammerDrive];}
  pxgUnitDrive = on ? window.__pd[0] : ()=>null; pxgHammerDrive = on ? window.__pd[1] : ()=>null;
  const n=PXG.draws, t0=performance.now(); for(let i=0;i<20;i++) drawScene(0); const ms=(performance.now()-t0)/20;
  return {draws:(PXG.draws-n)/20, ms, png:document.querySelector('#screen').toDataURL('image/png')}; }"""
res = {}
port, stop = sh.serve(str(ROOT))
try:
    with sync_playwright() as pw:
        br = pw.chromium.launch(executable_path='/opt/pw-browsers/chromium')
        for st in STAGES:
            pg = br.new_page(viewport={'width': 960, 'height': 1100})
            pg.route('**/favicon.ico', lambda r: r.fulfill(status=204, body=''))
            errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
            pg.goto(f'http://127.0.0.1:{port}/index.html')
            pg.wait_for_function('typeof loop==="function" && window.__bofAssetRuntimeReady', timeout=180000)
            pg.evaluate(sh.TRAP_RAF)
            pg.evaluate(sh.SETUP, {'state': 'PLAY', 'stage': st, 'pilot': 'cole', 'invuln': True})
            pg.evaluate("()=>{playerHit=function(){};}")
            for _ in range(28):
                pg.evaluate(sh.STEP, 60); pg.evaluate("()=>{player.invuln=1e9;}"); pg.wait_for_timeout(100)
            pg.evaluate("()=>{const t=stateT;pxgStep=(x)=>PXG_STEPS[4];}")   # hold one step so on/off compares like for like
            a = pg.evaluate(AB, True); b = pg.evaluate(AB, False); b2 = pg.evaluate(AB, False)
            A = Image.open(io.BytesIO(base64.b64decode(a['png'].split(',')[1]))).convert('RGB')
            B = Image.open(io.BytesIO(base64.b64decode(b['png'].split(',')[1]))).convert('RGB')
            d = (np.asarray(A, float) - np.asarray(B, float)).sum(-1)
            B2 = Image.open(io.BytesIO(base64.b64decode(b2['png'].split(',')[1]))).convert('RGB')
            noise = int((np.abs((np.asarray(B2, float) - np.asarray(B, float)).sum(-1)) > 6).sum())
            res[st] = {'draws': a['draws'], 'ms_on': round(a['ms'], 2), 'ms_off': round(b['ms'], 2), 'brighter_px': int((d > 6).sum()), 'darker_px': int((d < -6).sum()), 'off_vs_off_px': noise, 'errors': errs[:3], 'enemies': pg.evaluate("()=>enemies.length")}
            W, H = A.size
            pair = Image.new('RGB', (W * 2 + 6, H)); pair.paste(B, (0, 0)); pair.paste(A, (W + 6, 0)); pair.save(OUT / f'stage{st}_off_on.png')
            print(st, res[st], flush=True)
            pg.close()
        br.close()
finally:
    stop()
(OUT / 'live.json').write_text(json.dumps(res, indent=1))
