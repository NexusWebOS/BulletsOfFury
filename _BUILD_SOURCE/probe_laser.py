#!/usr/bin/env python3
"""probe_laser.py — the five laser tiers, as art and as drawn.

Mike: "level 3 laser looks underwhelming and needs an upgrade. all the lasers need to have a
consistent yet upgradeable look as they advance in level."

Two questions, and they have different answers:

  1. WHAT IS THE ART. nlz_<lv>_b0..5 exists for all five levels. Rendered side by side, does the
     set read as one weapon getting stronger, or as five unrelated beams?
  2. WHAT REACHES THE SCREEN. The draw scales the art by the beam's own width, so a tier can have
     good art and still land thin. Reported as the drawn width per level.

⚠ nlz_<lv>_m0..5 — the muzzle flare the draw reaches for — IS NOT IN THE MANIFEST AT ANY LEVEL.
That block cannot ever have drawn. Counted here so the claim is measured, not asserted.
"""
import http.server, socketserver, threading, functools, base64, os
GAME=r'C:/Users/Mdogg/Desktop/BOF-CODE/BulletsOfFury'
OUT=os.path.join(GAME,'docs','proofs')
def serve(d):
    h=functools.partial(http.server.SimpleHTTPRequestHandler, directory=d); h.log_message=lambda *a,**k:None
    s=socketserver.TCPServer(("127.0.0.1",0),h); threading.Thread(target=s.serve_forever,daemon=True).start()
    return s.server_address[1]
RUN=r"""
()=>{
  const out=[];
  for(let lv=1;lv<=5;lv++){
    for(let f=0;f<6;f++){ XART.rdy('nlz_'+lv+'_b'+f); }
    XART.rdy('nlz_'+lv+'_m0');
  }
  return true;
}
"""
MEASURE=r"""
()=>{
  const rows=[];
  const CW=150, CH=300;
  const strip=document.createElement('canvas');
  strip.width=CW*5; strip.height=CH+30;
  const sg=strip.getContext('2d'); sg.imageSmoothingEnabled=false;
  sg.fillStyle='#0d1017'; sg.fillRect(0,0,strip.width,strip.height);

  for(let lv=1;lv<=5;lv++){
    const k='nlz_'+lv+'_b0';
    const has=XART.rdy(k);
    const r={lv, hasBeam:has, muzzle:XART.rdy('nlz_'+lv+'_m0')};
    if(has){
      const im=XART.get(k);
      r.src=im.naturalWidth+'x'+im.naturalHeight;
      /* how much INK, and how bright? a tier that reads as weak usually has either a narrower
         lit core or a dimmer one, and both are measurable rather than matters of taste */
      const c=document.createElement('canvas'); c.width=im.naturalWidth; c.height=im.naturalHeight;
      const g=c.getContext('2d'); g.drawImage(im,0,0);
      const d=g.getImageData(0,0,c.width,c.height).data;
      let ink=0, lum=0, wide=0;
      const mid=(c.height/2)|0;
      for(let i=0;i<d.length;i+=4){ if(d[i+3]>30){ ink++; lum+=0.30*d[i]+0.59*d[i+1]+0.11*d[i+2]; } }
      for(let x=0;x<c.width;x++){ if(d[(mid*c.width+x)*4+3]>30) wide++; }
      r.inkPct=+(100*ink/(c.width*c.height)).toFixed(1);
      r.meanLum=ink?+(lum/ink).toFixed(0):0;
      r.coreWidthPct=+(100*wide/c.width).toFixed(0);
      /* ⚠ AT THE WIDTH THE GAME ACTUALLY USES. The first cut of this drew every tier at a
         constant 14 and the strip made the five look identical in size — which nearly sent me
         off to "add" a width progression that already exists. pShoot sets beam.w = 14 + lv*4
         on every shot, so the real beam runs 18px at level 1 to 34px at level 5, and the draw
         renders the art at bw*1.6. A probe that invents its own scale is not showing the game. */
      const bw=Math.max(6, 14+lv*4);
      r.beamW=bw;
      const drawW=bw*1.6*2.2;                       // 2.2x magnifier so the strip is legible
      sg.drawImage(im, lv*CW-CW/2-drawW/2, 14, drawW, CH-20);
    }
    sg.fillStyle='#9fd0ff'; sg.font='12px monospace'; sg.textAlign='center';
    sg.fillText('LEVEL '+lv, lv*CW-CW/2, CH+22);
    rows.push(r);
  }
  return {rows, img:strip.toDataURL('image/png')};
}
"""
from playwright.sync_api import sync_playwright
os.makedirs(OUT, exist_ok=True)
port=serve(GAME); url='http://127.0.0.1:%d/index.html'%port
with sync_playwright() as p:
    b=p.chromium.launch(args=['--disable-gpu','--no-sandbox','--mute-audio'])
    pg=b.new_page(viewport={'width':620,'height':900}, device_scale_factor=1)
    pg.goto(url, wait_until='load', timeout=60000)
    pg.wait_for_function("()=>typeof setState==='function'", timeout=45000)
    pg.wait_for_function("()=>(window.__bofFrames|0)>4", timeout=45000)
    pg.evaluate(RUN)
    pg.wait_for_function("()=>XART.rdy('nlz_1_b0')", timeout=45000)
    pg.wait_for_timeout(2000)
    r=pg.evaluate(MEASURE)
    print('%-6s %-7s %-10s %7s %8s %10s %8s %8s' %
          ('level','beamW','src','ink%','meanLum','coreWidth%','muzzle','art'))
    for e in r['rows']:
        print('%-6s %-7s %-10s %7s %8s %9s%% %8s %8s' %
              (e['lv'], e.get('beamW','-'), e.get('src','-'), e.get('inkPct','-'),
               e.get('meanLum','-'), e.get('coreWidthPct','-'), e['muzzle'], e['hasBeam']))
    with open(os.path.join(OUT,'laser_tiers_0811w_before.png'),'wb') as fh:
        fh.write(base64.b64decode(r['img'].split(',',1)[1]))
    print('-> docs/proofs/laser_tiers_0811w_before.png')
    b.close()
