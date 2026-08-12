#!/usr/bin/env python3
"""
probe_exit.py — is the outbound cinematic's FIRST frame the level's LAST frame?

    python3 _BUILD_SOURCE/probe_exit.py            # every stage with a built route
    python3 _BUILD_SOURCE/probe_exit.py --stage 2

WHY THIS EXISTS
Mike, 0810i: "Level 2 boss cuts to the lava instead of a connecting section at the end of the level
and another one to lead us to the cinematic that we can scroll infinitely."

probe_arrival.py measures the way IN. Nothing measured the way OUT, and the way out was worse: the
outbound drew the master through a modulo loop keyed off o.scroll, which starts at 0, so
`sY = H - (0 % H) - VH` landed on the BOTTOM of the plate. The boss died at the top of the level
and the volcano jumped straight back to the level's FIRST frame — a cut of the entire picture that
no state check could see, because mapScroll, camX and the player were all exactly where they
belonged. Same lesson as the arrival: only pixels can see a wrong picture drawn in the right place.

This is the mirror of probe_arrival, and it takes the same two precautions, for the same reasons
(both of which cost a debugging pass over there):

  FREEZE THE ANIMATION CLOCK. loop() is handed its timestamp, so the world still advances; what
  freezes is the wall clock the liquid reel and the plume read directly to pick a FRAME. Without
  it, a getImageData between the two captures is long enough for the water to step, and that reads
  as half the frame differing when nothing has moved.

  MASK THE CRAFT. PLAY draws the player through drawWorld; the outbound draws it held, through its
  own path. Two draws of one object that nothing forces to agree — reported separately rather than
  mixed into the terrain number it would otherwise swamp.
"""
import http.server, socketserver, threading, os, sys, functools, argparse

ROOT = os.path.dirname(os.path.abspath(__file__))
GAME = os.path.abspath(os.path.join(ROOT, '..'))

