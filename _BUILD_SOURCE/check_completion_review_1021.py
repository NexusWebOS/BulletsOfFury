from pathlib import Path
import json,sys,http.server
from playwright.sync_api import sync_playwright
R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');O=R/'_shots/request_completion_1021';sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
http.server.ThreadingHTTPServer.request_queue_size=128;port,stop=shoot.serve(str(R));rows=[]
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge');p=b.new_page()
  for w in [1440,390]:
   p.set_viewport_size(dict(width=w,height=1000 if w==1440 else 844));p.goto(f'http://127.0.0.1:{port}/_shots/request_completion_1021/review.html');p.evaluate('()=>Promise.all([...document.images].map(i=>i.decode()))')
   d=p.evaluate('()=>({width:innerWidth,scroll:document.documentElement.scrollWidth,open:document.querySelectorAll("article").length,rows:document.querySelectorAll("tbody tr").length,broken:[...document.images].filter(i=>!i.naturalWidth).length})');rows.append(d);assert d['scroll']<=w+1 and d['open']==5 and d['rows']==19 and not d['broken'];p.screenshot(path=str(O/('review-'+str(w)+'.png')))
  links=p.evaluate('[...new Set([...document.querySelectorAll("a")].map(a=>a.href))]')
  for link in links:assert p.request.get(link).status==200,link
  b.close()
finally:stop()
(O/'review-layout.json').write_text(json.dumps(dict(layout=rows,links=len(links),badLinks=0),indent=2));print(json.dumps(rows))
