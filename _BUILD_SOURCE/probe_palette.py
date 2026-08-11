#!/usr/bin/env python3
"""
probe_palette.py — prove a palette swap is a PALETTE SWAP.

    python3 _BUILD_SOURCE/probe_palette.py

WHY THIS EXISTS
"Palette/luminance swaps, not overlays" is a load-bearing rule in this project, not a preference —
xartTint's source-atop flood repainted the font's opaque drop shadow and turned ENTER into BNTBR,
and it looked like a font bug for three drops. The thing that would have ended it immediately was
comparing the tinted and untinted renders.

So this compares them. For each (source key -> swapped colour) pair it reports mean HUE and mean
LUMINANCE of the source and of the swap. A correct palette swap moves hue and holds luminance. An
overlay flattens luminance toward the flood colour, which is exactly what this catches.

It also confirms Axel's ball actually emits an axbeam through the game's own code path, because a
correctly-swapped sprite that nothing draws is still a bug — see the muzzle flash that was drawing
on the wrong frame of its reel while every assertion passed.
"""
import http.server, socketserver, threading, os, sys, functools, json

ROOT = os.path.dirname(os.path.abspath(__file__))
GAME = os.path.abspath(os.path.join(ROOT, '..'))

PAIRS = [('florb_3', '#2f6fff', "Axel's orbiting ball <- Falva's helper ball"),
         ('fllaser_3', '#2f6fff', "Axel's bolt        <- Falva's laser")]


def serve(directory, port=0):
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=directory)
    handler.log_message = lambda *a, **k: None
    httpd = socketserver.TCPServer(("127.0.0.1", port), handler)
    port = httpd.server_address[1]
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return port, httpd.shutdown


# mean hue / luminance over the OPAQUE pixels only — the transparent margin would drag both toward
# zero and make every comparison look the same
STATS = r"""
(cfg) => {
  const out = {};
  const meas = (img) => {
    const w = img.width || img.naturalWidth, h = img.height || img.naturalHeight;
    if (!w || !h) return null;
    const c = document.createElement('canvas'); c.width = w; c.height = h;
    const x = c.getContext('2d'); x.drawImage(img, 0, 0);
    let d; try { d = x.getImageData(0, 0, w, h).data; } catch(e) { return {err: String(e)}; }
    let n = 0, lum = 0, hx = 0, hy = 0, sat = 0;
    for (let i = 0; i < d.length; i += 4) {
      const a = d[i+3]; if (a < 128) continue;
      const r = d[i]/255, g = d[i+1]/255, b = d[i+2]/255;
      const mx = Math.max(r,g,b), mn = Math.min(r,g,b);
      lum += 0.2126*r + 0.7152*g + 0.0722*b;
      const s = mx ? (mx-mn)/mx : 0; sat += s;
      if (mx !== mn) {
        let hdeg;
        if (mx === r) hdeg = 60*(((g-b)/(mx-mn))%6);
        else if (mx === g) hdeg = 60*(((b-r)/(mx-mn))+2);
        else hdeg = 60*(((r-g)/(mx-mn))+4);
        const rad = hdeg*Math.PI/180;
        // circular mean, weighted by saturation: averaging degrees directly wraps wrongly at 360
        hx += Math.cos(rad)*s; hy += Math.sin(rad)*s;
      }
      n++;
    }
    if (!n) return null;
    let hue = Math.atan2(hy, hx)*180/Math.PI; if (hue < 0) hue += 360;
    return {n: n, lum: lum/n, sat: sat/n, hue: hue};
  };
  for (const [key, col, label] of cfg.pairs) {
    const r = {label: label, key: key, col: col};
    if (!XART.rdy(key)) { r.err = 'source not decoded'; out[key] = r; continue; }
    r.src = meas(XART.get(key));
    const sw = xartPalette(key, col);
    r.swapped = sw ? meas(sw) : null;
    if (!sw) r.err = 'xartPalette returned null';
    out[key] = r;
  }
  return out;
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
        pg.wait_for_function("() => typeof ASSETS!=='undefined' && typeof xartPalette==='function'",
                             timeout=45000)
        pg.wait_for_function("() => (window.__bofFrames|0) > 4", timeout=45000)

        # XART.rdy is false on its FIRST call — that call starts the load. Poll, never one-shot.
        pg.evaluate("(keys) => keys.forEach(k => XART.rdy(k))", [k for k, _, _ in PAIRS])
        try:
            pg.wait_for_function("(keys) => keys.every(k => XART.rdy(k))",
                                 arg=[k for k, _, _ in PAIRS], timeout=30000)
        except Exception:
            print('WARNING: source art never decoded; results below will say so')

        stats = pg.evaluate(STATS, {'pairs': [list(x) for x in PAIRS]})

        # and does the game actually emit an axbeam through its own path?
        emit = pg.evaluate("""() => {
            try {
              ASSETS.ready = true; run.pilot = 'axel';
              curStage = STAGES[0]; beginStage(1); setState(GS.PLAY);
              player.reset(); player.invuln = 1e9; startSpecial();
              const seen = {};
              for (let i = 0; i < 400; i++) {
                loop(performance.now() + i*16.7);
                for (const b of pBullets) if (b.kind === 'axbeam') {
                  seen.any = true;
                  if (b._f == null) seen.noFrame = true; else seen.frames = (seen.frames||{}), seen.frames[b._f] = 1;
                }
              }
              return {ok:true, any: !!seen.any, noFrame: !!seen.noFrame,
                      distinctFrames: seen.frames ? Object.keys(seen.frames).length : 0};
            } catch(e) { return {ok:false, err:String(e && e.message || e)}; }
        }""")
        b.close()
    stop()

    print('=== PALETTE SWAP: hue must MOVE, luminance must HOLD ===\n')
    bad = 0
    for key, col, label in PAIRS:
        r = stats.get(key) or {}
        print('%s   [%s -> %s]' % (label, key, col))
        if r.get('err'):
            print('   FAIL: %s\n' % r['err']); bad += 1; continue
        s, w = r.get('src'), r.get('swapped')
        if not s or not w:
            print('   FAIL: could not measure\n'); bad += 1; continue
        dl = abs(w['lum'] - s['lum'])
        dh = abs(((w['hue'] - s['hue'] + 180) % 360) - 180)
        print('   source   hue %6.1f°   lum %.3f   sat %.3f   (%d opaque px)'
              % (s['hue'], s['lum'], s['sat'], s['n']))
        print('   swapped  hue %6.1f°   lum %.3f   sat %.3f'
              % (w['hue'], w['lum'], w['sat']))
        okh, okl = dh > 30, dl < 0.06
        print('   hue moved %5.1f°  %s      luminance held  %+.3f  %s'
              % (dh, 'OK' if okh else 'FAIL - not a swap',
                 w['lum'] - s['lum'], 'OK' if okl else 'FAIL - overlay, not a palette swap'))
        if not (okh and okl):
            bad += 1
        print()

    print('=== and the bolt is actually emitted by the game ===')
    if not emit.get('ok'):
        print('   FAIL:', emit.get('err')); bad += 1
    else:
        print('   axbeam spawned: %s   _f set at spawn: %s   distinct frames seen: %d'
              % (emit['any'], not emit['noFrame'], emit['distinctFrames']))
        if not emit['any'] or emit['noFrame']:
            bad += 1

    if errs:
        print('\npage errors:', errs[:4])
    print('\n%s' % ('ALL CHECKS PASSED' if bad == 0 else '%d CHECK(S) FAILED' % bad))
    sys.exit(0 if bad == 0 else 1)


if __name__ == '__main__':
    main()
