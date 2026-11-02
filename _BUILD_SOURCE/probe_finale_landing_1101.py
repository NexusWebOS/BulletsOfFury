#!/usr/bin/env python3
"""probe_finale_landing_1101.py - Stage-5 finale (normal_finale_1031.js, 1101 pass):
  1. HQ leg flies FORWARD into the screen: during the hangar half of the flight the jet moves up the screen (away from
     the camera) every sample and its scale frame only grows (= the sprite only shrinks), ending small on the runway
     near the hangar door; it starts large near the bottom. Checked solo and co-op (wingman follows the same rule).
  2. The difficulty choice rows are drawn in the graphical Pixelmap Fury Strike face (PM27 events), selected row in its
     palette, unselected rows on the dim plane - Easy (3 rows) and Normal (2 rows).
Real Chromium; flight sampled through nf100Blit; contact sheet + menus in _shots/finale_landing_1101/.
"""
import os, sys, base64, io
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import shoot as sh
from PIL import Image, ImageDraw
OUT = os.path.join(os.path.dirname(HERE), '_shots', 'finale_landing_1101')

PREP = r"""() => { ASSETS.ready = true; window.__now = performance.now(); try { localStorage.clear(); } catch (e) {}
  const B = nf100Blit; window.__blits = []; nf100Blit = function (n, f, x, y) { if (/^ship_/.test(n)) window.__blits.push({n, f, x: Math.round(x), y: Math.round(y), t: NF100.current ? +NF100.current.t.toFixed(3) : null}); return B.apply(this, arguments); };
  return true; }"""

OPEN = r"""(c) => { diffKey = c.diff; DIFF = difficultyForRun('campaign', c.diff); startRun(5); run.mode = 'campaign'; run.stage = 5; curStage = STAGES[4];
  coopOn = !!c.coop; if (c.coop) { try { run2.pilot = 'lizzie'; } catch (e) {} }
  NF100.current = null; scLeaveStage({bonus: 0, rank: 'A'}); window.__blits = []; PM27.events.length = 0;
  return {state: String(state), phase: NF100.current && NF100.current.phase, second: NF100.current && NF100.current.second, pilot: run.pilot,
    w16: ['NORMAL - STANDARD FURY','HARD - THE NEXT CHALLENGE','FURIOUS - THE TRUE WAR'].map(t => [t, pm27Width(t, 16, 'fury_strike'), pm27Width(t, 18, 'fury_strike')])}; }"""

STEP = r"""(n) => { for (let i = 0; i < n; i++) { window.__now += 1000/60; try { loop(window.__now); } catch (e) { window.__err = String(e).slice(0, 200); } }
  const A = NF100.current; return {state: String(state), phase: A && A.phase, t: A ? A.t : null, err: window.__err || null}; }"""

MENU = r"""(sel) => { const A = NF100.current; A.phase = 'menu'; A.t = 1; A.sel = sel; PM27.events.length = 0;
  window.__now += 1000/60; loop(window.__now);
  const labels = nf100Options(A).map(o => o.label);
  return {labels, ev: PM27.events.filter(e => labels.includes(e.text)).map(e => ({text: e.text, family: e.family, palette: e.palette, h: e.height}))}; }"""

def grab(pg):
    d = pg.evaluate("() => document.getElementById('screen').toDataURL('image/png')")
    return Image.open(io.BytesIO(base64.b64decode(d.split(',', 1)[1]))).convert('RGB')

