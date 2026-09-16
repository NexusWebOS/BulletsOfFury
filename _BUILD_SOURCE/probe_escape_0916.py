#!/usr/bin/env python3
"""probe_escape_0916.py - S4-16: the Stage-4 giant strike's escape arrows, and the beat they flash on.

`8ed5f1a8` shipped these UNVERIFIED and said so in its own commit message; docs/RESUME_0916.md made
verifying them the first item. Mike: "Authored left/right escape arrows: flipped pair, flashing with
synchronized warning sounds for the giant strike."

Driven in real Chromium on the Furious Stage-4 Sovereign, forced into `stage4GiantStrikeStart`:

  * the arrows draw at all - the pair is ONE plate, so the left one is drawn with a NEGATIVE x
    scale. The blit is identified by the source plate's own dimensions and by the live CTM, read
    off the game context's OWN drawImage (a prototype trap records nothing - CLAUDE.md 0905h).
  * they sit IN the safe lanes the strike leaves open (17% of the camera at each edge) and point
    outward, at the player's altitude.
  * they FLASH rather than hold, seven times across the charge - the count L23_WARN_ARROWS.
  * ⚠ and the flash is claimed to be "synchronized" with the warning sound, so the sound is counted
    too: l23WarnSound is supposed to fire ONE alert, on the first arrow.

The sound is where this drop was broken. `l23WarnSound(B)` reads `B.t / B.warm`, and the giant
strike's object never sets `warm` - so k is NaN, n is NaN, `n === B._arrowN` is false for ever
(NaN equals nothing, itself included) and the `n>0` guard that limits it to one alert is false too.
Measured before the fix: the alert is called once per FRAME for the whole five-second charge.
"""
import os, sys, base64
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shoot

OUT = 'docs/proofs/escape_0916'

# the game context's own drawImage, with the live transform, plus every warning-sound call
TRAP = r"""() => {
  if (window.__etrap) return true;
  window.__etrap = 1;
  window.__dr = []; window.__rec = 0; window.__snd = [];
  const c = ctx, od = c.drawImage;
  c.drawImage = function (im) {
    try {
      if (window.__rec && im) {
        const a = arguments, W = im.width || im.naturalWidth, H = im.height || im.naturalHeight;
        let lx = 0, ly = 0, lw = W, lh = H;
        if (a.length >= 5) { lx = a[1]; ly = a[2]; lw = a[3]; lh = a[4]; } else if (a.length >= 3) { lx = a[1]; ly = a[2]; }
        const m = c.getTransform(), cx = lx + lw / 2, cy = ly + lh / 2;
        window.__dr.push({W: W, H: H, x: m.a * cx + m.c * cy + m.e, y: m.b * cx + m.d * cy + m.f,
                          sx: m.a, w: lw * Math.abs(m.a), alpha: c.globalAlpha});
      }
    } catch (e) {}
    return od.apply(this, arguments);
  };
  for (const k of ['alertLockon', 'dangerAlert', 'lockAlert', 'bossWeaponCharge']) {
    if (Audio.SFX && Audio.SFX[k]) {
      const o = Audio.SFX[k];
      Audio.SFX[k] = function () { try { window.__snd.push(k); } catch (e) {} return o.apply(this, arguments); };
    }
  }
  return true;
}"""

