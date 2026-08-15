#!/usr/bin/env python3
"""probe_stageend.py - "end screen, shouldnt remain paused".

Mike's 4th screenshot is ordinary gameplay - a powerup on screen, explosions - with the map at its
bottom edge and nothing advancing. The suspicion is that the stage runs OUT OF SCROLL before its
boss triggers, so drawLevelMaster clamps srcY at 0 and the player is left flying over a still
background with no way forward.

Plays each stage long enough to reach the end and reports, per stage:
  when mapScroll saturates, if it does
  whether the boss / miniboss had triggered by then
  how many seconds are spent at full scroll with no boss on the field - the "paused" window
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
(stage)=>{
  ASSETS.ready=true; run.stage=stage; run.pilot='cole';
  try{ beginStage(stage); }catch(e){}
  setState(GS.PLAY); player.reset(); player.invuln=999999;
  if(typeof seedWaves==='function'){ try{ seedWaves(20260815); }catch(e){} }

  const cfg=_levelCfg(stage)||_levelCfg();
  const mk=stageMasterKey(cfg);
  XART.rdy(mk);                       // start the decode; range is read after the warm wait
  let range=0;

  let satAt=null, satFrames=0, pausedFrames=0, bossAt=null, subAt=null, leftPlay=null, subDoneAt=null;
  const SEC=60;
  for(let f=0; f<SEC*220; f++){
    player.invuln=999999; player.hp=99;
    /* AND IT HAS TO SHOOT. The miniboss HOLDS THE SCROLL until it dies (0801hn), so a probe that
       never fires freezes the level itself and then reports the level as frozen. */
    if(f%4===0){ try{ pShoot(); }catch(e){} }
    try{ updatePlay(1/60); }catch(e){ return {stage, err:String(e), f}; }
    /* THE SCROLL LIVES IN THE DRAW. drawLevelMaster is what advances mapScroll (its own comment
       says so), so a probe that only pumps updatePlay measures a stage that never moves - range 0,
       scroll 0, and a saturation test that can never fire. */
    try{ drawWorld(1/60); }catch(e){}
    if(state!==GS.PLAY && leftPlay===null) leftPlay={f:f, s:String(state)};
    if(bossActive && bossAt===null) bossAt=f;
    if(typeof subBossActive!=='undefined' && subBossActive && subAt===null) subAt=f;
    if(typeof subBossDone!=='undefined' && subBossDone && subDoneAt===null) subDoneAt=f;
    if(range===0){ const _im=XART.rdy(mk)?XART.get(mk):null; if(_im) range=Math.max(0,_im.naturalHeight-VH); }
    if(range>0 && mapScroll>=range-1){
      if(satAt===null) satAt=f;
      satFrames++;
      if(!bossActive && !(typeof subBossActive!=='undefined' && subBossActive)) pausedFrames++;
    }
    if(leftPlay) break;
  }
  return {stage, range:Math.round(range), scroll:Math.round(mapScroll),
          satAt, satSec:+(satFrames/60).toFixed(1), pausedSec:+(pausedFrames/60).toFixed(1),
          bossSec: bossAt===null?null:+(bossAt/60).toFixed(1),
          subSec:  subAt===null?null:+(subAt/60).toFixed(1),
          leftPlay, bossDefeated:!!bossDefeated,
          subDoneSec: subDoneAt===null?null:+(subDoneAt/60).toFixed(1)};
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

    print('%-3s %7s %7s %8s %8s %9s %9s  %s'
          % ('st', 'range', 'scroll', 'mini@s', 'boss@s', 'miniDone', 'PAUSED s', 'left PLAY'))
    for st in (1, 2):
        r = pg.evaluate(RUN, st)
        if r.get('err'):
            print('%-3d *** %s (frame %d)' % (st, r['err'], r['f'])); continue
        lp = r['leftPlay']
        print('%-3d %7d %7d %8s %8s %9s %9s  %s'
              % (r['stage'], r['range'], r['scroll'], r['subSec'], r['bossSec'],
                 r['subDoneSec'], r['pausedSec'],
                 ('%s @%.1fs' % (lp['s'], lp['f'] / 60)) if lp else 'NO - still in PLAY'))
    b.close()
