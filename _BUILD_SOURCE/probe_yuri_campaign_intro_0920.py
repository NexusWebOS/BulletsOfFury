"""Inspect Yuri's current likeness in the first Campaign cinematic in Chromium."""
import base64
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
from shoot import serve,STEP,TRAP_RAF

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'_shots/yuri_campaign_intro_0920'
OUT.mkdir(parents=True,exist_ok=True)
port,stop=serve(str(ROOT))
errors=[]
results=[]
try:
  with sync_playwright() as pw:
    browser=pw.chromium.launch(args=['--disable-gpu','--no-sandbox','--mute-audio'])
    page=browser.new_page(viewport={'width':1280,'height':720})
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
    page.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load',timeout=60000)
    page.wait_for_function('() => typeof campaignIntroStart===\'function\' && (window.__bofFrames|0)>4',timeout=45000)
    page.evaluate(TRAP_RAF)
    for pilot in ['yuri','cole']:
      page.evaluate("p => {run.mode='campaign';run.pilot=p;pilotIndex=PILOTS.findIndex(x=>x.key===p);campaignIntroPilot=null;campaignIntroStart(()=>setState(GS.CAMPHUB));}",pilot)
      page.wait_for_function("() => campaignIntroReady()",timeout=30000)
      page.evaluate(STEP,650)
      result=page.evaluate("() => ({state,t:campaignIntro&&campaignIntro.t,pilot:campaignIntro&&campaignIntro.pilot,portrait:campaignIntroPortraitKey(campaignIntro.pilot),keys:campaignIntroKeys()})")
      assert result['state']=='campaignintro' and result['t']>10 and result['pilot']==pilot,result
      assert result['portrait']==('yuri_body_0' if pilot=='yuri' else 'pose_cole_0'),result
      assert 'pose_yuri_0' not in result['keys'],result
      if pilot=='yuri':
        assert page.evaluate("() => cutPose('yuri',0,true)")=='yuri_body_0'
      uri=page.evaluate("() => document.querySelector('#screen').toDataURL('image/png')")
      (OUT/(pilot+'_intro.png')).write_bytes(base64.b64decode(uri.split(',',1)[1]))
      results.append(result)
    browser.close()
finally:stop()
(OUT/'results.json').write_text(json.dumps({'results':results,'errors':errors},indent=2),encoding='utf-8')
assert not errors,errors[:10]
print('PASS current Yuri body in Campaign intro; Cole unaffected; no browser errors')
