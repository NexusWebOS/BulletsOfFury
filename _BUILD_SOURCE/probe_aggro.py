#!/usr/bin/env python3
"""probe_aggro.py - "make them a little bit more challenging and make them attack. same with my bosses."

Before changing any numbers, measure what each miniboss and boss actually DOES: how many rounds it
puts in the air per second, and how long the player can stand still in front of it untouched.

Both units are given a live player that does NOT shoot back, so the fight runs at full length and
the unit's own cadence is what is being measured rather than how fast a probe can kill it.

  SHOTS/s      enemy bullets created per second of the fight
  DRY s        longest stretch with nothing fired at all
  THREAT/s     rounds per second that actually pass through the player's column
"""
import http.server, socketserver, threading, functools
GAME = r'C:/Users/Mdogg/Desktop/BOF-CODE/BulletsOfFury'

def serve(d):
    h = functools.partial(http.server.SimpleHTTPRequestHandler, directory=d)
    h.log_message = lambda *a, **k: None
    s = socketserver.TCPServer(("127.0.0.1", 0), h)
    threading.Thread(target=s.serve_forever, daemon=True).start()
    return s.server_address[1]

RUN = r"""
([stage, which])=>{
  ASSETS.ready=true; run.stage=stage; run.pilot='cole';
  try{ beginStage(stage); }catch(e){}
  setState(GS.PLAY); player.reset();
  player.x=VW/2; player.y=VH*0.80; player.invuln=999999; player.hp=999;
  enemies.length=0; pBullets.length=0; eBullets.length=0;
  boss=null; bossActive=false; subBoss=null; subBossActive=false;

  let unit=null, name=null;
  if(which==='mini'){
    subBossDone=false; subBossTriggered=false;
    try{ spawnSubBoss__inner((SUBBOSS[stage]||{}).kind); }catch(e){ return {err:String(e)}; }
    unit=subBoss; name=unit&&unit.name;
  } else {
    try{ spawnBoss(STAGES[stage-1] && STAGES[stage-1].boss); }catch(e){ return {err:String(e)}; }
    unit=boss; bossActive=true; name=unit&&unit.name;
  }
  if(!unit) return {err:'no unit'};
  unit.hp=unit.maxhp=999999;              // the fight must not end early
  unit.x=VW/2; unit.y=VH*0.28; unit.ty=VH*0.28; unit.enter=false; unit.entry=0;

  const SEC=45, F=SEC*60;
  let shots=0, dry=0, worstDry=0, threat=0;
  let seen=new WeakSet();
  for(let f=0; f<F; f++){
    player.invuln=999999; player.hp=999;
    if(which==='mini'){ subBossActive=true; if(subBoss) subBoss.hp=999999; }
    else { bossActive=true; if(boss) boss.hp=999999; }
    try{ updatePlay(1/60); }catch(e){ return {err:String(e), f}; }
    let newThisFrame=0;
    for(const b of eBullets){
      if(!seen.has(b)){ seen.add(b); shots++; newThisFrame++; }
      /* [!] THREAT MUST BE MEASURED WHERE THE BULLET ARRIVES, NOT WHERE IT IS BORN. Counting at
         creation asks "was it spawned in the player's column", which an AIMED round - fired from
         the boss, toward the player - can never satisfy. A round counts once, the first time it
         actually reaches the player's row within a body width. */
      if(!b.__thr && Math.abs(b.x-player.x)<26 && Math.abs(b.y-player.y)<40){ b.__thr=1; threat++; }
    }
    if(newThisFrame===0){ dry++; if(dry>worstDry) worstDry=dry; } else dry=0;
  }
  return {name:name, hp:unit.maxhp, shots, sps:+(shots/SEC).toFixed(2),
          dry:+(worstDry/60).toFixed(1), tps:+(threat/SEC).toFixed(2)};
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

    for which in ('mini', 'boss'):
        print('\n=== %s ===' % which.upper())
        print('%-3s %-24s %8s %8s %8s %8s' % ('st', 'name', 'shots', 'shots/s', 'threat/s', 'worstDry'))
        for st in range(1, 9):
            r = pg.evaluate(RUN, [st, which])
            if r.get('err'):
                print('%-3d *** %s' % (st, r['err'])); continue
            flag = ''
            if r['sps'] < 1.0:   flag += '  *** BARELY FIRES'
            if r['dry'] >= 4.0:  flag += '  *** %.1fs SILENT' % r['dry']
            print('%-3d %-24s %8d %8s %8s %8s%s'
                  % (st, (r['name'] or '?')[:24], r['shots'], r['sps'], r['tps'], r['dry'], flag))
    b.close()
