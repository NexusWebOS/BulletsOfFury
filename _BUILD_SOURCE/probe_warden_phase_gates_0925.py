"""Follow the Stage 7 Warden intro and damage-gated phases in Chromium."""
import base64
import json
from pathlib import Path

import shoot as sh
from playwright.sync_api import sync_playwright

out = Path('_shots/warden_phase_gates_0925')
out.mkdir(parents=True, exist_ok=True)
port, stop = sh.serve(sh.GAME)
errors = []
rows = []
try:
    with sync_playwright() as pw:
        browser = pw.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
        page = browser.new_page(viewport={'width': 1100, 'height': 1200})
        page.on('pageerror', lambda e: errors.append(str(e)))
        page.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
        page.goto(f'http://127.0.0.1:{port}/index.html', wait_until='load')
        page.wait_for_function('() => (window.__bofFrames|0)>4')
        page.evaluate(sh.TRAP_RAF)
        page.evaluate(sh.SETUP, {'state': 'PLAY', 'stage': 7, 'pilot': 'cole', 'invuln': True})
        page.evaluate("""() => {s7Opening=null;stagePlan=[];waveIdx=999;
          _adaptiveSpawnT=999;spawnClock=9999;enemies=[];eBullets=[];pBullets=[];
          boss=null;bossActive=false;spawnBoss(curStage.boss);boss._scene=null;
          player.invuln=1e9;}""")

        def snapshot(label, image=False):
            row = page.evaluate("""() => {
              const S=boss&&boss._s7warden,F=S&&S.final;
              return {phase:F&&F.phase,mode:S&&S.mode,plants:S&&S.plants||0,
                hp:boss&&boss.hp,maxhp:boss&&boss.maxhp,
                cores:F&&F.cores.map(q=>({hp:q.hp,dead:q.dead})),
                rail:!!(F&&F.crippleRail),bullets:eBullets.length,
                hidden:!!(F&&F.bossHidden)};
            }""")
            row['label'] = label
            rows.append(row)
            if image:
                raw = page.evaluate("() => document.querySelector('#screen').toDataURL('image/png')")
                (out / f'{label}.png').write_bytes(base64.b64decode(raw.split(',', 1)[1]))
            return row

        for sec in range(1, 19):
            err = page.evaluate(sh.STEP, 60)
            if err: errors.append(f'intro second {sec}: {err}')
            row = snapshot(f'intro_{sec:02}', sec in (3, 8, 13))
            if row['phase'] == 'fight' and sec >= 11: break
        assert rows[-1]['phase'] == 'fight', rows[-1]
        assert rows[-1]['plants'] > 0, rows[-1]

        page.evaluate("""() => {boss.hp=boss.maxhp*.76;
          s7WardenHit(boss,boss.maxhp*.02,boss.x,boss.y);}""")
        stun = snapshot('stun', True)
        page.evaluate("""() => {const c=boss._s7warden.final.cores[0],p=s7WardenCorePos(boss,c.side);
          s7WardenHit(boss,c.hp*3,p.x,p.y);
          if(!c.dead)s7WardenHit(boss,c.hp*3,p.x,p.y);}""")
        core = snapshot('core_break', True)
        err = page.evaluate(sh.STEP, 240)
        if err: errors.append(f'stun recovery: {err}')
        recovered = snapshot('recovered')

        page.evaluate("""() => {boss.hp=boss.maxhp*.52;
          s7WardenHit(boss,boss.maxhp*.03,boss.x,boss.y);}""")
        hyper = snapshot('hyper', True)
        err = page.evaluate(sh.STEP, 120)
        if err: errors.append(f'hyper recovery: {err}')
        snapshot('hyper_recovered')

        page.evaluate("""() => {boss.hp=boss.maxhp*.27;
          s7WardenHit(boss,boss.maxhp*.03,boss.x,boss.y);}""")
        leg = snapshot('leg_burst', True)
        err = page.evaluate(sh.STEP, 130)
        if err: errors.append(f'cripple entry: {err}')
        cripple = snapshot('cripple', True)
        err = page.evaluate(sh.STEP, 90)
        if err: errors.append(f'cripple attack: {err}')
        snapshot('cripple_rail', True)

        page.evaluate("""() => {s7WardenHit(boss,boss.hp+10,boss.x,boss.y);}""")
        defeat = snapshot('defeat', True)
        err = page.evaluate(sh.STEP, 210)
        if err: errors.append(f'escape entry: {err}')
        escape = snapshot('escape', True)
        browser.close()
finally:
    stop()

report = {'rows': rows, 'errors': errors}
(out / 'report.json').write_text(json.dumps(report, indent=2))
print(json.dumps({'checkpoints': [stun, core, recovered, hyper, leg, cripple,
                                    defeat, escape], 'errors': errors}, indent=2))
assert not errors
assert stun['phase'] == 'stun'
assert core['cores'][0]['dead']
assert recovered['phase'] == 'fight'
assert hyper['phase'] == 'hyper'
assert leg['phase'] == 'legBurst'
assert cripple['phase'] == 'cripple'
assert defeat['phase'] == 'defeat'
assert escape['phase'] == 'escape'
