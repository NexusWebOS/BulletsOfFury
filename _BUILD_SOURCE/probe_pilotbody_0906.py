#!/usr/bin/env python3
"""probe_pilotbody_0906.py - does the pilot-select bay draw a STANDING FIGURE for all nine?

    python _BUILD_SOURCE/probe_pilotbody_0906.py

Mike, 0906: "and we do have the pilots on their own, from the cinematics we have. we use their
frames their. you can grab them from that."

He is right and the first cut of this screen missed it. `pose_<pilot>_0..5` is fifty-four cut,
background-free standing figures on the pilots_1 atlas - six poses for every one of the nine -
and the bay was falling back to a framed portrait bust captioned NO FIELD PHOTO for eight of them.

WHAT THIS ASSERTS, AND WHY IT IS NOT A KEY COUNT. CLAUDE.md: "A KEY-COUNTING PROBE IS NOT A PIXEL
PROBE" - a draw can ask for a key thirty times while something paints over it. So this wraps
`ctx.drawImage` (⚠ on the CONTEXT, never on CanvasRenderingContext2D.prototype - `ctx` carries its
own, measured, and a prototype trap on a running draw returns zero) and records the SIZE of every
blit landing inside the bay rectangle. A 256x320 source is a pose; a portrait cell is not. Then it
screenshots, so the claim is backed by a picture as well as a count.

⚠ AND IT MUST BE ABLE TO FAIL. Run with --bust and psBodyKey is stubbed to null, which is the
pre-fix screen: the same probe must then report nine busts and zero poses. A probe that has only
ever been green is not evidence.
"""
import os, sys, base64, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shoot as sh

PILOTS = ['axel', 'decker', 'maverick', 'freezer', 'juggernaut', 'yuri', 'lizzie', 'falva', 'cole']
# pilots whose cinematic poses are superseded and who must draw their OWN body art (PS_POSE_STALE)
DEDICATED = {'yuri'}
OUT = os.path.join(sh.GAME, 'docs/proofs/pilotbody_0906')

TRAP = r"""
() => {
  /* the bay rect, from drawPilot: PX=10 PY=58, BX=PX+6 BY=PY+6 BW=142, BH=PH-12 (PH=242) */
  const BX=16, BY=64, BW=142, BH=230;
  window.__bay = [];
  /* ⚠ IDENTIFY THE BLIT BY THE KEY IT ASKED FOR, NOT BY ITS SIZE. The first cut matched
     256x320 and reported nine clean poses - including Yuri, whose 256x320 was the character
     design Mike REPLACED. Every pose cell is the same size, so the size can only say "a pose",
     never WHOSE. XART.get is called immediately before the drawImage that uses it, so recording
     the key there and reading it in the wrapper names the art exactly.
     (XART.get returns a fresh canvas with no .src and no stable identity - CLAUDE.md - so the
     key is the only handle there is.) */
  window.__lastKey = null;
  if (typeof XART !== 'undefined' && !XART.__bofWrapped) {
    const og = XART.get.bind(XART);
    XART.__bofWrapped = 1;
    XART.get = function(k){ window.__lastKey = k; return og.apply(null, arguments); };
  }
  const cvs = document.querySelectorAll('canvas');
  for (const c of cvs) {
    const x = c.getContext('2d');
    if (!x || x.__bofWrapped) continue;
    const orig = x.drawImage.bind(x);
    x.__bofWrapped = 1;
    x.drawImage = function(img){
      const a = arguments;
      /* destination rect is the last four args in both the 5-arg and 9-arg forms */
      let dx,dy,dw,dh;
      if (a.length >= 9) { dx=a[5]; dy=a[6]; dw=a[7]; dh=a[8]; }
      else if (a.length >= 5) { dx=a[1]; dy=a[2]; dw=a[3]; dh=a[4]; }
      else { return orig.apply(x, a); }
      const cx = dx + dw/2, cy = dy + dh/2;
      if (cx > BX && cx < BX+BW && cy > BY && cy < BY+BH)
        window.__bay.push({key: window.__lastKey,
                           sw: img && img.width|0, sh: img && img.height|0,
                           dw: Math.round(dw), dh: Math.round(dh)});
      return orig.apply(x, a);
    };
  }
  return cvs.length;
}
"""

