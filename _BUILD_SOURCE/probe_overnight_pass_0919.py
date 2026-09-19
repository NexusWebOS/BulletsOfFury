import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import shoot
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1]
port,stop=shoot.serve(str(root))
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(args=['--disable-gpu','--no-sandbox','--mute-audio'])
  page=browser.new_page(viewport={'width':1440,'height':900})
  errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load',timeout=60000)
  page.wait_for_function("typeof ASSETS!=='undefined' && (window.__bofFrames|0)>4",timeout=45000)
  initial=page.evaluate("""() => {achToasts=[];run.mode='campaign';run.stage=1;run.pilot='yuri';run.score=41250;stageStats.shots=2841;stageStats.hits=1794;achToastPush({title:'TEST AWARD',points:10});drawStageClear._init=false;setState(GS.STAGECLEAR);return {bullets:SC_CONCEPT.find(x=>x.k==='BULLETS FIRED').fmt(stageStats),accuracy:SC_CONCEPT.find(x=>x.k==='WEAPON ACCURACY').fmt(stageStats),art:['port_cf_yuri_alert','port_cf_cole_alert','fire_whip_fx_0919','micon_firewhip_0919'].map(k=>!!XART._src[k])};}""")
  page.wait_for_timeout(900)
  page.evaluate("() => {stateT=5;drawStageClear._stamp=1;drawStageClear._pwChars=99;drawStageClear(1/60);}")
  proof=root/'_shots'/'overnight_0919';proof.mkdir(parents=True,exist_ok=True)
  page.screenshot(path=str(proof/'stageclear_debrief.png'))
  held=page.evaluate("() => ({state,t:achToasts[0]&&achToasts[0].t,queue:achToasts.length})")
  page.evaluate("() => {setState(GS.STAGESEL);}")
  page.wait_for_timeout(350)
  released=page.evaluate("() => ({state,t:achToasts[0]&&achToasts[0].t})")
  page.evaluate("() => {for(const k of ['port_cf_yuri_alert','port_cf_cole_alert','fire_whip_fx_0919','micon_firewhip_0919'])XART.rdy(k);}")
  page.wait_for_function("['port_cf_yuri_alert','port_cf_cole_alert','fire_whip_fx_0919','micon_firewhip_0919'].every(k=>XART.rdy(k))",timeout=20000)
  assert initial['bullets']=='2841' and initial['accuracy']=='63%',initial
  assert held['t']==0 and held['queue']>0 and released['t']>0,(held,released)
  assert all(initial['art']) and not errors,(initial,errors)
  print(json.dumps({'metrics':initial,'held':held,'released':released,'errors':errors}))
  browser.close()
finally:stop()
