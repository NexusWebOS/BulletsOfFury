#!/usr/bin/env python3
"""
probe_arrival.py — is the entry cinematic's last frame the level's FIRST frame? All nine stages.

    python3 _BUILD_SOURCE/probe_arrival.py                # every stage that has one
    python3 _BUILD_SOURCE/probe_arrival.py --stage 6
    python3 _BUILD_SOURCE/probe_arrival.py --stage 2,3,7

WHY THIS EXISTS
Mike: "connect the last transition tile to the level's first frame ... so we truly fly into level
1. No more fake transitions." Then, 0810i, for all of them: "make connecting sections ... that
directly connects to beginning of our levels so it's seamless."

probe_seam.py already showed the NUMBERS were clean across the stage-1 handoff — mapScroll 0 -> 0,
camX 160 -> 160, the ship untouched. Nothing jumped, and the transition was still fake, because the
opening generated a coastline from sine terms while PLAY painted the jungle master: same numbers,
different picture. Numbers cannot see that. Only pixels can.

⚠⚠ AND THIS PROBE WAS NOT SEEING THEM EITHER, FOR TWO DROPS (fixed 0810j). READ THIS BEFORE
TRUSTING ANY "0 differing pixels" NUMBER YOU FIND QUOTED IN THE DOCS.

The old loop was:

    if (st === 'opening') { lastOpen = grab(); step(); }
    else if (st === 'play') { firstPlay = grab(); break; }

grab() reads the canvas — it does not draw. The state flips to 'play' at the END of drawOpening,
i.e. inside a step() that has ALREADY drawn a cinematic frame. So on the next iteration the branch
sees 'play' and grabs a canvas that still holds that cinematic frame. `firstPlay` was never a play
frame. The probe compared two consecutive CINEMATIC frames — both static by then, because the
arrival has landed and dy is 0 — so it returned 0 differing pixels of 393,600 whatever the handoff
actually looked like. It could not have failed. That number is quoted in CLAUDE.md and in
docs/HANDOFF_CONNECTORS.md as the bar for this work, and it was measuring nothing.

This is the same failure as the one already recorded against probe_seam.py, one step further out:
that probe RECOMPUTED the value under test; this one READ THE WRONG FRAME. A probe must draw the
frame it intends to measure, then read it. The loop below steps first and grabs second, and it
labels which state each captured frame belongs to so the mistake cannot hide again.

⚠ ART FIRST, THEN STEP. The stepping happens in one evaluate so dt stays a true 16.7ms, and a
single synchronous burst never yields, so nothing can load during it (the --warm trap). The master
AND the stage's connector surface are polled to ready BEFORE the burst starts. Get that order
wrong and this measures a blank screen against a blank screen and calls it a perfect match.
"""
import http.server, socketserver, threading, os, sys, functools, argparse

ROOT = os.path.dirname(os.path.abspath(__file__))
GAME = os.path.abspath(os.path.join(ROOT, '..'))

# stage 9 is authored and has a _levelCfg entry but is NOT in STAGES[] (it is the bonus stage,
# entered from level 5 and not yet wired), so beginStage(9) has no curStage. Off by default.
DEFAULT_STAGES = [1, 2, 3, 4, 5, 6, 7, 8]


def serve(directory, port=0):
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=directory)
    handler.log_message = lambda *a, **k: None
    httpd = socketserver.TCPServer(("127.0.0.1", port), handler)
    port = httpd.server_address[1]
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return port, httpd.shutdown


SETUP = """
(st) => {
  ASSETS.ready = true; run.pilot = 'cole';
  curStage = STAGES[st-1] || STAGES[0];
  beginStage(st);
  // stage 1 owns the runway cinematic (GS.OPENING); every other stage enters through the launch.
  // The stage CARD is skipped deliberately — it is 3.6s of black with a plate on it and has
  // nothing to do with the join being measured.
  if (st === 1) { if (String(state) !== 'opening') { openingStart(1); setState(GS.OPENING); } }
  else { setState(GS.LAUNCH); }
  return String(state);
}
"""

