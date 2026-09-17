#!/usr/bin/env python3
"""
probe_infusion_0917.py - THE WEAPON INFUSIONS, IN REAL CHROMIUM.

Mike, 0917: "toy around with being able to toy around with the orbs, lasers, missiles and pellet based
weapons. Combinations could be incendiary bullets, lightning bullets, ice bullets ... This does not
apply to level 5 or level 9, space levels are in-eligible from this system."

Every element is driven through the REAL path: an infused round pushed by pShoot, stepped by the
live bullet loop, striking a unit through _hitEnemyCore. The effect is asserted on the TARGET - a
burn timer, a freeze stack, an arc in `zaps`, shards in pBullets - never on the flag that says the
effect should have happened.

⚠ A ROUND'S INFUSION IS STAMPED THE FIRST FRAME IT IS LIVE, so a bullet read straight after
pShoot has `_inf===undefined` and reads as "not infused" on a working build. Step one frame first.
⚠ ENG-05 (0915): a fresh hull survives its first lethal hit at 1hp. Kills here take two.
"""
import os, sys, base64
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.join(ROOT, '_BUILD_SOURCE'))
import shoot as sh
from playwright.sync_api import sync_playwright
OUT = os.path.join(ROOT, 'docs', 'proofs', 'infusion_0917')
N = {'ok': 0}; FAILS = []
def ok(c, m):
    if c: N['ok'] += 1; print('  ok   ' + m)
    else: FAILS.append(m); print('  FAIL ' + m)
def shot(pg, name):
    d = pg.evaluate("() => { const c=document.getElementById('screen'); return c?c.toDataURL('image/png'):null; }")
    if d: open(os.path.join(OUT, name), 'wb').write(base64.b64decode(d.split(',', 1)[1]))

ARM = """(elem) => {
  /* a clean field, the element at the level asked, a target parked in the gun line */
  enemies.length = 0; pBullets.length = 0; zaps.length = 0; particles.length = 0;
  run.infusion = null; if (elem) { infusionGrant(elem); }
  player.x = 240; player.y = 420; player.fireCd = 0; run.weapon = 0; run.wlevel = 1; run.wlevels[0] = 1;
  /* ⚠ THE TARGET MUST NOT SHOOT BACK. Sixty frames of a live drone firing at a parked ship
     killed the pilot between sections, so the pickup test ran on a dead player and the death test
     passed on an infusion that was never granted - two green-looking results from one corpse. */
  const e = spawnEnemy('drone', {x: 240, y: 300}); e.x = 240; e.y = 300; e.vx = 0; e.vy = 0; e.hp = 60; e.maxhp = 60; e._nef = null; e.shoots = false;
  player.dead = false; player.invuln = 999; run.lives = 5;
  return e ? {hp: e.hp} : null; }"""

FIRE_AND_WAIT = """(n) => {
  /* fire, then step until the round is gone or n frames pass; report what the target became */
  pShoot(); const e = enemies[0]; let f = 0;
  while (f < n && pBullets.length && !e.dead) { updatePlay(1/60); f++; }
  return {frames: f, hp: e.hp, burn: e._burn||0, frozen: e._frozen||0, poison: e._poison||0,
          soaked: e._soaked||0, zaps: zaps.length, live: pBullets.length,
          shards: pBullets.filter(b => b._prism).length, y: e.y, dead: !!(e.dead||e._dyingT!=null)}; }"""

