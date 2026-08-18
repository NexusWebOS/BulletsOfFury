#!/usr/bin/env python3
"""
probe_weaponid_0814a.py — THE PIXEL HALF of Mike's items 1, 2 and 3.

    python3 _BUILD_SOURCE/probe_weaponid_0814a.py

⚠ WHY THIS EXISTS SEPARATELY FROM probe_weaponid_0814a.js.

The .js probe drives the real engine and proves the STATE: which variant is held, which element
it reports, which flag lands on the projectile. CLAUDE.md rule 2 says that proves nothing about
what the player sees, and this file's history is a list of systems that were declared, flagged
and wired and still drew nothing — the quad-laser's muzzles, `_qlChg`, `micon_` asked of the
wrong store, the whole `NEWBOSS` table.

WHAT IT MEASURES: every art key the draw path asks XART for, during REAL frames of the real game
in real Chromium, with one variant held. The claim in each of Mike's three sentences is a claim
about WHICH ART COMES OUT, so that is the quantity:

    flamethrower  ->  nfw_wall_*   and NOT nib*      (item 1: they are separate attacks)
    ice breath    ->  nib*/nibr_*  and NOT nfw_wall_*
    fire orb      ->  nfb_orb*                        (control)
    ice orb       ->  nio_*                           (control)
    FIRE-ICE ORB  ->  nts_*        and NOT nfb_orb*/nio_*   (item 3: not a basic fireorb)

⚠ THE KEY LOG IS TAKEN FROM REAL FRAMES, VIA `loop()`. 0810l records that wrapping a draw call
and then invoking the draw BY HAND does not count what the frame draws. The wrapper here only
observes; the game runs itself.

⚠ AND THE FIRST CUT OF THIS PROBE MEASURED THE LEVEL, NOT THE WEAPON. It classified every lit
pixel in a 180x230 band as warm or cold. On stage 2 the desert made it read 143,194 warm with
the ICE BREATH equipped; on stage 4 the sky made every orb read cold. 153,866 "lit" pixels in a
165,600-pixel band is the tell — that is the backdrop, and the plume is a rounding error beside
it. Same shape as 0813x's edge detector finding the HUD. A colour figure is still printed, but
from a tight box around the projectile and as INDICATIVE ONLY; the assertion is the key log.

⚠ THE PLAYER NEVER FIRES IN THIS HARNESS. Firing needs an input tap nothing simulates, so
`pShoot()` is called directly — the note CLAUDE.md carries for probe_weapons.py.
"""
import os, sys, base64, http.server, socketserver, threading, functools

ROOT = os.path.dirname(os.path.abspath(__file__))
GAME = os.path.abspath(os.path.join(ROOT, '..'))
PROOF = os.path.join(GAME, 'docs', 'proofs')


def serve(directory, port=0):
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=directory)
    handler.log_message = lambda *a, **k: None
    httpd = socketserver.TCPServer(("127.0.0.1", port), handler)
    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()
    return httpd.server_address[1], httpd.shutdown


RUN = r"""
(cfg) => {
  const out = {ok:false, err:null};
  try {
    ASSETS.ready = true;
    run.pilot = cfg.pilot; run.stage = cfg.stage;
    curStage = STAGES[cfg.stage-1];
    beginStage(cfg.stage); setState(GS.PLAY);
    player.reset(); player.invuln = 1e9;

    run.weapon  = cfg.slot;
    run.wlevels = [0,0,0,0,0,0]; run.wlevels[cfg.slot] = cfg.lv; run.wlevel = cfg.lv;
    run.wvars   = [null,null,null,null,null,null]; run.wvars[cfg.slot] = cfg.variant;
    run._dbgIce = false; run._dbgFire = false;

    /* clear the field: an enemy explosion puts the same colours on screen as the weapon */
    enemies.length = 0; eBullets.length = 0; pBullets.length = 0; particles.length = 0;

    const seen = new Set();
    const _get = XART.get.bind(XART);
    XART.get = function(k){ seen.add(k); return _get(k); };

    /* touch the art this weapon needs so the lazy load STARTS — XART.rdy is false on its first
       call because that call is what begins the decode */
    for (const k of cfg.warm) { try { XART.rdy(k); } catch(e){} }
    seen.clear();                       // the warm touches are not draws; only frames count

    window.__probeFire = () => {
      for (let i = 0; i < cfg.frames; i++) {
        if (i % 3 === 0) { try { pShoot(); } catch(e){} }
        loop(performance.now() + i*16.7);
      }
      /* the projectile's own box, for the indicative colour sample */
      let box = null;
      for (const b of pBullets) {
        if (b.kind==='flame') { box={x0:b.x-40,x1:b.x+40,y0:b.top+20,y1:b.bot-20}; break; }
        if (b.kind==='orb')   { box={x0:b.x-b.w,x1:b.x+b.w,y0:b.y-b.w,y1:b.y+b.w}; break; }
      }
      return {keys:[...seen], box, n:pBullets.length};
    };
    out.ok = true;
  } catch(e) { out.err = String(e && e.message || e); }
  return out;
}
"""

