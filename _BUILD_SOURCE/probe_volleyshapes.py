#!/usr/bin/env python3
"""probe_volleyshapes.py — do the volley patterns fire, and is each one a DIFFERENT shape?

Mike: "Are too predictable or too simple like, needs to be have the bullets of fury feel with
machine gun styled enemy attacks and missiles and random patterns and screen filling patterns."

Three questions, because "more patterns" is easy to claim and easy to get wrong:

  1. DOES IT FIRE AT ALL. Every pattern is invoked through the real enemyVolley on a real spawned
     unit. This project's dominant failure is a system that is declared and never fires — the
     quad-laser's muzzles, _qlChg, enemyVolley's own fireCd, lordshadows. A `case` in a switch
     that no table entry reaches is exactly that shape.
  2. IS IT A DISTINCT SHAPE. Rounds are reported as count, horizontal span and vertical stagger.
     Two patterns with the same three numbers are the same pattern wearing two names.
  3. DOES SCREEN-FILLING ACTUALLY FILL. curtain/ripple are measured against the CAMERA width,
     since that is what the player sees — bullets live in world space and stage 1's world is 800
     against a 480 camera, so a pattern built on worldWidth would look wide and play thin.

Also reports rounds-per-second per stage, because the honest risk of adding four patterns is
simply making the screen busier, and Mike has cut volume before.
"""
import http.server, socketserver, threading, functools, os
GAME=r'C:/Users/Mdogg/Desktop/BOF-CODE/BulletsOfFury'
def serve(d):
    h=functools.partial(http.server.SimpleHTTPRequestHandler, directory=d); h.log_message=lambda *a,**k:None
    s=socketserver.TCPServer(("127.0.0.1",0),h); threading.Thread(target=s.serve_forever,daemon=True).start()
    return s.server_address[1]

SHAPES=r"""
()=>{
  ASSETS.ready=true; run.pilot='cole'; run.mode='arcade'; run.stage=1;
  beginStage(1); setState(GS.PLAY); player.reset(); player.invuln=1e9;
  player.x=240; player.y=430;
  const pats=['fan','wall','pincer','stagger','rake','salvo','curtain','ripple'];
  const out=[];
  for(const p of pats){
    /* drive the REAL enemyVolley by handing a unit a table row for this pattern — the same path
       enemyVolleyTick uses, not a reimplementation of the switch */
    enemies.length=0; eBullets.length=0;
    const e=spawnEnemy('s1jetdelta', 240, 120, {});
    if(!e){ out.push({p, err:'no unit'}); continue; }
    const saved=ENEMY_VOLLEY[e.type];
    ENEMY_VOLLEY[e.type]={pat:p, every:1};
    e._volN=0; e._volSeed=0;
    const ok=enemyVolley(e, true);
    const b=eBullets.slice();
    ENEMY_VOLLEY[e.type]=saved;
    if(!b.length){ out.push({p, fired:ok, n:0}); continue; }
    const xs=b.map(v=>v.x), ys=b.map(v=>v.y);
    const kinds={}; for(const v of b) kinds[v.kind]=(kinds[v.kind]||0)+1;
    out.push({p, fired:ok, n:b.length,
              spanX:Math.round(Math.max(...xs)-Math.min(...xs)),
              spanY:Math.round(Math.max(...ys)-Math.min(...ys)),
              kinds:Object.keys(kinds).join('+'),
              camSpanPct:+(100*(Math.max(...xs)-Math.min(...xs))/VW).toFixed(0)});
  }
  /* and does rotation actually rotate? same unit, consecutive volleys, which shape each time */
  enemies.length=0; eBullets.length=0;
  const r=spawnEnemy('s1jetdelta', 240, 120, {});
  const seq=[];
  if(r){
    const saved=ENEMY_VOLLEY[r.type];
    ENEMY_VOLLEY[r.type]={alt:['fan','rake'], every:1};
    r._volSeed=0;
    for(let i=0;i<6;i++){ eBullets.length=0; r._volN=i; enemyVolley(r,true); seq.push(eBullets.length); }
    ENEMY_VOLLEY[r.type]=saved;
  }
  /* ⚠ salvo IS GATED ON _eMslAllow(), which is Math.random() < 0.45 on stage 1 — so a single
     invocation firing nothing is the BUDGET working, not the pattern being broken. The two look
     identical from one sample, which is exactly the kind of thing this project mistakes for a
     dead system. Roll it 40 times and report the hit rate against the gate's own odds. */
  let salvoHits=0;
  enemies.length=0;
  const sv=spawnEnemy('s1jetdelta', 240, 120, {});
  if(sv){
    const saved=ENEMY_VOLLEY[sv.type];
    ENEMY_VOLLEY[sv.type]={pat:'salvo', every:1};
    for(let i=0;i<40;i++){ eBullets.length=0; sv._volN=i; sv._volSeed=0; enemyVolley(sv,true);
      if(eBullets.length) salvoHits++; }
    ENEMY_VOLLEY[sv.type]=saved;
  }
  return {out, rotation:seq,
          salvo:{hits:salvoHits, of:40,
                 gate:(typeof _eMslAllow==='function')?'present':'MISSING',
                 launcher:(typeof eMissileHoming==='function')?'present':'MISSING'}};
}
"""

