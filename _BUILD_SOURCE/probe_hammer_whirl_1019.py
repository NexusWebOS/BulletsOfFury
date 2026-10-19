#!/usr/bin/env python3
"""probe_hammer_whirl_1019.py - the Stage-8 Hammer form's whirlwind must wind up and accelerate like the real Stage-5
Hammer's. Real Chromium, real time, through Codex's Stage-8 review page (scene=hammer). Starts a whirlwind with the
game's own hammerWhirlStart, then records which f6 whirl pose (8..11) is drawn each frame and h.whirl.reel.
  pass: pose changes/s in the last second of the whirl > 1.4x the first second, and the drawn pose tracks reel/2.
  --bust disables the 1019 layer (window.CA19_OFF=1): the flat t*9 clock - must fail.
"""
import os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import shoot as sh

INSTR = r"""(bust) => { const W = window; W.CA19_OFF = bust ? 1 : 0; W.__W = [];
  const tag = new WeakMap(); const g = XART.get; XART.get = function (k) { const r = g.apply(this, arguments); try { if (r && typeof r === 'object') tag.set(r, k); } catch (e) {} return r; };
  let pose = null; const dI = ctx.drawImage; ctx.drawImage = function (im) { const k = tag.get(im); const m = k && /^f6_hammer_motion_(\d+)$/.exec(k); if (m) pose = +m[1]; return dI.apply(this, arguments); };
  const p = gd4Create(boss, 8).p; hammerWhirlStart(p); hammerState(p, 'whirlwind');
  W.__tick = setInterval(() => { const h = p._hammer; W.__W.push({t: performance.now() / 1000, st: h.state, pose, reel: h.whirl ? h.whirl.reel : null}); pose = null; }, 16);
  return true; }"""

def main():
    bust = '--bust' in sys.argv
    from playwright.sync_api import sync_playwright
    port, stop = sh.serve(sh.GAME)
    with sync_playwright() as p:
        b = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
        pg = b.new_page(viewport={'width': 1400, 'height': 1100})
        pg.goto('http://127.0.0.1:%d/docs/previews/stage8_pixellab_1018/index.html?scene=hammer&difficulty=hard' % port, wait_until='load', timeout=120000)
        fr = None
        for i in range(240):
            time.sleep(0.5)
            fr = next((f for f in pg.frames if f != pg.main_frame), None)
            try:
                if fr and fr.evaluate("() => { try { return !!(boss && boss._r30 && boss._r30.v18 && boss._r30.v18.form === 8); } catch (e) { return false; } }"): break
            except Exception: pass
        time.sleep(2); fr.evaluate(INSTR, bust)
        time.sleep(7)
        S = fr.evaluate("() => { clearInterval(window.__tick); return window.__W; }")
        b.close()
    stop()
    W = [s for s in S if s['st'] == 'whirlwind' and s['pose'] is not None and 8 <= s['pose'] <= 11]
    if len(W) < 20:
        print('FAIL too few whirlwind samples', len(W), set(s['st'] for s in S)); sys.exit(1)
    t0, t1 = W[0]['t'], W[-1]['t']
    def rate(a, b_):
        seg = [s for s in W if a <= s['t'] <= b_]
        ch = sum(1 for x, y in zip(seg, seg[1:]) if x['pose'] != y['pose'])
        return ch / max(.01, b_ - a)
    early, late = rate(t0, t0 + 1), rate(t1 - 1, t1)
    track = sum(1 for s in W if s['reel'] is not None and s['pose'] == 8 + (int(s['reel'] // 2) % 4)) / len(W)
    print('whirl %.1fs  pose changes/s first second %.1f, last second %.1f; pose==reel/2 on %.0f%% of frames' % (t1 - t0, early, late, track * 100))
    good = late > 1.4 * early and track > .8
    print(('ok   ' if good else 'FAIL ') + 'Stage-8 Hammer whirlwind winds up on the real Hammer reel clock')
    sys.exit(0 if good else 1)

if __name__ == '__main__':
    main()
