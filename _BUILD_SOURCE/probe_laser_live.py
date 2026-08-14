#!/usr/bin/env python3
"""probe_laser_live.py — the five laser tiers as the GAME draws them.

probe_laser.py measures the authored plates. This drives the real weapon: sets the laser to each
level, fires it through pShoot, steps a real frame, and crops the beam off the live canvas.

⚠ IT DRIVES pShoot RATHER THAN PUSHING A BEAM BY HAND. CLAUDE.md: "The player never fires in
shoot.py — firing needs an input tap the harness does not simulate, so pBullets stays empty and any
weapon FX measures as dead. A test must call pShoot() itself." A hand-built beam object would also
skip pShoot's `beam.w = 14 + lv*4`, which is the width the whole tiering rests on — the probe would
then be measuring its own assumptions.

Reports the lit width at each tier so "upgradeable" is a number, not an impression: how many pixels
across the beam's own row are brighter than the background.
"""
import http.server, socketserver, threading, functools, base64, os
GAME=r'C:/Users/Mdogg/Desktop/BOF-CODE/BulletsOfFury'
OUT=os.path.join(GAME,'docs','proofs')
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
  /* fire through the real weapon path, then draw the real frame */
  for(let i=0;i<3;i++){ pShoot(); updatePlay(1/60); try{ drawWorld(1/60); }catch(e){} }
  const beam=pBullets.filter(b=>b.kind==='beam')[0]||null;

  const cv=document.getElementById('screen');
  const g=cv.getContext('2d');
  const SX=cv.width/VW, SY=cv.height/VH;
  const row=Math.round(240*SY);
  const withBeam=g.getImageData(0,row,cv.width,1).data;
  /* ⚠ NO FRAME DIFFING. Two draws of the same tick do NOT match in this renderer - it reads
     performance.now() directly for water frames, clouds and scanlines - so a with/without diff
     lit up the whole 480px row at every tier. That is documented in CLAUDE.md from drop 0811m
     and I walked into it again here. The crop is the evidence; the numbers below are only the
     beam WIDTH the game set, which is read from the object rather than inferred from pixels. */
  let lit=0, peak=0, minX=1e9, maxX=-1;  /* crop centred on the beam the game actually drew, not on where we assumed it would be */
  const cx=(maxX<0)?Math.round(240*SX):Math.round((minX+maxX)/2);
  const c2=document.createElement('canvas'); c2.width=190; c2.height=300;
  const g2=c2.getContext('2d'); g2.imageSmoothingEnabled=false;
  g2.drawImage(cv, cx-95, Math.round(150*SY), 190, 300, 0,0,190,300);
  return {lv, beamW:beam?Math.round(beam.w):null, litPx:Math.round(lit/SX),
          spanPx:(maxX<0)?0:Math.round((maxX-minX)/SX),
          peakLum:Math.round(peak), crop:c2.toDataURL('image/png')};
}
"""
from playwright.sync_api import sync_playwright
os.makedirs(OUT, exist_ok=True)
port=serve(GAME); url='http://127.0.0.1:%d/index.html'%port
from PIL import Image
import io
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
    print('%-6s %8s %9s %9s %9s' % ('level','beam.w','lit px','span px','peak dL'))
    for lv in (1,2,3,4,5):
        r=pg.evaluate(SHOT,[lv])
        print('%-6s %8s %9s %9s %9s' % (r['lv'], r['beamW'], r['litPx'], r['spanPx'], r['peakLum']))
        crops.append(Image.open(io.BytesIO(base64.b64decode(r['crop'].split(',',1)[1]))))
    b.close()
    W=sum(c.width for c in crops); H=max(c.height for c in crops)
    strip=Image.new('RGB',(W,H),(13,16,23)); x=0
    for c in crops: strip.paste(c.convert('RGB'),(x,0)); x+=c.width
    strip.save(os.path.join(OUT,'laser_tiers_0811w_live.png'))
    print('-> docs/proofs/laser_tiers_0811w_live.png  (levels 1..5 left to right)')
