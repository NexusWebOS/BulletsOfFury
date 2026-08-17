#!/usr/bin/env python3
"""probe_carrier.py - the Doomsday Carrier's bay launch, deflection, and rising tide.

Mike: "those rockets should be projectiles that shoot forward via the animation finish so it looks
part of it and fluid ... the missle bays are to be destroyable, the missiles can be shot and
deflected back at the boss, as this is the only way to destroy the missile bays, and through gravity
as it constantly shoots missiles, they begin to float and row up and fill the screen if you dont."

Four claims, each measured separately because each can fail on its own:

  THE REEL DRIVES THE ROUND   the warhead must appear on the LAUNCH frame, not on a timer. Sampled
                              as: what animation frame was showing when a new round first existed.
  BAYS RESIST NORMAL FIRE     shooting the hull must NOT reduce bay hp. If it does, the whole
                              deflection mechanic is bypassable and the fight is brute-forceable.
  DEFLECTION IS THE KILL      a round shot by the player must flip to _ref, travel UP, and reduce a
                              bay on contact.
  THE TIDE RISES              rounds left alone must stop descending and gain altitude near the
                              floor, so the screen fills.

⚠ eBullets IS REASSIGNED, not mutated - rounds are tracked by identity.
"""
import http.server, socketserver, threading, functools
GAME = r'C:/Users/Mdogg/Desktop/BOF-CODE/BulletsOfFury'

def serve(d):
    h = functools.partial(http.server.SimpleHTTPRequestHandler, directory=d)
    h.log_message = lambda *a, **k: None
    s = socketserver.TCPServer(("127.0.0.1", 0), h)
    threading.Thread(target=s.serve_forever, daemon=True).start()
    return s.server_address[1]

SETUP = r"""
()=>{
  ASSETS.ready=true; run.stage=6; run.pilot='cole';
  try{ beginStage(6); }catch(e){} try{ warmStage(6); }catch(e){}
  setState(GS.PLAY); player.reset();
  player.x=VW/2; player.y=VH*0.82; player.invuln=999999; player.hp=999; player.dead=false;
  enemies.length=0; pBullets.length=0; eBullets.length=0; boss=null; subBoss=null;
  try{ spawnBoss('doomsdaycarrier'); }catch(e){ return {err:String(e)}; }
  if(!boss) return {err:'no boss'};
  const b=boss; bossActive=true; b._be=null; b.enter=false; b.entry=0; b._morphT=null;
  b.x=VW/2; b.y=VH*0.22; b.hp=b.maxhp=999999;
  const D=SHIPBOSS.doomsdaycarrier;
  for(let i=0;i<D.launch.frames;i++) XART.rdy(D.launch.pre+String(i).padStart(2,'0'));
  XART.rdy('nfx_omegawarhead_in'); XART.rdy('nfx_omegawarhead_ref');
  return {ok:true, release:D.launch.release, frames:D.launch.frames};
}
"""

RUN = r"""
(mode)=>{
  const b=boss; if(!b) return {err:'no boss'};
  const D=SHIPBOSS.doomsdaycarrier, L=D.launch;
  const out={launchFrames:[], bayL0:b._bay?b._bay.L:null};
  const seen=new WeakSet();
  let deflected=0, rose=0, maxRise=0;
  for(let f=0; f<60*26; f++){
    player.invuln=999999; player.hp=999; player.dead=false;
    b.x=VW/2; b.y=VH*0.22; bossActive=true; b.hp=b.maxhp=999999;
    if(mode==='hullfire'){
      /* pour damage into the HULL - bays must not care */
      try{ hitBoss(40); }catch(e){}
    }
    try{ updatePlay(1/60); }catch(e){ return {err:'updatePlay: '+String(e), f}; }
    for(const w of eBullets){
      if(w.kind!=='omegawarhead') continue;
      if(!seen.has(w)){
        seen.add(w);
        out.launchFrames.push(b._lc?b._lc.f:-1);     // frame showing when the round appeared
      }
      if(mode==='deflect' && !w._ref && w.y>VH*0.42){
        /* stand in for the player's gun: put a bullet on it */
        pBullets.push({x:w.x, y:w.y, vx:0, vy:-8, w:6, h:10, dmg:4, kind:'mg', t:0});
      }
      if(w._ref) deflected++;
      if(mode==='ignore' && w._buoy){ rose++; if(-w.vy>maxRise) maxRise=-w.vy; }
    }
  }
  out.bayL=b._bay?b._bay.L:null; out.bayR=b._bay?b._bay.R:null;
  out.deflectedFrames=deflected; out.roseFrames=rose; out.maxRise=+maxRise.toFixed(2);
  out.onScreen=eBullets.filter(function(w){return w.kind==='omegawarhead';}).length;
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
    pg.wait_for_timeout(3500)

    bad = 0
    for mode, label in (('ignore', 'left alone'), ('deflect', 'player shoots them'), ('hullfire', 'hull under fire')):
        s0 = pg.evaluate(SETUP)
        if s0.get('err'):
            print('setup ERR %s' % s0['err']); bad += 1; break
        r = pg.evaluate(RUN, mode)
        if r.get('err'):
            print('%-20s ERR %s' % (label, r['err'])); bad += 1; continue
        lf = r['launchFrames']
        print('\n=== %s ===' % label.upper())
        print('  rounds launched      %d   on animation frame(s) %s  (release frame is %s)'
              % (len(lf), sorted(set(lf))[:6], s0['release']))
        if lf and any(f < s0['release'] for f in lf):
            print('  *** a round appeared BEFORE the launch frame - it is on a timer, not the reel')
            bad += 1
        print('  bays  L %s  R %s   (started at %s each)' % (r['bayL'], r['bayR'], r['bayL0']))
        if mode == 'hullfire':
            if r['bayL'] != r['bayL0'] or r['bayR'] != r['bayL0']:
                print('  *** HULL FIRE DAMAGED A BAY - deflection is meant to be the only way'); bad += 1
            else:
                print('  hull fire left both bays intact, as intended')
        if mode == 'deflect':
            print('  deflected round-frames %d' % r['deflectedFrames'])
            if r['deflectedFrames'] == 0:
                print('  *** nothing ever deflected'); bad += 1
            elif r['bayL'] >= r['bayL0'] and r['bayR'] >= r['bayL0']:
                print('  *** rounds deflected but no bay took damage'); bad += 1
            else:
                print('  deflected rounds destroyed bay hp - the intended kill path works')
        if mode == 'ignore':
            print('  round-frames spent rising %d   fastest rise %s px/frame   still on screen %d'
                  % (r['roseFrames'], r['maxRise'], r['onScreen']))
            if r['roseFrames'] == 0:
                print('  *** nothing ever became buoyant - the tide does not build'); bad += 1

    if errs: print('\nPAGE ERRORS: %s' % errs[:3])
    print('\n%s' % ('the carrier fight behaves as specified' if bad == 0 else '*** %d problem(s)' % bad))
    br.close()
