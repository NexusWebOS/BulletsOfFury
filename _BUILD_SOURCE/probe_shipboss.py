#!/usr/bin/env python3
"""
probe_shipboss.py — do the five new ship bosses DRAW, FIRE, and FLASH WHITE when shot?

    python3 _BUILD_SOURCE/probe_shipboss.py

Mike, 0810s: "Wire them up, give them attacks that fit, make them challenging, glow white when
shot etc."  Three claims, three measurements, all off real pixels in real Chromium.

⚠ DRAWS is a FRAME DIFF, never a blit count. probe_boss.py reported 0 blits for two minibosses
that a screenshot showed drawn in full — wrapping drawImage and calling the draw function by hand
does not count what the real frame draws (0810l). So: render the frame with the unit, render it
without, and see whether the picture changed.

⚠ FLASHES is also a frame diff, and it is taken against the SAME unit rather than against nothing —
b.flash=0 vs b.flash=0.18 on an otherwise identical frame. A diff against an empty screen would go
green on the hull alone and prove nothing about the flash.

⚠ XART.rdy is false on its FIRST call — that call starts the load. Every key here is polled across
real awaits, because a synchronous burst never lets the network run (the --warm trap).

⚠ MEASUREMENTS AND SCREENSHOTS RUN ON SEPARATE PAGES, and the first cut of this probe died proving
why: five units of frame-diffing plus five toDataURL calls on one page crashed the renderer outright
("Target crashed"), which CLAUDE.md already records as "long warms plus many captures exhaust the
renderer". Each result is also PRINTED AS IT ARRIVES rather than collected and printed at the end —
when that crash hit, every measurement taken before it was lost with it.
"""
import http.server, socketserver, threading, os, functools, base64, json

GAME = r'C:/Users/Mdogg/Desktop/BOF-CODE/BulletsOfFury'
OUT = os.path.join(GAME, 'docs', 'proofs')

import os as _os
ONLY = _os.environ.get('ONLY')
UNITS = [
    ('infernoreaver', 2, 'boss', 'nsb_inferno_reaver'),
    ('cryospear',     3, 'boss', 'nsb_cryo_spear'),
    ('voidbat',       5, 'boss', 'nsb_void_bat'),
    ('siegeember',    2, 'mini', 'nsb_siege_ember'),
    ('thornrime',     3, 'mini', 'nsb_thorn_rime'),
    ('blacksteel',    4, 'mini', 'nsb_blacksteel'),
]
if ONLY: UNITS=[u for u in UNITS if u[0]==ONLY]


def serve(directory):
    h = functools.partial(http.server.SimpleHTTPRequestHandler, directory=directory)
    h.log_message = lambda *a, **k: None
    s = socketserver.TCPServer(("127.0.0.1", 0), h)
    threading.Thread(target=s.serve_forever, daemon=True).start()
    return s.server_address[1]


