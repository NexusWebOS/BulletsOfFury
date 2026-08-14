#!/usr/bin/env python3
"""probe_pelletfix.py — does the MG pellet still flip between two shapes?

The fault (drop 0811y): the art picker toggled mfx_mg_2_0 (18x20 blob) against mfx_mg_2_2
(20x45 streak) on performance.now(), seven times a second, so the round's drawn width swung
between about 14px and 7px in flight.

Three things checked, all against the REAL picker rather than a copy of its logic:

  1. SCOPE. pelletKey/pelletFam are declared next to FIRETYPES, in the region of game.js where
     DEAD_SUBBOSS, ARSENAL_DRONES and liveType all turned out to be function-scoped inside
     spawnEnemy's never-closed `if`. An art picker that cannot be reached draws nothing.
  2. MONOTONIC, NOT TOGGLING. Walk one round's lifetime and record the frame index it asks for
     each step. A birth reel only ever goes up and then holds; the old code alternated.
  3. THE FAMILIES ARE WIRED. Each stage should ask for its own colour family, and all five
     families x five frames should resolve as registered art.
"""
import http.server, socketserver, threading, functools, os
GAME=r'C:/Users/Mdogg/Desktop/BOF-CODE/BulletsOfFury'
def serve(d):
    h=functools.partial(http.server.SimpleHTTPRequestHandler, directory=d); h.log_message=lambda *a,**k:None
    s=socketserver.TCPServer(("127.0.0.1",0),h); threading.Thread(target=s.serve_forever,daemon=True).start()
    return s.server_address[1]
RUN=r"""
()=>{
  const out={scope:{pelletKey:typeof pelletKey, pelletFam:typeof pelletFam,
                    PELLET_FAM:(typeof PELLET_FAM==='undefined')?'undefined':'object'}};
  if(typeof pelletKey!=='function') return out;

  /* 2. one round's lifetime, through the real picker. b.t is what the eBullets loop advances. */
  run.stage=1;
  const b={kind:'mg', t:0, vx:0, vy:2.5, _ph:0};
  const seq=[];
  for(let i=0;i<40;i++){ b.t=i*0.01; seq.push(+pelletKey(b).split('_').pop()); }
  let monotonic=true;
  for(let i=1;i<seq.length;i++) if(seq[i]<seq[i-1]) monotonic=false;
  out.seq=seq.join('');
  out.monotonic=monotonic;
  out.distinct=Array.from(new Set(seq)).length;

  /* the OLD behaviour, for contrast: what the wall-clock toggle produced over the same span */
  const old=[]; for(let i=0;i<10;i++) old.push([0,2][(Math.floor((i*70)/70))%2]);
  out.oldSeq=old.join('');

  /* 3. every family/frame registered, and each stage's pick */
  const miss=[];
  for(let f=0;f<5;f++) for(let n=0;n<5;n++){
    const k='mfx_mg_'+f+'_'+n; if(!(XART._src && XART._src[k])) miss.push(k);
  }
  out.missing=miss;
  out.byStage={};
  for(let s=1;s<=9;s++){ run.stage=s; out.byStage[s]=pelletFam({}); }
  run.stage=1;
  return out;
}
"""
from playwright.sync_api import sync_playwright
port=serve(GAME); url='http://127.0.0.1:%d/index.html'%port
with sync_playwright() as p:
    b=p.chromium.launch(args=['--disable-gpu','--no-sandbox','--mute-audio'])
    pg=b.new_page(viewport={'width':620,'height':900}, device_scale_factor=1)
    pg.goto(url, wait_until='load', timeout=60000)
    pg.wait_for_function("()=>typeof setState==='function'", timeout=45000)
    pg.wait_for_function("()=>(window.__bofFrames|0)>4", timeout=45000)
    r=pg.evaluate(RUN)
    s=r['scope']
    ok = s['pelletKey']=='function' and s['pelletFam']=='function'
    print('SCOPE   pelletKey=%s pelletFam=%s PELLET_FAM=%s  -> %s'
          % (s['pelletKey'], s['pelletFam'], s['PELLET_FAM'],
             'REACHABLE' if ok else '*** NOT AT GLOBAL SCOPE — the picker never runs ***'))
    if ok:
        print('\nframe index over one round\'s first 0.40s')
        print('   before (wall-clock toggle) : %s ...' % r['oldSeq'])
        print('   after  (own age, birth)    : %s' % r['seq'])
        print('   monotonic=%s  distinct frames used=%d  -> %s'
              % (r['monotonic'], r['distinct'],
                 'NO TOGGLING' if r['monotonic'] else '*** STILL FLIPS BACKWARDS ***'))
        names={0:'red',1:'blue',2:'orange',3:'green',4:'white'}
        print('\nper-stage pellet family: ' + '  '.join(
            '%s=%s'%(k,names.get(int(v),'?')) for k,v in sorted(r['byStage'].items(), key=lambda kv:int(kv[0]))))
        print('registered plates missing: %s' % (', '.join(r['missing']) if r['missing'] else 'none (all 25)'))
    b.close()
