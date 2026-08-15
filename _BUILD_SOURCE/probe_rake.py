#!/usr/bin/env python3
"""probe_rake.py - the rotating beam rake.

Mike: "beams that rotate on the screen that kill you if you touch them, so you have to carefully
move while avoiding bullets between those beams too."

Three questions, and they are the ones that decide whether it is arcade or just cheap:

  DOES IT SWEEP?      the spokes must rotate, and not aim. Sampled angle over time, and the
                      player is moved between runs to prove the beam does not follow.
  IS THE WARM-UP SAFE? a hazard that bites before it is drawn is unreadable. Nothing may hit
                      during the 0.75s announce.
  IS THERE A GAP?     a standing player must eventually be swept (it works), and a player who
                      holds the middle of a corridor must survive a full rotation (it is fair).
                      Both matter - only the first would let a lethal wall pass.
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
([spokes, mode, px, py])=>{
  ASSETS.ready=true; run.stage=2; run.pilot='cole';
  try{ beginStage(2); }catch(e){}
  setState(GS.PLAY); player.reset();
  enemies.length=0; pBullets.length=0; eBullets.length=0; boss=null; subBoss=null;
  subBossDone=false; subBossTriggered=false;
  try{ spawnSubBoss__inner('siegeember'); }catch(e){ return {err:String(e)}; }
  const b=subBoss; if(!b) return {err:'no unit'};
  b.maxhp=b.hp=999999; b.enter=false; b.entry=0; b.x=VW/2; b.y=VH*0.22;
  subBossActive=true;

  player.x=px; player.y=py; player.invuln=0; player.hp=99; player.dead=false;

  beamRakeStart(b, spokes, 0.8, 5.0);
  const angs=[]; let hits=0, warmHits=0, liveFrames=0, minPerp=null;
  const R0=b._brk;
  for(let f=0; f<60*7; f++){
    b.x=VW/2; b.y=VH*0.22;                 // hold the hub still: this measures the RAKE, not the drift
    player.x=px; player.y=py;              // and hold the player, so a hit means the beam swept onto them
    /* [!] playerHit() SETS player.dead - it does NOT touch invuln, hp, shield or lives on a
       no-shield hit. Watching invuln/hp reported ZERO hits while the beams were passing 0.3px from
       the player, i.e. straight through them. The observable is `dead`. */
    const dead0=player.dead;
    if(b._brk) beamRakeTick(b, 1/60);
    const warm = b._brk ? (b._brk.t < b._brk.warm) : false;
    if(player.dead && !dead0){ if(warm) warmHits++; else hits++; player.dead=false; player.invuln=0; player.hp=99; }
    if(b._brk && !warm){ liveFrames++; if(f%18===0) angs.push(+(b._brk.ang).toFixed(2));
      /* DIAGNOSTIC: the closest any spoke came, in the same terms beamRakeTick uses. If this stays
         large the geometry is wrong; if it goes below the threshold and there is still no hit, the
         damage call is. */
      const ox=b.x, oy=(b._drawY!=null?b._drawY:b.y);
      const pxr=player.x-ox, pyr=player.y-oy;
      for(let i=0;i<b._brk.n;i++){
        const a2=b._brk.ang + i*(Math.PI*2/b._brk.n);
        const dx=Math.cos(a2), dy=Math.sin(a2);
        const proj=pxr*dx+pyr*dy; if(proj<0||proj>b._brk.len) continue;
        const perp=Math.abs(pxr*dy-pyr*dx);
        if(minPerp==null||perp<minPerp) minPerp=perp;
      }
    }
    if(!b._brk) break;
  }
  return {spokes, mode, hits, warmHits, minPerp:(minPerp==null?null:+minPerp.toFixed(1)), liveSec:+(liveFrames/60).toFixed(1), angs:angs.slice(0,8)};
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
    pg.wait_for_timeout(3000)

    VW, VH = pg.evaluate("()=>[VW,VH]")
    print('%-8s %-22s %6s %9s %8s  %s' % ('spokes', 'player at', 'hits', 'warm-hits', 'live s', 'angle samples'))
    bad = 0
    for spokes in (3, 5):
        for label, px, py in (('dead centre-low', VW / 2, VH * 0.78),
                              ('far left edge',   28,     VH * 0.86),
                              ('hard right edge', VW - 28, VH * 0.86)):
            r = pg.evaluate(RUN, [spokes, label, px, py])
            if r.get('err'):
                print('%-8d %-22s ERR %s' % (spokes, label, r['err'])); bad += 1; continue
            print('%-8d %-22s %6d %9d %8s  minPerp=%s  %s'
                  % (spokes, label, r['hits'], r['warmHits'], r['liveSec'], r['minPerp'], r['angs'][:4]))
            if r['warmHits'] > 0:
                print('         *** THE WARM-UP IS LETHAL — the announce has to be safe'); bad += 1
            if len(set(r['angs'])) < 3:
                print('         *** IT IS NOT ROTATING'); bad += 1
    print('\n%s' % ('rake reads as arcade' if bad == 0 else '*** %d problem(s)' % bad))
    b.close()
