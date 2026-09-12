#!/usr/bin/env python3
"""
probe_furnace_0912t.py - THE FURNACE TYRANT, STAGE 2 BOSS, IN REAL CHROMIUM.

    python3 _BUILD_SOURCE/probe_furnace_0912t.py --out /tmp/furnace

Mike, 0912: "the ember boss should be the new stage 2 boss, replacing our old one but use the old
one's fire shield instead of this ones. its pretty straight forward although the laser targetting
could be better" ... "faster projectiles".

  * stage 2's boss is the Furnace Tyrant, assembled by chains, invulnerable while it builds itself
  * it wears the MAGMA WARD's fire shield - which takes the rounds first, and breaks
  * arms -> core -> head, each part hurt only when exposed; the shield rearms once for the core
  * the cannon fires, the flamethrower spins 900 degrees, the core rings and lances
  * THE EYE LASERS: when the beam opens, the aim is ON a player who reversed during the charge (the
    pack's 0.23s guess missed that player every time), and a committed dodge during the burn escapes
  * the head is killed and the boss dies
The draw is identified by recording the KEYS XART.get is asked for.
"""
import os, sys, argparse, base64
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shoot

SETUP = r"""
async () => {
  const B=window.BOSSMODE, fr=()=>new Promise(r=>requestAnimationFrame(()=>r()));
  B.start(2,'boss','cole',false);
  const t0=performance.now();
  while(performance.now()-t0<40000 && !(typeof boss!=='undefined' && boss && boss._furnace && B.player && !B.player.dead)) await fr();
  B.setInvuln(true);
  const keys=Object.keys(BOFX.img).filter(k=>k.indexOf('fzt_')===0);
  const t1=performance.now();
  while(performance.now()-t1<15000 && !keys.every(k=>XART.rdy(k))) await fr();
  window.__fz={keys:[], snd:{}, hits:0};
  const og=XART.get.bind(XART);
  XART.get=function(k){ if(typeof k==='string' && k.indexOf('fzt_')===0) window.__fz.keys.push(k); return og(k); };
  for(const n of ['furnaceChainLaunch','furnaceArmLock','furnacePowerSurge','enemyBossCannon','furnaceHeavyLaser','bossfireInfernoreaver','furnaceFlameIgnite']){
    const f=Audio.SFX[n]; window.__fz.snd[n]=0;
    Audio.SFX[n]=function(){ window.__fz.snd[n]++; return f&&f.apply(this,arguments); };
  }
  const ph=window.playerHit; window.playerHit=function(){ window.__fz.hits++; return ph.apply(this,arguments); };
  return {boss:STAGES[1].boss, name:boss?boss.name:null, furnace:!!(boss&&boss._furnace), ready:keys.filter(k=>XART.rdy(k)).length,
          of:keys.length, shield:!!(boss&&boss._mwBarrier&&boss._mwBarrier.active), phase:boss&&boss._fz?boss._fz.phase:null};
}
"""

INTRO = r"""
async () => {
  const fr=()=>new Promise(r=>requestAnimationFrame(()=>r()));
  const b=boss, F=b._fz;
  let hittable=false, shotDuring=false, snapAt=null;
  const t0=performance.now();
  while(performance.now()-t0<16000 && F.phase==='intro'){
    await fr();
    if(F.phase==='intro' && bossHitTest(b.x,b.y)) hittable=true;   // sample only frames that are still the assembly
    if(F.pt>4.4 && !snapAt){ snapAt=F.pt; window.__introSnap=document.querySelector('#screen').toDataURL('image/png'); }
  }
  const keys=[...new Set(window.__fz.keys)];
  return {phase:F.phase, hittable:hittable, yaw:keys.filter(k=>/torso_yaw/.test(k)).length, chain:keys.some(k=>/chain_/.test(k)),
          head:keys.some(k=>/head_/.test(k)), snd:Object.assign({},window.__fz.snd), y:Math.round(b.y), VH:VH};
}
"""