# ⚠ CLASSIFY THE PLATE, NOT THE SCREEN.
#
# The first cut of this probe read a band of the CANVAS and counted warm and cold pixels. On
# stage 2 the desert reported 62,336 warm pixels with the ICE BREATH equipped — the plume is a
# few hundred pixels beside a backdrop of tens of thousands, so the figure was a measurement of
# the level. Same family as 0813x's edge detector finding the HUD instead of the terrain.
#
# The claim is about the ART, so the ART is what gets sampled: the exact plate the draw path
# asked for, on transparent black, alpha-masked. Nothing but the sprite can contribute.
PALETTE = r"""
(key) => {
  if (!key) return null;
  if (!XART.rdy(key)) return null;
  const im = XART.get(key);
  const w = im.naturalWidth || im.width, h = im.naturalHeight || im.height;
  if (!w || !h) return null;
  const c = document.createElement('canvas'); c.width = w; c.height = h;
  const x = c.getContext('2d'); x.drawImage(im, 0, 0);
  const d = x.getImageData(0, 0, w, h).data;
  let warm=0, cold=0, ink=0;
  for (let i=0;i<d.length;i+=4){
    if (d[i+3] < 40) continue;                  // transparent — not part of the sprite
    ink++;
    const r=d[i], b=d[i+2];
    if (r > b + 45) warm++;
    if (b > r + 45) cold++;
  }
  return {warm, cold, ink, w, h};
}
"""

GRAB = ("() => { const g = document.querySelector('#screen-area canvas')"
        " || document.querySelector('canvas'); return g ? g.toDataURL('image/png') : null; }")


def fam(keys, *prefixes):
    return sorted({k for k in keys if any(k.startswith(p) for p in prefixes)})


