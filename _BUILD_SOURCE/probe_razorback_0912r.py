#!/usr/bin/env python3
"""
probe_razorback_0912r.py - THE RAZORBACK SONIC SIEGE TANK, STAGE 1 MINIBOSS, IN REAL CHROMIUM.

    python3 _BUILD_SOURCE/probe_razorback_0912r.py --out /tmp/rzb

Mike, 0912: "This tank should be a sonic wave/sonic boom and missile tank that makes sense. it cant
fire off 3 missiles in spread at once, but it can certainly rapid fire and twist and turn and fire
off 1 by 1 rapidly in spread ... This one, should replace the stage 1 miniboss entirely."

Asserted on behaviour, through the debug host:
  * stage 1's miniboss IS the Razorback, and it draws its own rig from its own art
  * it twists and turns - the hull heading sweeps and more than one compass frame is drawn
  * SONIC HAMMER fires rounds AND a pressure wave, with Cole's sonic release
  * RAZOR RACK: one retina, missiles leave ONE AT A TIME, down a spread of distinct headings
  * only the exposed part takes damage - a real player round on the turret while the guns live
    does nothing, and one on a gun does
  * guns -> turret -> hull -> dead, in that order
  * the hull phase rams
⚠ The draw is identified by wrapping XART.get and recording the KEY (CLAUDE.md: XART.get returns a
canvas with no .src, and a size match cannot say whose art it is).
"""
import os, sys, argparse, base64
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shoot

SETUP = r"""
async () => {
  const B=window.BOSSMODE;
  const fr=()=>new Promise(r=>requestAnimationFrame(()=>r()));
  let started=false, role=null;
  for(const r of ['mini','sub','subboss','miniboss']){ try{ if(B.start(1,r,'cole',false)){ started=true; role=r; break; } }catch(e){} }
  const t0=performance.now();
  while(performance.now()-t0<30000 && !(typeof subBoss!=='undefined' && subBoss && subBoss._rzb && B.player && !B.player.dead)) await fr();
  B.setInvuln(true);
  const keys=Object.keys(BOFX.img).filter(k=>k.indexOf('rzb_')===0);
  const t1=performance.now();
  while(performance.now()-t1<15000 && !keys.every(k=>XART.rdy(k))) await fr();
  window.__rz={keys:[], snd:{}};
  const og=XART.get.bind(XART);
  XART.get=function(k){ if(typeof k==='string' && k.indexOf('rzb_')===0) window.__rz.keys.push(k); return og(k); };
  for(const n of ['coleSonicBoom','sonicChargeStart','missile','retinaCharge','clank','bossPhase']){
    const f=Audio.SFX[n]; window.__rz.snd[n]=0;
    Audio.SFX[n]=function(){ window.__rz.snd[n]++; return f&&f.apply(this,arguments); };
  }
  return {started:started, role:role, kind:(SUBBOSS[1]||{}).kind, rzb:!!(subBoss&&subBoss._rzb),
          name:subBoss?subBoss.name:null, ready:keys.filter(k=>XART.rdy(k)).length, of:keys.length};
}
"""

ARRIVE_AND_TURN = r"""
async () => {
  const fr=()=>new Promise(r=>requestAnimationFrame(()=>r()));
  const b=subBoss, R=b._rzb;
  const t0=performance.now();
  while(performance.now()-t0<6000 && R.state==='arrival') await fr();
  const arrived=R.state;
  window.__rz.keys.length=0;
  let aMin=1e9, aMax=-1e9, tMin=1e9, tMax=-1e9, xs=[];
  const t1=performance.now();
  // hold it in the guns phase and let it drive its own attack cycle for a while
  while(performance.now()-t1<7000){ await fr(); aMin=Math.min(aMin,R.a); aMax=Math.max(aMax,R.a);
    tMin=Math.min(tMin,R.turret); tMax=Math.max(tMax,R.turret); xs.push(b.x); player.x=b.x+Math.sin(performance.now()/700)*160; }
  const hulls=[...new Set(window.__rz.keys.filter(k=>/^rzb_hull_\d$/.test(k)))];
  const parts=[...new Set(window.__rz.keys)];
  return {arrived:arrived, hullSweep:+(aMax-aMin).toFixed(3), turretSweep:+(tMax-tMin).toFixed(3),
          xSpan:Math.round(Math.max(...xs)-Math.min(...xs)), hulls:hulls, parts:parts};
}
"""