def main():
    os.makedirs(OUT, exist_ok=True)
    port, stop = sh.serve(sh.GAME)
    with sync_playwright() as pw:
        br = pw.chromium.launch(); pg = br.new_page(viewport={'width': 1000, 'height': 1100})
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.on('console', lambda m: errs.append('console:' + m.text) if m.type == 'error' else None)
        pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=60000)
        pg.wait_for_function("() => typeof setState==='function' && typeof infusionGrant==='function'", timeout=60000)
        pg.wait_for_function("() => (window.__bofFrames|0) > 4", timeout=60000)
        pg.evaluate(sh.TRAP_RAF)
        pg.evaluate(sh.SETUP, {'state': 'PLAY', 'stage': 2, 'pilot': 'cole'})
        for _ in range(4):
            pg.evaluate(sh.STEP, [10]); pg.wait_for_timeout(400)
        pg.evaluate("() => { stageTimer = 5; }")

        # ---------- the table and the gates ----------
        ok(pg.evaluate("() => Object.keys(INFUSIONS).length === 9"), 'nine elements in the table (chromium joined later on 0917)')
        ok(pg.evaluate("() => infusionEligible()"), 'stage 2 is eligible')
        pool = pg.evaluate("() => infusionPool()")
        ok('water' not in pool and 'dark' not in pool, 'water and dark matter are gated off until earned (%s)' % pool)
        ok(pg.evaluate("() => { const s=run.stage; run.stage=5; const r=infusionEligible(); run.stage=s; return !r; }"),
           'stage 5 is NOT eligible')
        ok(pg.evaluate("() => { const s=run.stage; run.stage=9; const r=infusionEligible(); run.stage=s; return !r; }"),
           'stage 9 is NOT eligible')
        # the drop never yields an infusion on an ineligible stage - measured, not assumed
        got = pg.evaluate("""() => { const s=run.stage; run.stage=5; let n=0;
            for (let i=0;i<400;i++){ powerups.length=0; dropPowerup(200,200); if (powerups.some(p=>p.kind==='infuse')) n++; }
            run.stage=s; powerups.length=0; return n; }""")
        ok(got == 0, 'and 400 drops on stage 5 yield ZERO infusion pickups (%d)' % got)
        got2 = pg.evaluate("""() => { let n=0;
            for (let i=0;i<600;i++){ powerups.length=0; dropPowerup(200,200); if (powerups.some(p=>p.kind==='infuse')) n++; }
            powerups.length=0; return n; }""")
        ok(got2 > 5, 'while 600 drops on stage 2 yield some (%d)' % got2)

        # ---------- the grant ladder ----------
        pg.evaluate("() => { window.__ban=[]; const o=arcadeBanner; window.__banO=o; arcadeBanner=function(t){ window.__ban.push(String(t)); return o.apply(this,arguments); }; }")
        lad = pg.evaluate("() => { run.infusion=null; const out=[]; for(let i=0;i<4;i++){ infusionGrant('fire'); out.push(run.infusion.lv); } return {lv:out, ban:window.__ban.slice()}; }")
        ok(lad['lv'] == [1, 2, 3, 3], 'the same element levels up and caps at 3 (%s)' % lad['lv'])
        ok(any('FIREBURST' in b for b in lad['ban']), 'and level 3 announces the NAMED combination: %s' % lad['ban'])
        ok(pg.evaluate("() => { infusionGrant('ice'); return run.infusion.elem==='ice' && run.infusion.lv===1; }"),
           'a different element replaces it at level 1')

        # ---------- a round carries it ----------
        pg.evaluate(ARM, 'fire')
        st = pg.evaluate("() => { pShoot(); updatePlay(1/60); return pBullets.map(b => ({kind:b.kind, inf:b._inf, el:b._el})); }")
        ok(st and all(b['inf'] == 'fire' and b['el'] == 'fire' for b in st),
           'MG rounds fired under FIRE carry _inf and the fire ELEMENT (%d rounds)' % len(st))

        # ---------- each element, through the real hit ----------
        pg.evaluate(ARM, 'fire'); r = pg.evaluate(FIRE_AND_WAIT, 60)
        ok(r['burn'] > 0, 'FIRE: the target is BURNING after the hit (burn %.2f, hp %s)' % (r['burn'], r['hp']))
        hp0 = r['hp']; r2 = pg.evaluate("() => { const e=enemies[0]; for(let i=0;i<40;i++) updatePlay(1/60); return e.hp; }")
        ok(r2 < hp0, 'and the burn keeps eating it with no more rounds (%s -> %s)' % (hp0, r2))

        pg.evaluate(ARM, 'ice'); pg.evaluate("() => { enemies[0].vy = 2.0; }")
        r = pg.evaluate(FIRE_AND_WAIT, 60)
        ok(r['hp'] < 60, 'ICE: the round lands')
        vy = pg.evaluate("() => enemies[0].vy")
        ok(vy < 1.2, 'and the target is SLOWED by the cold (vy 2.0 -> %.2f)' % vy)
        pg.evaluate(ARM, 'ice'); pg.evaluate("() => { infusionGrant('ice'); infusionGrant('ice'); }")
        r = pg.evaluate(FIRE_AND_WAIT, 60)
        ok(r['frozen'] >= 1, 'GLACIAL STRIKE (L3): every hit stacks a FREEZE (frozen %d)' % r['frozen'])

        pg.evaluate(ARM, 'lightning')
        pg.evaluate("() => { const o = spawnEnemy('drone', {x: 300, y: 300}); o.x=300; o.y=300; o.vx=0; o.vy=0; o.hp=60; o.maxhp=60; o.shoots=false; }")
        r = pg.evaluate(FIRE_AND_WAIT, 60)
        other = pg.evaluate("() => enemies[1] ? enemies[1].hp : null")
        ok(r['zaps'] >= 1, 'LIGHTNING: the hit ARCS (%d zaps)' % r['zaps'])
        ok(other is not None and other < 60, 'and the arc strikes the neighbour (hp 60 -> %s)' % other)

        # the round needs ~12 frames to reach y=300 from the muzzle; the shards need ~55 to leave
        pg.evaluate(ARM, 'prism'); r = pg.evaluate(FIRE_AND_WAIT, 30)
        ok(r['shards'] >= 2, 'PRISM: the hit SPLITS into shards (%d in flight)' % r['shards'])
        ok(pg.evaluate("() => pBullets.filter(b=>b._prism).every(b=>b._inf===null)"),
           'and the shards are stamped _inf null, so they can never split again')

        pg.evaluate(ARM, 'toxic'); r = pg.evaluate(FIRE_AND_WAIT, 60)
        ok(r['poison'] > 0, 'TOXIC: the target is POISONED (%.2f)' % r['poison'])
        hp0 = r['hp']; r2 = pg.evaluate("() => { const e=enemies[0]; for(let i=0;i<40;i++) updatePlay(1/60); return e.hp; }")
        ok(r2 < hp0, 'and the poison ticks with no more rounds (%s -> %s)' % (hp0, r2))

        pg.evaluate(ARM, None); base = pg.evaluate(FIRE_AND_WAIT, 60)
        pg.evaluate(ARM, 'kinetic'); pg.evaluate("() => { infusionGrant('kinetic'); infusionGrant('kinetic'); }")
        kin = pg.evaluate(FIRE_AND_WAIT, 60)
        ok((60 - kin['hp']) > (60 - base['hp']), 'KINETIC (L3): the same rounds hit HARDER (%s vs %s damage)' % (60 - kin['hp'], 60 - base['hp']))
        ok(kin['y'] < 300, 'and the target is knocked back up the screen (y 300 -> %.1f)' % kin['y'])

        # ---------- the round LOOKS infused ----------
        pg.evaluate(ARM, 'fire')
        pg.evaluate("() => { window.__p87=[]; const o=p87Body; window.__p87O=o; p87Body=function(lv,inf){ window.__p87.push(inf||null); return o.apply(this,arguments); }; pShoot(); updatePlay(1/60); drawWorld(1/60); }")
        infs = pg.evaluate("() => window.__p87.slice()")
        # ⚠ the MUZZLE FLASH draws through p87Body too, with no infusion - it is not a round. The
        # claim is that the ROUNDS carry the palette, so the flash's null is expected in the trace.
        fires = [i for i in infs if i == 'fire']
        ok(len(fires) >= 2, 'in flight the rounds go through the pack with the FIRE palette (%d fire draws; trace %s)' % (len(fires), [str(i) for i in infs]))
        shot(pg, '01_fire_rounds.png')
        pg.evaluate("() => { p87Body = window.__p87O; }")

        # ---------- god's wrath ----------
        pg.evaluate(ARM, 'lightning'); pg.evaluate("() => { infusionGrant('lightning'); infusionGrant('lightning'); }")
        pg.evaluate("""() => { for (let i=0;i<4;i++){ const o=spawnEnemy('drone',{x:120+i*80,y:200}); o.x=120+i*80; o.y=200; o.vx=0; o.vy=0; o.hp=60; o.maxhp=60; o.shoots=false; }
            window.__rnd=Math.random; Math.random=()=>0.01; }""")
        pg.evaluate("() => { enemies[0].hp = 1; }")
        r = pg.evaluate(FIRE_AND_WAIT, 60)
        ok(r['zaps'] >= 5, "GODS WRATH (lightning L3, on a kill): the whole screen is struck (%d zaps)" % r['zaps'])
        hurt = pg.evaluate("() => enemies.filter(e => e.hp < 60 || e.dead || e._dyingT!=null).length")
        ok(hurt >= 4, 'and every hostile on screen took it (%d of %d)' % (hurt, pg.evaluate("() => enemies.length")))
        pg.evaluate("() => { updatePlay(1/60); drawWorld(1/60); }")
        shot(pg, '02_gods_wrath.png')
        pg.evaluate("() => { Math.random = window.__rnd; }")

        # ---------- the pickup, and death ----------
        pg.evaluate("() => { player.dead=false; player.invuln=999; run.infusion=null; enemies.length=0; powerups.length=0; powerups.push({x:player.x,y:player.y,vy:0,t:0,kind:'infuse',elem:'toxic',w:20,h:20,bob:0}); updatePlay(1/60); updatePlay(1/60); }")
        ok(pg.evaluate("() => !!(run.infusion && run.infusion.elem==='toxic')"), 'collecting the pickup grants its element')
        pg.evaluate("() => { player.invuln=0; run.lives=5; playerHit(); for(let i=0;i<200;i++) updatePlay(1/60); }")
        ok(pg.evaluate("() => !run.infusion"), 'and death clears it, the way death drops the gun')
        pg.evaluate("() => { arcadeBanner = window.__banO; }")

        ok(pg.evaluate("() => ['fire','ice','lightning','prism','toxic','kinetic','water','dark'].every(e => typeof XART._src['inf_'+e]==='string')"),
           'all eight badges are registered')
        ok(not errs, 'no page or console errors (%d)' % len(errs))
        for e in errs[:6]: print('    !', e)
        br.close(); stop()
    print('\n%d ok / %d fail' % (N['ok'], len(FAILS)))
    for f in FAILS: print('  FAIL', f)
    sys.exit(1 if FAILS else 0)

if __name__ == '__main__':
    main()
