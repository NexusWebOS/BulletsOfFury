#!/usr/bin/env python3
"""probe_miniwarm.py - is the miniboss a hitbox square, or a hitbox square FOR THE FIRST SECOND?

probe_miniboss.py showed all eight minibosses draw their art when the sheets are given wall-clock
to decode. That does not clear them: XART.rdy() is what STARTS a decode, so if nothing warms a
miniboss's art before it spawns, the player gets the placeholder for as long as the download takes
- which is exactly the "hitbox square" in the tester's screenshot.

This reproduces what a real run does and nothing more:
    beginStage(n) -> warmStage(n) -> a long settle (stands in for the minutes of play before the
    miniboss triggers) -> spawn -> draw IMMEDIATELY.

Any key the draw asks for that is not ready at that moment is a key nothing warmed. XART.rdy is
wrapped to record them, so the answer is a list of key names rather than an impression.
"""
import http.server, socketserver, threading, functools, os, base64
GAME = r'C:/Users/Mdogg/Desktop/BOF-CODE/BulletsOfFury'

def serve(d):
    h = functools.partial(http.server.SimpleHTTPRequestHandler, directory=d)
    h.log_message = lambda *a, **k: None
    s = socketserver.TCPServer(("127.0.0.1", 0), h)
    threading.Thread(target=s.serve_forever, daemon=True).start()
    return s.server_address[1]

HOOK = r"""
()=>{
  const r=XART.rdy.bind(XART);
  window.__ask=[];
  XART.rdy=function(k){ const v=r(k); if(window.__rec) window.__ask.push([k,!!v]); return v; };
}
"""
WARM = r"""
(stage)=>{ ASSETS.ready=true; run.stage=stage; run.pilot='cole';
  try{ beginStage(stage); }catch(e){}
  try{ warmStage(stage); }catch(e){}
  return true; }
"""
SPAWN_DRAW = r"""
(stage)=>{
  setState(GS.PLAY);
  enemies.length=0; pBullets.length=0; eBullets.length=0; boss=null;
  subBoss=null; subBossActive=false; subBossDone=false; subBossTriggered=false;
  const kind=(SUBBOSS[stage]||{}).kind||null;
  try{ spawnSubBoss__inner(kind); }catch(e){ return {stage, kind, err:String(e)}; }
  const b=subBoss; if(!b) return {stage, kind, err:'no subBoss'};
  b.x=VW/2; b.y=VH*0.34; b.ty=VH*0.34; b.entry=0; b._ent=0; b.enter=false;
  window.__ask=[]; window.__rec=true;
  for(let i=0;i<6;i++){ stateT+=1/60; try{ drawWorld(1/60); }catch(e){} }   // the first tenth of a second
  window.__rec=false;
  const miss={}, hit={};
  for(const [k,v] of window.__ask){ (v?hit:miss)[k]=1; }
  const cv=document.getElementById('screen');
  return {stage, kind, name:b.name||null, x:b.x, y:b.y, w:b.w, h:b.h, scale:cv.width/VW,
          missing:Object.keys(miss), ready:Object.keys(hit).length,
          img:cv.toDataURL('image/png')};
}
"""

def tones(path, cx, cy, w, h, scale):
    from PIL import Image
    from collections import Counter
    im = Image.open(path).convert('RGB')
    x0 = max(0, int((cx - w * 0.7) * scale)); x1 = min(im.width,  int((cx + w * 0.7) * scale))
    y0 = max(0, int((cy - h * 0.7) * scale)); y1 = min(im.height, int((cy + h * 0.7) * scale))
    box = im.crop((x0, y0, x1, y1)); px = box.load(); c = Counter()
    for y in range(box.height):
        for x in range(box.width):
            r, g, b = px[x, y]
            if r + g + b > 90: c[(r // 24, g // 24, b // 24)] += 1
    return len(c)

from playwright.sync_api import sync_playwright
OUT = os.path.join(GAME, 'docs', 'proofs')
os.makedirs(OUT, exist_ok=True)
port = serve(GAME)
with sync_playwright() as p:
    b  = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
    pg = b.new_page(viewport={'width': 620, 'height': 900}, device_scale_factor=1)
    pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=60000)
    pg.wait_for_function("()=>typeof setState==='function'", timeout=45000)
    pg.wait_for_function("()=>(window.__bofFrames|0)>4", timeout=45000)
    pg.evaluate(HOOK)

    print('%-6s %-12s %-22s %6s  %s' % ('stage', 'kind', 'name', 'tones', 'NOT READY at spawn'))
    for st in range(1, 9):
        pg.evaluate(WARM, st)
        pg.wait_for_timeout(4000)                     # stands in for the play before the trigger
        r = pg.evaluate(SPAWN_DRAW, st)
        if r.get('err'):
            print('%-6d %-12s *** %s' % (st, r.get('kind'), r['err'])); continue
        path = os.path.join(OUT, 'miniwarm_s%d_0812c.png' % st)
        with open(path, 'wb') as f:
            f.write(base64.b64decode(r['img'].split(',', 1)[1]))
        t = tones(path, r['x'], r['y'], r['w'], r['h'], r['scale'])
        miss = r['missing']
        print('%-6d %-12s %-22s %6d  %d not ready, %d ready'
              % (st, r['kind'], (r['name'] or '?')[:22], t, len(miss), r['ready']))
        for k in miss:
            print('           %s' % k)
    b.close()
    print('\n-> docs/proofs/miniwarm_s1..8_0812c.png')
