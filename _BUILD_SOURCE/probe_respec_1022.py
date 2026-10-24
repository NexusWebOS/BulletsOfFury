#!/usr/bin/env python3
"""
probe_respec_1022.py - RE-SPEC on the Forge, the Loadout and Decker's Upgrade Center (Mike, 2026-10-22).

Real Chromium, the real loop stepped (TRAP_RAF + STEP), keys through real KeyboardEvents.
  1. a stage clear (entering the debrief) grants 2 upgrades / 2 re-specs, and a Forge visit keeps them;
  2. THE FORGE: CHARGE once arms (nothing removed), CHARGE again removes the forged element, refunds the
     upgrade and costs a re-spec; the weapon can then be forged with a DIFFERENT element;
  3. a click on the Forge's re-spec bar arms it too;
  4. THE LOADOUT: CHARGE twice re-specs the selected bay;
  5. DECKER'S UPGRADE CENTER: RE-SPEC A WEAPON lists the weapons, FIRE twice re-specs the chosen one,
     B goes back to Decker's rows;
  6. with no re-specs left it refuses and removes nothing;
  7. the budget rides the campaign save;
  8. busted arm: window.RS22_OFF=1 - the old re-spec leaves the form earned and refunds nothing;
  9. 0 page / console errors.
--shots writes proof frames to docs/proofs/respec_1022/.
"""
import os, sys, base64
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.join(ROOT, '_BUILD_SOURCE'))
import shoot as sh
from playwright.sync_api import sync_playwright
N = {'ok': 0}; FAILS = []
SHOTS = '--shots' in sys.argv
OUT = os.path.join(ROOT, 'docs', 'proofs', 'respec_1022')
def ok(c, m):
    if c: N['ok'] += 1; print('  ok   ' + m)
    else: FAILS.append(m); print('  FAIL ' + m)

SEED = """() => { run.mode='campaign'; run.pilot='decker'; run.stage=2; coopOn=false; run.ngplus=false;
  run.forgeElems={fire:1, ice:1}; run.forgeForms={0:{fire:{elem:'fire',lv:1}}}; run.forge={0:run.forgeForms[0].fire};
  run.wlevels=WEAPONS.map((_,i)=>i<6?1:0); run.weapon=0; run.loadout=null; forgeLoadoutSync(); }"""

