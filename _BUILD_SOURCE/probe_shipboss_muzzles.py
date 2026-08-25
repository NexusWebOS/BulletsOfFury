#!/usr/bin/env python3
"""Render live ship-boss volleys to verify projectile and muzzle origins visually."""
import base64
import functools
import http.server
import os
import socketserver
import threading

GAME = r'C:/Users/Mdogg/Desktop/BOF-CODE/BulletsOfFury'
OUT = os.path.join(GAME, '_BUILD_SOURCE', 'qa_shipboss_muzzles')


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass


def serve(directory):
    handler = functools.partial(QuietHandler, directory=directory)
    server = socketserver.TCPServer(('127.0.0.1', 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


WARM = r"""
([stage, family])=>{
  ASSETS.ready=true; run.stage=stage; run.pilot='cole';
  beginStage(stage); warmStage(stage);
  for(let i=0;i<6;i++){
    XART.rdy('bfx_'+family+'_p_'+i);
    XART.rdy('bfx_'+family+'_m_'+i);
  }
  return true;
}
"""

SHOT = r"""
([stage, kind, phase])=>{
  setState(GS.PLAY); run.stage=stage; curStage=STAGES[stage-1];
  enemies.length=0; pBullets.length=0; eBullets.length=0;
  subBoss=null; subBossActive=false; boss=null; bossActive=false;
  spawnBoss(kind);
  const b=boss;
  b.x=VW/2; b.y=VH*0.29; b.ty=b.y; b.enter=false; b.entry=0;
  b._drawY=b.y; b.hp=b.maxhp*(phase===2?0.18:(phase===1?0.46:0.9));
  b._sbPhase=phase; b._sbStep=0;
  shipBossAttack(b);
  if(b._smz) b._smz.t=0.045;
  for(const q of eBullets){ q.t=0.04; }
  drawWorld(1/60);
  const D=SHIPBOSS[kind], cv=document.getElementById('screen');
  return {stage,kind,phase,family:D.proj,slots:b._smz?b._smz.slots.slice():[],
          bullets:eBullets.length,img:cv.toDataURL('image/png')};
}
"""

CUSTOM_SHOT = r"""
([stage, kind, phase])=>{
  setState(GS.PLAY); run.stage=stage; curStage=STAGES[stage-1];
  enemies.length=0; pBullets.length=0; eBullets.length=0;
  boss=null; bossActive=false; subBoss=null; subBossActive=false;
  spawnSubBoss__inner(kind);
  const b=subBoss;
  b.x=VW/2; b.y=VH*0.29; b.ty=b.y; b.enter=false; b.entry=0; b._drawY=b.y;
  b.atkPhase=phase; drawWorld(1/60); subBossAttack();
  if(b._cmz) b._cmz.t=0.045;
  for(const q of eBullets) q.t=0.04;
  drawWorld(1/60);
  const cv=document.getElementById('screen');
  return {stage,kind,phase,family:b._cmz&&b._cmz.family,
          muzzles:b._cmz?b._cmz.points.length:0,bullets:eBullets.length,
          img:cv.toDataURL('image/png')};
}
"""


from playwright.sync_api import sync_playwright

os.makedirs(OUT, exist_ok=True)
server = serve(GAME)
port = server.server_address[1]
cases = [
    (2, 'infernoreaver', 0),
    (3, 'cryospear', 0),
    (4, 'stormsovereign', 0),
    (5, 'xenoregent', 0),
    (6, 'doomsdaycarriermk2', 1),
    (7, 'sludgeemperor', 2),
]

with sync_playwright() as p:
    browser = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
    page = browser.new_page(viewport={'width': 620, 'height': 900}, device_scale_factor=1)
    page.goto(f'http://127.0.0.1:{port}/index.html', wait_until='load', timeout=60000)
    page.wait_for_function("()=>typeof setState==='function' && (window.__bofFrames|0)>4", timeout=45000)
    for stage, kind, phase in cases:
        family = page.evaluate(f"SHIPBOSS['{kind}'].proj")
        page.evaluate(WARM, [stage, family])
        page.wait_for_timeout(2500)
        result = page.evaluate(SHOT, [stage, kind, phase])
        path = os.path.join(OUT, f's{stage}_{kind}_p{phase}.png')
        with open(path, 'wb') as handle:
            handle.write(base64.b64decode(result['img'].split(',', 1)[1]))
        print(f"s{stage} {kind:22s} {result['family']:9s} bullets={result['bullets']:2d} "
              f"muzzles={','.join(result['slots']) or '-'} -> {os.path.basename(path)}")
    for stage, kind, phase, family in [(5, 'subcore', 0, 'cyclone'), (7, 'ratking', 1, 'sludge')]:
        page.evaluate(WARM, [stage, family])
        page.wait_for_timeout(1500)
        result = page.evaluate(CUSTOM_SHOT, [stage, kind, phase])
        path = os.path.join(OUT, f's{stage}_{kind}_p{phase}.png')
        with open(path, 'wb') as handle:
            handle.write(base64.b64decode(result['img'].split(',', 1)[1]))
        print(f"s{stage} {kind:22s} {str(result['family']):9s} bullets={result['bullets']:2d} "
              f"muzzles={result['muzzles']} -> {os.path.basename(path)}")
    browser.close()

server.shutdown()
