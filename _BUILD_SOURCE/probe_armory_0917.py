#!/usr/bin/env python3
"""
probe_armory_0917.py - the currency, on the live screens, in real Chromium.

Mike, 0917: "Furious Points are the answer to incentivise playing the game on higher difficulties and
other pilots, and your Score Points in-game ... You use your high score points to purchase Furious
Points. All icons here should get their level 1-5 upgrade generated variants, and upgraded projectiles."

The chain, every input a real key tap:
  a LEVEL ends -> computeStageResults converts that level's own score at 1,000 : 1, the remainder
  carries, and run.score is untouched; the RUN end banks nothing and the VAULT has no EXCHANGE row
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

        # ---- 1. THE LEVEL ENDS: its own score becomes FURIOUS POINTS ----
        # Mike, 0917: "At the end of each level, your Maintain your 'Score Points' as a high score
        # record keeper, but at the end of each level, your 'points' convert into FP".
        # Driven through computeStageResults, the real STAGE CLEAR path, not through the conversion
        # function itself - the claim is about WHERE it happens as much as what it does.
        pg.evaluate("""() => { run.stage=2; run.score=9400; run._fpLevelDone=false; stageStats.scoreStart=2000;
          window.__scoreBefore=run.score; computeStageResults(); }""")
        step(4)
        L = pg.evaluate("() => ({fp:furiousConverted(), bal:furiousBalance(), carry:furiousCarry(), score:run.score, before:window.__scoreBefore, n:(achievementState.fp&&achievementState.fp.levels.length)|0, e:run._fpLevel})")
        print('  level 2 end:', json.dumps(L))
        # [!] ASSERTED ON WHAT WAS CONVERTED, NOT ON THE BALANCE. The stage clear that drives this also
        # AWARDS achievements, and since Mike's "achievement points are also tied to this" those land in
        # the same balance - so a balance assertion here would be measuring the awards as well.
        ok(L['fp'] == 7, "a 7,400-point level converts to 7 FURIOUS PTS at 1,000:1 (%s)" % L['fp'])
        ok(L['bal'] >= 7, 'and those points are in the spendable balance (%s, awards included)' % L['bal'])
        ok(L['score'] == L['before'] == 9400, 'and THE SCORE IS NEVER SPENT - it stays the high-score record (%s)' % L['score'])
        ok(L['carry'] == 400, 'the 400 remainder CARRIES to the next level rather than evaporating (%s)' % L['carry'])
        ok(L['n'] == 1 and L['e'] and L['e']['stage'] == 2, 'the ledger holds ONE entry, for the level that earned it')
        # the next level converts again, and the carry pays out in it
        pg.evaluate("() => { beginStage(3); run.score=9400+700; stageStats.scoreStart=9400; computeStageResults(); }")
        step(4)
        C = pg.evaluate("() => ({fp:furiousConverted(), carry:furiousCarry(), n:achievementState.fp.levels.length})")
        ok(C['fp'] == 8 and C['carry'] == 100, 'the next level converts again and the carry pays out: 400 + 700 = 1 more point (%s)' % json.dumps(C))
        ok(C['n'] == 2 and pg.evaluate("() => achievementState.fp.levels.reduce((a,b)=>a+b.fp,0)===furiousConverted()"),
           'what has been converted is the SUM of the per-level entries, never a stored counter')

        # ---- 1b. the RUN end banks nothing any more, and says nothing about it ----
        pg.evaluate("() => { run.score=120000; run.lives=0; triggerGameOver(); }")
        step(90)
        ok(pg.evaluate("() => state==='gameover'"), 'GAME OVER is up')
        nb = pg.evaluate("() => { let n=0; const f=ctx.fillText; ctx.fillText=function(t){ if(/BANKED/.test(String(t))) n++; return f.apply(this,arguments); }; for(let i=0;i<3;i++) window.__step(1); ctx.fillText=f; return n; }")
        ok(nb == 0, 'and it prints NO BANKED line - the run end is not where points come from any more (%d)' % nb)
        ok(pg.evaluate("() => furiousConverted()===8"), 'a 120,000-point run ending converts nothing: only a LEVEL converts')
        shot('01_gameover_no_bank')

        # ---- 2. the VAULT has no EXCHANGE row, and THE ARMORY is its last ----
        # seeded the only way there is now: a level that scored 1,200,000, which is one rung of the
        # upgrade ladder (1,000) plus change - so the buy below succeeds and the NEXT one, at 1,250,
        # is honestly short, which is what the refusal act needs.
        # [!] THE COMBINATIONS ARE EARNED FROM A BOSS (Mike, 0917) - the ARMORY only sells their LEVELS,
        # so the two pairs this probe buys levels for are granted the way the pickup grants them.
        # probe_bossdrop_0917.py is what proves the boss actually leaves one.
        pg.evaluate("""() => { achievementState=achievementEmpty(); furiousConvertLevel(1, 1200000);
          forgeComboGrant('lightning',3); forgeComboGrant('fire',0);
          setState(GS.VAULT); vaultOpen(); }""")
        step(30); pg.wait_for_timeout(500); step(10)
        V = pg.evaluate("() => ({n:vault.rows.length, cat:furiousShopIds().length, ex:vault.rows.filter(r=>r.exchange).length, last:!!vault.rows[vault.rows.length-1].armory, bal:furiousBalance()})")
        print('  vault:', json.dumps(V))
        ok(V['ex'] == 0, 'the VAULT has NO EXCHANGE row - the conversion is automatic, so there is nothing to press (%d)' % V['ex'])
        ok(V['n'] == V['cat'] + 1 and V['last'], 'it is the catalogue, then THE ARMORY last')
        ok(V['bal'] == 1200, 'and the balance the sub-header shows is what the levels converted (%d)' % V['bal'])
        shot('02_vault_no_exchange')
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
        ok(pg.evaluate("() => forgeOwnedLevel('lightning',3)===2 && furiousBalance()===1200-1000"), 'FIRE buys TESLA BEAM level II at the first rung (1,000) and the price leaves the balance')
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
        pg.evaluate("() => { setState(GS.PLAY); run.forge={}; run.forgeElems={}; run.loadout=null; run.weapon=3; run.wlevel=1; forgeStart(function(){ setState(GS.TITLE); }); }")
        step(50); pg.wait_for_timeout(400); step(10)
        ok(pg.evaluate("() => state==='forge'"), 'the Forge is up')
        # walk to the laser slot and combine (slot -> element -> FIRE). 0917b: the weapon LIST moved to the
        # LOADOUT screen, so a slot opens its elements directly, and the combine opens THE FORGING.
        pg.evaluate("() => { forge.sel=run.loadout.indexOf(3); }")
        tap(keys['fire']); tap(keys['fire'])
        F = pg.evaluate("() => ({f:run.forge[3]||null, inf:run.infusion, icon:weaponIconKey(3,1), nm:weaponDisplayName(3)})")
        ok(F['f'] and F['f']['elem'] == 'lightning' and F['f']['lv'] == 2, 'combining LIGHTNING on the LASER opens it at the OWNED level II: %s' % json.dumps(F['f']))
        ok(F['icon'] == 'micon_forge_lightning_3_2' and F['nm'] == 'TESLA BEAM', 'the badge is the level-II plate and the name TESLA BEAM (%s)' % F['icon'])
        # the weld is its own screen now: skip it, let the product come up, and BACK (FORGE MORE) returns here
        ok(pg.evaluate("() => state==='forging'"), 'the combine opens THE FORGING (0917b)')
        step(30); tap(keys['fire']); step(90)   # a press in the weld's first 0.4s is ignored, so it cannot carry the combine's own press
        ok(pg.evaluate("() => state==='forged'"), 'and then the PRODUCT screen')
        step(40); tap(keys['back']); step(10)
        ok(pg.evaluate("() => state==='forge'"), 'BACK on the product (a combine left) returns to the Forge')
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
        pg.evaluate("() => { for(let l=2;l<=5;l++) achievementState.owned[forgeLevelId('fire',0,l)]={at:1,cost:0}; run.forgeCombos=2; forgeCombine(0,'fire'); }")
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
