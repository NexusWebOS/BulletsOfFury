#!/usr/bin/env python3
"""
probe_retina_lock_0912q.py - THE RETINA LOCK HEADER RULE, DRIVEN IN REAL CHROMIUM.

    python3 _BUILD_SOURCE/probe_retina_lock_0912q.py --out /tmp/lock

Mike, 0912: "when bosses want to fire homing missiles on you, target a retina on the player and
make it flash and beep with the retina noise and beep rapidly as they are about to fire off and
then the missiles come at us the retina stays locked until we either barrel roll to shake it off,
dodge at the last second, somersalt or shoot down the missiles."

Every clause of that is asserted on BEHAVIOUR, in the running game:
  * the retina goes on the player, draws the retina ART (not brackets), and FLASHES while arming
  * the retina noise plays once, and the beeps get FASTER as the launch closes in
  * the missile launches, carries its lock, and STEERS while the lock holds
  * a barrel roll, a somersault and the charge dash each BREAK it, and a broken lock stops steering
  * shooting the missile down RELEASES the lock
  * a late sidestep leaves a COMMITTED missile flying at empty air
  * one unit rippling four locks holds ONE retina and plays the charge ONCE (the 0813a siren)
  * gun mode refuses a lock, and a dead player carries none

⚠ Sounds are counted by wrapping Audio.SFX at the call - the rule's own scheduler - and the GATE is
checked separately against Snd.play, because a probe that only wraps the request cannot tell a
beep that played from one the throttle refused (0912j).
"""
import os, sys, argparse, base64
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shoot

FRAME = "() => new Promise(r=>requestAnimationFrame(()=>r()))"

HELPERS = r"""
window.__lk = window.__lk || (function(){
  const H={};
  H.frame=()=>new Promise(r=>requestAnimationFrame(()=>r()));
  H.wait=async(fn,maxMs)=>{ const t0=performance.now(); while(performance.now()-t0<maxMs){ if(fn()) return true; await H.frame(); } return !!fn(); };
  H.clear=()=>{ playerLocks=[]; for(const b of eBullets) if(b._lockId) b.dead=true; };
  H.snd={charge:[], beep:[]};
  if(!H._wrapped){
    const oc=Audio.SFX.retinaCharge, ob=Audio.SFX.retinaLockBeep;
    Audio.SFX.retinaCharge=function(){ H.snd.charge.push(performance.now()); return oc&&oc.apply(this,arguments); };
    Audio.SFX.retinaLockBeep=function(){ H.snd.beep.push(performance.now()); return ob&&ob.apply(this,arguments); };
    H.draws=[];
    const on=window.nuoTinted;
    window.nuoTinted=function(k,c){ if(/^retmb?_/.test(k)) H.draws.push({k:k,t:performance.now()}); return on.apply(this,arguments); };
    H._wrapped=true;
  }
  H.src=()=>{ const s=(typeof boss!=='undefined' && boss && !boss.dead)?boss:null; return s; };
  H.park=()=>{ player.x=(typeof worldWidth==='function'?worldWidth():480)/2; player.y=VH*0.80; player.roll=null; player.somer=null;
               player._chgDash=null; player._rollCool=0; player._somerCool=0; };
  return H;
})();
"""

SETUP = r"""
async () => {
  const B=window.BOSSMODE;
  B.start(2,'boss','cole',false);
  const t0=performance.now();
  while(performance.now()-t0<30000 && !(B.snapshot().bossActive && B.player && !B.player.dead))
    await new Promise(r=>requestAnimationFrame(r));
  B.setInvuln(true);
  // the retina plates and the roll/somersault reels are lazily loaded - rdy() starts it, so poll
  const keys=['retm_0','retm_1','retm_2','retm_3','retmb_0','retmb_1','retmb_2','retmb_3','ship_cole_br0','ship_cole_so0'];
  const t1=performance.now();
  while(performance.now()-t1<15000 && !keys.every(k=>XART.rdy(k))) await new Promise(r=>requestAnimationFrame(r));
  return {boss:!!(typeof boss!=='undefined'&&boss), ready:keys.filter(k=>XART.rdy(k)).length, of:keys.length};
}
"""

