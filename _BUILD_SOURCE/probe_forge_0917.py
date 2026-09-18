#!/usr/bin/env python3
"""
probe_forge_0917.py - THE FORGE, driven like a player, in real Chromium.

Mike, 0917: "the in between stage screen of weapons being unlocked, weapons being combined ...
You should be allowed 2 combinations in between each level, and this upgrade permanently takes
over your weapon style until you reset it via re-spec ... 2 re-specs per level completion ...
limit the amount of weapon types that can spawn to 6 per level, and make the player select their
loadout including their new upgraded weapon type replacing the weapon type it was I.E machine gun
now becomes incendary slugs."

The whole flow, end to end, with REAL KEY TAPS through the game's own bind table:

  play stage 1 -> a real INFUSE pickup is collected (that is how an element is DISCOVERED)
  -> the boss dies -> the debrief -> CONTINUE -> THE FORGE
  -> combine MG + fire (INCENDIARY SLUGS) -> combine LASER + lightning (TESLA BEAM)
  -> a third combine is refused -> re-spec the laser -> swap a loadout slot
  -> CONTINUE -> stage 2 -> the MG is still INCENDIARY SLUGS, its rounds wear fire,
     and the crate pool is the six-weapon loadout.

⚠ EVERY MENU READER CONSUMES ITS TAP, so the load-bearing assertion is that ONE press moves the
cursor EXACTLY one slot (CLAUDE.md: `menuLeft()||menuRight()` always resolving to +1).
⚠ THE WEAPON UNLOCKS ARE ACCOUNT-LEVEL (localStorage). They are set here to make the pool bigger
than the loadout, and REMOVED at the end so the next probe boots clean.
"""
import os, sys, base64, json, io
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.join(ROOT, '_BUILD_SOURCE'))
import shoot as sh
from playwright.sync_api import sync_playwright

OUT = os.path.join(ROOT, 'docs', 'proofs', 'forge_0917')
N = {'ok': 0}; FAILS = []
def ok(c, m):
    if c: N['ok'] += 1; print('  ok   ' + m)
    else: FAILS.append(m); print('  FAIL ' + m)

