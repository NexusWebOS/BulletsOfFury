#!/usr/bin/env python3
"""probe_p87.py - the nca_87 pack on the machine gun and the spread, at all eight levels.

Mike's scheme is a GLOW colour and a BODY colour per level, and the two have to mesh. That cannot
be judged from a table, so this fires real bullets through the real draw path and lays the eight
levels out side by side.

Two things it is specifically looking for, because both are known failure modes here:

  THE ROUND MUST NOT PULSE. Row 1 of the sheet is 50px wide at frame 0 and 26px at frame 2. If the
  reel is looped or driven off the wall clock instead of the round's own age, the bullet throbs -
  the "wobbly projectiles" of 0811y. Rounds are sampled at several ages down the screen so a pulse
  would show as alternating widths in one column.

  WHITE AND BLACK MUST NOT COME OUT GREY. xartPalette's default is a 'color' composite, which
  takes hue and saturation from the fill - and an achromatic fill has none to give. Levels 3
  (white) and 4 (black) are the ones to look at.
"""
import http.server, socketserver, threading, functools, os, base64
GAME = r'C:/Users/Mdogg/Desktop/BOF-CODE/BulletsOfFury'
OUT  = os.path.join(GAME, 'docs', 'proofs')

def serve(d):
    h = functools.partial(http.server.SimpleHTTPRequestHandler, directory=d)
    h.log_message = lambda *a, **k: None
    s = socketserver.TCPServer(("127.0.0.1", 0), h)
    threading.Thread(target=s.serve_forever, daemon=True).start()
    return s.server_address[1]

SHOT = r"""
([kind, lv])=>{
  ASSETS.ready=true; run.stage=1; run.pilot='cole';
  run.weapon = (kind==='mg') ? 0 : 1;
  run.wlevel = lv;
  setState(GS.PLAY);
  enemies.length=0; eBullets.length=0; boss=null; subBoss=null;
  pBullets.length=0;
  /* a column of rounds at increasing AGE, so a reel that pulses shows as alternating widths */
  for(let i=0;i<7;i++){
    pBullets.push({kind:kind, x:VW/2, y:VH*0.86 - i*52, vx:0, vy:-9, lv:lv,
                   t:i*0.05, w:6, h:14, dmg:1, dead:false});
  }
  /* and a fan, so the spread's authored diagonals are exercised */
  if(kind==='spread'){
    pBullets.length=0;
    const angs=[-Math.PI/2, -Math.PI/2-0.5, -Math.PI/2+0.5, -Math.PI/2-0.85, -Math.PI/2+0.85];
    angs.forEach((a,i)=>{
      for(let j=0;j<3;j++)
        pBullets.push({kind:'spread', x:VW/2 + Math.cos(a)*(60+j*46), y:VH*0.88 + Math.sin(a)*(60+j*46),
                       vx:Math.cos(a)*9, vy:Math.sin(a)*9, lv:lv, t:0.12+j*0.05, w:6,h:14, dmg:1, dead:false});
    });
  }
  ctx.fillStyle='#0b0d12'; ctx.fillRect(0,0,VW,VH);
  try{ drawBullets(); }catch(e){ return {err:String(e)}; }
  const cv=document.getElementById('screen');
  return {lv, kind, glow:wlvGlow(lv), body:String(WLV_BODY[lv]),
          img:cv.toDataURL('image/png')};
}
"""

from playwright.sync_api import sync_playwright
os.makedirs(OUT, exist_ok=True)
port = serve(GAME)
with sync_playwright() as p:
    b  = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
    pg = b.new_page(viewport={'width': 620, 'height': 900}, device_scale_factor=1)
    pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=60000)
    pg.wait_for_function("()=>typeof setState==='function'", timeout=45000)
    pg.wait_for_function("()=>(window.__bofFrames|0)>4", timeout=45000)
    pg.wait_for_function("()=>XART.rdy('nca_87')", timeout=45000)   # the pack itself, decoded

    from PIL import Image
    import io
    for kind in ('mg', 'spread'):
        tiles = []
        for lv in range(1, 9):
            r = pg.evaluate(SHOT, [kind, lv])
            if r.get('err'):
                print('%s lv%d ERROR %s' % (kind, lv, r['err'])); continue
            print('%-6s lv%d  glow %-8s body %s' % (kind, lv, r['glow'], r['body']))
            im = Image.open(io.BytesIO(base64.b64decode(r['img'].split(',', 1)[1])))
            tiles.append(im.crop((im.width // 2 - 150, 0, im.width // 2 + 150, im.height)))
        w = 150
        h = int(tiles[0].height * w / tiles[0].width)
        sheet = Image.new('RGB', (w * len(tiles), h), (11, 13, 18))
        for i, t in enumerate(tiles):
            sheet.paste(t.resize((w, h)), (i * w, 0))
        name = 'p87_%s_levels_0812d.png' % kind
        sheet.save(os.path.join(OUT, name))
        print('  -> docs/proofs/%s' % name)
    b.close()
