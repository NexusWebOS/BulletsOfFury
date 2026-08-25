#!/usr/bin/env python3
"""
shoot.py — SCREENSHOT THE REAL GAME.

    python3 shoot.py --state PILOT --pilot cole --out /tmp/shots
    python3 shoot.py --state PLAY --stage 1 --seconds 20 --fps 4 --gif
    python3 shoot.py --script my_scenario.js --out /tmp/shots

⚠ WHY THIS EXISTS, AND IT IS THE MOST IMPORTANT TOOL IN THE REPO.

Every significant miss in this project traces to one gap: nobody could see the game except Mike.

  - the muzzle flash "wasn't there" — it was drawing, on the wrong frame of its reel
  - the stats screen looked right in a Python mock and wrong in the browser, because the mock
    was not the game's renderer
  - stage 1's jets never fired for weeks because the wave table still spawned retired types,
    while the assertion suite reported 2,352 passing
  - verify_atlas said "boss reached" on stage 1 while force-killing the miniboss to get there

The assertion harness proves STATE. A Python render proves what Python would draw. Neither proves
what the player sees. This runs the actual index.html in a real Chromium, lets the real game.js
draw to a real canvas, and captures the pixels.

If a change cannot be seen here, it has not been verified.

HOW IT WORKS
  1. serve the game over http (file:// blocks the module and asset loads)
  2. open it in headless chromium at the native 480x512
  3. wait for ASSETS.ready and the first drawn frame
  4. drive it into the state you asked for, using the game's own functions
  5. step the loop and screenshot the canvas on a fixed cadence
  6. optionally stitch the frames into a gif

WHAT IT DELIBERATELY DOES NOT DO
  It does not stub, mock or fake anything. There is no fake Image, no fake ctx, no substitute
  canvas. That is the entire point — the moment this file starts approximating the renderer it
  becomes another thing that can be green while the game is broken.
"""
import argparse, http.server, socketserver, threading, os, sys, time, json, functools

ROOT = os.path.dirname(os.path.abspath(__file__))
GAME = os.path.abspath(os.path.join(ROOT, '..'))


def serve(directory, port=0):
    """A quiet static server. Returns (port, shutdown)."""
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=directory)
    handler.log_message = lambda *a, **k: None
    httpd = socketserver.TCPServer(("127.0.0.1", port), handler)
    port = httpd.server_address[1]
    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()
    return port, httpd.shutdown


# The game exposes its state machine globally, so driving it needs no test hooks in game.js —
# which matters: a hook that only exists for the harness is a hook that can drift from real play.
SETUP = r"""
(cfg) => {
  const out = {ok:false, log:[]};
  try {
    if (typeof ASSETS === 'undefined') { out.err='no ASSETS'; return out; }
    ASSETS.ready = true;
    if (cfg.pilot && typeof run !== 'undefined') run.pilot = cfg.pilot;
    if (cfg.stage && typeof run !== 'undefined') run.stage = cfg.stage;
    if (cfg.state === 'PLAY') {
      if (typeof STAGES !== 'undefined') curStage = STAGES[(cfg.stage||1)-1];
      beginStage(cfg.stage||1);
      setState(GS.PLAY);
      if (typeof player !== 'undefined' && player.reset) player.reset();
      if (cfg.invuln && typeof player !== 'undefined') player.invuln = 1e9;
    } else if (GS[cfg.state] != null) {
      setState(GS[cfg.state]);
    } else {
      out.err = 'unknown state ' + cfg.state; return out;
    }
    out.state = (typeof state !== 'undefined') ? state : '?';
    out.ok = true;
  } catch (e) { out.err = String(e && e.message || e); }
  return out;
}
"""

