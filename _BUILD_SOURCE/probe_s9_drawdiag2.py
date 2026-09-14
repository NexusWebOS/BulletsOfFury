#!/usr/bin/env python3
"""probe_s9_drawdiag2.py - XART._src carries ns9e_wskim_idle, yet XART.rdy() stays false and the
browser never requests the PNG. Ask the loader directly what object it handed back. 0905z."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shoot as sh
from playwright.sync_api import sync_playwright

Q = r"""
() => {
  const k = 'ns9e_wskim_idle';
  const o = {};
  o.inImg      = !!(window.BOFX && BOFX.img && BOFX.img[k]);
  o.imgPath    = (window.BOFX && BOFX.img) ? BOFX.img[k] : null;
  o.inCells    = !!(window.BOFX && BOFX.cells && BOFX.cells[k]);
  o.cellRec    = (window.BOFX && BOFX.cells) ? BOFX.cells[k] : null;
  o.inEcells   = !!(window.BOFX && BOFX.ecells && BOFX.ecells[k]);
  o.ecellRec   = (window.BOFX && BOFX.ecells) ? BOFX.ecells[k] : null;
  o.src        = XART._src ? XART._src[k] : null;
  o.root       = XART.root ? XART.root(k) : null;
  const raw = XART.raw(k);
  o.rawType    = raw === null ? 'null' : (raw === undefined ? 'undefined' : (raw.tagName || raw.constructor.name));
  o.rawSrc     = raw && raw.src ? raw.src : null;
  o.rawComplete= raw ? !!raw.complete : null;
  o.rawNW      = raw ? (raw.naturalWidth != null ? raw.naturalWidth : raw.width) : null;
  o.cachedImg  = (XART.img && XART.img[k] !== undefined) ? (XART.img[k] === null ? 'null' : 'obj') : 'absent';
  // and the same for the root texture, in case it is an atlas cell after all
  if (o.root && o.root !== k) {
    const rr = XART.raw(o.root);
    o.rootType = rr === null ? 'null' : (rr === undefined ? 'undefined' : (rr.tagName || rr.constructor.name));
    o.rootSrc = rr && rr.src ? rr.src : null;
    o.rootComplete = rr ? !!rr.complete : null;
    o.rootNW = rr ? (rr.naturalWidth != null ? rr.naturalWidth : rr.width) : null;
  }
  return o;
}
"""


def main():
    port, stop = sh.serve(sh.GAME)
    try:
        with sync_playwright() as pw:
            b = pw.chromium.launch()
            pg = b.new_page(viewport={'width': 480, 'height': 512})
            reqs = []
            pg.on('request', lambda r: reqs.append(r.url))
            pg.goto('http://127.0.0.1:%d/index.html' % port)
            pg.wait_for_function('typeof ASSETS!=="undefined" && typeof loop==="function"', timeout=30000)
            pg.wait_for_timeout(2500)
            pg.evaluate(sh.TRAP_RAF)
            pg.evaluate(sh.SETUP, {'state': 'PLAY', 'stage': 9, 'pilot': 'cole', 'invuln': True})
            pg.evaluate(sh.STEP, 30)
            for k, v in pg.evaluate(Q).items():
                print('  %-12s %s' % (k, v))
            pg.wait_for_timeout(1500)
            print('\n  after a real 1.5s wait, rdy =', pg.evaluate('() => XART.rdy("ns9e_wskim_idle")'))
            hits = [u for u in reqs if 'ns9e_' in u or 'void_rift/enemies' in u]
            print('  network requests touching the void roster: %d' % len(hits))
            for u in hits[:6]:
                print('    ', u)
            b.close()
    finally:
        stop()


if __name__ == '__main__':
    main()
