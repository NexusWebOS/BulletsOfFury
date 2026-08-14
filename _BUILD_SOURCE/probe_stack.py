#!/usr/bin/env python3
"""probe_stack.py — do enemies still stack, and are the boats in the water?

Mike: "make sure enemies do not collide with each other or stack on each other like that" and
"boats only exsit on the water section."

OVERLAP is measured as the worst pair on any frame, as a fraction of the smaller unit's box, so a
number here is "how buried was the most buried unit" rather than a count that hides severity.
BOATS-ON-LAND samples the land mask under each naval unit, which is the same alpha the game uses.
"""
import http.server, socketserver, threading, os, functools
GAME=r'C:/Users/Mdogg/Desktop/BOF-CODE/BulletsOfFury'
def serve(d):
    h=functools.partial(http.server.SimpleHTTPRequestHandler, directory=d); h.log_message=lambda *a,**k:None
    s=socketserver.TCPServer(("127.0.0.1",0),h); threading.Thread(target=s.serve_forever,daemon=True).start()
    return s.server_address[1]
RUN=r"""
([stage, sepOn])=>{
  ASSETS.ready=true; run.pilot='cole'; run.mode='arcade';
  beginStage(stage); setState(GS.PLAY); player.invuln=1e9;
  window.__sepOff = !sepOn;
  let worst=0, frames=0, badPairs=0, boatsOnLand=0, boatSamples=0;
  const t0=performance.now();
  for(let i=0;i<1800;i++){
    loop(t0+i*16.7); frames++;
    for(let a=0;a<enemies.length;a++){
      const A=enemies[a]; if(A.dead||A.prop||A.enter) continue;
      if(A._naval && _landMasks['mapJungle']){
        const m=_landMasks['mapJungle'];
        const range=Math.max(0,m.h-VH), mapY=Math.max(0,range-mapScroll)+A.y;
        boatSamples++;
        if(_isLand('mapJungle', A.x, mapY)) boatsOnLand++;
      }
      for(let b=a+1;b<enemies.length;b++){
        const B=enemies[b]; if(B.dead||B.prop||B.enter) continue;
        const ox=(A.w+B.w)*0.42-Math.abs(B.x-A.x), oy=(A.h+B.h)*0.42-Math.abs(B.y-A.y);
        if(ox>0&&oy>0){ badPairs++;
          const f=Math.min(ox/Math.min(A.w,B.w), oy/Math.min(A.h,B.h));
          if(f>worst) worst=f; }
      }
    }
  }
  return {stage, frames, badPairs, worstOverlapPct:+(worst*100).toFixed(1),
          boatSamples, boatsOnLand};
}
"""
from playwright.sync_api import sync_playwright
port=serve(GAME); url='http://127.0.0.1:%d/index.html'%port
with sync_playwright() as p:
    for st in [1,4]:
        b=p.chromium.launch(args=['--disable-gpu','--no-sandbox','--mute-audio'])
        pg=b.new_page(viewport={'width':620,'height':900}, device_scale_factor=1)
        pg.goto(url, wait_until='load', timeout=60000)
        pg.wait_for_function("()=>typeof setState==='function'", timeout=45000)
        pg.wait_for_function("()=>(window.__bofFrames|0)>4", timeout=45000)
        r=pg.evaluate(RUN,[st,True])
        print('stage %d  overlapping pair-frames %-6d  worst overlap %5.1f%%   boats sampled %-5d on LAND %d'
              % (r['stage'], r['badPairs'], r['worstOverlapPct'], r['boatSamples'], r['boatsOnLand']))
        b.close()
