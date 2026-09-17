#!/usr/bin/env python3
"""
capture_clip_0916.py - RECORD REAL GAMEPLAY CLIPS FOR MARKETING.

    python _BUILD_SOURCE/capture_clip_0916.py --stage 1 --seconds 12 --out docs/marketing_0916/clips
    python _BUILD_SOURCE/capture_clip_0916.py --fight s1_boss_overlordx --seconds 20
    python _BUILD_SOURCE/capture_clip_0916.py --list-fights

WHY THIS AND NOT shoot.py
  shoot.py steps loop() by hand and screenshots each frame through the CDP bridge. That is exactly
  right for a proof -- it is deterministic and a frame is a regression test. It is the wrong tool
  for a 20-second clip: it is one round trip per frame, and shoot.py's own note records that a long
  warm combined with many captures faults the renderer ("Target crashed").

  The game already ships the right mechanism. `R` in debug mode runs captureStream + MediaRecorder
  over a composite of all THREE canvases (HUD strip, EQUIPPED box, play field) at 8 Mbit -- drop
  0910d. That runs entirely inside the page: no per-frame IPC, real dt, real motion blur-free 60fps.
  This drives that recorder headlessly and pulls the blob out at the end.

  ⚠ IT THEREFORE RUNS IN REAL TIME AND THE CAPTURE IS ONLY AS SMOOTH AS THE HEADLESS BROWSER.
  The tool MEASURES the frame rate it actually achieved (frames drawn / wall seconds) and prints
  it. Read that number. A clip captured at 34 fps is not a 60 fps clip with a smaller file -- it
  is a clip that visibly stutters, and nothing else in the pipeline can tell you.

  ⚠ AND THE PLAYER DOES NOT FIRE ON ITS OWN (CLAUDE.md, at shoot.py). Firing needs an input tap
  the harness does not simulate, so a clip left alone is the ship gliding through a battle without
  shooting -- which looks like a broken build, not a trailer. `pShoot()` is driven directly here,
  on the same cadence the weapon's own cooldown allows.
"""
import argparse, base64, os, subprocess, sys, time

ROOT = os.path.dirname(os.path.abspath(__file__))
GAME = os.path.abspath(os.path.join(ROOT, '..'))
sys.path.insert(0, ROOT)
from shoot import serve  # noqa: E402  -- the same quiet threaded server


# Drive the game into a scene using ITS OWN functions. No test hooks: a hook that exists only for
# the harness is a hook that can drift from real play.
SETUP = r"""
(cfg) => {
  const out = {ok:false};
  try {
    if (typeof ASSETS === 'undefined') { out.err = 'no ASSETS'; return out; }
    ASSETS.ready = true;
    if (cfg.pilot && typeof run !== 'undefined') run.pilot = cfg.pilot;
    if (typeof DIFF !== 'undefined' && cfg.diff && typeof setDifficulty === 'function') {
      try { setDifficulty(cfg.diff); } catch(_e){}
    }
    if (cfg.state === 'PLAY') {
      if (typeof STAGES !== 'undefined') curStage = STAGES[(cfg.stage||1)-1];
      run.stage = cfg.stage || 1;
      beginStage(cfg.stage || 1);
      setState(GS.PLAY);
      if (typeof player !== 'undefined' && player.reset) player.reset();
    } else if (GS[cfg.state] != null) {
      setState(GS[cfg.state]);
    } else { out.err = 'unknown state ' + cfg.state; return out; }
    out.state = (typeof state !== 'undefined') ? state : '?';
    out.ok = true;
  } catch(e) { out.err = String(e && e.message || e); }
  return out;
}
"""

