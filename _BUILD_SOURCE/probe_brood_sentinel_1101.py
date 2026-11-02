#!/usr/bin/env python3
"""probe_brood_sentinel_1101.py - Brood Sentinel 1101 layer (assets/brood_sentinel_1101.js), real Chromium.
Per difficulty (normal/hard/furious), the real ll18brood spawned on Stage 7, its own clock:
  - claw tell: both claws rotate OUTWARD/BACK (tips rise above the mount) before the lunge
  - claw strike: during the lunge the claws swing FORWARD (tips sweep inward/down past the start pose), contact live
  - maw: exactly 3 fans per cycle, each with the rank's fly count, released from the mouth, spread across a wide arc
  - flies: drawn at 64 px, shootable (real player fire in the 'firing' arm destroys them) and each kill bursts
    into blood (BS111 'blood' events + actual blood-sheet blits)
  - flies that reach a passive pilot still register real hits (playerHit counted, not stubbed away)
Frames saved to _shots/brood_sentinel_1101/.
"""
import os, sys, base64, io, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import shoot as sh
from PIL import Image
OUT = os.path.join(os.path.dirname(HERE), '_shots', 'brood_sentinel_1101')

SETUP = r"""(d) => { ASSETS.ready = true; diffKey = d; DIFF = DIFFS[d]; run.mode = 'arcade'; coopOn = false;
  startRun(7); curStage = STAGES[6]; beginStage(7); setState(GS.PLAY); player.reset();
  try { BOFCinematicDirector.cancel(); } catch (e) {} for (const k of ['story','fb2Talk','fb2Intro','s6Opening']) { try { window.eval(k + '=null'); } catch (e) {} }
  stagePlan = []; window.__now = performance.now(); window.__hits = 0;
  const PH = playerHit; playerHit = function () { window.__hits++; player.invuln = 0.05; };  // count real contacts, keep the pilot alive
  const tag = new WeakMap(), g = XART.get; XART.get = function (k) { const r = g.apply(this, arguments); try { if (r && typeof r === 'object') tag.set(r, k); } catch (e) {} return r; };
  window.__blits = {}; const dI = ctx.drawImage; ctx.drawImage = function (im) { const k = tag.get(im); if (k === 'bs111_blood_burst' || k === 's711_fly') { const w = arguments.length >= 9 ? arguments[7] : arguments[3]; (window.__blits[k] = window.__blits[k] || []).push(Math.round(w)); } return dI.apply(this, arguments); };
  return true; }"""
SPAWN = r"""(c) => { for (const e of enemies) e.dead = true; enemies.length = 0; eBullets.length = 0; stagePlan = []; stageTimer = 2; BS111.events.length = 0; window.__hits = 0; window.__blits = {};
  player.x = (worldWidth() > viewW() ? camX : 0) + VW / 2; player.y = VH - 90;
  spawnEnemy('ll18brood', worldWidth() / 2, -120, {}); const e = enemies[enemies.length - 1]; window.__B = e; window.__log = [];
  return {type: e && e.type, model: e && e._s711 && e._s711.model, hp: e && e.hp}; }"""
STEP = r"""(c) => { const e = window.__B, W = window;
  for (let i = 0; i < c.n; i++) { stageTimer = 2; W.__now += 1000/60;
    if (c.fire) { Input.keys.j = true; player.x += ((e ? e.x : player.x) - player.x) * .04; if (e && !e.dead) e.hp = Math.max(e.hp, 150); }  // test-only: keep the Brood alive so only flies are shot down
    try { loop(W.__now); } catch (err) { W.__err = String(err).slice(0, 160); }
    if (e && e._s711) { const A = e._s711, q0 = s711Part(e, 0), q1 = s711Part(e, 1);
      W.__log.push({ph: A.phase, t: +A.t.toFixed(3), ex: Math.round(e.x), ey: Math.round(e.y), a0: +A.angles[0]?.toFixed(3), a1: +A.angles[1]?.toFixed(3),
        t0: [Math.round(q0.tip.x - q0.x), Math.round(q0.tip.y - q0.y)], t1: [Math.round(q1.tip.x - q1.x), Math.round(q1.tip.y - q1.y)],
        flies: eBullets.filter(b => b._s711Kind === 'broodfly' && !b.dead).length}); } }
  if (c.fire) Input.keys.j = false;
  return {err: W.__err || null, phase: e && e._s711 && e._s711.phase, dead: !e || e.dead}; }"""

def grab(pg, box=None):
    d = pg.evaluate("() => document.getElementById('screen').toDataURL('image/png')")
    im = Image.open(io.BytesIO(base64.b64decode(d.split(',', 1)[1]))).convert('RGB')
    return im

