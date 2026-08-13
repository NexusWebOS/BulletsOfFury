#!/usr/bin/env python3
"""probe_types.py — which enemy TYPES does each stage actually field, and which of them SHOOT?

The volley layer's first cut targeted drone/gunship/turret/mech/octo — generic names read off the
type switch rather than out of the live rosters — and fired exactly zero rounds. Same class of
mistake as ENEMY_ART aliasing jet1..5 onto alien drone-ships: the switch lists what the engine CAN
draw, not what a stage SPAWNS. This asks the running game.
"""
import http.server, socketserver, threading, os, functools, json

GAME = r'C:/Users/Mdogg/Desktop/BOF-CODE/BulletsOfFury'

def serve(d):
    h = functools.partial(http.server.SimpleHTTPRequestHandler, directory=d)
    h.log_message = lambda *a, **k: None
    s = socketserver.TCPServer(("127.0.0.1", 0), h)
    threading.Thread(target=s.serve_forever, daemon=True).start()
    return s.server_address[1]

RUN = r"""
([stage, seconds]) => {
  ASSETS.ready=true; run.pilot='cole'; run.mode='arcade';
  beginStage(stage); setState(GS.PLAY);
  player.invuln = 1e9;
  const seen = {};
  const t0 = performance.now();
  const frames = Math.round(seconds*60);
  for(let i=0;i<frames;i++){
    loop(t0+i*16.7);
    for(const e of enemies){
      if(e.__tseen) continue; e.__tseen=1;
      const k = e.type||'?';
      seen[k] = seen[k] || {n:0, shoots:0, prof:{}};
      seen[k].n++;
      if(e.shoots) seen[k].shoots++;
      if(e.atkProfile) seen[k].prof[e.atkProfile] = (seen[k].prof[e.atkProfile]||0)+1;
    }
  }
  return {stage, seen};
}
"""

def main():
    from playwright.sync_api import sync_playwright
    port = serve(GAME); url='http://127.0.0.1:%d/index.html'%port
    out={}
    with sync_playwright() as p:
        for st in [1,2,3,4,5,6,7,8]:
            b = p.chromium.launch(args=['--disable-gpu','--no-sandbox','--mute-audio'])
            pg = b.new_page(viewport={'width':620,'height':900}, device_scale_factor=1)
            try:
                pg.goto(url, wait_until='load', timeout=60000)
                pg.wait_for_function("()=>typeof setState==='function'", timeout=45000)
                pg.wait_for_function("()=>(window.__bofFrames|0)>4", timeout=45000)
                r = pg.evaluate(RUN, [st, 40])
                out[st]=r['seen']
                items = sorted(r['seen'].items(), key=lambda z:-z[1]['n'])
                print('stage %d' % st)
                for k,v in items:
                    prof = ','.join('%s x%d'%(a,c) for a,c in v['prof'].items()) or '-'
                    print('   %-16s n=%-3d shoots=%-3d profile=%s' % (k, v['n'], v['shoots'], prof))
            except Exception as ex:
                print('stage %d FAILED %s' % (st, str(ex)[:70]))
            finally:
                pg.close(); b.close()
    json.dump(out, open(os.path.join(GAME,'docs','proofs','types_by_stage_0810u.json'),'w'), indent=1)

if __name__=='__main__':
    main()
