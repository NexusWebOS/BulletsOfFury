from pathlib import Path
from playwright.sync_api import sync_playwright
import json,http.server,sys
R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');Q=R/'_shots/holoscan_1021';sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
http.server.ThreadingHTTPServer.request_queue_size=128;port,stop=shoot.serve(str(R));checks=[];errors=[]
def ck(n,v,d=None):checks.append(dict(name=n,ok=bool(v),data=d));print(('PASS ' if v else 'FAIL ')+n,flush=True)
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge');p=b.new_page(viewport=dict(width=1440,height=1000));p.set_default_timeout(180000)
  p.route('**/favicon.ico',lambda r:r.fulfill(status=204,body=''));p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:500]) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/extensions/bof-field-manual/guide.html');p.evaluate('localStorage.setItem("holoscan-progress-sentinel","keep")');before=p.evaluate('JSON.stringify(Object.fromEntries(Object.entries(localStorage).sort()))')
  p.goto(f'http://127.0.0.1:{port}/_shots/holoscan_1021/review.html');p.wait_for_function('document.querySelector("#preview-status").hidden')
  f=p.frames[1];f.wait_for_function('BOFHOLOSCAN.visible');ck('Interactive review opens the real dossier',f.evaluate('HS21.visible&&TUT.L.def.id==="bob_card"&&!!window.BOF_ATLAS_CLOCK'))
  f.locator('[data-part="1"]').click();f.wait_for_function('TUT.L.sel===1');ck('Interactive review uses native part selection',f.evaluate('IC20.cardFrame.part==="missile"'))
  for width,height in [(1440,1000),(390,844)]:
   p.set_viewport_size(dict(width=width,height=height));p.wait_for_timeout(200)
   d=p.evaluate('()=>({width:innerWidth,scroll:document.documentElement.scrollWidth,broken:[...document.images].filter(i=>i.complete&&!i.naturalWidth).length})');ck(str(width)+' review fits and images load',d['scroll']<=width+1 and not d['broken'],d);p.screenshot(path=str(Q/f'review-{width}.png'))
  p.locator('#live-scan').scroll_into_view_if_needed()
  f.locator('.hs-deploy').click(timeout=15000);f.wait_for_function('TUT.L.def.id==="exam"',timeout=20000);ck('Review deployment enters actual tutorial exercise',f.evaluate('!HS21.visible&&TUT.L.def.id==="exam"'))
  p.locator('#restart-scan').click();p.wait_for_function('document.querySelector("#preview-status").hidden');p.frames[1].wait_for_function('BOFHOLOSCAN.visible');ck('Restart creates one fresh isolated preview',p.frames[1].evaluate('TUT.L.def.id==="bob_card"'))
  after=p.evaluate('JSON.stringify(Object.fromEntries(Object.entries(localStorage).sort()))');ck('Preview deploy and restart leave persisted progress untouched',before==after)
  ck('No browser errors',not errors,errors);b.close()
finally:stop()
(Q/'review-checks.json').write_text(json.dumps(dict(checks=checks,errors=errors),indent=2));print(json.dumps(dict(passed=sum(c['ok'] for c in checks),checks=len(checks),errors=errors)))
sys.exit(0 if not errors and all(c['ok'] for c in checks) else 1)