# touch everything the connector needs so the decode starts before the burst
TOUCH = """
(st) => {
  const c = _levelCfg(); if (c) XART.rdy(stageMasterKey(c));
  const cc = (typeof ENTRY_CONN !== 'undefined') ? (ENTRY_CONN[st] || {}) : {};
  if (cc.flat) XART.rdy(cc.flat);
  if (cc.bed && typeof _liquidFrames === 'function') _liquidFrames(cc.bed);
  return true;
}
"""

READY = """
(st) => {
  const c = _levelCfg(); if (!c || !XART.rdy(stageMasterKey(c))) return false;
  const cc = (typeof ENTRY_CONN !== 'undefined') ? (ENTRY_CONN[st] || {}) : {};
  if (cc.flat && !XART.rdy(cc.flat)) return false;
  if (cc.bed && typeof _liquidFrames === 'function') {
    const fr = _liquidFrames(cc.bed);
    if (!fr || !fr.length) return false;
    for (const f of fr) if (!(f && f.complete && f.naturalWidth)) return false;
  }
  return true;
}
"""

RUN = r"""
() => {
  const cv = document.querySelector('#screen-area canvas') || document.querySelector('canvas');
  const W = cv.width, H = cv.height;
  /* ⚠ alpha:false. With an alpha-backed scratch canvas, getImageData round-trips through
     premultiplied alpha and comes back a few counts off on any pixel that is not fully opaque —
     which showed up as tens of percent of "differing" pixels that a lossless PNG capture of the
     same two frames did not see. The comparison surface has to be exact or it invents differences. */
  const sc = document.createElement('canvas'); sc.width = W; sc.height = H;
  const sx = sc.getContext('2d', {alpha:false});
  const grab = () => { sx.clearRect(0,0,W,H); sx.drawImage(cv,0,0); return sx.getImageData(0,0,W,H).data; };

  // the countdown is drawn at VH*0.34..0.52 in logical space; compare strictly BELOW it, so the
  // terrain band — the thing that has to be continuous — is what is measured
  const band = Math.floor(H * 0.60);

  /* THE SHIP'S OWN ROWS ARE REPORTED SEPARATELY, and it is not a fudge — it is the finding.
     drawLaunch draws the ship ITSELF (drawShipSprite plus a hand-rolled nthp_ plume blitted with
     'lighter'), while PLAY draws the player through its own path. Two draws of one object that
     nothing forces to agree — the same shape as the pose seam 0810a fixed, one layer further in,
     and still live: the plume changes appearance on the GO frame. Everything OUTSIDE those rows is
     terrain, which is what the connector is responsible for, so the two numbers answer two
     different questions and mixing them hides both. */
  /* THE CRAFT IS MASKED AS A BOX, NOT AS WHOLE ROWS. Measured on stage 2: every remaining
     differing pixel sat in rows 737-966 AND columns 425-534 — the ship and the plume beneath it,
     110px wide, and nothing else anywhere in the band. Masking whole rows to cover the plume would
     have thrown away the bottom third of the frame and left a sample too small to mean anything;
     a box costs about 4% of the band and leaves the terrain measurement honest. */
  const pxPerLogical = H / 512;                         // canvas px per logical px (VH is 512)
  let shipTop = -1, shipBot = -1, shipL = -1, shipR = -1;
  try { const p = playShipPose();
        shipTop = (p.y - p.h*0.90)*pxPerLogical;
        shipBot = (p.y + p.h*1.60)*pxPerLogical;        // the plume reaches well below the hull
        shipL   = (p.x - p.h*0.85)*pxPerLogical;
        shipR   = (p.x + p.h*0.85)*pxPerLogical; } catch(e) {}

  const diff = (a,b) => {
    let n=0, tot=0, worst=0, nT=0, totT=0;
    for (let y = band; y < H; y++) {
      const yShip = (y >= shipTop && y <= shipBot);
      for (let x = 0; x < W; x++) {
        const i = (y*W+x)*4;
        const d = Math.max(Math.abs(a[i]-b[i]), Math.abs(a[i+1]-b[i+1]), Math.abs(a[i+2]-b[i+2]));
        tot++; if (d > 8) n++;
        if (d > worst) worst = d;
        if (!(yShip && x >= shipL && x <= shipR)) { totT++; if (d > 8) nT++; }
      }
    }
    return {differing:n, total:tot, pct:+(100*n/tot).toFixed(3), worstChannelDelta:worst,
            terrainDiffering:nT, terrainTotal:totT, terrainPct:+(100*nT/Math.max(1,totT)).toFixed(3),
            shipBox:[Math.round(shipL), Math.round(shipTop), Math.round(shipR), Math.round(shipBot)]};
  };

  /* ⚠ FREEZE THE ANIMATION CLOCK FOR THE WHOLE BURST.
     loop() is handed its timestamp explicitly, so the WORLD still advances normally — dt stays a
     true 16.7ms and every phase machine runs at its authored speed. What freezes is the separate
     thing that reads the wall clock directly to pick a REEL FRAME: the animated liquid bed, the
     thruster plume, the connector surface. Those advance on their own timer, and they were
     wrecking this measurement — a getImageData on a 960x1024 canvas costs real milliseconds, so
     the water could and did step a frame BETWEEN the two captures. That reads as ~68% of the
     stage-1 band differing when nothing about the join has moved at all: the water was simply
     being water. Held still, what remains is geometry, which is the thing under test. */
  const _realNow = performance.now.bind(performance);
  const _frozen = _realNow();
  performance.now = () => _frozen;

  const t0 = _frozen;
  let f = 0;
  const step = () => { loop(t0 + (f++)*16.7); };

  /* STEP FIRST, GRAB SECOND — see the header. Each captured frame is labelled with the state that
     DREW it, so a frame can never be filed under the wrong side of the handoff again. */
  let lastCine = null, joinPlay = null, rawPlay = null, cineState = null, frames = 0;
  let ivAtFlip = null;
  for (let i = 0; i < 6000; i++) {
    const before = String(state);
    step(); frames++;
    const after = String(state);
    if (before !== 'play' && after === 'play') {
      cineState = before;
      lastCine = grab();          // the frame the step above just drew, while still in `before`

      /* ---- THE JOIN, ISOLATED ----
         Two variables sit between these frames that have NOTHING to do with whether the picture
         is continuous, and both had to be held still or they drown the measurement:

           mapScroll   PLAY's first tick advances it by dt*40 (0.67px). That is the level
                       correctly STARTING TO MOVE, not a cut — but it resamples the master at a
                       fractional source offset, and on a high-frequency plate that trips the
                       per-pixel threshold almost everywhere. Held by drawing with dt = 0.
           i-frames    player.reset() leaves invuln at 120 and the player draw hides the ship on
                       a 4-on/4-off blink (game.js: `Math.floor(player.invuln/4)%2`), so the ship
                       is INVISIBLE on play's first tick at every stage, every time — while the
                       cinematic drew it solid a frame earlier. Neutralised here so the two sides
                       are comparable; it is reported separately below, because a ship that
                       strobes the instant control is handed over is its own finding, not noise.
           shake       drawLaunch fires shake=5 with GO, and drawWorld applies it as a RANDOM
                       translate of the entire scene. A random offset makes every pixel differ by
                       construction. It is a deliberate jolt on the GO beat, not a property of the
                       join, so it is held at 0 for the comparison.

         Whatever still differs once those are held IS the join. */
      ivAtFlip = player.invuln;
      const _iv = player.invuln, _sh = shake;
      player.invuln = 0; shake = 0;
      try { ctx.setTransform(SS,0,0,SS,0,0); } catch(e) {}
      drawWorld(0);
      joinPlay = grab();
      player.invuln = _iv; shake = _sh;

      step(); frames++;           // and the next REAL frame, unmodified, for the raw number
      rawPlay = grab();
      break;
    }
    if (before === 'play') { return {err:'already in play before any cinematic ran'}; }
  }
  if (!lastCine || !joinPlay) return {err:'never crossed the handoff', state:String(state), frames:frames};
  return {ok:true, band:band, H:H, W:W, cineState:cineState, frames:frames, invulnAtFlip:ivAtFlip,
          mapScroll:(typeof mapScroll!=='undefined'?mapScroll:null),
          camX:(typeof camX!=='undefined'?camX:null),
          join: diff(lastCine, joinPlay),
          raw:  diff(lastCine, rawPlay)};
}
"""


