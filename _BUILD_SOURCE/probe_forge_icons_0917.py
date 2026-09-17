#!/usr/bin/env python3
"""
probe_forge_icons_0917.py - the forged badges reach the screen, by KEY, in real Chromium.

Mike, 0917: "I wanted weapon icons of each type after being upgraded with our element type,
generate those."

What this checks:
  REGISTERED - every micon_forge_<elem>_<slot> for 9 elements x 6 forgeable slots is in X._src, the
               file decodes (XART.rdy polled - false on its first call), and it is FAMILY height.
  RESOLVED   - weaponIconKey(w) answers the forged key once the slot is forged, and the tier key again
               after a re-spec; with an opt (a pickup question) it answers the forged key too.
  DRAWN      - on the live Forge screen a forged machine gun's box asks XART for micon_forge_fire_0
               (XART.get wrapped and the KEY recorded - a canvas has no .src), and the EQUIPPED box
               on stage 2 draws it through iconBlit.
  CONTROL    - an element with no plate registered (a bogus key) keeps the tier icon: the branch is
               registered-or-nothing, never a hole.

⚠ A proof frame is taken INSIDE the run while the Forge is up.
"""
import os, sys, base64, json
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.join(ROOT, '_BUILD_SOURCE'))
import shoot as sh
from playwright.sync_api import sync_playwright