SHIELD_AND_ARMS = r"""
async () => {
  const fr=()=>new Promise(r=>requestAnimationFrame(()=>r()));
  const b=boss, F=b._fz, H=b._mwBarrier;
  F.trans=0;
  const shield0=H.hp, pools0=Object.assign({},F.pools), hp0=b.hp;
  // a real round on the hull while the shield is up
  _dmgBullet=null; _lastHitX=b.x; _lastHitY=b.y; hitBoss(12);
  const shieldAfter=H.hp, poolsAfterShield=Object.assign({},F.pools);
  // break the shield outright
  magmaWardBarrierDamage(b, 99999, b.x, b.y);
  const shieldUp=H.active;
  b._mwStun=0;
  // the body cannot be hurt while the arms live
  _lastHitX=b.x; _lastHitY=b.y; hitBoss(12);
  const bodyAfter=F.pools.body;
  // the left arm can
  const box=furnaceBoxes(b).find(q=>q.key==='left');
  _lastHitX=box.x; _lastHitY=box.y; hitBoss(12);
  const leftAfter=F.pools.left;
  return {shield0:shield0, shieldAfter:shieldAfter, armsUntouchedByShieldHit:poolsAfterShield.left===pools0.left && poolsAfterShield.body===pools0.body,
          shieldUp:shieldUp, body0:pools0.body, bodyAfter:bodyAfter, left0:pools0.left, leftAfter:leftAfter};
}
"""

ARMS_WEAPONS = r"""
async () => {
  const fr=()=>new Promise(r=>requestAnimationFrame(()=>r()));
  const b=boss, F=b._fz; b._mwStun=0; F.trans=0;
  // CANNON
  for(const q of eBullets) if(q._fzt) q.dead=true;
  F.idx=0; F.attack='cannon'; F.at=0; F.shotBeat=-1;
  const seen=new Set(); let spd=0;
  let t0=performance.now();
  while(performance.now()-t0<4500){ await fr(); b._mwStun=0;
    for(const q of eBullets) if(q.kind==='fztFireball' && !seen.has(q)){ seen.add(q); spd=Math.max(spd,Math.hypot(q.vx,q.vy)); } }
  const cannonShots=seen.size, cannonSnd=window.__fz.snd.enemyBossCannon;
  // SPIN 900 with the flamethrower
  F.attack='spin900'; F.at=0; F.startX=b.x; F.endX=b.x+60; F.dir=1;
  let aMin=1e9,aMax=-1e9, flame=0;
  t0=performance.now();
  while(performance.now()-t0<6200){ await fr(); b._mwStun=0; if(F.attack!=='spin900') break;
    aMin=Math.min(aMin,F.a); aMax=Math.max(aMax,F.a); if(F.beams.some(q=>q.kind==='flame')) flame++; }
  window.__armsSnap=document.querySelector('#screen').toDataURL('image/png');
  return {cannonShots:cannonShots, speed:+spd.toFixed(2), cannonSnd:cannonSnd, spin:+(aMax-aMin).toFixed(2), flameFrames:flame};
}
"""

CORE = r"""
async () => {
  const fr=()=>new Promise(r=>requestAnimationFrame(()=>r()));
  const b=boss, F=b._fz;
  const H=b._mwBarrier;
  for(const k of ['left','right']){ const box=furnaceBoxes(b).find(q=>q.key===k); if(box) furnaceHit(b,99999,box.x,box.y); }
  const phase=F.phase, rearmed=H.active, rearms=H.rearms, shieldRatio=+(H.hp/H.maxhp).toFixed(2);
  magmaWardBarrierDamage(b,99999,b.x,b.y); b._mwStun=0; F.trans=0;
  // RING
  for(const q of eBullets) if(q._fzt) q.dead=true;
  F.attack='ring'; F.at=0; F.burstBeat=-1;
  let peak=0; let t0=performance.now();
  while(performance.now()-t0<2600){ await fr(); b._mwStun=0; peak=Math.max(peak, eBullets.filter(q=>q.kind==='fztFireball').length); }
  // LANCE: the player stands off to one side; the lance creeps toward them while it burns
  F.attack='coreLaser'; F.at=0; F.burstBeat=-1;
  const W=worldWidth(); b.x=W*0.40; player.x=W*0.62;
  let widest=0, xAtFire=null, xEnd=null;
  t0=performance.now();
  while(performance.now()-t0<5400 && F.attack==='coreLaser'){ await fr(); b._mwStun=0;
    const beam=F.beams.find(q=>q.kind==='core'); if(beam){ widest=Math.max(widest,beam.width); if(xAtFire==null) xAtFire=b.x; xEnd=b.x; }
    if(F.at>2.6 && !window.__coreSnap) window.__coreSnap=document.querySelector('#screen').toDataURL('image/png'); }
  return {phase:phase, rearmed:rearmed, rearms:rearms, shieldRatio:shieldRatio, ringPeak:peak, widest:Math.round(widest),
          creep:(xAtFire!=null&&xEnd!=null)?Math.round(xEnd-xAtFire):null, lanceSnd:window.__fz.snd.furnaceHeavyLaser};
}
"""

