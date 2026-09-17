#!/usr/bin/env python3
"""
probe_forge_noncarriers_0917.py - the flamethrower, laser mist and the lightning orb really take an
element, measured in real Chromium.

Mike, 0917, listing the equip rule: "1 flamethrower/ice breath/ other types upgrade." Those three were
listed as CANNOT TAKE AN ELEMENT because their rounds were not in INFUSION_CARRIERS - a reading taken
from the table rather than from the muzzles. This proves the three claims that matter for each of them:

  STAMPED  - the round in flight carries _inf and _infLv (identified on the live pBullets, not inferred)
  ON HIT   - the element's own touch lands on a real enemy through the shared hook: fire sets _burn,
             ice stacks _frozen, toxic sets _poison. Measured on a drone that is hit by that weapon and
             by nothing else.
  LOOK     - the level's aura is drawn for it (infusionGlowPlate / the column plate asked for by KEY),
             and the flame takes the COLUMN path rather than a round plate the height of its reach.
  NAMED    - weaponDisplayName answers the forged name, so the Forge box and the HUD say what it is.

⚠ The flamethrower is Cole's slot 4 and the ICE BREATH is Freezer's - flameIsIce() decides which, so the
mist/orb runs are flown by the pilots who own them (laser mist is universal, the lightning orb is Yuri's).
"""
import os, sys, base64, json
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.join(ROOT, '_BUILD_SOURCE'))
import shoot as sh
from playwright.sync_api import sync_playwright

OUT = os.path.join(ROOT, 'docs', 'proofs', 'forge_noncarriers_0917')
N = {'ok': 0}; FAILS = []
def ok(c, m):
    if c: N['ok'] += 1; print('  ok   ' + m)
    else: FAILS.append(m); print('  FAIL ' + m)

CASES = [
    # slot, pilot, element, the field the element's touch writes, the forged name
    (4, 'cole',   'toxic',     '_poison', 'VENOM JET'),
    (6, 'cole',   'fire',      '_burn',   'EMBER MIST'),
    (8, 'yuri',   'ice',       '_frozen', 'HAIL SPHERE'),
]