def main():
    from playwright.sync_api import sync_playwright
    os.makedirs(OUT, exist_ok=True)
    port, stop = sh.serve(sh.GAME)
    res, errs = [], []
    def check(name, ok, info=''):
        res.append(bool(ok)); print(('ok   ' if ok else 'FAIL ') + name + ('   ' + str(info)[:400] if info else ''), flush=True)
    with sync_playwright() as p:
        b = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
        pg = b.new_page(viewport={'width': 1000, 'height': 1100})
        pg.on('pageerror', lambda e: errs.append('page: ' + str(e)[:200]))
        pg.on('console', lambda m: errs.append('console: ' + m.text[:200]) if m.type == 'error' else None)
        pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=180000)
        pg.wait_for_function("() => typeof setState==='function' && (window.__bofFrames|0) > 4", timeout=180000)
        pg.evaluate(sh.TRAP_RAF); pg.wait_for_timeout(60)
        pg.evaluate(PREP)
        for coop in (False, True):
            tag = 'co-op' if coop else 'solo'
            r = pg.evaluate(OPEN, {'diff': 'normal', 'coop': coop})
            pg.wait_for_function("() => nf100Warm()", timeout=60000)
            check('%s: Stage-5 clear opens the return flight' % tag, r['phase'] == 'flight', r)
            print('     widths', r['w16'])
            frames = []
            for k in range(46):
                s = pg.evaluate(STEP, 10); pg.wait_for_timeout(10)
                if not coop and k % 3 == 2 and s['phase'] == 'flight': frames.append(('t=%.1f' % s['t'], grab(pg)))
                if s['phase'] != 'flight': break
            B = pg.evaluate("() => window.__blits")
            pil = [x for x in B if x['t'] is not None and x['t'] > 3.45 and x['n'] == 'ship_' + r['pilot']]
            mate = [x for x in B if x['t'] is not None and x['t'] > 3.45 and x['n'] != 'ship_' + r['pilot']]
            ys = [x['y'] for x in pil]; fs = [x['f'] for x in pil]
            check('%s: HQ leg sampled' % tag, len(pil) > 20, len(pil))
            if len(pil) > 20:
                check('%s: jet moves up the screen (away from camera) the whole HQ leg' % tag, all(b2 <= a2 for a2, b2 in zip(ys, ys[1:])) and ys[0] - ys[-1] > 200, (ys[:3], ys[-3:]))
                check('%s: jet only shrinks (scale frame never decreases)' % tag, all(b2 >= a2 for a2, b2 in zip(fs, fs[1:])) and fs[-1] - fs[0] >= 30, (fs[:3], fs[-3:]))
                check('%s: starts large near the bottom, ends small at the hangar runway' % tag, fs[0] <= 3 and ys[0] + 48 > 480 and 37 <= fs[-1] <= 47 and 230 <= ys[-1] + 48 <= 330 and 200 <= pil[-1]['x'] + 64 <= 330, (pil[0], pil[-1]))
            if coop:
                mf = [x['f'] for x in mate]; my = [x['y'] for x in mate]
                check('co-op: wingman flies the same forward path', len(mate) > 20 and all(b2 >= a2 for a2, b2 in zip(mf, mf[1:])) and all(b2 <= a2 for a2, b2 in zip(my, my[1:])), (mate[:1], mate[-1:]))
            if frames:
                w, h = 240, 256; S = Image.new('RGB', (w * len(frames), h))
                for i, (lab, im) in enumerate(frames):
                    im = im.resize((w, int(im.height * w / im.width))); S.paste(im, (i * w, 0)); ImageDraw.Draw(S).text((i * w + 4, 4), lab, fill=(255, 255, 0))
                S.save(os.path.join(OUT, 'flight-sheet.png'))
        for diff, n in (('easy', 3), ('normal', 2)):
            pg.evaluate(OPEN, {'diff': diff, 'coop': False})
            for sel in range(n):
                m = pg.evaluate(MENU, sel); grab(pg).save(os.path.join(OUT, '%s-menu-%d.png' % (diff, sel)))
            fam = set(e['family'] for e in m['ev']); seen = set(e['text'] for e in m['ev'])
            check('%s menu: every choice row drawn in Fury Strike' % diff.upper(), seen == set(m['labels']) and fam == {'fury_strike'}, m['ev'])
            check('%s menu: all rows share one size' % diff.upper(), len(set(e['h'] for e in m['ev'])) == 1, m['ev'])
            sel_pal = [e['palette'] for e in m['ev'] if e['text'] == m['labels'][n - 1]]
            check('%s menu: selected row uses its palette, others chrome' % diff.upper(), sel_pal and sel_pal[0] != 'chrome' and all(e['palette'] == 'chrome' for e in m['ev'] if e['text'] != m['labels'][n - 1]), m['ev'])
        check('no page/console errors', not errs, errs[:4])
        b.close()
    stop()
    print('%d/%d passed' % (sum(res), len(res)))
    sys.exit(0 if all(res) else 1)

if __name__ == '__main__':
    main()
