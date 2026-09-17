#!/usr/bin/env python3
"""
probe_sonic_0917.py - COLE'S SONIC BOOM, the deadly version, measured in real Chromium.

Mike, 0917: "I also need Cole's Sonic Wave/Boom to be upgraded and feel/sound and work like a
deadly sonic sound attack."

What changed and what this checks:
  SOUND  - the dedicated release cue used to be built into a local and NEVER CALLED. Now a full
           charge asks for coleSonicFull and a half charge for coleSonicHalf (both new, both through
           the gated generator). Counted by wrapping weaponFeedbackSound - a source pin cannot
           tell "written" from "played".
  LOOK   - the wavefront is the Razorback's authored pressure arc, rzb_sonic_wave, rotated to lead
           upward, and a release ring (rzb_sonic_ring) grows off the hull. Identified by KEY
           through a wrapped XART.get (XART.get returns a canvas with no .src).
  WORK   - SONIC_DMG 7 -> 11 (a full charge is 26), and the wave SHOVES ordinary hulls back up the
           screen. Measured on a real drone: its y before and after the wave passes.

⚠ A proof frame is taken INSIDE the run while the wave is in flight - a frame after the run shows
nothing and reads as "never drawn" (0916's escape-arrow lesson).
"""
import os, sys, base64, json
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
sys.path.insert(0, os.path.join(ROOT, '_BUILD_SOURCE'))
import shoot as sh
from playwright.sync_api import sync_playwright

OUT = os.path.join(ROOT, 'docs', 'proofs', 'sonic_0917')
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
        pg.wait_for_function("() => typeof setState==='function' && typeof sonicRelease==='function'", timeout=60000)
        pg.wait_for_function("() => (window.__bofFrames|0) > 4", timeout=60000)
        pg.evaluate(sh.TRAP_RAF)
        pg.evaluate(sh.SETUP, {'state': 'PLAY', 'stage': 1, 'pilot': 'cole'})
        pg.evaluate("() => { window.__step=%s; window.playerHit=function(){}; run.lives=9; enemies.length=0; mapScroll=2400; }" % sh.STEP)
        pg.evaluate("() => { XART.rdy('rzb_sonic_wave'); XART.rdy('rzb_sonic_ring'); for(let i=0;i<4;i++){ XART.rdy('nsw_dist_'+i); XART.rdy('nsw_circ_'+i); } XART.rdy('nsw_ring_3'); }")
        for _ in range(6):
            pg.evaluate("() => window.__step(8)"); pg.wait_for_timeout(420)
        # traps: sounds asked for, art keys asked for
        pg.evaluate("""() => {
          window.__snd = {}; const f = weaponFeedbackSound;
          weaponFeedbackSound = function(name, vol){ window.__snd[name]=(window.__snd[name]|0)+1; return f.apply(this, arguments); };
          window.__keys = {}; const g = XART.get.bind(XART);
          XART.get = function(k){ if(/rzb_sonic|nsw_/.test(String(k))) window.__keys[k]=(window.__keys[k]|0)+1; return g(k); };
        }""")
        ok(pg.evaluate("() => XART.rdy('rzb_sonic_wave') && XART.rdy('rzb_sonic_ring')"), 'the Razorback sonic wave and ring plates are registered and decoded')
        ok(pg.evaluate("() => SONIC_DMG===11"), 'SONIC_DMG is 11 (a full charge is 26, a tap 7)')
        ok(pg.evaluate("() => !!(BOFA&&BOFA.sfx&&/cole_sonic_full/.test(String(BOFA.sfx.coleSonicFull||'')))&&!!(BOFA.sfx.coleSonicHalf)"),
           'coleSonicFull / coleSonicHalf are registered in the code-owned sound block')

        # a target column above the ship: drones that do not move on their own
        pg.evaluate("""() => {
          window.__targets = [];
          for(let i=0;i<3;i++){ const e=spawnEnemy('drone',{x:worldWidth()*0.5, y:120+i*70}); if(!e) continue;
            e.x=worldWidth()*0.5; e.y=120+i*70; e.vx=0; e.vy=0; e.shoots=false; e.hp=60; e.maxhp=60; e.dropOk=false; window.__targets.push(e); }
          player.x=worldWidth()*0.5; player.y=400; player.dead=false;
        }""")
        ys0 = pg.evaluate("() => window.__targets.map(e=>e.y)")
        hp0 = pg.evaluate("() => window.__targets.map(e=>e.hp)")

        # ---- a FULL release, fired through the real release function ----
        pg.evaluate("() => { window.__snd={}; window.__keys={}; sonicRelease(1.0); }")
        seen_wave = 0; seen_ring = 0; shot_taken = False
        for i in range(40):
            pg.evaluate("() => window.__step(1)")
            k = pg.evaluate("() => window.__keys")
            seen_wave = max(seen_wave, k.get('rzb_sonic_wave', 0)); seen_ring = max(seen_ring, k.get('rzb_sonic_ring', 0))
            if i == 8 and not shot_taken:
                d = pg.evaluate("() => { const c=document.getElementById('screen'); return c?c.toDataURL('image/png'):null; }")
                if d: open(os.path.join(OUT, 'sonic_full_in_flight.png'), 'wb').write(base64.b64decode(d.split(',', 1)[1])); shot_taken = True
        snd = pg.evaluate("() => window.__snd")
        print('  sounds asked:', json.dumps(snd), '| wave blits', seen_wave, '| ring blits', seen_ring)
        ok(snd.get('coleSonicFull', 0) >= 1, 'a FULL release asks for coleSonicFull (the cue that was never called before)')
        ok(snd.get('colePressureRelease', 0) >= 1, 'and still plays the pressure-release feedback under it')
        ok(seen_wave >= 5, 'the wavefront is drawn with rzb_sonic_wave, by KEY (%d blits)' % seen_wave)
        ok(seen_ring >= 3, 'the release ring is drawn with rzb_sonic_ring (%d blits)' % seen_ring)
        ys1 = pg.evaluate("() => window.__targets.map(e=>e.y)")
        hp1 = pg.evaluate("() => window.__targets.map(e=>e.hp)")
        hit = [i for i in range(len(hp0)) if hp1[i] < hp0[i]]
        print('  targets y', ys0, '->', ys1, '| hp', hp0, '->', hp1)
        ok(len(hit) >= 2, 'the wave PIERCES the column - %d of 3 drones took damage' % len(hit))
        ok(all(hp0[i] - hp1[i] >= 20 for i in hit), 'each took the full-charge hit (26 against 60 hp, after the ENG-05 floor)')
        ok(all(ys1[i] < ys0[i] - 10 for i in hit), 'and each hit drone was SHOVED back up the screen (dy %s)' % [round(ys1[i] - ys0[i], 1) for i in hit])

        # ---- a HALF release asks for the half cue ----
        pg.evaluate("() => { for(const b of pBullets) b.dead=true; pBullets.length=0; window.__snd={}; sonicRelease(0.4); }")
        pg.evaluate("() => window.__step(3)")
        snd2 = pg.evaluate("() => window.__snd")
        ok(snd2.get('coleSonicHalf', 0) >= 1 and not snd2.get('coleSonicFull', 0), 'a HALF release asks for coleSonicHalf, not the full cue')

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