def main():
    port, stop = sh.serve(sh.GAME)
    with sync_playwright() as pw:
        br = pw.chromium.launch(executable_path='/opt/pw-browsers/chromium', args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
        pg = br.new_page(viewport={'width': 1100, 'height': 900}); errs = []
        pg.on('pageerror', lambda e: errs.append('page:' + str(e)[:200]))
        pg.on('console', lambda m: errs.append('console:' + m.text[:200]) if m.type == 'error' else None)
        pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=90000)
        pg.wait_for_function("() => (window.__bofFrames|0) > 4", timeout=90000)
        pg.evaluate(sh.TRAP_RAF)
        pg.evaluate("() => { window.__step=%s; }" % sh.STEP)
        pg.evaluate("""() => { window.__press=(k)=>{ window.dispatchEvent(new KeyboardEvent('keydown',{key:k,bubbles:true})); window.__step(1);
                       window.dispatchEvent(new KeyboardEvent('keyup',{key:k,bubbles:true})); }; }""")
        def settle(n=40): pg.evaluate("(n) => { for(let i=0;i<n;i++) window.__step(1); }", n)
        def real(n=4):
            for _ in range(n): settle(15); pg.wait_for_timeout(250)
        def ev(js, a=None): return pg.evaluate(js, a) if a is not None else pg.evaluate(js)
        def state(): return ev("() => state")
        def press(k): ev("(k) => window.__press(k)", k); settle(4)
        def shot(name):
            if not SHOTS: return
            os.makedirs(OUT, exist_ok=True)
            d = ev("() => document.getElementById('screen').toDataURL('image/png')")
            open(os.path.join(OUT, name + '.png'), 'wb').write(base64.b64decode(d.split(',')[1]))
        def forms(w=0): return ev("(w) => Object.keys((run.forgeForms&&run.forgeForms[w])||{})", w)
        def budget(): return ev("() => [run.forgeCombos|0, run.forgeRespecs|0]")

        # 1. the stage clear grants, the Forge keeps
        ev(SEED)
        ev("() => { run.forgeCombos=0; run.forgeRespecs=0; setState(GS.STAGECLEAR); }")
        ok(budget() == [2, 2], 'a stage clear grants 2 upgrades / 2 re-specs (%s)' % budget())
        ev("() => { run.forgeRespecs=1; run.forgeCombos=0; forgeStart(()=>setState(GS.TITLE)); }"); real(3)
        ok(state() == 'forge' and budget() == [0, 1], 'a Forge visit keeps what the stage has left (%s %s)' % (state(), budget()))
        # 2. the Forge: arm, then re-spec
        ev("() => { run.forgeRespecs=2; forge.sel=0; forge.row=0; }"); real(2)
        shot('forge_button')
        press('h'); real(1)
        armed = ev("() => !!(forge._rsArm) && forge.msg")
        ok(armed and 'AGAIN' in armed and forms() == ['fire'], 'Forge: the first CHARGE arms and removes nothing (%r)' % armed)
        shot('forge_armed')
        press('h'); real(1)
        ok(forms() == [] and budget() == [1, 1] and not ev("() => !!run.forge[0]"),
           'Forge: the second CHARGE removes INCENDIARY SLUGS, refunds 1 upgrade, costs 1 re-spec (forms %s budget %s)' % (forms(), budget()))
        ok(ev("() => !run.infusion"), 'the equipped machine gun drops its fire infusion')
        r = ev("() => forgeCombine(0,'ice')")
        ok(r == 'ok' and forms() == ['ice'], 'the weapon can now be forged with a different element (%s %s)' % (r, forms()))
        shot('forge_done')
        # 3. a click on the bar arms
        ev("() => { if(state!==GS.FORGE){ forgeStart(()=>setState(GS.TITLE)); } forge._rsArm=null; forge.sel=0; forge.row=0; forge.t=2; }"); real(1)
        hit = ev("""() => { const W=cutsceneViewWidth(),H=VH,B=frc(RS22_FORGE_BAR,W,H); forge.md=false;
                    Object.assign(Input.mouse,{x:B[0]+B[2]/2,y:B[1]+B[3]/2,down:true,inside:true}); window.__step(1);
                    Input.mouse.down=false; window.__step(1); return [!!forge._rsArm, forge.row]; }""")
        ok(hit[0] and hit[1] == 0, 'Forge: a click on the RE-SPEC bar arms it, the slot does not open (%s)' % hit)
        # 4. the Loadout
        ev("() => { forge=null; run.forgeForms[1]={toxic:{elem:'toxic',lv:1}}; run.forge[1]=run.forgeForms[1].toxic; run.forgeElems.toxic=1; run.forgeRespecs=1; run.forgeCombos=0; loadoutStart(()=>setState(GS.TITLE)); }")
        real(3); ev("() => { loadoutScr.sel=run.loadout.indexOf(1); loadoutScr.row=0; }"); real(1)
        press('h'); real(1); press('h'); real(1)
        ok(forms(1) == [] and budget() == [1, 0], 'Loadout: CHARGE twice re-specs the selected bay (forms %s budget %s)' % (forms(1), budget()))
        shot('loadout_after')
        # 6. none left
        ev("() => { run.forgeForms[1]={toxic:{elem:'toxic',lv:1}}; run.forgeRespecs=0; loadoutScr._rsArm=null; }")
        press('h'); real(1); press('h'); real(1)
        ok(forms(1) == ['toxic'] and ev("() => loadoutScr.msg").startswith('NO RE-SPECS LEFT'), 'with no re-specs left it refuses and removes nothing (%r)' % ev("() => loadoutScr.msg"))
        ev("() => { loadoutScr=null; }")
        # 5. Decker's Upgrade Center
        ev(SEED)
        ev("""() => { run.forgeRespecs=2; run.forgeCombos=0; UC22.focus=false; UC22.open=false; UC22.pending=false; window.sselCommitted=false;
                 campaign.unlockedMax=3; campaign.bonusUnlocked=false; campaign._booted=true; campaign._introSeen=true; openStageSelect(2,{}); }""")
        for _ in range(40):
            settle(60)
            if ev("() => state===GS.STAGESEL && campPauseIsCampaignScreen() && !sselUnlockCine && sselBoot===0"): break
        ev("() => { UC22.focus=true; UC22.pending=true; }"); real(3)
        ok(ev("() => UC22.open"), "Decker's screen is open on the map")
        ok(ev("() => UC22_ROWS[2]") == 'RE-SPEC A WEAPON', 'Decker offers RE-SPEC A WEAPON')
        ev("() => { UC22.sel=2; UC22.t=1; }"); press('j'); real(2)
        ok(ev("() => !!UC22.rs") and state() == 'stagesel', 'RE-SPEC A WEAPON opens the weapon list on the map')
        ev("() => { UC22.rs.sel=uc22RespecWeapons().indexOf(0); }"); real(2)
        shot('center_list')
        press('j'); real(1)
        ok(forms() == ['fire'] and 'AGAIN' in ev("() => UC22.msg"), 'Upgrade Center: FIRE once arms (%r)' % ev("() => UC22.msg"))
        shot('center_armed')
        press('j'); real(1)
        ok(forms() == [] and budget() == [1, 1], 'Upgrade Center: FIRE again re-specs the machine gun (forms %s budget %s)' % (forms(), budget()))
        shot('center_done')
        press('escape'); real(2)
        ok(ev("() => UC22.open && !UC22.rs && UC22.sel===2"), "B goes back to Decker's rows")
        press('escape'); real(2)
        ok(not ev("() => UC22.open"), "a second B leaves Decker's screen")
        # 7. save
        snap = ev("() => { run.forgeRespecs=1; run.forgeCombos=2; return campSnapshot(); }")
        ok(snap.get('forgeRespecs') == 1 and snap.get('forgeCombos') == 2, 'the campaign save carries the budget')
        back = ev("(s) => { run.forgeRespecs=0; run.forgeCombos=0; campApply(s); return [run.forgeCombos, run.forgeRespecs]; }", snap)
        ok(back == [2, 1], 'loading the save restores it (%s)' % back)
        # 8. busted arm
        ev(SEED)
        old = ev("() => { window.RS22_OFF=1; run.forgeRespecs=2; run.forgeCombos=0; const r=forgeRespec(0); const o=[r, Object.keys(run.forgeForms[0]||{}), run.forgeCombos]; window.RS22_OFF=0; return o; }")
        ok(old[1] == ['fire'] and old[2] == 0, 'busted arm: RS22_OFF keeps the form and refunds nothing (%s)' % old)
        bad = [e for e in errs if 'favicon' not in e and 'AudioContext encountered an error' not in e]
        ok(not bad, 'page/console errors: %d %s' % (len(bad), bad[:3]))
        br.close()
    stop()
    print('\n%d ok / %d fail' % (N['ok'], len(FAILS)))
    for f in FAILS: print('  FAIL ' + f)
    sys.exit(1 if FAILS else 0)

if __name__ == '__main__':
    main()
