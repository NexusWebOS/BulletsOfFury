#!/usr/bin/env python3
"""probe_muzzle.py - the player's muzzle flash, at every tier, for both weapons.

Written because `node --check` CANNOT catch what nearly shipped here. The flash block was inserted
between the two legacy branches, so `let _p87muz` was declared AFTER a branch that reads it - a
temporal-dead-zone ReferenceError that throws on every spread shot, and passes a syntax check
cleanly. This probe fails loudly on ANY thrown error, which is the only way that class of mistake
is caught before Mike sees it.

It also checks the two things the flash is supposed to fix:
  TIER 6-8 ARE NOT CLAMPED. _mgMuzLv was stored as min(5, lv) at all five assignment sites, so
  Cole's exclusive tiers lit the level-5 flash.
  THE REEL IS A ONE-SHOT. It was driven by performance.now(), so which of the four frames you saw
  depended on when you pulled the trigger rather than on how far the flash had come.
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

SHOT = r"""
([weapon, lv, muzT])=>{
  ASSETS.ready=true; run.stage=1; run.pilot='cole';
  run.weapon=weapon; run.wlevel=lv;
  setState(GS.PLAY);
  enemies.length=0; pBullets.length=0; eBullets.length=0; boss=null; subBoss=null;
  player.x=VW/2; player.y=VH*0.72; player.hp=99; player.invuln=999;
  player._mgMuzT=muzT; player._mgMuzLv=lv;
  ctx.fillStyle='#0b0d12'; ctx.fillRect(0,0,VW,VH);
  let err=null;
  try{ drawPlayer(1/60); }catch(e){ err=String(e); }
  return {weapon, lv, muzT, err, lvStored:player._mgMuzLv,
          img:document.getElementById('screen').toDataURL('image/png')};
}
"""
FIRE = r"""
(lv)=>{
  /* fire for real, so the ASSIGNMENT sites are exercised rather than a hand-set value.
     TIER 8 DOES NOT FIRE THE MACHINE GUN - coleTier()>=8 returns immediately because the fusion
     cannon replaces it, driven from the input path. Asking tier 8 for a machine-gun muzzle level
     therefore reads whatever the previous shot left behind, which is what made my first run report
     "still clamped to 5". 6 and 7 are the tiers that exercise this.
     AND THE PILOT MUST BE COLE. coleTier() caps everyone else at 5, so firing as whoever the
     game booted with reports tiers 6 and 7 as "clamped" when the clamp is the correct rule.
     Two probe faults in a row on the same three lines. */
  run.pilot='cole'; run.weapon=0; run.wlevel=lv; player.fireCd=0; player._mgMuzLv=0;
  let err=null;
  try{ pShoot(); }catch(e){ err=String(e); }
  return {err, lv:player._mgMuzLv, t:player._mgMuzT};
}
"""

from playwright.sync_api import sync_playwright
os.makedirs(OUT, exist_ok=True)
port = serve(GAME)
with sync_playwright() as p:
    b  = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
    pg = b.new_page(viewport={'width': 620, 'height': 900}, device_scale_factor=1)
    page_errors = []
    pg.on('pageerror', lambda e: page_errors.append(str(e)))
    pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=60000)
    pg.wait_for_function("()=>typeof setState==='function'", timeout=45000)
    pg.wait_for_function("()=>(window.__bofFrames|0)>4", timeout=45000)
    pg.wait_for_function("()=>XART.rdy('nca_87')", timeout=45000)

    from PIL import Image
    bad = 0
    for _lv in (5, 6, 7):
        r = pg.evaluate(FIRE, _lv)
        okc = (r['lv'] == _lv)
        print('LIVE pShoot at tier %d -> stored _mgMuzLv=%s  err=%s  %s'
              % (_lv, r['lv'], r['err'] or 'none', 'ok' if okc else '*** CLAMPED'))
        if r['err'] or not okc: bad += 1

    for weapon, label in ((0, 'mg'), (1, 'spread')):
        tiles = []
        for lv in range(1, 9):
            s = pg.evaluate(SHOT, [weapon, lv, 0.055])
            if s['err']:
                print('  %s lv%d THREW %s' % (label, lv, s['err'])); bad += 1; continue
            im = Image.open(io.BytesIO(base64.b64decode(s['img'].split(',', 1)[1])))
            tiles.append(im.crop((im.width // 2 - 110, int(im.height * 0.52), im.width // 2 + 110, int(im.height * 0.84))))
        if tiles:
            w, h = 150, int(tiles[0].height * 150 / tiles[0].width)
            sheet = Image.new('RGB', (w * len(tiles), h), (11, 13, 18))
            for i, t in enumerate(tiles): sheet.paste(t.resize((w, h)), (i * w, 0))
            sheet.save(os.path.join(OUT, 'muzzle_%s_0812g.png' % label))
            print('  -> docs/proofs/muzzle_%s_0812g.png  (%d tiers)' % (label, len(tiles)))

    # the reel must advance with the flash's own age, not the wall clock
    seen = []
    for t in (0.070, 0.052, 0.035, 0.018):
        s = pg.evaluate(SHOT, [0, 5, t])
        im = Image.open(io.BytesIO(base64.b64decode(s['img'].split(',', 1)[1])))
        px = im.convert('RGB').load()
        lit = sum(1 for y in range(int(im.height*0.52), int(im.height*0.76))
                    for x in range(im.width//2-70, im.width//2+70) if sum(px[x, y]) > 150)
        seen.append((t, lit))
    print('ONE-SHOT reel, ink by remaining flash time: %s' % ', '.join('%.3fs=%d' % v for v in seen))
    if len(set(v[1] for v in seen)) < 3:
        print('  *** the reel is not advancing with the flash'); bad += 1

    if page_errors:
        print('PAGE ERRORS: %s' % page_errors[:3]); bad += len(page_errors)
    print('\n%s' % ('ALL CLEAN' if bad == 0 else '*** %d PROBLEM(S)' % bad))
    b.close()