RUN = r"""async ([frames]) => {
  const B = window.BOSSMODE, b = B.boss || boss;
  const A = XART.rdy('warn_escape_arrow_0916') ? XART.get('warn_escape_arrow_0916') : null;
  if (!A) return {err: 'the arrow plate never decoded'};
  const isArrow = r => r.W === A.width && r.H === A.height;
  window.__snd = [];
  const started = stage4GiantStrikeStart(b);
  const out = [], S = b._s4war;
  let shot = null;
  for (let i = 0; i < frames; i++) {
    window.__dr = []; window.__rec = 1;
    await new Promise(r => requestAnimationFrame(r));
    window.__rec = 0;
    const G = S.giantStrike;
    const ar = window.__dr.filter(isArrow);
    out.push({t: G ? +G.t.toFixed(3) : -1, arrows: ar.length,
              arrowN: G ? (Number.isNaN(G._arrowN) ? 'NaN' : G._arrowN) : null,
              released: G ? !!G.released : null,
              mirrored: ar.filter(r => r.sx < 0).length,
              xs: ar.map(r => Math.round(r.x)), alpha: ar.map(r => +r.alpha.toFixed(2)),
              sounds: window.__snd.length});
    /* ⚠ THE PROOF FRAME MUST BE TAKEN INSIDE A LIT FRAME. Read straight after the rAF callback
       that drew it, before the next frame clears - the first cut screenshotted after the whole
       run and caught a picture with no arrows in it at all, which reads exactly like "they never
       drew" on a build where they drew 234 times. */
    if (!shot && ar.length && G && G.t > 3.0) {
      try { const c = document.getElementById('screen'); if (c) shot = c.toDataURL('image/png'); } catch (e) {}
    }
    if (!G) break;
  }
  const R = stage4GiantStrikeBounds(), m = ctx.getTransform();
  return {started: started, frames: out, sounds: window.__snd.slice(), shot: shot,
          plate: {W: A.width, H: A.height},
          bounds: {viewLeft: R.viewLeft, viewRight: R.viewRight, safe: R.safe, scale: m.a,
                   camX: (B.snapshot && B.snapshot().camX) || 0},
          arrowsConst: L23_WARN_ARROWS, charge: S4_GIANT_STRIKE.charge};
}"""

START = r"""async ([stage, pilot]) => {
  const B = window.BOSSMODE;
  diffKey = 'furious';
  B.start(stage, 'boss', pilot, false);
  for (let i = 0; i < 1200 && !(B.snapshot().bossActive && B.player && !B.player.dead); i++)
    await new Promise(r => requestAnimationFrame(r));
  diffKey = 'furious';
  if (B.player) { B.player.invuln = 1e9; }
  playerHit = function () {};
  const b = B.boss || boss;
  return {boss: !!b, war: !!(b && b._s4war), mini: !!(b && b._s4war && b._s4war.mini), diff: diffKey};
}"""


