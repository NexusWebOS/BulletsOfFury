#!/usr/bin/env python3
"""
probe_seam.py — MEASURE THE STAGE-INTRO SEAM, in the real browser.

    python3 _BUILD_SOURCE/probe_seam.py --stage 1
    python3 _BUILD_SOURCE/probe_seam.py --stage 2 --frames 1600

WHY THIS EXISTS
Mike: "kill the jerk after 3-2-1 that knocks the ship back and clips it in and out."

There are TWO intro systems and they fail differently, which is why the symptom moved around:

  stage 1      GS.OPENING — the runway cinematic. The ship and camera are continuous across the
               handoff (measured), but the opening paints a GENERATED coast while PLAY paints the
               stage master, so the whole picture swaps. That is "the fake transition".
  stages 2-9   GS.INTRO -> GS.LAUNCH. drawLaunch's _drawLevelRegion calls the real drawBG, so
               mapScroll IS continuous — but the SHIP is drawn by two different rules:

                   screen x    launch draws at VW/2; PLAY draws at player.x - camX
                   screen y    launch holds VH*ANCHORY (0.60); player.reset() puts play at VH*0.78
                   draw height launch passes a CANVAS height to drawShipSprite; PLAY scales to a
                               CONTENT height and divides by the pilot's content fraction

Rather than diff pixels and argue about what moved, this records the actual numbers on both sides
of the seam and prints the deltas. A fix is correct when all three deltas are 0.

It drives the real game the way shoot.py does — real Chromium, real index.html, the game's own
state machine, no stubs. drawShipSprite is wrapped to capture what the launch really asked for
rather than recomputing it from the source and hoping the source is what runs.

⚠ THE WHOLE RUN HAPPENS IN ONE evaluate. The first version stepped one frame per evaluate and read
the sample back each time: ~1.6s of wall clock per frame, and since the game takes dt from
performance.now(), every frame saw a dt of 1.6 SECONDS. A 14.6s cinematic "completed" in nine
frames. Batching keeps dt at the 16.7ms the game is written for.
"""
import argparse, http.server, socketserver, threading, os, sys, json, functools

ROOT = os.path.dirname(os.path.abspath(__file__))
GAME = os.path.abspath(os.path.join(ROOT, '..'))


def serve(directory, port=0):
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=directory)
    handler.log_message = lambda *a, **k: None
    httpd = socketserver.TCPServer(("127.0.0.1", port), handler)
    port = httpd.server_address[1]
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return port, httpd.shutdown


