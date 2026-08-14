import http.server, socketserver, threading, os, functools
GAME=r'C:/Users/Mdogg/Desktop/BOF-CODE/BulletsOfFury'
def serve(d):
    h=functools.partial(http.server.SimpleHTTPRequestHandler, directory=d); h.log_message=lambda *a,**k:None
    s=socketserver.TCPServer(("127.0.0.1",0),h); threading.Thread(target=s.serve_forever,daemon=True).start()
    return s.server_address[1]
RUN=r"""
(stage)=>{
  ASSETS.ready=true; run.pilot='cole'; run.mode='arcade';
  beginStage(stage); setState(GS.PLAY); player.invuln=1e9;
  /* a unit POPS IN if, on the first frame it exists, any part of it is already inside the frame.
     top edge = y - h/2 ; inside the frame means top > 0. */
  const pops=[], ok=[];
  const real=spawnEnemy;
  spawnEnemy=function(){ const e=real.apply(null,arguments);
    if(e){ const top=e.y-e.h*0.5;
      (top > 0 ? pops : ok).push({t:e.type, y:Math.round(e.y), h:Math.round(e.h), top:Math.round(top)}); }
    return e; };
  const t0=performance.now(); for(let i=0;i<2700;i++) loop(t0+i*16.7);
  spawnEnemy=real;
  const byType={}; for(const p of pops) byType[p.t]=(byType[p.t]||0)+1;
  return {stage, total:pops.length+ok.length, popped:pops.length, byType, sample:pops.slice(0,5)};
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
        r=pg.evaluate(RUN, st)
        print('stage %d: %d spawns, %d POPPED IN  %s' % (r['stage'], r['total'], r['popped'], r['byType'] or ''))
        for s2 in r['sample']: print('      ', s2)
        b.close()
