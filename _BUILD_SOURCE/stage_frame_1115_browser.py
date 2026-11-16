from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import hashlib,json
R=Path(__file__).resolve().parents[1];O=R/'_shots/stage_frame_1115';errors=[];checks=[]
def ck(name,ok,data=None):checks.append(dict(name=name,ok=bool(ok),data=data))
with sync_playwright()as pw:
 b=pw.chromium.launch(args=['--no-sandbox']);p=b.new_page(viewport={'width':1150,'height':900})
 p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None);p.on('response',lambda r:errors.append(str(r.status)+' '+r.url)if r.status>=400 else None)
 p.goto('http://127.0.0.1:8766/_shots/stage_frame_1115/review.html');p.wait_for_function("[...document.images].every(i=>i.complete&&i.naturalWidth>0)")
 q=p.evaluate("()=>[...document.images].map(i=>({src:i.getAttribute('src'),size:[i.naturalWidth,i.naturalHeight]}))")
 ck('all seven generated/native preview images load',len(q)==7,q)
 hashes=[]
 for i in range(4):
  p.wait_for_timeout(350);data=p.locator('#reveal').screenshot();(O/('gif-browser-'+str(i)+'.png')).write_bytes(data);hashes.append(hashlib.sha256(data).hexdigest())
 ck('actual GIF element advances in Chromium',len(set(hashes))>=3,hashes)
 ck('animated GIF preserves native crop dimensions',q[0]['size']==[960,424],q[0])
 ck('review page has no horizontal overflow',p.evaluate('document.documentElement.scrollWidth<=innerWidth'))
 p.screenshot(path=str(O/'review-browser.png'));ck('no review page/console/HTTP errors',not errors,errors);b.close()
(O/'browser-qa.json').write_text(json.dumps(dict(checks=checks,errors=errors),indent=2),encoding='utf8');print(str(sum(c['ok']for c in checks))+'/'+str(len(checks))+' browser preview checks passed');assert all(c['ok']for c in checks)
