#!/usr/bin/env python3
"""probe_quadlaser.py — do the level-1 miniboss's four beams fire, and does killing one OPEN its lane?

Mike: "Program lasers to shoot from the beams on the level 1 miniboss." The claim is not just
"it shoots" — it is that each cannon holds a fixed lane and breaking it removes that lane for
good, then the nose takes over with charge lasers. So this measures the LANE SET at four cannon
counts and checks it shrinks to exactly the surviving muzzles.
"""
import http.server, socketserver, threading, os, functools

GAME = r'C:/Users/Mdogg/Desktop/BOF-CODE/BulletsOfFury'

def serve(d):
    h = functools.partial(http.server.SimpleHTTPRequestHandler, directory=d)
    h.log_message = lambda *a, **k: None
    s = socketserver.TCPServer(("127.0.0.1", 0), h)
    threading.Thread(target=s.serve_forever, daemon=True).start()
    return s.server_address[1]

RUN = r"""
(deadIds) => {
  ASSETS.ready=true; run.pilot='cole'; run.mode='arcade';
  beginStage(1); setState(GS.PLAY);
  subBoss=null; eBullets.length=0;
  const t0=performance.now(); let f=0; const step=()=>loop(t0+(f++)*16.7);
  for(let i=0;i<40;i++) step();
  spawnSubBoss('quadlaser'); const b=subBoss;
  if(!b) return {error:'no spawn'};
  b.enter=false; b.x=VW/2; b.y=150; b.ty=150;
  for(const c of b._qlCan) if(deadIds.indexOf(c.id)>=0) c.dead=true;
  const S=b.w/384;

  /* ⚠ MUZZLE LANES ARE COMPUTED AT FIRE TIME, NOT AT SETUP. updateSubBoss drifts an air
     miniboss to WORLD centre (worldWidth()/2 + sin*96), so a stage-1 unit placed at VW/2=240
     is near 496 by the time it shoots. The first cut of this probe snapshotted b.x during
     setup and reported every volley as off-target by a constant 256 - the game was right and
     the measurement was stale. Same family as probe_seam.py recomputing the value under test. */
  eBullets.length=0;
  const volleys=[]; let muzzleX=[]; let guard=0;
  while(volleys.length<3 && guard++<900){
    const n0=eBullets.length; step();
    if(eBullets.length>n0){
      if(!muzzleX.length) muzzleX=b._qlCan.filter(c=>!c.dead).map(c=>Math.round(b.x+(c.mz[0]-192)*S));
      volleys.push(eBullets.slice(n0).map(z=>({x:Math.round(z.x), vx:+z.vx.toFixed(2), k:z.kind})));
    }
  }
  const flat=volleys.length?volleys[0]:[];
  return {alive:b._qlCan.filter(c=>!c.dead).length, muzzleX,
          perVolley: volleys.map(v=>v.length),
          firstVolleyX: flat.map(z=>z.x), kinds:[...new Set(flat.map(z=>z.k))],
          fanned: flat.some(z=>Math.abs(z.vx)>0.05),
          muzFlash: +(b._muz||0).toFixed(2), chgN: b._qlChgN|0};
}
"""

CASES = [([], 'all four alive'),
         (['left_outer'], 'left_outer destroyed'),
         (['left_outer','right_outer'], 'both outers destroyed'),
         (['left_outer','left_inner','right_inner','right_outer'], 'ALL destroyed -> charge phase')]

def main():
    from playwright.sync_api import sync_playwright
    port = serve(GAME); url='http://127.0.0.1:%d/index.html'%port
    with sync_playwright() as p:
        b = p.chromium.launch(args=['--disable-gpu','--no-sandbox','--mute-audio'])
        pg = b.new_page(viewport={'width':620,'height':900}, device_scale_factor=1)
        pg.goto(url, wait_until='load', timeout=60000)
        pg.wait_for_function("()=>typeof setState==='function'", timeout=45000)
        pg.wait_for_function("()=>(window.__bofFrames|0)>4", timeout=45000)
        print('%-32s %5s %-26s %-9s %-26s %s' % ('CASE','alive','muzzle lanes','per volley','bullets fired at x','kind'))
        print('-'*128)
        bad=[]
        for dead, label in CASES:
            r = pg.evaluate(RUN, dead)
            if r.get('error'): print(label, r['error']); bad.append(label); continue
            print('%-32s %5d %-26s %-9s %-26s %s' % (label, r['alive'], str(r['muzzleX']),
                  str(r['perVolley']), str(r['firstVolleyX']), ','.join(r['kinds'])))
            if r['alive']:
                if sorted(r['firstVolleyX']) != sorted(r['muzzleX']):
                    bad.append(label+': bullets not on the live muzzles')
            else:
                if len(r['firstVolleyX'])<3: bad.append(label+': no charge laser')
        print('-'*128)
        print('VERDICT:', 'BEAMS FIRE FROM THE CANNONS AND EACH KILL OPENS ITS LANE' if not bad else 'PROBLEMS -> '+'; '.join(bad))
        b.close()

if __name__=='__main__':
    main()
