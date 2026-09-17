#!/usr/bin/env python3
"""
probe_laserpixels_0916.py - DID BAKING THE SPACE LASER'S GLOW CHANGE THE PICTURE?

    python _BUILD_SOURCE/probe_laserpixels_0916.py

The speedup is worthless if the round looks different. Mike owns every creative decision, and
CLAUDE.md's standing rule for this shape of change is the Magma Ward's: SAME PIXELS, less work.

This renders the shipped path (per-round `shadowBlur=7`) and the baked path into two offscreen
canvases at identical positions, over several destination colours, and diffs them channel by
channel.

⚠ SEVERAL DESTINATION COLOURS, NOT ONE, AND THAT IS THE POINT. The draw runs under
  `globalCompositeOperation='lighter'`, which ADDS to whatever is already there and clamps at 255.
  A comparison over a transparent or black background would agree even if the two paths composited
  differently, because addition and source-over are indistinguishable against nothing. The bright
  destination is where a wrong bake shows up.

⚠ AND IT TESTS THE FRACTIONAL POSITIONS THE GAME ACTUALLY USES. Bullets sit at arbitrary float
  coordinates; the baked plate is blitted 1:1 at a float origin while the shipped path scaled the
  sprite at a float origin. If that difference costs anything it costs it at fractional offsets,
  so the sweep includes .0, .25, .5 and .75.
"""
import argparse, os, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
GAME = os.path.abspath(os.path.join(ROOT, '..'))
sys.path.insert(0, ROOT)
from shoot import serve  # noqa: E402
from profile_space_0916 import SETUP  # noqa: E402