SONIC = r"""
async () => {
  const fr=()=>new Promise(r=>requestAnimationFrame(()=>r()));
  const b=subBoss, R=b._rzb;
  for(const q of eBullets) if(q._rzb) q.dead=true;
  R.waves=[]; window.__rz.snd.coleSonicBoom=0;
  R.attack='sonic'; R.at=0; R.beat=-1; R.trans=0;
  let rounds=0, waves=0, charged=false;
  const t0=performance.now();
  while(performance.now()-t0<2600){ await fr(); if(R.charge>0.5) charged=true;
    rounds=Math.max(rounds, eBullets.filter(q=>q.kind==='rzbSonic' && !q.dead).length); waves=Math.max(waves, R.waves.length); }
  return {charged:charged, rounds:rounds, waves:waves, boom:window.__rz.snd.coleSonicBoom};
}
"""

MISSILES = r"""
async () => {
  const fr=()=>new Promise(r=>requestAnimationFrame(()=>r()));
  const b=subBoss, R=b._rzb;
  for(const q of eBullets) if(q._rzb) q.dead=true;
  playerLocks=[];
  player.x=b.x; player.y=VH*0.80;
  R.attack='missiles'; R.at=0; R.beat=-1; R.trans=0;
  const seen=new Set(); let maxPerFrame=0, heads=[], retinas=0;
  const t0=performance.now();
  while(performance.now()-t0<4200){
    await fr();
    retinas=Math.max(retinas, playerLocks.filter(L=>L.src===b).length);
    let fresh=0;
    for(const q of eBullets){ if(q.kind==='rzbMissile' && !seen.has(q)){ seen.add(q); fresh++; heads.push(+Math.atan2(q.vy,q.vx).toFixed(2)); } }
    maxPerFrame=Math.max(maxPerFrame, fresh);
  }
  const lockBound=[...seen].filter(q=>q._lockId).length;
  return {total:seen.size, maxPerFrame:maxPerFrame, distinctHeadings:new Set(heads).size, retinas:retinas, lockBound:lockBound};
}
"""

PARTS = r"""
async () => {
  const fr=()=>new Promise(r=>requestAnimationFrame(()=>r()));
  const b=subBoss, R=b._rzb;
  R.trans=0; R.state='guns';
  const hp0=b.hp, turret0=R.pools.turret, left0=R.pools.left;
  // a REAL player round on the turret while both guns live
  pBullets.push({x:b.x, y:b.y, vx:0, vy:0, w:8, h:14, dmg:9, t:0});
  await fr(); await fr();
  const turretAfter=R.pools.turret, hpAfterArmour=b.hp;
  // a REAL player round on the left gun
  const g=rzbWorld(b,-57,96);
  pBullets.push({x:g.x, y:g.y, vx:0, vy:0, w:8, h:14, dmg:9, t:0});
  await fr(); await fr();
  const leftAfter=R.pools.left;
  const states=[R.state];
  // break the guns, then the turret, then the hull, through hitSubBoss at each part's own point
  for(const k of ['left','right']){ const p=rzbWorld(b,k==='left'?-57:57,96); R.trans=0; hitSubBoss(9999,p.x,p.y); }
  states.push(R.state);
  const gunsCleared = R.pools.left<=0 && R.pools.right<=0;
  const hpAfterGuns=b.hp;
  // the transition window is real: a hit during it does nothing
  const tBefore=R.pools.turret; hitSubBoss(50,b.x,b.y); const tDuring=R.pools.turret;
  R.trans=0; hitSubBoss(9999,b.x,b.y); states.push(R.state);
  // hull phase rams
  R.trans=0; R.attack='ram'; R.at=0; R.beat=-1;
  let maxY=b.y; const t0=performance.now();
  while(performance.now()-t0<2600){ await fr(); maxY=Math.max(maxY,b.y); }
  R.trans=0; hitSubBoss(99999,b.x,b.y); await fr();
  return {hp0:hp0, turret0:turret0, turretAfter:turretAfter, hpAfterArmour:hpAfterArmour, left0:left0, leftAfter:leftAfter,
          states:states, gunsCleared:gunsCleared, hpAfterGuns:hpAfterGuns, tBefore:tBefore, tDuring:tDuring,
          ramY:Math.round(maxY), VH:VH, dead:!!b.dead, hpEnd:b.hp};
}
"""

