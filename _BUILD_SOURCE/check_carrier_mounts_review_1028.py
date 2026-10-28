from pathlib import Path
import json
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];O=R/'_shots/carrier_mounts_1028';errors=[];checks={}
with sync_playwright()as pw:
 b=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1280,'height':900})
 p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None);p.on('response',lambda r:errors.append(str(r.status)+' '+r.url)if r.status>=400 else None)
 p.goto('http://127.0.0.1:8795/docs/previews/carrier_mounts_1028/index.html',wait_until='load');p.wait_for_function('v.readyState>=2',timeout=60000)
 checks['nativeFilmLoaded']=p.evaluate('v.duration>7.4&&v.videoWidth===1280&&v.videoHeight===800')
 checks['bothNativeStillsLoaded']=p.evaluate("[...document.querySelectorAll('.shots img')].every(i=>i.complete&&i.naturalWidth===1280)")
 p.evaluate('()=>{v.muted=true;return v.play()}');p.wait_for_timeout(500);start=p.evaluate('v.currentTime');p.wait_for_timeout(500);checks['playbackAdvances']=p.evaluate('v.currentTime')>start
 p.evaluate('v.currentTime=6.3');p.wait_for_function('Math.abs(v.currentTime-6.3)<.4&&v.readyState>=2');checks['seekToLastVolley']=True
 p.evaluate('v.pause()');p.screenshot(path=str(O/'review-desktop.png'),full_page=True);checks['desktopFits']=p.evaluate('document.documentElement.scrollWidth<=innerWidth')
 p.set_viewport_size({'width':480,'height':900});p.screenshot(path=str(O/'review-mobile.png'),full_page=True);checks['mobileFits']=p.evaluate('document.documentElement.scrollWidth<=innerWidth')
 checks['noVideoBrowserOrAssetErrors']=p.evaluate('v.error===null')and not errors;b.close()
result=dict(checks=checks,errors=errors);(O/'playback.json').write_text(json.dumps(result,indent=2));q=R/'docs/qa/carrier_mounts_1028.json';qa=json.loads(q.read_text());qa['playback']=result;q.write_text(json.dumps(qa,indent=2))
print(json.dumps(result));raise SystemExit(0 if all(checks.values())else 1)