# Wrap drawShipSprite so we record the pose the LAUNCH actually drew, and sample the PLAY pose from
# the player object plus the camera. Both go into one trace keyed by state, so the seam is just the
# frame where state flips.
INSTRUMENT = r"""
() => {
  window.__ship = null;
  const orig = window.drawShipSprite;
  if (typeof orig !== 'function') return 'drawShipSprite is not global';
  window.drawShipSprite = function(x, y, h, suf) {
    window.__ship = {x: x, y: y, h: h};
    return orig.apply(this, arguments);
  };
  /* The opening draws its own ship rather than going through drawShipSprite, so capture that too.
     ⚠ RECORD WHAT WAS DRAWN, DO NOT RECOMPUTE IT. The first version of this hook set
        x: player.x - camX
     which is the very thing under test — so it reported the ship as continuous across the handoff
     while the real draw was putting it at screen x 400 with no camera at all, 160px right of where
     PLAY starts. A probe that assumes the fix cannot find the bug. It now wraps drawImage for the
     duration of the call and reads the transform the game actually had. */
  const oship = window.openingDrawShip;
  if (typeof oship === 'function') {
    window.openingDrawShip = function() {
      const c = document.querySelector('#screen-area canvas') || document.querySelector('canvas');
      const g = c && c.getContext('2d');
      if (!g) return oship.apply(this, arguments);
      const origDraw = g.drawImage;
      let seen = null;
      /* ⚠ getTransform() carries the canvas's BASE DEVICE SCALE as well as the game's translates —
         index.html backs a 480x512 logical canvas with a 960x1024 store. Reported raw, the opening
         side comes out in device pixels and the PLAY side in logical ones, and a perfectly
         continuous handoff reads as an exact 2x "jerk". Normalise by the scale so both sides are
         in the same units, which is the entire point of putting them side by side. */
      const S = (c.width || VW) / VW;
      g.drawImage = function(im, dx, dy, dw, dh) {
        if (arguments.length === 5 && seen === null) {
          const m = g.getTransform();           // includes every translate the draw applied
          seen = {x: (m.a*(dx + dw/2) + m.e)/S, y: (m.d*(dy + dh/2) + m.f)/S, h: dh*m.d/S};
        }
        return origDraw.apply(g, arguments);
      };
      try { return oship.apply(this, arguments); }
      finally { g.drawImage = origDraw; if (seen) window.__ship = seen; }
    };
  }
  // content-height fraction per pilot, the same table _drawPlayerCore uses
  window.__cf = function(){
    const T = {axel:0.8081, cole:0.8081, decker:0.7935, falva:0.7929, freezer:0.8081,
               juggernaut:0.7964, lizzie:0.8429, maverick:0.8022, yuri:0.7454};
    const p = (typeof run!=='undefined' && run.pilot) || 'cole';
    return T[p] != null ? T[p] : 0.80;
  };
  window.__sample = () => {
    const s = {
      state: (typeof state!=='undefined') ? String(state) : '?',
      phase: (typeof drawLaunch!=='undefined' && drawLaunch._phase) || null,
      openT: (typeof opening!=='undefined' && opening) ? opening.t : null,
      dist:  (typeof drawLaunch!=='undefined' && drawLaunch._dist) || 0,
      map:   (typeof mapScroll!=='undefined') ? mapScroll : null,
      camX:  (typeof camX!=='undefined') ? camX : null,
      px:    (typeof player!=='undefined') ? player.x : null,
      py:    (typeof player!=='undefined') ? player.y : null,
      ph:    (typeof player!=='undefined') ? player.h : null
    };
    s.ship = window.__ship ? {x: window.__ship.x, y: window.__ship.y, h: window.__ship.h} : null;
    window.__ship = null;
    // what PLAY would draw: screen x is world x minus the camera; canvas height is content/cf
    if (s.px != null) {
      s.playX = s.px - (s.camX || 0);
      s.playY = s.py;
      s.playH = ((s.ph || 34) * 2.05) / window.__cf();
    }
    return s;
  };
  return null;
}
"""

