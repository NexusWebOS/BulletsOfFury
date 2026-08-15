#!/usr/bin/env python3
"""probe_404stage.py - who asks for assets/game/stage1.png?

The stage-select screen 404s on it and draws an empty preview card over the map (visible in
docs/proofs/stagesel_mouse_0812b.png, bottom-left). grep finds no such path in game.js, the
manifest, or index.html - so the string is BUILT at runtime. Rather than guess, this hooks the
Image src setter before the game boots and prints the assigning stack.
"""
import http.server, socketserver, threading, functools, os
GAME = r'C:/Users/Mdogg/Desktop/BOF-CODE/BulletsOfFury'

def serve(d):
    h = functools.partial(http.server.SimpleHTTPRequestHandler, directory=d)
    h.log_message = lambda *a, **k: None
    s = socketserver.TCPServer(("127.0.0.1", 0), h)
    threading.Thread(target=s.serve_forever, daemon=True).start()
    return s.server_address[1]

HOOK = r"""
() => {
  window.__srcLog = [];
  const d = Object.getOwnPropertyDescriptor(HTMLImageElement.prototype, 'src');
  Object.defineProperty(HTMLImageElement.prototype, 'src', {
    set(v){ if(typeof v==='string' && !/^data:/.test(v))
              window.__srcLog.push({url:v, stack:(new Error()).stack});
            d.set.call(this, v); },
    get(){ return d.get.call(this); }, configurable:true });
}
"""
GO = r"""
()=>{ ASSETS.ready=true; campaign.unlockedMax=8; setState(GS.STAGESEL);
      for(let i=0;i<90;i++){ try{ drawStageSelect(1/60); }catch(e){} }
      return window.__srcLog.filter(e=>/stage\d+\.png|\/stage[^\/]*$/.test(e.url)); }
"""

from playwright.sync_api import sync_playwright
port = serve(GAME)
with sync_playwright() as p:
    b  = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
    pg = b.new_page(viewport={'width': 620, 'height': 900}, device_scale_factor=1)
    pg.add_init_script("(%s)()" % HOOK.strip())
    bad = []
    pg.on('response', lambda r: bad.append(r.url) if r.status == 404 else None)
    pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=60000)
    pg.wait_for_function("()=>typeof setState==='function'", timeout=45000)
    pg.wait_for_function("()=>(window.__bofFrames|0)>4", timeout=45000)
    hits = pg.evaluate(GO)
    print('SUSPECT IMAGE LOADS: %d' % len(hits))
    for h in hits:
        print('\n  url: %s' % h['url'])
        for line in (h['stack'] or '').split('\n')[1:7]:
            print('     %s' % line.strip())
    print('\n404s SEEN ON THE WIRE: %d' % len(bad))
    for u in dict.fromkeys(bad):
        print('  %s' % u)
    b.close()
