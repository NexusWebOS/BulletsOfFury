#!/usr/bin/env python3
"""
probe_enemies.py — which enemies actually put pixels on the canvas, and which enter properly.

    python3 _BUILD_SOURCE/probe_enemies.py
    python3 _BUILD_SOURCE/probe_enemies.py --stages 1,5,6,7,8,9 --seconds 40

WHY THIS EXISTS
Two of Mike's reports, and both are invisible to the assertion suite:

  "why enemies are appearing on stage 1 out of thin air instead of flying in"
  "why enemies disappear on levels 5 and forward"

The suite can prove an enemy is in the array with the right hp and pattern. It cannot prove the
thing ever reached the screen. CLAUDE.md names this failure mode exactly: hand drawEnemy a unit
whose art key does not resolve and it "spawns, moves, shoots, collides, and draws NOTHING" — the
lookup misses, it falls through to the legacy rigs, and the player sees an empty level that still
kills them.

So this counts BLITS. drawImage is wrapped for the duration of each drawEnemy(e) call, and any
unit that draws zero images while alive and on screen is reported by type. That is the only
measure that answers "disappear".

It also records each unit's FIRST observed y. A unit whose first sighting is already inside the
playfield never flew in — it appeared. That is the stage-1 report, and it is measured rather than
eyeballed.

⚠ ART MUST LOAD FIRST. Stepping happens in batches with real waits between them so the lazy loads
land; a single synchronous burst never yields and would report every unit as invisible. That would
look like a catastrophic finding and be an artefact of the harness.
"""
import argparse, http.server, socketserver, threading, os, sys, functools, json

ROOT = os.path.dirname(os.path.abspath(__file__))
GAME = os.path.abspath(os.path.join(ROOT, '..'))


def serve(directory, port=0):
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=directory)
    handler.log_message = lambda *a, **k: None
    httpd = socketserver.TCPServer(("127.0.0.1", port), handler)
    port = httpd.server_address[1]
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return port, httpd.shutdown


INSTRUMENT = r"""
() => {
  const cv = document.querySelector('#screen-area canvas') || document.querySelector('canvas');
  const g = cv.getContext('2d');
  window.__seen = {};          // id -> {type, firstY, blits, frames, onscreen}
  window.__nid = 1;
  const origDrawEnemy = window.drawEnemy;
  const origDrawImage = g.drawImage;
  let counting = null;
  g.drawImage = function() { if (counting) counting.n++; return origDrawImage.apply(g, arguments); };
  window.drawEnemy = function(e) {
    if (!e.__pid) e.__pid = window.__nid++;
    let rec = window.__seen[e.__pid];
    if (!rec) {
      rec = window.__seen[e.__pid] = {type: e.type || e._amini || '?', firstY: Math.round(e.y),
                                      blits: 0, frames: 0, onscreen: 0};
    }
    const prev = counting; counting = {n: 0};
    try { return origDrawEnemy.apply(this, arguments); }
    finally {
      const n = counting.n; counting = prev;
      rec.blits += n; rec.frames++;
      if (e.y > 0 && e.y < VH && !e.dead) rec.onscreen++;
    }
  };
  return null;
}
"""

STEP = "(n) => { const t=performance.now(); for(let i=0;i<n;i++){ try{ loop(t+i*16.7); }catch(e){ return String(e&&e.message||e);} } return null; }"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--stages', default='1,2,3,4,5,6,7,8,9')
    ap.add_argument('--seconds', type=float, default=45, help='game-seconds of wave script per stage')
    args = ap.parse_args()
    stages = [int(s) for s in args.stages.split(',') if s.strip()]

    from playwright.sync_api import sync_playwright
    port, stop = serve(GAME)
    url = 'http://127.0.0.1:%d/index.html' % port
    errs, out = [], {}

    with sync_playwright() as p:
        b = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
        pg = b.new_page(viewport={'width': 1100, 'height': 1200}, device_scale_factor=1)
        pg.on('pageerror', lambda e: errs.append(str(e)[:160]))
        pg.goto(url, wait_until='load', timeout=60000)
        pg.wait_for_function("() => typeof ASSETS!=='undefined' && typeof drawEnemy==='function'", timeout=45000)
        pg.wait_for_function("() => (window.__bofFrames|0) > 4", timeout=45000)
        pg.evaluate(INSTRUMENT)

        for st in stages:
            pg.evaluate("""(st) => {
                ASSETS.ready = true; run.pilot='cole'; curStage = STAGES[st-1];
                beginStage(st); setState(GS.PLAY);
                player.reset(); player.invuln = 1e9;
                window.__seen = {}; window.__nid = 1;
                enemies.length = 0;
            }""", st)
            # ⚠ batches with real waits, so lazily-loaded art actually arrives — see the header
            frames = int(args.seconds * 60)
            per = 60
            for _ in range(max(1, frames // per)):
                err = pg.evaluate(STEP, per)
                if err:
                    errs.append('stage %d: %s' % (st, err)); break
                pg.wait_for_timeout(45)
            out[st] = pg.evaluate("() => window.__seen")
        b.close()
    stop()

    print('%-6s %-7s %-8s %-9s  %s' % ('stage', 'units', 'blind', 'popped-in', 'detail'))
    print('-' * 88)
    for st in stages:
        seen = out.get(st) or {}
        recs = list(seen.values())
        live = [r for r in recs if r['onscreen'] > 0]
        blind = [r for r in live if r['blits'] == 0]
        popped = [r for r in recs if r['firstY'] > 0]
        bt = {}
        for r in blind:
            bt[r['type']] = bt.get(r['type'], 0) + 1
        pt = {}
        for r in popped:
            pt[r['type']] = pt.get(r['type'], 0) + 1
        detail = ''
        if bt:
            detail += 'INVISIBLE: ' + ', '.join('%s x%d' % (k, v) for k, v in sorted(bt.items()))
        if pt:
            detail += ('  |  ' if detail else '') + 'POP-IN: ' + \
                      ', '.join('%s x%d' % (k, v) for k, v in sorted(pt.items()))
        print('%-6d %-7d %-8d %-9d  %s' % (st, len(recs), len(blind), len(popped), detail or 'clean'))

    if errs:
        print('\npage errors (%d):' % len(errs))
        for e in errs[:8]:
            print('   ', e)


if __name__ == '__main__':
    main()