# The autopilot. It is deliberately dumb and deliberately ALIVE: it holds the trigger, drifts the
# ship on a slow lissajous so the camera pans and the parallax reads, and never dies -- a marketing
# clip is a showcase, not a playtest, so invulnerability is honest here as long as nothing claims
# it was a real run.
PILOT_AI = r"""
(cfg) => {
  window.__bofAuto = {t:0, shots:0, frames:0, hits:0};

  // ⚠ KEEP THE PILOT ALIVE BY STUBBING playerHit, NEVER BY PINNING invuln.
  // CLAUDE.md records this exact mistake costing a whole recording: the damage blink is
  // Math.floor(player.invuln/4)%2, so a pinned invuln does not protect the ship, it STROBES it
  // four frames on and four frames off for the length of the clip. Every state check stays green
  // and the trailer has no aircraft in it. Measured here on the first capture: 556 shots fired,
  // score 0 -> 1590, and the ship absent from three of four sampled frames.
  if (typeof window.playerHit === 'function') {
    window.__bofRealHit = window.playerHit;
    window.playerHit = function(){ window.__bofAuto.hits++; return; };
  }
  if (typeof player !== 'undefined') player.invuln = 0;

  // ⚠ AND THE RECORDER PAINTS ITS OWN RED "REC 00:00" BADGE INTO THE FRAME.
  // debugRecOverlay is drawn from the game's own draw, so it is inside the captured composite,
  // not around it -- a marketing clip would ship with a debug badge burnt into the top right.
  if (typeof window.debugRecOverlay === 'function') {
    window.__bofRealOverlay = window.debugRecOverlay;
    window.debugRecOverlay = function(){};
  }

  // ⚠ WITHOUT THIS, EVERY PILOT SHOWCASE LOOKS IDENTICAL.
  // pShoot() alone fires the default machine gun at tier 1, which is the same picture for all
  // nine pilots. What separates them is the SPECIAL (startSpecial(): Cole's nukes, Juggernaut's
  // wrecking balls, Falva's anchored laser balls, Axel's aegis orbs) and the weapon TIER. The
  // first pilot reel came back as six clips of the same orange bullet stream.
  if (cfg.weapon != null && typeof run !== 'undefined') {
    run.weapon = cfg.weapon;
    if (run.wlevels) run.wlevels[cfg.weapon] = Math.max(run.wlevels[cfg.weapon]|0, cfg.wlevel||5);
  }
  if (cfg.wlevel != null && typeof run !== 'undefined') run.wlevel = cfg.wlevel;
  window.__bofSpecialAt = (cfg.special ? (cfg.specialAt != null ? cfg.specialAt : 2.0) : -1);

  window.__bofAutoTick = function(){
    const A = window.__bofAuto; if(!A) return;
    A.frames++;
    A.t += 1/60;
    try {
      // the special runs 15s; re-arm it if the clip outlives one
      if (window.__bofSpecialAt >= 0 && A.t >= window.__bofSpecialAt &&
          typeof startSpecial === 'function' &&
          (typeof special === 'undefined' || !special)) {
        startSpecial(); A.specials = (A.specials|0) + 1;
        window.__bofSpecialAt = A.t + 16.0;
      }
      if (typeof player !== 'undefined' && typeof VW !== 'undefined') {
        const cx = VW*0.5 + Math.sin(A.t*0.55)*VW*0.30;
        const cy = VH*0.62 + Math.sin(A.t*0.37+1.1)*VH*0.16;
        player.x += (cx - player.x)*0.06;
        player.y += (cy - player.y)*0.06;
        if (player.invuln > 0) player.invuln = 0;   // no blink, ever
      }
      if (typeof pShoot === 'function') {
        if (typeof player === 'undefined' || !player.fireCd || player.fireCd <= 0) {
          pShoot(); A.shots++;
        }
      }
    } catch(_e){}
  };
  return true;
}
"""