GRAB = ("() => {"
        " const g = document.querySelector('#screen-area canvas') || document.querySelector('canvas');"
        " if(!g) return null; return g.toDataURL('image/png'); }")

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
        pg.wait_for_function("() => typeof setState==='function' && typeof forgeStart==='function'", timeout=60000)
        pg.wait_for_function("() => (window.__bofFrames|0) > 4", timeout=60000)
        pg.evaluate(sh.TRAP_RAF)
        pg.evaluate(sh.SETUP, {'state': 'PLAY', 'stage': 1, 'pilot': 'cole'})
        pg.evaluate("() => { window.__step=%s; window.playerHit=function(){}; run.lives=9; enemies.length=0; mapScroll=2400; }" % sh.STEP)
        # the account-level unlocks, so more weapons are unlocked than the loadout holds
        # ⚠ chaingunUnlock() EQUIPS the chaingun - it is the stage-5 reward path, and it hands the
        # player the gun. Left alone it made the held weapon slot 7 for the whole probe, so the MG's
        # forged element never had a gun in hand to apply to and five assertions failed on a build
        # that was right. The unlock is taken, the hand is put back on the machine gun.
        pg.evaluate("() => { chaingunUnlock(); laserMistUnlock(); run.weapon=0; run.wlevel=1; run.mode='arcade'; }")
        pg.evaluate("() => { XART.rdy('statpanel_full_0916'); for(const e of Object.keys(INFUSIONS)) XART.rdy('inf_'+e); }")
        for _ in range(6):
            pg.evaluate("() => window.__step(8)"); pg.wait_for_timeout(400)

        def step(n): pg.evaluate("(n) => { for(let i=0;i<n;i++) window.__step(1); }", n)
        def tap(k, after=3):
            pg.evaluate("([k]) => BOSSMODE.hold(k,true)", [k]); step(1)
            pg.evaluate("([k]) => BOSSMODE.hold(k,false)", [k]); step(after)
        def shot(name):
            d = pg.evaluate(GRAB)
            if d: open(os.path.join(OUT, name + '.png'), 'wb').write(base64.b64decode(d.split(',', 1)[1]))
        def st(): return pg.evaluate("() => state")
        def until(pred, cap, chunk=10, wait=60):
            for _ in range(cap):
                if pg.evaluate(pred): return True
                step(chunk); pg.wait_for_timeout(wait)
            return False

        mode = pg.evaluate("() => run.mode")
        print('  run.mode', mode, '| pool', pg.evaluate("() => crateWeaponPool(true)"))

        # ---- the combinations are EARNED FROM BOSSES (0917 economy) -------------------------------------
        # This probe used to discover elements through a field INFUSE pickup. Since 32f4eac4 a pickup grants
        # nothing and since 0917b none reach the field at all; the boss drop is proven by probe_bossdrop_0917.
        # Here the two pairs are granted through the SAME function that drop calls, so the Forge is tested
        # on a known profile rather than on whichever pair a random boss drop happens to hand over.
        pg.evaluate("() => { forgeComboGrant('fire',0); forgeComboGrant('lightning',3); run.infusion=null; }")
        ok(pg.evaluate("() => JSON.stringify(forgeDiscovered())") == '["fire","lightning"]',
           'forgeDiscovered() lists the earned elements in table order: fire, lightning')
        ok(pg.evaluate("() => JSON.stringify(forgeElemsFor(0))+JSON.stringify(forgeElemsFor(3))") == '["fire"]["lightning"]',
           'and each is earned for ITS slot only: fire on the MG, lightning on the laser')
        ok(pg.evaluate("() => forgeVisible()"), 'forgeVisible() - there is something to do, so the screen will open')

        # ---- the boss dies, the debrief runs, CONTINUE opens the Forge ----------------------------
        pg.evaluate("() => { enemies.length=0; spawnBoss(curStage.boss); }")
        step(30)
        pg.evaluate("() => { boss.hp=0; bossDie(); }")
        # the boss's own guaranteed drop would add a RANDOM pair to the profile - taken off the field so the
        # element lists below are the two granted above (probe_bossdrop_0917 owns the drop itself)
        pg.evaluate("() => { const _kd=forgeBossDrop; forgeBossDrop=function(){ return null; }; setTimeout(function(){ forgeBossDrop=_kd; }, 60000); powerups=powerups.filter(function(q){ return q.kind!=='forgecombo'; }); }")
        ok(until("() => state==='stageclear'", 260), 'the boss death runs through to the debrief (state stageclear)')
        step(80)
        tap('enter', 20); step(60)
        for _ in range(12):
            if st() == 'forge': break
            tap('enter', 20); step(30)
        ok(st() == 'forge', 'CONTINUE on the debrief opens THE FORGE (state %s)' % st())
        step(60); pg.wait_for_timeout(600); step(10)
        shot('forge_01_open')
        F = pg.evaluate("() => ({sel:forge.sel,row:forge.row,combos:run.forgeCombos,respecs:run.forgeRespecs,load:run.loadout,pool:forge.pool})")
        print('  forge open:', json.dumps(F))
        ok(F['combos'] == 2 and F['respecs'] == 2, 'it opens with 2 COMBINES and 2 RE-SPECS for this stage')
        ok(len(F['pool']) > 6 and len(F['load']) == 6, 'with %d weapons unlocked the loadout is capped at 6' % len(F['pool']))
        ok(len(set(F['load'])) == 6 and all(w in F['pool'] for w in F['load']), 'the loadout is six DISTINCT unlocked weapons')

        # ---- the cursor moves exactly one slot per press ------------------------------------------
        tap('d'); s1 = pg.evaluate("() => forge.sel")
        tap('d'); s2 = pg.evaluate("() => forge.sel")
        tap('a'); s3 = pg.evaluate("() => forge.sel")
        ok((s1, s2, s3) == (1, 2, 1), 'RIGHT, RIGHT, LEFT move the cursor exactly 1, 2, 1 (%s)' % str((s1, s2, s3)))
        tap('a')
        ok(pg.evaluate("() => forge.sel") == 0, 'and back on the MACHINE GUN')

        # ---- combine MG + fire ------------------------------------------------------------------
        # 0917b: a slot opens its ELEMENT row directly (the weapon list moved to the LOADOUT screen), and a
        # combine opens THE FORGING -> THE PRODUCT; BACK on the product returns to the Forge.
        def weld_back():
            ok(pg.evaluate("() => state") == 'forging', 'the combine opens THE FORGING')
            step(300)
            ok(pg.evaluate("() => state") == 'forged', 'the weld runs 0-100% and the PRODUCT comes up')
            step(30); tap('escape', 10)
            ok(pg.evaluate("() => state") == 'forge', 'BACK on the product returns to the Forge')
        tap('j'); ok(pg.evaluate("() => forge.row") == 1, 'FIRE on a slot goes straight to its element row')
        ok(pg.evaluate("() => forgeDiscovered()[forge.esel]") == 'fire', 'the element cursor starts on FIRE')
        shot('forge_02_pick_element')
        tap('j')
        R = pg.evaluate("() => ({f:run.forge[0]||null, c:run.forgeCombos, row:forge.row, nm:weaponDisplayName(0), inf:run.infusion?run.infusion.elem+':'+run.infusion.lv:null})")
        print('  after combine:', json.dumps(R))
        ok(R['f'] and R['f']['elem'] == 'fire' and R['f']['lv'] == 1, 'the machine gun is FORGED: fire, level 1')
        ok(R['c'] == 1, 'one combine spent (1 left)')
        ok(R['nm'] == 'INCENDIARY SLUGS', 'and it is named INCENDIARY SLUGS (%s)' % R['nm'])
        ok(R['inf'] == 'fire:1', 'the held weapon takes the element at once (run.infusion %s)' % R['inf'])
        weld_back()
        step(20); shot('forge_03_incendiary_slugs')

        # ---- combine LASER + lightning, then the third combine is refused ----------------------------
        tap('d'); tap('d'); tap('d')
        ok(pg.evaluate("() => run.loadout[forge.sel]") == 3, 'three RIGHT presses land on the LASER')
        tap('j')
        want = pg.evaluate("() => forgeElemsFor(3).indexOf('lightning')")
        for _ in range(max(0, want)): tap('d')
        ok(pg.evaluate("() => forgeElemsFor(3)[forge.esel]") == 'lightning', 'RIGHT on the element row picks LIGHTNING')
        tap('j')
        R2 = pg.evaluate("() => ({f:run.forge[3]||null, c:run.forgeCombos, nm:weaponDisplayName(3)})")
        ok(R2['f'] and R2['f']['elem'] == 'lightning' and R2['nm'] == 'TESLA BEAM', 'the laser is FORGED lightning: TESLA BEAM (%s)' % R2['nm'])
        ok(R2['c'] == 0, 'both combines spent')
        weld_back()
        step(20); shot('forge_04_tesla_beam')
        tap('j')
        ok(pg.evaluate("() => forge.row") == 0 and 'NO COMBINES' in pg.evaluate("() => forge.msg"),
           'a THIRD combine is refused and says why: %r' % pg.evaluate("() => forge.msg"))

        # ---- re-spec the laser ----------------------------------------------------------------------
        tap('h')
        R3 = pg.evaluate("() => ({f:run.forge[3]||null, r:run.forgeRespecs, nm:weaponDisplayName(3)})")
        ok(R3['f'] is None and R3['nm'] == 'LASER' and R3['r'] == 1, 'CHARGE re-specs the laser back to LASER, one re-spec left (%s)' % json.dumps(R3))
        step(20); shot('forge_05_respec')

        # ---- the save carries it ----------------------------------------------------------------------
        snap = pg.evaluate("() => { const s=campSnapshot(); return {forge:s.forge, elems:s.forgeElems, load:s.loadout}; }")
        # the EARNED combinations live in the profile (achievementState.owned), not in the run save - so the
        # save carries what this RUN forged and its loadout, and the combinations survive without it
        ok(snap['forge'].get('0', {}).get('elem') == 'fire' and len(snap['load']) == 6,
           'campSnapshot carries the forge and the loadout')
        ok(pg.evaluate("() => forgeComboOwned('fire',0) && forgeComboOwned('lightning',3)"),
           'and the earned combinations are the PROFILE\'s, independent of any run save')
        ok(pg.evaluate("() => { const s=campSnapshot(); const keep={f:run.forge,e:run.forgeElems,l:run.loadout};"
                       " run.forge={}; run.forgeElems={}; run.loadout=null; campApply(s);"
                       " const r=!!(run.forge[0]&&run.forge[0].elem==='fire'&&run.loadout&&run.loadout.length===6);"
                       " run.forge=keep.f; run.forgeElems=keep.e; run.loadout=keep.l; run.mode='arcade'; return r; }"),
           'campApply restores them onto a cleared run')

        # ---- START -> THE LOADOUT: the scrollable list, one ding per icon (Mike, 0917) -----------------
        # "when I select a weapon slot, should become like a scrollable list I can select and ding's with
        # each icon. Missiles is a slot that remains Missiles and will never not be missiles"
        tap('enter', 20)
        ok(pg.evaluate("() => state") == 'loadout', 'START on the Forge opens THE LOADOUT (%s)' % pg.evaluate("() => state"))
        step(50)
        pg.evaluate("() => { loadoutScr.sel=run.loadout.indexOf(3); window.__blips=0; const b=Audio.SFX.blip; Audio.SFX.blip=function(){ window.__blips++; return b&&b.apply(this,arguments); }; }")
        tap('j')
        ok(pg.evaluate("() => loadoutScr.row") == 1, 'FIRE on a bay opens the weapon pool')
        ok(pg.evaluate("() => loadoutScr.pool[loadoutScr.psel]===run.loadout[loadoutScr.sel]"), 'the pool opens on the weapon already in that bay')
        b0 = pg.evaluate("() => window.__blips|0")
        tap('d'); p1 = pg.evaluate("() => loadoutScr.psel"); tap('d'); p2 = pg.evaluate("() => loadoutScr.psel"); tap('a'); p3 = pg.evaluate("() => loadoutScr.psel")
        b1 = pg.evaluate("() => window.__blips|0")
        n = pg.evaluate("() => loadoutScr.pool.length")
        ok(p2 == (p1 + 1) % n and p3 == p1, 'RIGHT, RIGHT, LEFT move the pool cursor exactly +1, +1, -1 (%s)' % str((p1, p2, p3)))
        ok(b1 - b0 >= 3, 'and each move DINGS (%d blips for 3 moves)' % (b1 - b0))
        step(20); shot('forge_06_picker')
        pg.evaluate("() => { loadoutScr.psel = loadoutScr.pool.indexOf(6); }")
        sel_pick = pg.evaluate("() => loadoutScr.sel")
        before = pg.evaluate("() => run.loadout.slice()")
        tap('j')
        after = pg.evaluate("() => run.loadout.slice()")
        ok(after[sel_pick] == 6 and 6 not in before and len(set(after)) == 6 and 2 in after,
           'FIRE puts the picked weapon in the bay, no duplicates, missiles still in the loadout (%s -> %s)' % (before, after))
        ok(pg.evaluate("() => loadoutScr.row") == 0, 'and the pool closes')
        mi = pg.evaluate("() => run.loadout.indexOf(2)")
        pg.evaluate("([i]) => { loadoutScr.sel = i; }", [mi])
        tap('j')
        ok(pg.evaluate("() => loadoutScr.row") == 0 and 'MISSILES STAY MISSILES' in pg.evaluate("() => loadoutScr.msg"),
           'FIRE on the MISSILES bay refuses the pool and says so: %r' % pg.evaluate("() => loadoutScr.msg"))
        pg.evaluate("() => { loadoutScr.sel = 1; }")
        tap('j'); pg.evaluate("() => { loadoutScr.psel = loadoutScr.pool.indexOf(run.loadout[4]); }")
        b4 = pg.evaluate("() => run.loadout[4]"); b1w = pg.evaluate("() => run.loadout[1]")
        tap('j')
        ok(pg.evaluate("([a,b]) => run.loadout[1]===a && run.loadout[4]===b", [b4, b1w]), 'picking a weapon that sits in another bay SWAPS the two bays')
        step(10)

        # ---- CONTINUE -> the next stage, where the machine gun is still INCENDIARY SLUGS ---------------
        tap('enter', 20)   # START on the loadout fades to the next level
        ok(until("() => state==='play' && (run.stage|0)===2", 400, 10, 40), 'CONTINUE leaves the Forge and stage 2 begins (state %s, stage %s)' % (st(), pg.evaluate("() => run.stage")))
        pg.evaluate("() => { player.dead=false; enemies.length=0; }")
        for _ in range(6):
            step(8); pg.wait_for_timeout(300)
        P = pg.evaluate("() => ({w:run.weapon, inf:run.infusion?run.infusion.elem+':'+run.infusion.lv:null, nm:weaponDisplayName(run.weapon), pool:crateWeaponPool(), load:run.loadout})")
        print('  stage 2:', json.dumps(P))
        ok(P['w'] == 0 and P['inf'] == 'fire:1', 'on stage 2 the held MG carries its forged element (run.infusion %s)' % P['inf'])
        ok(P['nm'] == 'INCENDIARY SLUGS', 'and is still named INCENDIARY SLUGS')
        ok(len(P['pool']) <= 6 and all(w in P['load'] for w in P['pool']), 'the crate pool on stage 2 is the six-weapon loadout (%s)' % P['pool'])
        key = pg.evaluate("() => { const b=BOSSMODE.binds(); return (b&&b.fire&&b.fire[0])||'j'; }")
        pg.evaluate("([k]) => BOSSMODE.hold(k,true)", [key]); step(40)
        tagged = pg.evaluate("() => pBullets.filter(b=>b.kind==='mg'&&b._inf==='fire').length")
        pg.evaluate("([k]) => BOSSMODE.hold(k,false)", [key])
        ok(tagged > 0, 'its rounds are stamped fire in flight (%d)' % tagged)
        shot('play_stage2_incendiary_slugs')

        # ---- death keeps the FORGE (it is permanent) even though it clears the in-play element ---------
        ok(pg.evaluate("() => { run.infusion=null; forgeApply(); return run.infusion&&run.infusion.elem==='fire'; }"),
           'after the in-play element is cleared, forgeApply puts the forged one straight back')

        print('  errors:', len(errs))
        for e in errs[:6]: print('   !', e[:200])
        ok(len(errs) == 0, 'no page or console errors (%d)' % len(errs))
        # leave the account clean
        pg.evaluate("() => { try{ localStorage.removeItem(CHAINGUN_UNLOCK_KEY); localStorage.removeItem(LASER_MIST_UNLOCK_KEY); }catch(_){} }")
        br.close()
    stop()
    json.dump({'ok': N['ok'], 'fail': FAILS}, open(os.path.join(OUT, '_result.json'), 'w'), indent=2)
    print('\n%d ok / %d fail' % (N['ok'], len(FAILS)))
    for f in FAILS: print('  FAIL', f)
    sys.exit(1 if FAILS else 0)

if __name__ == '__main__':
    main()
