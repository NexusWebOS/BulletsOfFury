#!/usr/bin/env python3
"""probe_flamebox.py - the flame/ice hitbox against the plume that is actually DRAWN.

Mike: "Flamethrower and Ice breath - improve hitboxes to be from where they start t owhere they
end. anytime we hit anything with these attacks, shouild make an attack sound like all other
attacks do. Stop using that annoying beep noise wehn homing missiles are shot off at us too."

flameDraw lays the plate down as a UNIFORM column flameHalfW(lv,1) wide. flameHit used to evaluate
flameHalfW at the travel fraction, which TAPERS to flameBase at the nozzle - at lv5, 96px drawn
against 35px tested. This measures the hit boundary at three heights and compares each to the drawn
half-width, so a taper shows up as a boundary that shrinks toward the nozzle.

  ⚠ DRIVE flameFire(), NOT Input. Input's direction fields are GETTERS - assigning them is a silent
    no-op, which is how an earlier probe "held fire" for 900 frames and measured a weapon that was
    never firing. flameFire(lv) is the real entry point and takes the level directly.

  ⚠ pBullets IS REASSIGNED, not mutated. The flame is re-found from the pool after every tick
    rather than held across them.

Also counts the sounds, because "the hitbox is right" and "you can hear it land" are two claims:
the hit SFX must fire on a flame hit, and lockAlert must NOT fire on a missile lock.
"""
import http.server, socketserver, threading, functools
GAME = r'C:/Users/Mdogg/Desktop/BOF-CODE/BulletsOfFury'

def serve(d):
    h = functools.partial(http.server.SimpleHTTPRequestHandler, directory=d)
    h.log_message = lambda *a, **k: None
    s = socketserver.TCPServer(("127.0.0.1", 0), h)
    threading.Thread(target=s.serve_forever, daemon=True).start()
    return s.server_address[1]

RUN = r"""
(pilot)=>{
  ASSETS.ready=true; run.stage=1; run.pilot=pilot;
  try{ beginStage(1); }catch(e){}
  setState(GS.PLAY); player.reset();
  player.x=VW/2; player.y=VH*0.72; player.invuln=999999; player.hp=99; player.dead=false;
  run.weapon=4; run.wlevel=5;
  enemies.length=0; pBullets.length=0; eBullets.length=0;

  /* count sounds by wrapping the SFX themselves - weaponHitSfx routes to crackle/shatter/hit */
  const sfx={};
  for(const k of ['crackle','shatter','hit','lockAlert']){
    const o=Audio.SFX[k];
    if(typeof o==='function'){ Audio.SFX[k]=function(){ sfx[k]=(sfx[k]||0)+1; try{ return o.apply(this,arguments); }catch(e){} }; }
  }

  /* build the flame and let updatePlay set top/bot (they are assigned in the UPDATE, not at spawn) */
  let f=null;
  for(let i=0;i<4;i++){
    try{ flameFire(5); }catch(e){ return {err:'flameFire: '+String(e)}; }
    try{ updatePlay(1/60); }catch(e){ return {err:'updatePlay: '+String(e)}; }
    f=null; for(const b of pBullets){ if(b.kind==='flame'){ f=b; break; } }
  }
  if(!f) return {err:'no flame in pBullets'};
  if(f.top==null || f.bot==null) return {err:'flame has no top/bot'};

  const icy   = flameIsIce();
  const halfD = flameHalfWDrawn(f.lv);
  const topD  = flameSpanTop(f);
  const reach = f.bot-f.top;

  /* the hit boundary at three heights along the plume: |dx| where flameHit flips false */
  function boundaryAt(yy){
    let lo=0, hi=400;
    if(!flameHit(f, f.x, yy, 0, 0)) return -1;          // not hit even on the axis
    for(let i=0;i<40;i++){ const m=(lo+hi)/2; if(flameHit(f, f.x+m, yy, 0, 0)) lo=m; else hi=m; }
    return +lo.toFixed(1);
  }
  const yNoz = f.bot-6, yMid=(topD+f.bot)/2, yTip=topD+Math.max(6, reach*0.06);
  const bounds={nozzle:boundaryAt(yNoz), middle:boundaryAt(yMid), tip:boundaryAt(yTip)};

  /* where does it stop vertically? walk down from the tip until it stops hitting */
  let farEdge=null;
  for(let yy=f.bot+40; yy>=f.top-40; yy-=1){ if(flameHit(f, f.x, yy, 0, 0)) farEdge=yy; }

  /* END TO END: a real enemy parked off-axis at the NOZZLE - the case that used to take nothing.
     The observable is its hp, and the pool is re-read because spawn paths reassign it. */
  let dmg=null, hitSfxDelta=null;
  try{
    enemies.length=0;
    spawnEnemy(1);
    let e=null; for(const q of enemies){ if(!q.dead){ e=q; break; } }
    if(e){
      e.hp=9999; e.maxhp=9999; e.dead=false; e.enter=false; e.entry=0;
      const hp0=e.hp;
      const s0=(sfx.crackle||0)+(sfx.shatter||0)+(sfx.hit||0);
      for(let i=0;i<30;i++){
        e.x=player.x+halfD*0.75; e.y=f.bot-10;        // inside the DRAWN column, beside the ship
        e.hp=Math.min(e.hp,9999); e.dead=false;
        flameFire(5); updatePlay(1/60);
        let still=null; for(const q of enemies){ if(q===e){ still=q; break; } }
        if(!still) break;
      }
      dmg = +(hp0-e.hp).toFixed(1);
      hitSfxDelta = ((sfx.crackle||0)+(sfx.shatter||0)+(sfx.hit||0)) - s0;
    }
  }catch(e){ dmg='ERR '+String(e); }

  /* THE BEEP: enemyLockOn must no longer alarm. Pass a src with no fk - fk==='gun' early-returns. */
  const lb0=sfx.lockAlert||0;
  try{ for(let i=0;i<5;i++) enemyLockOn({x:100,y:80}, 0.7); }catch(e){}
  const lockBeeps=(sfx.lockAlert||0)-lb0;

  return {pilot, icy, lv:f.lv, halfDrawn:+halfD.toFixed(1),
          base:+flameBase(f.lv).toFixed(1), flare:+flameFlare(f.lv).toFixed(2),
          top:+f.top.toFixed(0), bot:+f.bot.toFixed(0), topDrawn:+topD.toFixed(0),
          farEdge:(farEdge==null?null:+farEdge.toFixed(0)),
          bounds, dmg, hitSfxDelta, lockBeeps};
}
"""

