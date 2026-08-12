#!/usr/bin/env python3
"""
probe_arrival.py — is the opening's last frame the level's FIRST frame?

    python3 _BUILD_SOURCE/probe_arrival.py

WHY THIS EXISTS
Mike: "connect the last transition tile to the level's first frame ... so we truly fly into level
1. No more fake transitions."

probe_seam.py already showed the numbers were clean across that handoff — mapScroll 0 -> 0, camX
160 -> 160, the ship untouched. Nothing jumped. And the transition was still fake, because the
opening generated a coastline from sine terms while PLAY painted the jungle master: same numbers,
different picture. Numbers cannot see that. Only pixels can.

So this reads the actual canvas on both sides of the flip and diffs them. The countdown text is
drawn over the cinematic and not over PLAY, so the frames are compared BELOW it — the terrain band
is what has to be continuous.

⚠ ART FIRST, THEN STEP. The stepping happens in one evaluate so dt stays at a true 16.7ms, and a
single synchronous burst never yields, so nothing can load during it (the --warm trap). The master
and the water flat are therefore polled to ready BEFORE the burst starts. Get that order wrong and
this measures a blank screen against a blank screen and calls it a perfect match.
"""
import http.server, socketserver, threading, os, sys, functools, json

ROOT = os.path.dirname(os.path.abspath(__file__))
GAME = os.path.abspath(os.path.join(ROOT, '..'))


def serve(directory, port=0):
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=directory)
    handler.log_message = lambda *a, **k: None
    httpd = socketserver.TCPServer(("127.0.0.1", port), handler)
    port = httpd.server_address[1]
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return port, httpd.shutdown


RUN = r"""
() => {
  const cv = document.querySelector('#screen-area canvas') || document.querySelector('canvas');
  const W = cv.width, H = cv.height;
  const sc = document.createElement('canvas'); sc.width = W; sc.height = H;
  const sx = sc.getContext('2d');
  const grab = () => { sx.clearRect(0,0,W,H); sx.drawImage(cv,0,0); return sx.getImageData(0,0,W,H).data; };

  // the countdown is drawn at VH*0.42 in logical space; compare strictly BELOW it
  const band = Math.floor(H * 0.60);

  const diff = (a,b) => {
    let n = 0, tot = 0;
    for (let y = band; y < H; y++) {
      for (let x = 0; x < W; x++) {
        const i = (y*W+x)*4; tot++;
        if (Math.abs(a[i]-b[i])>8 || Math.abs(a[i+1]-b[i+1])>8 || Math.abs(a[i+2]-b[i+2])>8) n++;
      }
    }
    return {differing:n, total:tot, pct:+(100*n/tot).toFixed(3)};
  };

  const t0 = performance.now();
  let f = 0, lastOpen = null, firstPlay = null, sawArrival = false, tAtLand = null;
  const step = () => { loop(t0 + (f++)*16.7); };

  for (let i = 0; i < 3000; i++) {
    const st = String(state);
    if (st === 'opening') {
      if (opening && opening.t >= OPEN_T[3] && tAtLand === null) tAtLand = opening.t;
      lastOpen = grab();          // keep overwriting: the last one is the frame before the flip
      sawArrival = sawArrival || !!window.__sawArrival;
      step();
    } else if (st === 'play') {
      firstPlay = grab();
      break;
    } else { step(); }
  }
  if (!lastOpen || !firstPlay) return {err:'never crossed the handoff', state:String(state)};
  return {ok:true, band:band, H:H, tAtLand:tAtLand,
          terrain: diff(lastOpen, firstPlay)};
}
"""


def main():
    from playwright.sync_api import sync_playwright
    port, stop = serve(GAME)
    url = 'http://127.0.0.1:%d/index.html' % port
    errs = []
    with sync_playwright() as p:
        b = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
        pg = b.new_page(viewport={'width': 1100, 'height': 1200}, device_scale_factor=1)
        pg.on('pageerror', lambda e: errs.append(str(e)[:200]))
        pg.goto(url, wait_until='load', timeout=60000)
        pg.wait_for_function("() => typeof ASSETS!=='undefined' && typeof setState==='function'", timeout=45000)
        pg.wait_for_function("() => (window.__bofFrames|0) > 4", timeout=45000)

        pg.evaluate("""() => {
            ASSETS.ready = true; run.pilot='cole'; curStage = STAGES[0];
            beginStage(1);
            if (String(state) !== 'opening') { openingStart(1); setState(GS.OPENING); }
        }""")

        # ⚠ art BEFORE the burst — see the header
        pg.evaluate("""() => { const c=_levelCfg(); XART.rdy(stageMasterKey(c)); XART.rdy('tflat_water'); }""")
        try:
            pg.wait_for_function(
                "() => { const c=_levelCfg(); return XART.rdy(stageMasterKey(c)) && XART.rdy('tflat_water'); }",
                timeout=60000)
        except Exception:
            print('FAIL: the stage master never decoded — this would have measured blank vs blank')
            b.close(); stop(); sys.exit(1)

        r = pg.evaluate(RUN)
        b.close()
    stop()

    if r.get('err'):
        print('FAIL:', r['err'], r); sys.exit(1)

    t = r['terrain']
    print('compared the terrain band below y=%d of %d (the countdown sits above it)' % (r['band'], r['H']))
    print('the level landed at t=%.2fs, and OPEN_T[3] is where COAST ends\n' % (r['tAtLand'] or -1))
    print('  last cinematic frame vs first PLAY frame:')
    print('     differing pixels %d / %d  =  %.3f%%' % (t['differing'], t['total'], t['pct']))
    ok = t['pct'] < 1.0
    print('\n  %s' % ('SAME PICTURE — we fly into the real level' if ok else
                      'STILL A CUT — the picture changes at the handoff'))
    if errs:
        print('\npage errors:', errs[:4])
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
