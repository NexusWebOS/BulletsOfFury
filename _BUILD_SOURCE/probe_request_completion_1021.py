from pathlib import Path
import json,sys,http.server,hashlib,zipfile
from playwright.sync_api import sync_playwright
R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');O=R/'_shots/request_completion_1021';sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
http.server.ThreadingHTTPServer.request_queue_size=128;port,stop=shoot.serve(str(R));checks=[];errors=[]
def ck(name,ok,data=None):
 checks.append(dict(name=name,ok=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name,flush=True)
try:
 with sync_playwright() as pw:
  for browser in ([] if '--atlas-only' in sys.argv else ['msedge','chrome','firefox']):
   b=pw.firefox.launch() if browser=='firefox' else pw.chromium.launch(channel=browser)
   p=b.new_page(viewport=dict(width=1440,height=1000));p.set_default_timeout(180000)
   p.route('**/favicon.ico',lambda r:r.fulfill(status=204,body=''))
   p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:400]) if m.type=='error' else None)
   p.goto(f'http://127.0.0.1:{port}/extensions/bof-field-manual/guide.html')
   p.evaluate('()=>Promise.all([...document.images].map(im=>{im.loading="eager";return im.decode().catch(()=>null)}))')
   ck(browser+' guide artwork loads',p.evaluate('[...document.images].every(i=>i.complete&&i.naturalWidth>0)'))
   ck(browser+' current HUD and paired abilities',p.evaluate('()=>{const t=document.querySelector("#hud-left").textContent;return t.includes("second row")&&entries.some(e=>e.id==="rebel-current-nyx")&&abilityDetail.cole.includes("SONIC BOOM")&&abilityDetail.lizzie.includes("HEAVY TURRET")}'))
   ck(browser+' all dossier IDs remain unique',p.evaluate('new Set(entries.map(e=>e.id)).size===entries.length'))
   p.locator('#search').fill('CHROME HEART');ck(browser+' search finds secret fight',p.locator('#chrome-heart').count()==1)
   p.locator('#chrome-heart button').click();p.locator('#chrome-heart summary').click();p.locator('#chrome-heart textarea').fill('Keep room for the slam.');p.reload();p.locator('#search').fill('CHROME HEART')
   ck(browser+' notes and bookmark survive reload',p.locator('#chrome-heart textarea').input_value()=='Keep room for the slam.' and p.locator('#chrome-heart button').get_attribute('aria-pressed')=='true')
   p.locator('#search').fill('YOUR COMBAT CONSOLE');p.locator('#hud-full').screenshot(path=str(O/(browser+'-manual-hud.png')))
   for w in [1440,390]:
    p.set_viewport_size(dict(width=w,height=1000 if w==1440 else 844));p.locator('#search').fill('CHROME HEART');p.wait_for_timeout(100)
    ck(browser+' guide fits '+str(w),p.evaluate('document.documentElement.scrollWidth<=innerWidth+1'));p.screenshot(path=str(O/(browser+'-manual-'+str(w)+'.png')))
   b.close()
  # Live preview adapter, including the new secret route, must stay save-isolated.
  b=pw.chromium.launch(channel='msedge');p=b.new_page(viewport=dict(width=1440,height=1000));p.set_default_timeout(180000)
  p.route('**/favicon.ico',lambda r:r.fulfill(status=204,body=''));p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:500]) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/extensions/bof-field-manual/guide.html');p.evaluate('localStorage.setItem("completion-sentinel","keep")');before=p.evaluate('JSON.stringify(Object.fromEntries(Object.entries(localStorage).sort()))')
  p.goto(f'http://127.0.0.1:{port}/enemy-atlas.html#bof-rebel-rook');p.wait_for_function('document.querySelector("#loading").hidden')
  f=p.frames[1];ck('Rook native current aircraft loaded',f.evaluate('()=>{const a=BOF_ENEMY_ATLAS.snapshot();return !a.error&&a.actor?.type==="rebelsquad"}'))
  p.locator('#animations').scroll_into_view_if_needed();p.wait_for_timeout(1800)
  ck('Contact sheet shows all five current motion banks',p.evaluate('()=>{const t=document.querySelector("#animations").textContent;return ["Idle","Attack","Drift","Roll","Somer"].every(s=>t.includes(s))}'))
  ck('Contact sheet draws actual sheet pixels',p.evaluate('()=>[...document.querySelectorAll("#animations canvas")].every(c=>{const d=c.getContext("2d").getImageData(0,0,c.width,c.height).data;let n=0;for(let i=3;i<d.length;i+=4)if(d[i])n++;return n>40})'))
  p.locator('#animations').screenshot(path=str(O/'current-flight-banks.png'))
  p.locator('#search').fill('CHROME HEART');p.locator('#roster button').click();p.wait_for_function('document.querySelector("#loading").hidden')
  ck('Secret preview runs native owner without unlocking',f.evaluate('()=>!!boss?._heart&&run._heartMode&&!CH21.unlocked&&!BOF_ENEMY_ATLAS.snapshot().error'))
  p.locator('#animations').scroll_into_view_if_needed();p.wait_for_timeout(1600)
  ck('Secret contact sheets animate seven individually sliced banks',p.evaluate('()=>document.querySelectorAll("#animations canvas").length===7&&!document.querySelector("#animations").textContent.includes("Nca Ch21 Sheet")'))
  p.locator('#animations').screenshot(path=str(O/'secret-animation-banks.png'))
  p.locator('#search').fill('');p.locator('#engine').scroll_into_view_if_needed();p.wait_for_timeout(1400);p.screenshot(path=str(O/'chrome-heart-atlas.png'))
  p.locator('#pause').click();n=f.evaluate('BOF_ENEMY_ATLAS.snapshot().frames');p.wait_for_timeout(250);ck('Secret preview pause freezes combat',f.evaluate('BOF_ENEMY_ATLAS.snapshot().frames')==n)
  p.locator('#step').click();p.wait_for_timeout(180);ck('Secret preview advances one frame',f.evaluate('BOF_ENEMY_ATLAS.snapshot().frames')==n+1)
  p.locator('#search').fill('SIEGEFORTRESS17');p.locator('#roster button').click();p.wait_for_function('document.querySelector("#loading").hidden')
  ck('Returning to normal encounter clears secret owner',f.evaluate('()=>!run._heartMode&&!boss?._heart&&BOF_ENEMY_ATLAS.snapshot().actor?.type==="siegefortress17"'))
  ck('Encyclopedia leaves persistent progress untouched',before==p.evaluate('JSON.stringify(Object.fromEntries(Object.entries(localStorage).sort()))'))
  b.close()
finally:stop()
m=json.loads((R/'extensions/bof-field-manual/manifest.json').read_text());ck('Offline extension remains permission-free',m['version']=='1.2.0' and not m.get('permissions') and not m.get('host_permissions'))
z=Path(r'C:/Users/Mike/Documents/New project/output/bof-field-manual/BOF-Field-Manual-1.2.zip')
with zipfile.ZipFile(z) as f:ck('Extension package is intact and compact',f.testzip() is None and z.stat().st_size<25_000_000,dict(bytes=z.stat().st_size,files=len(f.namelist())))
ck('No page or console errors',not errors,errors)
(O/('atlas-refinement.json' if '--atlas-only' in sys.argv else 'guide-atlas-verification.json')).write_text(json.dumps(dict(checks=checks,errors=errors),indent=2));print(json.dumps(dict(checks=len(checks),passed=sum(c['ok'] for c in checks),errors=errors)))
sys.exit(0 if not errors and all(c['ok'] for c in checks) else 1)
