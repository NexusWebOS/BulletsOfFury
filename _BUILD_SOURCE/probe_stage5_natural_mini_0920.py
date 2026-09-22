"""Reach the Stage-5 Chaos Harrier through ordinary stage progression in Chromium."""
import base64
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
from shoot import serve,SETUP,STEP,TRAP_RAF

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'_shots/stage5_natural_mini_0920'
OUT.mkdir(parents=True,exist_ok=True)
port,stop=serve(str(ROOT))
errors=[]
states=[]
try:
  with sync_playwright() as pw:
    browser=pw.chromium.launch(args=['--disable-gpu','--no-sandbox','--mute-audio'])
    page=browser.new_page(viewport={'width':1100,'height':1200})
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
    page.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load',timeout=60000)
    page.wait_for_function('() => (window.__bofFrames|0)>4',timeout=45000)
    page.evaluate(TRAP_RAF)
    assert page.evaluate(SETUP,{'state':'PLAY','stage':5,'pilot':'cole','invuln':True})['ok']
    active=None
    for i in range(140):
      result=page.evaluate(STEP,30)
      assert result is None,result
      state=page.evaluate("() => ({state,stageTimer,mapScroll,subBossTriggered,subBossActive,kind:subBoss&&subBoss.kind,waves:waveIdx,enemies:enemies.length,environment:enemies.filter(e=>e._environmentBody).length,rocks:l5Rocks.length})")
      if i%20==0 or state['subBossTriggered']:states.append(state)
      if state['subBossActive']:
        active=state
        break
    assert active and active['kind']=='chaosharrier',states[-5:]
    assert active['enemies']==active['environment'],active
    page.wait_for_timeout(200)
    page.evaluate(STEP,50)
    after=page.evaluate("() => ({state,stageTimer,mapScroll,subBossTriggered,subBossActive,kind:subBoss&&subBoss.kind,waves:waveIdx,enemies:enemies.length,environment:enemies.filter(e=>e._environmentBody).length,rocks:l5Rocks.length})")
    assert after['enemies']==after['environment'],after
    uri=page.evaluate("() => document.querySelector('#screen').toDataURL('image/png')")
    (OUT/'natural_spawn.png').write_bytes(base64.b64decode(uri.split(',',1)[1]))
    browser.close()
finally:stop()
(OUT/'results.json').write_text(json.dumps({'states':states,'active':active,'after':after,'errors':errors},indent=2),encoding='utf-8')
assert not errors,errors[:10]
print('PASS Stage-5 Chaos Harrier naturally spawned from normal progression',active,after)
