#!/usr/bin/env python3
"""probe_signdrift.py - do the roadside signs move WITH the ground, or across it?

Mike: "the signs are scrolling" (and previously: "they do not scroll ever").

The claim in the source (drop 0810h, game.js:2936) is that they already stay put, because both the
signs and the props draw at `y - mapScroll`. But the TERRAIN is not drawn that way. drawLevelMaster
windows the master at

    srcY = rangeSrc - (mapScroll/range)*rangeSrc

so srcY DECREASES as the level advances and a feature at master row R lands at screen `R - srcY`,
which INCREASES - terrain moves DOWN the screen. A sign at `sn.y - mapScroll` moves UP. If that is
right they drift apart at twice the scroll rate, which is precisely "the signs are scrolling".

⚠ MEASURED, NOT DERIVED. Reasoning about the sign of an offset is exactly how this gets got wrong,
so this measures both displacements off the canvas:

  TERRAIN  cross-correlate a vertical strip between two frames -> how far the ground actually moved.
  SIGN     diff the same two frames with the sign list emptied vs intact, and track the centroid of
           what changes -> how far the sign actually moved.

Same two frames, same units. If the two numbers have opposite signs, they are sliding past each
other.
"""
import http.server, socketserver, threading, functools, base64, io, os
GAME = r'C:/Users/Mdogg/Desktop/BOF-CODE/BulletsOfFury'
OUT  = os.path.join(GAME, 'docs', 'proofs')

def serve(d):
    h = functools.partial(http.server.SimpleHTTPRequestHandler, directory=d)
    h.log_message = lambda *a, **k: None
    s = socketserver.TCPServer(("127.0.0.1", 0), h)
    threading.Thread(target=s.serve_forever, daemon=True).start()
    return s.server_address[1]

SHOT = r"""
([stage, scroll, withSigns])=>{
  ASSETS.ready=true; run.stage=stage; run.pilot='cole';
  try{ beginStage(stage); }catch(e){} try{ warmStage(stage); }catch(e){}
  setState(GS.PLAY); player.reset(); player.invuln=999999;
  player.x=-9999; player.y=-9999;              // park the ship out of the measured band
  enemies.length=0; pBullets.length=0; eBullets.length=0; boss=null; subBoss=null;
  /* toggle the sign list so the frame difference isolates the SIGNS from the ground */
  if(!window.__rsSave) window.__rsSave=JSON.parse(JSON.stringify(window.BOFRS||{}));
  window.BOFRS = withSigns ? JSON.parse(JSON.stringify(window.__rsSave)) : {};
  mapScroll=scroll;
  const cv=document.getElementById('screen');
  try{ drawWorld(1/60); }catch(e){ return {err:String(e)}; }
  const list=(window.__rsSave||{})[String(stage)]||[];
  return {img:cv.toDataURL('image/png'), VW:VW, VH:VH, nSigns:list.length,
          sampleY:(list[0]?list[0].y:null)};
}
"""

from playwright.sync_api import sync_playwright
from PIL import Image
os.makedirs(OUT, exist_ok=True)
port = serve(GAME)

def gray_rows(im, x0, x1):
    """mean luminance per row over a column band -> a 1-D signal to correlate"""
    px = im.load()
    return [sum(sum(px[x, y]) for x in range(x0, x1)) / (3.0 * (x1 - x0))
            for y in range(im.height)]

def best_shift(a, b, maxs):
    """shift s (in rows) that best aligns b onto a; positive = content moved DOWN"""
    best, bestv = 0, None
    n = len(a)
    for s in range(-maxs, maxs + 1):
        num = cnt = 0.0
        for y in range(n):
            y2 = y - s
            if 0 <= y2 < n:
                num += abs(a[y] - b[y2]); cnt += 1
        if cnt < n * 0.5: continue
        v = num / cnt
        if bestv is None or v < bestv: bestv, best = v, s
    return best

with sync_playwright() as p:
    br = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
    pg = br.new_page(viewport={'width': 620, 'height': 900}, device_scale_factor=1)
    errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=60000)
    pg.wait_for_function("()=>typeof setState==='function'", timeout=45000)
    pg.wait_for_function("()=>(window.__bofFrames|0)>4", timeout=45000)
    pg.wait_for_timeout(3500)

    STEP = 60
    bad = 0
    measured = 0
    # scroll chosen so a sign is MID-SCREEN: sy = sn.y - mapScroll, and stage 4's signs run 1002..2760
    BASE = {1: 1200, 4: 900}
    for stage in (1, 4):
        print('\n=== STAGE %d ===' % stage)
        frames = {}
        base = BASE.get(stage, 1200)
        for scroll in (base, base + STEP):
            for ws in (True, False):
                s = pg.evaluate(SHOT, [stage, scroll, ws])
                if s.get('err'):
                    print('  render ERR %s' % s['err']); bad += 1; frames = None; break
                frames[(scroll, ws)] = (
                    Image.open(io.BytesIO(base64.b64decode(s['img'].split(',', 1)[1]))).convert('RGB'), s)
            if frames is None: break
        if not frames: continue
        n = frames[(base, True)][1]['nSigns']
        print('  %d sign(s) registered for this stage' % n)
        if n == 0:
            print('  (no signs here - nothing to measure)'); continue

        # TERRAIN: correlate the no-signs frames
        a = frames[(base, False)][0]; b = frames[(base + STEP, False)][0]
        x0, x1 = int(a.width * 0.20), int(a.width * 0.40)
        ga = gray_rows(a.crop((x0, int(a.height * 0.20), x1, int(a.height * 0.80))), 0, x1 - x0)
        gb = gray_rows(b.crop((x0, int(b.height * 0.20), x1, int(b.height * 0.80))), 0, x1 - x0)
        tshift = best_shift(ga, gb, 90)

        # SIGNS: centroid of (with - without) in each frame
        def sign_centroid(scroll):
            w = frames[(scroll, True)][0]; wo = frames[(scroll, False)][0]
            tot = 0.0; acc = 0.0
            for y in range(0, w.height, 2):
                for x in range(0, w.width, 2):
                    p1 = w.getpixel((x, y)); p0 = wo.getpixel((x, y))
                    d = abs(p1[0]-p0[0]) + abs(p1[1]-p0[1]) + abs(p1[2]-p0[2])
                    if d > 40: acc += y * d; tot += d
            return (acc / tot) if tot else None
        c0 = sign_centroid(base); c1 = sign_centroid(base + STEP)
        if c0 is None or c1 is None:
            print('  *** the signs drew nothing at this scroll - cannot measure'); continue
        sshift = c1 - c0
        # canvas is SS=2, report in virtual px
        scale = frames[(base, True)][0].width / frames[(base, True)][1]['VW']
        print('  ground moved %+.0f px over %d of mapScroll' % (tshift / scale, STEP))
        print('  signs  moved %+.0f px over the same step' % (sshift / scale))
        if tshift == 0:
            print('  (ground did not move - cannot compare)'); continue
        if (tshift / scale) * (sshift / scale) < 0:
            print('  *** OPPOSITE DIRECTIONS - the signs slide across the ground'); bad += 1
        elif abs(abs(tshift) - abs(sshift)) / max(1.0, abs(tshift)) > 0.25:
            print('  *** same direction but different rate - they still drift'); bad += 1
        else:
            print('  signs are pinned to the ground')
        measured += 1

    if errs: print('\nPAGE ERRORS: %s' % errs[:3])
    print('\n%s' % ('signs ride with the terrain' if bad == 0 else '*** %d problem(s)' % bad))
    br.close()