# Count the frames the player hull was actually BLITTED, so "the ship is in the clip" is measured
# off the draw rather than assumed from the state. Identify the blit by the KEY asked for:
# XART.get returns a fresh canvas with no .src and no stable identity (CLAUDE.md), and ctx carries
# its own drawImage so a prototype trap catches nothing.
SHIP_TRAP = r"""
() => {
  if (window.__bofShipTrap) return true;
  if (typeof XART === 'undefined' || typeof XART.get !== 'function') return false;
  window.__bofShip = {frames:0, keys:{}};
  const real = XART.get.bind(XART);
  XART.get = function(k){
    try {
      // ⚠ 'ship_' ALONE IS NOT THE PLAYER ON EVERY STAGE. Stage 5 transforms the aircraft into
      // the Furyship and stages 5/9 fly THAT, which resolves through 'fury_' and the space atlas
      // (`ngm_space_atlas`) instead. A trap keyed on 'ship_' reported 0 blits over 144 frames on
      // stage 9 -- a clip with the ship plainly in it -- which reads exactly like the invuln
      // strobe this trap exists to catch. Two families, one counter.
      if (typeof k === 'string' &&
          (k.indexOf('ship_') === 0 || k.indexOf('fury_') === 0 || k.indexOf('ngm_space') === 0)) {
        window.__bofShip.frames++;
        window.__bofShip.keys[k] = (window.__bofShip.keys[k]|0) + 1;
      }
    } catch(_e){}
    return real.apply(this, arguments);
  };
  window.__bofShipTrap = true;
  return true;
}
"""

# Hook the autopilot onto the END of loop() so it runs once per drawn frame and cannot desync from
# the game's clock. Wrapping the top-level binding is legal -- `loop` is a function declaration in
# global scope, so the name is reassignable (this is the route bossmode.js already uses).
HOOK = r"""
() => {
  if (window.__bofHooked) return true;
  const inner = window.loop;
  if (typeof inner !== 'function') return false;
  window.loop = function(ts){
    const r = inner.apply(this, arguments);
    try { if (window.__bofAutoTick) window.__bofAutoTick(); } catch(_e){}
    return r;
  };
  window.__bofHooked = true;
  return true;
}
"""

REC_START = "() => (typeof debugRecStart==='function') ? debugRecStart() : 'no recorder'"
REC_STOP = "() => (typeof debugRecStop==='function') ? debugRecStop() : 'no recorder'"

# Pull the finished blob out as base64. The recorder's onstop fires asynchronously after stop(),
# so the caller polls debugRec.last before asking for this.
REC_READY = "() => !!(typeof debugRec!=='undefined' && debugRec.last && debugRec.last.blob)"
REC_GRAB = r"""
async () => {
  const L = debugRec.last;
  if (!L || !L.blob) return null;
  const buf = await L.blob.arrayBuffer();
  const bytes = new Uint8Array(buf);
  let s = '';
  const CH = 0x8000;
  for (let i=0;i<bytes.length;i+=CH) s += String.fromCharCode.apply(null, bytes.subarray(i,i+CH));
  return {b64: btoa(s), name: L.name, dur: L.dur, size: L.size};
}
"""

STATS = r"""
() => ({
  frames: (window.__bofFrames|0),
  shots: (window.__bofAuto ? window.__bofAuto.shots : 0),
  enemies: (typeof enemies!=='undefined' ? enemies.length : -1),
  pbullets: (typeof pBullets!=='undefined' ? pBullets.length : -1),
  ebullets: (typeof eBullets!=='undefined' ? eBullets.length : -1),
  boss: (typeof boss!=='undefined' && boss ? (boss.name||boss.kind||'yes') : ''),
  sub: (typeof subBoss!=='undefined' && subBoss ? (subBoss.kind||'yes') : ''),
  state: (typeof state!=='undefined' ? state : '?'),
  score: (typeof run!=='undefined' ? (run.score|0) : -1),
  shipBlits: (window.__bofShip ? window.__bofShip.frames : -1),
  hits: (window.__bofAuto ? window.__bofAuto.hits : 0),
  specials: (window.__bofAuto ? (window.__bofAuto.specials|0) : 0),
  weapon: (typeof run!=='undefined' ? (run.weapon|0) : -1),
  wlevel: (typeof run!=='undefined' ? (run.wlevel|0) : -1),
})
"""

