from pathlib import Path
from urllib.parse import urljoin
from playwright.sync_api import sync_playwright
import json
R=Path(__file__).resolve().parents[1];O=R/'_shots/release_qa_1116';errors=[]
with sync_playwright()as w:
 b=w.chromium.launch(args=['--no-sandbox']);p=b.new_page(viewport={'width':1440,'height':1100});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'else None);p.on('response',lambda r:errors.append(str(r.status)+' '+r.url)if r.status>=400 else None)
 p.goto('http://127.0.0.1:8765/_shots/release_qa_1116/review.html');p.wait_for_function('Array.from(document.images).every(i=>i.complete&&i.naturalWidth>0)');links=p.locator('a[href]').evaluate_all('(a)=>a.map(e=>e.href)');heads=[]
 for url in sorted(set(links)):
  r=p.request.head(url);heads.append({'url':url,'status':r.status})
 p.screenshot(path=str(O/'review-top.png'));p.locator('h2').nth(1).scroll_into_view_if_needed();p.screenshot(path=str(O/'review-evidence.png'));b.close()
(O/'review-checks.json').write_text(json.dumps({'errors':errors,'links':heads,'imagesDecoded':True},indent=2),encoding='utf8');print(json.dumps({'errors':errors,'links':len(heads),'badLinks':[q for q in heads if q['status']>=400]}));assert not errors and all(q['status']<400 for q in heads)
