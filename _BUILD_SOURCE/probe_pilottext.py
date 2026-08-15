#!/usr/bin/env python3
"""probe_pilottext.py - the pilot-select dialogue box, before and after the font swap.

Mike: "Go to the dialogue boxes/text when you select a pilot. elimnate this basic ass text and use
our in-game font."

drawCommWindow's own comment already conceded the body: the NAME was moved to the authored face in
0811f and the body was left on canvas text because "stageText has no wrap or measure, so converting
it needs a line-breaker rather than a one-line swap". That line-breaker exists - msgWrap/msgMeasure/
msgTextLeft were built for the stage dialogue window - so this checks the result.

Renders the comm window at a few typewriter positions, because the body reveals character by
character and a wrap that reflows mid-type is the specific thing to avoid.
"""
import http.server, socketserver, threading, functools, os, base64, io, sys
GAME = r'C:/Users/Mdogg/Desktop/BOF-CODE/BulletsOfFury'
OUT  = os.path.join(GAME, 'docs', 'proofs')
TAG  = sys.argv[1] if len(sys.argv) > 1 else 'after'

def serve(d):
    h = functools.partial(http.server.SimpleHTTPRequestHandler, directory=d)
    h.log_message = lambda *a, **k: None
    s = socketserver.TCPServer(("127.0.0.1", 0), h)
    threading.Thread(target=s.serve_forever, daemon=True).start()
    return s.server_address[1]

SHOT = r"""
(chars)=>{
  ASSETS.ready=true; run.pilot='cole';
  setState(GS.PILOT);
  ctx.fillStyle='#0b0d12'; ctx.fillRect(0,0,VW,VH);
  const P=(typeof PILOTS!=='undefined') ? (PILOTS.find(p=>p.key==='cole')||PILOTS[0]) : null;
  if(!P) return {err:'no pilots'};
  const _pp=(typeof pilotPortrait==='function')?pilotPortrait(P.key,'idle'):('face_'+P.key);
  let err=null;
  try{
    drawCommWindow({tint:P.tint, name:P.name, frameKey:'dlg_'+P.key, portraitKey:_pp,
                    cardKey:'card_'+P.key,
                    text:'GOOD LUCK, PILOT! THE JUNGLE RUN IS HOT TODAY - WATCH THE RIVER.',
                    charsShown:chars, appear:1});
  }catch(e){ err=String(e); }
  return {err, img:document.getElementById('screen').toDataURL('image/png')};
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
    # TRIGGER THE WARM, THEN GIVE THE BROWSER REAL WALL-CLOCK. uiFontWarm only STARTS the decode;
    # a synchronous render immediately after it can photograph nothing but the fallback face, which
    # is what made the warm look like it had not worked.
    pg.evaluate("()=>{ ASSETS.ready=true; setState(GS.PILOT); try{ drawPilot(1/60); }catch(e){} }")
    try:
        pg.wait_for_function("()=>{ const a=(typeof defFontArt==='function')?defFontArt():null;"
                             " return !!(a && a.font && a.img && a.img.complete && a.img.naturalWidth); }",
                             timeout=30000)
        print('UI font decoded after the warm')
    except Exception as e:
        print('*** UI font never decoded: %s' % str(e)[:80])

    from PIL import Image
    tiles = []
    for chars in (14, 34, 999):
        r = pg.evaluate(SHOT, chars)
        if r.get('err'):
            print('chars=%s THREW %s' % (chars, r['err'])); continue
        im = Image.open(io.BytesIO(base64.b64decode(r['img'].split(',', 1)[1])))
        tiles.append(im.crop((0, int(im.height * 0.30), im.width, int(im.height * 0.80))))
        print('chars=%-4s rendered' % chars)
    if tiles:
        w = tiles[0].width // 2
        h = tiles[0].height // 2
        sheet = Image.new('RGB', (w, h * len(tiles)), (11, 13, 18))
        for i, t in enumerate(tiles):
            sheet.paste(t.resize((w, h)), (0, i * h))
        name = 'pilottext_%s_0812j.png' % TAG
        sheet.save(os.path.join(OUT, name))
        print('-> docs/proofs/%s' % name)
    if errs: print('PAGE ERRORS: %s' % errs[:2])
    b.close()
