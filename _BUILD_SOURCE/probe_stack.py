#!/usr/bin/env python3
"""probe_stack.py — do enemies still stack, and are the boats in the water?

Mike: "make sure enemies do not collide with each other or stack on each other like that" and
"boats only exsit on the water section."

OVERLAP is measured as the worst pair on any frame, as a fraction of the smaller unit's box, so a
number here is "how buried was the most buried unit" rather than a count that hides severity.
BOATS-ON-LAND samples the land mask under each naval unit, which is the same alpha the game uses.

⚠ IT REPORTS SCOPE FIRST, AND THAT IS NOT DECORATION. enemySeparate is declared a few hundred
lines above updatePlay, in the same file region where DEAD_SUBBOSS, ARSENAL_DRONES and liveType
all turned out to be function-scoped inside spawnEnemy's never-closed `if` — each of them correct,
registered, and unreachable at runtime for drops at a time. A separation pass that is never called
measures exactly like a separation pass that does not work. So the first thing printed is whether
the function exists at global scope, and the run is meaningless if it says MISSING.

⚠ AND IT RUNS BOTH SIDES ITSELF, in a fresh browser each, because the standing trap in this
project is that comparing two runs measures wave randomness rather than the change. Same stage,
same frame count, separation the only difference.

MEASURED BASELINES, with no separation and no water rule in the tree (drop 0811j):

    stage 1   839 overlapping pair-frames, worst 71.9% burial, 955/955 naval samples ON LAND
    stage 4   127 overlapping pair-frames, worst 153.6% burial (one unit fully inside another)

Those are the numbers any fix has to beat. For reference, the reverted relaxation pass took stage 1
from 839 pair-frames to 152 and the worst case from 71.9% to 51.8% - it helped a great deal and
still did not clear it, which is worth knowing before someone assumes a nudge is enough.
"""
import http.server, socketserver, threading, os, functools
GAME=r'C:/Users/Mdogg/Desktop/BOF-CODE/BulletsOfFury'
def serve(d):
    h=functools.partial(http.server.SimpleHTTPRequestHandler, directory=d); h.log_message=lambda *a,**k:None
    s=socketserver.TCPServer(("127.0.0.1",0),h); threading.Thread(target=s.serve_forever,daemon=True).start()
    return s.server_address[1]

SCOPE=r"""
()=>({
  enemySeparate: typeof enemySeparate,
  sepShift:      typeof sepShift,
  sepLandRef:    typeof sepLandRef,
  SEP_MIN:       (typeof SEP_MIN==='undefined') ? 'undefined' : SEP_MIN,
})
"""

