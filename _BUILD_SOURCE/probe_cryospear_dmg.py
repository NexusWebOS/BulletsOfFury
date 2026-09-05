"""probe_cryospear_dmg.py - does the CRYO SPEAR actually swap plates at 62% and 30%?

Drives the real game in real Chromium and asks the only question that matters: which art key did
the DRAW ask for at each health band. Not "is the file registered", not "does the table have a
dmg array" - both of those can be true while the fight opens on the intact hull forever.

Three traps this is built around, all from CLAUDE.md:

  * `XART.get(k)` RETURNS A CANVAS, NOT AN Image, so it has no `.src`. Identify a blit by wrapping
    XART.get and recording the KEY, never by reading im.src (that measures zero on working code).
  * `XART.rdy(k)` IS FALSE ON ITS FIRST CALL - that call starts the lazy load. And shipBossDraw
    reads `if(_dk && XART.rdy(_dk)) _hk=_dk;`, so an unready plate SILENTLY keeps the intact hull.
    A one-shot check would report a working swap as broken. Poll against real elapsed time.
  * A probe that steps loop() WITHOUT TRAP_RAF spawns a new live rAF chain every frame.
"""
import os, sys, base64, importlib.util, json

spec = importlib.util.spec_from_file_location("shoot", os.path.abspath('_BUILD_SOURCE/shoot.py'))
sh = importlib.util.module_from_spec(spec); spec.loader.exec_module(sh)
from playwright.sync_api import sync_playwright

OUT = 'docs/proofs/cryospear_dmg_0905'; os.makedirs(OUT, exist_ok=True)
CAP = "() => { const c=document.getElementById('screen'); return c?c.toDataURL('image/png'):null; }"

HOOK = """() => {
  window.__keys = [];
  const o = XART.get.bind(XART);
  XART.get = function(k){ if(typeof k==='string') window.__keys.push(k); return o(k); };
  return true;
}"""

BANDS = [
    (1.00, 'nsb_cryo_spear',          'intact  (above 62%)'),
    (0.50, 'nsb_cryo_spear_damaged',  'damaged (62% and below)'),
    (0.20, 'nsb_cryo_spear_critical', 'critical (30% and below)'),
]

port, stop = sh.serve(sh.GAME)
errs = []
fails = []
with sync_playwright() as p:
    b = p.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
    pg = b.new_page(viewport={'width': 960, 'height': 1040})
    pg.on('pageerror', lambda e: errs.append(str(e)[:200]))
    pg.on('console', lambda m: errs.append('console:' + m.text[:160]) if m.type == 'error' else None)
    pg.goto('http://127.0.0.1:%d/index.html' % port, wait_until='load', timeout=120000)
    pg.wait_for_function("() => typeof state!=='undefined' && (window.__bofFrames|0) > 4", timeout=120000)
    pg.evaluate(sh.TRAP_RAF)          # without this every manual frame spawns another live rAF chain
    pg.evaluate("() => { ASSETS.ready = true; }")
    pg.evaluate(sh.SETUP, {'state': 'PLAY', 'pilot': 'cole', 'stage': 3, 'invuln': True})
    pg.evaluate("""()=>{ run.stage=3; curStage=STAGES[2]; player.dead=false; player.invuln=1e9;
      stagePlan=[]; enemies.length=0; eBullets.length=0;
      spawnSubBoss('rimewall'); if(subBoss){ subBoss.enter=false; subBoss.x=240; subBoss.y=150; } }""")

    info = pg.evaluate("()=>{ const D=SHIPBOSS.rimewall; return {alive:!!subBoss, hp:subBoss&&subBoss.hp,"
                       " maxhp:subBoss&&subBoss.maxhp, key:D.key, dmg:D.dmg||null}; }")
    print('spawned:', json.dumps(info), flush=True)
    if not info['alive']:
        raise SystemExit('FAIL: rimewall did not spawn')
    if not info['dmg']:
        raise SystemExit('FAIL: SHIPBOSS.rimewall carries no dmg array')

    # ---- poll readiness against REAL time; rdy() is false on its first call ---------------------
    ready = False
    for i in range(60):
        pg.evaluate(sh.STEP, 4); pg.wait_for_timeout(120)
        r = pg.evaluate("()=>({d:XART.rdy('nsb_cryo_spear_damaged'),c:XART.rdy('nsb_cryo_spear_critical'),"
                        "i:XART.rdy('nsb_cryo_spear')})")
        if r['d'] and r['c'] and r['i']:
            ready = True
            print('all three plates decoded after %d polls (%.1fs real)' % (i + 1, (i + 1) * 0.12), flush=True)
            break
    if not ready:
        print('!! plates never became ready:', r, flush=True)
        fails.append('readiness')

    # ---- drive each health band and record what the DRAW asked for -----------------------------
    for frac, expect, label in BANDS:
        pg.evaluate(sh.STEP, 2); pg.wait_for_timeout(40)
        pg.evaluate("(f)=>{ subBoss.hp = subBoss.maxhp*f; }", frac)
        pg.evaluate(HOOK)                       # fresh recorder for this band
        pg.evaluate(sh.STEP, 3); pg.wait_for_timeout(90)
        keys = pg.evaluate("()=>window.__keys") or []
        hull = [k for k in keys if k.startswith('nsb_cryo_spear')]
        got = hull[0] if hull else None
        ok = (got == expect)
        if not ok: fails.append('%s: expected %s, draw asked %s' % (label, expect, got))
        print('%-26s hp=%.2f  draw asked: %-28s %s' % (label, frac, got, 'OK' if ok else '<<< WRONG'), flush=True)
        d = pg.evaluate(CAP)
        if d:
            open(os.path.join(OUT, 'band_%02d_%s.png' % (int(frac * 100), expect)), 'wb').write(
                base64.b64decode(d.split(',', 1)[1]))

    print('\npage errors:', errs[:5] if errs else 'none', flush=True)
    b.close()
stop()

print('\n' + ('PASS - the Cryo Spear swaps plates at both thresholds' if not fails
              else 'FAIL:\n  ' + '\n  '.join(fails)))
sys.exit(1 if fails else 0)