def main():
    os.makedirs(OUT, exist_ok=True)
    from playwright.sync_api import sync_playwright
    port, stop = shoot.serve(shoot.GAME)
    errs, fails, n_ok = [], [], [0]

    def ok(c, m):
        if c:
            n_ok[0] += 1; print('  ok  ', m)
        else:
            fails.append(m); print('  FAIL', m)

    with sync_playwright() as p:
        b = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
        pg = b.new_page(viewport={'width': 1100, 'height': 1000}, device_scale_factor=1)
        pg.on('pageerror', lambda e: errs.append('pageerror: ' + str(e)[:200]))
        pg.on('console', lambda m: errs.append('console: ' + m.text[:200]) if m.type == 'error' else None)
        pg.goto('http://127.0.0.1:%d/index.html?bossmode=1' % port, wait_until='load', timeout=60000)
        pg.wait_for_function("() => window.BOSSMODE && window.BOSSMODE.ready", timeout=90000)

        S = pg.evaluate(START, [4, 'cole'])
        ok(S.get('boss') and S.get('war'), 'the Stage-4 Sovereign is up with its warfare rig (%s)' % S)
        ok(S.get('diff') == 'furious', 'on furious, which is the only difficulty that fields the strike')

        # XART.rdy is false on its FIRST call - that call starts the load. Touch, then wait.
        for _ in range(40):
            if pg.evaluate("() => XART.rdy('warn_escape_arrow_0916')"):
                break
            pg.wait_for_timeout(80)
        ok(pg.evaluate("() => XART.rdy('warn_escape_arrow_0916')"), 'the authored escape arrow plate decoded')

        pg.evaluate(TRAP)
        R = pg.evaluate(RUN, [330])
        if R.get('err'):
            print('  FAIL', R['err']); fails.append(R['err'])
        else:
            F = [f for f in R['frames'] if not f['released'] and f['t'] >= 0]
            drew = [f for f in F if f['arrows']]
            ok(R['started'], 'the giant strike started')
            ok(len(drew) > 0, 'the escape arrows DRAW during the charge (%d of %d charge frames)' % (len(drew), len(F)))
            ok(drew and all(f['arrows'] == 2 for f in drew), 'exactly two arrows on every frame they are lit')
            ok(drew and all(f['mirrored'] == 1 for f in drew), 'one of the pair is drawn mirrored - it is one plate, flipped')

            # they belong in the safe lanes, one each side
            B_ = R['bounds']; sc = B_['scale'] or 2
            # ⚠ THE BLIT IS IN CANVAS SPACE AND THE LANES ARE IN WORLD SPACE. stage4GiantStrikeDraw
            # runs inside drawWorld's translate(-camX), so the recorded x is (world - camX) * scale.
            # The first cut of this probe compared the two directly and reported the RIGHT arrow
            # 59px inside the danger zone on correct code - exactly the world-vs-screen fault
            # CLAUDE.md records for the launch seam, the outbound routes, the level-1 ship,
            # probe_seam and bulletsofdebug's FOV cone. Add the camera back.
            cam = B_['camX'] or 0
            xs = [x / sc + cam for f in drew for x in f['xs']]
            left = [x for x in xs if x < (B_['viewLeft'] + B_['viewRight']) / 2]
            right = [x for x in xs if x >= (B_['viewLeft'] + B_['viewRight']) / 2]
            ok(left and right, 'one arrow each side of the strike (%d left, %d right)' % (len(left), len(right)))
            ok(left and max(left) <= B_['viewLeft'] + B_['safe'] + 2,
               'the left arrow sits inside the left safe lane (worst %.1f of %.1f)' % (max(left) if left else -1, B_['viewLeft'] + B_['safe']))
            ok(right and min(right) >= B_['viewRight'] - B_['safe'] - 2,
               'the right arrow sits inside the right safe lane (best %.1f of %.1f)' % (min(right) if right else -1, B_['viewRight'] - B_['safe']))

            # a FLASH, not a hold: the lit frames come in bursts, one per revealed arrow
            lit = [bool(f['arrows']) for f in F]
            bursts = sum(1 for i in range(1, len(lit)) if lit[i] and not lit[i - 1]) + (1 if lit and lit[0] else 0)
            ok(any(not x for x in lit), 'they flash rather than hold (%d of %d charge frames dark)' % (sum(1 for x in lit if not x), len(lit)))
            ok(abs(bursts - R['arrowsConst']) <= 1,
               'one flash per revealed arrow: %d bursts against L23_WARN_ARROWS=%d' % (bursts, R['arrowsConst']))

            # ⚠ THE SOUND. l23WarnSound is meant to fire ONE alert, on the first arrow.
            nan = [f for f in F if f['arrowN'] == 'NaN']
            ok(not nan, "the warning's arrow index is a number, not NaN (%d frames NaN)" % len(nan))
            alerts = [s for s in R['sounds'] if s in ('alertLockon', 'dangerAlert', 'lockAlert')]
            ok(len(alerts) <= R['arrowsConst'],
               'the warning alert fires on its own beat, not every frame (%d calls across the charge)' % len(alerts))

        d = R.get('shot')
        ok(bool(d), 'a proof frame was captured inside a lit frame')
        if d:
            open(os.path.join(OUT, 'strike_arrows_lit.png'), 'wb').write(base64.b64decode(d.split(',', 1)[1]))
        print('    sound calls across the charge:', R.get('sounds'))

        ok(not errs, 'no page or console errors (%d)' % len(errs))
        for e in errs[:6]:
            print('    !', e)
        b.close(); stop()

    print('\n%d ok / %d fail' % (n_ok[0], len(fails)))
    for f in fails:
        print('  FAIL', f)
    sys.exit(1 if fails else 0)


if __name__ == '__main__':
    main()