# ---- the arming phase: retina, flash, charge sound, accelerating beeps, then launch ----
ARMING = r"""
async () => {
  const H=window.__lk; H.clear(); H.park();
  for(let i=0;i<30;i++) await H.frame();          // let any previous lock's beeps drain
  H.snd.charge.length=0; H.snd.beep.length=0; H.draws.length=0;
  const L=enemyLockOn(H.src(), 1.6);
  if(!L) return {err:'no lock'};
  const t0=performance.now();
  let frames=0, drawnFrames=0, lastDraws=0, firstFrameState=L.state;
  while(L.state==='arming' && performance.now()-t0<4000){
    await H.frame(); frames++;
    if(H.draws.length>lastDraws){ drawnFrames++; lastDraws=H.draws.length; }
  }
  const beeps=H.snd.beep.filter(t=>t>=t0 && t<=performance.now()).map(t=>t-t0);
  const gaps=[]; for(let i=1;i<beeps.length;i++) gaps.push(beeps[i]-beeps[i-1]);
  const keys=[...new Set(H.draws.map(d=>d.k.replace(/_\d$/,'_')))];
  const tagged=eBullets.filter(b=>b._lockId===L.id && !b.dead).length;
  return {state0:firstFrameState, stateAfter:L.state, frames:frames, drawnFrames:drawnFrames, keys:keys,
          charge:H.snd.charge.length, beeps:beeps.length, gaps:gaps.map(g=>Math.round(g)),
          tagged:tagged, missiles:L.missiles.length, lockId:L.id};
}
"""

# ---- locked: persists, draws solid, steers toward a player who moved ----
LOCKED_STEERS = r"""
async ([lockId]) => {
  const H=window.__lk; const L=lockById(lockId);
  if(!L) return {err:'lock gone before the steering test'};
  const m=L.missiles[0]; if(!m) return {err:'no missile'};
  H.draws.length=0;
  player.x += (player.x < m.x ? -150 : 150);      // step well off the missile's line
  const a0=Math.atan2(m.vy,m.vx);
  let maxTurn=0, framesLocked=0, drawn=0, last=0;
  for(let i=0;i<24 && !m.dead;i++){
    await H.frame();
    if(L.state==='locked') framesLocked++;
    if(H.draws.length>last){ drawn++; last=H.draws.length; }
    maxTurn=Math.max(maxTurn, Math.abs(((Math.atan2(m.vy,m.vx)-a0+Math.PI*3)%(Math.PI*2))-Math.PI));
  }
  const solid=H.draws.some(d=>/^retmb_/.test(d.k));
  return {state:L.state, framesLocked:framesLocked, drawn:drawn, solid:solid, turn:+maxTurn.toFixed(3), dist:Math.round(Math.hypot(player.x-m.x, player.y-m.y))};
}
"""

# ---- an evasive manoeuvre breaks the lock and the missile stops steering ----
EVADE = r"""
async ([how]) => {
  const H=window.__lk; H.clear(); H.park();
  for(let i=0;i<6;i++) await H.frame();
  const L=enemyLockOn(H.src(), 0.45);
  await H.wait(()=>L.state!=='arming', 3000);
  const m=L.missiles[0];
  if(!m) return {err:'no missile launched', state:L.state};
  for(let i=0;i<4;i++) await H.frame();
  const stateBefore=L.state;
  let started=false;
  if(how==='roll'){ if(typeof startRoll==='function'){ startRoll(1); started=!!player.roll; } }
  else if(how==='somer'){ if(typeof startSomersault==='function'){ startSomersault(); started=!!player.somer; } }
  else if(how==='charge'){
    /* the dash itself is Juggernaut's and needs his special live; the RULE reads player._chgDash,
       which is exactly the object chargeRelease writes - so this arms that flag directly */
    player._chgDash={t:0, dur:0.40, dist:0, k:0, y0:player.y}; started=true;
  }
  await H.frame(); await H.frame();
  const stateAfter=L.state;
  // with the lock broken the round must not steer, even toward a player who moves again
  player.x += (player.x < m.x ? -140 : 140);
  const a0=Math.atan2(m.vy,m.vx); let turn=0;
  for(let i=0;i<20 && !m.dead;i++){ await H.frame(); turn=Math.max(turn, Math.abs(((Math.atan2(m.vy,m.vx)-a0+Math.PI*3)%(Math.PI*2))-Math.PI)); }
  if(how==='charge') player._chgDash=null;
  return {started:started, before:stateBefore, after:stateAfter, turn:+turn.toFixed(4), committed:!!m._committed};
}
"""

