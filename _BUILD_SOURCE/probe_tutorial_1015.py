#!/usr/bin/env python3
"""probe_tutorial_1015.py - the training flight, driven in real Chromium with key presses only.

    python _BUILD_SOURCE/probe_tutorial_1015.py            # all arms
    python _BUILD_SOURCE/probe_tutorial_1015.py --pilot juggernaut

Arms:
  ask      a Stage-1 start off pilot select stops on GS.TUTASK; YES is the default; UP/DOWN move it
  flight   YES -> the training card -> PLAY -> every lesson completed by an input-only driver, nothing
           foreign on the field, no life lost -> hands back to a normal Stage-1 start, mode restored
  no       NO starts the game exactly as before (arcade: INTRO; campaign: its prologue / the map)
  skip     pause -> SKIP TUTORIAL ends the flight and starts Stage 1
  bypass   a password start (stage 3) and a non-pilot-screen start never ask
Frames: _shots/tutorial_1015/.
"""
import os, sys, json, time, base64, argparse
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))
sys.path.insert(0, HERE)
import shoot as sh  # noqa: E402

OUT = os.path.join(ROOT, '_shots', 'tutorial_1015')

SETUP = r"""(cfg) => {
  ASSETS.ready = true;
  try { achToastPush = function(){}; } catch (e) {}
  const pi = PILOTS.findIndex(p => p.key === cfg.pilot); if (pi >= 0) pilotIndex = pi;
  diffKey = 'normal'; coopOn = false; run.mode = cfg.mode || 'arcade'; run.ngplus = false;
  if (cfg.clear) BOFTUTORIAL.reset();
  for (const k of ['a','d','w','s','j','k','c','y','h','p','enter','arrowup','arrowdown']) if (Input.keys[k] === undefined) Input.keys[k] = false;
  setState(GS.PILOT);
  return state;
}"""

# the driver: reads the screen state the way a player would and presses keys - never writes game state
DRIVER = r"""() => {
  const K = Input.keys;
  const TD = window.TD = {i: 0, taps: [], log: [], held: {}, lastLesson: -1, roll: 0};
  function tap(k){ if (K[k] === undefined) K[k] = false; Input.injectTap(k); }
  function steer(tx, ty, dead){
    dead = dead || 6;
    K.a = tx < player.x - dead; K.d = tx > player.x + dead;
    K.w = ty < player.y - dead; K.s = ty > player.y + dead;
  }
  function stop(){ K.a = K.d = K.w = K.s = false; }
  TD.tick = function(){
    TD.i++;
    if (TD.taps.length && TD.taps[0][0] <= TD.i) { tap(TD.taps.shift()[1]); }
    const T = BOFTUTORIAL.live;
    if (state !== GS.PLAY || !T || !T.L) { stop(); K.j = false; return; }
    const L = T.L, id = L.def.id, low = PLAY.y + PLAY.h - 70;
    if (T.i !== TD.lastLesson) { TD.lastLesson = T.i; TD.t0 = TD.i; TD.log.push([T.i, id, TD.i]); TD.taps.length = 0; }
    const age = TD.i - TD.t0;
    if (T.done > 0) { stop(); K.j = false; return; }
    if (L.def.info) { stop(); K.j = false; if (age % 90 === 80) tap('j'); return; }
    K.j = true;
    if (id === 'move') { const b = L.beacons.find(b => !b.hit); if (b) steer(b.x, b.y, 4); else stop(); K.j = false; return; }
    if (id === 'fire' || id === 'exam') {
      const live = enemies.filter(e => e._tut && !e.dead && e._dyingT == null);
      if (live.length) steer(live[0].x, low); else stop(); return;
    }
    if (id === 'crate' || id === 'special') {
      const p = powerups.find(p => p.kind === 'weapon' || /icon|box|special/.test(p.kind || '') && !/crate/.test(p.kind || ''));
      const c = powerups.find(p => /crate/.test(p.kind || ''));
      if (p) { steer(p.x, p.y, 4); K.j = false; }
      else if (c) steer(c.x, low);
      else stop();
      return;
    }
    if (id === 'roll') { stop(); if (age === 30) { tap('a'); TD.taps.push([TD.i + 5, 'a']); } return; }
    if (id === 'somer') { stop(); if (age === 30) { tap('w'); TD.taps.push([TD.i + 5, 'w']); } return; }
    if (id === 'missile') { const e = enemies.find(e => e._tut && !e.dead); if (e) steer(e.x, low); if (age === 40) tap('k'); return; }
    if (id === 'retina') {
      const e = enemies.find(e => e._tut && !e.dead); if (e) steer(e.x, low);
      if (age === 30) tap('c');
      if (retina.phase === 'locked' && !TD.fired) { TD.fired = TD.i; tap('k'); }
      if (age % 120 === 119) { TD.fired = 0; tap('c'); }
      return;
    }
    if (id === 'warn') {
      K.j = false; const C = L.c;
      if (C && C.t > 2.4 / 3 - 0.05) { const away = C.x < (camLeftX() + camRightX()) / 2 ? C.x + 120 : C.x - 120; steer(away, low); }
      else steer(player.x, low);
      return;
    }
    if (id === 'strike') {
      K.j = false; const q = L.cur;
      if (q && q.t > q.warn * q.trackFor) { const away = q.x < (camLeftX() + camRightX()) / 2 ? q.x + 110 : q.x - 110; steer(away, low); }
      else stop();
      return;
    }
    stop();
  };
  return true;
}"""