# Jump straight to an encounter using the debug menu's own table, so a clip of "the stage 6
# miniboss" is the encounter the game itself names, not a stage number and a stopwatch.
LIST_FIGHTS = r"""
() => {
  if (typeof debugFightList !== 'function') return [];
  try {
    return debugFightList().map(function(f, i){
      return {i:i, stage:f.stage, role:f.role, kind:f.kind, name:f.name||''};
    });
  } catch(e) { return [String(e)]; }
}
"""
JUMP_FIGHT = r"""
(idx) => {
  try {
    const L = debugFightList();
    const f = L[idx];
    if (!f) return 'no fight ' + idx;
    if (typeof debugStartFight === 'function') { debugStartFight(f); return 'ok:' + (f.name||f.kind); }
    return 'no debugStartFight';
  } catch(e) { return String(e && e.message || e); }
}
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--stage', type=int, default=1)
    ap.add_argument('--pilot', default='cole')
    ap.add_argument('--diff', default=None, help='difficulty name if the build exposes setDifficulty')
    ap.add_argument('--seconds', type=float, default=12)
    ap.add_argument('--settle', type=float, default=3.0, help='seconds of real play before REC starts')
    ap.add_argument('--fight', default=None, help='a debugFightList index or a substring of its name')
    ap.add_argument('--list-fights', action='store_true')
    ap.add_argument('--out', default='docs/marketing_0916/clips')
    ap.add_argument('--name', default=None)
    ap.add_argument('--weapon', type=int, default=None,
                    help='run.weapon slot: 0 mg 1 spread 2 missile 3 laser 4 flame 5 iceorb '
                         '6 lasermist 7 chaingun 8 lightning')
    ap.add_argument('--wlevel', type=int, default=None, help='weapon tier, 1-5 (Cole reaches 8)')
    ap.add_argument('--special', action='store_true', help="fire the pilot's special on a loop")
    ap.add_argument('--special-at', type=float, default=2.0)
    ap.add_argument('--no-autopilot', action='store_true')
    ap.add_argument('--headed', action='store_true')
    args = ap.parse_args()

    outdir = args.out if os.path.isabs(args.out) else os.path.join(GAME, args.out)
    os.makedirs(outdir, exist_ok=True)

    from playwright.sync_api import sync_playwright
    port, stop = serve(GAME)
    url = 'http://127.0.0.1:%d/index.html' % port
    errs = []

    with sync_playwright() as p:
        b = p.chromium.launch(
            headless=not args.headed,
            args=['--no-sandbox', '--mute-audio', '--autoplay-policy=no-user-gesture-required',
                  '--disable-features=IsolateOrigins,site-per-process'])
        pg = b.new_page(viewport={'width': 1100, 'height': 1250}, device_scale_factor=1)
        pg.on('pageerror', lambda e: errs.append('pageerror: ' + str(e)[:200]))
        pg.on('console', lambda m: errs.append('console.error: ' + m.text[:180])
              if m.type == 'error' else None)

        pg.goto(url, wait_until='load', timeout=60000)
        pg.wait_for_function("() => typeof ASSETS!=='undefined' && typeof setState==='function'",
                             timeout=45000)
        pg.wait_for_function("() => (window.__bofFrames|0) > 4", timeout=45000)

        if args.list_fights:
            for f in pg.evaluate(LIST_FIGHTS):
                print('%3d  stage %s  %-9s %-22s %s' % (f['i'], f['stage'], f['role'],
                                                        f['kind'], f['name']))
            b.close(); stop(); return

        res = pg.evaluate(SETUP, {'state': 'PLAY', 'stage': args.stage,
                                  'pilot': args.pilot, 'diff': args.diff})
        if not res.get('ok'):
            print('setup failed:', res.get('err'))
            b.close(); stop(); sys.exit(1)

        if args.fight is not None:
            fights = pg.evaluate(LIST_FIGHTS)
            idx = None
            if args.fight.isdigit():
                idx = int(args.fight)
            else:
                q = args.fight.lower()
                for f in fights:
                    hay = ('%s %s %s' % (f['kind'], f['name'], f['role'])).lower()
                    if q in hay:
                        idx = f['i']; break
            if idx is None:
                print('no fight matching %r; --list-fights to see them' % args.fight)
                b.close(); stop(); sys.exit(1)
            print('jumping to fight', idx, fights[idx].get('name') or fights[idx]['kind'])
            print('  ->', pg.evaluate(JUMP_FIGHT, idx))
            pg.wait_for_timeout(700)

        if not args.no_autopilot:
            pg.evaluate(PILOT_AI, {'weapon': args.weapon, 'wlevel': args.wlevel,
                                   'special': args.special, 'specialAt': args.special_at})
            if not pg.evaluate(HOOK):
                print('could not hook loop(); the ship will not fire')
        pg.evaluate(SHIP_TRAP)

        # let the scene settle and its lazy art decode before the recorder opens. XART.rdy is false
        # on its FIRST call -- that call starts the load -- so a clip that opens the instant the
        # stage begins opens on undecoded plates.
        pg.wait_for_timeout(int(args.settle * 1000))

        pre = pg.evaluate(STATS)
        r = pg.evaluate(REC_START)
        if r is not True:
            print('recorder refused to start:', r)
            print('  (headless chromium without MediaRecorder support cannot do this)')
            b.close(); stop(); sys.exit(1)

        t0 = time.time()
        pg.wait_for_timeout(int(args.seconds * 1000))
        wall = time.time() - t0
        pg.evaluate(REC_STOP)

        for _ in range(60):
            if pg.evaluate(REC_READY):
                break
            pg.wait_for_timeout(200)
        else:
            print('the recorder never produced a blob')
            b.close(); stop(); sys.exit(1)

        post = pg.evaluate(STATS)
        got = pg.evaluate(REC_GRAB)
        b.close()
    stop()

    drawn = post['frames'] - pre['frames']
    fps = drawn / wall if wall > 0 else 0

    stem = args.name or (args.fight and ('fight_' + str(args.fight)) or ('stage%d' % args.stage))
    stem = ''.join(c if (c.isalnum() or c in '-_') else '_' for c in stem)
    webm = os.path.join(outdir, stem + '.webm')
    open(webm, 'wb').write(base64.b64decode(got['b64']))

    print('--- capture ---------------------------------------------------')
    print('  clip          %s  (%.1f MB, %.1fs)' % (webm, got['size'] / 1e6, got['dur']))
    print('  MEASURED FPS  %.1f   (%d frames in %.1fs wall)' % (fps, drawn, wall))
    if fps < 45:
        print('  !! under 45fps -- this clip will visibly stutter. Shorten it, or drop the')
        print('     stage, or run --headed on a machine that can hold 60.')
    print('  shots fired   %d   specials %d   weapon %d tier %d'
          % (post['shots'] - pre['shots'], post['specials'], post['weapon'], post['wlevel']))
    if args.special and post['specials'] == 0:
        print('  !! THE SPECIAL NEVER FIRED -- every pilot clip will look like the same gun.')
    ship = post['shipBlits'] - max(0, pre['shipBlits'])
    ratio = (ship / drawn) if drawn else 0
    print('  ship blits    %d over %d frames  (%.2f per frame)' % (ship, drawn, ratio))
    if ratio < 0.5:
        print('  !! THE PLAYER SHIP IS BARELY IN THIS CLIP. That is the invuln blink, not a')
        print('     missing draw -- keep the pilot alive by stubbing playerHit, never by')
        print('     pinning invuln (CLAUDE.md).')
    print('  enemies       %d -> %d      ebullets %d -> %d'
          % (pre['enemies'], post['enemies'], pre['ebullets'], post['ebullets']))
    print('  boss/sub      %r / %r' % (post['boss'], post['sub']))
    print('  score         %d -> %d' % (pre['score'], post['score']))
    if post['shots'] - pre['shots'] == 0 and not args.no_autopilot:
        print('  !! THE SHIP NEVER FIRED. pShoot is a chain of early returns and a weapon that')
        print('     claims the trigger silences everyone -- check the pilot.')
    for e in errs[:8]:
        print('  err', e)

    mp4 = os.path.join(outdir, stem + '.mp4')
    ff = ['ffmpeg', '-y', '-loglevel', 'error', '-i', webm,
          '-c:v', 'libx264', '-preset', 'slow', '-crf', '16',
          '-pix_fmt', 'yuv420p', '-movflags', '+faststart', mp4]
    try:
        subprocess.run(ff, check=True)
        print('  mp4           %s' % mp4)
    except Exception as e:
        print('  ffmpeg failed:', e)


if __name__ == '__main__':
    main()
