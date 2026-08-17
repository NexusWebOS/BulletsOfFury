#!/usr/bin/env python3
"""probe_tanksideways.py - which tanks move sideways, and what pattern is actually driving them?

Mike: "tanks do not go sideways."

`case 's1tank': tankTick(e, dt)` is forward/back only - tankTick never touches e.x. So any lateral
motion is coming from somewhere OUTSIDE it, which is the same shape as the jet-displacement bug
(CLAUDE.md: "something outside jetTick displaces them").

The prime suspect is the standing _selfPat trap: a unit whose type is not listed there has the
pattern its apply* function just set OVERWRITTEN by the generic block, and several of those generic
patterns ('sine', 'weave', 'strafe', 'hunt', 'dive') carry an e.x term. The 0811l note records
exactly this happening to stage-4 jets through a spelling gap.

⚠ MEASURED, NOT DERIVED. This spawns each stage's real waves, finds the TANKS, and records both the
pattern they ended up with and how far they actually travel in x. A tank is identified by its roster
entry (wheels/tracked art or a type naming a tank/truck), never by assuming a pattern.

⚠ enemies IS REASSIGNED, not mutated - units are tracked by identity and re-found each frame.
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
(stage)=>{
  ASSETS.ready=true; run.stage=stage; run.pilot='cole';
  try{ beginStage(stage); }catch(e){ return {err:'beginStage: '+String(e)}; }
  setState(GS.PLAY); player.reset();
  player.x=VW/2; player.y=VH*0.80; player.invuln=999999; player.hp=999;
  enemies.length=0; pBullets.length=0; eBullets.length=0; boss=null; subBoss=null;

  /* ⚠ TIGHT. The first version also matched on e.art and e.wheels and swept up jets, mines,
     corvettes and landing craft - 14 of the 16 "sideways tanks" it reported were not tanks. The
     TYPE is the only reliable identifier. */
  const isTank=(e)=>/tank|apc|truck/i.test(String(e.type||e.kind||''));

  const seen=new Map();   // identity -> {type, pat0, x0, minx, maxx, frames}
  const SEC=14;
  for(let f=0; f<60*SEC; f++){
    player.invuln=999999; player.hp=999; player.dead=false;
    try{ updatePlay(1/60); }catch(e){ return {err:'updatePlay: '+String(e), f}; }
    for(const e of enemies){
      if(e.dead) continue;
      if(!isTank(e)) continue;
      let r=seen.get(e);
      if(!r){
        r={type:String(e.type||e.kind||'?'), pat:'?', pats:{},
           x0:e.x, minx:e.x, maxx:e.x, entry:!!e.enter, n:0};
        seen.set(e,r);
      }
      /* pat is read EVERY frame, not just on first sighting - it is assigned after spawn, so
         sampling once caught undefined and printed '?' for every single unit. */
      const _p=String(e.pat==null?'(none)':e.pat); r.pats[_p]=(r.pats[_p]||0)+1; r.pat=_p;
      /* ignore the ENTRY glide - a unit flying in from off-screen legitimately moves in x.
         Only measure once it is on station. */
      if(e.enter || (e.entry||0)>0){ r.x0=e.x; r.minx=e.x; r.maxx=e.x; continue; }
      /* SPAN ALONE CANNOT TELL A ONE-FRAME SNAP FROM CONTINUOUS SLIDING, and the spawn snap
         legitimately repositions a tank onto drivable ground in a single frame. Track the largest
         single-frame step and how many frames actually moved: a snap is one big step, drift is many
         small ones. */
      if(r.lastx!=null){
        const d=Math.abs(e.x-r.lastx);
        if(d>0.05){ r.moving=(r.moving||0)+1; if(d>(r.maxStep||0)) r.maxStep=d; }
      }
      r.lastx=e.x;
      if(e.x<r.minx) r.minx=e.x;
      if(e.x>r.maxx) r.maxx=e.x;
      r.n++;
    }
  }
  const out=[];
  for(const r of seen.values()){
    if(r.n<30) continue;                       // too short-lived to judge
    out.push({type:r.type, pat:Object.keys(r.pats).join(','), span:+(r.maxx-r.minx).toFixed(1),
              frames:r.n, moving:(r.moving||0), maxStep:+((r.maxStep||0)).toFixed(1)});
  }
  return {stage, tanks:out};
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

    LATERAL = {'sine', 'weave', 'strafe', 'hunt', 'dive', 'gbox', 'kamikaze', 'swoop'}
    bad = 0
    total = 0
    print('%-7s %-20s %8s  %s' % ('stage', 'type', 'x span', 'verdict'))
    for stage in (1, 4, 7):
        r = pg.evaluate(RUN, stage)
        if r.get('err'):
            print('%-7d *** %s' % (stage, r['err'])); bad += 1; continue
        if not r['tanks']:
            print('%-7d (no tanks seen in 14s)' % stage); continue
        for t in r['tanks']:
            total += 1
            v = ''
            if t['moving'] <= 2 and t['span'] > 6:
                v = 'one-frame spawn snap (%.0fpx), then holds its lane' % t['maxStep']
            elif t['span'] > 6:
                v = '*** SLIDES - moved on %d frames, max step %.1f' % (t['moving'], t['maxStep'])
                bad += 1
            else:
                v = 'holds its lane'
            print('%-7d %-20s %8.1f  %s' % (stage, t['type'][:20], t['span'], v))

    if errs: print('\nPAGE ERRORS: %s' % errs[:3])
    if total == 0:
        print('\n*** NO TANKS MEASURED - nothing was tested')
    else:
        print('\n%s' % ('every tank holds its lane (%d measured)' % total
                        if bad == 0 else '*** %d tank(s) drift sideways' % bad))
    br.close()
