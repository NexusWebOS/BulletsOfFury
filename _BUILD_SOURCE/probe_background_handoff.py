#!/usr/bin/env python3
"""Verify that the launch connector and PLAY render the same background at the join.

Unlike probe_arrival.py, this deliberately excludes gameplay-plane hazards (Stage 5 rocks,
Stage 6 missiles, bullets, and the player). Those objects are allowed to become active when PLAY
begins; this probe answers the narrower question of whether the background itself cuts.
"""
import functools
import http.server
import socketserver
import threading

from playwright.sync_api import sync_playwright


GAME = r"C:/Users/Mdogg/Desktop/BOF-CODE/BulletsOfFury"


def serve(directory):
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=directory)
    handler.log_message = lambda *args, **kwargs: None
    server = socketserver.TCPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server.server_address[1]


SETUP = """
(stage) => {
  ASSETS.ready = true;
  run.pilot = 'cole';
  curStage = STAGES[stage - 1] || STAGES[0];
  beginStage(stage);
  setState(GS.LAUNCH);
  const cfg = _levelCfg();
  XART.rdy(stageMasterKey(cfg));
  return true;
}
"""


READY = """
() => {
  const cfg = _levelCfg();
  return !!(cfg && XART.rdy(stageMasterKey(cfg)));
}
"""


MEASURE = r"""
() => {
  const cv = document.querySelector('canvas');
  const W = cv.width, H = cv.height;
  const snap = document.createElement('canvas'); snap.width=W; snap.height=H;
  const sg = snap.getContext('2d', {alpha:false});
  const grab = () => { sg.drawImage(cv,0,0); return sg.getImageData(0,0,W,H).data; };
  const clear = () => { ctx.setTransform(SS,0,0,SS,0,0); ctx.fillStyle='#000'; ctx.fillRect(0,0,VW,VH); };

  clear();
  entryConnectorDraw(run.stage, 0);
  drawScanlines();
  const connector = grab();

  clear();
  ctx.save();
  if(worldWidth()>viewW()) ctx.translate(-camX,0);
  drawBG(0);
  ctx.restore();
  drawScanlines();
  const playBackground = grab();

  let differing=0, worst=0;
  for(let i=0;i<connector.length;i+=4){
    const d=Math.max(Math.abs(connector[i]-playBackground[i]),
                     Math.abs(connector[i+1]-playBackground[i+1]),
                     Math.abs(connector[i+2]-playBackground[i+2]));
    if(d>8) differing++;
    if(d>worst) worst=d;
  }
  return {differing, total:W*H, pct:+(100*differing/(W*H)).toFixed(4), worst};
}
"""


port = serve(GAME)
with sync_playwright() as playwright:
    browser = playwright.chromium.launch(args=["--disable-gpu", "--no-sandbox", "--mute-audio"])
    page = browser.new_page(viewport={"width": 620, "height": 900})
    page.goto(f"http://127.0.0.1:{port}/index.html", wait_until="load", timeout=60000)
    page.wait_for_function("() => typeof setState==='function' && (window.__bofFrames|0)>4", timeout=45000)
    for stage in (5, 6):
        page.evaluate(SETUP, stage)
        page.wait_for_function(READY, timeout=60000)
        page.wait_for_timeout(1200)
        result = page.evaluate(MEASURE)
        verdict = "PASS" if result["differing"] == 0 else "CUT"
        print(f"stage {stage}: {verdict} {result['differing']}/{result['total']} "
              f"({result['pct']:.4f}%), worst channel delta {result['worst']}")
    browser.close()
