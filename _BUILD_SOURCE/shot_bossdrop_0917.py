#!/usr/bin/env python3
"""shot_bossdrop_0917.py - the proof card: the combination powerup on the field, the STYLISH award
over a live stage, the ARMORY with earned and unearned rows, and the Forge's per-slot element strip.

⚠ EVERY FRAME IS TAKEN INSIDE THE RUN, over the real playfield. A frame taken on a cleared canvas
proves the draw call ran and nothing about whether the thing is legible where it actually appears -
which is how the first STYLISH card came back as a word floating on white.
"""
import os, sys, base64
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.join(ROOT, '_BUILD_SOURCE'))
import shoot as sh
from playwright.sync_api import sync_playwright
OUT = os.path.join(ROOT, 'docs', 'proofs', 'bossdrop_0917')

def main():
    os.makedirs(OUT, exist_ok=True)
    port, stop = sh.serve(sh.GAME)
    with sync_playwright() as pw:
        br = pw.chromium.launch(); pg = br.new_page(viewport={'width': 1000, 'height': 1200})
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=60000)
        pg.wait_for_function("() => typeof forgeBossDrop==='function' && typeof drawArmory==='function'", timeout=60000)
        pg.wait_for_function("() => (window.__bofFrames|0) > 4", timeout=60000)
        pg.evaluate(sh.TRAP_RAF)
        pg.evaluate("() => { try{ localStorage.removeItem(ACHIEVEMENT_STORE_KEY); }catch(_){} achievementReload(); }")
        pg.evaluate(sh.SETUP, {'state': 'PLAY', 'stage': 1, 'pilot': 'cole'})
        pg.evaluate("() => { window.__step=%s; window.playerHit=function(){}; run.mode='arcade'; run.lives=9; }" % sh.STEP)
        def step(n): pg.evaluate("(n) => { for(let i=0;i<n;i++) window.__step(1); }", n)
        def shot(name):
            d = pg.evaluate("() => { const c=document.getElementById('screen'); return c?c.toDataURL('image/png'):null; }")
            if d: open(os.path.join(OUT, name + '.png'), 'wb').write(base64.b64decode(d.split(',', 1)[1]))
            print('  ' + name)
        step(10); pg.wait_for_timeout(1200); step(10)

        # the combination powerup, over the field, beside the player
        pg.evaluate("""() => { powerups.length=0; enemies.length=0;
          const P=forgeBossDrop(player.x, player.y-150);
          if(P){ P.vy=0; XART.rdy('inf_'+P.elem); }
          window.__combo=powerups.filter(p=>p.kind==='forgecombo')[0]||null; }""")
        pg.wait_for_timeout(1500); step(6)
        pg.evaluate("() => { const P=window.__combo; if(P){ P.y=player.y-150; P.vy=0; } }")
        step(2); shot('10_combo_on_field')

        # the STYLISH award over a live stage
        pg.evaluate("""() => { powerups.length=0; player.roll=null; player._rollCool=0; stylish=null;
          startRoll(1); stylishCheck({x:player.x,y:player.y,vx:0,vy:0,w:8,h:8,kind:'pellet',dead:false});
          stylish.t=0.30; }""")
        step(1); shot('11_stylish_typing_in')
        pg.evaluate("() => { stylish.t=0.75; }"); step(1); shot('12_stylish_held')
        pg.evaluate("() => { stylish.t=1.30; }"); step(1); shot('13_stylish_typing_out')

        # THE ARMORY: one earned row among unearned ones
        pg.evaluate("""() => { achievementState=achievementEmpty(); furiousConvertLevel(1, 3000000);
          forgeComboGrant('fire',0); forgeComboGrant('ice',0);
          for(const e of Object.keys(INFUSIONS)) for(const w of FORGE_WEAPONS) for(let l=1;l<=5;l++) XART.rdy('micon_forge_'+e+'_'+w+(l>1?'_'+l:''));
          if(typeof laserMistWarm==='function') laserMistWarm();
          armoryOpen('vault'); setState(GS.ARMORY); }""")
        pg.wait_for_timeout(1800); step(20); shot('14_armory_boss_drop_rows')

        # THE FORGE: the element strip for a slot with two earned combinations
        pg.evaluate("""() => { setState(GS.PLAY); run.forge={}; run.forgeCombos=2; run.forgeRespecs=2;
          run.weapon=0; forgeLoadoutSync(); forgeStart(function(){}); }""")
        pg.wait_for_timeout(1500); step(60); pg.wait_for_timeout(900); step(60)
        pg.evaluate("() => { if(typeof forge!=='undefined'&&forge){ forge.sel=0; forge.row=1; } }")
        step(20); shot('15_forge_earned_for_slot')
        print('  errors:', len(errs))
        for e in errs[:5]: print('   !', e[:160])
        pg.evaluate("() => { try{ localStorage.removeItem(ACHIEVEMENT_STORE_KEY); }catch(_){} achievementReload(); }")
        br.close()
    stop()

if __name__ == '__main__':
    main()
