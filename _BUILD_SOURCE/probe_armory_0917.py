#!/usr/bin/env python3
"""
probe_armory_0917.py - the currency, on the live screens, in real Chromium.

Mike, 0917: "Furious Points are the answer to incentivise playing the game on higher difficulties and
other pilots, and your Score Points in-game ... You use your high score points to purchase Furious
Points. All icons here should get their level 1-5 upgrade generated variants, and upgraded projectiles."

The chain, every input a real key tap:
  a HARD run ends -> GAME OVER prints the BANKED line (score x difficulty x new-pilot)
  the VAULT's EXCHANGE row buys Furious Points from that credit
  THE ARMORY (last vault row): tabs per weapon, rows per element, FIRE buys the next level, the badge
  on the row changes to the level's own plate, a short balance is refused with the shortfall named
  the Forge: combining the bought element opens the weapon at the OWNED level and the box wears the
  level badge; RETINA opens the Armory from the Forge and BACK returns
  in play: a level-V round is bigger and hits harder than the same gun bare (measured on pBullets)

⚠ The profile is localStorage and PERSISTS - cleared at the start and at the end (the awards probe's lesson).
"""
import os, sys, base64, json
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.join(ROOT, '_BUILD_SOURCE'))
import shoot as sh
from playwright.sync_api import sync_playwright

