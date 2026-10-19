#!/usr/bin/env python3
"""probe_hammer_compare_1019.py - Mike (overnight 1019): "Hammer form on level 8, doesnt spin properly like our actual
hammer boss does. I know his forms lack animation."

Real Chromium, real time. Records, for the real Stage-5 Hammer and for the Stage-8 Hammer form (entered through Codex's
own review page, docs/previews/stage8_pixellab_1018/?scene=hammer), every hammer state it enters and, per state, the
art families drawn (XART keys, digits folded) and the draw rotation range of the biggest blit. Also saves a contact
sheet of frames taken while each one is in a spin/whirlwind/ball/curl state.
"""
import os, sys, json, base64, io, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import shoot as sh
from PIL import Image
OUT = os.path.join(os.path.dirname(HERE), '_shots', 'claude_assist_1019')

INSTR = r"""(cfg) => { const W = window; W.__H = {states: {}, order: [], shots: []};
  const fam = k => String(k).replace(/[0-9]+/g, '#');
  const curKeys = new Set(); const g = XART.get; XART.get = function (k) { curKeys.add(fam(k)); return g.apply(this, arguments); };
  const rot = {v: []}; const dI = ctx.drawImage; ctx.drawImage = function (im) { const a = arguments; if (a.length >= 5) { const m = ctx.getTransform(); const w = (a.length === 9 ? a[7] : a[3]) * Math.hypot(m.a, m.b); if (w > 60) rot.v.push(Math.atan2(m.b, m.a)); } return dI.apply(this, a); };
  const hammerOf = () => { if (cfg.which === 's5') return boss && boss._hammer ? boss : null;
    try { const b = boss; if (!b || !b._r30 || !b._r30.v18 || b._r30.v18.form !== 8) return null; return gd4Create(b, 8).p; } catch (e) { return null; } };
  W.__tick = setInterval(() => { try {
    const p = hammerOf(); const st = p && p._hammer ? p._hammer.state : '(none)';
    const H = W.__H; let S = H.states[st]; if (!S) { S = H.states[st] = {n: 0, keys: {}, rmin: 9, rmax: -9}; }
    if (H.order[H.order.length - 1] !== st) H.order.push(st);
    S.n++; for (const k of curKeys) S.keys[k] = (S.keys[k] || 0) + 1;
    for (const r of rot.v) { S.rmin = Math.min(S.rmin, r); S.rmax = Math.max(S.rmax, r); }
    curKeys.clear(); rot.v = [];
    if (/spin|whirl|ball|curl/.test(st) && H.shots.length < 16 && S.n % 6 === 1) H.shots.push({st, img: document.getElementById('screen').toDataURL('image/jpeg', .7)});
    if (typeof player !== 'undefined') player.invuln = Math.max(player.invuln || 0, 0);
  } catch (e) {} }, 50);
  return true; }"""

S5 = r"""() => { playerHit = function(){}; ASSETS.ready = true; diffKey = 'normal'; run.mode = 'arcade';
  startRun(5); curStage = STAGES[4]; beginStage(5); setState(GS.PLAY); player.reset();
  try { BOFCinematicDirector.cancel(); } catch (e) {} try { fb2Intro = null; fb2Talk = null; story = null; } catch (e) {}
  stagePlan = []; enemies = []; spawnBoss(STAGES[4].boss); bossActive = true; bossWarned = true; return boss && boss.kind; }"""

def film(pg, frame, which, secs):
    frame.evaluate(INSTR, {'which': which})
    for i in range(secs):
        time.sleep(1)
        if i % 10 == 0:
            print(which, i, frame.evaluate("() => window.__H.order.slice(-6).join(' > ')"), flush=True)
    H = frame.evaluate("() => { clearInterval(window.__tick); return window.__H; }")
    return H

def main():
    secs = int(sys.argv[1]) if len(sys.argv) > 1 else 70
    from playwright.sync_api import sync_playwright
    os.makedirs(OUT, exist_ok=True)
    port, stop = sh.serve(sh.GAME)
    rep = {}
    with sync_playwright() as p:
        b = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
        # Stage 5 boss
        pg = b.new_page(viewport={'width': 1000, 'height': 1100})
        pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=120000)
        pg.wait_for_function("() => typeof setState==='function' && (window.__bofFrames|0) > 4", timeout=120000)
        print('stage5 boss', pg.evaluate(S5), flush=True)
        rep['s5'] = film(pg, pg, 's5', secs); pg.close()
        # Stage 8 hammer form via Codex's review page
        pg = b.new_page(viewport={'width': 1400, 'height': 1100})
        pg.goto('http://127.0.0.1:%d/docs/previews/stage8_pixellab_1018/index.html?scene=hammer&difficulty=normal' % port, wait_until='load', timeout=120000)
        fr = None
        for i in range(240):
            time.sleep(0.5)
            fr = next((f for f in pg.frames if f != pg.main_frame), None)
            try:
                if fr and fr.evaluate("() => { try { return !!(boss && boss._r30 && boss._r30.v18 && boss._r30.v18.form === 8); } catch (e) { return false; } }"): break
            except Exception: pass
        print('stage8 hammer form ready', bool(fr), flush=True)
        rep['s8'] = film(pg, fr, 's8', secs)
        b.close()
    stop()
    tiles = []
    for which in ('s5', 's8'):
        H = rep[which]
        print('\n==', which, 'state order:', ' > '.join(H['order'][:40]))
        for st, S in sorted(H['states'].items(), key=lambda kv: -kv[1]['n']):
            top = sorted(S['keys'].items(), key=lambda kv: -kv[1])[:6]
            print('  %-16s n=%-4d rot %.2f..%.2f  %s' % (st, S['n'], S['rmin'], S['rmax'], [k for k, _ in top]))
        for s in H['shots']:
            im = Image.open(io.BytesIO(base64.b64decode(s['img'].split(',', 1)[1]))).convert('RGB'); im.thumbnail((360, 400)); tiles.append((which + ' ' + s['st'], im))
        H.pop('shots', None)
    if tiles:
        from PIL import ImageDraw
        cols = 6; w, h = 360, 400; rows = (len(tiles) + cols - 1) // cols
        S = Image.new('RGB', (w * cols, h * rows))
        for i, (lab, im) in enumerate(tiles):
            S.paste(im, ((i % cols) * w, (i // cols) * h)); ImageDraw.Draw(S).text(((i % cols) * w + 4, (i // cols) * h + 4), lab, fill=(255, 255, 0))
        S.save(os.path.join(OUT, 'hammer_compare.jpg'))
    json.dump(rep, open(os.path.join(OUT, 'hammer_compare.json'), 'w'), indent=1)

if __name__ == '__main__':
    main()
