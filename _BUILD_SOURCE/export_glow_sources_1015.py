"""Export the exact pixels of every surveyed glow source (1015b).

The survey (probe_glow_usage_1015.py) records which keys the game draws inside enemy / miniboss / boss draws.
This reads each key back through XART in real Chromium over http (an untainted canvas) and saves the image
the game actually blits - cells cut from their atlas, loose plates as decoded - so the baker works on the
same pixels at the same size the runtime will overlay. Usage: python _BUILD_SOURCE/export_glow_sources_1015.py
Reads _BUILD_SOURCE/glow_usage_1015.json (written by pixel_glow_1015.py --survey), writes _shots/glow_usage_1015/src/.
"""
import base64, json, sys
from pathlib import Path
from playwright.sync_api import sync_playwright
sys.path.insert(0, str(Path(__file__).parent))
import shoot as sh
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '_shots/glow_usage_1015/src'; OUT.mkdir(parents=True, exist_ok=True)
keys = sorted(json.loads((ROOT / '_BUILD_SOURCE/glow_usage_1015.json').read_text())['keys'])
port, stop = sh.serve(str(ROOT))
missing = []
try:
    with sync_playwright() as pw:
        br = pw.chromium.launch(executable_path='/opt/pw-browsers/chromium')
        pg = br.new_page(viewport={'width': 640, 'height': 480})
        pg.route('**/favicon.ico', lambda r: r.fulfill(status=204, body=''))
        pg.goto(f'http://127.0.0.1:{port}/index.html')
        pg.wait_for_function('typeof loop==="function" && window.__bofAssetRuntimeReady', timeout=180000)
        pg.evaluate(sh.TRAP_RAF)
        for i in range(0, len(keys), 40):
            batch = keys[i:i + 40]
            pg.evaluate("(ks)=>{for(const k of ks)XART.rdy(k);}", batch)
            try:
                pg.wait_for_function("(ks)=>ks.every(k=>XART.rdy(k))", arg=batch, timeout=30000)
            except Exception:
                pass
            got = pg.evaluate(r"""(ks)=>ks.map(k=>{ if(!XART.rdy(k)) return [k,null];
              const im=XART.get(k),w=im.naturalWidth||im.width,h=im.naturalHeight||im.height;
              const c=document.createElement('canvas');c.width=w;c.height=h;c.getContext('2d').drawImage(im,0,0);
              return [k,c.toDataURL('image/png')]; })""", batch)
            for k, data in got:
                if not data:
                    missing.append(k); continue
                (OUT / (k + '.png')).write_bytes(base64.b64decode(data.split(',')[1]))
            print(i + len(batch), '/', len(keys), 'missing', len(missing), flush=True)
        br.close()
finally:
    stop()
print('missing', missing)