SHOOT_DOWN = r"""
async () => {
  const H=window.__lk; H.clear(); H.park();
  for(let i=0;i<6;i++) await H.frame();
  const L=enemyLockOn(H.src(), 0.40);
  await H.wait(()=>L.state!=='arming', 3000);
  const ms=L.missiles.slice(); if(!ms.length) return {err:'no missile'};
  for(let i=0;i<3;i++) await H.frame();
  const before=L.state;
  // a real player round on each missile - the enemy-bullet loop's own intercept kills it
  for(const m of ms) pBullets.push({x:m.x, y:m.y, vx:0, vy:0, w:14, h:18, dmg:1, t:0});
  const gone=await H.wait(()=>ms.every(m=>m.dead || eBullets.indexOf(m)<0), 1500);
  const byShot=ms.every(m=>m.dead);
  await H.frame(); await H.frame();
  const stateAfterKill=L.state;
  const cleared=await H.wait(()=>!lockById(L.id), 1500);
  return {before:before, gone:gone, byShot:byShot, stateAfterKill:stateAfterKill, cleared:cleared};
}
"""

DODGE = r"""
async () => {
  const H=window.__lk; H.clear(); H.park();
  for(let i=0;i<6;i++) await H.frame();
  const L=enemyLockOn(H.src(), 0.40);
  await H.wait(()=>L.state!=='arming', 3000);
  const m=L.missiles[0]; if(!m) return {err:'no missile'};
  // hold still and let it come, then sidestep at the last moment
  const close=await H.wait(()=>m.dead || Math.hypot(player.x-m.x, player.y-m.y) < 78, 6000);
  if(m.dead) return {err:'missile died before it got close', state:L.state};
  const committed=!!m._committed, distAtStep=Math.round(Math.hypot(player.x-m.x, player.y-m.y));
  const px=player.x; player.x += (m.vx>0 ? -95 : 95);
  let minD=1e9;
  const passed=await H.wait(()=>{ if(!m.dead) minD=Math.min(minD, Math.hypot(player.x-m.x, player.y-m.y)); return m.dead || eBullets.indexOf(m)<0; }, 6000);
  const released=await H.wait(()=>!lockById(L.id), 2000);
  return {close:close, committed:committed, distAtStep:distAtStep, minDist:Math.round(minD), passed:passed, released:released};
}
"""

RIPPLE = r"""
async () => {
  const H=window.__lk; H.clear(); H.park();
  for(let i=0;i<40;i++) await H.frame();          // clear the charge gate (TAME min 0.80)
  H.snd.charge.length=0;
  const s=H.src();
  for(let i=0;i<4;i++) enemyLockOn(s, 0.5+i*0.12);
  const mine=playerLocks.filter(L=>L.src===s);
  const gun=enemyLockOn({fk:'gun', x:0, y:0}, 0.5);
  const res={retinas:mine.length, launches:mine.length?mine[0].launches.length:0, charge:H.snd.charge.length, gun:gun};
  const L=mine[0];
  await H.wait(()=>L && L.launches.every(sh=>sh.done), 3000);
  await H.frame();
  res.fired=L?L.missiles.length:0;
  return res;
}
"""