HEAD = r"""
async () => {
  const fr=()=>new Promise(r=>requestAnimationFrame(()=>r()));
  const b=boss, F=b._fz, H=b._mwBarrier;
  if(H && H.active) magmaWardBarrierDamage(b,99999,b.x,b.y);
  b._mwStun=0;
  furnaceHit(b,99999,b.x,b.y);
  const phase=F.phase, shieldOff=!(H&&H.active);
  F.trans=0; F.attack='eyeBurst'; F.at=0; F.idx=0; F.shotBeat=-1;
  const W=worldWidth(); player.y=VH*0.80;
  // ---- REVERSAL: sweep right through the charge, reverse late, stop; measure the aim when the beam opens
  let errAtOpen=null, cyc0=null;
  const until=performance.now()+4000;
  while(performance.now()<until){
    await fr(); b._mwStun=0;
    const cyc=F.at%1.25;
    if(cyc<0.45) player.x=Math.min(W-30, player.x+3.2);
    else if(cyc<0.65) player.x=Math.max(30, player.x-4.0);
    if(cyc>=0.72 && cyc<0.80 && errAtOpen==null){
      const eye={x:b.x+19*FZT_S, y:b.y}, want=fztAim(eye,player);
      errAtOpen=Math.abs(fztWrap(F.eye[1]-want));
    }
    if(errAtOpen!=null) break;
  }
  // ---- COMMITTED DODGE: wait for the next beam, then leave hard and count the hits after leaving
  while(F.at%1.25 >= 0.05) await fr();
  while(F.at%1.25 < 0.76){ await fr(); b._mwStun=0; }
  player.x = (player.x < W/2) ? player.x+170 : player.x-170;
  const h0=window.__fz.hits;
  for(let i=0;i<20;i++){ await fr(); b._mwStun=0; if(F.at%1.25 < 0.72) break; }
  const hitsAfterDodge=window.__fz.hits-h0;
  // ---- STANDING STILL is punished
  while(F.at%1.25 >= 0.05) await fr();
  const h1=window.__fz.hits; let snapped=false;
  const stillUntil=performance.now()+2600;
  while(performance.now()<stillUntil){ await fr(); b._mwStun=0; if(!snapped && F.at%1.25>0.8){ snapped=true; window.__headSnap=document.querySelector('#screen').toDataURL('image/png'); } }
  const hitsStill=window.__fz.hits-h1;
  // ---- kill it
  /* through hitBoss, the real path - furnaceHit alone moves the part pool but never the boss's hp,
     so it cannot reach bossDie */
  _dmgBullet=null; _lastHitX=b.x; _lastHitY=b.y; F.trans=0; hitBoss(99999);
  for(let i=0;i<4;i++) await fr();
  return {phase:phase, shieldOff:shieldOff, errAtOpen:errAtOpen!=null?+errAtOpen.toFixed(3):null,
          hitsAfterDodge:hitsAfterDodge, hitsStill:hitsStill, dead:!!b.dead, hp:b.hp};
}
"""


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--out', default='/tmp/furnace'); a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    from playwright.sync_api import sync_playwright
    port, stop = shoot.serve(shoot.GAME); errs = []; fails = []; n_ok = [0]
    def ok(c, m):
        if c: n_ok[0] += 1; print('  ok  ', m)
        else: fails.append(m); print('  FAIL', m)
    def save(pg, var, name):
        d = pg.evaluate("() => window.%s || null" % var)
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
        ok(st['boss'] == 'infernoreaver' and st['furnace'] and st['name'] == 'FURNACE TYRANT',
           "stage 2's boss is the FURNACE TYRANT (%s)" % st['name'])
        ok(st['ready'] == st['of'] == 45, 'all %d of its plates resolve and decode' % st['of'])
        ok(st['shield'], "it wears the MAGMA WARD's fire shield from the start")

        it = pg.evaluate(INTRO)
        print('intro', it)
        save(pg, '__introSnap', '01_assembly.png')
        ok(it['phase'] == 'arms', 'the chain assembly completes and the fight opens on the ARMS (%s)' % it['phase'])
        ok(not it['hittable'], 'nothing can hit it while it builds itself')
        ok(it['yaw'] >= 3 and it['chain'] and it['head'], 'it draws the torso turntable, the chains and the head (%d yaw frames)' % it['yaw'])
        ok(it['snd']['furnaceChainLaunch'] >= 3 and it['snd']['furnaceArmLock'] >= 3 and it['snd']['furnacePowerSurge'] >= 1,
           'with the pack\'s chain, latch and power-surge cues: %s' % it['snd'])
        ok(0 < it['y'] < it['VH'] * 0.5, 'and it settles in the top half of the screen, never below the player (y %s)' % it['y'])

        sa = pg.evaluate(SHIELD_AND_ARMS)
        print('shield/arms', sa)
        ok(sa['shieldAfter'] < sa['shield0'] and sa['armsUntouchedByShieldHit'], 'the fire shield takes the round first (%s -> %s), the hull takes nothing' % (sa['shield0'], sa['shieldAfter']))
        ok(not sa['shieldUp'], 'and the shield breaks')
        ok(sa['bodyAfter'] == sa['body0'], 'the body cannot be hurt while its arms live')
        ok(sa['leftAfter'] < sa['left0'], 'an arm can (%s -> %s)' % (sa['left0'], sa['leftAfter']))

        aw = pg.evaluate(ARMS_WEAPONS)
        print('arms weapons', aw)
        save(pg, '__armsSnap', '02_arms.png')
        ok(aw['cannonShots'] >= 2 and aw['cannonSnd'] >= 1, 'the cannon charges and fires (%d rounds)' % aw['cannonShots'])
        ok(aw['speed'] >= 4.0, 'at the faster projectile speed Mike asked for (%.2f px/frame; the pack\'s speed here would be 3.09)' % aw['speed'])
        ok(aw['spin'] >= 15.0 and aw['flameFrames'] > 60, 'the flamethrower spins its 900 degrees (%.2f rad) with the flame lit for %d frames' % (aw['spin'], aw['flameFrames']))

        co = pg.evaluate(CORE)
        print('core', co)
        save(pg, '__coreSnap', '03_core_lance.png')
        ok(co['phase'] == 'core', 'breaking both arms opens the CORE')
        ok(co['rearmed'] and co['rearms'] == 1 and abs(co['shieldRatio'] - 0.70) < 0.02, 'and the fire shield rearms ONCE, at 70%% (%s)' % co['shieldRatio'])
        ok(co['ringPeak'] >= 18, 'the reactor nova throws a full ring (%d rounds on screen)' % co['ringPeak'])
        ok(co['widest'] > 100 and co['lanceSnd'] >= 1, 'the furnace lance swells to %d px' % co['widest'])
        ok(co['creep'] is not None and co['creep'] > 8, 'and creeps toward the player while it burns (+%s px)' % co['creep'])

        hd = pg.evaluate(HEAD)
        print('head', hd)
        save(pg, '__headSnap', '04_head_lasers.png')
        ok(hd['phase'] == 'head' and hd['shieldOff'], 'the PREDATOR HEAD flies alone, unshielded (the named exception Mike approved)')
        ok(hd['errAtOpen'] is not None and hd['errAtOpen'] < 0.12,
           'THE LASERS TRACK: a player who reversed late in the charge is still under the beam when it opens (%.3f rad off)' % (hd['errAtOpen'] if hd['errAtOpen'] is not None else 9))
        ok(hd['hitsAfterDodge'] == 0, 'but a committed dodge during the burn escapes it (%d hits after leaving)' % hd['hitsAfterDodge'])
        ok(hd['hitsStill'] >= 1, 'and standing still is punished (%d hits)' % hd['hitsStill'])
        ok(hd['dead'], 'destroying the head kills the Furnace Tyrant')
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