# Step the whole run in ONE evaluate, sampling after each frame, and stop once PLAY has been up for
# a while. Timestamps advance by a fixed 16.7ms so dt is the real frame time.
RUN = r"""
(n) => {
  const out = [];
  const t0 = performance.now();
  let playFrames = 0;
  for (let i=0;i<n;i++) {
    try { loop(t0 + i*16.7); }
    catch(e) { return {err: String(e && e.message || e), frame: i, trace: out}; }
    const s = window.__sample(); s.f = i; out.push(s);
    if (s.state === 'play') { playFrames++; if (playFrames > 40) break; }
  }
  return {err: null, trace: out};
}
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--stage', type=int, default=1)
    ap.add_argument('--pilot', default='cole')
    ap.add_argument('--frames', type=int, default=2000, help='max frames to run after beginStage')
    ap.add_argument('--json', default=None, help='write the full trace here')
    args = ap.parse_args()

    from playwright.sync_api import sync_playwright

    port, stop = serve(GAME)
    url = 'http://127.0.0.1:%d/index.html' % port
    errs = []

    with sync_playwright() as p:
        b = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
        pg = b.new_page(viewport={'width': 1100, 'height': 1200}, device_scale_factor=1)
        pg.on('pageerror', lambda e: errs.append(str(e)[:200]))
        pg.goto(url, wait_until='load', timeout=60000)
        try:
            pg.wait_for_function("() => typeof ASSETS!=='undefined' && typeof setState==='function'",
                                 timeout=45000)
            pg.wait_for_function("() => (window.__bofFrames|0) > 4", timeout=45000)
        except Exception as e:
            print('the game never started drawing:', str(e)[:160]); b.close(); stop(); sys.exit(1)

        bad = pg.evaluate(INSTRUMENT)
        if bad:
            print('instrument failed:', bad); b.close(); stop(); sys.exit(1)

        # Drive the real entry path: ASSETS.ready, pilot, then beginStage and let the state machine
        # walk INTRO -> LAUNCH -> PLAY (or OPENING -> PLAY) on its own. Nothing is forced.
        res = pg.evaluate("""(cfg) => {
            try {
              ASSETS.ready = true;
              run.pilot = cfg.pilot;
              curStage = STAGES[cfg.stage-1];
              beginStage(cfg.stage);
              return {ok:true, state:String(state)};
            } catch(e) { return {ok:false, err:String(e && e.message || e)}; }
        }""", {'stage': args.stage, 'pilot': args.pilot})
        if not res.get('ok'):
            print('beginStage failed:', res.get('err')); b.close(); stop(); sys.exit(1)

        out = pg.evaluate(RUN, args.frames)
        b.close()
    stop()

    trace = out.get('trace') or []
    if out.get('err'):
        print('threw at frame %s: %s' % (out.get('frame'), out['err']))
    if not trace:
        print('no trace'); sys.exit(1)

    states = []
    for s in trace:
        if not states or states[-1][0] != s['state']:
            states.append((s['state'], s['f']))
    print('stage %d  entry=%s  frames=%d' % (args.stage, res.get('state'), len(trace)))
    print('states:', ' -> '.join('%s@%d' % (n, f) for n, f in states))

    seam = None
    for i in range(1, len(trace)):
        if trace[i]['state'] == 'play' and trace[i-1]['state'] != 'play':
            seam = i
            break
    if seam is None:
        print('never reached PLAY in %d frames — the intro is longer than the sample window'
              % len(trace))
        if args.json:
            json.dump(trace, open(args.json, 'w'), indent=1)
        sys.exit(2)

    before, after = trace[seam-1], trace[seam]
    print('\nseam at frame %d = %.2fs  (%s -> %s)'
          % (seam, seam*16.7/1000.0, before['state'], after['state']))

    lastship = None
    for s in reversed(trace[:seam]):
        if s['ship']:
            lastship = s
            break

    print('\n--- SHIP ACROSS THE SEAM ---')
    if lastship and after.get('playX') is not None:
        L, P = lastship['ship'], after
        print('  intro drew    x=%7.2f  y=%7.2f  h=%6.2f   (frame %d, phase %s)'
              % (L['x'], L['y'], L['h'], lastship['f'], lastship['phase']))
        print('  play draws    x=%7.2f  y=%7.2f  h=%6.2f'
              % (P['playX'], P['playY'], P['playH']))
        dx, dy, dh = P['playX'] - L['x'], P['playY'] - L['y'], P['playH'] - L['h']
        ok = max(abs(dx), abs(dy), abs(dh)) < 0.5
        print('  DELTA         x=%+7.2f  y=%+7.2f  h=%+6.2f   %s'
              % (dx, dy, dh, 'OK' if ok else '<-- THE JERK'))
    else:
        print('  the intro never drew a ship through either hook')

    print('\n--- TERRAIN / CAMERA ACROSS THE SEAM ---')
    print('  mapScroll  %8.2f -> %8.2f   delta %+8.2f'
          % (before['map'] or 0, after['map'] or 0, (after['map'] or 0) - (before['map'] or 0)))
    print('  camX       %8.2f -> %8.2f   delta %+8.2f'
          % (before['camX'] or 0, after['camX'] or 0, (after['camX'] or 0) - (before['camX'] or 0)))

    play = [s for s in trace[seam:] if s['camX'] is not None]
    if play and abs(play[-1]['camX'] - play[0]['camX']) > 0.5:
        print('  camX over the first %d play frames: %.2f -> %.2f'
              % (len(play), play[0]['camX'], play[-1]['camX']))
        print('    <-- THE CAMERA SLIDES after control is handed over')

    if errs:
        print('\npage errors (%d):' % len(errs))
        for e in errs[:6]:
            print('   ', e)

    if args.json:
        json.dump(trace, open(args.json, 'w'), indent=1)
        print('\ntrace -> %s' % args.json)


if __name__ == '__main__':
    main()
