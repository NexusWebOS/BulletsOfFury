"""probe_warden_helpers.py - backlog item 4, behaviour half.

Mike: "it should no longer get its helpers either."

Two things must BOTH be true, and a probe that only checks the first is worthless:

  1. the Olive Warden never fields a helper drone - none built, never `summoned`, and the 300px
     drone collision reach never opens;
  2. THE WARDEN IS STILL DANGEROUS. Removing a unit's helpers by accidentally disarming the unit
     would look identical to success on a check that only counts drones. So this also records
     rounds fired and mode transitions, and FAILS if the fight goes quiet.

Runs the mini through several full cycles so the 'drones' PHASE is entered (it is kept - it still
carries the Warden's own wall attack; only the helpers are gone).
"""
import os, sys, base64, importlib.util, json, collections

spec = importlib.util.spec_from_file_location("shoot", os.path.abspath('_BUILD_SOURCE/shoot.py'))
sh = importlib.util.module_from_spec(spec); spec.loader.exec_module(sh)
from playwright.sync_api import sync_playwright

OUT = 'docs/proofs/warden_helpers_0905'; os.makedirs(OUT, exist_ok=True)
CAP = "() => { const c=document.getElementById('screen'); return c?c.toDataURL('image/png'):null; }"

port, stop = sh.serve(sh.GAME)
errs = []
with sync_playwright() as p:
    b = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
    pg = b.new_page(viewport={'width': 960, 'height': 1040})
    pg.on('pageerror', lambda e: errs.append(str(e)[:200]))
    pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=120000)
    pg.wait_for_function("() => typeof state!=='undefined' && (window.__bofFrames|0) > 4", timeout=120000)
    pg.evaluate(sh.TRAP_RAF)
    pg.evaluate("() => { ASSETS.ready = true; }")
    pg.evaluate(sh.SETUP, {'state': 'PLAY', 'pilot': 'cole', 'stage': 4, 'invuln': True})
    pg.evaluate("""()=>{ run.stage=4; curStage=STAGES[3]; player.dead=false; player.invuln=1e9;
      stagePlan=[]; enemies.length=0; eBullets.length=0;
      spawnSubBoss('olivewarden'); if(subBoss){ subBoss.enter=false; } }""")

    init = pg.evaluate("()=>{ const S=subBoss&&subBoss._s4war; return {alive:!!subBoss, ship:subBoss&&subBoss._ship,"
                       " mini:S&&S.mini, drones:S?S.drones.length:null, summoned:S?S.summoned:null}; }")
    print('at spawn:', json.dumps(init), flush=True)

    modes = collections.Counter()
    ever_summoned = False
    ever_drones = 0
    ever_reach = False
    rounds = 0
    shots_seen = 0
    for i in range(90):
        pg.evaluate(sh.STEP, 8); pg.wait_for_timeout(45)
        st = pg.evaluate("""()=>{ const S=subBoss&&subBoss._s4war; if(!S) return null;
          const reach=(subBoss._ship==='olivewarden'&&S.summoned)?300:0;
          return {mode:S.mode, summoned:!!S.summoned, drones:S.drones.length, round:S.round,
                  reach:reach, eb:eBullets.length, alive:!(subBoss.dead)}; }""")
        if not st: break
        modes[st['mode']] += 1
        ever_summoned = ever_summoned or st['summoned']
        ever_drones = max(ever_drones, st['drones'])
        ever_reach = ever_reach or bool(st['reach'])
        rounds = max(rounds, st['round'])
        shots_seen = max(shots_seen, st['eb'])
        if i in (20, 50, 80):
            d = pg.evaluate(CAP)
            if d: open(os.path.join(OUT, 'warden_%02d_%s.png' % (i, st['mode'])), 'wb').write(
                base64.b64decode(d.split(',', 1)[1]))

    print('modes entered   :', dict(modes), flush=True)
    print('mode changes    :', rounds, flush=True)
    print('drones ever     :', ever_drones, flush=True)
    print('summoned ever   :', ever_summoned, flush=True)
    print('drone reach ever:', ever_reach, flush=True)
    print('peak eBullets   :', shots_seen, flush=True)
    print('page errors     :', errs[:4] if errs else 'none', flush=True)
    b.close()
stop()

fails = []
if ever_drones != 0:   fails.append('the Warden built %d helper drone(s)' % ever_drones)
if ever_summoned:      fails.append('S.summoned went true - the helper reveal still fires')
if ever_reach:         fails.append('the 300px drone collision reach opened')
if 'drones' not in modes: fails.append('never entered the drones PHASE - the kept beat is gone')
if shots_seen < 8:     fails.append('the Warden fired almost nothing (peak eBullets %d) - '
                                    'helpers removed by disarming the unit' % shots_seen)
if errs:               fails.append('page errors: %s' % errs[:2])
print('\n' + ('PASS - no helpers, and the Warden still fights' if not fails
              else 'FAIL:\n  ' + '\n  '.join(fails)))
sys.exit(1 if fails else 0)
