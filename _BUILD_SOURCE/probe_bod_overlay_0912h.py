#!/usr/bin/env python3
"""
probe_bod_overlay_0912h.py - DOES THE OVERLAY LAND ON THE UNIT?

    python3 _BUILD_SOURCE/probe_bod_overlay_0912h.py --out /tmp/bodov

Bullets of Debug draws its FOV cone, hull box and anchor marks on its OWN canvas, over an iframe
holding the real game. So it has to map world -> guest canvas -> overlay canvas, and CLAUDE.md
records that class of bug five separate times: the launch seam (0810a), the outbound routes (0810c),
the level-1 ship (0810e), a probe that recomputed it rather than recording it (probe_seam), and this
editor's FOV cone, which sat ~190px right of the ship on a wide stage while every number it printed
looked correct.

⚠ THIS PROBE DOES NOT RE-DERIVE THE MAPPING. It reads two recorded facts and compares them:

    the ENGINE's side  -> BOFDEBUG.xform, the live CTM captured off `ctx.drawImage` during a real
                          frame while `_inWorldXform` is true. That is the matrix drawWorld
                          installed, not a reconstruction of it.
    the EDITOR's side  -> BOD.S._mark, the point drawOverlay actually drew the cone apex at.

Both are converted to PAGE pixels through `getBoundingClientRect`, so the comparison is in a space
neither side computed. A probe that rebuilds `(x-camX)*vz` to check code that computes
`(x-camX)*vz` asserts its own arithmetic and passes on a broken frame.

⚠ AND IT IS RUN BUSTED FIRST. `BOD.S.bustCam` puts the overlay back to reading world coords as
screen coords; the alignment assertion must FAIL there, or it is not measuring anything.

Stage 6 is the subject deliberately: world 680 against a 565px visible width, so camX has ~115px of
travel AND the zoom is off 1.0 - the two terms that cancel out to nothing on a narrow stage at fit.
"""
import os, sys, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shoot

TOL = 6.0          # px of page space. The overlay is integer-placed over a scaled iframe.
BUST_MIN = 25.0    # a busted mapping must be off by MORE than this, or the test proves nothing.


def measure(pg, label):
    """Return (engine_page_xy, overlay_page_xy, detail) for the live unit, or None."""
    return pg.evaluate("""() => {
        const f=document.querySelector('#host');
        const W=f.contentWindow, D=W.BOFDEBUG, B=window.BOD;
        const u=B.unit(); if(!u) return {err:'no unit'};
        /* ⚠ THIS FUNCTION MUTATES NOTHING. `S._mark` is what the overlay drew on its LAST frame, so
           moving the unit here and then comparing the engine's mapping of its NEW position against
           that mark measures the unit's own travel, not the mapping - it reported +71px across and
           +134px down on a correct build. Seating happens in seat(), a frame earlier. */
        const m=D.xform.get(u.x, u.y); if(!m) return {err:'no matrix captured'};
        const mk=B.S._mark; if(!mk) return {err:'overlay drew no mark'};

        /* the guest canvas, as it sits on the page */
        const gc=W.document.querySelector('#screen');
        if(!gc) return {err:'no guest canvas'};
        const gr=gc.getBoundingClientRect(), fr=f.getBoundingClientRect();
        /* CTM is in BACKING-STORE px (SS=2), so normalise by canvas.width before scaling to CSS */
        const ex = fr.left + gr.left + (m.x/m.cw)*gr.width;
        const ey = fr.top  + gr.top  + (m.y/m.ch)*gr.height;

        const ov=document.querySelector('#overlay').getBoundingClientRect();
        const ax = ov.left + mk.x, ay = ov.top + mk.y;

        return {eng:[ex,ey], ov:[ax,ay], dx:ax-ex, dy:ay-ey,
                unit:{x:Math.round(u.x), y:Math.round(u.y), type:u.type},
                cam:Math.round(mk.cam*10)/10, vz:Math.round(mk.vz*1000)/1000,
                ctm:{a:m.a,d:m.d,e:Math.round(m.e*10)/10,f:Math.round(m.f*10)/10, cw:m.cw, ch:m.ch}};
    }""")


