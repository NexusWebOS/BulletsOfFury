from pathlib import Path
import json
from playwright.sync_api import sync_playwright
R=Path('.').resolve();D=R/'_shots/warden_lunge_1028';errors=[]
with sync_playwright()as pw:
 b=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1280,'height':900});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None)
 p.on('response',lambda r:errors.append(str(r.status)+' '+r.url)if r.status>=400 else None)
 p.goto('http://127.0.0.1:8795/docs/previews/warden_lunge_1028/index.html?t=19');p.wait_for_function('v.readyState>=2&&v.currentTime>=18.9',timeout=30000);p.evaluate('()=>{v.muted=true;return v.play()}');p.wait_for_timeout(650);start=p.evaluate('v.currentTime');p.wait_for_timeout(650);advanced=p.evaluate('v.currentTime')>start
 p.evaluate('v.currentTime=153.8');p.wait_for_function('v.readyState>=2&&v.currentTime>=153.7');p.screenshot(path=str(D/'review-playing.png'));result=p.evaluate('({duration:v.duration,time:v.currentTime,ready:v.readyState,error:v.error?.message})');b.close()
result.update(advanced=advanced,errors=errors);(D/'playback.json').write_text(json.dumps(result,indent=2));print(result)
