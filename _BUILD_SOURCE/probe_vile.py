#!/usr/bin/env python3
"""probe_vile.py - the stage-8 finale, one form at a time.

Mike: "4 forms, very tanky, attack pattern is the same through all 4 forms."

⚠ THE FORM IS DRIVEN BY DAMAGE, so a probe that pins HP to keep the fight alive never sees past
form 0 - and form 0 is deliberately the least threatening of the four (a cocoon that throws wall
volleys you walk through the gap of). Measuring the boss "at full health" therefore reports the
opener as if it were the whole fight, which is the same phase-gating trap that hid the X-strike and
the charge beam in 0812m. Each form is built explicitly here.

Reports per form: rounds per second, rounds actually reaching the player's row, the longest silence,
and whether the rotating rake ever arms.
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
(form)=>{
  ASSETS.ready=true; run.stage=8; run.pilot='cole';
  try{ beginStage(8); }catch(e){}
  setState(GS.PLAY); player.reset();
  player.x=VW/2; player.y=VH*0.80; player.invuln=999999; player.hp=999;
  enemies.length=0; pBullets.length=0; eBullets.length=0; subBoss=null; boss=null;
  try{ spawnBoss('vileexistence'); }catch(e){ return {err:String(e)}; }
  const b=boss; if(!b) return {err:'no boss'};
  bossActive=true; b.enter=false; b.entry=0; b.y=VH*0.24;
  try{ vileBuildForm(b, form); }catch(e){ return {err:'buildForm: '+String(e)}; }
  /* ⚠ buildModularBoss RE-ARMS THE POWER-ON. updateBoss returns early while `_be` is set - the
     boss is still assembling - so it never reaches its attack and every form measured as firing
     NOTHING. Clearing it is what makes this measure the FIGHT rather than the entrance. */
  b._be=null; b.enter=false; b.entry=0; b._morphT=null; b.fireCd=0.3;

  const SEC=45, F=SEC*60;
  let shots=0, threat=0, dry=0, worstDry=0, rakeF=0;
  const seen=new WeakSet();
  for(let f=0;f<F;f++){
    player.invuln=999999; player.hp=999;
    bossActive=true; b.hp=b.maxhp=999999;      // keep the fight alive; the FORM is set explicitly
    try{ updatePlay(1/60); }catch(e){ return {err:String(e), f}; }
    if(b._brk) rakeF++;
    let n=0;
    for(const x of eBullets){
      if(!seen.has(x)){ seen.add(x); shots++; n++; }
      if(!x.__t && Math.abs(x.x-player.x)<26 && Math.abs(x.y-player.y)<40){ x.__t=1; threat++; }
    }
    if(n===0){ dry++; if(dry>worstDry) worstDry=dry; } else dry=0;
  }
  return {form, name:b.name||'?', shots, sps:+(shots/SEC).toFixed(2),
          tps:+(threat/SEC).toFixed(2), dry:+(worstDry/60).toFixed(1),
          rakeSec:+(rakeF/60).toFixed(1)};
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
    pg.wait_for_timeout(3500)

    print('%-5s %-20s %7s %8s %9s %8s %8s' % ('form', 'name', 'shots', 'shots/s', 'threat/s', 'worstDry', 'rake s'))
    for form in range(4):
        r = pg.evaluate(RUN, form)
        if r.get('err'):
            print('%-5d *** %s' % (form, r['err'])); continue
        flag = ''
        if r['tps'] < 0.8:  flag += '  *** barely threatens'
        if r['dry'] >= 3.0: flag += '  *** %.1fs silent' % r['dry']
        print('%-5d %-20s %7d %8s %9s %8s %8s%s'
              % (form, r['name'][:20], r['shots'], r['sps'], r['tps'], r['dry'], r['rakeSec'], flag))
    b.close()
