#!/usr/bin/env python3
"""probe_ticks.py — the units that "fire from their own tick": do they actually fire?

Stage 7 fields 14 units with e.shoots false on every one, and stage 8 the same. The spawn cases
say that is deliberate - volcTick, sewerTick, orbitalTick and the elite8 rig are supposed to fire
them on their own cadences. This spawns ONE of each in isolation and counts what it puts out over
20 seconds, so a system that is declared and never fires cannot hide behind a comment.
"""
import http.server, socketserver, threading, os, functools, json

GAME=r'C:/Users/Mdogg/Desktop/BOF-CODE/BulletsOfFury'
def serve(d):
    h=functools.partial(http.server.SimpleHTTPRequestHandler, directory=d); h.log_message=lambda *a,**k:None
    s=socketserver.TCPServer(("127.0.0.1",0),h); threading.Thread(target=s.serve_forever,daemon=True).start()
    return s.server_address[1]

RUN = r"""
([stage, types, seconds]) => {
  ASSETS.ready=true; run.pilot='cole'; run.mode='arcade';
  beginStage(stage); setState(GS.PLAY);
  player.invuln=1e9; player.x=VW/2; player.y=VH*0.8;
  const out={};
  const t0=performance.now(); let f=0;
  for(const ty of types){
    enemies.length=0; eBullets.length=0;
    let e=null;
    try { e = spawnEnemy(ty); } catch(err){ out[ty]={err:String(err.message||err).slice(0,50)}; continue; }
    if(!e) e = enemies[0];
    if(!e){ out[ty]={err:'no spawn'}; continue; }
    e.x=VW/2; e.y=VH*0.28; e.enter=false; e._entT=9;
    let born=0;
    const frames=Math.round(seconds*60);
    for(let i=0;i<frames;i++){
      loop(t0+(f++)*16.7);
      for(const b of eBullets){ if(b.__s) continue; b.__s=1; born++; }
      if(!enemies.length) break;              // it died or left; stop counting
    }
    out[ty]={born, shoots:!!e.shoots, alive:enemies.length>0, hp:e.hp};
  }
  return out;
}
"""

GROUPS = [
  (7, ['skimmer','sentry','crawler','shambler','maw','barge'], 'sewerTick'),
  (2, ['ash','lance','skim','disc','eye','cruc'],              'volcTick'),
  (5, ['needle','oracle','crescent','hauler'],                 'orbitalTick'),
  (8, ['talon','hell','cdisc'],                                'elite8'),
  (6, ['l6x_st','l6x_tf'],                                     'L6X'),
]

def main():
    from playwright.sync_api import sync_playwright
    port=serve(GAME); url='http://127.0.0.1:%d/index.html'%port
    res={}
    with sync_playwright() as p:
        for stage, types, label in GROUPS:
            b=p.chromium.launch(args=['--disable-gpu','--no-sandbox','--mute-audio'])
            pg=b.new_page(viewport={'width':620,'height':900}, device_scale_factor=1)
            try:
                pg.goto(url, wait_until='load', timeout=60000)
                pg.wait_for_function("()=>typeof setState==='function'", timeout=45000)
                pg.wait_for_function("()=>(window.__bofFrames|0)>4", timeout=45000)
                r=pg.evaluate(RUN, [stage, types, 20])
                res[label]=r
                print('%s  (stage %d, 20s each, one unit in isolation)' % (label, stage))
                for ty in types:
                    v=r.get(ty)
                    if not v: print('   %-12s no result' % ty); continue
                    if v.get('err'): print('   %-12s ERROR %s' % (ty, v['err'])); continue
                    flag = '' if v['born']>0 else '   <-- FIRES NOTHING'
                    print('   %-12s bullets=%-4d shoots=%-5s alive=%s%s' % (ty, v['born'], v['shoots'], v['alive'], flag))
                print()
            except Exception as ex:
                print('%s FAILED %s\n' % (label, str(ex)[:80]))
            finally:
                pg.close(); b.close()
    json.dump(res, open(os.path.join(GAME,'docs','proofs','ticks_0810w.json'),'w'), indent=1)

if __name__=='__main__':
    main()
