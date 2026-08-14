#!/usr/bin/env python3
"""probe_laser_live.py — the five laser tiers as the GAME draws them.

probe_laser.py measures the authored plates. This drives the real weapon: sets the laser to each
level, fires it through pShoot, steps real frames, and crops the beam off the live canvas.

⚠ IT DRIVES pShoot RATHER THAN PUSHING A BEAM BY HAND. CLAUDE.md: "The player never fires in
shoot.py — firing needs an input tap the harness does not simulate, so pBullets stays empty and any
weapon FX measures as dead. A test must call pShoot() itself." A hand-built beam would also skip
pShoot's `beam.w = 14 + lv*4`, which is the width the tiering rests on, so the probe would be
measuring its own assumptions.

⚠ NO FRAME DIFFING. Two draws of the same tick do NOT match in this renderer — drawWorld reads
performance.now() directly for water frames, clouds and scanlines — so a with/without diff lit up
the whole 480px row at every tier and reported nothing. Documented in CLAUDE.md at drop 0811m, and
walked into again at 0811w. **The crop is the evidence.** The only number quoted is beam.w, read
off the object rather than inferred from pixels.

Run with --tag NAME to write docs/proofs/laser_tiers_<NAME>.png.
"""
import http.server, socketserver, threading, functools, base64, os, sys, io
GAME=r'C:/Users/Mdogg/Desktop/BOF-CODE/BulletsOfFury'
OUT=os.path.join(GAME,'docs','proofs')
TAG='live'
if '--tag' in sys.argv: TAG=sys.argv[sys.argv.index('--tag')+1]

def serve(d):
    h=functools.partial(http.server.SimpleHTTPRequestHandler, directory=d); h.log_message=lambda *a,**k:None
    s=socketserver.TCPServer(("127.0.0.1",0),h); threading.Thread(target=s.serve_forever,daemon=True).start()
    return s.server_address[1]

SETUP=r"""
()=>{
  ASSETS.ready=true; run.pilot='cole'; run.mode='arcade'; run.stage=1;
  beginStage(1); setState(GS.PLAY); player.reset(); player.invuln=1e9;
  for(let lv=1;lv<=5;lv++) for(let f=0;f<6;f++) XART.rdy('nlz_'+lv+'_b'+f);
  return true;
}
"""

SHOT=r"""
([lv])=>{
  run.weapon=3; run.wlevels=run.wlevels||{}; run.wlevels[3]=lv; run.wlevel=lv;
  player.x=240; player.y=400; player.invuln=1e9;
  enemies.length=0; eBullets.length=0; pBullets.length=0;
  /* ⚠ CLEAR THE FIRE COOLDOWN BETWEEN TIERS. This walks all five levels on ONE page and pShoot
     early-returns while player.fireCd is counting down, so the first tiers produced no beam and
     their crops came back as bare terrain. That looked like "levels 1 and 2 do not draw" — a game
     bug that does not exist. State carried between iterations, exactly the way the suite's own
     order-dependent fixtures do. */
  player.fireCd=0; player.dead=false;
  let beam=null;
  for(let i=0;i<24 && !beam;i++){
    player.fireCd=0; pShoot();
    updatePlay(1/60); try{ drawWorld(1/60); }catch(e){}
    beam=pBullets.filter(b=>b.kind==='beam')[0]||null;
  }
  if(!beam) return {lv, beamW:null, crop:null, fired:false};
  for(let i=0;i<4;i++){ player.fireCd=0; pShoot(); updatePlay(1/60); try{ drawWorld(1/60); }catch(e){} }

  const cv=document.getElementById('screen');
  const SX=cv.width/VW, SY=cv.height/VH;
  /* ⚠ THE BEAM IS AT A WORLD x AND THE CANVAS IS IN SCREEN SPACE. drawWorld runs under
     translate(-camX), so cropping at beam.x without subtracting camX frames the wrong column —
     which is why earlier strips showed terrain where a beam should have been. Same world-vs-screen
     fault this file records for the launch seam, the outbound routes and the dialogue window. */
  const camx=(typeof camX!=='undefined')?camX:0;
  const cx=Math.round((beam.x-camx)*SX);
  const c2=document.createElement('canvas'); c2.width=190; c2.height=320;
  const g2=c2.getContext('2d'); g2.imageSmoothingEnabled=false;
  g2.fillStyle='#0d1017'; g2.fillRect(0,0,190,320);
  g2.drawImage(cv, cx-95, Math.round(60*SY), 190, 320, 0,0,190,320);
  return {lv, beamW:Math.round(beam.w), crop:c2.toDataURL('image/png'), fired:true};
}
"""

from playwright.sync_api import sync_playwright
from PIL import Image
os.makedirs(OUT, exist_ok=True)
port=serve(GAME); url='http://127.0.0.1:%d/index.html'%port
with sync_playwright() as p:
    b=p.chromium.launch(args=['--disable-gpu','--no-sandbox','--mute-audio'])
    pg=b.new_page(viewport={'width':620,'height':900}, device_scale_factor=1)
    pg.goto(url, wait_until='load', timeout=60000)
    pg.wait_for_function("()=>typeof setState==='function'", timeout=45000)
    pg.wait_for_function("()=>(window.__bofFrames|0)>4", timeout=45000)
    pg.evaluate(SETUP)
    pg.wait_for_function("()=>XART.rdy('nlz_3_b0')", timeout=45000)
    pg.wait_for_timeout(1500)
    crops=[]
    print('%-6s %8s %8s' % ('level','beam.w','fired'))
    for lv in (1,2,3,4,5):
        r=pg.evaluate(SHOT,[lv])
        print('%-6s %8s %8s' % (r['lv'], r['beamW'], r['fired']))
        if r['crop']:
            crops.append(Image.open(io.BytesIO(base64.b64decode(r['crop'].split(',',1)[1]))))
    b.close()
    if crops:
        W=sum(c.width for c in crops); H=max(c.height for c in crops)
        strip=Image.new('RGB',(W,H),(13,16,23)); x=0
        for c in crops: strip.paste(c.convert('RGB'),(x,0)); x+=c.width
        name='laser_tiers_%s.png'%TAG
        strip.save(os.path.join(OUT,name))
        print('-> docs/proofs/%s  (levels 1..5 left to right)'%name)
