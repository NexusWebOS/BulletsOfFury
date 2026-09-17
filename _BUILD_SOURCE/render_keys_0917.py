#!/usr/bin/env python3
"""
render_keys_0917.py - resolve art keys in the LIVE engine and write them out at 4x.

Rule 1 of CLAUDE.md: filenames lie, render the art before you trust it. This asks XART for each
key the way the game does, waits for the decode (rdy() is false on its FIRST call - that call is
what starts the load), and saves each cell composited onto a dark background.

⚠ NEVER convert('RGB') a cell - these plates carry a magenta payload under fully transparent
pixels and convert() paints it back on (0906v, four drops of chasing dots that were not in the
game). Composite with paste(im, (0,0), im).

    python _BUILD_SOURCE/render_keys_0917.py nwp_lfi_laser_start nwp_lfi_laser_middle ...
"""
import os, sys, base64, io, json
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.join(ROOT, '_BUILD_SOURCE'))
import shoot as sh
from playwright.sync_api import sync_playwright
from PIL import Image

OUT = os.path.join(ROOT, 'docs', 'proofs', 'keys_0917')

def main():
    keys = sys.argv[1:]
    if not keys:
        print('usage: render_keys_0917.py <key> [key ...]'); sys.exit(2)
    os.makedirs(OUT, exist_ok=True)
    port, stop = sh.serve(sh.GAME)
    rows = []
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        pg = br.new_page(viewport={'width': 800, 'height': 600})
        pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=60000)
        pg.wait_for_function("() => typeof XART!=='undefined'", timeout=60000)
        pg.wait_for_function("() => (window.__bofFrames|0) > 4", timeout=60000)
        pg.evaluate("(ks) => { ks.forEach(k => { try{ XART.rdy(k); }catch(_){} }); }", keys)
        pg.wait_for_timeout(2500)                     # the decode needs REAL time, not frames
        pg.evaluate("(ks) => { ks.forEach(k => { try{ XART.rdy(k); }catch(_){} }); }", keys)
        pg.wait_for_timeout(1500)
        for k in keys:
            d = pg.evaluate("""(k) => {
              if(!XART.rdy(k)) return null;
              const im = XART.get(k); if(!im) return null;
              const w = im.naturalWidth || im.width, h = im.naturalHeight || im.height;
              if(!w || !h) return null;
              const c = document.createElement('canvas'); c.width = w; c.height = h;
              c.getContext('2d').drawImage(im, 0, 0);
              return {png: c.toDataURL('image/png'), w: w, h: h};
            }""", k)
            if not d:
                print('  %-32s NOT READY / no art' % k); rows.append({'key': k, 'ok': False}); continue
            im = Image.open(io.BytesIO(base64.b64decode(d['png'].split(',', 1)[1]))).convert('RGBA')
            bg = Image.new('RGBA', im.size, (18, 18, 24, 255))
            bg.paste(im, (0, 0), im)                  # composite, never convert() (0906v)
            z = bg.resize((im.width * 4, im.height * 4), Image.NEAREST)
            p = os.path.join(OUT, k + '.png')
            z.convert('RGB').save(p)
            opaque = sum(1 for px in im.getdata() if px[3] > 8)
            print('  %-32s %4dx%-4d  %6d opaque px  -> %s' % (k, d['w'], d['h'], opaque, os.path.basename(p)))
            rows.append({'key': k, 'ok': True, 'w': d['w'], 'h': d['h'], 'opaque': opaque})
        br.close()
    stop()
    json.dump(rows, open(os.path.join(OUT, '_index.json'), 'w'), indent=2)

if __name__ == '__main__':
    main()