RATE=r"""
([stage, newPatterns])=>{
  let _s=20260811>>>0;
  Math.random=function(){ _s=(_s*1664525+1013904223)>>>0; return _s/4294967296; };
  ASSETS.ready=true; run.pilot='cole'; run.mode='arcade';
  /* ⚠ THE BASELINE ARM COLLAPSES THE TABLE BACK TO WHAT IT WAS. Every alt:[...] row reverts to
     its FIRST entry, which is the pattern that row carried before 0811s — so the A/B measures
     the four new shapes and the rotation, and nothing else. Adding four patterns and reporting
     the resulting bullet count with no before is how "more variety" ships as "twice the bullets";
     Mike has cut volume once already. */
  if(!newPatterns){
    for(const k in ENEMY_VOLLEY){
      const V=ENEMY_VOLLEY[k];
      if(V.alt && V.alt.length){ ENEMY_VOLLEY[k]={pat:V.alt[0], every:V.every}; }
    }
  }
  beginStage(stage); setState(GS.PLAY); player.invuln=1e9;
  let rounds=0, peak=0, prev=0;
  const t0=performance.now();
  for(let i=0;i<1800;i++){
    loop(t0+i*16.7);
    /* ⚠ eBullets is REASSIGNED by its cull, so a wrapped push is discarded on the first frame.
       Count the RISE in length instead — the standing trap in this project. */
    if(eBullets.length>prev) rounds += eBullets.length-prev;
    prev=eBullets.length;
    if(eBullets.length>peak) peak=eBullets.length;
  }
  return {stage, rounds, perSec:+(rounds/30).toFixed(1), peakOnScreen:peak};
}
"""
from playwright.sync_api import sync_playwright
port=serve(GAME); url='http://127.0.0.1:%d/index.html'%port
def page(p):
    b=p.chromium.launch(args=['--disable-gpu','--no-sandbox','--mute-audio'])
    pg=b.new_page(viewport={'width':620,'height':900}, device_scale_factor=1)
    pg.goto(url, wait_until='load', timeout=60000)
    pg.wait_for_function("()=>typeof setState==='function'", timeout=45000)
    pg.wait_for_function("()=>(window.__bofFrames|0)>4", timeout=45000)
    return b, pg
with sync_playwright() as p:
    b, pg = page(p)
    r=pg.evaluate(SHAPES)
    print('%-9s %5s %4s %8s %8s %9s  %s' % ('pattern','fired','n','spanX','spanY','% of cam','kinds'))
    for e in r['out']:
        if e.get('err') or not e.get('n'):
            print('%-9s %5s %4s   *** FIRED NOTHING ***' % (e['p'], e.get('fired'), e.get('n',0))); continue
        print('%-9s %5s %4d %8d %8d %8s%%  %s' % (e['p'], e['fired'], e['n'], e['spanX'], e['spanY'],
                                                  e['camSpanPct'], e['kinds']))
    print('\nrotation (rounds per consecutive volley, alt fan/rake): %s  -> %s'
          % (r['rotation'], 'ROTATES' if len(set(r['rotation']))>1 else '*** SAME SHAPE EVERY TIME ***'))
    s=r['salvo']
    print('salvo   %d/%d volleys produced missiles   gate=%s launcher=%s   -> %s'
          % (s['hits'], s['of'], s['gate'], s['launcher'],
             'the missile BUDGET is thinning it, not a dead pattern'
             if s['hits'] else '*** DEAD PATTERN ***'))
    b.close()
    print()
    print('%-8s %22s %22s' % ('', 'BEFORE (old table)', 'AFTER (0811s)'))
    for st in (1,5,7):
        row={}
        for newp in (False, True):
            b, pg = page(p)
            row[newp]=pg.evaluate(RATE,[st,newp])
            b.close()
        a,c=row[False],row[True]
        print('stage %d  %8s/sec peak %-5d %8s/sec peak %-5d   %+.0f%% rounds'
              % (st, a['perSec'], a['peakOnScreen'], c['perSec'], c['peakOnScreen'],
                 100.0*(c['rounds']-a['rounds'])/max(1,a['rounds'])))
