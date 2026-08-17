#!/usr/bin/env python3
"""probe_reaverpal.py - what colour does the INFERNO REAVER actually shoot?

Mike: "Do not use red pellets or effects for his attacks. bad move here. It will look bad with the
lava. Use yellow/white, orange/white, white/red with the red being inside if anything."

⚠ MEASURE BEFORE CHANGING. _PLASMA_PAL[2] is 'red', which looks like the answer - but the reaver's
pattern is 'ember', and ember fires through _shipShot as kind 'eshot', NOT 'plasma'. Guessing from
the palette table would have recoloured a projectile this boss never fires. So this reports the
bullet KINDS the boss actually emits, and then the mean colour of the pixels they put on screen.

Colour is read off the canvas rather than inferred from a key, because a family name is not a
colour: EA_COMET_ROW calls row 9 'red' and row 14 'orange' and only the pixels settle it.
"""
import http.server, socketserver, threading, functools, base64, io, os
GAME = r'C:/Users/Mdogg/Desktop/BOF-CODE/BulletsOfFury'
OUT  = os.path.join(GAME, 'docs', 'proofs')

def serve(d):
    h = functools.partial(http.server.SimpleHTTPRequestHandler, directory=d)
    h.log_message = lambda *a, **k: None
    s = socketserver.TCPServer(("127.0.0.1", 0), h)
    threading.Thread(target=s.serve_forever, daemon=True).start()
    return s.server_address[1]

KINDS = r"""
()=>{
  ASSETS.ready=true; run.stage=2; run.pilot='cole';
  try{ beginStage(2); }catch(e){}
  setState(GS.PLAY); player.reset();
  player.x=VW/2; player.y=VH*0.80; player.invuln=999999; player.hp=999;
  enemies.length=0; pBullets.length=0; eBullets.length=0; boss=null; subBoss=null;
  try{ spawnBoss('infernoreaver'); }catch(e){ return {err:String(e)}; }
  const b=boss; if(!b) return {err:'no boss'};
  bossActive=true; b._be=null; b.enter=false; b.entry=0; b.y=VH*0.22; b.fireCd=0.2;

  const kinds={}, pals={};
  const seen=new WeakSet();
  for(let f=0; f<60*40; f++){
    player.invuln=999999; player.hp=999; bossActive=true; b.hp=b.maxhp=999999;
    try{ updatePlay(1/60); }catch(e){ return {err:'updatePlay: '+String(e), f}; }
    for(const x of eBullets){
      if(seen.has(x)) continue; seen.add(x);
      kinds[x.kind]=(kinds[x.kind]||0)+1;
      const p=x.pal||'(none)'; pals[p]=(pals[p]||0)+1;
    }
  }
  return {kinds, pals, pat:b.pat, pats:(b.pats||null)};
}
"""

# render a lone bullet of each kind on a black field and read its mean colour
SHOT = r"""
(kind)=>{
  ASSETS.ready=true; run.stage=2; run.pilot='cole';
  try{ beginStage(2); }catch(e){} try{ warmStage(2); }catch(e){}
  setState(GS.PLAY); player.reset(); player.invuln=999999;
  enemies.length=0; pBullets.length=0; eBullets.length=0; boss=null; subBoss=null;
  const cv=document.getElementById('screen'), c2=cv.getContext('2d');
  c2.save(); c2.setTransform(1,0,0,1,0,0);
  c2.fillStyle='#000'; c2.fillRect(0,0,cv.width,cv.height); c2.restore();
  eBullets.length=0;
  eBullets.push({x:VW/2, y:VH/2, vx:0, vy:0, w:26, h:26, dmg:1, t:0.25, kind:kind});
  try{ drawEnemyBullets ? drawEnemyBullets() : null; }catch(e){}
  try{ drawWorld(1/60); }catch(e){ return {err:String(e)}; }
  return {img:cv.toDataURL('image/png'), VW:VW, VH:VH, w:cv.width, h:cv.height};
}
"""

from playwright.sync_api import sync_playwright
from PIL import Image
os.makedirs(OUT, exist_ok=True)
port = serve(GAME)
with sync_playwright() as p:
    br = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
    pg = br.new_page(viewport={'width': 620, 'height': 900}, device_scale_factor=1)
    errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=60000)
    pg.wait_for_function("()=>typeof setState==='function'", timeout=45000)
    pg.wait_for_function("()=>(window.__bofFrames|0)>4", timeout=45000)
    pg.wait_for_timeout(3000)

    r = pg.evaluate(KINDS)
    if r.get('err'):
        print('*** %s' % r['err'])
    else:
        print('reaver base pattern : %s' % r['pat'])
        print('reaver pattern pool : %s' % r['pats'])
        print('\nbullet KINDS over 40s:')
        for k, v in sorted(r['kinds'].items(), key=lambda kv: -kv[1]):
            print('   %-14s %5d' % (k, v))
        print('bullet PAL field:')
        for k, v in sorted(r['pals'].items(), key=lambda kv: -kv[1]):
            print('   %-14s %5d' % (k, v))

        # mean colour of each kind the boss actually fires
        print('\nmean colour of the pixels each kind draws (lit pixels only):')
        for kind in list(r['kinds'].keys()):
            s = pg.evaluate(SHOT, kind)
            if s.get('err'):
                print('   %-14s render ERR %s' % (kind, s['err'])); continue
            im = Image.open(io.BytesIO(base64.b64decode(s['img'].split(',', 1)[1]))).convert('RGB')
            sc = im.width / s['VW']
            cx, cy = int(s['VW'] / 2 * sc), int(s['VH'] / 2 * sc)
            box = im.crop((cx - 40, cy - 40, cx + 40, cy + 40))
            px = [q for q in box.getdata() if sum(q) > 90]
            if not px:
                print('   %-14s *** drew nothing' % kind); continue
            R = sum(q[0] for q in px) / len(px)
            G = sum(q[1] for q in px) / len(px)
            B = sum(q[2] for q in px) / len(px)
            # "red" = strongly red-dominant with little green. orange/yellow lift green.
            verdict = 'RED' if (R > 90 and G < R * 0.45 and B < R * 0.55) else \
                      'orange/amber' if (G >= R * 0.45 and G < R * 0.80 and B < R * 0.6) else \
                      'yellow/white' if (G >= R * 0.80) else 'other'
            print('   %-14s rgb(%3d,%3d,%3d)  %5d px   -> %s'
                  % (kind, R, G, B, len(px), verdict))
            box.resize((160, 160), Image.NEAREST).save(os.path.join(OUT, 'reaver_%s.png' % kind))
        print('\n-> swatches in docs/proofs/reaver_*.png')

    if errs: print('\nPAGE ERRORS: %s' % errs[:3])
    br.close()