def run_stage(browser, url, stage):
    pg = browser.new_page(viewport={'width': 1100, 'height': 1200}, device_scale_factor=1)
    errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)[:200]))
    try:
        pg.goto(url, wait_until='load', timeout=60000)
        pg.wait_for_function("() => typeof ASSETS!=='undefined' && typeof setState==='function'", timeout=45000)
        pg.wait_for_function("() => (window.__bofFrames|0) > 4", timeout=45000)
        st0 = pg.evaluate(SETUP, stage)
        pg.evaluate(TOUCH, stage)                      # ⚠ art BEFORE the burst — see the header
        try:
            pg.wait_for_function(READY, arg=stage, timeout=60000)
        except Exception:
            return {'err': 'connector art never decoded — this would have measured blank vs blank',
                    'entryState': st0, 'pageErrors': errs[:3]}
        r = pg.evaluate(RUN)
        r['entryState'] = st0
        r['pageErrors'] = errs[:3]
        return r
    finally:
        pg.close()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--stage', default=None, help='one stage, or a comma list; default is 1-8')
    args = ap.parse_args()
    stages = ([int(s) for s in args.stage.split(',')] if args.stage else DEFAULT_STAGES)

    from playwright.sync_api import sync_playwright
    port, stop = serve(GAME)
    url = 'http://127.0.0.1:%d/index.html' % port
    results = {}
    with sync_playwright() as p:
        b = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
        for st in stages:
            results[st] = run_stage(b, url, st)
        b.close()
    stop()

    print('THE JOIN: the entry cinematic\'s last frame vs PLAY\'s first frame.')
    print('Compared below y=0.60*H — the countdown sits above that; the terrain band is what')
    print('has to be continuous. A pixel counts as differing if any channel moves by more than 8.\n')
    bad = 0
    for st in stages:
        r = results[st]
        if r.get('err'):
            print('  stage %d   FAIL — %s' % (st, r['err']))
            if r.get('pageErrors'):
                print('            page errors: %s' % r['pageErrors'])
            bad += 1
            continue
        j = r['join']
        verdict = 'SEAMLESS' if j['terrainPct'] < 1.0 else 'A CUT'
        print('  stage %d   %-9s TERRAIN %6d / %d = %6.3f%%'
              % (st, verdict, j['terrainDiffering'], j['terrainTotal'], j['terrainPct']))
        print('            whole band incl. the craft %6.3f%%  (craft box x%d-%d y%d-%d draws twice)'
              % (j['pct'], j['shipBox'][0], j['shipBox'][2], j['shipBox'][1], j['shipBox'][3]))
        print('            from %-7s after %d frames; mapScroll %.2f camX %.1f invuln %s'
              % (r['cineState'], r['frames'], r['mapScroll'] or 0, r['camX'] or 0, r['invulnAtFlip']))
        if r.get('pageErrors'):
            print('            ⚠ page errors: %s' % r['pageErrors'])
        if j['terrainPct'] >= 1.0:
            bad += 1
    print('\n%s' % ('ALL JOINS SEAMLESS — every stage flies into its own first frame'
                    if bad == 0 else '%d stage(s) still cut' % bad))
    sys.exit(0 if bad == 0 else 1)


if __name__ == '__main__':
    main()
