from pathlib import Path
import json
from playwright.sync_api import sync_playwright
W=Path(__file__).resolve().parents[1]/'_shots/weapon_contacts_1031';checks=[];errors=[]
def ck(name,value,data=None):checks.append(dict(name=name,passed=bool(value),data=data));print('PASS'if value else'FAIL',name,flush=True)
with sync_playwright()as pw:
 b=pw.chromium.launch(channel='msedge',headless=True);p=b.new_page(viewport={'width':1280,'height':900});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None)
 r=p.goto('http://127.0.0.1:8805/current/weapon-contacts-1031.html',wait_until='networkidle');p.wait_for_function('film.readyState>=2',timeout=60000)
 q=p.evaluate('({duration:film.duration,w:film.videoWidth,h:film.videoHeight,buttons:document.querySelectorAll("button[data-at]").length})')
 ck('Local preview page loads',r.status==200);ck('14.4s native preview decodes at1280x800',abs(q['duration']-14.4)<.1 and q['w']==1280 and q['h']==800,q)
 for i,at in enumerate([0,2.4,4.8,7.2,9.6,12]):
  p.locator('button[data-at]').nth(i).click();p.wait_for_function('(t)=>film.currentTime>t+.06',arg=at,timeout=10000);p.evaluate('film.pause()');t=p.evaluate('film.currentTime');ck('Chapter '+str(i+1)+' seeks and plays',at<t<at+1,t)
 p.screenshot(path=str(W/'preview-player.png'));ck('Preview has no page/console errors',not errors,errors);b.close()
(W/'player-checks.json').write_text(json.dumps(checks,indent=2));assert all(c['passed']for c in checks)
