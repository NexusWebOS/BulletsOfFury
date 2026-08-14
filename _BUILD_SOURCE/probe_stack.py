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

⚠ THE BOAT COLUMNS SPLIT BEACHED FROM LIVE, and that distinction is the whole of the boats
question. Drop 0809n made a boat stop steering and withdraw off the bottom once the coastline has
passed under it — past that point being over jungle is CORRECT and deliberate. A flat
"boats on land" count includes those, which is why it reads 779/779 whatever the water rule does.
LIVE is the number that means anything.

MEASURED BASELINES, with no separation and no water rule in the tree (drop 0811j):

    stage 1   839 overlapping pair-frames, worst 71.9% burial, 955/955 naval samples ON LAND
    stage 4   127 overlapping pair-frames, worst 153.6% burial (one unit fully inside another)

⚠ Both of those are RETRACTED as targets — see PASSOVER_0811L. They were one sample of an unseeded
distribution that swings between 839 and 424, and `worst` is a max over 1800 frames that cannot
tell "stacked" from "spawned on the same point". Use the SETTLED columns.
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
  pickWaterX:    typeof pickWaterX,
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
      boatsOnLand=0, boatSamples=0, uid=0, worstWho=null,
      wetFixed=0, boatsSeen=0, beachedSamples=0, liveSamples=0, liveOnLand=0,
      liveNoWaterRow=0, liveWaterExisted=0, widestWater=0, hullW=0, rowsWithWater=0;
  const t0=performance.now();
  for(let i=0;i<1800;i++){
    loop(t0+i*16.7); frames++;
    for(let a=0;a<enemies.length;a++){
      const A=enemies[a]; if(A.dead||A.prop||A.enter) continue;
      if(A.__age==null){ A.__age=0; A.__id=++uid; } A.__age++;
      if(A._naval && _landMasks['mapJungle']){
        const m=_landMasks['mapJungle'];
        const range=Math.max(0,m.h-VH), mapY=Math.max(0,range-mapScroll)+A.y;
        const onLand=_isLand('mapJungle', A.x, mapY);
        boatSamples++; if(onLand) boatsOnLand++;
        if(A._wetFix) wetFixed++;
        if(!A.__seen){ A.__seen=1; boatsSeen++; }
        /* ⚠ BEACHED IS DELIBERATE, LIVE IS THE QUESTION. See the header. */
        if(A._beached) beachedSamples++;
        else { liveSamples++; if(onLand) liveOnLand++;
          /* ⚠ IS THERE ANY WATER ON THIS ROW AT ALL? That is the difference between a PLACEMENT
             bug (water exists, the boat is not on it) and a WAVE bug (the script is fielding
             boats after the coastline has gone by, so no x on this row is water and no placement
             rule can ever succeed). pickWaterX returning null is the same signal from inside the
             game; this measures it from outside, across the whole play width. */
          /* ⚠ HOW WIDE IS THE CHANNEL, AND HOW WIDE IS THE HULL? pickWaterX requires the whole
             footprint on water. If the river is narrower than the boat, NO x satisfies that and
             the search returns null everywhere — which looks identical to "there is no water".
             Three attempts at this fix have now died on the difference. */
          let run=0, best=0, any=0;
          for(let sx=PLAY.x+4; sx<PLAY.x+PLAY.w-4; sx+=4){
            if(!_isLand('mapJungle', sx, mapY)){ any=1; run+=4; if(run>best) best=run; } else run=0;
          }
          if(onLand){ if(!any) liveNoWaterRow++; else liveWaterExisted++; }
          if(best>widestWater) widestWater=best;
          hullW=Math.round((A.w||48)*0.9);
          if(any) rowsWithWater++;
        }
      }
      for(let b=a+1;b<enemies.length;b++){
        const B=enemies[b]; if(B.dead||B.prop||B.enter) continue;
        const ox=(A.w+B.w)*0.42-Math.abs(B.x-A.x), oy=(A.h+B.h)*0.42-Math.abs(B.y-A.y);
        if(ox>0&&oy>0){ badPairs++;
          const f=Math.min(ox/Math.min(A.w,B.w), oy/Math.min(A.h,B.h));
          if(f>worst) worst=f;
          /* ⚠ SETTLED IS THE NUMBER THAT DESCRIBES WHAT MIKE SEES. `worst` is a MAX over 1800
             frames, so two units that spawn on the same point pin it near 100% on the single
             frame they appear, however fast they are then pushed apart. A pair only counts as
             settled once BOTH units are half a second old, which is exactly the difference
             between "stacked" and "spawned together". */
          if((A.__age>30) && (B.__age||0)>30){ settledPairs++;
            if(f>worstSettled){ worstSettled=f;
              /* WHO. A burial figure with no unit attached is a number to tune against rather
                 than a bug to fix — stage 4 sat at 150% for two attempts before anyone asked
                 which two units it was. */
              const tag=(U)=>({type:U.type, pat:U.pattern, w:Math.round(U.w), h:Math.round(U.h),
                               x:Math.round(U.x), y:Math.round(U.y),
                               grounded:!!(U.ground||U.microturret||U.pattern==='ground'),
                               naval:!!U._naval, beached:!!U._beached});
              worstWho={a:tag(A), b:tag(B), ox:Math.round(ox), oy:Math.round(oy)};
            } }
        }
      }
    }
  }
  return {stage, frames, badPairs, settledPairs,
          worstOverlapPct:+(worst*100).toFixed(1),
          worstSettledPct:+(worstSettled*100).toFixed(1),
          worstWho, boatSamples, boatsOnLand, wetFixed, boatsSeen,
          beachedSamples, liveSamples, liveOnLand, liveNoWaterRow, liveWaterExisted,
          widestWater, hullW, rowsWithWater};
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
    ok = s['enemySeparate']=='function' and s['sepShift']=='function' and s['pickWaterX']=='function'
    print('SCOPE  enemySeparate=%s  sepShift=%s  sepLandRef=%s  pickWaterX=%s  SEP_MIN=%s   -> %s'
          % (s['enemySeparate'], s['sepShift'], s['sepLandRef'], s['pickWaterX'], s['SEP_MIN'],
             'REACHABLE' if ok else '*** MISSING AT GLOBAL SCOPE - every number below is meaningless ***'))
    b.close()
    print()
    for st in [1,4]:
        for sep in [False, True]:
            b, pg = page(p)
            r=pg.evaluate(RUN,[st,sep])
            print('stage %d  sep %-3s  pair-frames %-6d worst %6.1f%%  |  SETTLED %-6d worst %6.1f%%'
                  % (r['stage'], 'ON' if sep else 'off', r['badPairs'], r['worstOverlapPct'],
                     r['settledPairs'], r['worstSettledPct']))
            if r['boatSamples']:
                print('          boats %d distinct, %d sample-frames | LIVE %d of which ON LAND %d | beached (correct) %d | solved %d'
                      % (r['boatsSeen'], r['boatSamples'], r['liveSamples'], r['liveOnLand'],
                         r['beachedSamples'], r['wetFixed']))
                if r['liveOnLand']:
                    print('          of those %d live-on-land: %d had NO WATER ANYWHERE ON THE ROW (a wave problem), %d had water somewhere (a placement problem)'
                          % (r['liveOnLand'], r['liveNoWaterRow'], r['liveWaterExisted']))
                print('          channel: widest contiguous water on any sampled row = %dpx, hull footprint = %dpx  -> %s'
                      % (r['widestWater'], r['hullW'],
                         'the hull FITS' if r['widestWater']>=r['hullW'] else
                         '*** THE HULL DOES NOT FIT — pickWaterX can never succeed ***'))
            w=r.get('worstWho')
            if w:
                f=lambda u:'%s/%s %dx%d @(%d,%d)%s%s' % (u['type'],u['pat'],u['w'],u['h'],u['x'],u['y'],
                                                         ' GROUND' if u['grounded'] else '',
                                                         ' NAVAL' if u['naval'] else '')
                print('          worst settled pair:  %s   vs   %s   (ox %d, oy %d)'
                      % (f(w['a']), f(w['b']), w['ox'], w['oy']))
            b.close()
        print()
