"""Native stage starts have no automatic special delivery; scheduled crates still work.

--before records the reported delivery. All outputs stay under ignored _shots/.
"""
from pathlib import Path
import json
import sys
import shoot
from playwright.sync_api import sync_playwright

ROOT = Path(shoot.GAME)
BEFORE = '--before' in sys.argv
OUT = ROOT / '_shots' / 'no_opening_special_1018' / ('before' if BEFORE else 'after')

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    port, stop = shoot.serve(str(ROOT))
    checks, errors, cases = [], [], []

    def check(name, passed):
        checks.append(dict(name=name, passed=bool(passed)))
        print(('PASS ' if passed else 'FAIL ') + name, flush=True)

    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(channel='msedge', args=['--mute-audio'])
            page = browser.new_page(viewport=dict(width=1600, height=900))
            page.on('pageerror', lambda e: errors.append(str(e)))
            page.on('console', lambda m: errors.append(m.text) if m.type == 'error' or 'draw error' in m.text else None)
            page.on('response', lambda r: errors.append(str(r.status)+': '+r.url) if r.status >= 400 else None)
            page.goto(f'http://127.0.0.1:{port}/index.html', timeout=120000)
            page.wait_for_function('window.__bofFrames>4', timeout=120000)
            page.evaluate(shoot.TRAP_RAF)
            page.wait_for_timeout(35)
            page.evaluate('playerHit=function(){}')

            def frames(n):
                for i in range(0, n, 24):
                    err = page.evaluate(shoot.STEP, min(24, n-i))
                    if err:
                        errors.append(err)
                    page.wait_for_timeout(5)

            def start(stage, pilot='cole', coop=False):
                r = page.evaluate('''q=>{
                    coopOn=q.coop;pilotIndex=PILOTS.findIndex(p=>p.key===q.pilot);p2Index=PILOTS.findIndex(p=>p.key==='lizzie');
                    run.pilot=q.pilot;run.mode='arcade';diffKey='normal';FS11.events=[];FS11.draws={};
                    startRun(q.stage);
                    // Focus on the first PLAY seconds, after the authored intro/fly-in.
                    BOFCinematicDirector.cancel();story=fb2Talk=s6Opening=null;H3.release=false;AP10_X.intro=null;
                    setState(GS.PLAY);return {stage:run.stage,pending:FS11.pending,boxes:FS11.boxes.length};
                }''', dict(stage=stage, pilot=pilot, coop=coop))
                page.wait_for_function('()=>{stageLoadTick();return stageLoadReady(run.stage)&&bmfReady("game");}', timeout=120000)
                return r

            def snapshot():
                return page.evaluate('''()=>({stage:run.stage,pilot:run.pilot,state,timer:stageTimer,
                    pending:FS11.pending,boxes:FS11.boxes.length,special:special?.pilot||null,
                    openingDraws:FS11.draws.opening||0,events:FS11.events.filter(e=>e.event.startsWith('opening-'))})''')

            pilots = page.evaluate('Object.keys(FS11_UPGRADES)')
            targets = [(1, 'cole', False)] if BEFORE else [(s, 'cole', False) for s in range(1, 10)] + [(1, p, False) for p in pilots if p != 'cole'] + [(1, 'cole', True)]
            for stage, pilot, coop in targets:
                initial = start(stage, pilot, coop)
                frames(150)
                mid = snapshot()
                if stage == 1 or stage == 4:
                    page.screenshot(path=str(OUT / f'stage{stage}_{pilot}_{"coop" if coop else "solo"}.png'))
                frames(330)
                final = snapshot()
                cases.append(dict(initial=initial, midway=mid, final=final, coop=coop))
                label = f'Stage {stage} / {pilot}' + (' / co-op' if coop else '')
                check(label+': no delivery queued at start', initial['pending'] is None and initial['boxes'] == 0)
                check(label+': no opening crate or free ability arrives', not final['events'] and not mid['boxes'] and not final['boxes'] and not mid['special'] and not final['special'])
                check(label+': no opening delivery is rendered', mid['openingDraws'] == 0 and final['openingDraws'] == 0)

            if not BEFORE:
                start(1, 'axel')
                # Retain the native clock and supply scheduler. Isolate it from enemy drops.
                page.evaluate('stagePlan=[];enemies=[];powerups=[]')
                limit = page.evaluate('Math.ceil(curStage.length*.22*60)+90')
                for _ in range(0, limit, 24):
                    frames(24)
                    if page.evaluate('!!_sc1&&powerups.some(p=>p.kind==="scrate"&&!p.dead)'):
                        break
                found = page.evaluate('!!_sc1&&powerups.some(p=>p.kind==="scrate"&&!p.dead)')
                check('The native mid-level scheduler still spawns its ordinary special crate', found)
                if found:
                    page.evaluate('''()=>{const p=powerups.find(p=>p.kind==='scrate'&&!p.dead);
                        p.x=player.x;p.y=player.y-100;p.vy=.7;window.__regularSpecialCrate=p;}''')
                    page.screenshot(path=str(OUT/'regular_crate.png'))
                    page.keyboard.down('j')
                    frames(90)
                    page.keyboard.up('j')
                    check('Actual gunfire breaks the ordinary crate', page.evaluate('!!window.__regularSpecialCrate.dead'))
                    frames(180)
                    page.screenshot(path=str(OUT/'regular_special_collected.png'))
                    check('Collecting the normal drop activates the pilot special', page.evaluate('special?.pilot==="axel"&&special._fs11Level===1'))
                check('The opening queue remains empty after normal pickup collection', page.evaluate('FS11.pending===null&&FS11.boxes.length===0&&!FS11.events.some(e=>e.event.startsWith("opening-"))'))
            check('No page, console, draw or asset errors', not errors)
            browser.close()
    finally:
        stop()
    report = dict(cases=cases, checks=checks, errors=errors, passed=sum(c['passed'] for c in checks), failed=sum(not c['passed'] for c in checks))
    (OUT/'report.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(f"{report['passed']} passed / {report['failed']} failed", flush=True)
    return 0 if BEFORE else int(report['failed'] > 0)

if __name__ == '__main__':
    sys.exit(main())
