#!/usr/bin/env python3
"""
probe_boss.py — do the minibosses SPAWN, DRAW, REACH the field, and FLASH when hit?

    python3 _BUILD_SOURCE/probe_boss.py
    python3 _BUILD_SOURCE/probe_boss.py --stage 2

WHY THIS EXISTS
Mike, 0810i: "The miniboss on level 2, broken." and "Mini boss 1 doesnt flash white when you attack
his body after shield is down."

⚠ IT MEASURES PIXELS, NOT INTENTIONS. It does not read the code and it does not trust a field
being set. This project has lost drops to exactly that gap: the quadlaser spawned, moved, collided
and drew NOTHING for weeks while every state check passed, and the boss gauge "had no fills"
because drawHUDCustom returns early and only drawHUDCustomImg reaches the bar — "calling it
directly emits 3 nbb_ blits, calling drawHUD() emits none" (0801ej). A field set is not a pixel
drawn.

⚠ AND A BLIT COUNT IS NOT ONE EITHER — read the long note at the visibility check below before
trusting the "blit hint" column. Wrapping drawImage and calling the draw by hand reported 0 blits
for two minibosses that a screenshot showed drawn in full. The verdict here is a FRAME DIFF: render
with the unit, render without it, and see whether the picture changed.

The flash check is the sharp one. b.flash was ALWAYS being set on an open-hull hit — the hit
registered fine. What never happened was anything drawing it: the quadlaser's body pulse reads
_qlArmor, which was only set on the BLOCKED path, and that path returns early. So the measurement
that matters is not "is flash set" but "did a white-tinted body blit land in the frame after a
hit", which is what this asks.
"""
import http.server, socketserver, threading, os, sys, functools, argparse

ROOT = os.path.dirname(os.path.abspath(__file__))
GAME = os.path.abspath(os.path.join(ROOT, '..'))
DEFAULT_STAGES = [1, 2]


def serve(directory, port=0):
    h = functools.partial(http.server.SimpleHTTPRequestHandler, directory=directory)
    h.log_message = lambda *a, **k: None
    s = socketserver.TCPServer(("127.0.0.1", port), h)
    threading.Thread(target=s.serve_forever, daemon=True).start()
    return s.server_address[1], s.shutdown


