#!/usr/bin/env python3
"""probe_manoeuvre.py - do the ship bosses actually charge, cross and ram?

Mike: "I wanna see our jet mini bosses and bosses charge at us, and then do in-game off screen on
screen x pattern strikes where we have to avoid them, then they try to do a vertical south,
vertical north, vertical south aggresively like they are trying to ram into us."

Runs each ship boss and miniboss for 70 seconds and reports how long it spends in each manoeuvre
state, how far it travels vertically, and how long the charge-beam telegraph is up.

⚠ HP FRACTION PICKS BOTH THE ATTACK AND THE MANOEUVRE. shipBossPhase reads hp/maxhp, and both the
pattern list and shipBossPickMove are indexed off it - so a unit pinned at FULL health only ever
shows phase 0, which has no X-strike and no charge beam. Held at a chosen fraction per run, or the
probe reports two working features as missing.
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
([stage, which, frac])=>{
  ASSETS.ready=true; run.stage=stage; run.pilot='cole';
  try{ beginStage(stage); }catch(e){}
  setState(GS.PLAY); player.reset();
  player.x=VW/2; player.y=VH*0.80; player.invuln=999999; player.hp=999;
  enemies.length=0; pBullets.length=0; eBullets.length=0; boss=null; subBoss=null;
  let u=null;
  if(which==='mini'){
    subBossDone=false; subBossTriggered=false;
    try{ spawnSubBoss__inner((SUBBOSS[stage]||{}).kind); }catch(e){ return {err:String(e)}; }
    u=subBoss;
  } else {
    try{ spawnBoss(STAGES[stage-1].boss); }catch(e){ return {err:String(e)}; }
    u=boss; bossActive=true;
  }
  if(!u) return {err:'no unit'};
  if(!u._ship) return {skip:1, name:u.name||'?'};
  u.maxhp=999999; u.hp=Math.round(u.maxhp*frac); u.enter=false; u.entry=0;

  const seen={}; let minY=1e9, maxY=-1e9, off=0, beam=0, msl=0;
  const seenB=new WeakSet();
  for(let f=0; f<60*70; f++){
    player.invuln=999999; player.hp=999;
    if(which==='mini'){ subBossActive=true; subBoss.hp=Math.round(subBoss.maxhp*frac); }
    else { bossActive=true; boss.hp=Math.round(boss.maxhp*frac); }
    try{ updatePlay(1/60); }catch(e){ return {err:String(e), f}; }
    if(u._sbm!=null) seen[u._sbm]=(seen[u._sbm]||0)+1;
    if(u._cbT!=null) beam++;
    for(const b of eBullets){ if(!seenB.has(b)){ seenB.add(b); if(b.kind==='emissile'||b.kind==='erocket') msl++; } }
    if(u.y<minY) minY=u.y;
    if(u.y>maxY) maxY=u.y;
    if(u.y<-10 || u.y>VH+10) off++;
  }
  return {name:u.name||'?', states:seen, minY:Math.round(minY), maxY:Math.round(maxY),
          offSec:+(off/60).toFixed(1), beamSec:+(beam/60).toFixed(1), missiles:msl};
}
"""

NAMES = {0: 'hold', 1: 'tell', 2: 'charge', 3: 'XSTRIKE', 4: 'ram', 5: 'recover'}

from playwright.sync_api import sync_playwright
port = serve(GAME)
with sync_playwright() as p:
    b  = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
    pg = b.new_page(viewport={'width': 620, 'height': 900}, device_scale_factor=1)
    pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=60000)
    pg.wait_for_function("()=>typeof setState==='function'", timeout=45000)
    pg.wait_for_function("()=>(window.__bofFrames|0)>4", timeout=45000)
    pg.wait_for_timeout(3000)

    for frac, label in ((0.95, 'PHASE 0 (fresh)'), (0.45, 'PHASE 1 (hurt)'), (0.12, 'PHASE 2 (dying)')):
        print('\n=== %s ===' % label)
        for which, st in (('mini', 2), ('mini', 4), ('boss', 2), ('boss', 5)):
            r = pg.evaluate(RUN, [st, which, frac])
            if r.get('err'):    print('%-5s st%d ERR %s' % (which, st, r['err'])); continue
            if r.get('skip'):   print('%-5s st%d not a ship boss (%s)' % (which, st, r.get('name'))); continue
            stt = '  '.join('%s %.0fs' % (NAMES.get(int(k), k), v / 60)
                            for k, v in sorted(r['states'].items(), key=lambda x: int(x[0])))
            print('%-5s st%d %-20s y %4d..%4d off %4.1fs beam %4.1fs msl %3d | %s'
                  % (which, st, r['name'][:20], r['minY'], r['maxY'], r['offSec'], r['beamSec'], r['missiles'], stt))
    b.close()
