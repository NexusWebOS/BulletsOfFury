#!/usr/bin/env python3
"""probe_player_shield_1018.py - every pilot's shield, rendered in real Chromium, cropped around the ship.

Mike: "all player shields need to be glowing an animated and properly centered with them."
Writes _shots/shield_1018/<tag>_sheet.png: nine pilots x 4 animation moments, plus centring numbers
(shield ink centre vs hull ink centre, measured off the canvas with and without the shield)."""
import os, sys, json, base64, io
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import shoot as sh
from PIL import Image, ImageChops
OUT = os.path.join(os.path.dirname(HERE), '_shots', 'shield_1018')
PILOTS = ['cole', 'maverick', 'lizzie', 'juggernaut', 'yuri', 'freezer', 'falva', 'decker', 'axel']

SETUP = r"""(cfg) => {
  ASSETS.ready = true; diffKey = 'normal'; run.mode = 'arcade';
  const pi = PILOTS.findIndex(p => p.key === cfg.pilot); if (pi >= 0) pilotIndex = pi;
  startRun(cfg.stage); curStage = STAGES[cfg.stage - 1]; beginStage(cfg.stage); setState(GS.PLAY); player.reset();
  playerHit = function(){}; stagePlan = []; enemies.length = 0; run.pilot = cfg.pilot;
  window.__now = performance.now(); for (const k of Object.keys(XART._src || {})) if (/shield/.test(k)) XART.rdy(k);
  return run.pilot; }"""
STEP = r"""(n) => { for (let i = 0; i < n; i++) { window.__now += 1000/60; enemies.length = 0; eBullets.length = 0; player.invuln = 0; player.x = 340; player.y = 380;
  try { loop(window.__now); } catch (e) { window.__err = String(e).slice(0,200); } } return {cam: (worldWidth() > viewW()) ? camX : 0, z: viewZoom(), ss: document.getElementById('screen').width / VW, err: window.__err || null}; }"""
GRAB = r"""(on) => { run.shield = on ? 3 : 0; window.__now += 1000/60; enemies.length = 0; eBullets.length = 0; player.invuln = 0; player.x = 340; player.y = 380;
  try { loop(window.__now); } catch (e) {} return document.getElementById('screen').toDataURL('image/png'); }"""

def img(d): return Image.open(io.BytesIO(base64.b64decode(d.split(',', 1)[1]))).convert('RGBA')

def main():
    tag = sys.argv[1] if len(sys.argv) > 1 else 'before'
    stage = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    os.makedirs(OUT, exist_ok=True)
    from playwright.sync_api import sync_playwright
    port, stop = sh.serve(sh.GAME)
    rows, nums = [], {}
    with sync_playwright() as p:
        b = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
        for pk in PILOTS:
            pg = b.new_page(viewport={'width': 1000, 'height': 1100})
            pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=120000)
            pg.wait_for_function("() => typeof setState==='function' && (window.__bofFrames|0) > 4", timeout=120000)
            pg.evaluate(sh.TRAP_RAF); pg.wait_for_timeout(60)
            pg.evaluate(SETUP, {'pilot': pk, 'stage': stage})
            for i in range(4): pg.evaluate(STEP, 30); pg.wait_for_timeout(250)
            st = pg.evaluate(STEP, 1)
            k = st['ss']; sx = k * (340 - st['cam']); sy = k * 380; R = int(70 * k)
            box = (int(sx - R), int(sy - R), int(sx + R), int(sy + R))
            base = img(pg.evaluate(GRAB, False)).crop(box)
            frames = []
            for k in range(4):
                pg.evaluate(STEP, 7)
                frames.append(img(pg.evaluate(GRAB, True)).crop(box))
            # shield ink = pixels that differ from the no-shield frame
            diff = ImageChops.difference(frames[0].convert('RGB'), base.convert('RGB')).convert('L').point(lambda v: 255 if v > 24 else 0)
            bb = diff.getbbox()
            hull = ImageChops.difference(base.convert('RGB'), img(pg.evaluate("() => { const s=player.x; player.x=-999; window.__now+=1000/60; try{loop(window.__now);}catch(e){} player.x=s; return document.getElementById('screen').toDataURL('image/png'); }")).crop(box).convert('RGB')).convert('L').point(lambda v: 255 if v > 24 else 0).getbbox()
            c = lambda q: None if not q else (round((q[0] + q[2]) / 2 - R, 1), round((q[1] + q[3]) / 2 - R, 1))
            nums[pk] = {'shield_bbox_centre': c(bb), 'hull_bbox_centre': c(hull), 'shield_bbox': bb, 'hull_bbox': hull, 'err': st['err']}
            # temporal change between shield frames: is it animated?
            nums[pk]['anim_px'] = sum(1 for v in ImageChops.difference(frames[0].convert('RGB'), frames[2].convert('RGB')).convert('L').getdata() if v > 24)
            row = Image.new('RGBA', (2 * R * 5, 2 * R), (0, 0, 0, 255))
            row.paste(base, (0, 0))
            for k, f in enumerate(frames): row.paste(f, (2 * R * (k + 1), 0))
            rows.append(row)
            print(pk, json.dumps(nums[pk]), flush=True)
            pg.close()
        b.close()
    stop()
    sheet = Image.new('RGBA', (rows[0].width, rows[0].height * len(rows)))
    for i, r in enumerate(rows): sheet.paste(r, (0, i * r.height))
    sheet.resize((sheet.width // 2, sheet.height // 2)).save(os.path.join(OUT, '%s_sheet.png' % tag))
    json.dump(nums, open(os.path.join(OUT, '%s.json' % tag), 'w'), indent=1)

if __name__ == '__main__':
    main()
