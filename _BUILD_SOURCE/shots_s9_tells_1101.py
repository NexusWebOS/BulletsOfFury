#!/usr/bin/env python3
"""shots_s9_tells_1101.py - contact sheet of every Stage-9 type at the end of its tell (warning fully drawn) and
just after its volley releases, so the FOV lanes can be checked against the guns and the rounds. Real Chromium.
Uses probe_s9_fov_1101's spawn path. Writes _shots/s9_tells_1101/sheet_<n>.png."""
import os, sys, base64, io
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import shoot as sh, probe_s9_fov_1101 as P
from PIL import Image, ImageDraw
OUT = os.path.join(os.path.dirname(HERE), '_shots', 's9_tells_1101')

def grab(pg):
    d = pg.evaluate("() => document.getElementById('screen').toDataURL('image/png')")
    return Image.open(io.BytesIO(base64.b64decode(d.split(',', 1)[1]))).convert('RGB')

def main():
    from playwright.sync_api import sync_playwright
    os.makedirs(OUT, exist_ok=True)
    port, stop = sh.serve(sh.GAME); tiles = []
    with sync_playwright() as p:
        b = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio']); pg = b.new_page(viewport={'width': 1000, 'height': 1100})
        pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=180000)
        pg.wait_for_function("() => typeof setState==='function' && (window.__bofFrames|0) > 4", timeout=180000)
        pg.evaluate(sh.TRAP_RAF); pg.wait_for_timeout(60); pg.evaluate(P.SETUP, 'hard')
        for i in range(200):
            if pg.evaluate("() => { try { stageLoadTick(); return stageLoadReady(9); } catch (e) { return true; } }"): break
            pg.wait_for_timeout(100)
        for typ, x, y, o in P.CAST:
            key = typ + ('/' + o['_s9Role'] if '_s9Role' in o else '')
            pg.evaluate(P.SPAWN, {'type': typ, 'x': x, 'y': y, 'opts': o})
            got = {}
            for k in range(14 * 20):
                pg.evaluate(P.STEP, 3)
                st = pg.evaluate("() => { const e = [...window.__U].find(u => !u.dead); const A = e && e._s911; if (!A) return null; return {ph: A.phase, atk: A.attack, t: A.t, warm: A.warm, x: e.x - ((worldWidth() > viewW()) ? camX : 0)}; }")
                if not st: break
                if st['ph'] in ('tell', 'pass') and 'tell' not in got and (st['ph'] == 'pass' or st['t'] > st['warm'] * .85) and 20 < st['x'] < 460:
                    got['tell'] = (grab(pg), '%s %s' % (st['atk'] or st['ph'], 'tell'))
                elif 'tell' in got and 'fire' not in got and st['ph'] in ('fire', 'dash', 'beam', 'flight', 'pass'):
                    pg.evaluate(P.STEP, 9); got['fire'] = (grab(pg), '%s release' % (st['atk'] or st['ph']))
                if len(got) == 2: break
            for k2 in ('tell', 'fire'):
                if k2 in got: im, lab = got[k2]; tiles.append(('%s: %s' % (key, lab), im))
        b.close()
    stop()
    per = 12
    for n in range(0, len(tiles), per):
        grp = tiles[n:n + per]; cols = 6; w, h = 240, 256; rows = (len(grp) + cols - 1) // cols
        S = Image.new('RGB', (w * cols, h * rows))
        for i, (lab, im) in enumerate(grp):
            S.paste(im.resize((w, h)), ((i % cols) * w, (i // cols) * h)); ImageDraw.Draw(S).text(((i % cols) * w + 3, (i // cols) * h + 3), lab, fill=(255, 255, 0))
        S.save(os.path.join(OUT, 'sheet_%d.png' % (n // per))); print('sheet', n // per, len(grp))

if __name__ == '__main__':
    main()