RUN = r"""
([kind, stage, slot]) => {
  ASSETS.ready = true; run.pilot='cole'; run.mode='arcade';
  beginStage(stage); setState(GS.PLAY);
  bossActive=false; subBoss=null; boss=null; eBullets.length=0;

  const t0 = performance.now(); let f=0;
  const step = () => loop(t0 + (f++)*16.7);
  for (let i=0;i<40;i++) step();

  /* ⚠ spawnSubBoss__inner ASSIGNS the global and returns nothing — it ends on
     `subBoss=b; subBossActive=true;` with no return. Reading its return value reports every
     miniboss as a failed spawn, which is what the first run of this probe did. Every fixture in
     test_fl.js reads the global for exactly this reason. */
  let b;
  if (slot==='boss'){ spawnBoss(kind); b=boss; bossActive=true; }
  else { spawnSubBoss(kind); b=subBoss; }
  if(!b) return {kind, error:'spawn produced no unit'};
  b.enter=false; b.x=VW/2; b.y=150; b.tx=VW/2; b.ty=150;

  const cv=document.getElementById('screen'), gw=cv.width, gh=cv.height;
  const buf=document.createElement('canvas'); buf.width=gw; buf.height=gh;
  const bx=buf.getContext('2d',{alpha:false});
  const snap=()=>{bx.clearRect(0,0,gw,gh); bx.drawImage(cv,0,0);
                  return bx.getImageData(0,0,gw,gh).data;};
  const diff=(a,c)=>{let n=0; for(let k=0;k<a.length;k+=4){
      if(Math.abs(a[k]-c[k])>10||Math.abs(a[k+1]-c[k+1])>10||Math.abs(a[k+2]-c[k+2])>10) n++;} return n;};

  /* ---- DRAWS: with the unit vs without it, time frozen so nothing else moves ---- */
  const realNow=performance.now.bind(performance); const FR=realNow();
  performance.now=()=>FR; const T=t0+f*16.7;
  loop(T); const withIt=snap();
  const keepB=boss, keepS=subBoss, keepA=bossActive;
  boss=null; subBoss=null; bossActive=false;
  loop(T); const without=snap();
  boss=keepB; subBoss=keepS; bossActive=keepA;

  /* ---- FLASHES: same unit, flash off vs flash on ---- */
  b.flash=0; loop(T); const noFlash=snap();
  b.flash=0.18; loop(T); const yesFlash=snap();
  b.flash=0;
  performance.now=realNow;

  /* ---- FIRES: run it and count what lands in eBullets ---- */
  /* ⚠ MEASURE THE GAP BETWEEN VOLLEYS, NOT JUST THE VOLLEYS. The first cut stopped at 6 waves
     and reported perWave [7,7,7,7,7,7] - which looked like six volleys and was six CONSECUTIVE
     FRAMES: shipBossAttack never reset fireCd, so once it hit zero the boss fired every frame for
     the rest of the fight. A count with no interval cannot tell those apart. */
  eBullets.length=0;
  const shots=[]; const gaps=[]; let waves=0, lastAt=-1;
  for (let i=0;i<900;i++){
    const before=eBullets.length;
    step();
    if (eBullets.length>before){
      waves++; shots.push(eBullets.length-before);
      if(lastAt>=0) gaps.push(i-lastAt);
      lastAt=i;
    }
    if (waves>=8) break;
  }
  const vx=eBullets.map(z=>+z.vx.toFixed(2)), vy=eBullets.map(z=>+z.vy.toFixed(2));
  const xs=eBullets.map(z=>Math.round(z.x));

  return {kind, stage, slot, name:b.name, hp:b.maxhp, w:b.w, h:b.h,
          art:b._ship, artReady:XART.rdy(SHIPBOSS[kind].key),
          drawPixels:diff(withIt,without),
          flashPixels:diff(noFlash,yesFlash),
          waves, perWave:shots, gapsFrames:gaps, bullets:eBullets.length,
          vyMin:Math.min.apply(null,vy), vyMax:Math.max.apply(null,vy),
          anyAimed: vx.some((v,i)=>Math.abs(v)>0.01),
          spreadX: xs.length ? (Math.max.apply(null,xs)-Math.min.apply(null,xs)) : 0,
          lanes: Array.from(new Set(xs.map(z=>Math.round(z/40)))).length};
}
"""

SHOT = r"""
([kind, stage, slot]) => {
  ASSETS.ready=true; run.pilot='cole'; run.mode='arcade';
  beginStage(stage); setState(GS.PLAY);
  bossActive=false; subBoss=null; boss=null; eBullets.length=0;
  const t0=performance.now(); let f=0;
  for(let i=0;i<40;i++) loop(t0+(f++)*16.7);
  let b;
  if(slot==='boss'){ spawnBoss(kind); b=boss; bossActive=true; } else { spawnSubBoss(kind); b=subBoss; }
  if(!b) return 'null';
  b.enter=false; b.x=VW/2; b.y=170; b.tx=VW/2; b.ty=170;
  for(let i=0;i<150;i++) loop(t0+(f++)*16.7);
  return 'ok';
}
"""


