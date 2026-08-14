#!/usr/bin/env python3
"""probe_popin.py — does anything MATERIALISE in frame instead of entering?

Mike, repeatedly: "I still have enemies appearing out of thin air for level 1 ... We've gone over
this one like 20x."

⚠ THE ORIGINAL TEST ONLY LOOKED AT THE TOP EDGE (`y - h/2 > 0`) AND IGNORED x ENTIRELY, and that
is why this has been chased for drops. Stage 1's corner-route jets spawn at x = -28 and x = VW+28
with y = 96/150 — deliberately off the SIDE, at an entry altitude, which is exactly how a corner
route is supposed to start (drop 0801kn, and the clamp that broke it in 0809a). The old test
flagged all four as pop-ins because their top edge is inside the frame. They are not popping in;
they are entering from the side, and "fixing" them would have broken the routes.

A unit appears out of thin air when NO PART of it is off ANY edge on its first frame — there is no
edge it could be entering from. That is the test here. It reports both numbers so the difference
between them stays visible:

    ENTERING   some part off an edge, on any side. Correct, whatever the top edge says.
    POPPED     the whole box is inside the play area. This is the bug.
"""
import http.server, socketserver, threading, os, functools
GAME=r'C:/Users/Mdogg/Desktop/BOF-CODE/BulletsOfFury'
def serve(d):
    h=functools.partial(http.server.SimpleHTTPRequestHandler, directory=d); h.log_message=lambda *a,**k:None
    s=socketserver.TCPServer(("127.0.0.1",0),h); threading.Thread(target=s.serve_forever,daemon=True).start()
    return s.server_address[1]
RUN=r"""
(stage)=>{
  ASSETS.ready=true; run.pilot='cole'; run.mode='arcade';
  beginStage(stage); setState(GS.PLAY); player.invuln=1e9;
  const pops=[], side=[], top=[];
  /* ⚠ MEASURED ON THE UNIT'S FIRST DRAWN FRAME, NOT AT spawnEnemy's RETURN — and the first cut
     of this got it wrong in a way that invented four bugs. l6Crosser and its siblings CORRECT x
     immediately after the spawn call ("spawnEnemy clamps x into the field — place truly
     offscreen"), so reading e.x on return catches an intermediate value: stage 5's octo and
     stage 6's fang both showed at exactly x=480 (=VW) and were flagged as materialising in open
     sky, when a line later they are at worldWidth()+50.

     That is the probe_seam.py lesson exactly — a probe that reads the wrong moment asserts a bug
     that is not there. Units are queued at spawn and their box is read after the NEXT loop(),
     which is the first frame the player could actually see them. */
  let pending=[];
  const real=spawnEnemy;
  spawnEnemy=function(){ const e=real.apply(null,arguments);
    /* record where the WAVE asked for it, so a unit that is moved between the spawn call and its
       first drawn frame reports both numbers and the mover can be identified instead of guessed */
    /* ⚠ inPlace IS A DECLARATION, NOT AN EXCUSE. Some units are AUTHORED to appear where they
       are: a splitter's two halves emerge from the wreck, a sewer maw surfaces mid-screen. Those
       are beats, not pop-ins, and a check that flags them invites someone to "fix" the design.
       They carry {inPlace:1} at their spawn site so the intent lives in the game, not in a list
       maintained here. Anything WITHOUT it is expected to enter from an edge. */
    if(e && !e.prop && e.pattern!=='prop' && !e.inPlace){ e.__sx=e.x; e.__sy=e.y; pending.push(e); }
    return e; };
  const classify=()=>{
    if(!pending.length) return;
    const W=(typeof worldWidth==='function')?worldWidth():VW;
    for(const e of pending){
      if(e.dead) continue;
      const t=e.y-e.h*0.5, b=e.y+e.h*0.5, l=e.x-e.w*0.5, r=e.x+e.w*0.5;
      const rec={t:e.type, x:Math.round(e.x), y:Math.round(e.y),
                 sx:Math.round(e.__sx), sy:Math.round(e.__sy),
                 w:Math.round(e.w), h:Math.round(e.h),
                 top:Math.round(t), left:Math.round(l), right:Math.round(r), W:Math.round(W),
                 pat:e.pattern, route:e._route||null, esw:!!e._esw, ent:!!e._entered};
      /* off ANY edge = there is an edge it can be entering from */
      if(t<=0 || b>=VH || l<=0 || r>=W) { (t<=0?top:side).push(rec); }
      else pops.push(rec);
    }
    pending=[];
  };
  const t0=performance.now();
  for(let i=0;i<2700;i++){ loop(t0+i*16.7); classify(); }
  spawnEnemy=real;
  const byType={}; for(const p of pops) byType[p.t]=(byType[p.t]||0)+1;
  return {stage, total:pops.length+side.length+top.length,
          popped:pops.length, fromTop:top.length, fromSide:side.length,
          byType, sample:pops.slice(0,6), sideSample:side.slice(0,2)};
}
"""
from playwright.sync_api import sync_playwright
port=serve(GAME); url='http://127.0.0.1:%d/index.html'%port
with sync_playwright() as p:
    # every stage that fields a roster — the VW-vs-worldWidth confusion is not stage-specific,
    # it just happens to be visible on the stages whose world is wider than the viewport
    for st in [1,2,3,4,5,6,7,8]:
        b=p.chromium.launch(args=['--disable-gpu','--no-sandbox','--mute-audio'])
        pg=b.new_page(viewport={'width':620,'height':900}, device_scale_factor=1)
        pg.goto(url, wait_until='load', timeout=60000)
        pg.wait_for_function("()=>typeof setState==='function'", timeout=45000)
        pg.wait_for_function("()=>(window.__bofFrames|0)>4", timeout=45000)
        r=pg.evaluate(RUN, st)
        print('stage %d: %d spawns | entering from TOP %d, from a SIDE %d | POPPED IN %d  %s'
              % (r['stage'], r['total'], r['fromTop'], r['fromSide'], r['popped'], r['byType'] or ''))
        for s2 in r['sample']:      print('        POP  ', s2)
        for s2 in r['sideSample']:  print('        side ', s2)
        b.close()
