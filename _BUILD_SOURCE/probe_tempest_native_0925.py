"""Real Chromium smoke test of the campaign Tempest duo and independent gates."""
import base64
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
import shoot as sh
from playwright.sync_api import sync_playwright

out = Path('_shots/tempest_native_0925')
out.mkdir(parents=True, exist_ok=True)
port, stop = sh.serve(sh.GAME)
errors = []
try:
    with sync_playwright() as pw:
        br = pw.chromium.launch(args=['--disable-gpu','--no-sandbox','--mute-audio'])
        pg = br.new_page(viewport={'width':1100,'height':1200})
        pg.on('pageerror', lambda e: errors.append(str(e)))
        pg.on('console', lambda m: errors.append(m.text) if m.type=='error' else None)
        pg.goto(f'http://127.0.0.1:{port}/index.html', wait_until='load')
        pg.wait_for_function("() => (window.__bofFrames|0)>4")
        pg.evaluate(sh.TRAP_RAF)
        pg.evaluate(sh.SETUP, {'state':'PLAY','stage':6,'pilot':'cole','invuln':True})
        pg.evaluate("""() => {s6Opening=null;stagePlan=[];waveIdx=999;_adaptiveSpawnT=999;
            spawnClock=9999;enemies=[];eBullets=[];pBullets=[];subBoss=null;
            subBossActive=false;subBossDone=false;spawnSubBoss('tempestbrothers');
            subBoss._scene=null;}""")
        for n in range(24):
            err=pg.evaluate(sh.STEP,30)
            if err: raise RuntimeError(err)
            if n%4==0:pg.wait_for_timeout(25)
        state1=pg.evaluate("""() => {const D=subBoss._tempestDuo;return {hp:subBoss.hp,
            ships:D.ships.map(p=>({phase:p._ai.phase,state:p._ai.state,
            x:p.x,y:p.y,vulnerable:p._tlv.vuln})),shots:eBullets.length};}""")
        png=pg.evaluate("() => document.querySelector('#screen').toDataURL('image/png')")
        (out/'combat.png').write_bytes(base64.b64decode(png.split(',',1)[1]))
        state2=pg.evaluate("""() => {const b=subBoss,D=b._tempestDuo,p=D.ships[0];
            D.ai.black.enter('chase');D.ai.black.vulnerable=true;
            tempestBrothersSync(b);hitSubBoss(b.maxhp*10,p.x,p.y);
            return {black:D.ai.black.hp,gray:D.ai.gray.hp,phase:D.ai.black.phase,
                fraction:b.hp/b.maxhp};}""")
        for n in range(8):
            err=pg.evaluate(sh.STEP,30)
            if err: raise RuntimeError(err)
        state3=pg.evaluate("""() => {const D=subBoss._tempestDuo;return {
            black:D.ai.black.phase,gray:D.ai.gray.phase,
            motions:D.ships.map(p=>({x:p.x,y:p.y,dead:p.dead}))};}""")
        png=pg.evaluate("() => document.querySelector('#screen').toDataURL('image/png')")
        (out/'gate.png').write_bytes(base64.b64decode(png.split(',',1)[1]))
        report={'combat':state1,'gate':state2,'after':state3,'errors':errors}
        (out/'report.json').write_text(json.dumps(report,indent=2))
        print(json.dumps(report,indent=2))
        assert not errors
        assert state1['ships'][0]['phase']!='arrival'
        assert state2['black']==6000 and state2['gray']==8000
        assert state2['phase']=='overtake'
        br.close()
finally:
    stop()
