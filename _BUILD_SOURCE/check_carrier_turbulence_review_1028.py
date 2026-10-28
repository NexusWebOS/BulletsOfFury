from pathlib import Path
import json
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];O=R/'_shots/carrier_turbulence_1028';errors=[];checks={}
with sync_playwright()as pw:
 b=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1280,'height':900})
 p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None)
 p.on('response',lambda r:errors.append(str(r.status)+' '+r.url)if r.status>=400 else None)
 p.goto('http://127.0.0.1:8795/docs/previews/carrier_turbulence_1028/index.html',wait_until='load',timeout=60000)
 p.wait_for_function('v.readyState>=2',timeout=60000)
 checks['completeFilmLoaded']=p.evaluate('v.duration>100&&v.videoWidth===1280&&v.videoHeight===800')
 checks['allDecodedStillsLoaded']=p.evaluate("[...document.querySelectorAll('.shots img')].every(i=>i.complete&&i.naturalWidth===1280)")
 p.evaluate('()=>{v.muted=true;return v.play()}');p.wait_for_timeout(650);start=p.evaluate('v.currentTime');p.wait_for_timeout(650);checks['nativeControlsPlayVideo']=p.evaluate('v.currentTime')>start
 chapters=[]
 buttons=p.locator('[data-time]')
 for i in range(buttons.count()):
  btn=buttons.nth(i);at=float(btn.get_attribute('data-time'));label=btn.inner_text();btn.click();p.wait_for_function('t=>v.readyState>=2&&Math.abs(v.currentTime-t)<.7',arg=at,timeout=15000)
  chapters.append(dict(label=label,requested=at,time=p.evaluate('v.currentTime')))
 checks['allSixChaptersSeek']=len(chapters)==6
 p.locator('[data-time]').nth(1).click();p.wait_for_timeout(200);p.evaluate('v.pause()');p.screenshot(path=str(O/'review-desktop.png'),full_page=True)
 checks['desktopFits']=p.evaluate('document.documentElement.scrollWidth<=innerWidth')
 p.set_viewport_size({'width':480,'height':900});p.screenshot(path=str(O/'review-mobile.png'),full_page=True)
 checks['mobileFits']=p.evaluate('document.documentElement.scrollWidth<=innerWidth')
 checks['noVideoError']=p.evaluate('v.error===null');checks['noBrowserErrors']=not errors
 b.close()
result=dict(checks=checks,chapters=chapters,errors=errors);(O/'playback.json').write_text(json.dumps(result,indent=2))
q=R/'docs/qa/carrier_turbulence_1028.json';qa=json.loads(q.read_text());qa['playback']=result;q.write_text(json.dumps(qa,indent=2))
print(json.dumps(result,indent=2));raise SystemExit(0 if all(checks.values())else 1)
