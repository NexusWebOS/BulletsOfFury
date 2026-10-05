"""probe_hivewing_1002 - the Warhive's launched escorts as a squadron (Mike, 1002), in real Chromium.

    python3 _BUILD_SOURCE/probe_hivewing_1002.py [--diff normal] [--old]

Four hivewing escorts on Stage 6, a pilot weaving left/right, ~30 simulated seconds. Asserts:
  - DIVES are warned: every dive's tell lasts >= 0.5 s with the warning lane, and the run vector equals the
    vector the tell committed to (locked for the last 40%, so a late break dodges);
  - a PINCER happens: two jets warn and fire converging dart streams from opposite edges;
  - a MISSILE play opens a retina lock from an escort with missiles bound to it;
  - LEAD AIM: on a moving pilot, burst headings differ from the straight-at-the-pilot heading;
  - zero page errors.
--old routes feedback_1002.js to an empty body (the busted arm).
"""
import argparse, base64, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shoot

SETUP = r"""
(cfg)=>{
  ASSETS.ready=true; window.__bofStepNow=performance.now(); diffKey=cfg.diff; if(typeof DIFFS!=='undefined'&&DIFFS[cfg.diff])DIFF=DIFFS[cfg.diff];
  run.pilot='cole'; run.stage=6; run.mode='arcade'; curStage=STAGES[5];
  beginStage(6); setState(GS.PLAY); player.reset(); playerHit=function(){};
  s6Opening=null; run._mission29OpeningDone=true; stagePlan=[]; enemies.length=0;
  for(let i=0;i<4;i++){const e=spawnEnemy('xelite_hivewing',camLeftX()+80+i*90,-60-i*20,{});e._hwSlot=i;e._hwN=4;e._et=i*1.37;e._hwDive=2+i*1.2;e.hp=e.maxhp=9999;}
  const L=window.__L={dives:[],pincers:{},pinShots:0,locks:0,lockMissiles:0,lead:[],diveRuns:0};
  return {n:enemies.filter(e=>e._elx==='hivewing').length};
}
"""
STEP = r"""
(a)=>{
  const L=window.__L;
  for(let i=0;i<a.n;i++){
    window.__bofStepNow+=1000/60; window.__f=(window.__f|0)+1;
    // the pilot weaves, so lead aim has something to lead
    const tx=camLeftX()+viewW()/2+Math.sin(window.__f/50)*150; player.x+=Math.max(-4,Math.min(4,tx-player.x)); player.y=VH-90;
    const pre=new Map();for(const e of enemies)if(e._elx==='hivewing')pre.set(e,{st:e._hwD&&e._hwD.st,fa:e._hwD&&e._hwD._fa,t2:e._hwD&&e._hwD._t2,burst:e._hwBurst||0,tac:e._fb2Tac&&e._fb2Tac.phase});
    loop(window.__bofStepNow);
    for(const e of enemies){if(e._elx!=='hivewing'||e.dead)continue;const P=pre.get(e)||{};const D=e._hwD,A=e._fb2Tac;
      if(D&&D.st==='run'&&P.st==='tell'){L.diveRuns++;L.dives.push({tell:+(P.t2||0).toFixed(3),warn:D._warn,locked:Math.abs((D.a||0)-(P.fa||0))<1e-6});}
      if(A&&A.kind==='pincer'){const k=A.id.replace(/-\d+$/,'');L.pincers[k]=L.pincers[k]||{sides:{},fired:0};L.pincers[k].sides[A.side]=1;if(A.phase==='fire')L.pincers[k].fired=Math.max(L.pincers[k].fired,A.shots);}
      if((e._hwBurst||0)>(P.burst||0)){const T=targetShip(e.x,e.y),direct=Math.atan2(T.y-e.y,T.x-e.x);L.lead.push(+Math.abs(e._hwBA-direct).toFixed(3));}
    }
    for(const Lk of playerLocks)if(Lk.src&&Lk.src._elx==='hivewing'){L.locks=1;L.lockMissiles=Math.max(L.lockMissiles,Lk.missiles.length);}
    if(a.grab&&!window.__grabbed){const W=enemies.find(e=>e._elx==='hivewing'&&((e._hwD&&e._hwD.st==='tell'&&e._hwD._t2>.3)||(e._fb2Tac&&e._fb2Tac.phase==='warn'&&e._fb2Tac.t>.3)));
      if(W){window.__grabbed=1;return {grab:document.querySelector('#screen').toDataURL('image/png')};}}
  }
  return {};
}
"""


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--diff', default='normal'); ap.add_argument('--old', action='store_true')
    ap.add_argument('--out', default='_shots/hivewing_1002')
    a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
    from playwright.sync_api import sync_playwright
    port, stop = shoot.serve(shoot.GAME); errs = []; fails = []
    with sync_playwright() as p:
        chrome = os.environ.get('BOF_CHROME', '/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
        b = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'], **({'executable_path': chrome} if os.path.exists(chrome) else {}))
        pg = b.new_page(viewport={'width': 1100, 'height': 1200})
        pg.on('pageerror', lambda e: errs.append(str(e)[:300]))
        pg.on('response', lambda r: errs.append('HTTP %d %s' % (r.status, r.url)) if r.status >= 400 else None)
        if a.old:
            pg.route('**/assets/feedback_1002.js', lambda r: r.fulfill(status=200, content_type='application/javascript', body='/* busted arm */'))
        pg.goto(f'http://127.0.0.1:{port}/index.html', wait_until='load', timeout=60000)
        pg.wait_for_function("() => (window.__bofFrames|0) > 4", timeout=45000)
        pg.evaluate(shoot.TRAP_RAF)
        print('setup', pg.evaluate(SETUP, {'diff': a.diff}))
        pg.wait_for_timeout(1200); shots = 0
        for k in range(180):
            r = pg.evaluate(STEP, {'n': 10, 'grab': shots < 3})
            if r.get('grab'):
                with open(os.path.join(a.out, 'warn_%d.png' % shots), 'wb') as fh: fh.write(base64.b64decode(r['grab'].split(',', 1)[1]))
                shots += 1; pg.evaluate("()=>{window.__grabbed=0}") if shots < 3 else None
                pg.evaluate("()=>{}")
            pg.wait_for_timeout(6)
        L = pg.evaluate("()=>window.__L")
        b.close()
    stop()
    print('dives', L['diveRuns'], L['dives'][:6])
    print('pincers', L['pincers'])
    print('locks', L['locks'], 'missiles', L['lockMissiles'])
    lead = L['lead']; print('lead deltas', len(lead), lead[:12])
    if not L['diveRuns']: fails.append('no dive ran')
    for d in L['dives']:
        if d['tell'] < .5: fails.append('a dive had a %.2fs tell' % d['tell']); break
    for d in L['dives']:
        if not d['locked']: fails.append('a dive ran on a vector other than the one it committed to'); break
    if not any(len(v['sides']) == 2 and v['fired'] >= 6 for v in L['pincers'].values()): fails.append('no two-sided pincer fired its streams')
    if not (L['locks'] and L['lockMissiles']): fails.append('no escort missile lock with missiles')
    if not lead or sum(1 for x in lead if x > .02) < max(1, len(lead) // 3): fails.append('bursts do not lead the moving pilot')
    print('errors', errs[:4])
    if errs: fails.append('page errors')
    print('FAIL' if fails else 'PASS', fails)


if __name__ == '__main__':
    main()
