#!/usr/bin/env python3
"""probe_wobble.py — which projectiles "appear wobbly", and is it frame-rate dependent?

Mike, 0811m: 'Projecticles - "Appear wobly" sometimes'

"Sometimes" is the word that matters. A shape that is always the same is an authored corkscrew;
one that changes with the frame time is a bug. So every enemy bullet kind is flown twice over the
same simulated duration — once at a STEADY 1/60, once with the frame time jittering the way a real
browser's does — and the two paths are compared.

  lateral   the largest sideways excursion from the straight line between first and last point.
            A big number is not itself a fault: the swirl missiles are SUPPOSED to corkscrew.
  drift     how much that excursion CHANGES between the steady and jittered runs. This is the
            fault. A projectile whose shape depends on how long a frame took will read as
            wobbling whenever the machine hitches, and be clean on a good run — exactly
            "sometimes".

⚠ THE TWO RUNS COVER THE SAME SIMULATED TIME, not the same frame count, or the jittered arm would
simply travel further and every kind would look broken.
"""
import http.server, socketserver, threading, os, functools
GAME=r'C:/Users/Mdogg/Desktop/BOF-CODE/BulletsOfFury'
def serve(d):
    h=functools.partial(http.server.SimpleHTTPRequestHandler, directory=d); h.log_message=lambda *a,**k:None
    s=socketserver.TCPServer(("127.0.0.1",0),h); threading.Thread(target=s.serve_forever,daemon=True).start()
    return s.server_address[1]

RUN=r"""
([jitter])=>{
  ASSETS.ready=true; run.pilot='cole'; run.mode='arcade'; run.stage=1;
  beginStage(1); setState(GS.PLAY); player.reset(); player.invuln=1e9;
  player.x=240; player.y=430;

  /* the kinds eShoot/eShootT actually mint, plus the swirl missile which is set up by hand
     because only the black bomber's quad launch produces one */
  const KINDS=['mg','shell','dart','ice','flare','minigunT','chaingunT','bolt','emissile','groundup'];
  const out={};
  const SIM=1.4;                            // seconds of flight, identical in both arms

  const fly=(setup)=>{
    eBullets.length=0;
    setup();
    const b=eBullets[0]; if(!b) return null;
    const pts=[]; let t=0, i=0;
    while(t<SIM){
      /* jitter mirrors a real browser: mostly 60Hz with occasional long frames */
      const dt = jitter ? ((i%7===0)?1/22:(i%3===0)?1/48:1/72) : 1/60;
      t+=dt; i++;
      updateEBulletsOnly(dt);
      if(b.dead) break;
      pts.push([b.x,b.y]);
    }
    if(pts.length<3) return null;
    const [x0,y0]=pts[0], [x1,y1]=pts[pts.length-1];
    const dx=x1-x0, dy=y1-y0, L=Math.hypot(dx,dy)||1;
    let worst=0;
    for(const [px,py] of pts){
      const d=Math.abs((px-x0)*dy-(py-y0)*dx)/L;   // perpendicular distance to the chord
      if(d>worst) worst=d;
    }
    return {lateral:+worst.toFixed(2), n:pts.length,
            end:[Math.round(x1),Math.round(y1)]};
  };

  for(const k of KINDS){
    out[k]=fly(()=>{ eShoot(240, 90, Math.PI/2, 3.0, k); });
  }
  /* the swirl: the black bomber's quad launch, one round of it */
  out['emissile+swirl']=fly(()=>{
    eShoot(240, 90, Math.PI/2, 3.0, 'emissile');
    const b=eBullets[0]; if(b){ b._swirl=1; b._swPh=0; b._swAmp=1.15; }
  });
  return out;
}
"""

# updateEBulletsOnly does not exist in the game — the bullet loop lives inside updatePlay. Rather
# than carve it out (which would measure a copy, not the game), step the REAL loop and keep every
# other system quiet by clearing the pools it would otherwise fill.
SHIM=r"""
()=>{
  window.updateEBulletsOnly=function(dt){
    enemies.length=0; powerups.length=0;   // nothing else spawns or moves
    updatePlay(dt);
  };
  return true;
}
"""

from playwright.sync_api import sync_playwright
port=serve(GAME); url='http://127.0.0.1:%d/index.html'%port
with sync_playwright() as p:
    res={}
    for jit in (False, True):
        b=p.chromium.launch(args=['--disable-gpu','--no-sandbox','--mute-audio'])
        pg=b.new_page(viewport={'width':620,'height':900}, device_scale_factor=1)
        pg.goto(url, wait_until='load', timeout=60000)
        pg.wait_for_function("()=>typeof setState==='function'", timeout=45000)
        pg.wait_for_function("()=>(window.__bofFrames|0)>4", timeout=45000)
        pg.evaluate(SHIM)
        res['jit' if jit else 'steady']=pg.evaluate(RUN,[jit])
        b.close()
    print('%-16s %10s %10s %10s   %s' % ('kind','steady','jittered','drift',''))
    for k in res['steady']:
        a, c = res['steady'][k], res['jit'].get(k)
        if not a or not c:
            print('%-16s %10s' % (k, 'no flight')); continue
        drift=abs(c['lateral']-a['lateral'])
        flag=''
        if a['lateral']>1.5 and drift>a['lateral']*0.25: flag='<= SHAPE DEPENDS ON FRAME TIME'
        elif drift>2.0:                                  flag='<= drifts with frame time'
        print('%-16s %10.2f %10.2f %10.2f   %s' % (k, a['lateral'], c['lateral'], drift, flag))