# only the joins that are actually built — outboundStart populates `via` for 1, 2 and 3 only
DEFAULT_STAGES = [2]


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
  setState(GS.PLAY);
  return String(state);
}
"""

TOUCH = """
(st) => {
  const c = _levelCfg(); if (c) XART.rdy(stageMasterKey(c));
  const cc = (typeof ENTRY_CONN !== 'undefined') ? (ENTRY_CONN[st] || {}) : {};
  if (cc.flat) XART.rdy(cc.flat);
  if (cc.bed && typeof _liquidFrames === 'function') _liquidFrames(cc.bed);
  XART.rdy('tflat_ice');                      // the 2->3 route freezes over
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
(st) => {
  const cv = document.querySelector('#screen-area canvas') || document.querySelector('canvas');
  const W = cv.width, H = cv.height;
  const sc = document.createElement('canvas'); sc.width = W; sc.height = H;
  const sx = sc.getContext('2d', {alpha:false});
  const grab = () => { sx.clearRect(0,0,W,H); sx.drawImage(cv,0,0); return sx.getImageData(0,0,W,H).data; };
  const band = Math.floor(H * 0.60);

  const pxPerLogical = H / 512;
  let sT=-1, sB=-1, sL=-1, sR=-1;
  try { const p = playShipPose();
        sT=(p.y-p.h*0.90)*pxPerLogical; sB=(p.y+p.h*1.60)*pxPerLogical;
        sL=(p.x-p.h*0.85)*pxPerLogical; sR=(p.x+p.h*0.85)*pxPerLogical; } catch(e){}

  const diff = (a,b) => {
    let n=0,tot=0,worst=0,nT=0,totT=0;
    for (let y=band; y<H; y++){
      const yS=(y>=sT && y<=sB);
      for (let x=0; x<W; x++){
        const i=(y*W+x)*4;
        const d=Math.max(Math.abs(a[i]-b[i]),Math.abs(a[i+1]-b[i+1]),Math.abs(a[i+2]-b[i+2]));
        tot++; if(d>8) n++; if(d>worst) worst=d;
        if(!(yS && x>=sL && x<=sR)){ totT++; if(d>8) nT++; }
      }
    }
    return {pct:+(100*n/tot).toFixed(3), terrainPct:+(100*nT/Math.max(1,totT)).toFixed(3),
            terrainDiffering:nT, terrainTotal:totT, worstChannelDelta:worst};
  };

  // freeze the reel clock — see the header
  const _realNow = performance.now.bind(performance);
  const _frozen = _realNow();
  performance.now = () => _frozen;

  /* Put the level at its END, which is where a boss dies, and draw PLAY's last frame. dt 0 so
     mapScroll does not move between this frame and the outbound's first. */
  const rng = (typeof levelScrollRange === 'function') ? levelScrollRange() : 0;
  mapScroll = rng;
  try { ctx.setTransform(SS,0,0,SS,0,0); } catch(e) {}
  /* ⚠ NO drawScanlines() HERE. drawWorld ends with its own call, and adding a second darkened
     every other row TWICE — which measured as 39% of the band differing and looked exactly like a
     real cut. The outbound side below does need one, because drawOutbound applies it around
     outboundDraw() rather than inside it. Mirror the real call sites, not the intent. */
  drawWorld(0);
  const playLast = grab();

  // now hand over exactly as the stage clear does
  outboundStart(st);
  setState(GS.OUTBOUND);
  const via = (outbound && outbound.via) ? outbound.via.slice() : [];
  try { ctx.setTransform(SS,0,0,SS,0,0); } catch(e) {}
  outboundDraw();
  if (typeof drawScanlines === 'function') drawScanlines();
  const outFirst = grab();

  return {ok:true, via:via, phase:outbound?outbound.phase:null,
          exitDy:(outbound&&outbound.exitDy)||0, mapScroll:mapScroll, range:rng,
          join: diff(playLast, outFirst)};
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
        pg.evaluate(SETUP, stage)
        pg.evaluate(TOUCH, stage)
        try:
            pg.wait_for_function(READY, arg=stage, timeout=60000)
        except Exception:
            return {'err': 'connector art never decoded — this would have measured blank vs blank',
                    'pageErrors': errs[:3]}
        r = pg.evaluate(RUN, stage)
        r['pageErrors'] = errs[:3]
        return r
    finally:
        pg.close()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--stage', default=None, help='one stage, or a comma list; default is 2')
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

    print("THE EXIT JOIN: PLAY's last frame vs the outbound cinematic's first frame.")
    print('Compared below y=0.60*H. The craft is masked — PLAY draws it and the outbound holds it,')
    print('through two different paths, so it is reported apart from the terrain.\n')
    bad = 0
    for st in stages:
        r = results[st]
        if r.get('err'):
            print('  stage %d   FAIL — %s' % (st, r['err'])); bad += 1; continue
        j = r['join']
        verdict = 'SEAMLESS' if j['terrainPct'] < 1.0 else 'A CUT'
        print('  stage %d -> %d   %-9s TERRAIN %6d / %d = %6.3f%%'
              % (st, st+1, verdict, j['terrainDiffering'], j['terrainTotal'], j['terrainPct']))
        print('               whole band incl. the craft %6.3f%%   route via %s'
              % (j['pct'], r['via']))
        print('               mapScroll %.0f of range %.0f, exitDy %.1f, phase %s'
              % (r['mapScroll'], r['range'], r['exitDy'], r['phase']))
        if r.get('pageErrors'):
            print('               ⚠ page errors: %s' % r['pageErrors'])
        if j['terrainPct'] >= 1.0:
            bad += 1
    print('\n%s' % ('THE LEVEL IS FLOWN OUT OF, NOT CUT AWAY FROM' if bad == 0
                    else '%d exit(s) still cut' % bad))
    sys.exit(0 if bad == 0 else 1)


if __name__ == '__main__':
    main()
