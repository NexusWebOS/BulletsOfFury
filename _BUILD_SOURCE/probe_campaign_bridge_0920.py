"""Exercise the Stage-1 Campaign flight bridge in the real Chromium canvas."""
import base64
import json
from pathlib import Path

from playwright.sync_api import sync_playwright
from shoot import serve, STEP, TRAP_RAF

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'_shots/campaign_bridge_0920'
OUT.mkdir(parents=True,exist_ok=True)
port,stop=serve(str(ROOT))
errors=[]
states=[]
try:
  with sync_playwright() as pw:
    browser=pw.chromium.launch(args=['--disable-gpu','--no-sandbox','--mute-audio'])
    page=browser.new_page(viewport={'width':1280,'height':720})
    page.on('pageerror',lambda e:errors.append('page '+str(e)))
    page.on('console',lambda m:errors.append('console '+m.text) if m.type=='error' else None)
    page.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load',timeout=60000)
    page.wait_for_function('() => typeof campaignBridgeStart===\'function\' && (window.__bofFrames|0)>4',timeout=45000)
    page.evaluate(TRAP_RAF)
    for pilot in ['yuri','cole']:
      page.evaluate("p => {run.mode='campaign';run.pilot=p;pilotIndex=PILOTS.findIndex(x=>x.key===p);window.__bridgeDone=0;campaignBridgeStart(()=>{window.__bridgeDone++;setState(GS.CAMPHUB);});}",pilot)
      page.wait_for_function("() => XART.rdy('cinbg_stage1_route') && XART.rdy(cinShipKey(campaignBridge.lead,1)) && XART.rdy(cinShipKey(campaignBridge.wing,1)) && bmfReady('dialogue')",timeout=20000)
      page.evaluate(STEP,80)
      result=page.evaluate("() => ({state,hqMode,lead:campaignBridge&&campaignBridge.lead,wing:campaignBridge&&campaignBridge.wing,i:campaignBridge&&campaignBridge.i,done:window.__bridgeDone,route:XART.rdy('cinbg_stage1_route')})")
      assert result['state']=='cutscene' and result['i']==0 and result['done']==0,result
      assert result['lead']==pilot and result['wing']==('axel' if pilot=='cole' else 'cole'),result
      uri=page.evaluate("() => document.querySelector('#screen').toDataURL('image/png')")
      (OUT/(pilot+'_flight.png')).write_bytes(base64.b64decode(uri.split(',',1)[1]))
      page.evaluate(STEP,710)
      end=page.evaluate("() => ({state,done:window.__bridgeDone,bridge:campaignBridge})")
      assert end['done']==1 and end['bridge'] is None,end
      states.append({'pilot':pilot,'mid':result,'end':end})
    page.evaluate("() => {run.mode='campaign';run.stage=1;run.pilot='yuri';campaign.unlockedMax=1;scLeaveStage({bonus:0,rank:'A'});}")
    routed=page.evaluate("() => ({state,hqMode,lead:campaignBridge&&campaignBridge.lead,unlock:campaign.unlockedMax})")
    assert routed['state']=='cutscene' and routed['hqMode']=='bridge',routed
    page.evaluate(STEP,730)
    after=page.evaluate("() => ({state,bridge:campaignBridge,unlock:campaign.unlockedMax,cine:sselUnlockCine&&sselUnlockCine.stage})")
    assert after['bridge'] is None and after['state']=='stagesel' and after['cine']==2,after
    page.evaluate(STEP,300)
    assert page.evaluate("() => campaign.unlockedMax")>=2
    states.append({'stageClearRoute':routed,'after':after})
    browser.close()
finally:stop()
(OUT/'results.json').write_text(json.dumps({'states':states,'errors':errors},indent=2),encoding='utf-8')
assert not errors,errors[:10]
print('PASS Stage-1 two-ship Campaign bridge, Stage Clear to map routing, and no browser errors')