STEPN = r"""(n) => {
  if (!Number.isFinite(window.__now)) window.__now = performance.now();
  for (let k = 0; k < n; k++) {
    if (window.TD) TD.tick();
    window.__now += 1000 / 60;
    try { loop(window.__now); } catch (e) { window.__perr = String(e).slice(0, 160); }
  }
  const T = BOFTUTORIAL.live;
  const foreign = enemies.filter(e => !e._tut).length;
  return {state, stage: run.stage, mode: run.mode, lives: run.lives, tut: !!T, lesson: T && T.L ? T.L.def.id : null,
          li: T ? T.i : -1, hits: T ? T.hits : 0, done: T ? T.done : 0, foreign, ask: !!BOFTUTORIAL.ask,
          dead: !!player.dead, _h: (T && T.hitLog ? (window.__tutHits = T.hitLog.slice()) : 0) && 0, err1: !!drawScene._tutErr, err2: !!drawScene._tutErr2, pause: PLAY_PAUSE_ROWS[2]};
}"""


def shot(pg, name):
    d = pg.evaluate("() => document.getElementById('screen').toDataURL('image/png')")
    open(os.path.join(OUT, name + '.png'), 'wb').write(base64.b64decode(d.split(',', 1)[1]))


def run_until(pg, pred, limit_frames, chunk=30):
    n = 0; m = None
    while n < limit_frames:
        m = pg.evaluate(STEPN, chunk); n += chunk
        if m['state'] != 'play': pg.wait_for_timeout(60)
        elif n % 600 == 0: pg.wait_for_timeout(20)
        if pred(m): return m, n
    return m, n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pilot', default='cole')
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    from playwright.sync_api import sync_playwright
    port, stop = sh.serve(sh.GAME)
    res = []
    def ok(c, msg):
        res.append((bool(c), msg)); print(('ok   ' if c else 'FAIL ') + msg, flush=True)

    def page(p, errs):
        b = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
        pg = b.new_page(viewport={'width': 1000, 'height': 1100}, device_scale_factor=1)
        pg.on('pageerror', lambda e: errs.append('page: ' + str(e)[:200]))
        pg.on('console', lambda m: errs.append('console: ' + m.text[:200]) if m.type == 'error' else None)
        pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=120000)
        pg.wait_for_function("() => typeof setState==='function' && (window.__bofFrames|0) > 4", timeout=120000)
        pg.evaluate(sh.TRAP_RAF); pg.wait_for_timeout(60)
        return b, pg

    with sync_playwright() as p:
        # ---------------- ask + full flight ----------------
        errs = []
        b, pg = page(p, errs)
        pg.evaluate(SETUP, {'pilot': a.pilot, 'mode': 'arcade', 'clear': True})
        pg.evaluate("() => startRun(1)")
        m = pg.evaluate(STEPN, 20)
        ok(m['state'] == 'tutask', 'a Stage-1 start off pilot select asks first (state %s)' % m['state'])
        sel0 = pg.evaluate("() => BOFTUTORIAL.ask && BOFTUTORIAL.ask.sel")
        ok(sel0 == 0, 'YES is the default answer for a first-time pilot')
        pg.evaluate(STEPN, 30); shot(pg, '01_ask')
        pg.evaluate("() => Input.injectTap('arrowdown')"); pg.evaluate(STEPN, 2)
        ok(pg.evaluate("() => BOFTUTORIAL.ask.sel") == 1, 'DOWN moves to NO')
        pg.evaluate("() => Input.injectTap('arrowup')"); pg.evaluate(STEPN, 2)
        ok(pg.evaluate("() => BOFTUTORIAL.ask.sel") == 0, 'UP moves back to YES')
        pg.evaluate("() => Input.injectTap('j')"); m = pg.evaluate(STEPN, 4)
        ok(m['tut'] and m['mode'] == 'arcade', 'YES starts the training flight')
        ok(m['pause'] == 'SKIP TUTORIAL', 'the pause menu offers SKIP TUTORIAL during the flight')
        m, n = run_until(pg, lambda m: m['state'] == 'intro', 600)
        pg.evaluate(STEPN, 50); shot(pg, '02_card')
        pg.evaluate(DRIVER)
        m, n = run_until(pg, lambda m: m['state'] == 'play', 20000)
        ok(m['state'] == 'play' and m['tut'], 'the card and launch hand over to PLAY with the flight live')
        lessons = pg.evaluate("() => BOFTUTORIAL.lessons")
        seen = {}; maxforeign = 0; total = 0; t_start = time.time(); lives0 = m['lives']; shots_taken = set()
        while total < 60 * 60 * 8:
            m = pg.evaluate(STEPN, 30); total += 30
            if total % 600 == 0: pg.wait_for_timeout(15)
            maxforeign = max(maxforeign, m['foreign'])
            if m['lesson'] and m['lesson'] not in seen:
                for k, v in seen.items():          # a lesson that finished between samples (the info cards take 0.25 s)
                    if 'end' not in v: v['end'] = total; v['hits'] = m['hits'] - v['hits0']
                seen[m['lesson']] = {'start': total, 'hits0': m['hits']}
            if m['lesson'] and m['lesson'] not in shots_taken and m['lesson'] in seen and total - seen[m['lesson']]['start'] >= 120:
                shots_taken.add(m['lesson']); shot(pg, '1%02d_%s' % (lessons.index(m['lesson']), m['lesson']))
            if m['lesson'] in seen and m['done'] > 0 and 'end' not in seen[m['lesson']]:
                seen[m['lesson']]['end'] = total; seen[m['lesson']]['hits'] = m['hits'] - seen[m['lesson']]['hits0']
                if m['lesson'] in ('fire', 'exam', 'warn'): shot(pg, '2%02d_%s_done' % (lessons.index(m['lesson']), m['lesson']))
            if not m['tut']:
                for k, v in seen.items():
                    if 'end' not in v: v['end'] = total; v['hits'] = m['hits'] - v['hits0']
                break
        print(json.dumps(seen), flush=True)
        print('driver log', pg.evaluate("() => TD.log"), flush=True)
        print('hit log', json.dumps(pg.evaluate("() => (window.__tutHits||[])"))[:3000], flush=True)
        for lid in lessons:
            s = seen.get(lid, {})
            ok('end' in s, 'lesson %-8s completed by inputs alone (%.1f s, %d hits)' % (lid, (s.get('end', 0) - s.get('start', 0)) / 60.0, s.get('hits', 0)))
        ok(maxforeign == 0, 'nothing but the tutorial units ever stood on the field (max foreign %d)' % maxforeign)
        ok(m['lives'] == lives0 and not m['dead'], 'no life was lost in the flight')
        ok(not m['tut'] and m['mode'] == 'arcade', 'the flight hands back with the arcade mode restored')
        m2, _ = run_until(pg, lambda m: m['state'] in ('intro', 'launch', 'play'), 600)
        ok(m2['state'] in ('intro', 'launch', 'play') and m2['stage'] == 1 and not m2['tut'] and not m2['ask'],
           'Stage 1 then starts normally without asking again (state %s)' % m2['state'])
        ok(pg.evaluate("() => PLAY_PAUSE_ROWS[2]") == 'RESTART LEVEL', 'the pause row is restored')
        ok(pg.evaluate("() => !!BOFTUTORIAL.store().done"), 'finishing is remembered')
        pg.evaluate(SETUP, {'pilot': a.pilot, 'mode': 'arcade'}); pg.evaluate("() => startRun(1)"); pg.evaluate(STEPN, 3)
        ok(pg.evaluate("() => BOFTUTORIAL.ask && BOFTUTORIAL.ask.sel") == 1, 'a pilot who has flown it is still asked, with NO as the default')
        pg.evaluate(STEPN, 30); shot(pg, '03_ask_seen')
        ok(not m['err1'] and not m['err2'] and not errs, 'no page or console errors (%s)' % (errs[:3],))
        b.close()

        # ---------------- NO (arcade + campaign) ----------------
        for mode in ('arcade', 'campaign'):
            errs = []
            b, pg = page(p, errs)
            pg.evaluate(SETUP, {'pilot': a.pilot, 'mode': mode, 'clear': True})
            pg.evaluate("() => startRun(1)"); pg.evaluate(STEPN, 20)
            pg.evaluate("() => Input.injectTap('arrowdown')"); pg.evaluate(STEPN, 2)
            pg.evaluate("() => Input.injectTap('j')"); m = pg.evaluate(STEPN, 6)
            want = ('intro',) if mode == 'arcade' else ('campaignintro', 'stagesel', 'cutscene')
            ok(m['state'] in want and not m['tut'] and m['mode'] == mode,
               'NO in %s starts the game as before (state %s, mode %s)' % (mode, m['state'], m['mode']))
            ok(not errs, '%s NO: no page errors (%s)' % (mode, errs[:2]))
            b.close()

        # ---------------- campaign YES -> skip from pause ----------------
        errs = []
        b, pg = page(p, errs)
        pg.evaluate(SETUP, {'pilot': a.pilot, 'mode': 'campaign', 'clear': True})
        pg.evaluate("() => startRun(1)"); pg.evaluate(STEPN, 20)
        pg.evaluate("() => Input.injectTap('j')"); pg.evaluate(STEPN, 4)
        pg.evaluate(DRIVER)
        m, _ = run_until(pg, lambda m: m['state'] == 'play' and m['li'] >= 1, 20000)
        ok(m['state'] == 'play' and m['mode'] == 'arcade', 'a campaign pilot flies the training flight')
        pg.evaluate("() => { Input.keys.p = false; Input.injectTap('p'); }"); m = pg.evaluate(STEPN, 70)
        ok(m['state'] == 'paused', 'START pauses the flight')
        shot(pg, '04_pause')
        for _ in range(2):
            pg.evaluate("() => Input.injectTap('arrowdown')"); pg.evaluate(STEPN, 3)
        pg.evaluate(STEPN, 20); shot(pg, '04b_pause_skip')
        pg.evaluate("() => Input.injectTap('j')"); m = pg.evaluate(STEPN, 10)
        ok(not m['tut'] and m['mode'] == 'campaign' and m['state'] in ('campaignintro', 'stagesel', 'cutscene'),
           'SKIP TUTORIAL hands a campaign pilot to the campaign prologue (state %s, mode %s)' % (m['state'], m['mode']))
        ok(not errs, 'skip: no page errors (%s)' % (errs[:2],))
        b.close()

        # ---------------- co-op: the flight is solo, the second seat comes back ----------------
        errs = []
        b, pg = page(p, errs)
        pg.evaluate(SETUP, {'pilot': a.pilot, 'mode': 'arcade', 'clear': True})
        pg.evaluate("() => { coopOn = true; p2Index = (pilotIndex + 1) % PILOTS.length; setState(GS.COOPROSTER); startRun(1); }")
        m = pg.evaluate(STEPN, 20)
        ok(m['state'] == 'tutask', 'a co-op start off the roster asks too (state %s)' % m['state'])
        pg.evaluate("() => Input.injectTap('j')"); pg.evaluate(STEPN, 4)
        ok(pg.evaluate("() => coopOn") is False, 'the training flight is flown solo')
        pg.evaluate(DRIVER)
        m, _ = run_until(pg, lambda m: m['state'] == 'play' and m['li'] >= 1, 20000)
        pg.evaluate("() => { Input.keys.p = false; Input.injectTap('p'); }"); pg.evaluate(STEPN, 70)
        for _ in range(2):
            pg.evaluate("() => Input.injectTap('arrowdown')"); pg.evaluate(STEPN, 3)
        pg.evaluate(STEPN, 20); pg.evaluate("() => Input.injectTap('j')"); m = pg.evaluate(STEPN, 10)
        ok(pg.evaluate("() => coopOn && typeof coopActive==='function' && coopActive()") and not m['tut'],
           'after the flight the co-op run starts with both seats (state %s)' % m['state'])
        ok(not errs, 'co-op: no page errors (%s)' % (errs[:2],))
        b.close()

        # ---------------- bypass ----------------
        errs = []
        b, pg = page(p, errs)
        pg.evaluate(SETUP, {'pilot': a.pilot, 'mode': 'arcade', 'clear': True})
        pg.evaluate("() => { setState(GS.PASSWORD); startRun(3); }"); m = pg.evaluate(STEPN, 4)
        ok(not m['ask'] and m['stage'] == 3, 'a password start never asks (state %s)' % m['state'])
        pg.evaluate(SETUP, {'pilot': a.pilot, 'mode': 'arcade'})
        pg.evaluate("() => { setState(GS.TITLE); startRun(1); }"); m = pg.evaluate(STEPN, 4)
        ok(not m['ask'], 'a Stage-1 start from anywhere but the pilot screens never asks')
        b.close()
    stop()
    bad = [r for r in res if not r[0]]
    print('%d ok / %d fail' % (len(res) - len(bad), len(bad)))
    json.dump({'checks': [{'ok': r[0], 'msg': r[1]} for r in res]}, open(os.path.join(OUT, 'report.json'), 'w'), indent=1)
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