# Stepping the loop by hand rather than letting rAF free-run makes the capture deterministic:
# the same command produces the same frames, which is what makes a screenshot a regression test
# rather than a snapshot of a moment.
STEP = r"""
(n) => {
  for (let i=0;i<n;i++) {
    try {
      if (typeof loop === 'function') loop(performance.now() + i*16.7);
      else if (typeof frame === 'function') frame(16.7);
      if (typeof window.__qaTick === 'function') window.__qaTick(i);
    } catch(e) { return String(e && e.message || e); }
  }
  return null;
}
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--state', default='TITLE', help='TITLE PILOT PASSWORD OPTIONS PLAY STAGECLEAR ...')
    ap.add_argument('--pilot', default='cole')
    ap.add_argument('--stage', type=int, default=1)
    ap.add_argument('--seconds', type=float, default=0, help='0 = a single shot')
    ap.add_argument('--fps', type=float, default=4, help='screenshots per second')
    ap.add_argument('--warm', type=int, default=90, help='frames to run before the first shot')
    ap.add_argument('--out', default='/tmp/shots')
    ap.add_argument('--gif', action='store_true')
    ap.add_argument('--script', default=None, help='a JS file evaluated after setup, for custom scenes')
    ap.add_argument('--invuln', action='store_true', default=True)
    args = ap.parse_args()

    os.makedirs(args.out, exist_ok=True)
    for f in os.listdir(args.out):
        if f.startswith('shot_'):
            os.remove(os.path.join(args.out, f))

    from playwright.sync_api import sync_playwright

    port, stop = serve(GAME)
    url = f'http://127.0.0.1:{port}/index.html'
    errs, shots = [], []

    with sync_playwright() as p:
        b = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
        # the game sizes its canvas to the window, and index.html renders at 2x — a viewport smaller
        # than the canvas makes Locator.screenshot hang waiting for it to be fully visible
        pg = b.new_page(viewport={'width': 1100, 'height': 1200}, device_scale_factor=1)
        pg.on('pageerror', lambda e: errs.append(str(e)[:200]))
        pg.on('console', lambda m: errs.append('console.' + m.type + ': ' + m.text[:160])
              if m.type == 'error' else None)

        pg.goto(url, wait_until='load', timeout=60000)

        # the game boots asynchronously; wait for it to actually be drawing rather than sleeping
        try:
            pg.wait_for_function("() => typeof ASSETS!=='undefined' && typeof setState==='function'",
                                 timeout=45000)
            pg.wait_for_function("() => (window.__bofFrames|0) > 4", timeout=45000)
        except Exception as e:
            print('the game never started drawing:', str(e)[:160])
            for x in errs[:6]:
                print('   ', x)
            b.close(); stop(); sys.exit(1)

        # Freeze the browser-owned rAF chain before deterministic stepping. Calling loop() by hand
        # while its final requestAnimationFrame(loop) is still live creates another chain on every
        # step; a nominal three-second capture was measured at 60,000+ frames and short muzzle FX
        # vanished between samples. The game has already proven that its natural loop booted above.
        # From here the harness is the sole clock, exactly as this file's contract promises.
        pg.evaluate("() => { window.requestAnimationFrame = () => 0; }")

        res = pg.evaluate(SETUP, {'state': args.state, 'pilot': args.pilot,
                                  'stage': args.stage, 'invuln': args.invuln})
        if not res.get('ok'):
            print('setup failed:', res.get('err'))
            b.close(); stop(); sys.exit(1)

        if args.script and os.path.exists(args.script):
            pg.evaluate(open(args.script).read())

        err = pg.evaluate(STEP, args.warm)
        if err:
            print('threw while warming:', err)

        # ⚠ TAKE THE PIXELS FROM THE CANVAS, NOT A SCREENSHOT OF THE ELEMENT.
        # index.html centres the canvas with a CSS transform, and Locator.screenshot hangs waiting
        # for a transformed element to settle. toDataURL reads the backing store directly, which is
        # both faster and exactly what the game drew — no compositing, no CSS scaling, no chrome.
        # ⚠ AND TAKE ALL THREE CANVASES, NOT JUST THE GAME (drop 0809m).
        # index.html has THREE: #hud (480x62), #equipcv (128x128) and #screen (480x512).
        # This grabbed only #screen, so the HUD strip and the equipment box were invisible to
        # shoot.py — which is the tool CLAUDE.md names as the one that proves pixels. A HUD bug
        # was therefore unseeable by the suite AND by the capture, which is how you end up
        # staring at a frame with no HUD in it and concluding the HUD is broken.
        # Composited in the same arrangement index.html lays them out: hud row on top, game
        # below. Falls back to the game canvas alone if the others are absent.
        GRAB = ("() => {"
                " const g = document.querySelector('#screen-area canvas') || document.querySelector('canvas');"
                " if(!g) return null;"
                " const h = document.querySelector('#hud'), e = document.querySelector('#equipcv');"
                " if(!h && !e) return g.toDataURL('image/png');"
                " const hw = h ? h.width : 0, hh = h ? h.height : 0;"
                " const ew = e ? e.width : 0, eh = e ? e.height : 0;"
                " const rowH = Math.max(hh, eh), W = Math.max(hw + ew, g.width), H = rowH + g.height;"
                # ONE SCRATCH CANVAS, REUSED, rather than a fresh one per capture. This is
                # hygiene, not a cure: a long warm (~3900 frames) COMBINED with many captures
                # still faults the renderer ("Target crashed"). Measured - warm 200 + 9 shots
                # passes, warm 3900 + 1 shot passes, warm 3900 + 9 shots crashes. So it is
                # accumulated memory across a long headless run, not any one frame.
                # Worth knowing because the fault surfaces as whatever you happened to be
                # testing at the time: it cost a whole pass being read as a boss-death crash.
                # If you need deep warm AND a sequence, take the shots in separate runs.
                " let c = window.__shotc;"
                " if(!c){ c = window.__shotc = document.createElement('canvas'); }"
                " if(c.width !== W || c.height !== H){ c.width = W; c.height = H; }"
                " const x = c.getContext('2d');"
                " x.fillStyle = '#000'; x.fillRect(0, 0, W, H);"
                " if(h) x.drawImage(h, 0, 0);"
                " if(e) x.drawImage(e, hw, 0);"
                " x.drawImage(g, 0, rowH);"
                " return c.toDataURL('image/png'); }")

        import base64
        n = 1 if args.seconds <= 0 else max(1, int(args.seconds * args.fps))
        step = max(1, int(60 / args.fps))
        max_ebullets = 0
        max_boss_bullets = 0
        seen_boss_families = set()
        seen_muzzle_slots = set()
        for i in range(n):
            probe = pg.evaluate("() => { const a=(typeof eBullets!=='undefined'?eBullets:[]),"
                                " bb=a.filter(b=>b&&b._boss);"
                                " return {e:a.length,b:bb.length,f:bb.map(b=>b._bfam||''),"
                                " m:(typeof subBoss!=='undefined'&&subBoss&&subBoss._smz?subBoss._smz.slots:[])}; }")
            max_ebullets = max(max_ebullets, probe['e'])
            max_boss_bullets = max(max_boss_bullets, probe['b'])
            seen_boss_families.update(probe['f'])
            seen_muzzle_slots.update(probe['m'])
            data = pg.evaluate(GRAB)
            if not data:
                print('no canvas found'); break
            path = os.path.join(args.out, 'shot_%04d.png' % i)
            open(path, 'wb').write(base64.b64decode(data.split(',', 1)[1]))
            shots.append(path)
            if i < n - 1:
                err = pg.evaluate(STEP, step)
                if err:
                    print('threw at frame %d: %s' % (i, err)); break

        info = pg.evaluate("() => ({state:(typeof state!=='undefined'?state:'?'),"
                           "frames:(window.__bofFrames|0),"
                           "enemies:(typeof enemies!=='undefined'?enemies.length:-1),"
                           "ebullets:(typeof eBullets!=='undefined'?eBullets.length:-1),"
                           "bossBullets:(typeof eBullets!=='undefined'?eBullets.filter(b=>b&&b._boss).length:-1),"
                           "bossFamilies:(typeof eBullets!=='undefined'?[...new Set(eBullets.filter(b=>b&&b._boss).map(b=>b._bfam||''))]:[]),"
                           "subMuzzle:(typeof subBoss!=='undefined'&&subBoss&&subBoss._smz?subBoss._smz.slots:[])})")
        b.close()
    stop()

    print('state=%s  frames=%d  enemies=%d  ebullets=%d  bossBullets=%d  bossFamilies=%s  subMuzzle=%s' %
          (info['state'], info['frames'], info['enemies'], info['ebullets'], info['bossBullets'],
           ','.join(info['bossFamilies']), ','.join(info['subMuzzle'])))
    print('capture peaks: ebullets=%d bossBullets=%d bossFamilies=%s muzzleSlots=%s' %
          (max_ebullets, max_boss_bullets, ','.join(sorted(seen_boss_families)),
           ','.join(sorted(seen_muzzle_slots))))
    print('captured %d shot(s) -> %s' % (len(shots), args.out))
    if errs:
        print('page errors (%d):' % len(errs))
        for e in errs[:8]:
            print('   ', e)

    if args.gif and len(shots) > 1:
        from PIL import Image
        ims = [Image.open(s).convert('RGB').convert('P', palette=Image.ADAPTIVE) for s in shots]
        g = os.path.join(args.out, 'capture.gif')
        ims[0].save(g, save_all=True, append_images=ims[1:],
                    duration=int(1000 / args.fps), loop=0, optimize=True)
        print('gif -> %s (%.1f MB)' % (g, os.path.getsize(g) / 1e6))


if __name__ == '__main__':
    main()