def main():
    from playwright.sync_api import sync_playwright
    os.makedirs(OUT, exist_ok=True)
    port, stop = sh.serve(sh.GAME); res = []; errs = []
    def check(name, ok, info=''):
        res.append(bool(ok)); print(('ok   ' if ok else 'FAIL ') + name + ('   ' + str(info)[:330] if info else ''), flush=True)
    NF = {'normal': 7, 'hard': 9, 'furious': 11}
    with sync_playwright() as p:
        b = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
        for diff in ('normal', 'hard', 'furious'):
            pg = b.new_page(viewport={'width': 1000, 'height': 1100})
            pg.on('pageerror', lambda e: errs.append('page: ' + str(e)[:200]))
            pg.on('console', lambda m: errs.append('console: ' + m.text[:200]) if m.type == 'error' else None)
            pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=180000)
            pg.wait_for_function("() => typeof setState==='function' && (window.__bofFrames|0) > 4", timeout=180000)
            pg.evaluate(sh.TRAP_RAF); pg.wait_for_timeout(60); pg.evaluate(SETUP, diff)
            for i in range(200):
                if pg.evaluate("() => { try { stageLoadTick(); return stageLoadReady(7) && XART.rdy('bs111_blood_burst') && XART.rdy('s711_fly'); } catch (e) { return true; } }"): break
                pg.wait_for_timeout(100)
            D = diff.upper()
            # ---- passive arm: claws + fans + hits
            pg.evaluate(SPAWN, {}); shots = {}
            for k in range(14 * 6):
                s = pg.evaluate(STEP, {'n': 10, 'fire': False}); pg.wait_for_timeout(8)
                L = pg.evaluate("() => window.__log.slice(-1)[0] || null")
                if L:
                    key = None
                    if L['ph'] == 'claw-tell' and 'tell' not in shots and L['t'] > .8: key = 'tell'
                    if L['ph'] == 'claw' and 'strike' not in shots and L['t'] > .3: key = 'strike'
                    if L['ph'] == 'mouth-fire' and 'fan' not in shots and L['flies'] >= NF[diff] * 2: key = 'fan'
                    if key: shots[key] = grab(pg); shots[key].save(os.path.join(OUT, '%s-%s.png' % (diff, key)))
                if s['dead']: break
            Lg = pg.evaluate("() => window.__log"); ev = pg.evaluate("() => BS111.events"); hits = pg.evaluate("() => window.__hits")
            # first claw cycle only: the contiguous tell, then the contiguous lunge that follows it
            def run_of(ph, after=0):
                i = next((j for j in range(after, len(Lg)) if Lg[j]['ph'] == ph), None)
                if i is None: return [], len(Lg)
                k = i
                while k < len(Lg) and Lg[k]['ph'] == ph: k += 1
                return Lg[i:k], k
            tell, endt = run_of('claw-tell'); claw, _ = run_of('claw', endt)
            if tell and claw:
                s0 = tell[0]; wb = tell[-1]
                # tip vector relative to the mount: wind-up raises tips (y smaller) and moves them outward (left claw x<0, right x>0)
                check('%s claws wind OUTWARD and BACK during the tell' % D, wb['t0'][1] < s0['t0'][1] - 20 and wb['t0'][0] < s0['t0'][0] - 20 and wb['t1'][1] < s0['t1'][1] - 20 and wb['t1'][0] > s0['t1'][0] + 20, (s0['t0'], wb['t0'], s0['t1'], wb['t1']))
                fwd = max(claw, key=lambda x: x['t'])
                mid = [x for x in claw if x['a0'] is not None]
                swung = min(mid, key=lambda x: x['a0'])
                check('%s claws swing FORWARD across the front on the lunge' % D, swung['t0'][0] > s0['t0'][0] and swung['t1'][0] < s0['t1'][0] and swung['t0'][1] > wb['t0'][1] + 40, (wb['t0'], swung['t0'], swung['t1']))
                body = max(math.hypot(x['ex'] - claw[0]['ex'], x['ey'] - claw[0]['ey']) for x in claw)
                held = [x for x in claw if x['t'] < .12]
                check('%s claws stay drawn back while the body launches' % D, held and all(abs(x['a0'] - wb['a0']) < .25 for x in held) and body > 60, (len(held), round(body)))
            else:
                check('%s claw cycle observed' % D, False, (len(tell), len(claw)))
            fans = [e for e in ev if e['event'] == 'fan']
            first = fans[:3]
            check('%s maw releases 3 fans per cycle' % D, len(first) == 3 and [f['fan'] for f in first] == [0, 1, 2], fans[:4])
            check('%s each fan has %d flies' % (D, NF[diff]), first and all(f['flies'] == NF[diff] for f in first), first)
            flysz = pg.evaluate("() => (window.__blits.s711_fly || []).slice(-50)")
            check('%s flies drawn at 64 px' % D, flysz and set(flysz) == {64}, sorted(set(flysz))[:5])
            check('%s flies that reach a passive pilot still hit' % D, hits > 0, hits)
            # ---- firing arm: shoot the flies down
            pg.evaluate(SPAWN, {});
            for k in range(14 * 6):
                s = pg.evaluate(STEP, {'n': 10, 'fire': True}); pg.wait_for_timeout(8)
                if 'blood' not in shots and pg.evaluate("() => BS111.fx.length") > 0: shots['blood'] = grab(pg); shots['blood'].save(os.path.join(OUT, '%s-blood.png' % diff))
                if s['dead']: break
            ev = pg.evaluate("() => BS111.events"); blood = [e for e in ev if e['event'] == 'blood']
            early = [e for e in blood if e['t'] < 2.5]
            check('%s player fire shoots flies down (early deaths in flight)' % D, len(early) >= 3, (len(blood), len(early)))
            bb = pg.evaluate("() => (window.__blits.bs111_blood_burst || []).length")
            check('%s each kill bursts into blood (blood sheet actually drawn)' % D, bb > 0, bb)
            pg.close()
        check('no page/console errors', not errs, errs[:4])
        b.close()
    stop()
    print('%d/%d passed' % (sum(res), len(res)))
    sys.exit(0 if all(res) else 1)

if __name__ == '__main__':
    main()