RUN=r"""
([stage, sepOn])=>{
  /* ⚠ THE WAVES ARE SEEDED, and without this the arms are not comparable. An unseeded pair of
     runs moved the sep-OFF pair-frame count between 839 and 424 on stage 1 — a bigger swing than
     anything separation does — which is this project's standing "comparing two runs measures wave
     randomness" trap in its purest form. Seeded, both arms field the identical battle and the
     only difference left is the code under test. */
  let _s=20260811>>>0;
  Math.random=function(){ _s=(_s*1664525+1013904223)>>>0; return _s/4294967296; };

  ASSETS.ready=true; run.pilot='cole'; run.mode='arcade';
  beginStage(stage); setState(GS.PLAY); player.invuln=1e9;
  window.__sepOff = !sepOn;
  let worst=0, worstSettled=0, frames=0, badPairs=0, settledPairs=0,
      boatsOnLand=0, boatSamples=0, uid=0, worstWho=null;
  const t0=performance.now();
  for(let i=0;i<1800;i++){
    loop(t0+i*16.7); frames++;
    for(let a=0;a<enemies.length;a++){
      const A=enemies[a]; if(A.dead||A.prop||A.enter) continue;
      if(A.__age==null){ A.__age=0; A.__id=++uid; } A.__age++;
      if(A._naval && _landMasks['mapJungle']){
        const m=_landMasks['mapJungle'];
        const range=Math.max(0,m.h-VH), mapY=Math.max(0,range-mapScroll)+A.y;
        boatSamples++;
        if(_isLand('mapJungle', A.x, mapY)) boatsOnLand++;
      }
      for(let b=a+1;b<enemies.length;b++){
        const B=enemies[b]; if(B.dead||B.prop||B.enter) continue;
        const ox=(A.w+B.w)*0.42-Math.abs(B.x-A.x), oy=(A.h+B.h)*0.42-Math.abs(B.y-A.y);
        if(ox>0&&oy>0){ badPairs++;
          const f=Math.min(ox/Math.min(A.w,B.w), oy/Math.min(A.h,B.h));
          if(f>worst) worst=f;
          /* ⚠ SETTLED IS THE NUMBER THAT DESCRIBES WHAT MIKE SEES. `worst` is a MAX over 1800
             frames, so two units that spawn on the same point pin it near 100% on the single
             frame they appear, however fast they are then pushed apart — which is why the
             recorded 71.9% baseline barely moves under a working separation pass and is a poor
             target. A pair only counts as settled once BOTH units are half a second old, which
             is exactly the difference between "stacked" and "spawned together". */
          if((A.__age>30) && (B.__age||0)>30){ settledPairs++;
            if(f>worstSettled){ worstSettled=f;
              /* WHO. A burial figure with no unit attached is a number to tune against rather
                 than a bug to fix — stage 4 sat at 150% for two attempts before anyone asked
                 which two units it was. */
              const tag=(U)=>({type:U.type, pat:U.pattern, w:Math.round(U.w), h:Math.round(U.h),
                               x:Math.round(U.x), y:Math.round(U.y),
                               grounded:!!(U.ground||U.microturret||U.pattern==='ground'),
                               naval:!!U._naval, prop:!!U.prop});
              worstWho={a:tag(A), b:tag(B), ox:Math.round(ox), oy:Math.round(oy)};
            } }
        }
      }
    }
  }
  return {stage, frames, badPairs, settledPairs,
          worstOverlapPct:+(worst*100).toFixed(1),
          worstSettledPct:+(worstSettled*100).toFixed(1),
          worstWho, boatSamples, boatsOnLand};
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
    s = pg.evaluate(SCOPE)
    ok = s['enemySeparate']=='function' and s['sepShift']=='function'
    print('SCOPE  enemySeparate=%s  sepShift=%s  sepLandRef=%s  SEP_MIN=%s   -> %s'
          % (s['enemySeparate'], s['sepShift'], s['sepLandRef'], s['SEP_MIN'],
             'REACHABLE' if ok else '*** MISSING AT GLOBAL SCOPE — every number below is meaningless ***'))
    b.close()
    print()
    for st in [1,4]:
        for sep in [False, True]:
            b, pg = page(p)
            r=pg.evaluate(RUN,[st,sep])
            print('stage %d  sep %-3s  pair-frames %-6d  worst %6.1f%%  |  SETTLED pair-frames %-6d worst %6.1f%%  |  boats %-5d on LAND %d'
                  % (r['stage'], 'ON' if sep else 'off', r['badPairs'], r['worstOverlapPct'],
                     r['settledPairs'], r['worstSettledPct'],
                     r['boatSamples'], r['boatsOnLand']))
            w=r.get('worstWho')
            if w:
                f=lambda u:'%s/%s %dx%d @(%d,%d)%s%s' % (u['type'],u['pat'],u['w'],u['h'],u['x'],u['y'],
                                                         ' GROUND' if u['grounded'] else '',
                                                         ' NAVAL' if u['naval'] else '')
                print('          worst settled pair:  %s   vs   %s   (ox %d, oy %d)'
                      % (f(w['a']), f(w['b']), w['ox'], w['oy']))
            b.close()
        print()
