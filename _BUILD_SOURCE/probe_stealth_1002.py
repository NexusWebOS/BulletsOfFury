"""probe_stealth_1002 - Stage 6's stealth flights (Mike, 1002) in real Chromium.

    python3 _BUILD_SOURCE/probe_stealth_1002.py [--diff normal] [--old]

For each role (red / green / orange) and each entry (east / west / south / north):
  - a WARNING comes first: the arrow plate and the impact-imminent asterisk are drawn (by KEY, a wrap on
    XART.get) and no jet exists until the warning has run;
  - the jet then enters, drawn from its own role sheet (fb2_stealth_<role>);
  - RED opens a retina lock on the pilot with missiles bound to it; GREEN puts an atom-bomb reticle down;
    ORANGE puts machine-gun rounds in eBullets.
Also: spawnEnemy('s6bomber') on stage 6 creates NO s6bomber and plans a flight instead; s6StrikeSpawn too.
--old routes feedback_1002.js to an empty body.
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
  const L=window.__L={keys:{}};
  const g=XART.get; XART.get=function(k){L.keys[k]=(L.keys[k]||0)+1; return g.apply(this,arguments);};
  for(const k of ['fb2_stealth_red','fb2_stealth_green','fb2_stealth_orange','warn_escape_arrow_0916','bmfx_alert_green_impact_imminent','bmfx_alert_yellow_impact_imminent','bmfx_alert_red_impact_imminent','lz_bomb'])try{XART.rdy(k)}catch(e){}
  return {stage:run.stage, flights:typeof fb2Flights!=='undefined'};
}
"""
CASE = r"""
(c)=>{
  enemies.length=0; eBullets.length=0; playerLocks.length=0; groundTargetingFx.length=0;
  player.x=(camLeftX()+camRightX())/2; player.y=VH-90;
  window.__L.keys={};
  let mode=c.via;
  if(mode==='plan'){ if(typeof fb2FlightPlan!=='function')return {err:'no fb2FlightPlan'}; fb2FlightPlan(c.dir,c.role); }
  else if(mode==='bomber'){ const r=spawnEnemy('s6bomber',c.dir==='east'?-105:worldWidth()+95,VH*.25,{_side:c.dir==='east'?1:-1,_jetManeuver:'bomb'}); }
  else if(mode==='strike'){ s6StrikeSpawn(c.dir); }
  const mine=(typeof fb2Flights!=='undefined'&&fb2Flights.length)?fb2Flights[fb2Flights.length-1]:null;   // THIS case's flight; a stage director may plan others
  const out={warnFrames:0,jetBefore:0,spawnedAt:null,role:null,locks:0,lockMissiles:0,atoms:0,mg:0,bombers:0,keys:{}};
  for(let i=0;i<c.n;i++){
    window.__bofStepNow+=1000/60; loop(window.__bofStepNow);
    const pending=mine&&!mine.spawned?1:0;
    const J=mine&&mine.jet, jets=J&&!J.dead?[J]:[];
    if(pending)out.warnFrames++;
    if(mine&&!mine.spawned&&J)out.jetBefore++;
    if(J){out.shots=J._fb2Stealth.shots;out.rounds=J._fb2Rounds||0;out.jy=Math.round(J.y);if(J.dead&&out.deadAt==null)out.deadAt=i;}
    if(jets.length&&out.spawnedAt==null){out.spawnedAt=i;out.role=J._fb2Stealth.role;out.dir=J._fb2Stealth.direction;}
    out.bombers=Math.max(out.bombers,enemies.filter(e=>e.type==='s6bomber'&&!e.dead).length);
    for(const L of playerLocks)if(J&&L.src===J){out.locks=1;out.lockMissiles=Math.max(out.lockMissiles,L.missiles.length);}
    out.atoms=Math.max(out.atoms,groundTargetingFx.filter(q=>q._fb2Atom&&J&&q.owner===J).length);
    out.mg=Math.max(out.mg,eBullets.filter(b=>b.kind==='mg'&&J&&b._fb2Src===J).length);
    if(c.grabAt===i)out.grab=document.querySelector('#screen').toDataURL('image/png');
  }
  out.keys=Object.keys(window.__L.keys).filter(k=>/fb2_stealth|warn_escape|impact_imminent/.test(k));
  return out;
}
"""


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--diff', default='normal'); ap.add_argument('--old', action='store_true')
    ap.add_argument('--out', default='_shots/stealth_1002')
    a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
    from playwright.sync_api import sync_playwright
    port, stop = shoot.serve(shoot.GAME); errs = []; fails = []
    cases = [('plan', 'east', 'red'), ('plan', 'west', 'green'), ('plan', 'south', 'orange'), ('plan', 'north', 'red'),
             ('plan', 'south', 'green'), ('plan', 'east', 'orange'), ('bomber', 'east', None), ('strike', 'west', None)]
    res = []
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
        pg.wait_for_timeout(1500)
        for via, d, role in cases:
            r = pg.evaluate(CASE, {'via': via, 'dir': d, 'role': role, 'n': 300, 'grabAt': 60 if via == 'plan' and role in ('red', 'orange') else (150 if via == 'plan' else -1)})
            pg.wait_for_timeout(200)
            g = r.pop('grab', None)
            if g:
                with open(os.path.join(a.out, '%s_%s_%s.png' % (via, d, role)), 'wb') as fh: fh.write(base64.b64decode(g.split(',', 1)[1]))
            res.append((via, d, role, r)); print(via, d, role, json.dumps(r))
        b.close()
    stop()
    for via, d, role, r in res:
        tag = '%s/%s/%s' % (via, d, role)
        if r.get('err'): fails.append(tag + ': ' + r['err']); continue
        if r['bombers']: fails.append(tag + ': an s6bomber still spawned')
        if r['spawnedAt'] is None: fails.append(tag + ': no stealth jet ever entered'); continue
        if r['warnFrames'] < 40: fails.append(tag + ': warning too short (%d frames)' % r['warnFrames'])
        if r['jetBefore']: fails.append(tag + ': the jet was on the field during its own warning')
        if 'warn_escape_arrow_0916' not in r['keys']: fails.append(tag + ': no arrow drawn')
        if not any('impact_imminent' in k for k in r['keys']): fails.append(tag + ': no asterisk drawn')
        if 'fb2_stealth_' + r['role'] not in r['keys']: fails.append(tag + ': jet not drawn from its role sheet')
        if role and r['role'] != role: fails.append(tag + ': role %s' % r['role'])
        rr = r['role']
        if rr == 'red' and not (r['locks'] and r['lockMissiles']): fails.append(tag + ': red opened no retina lock with missiles')
        if rr == 'green' and not r['atoms']: fails.append(tag + ': green dropped no atom bomb')
        if rr == 'orange' and r['mg'] < 3: fails.append(tag + ': orange fired no machine gun')
    print('errors', errs[:4])
    if errs: fails.append('page errors')
    print('FAIL' if fails else 'PASS', fails)


if __name__ == '__main__':
    main()