OUT = os.path.join(ROOT, 'docs', 'proofs', 'forge_icons_0917')
ELEMS = ['fire', 'ice', 'lightning', 'prism', 'toxic', 'kinetic', 'chrome', 'water', 'dark']
SLOTS = [0, 1, 2, 3, 5, 7]
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
        pg.wait_for_function("() => typeof setState==='function' && typeof forgeStart==='function'", timeout=60000)
        pg.wait_for_function("() => (window.__bofFrames|0) > 4", timeout=60000)
        pg.evaluate(sh.TRAP_RAF)
        pg.evaluate(sh.SETUP, {'state': 'PLAY', 'stage': 1, 'pilot': 'cole'})
        pg.evaluate("() => { window.__step=%s; window.playerHit=function(){}; run.mode='arcade'; run.lives=9; }" % sh.STEP)
        keys = ['micon_forge_%s_%d' % (e, s) for e in ELEMS for s in SLOTS]
        # ---- REGISTERED ----
        reg = pg.evaluate("(ks) => ks.filter(k => !(XART._src && XART._src[k]))", keys)
        ok(len(reg) == 0, '54 forged badge keys are registered in the code-owned X._src block (%d missing)' % len(reg))
        pg.evaluate("(ks) => { for(const k of ks) XART.rdy(k); }", keys)
        pg.wait_for_function("(ks) => ks.every(k => XART.rdy(k))", arg=keys, timeout=30000)
        dims = pg.evaluate("(ks) => ks.map(k => { const im=XART.get(k); return im ? [im.width, im.height] : null; })", keys)
        ok(all(d and d[1] == 112 for d in dims), 'all 54 decode at the FAMILY height (112)')
        ws = sorted(set(d[0] for d in dims if d))
        print('  widths:', ws)
        ok(ws and ws[0] >= 80 and ws[-1] <= 140, 'and their widths sit in one family (%d..%d)' % (ws[0], ws[-1]))
        # ---- RESOLVED ----
        pg.evaluate("() => { run.forge={}; run.forgeElems={}; run.loadout=null; run.forgeCombos=2; run.forgeRespecs=2; run.weapon=0; run.wlevel=1; run.infusion=null; forgeDiscover('fire'); forgeDiscover('lightning'); }")
        k0 = pg.evaluate("() => weaponIconKey(0, 1)")
        ok(k0 == 'micon_mg_1', 'a bare machine gun resolves its tier icon (%s)' % k0)
        pg.evaluate("() => forgeCombine(0, 'fire')")
        k1 = pg.evaluate("() => weaponIconKey(0, 1)")
        ok(k1 == 'micon_forge_fire_0', 'a FORGED machine gun resolves micon_forge_fire_0 (%s)' % k1)
        k1o = pg.evaluate("() => weaponIconKey(0, 1, {fixed:true})")
        ok(k1o == 'micon_forge_fire_0', 'and so does a PICKUP question about that slot - the crate agrees with the name (%s)' % k1o)
        pg.evaluate("() => forgeCombine(7, 'lightning')")
        k7 = pg.evaluate("() => weaponIconKey(7, 3)")
        ok(k7 == 'micon_forge_lightning_7', 'the chaingun (slot 7, its own branch) resolves micon_forge_lightning_7 (%s)' % k7)
        # control: a forged element whose plate is not registered keeps the tier icon
        pg.evaluate("() => { run.forge[3]={elem:'bogus',lv:1}; }")
        k3 = pg.evaluate("() => weaponIconKey(3, 2)")
        ok(k3 == 'micon_laser_2', 'CONTROL: a forged element with no registered plate keeps the tier icon, never a hole (%s)' % k3)
        pg.evaluate("() => { delete run.forge[3]; forgeRespec(0); }")
        k0b = pg.evaluate("() => weaponIconKey(0, 1)")
        ok(k0b == 'micon_mg_1', 'after a RE-SPEC the machine gun is back on its tier icon (%s)' % k0b)
        nm = pg.evaluate("() => weaponDisplayName(7)")
        ok(nm == 'STORM GATLING', 'the chaingun is named STORM GATLING beside its badge (%s)' % nm)

        # ---- DRAWN: the live Forge screen ----
        pg.evaluate("() => { chaingunUnlock(); laserMistUnlock(); run.weapon=0; run.wlevel=1; run.forgeCombos=2; forgeCombine(0,'fire'); run.loadout=[2,0,1,3,5,7]; XART.rdy('statpanel_full_0916'); }")   # the chaingun must be IN the loadout to have a box - forgeLoadoutSync fills six from the pool in order and slot 7 is the eighth
        pg.wait_for_function("() => XART.rdy('statpanel_full_0916')", timeout=30000)
        pg.evaluate("() => { window.__keys={}; const g=XART.get.bind(XART); XART.get=function(k){ if(/^micon_forge_/.test(String(k))) window.__keys[k]=(window.__keys[k]|0)+1; return g(k); }; forgeStart(function(){ setState(GS.TITLE); }); }")
        pg.evaluate("() => { for(let i=0;i<50;i++) window.__step(1); }")
        pg.wait_for_timeout(600)
        pg.evaluate("() => { window.__keys={}; for(let i=0;i<30;i++) window.__step(1); }")
        k = pg.evaluate("() => window.__keys")
        print('  forge asks:', json.dumps(k))
        ok(pg.evaluate("() => state==='forge'"), 'the Forge is up')
        ok(k.get('micon_forge_fire_0', 0) >= 20, 'the machine gun box asks XART for micon_forge_fire_0 by KEY every frame (%d of 30)' % k.get('micon_forge_fire_0', 0))
        ok(k.get('micon_forge_lightning_7', 0) >= 20, 'and the chaingun box for micon_forge_lightning_7 (%d of 30)' % k.get('micon_forge_lightning_7', 0))
        d = pg.evaluate("() => { const c=document.getElementById('screen'); return c?c.toDataURL('image/png'):null; }")
        if d: open(os.path.join(OUT, 'forge_badges_live.png'), 'wb').write(base64.b64decode(d.split(',', 1)[1]))
        # the picker list with badges
        pg.evaluate("() => { forge.row=2; forge.psel=0; forge.pscroll=0; window.__keys={}; for(let i=0;i<30;i++) window.__step(1); }")
        k2 = pg.evaluate("() => window.__keys")
        ok(k2.get('micon_forge_fire_0', 0) >= 20, 'the PICKER list draws the forged machine gun with its badge too (%d of 30)' % k2.get('micon_forge_fire_0', 0))
        d = pg.evaluate("() => { const c=document.getElementById('screen'); return c?c.toDataURL('image/png'):null; }")
        if d: open(os.path.join(OUT, 'forge_picker_live.png'), 'wb').write(base64.b64decode(d.split(',', 1)[1]))

        # ---- the EQUIPPED box in play ----
        pg.evaluate("() => { forge=null; setState(GS.PLAY); run.weapon=0; run.wlevel=1; forgeApply(); window.__keys={}; for(let i=0;i<40;i++) window.__step(1); }")
        k3 = pg.evaluate("() => window.__keys")
        ok(k3.get('micon_forge_fire_0', 0) >= 10, 'in PLAY the EQUIPPED box / HUD asks for micon_forge_fire_0 (%d of 40 frames)' % k3.get('micon_forge_fire_0', 0))
        pg.evaluate("() => { try{ localStorage.removeItem(CHAINGUN_UNLOCK_KEY); localStorage.removeItem(LASER_MIST_UNLOCK_KEY); }catch(_){} }")
        print('  errors:', len(errs))
        for e in errs[:5]: print('   !', e[:200])
        ok(len(errs) == 0, 'no page or console errors (%d)' % len(errs))
        br.close()
    stop()
    print('\n%d ok / %d fail' % (N['ok'], len(FAILS)))
    for f in FAILS: print('  FAIL', f)
    sys.exit(1 if FAILS else 0)

if __name__ == '__main__':
    main()