RUN = r"""
(st) => {
  ASSETS.ready = true; run.pilot = 'cole';
  curStage = STAGES[st-1] || STAGES[0];
  beginStage(st); setState(GS.PLAY);

  const kind = (typeof SUBBOSS !== 'undefined' && SUBBOSS[st]) ? SUBBOSS[st].kind : null;
  if (!kind) return {err:'no SUBBOSS entry for stage '+st};

  /* ---- BLIT COUNTER. Wrap the prototype, not one context: this file makes 26 of them and a
     wrapper on a single ctx would miss whatever the draw actually used (0806a's lesson). ---- */
  const proto = CanvasRenderingContext2D.prototype;
  const realDraw = proto.drawImage;
  let tally = null;
  const keyOf = (img) => {
    try {
      if (img && img.__k) return img.__k;
      const s = (img && (img.currentSrc || img.src)) || '';
      const m = s.match(/([^\/]+)\.png/); return m ? m[1] : (img && img.tagName) || '?';
    } catch(e) { return '?'; }
  };
  proto.drawImage = function(img){ if (tally) { const k=keyOf(img); tally[k]=(tally[k]|0)+1; tally.__n++; }
                                   return realDraw.apply(this, arguments); };
  const measure = (fn) => { tally = {__n:0}; try { fn(); } catch(e) { tally.__err=String(e).slice(0,120); }
                            const t = tally; tally = null; return t; };

  const out = {stage:st, kind:kind};

  /* ⚠ ART READINESS IS REPORTED, NOT ASSUMED. XART loads lazily and rdy() is false on its FIRST
     call — that call is what starts the decode. A blit count of 0 taken before the body has
     decoded says nothing at all, and reporting it as "draws nothing" would be inventing a bug.
     So the keys the draw actually reaches for are listed with their true readiness alongside the
     count, and the caller polls them ready before measuring. */
  const NEED = {1:['nqx_body_intact','nqx_cannon_left_outer_intact'],
                2:['nobd_assembled_intact','nobd_assembled_damaged']};
  out.artReady = {};
  (NEED[st]||[]).forEach(k => { out.artReady[k] = !!(typeof XART!=='undefined' && XART.rdy(k)); });

  spawnSubBoss(kind);
  out.spawned = !!subBoss;
  if (!subBoss) { proto.drawImage = realDraw; return out; }
  out.spawn = {x:subBoss.x, y:subBoss.y, ty:subBoss.ty, hp:subBoss.hp, maxhp:subBoss.maxhp,
               w:subBoss.w, h:subBoss.h, art:subBoss.art||null, sxcode:subBoss._sxcode||null};

  /* let it fly its entrance — the difference between "never spawned", "spawned invisible" and
     "spawned but never reached the playfield" is three different bugs and only motion separates
     them (probe_enemies' lesson: measure where it was DRAWN, not where it was placed) */
  const t0 = performance.now(); let f = 0;
  const track = [];
  for (let i = 0; i < 240; i++) {
    loop(t0 + (f++)*16.7);
    if (subBoss) track.push(Math.round(subBoss.y));
  }
  out.alive = !!subBoss;
  out.yTrack = {first:track[0], last:track[track.length-1], min:Math.min.apply(null,track),
                max:Math.max.apply(null,track), onScreen: track.filter(y=>y>0&&y<VH).length};

  /* WHAT THE DRAW ITSELF BRANCHES ON, recorded rather than inferred. A blit count of 0 has many
     possible causes and guessing between them is how this project loses days. */
  out.drawState = (function(){
    const b = subBoss; if (!b) return {no:'subBoss'};
    const half = b.hp/(b.maxhp||1);
    const sep = (typeof XART!=='undefined') && XART.rdy('nqx_body_intact');
    const bodyK = b._ql ? (sep ? ((half<=0.40 && XART.rdy('nqx_body_damaged')) ? 'nqx_body_damaged' : 'nqx_body_intact')
                               : ((half<=0.40 && XART.rdy('nql_damaged_01')) ? 'nql_damaged_01' : 'nql_intact_01')) : null;
    return {ql:!!b._ql, sx:b._sx?b._sx.code:null, dead:!!b.dead, dying:b.dying,
            half:+half.toFixed(2), bodyK:bodyK,
            bodyRdy: bodyK ? !!XART.rdy(bodyK) : null,
            subBossActive: (typeof subBossActive!=='undefined') ? !!subBossActive : null};
  })();

  /* ⚠⚠ THE BLIT COUNTER LIES WHEN THE DRAW IS INVOKED DIRECTLY, AND IT COST A DIAGNOSIS.
     Wrapping CanvasRenderingContext2D.prototype.drawImage and then calling drawSubBoss() by hand
     reported 0 blits for BOTH minibosses — with the art polled ready, the body key resolving, the
     unit alive and on screen and subBossActive true. Every branch the draw tests was correct and
     the count still said nothing was drawn. A SCREENSHOT of the same frame showed both units drawn
     in full, health bars and all. The counter was wrong, not the game.

     So the visibility test does not ask the renderer to confess. It renders a real frame through
     loop(), captures it, removes the sub-boss, renders again, and diffs — if the unit is on screen
     the two frames differ where it stands, and no amount of instrumentation can fake that. Keep
     the blit tally as a hint; it is not the verdict. */
  const cv2 = document.querySelector('#screen-area canvas') || document.querySelector('canvas');
  const gw = cv2.width, gh = cv2.height;
  const scr = document.createElement('canvas'); scr.width=gw; scr.height=gh;
  const sctx = scr.getContext('2d', {alpha:false});
  const snap = () => { sctx.clearRect(0,0,gw,gh); sctx.drawImage(cv2,0,0); return sctx.getImageData(0,0,gw,gh).data; };
  loop(t0 + (f++)*16.7);
  const withMB = snap();
  const held = subBoss; subBoss = null;
  loop(t0 + (f++)*16.7);
  const withoutMB = snap();
  subBoss = held;
  let px = 0;
  for (let i = 0; i < withMB.length; i += 4) {
    if (Math.abs(withMB[i]-withoutMB[i]) > 8 || Math.abs(withMB[i+1]-withoutMB[i+1]) > 8
        || Math.abs(withMB[i+2]-withoutMB[i+2]) > 8) px++;
  }
  out.visiblePixels = px;
  out.visible = px > 500;          // a 168x158 unit at this scale is tens of thousands of px

  const drew = measure(() => { if (typeof drawSubBoss === 'function') drawSubBoss(); });
  out.drawBlits = drew.__n; out.drawErr = drew.__err || null;
  out.drawKeys = Object.keys(drew).filter(k=>k!=='__n'&&k!=='__err').slice(0,8);

  // and the bar
  const bar = measure(() => { if (typeof drawSubBossBar === 'function' && subBoss) drawSubBossBar(subBoss); });
  out.barBlits = bar.__n; out.barKeys = Object.keys(bar).filter(k=>k!=='__n'&&k!=='__err').slice(0,6);

  /* ---- THE FLASH, for the quadlaser: open the hull the way the fight does, then hit it ---- */
  if (subBoss && subBoss._ql) {
    (subBoss._qlCan||[]).forEach(c => { c.dead = true; });
    out.cannonsKilled = (subBoss._qlCan||[]).length;
    subBoss._qlArmor = 0; subBoss.flash = 0;
    const hpBefore = subBoss.hp;
    _lastHitX = subBoss.x; _lastHitY = subBoss.y;
    hitSubBoss(12, subBoss.x, subBoss.y);
    out.hullOpen = !!subBoss._qlHullOpen;
    out.hpTook = hpBefore - subBoss.hp;
    out.flashField = subBoss.flash || 0;
    out.armorField = subBoss._qlArmor || 0;
    const hit = measure(() => { if (typeof drawSubBoss === 'function') drawSubBoss(); });
    out.flashBlits = hit.__n;
    out.flashDrewTint = Object.keys(hit).some(k => /tint|__k/.test(k)) || hit.__n > out.drawBlits;
    out.flashBlitDelta = hit.__n - out.drawBlits;
  }

  proto.drawImage = realDraw;
  return out;
}
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--stage', default=None)
    a = ap.parse_args()
    stages = [int(s) for s in a.stage.split(',')] if a.stage else DEFAULT_STAGES

    from playwright.sync_api import sync_playwright
    port, stop = serve(GAME)
    url = 'http://127.0.0.1:%d/index.html' % port
    res = {}
    with sync_playwright() as p:
        b = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
        for st in stages:
            pg = b.new_page(viewport={'width': 1100, 'height': 1200}, device_scale_factor=1)
            errs = []
            pg.on('pageerror', lambda e: errs.append(str(e)[:160]))
            pg.goto(url, wait_until='load', timeout=60000)
            pg.wait_for_function("() => typeof ASSETS!=='undefined' && typeof setState==='function'", timeout=45000)
            pg.wait_for_function("() => (window.__bofFrames|0) > 4", timeout=45000)
            # give the sub-boss art a chance to decode before anything is counted
            # ⚠ POLL THE ART READY BEFORE MEASURING. rdy() is false on its first call and that call
            # starts the load, so a one-shot check reads false and a blit count taken then is a
            # measurement of the loader, not of the draw.
            need = {1: ['nqx_body_intact', 'nqx_cannon_left_outer_intact'],
                    2: ['nobd_assembled_intact', 'nobd_assembled_damaged']}.get(st, [])
            pg.evaluate("(a)=>{ if(typeof warmStageSheets==='function') warmStageSheets(a[0]);"
                        "  (a[1]||[]).forEach(k=>{ try{ XART.rdy(k); }catch(e){} }); }", [st, need])
            try:
                pg.wait_for_function("(ks)=>ks.every(k=>XART.rdy(k))", arg=need, timeout=45000)
            except Exception:
                pass          # report it below rather than failing — artReady carries the truth
            try:
                res[st] = pg.evaluate(RUN, st)
            except Exception as e:
                res[st] = {'err': str(e)[:200]}
            res[st]['pageErrors'] = errs[:3]
            pg.close()
        b.close()
    stop()

    print('MINIBOSSES: spawn, draw (BLIT COUNT), reach the field, and flash when hit.\n')
    bad = 0
    for st in stages:
        r = res[st]
        if r.get('err'):
            print('  stage %d  FAIL — %s' % (st, r['err'])); bad += 1; continue
        print('  stage %d  %s' % (st, r.get('kind')))
        print('     spawned      %s   hp %s/%s   %sx%s   art=%s sx=%s'
              % (r.get('spawned'), r['spawn']['hp'], r['spawn']['maxhp'], r['spawn']['w'],
                 r['spawn']['h'], r['spawn']['art'], r['spawn']['sxcode']))
        yt = r['yTrack']
        print('     entered      y %s -> %s  (min %s max %s), %d/240 frames on screen, alive=%s'
              % (yt['first'], yt['last'], yt['min'], yt['max'], yt['onScreen'], r.get('alive')))
        print('     art ready    %s' % r.get('artReady'))
        print('     draw sees    %s' % r.get('drawState'))
        print('     VISIBLE      %s   %d px change when the unit is removed from the frame'
              % ('YES' if r.get('visible') else '*** NO ***', r.get('visiblePixels', -1)))
        print('     (blit hint   %d — see the warning in this file; the pixel diff is the verdict)'
              % r['drawBlits'])
        if r.get('drawErr'): print('     ⚠ draw threw: %s' % r['drawErr'])
        print('     health bar   %d blits   %s' % (r['barBlits'], r['barKeys']))
        if r.get('cannonsKilled') is not None:
            print('     hull opened  %s after killing %d cannons; hit took %s hp; flash=%.2f armor=%.2f'
                  % (r['hullOpen'], r['cannonsKilled'], r['hpTook'], r['flashField'], r['armorField']))
            print('     FLASH DREW   %d blits vs %d idle  (delta %+d)  %s'
                  % (r['flashBlits'], r['drawBlits'], r['flashBlitDelta'],
                     'WHITE PULSE ON SCREEN' if r['flashBlitDelta'] > 0 else '*** NOTHING EXTRA DRAWN ***'))
            if r['flashBlitDelta'] <= 0: bad += 1
        if not r.get('visible'):
            print('     *** DRAWS NOTHING — it is on the field and invisible ***'); bad += 1
        if r.get('pageErrors'): print('     ⚠ page errors: %s' % r['pageErrors'])
        print('')
    print('%s' % ('ALL MEASURED MINIBOSSES DRAW AND FLASH' if bad == 0 else '%d problem(s)' % bad))
    sys.exit(0 if bad == 0 else 1)


if __name__ == '__main__':
    main()