def seat(pg):
    """Pin the subject still and on screen, a frame BEFORE it is measured.

    s6dart is a fast mover and the lab runs real time, so across four measurements it flew off the
    bottom and was culled - which read as 'the cone stopped painting' and 'FIRE fired nothing'
    rather than as a unit that was simply gone. This probe is about the MAPPING, so the subject is
    held still; the engine still maps and draws it exactly as it would any other frame.
    """
    return pg.evaluate("""() => { const W=document.querySelector('#host').contentWindow;
        const u=window.BOD.unit(); if(!u) return false;
        u.vx=0; u.vy=0; u._dyingT=null; u.x=Math.round(W.player.x-60); u.y=170;
        W.BOFDEBUG.xform.clear(); return true; }""")


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--out', default='/tmp/bodov'); a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    from playwright.sync_api import sync_playwright
    port, stop = shoot.serve(shoot.GAME); errs = []; fails = []; n_ok = [0]
    def ok(c, m):
        if c: n_ok[0] += 1; print('  ok  ', m)
        else: fails.append(m); print('  FAIL', m)

    with sync_playwright() as p:
        b = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
        pg = b.new_page(viewport={'width': 1600, 'height': 1000})
        pg.on('pageerror', lambda e: errs.append('pageerror: ' + str(e)[:220]))
        pg.on('console', lambda m: errs.append('console.error: ' + m.text[:200]) if m.type == 'error' else None)

        pg.goto(f'http://127.0.0.1:{port}/bulletsofdebug.html', wait_until='load', timeout=60000)
        pg.wait_for_function("() => window.BOD && window.BOD.api() && window.BOD.api().ready", timeout=90000)
        ok(True, 'the editor boots and reaches the engine')

        # the matrix trap has to be armed before the frame we measure
        ok(pg.evaluate("() => document.querySelector('#host').contentWindow.BOFDEBUG.xform.arm()"),
           'the world-matrix trap arms on ctx itself (not the prototype - 0905h)')

        # STAGE 6: wide world, so camX has travel AND the zoom is off 1.0
        pg.evaluate("() => { const s=document.querySelector('#t-stage'); s.value='6'; "
                    "s.dispatchEvent(new Event('change',{bubbles:true})); }")
        pg.evaluate("() => window.BOD.labOpen()")
        pg.wait_for_function("() => { const d=window.BOD.api(); return d && d.snapshot().lab; }", timeout=60000)

        # push the player right so the camera is genuinely scrolled - camX 0 proves nothing
        pg.evaluate("""() => { const W=document.querySelector('#host').contentWindow;
            W.player.x = W.BOFDEBUG.snapshot().worldW - 40; }""")
        pg.wait_for_timeout(700)
        snap = pg.evaluate("() => window.BOD.api().snapshot()")
        ok(snap['camX'] > 40, 'the camera is genuinely scrolled before anything is measured (camX %s of world %s)'
           % (round(snap['camX'], 1), snap['worldW']))
        # ⚠ MEASURED, NOT ASSUMED: every stage is a true 680 world at zoom 1.00 today (all nine
        # checked), so the ZOOM term is dormant and camX is the only live one. game.js's own comment
        # at viewZoom() still says stages 1/2/3/7/8 are 800 and is stale. The zoom half is forced
        # below instead of being asserted live.
        ok(abs(snap['vz'] - 1.0) < 0.01,
           'the view zoom is 1.00 game-wide today, so camX is the live term (vz %s, world %s)'
           % (round(snap['vz'], 3), snap['worldW']))

        # ⚠ SPAWN THROUGH THE EDITOR'S OWN PATH, NOT BY ASSIGNING S.unit. `S.unit` is a FLAG
        # (`unit()` re-fetches the live object every time - `enemies` is reassigned every frame by
        # the cull), and the inspector is rendered by pick()/spawn(), not by the assignment. Writing
        # the flag by hand left #i-shape absent and the FIRE default unreadable.
        pg.keyboard.press('l'); pg.wait_for_timeout(250)
        pg.fill('#roster-filter', 's6dart'); pg.wait_for_timeout(250)
        pg.evaluate("""() => { const el=[...document.querySelectorAll('#roster .ri')]
            .find(e=>e.textContent.trim().startsWith('s6dart')); if(el) el.click(); }""")
        pg.wait_for_timeout(250)
        pg.evaluate("() => window.BOD.spawn()")
        pg.wait_for_function("() => window.BOD.unit()", timeout=30000)
        ok(pg.evaluate("() => !!document.querySelector('#i-shape')"),
           'the unit spawns through the editor path and the inspector renders')
        pg.wait_for_timeout(600)

        # ---- BUSTED ARM FIRST: the check must be able to fail ----
        pg.evaluate("() => { window.BOD.S.bustCam=true; }")
        ok(seat(pg), 'the subject is pinned still and on screen before measuring')
        pg.wait_for_timeout(400)
        bust = measure(pg, 'bust')
        if bust.get('err'):
            ok(False, 'busted measurement failed to run: ' + bust['err'])
        else:
            off = max(abs(bust['dx']), abs(bust['dy']))
            ok(off > BUST_MIN,
               'BUSTED: ignoring the camera puts the overlay %.1fpx off the unit - the check can fail'
               % off)
            pg.screenshot(path=os.path.join(a.out, '01_busted.png'))

        # ---- and now the real mapping ----
        pg.evaluate("() => { window.BOD.S.bustCam=false; }")
        seat(pg); pg.wait_for_timeout(400)
        m = measure(pg, 'live')
        if m.get('err'):
            ok(False, 'live measurement failed to run: ' + m['err'])
        else:
            print('       engine %s  overlay %s  ctm %s' %
                  ([round(v, 1) for v in m['eng']], [round(v, 1) for v in m['ov']], m['ctm']))
            ok(abs(m['dx']) <= TOL,
               'the overlay lands on the unit horizontally: %.1fpx (cam %s, vz %s)'
               % (m['dx'], m['cam'], m['vz']))
            ok(abs(m['dy']) <= TOL,
               'and vertically, which is the half that is NOT y*vz: %.1fpx' % m['dy'])
            pg.screenshot(path=os.path.join(a.out, '02_aligned.png'))

        # ---- THE ZOOM HALF, FORCED. It is dormant at 680/680, so it cannot be verified from
        # ---- gameplay - but VIEW_PLATE_W is "the whole dial" and a plate-width change would make
        # ---- the overlay wrong everywhere. `viewZoom` is a column-0 function, so it IS a window
        # ---- property and can be forced; the engine's CTM and the overlay both then see 0.85.
        pg.evaluate("() => { const W=document.querySelector('#host').contentWindow; "
                    "W.__vz0=W.viewZoom; W.viewZoom=function(){ return 0.85; }; "
                    "W.BOFDEBUG.xform.clear(); }")
        seat(pg); pg.wait_for_timeout(500)
        z = measure(pg, 'zoomed')
        if z.get('err'):
            ok(False, 'forced-zoom measurement failed to run: ' + z['err'])
        else:
            ok(abs(z['vz'] - 0.85) < 0.01, 'the forced zoom reaches both sides (vz %s)' % z['vz'])
            ok(abs(z['dx']) <= TOL and abs(z['dy']) <= TOL,
               'and the overlay still lands on the unit under a zoom: %.1f, %.1fpx - the bottom-edge '
               'anchor is carried, not y*vz' % (z['dx'], z['dy']))
            pg.screenshot(path=os.path.join(a.out, '02b_zoomed.png'))
        pg.evaluate("() => { const W=document.querySelector('#host').contentWindow; "
                    "if(W.__vz0) W.viewZoom=W.__vz0; W.BOFDEBUG.xform.clear(); }")
        seat(pg); pg.wait_for_timeout(400)

        # the cone must also still be INK on the canvas - a correct mark nobody can see is no use
        ink = pg.evaluate("""() => { const c=document.querySelector('#overlay');
            const u=window.BOD.unit();
            if(!u) return {err:'the unit is gone - nothing to draw'};
            if(!c.width||c.width<2) return {err:'overlay canvas is '+c.width+'x'+c.height};
            const d=c.getContext('2d').getImageData(0,0,c.width,c.height).data;
            let n=0; for(let i=3;i<d.length;i+=16) if(d[i]>8) n++;
            return {n:n, w:c.width, h:c.height}; }""")
        ok(not ink.get('err') and ink.get('n', 0) > 300,
           'and the cone is still painted where it landed (%s)'
           % (ink.get('err') or ('%d px on a %dx%d overlay' % (ink['n'], ink['w'], ink['h']))))

        # FIRE ONCE must demonstrate a PATTERN on the first click, not one round
        fired = pg.evaluate("""() => { const d=window.BOD.api(); const n0=d.eBullets.length;
            const sel=document.querySelector('#i-shape');
            if(!sel) return {shape:'(no inspector)', added:0};
            if(!window.BOD.unit()) return {shape:sel.value, added:0, err:'unit gone'};
            window.BOD.fireOnce(); return {shape:sel.value, added:d.eBullets.length-n0}; }""")
        ok(fired['shape'] == 'fan' and fired['added'] > 1,
           'the FIRE default demonstrates a pattern on the first click: %s of %d rounds'
           % (fired['shape'], fired['added']))

        pg.wait_for_timeout(400)
        pg.screenshot(path=os.path.join(a.out, '03_final.png'))
        b.close()
    stop()
    print('\n%d ok / %d fail' % (n_ok[0], len(fails)))
    for f in fails: print('  FAIL', f)
    if errs:
        print('page errors (%d):' % len(errs))
        for e in errs[:8]: print('   ', e)
    sys.exit(1 if fails or errs else 0)


if __name__ == '__main__':
    main()