OUT = os.path.join(ROOT, 'docs', 'proofs', 'armory_0917')
N = {'ok': 0}; FAILS = []
def ok(c, m):
    if c: N['ok'] += 1; print('  ok   ' + m)
    else: FAILS.append(m); print('  FAIL ' + m)

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
        pg.wait_for_function("() => typeof setState==='function' && typeof drawArmory==='function'", timeout=60000)
        pg.wait_for_function("() => (window.__bofFrames|0) > 4", timeout=60000)
        pg.evaluate(sh.TRAP_RAF)
        pg.evaluate("() => { try{ localStorage.removeItem(ACHIEVEMENT_STORE_KEY); }catch(_){} achievementReload(); }")
        pg.evaluate(sh.SETUP, {'state': 'PLAY', 'stage': 1, 'pilot': 'cole'})
        pg.evaluate("() => { window.__step=%s; window.playerHit=function(){}; run.mode='arcade'; run.lives=9; diffKey='hard'; DIFF=difficultyForRun(run.mode,'hard'); XART.rdy('statpanel_full_0916'); }" % sh.STEP)
        def step(n): pg.evaluate("(n) => { for(let i=0;i<n;i++) window.__step(1); }", n)
        def tap(k, hold=2, settle=6):
            pg.evaluate("([k]) => BOSSMODE.hold(k,true)", [k]); step(hold)
            pg.evaluate("([k]) => BOSSMODE.hold(k,false)", [k]); step(settle)
        def shot(name):
            d = pg.evaluate("() => { const c=document.getElementById('screen'); return c?c.toDataURL('image/png'):null; }")
            if d: open(os.path.join(OUT, name + '.png'), 'wb').write(base64.b64decode(d.split(',', 1)[1]))
        keys = pg.evaluate("() => ({fire:(keybind.fire||['j'])[0], retina:(keybind.retina||['c'])[0], back:(keybind.back||['k'])[0]})")
        print('  keys:', json.dumps(keys))
        for _ in range(4): step(8); pg.wait_for_timeout(300)

        # ---- 1. the run ends: GAME OVER banks the score ----
        pg.evaluate("() => { run.score=120000; run.lives=0; triggerGameOver(); }")
        step(90)
        B = pg.evaluate("() => run._banked")
        ok(pg.evaluate("() => state==='gameover'"), 'GAME OVER is up')
        ok(B and B['credit'] == 270000 and B['dm'] == 1.5 and B['pm'] == 1.5, 'a 120,000 HARD run on a fresh Cole banks 270,000 credit (x1.5 x1.5): %s' % json.dumps(B))
        ok(pg.evaluate("() => scoreBankCredit()===270000 && furiousBalance()===0"), 'the credit is in the bank; the balance is still 0 until exchanged')
        shot('01_gameover_banked')
        # the BANKED line is drawn: trap fillText
        n = pg.evaluate("() => { let n=0; const f=ctx.fillText; ctx.fillText=function(t){ if(/^BANKED/.test(String(t))) n++; return f.apply(this,arguments); }; for(let i=0;i<3;i++) window.__step(1); ctx.fillText=f; return n; }")
        ok(n >= 3, 'the GAME OVER screen prints the BANKED line every frame (%d of 3)' % n)

        # ---- 2. the VAULT exchanges it ----
        pg.evaluate("() => { setState(GS.VAULT); vaultOpen(); }")
        step(30); pg.wait_for_timeout(500); step(10)
        ok(pg.evaluate("() => vault.rows[0].exchange===true && vault.i===0"), 'the VAULT opens on the EXCHANGE row')
        shot('02_vault_exchange')
        tap(keys['fire'])
        ok(pg.evaluate("() => furiousBalance()===270 && scoreBankCredit()===0"), 'FIRE on EXCHANGE buys 270 FURIOUS PTS and empties the credit')
        ok('270' in pg.evaluate("() => vault.msg"), 'and the screen says so: %r' % pg.evaluate("() => vault.msg"))
        tap(keys['fire'])
        ok(pg.evaluate("() => furiousBalance()===270") and 'NOTHING' in pg.evaluate("() => vault.msg"), 'a second press with nothing banked is refused with words')
        # DOWN to THE ARMORY (the last row) and open it
        rows = pg.evaluate("() => vault.rows.length")
        for _ in range(rows - 1): tap('s', 2, 3)
        ok(pg.evaluate("() => vault.rows[vault.i].armory===true"), 'DOWN x%d lands on THE ARMORY' % (rows - 1))
        tap(keys['fire'])
        ok(pg.evaluate("() => state==='armory' && armory && armory.back==='vault'"), 'FIRE opens THE ARMORY (back = vault)')

        # ---- 3. THE ARMORY: buy a level ----
        pg.evaluate("() => { for(const e of Object.keys(INFUSIONS)) for(const w of FORGE_WEAPONS) for(let l=1;l<=5;l++) XART.rdy('micon_forge_'+e+'_'+w+(l>1?'_'+l:'')); }")
        pg.wait_for_function("() => XART.rdy('micon_forge_lightning_3_2') && XART.rdy('micon_forge_lightning_3')", timeout=30000)
        step(20)
        shot('03_armory_mg')
        tap('d', 2, 3); tap('d', 2, 3); tap('d', 2, 3)
        ok(pg.evaluate("() => FORGE_WEAPONS[armory.tab]===3"), 'RIGHT x3 is the LASER tab')
        tap('s', 2, 3); tap('s', 2, 3)
        ok(pg.evaluate("() => Object.keys(INFUSIONS)[armory.i]==='lightning'"), 'DOWN x2 is LIGHTNING (TESLA BEAM)')
        pg.evaluate("() => { window.__keys={}; const g=XART.get.bind(XART); XART.get=function(k){ if(/^micon_forge_lightning_3/.test(String(k))) window.__keys[k]=(window.__keys[k]|0)+1; return g(k); }; for(let i=0;i<10;i++) window.__step(1); }")
        k0 = pg.evaluate("() => window.__keys")
        ok(k0.get('micon_forge_lightning_3', 0) >= 10 and not k0.get('micon_forge_lightning_3_2'), 'the TESLA BEAM row wears the level-I badge before the buy (%s)' % json.dumps(k0))
        tap(keys['fire'])
        ok(pg.evaluate("() => forgeOwnedLevel('lightning',3)===2 && furiousBalance()===270-FORGE_LEVEL_COST[2]"), 'FIRE buys TESLA BEAM level II and the price leaves the balance')
        pg.evaluate("() => { window.__keys={}; for(let i=0;i<10;i++) window.__step(1); }")
        k1 = pg.evaluate("() => window.__keys")
        ok(k1.get('micon_forge_lightning_3_2', 0) >= 10, 'and the row now wears the level-II badge, by KEY (%s)' % json.dumps(k1))
        shot('04_armory_tesla_L2')
        tap(keys['fire'])
        ok(pg.evaluate("() => forgeOwnedLevel('lightning',3)===2") and 'MORE FURIOUS PTS' in pg.evaluate("() => armory.msg"), 'level III is refused - the balance is short and the shortfall is named: %r' % pg.evaluate("() => armory.msg"))
        shot('05_armory_refused')
        tap(keys['back'])
        ok(pg.evaluate("() => state==='vault'"), 'BACK returns to the VAULT')

        # ---- 4. the Forge opens the weapon at the owned level; RETINA opens the Armory and BACK returns ----
        pg.evaluate("() => { setState(GS.PLAY); run.forge={}; run.forgeElems={}; run.loadout=null; run.weapon=3; run.wlevel=1; forgeDiscover('lightning'); forgeStart(function(){ setState(GS.TITLE); }); }")
        step(50); pg.wait_for_timeout(400); step(10)
        ok(pg.evaluate("() => state==='forge'"), 'the Forge is up')
        # walk to the laser slot and combine (list -> keep -> element -> FIRE)
        pg.evaluate("() => { forge.sel=run.loadout.indexOf(3); }")
        tap(keys['fire']); tap(keys['fire']); tap(keys['fire'])
        F = pg.evaluate("() => ({f:run.forge[3]||null, inf:run.infusion, icon:weaponIconKey(3,1), nm:weaponDisplayName(3)})")
        ok(F['f'] and F['f']['elem'] == 'lightning' and F['f']['lv'] == 2, 'combining LIGHTNING on the LASER opens it at the OWNED level II: %s' % json.dumps(F['f']))
        ok(F['icon'] == 'micon_forge_lightning_3_2' and F['nm'] == 'TESLA BEAM', 'the badge is the level-II plate and the name TESLA BEAM (%s)' % F['icon'])
        step(20); shot('06_forge_tesla_L2')
        tap(keys['retina'])
        ok(pg.evaluate("() => state==='armory' && armory.back==='forge'"), 'RETINA on the Forge opens THE ARMORY (back = forge)')
        step(20); shot('07_armory_from_forge')
        tap(keys['back'])
        ok(pg.evaluate("() => state==='forge' && !!forge"), 'BACK returns to the Forge, which is still there')

        # ---- 5. in play: a level-V round is bigger and hits harder ----
        pg.evaluate("() => { forge=null; setState(GS.PLAY); enemies.length=0; pBullets.length=0; run.weapon=0; run.wlevel=1; run.forge={}; run.infusion=null; player.dead=false; }")
        fire = keys['fire']
        def rounds(frames):
            pg.evaluate("([k]) => { pBullets.length=0; BOSSMODE.hold(k,true); }", [fire]); step(frames)
            pg.evaluate("([k]) => BOSSMODE.hold(k,false)", [fire])
            return pg.evaluate("() => pBullets.filter(b=>b.kind==='mg'&&!b._child).map(b=>({w:b.w,h:b.h,dmg:b.dmg,inf:b._inf||null,sc:!!b._infScaled}))")
        bare = rounds(20)
        pg.evaluate("() => { for(let l=2;l<=5;l++) achievementState.owned[forgeLevelId('fire',0,l)]={at:1,cost:0}; run.forgeCombos=2; forgeDiscover('fire'); forgeCombine(0,'fire'); }")
        ok(pg.evaluate("() => run.forge[0].lv===5 && run.infusion.lv===5"), 'with fire I..V owned, combining fire on the MG holds it at level V')
        five = rounds(20)
        print('  bare:', json.dumps(bare[:2]), ' level V:', json.dumps(five[:2]))
        ok(len(bare) >= 2 and len(five) >= 2, 'both guns fired (%d / %d rounds)' % (len(bare), len(five)))
        ok(all(r['inf'] is None for r in bare) and all(r['inf'] == 'fire' and r['sc'] for r in five), 'the bare rounds carry no element; the level-V rounds are fire and scaled once each')
        ok(five[0]['dmg'] > bare[0]['dmg'] and abs(five[0]['w'] / bare[0]['w'] - 1.24) < 0.02, 'a level-V round hits harder (%d vs %d) and is 24%% bigger (w %.1f vs %.1f)' % (five[0]['dmg'], bare[0]['dmg'], five[0]['w'], bare[0]['w']))

        pg.evaluate("() => { try{ localStorage.removeItem(ACHIEVEMENT_STORE_KEY); }catch(_){} }")
        print('  errors:', len(errs))
        for e in errs[:6]: print('   !', e[:200])
        ok(len(errs) == 0, 'no page or console errors (%d)' % len(errs))
        br.close()
    stop()
    print('\n%d ok / %d fail' % (N['ok'], len(FAILS)))
    for f in FAILS: print('  FAIL', f)
    sys.exit(1 if FAILS else 0)

if __name__ == '__main__':
    main()
