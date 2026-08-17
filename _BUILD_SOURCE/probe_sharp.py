#!/usr/bin/env python3
"""probe_sharp.py - is the level art actually crisp, or just differently blurry?

Mike: "Its likke you've upscaled my levels in-game and they dont look as clear ... the stages were
already graphic at 800 wide my man, hwat are you doing?"

The masters are 800 wide and drawn 1:1 in virtual space, but SS=2 puts them on a VW*2 backing, so
every authored column was resampled to two under imageSmoothingQuality='high'.

MEASURED AS COLOUR COUNT, NOT BY EYE. A nearest-neighbour double copies each source pixel, so the
palette of a crop is unchanged. A bilinear double invents a blended value between every authored
pair, which multiplies the distinct colours in the same crop. The ratio between the two is the blur.

Renders the same stage frame with smoothing forced ON and OFF and compares. Also samples a single
horizontal run to count how many 2px-wide blocks are actually uniform - under a clean 2x every
pair of backing columns must be identical, and that is a property, not an impression.
"""
import http.server, socketserver, threading, functools, base64, io, os, sys
GAME = r'C:/Users/Mdogg/Desktop/BOF-CODE/BulletsOfFury'
OUT  = os.path.join(GAME, 'docs', 'proofs')

def serve(d):
    h = functools.partial(http.server.SimpleHTTPRequestHandler, directory=d)
    h.log_message = lambda *a, **k: None
    s = socketserver.TCPServer(("127.0.0.1", 0), h)
    threading.Thread(target=s.serve_forever, daemon=True).start()
    return s.server_address[1]

SHOT = r"""
([stage, smooth])=>{
  ASSETS.ready=true; run.stage=stage; run.pilot='cole';
  try{ beginStage(stage); }catch(e){} try{ warmStage(stage); }catch(e){}
  setState(GS.PLAY); player.reset(); player.invuln=999999;
  enemies.length=0; pBullets.length=0; eBullets.length=0; boss=null; subBoss=null;
  mapScroll=600;
  const cv=document.getElementById('screen');
  const c=cv.getContext('2d');
  /* force the flag AFTER every init path has run, so this measures the draw and not the boot */
  c.imageSmoothingEnabled = !!smooth;
  if(smooth) c.imageSmoothingQuality='high';
  try{ drawWorld(1/60); }catch(e){ return {err:String(e)}; }
  return {img:cv.toDataURL('image/png'), w:cv.width, h:cv.height,
          ss:(typeof SS==='number')?SS:null, VW:VW, VH:VH,
          flag:c.imageSmoothingEnabled};
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

    css = pg.evaluate("()=>{const c=document.querySelector('#screen-area canvas');"
                      "return c?getComputedStyle(c).imageRendering:'(no canvas)';}")
    boot = pg.evaluate("()=>document.getElementById('screen').getContext('2d').imageSmoothingEnabled")
    print('canvas CSS image-rendering : %s' % css)
    print('imageSmoothingEnabled at boot: %s' % boot)
    if css != 'pixelated':
        print('*** the display scale is still filtered')
    if boot:
        print('*** the draw default is still bilinear')

    print('\n%-7s %-9s %10s %10s %8s   %s' % ('stage', 'smoothing', 'colours', 'colours', 'ratio', 'uniform 2px pairs'))
    print('%-7s %-9s %10s %10s %8s' % ('', '', 'ON', 'OFF', ''))
    bad = 0
    for stage in (1, 5, 8):
        res = {}
        for smooth in (True, False):
            s = pg.evaluate(SHOT, [stage, smooth])
            if s.get('err'):
                print('stage %d render ERR %s' % (stage, s['err'])); bad += 1; res = None; break
            im = Image.open(io.BytesIO(base64.b64decode(s['img'].split(',', 1)[1]))).convert('RGB')
            # a mid-screen crop of the BACKDROP, away from HUD and player
            crop = im.crop((int(im.width * 0.15), int(im.height * 0.25),
                            int(im.width * 0.55), int(im.height * 0.55)))
            colours = len(set(crop.getdata()))
            # under a clean nearest 2x, backing columns pair up identically
            row = crop.height // 2
            pairs = tot = 0
            for x in range(0, crop.width - 1, 2):
                tot += 1
                if crop.getpixel((x, row)) == crop.getpixel((x + 1, row)): pairs += 1
            res[smooth] = (colours, pairs, tot, s)
            crop.save(os.path.join(OUT, 'sharp_s%d_%s.png' % (stage, 'on' if smooth else 'off')))
        if not res: continue
        cON = res[True][0]; cOFF = res[False][0]
        pOFF, tOFF = res[False][1], res[False][2]
        ratio = (cON / cOFF) if cOFF else 0
        print('%-7d %-9s %10d %10d %7.2fx   %d/%d (%.0f%%) with smoothing OFF'
              % (stage, '', cON, cOFF, ratio, pOFF, tOFF, 100.0 * pOFF / max(1, tOFF)))
        if max(cON, cOFF) < 200:
            # a near-empty crop is an UNRENDERED backdrop, not a sharp one. Saying "no blur here"
            # about blank canvas is the same class of error as measuring the lava background.
            print('        (crop is essentially blank - backdrop did not render at this scroll,'
                  ' not measured)')
        elif cOFF >= cON:
            print('        *** turning smoothing off did not reduce the palette - the blur is'
                  ' coming from somewhere else on this stage'); bad += 1
        if pOFF < tOFF * 0.9:
            print('        *** even with smoothing off the 2x is not landing on clean pairs —'
                  ' something is drawn at a non-integer scale'); bad += 1

    s0 = pg.evaluate(SHOT, [1, False])
    print('\nbacking canvas %dx%d, SS=%s, virtual %dx%d'
          % (s0['w'], s0['h'], s0['ss'], s0['VW'], s0['VH']))
    print('-> crops in docs/proofs/sharp_s*_on|off.png')
    if errs: print('\nPAGE ERRORS: %s' % errs[:3])
    print('\n%s' % ('the levels draw at their authored crispness'
                    if bad == 0 else '*** %d problem(s)' % bad))
    br.close()
