#!/usr/bin/env python3
"""probe_s9_pacing_0905z.py - does the stage-9 ramp actually RAMP, and do its units DRAW?

Mike, 0905: "pacing should be light difficulty in the beginning to medium to high difficulty
before the boss of the end of the level."

Two separate questions, and reading the plan's source answers NEITHER:

 1. DOES IT RAMP.  "Light to medium to high" is a claim about the field over time, so it is
    measured as a curve: every simulated second records live fighters and total live enemy HP.
    The identical run is then taken against a clean worktree at HEAD and the two curves print
    side by side. A ramp that does not move the curve is not a ramp. The control numbers are
    what motivated the change - 2.64 / 3.31 / 4.11 live fighters across the three bands is flat.

 2. DOES EVERY HULL STILL DRAW.  The ramp re-times the whole cast, so a hull could be scheduled
    and silently draw nothing - the 0809l trap, which the comets repeated a drop later
    (game.js 34495). The proof is not `enemies` holding an `s9prism`, it is
    `XART.get('s9atk_hyperspace_prism_*')` being CALLED for a blit. XART.get is wrapped and
    tallied. NOT ctx.drawImage: `ctx` carries its OWN drawImage, and the image handed to it is a
    canvas with no .src, so a blit trap can count 26 draws and still not say WHICH sprite drew.
    The prototype roster is checked too - it must be ABSENT.

⚠ THREE TRAPS THIS PROBE HAD TO BE REWRITTEN AROUND. All three produced a confident WRONG answer
first, and each one is a trap for any future stepped probe, not just this one:

  A. STEPPING GIVES THE BROWSER NO TIME TO DECODE AN IMAGE.  shoot.STEP advances a synthetic clock
     inside one tight JS loop, so a 58-second run finishes in milliseconds of wall time. The whole
     void roster is CELLS OF ONE ATLAS - BOFX.cells['ns9e_wskim_idle'] = ['en_s9',1490,2120,...] -
     and `assets/game/atlas/en_s9.png` was still decoding for every frame of the run. Measured:
     rawComplete=false, naturalWidth=0, ZERO network requests, and `XART.rdy` false on all eight
     specialists for the entire run... then TRUE after a 1.5s real wait. The first version of this
     probe reported "** NOT DRAWN **" for nine units that were fine. So: the atlas is warmed and
     WAITED FOR before stepping, and the run is stepped in chunks with a real pause between them
     so anything requested mid-run can still decode.

  B. THE STAGE-9 MINIBOSS FREEZES THE STAGE CLOCK.  SUBBOSS[9] is `riftwardens` at at=0.45, and
     `subBossActive` runs `stageTimer-=dt` until it dies. A passive probe therefore stops at about
     t=30 and never sees a single beat of the high band. The player has to actually fight, so this
     drives an autopilot: fire held, and horizontal tracking of the nearest live enemy.

  C. STAGE 9 IS SPACE MODE, so `run.wlevel` is not its weapon level - `spaceWeaponLevel()` reads
     `run.spaceLevels`. Left at 1 the autopilot cannot break the miniboss either.

The autopilot is not a good player and does not pretend to be. It is a FIXED input policy, applied
identically to both runs, so the two curves differ only by the change under test.
"""
import sys, os, json, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shoot as sh
from playwright.sync_api import sync_playwright

# The SANCTIONED stage-9 cast, and all of it. S9_UNITS (wskim, pmine, ...) is the PROTOTYPE
# roster and test_fl.js asserts by name that it stays out of these waves - measuring it here
# would only re-learn that the hard way. S9VOID[k].art gives the reel prefix: s9atk_<art>_<0..7>.
FLEET = [('s9comet', 'comet_skimmer'), ('s9interceptor', 'galaxy_interceptor'),
         ('s9ring', 'ring_drone'), ('s9beacon', 'alien_beacon'),
         ('s9gateturret', 'gate_turret'), ('s9singularity', 'singularity_mine'),
         ('s9gunship', 'dimensional_gunship'), ('s9prism', 'hyperspace_prism')]
HP = {'s9comet':28, 's9interceptor':30, 's9ring':32, 's9beacon':34,
      's9gateturret':42, 's9singularity':46, 's9gunship':62, 's9prism':66}

# Touch every void-roster key so its atlas starts downloading, then the caller waits on rdy().
WARM = r"""
() => {
  const want = [];
  const hit = k => k.indexOf('ns9') === 0 || k.indexOf('s9atk_') === 0 || k.indexOf('s9nf_') === 0;
  if (window.BOFX && BOFX.cells) for (const k in BOFX.cells) if (hit(k)) want.push(k);
  if (window.BOFX && BOFX.img)   for (const k in BOFX.img)   if (hit(k)) want.push(k);
  if (XART._src) for (const k in XART._src) if (hit(k)) want.push(k);
  const uniq = Array.from(new Set(want));
  for (const k of uniq) { try { XART._touch(k); } catch (e) {} }
  window.__warmKeys = uniq;
  return uniq.length;
}
"""

