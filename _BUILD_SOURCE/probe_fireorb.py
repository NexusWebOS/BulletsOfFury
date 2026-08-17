#!/usr/bin/env python3
"""probe_fireorb.py - the INFERNO REAVER's charged fire orb.

Mike: "likes hes charging up a fire attack as an aura surrounds him, and then he releases it like
maverick would and a big ass fire orb comes flying andh homing at us, if we dodge out of its path
as it gets near us, it goes off screen and does not continue to home on the player."

Three claims, and the third is the one that makes it a dodge rather than a timer:

  IT CHARGES        b.flash must rise during the wind-up (the aura is the boss's own plate) and
                    nothing may be launched until FIREORB_CHARGE has elapsed.
  IT HOMES FAR      parked player, orb launched wide -> the miss distance must SHRINK.
  IT COMMITS NEAR   the player breaks sideways once the orb is inside FIREORB_COMMIT. The orb must
                    then leave the world WITHOUT re-acquiring. Measured as: does it ever get close
                    again after the break, and does it exit.

⚠ eBullets IS REASSIGNED, not mutated - the orb is re-found from the pool each frame by identity.
"""
import http.server, socketserver, threading, functools, math
GAME = r'C:/Users/Mdogg/Desktop/BOF-CODE/BulletsOfFury'

def serve(d):
    h = functools.partial(http.server.SimpleHTTPRequestHandler, directory=d)
    h.log_message = lambda *a, **k: None
    s = socketserver.TCPServer(("127.0.0.1", 0), h)
    threading.Thread(target=s.serve_forever, daemon=True).start()
    return s.server_address[1]

RUN = r"""
(dodge)=>{
  ASSETS.ready=true; run.stage=2; run.pilot='cole';
  try{ beginStage(2); }catch(e){}
  setState(GS.PLAY); player.reset();
  player.x=VW*0.5; player.y=VH*0.80; player.invuln=999999; player.hp=999; player.dead=false;
  enemies.length=0; pBullets.length=0; eBullets.length=0; boss=null; subBoss=null;
  try{ spawnBoss('infernoreaver'); }catch(e){ return {err:String(e)}; }
  const b=boss; if(!b) return {err:'no boss'};
  bossActive=true; b._be=null; b.enter=false; b.entry=0; b.x=VW*0.5; b.y=VH*0.20;

  /* drive the wind-up directly - the pattern picker would take an unknown number of volleys */
  const flash0=b.flash||0;
  reaverOrbStart(b);
  let flashPeak=0, launchT=null, orb=null;
  for(let f=0; f<60*3 && !orb; f++){
    b.hp=b.maxhp=999999; bossActive=true;
    reaverOrbTick(b, 1/60);
    flashPeak=Math.max(flashPeak, b.flash||0);
    for(const x of eBullets){ if(x.kind==='fireorb'){ orb=x; launchT=f/60; break; } }
  }
  if(!orb) return {err:'no orb launched'};

  const out={charge:+launchT.toFixed(2), flashPeak:+flashPeak.toFixed(3),
             pal:orb.pal||null, fx:orb._fx||null, szMul:orb.szMul||null,
             w:orb.w, spd:orb.spd};

  /* push it wide so there is something to home ONTO */
  orb.x=VW*0.5; orb.y=VH*0.30;
  player.x=VW*0.18; player.y=VH*0.80;
  const sp=orb.spd||2.6;
  orb.vx=0; orb.vy=sp; orb.ang=Math.PI/2; orb._committed=false;

  const D=()=>Math.sqrt((player.x-orb.x)*(player.x-orb.x)+(player.y-orb.y)*(player.y-orb.y));
  const d0=D();
  let dMin=d0, committedAt=null, broke=false, dAfterBreak=null, exited=false, frames=0;
  for(let f=0; f<60*10; f++){
    frames=f;
    player.invuln=999999; player.hp=999; player.dead=false;
    bossActive=true; b.hp=b.maxhp=999999;
    /* THE BREAK: once it has committed, run sideways. A shot that keeps homing will turn back. */
    if(dodge && orb._committed && !broke){ broke=true; }
    if(broke){ player.x=Math.max(20, Math.min(VW-20, player.x + 5.0)); }
    try{ updatePlay(1/60); }catch(e){ return {err:'updatePlay: '+String(e)}; }
    let still=null; for(const x of eBullets){ if(x===orb){ still=x; break; } }
    if(!still){ exited=true; break; }
    const d=D();
    if(d<dMin) dMin=d;
    if(orb._committed && committedAt==null) committedAt=+d.toFixed(0);
    if(broke){ dAfterBreak = (dAfterBreak==null) ? d : Math.min(dAfterBreak, d); }
    if(orb.y>VH+80 || orb.y<-80 || orb.x<-80 || orb.x>VW+80){ exited=true; break; }
  }
  out.d0=+d0.toFixed(0); out.dMin=+dMin.toFixed(0);
  out.committedAt=committedAt; out.exited=exited; out.sec=+(frames/60).toFixed(1);
  out.dAfterBreak=(dAfterBreak==null?null:+dAfterBreak.toFixed(0));
  out.commitR=(typeof FIREORB_COMMIT==='number')?FIREORB_COMMIT:null;
  return out;
}
"""

from playwright.sync_api import sync_playwright
port = serve(GAME)
with sync_playwright() as p:
    br = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
    pg = br.new_page(viewport={'width': 620, 'height': 900}, device_scale_factor=1)
    errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=60000)
    pg.wait_for_function("()=>typeof setState==='function'", timeout=45000)
    pg.wait_for_function("()=>(window.__bofFrames|0)>4", timeout=45000)
    pg.wait_for_timeout(3000)

    bad = 0
    for dodge in (False, True):
        r = pg.evaluate(RUN, dodge)
        print('\n=== %s ===' % ('PLAYER BREAKS LATE' if dodge else 'PLAYER HOLDS STILL'))
        if r.get('err'):
            print('  *** %s' % r['err']); bad += 1; continue
        if not dodge:
            print('  wind-up            %ss   (aura peak b.flash %s)' % (r['charge'], r['flashPeak']))
            print('  orb art            _fx=%s pal=%s szMul=%s w=%s' % (r['fx'], r['pal'], r['szMul'], r['w']))
            if r['pal'] == 'red':
                print('  *** RED - Mike ruled red out on the lava stage'); bad += 1
            if r['charge'] < 0.5:
                print('  *** no readable wind-up'); bad += 1
            if r['flashPeak'] <= 0:
                print('  *** no aura - b.flash never rose'); bad += 1
        print('  miss distance      start %s -> closest %s   (commit radius %s)'
              % (r['d0'], r['dMin'], r['commitR']))
        print('  committed at       %s px' % r['committedAt'])
        print('  left the world     %s  after %ss' % (r['exited'], r['sec']))
        if not dodge:
            if r['dMin'] >= r['d0']:
                print('  *** it never closed - it is not homing at all'); bad += 1
        else:
            print('  closest AFTER the break: %s' % r['dAfterBreak'])
            if r['committedAt'] is None:
                print('  *** it never committed - it would track forever'); bad += 1
            elif not r['exited']:
                print('  *** it did not leave - still chasing'); bad += 1

    if errs: print('\nPAGE ERRORS: %s' % errs[:3])
    print('\n%s' % ('the orb homes, commits and leaves' if bad == 0 else '*** %d problem(s)' % bad))
    br.close()
