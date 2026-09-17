#!/usr/bin/env python3
"""Where does stage 1 stop being blue water? Sample the live backdrop at several mapScroll
positions and report the mean hue/blueness of the play field, so the showcase reel can be shot
over ground that a pale ice-blue orb can actually be seen against."""
import os, sys, base64, io
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.join(ROOT, '_BUILD_SOURCE'))
import shoot as sh
from playwright.sync_api import sync_playwright
from PIL import Image

def main():
    port, stop = sh.serve(sh.GAME)
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        pg = br.new_page(viewport={'width': 1000, 'height': 1200})
        pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=60000)
        pg.wait_for_function("() => typeof setState==='function'", timeout=60000)
        pg.wait_for_function("() => (window.__bofFrames|0) > 4", timeout=60000)
        pg.evaluate(sh.TRAP_RAF)
        pg.evaluate(sh.SETUP, {'state': 'PLAY', 'stage': 1, 'pilot': 'cole'})
        pg.evaluate("() => { window.playerHit=function(){}; enemies.length=0; }")
        for _ in range(6):
            pg.evaluate(sh.STEP, [8]); pg.wait_for_timeout(400)
        for ms in [0, 400, 800, 1200, 1600, 2000, 2400, 2800, 3200, 3600, 4000]:
            pg.evaluate("(v) => { mapScroll = v; }", ms)
            pg.evaluate(sh.STEP, [2]); pg.wait_for_timeout(120)
            d = pg.evaluate("() => { const c=document.getElementById('screen'); return c?c.toDataURL('image/png'):null; }")
            im = Image.open(io.BytesIO(base64.b64decode(d.split(',', 1)[1]))).convert('RGB')
            im = im.resize((60, 64))
            px = list(im.getdata())
            n = len(px)
            blue = sum(1 for r, g, b in px if b > r + 24) / n
            mr = sum(p[0] for p in px)/n; mg = sum(p[1] for p in px)/n; mb = sum(p[2] for p in px)/n
            print('mapScroll %5d  blue-dominant %.2f   mean rgb %3.0f/%3.0f/%3.0f' % (ms, blue, mr, mg, mb))
        br.close()
    stop()

if __name__ == '__main__':
    main()