def main():
    os.makedirs(OUT, exist_ok=True)
    port, stop = sh.serve(sh.GAME)
    with sync_playwright() as pw:
        br = pw.chromium.launch()
        pg = br.new_page(viewport={'width': 1000, 'height': 1200})
        errs = []
        pg.on('pageerror', lambda e: errs.append('page:' + str(e)))
        pg.on('console', lambda m: errs.append('console:' + m.text) if m.type == 'error' else None)
        pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=60000)
        pg.wait_for_function("() => typeof setState==='function' && typeof forgeCombine==='function'", timeout=60000)
        pg.wait_for_function("() => (window.__bofFrames|0) > 4", timeout=60000)
        pg.evaluate(sh.TRAP_RAF)
        # the three slots answer the rule before a single round is fired
        pg.evaluate(sh.SETUP, {'state': 'PLAY', 'stage': 1, 'pilot': 'cole'})
        pg.evaluate("() => { window.__step=%s; window.playerHit=function(){}; run.mode='arcade'; run.lives=9; mapScroll=2400; }" % sh.STEP)
        ok(pg.evaluate("() => FORGE_WEAPONS.length===9 && [4,6,8].every(w=>forgeCanTake(w))"),
           'the Forge accepts all nine weapon slots, including 4 / 6 / 8')
        ok(pg.evaluate("() => Object.keys(INFUSIONS).every(e=>[4,6,8].every(w=>typeof FORGE_NAMES[e][w]==='string'&&FORGE_NAMES[e][w].indexOf(\"'\")<0))"),
           'every element x new slot has a name, none carrying an apostrophe (the UI face has no usable one)')
        ok(pg.evaluate("() => ['flame','lasermist','yuriLightningOrb','yuriLightningBolt'].every(k=>!!INFUSION_CARRIERS[k])"),
           'and their round kinds are carriers: flame / lasermist / yuriLightningOrb / yuriLightningBolt')

        key = pg.evaluate("() => (keybind.fire||['j'])[0]")
        for slot, pilot, elem, field, name in CASES:
            pg.evaluate(sh.SETUP, {'state': 'PLAY', 'stage': 1, 'pilot': pilot})
            pg.evaluate("""([w,e,k]) => {
              window.__step=%s; window.playerHit=function(){}; run.mode='arcade'; run.lives=9; mapScroll=2400;
              enemies.length=0; pBullets.length=0; particles.length=0;
              run.weapon=w; run.wlevel=5; run.wlevels[w]=5; run.forge={}; run.forge[w]={elem:e,lv:4}; run.infusion=null; forgeApply();
              /* ⚠ EACH REWARD WEAPON REFUSES TO FIRE UNTIL IT IS UNLOCKED - yuriLightningOrbFire's first
                 line is a pilot AND unlock gate, so the probe's first run measured 0 rounds on slot 8 and
                 read as a dead forge. The probe was short an unlock, the game was right. */
              if(w===6 && typeof laserMistUnlock==='function') laserMistUnlock();
              if(w===8 && typeof yuriLightningOrbGrantStage4==='function') yuriLightningOrbGrantStage4();
              run.weapon=w; run.wlevel=5;   /* the grant EQUIPS its own weapon - put the hand back */
              player.x=worldWidth()*0.5; player.y=400; player.dead=false; player.fireCd=0;
              window.__aura=0; const g=infusionGlowPlate; infusionGlowPlate=function(a,b,c){ window.__aura++; return g(a,b,c); };
              window.__col=0; const di=ctx.drawImage; ctx.drawImage=function(){ if(window.__inAura) window.__col++; return di.apply(this,arguments); };
              const ad=infusionAuraDraw; infusionAuraDraw=function(b){ window.__inAura=true; window.__auraKind=b.kind; try{ return ad(b); } finally{ window.__inAura=false; } };
              /* ONE target, directly above, that shoots nothing and drops nothing */
              const t=spawnEnemy('drone',{x:player.x,y:250}); if(t){ t.x=player.x; t.y=250; t.vx=0; t.vy=0; t.shoots=false; t.hp=900; t.maxhp=900; t.dropOk=false; window.__t=t; }
            }""" % sh.STEP, [slot, elem, key])
            pg.evaluate("([k]) => BOSSMODE.hold(k,true)", [key])
            pg.evaluate("() => { for(let i=0;i<70;i++) window.__step(1); }")
            R = pg.evaluate("""([f]) => ({
                 name:weaponDisplayName(run.weapon), inf:run.infusion?run.infusion.elem+':'+run.infusion.lv:null,
                 stamped:pBullets.filter(b=>b._inf).map(b=>b.kind+':'+b._inf+':'+(b._infLv|0)).slice(0,3),
                 nStamped:pBullets.filter(b=>b._inf).length, nRounds:pBullets.length,
                 touch:(window.__t?(window.__t[f]||0):0), hp:(window.__t?window.__t.hp:null),
                 aura:window.__aura, col:window.__col, auraKind:window.__auraKind||null })""", [field])
            shot = pg.evaluate("() => { const c=document.getElementById('screen'); return c?c.toDataURL('image/png'):null; }")
            if shot: open(os.path.join(OUT, 'slot%d_%s.png' % (slot, elem)), 'wb').write(base64.b64decode(shot.split(',', 1)[1]))
            pg.evaluate("([k]) => BOSSMODE.hold(k,false)", [key])
            print('  slot %d %s: %s' % (slot, elem, json.dumps(R)))
            ok(R['name'] == name, 'slot %d forged %s is named %s (%s)' % (slot, elem, name, R['name']))
            ok(R['nStamped'] > 0 and all(x.endswith(':' + elem + ':4') for x in R['stamped']),
               'its rounds in flight carry the element AND the level (%s)' % R['stamped'])
            ok(R['touch'] > 0, "the element's own touch landed on the target through the shared hook (%s = %s)" % (field, R['touch']))
            ok(R['hp'] is not None and R['hp'] < 900, 'and the weapon still did its ordinary damage (hp %s of 900)' % R['hp'])
            if slot == 4:
                ok(R['auraKind'] == 'flame' and R['col'] > 0, 'the FLAME takes the column aura, not a round plate the height of its reach (%s, %d blits)' % (R['auraKind'], R['col']))
                ok(R['aura'] == 0, 'so it never asks for a round glow plate (%d)' % R['aura'])
            else:
                ok(R['aura'] > 0, 'the level aura plate is asked for by KEY on every frame it is alive (%d)' % R['aura'])

        # the flamethrower keeps its OWN element through the forge
        pg.evaluate(sh.SETUP, {'state': 'PLAY', 'stage': 1, 'pilot': 'cole'})
        pg.evaluate("""() => { window.__step=%s; run.weapon=4; run.wlevel=5; run.forge={4:{elem:'ice',lv:3}}; run.infusion=null; forgeApply();
          pBullets.length=0; player.fireCd=0; player.dead=false; }""" % sh.STEP)
        pg.evaluate("([k]) => BOSSMODE.hold(k,true)", [key]); pg.evaluate("() => { for(let i=0;i<20;i++) window.__step(1); }")
        F = pg.evaluate("() => { const f=pBullets.filter(b=>b.kind==='flame')[0]; return f?{el:f._el,inf:f._inf}:null; }")
        pg.evaluate("([k]) => BOSSMODE.hold(k,false)", [key])
        ok(F and F['el'] == 'fire' and F['inf'] == 'ice',
           "Cole's FLAMETHROWER forged with ICE stays a FIRE weapon that also chills (_el %s, _inf %s)" % (F and F['el'], F and F['inf']))
        print('  errors:', len(errs))
        for e in errs[:5]: print('   !', e[:200])
        pg.evaluate("() => { try{ localStorage.removeItem(YURI_LIGHTNING_ORB_UNLOCK_KEY); localStorage.removeItem(LASER_MIST_UNLOCK_KEY); }catch(_){} }")
        ok(len(errs) == 0, 'no page or console errors (%d)' % len(errs))
        br.close()
    stop()
    print('\n%d ok / %d fail' % (N['ok'], len(FAILS)))
    for f in FAILS: print('  FAIL', f)
    sys.exit(1 if FAILS else 0)

if __name__ == '__main__':
    main()