COMPARE = r"""
(cfg) => {
  if (typeof spaceLaserPulseCanvas !== 'function') return {err:'no spaceLaserPulseCanvas'};
  if (typeof spaceLaserGlowCanvas !== 'function') return {err:'no spaceLaserGlowCanvas (fix not loaded)'};
  const PAD = (typeof SPACE_LASER_GLOW_PAD !== 'undefined') ? SPACE_LASER_GLOW_PAD : 20;
  const BLUR = (typeof SPACE_LASER_GLOW_BLUR !== 'undefined') ? SPACE_LASER_GLOW_BLUR : 7;
  const W = 160, H = 160;
  const out = {rows:[]};

  function mk(){ const c=document.createElement('canvas'); c.width=W; c.height=H; return c; }
  const ca = mk(), cb = mk();
  const ga = ca.getContext('2d'), gb = cb.getContext('2d');

  for (const lv of [1,2,3,4,5]) {
    for (const pulse of [0,1]) {
      const key = 'laser_' + lv + '_pulse_' + ((pulse & 1) ? 'short' : 'long');
      const lp = spaceLaserPulseCanvas(key);
      if (!lp) { out.rows.push({key:key, err:'no pulse canvas'}); continue; }
      const col = SPACE_LASER_COL[Math.max(0, Math.min(4, lv-1))];
      const lh = Math.max(20, Math.min(30, (cfg.bh||26)*0.72));
      const lw = lh * (lp.width / lp.height);

      for (const bg of cfg.backgrounds) {
        for (const frac of cfg.fracs) {
          const x = 80 + frac, y = 80 + frac;

          ga.setTransform(1,0,0,1,0,0); gb.setTransform(1,0,0,1,0,0);
          ga.globalCompositeOperation='source-over'; gb.globalCompositeOperation='source-over';
          ga.globalAlpha=1; gb.globalAlpha=1;
          ga.clearRect(0,0,W,H); gb.clearRect(0,0,W,H);
          if (bg !== null) { ga.fillStyle=bg; ga.fillRect(0,0,W,H); gb.fillStyle=bg; gb.fillRect(0,0,W,H); }

          // --- A: the shipped draw
          ga.save(); ga.globalCompositeOperation='lighter';
          ga.shadowColor=col; ga.shadowBlur=BLUR;
          ga.drawImage(lp, x-lw/2, y-lh/2, lw, lh);
          ga.restore();

          // --- B: the baked plate at an INTEGER origin, with the sub-pixel phase baked in.
          // Mirrors the shipped call site exactly; if these two ever drift apart the probe is
          // measuring something the game does not do.
          const PH = (typeof SPACE_LASER_GLOW_PHASE !== 'undefined') ? SPACE_LASER_GLOW_PHASE : 4;
          const dx = x-lw/2, dy = y-lh/2;
          const ix = Math.floor(dx), iy = Math.floor(dy);
          const pxq = Math.round((dx-ix)*PH)%PH, pyq = Math.round((dy-iy)*PH)%PH;
          const glow = spaceLaserGlowCanvas(key, col, lw, lh, pxq, pyq);
          if (!glow) { out.rows.push({key:key, err:'no glow canvas'}); continue; }
          gb.save(); gb.globalCompositeOperation='lighter';
          gb.drawImage(glow, ix-PAD, iy-PAD);      // halo, cached
          gb.drawImage(lp, dx, dy, lw, lh);        // pulse, the original call verbatim
          gb.restore();

          const A = ga.getImageData(0,0,W,H).data;
          const B = gb.getImageData(0,0,W,H).data;
          let diff=0, maxd=0, lit=0;
          for (let i=0;i<A.length;i+=4){
            if (A[i]|A[i+1]|A[i+2]) lit++;
            for (let k=0;k<4;k++){
              const d = Math.abs(A[i+k]-B[i+k]);
              if (d) { diff++; if (d>maxd) maxd=d; }
            }
          }
          out.rows.push({key:key, bg:(bg||'transparent'), frac:frac,
                         litPx:lit, diffChannels:diff, maxDelta:maxd});
          if (cfg.shot && bg === cfg.shot.bg && frac === cfg.shot.frac && key === cfg.shot.key) {
            out.shotA = ca.toDataURL('image/png');
            out.shotB = cb.toDataURL('image/png');
          }
        }
      }
    }
  }
  return out;
}
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--stage', type=int, default=9)
    args = ap.parse_args()

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
        pg.evaluate(SETUP, {'stage': args.stage, 'pilot': 'cole'})
        pg.wait_for_timeout(3500)
        res = pg.evaluate(COMPARE, {
            'bh': 26,
            'backgrounds': [None, '#000000', '#204060', '#c8c8c8'],
            'fracs': [0.0, 0.25, 0.5, 0.75],
            'shot': {'bg': '#204060', 'frac': 0.25, 'key': 'laser_1_pulse_long'},
        })
        b.close()
    stop()

    if res.get('err'):
        print('  ' + res['err']); sys.exit(1)

    rows = res['rows']
    errs = [r for r in rows if r.get('err')]
    ok = [r for r in rows if not r.get('err')]
    worst = max((r['maxDelta'] for r in ok), default=-1)
    total_diff = sum(r['diffChannels'] for r in ok)
    total_lit = sum(r['litPx'] for r in ok)

    print('  %d comparisons (5 levels x 2 pulses x 4 backgrounds x 4 sub-pixel offsets)' % len(ok))
    for e in errs:
        print('  !! %s: %s' % (e['key'], e['err']))
    print('  worst single-channel delta: %d / 255' % worst)
    print('  channels differing at all : %d of %d lit pixels' % (total_diff, total_lit))
    print('')
    bad = [r for r in ok if r['maxDelta'] > 2]
    if bad:
        print('  cases over a 2/255 delta:')
        for r in bad[:10]:
            print('    %-28s bg %-12s +%.2f  max %d  (%d channels)'
                  % (r['key'], r['bg'], r['frac'], r['maxDelta'], r['diffChannels']))
    else:
        print('  PASS - no comparison differs by more than 2/255 on any channel.')
    # ⚠ THE TRANSPARENT CASE IS A READBACK ARTEFACT, NOT A VISUAL DIFFERENCE, and reporting it
    # beside the others would overstate the change by a factor of twenty. getImageData returns
    # UNPREMULTIPLIED colour, so a pixel at alpha 1/255 reconstructs its RGB by dividing by that
    # alpha - two halos differing by one unit of alpha in the faintest fringe read as a 255-unit
    # colour difference. The game never draws the playfield onto nothing; every real destination
    # is opaque. Scored separately, and the opaque rows are the ones that mean anything.
    opaque = [r for r in ok if r['bg'] != 'transparent']
    trans = [r for r in ok if r['bg'] == 'transparent']
    ow = max((r['maxDelta'] for r in opaque), default=-1)
    print('  OPAQUE destinations (what the game actually draws onto):')
    print('    worst single-channel delta %d / 255 over %d comparisons' % (ow, len(opaque)))
    print('  transparent destination (unpremultiplied readback, not a real case):')
    print('    worst %d / 255 over %d comparisons'
          % (max((r['maxDelta'] for r in trans), default=-1), len(trans)))

    if res.get('shotA'):
        import base64
        outdir = os.path.join(GAME, 'docs', 'proofs', 'space_laser_0916')
        os.makedirs(outdir, exist_ok=True)
        for nm, key in (('before_shipped.png', 'shotA'), ('after_baked.png', 'shotB')):
            open(os.path.join(outdir, nm), 'wb').write(
                base64.b64decode(res[key].split(',', 1)[1]))
        print('')
        print('  wrote before/after PNGs to docs/proofs/space_laser_0916/')

    if worst == 0:
        print('  PASS - byte-for-byte IDENTICAL on every case.')


if __name__ == '__main__':
    main()