from playwright.sync_api import sync_playwright
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

    bad = 0
    for pilot in ('cole', 'freezer'):
        r = pg.evaluate(RUN, pilot)
        kind = 'ICE BREATH' if pilot == 'freezer' else 'FLAMETHROWER'
        print('\n=== %s (%s) ===' % (kind, pilot))
        if r.get('err'):
            print('  *** %s' % r['err']); bad += 1; continue
        print('  ice path            %s' % r['icy'])
        print('  lv %d  base %s  flare %s   -> drawn half-width %s'
              % (r['lv'], r['base'], r['flare'], r['halfDrawn']))
        print('  plume y  %s .. %s   (drawn tip %s, hitbox tip %s, nozzle %s)'
              % (r['top'], r['bot'], r['topDrawn'], r['farEdge'], r['bot']))
        b = r['bounds']
        print('  hit boundary   nozzle %-7s middle %-7s tip %-7s'
              % (b['nozzle'], b['middle'], b['tip']))
        for where in ('nozzle', 'middle', 'tip'):
            v = b[where]
            if v < 0:
                print('  *** no hit at all at the %s' % where); bad += 1
            elif abs(v - r['halfDrawn']) > 2.0:
                print('  *** %s boundary %s != drawn %s - the hitbox does not match the art'
                      % (where, v, r['halfDrawn'])); bad += 1
        if r['farEdge'] is not None and abs(r['farEdge'] - r['topDrawn']) > 3:
            print('  *** hitbox tip at %s but the plate tip is %s'
                  % (r['farEdge'], r['topDrawn'])); bad += 1
        print('  point-blank off-axis enemy took %s damage' % r['dmg'])
        if not isinstance(r['dmg'], (int, float)) or r['dmg'] <= 0:
            print('  *** IT TOOK NOTHING - inside the drawn column and unharmed'); bad += 1
        print('  hit sounds during that %s' % r['hitSfxDelta'])
        if not r['hitSfxDelta']:
            print('  *** silent - Mike asked for a sound on every hit'); bad += 1
        print('  lockAlert beeps on 5 missile locks: %s' % r['lockBeeps'])
        if r['lockBeeps']:
            print('  *** STILL BEEPING'); bad += 1

    if errs: print('\nPAGE ERRORS: %s' % errs[:3])
    print('\n%s' % ('flame/ice boxes match the art' if bad == 0 else '*** %d problem(s)' % bad))
    br.close()
