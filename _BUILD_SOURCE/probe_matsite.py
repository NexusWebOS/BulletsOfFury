#!/usr/bin/env python3
"""probe_matsite.py - WHICH code path puts an enemy on screen instead of above it?

probe_appear.py established the fact: 11 of 24 stage-1 units first exist below the top edge, the
worst at y=154, and stage 3 as deep as y=312. probe_popin.py had reported ZERO for two drops
because it watched spawnEnemy's ARGUMENT rather than where units actually end up.

Then trapping enemies.push showed NOTHING is pushed on screen - zero on all three stages. So the
unit is created correctly above the top edge and something MOVES IT DOWN before the frame ends.

This tags every unit with its push y and the stack that made it, then compares against where it
actually sits one frame later. The answer comes back as file:line, not as a theory.
"""
import http.server, socketserver, threading, functools, collections
GAME = r'C:/Users/Mdogg/Desktop/BOF-CODE/BulletsOfFury'

def serve(d):
    h = functools.partial(http.server.SimpleHTTPRequestHandler, directory=d)
    h.log_message = lambda *a, **k: None
    s = socketserver.TCPServer(("127.0.0.1", 0), h)
    threading.Thread(target=s.serve_forever, daemon=True).start()
    return s.server_address[1]

RUN = r"""
(stage)=>{
  ASSETS.ready=true; run.stage=stage; run.pilot='cole';
  try{ beginStage(stage); }catch(e){}
  setState(GS.PLAY); player.reset(); player.invuln=999999;
  if(typeof seedWaves==='function'){ try{ seedWaves(20260815); }catch(e){} }

  const hits=[];
  const realPush=Array.prototype.push;
  enemies.push=function(){
    for(let i=0;i<arguments.length;i++){
      const e=arguments[i];
      if(e && typeof e.y==='number'){
        e.__py=e.y;
        e.__st=(new Error()).stack.split('\n').slice(2,7)
                 .map(function(s){ return s.trim().replace(/^at\s+/,'').replace(/\(http:\/\/[^\/]+/,'('); })
                 .join(' | ');
      }
    }
    return realPush.apply(this, arguments);
  };

  for(let f=0; f<60*90; f++){
    player.invuln=999999; player.hp=99;
    try{ updatePlay(1/60); }catch(e){ break; }
    for(const e of enemies){
      if(e.__py===undefined || e.__done) continue;
      e.__done=1;
      if(e.__py<=4 && e.y>40){
        hits.push({from:Math.round(e.__py), to:Math.round(e.y),
                   t:String(e.type||e._nef||e.art||'?'), st:e.__st});
      }
    }
  }
  enemies.push=realPush;
  if(typeof unseedWaves==='function'){ try{ unseedWaves(); }catch(e){} }
  return hits;
}
"""

from playwright.sync_api import sync_playwright
port = serve(GAME)
with sync_playwright() as p:
    b  = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
    pg = b.new_page(viewport={'width': 620, 'height': 900}, device_scale_factor=1)
    pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=60000)
    pg.wait_for_function("()=>typeof setState==='function'", timeout=45000)
    pg.wait_for_function("()=>(window.__bofFrames|0)>4", timeout=45000)
    pg.wait_for_timeout(2500)

    for st in (1, 2, 3):
        hits = pg.evaluate(RUN, st)
        print('\n=== stage %d: %d units JUMPED on screen within their first frame ===' % (st, len(hits)))
        by = collections.Counter()
        for h in hits:
            by[h['st'].split(' | ')[0]] += 1
        for frame, n in by.most_common(5):
            moves = sorted({'%d->%d' % (h['from'], h['to']) for h in hits if h['st'].startswith(frame)})
            kinds = sorted({h['t'] for h in hits if h['st'].startswith(frame)})
            print('  x%-3d %s' % (n, ', '.join(moves[:6])))
            print('       kinds: %s' % ', '.join(kinds[:5]))
            print('       %s' % frame[:150])
    b.close()
