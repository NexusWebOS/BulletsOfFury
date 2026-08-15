#!/usr/bin/env python3
"""probe_appear.py - "they appeared out of thin air instead of coming from the top of the screen".

probe_popin.py reports ZERO pop-ins on all eight stages, measuring where units SPAWN. Mike is
still seeing them appear mid-screen, so spawn position is not the thing that is wrong.

The hypothesis this tests: the unit spawns correctly above the top edge and flies down INVISIBLE,
because XART.rdy() is false until something asks for its key - and the first thing to ask is the
first draw. It then becomes visible wherever it happens to be, which is mid-screen. That is the
same unwarmed-art fault already found in the minibosses (0812c) and the bosses (0812f), and it
would look exactly like what he describes.

Measures, over a live stage:
  ART AT SPAWN   for every unit spawned, whether its art key was ready the moment it existed.
  VISIBLE Y      the y at which each unit FIRST drew a pixel, vs the y it spawned at.
  OVERLAP        pairwise box overlap between live units, for "they stack on each other".
"""
import http.server, socketserver, threading, functools, os
GAME = r'C:/Users/Mdogg/Desktop/BOF-CODE/BulletsOfFury'

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

  const seen=new Map();          // enemy -> {spawnY, artKey, readyAtSpawn, firstDrawY}
  let maxOverlap=0, overlapPairs=0, enterPairs=0, samples=0;

  const artOf=(e)=> e.art || e._nef || e._vk || null;

  for(let f=0; f<60*90; f++){
    player.invuln=999999; player.hp=99;
    try{ updatePlay(1/60); }catch(e){ return {err:String(e)}; }

    for(const e of enemies){
      if(e.dead) continue;
      if(!seen.has(e)){
        const k=artOf(e);
        seen.set(e, {y:Math.round(e.y), k:k,
                     rdy:(k && typeof XART!=='undefined') ? !!XART.rdy(k) : null,
                     vis:null});
      }
      const rec=seen.get(e);
      if(rec.vis===null && rec.k && typeof XART!=='undefined' && XART.rdy(rec.k)) rec.vis=Math.round(e.y);
      /* THE QUANTITY THAT MATTERS is not "was it cold at spawn" but "how long was it ON SCREEN
         and undrawable" - a unit that decodes while still above the top edge costs nothing. */
      if(e.y>0 && e.y<VH && rec.k && typeof XART!=='undefined' && !XART.rdy(rec.k)) rec.blind=(rec.blind||0)+1;
    }
    /* pairwise overlap, sampled - two units sharing more than a third of the smaller box is the
       "stacked on top of each other" Mike photographed */
    if(f%20===0){
      const live=enemies.filter(e=>!e.dead && e.y>-40 && e.y<VH+40);
      samples++;
      for(let i=0;i<live.length;i++) for(let j=i+1;j<live.length;j++){
        const a=live[i], b=live[j];
        const ow=Math.min(a.x+a.w/2,b.x+b.w/2)-Math.max(a.x-a.w/2,b.x-b.w/2);
        const oh=Math.min(a.y+a.h/2,b.y+b.h/2)-Math.max(a.y-a.h/2,b.y-b.h/2);
        if(ow>0&&oh>0){
          const frac=(ow*oh)/Math.max(1,Math.min(a.w*a.h,b.w*b.h));
          if(frac>0.33){ overlapPairs++; if(a.enter||b.enter) enterPairs++; }
          if(frac>maxOverlap) maxOverlap=frac;
        }
      }
    }
  }
  if(typeof unseedWaves==='function'){ try{ unseedWaves(); }catch(e){} }

  /* THE ART CHECK ABOVE WAS MEANINGLESS and is left only as a warning: `e.art` holds a BASE
     ('nef_s1_jungle_tank') and the draw appends a damage state ('_intact'), so the base is never a
     key in any store and XART.rdy() on it is false forever. That reported 24/24 units "art cold"
     and one of them blind for 5,220 frames, which is what an always-false predicate looks like.

     WHAT IS MEASURED NOW is the thing Mike described: the y at which each unit FIRST EXISTS in
     the enemies array, by whatever spawner put it there. A unit that first appears below the top
     edge did not fly in - it materialised. */
  let total=0, onscreen=0, worst=-9999; const bad=[];
  for(const [e,r] of seen){
    total++;
    if(r.y>4){ onscreen++; if(r.y>worst) worst=r.y;
               if(bad.length<6) bad.push((r.k||'?')+'@y'+r.y); }
  }
  return {stage, total, onscreen, worst, bad,
          maxOverlap:+maxOverlap.toFixed(2), overlapPairs, enterPairs, samples};
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
    pg.wait_for_timeout(3000)

    print('%-3s %6s %14s %9s %8s %8s %8s' % ('st','units','MATERIALISED','worst-y','maxOvlp','stacked','entering'))
    for st in (1, 2, 3):
        r = pg.evaluate(RUN, st)
        if r.get('err'):
            print('%-3d *** %s' % (st, r['err'])); continue
        print('%-3d %6d %14d %9d %8s %8d %8d   %s'
              % (r['stage'], r['total'], r['onscreen'], r['worst'],
                 r['maxOverlap'], r['overlapPairs'], r['enterPairs'], ', '.join(r['bad'][:4])))
    b.close()
