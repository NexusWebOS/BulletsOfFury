#!/usr/bin/env python3
"""probe_hudcorners.py - the roll charge bar, the corner equipment box, and the 5s cooldown.

Mike: "lets do a 5 second cooldown on barrel rolling. make a little charge bar that appears in the
bottom left corner, and also I've noticed our equipment box doesnt appear in-game in my hud. Place
that on the lower right corner of the game."

Checks the behaviour as well as the pixels, because a bar that draws and a cooldown that works are
two different claims:

  THE COOLDOWN GATES THE ROLL   a second roll must be refused, and must re-arm at ~5s, not 0.18.
  THE BAR TRACKS IT             filled when ready, empty right after a roll, part-filled between.
  BOTH CORNERS ARE INSIDE       drawn in PLAY coordinates - the whole point is that the strip
                                version got cropped off the right of a narrow window.
"""
import http.server, socketserver, threading, functools, os, base64, io
GAME = r'C:/Users/Mdogg/Desktop/BOF-CODE/BulletsOfFury'
OUT  = os.path.join(GAME, 'docs', 'proofs')

def serve(d):
    h = functools.partial(http.server.SimpleHTTPRequestHandler, directory=d)
    h.log_message = lambda *a, **k: None
    s = socketserver.TCPServer(("127.0.0.1", 0), h)
    threading.Thread(target=s.serve_forever, daemon=True).start()
    return s.server_address[1]

BEHAVIOUR = r"""
()=>{
  ASSETS.ready=true; run.stage=1; run.pilot='cole';
  try{ beginStage(1); }catch(e){}
  setState(GS.PLAY); player.reset(); player.invuln=0; player._rollCool=0;
  const out={brCool:(typeof BR_COOL==='number')?BR_COOL:null};
  startRoll(1);
  out.rolled = !!player.roll;
  /* run the roll out, then try again immediately - it must be refused */
  /* [!] THE TICK IS updateRoll, NOT rollTick. Calling a name that does not exist meant the roll
     never COMPLETED, so _rollCool was never set at all - and the probe then reported the cooldown
     as broken when it had simply never been armed. */
  for(let i=0;i<60 && player.roll;i++){ updateRoll(1/60); }
  out.coolAfter = +(player._rollCool||0).toFixed(2);
  startRoll(-1);
  out.secondRefused = !player.roll;
  /* how long until it re-arms */
  let t=0;
  while((player._rollCool||0)>0 && t<12){ player._rollCool=Math.max(0,player._rollCool-1/60); t+=1/60; }
  out.rearmSec=+t.toFixed(1);
  startRoll(-1);
  out.thirdAllowed = !!player.roll;
  return out;
}
"""

SHOT = r"""
(cool)=>{
  ASSETS.ready=true; run.stage=1; run.pilot='cole';
  try{ beginStage(1); }catch(e){} try{ warmStage(1); }catch(e){}
  setState(GS.PLAY); player.reset(); player.invuln=999999;
  run.shield=2; run.speedLevel=3; run.wlevel=4; run.weapon=0; run.lives=3; run.bombs=3;
  player._rollCool=cool; player.roll=null;
  player.x=VW/2; player.y=VH*0.72;
  enemies.length=0; eBullets.length=0;
  try{ drawWorld(1/60); }catch(e){ return {err:String(e)}; }
  try{ drawHUDOverlay(); }catch(e){ return {err:'overlay: '+String(e)}; }
  return {img:document.getElementById('screen').toDataURL('image/png'),
          play:{x:PLAY.x,y:PLAY.y,w:PLAY.w,h:PLAY.h}, VW:VW, VH:VH};
}
"""

from playwright.sync_api import sync_playwright
os.makedirs(OUT, exist_ok=True)
port = serve(GAME)
with sync_playwright() as p:
    b  = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
    pg = b.new_page(viewport={'width': 620, 'height': 900}, device_scale_factor=1)
    errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=60000)
    pg.wait_for_function("()=>typeof setState==='function'", timeout=45000)
    pg.wait_for_function("()=>(window.__bofFrames|0)>4", timeout=45000)
    pg.wait_for_timeout(3500)
    # WARM THE EQUIPPED ICON FIRST. XART.rdy() is what STARTS a decode and returns false on that
    # first call, so a single synchronous render draws the frame with an empty socket - which looks
    # exactly like "the icon is not wired" and is not.
    # micon_ lives in BOFX.icons and draws from a SHEET - warm the sheet, not the key
    pg.evaluate("()=>{ XART.rdy('nia_icons'); XART.rdy('nia_icons2'); XART.rdy('nequipbox'); }")
    try:
        pg.wait_for_function("()=>XART.rdy('nequipbox') && (XART.rdy('nia_icons')||XART.rdy('nia_icons2'))", timeout=20000)
        print('equip frame + icon sheet decoded')
    except Exception:
        print('*** equip art never decoded')

    r = pg.evaluate(BEHAVIOUR)
    print('BR_COOL            %s' % r['brCool'])
    print('roll started       %s' % r['rolled'])
    print('cooldown after     %ss' % r['coolAfter'])
    print('second roll refused%s' % ('  yes' if r['secondRefused'] else '  *** NO - it chained'))
    print('re-arms after      %ss' % r['rearmSec'])
    print('third roll allowed %s' % ('yes' if r['thirdAllowed'] else '*** NO - stuck locked'))

    from PIL import Image
    tiles = []
    for cool, lab in ((0.0, 'ready'), (2.5, 'half'), (4.9, 'just rolled')):
        sres = pg.evaluate(SHOT, cool)
        if sres.get('err'):
            print('shot %s ERR %s' % (lab, sres['err'])); continue
        im = Image.open(io.BytesIO(base64.b64decode(sres['img'].split(',', 1)[1])))
        pl = sres['play']
        sc = im.width / sres['VW']
        # crop the bottom band of the PLAY rect, where both readouts live
        tiles.append(im.crop((int(pl['x'] * sc), int((pl['y'] + pl['h'] - 40) * sc),
                              int((pl['x'] + pl['w']) * sc), int((pl['y'] + pl['h']) * sc))))
        print('rendered %s' % lab)
    if tiles:
        w = tiles[0].width
        h = tiles[0].height
        sheet = Image.new('RGB', (w, h * len(tiles)), (11, 13, 18))
        for i, t in enumerate(tiles): sheet.paste(t, (0, i * h))
        sheet.save(os.path.join(OUT, 'hudcorners_0812p.png'))
        print('-> docs/proofs/hudcorners_0812p.png')
    if errs: print('PAGE ERRORS: %s' % errs[:2])
    b.close()
