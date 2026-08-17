#!/usr/bin/env python3
"""probe_stage5space.py - is stage 5 space for the WHOLE level, or only where you happen to look?

Mike: "your using a skybackground level 5 when its space the whole time."

⚠ THE NAME WAS THE TRAP, AND SO WAS SAMPLING ONE FRAME. storm800_rc2_master reads as space at
about 45% of its height - one orbital band with Earth's horizon - and as storm cloud, rain and
lightning everywhere else. A single mid-reel render of that plate says "space, looks fine", which
is exactly the wrong answer. This walks the scroll end to end instead.

Space is DARK and low-saturation-blue. Storm cloud is bright. Mean luminance across the frame
separates them cleanly (measured: the storm plate sits at 70-81, the orbital plate's edges at 7-11),
so every sampled point through the level must stay dark.

Also renders stage 8 as a control - it was already a space stage, so if the metric called stage 8
sky the metric would be wrong rather than the stage.
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
([stage, scroll])=>{
  ASSETS.ready=true; run.stage=stage; run.pilot='cole';
  try{ beginStage(stage); }catch(e){} try{ warmStage(stage); }catch(e){}
  setState(GS.PLAY); player.reset(); player.invuln=999999;
  enemies.length=0; pBullets.length=0; eBullets.length=0; boss=null; subBoss=null;
  /* mapScroll lives in the DRAW, so set it and draw in the same evaluate */
  mapScroll=scroll;
  const cv=document.getElementById('screen');
  try{ drawWorld(1/60); }catch(e){ return {err:String(e)}; }
  const cfg=(typeof _levelCfg==='function')?_levelCfg():null;
  return {img:cv.toDataURL('image/png'), VW:VW, VH:VH,
          master:cfg?cfg.master:null, loop:cfg?!!cfg.loopMaster:null};
}
"""

from playwright.sync_api import sync_playwright
from PIL import Image
os.makedirs(OUT, exist_ok=True)
port = serve(GAME)
with sync_playwright() as p:
    br = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
    pg = br.new_page(viewport={'width': 620, 'height': 900}, device_scale_factor=1)
    errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=60000)
    pg.wait_for_function("()=>typeof setState==='function'", timeout=45000)
    pg.wait_for_function("()=>(window.__bofFrames|0)>4", timeout=45000)
    pg.wait_for_timeout(3500)

    SCROLLS = [0, 400, 900, 1500, 2200, 3000, 3900, 4800]
    bad = 0
    for stage in (5, 8):
        print('\n=== STAGE %d ===' % stage)
        tiles = []
        first = None
        worst = None
        for sc in SCROLLS:
            s = pg.evaluate(SHOT, [stage, sc])
            if s.get('err'):
                print('  scroll %-5d render ERR %s' % (sc, s['err'])); bad += 1; continue
            if first is None:
                first = s
                print('  master %s   looping %s' % (s['master'], s['loop']))
            im = Image.open(io.BytesIO(base64.b64decode(s['img'].split(',', 1)[1]))).convert('RGB')
            # the play field only - avoid the HUD strip and the letterbox
            crop = im.crop((int(im.width * 0.10), int(im.height * 0.18),
                            int(im.width * 0.90), int(im.height * 0.85)))
            px = list(crop.getdata()); n = len(px)
            lum = sum(sum(q) for q in px) / (3.0 * n)
            verdict = 'SKY/bright' if lum > 55 else 'space'
            if verdict != 'space':
                bad += 1
                if worst is None or lum > worst[1]: worst = (sc, lum)
            print('  scroll %-5d mean luminance %5.1f  -> %s' % (sc, lum, verdict))
            t = crop.copy(); t.thumbnail((190, 190)); tiles.append(t)
        if tiles:
            w = max(t.width for t in tiles)
            cols = 4
            rows = (len(tiles) + cols - 1) // cols
            hh = max(t.height for t in tiles)
            sheet = Image.new('RGB', (w * cols, hh * rows), (10, 10, 14))
            for i, t in enumerate(tiles):
                sheet.paste(t, ((i % cols) * w, (i // cols) * hh))
            sheet.save(os.path.join(OUT, 'stage%d_scrollwalk.png' % stage))
            print('  -> docs/proofs/stage%d_scrollwalk.png' % stage)
        if worst:
            print('  *** brightest point scroll %d at luminance %.1f - still sky there'
                  % (worst[0], worst[1]))

    if errs: print('\nPAGE ERRORS: %s' % errs[:3])
    print('\n%s' % ('space the whole way' if bad == 0 else '*** %d sampled point(s) are not space' % bad))
    br.close()
