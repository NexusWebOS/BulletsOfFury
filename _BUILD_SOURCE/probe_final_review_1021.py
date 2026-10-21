from pathlib import Path
from playwright.sync_api import sync_playwright
import json
R=Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury');O=R/'_shots/final_version_1021';errors=[];rows=[]
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge');p=b.new_page(viewport=dict(width=1440,height=1000));p.on('pageerror',lambda e:errors.append(str(e)));p.goto('http://127.0.0.1:8794/_shots/final_version_1021/review.html');p.wait_for_function('actors.length>40');p.wait_for_timeout(400)
 for size in [(1440,1000),(390,844)]:
  p.set_viewport_size(dict(width=size[0],height=size[1]));p.evaluate('scrollTo(0,0)');p.wait_for_timeout(200);p.screenshot(path=str(O/('review-'+str(size[0])+'.png')))
  rows.append(dict(size=size,overflow=p.evaluate('document.documentElement.scrollWidth>innerWidth'),models=p.locator('#aircraft article').count(),pending=p.locator('#status').inner_text()))
  for anchor in ['hammer','air','city','concepts']:
   p.locator('#'+anchor).scroll_into_view_if_needed();p.wait_for_timeout(160)
  for select in p.locator('select').all():
   select.scroll_into_view_if_needed();count=select.locator('option').count();select.select_option(index=min(1,count-1));p.wait_for_timeout(40)
 p.locator('#pause').click();assert p.locator('#pause').inner_text()=='Resume animations';b.close()
(O/'review-qa.json').write_text(json.dumps(dict(rows=rows,errors=errors),indent=2));print(json.dumps(dict(rows=rows,errors=errors)));assert not errors and all(not r['overflow'] and r['models']==40 for r in rows)
