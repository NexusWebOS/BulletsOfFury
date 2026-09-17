#!/usr/bin/env python3
"""
probe_halopad_0916.py - HOW FAR DOES shadowBlur=7 ACTUALLY REACH?

    python _BUILD_SOURCE/probe_halopad_0916.py

SPACE_LASER_GLOW_PAD was set to 20 on a rule of thumb ("blur reaches ~1.5x its radius"). The pad
is pure fill rate: every laser round blits a plate of (lw + 2*pad) x (lh + 2*pad) under 'lighter',
138 times a frame, so an over-generous pad is measurable waste and an under-generous one CLIPS THE
GLOW, which is a visible art change.

This measures the real extent: bake the halo with a large pad, then find the outermost row and
column carrying any alpha at all. The answer sets the constant, rather than the constant being a
guess that happens to work.
"""
import os, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
GAME = os.path.abspath(os.path.join(ROOT, '..'))
sys.path.insert(0, ROOT)
from shoot import serve  # noqa: E402
from profile_space_0916 import SETUP  # noqa: E402

MEASURE = r"""
() => {
  if (typeof spaceLaserPulseCanvas !== 'function') return {err:'no pulse fn'};
  const BLUR = (typeof SPACE_LASER_GLOW_BLUR !== 'undefined') ? SPACE_LASER_GLOW_BLUR : 7;
  const BIG = 60;                       // deliberately far larger than any plausible pad
  const out = {blur:BLUR, rows:[]};
  for (const lv of [1,2,3,4,5]) {
    for (const pulse of [0,1]) {
      const key = 'laser_' + lv + '_pulse_' + ((pulse&1)?'short':'long');
      const lp = spaceLaserPulseCanvas(key);
      if (!lp) continue;
      const col = SPACE_LASER_COL[Math.max(0,Math.min(4,lv-1))];
      const lh = 20, lw = lh*(lp.width/lp.height);
      const c = document.createElement('canvas');
      c.width = Math.ceil(lw)+BIG*2; c.height = Math.ceil(lh)+BIG*2;
      const g = c.getContext('2d');
      const OFF = c.width+8;
      g.shadowColor = col; g.shadowBlur = BLUR; g.shadowOffsetX = OFF;
      g.drawImage(lp, BIG-OFF, BIG, lw, lh);
      const d = g.getImageData(0,0,c.width,c.height).data;
      let minX=c.width, maxX=-1, minY=c.height, maxY=-1;
      for (let y=0;y<c.height;y++){
        for (let x=0;x<c.width;x++){
          if (d[(y*c.width+x)*4+3] > 0){
            if(x<minX)minX=x; if(x>maxX)maxX=x;
            if(y<minY)minY=y; if(y>maxY)maxY=y;
          }
        }
      }
      // how far the halo reaches OUTSIDE the sprite's own box
      out.rows.push({key:key, lw:+lw.toFixed(2), lh:lh,
                     left: BIG-minX, right: maxX-(BIG+Math.ceil(lw)-1),
                     top: BIG-minY, bottom: maxY-(BIG+Math.ceil(lh)-1)});
    }
  }
  return out;
}
"""


def main():
    from playwright.sync_api import sync_playwright
    port, stop = serve(GAME)
    url = 'http://127.0.0.1:%d/index.html' % port
    with sync_playwright() as p:
        b = p.chromium.launch(headless=True, args=['--no-sandbox', '--mute-audio'])
        pg = b.new_page(viewport={'width': 1100, 'height': 1250}, device_scale_factor=1)
        pg.goto(url, wait_until='load', timeout=60000)
        pg.wait_for_function("() => typeof ASSETS!=='undefined' && typeof setState==='function'",
                             timeout=45000)
        pg.wait_for_function("() => (window.__bofFrames|0) > 4", timeout=45000)
        pg.evaluate(SETUP, {'stage': 9, 'pilot': 'cole'})
        pg.wait_for_timeout(3500)
        res = pg.evaluate(MEASURE)
        b.close()
    stop()

    if res.get('err'):
        print(res['err']); return
    print('  shadowBlur = %d' % res['blur'])
    print('  %-24s %10s %7s %7s %7s %7s' % ('plate', 'sprite', 'left', 'right', 'top', 'bottom'))
    worst = 0
    for r in res['rows']:
        worst = max(worst, r['left'], r['right'], r['top'], r['bottom'])
        print('  %-24s %10s %7d %7d %7d %7d'
              % (r['key'], '%.1fx%d' % (r['lw'], r['lh']),
                 r['left'], r['right'], r['top'], r['bottom']))
    print('')
    print('  furthest the halo reaches beyond the sprite: %d px' % worst)
    print('  so SPACE_LASER_GLOW_PAD needs to be at least %d (+1 for the sub-pixel phase)'
          % (worst + 1))


if __name__ == '__main__':
    main()
