#!/usr/bin/env python3
"""probe_bank.py - "falva doesnt twist at all when I move her left and right".

Every pilot, driven through the REAL input path, reporting the bank value the ramp reaches and the
frame key the draw then picks.

Two things this had to get right before it could say anything true:
  Input.lf / Input.rt ARE GETTERS over keybind.left/right. Assigning to them is a silent no-op, so
  a probe that "holds right" that way holds nothing and reports every pilot as broken.
  AND updatePlay THROWS WITHOUT beginStage - a null wave list - which also reports every pilot as
  broken, for a third unrelated reason.
"""
import http.server, socketserver, threading, functools
GAME = r'C:/Users/Mdogg/Desktop/BOF-CODE/BulletsOfFury'

def serve(d):
    h = functools.partial(http.server.SimpleHTTPRequestHandler, directory=d)
    h.log_message = lambda *a, **k: None
    s = socketserver.TCPServer(("127.0.0.1", 0), h)
    threading.Thread(target=s.serve_forever, daemon=True).start()
    return s.server_address[1]

JS = r"""
(pk)=>{
  ASSETS.ready=true; run.stage=1; run.pilot=pk;
  try{ beginStage(1); }catch(e){}
  setState(GS.PLAY); player.reset(); player.invuln=0;
  const out={pilot:pk, flip:!!(typeof SHIP_BANK_FLIP!=='undefined' && SHIP_BANK_FLIP[pk])};
  keybind.right.forEach(k=>{ Input.keys[k]=true; });
  keybind.left.forEach(k=>{ Input.keys[k]=false; });
  out.rtSeen=Input.rt;
  for(let i=0;i<40;i++){ try{ updatePlay(1/60); }catch(e){ out.err=String(e); break; } }
  out.bank=+(player._bank||0).toFixed(3);
  out.key=(typeof _shipFrameKey==='function')?_shipFrameKey(pk):null;
  out.rdy=out.key?!!XART.rdy(out.key):null;
  keybind.right.forEach(k=>{ Input.keys[k]=false; });
  return out;
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
    print('%-11s %6s %-6s %-24s %-6s %s' % ('pilot', 'bank', 'rt', 'frame key', 'rdy', 'flip'))
    bad = 0
    for pk in ('cole', 'falva', 'lizzie', 'axel', 'decker', 'freezer', 'juggernaut', 'maverick', 'yuri'):
        r = pg.evaluate(JS, pk)
        flag = ''
        if r.get('err'): flag = '  *** ' + r['err']; bad += 1
        elif abs(r.get('bank') or 0) < 0.5: flag = '  *** DOES NOT BANK'; bad += 1
        elif not r.get('rdy'): flag = '  *** frame not ready'; bad += 1
        print('%-11s %6s %-6s %-24s %-6s %-5s%s'
              % (pk, r.get('bank'), r.get('rtSeen'), str(r.get('key')), str(r.get('rdy')), r.get('flip'), flag))
    b.close()
    print('\n%s' % ('ALL PILOTS BANK' if bad == 0 else '*** %d pilot(s) with a problem' % bad))
