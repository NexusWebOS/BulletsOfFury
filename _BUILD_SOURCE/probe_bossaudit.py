#!/usr/bin/env python3
"""probe_bossaudit.py - all eight stage BOSSES, spawned and rendered.

The companion to probe_miniwarm.py. Same method and the same two traps guarded:

  XART.rdy() IS FALSE ON ITS FIRST CALL - it starts the decode - so spawn and render are split by
  a real-time wait, or every boss photographs as its placeholder.

  AND A "BOXY" TEST ON ROW EXTENTS ALSO FIRES ON ANY SPRITE LARGER THAN THE SCAN WINDOW, which is
  how four working minibosses got reported broken in 0812c. The numbers here are advisory; the
  PNGs are the evidence.

Reports, per boss: what it spawned as, which draw path claimed it (ship / modular / sectional /
mech / genesis / newboss / procedural fallback), and any art key its first frames asked for that
was not ready.
"""
import http.server, socketserver, threading, functools, os, base64
GAME = r'C:/Users/Mdogg/Desktop/BOF-CODE/BulletsOfFury'
OUT  = os.path.join(GAME, 'docs', 'proofs')

def serve(d):
    h = functools.partial(http.server.SimpleHTTPRequestHandler, directory=d)
    h.log_message = lambda *a, **k: None
    s = socketserver.TCPServer(("127.0.0.1", 0), h)
    threading.Thread(target=s.serve_forever, daemon=True).start()
    return s.server_address[1]

HOOK = r"""
()=>{ const r=XART.rdy.bind(XART); window.__ask=[];
      XART.rdy=function(k){ const v=r(k); if(window.__rec) window.__ask.push([k,!!v]); return v; }; }
"""
WARM = r"""
(n)=>{ ASSETS.ready=true; run.stage=n; run.pilot='cole';
       try{ beginStage(n); }catch(e){} try{ warmStage(n); }catch(e){} return true; }
"""
SPAWN = r"""
(n)=>{
  setState(GS.PLAY);
  enemies.length=0; pBullets.length=0; eBullets.length=0; subBoss=null; subBossActive=false;
  boss=null; bossActive=false;
  const kind=STAGES[n-1] && STAGES[n-1].boss;
  try{ spawnBoss(kind); }catch(e){ return {n, kind, err:String(e)}; }
  const b=boss; if(!b) return {n, kind, err:'no boss after spawnBoss'};
  b.x=VW/2; b.y=VH*0.30; b.ty=VH*0.30; b.entry=0; b.enter=false;
  window.__ask=[]; window.__rec=true;
  for(let i=0;i<8;i++){ stateT+=1/60; try{ drawWorld(1/60); }catch(e){} }
  window.__rec=false;
  const miss={}; for(const [k,v] of window.__ask) if(!v) miss[k]=1;
  /* which renderer owns it — the same order drawBoss tests in */
  const path = b._ship?'ship' : b._gen?'genesis' : b._mech?'mech' : b._sx?'sectional'
             : b.modular?'modular' : b.mega?'mega'
             : (typeof NEWBOSS!=='undefined' && NEWBOSS[n] && XART.rdy(NEWBOSS[n].idle+'_0'))?'newboss'
             : 'PROCEDURAL FALLBACK';
  const cv=document.getElementById('screen');
  return {n, kind, name:b.name||null, hp:b.hp, w:b.w, h:b.h, path,
          missing:Object.keys(miss), img:cv.toDataURL('image/png')};
}
"""

from playwright.sync_api import sync_playwright
os.makedirs(OUT, exist_ok=True)
port = serve(GAME)
with sync_playwright() as p:
    b  = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
    pg = b.new_page(viewport={'width': 620, 'height': 900}, device_scale_factor=1)
    pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=60000)
    pg.wait_for_function("()=>typeof setState==='function'", timeout=45000)
    pg.wait_for_function("()=>(window.__bofFrames|0)>4", timeout=45000)
    pg.evaluate(HOOK)

    print('%-3s %-16s %-24s %6s  %-18s %s' % ('st', 'kind', 'name', 'hp', 'draw path', 'NOT READY'))
    for st in range(1, 9):
        pg.evaluate(WARM, st)
        pg.wait_for_timeout(4000)
        r = pg.evaluate(SPAWN, st)
        if r.get('err'):
            print('%-3d %-16s *** %s' % (st, r.get('kind'), r['err'])); continue
        with open(os.path.join(OUT, 'boss_s%d_0812f.png' % st), 'wb') as f:
            f.write(base64.b64decode(r['img'].split(',', 1)[1]))
        miss = r['missing']
        print('%-3d %-16s %-24s %6d  %-18s %s'
              % (st, r['kind'], (r['name'] or '?')[:24], r['hp'], r['path'],
                 (', '.join(miss[:4]) + (' +%d' % (len(miss) - 4) if len(miss) > 4 else '')) if miss else '-'))
    b.close()
    print('\n-> docs/proofs/boss_s1..8_0812f.png')
