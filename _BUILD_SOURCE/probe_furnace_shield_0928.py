#!/usr/bin/env python3
"""probe_furnace_shield_0928.py - can the pilot's own gun break the Stage-2 Furnace Tyrant's fire shield?

Found by probe_sustained_0928 (Normal, Freezer): the SHIELD bar stayed full for a 2:46 fight. This
separates the bot from the game: the pilot is parked under the boss at fixed ranges, FIRE is held
through the real input path, and the shield / hull pools are read every second.
  python3 _BUILD_SOURCE/probe_furnace_shield_0928.py
"""
import os, sys, json, http.server
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
http.server.SimpleHTTPRequestHandler.log_message = lambda *a: None
import shoot as sh
from playwright.sync_api import sync_playwright

SETUP = r"""
(c) => {
  diffKey = c.diff; DIFF = DIFFS[c.diff]; run.mode = 'campaign'; run.pilot = c.pilot; run.stage = 2;
  curStage = STAGES[1]; beginStage(2); setState(GS.PLAY); player.reset();
  if (c.weapon != null) { run.weapon = c.weapon; run.wlevel = c.level || 1; }
  story = null; stagePlan = []; waveIdx = 999; spawnClock = 9999; enemies = []; eBullets = []; subBossDone = true;
  window.playerHit = function(){};
  spawnBoss('infernoreaver');
  return {kind: boss && boss.kind, weapon: run.weapon, wlevel: run.wlevel, pilot: run.pilot};
}
"""
READ = r"""() => { const H = boss && boss._mwBarrier; return {t: +(boss.t||0).toFixed(1), enter: !!boss.enter,
  shield: H ? Math.round(H.hp) : null, shieldMax: H ? H.maxhp : null, active: H ? H.active : null, hp: Math.round(boss.hp), maxhp: boss.maxhp,
  phase: boss._fz && boss._fz.phase, weapon: run.weapon, wlevel: run.wlevel, pb: pBullets.length,
  bx: Math.round(boss.x), by: Math.round(boss._drawY != null ? boss._drawY : boss.y)}; }"""

def main():
    port, stop = sh.serve(sh.GAME)
    out = []
    cases = [('freezer', None, None), ('freezer', 4, 1), ('maverick', None, None), ('maverick', 0, 3)]
    with sync_playwright() as pw:
        br = pw.chromium.launch(args=['--no-sandbox', '--mute-audio'])
        for pilot, weapon, level in cases:
            for dist in (120, 220, 320):
                pg = br.new_page(viewport={'width': 1000, 'height': 1100})
                errs = []
                pg.on('pageerror', lambda e: errs.append(str(e)))
                pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=120000)
                pg.wait_for_function("() => (window.__bofFrames|0)>4", timeout=120000)
                pg.evaluate(sh.TRAP_RAF)
                info = pg.evaluate(SETUP, {'diff': 'normal', 'pilot': pilot, 'weapon': weapon, 'level': level})
                # let the assembly finish arriving, with real pauses so the plates decode
                for _ in range(20):
                    pg.evaluate(sh.STEP, 30); pg.wait_for_timeout(40)
                    if not pg.evaluate("() => !!boss.enter"): break
                pg.evaluate("(d) => { window.__apd = d; window.__qaTick = () => { const by = boss._drawY != null ? boss._drawY : boss.y;"
                            " player.x = boss.x; player.y = Math.min(PLAY.y + PLAY.h - 8, by + d); Input.keys.j = true; }; }", dist)
                s0 = pg.evaluate(READ)
                samples = [s0]
                for sec in range(12):
                    pg.evaluate(sh.STEP, 60); pg.wait_for_timeout(30)
                    samples.append(pg.evaluate(READ))
                s1 = samples[-1]
                row = {'pilot': pilot, 'weaponAsked': weapon, 'dist': dist, 'setup': info,
                       'shield0': s0['shield'], 'shield1': s1['shield'], 'shieldMax': s0['shieldMax'], 'shieldActive1': s1['active'],
                       'hp0': s0['hp'], 'hp1': s1['hp'], 'maxhp': s0['maxhp'], 'weapon': s1['weapon'], 'errs': errs[:3],
                       'trace': [(q['shield'], q['hp'], q['active']) for q in samples]}
                out.append(row)
                print('%-8s w=%s lv=%s d=%3d  shield %s->%s/%s (active %s)  hp %s->%s/%s  errs %d' % (pilot, s1['weapon'], s1['wlevel'], dist,
                      s0['shield'], s1['shield'], s0['shieldMax'], s1['active'], s0['hp'], s1['hp'], s0['maxhp'], len(errs)), flush=True)
                pg.close()
        br.close()
    stop()
    os.makedirs(os.path.join(sh.GAME, '_shots', 'opus0928'), exist_ok=True)
    json.dump(out, open(os.path.join(sh.GAME, '_shots', 'opus0928', 'furnace_shield.json'), 'w'), indent=1)

if __name__ == '__main__':
    main()