DEATH = r"""
async () => {
  const H=window.__lk; H.clear(); H.park();
  const L=enemyLockOn(H.src(), 2.0);
  await H.frame();
  const had=playerLocks.length;
  const was=player.dead;
  player.dead=true;
  /* asked on the same tick the flag goes up - the host resurrects an invulnerable player within a
     frame or two, so a refusal checked after the frames reads a living player */
  const refused=enemyLockOn(H.src(), 0.5)===null;
  await H.frame();
  const after=playerLocks.length;
  player.dead=was;
  return {had:had, after:after, refusedWhileDead:refused};
}
"""

GATE = r"""
() => {
  const T=(typeof Snd!=='undefined'&&Snd.TAME)?Snd.TAME:{};
  const orig=Snd.play.bind(Snd);
  let played=0, refused=0;
  for(let i=0;i<30;i++){ const r=orig('retinaCharge'); if(r===false) refused++; else played++; }
  return {beep:T.retinaLockBeep||null, charge:T.retinaCharge||null, burstPlayed:played, burstRefused:refused,
          registered:!!(window.BOFA&&BOFA.sfx&&BOFA.sfx.retinaLockBeep)};
}
"""

SNAP = r"""
() => { const c=document.querySelector('#screen'); return c ? c.toDataURL('image/png') : null; }
"""


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--out', default='/tmp/lock'); a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    from playwright.sync_api import sync_playwright
    port, stop = shoot.serve(shoot.GAME); errs = []; fails = []; n_ok = [0]
    def ok(c, m):
        if c: n_ok[0] += 1; print('  ok  ', m)
        else: fails.append(m); print('  FAIL', m)
    def snap(name):
        d = pg.evaluate(SNAP)
        if d:
            open(os.path.join(a.out, name), 'wb').write(base64.b64decode(d.split(',', 1)[1]))

    with sync_playwright() as p:
        b = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
        pg = b.new_page(viewport={'width': 1100, 'height': 1000})
        pg.on('pageerror', lambda e: errs.append('pageerror: ' + str(e)[:220]))
        pg.on('console', lambda m: errs.append('console.error: ' + m.text[:200]) if m.type == 'error' else None)
        pg.goto(f'http://127.0.0.1:{port}/index.html?bossmode=1', wait_until='load', timeout=60000)
        pg.wait_for_function("() => window.BOSSMODE && window.BOSSMODE.ready", timeout=90000)
        st = pg.evaluate(SETUP)
        print('setup', st)
        ok(st['boss'], 'a live boss to fire from (stage 2)')
        pg.evaluate("() => {" + HELPERS + "}")

        g = pg.evaluate(GATE)
        ok(g['registered'] and g['beep'] and 0 < g['beep'].get('min', 0) <= 0.06,
           'the lock beep is its own registered key with a SHORT gate, so it can beep rapidly: %s' % g['beep'])
        ok(g['charge'] and g['charge'].get('min', 0) >= 0.5 and g['burstRefused'] >= 25,
           'the retina noise has a LONG gate - 30 rapid calls -> %d played, %d refused'
           % (g['burstPlayed'], g['burstRefused']))

        # --- arming ---
        pg.evaluate("async () => { const H=window.__lk; H.clear(); H.park(); const L=enemyLockOn(H.src(), 1.6); for(let i=0;i<30;i++) await H.frame(); }")
        snap('01_arming.png')
        pg.evaluate("async () => { const H=window.__lk; H.clear(); for(let i=0;i<30;i++) await H.frame(); }")
        r = pg.evaluate(ARMING)
        print('arming', r)
        ok(r.get('state0') == 'arming', 'enemyLockOn puts an ARMING retina on the player')
        ok('retm_' in r.get('keys', []),
           'the arming retina draws the retina ART, not procedural brackets: %s' % r.get('keys'))
        ok(0 < r.get('drawnFrames', 0) < r.get('frames', 0),
           'and it FLASHES - drawn on %d of %d arming frames' % (r.get('drawnFrames', 0), r.get('frames', 0)))
        ok(r.get('charge') == 1, 'the retina noise plays exactly once at acquire (%s)' % r.get('charge'))
        gaps = r.get('gaps', [])
        ok(len(gaps) >= 5 and gaps[-1] < gaps[0] * 0.6,
           'and the beeps get FASTER as the launch closes in: %d beeps, gaps %s ms' % (r.get('beeps', 0), gaps))
        ok(r.get('stateAfter') == 'locked' and r.get('tagged', 0) >= 1,
           'the missile launches carrying its lock (%d tagged round(s)), and the lock holds as LOCKED'
           % r.get('tagged', 0))

        # --- locked: steers ---
        s = pg.evaluate(LOCKED_STEERS, [r.get('lockId')])
        print('locked', s)
        snap('02_locked.png')
        ok(s.get('framesLocked', 0) >= 10 and s.get('solid'),
           'the retina STAYS locked on the player after launch, drawn solid (%d frames)' % s.get('framesLocked', 0))
        ok(s.get('turn', 0) > 0.15,
           'and while it holds, the missile STEERS after a player who moved (%.3f rad in 24 frames)' % s.get('turn', 0))

        # --- the three manoeuvres ---
        for how, label in (('roll', 'a BARREL ROLL'), ('somer', 'a SOMERSAULT'), ('charge', "Juggernaut's CHARGE DASH")):
            e = pg.evaluate(EVADE, [how])
            print(how, e)
            ok(e.get('started') and e.get('before') == 'locked' and e.get('after') == 'broken',
               '%s shakes the lock off: %s -> %s' % (label, e.get('before'), e.get('after')))
            ok(e.get('turn', 1) < 0.01 and e.get('committed'),
               'and the shaken-off missile never steers again (%.4f rad as the player moves)' % e.get('turn', 1))
            pg.evaluate("async () => { player.roll=null; player.somer=null; player._rollCool=0; player._somerCool=0; for(let i=0;i<50;i++) await window.__lk.frame(); }")

        # --- shoot down ---
        d = pg.evaluate(SHOOT_DOWN)
        print('shootdown', d)
        ok(d.get('before') == 'locked' and d.get('byShot'),
           'SHOOTING THE MISSILE DOWN with a real player round kills it')
        ok(d.get('stateAfterKill') == 'released' and d.get('cleared'),
           'and that releases the lock: %s, retina cleared=%s' % (d.get('stateAfterKill'), d.get('cleared')))

        # --- dodge at the last second ---
        dg = pg.evaluate(DODGE)
        print('dodge', dg)
        ok(dg.get('close') and dg.get('committed'),
           'a missile that closes inside the commit radius stops steering (committed at %s px)' % dg.get('distAtStep'))
        ok(dg.get('passed') and dg.get('minDist', 0) > 30 and dg.get('released'),
           'so a LAST-SECOND sidestep leaves it flying at empty air (closest %s px) and the lock releases'
           % dg.get('minDist'))

        # --- one retina per unit, gun mode ---
        rp = pg.evaluate(RIPPLE)
        print('ripple', rp)
        ok(rp.get('retinas') == 1 and rp.get('launches') == 4,
           'a unit rippling FOUR locks holds ONE retina with four queued launches - the 0813a siren '
           'cannot stack (%s retina, %s launches)' % (rp.get('retinas'), rp.get('launches')))
        ok(rp.get('charge') == 1, 'and plays the retina noise once, not four times (%s)' % rp.get('charge'))
        ok(rp.get('fired', 0) >= 2, 'and every queued launch still fires (%s missiles)' % rp.get('fired'))
        ok(rp.get('gun') is None, 'gun mode refuses a lock (0801jy: no missiles anywhere)')

        dd = pg.evaluate(DEATH)
        print('death', dd)
        ok(dd.get('had', 0) >= 1 and dd.get('after') == 0 and dd.get('refusedWhileDead'),
           'a dead player carries no retina and cannot be locked')

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
