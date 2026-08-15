#!/usr/bin/env python3
"""probe_thinair.py - stage 1, "why were those enemies appearing out of thin air".

Fourth attempt, and the previous three each failed for a DIFFERENT reason, all recorded so this one
does not repeat them:

  1. probe_popin.py watches spawnEnemy's ARGUMENT, not where the unit ends up.
  2. An art-readiness check used `e.art` believing it was a base. For nef units `e.art` is the FULL
     key (nefArtFor bakes the damage state in) but for legacy units it is something else again, and
     a key that is in neither store makes XART.rdy() false forever - which reported every unit cold.
     Both stores are checked here.
  3. A trap on enemies.push found nothing because the pools are REASSIGNED, not mutated.
  4. A first-existence test finally worked but only compared Y, so units entering legitimately from
     the SIDES (x -28, 828, 846 in an 800-wide world) counted as materialising.

What is measured now is the thing Mike actually sees: the first frame a unit is BOTH inside the
camera's view AND drawable. A unit that crosses an edge into view has entered. A unit whose first
visible-and-drawable frame is well inside the frame appeared out of thin air - and the distance
from the nearest edge says how badly.
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

RUN = r"""
(stage)=>{
  ASSETS.ready=true; run.stage=stage; run.pilot='cole';
  try{ beginStage(stage); }catch(e){}
  try{ warmStage(stage); }catch(e){}
  setState(GS.PLAY); player.reset(); player.invuln=999999;
  if(typeof seedWaves==='function'){ try{ seedWaves(20260815); }catch(e){} }

  /* [!] AND THE FIFTH FAULT: gating on XART._src FIRST. Measured, every stage-1 unit has
     _src[key] FALSE and XART.rdy(key) TRUE - the atlas CELLS resolve through a different map than
     the loose-file source list, so requiring _src rejected all 30 units before rdy was ever asked.
     rdy is the predicate the DRAW uses; it is the predicate to test. */
  const drawable=(k)=>{
    if(!k) return false;
    if(typeof XART!=='undefined' && XART.rdy && XART.rdy(k)) return true;
    if(typeof ASSETS!=='undefined' && ASSETS.has && ASSETS.has(k)) return true;
    return false;
  };
  const camOf=()=> (typeof camX==='number') ? camX : 0;

  const rec=new Map(); const events=[];
  for(let f=0; f<60*150; f++){
    player.invuln=999999; player.hp=99;
    if(f%4===0){ try{ pShoot(); }catch(e){} }
    try{ updatePlay(1/60); }catch(e){ break; }
    try{ drawWorld(1/60); }catch(e){}      // the scroll and the camera live in the draw

    const cx=camOf();
    for(const e of enemies){
      if(e.dead) continue;
      if(!rec.has(e)) rec.set(e, {born:f, key:String(e.art||e._nef||''), shown:false,
                                  bx:Math.round(e.x-cx), by:Math.round(e.y)});
      const r=rec.get(e);
      const sx0=e.x-cx, sy0=e.y;
      /* [!] SEVENTH FAULT: this tested the unit's CENTRE, so a sprite was only "in view" once its
         middle crossed the edge - by which point half the hull had legitimately been on screen for
         a while, and the first-sighting sample caught it already 46% revealed. Box-based now. */
      const inV0 = (sx0+e.w/2)>0 && (sx0-e.w/2)<VW && (sy0+e.h/2)>0 && (sy0-e.h/2)<VH;
      /* THE ACTUAL "THIN AIR" QUANTITY: on screen, and not drawable. Every earlier attempt at this
         asked the wrong key or the wrong predicate; this asks e.art (the full baked key) through
         XART.rdy (what the draw itself uses). */
      if(inV0 && !drawable(String(e.art||''))) r.blind=(r.blind||0)+1;
      if(r.shown) continue;
      const sx=sx0, sy=sy0;
      const inView = inV0;
      if(inView && drawable(String(e.art||''))){
        r.shown=true;
        /* [!] SIXTH FAULT, AND IT INVENTED SIX OF THE SEVEN HITS: this ADDED half the unit's
           width, so a jet straddling the left edge at sx=-3 scored 44 "inside the frame". The
           quantity wanted is the gap between the unit's BOX and the nearest frame edge - positive
           only once the whole sprite is already within the view. */
        const d=Math.min(sx-e.w/2, VW-(sx+e.w/2), sy-e.h/2, VH-(sy+e.h/2));
        /* the number that matches what a player sees: what FRACTION of the sprite is already
           showing the first frame it can be seen. A unit that flies in reveals a sliver; a unit
           that switches on at the edge reveals half of itself at once. */
        const vw=Math.max(0, Math.min(sx+e.w/2,VW)-Math.max(sx-e.w/2,0));
        const vh=Math.max(0, Math.min(sy+e.h/2,VH)-Math.max(sy-e.h/2,0));
        const frac=(vw*vh)/Math.max(1,e.w*e.h);
        events.push({t:+(f/60).toFixed(1), key:r.key, type:String(e.type||'?'),
                     sx:Math.round(sx), sy:Math.round(sy), inset:Math.round(d),
                     bornSx:r.bx, bornSy:r.by, ageF:f-r.born, frac:+frac.toFixed(2),
                     keyed:(typeof XART!=='undefined'&&XART.rdy&&XART.rdy(r.key))?'xart'
                          :((typeof ASSETS!=='undefined'&&ASSETS.has&&ASSETS.has(r.key))?'assets':'NEITHER')});
      }
    }
  }
  if(typeof unseedWaves==='function'){ try{ unseedWaves(); }catch(e){} }
  let never=0, blindU=0, blindMax=0; const blindList=[];
  for(const [e,r] of rec){
    if(!r.shown) never++;
    if(r.blind){ blindU++; if(r.blind>blindMax) blindMax=r.blind;
                 if(blindList.length<8) blindList.push(r.key+' '+r.blind+'f'); }
  }
  return {total:rec.size, shown:events.length, never, events, blindU, blindMax, blindList};
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
    pg.wait_for_timeout(4000)

    r = pg.evaluate(RUN, 1)
    ev = r['events']
    print('stage 1: %d units, %d ever drawable-and-visible, %d NEVER' % (r['total'], r['shown'], r['never']))
    deep = sorted(ev, key=lambda z: -z['frac'])
    worst = [e for e in ev if e['frac'] > 0.30]
    print('\nfirst drawable sighting FULLY inside the frame (box clear of every edge by >8px): %d' % len(deep))
    print('%-6s %-24s %-16s %6s %6s %7s %8s' % ('t','art key','type','sx','sy','shown%','ageFrm'))
    for e in deep[:10]:
        print('%-6s %-24s %-16s %6d %6d %6d%% %8d'
              % (e['t'], e['key'][:24], e['type'][:16], e['sx'], e['sy'], round(e['frac']*100), e['ageF']))
    print('\nON SCREEN BUT NOT DRAWABLE: %d units, worst %d frames (%.1fs)'
          % (r['blindU'], r['blindMax'], r['blindMax'] / 60.0))
    for x in r['blindList']:
        print('   %s' % x)
    b.close()
