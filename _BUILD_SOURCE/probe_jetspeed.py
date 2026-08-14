#!/usr/bin/env python3
"""probe_jetspeed.py — does a jet actually fly at ONE airspeed?

CLAUDE.md has carried this as open for drops:

    "Jets: observed speed varies 96-138 even on `straight`; something outside jetTick displaces
     them. A rescale inside jetTick does not fix it - the other mover runs after."

Drop 0811o identified a candidate — the catch-all edge pin in the enemy update loop, which snapped
any unit outside [w*0.66, W-w*0.66] to that margin on its first tick, a teleport of up to 91px in
one frame — and gated it on _inField. **That identification was never verified against the speed
figure**, which is the whole reason this probe exists: a cause that explains a symptom is not the
same as a cause that removes it.

⚠ MEASURED AS PER-FRAME DISPLACEMENT / dt, not as a velocity field read off the unit. Reading e.vx
would report what jetTick INTENDED and tell us nothing about what moved the jet afterwards — the
probe_seam.py mistake of recomputing the thing under test. This records where the unit WAS and
where it ENDED UP.

⚠ AND THE FIRST FRAME IS REPORTED SEPARATELY. A one-frame teleport at spawn is a different fault
from a jet that wobbles all the way down, and averaging them together hides both.
"""
import http.server, socketserver, threading, functools
GAME=r'C:/Users/Mdogg/Desktop/BOF-CODE/BulletsOfFury'
def serve(d):
    h=functools.partial(http.server.SimpleHTTPRequestHandler, directory=d); h.log_message=lambda *a,**k:None
    s=socketserver.TCPServer(("127.0.0.1",0),h); threading.Thread(target=s.serve_forever,daemon=True).start()
    return s.server_address[1]
RUN=r"""
([route, pinOn, sepOn])=>{
  /* ⚠ THE THIRD ARM EXISTS BECAUSE THE OBVIOUS SUSPECT IS MY OWN CODE. Curved routes still read
     60..128 against a 96 airspeed after the pin is gated, and enemySeparate (0811l) pushes units
     apart at up to SEP_CAP=130 px/s — which would land squarely in that range. A hypothesis that
     convenient has to be tested, not assumed. */
  window.__sepOff = !sepOn;
  let _s=20260811>>>0;
  Math.random=function(){ _s=(_s*1664525+1013904223)>>>0; return _s/4294967296; };
  ASSETS.ready=true; run.stage=1; run.pilot='cole'; run.mode='arcade';
  beginStage(1); setState(GS.PLAY); player.reset(); player.invuln=1e9;
  player.x=240; player.y=470;

  enemies.length=0; eBullets.length=0; pBullets.length=0;
  const sx=(route==='cornerLR')?40:(route==='cornerRL')?440:240;
  const e=spawnEnemy('s1jetdelta', sx, -30, {route});
  if(!e) return null;
  /* pinOn=false reproduces the pre-0811o behaviour by clearing the latch every frame, so the
     edge pin engages from tick one exactly as it used to. Same build, both arms. */
  const dt=1/60, spd=e._jspd||96;
  const obs=[]; let first=null, px=e.x, py=e.y;
  for(let i=0;i<60*6;i++){
    e._dodge=0; player.hp=99;
    if(!pinOn) e._inField=1;            // force the old always-on pin
    updatePlay(dt);
    if(e.dead) break;
    const d=Math.hypot(e.x-px, e.y-py)/dt;
    if(first===null) first=d; else obs.push(d);
    px=e.x; py=e.y;
    if(e.y>VH+60) break;
  }
  if(obs.length<10) return null;
  obs.sort((a,b)=>a-b);
  const mean=obs.reduce((a,b)=>a+b,0)/obs.length;
  return {route, nominal:spd, firstFrame:+first.toFixed(1),
          min:+obs[0].toFixed(1), max:+obs[obs.length-1].toFixed(1),
          p50:+obs[(obs.length*0.5)|0].toFixed(1),
          p95:+obs[(obs.length*0.95)|0].toFixed(1),
          mean:+mean.toFixed(1), n:obs.length};
}
"""
from playwright.sync_api import sync_playwright
port=serve(GAME); url='http://127.0.0.1:%d/index.html'%port
def page(p):
    b=p.chromium.launch(args=['--disable-gpu','--no-sandbox','--mute-audio'])
    pg=b.new_page(viewport={'width':620,'height':900}, device_scale_factor=1)
    pg.goto(url, wait_until='load', timeout=60000)
    pg.wait_for_function("()=>typeof setState==='function'", timeout=45000)
    pg.wait_for_function("()=>(window.__bofFrames|0)>4", timeout=45000)
    return b, pg
with sync_playwright() as p:
    print('%-10s %-8s %-4s %7s %7s %7s %7s %7s %9s' %
          ('route','pin','sep','nominal','min','p50','p95','max','frame 1'))
    for route in ('straight','curveL','cornerLR'):
        for pin,sep in ((False,True),(True,True),(True,False)):
            b, pg = page(p)
            r=pg.evaluate(RUN,[route,pin,sep])
            b.close()
            lbl=('gated' if pin else 'always')
            if not r: print('%-10s %-8s %-4s  no flight' % (route,lbl,'on' if sep else 'OFF')); continue
            flag=''
            if r['max']-r['min'] > r['nominal']*0.12: flag='  <= varies'
            print('%-10s %-8s %-4s %7d %7s %7s %7s %7s %9s%s' %
                  (route, lbl, 'on' if sep else 'OFF', r['nominal'],
                   r['min'], r['p50'], r['p95'], r['max'], r['firstFrame'], flag))
