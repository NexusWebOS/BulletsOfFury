from pathlib import Path
from playwright.sync_api import sync_playwright
import json
R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');O=R/'_shots/menu_heart_1021';rows=[]
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge');p=b.new_page();p.goto('http://127.0.0.1:8794/_shots/menu_heart_1021/review.html');p.wait_for_function('Array.from(document.images).every(i=>i.complete&&i.naturalWidth)',timeout=60000)
 for w,h in [(1440,1000),(390,844)]:
  p.set_viewport_size({'width':w,'height':h});row=p.evaluate('()=>({width:innerWidth,scroll:document.documentElement.scrollWidth,concepts:document.querySelectorAll(\'article[id^="concept-"]\').length,frames:document.querySelectorAll("#frames article img").length,reel:!!document.querySelector(\'img[src="heart-actions.gif"]\'),broken:[...document.images].filter(i=>!i.complete||!i.naturalWidth).length})');rows.append(row);p.screenshot(path=str(O/f'review-{w}.png'))
 b.close()
(O/'final-review.json').write_text(json.dumps(rows,indent=2));print(json.dumps(rows));assert all(r['scroll']<=r['width'] and r['concepts']==5 and r['frames']==4 and r['reel'] and r['broken']==0 for r in rows)
