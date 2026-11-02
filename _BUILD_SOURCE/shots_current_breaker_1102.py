#!/usr/bin/env python3
"""shots_current_breaker_1102.py - Current Breaker phase-by-phase contact sheet in real Chromium (TRAP_RAF stepping).
Spawns cbreak alone on Stage 9 (stage clock held, plan empty, protected pilot), grabs the canvas every N frames with the
CB112 phase, then builds a labelled contact sheet. Also logs HP, phase timeline, hazards/reticles live and errors.
  python _BUILD_SOURCE/shots_current_breaker_1102.py [--diff furious] [--every 20] [--secs 46] [--out name]
"""
import os, sys, json, base64, io
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import shoot as sh
from PIL import Image, ImageDraw
A = sys.argv
DIFF = A[A.index('--diff') + 1] if '--diff' in A else 'furious'
EVERY = int(A[A.index('--every') + 1]) if '--every' in A else 20
SECS = int(A[A.index('--secs') + 1]) if '--secs' in A else 46
NAME = A[A.index('--out') + 1] if '--out' in A else DIFF
OUT = os.path.join(os.path.dirname(HERE), '_shots', 'cb_inspect_1102')
SETUP = r"""(d) => { ASSETS.ready = true; diffKey = d; DIFF = DIFFS[d]; run.mode = 'arcade'; coopOn = false;
  startRun(9); curStage = STAGES[8]; beginStage(9); setState(GS.PLAY); player.reset();
  try { BOFCinematicDirector.cancel(); } catch (e) {} for (const k of ['story','fb2Talk','fb2Intro','s6Opening']) { try { window.eval(k + '=null'); } catch (e) {} }
  playerHit = function(){}; stagePlan = []; window.__now = performance.now(); return true; }"""
SPAWN = r"""() => { for (const e of enemies) e.dead = true; enemies.length = 0; eBullets.length = 0; stagePlan = []; stageTimer = 2;
  player.x = (worldWidth() > viewW() ? camX : 0) + VW / 2; player.y = VH - 90; const n = enemies.length;
  spawnEnemy('cbreak', worldWidth() * .72, -124, {}); window.__cb = enemies.slice(n).find(e => e.type === 'cbreak'); return {hp: Math.round(window.__cb.hp), maxHp: Math.round(window.__cb.maxHp || window.__cb.hp)}; }"""
FIRE = '--fire' in A   # firing arm: pilot holds the real fire key and drifts under the Current Breaker
STEP = r"""(c) => { const n = c.n; for (let i = 0; i < n; i++) { stageTimer = 2; window.__now += 1000/60;
    if (c.fire) { const e = window.__cb; Input.keys.j = true; if (e && !e.dead) player.x += (e.x - player.x) * .05; }
    try { loop(window.__now); } catch (e) { window.__err = String(e).slice(0, 160); } }
  const e = window.__cb, q = e && e._cb112; return {phase: q ? q.phase : (e && e.dead ? 'dead' : '?'), t: q ? +q.t.toFixed(2) : 0, age: q ? +q.age.toFixed(2) : 0,
   x: e ? Math.round(e.x) : 0, y: e ? Math.round(e.y) : 0, hp: e ? Math.round(e.hp) : 0, dead: !e || e.dead, flash: e ? +(e.flash||0).toFixed(3) : 0, dying: e ? e._dyingT ?? null : null, bullets: eBullets.length,
   hazards: (typeof S911 !== 'undefined' && S911.hazards) ? S911.hazards.size : 0, err: window.__err || null}; }"""

def main():
    from playwright.sync_api import sync_playwright
    os.makedirs(OUT, exist_ok=True); port, stop = sh.serve(sh.GAME); frames, log, errs = [], [], []
    with sync_playwright() as p:
        b = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio']); pg = b.new_page(viewport={'width': 1000, 'height': 1100})
        pg.on('pageerror', lambda e: errs.append(str(e)[:200]))
        pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=180000)
        pg.wait_for_function("() => typeof setState==='function' && (window.__bofFrames|0) > 4", timeout=180000)
        pg.evaluate(sh.TRAP_RAF); pg.wait_for_timeout(60); pg.evaluate(SETUP, DIFF)
        for i in range(200):
            if pg.evaluate("() => { try { stageLoadTick(); return stageLoadReady(9); } catch (e) { return true; } }"): break
            pg.wait_for_timeout(100)
        s = pg.evaluate(SPAWN); print('spawn', s)
        last = None
        for k in range(SECS * 60 // EVERY):
            r = pg.evaluate(STEP, {"n": EVERY, "fire": FIRE}); pg.wait_for_timeout(8); log.append(r)
            if r['phase'] != last: print('%6.2fs %-18s x%4d y%4d hp%4d' % (k * EVERY / 60, r['phase'], r['x'], r['y'], r['hp']), flush=True); last = r['phase']
            d = pg.evaluate("() => document.getElementById('screen').toDataURL('image/png')")
            im = Image.open(io.BytesIO(base64.b64decode(d.split(',', 1)[1]))).convert('RGB'); frames.append((r, im))
            if r['dead']: break
        b.close()
    stop()
    # contact sheet: one tile per frame, labelled
    tw = 240; th = int(frames[0][1].height * tw / frames[0][1].width); cols = 8; rows = (len(frames) + cols - 1) // cols
    for page in range(0, rows, 6):
        sub = frames[page * cols:(page + 6) * cols]; rr = (len(sub) + cols - 1) // cols
        sheet = Image.new('RGB', (cols * tw, rr * (th + 16)), (16, 16, 20)); dr = ImageDraw.Draw(sheet)
        for i, (r, im) in enumerate(sub):
            x, y = i % cols * tw, i // cols * (th + 16); sheet.paste(im.resize((tw, th)), (x, y + 16))
            dr.text((x + 3, y + 2), '%s %.2f' % (r['phase'], r['t']), fill=(255, 230, 120))
        sheet.save(os.path.join(OUT, '%s_sheet_%d.jpg' % (NAME, page // 6)), quality=82)
    for r, im in frames: pass
    json.dump({'spawn': s, 'log': log, 'errors': errs}, open(os.path.join(OUT, '%s_log.json' % NAME), 'w'), indent=1)
    # also keep full-size frames at each phase start
    seen = set()
    for r, im in frames:
        if r['phase'] not in seen: seen.add(r['phase']); im.save(os.path.join(OUT, '%s_%s.png' % (NAME, r['phase'])))
    print('frames', len(frames), 'errors', errs[:3])

if __name__ == '__main__':
    main()
