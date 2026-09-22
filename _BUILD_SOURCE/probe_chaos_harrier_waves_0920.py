"""Stage 5 Harrier warning/fight suspends queued waves without stalling the encounter."""
from pathlib import Path
from playwright.sync_api import sync_playwright
from shoot import serve, SETUP, STEP, TRAP_RAF

ROOT=Path(__file__).resolve().parents[1]
port,stop=serve(str(ROOT))
errors=[]
try:
    with sync_playwright() as pw:
        browser=pw.chromium.launch(args=['--disable-gpu','--no-sandbox','--mute-audio'])
        page=browser.new_page(viewport={'width':1100,'height':1200})
        page.on('pageerror',lambda e:errors.append(str(e)))
        page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
        page.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load',timeout=60000)
        page.wait_for_function("() => typeof ASSETS !== 'undefined' && (window.__bofFrames|0)>4",timeout=45000)
        page.evaluate(TRAP_RAF)
        assert page.evaluate(SETUP,{'state':'PLAY','stage':5,'pilot':'cole','invuln':True})['ok']
        page.evaluate((ROOT/'_BUILD_SOURCE/scenario_chaosharrier.js').read_text())
        lanes=page.evaluate("""() => {const out=[];for(const kind of ['crate','capsule','mcrate']){spawnContainer(kind);const p=powerups[powerups.length-1];out.push({kind,x:p.x,dist:Math.abs(p.x-subBoss.x)});}powerups.length=0;return {out,min:subBoss.w*.5+38};}""")
        assert all(row['dist']>=lanes['min'] for row in lanes['out']),lanes
        init=page.evaluate("""() => {waveIdx=0;_waveGap=0;stageTimer=70;l5Rocks.length=0;l5RockT=0;return {waveIdx,stageTimer,waveTime:stagePlan[0].t};}""")
        assert init['stageTimer']>init['waveTime'],init
        page.evaluate(STEP,60)
        held=page.evaluate("""() => ({waveIdx,active:subBossActive,stageTimer,enemies:enemies.length,rocks:l5Rocks.length})""")
        assert held['waveIdx']==0 and held['active'] and held['rocks']==0 and held['enemies']==0,held
        page.evaluate("""() => {subBossActive=false;subBossDone=true;subBoss=null;_waveGap=0;enemies.length=0;}""")
        page.evaluate(STEP,2)
        resumed=page.evaluate("""() => ({waveIdx,stageTimer,enemies:enemies.length,rocks:l5Rocks.length,comets:enemies.filter(e=>/^comet/.test(e.type||'')).length})""")
        assert resumed['waveIdx']>0 and resumed['rocks']+resumed['comets']>=1,resumed
        browser.close()
finally:
    stop()
print({'pickupLanes':lanes,'initial':init,'held':held,'resumed':resumed,'errors':errors})
assert not errors,errors[:8]
print('PASS Stage 5 miniboss holds and resumes field waves in Chromium')
