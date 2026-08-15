#!/usr/bin/env python3
"""probe_miniboss.py - "a miniboss is still just the hitbox square". WHICH one?

Mike said one was never replaced and the thread never named the stage. Eight stages have a
SUBBOSS entry, so this spawns each one and RENDERS it, then measures the drawn result instead of
asking whether an art key is registered - a registered key that never decodes draws nothing, and
a procedural fallback draws something that is not the art.

Two measurements per miniboss, because they fail differently:
  COLOURS   a hand-drawn fallback is a handful of flat fills; real pixel art is dozens of tones.
            A near-solid rectangle is the specific thing the tester photographed.
  EDGES     art has an irregular silhouette; a box has four straight sides. Counting the distinct
            x-extents across the sprite's rows separates the two without recognising anything.
"""
import http.server, socketserver, threading, functools, os, base64
GAME = r'C:/Users/Mdogg/Desktop/BOF-CODE/BulletsOfFury'
OUT  = os.path.join(GAME, 'docs', 'proofs')

def serve(d):
    h = functools.partial(http.server.SimpleHTTPRequestHandler, directory=d)
    h.log_message = lambda *a, **k: None
    s = socketserver.TCPServer(("127.0.0.1", 0), h)
    threading.Thread(target=s.serve_forever, daemon=True).start()
    return s.server_address[1]

# XART.rdy IS FALSE ON ITS FIRST CALL - it is what STARTS the decode. So a probe that spawns a
# miniboss and screenshots in the same synchronous block photographs the game's placeholder, not
# the miniboss, and reports art that works perfectly as "still a hitbox square". Spawn and render
# are split, with a REAL-TIME wait between them: warm, hand the browser the wall-clock it needs to
# decode, then draw.
WARM = r"""
(stage)=>{
  ASSETS.ready=true;
  run.stage=stage; run.pilot='cole';
  if(typeof beginStage==='function'){ try{ beginStage(stage); }catch(e){} }
  if(typeof warmStage==='function'){ try{ warmStage(stage); }catch(e){} }
  if(typeof warmStageSheets==='function'){ try{ warmStageSheets(stage); }catch(e){} }
  return true;
}
"""
SHOT = r"""
(stage)=>{
  ASSETS.ready=true;
  run.stage=stage; run.pilot='cole';
  setState(GS.PLAY);
  /* the arrays are pBullets/eBullets, not bullets/ebullets - a wrong name here throws a
     ReferenceError that reads as "the miniboss failed to spawn" */
  enemies.length=0; pBullets.length=0; eBullets.length=0;
  boss=null;
  var kind=(SUBBOSS[stage]||{}).kind||null;
  /* spawnSubBoss RETURNS NOTHING - it assigns the global `subBoss` and sets subBossActive.
     Reading its return value reported "failed to spawn" for all eight, which is the shape of a
     wrong contract, not of eight broken minibosses. */
  subBoss=null; subBossActive=false; subBossDone=false; subBossTriggered=false;
  try{ spawnSubBoss__inner(kind); }catch(e){ return {stage:stage, kind:kind, err:String(e)}; }
  var b=subBoss;
  if(!b) return {stage:stage, kind:kind, err:'no subBoss after spawn (retired in DEAD_SUBBOSS?)'};
  /* park it in open sky, mid-screen, and let its own tick settle the entry */
  b.x=VW/2; b.y=VH*0.34; b.ty=VH*0.34; b.entry=0; b._ent=0;
  for(var i=0;i<80;i++){ stateT+=1/60; try{ drawWorld(1/60); }catch(e){} }
  var cv=document.getElementById('screen');
  return {stage:stage, kind:kind, name:b.name||null, w:b.w, h:b.h,
          x:b.x, y:b.y, sub:!!b.sub, art:b.art||null,
          modular:!!b.modular, sx:!!b._sx, herald:!!b._herald, exca:!!b._exca,
          scale:cv.width/VW, img:cv.toDataURL('image/png')};
}
"""

def analyse(path, cx, cy, w, h, scale):
    from PIL import Image
    im = Image.open(path).convert('RGB')
    x0 = max(0, int((cx - w * 0.75) * scale)); x1 = min(im.width,  int((cx + w * 0.75) * scale))
    y0 = max(0, int((cy - h * 0.75) * scale)); y1 = min(im.height, int((cy + h * 0.75) * scale))
    box = im.crop((x0, y0, x1, y1))
    px = box.load()
    from collections import Counter
    cols = Counter(); rows = []
    for y in range(box.height):
        lit = [x for x in range(box.width) if sum(px[x, y]) > 90]
        if lit: rows.append((min(lit), max(lit)))
        for x in range(box.width):
            r, g, b = px[x, y]
            if r + g + b > 90: cols[(r // 24, g // 24, b // 24)] += 1
    lefts = len(set(r[0] for r in rows)); rights = len(set(r[1] for r in rows))
    return len(cols), lefts, rights, len(rows)

from playwright.sync_api import sync_playwright
os.makedirs(OUT, exist_ok=True)
port = serve(GAME)
with sync_playwright() as p:
    b  = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
    pg = b.new_page(viewport={'width': 620, 'height': 900}, device_scale_factor=1)
    pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=60000)
    pg.wait_for_function("()=>typeof setState==='function'", timeout=45000)
    pg.wait_for_function("()=>(window.__bofFrames|0)>4", timeout=45000)

    print('%-6s %-12s %-22s %6s %6s %7s  %s' % ('stage', 'kind', 'name', 'tones', 'lefts', 'rights', 'verdict'))
    for st in range(1, 9):
        pg.evaluate(WARM, st)
        pg.wait_for_timeout(2500)          # wall-clock, so the sheets actually decode
        r = pg.evaluate(SHOT, st)
        if r.get('err'):
            print('%-6d %-12s %s' % (st, r.get('kind'), '*** ' + r['err']))
            continue
        name = 'miniboss_s%d_0812c.png' % st
        path = os.path.join(OUT, name)
        with open(path, 'wb') as f:
            f.write(base64.b64decode(r['img'].split(',', 1)[1]))
        tones, lefts, rights, nrows = analyse(path, r['x'], r['y'], r['w'], r['h'], r['scale'])
        # a hand-drawn fallback is flat and straight-sided; art is neither
        boxy = (tones <= 12) or (nrows > 8 and lefts <= 3 and rights <= 3)
        print('%-6d %-12s %-22s %6d %6d %7d  %s'
              % (st, r['kind'], (r['name'] or '?')[:22], tones, lefts, rights,
                 '*** BOX / FALLBACK ***' if boxy else 'art'))
    b.close()
    print('\n-> docs/proofs/miniboss_s1..8_0812c.png')