SNAP = r"""() => { const c=document.querySelector('#screen'); return c ? c.toDataURL('image/png') : null; }"""


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--out', default='/tmp/rzb'); a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    from playwright.sync_api import sync_playwright
    port, stop = shoot.serve(shoot.GAME); errs = []; fails = []; n_ok = [0]
    def ok(c, m):
        if c: n_ok[0] += 1; print('  ok  ', m)
        else: fails.append(m); print('  FAIL', m)
    def snap(pg, name):
        d = pg.evaluate(SNAP)
        if d: open(os.path.join(a.out, name), 'wb').write(base64.b64decode(d.split(',', 1)[1]))

    with sync_playwright() as p:
        b = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
        pg = b.new_page(viewport={'width': 1100, 'height': 1000})
        pg.on('pageerror', lambda e: errs.append('pageerror: ' + str(e)[:220]))
        pg.on('console', lambda m: errs.append('console.error: ' + m.text[:200]) if m.type == 'error' else None)
        pg.goto(f'http://127.0.0.1:{port}/index.html?bossmode=1', wait_until='load', timeout=60000)
        pg.wait_for_function("() => window.BOSSMODE && window.BOSSMODE.ready", timeout=90000)
        st = pg.evaluate(SETUP)
        print('setup', st)
        ok(st['kind'] == 'razorback', "stage 1's miniboss is the RAZORBACK (SUBBOSS[1].kind = %s)" % st['kind'])
        ok(st['rzb'] and st['name'] == 'RAZORBACK', 'the debug host spawns it as a live tank (%s via role %s)' % (st['name'], st['role']))
        ok(st['ready'] == st['of'] and st['of'] == 25, 'all %d of its art cells resolve and decode' % st['of'])

        t = pg.evaluate(ARRIVE_AND_TURN)
        print('turn', {k: v for k, v in t.items() if k != 'parts'})
        snap(pg, '01_guns_phase.png')
        ok(t['arrived'] == 'guns', 'it rolls in and exposes its GUNS first (%s)' % t['arrived'])
        need = ['rzb_turret', 'rzb_machinegun', 'rzb_missile_pod', 'rzb_tread', 'rzb_rotor']
        ok(all(k in t['parts'] for k in need), 'it draws its own rig - turret, guns, pods, treads, rotors: %s'
           % sorted(k for k in t['parts'] if not k.startswith('rzb_hull_')))
        ok(t['hullSweep'] > 0.5 and len(t['hulls']) >= 2,
           'it TWISTS AND TURNS - the hull swept %.2f rad through %d compass frames %s'
           % (t['hullSweep'], len(t['hulls']), t['hulls']))
        ok(t['turretSweep'] > 0.3, 'and the turret tracks independently (%.2f rad)' % t['turretSweep'])

        s = pg.evaluate(SONIC)
        print('sonic', s)
        snap(pg, '02_sonic.png')
        ok(s['charged'] and s['rounds'] >= 5 and s['waves'] >= 1,
           'SONIC HAMMER charges, then fires %d sonic rounds and %d pressure wave(s)' % (s['rounds'], s['waves']))
        ok(s['boom'] >= 1, "with Cole's sonic release (%d plays requested)" % s['boom'])

        mm = pg.evaluate(MISSILES)
        print('missiles', mm)
        snap(pg, '03_missiles.png')
        ok(mm['retinas'] == 1, 'RAZOR RACK puts ONE retina on the player (%d)' % mm['retinas'])
        ok(mm['total'] >= 8 and mm['maxPerFrame'] == 1,
           'and its %d missiles leave ONE AT A TIME - never more than %d in a frame, never three at once'
           % (mm['total'], mm['maxPerFrame']))
        ok(mm['distinctHeadings'] >= 5, 'down a SPREAD of %d distinct headings' % mm['distinctHeadings'])
        ok(mm['lockBound'] == mm['total'], 'every one of them is bound to the retina lock (%d/%d)' % (mm['lockBound'], mm['total']))

        pr = pg.evaluate(PARTS)
        print('parts', pr)
        ok(pr['turretAfter'] == pr['turret0'] and pr['hpAfterArmour'] == pr['hp0'],
           'a real player round on the TURRET while the guns live does nothing (%s -> %s)' % (pr['turret0'], pr['turretAfter']))
        ok(pr['leftAfter'] < pr['left0'], 'and one on the LEFT GUN takes its pool %s -> %s' % (pr['left0'], pr['leftAfter']))
        ok(pr['states'] == ['guns', 'turret', 'hull'], 'guns -> turret -> hull, in order: %s' % pr['states'])
        ok(pr['tDuring'] == pr['tBefore'], 'the transition window after a break is real - a hit during it is shrugged off')
        ok(pr['ramY'] > pr['VH'] * 0.55, 'the exposed hull RAMS down the screen (reached y %s of %s)' % (pr['ramY'], pr['VH']))
        ok(pr['dead'] and pr['hpEnd'] <= 0, 'and destroying the hull kills it')
        b.close()
    stop()
    print('\n%d ok / %d fail' % (n_ok[0], len(fails)))
    for f in fails: print('  FAIL', f)
    if errs:
        print('page errors (%d):' % len(errs))
        for e in errs[:8]: print('   ', e)
    sys.exit(1 if fails or errs else 0)


if __name__ == '__main__':
    main()