def main():
    from playwright.sync_api import sync_playwright
    os.makedirs(PROOF, exist_ok=True)

    NTS = (['nts_orb_%d' % i for i in range(12)] + ['nts_shard_%d' % i for i in range(8)]
           + ['nts_burst_%d' % i for i in range(8)] + ['nts_chg_%d' % i for i in range(4)]
           + ['nts_rel_%d' % i for i in range(4)] + ['nts_imp_%d' % i for i in range(4)])
    FLAME = (['nfw_wall_%d' % i for i in range(8)] + ['nibr_%d' % i for i in range(8)]
             + ['nib_roll_%d' % i for i in range(8)] + ['nib_hold_%d' % i for i in range(6)])
    ORB = (['nio_%d' % i for i in range(8)]
           + ['nfb_orb%d_%d' % (l, f) for l in range(1, 6) for f in range(8)]
           + ['iceorb_%d' % i for i in range(4)] + ['fireshard_%d' % i for i in range(4)]
           + ['iceshard_%d' % i for i in range(4)])

    # label, pilot, stage, slot, variant, warm-list, must-draw, must-NOT-draw, plate colour
    CASES = [
        ('FLAMETHROWER  item 1', 'freezer', 2, 4, 'flamethrower', FLAME + NTS,
         ('nfw_wall_',), ('nib_roll_', 'nib_hold_', 'nibr_'), 'warm'),
        ('ICE BREATH    item 1', 'freezer', 2, 4, 'icebreath', FLAME + NTS,
         ('nibr_', 'nib_roll_', 'nib_hold_'), ('nfw_wall_',), 'cold'),
        ('FIRE ORB      control', 'cole', 3, 5, 'fireorb', ORB + NTS,
         ('nfb_orb',), ('nts_', 'nio_'), 'warm'),
        ('ICE ORB       control', 'cole', 4, 5, 'iceorb', ORB + NTS,
         ('nio_',), ('nts_', 'nfb_orb'), 'cold'),
        ('FIRE-ICE ORB  item 3', 'freezer', 4, 5, 'fireice', ORB + NTS,
         ('nts_orb_', 'nts_shard_'), ('nfb_orb', 'nio_'), 'both'),
    ]

    port, stop = serve(GAME)
    url = 'http://127.0.0.1:%d/index.html' % port
    rows, fails = [], 0

    with sync_playwright() as p:
        b = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
        for (label, pilot, stage, slot, variant, warm, must, mustnot, expect_colour) in CASES:
            pg = b.new_page(viewport={'width': 1100, 'height': 1200}, device_scale_factor=1)
            pg.goto(url, wait_until='load', timeout=60000)
            pg.wait_for_function("() => typeof ASSETS!=='undefined' && typeof setState==='function'", timeout=45000)
            pg.wait_for_function("() => (window.__bofFrames|0) > 4", timeout=45000)

            res = pg.evaluate(RUN, {'pilot': pilot, 'stage': stage, 'slot': slot,
                                    'variant': variant, 'lv': 5, 'frames': 40, 'warm': warm})
            if not res.get('ok'):
                print('setup failed for %s: %s' % (label, res.get('err')))
                fails += 1; pg.close(); continue

            # ⚠ AN AWAIT BOUNDARY IS WHAT LETS THE DECODE FINISH. shoot.py's `--warm N` is a single
            # synchronous burst and lazily-loaded art never arrives inside it, at any N.
            pg.wait_for_timeout(1500)
            r = pg.evaluate("() => window.__probeFire()")
            keys = r['keys']

            drew = fam(keys, *must)
            leaked = fam(keys, *mustnot)
            good = bool(drew) and not leaked

            # the colour of the plate that was actually drawn, alpha-masked
            col = (pg.evaluate(PALETTE, drew[0]) if drew else None) or {'warm': -1, 'cold': -1, 'ink': 0}
            if col['ink']:
                wpc = 100.0 * col['warm'] / col['ink']
                cpc = 100.0 * col['cold'] / col['ink']
                # each case must also LOOK like what it claims to be
                if expect_colour == 'warm' and not (wpc > 20 and cpc < 5):
                    good = False
                if expect_colour == 'cold' and not (cpc > 20 and wpc < 5):
                    good = False
                if expect_colour == 'both' and not (wpc > 10 and cpc > 10):
                    good = False
            else:
                wpc = cpc = -1.0
            if not good:
                fails += 1

            png = pg.evaluate(GRAB)
            slug = variant + ('_s%d' % stage)
            if png:
                open(os.path.join(PROOF, 'weaponid_0814a_%s.png' % slug), 'wb').write(
                    base64.b64decode(png.split(',', 1)[1]))
            rows.append((label, variant, drew, leaked, good, wpc, cpc, expect_colour))
            pg.close()
        b.close()
    stop()

    print('\n%-22s %-13s %-30s %-18s %-7s %-7s %-6s' %
          ('CASE', 'HELD', 'DREW (required)', 'LEAKED', 'warm%', 'cold%', 'want'))
    print('-' * 108)
    for (label, variant, drew, leaked, good, wpc, cpc, exp) in rows:
        print('%-22s %-13s %-30s %-18s %6.1f%% %6.1f%% %-6s %s' % (
            label, variant,
            (', '.join(drew[:2]) + (' +%d' % (len(drew) - 2) if len(drew) > 2 else '')) or 'NOTHING',
            (', '.join(leaked[:2])) or '-',
            wpc, cpc, exp, 'OK ' if good else 'FAIL'))
    print("\nwarm%/cold% are of the DRAWN PLATE's own ink, alpha-masked - not of the screen.")
    print('frames saved to docs/proofs/weaponid_0814a_*.png')
    print('%d of %d cases as expected' % (len(rows) - fails, len(rows)))
    sys.exit(1 if fails else 0)


if __name__ == '__main__':
    main()