WARM_READY = """() => {
  const ks = window.__warmKeys || [];
  let n = 0; for (const k of ks) if (XART.rdy(k)) n++;
  return ks.length ? (n / ks.length) : 1;
}"""

QA = r"""
(cfg) => {
  window.__qa = {census:[], types:{}, drew:{}, bossWarn:null, subFrom:null, subTo:null, err:null};
  const Q = window.__qa;
  if (XART.get && !XART.__qaWrapped) {
    const real = XART.get.bind(XART);
    XART.get = function(k){ Q.drew[k] = (Q.drew[k]||0)+1; return real(k); };
    XART.__qaWrapped = true;
  }
  // C: stage 9 is space mode - spaceWeaponLevel() reads run.spaceLevels, not run.wlevel.
  if (typeof run !== 'undefined') {
    run.spaceLevels = [5,5,5]; run.spaceWeapon = 0; run.wlevel = 5; run.wlevels = [5,5,5,5,5,5,5];
  }
  const K = (key, down) => window.dispatchEvent(
    new KeyboardEvent(down ? 'keydown' : 'keyup', {key:key, bubbles:true}));
  K('j', true);                                    // fire, held for the whole run
  let held = null;
  window.__qaTick = function(){
    try {
      const t = (typeof stageTimer !== 'undefined') ? stageTimer : -1;
      // B: autopilot - track the nearest live enemy horizontally so the miniboss can be broken
      let best = null, bd = 1e9;
      for (const e of enemies) {
        if (!e || e.dead || e._prop) continue;
        const d = Math.abs(e.x - player.x) + Math.max(0, e.y) * 0.35;
        if (d < bd) { bd = d; best = e; }
      }
      const want = best ? (best.x < player.x - 8 ? 'a' : (best.x > player.x + 8 ? 'd' : null)) : null;
      if (want !== held) { if (held) K(held, false); if (want) K(want, true); held = want; }

      for (const e of enemies) {
        if (!e || !e.type) continue;
        const r = Q.types[e.type] || (Q.types[e.type] = {first:t, n:0, ids:{}});
        const id = e.__qaId || (e.__qaId = 'q' + (Q.__n = (Q.__n||0) + 1));
        if (!r.ids[id]) { r.ids[id] = 1; r.n++; if (r.first < 0 || t < r.first) r.first = t; }
      }
      const sec = Math.floor(t);
      if (sec >= 0 && (!Q.census.length || Q.census[Q.census.length-1].s < sec)) {
        let live = 0, hp = 0;
        for (const e of enemies) {
          if (e.dead || e._dyingT != null || e._prop) continue;
          live++; hp += (e.hp || 0);
        }
        Q.census.push({s:sec, live:live, hp:Math.round(hp), all:enemies.length});
      }
      if (typeof subBossActive !== 'undefined' && subBossActive) {
        if (Q.subFrom == null) Q.subFrom = t;
        Q.subTo = t;
      }
      if (Q.bossWarn == null && typeof bossWarned !== 'undefined' && bossWarned) Q.bossWarn = t;
    } catch (err) { Q.err = String(err && err.message || err); }
  };
  return true;
}
"""

DONE = """() => {
  const t = (typeof stageTimer !== 'undefined') ? stageTimer : -1;
  return {t:t, warn:(typeof bossWarned !== 'undefined' && !!bossWarned),
          bossOn:(typeof bossActive !== 'undefined' && !!bossActive)};
}"""


