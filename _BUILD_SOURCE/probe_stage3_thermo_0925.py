"""Exercise the live Furious Stage 3 atomic handoff in Chromium."""
import base64
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import shoot as sh
from playwright.sync_api import sync_playwright

out = Path('_shots/stage3_thermo_0925')
out.mkdir(parents=True, exist_ok=True)
port, stop = sh.serve(sh.GAME)
errors = []
report = {}
try:
    with sync_playwright() as pw:
        browser = pw.chromium.launch(args=['--disable-gpu', '--no-sandbox', '--mute-audio'])
        page = browser.new_page(viewport={'width': 1100, 'height': 1200})
        page.on('pageerror', lambda e: errors.append(str(e)))
        page.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
        page.goto(f'http://127.0.0.1:{port}/index.html', wait_until='load')
        page.wait_for_function('() => (window.__bofFrames|0)>4')
        page.evaluate(sh.TRAP_RAF)
        page.evaluate(sh.SETUP, {'state': 'PLAY', 'stage': 3, 'pilot': 'cole', 'diff': 'furious', 'invuln': True})
        page.evaluate("() => {diffKey='furious';DIFF=DIFFS.furious;}")
        page.wait_for_function("() => XART.rdy('s3thermo_nuclear_retina') && XART.rdy('s3thermo_thermocloud') && XART.rdy('s3thermo_therno_robonoid')", timeout=30000)
        for role, old_kind, new_kind in [('mini', 'frostcruiser', 'thermocloud'), ('boss', 'cryospear', 'therno')]:
            init = page.evaluate("""([role, kind]) => {
              stagePlan=[];waveIdx=999;spawnClock=9999;enemies=[];eBullets=[];pBullets=[];
              if(role==='mini'){subBoss=null;subBossActive=false;spawnSubBoss__inner(kind);
                subBoss.enter=false;subBoss.t=3;subBoss.x=worldWidth()/2;subBoss.y=subBoss.ty;}
              else {subBoss=null;subBossActive=false;boss=null;bossActive=false;spawnBoss(kind);
                boss.enter=false;boss.t=3;boss.x=worldWidth()/2;boss.y=boss.ty;}
              const b=role==='mini'?subBoss:boss;
              return {stage:run.stage,diff:diffKey,kind:b.kind,name:b.name};
            }""", [role, old_kind])
            samples = []
            for i in range(75):
                sample = page.evaluate("""(role) => {
                  const b=role==='mini'?subBoss:boss;
                  if(b && b.kind!==(role==='mini'?'thermocloud':'therno'))
                    s3ThermoStrikeTick(role,b,.05);
                  const s=S3_THERMO_STRIKE[role],now=role==='mini'?subBoss:boss;
                  return {t:s&&s.t,impact:s&&s.impact,kind:now&&now.kind,name:now&&now.name};
                }""", role)
                if i in (5, 27, 39, 59, 74):
                    err = page.evaluate(sh.STEP, 1)
                    if err:
                        errors.append(err)
                    png = page.evaluate("() => document.querySelector('#screen').toDataURL('image/png')")
                    (out / f'{role}_{i:02}.png').write_bytes(base64.b64decode(png.split(',', 1)[1]))
                    samples.append(sample)
            report[role] = {'init': init, 'samples': samples,
                            'new': page.evaluate("""(role) => {
                              const b=role==='mini'?subBoss:boss;
                              return {kind:b&&b.kind,form:!!(b&&b._s3Thermo),hp:b&&b.hp,
                                bullets:eBullets.length};
                            }""", role)}
            if init['diff'] != 'furious' or report[role]['new']['kind'] != new_kind or not report[role]['new']['form']:
                errors.append(f'{role} handoff failed: {init} -> {report[role]["new"]}')
            page.evaluate("""(role) => {const b=role==='mini'?subBoss:boss;
              b.enter=false;b.x=worldWidth()/2;b.y=b.ty;b.t=0;
              if(role==='mini')subBossActive=true;else bossActive=true;
              eBullets.length=0;stagePlan=[];waveIdx=999;spawnClock=9999;}
            """, role)
            seen = set()
            for i in range(360):
                err = page.evaluate(sh.STEP, 1)
                if err:
                    errors.append(err)
                    break
                if i % 30 == 0:
                    seen.update(page.evaluate('() => eBullets.map(q => q.kind)'))
            report[role]['combat'] = page.evaluate("""(role) => {const b=role==='mini'?subBoss:boss;
              return {kind:b&&b.kind,shots:b&&b._s3Thermo&&b._s3Thermo.shots,
                cycle:b&&b._s3Thermo&&b._s3Thermo.cycle,bullets:eBullets.length};}
            """, role)
            report[role]['combat']['seen'] = sorted(seen)
            png = page.evaluate("() => document.querySelector('#screen').toDataURL('image/png')")
            (out / f'{role}_combat.png').write_bytes(base64.b64decode(png.split(',', 1)[1]))
            if not report[role]['combat']['shots']:
                errors.append(f'{role} emitted no attacks after handoff')
        report['errors'] = errors
        (out / 'report.json').write_text(json.dumps(report, indent=2))
        print(json.dumps(report, indent=2))
        assert not errors
        browser.close()
finally:
    stop()
