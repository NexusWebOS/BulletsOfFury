#!/usr/bin/env python3
"""probe_hammer_ball_1019.py - does the Hammer's ball actually turn on screen? Stage 5 (arch_spiked_ball) against the
Stage 8 Hammer form (f6_hammer_motion_<ball>), real Chromium, real time. For every blit of the ball sprite it records the
rotation of the live transform; reports the angle swept per second while in the 'ball' state, and h.angle's own rate.
  --bust  (Stage 8 only) disables the 1019 fix layer so the check can fail.
"""
import os, sys, json, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import shoot as sh

INSTR = r"""(cfg) => { const W = window; W.CA19_OFF = cfg.bust ? 1 : 0; W.__B = {samples: []};
  const isBall = cfg.which === 's5' ? (k => /^arch_spiked_ball/.test(k)) : (k => /^f6_hammer_motion_/.test(k));
  const tag = new WeakMap(); const g = XART.get; XART.get = function (k) { const r = g.apply(this, arguments); try { if (r && typeof r === 'object') tag.set(r, k); } catch (e) {} return r; };
  let rots = []; const dI = ctx.drawImage; ctx.drawImage = function (im) { const k = tag.get(im); if (k && isBall(k)) { const m = ctx.getTransform(); rots.push({k, a: Math.atan2(m.b, m.a)}); } return dI.apply(this, arguments); };
  const hammerOf = () => { if (cfg.which === 's5') return boss && boss._hammer ? boss : null;
    try { const b = boss; if (!b || !b._r30 || !b._r30.v18 || b._r30.v18.form !== 8) return null; return gd4Create(b, 8).p; } catch (e) { return null; } };
  W.__tick = setInterval(() => { const p = hammerOf(); const h = p && p._hammer;
    if (h && h.state === 'ball') W.__B.samples.push({t: performance.now() / 1000, angle: h.angle, rots: rots.slice(-3)});
    rots = []; }, 50);
  if (cfg.force) { const p = hammerOf(); if (p) { const h = p._hammer; hammerState(p, 'curl'); } }
  return true; }"""

S5 = r"""() => { playerHit = function(){}; ASSETS.ready = true; diffKey = 'normal'; run.mode = 'arcade';
  startRun(5); curStage = STAGES[4]; beginStage(5); setState(GS.PLAY); player.reset();
  try { BOFCinematicDirector.cancel(); } catch (e) {} try { fb2Intro = null; fb2Talk = null; story = null; } catch (e) {}
  stagePlan = []; enemies = []; spawnBoss(STAGES[4].boss); bossActive = true; bossWarned = true; return boss && boss.kind; }"""

def analyse(S, label):
    pts = [s for s in S if s['rots']]
    if len(pts) < 4:
        print(label, 'too few ball samples', len(S), len(pts)); return None
    import math
    sweep = 0; arate = 0
    for a, b in zip(pts, pts[1:]):
        d = b['rots'][-1]['a'] - a['rots'][-1]['a']
        d = (d + math.pi) % (2 * math.pi) - math.pi
        sweep += abs(d)
        arate += abs((b['angle'] or 0) - (a['angle'] or 0))
    dur = pts[-1]['t'] - pts[0]['t']
    r = {'samples': len(pts), 'secs': round(dur, 2), 'drawnDegPerSec': round(math.degrees(sweep) / max(dur, .01), 1),
         'hAngleDegPerSec': round(math.degrees(arate) / max(dur, .01), 1), 'keys': sorted({x['k'] for s in pts for x in s['rots']})}
    print(label, r, flush=True); return r

def wait_ball(frame, secs):
    for i in range(secs):
        time.sleep(1)
        n = frame.evaluate("() => window.__B.samples.length")
        if n > 60: break
    return frame.evaluate("() => { clearInterval(window.__tick); return window.__B.samples; }")

def main():
    bust = '--bust' in sys.argv
    from playwright.sync_api import sync_playwright
    port, stop = sh.serve(sh.GAME); out = {}
    with sync_playwright() as p:
        b = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
        if not bust:
            pg = b.new_page(viewport={'width': 1000, 'height': 1100})
            pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=120000)
            pg.wait_for_function("() => typeof setState==='function' && (window.__bofFrames|0) > 4", timeout=120000)
            pg.evaluate(S5); time.sleep(3); pg.evaluate(INSTR, {'which': 's5', 'bust': False, 'force': True})
            out['s5'] = analyse(wait_ball(pg, 40), 'stage5 spiked ball'); pg.close()
        pg = b.new_page(viewport={'width': 1400, 'height': 1100})
        pg.goto('http://127.0.0.1:%d/docs/previews/stage8_pixellab_1018/index.html?scene=hammer&difficulty=normal' % port, wait_until='load', timeout=120000)
        fr = None
        for i in range(240):
            time.sleep(0.5)
            fr = next((f for f in pg.frames if f != pg.main_frame), None)
            try:
                if fr and fr.evaluate("() => { try { return !!(boss && boss._r30 && boss._r30.v18 && boss._r30.v18.form === 8); } catch (e) { return false; } }"): break
            except Exception: pass
        time.sleep(3); fr.evaluate(INSTR, {'which': 's8', 'bust': bust, 'force': True})
        out['s8'] = analyse(wait_ball(fr, 40), 'stage8 hammer ball' + (' (bust)' if bust else ''))
        b.close()
    stop()
    s8 = out.get('s8') or {}
    good = bool(s8) and s8['drawnDegPerSec'] >= 0.5 * s8['hAngleDegPerSec'] and s8['drawnDegPerSec'] > 90
    print(('ok   ' if good else 'FAIL ') + 'Stage 8 ball turns on screen at its own spin rate')
    sys.exit(0 if good else 1)

if __name__ == '__main__':
    main()