READY = r"""
() => {
  if (typeof XART === 'undefined') return 0;
  const P = ['axel','decker','maverick','freezer','juggernaut','yuri','lizzie','falva','cole'];
  let n = 0;
  for (const p of P) { if (XART.rdy('pose_'+p+'_0')) n++; }
  /* Yuri's own body art is a LOOSE file, not an atlas cell - wait for it too, or the run
     measures him during his decode window and reports a bust as a failure. */
  return (n + (XART.rdy('yuri_body_0') ? 1 : 0)) / (P.length + 1);
}
"""


def main():
    bust = '--bust' in sys.argv
    os.makedirs(OUT, exist_ok=True)
    port, stop = sh.serve(sh.GAME)
    from playwright.sync_api import sync_playwright
    rows, errs = [], []
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        pg = br.new_page(viewport={'width': 900, 'height': 900})
        pg.on('pageerror', lambda e: errs.append('pageerror: ' + str(e)))
        pg.on('console', lambda m: errs.append('console.' + m.type + ': ' + m.text)
              if m.type == 'error' else None)
        pg.goto('http://127.0.0.1:%d/index.html' % port)
        # ⚠ WAIT FOR THE GAME, DO NOT GUESS A TIMEOUT. The first cut slept 2500ms and then
        # threw "XART is not defined" - game.js had not finished executing, and SETUP's own
        # try/catch had swallowed the same failure one call earlier and returned {ok:false}
        # unread. A fixed sleep is the frame-count-as-a-clock mistake in another costume.
        pg.wait_for_function("() => typeof XART !== 'undefined' && typeof GS !== 'undefined'",
                             timeout=30000)
        pg.wait_for_timeout(400)
        pg.evaluate(sh.TRAP_RAF)
        if bust:
            pg.evaluate("() => { window.psBodyKey = () => null; }")
            print('!! --bust: psBodyKey stubbed to null (the pre-fix screen)\n')

        st = pg.evaluate(sh.SETUP, {'state': 'PILOT', 'pilot': 'cole'})
        if not st.get('ok'):
            print('SETUP FAILED: %s' % st.get('err'))
            br.close(); stop(); return 1
        # touch every pose key, then WAIT for the atlas - XART.rdy is false on its first call
        pg.evaluate("() => { const P=['axel','decker','maverick','freezer','juggernaut','yuri',"
                    "'lizzie','falva','cole']; for(const p of P) XART.rdy('pose_'+p+'_0');"
                    " for(let i=0;i<7;i++) XART.rdy('yuri_body_'+i); }")
        try:
            pg.wait_for_function('(' + READY + ')() >= 1', timeout=15000)
        except Exception:
            print('⚠ pose atlas did not fully decode in 15s; continuing so the count is honest')
        print('pose art ready: %.0f%%\n' % (pg.evaluate(READY) * 100))
        # ⚠ UNLOCK COLE OR HIS BAY IS NEVER MEASURED. He is the password-gated ninth slot
        # (isPilotLocked), so his panel correctly draws a '?' and no figure - which this probe
        # scored as a FAILURE on its first key-accurate run. A locked slot behaving correctly
        # is not a missing standing figure, and the probe has to know the difference.
        pg.evaluate("() => { coleUnlocked = true; }")
        pg.evaluate(TRAP)

        for i, p in enumerate(PILOTS):
            # ⚠ THE SELECTED PILOT IS `pilotIndex`, AND `pilotRot` OVERRIDES IT. drawPilot reads
            # showIdx = (pilotRot>0.5) ? pilotFrom : pilotIndex, so a probe that sets only the
            # index can still be photographing the pilot it is rotating AWAY from. The first
            # run set a `pilotIdx` that nothing reads and drew pose_axel_0 nine times - which
            # the size-based check had scored 9/9. Assert the switch took instead of assuming.
            got = pg.evaluate("(i) => { pilotIndex = i; pilotRot = 0; pilotFrom = i;"
                              " pilotPending = null; pilotSlide = 0;"
                              " if (typeof run !== 'undefined' && PILOTS[i]) run.pilot = PILOTS[i].key;"
                              " return PILOTS[pilotIndex] && PILOTS[pilotIndex].key; }", i)
            if got != p:
                errs.append('pilot switch: asked %s, screen shows %s' % (p, got))
            pg.evaluate("() => { window.__bay = []; }")
            err = pg.evaluate(sh.STEP, 6)
            if err:
                errs.append('step(%s): %s' % (p, err))
            bay = pg.evaluate("() => window.__bay")
            want = p + '_body_0' if p in DEDICATED else 'pose_' + p
            body = [b for b in bay if b.get('key') and b['key'].startswith(want)]
            other = [b for b in bay if b not in body]
            rows.append((p, want, body[0] if body else None, other[0] if other else None))
            png = pg.evaluate("() => { const g=document.querySelector('#screen-area canvas')"
                              "||document.querySelector('canvas'); return g?g.toDataURL('image/png'):null; }")
            if png:
                open(os.path.join(OUT, '%s.png' % p), 'wb').write(
                    base64.b64decode(png.split(',', 1)[1]))
        # ---- THE SPIN. Mike asked for the hulls to turn, and a still frame cannot show it.
        # Step a real stretch of frames on one pilot and collect the distinct roll frames the
        # panel actually asked XART for. A count of ONE means a static hull wearing the word
        # 'spin'; eight means the full 360 the barrel-roll reel carries.
        pg.evaluate("(i) => { pilotIndex = i; pilotRot = 0; pilotFrom = i; }", 2)
        pg.evaluate("() => { window.__spin = []; const og = XART.get.bind(XART);"
                    " if (!XART.__spinWrapped) { XART.__spinWrapped = 1;"
                    "   XART.get = function(k){ if (/^ship_[a-z]+_(br|pv)/.test(k)) window.__spin.push(k);"
                    "     return og.apply(null, arguments); }; } }")
        for _ in range(6):
            pg.evaluate(sh.STEP, 40)
            pg.wait_for_timeout(40)
        spin = pg.evaluate("() => window.__spin")
        seen = sorted(set(spin))
        br.close()
    stop()

    print('%-11s  %-16s  %-24s  %s' % ('pilot', 'wanted', 'key actually drawn', 'source -> drawn'))
    print('-' * 80)
    ok = 0
    for p, want, hit, other in rows:
        got = hit or other
        k = (got.get('key') or '(no key)') if got else '(nothing drawn)'
        sz = ('%dx%d -> %dx%d' % (got['sw'], got['sh'], got['dw'], got['dh'])) if got else '-'
        print('%-11s  %-16s  %-24s  %s%s' % (p, want + '*', k, sz, '' if hit else '   <-- WRONG'))
        if hit:
            ok += 1
    print(chr(10) + '%d/9 pilots draw the standing figure they should' % ok)
    print(chr(10) + 'the horizontal spin, over 240 frames on one pilot:')
    print('   %d distinct hull frames asked for: %s' % (len(seen), ', '.join(seen) or '(none)'))
    if len(seen) < 8:
        print('   !! fewer than the eight the barrel-roll reel carries - the hull is not turning')
    print('shots -> docs/proofs/pilotbody_0906/')
    if errs:
        print('\n%d console/page errors:' % len(errs))
        for e in errs[:8]:
            print('   ' + e)
    else:
        print('0 console errors, 0 page errors')
    return 0 if (ok == 9 and not errs) else 1


if __name__ == '__main__':
    sys.exit(main())