def main():
    from playwright.sync_api import sync_playwright
    os.makedirs(OUT, exist_ok=True)
    port = serve(GAME)
    url = 'http://127.0.0.1:%d/index.html' % port
    res = []
    with sync_playwright() as p:
        b = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
        pg = b.new_page(viewport={'width': 1100, 'height': 1100}, device_scale_factor=1)
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)[:200]))
        pg.goto(url, wait_until='load', timeout=60000)
        pg.wait_for_function("() => typeof setState==='function' && typeof SHIPBOSS!=='undefined'",
                             timeout=45000)
        pg.wait_for_function("() => (window.__bofFrames|0) > 4", timeout=45000)

        keys = [u[3] for u in UNITS]
        ok = 0
        for _ in range(30):
            pg.evaluate("(ks)=>ks.forEach(k=>{try{XART.rdy(k);}catch(e){}})", keys)
            pg.wait_for_timeout(250)
            ok = pg.evaluate("(ks)=>ks.filter(k=>XART.rdy(k)).length", keys)
            if ok == len(keys):
                break
        print('ship art ready %d/%d\n' % (ok, len(keys)))

        for kind, stage, slot, _k in ([] if os.environ.get('SHOTONLY') else UNITS):
            if pg.is_closed():
                break
            r = pg.evaluate(RUN, [kind, stage, slot])
            res.append(r)
            g = r.get('gapsFrames') or []
            print('  measured %-14s draw=%-9s flash=%-8s bullets=%-4s gap frames=%s'
                  % (kind, r.get('drawPixels', r.get('error')),
                     r.get('flashPixels', '-'), r.get('bullets', '-'), g[:6]))
        pg.close()

        # screenshots on a FRESH BROWSER each — a fresh PAGE was not enough, the shared browser
        # still died partway through the set ("Target closed"). One stage master per browser.
        for kind, stage, slot, _k in ([] if os.environ.get('NOSHOT') else UNITS):
            sb = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
            sp = sb.new_page(viewport={'width': 620, 'height': 900}, device_scale_factor=1)
            try:
                sp.goto(url, wait_until='load', timeout=60000)
                sp.wait_for_function("() => typeof setState==='function'", timeout=45000)
                sp.wait_for_function("() => (window.__bofFrames|0) > 4", timeout=45000)
                for _ in range(24):
                    sp.evaluate("(ks)=>ks.forEach(k=>{try{XART.rdy(k);}catch(e){}})", keys)
                    sp.wait_for_timeout(200)
                    if sp.evaluate("(ks)=>ks.every(k=>XART.rdy(k))", keys):
                        break
                sp.evaluate(SHOT, [kind, stage, slot])
                d = sp.evaluate("()=>document.getElementById('screen').toDataURL('image/png')")
                open(os.path.join(OUT, 'shipboss_0810s_%s.png' % kind), 'wb').write(
                    base64.b64decode(d.split(',', 1)[1]))
                print('  shot     %s' % kind)
            except Exception as e:
                print('  shot     %-14s FAILED: %s' % (kind, str(e)[:80]))
            finally:
                sp.close(); sb.close()
        b.close()

    print('THE FIVE SHIP BOSSES — drawn / fires / flashes, all off real pixels\n')
    hdr = '%-14s %-5s %-20s %6s %5s %10s %10s %6s %8s %7s %5s'
    print(hdr % ('KIND', 'SLOT', 'NAME', 'HP', 'SIZE', 'DRAW px', 'FLASH px',
                 'waves', 'bullets', 'vy', 'lanes'))
    print('-' * 116)
    bad = []
    for r in res:
        if r.get('error'):
            print('%-14s ERROR %s' % (r['kind'], r['error'])); bad.append(r['kind']); continue
        print(hdr % (r['kind'], r['slot'], r['name'], r['hp'], '%dx%d' % (r['w'], r['h']),
                     '{:,}'.format(r['drawPixels']), '{:,}'.format(r['flashPixels']),
                     r['waves'], r['bullets'],
                     '%.1f-%.1f' % (r['vyMin'], r['vyMax']), r['lanes']))
        if r['drawPixels'] < 2000: bad.append(r['kind'] + ':not drawn')
        if r['flashPixels'] < 500: bad.append(r['kind'] + ':no white flash')
        if r['bullets'] < 6:       bad.append(r['kind'] + ':not firing')
    print('-' * 116)
    print('\nper-wave bullet counts (the shape of each pattern):')
    for r in res:
        if not r.get('error'):
            print('   %-14s %s   x-spread %dpx across %d lanes'
                  % (r['kind'], r['perWave'], r['spreadX'], r['lanes']))
    print('\nVERDICT:', 'ALL FIVE DRAW, FIRE AND FLASH' if not bad else 'PROBLEMS -> ' + ', '.join(bad))
    if errs: print('page errors:', errs[:4])
    json.dump(res, open(os.path.join(OUT, 'shipboss_0810s.json'), 'w'), indent=1)


if __name__ == '__main__':
    main()