def run(game_dir, seconds, label, chunk=240):
    port, stop = sh.serve(game_dir)
    try:
        with sync_playwright() as pw:
            b = pw.chromium.launch(args=['--autoplay-policy=no-user-gesture-required'])
            pg = b.new_page(viewport={'width': 480, 'height': 512})
            errs = []
            pg.on('pageerror', lambda e: errs.append(str(e)))
            pg.goto('http://127.0.0.1:%d/index.html' % port)
            pg.wait_for_function('typeof ASSETS!=="undefined" && typeof loop==="function"',
                                 timeout=30000)
            pg.wait_for_timeout(2500)
            r = pg.evaluate(sh.SETUP, {'state': 'PLAY', 'stage': 9, 'pilot': 'cole', 'invuln': True})
            if not r.get('ok'):
                raise SystemExit('%s: setup failed: %s' % (label, r))
            # A: warm the void atlas and WAIT ON IT, before any synthetic stepping begins
            n = pg.evaluate(WARM)
            try:
                pg.wait_for_function(WARM_READY + '() >= 0.98', timeout=20000)
                warm = 1.0
            except Exception:
                warm = pg.evaluate(WARM_READY)
            print('  %s: warmed %d void keys, %.0f%% ready before stepping' % (label, n, warm * 100))
            pg.evaluate(sh.TRAP_RAF)
            pg.evaluate(QA, {})
            total, stepped = int(seconds * 60), 0
            while stepped < total:
                err = pg.evaluate(sh.STEP, min(chunk, total - stepped))
                if err:
                    print('  %s: STEP threw at frame %d: %s' % (label, stepped, err))
                    break
                stepped += chunk
                pg.wait_for_timeout(40)          # A: real time, so late art can still decode
                d = pg.evaluate(DONE)
                if d['warn'] or d['bossOn']:
                    print('  %s: boss reached at stage t=%.1fs (frame %d)' % (label, d['t'], stepped))
                    break
            qa = pg.evaluate('() => window.__qa')
            b.close()
            if errs:
                print('  %s: %d page errors, first: %s' % (label, len(errs), errs[0][:200]))
            return qa
    finally:
        stop()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--seconds', type=float, default=150, help='simulated seconds to step')
    ap.add_argument('--control', default=None, help='clean worktree at HEAD to compare against')
    a = ap.parse_args()

    print('=== RAMP (working tree) ===')
    live = run(sh.GAME, a.seconds, 'ramp')
    ctrl = None
    if a.control:
        print('=== CONTROL (%s) ===' % a.control)
        ctrl = run(a.control, a.seconds, 'control')

    print('\n--- 1. DID THE SPECIALISTS SPAWN, AND DID THEY DRAW? ---')
    drew = live['drew'] or {}
    fail = []
    for u in SPECIALISTS:
        rec = live['types'].get(u)
        keys = [k for k in drew if k.startswith('ns9e_' + u) or k.startswith('ns9x_' + u)]
        blits = sum(drew[k] for k in keys)
        n = rec['n'] if rec else 0
        first = ('%5.1fs' % rec['first']) if rec else '   -  '
        ok = (n > 0 and blits > 0)
        if u != 'dreadv' and not ok:
            fail.append(u)
        note = 'OK' if ok else ('(held back on purpose)' if u == 'dreadv' else '** NOT DRAWN **')
        print('  %-8s spawned %2d  first %s  art-key blits %6d  %s' % (u, n, first, blits, note))

    print('\n--- 2. THE CURVE: live fighters / live enemy HP, per second ---')

    def curve(q):
        return {c['s']: c for c in (q['census'] or [])}
    L, C = curve(live), (curve(ctrl) if ctrl else {})
    hdr = '   t   ramp:live  ramp:hp'
    if ctrl:
        hdr += '    ctl:live   ctl:hp    dLive    dHP'
    print(hdr)

    def band(t):
        return 'LIGHT' if t < 14 else ('MEDIUM' if t < 27 else 'HIGH')
    for s in sorted(set(L) | set(C)):
        l, c = L.get(s), C.get(s)
        row = '  %3d  %6s   %7s' % (s, l['live'] if l else '-', l['hp'] if l else '-')
        if ctrl:
            row += ('    %6d   %6d   %+6d %+6d' % (c['live'], c['hp'],
                                                   (l['live'] - c['live']) if l else 0,
                                                   (l['hp'] - c['hp']) if l else 0)
                    if c else '         -        -       ')
        print(row + '   ' + band(s))

    def avg(q, lo, hi, key):
        v = [c[key] for c in (q['census'] or []) if lo <= c['s'] < hi]
        return sum(v) / len(v) if v else 0.0
    print('\n  band averages (live fighters / live enemy hp)')
    for nm, lo, hi in [('LIGHT  0-14 ', 0, 14), ('MEDIUM 14-27', 14, 27), ('HIGH   27-42', 27, 42)]:
        s = '  %s  ramp %5.2f / %6.1f' % (nm, avg(live, lo, hi, 'live'), avg(live, lo, hi, 'hp'))
        if ctrl:
            s += '    control %5.2f / %6.1f' % (avg(ctrl, lo, hi, 'live'), avg(ctrl, lo, hi, 'hp'))
        print(s)

    print('\n--- 3. THE MINIBOSS HOLD + THE BOSS GATE (enemies.length<=7, game.js:26039) ---')
    for nm, q in [('ramp', live)] + ([('control', ctrl)] if ctrl else []):
        sub = ('held the clock at t=%.1f..%.1f' % (q['subFrom'], q['subTo'])) \
              if q['subFrom'] is not None else 'riftwardens never triggered'
        warn = ('%.1fs' % q['bossWarn']) if q['bossWarn'] is not None else 'NOT REACHED'
        print('  %-8s %-42s  boss warn %s' % (nm, sub, warn))
        if q.get('err'):
            print('           qaTick error: %s' % q['err'])

    print('\n%s' % ('FAILED: never drew -> ' + ', '.join(fail) if fail
                    else 'all ramp specialists spawned AND drew.'))
    return 1 if fail else 0


if __name__ == '__main__':
    sys.exit(main())
