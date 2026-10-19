"""Native review UI, data, responsive layout and full-field asset links."""
from pathlib import Path
import http.server,json,sys
from urllib.parse import urljoin
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];O=R/'_shots/overnight_combat_1019/review';O.mkdir(parents=True,exist_ok=True)
checks=[];errors=[];port,stop=shoot.serve(str(R));http.server.ThreadingHTTPServer.request_queue_size=128
def ck(name,ok,data=None):checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name,flush=True)
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(channel='msedge');p=br.new_page(viewport=dict(width=1600,height=1000));p.set_default_timeout(180000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:700]) if m.type=='error' else None);p.on('response',lambda r:errors.append(str(r.status)+' '+r.url.split('?')[0]) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/docs/previews/overnight_1019/index.html');p.wait_for_function('D&&document.querySelectorAll("#campaignTable tbody tr").length===30')
  ck('30 completed current campaign cases and the complete authored-movement matrix load',p.evaluate('D.campaign.every(c=>c.outcome==="complete"&&!c.errors.length)&&D.shippingProgress.length===30&&D.shippingProgress.every(c=>c.outcome==="complete"&&!c.errors.length)&&D.matrixComplete&&D.enemies.length===D.matrixExpected&&D.matrixSource==="enemy_matrix/shipping-final-factory"&&D.matrixVersion===7'))
  ck('57 equal-window native encounter cases load',p.evaluate('D.encounters.length===57'))
  ck('Current encounter source and all 1007 focused native checks pass',p.evaluate('D.encounterSource==="encounters/shipping-final"&&D.matrixVersion>=6&&Object.values(D.native).reduce((s,q)=>s+q.passed,0)===1007&&Object.values(D.native).every(q=>!q.failed&&!q.errors.length)'))
  ck('All nine friendly hulls and the naturally docked mount have native evidence',p.evaluate('D.native["All nine cloaked pilots and docked mount"].passed===23&&D.gallery.some(q=>q.path==="stealth-pilots/lizzie-natural-mounted-cloak.jpg")&&D.campaign.filter(q=>q.stage===6&&q.route==="right").every(q=>q.id.endsWith("stealth-mount-final"))'))
  ck('75 co-op cases apply the native party factor once, with integer EHP normalization',p.evaluate('D.coopPools.length===75&&D.coopPools.every(q=>q.multiplier===1.25&&q.party>q.solo&&Math.abs(q.party-q.before*q.multiplier)<=1)'))
  ck('Ordinary round ownership totals reconcile in every roster row',p.evaluate('D.enemies.every(q=>q.parentShots+q.helperShots+q.unattributedShots===q.shots)'))
  ck('Extended Hammer books stop at the native morph and expose the actual pose gap',p.evaluate('D.hammerBooks.length===3&&D.hammerBooks.every(q=>q.morphed&&q.seconds>40&&q.seconds<50&&q.warn===1&&q.ball===31&&q.whirl===8&&q.nova===1)'))
  ck('Thirty native stealth factory cases include full-field release captures and real bomb warnings',p.evaluate('D.enemies.filter(q=>q.flightRole).length===30&&D.enemies.filter(q=>q.flightRole).every(q=>q.screenshot&&q.shots+q.ground>0)&&D.enemies.filter(q=>q.flightRole==="green").every(q=>q.groundWarnings.some(g=>g.warn>=1.45&&g.track===false))'))
  ck('Current three-seed pressure, signature controls and final Furious route load',p.evaluate('D.rebelSeeds.length===18&&D.signatureControls.length===27&&D.rebelFinals.length===1&&D.rebelFinals[0].outcome==="complete"&&!D.rebelFinals[0].errors.length'))
  ck('Furious summary uses production-final pressure rather than the earlier two-gun candidate',p.evaluate('D.rebels.candidate.filter(q=>q.difficulty==="furious").map(q=>q.contacts).join(",")==="20,19"'))
  ck('All fifteen shipping password cases are error-free',p.evaluate('D.passwords.length===15&&!D.passwordErrors.length&&D.passwords.every(q=>q.finite)'))
  p.screenshot(path=str(O/'findings.png'),full_page=True)
  p.get_by_role('button',name='Enemy roster',exact=True).click();p.select_option('#stage','5');p.select_option('#difficulty','furious');count=p.locator('#enemyTable tbody tr').count();ck('Stage and difficulty filters show the 12 live Stage 5 roles',count==12,count)
  p.fill('#search','ram');ck('Ram roles stay distinct from inactive shooters',p.locator('#enemyTable tbody tr').count()==1);p.fill('#search','');p.screenshot(path=str(O/'stage5-matrix.png'))
  p.get_by_role('button',name='Art & motion',exact=True).click();p.wait_for_function('[...document.querySelectorAll("#artGrid img")].every(im=>im.complete&&im.naturalWidth>0)');ck('All eight accepted animation previews load',p.locator('#artGrid img').count()==8)
  for a in p.locator('#artGrid a').all():
   response=p.request.get(urljoin(p.url,a.get_attribute('href')));ck('Onion registration '+a.get_attribute('href').split('/')[-1],response.ok)
  p.get_by_role('button',name='Full-field evidence',exact=True).click();p.locator('#gallery').scroll_into_view_if_needed();p.evaluate('document.querySelectorAll("#gallery img").forEach(im=>im.loading="eager")');p.wait_for_function('[...document.querySelectorAll("#gallery img")].every(im=>im.complete&&im.naturalWidth>0)');ck('Full-field captures use original image dimensions',p.evaluate('[...document.querySelectorAll("#gallery img")].filter(im=>!im.src.includes("stealth")).every(im=>im.naturalWidth>=600)'))
  p.screenshot(path=str(O/'evidence.png'))
  p.set_viewport_size(dict(width=390,height=844));p.get_by_role('button',name='Findings',exact=True).click();p.evaluate('scrollTo(0,0)');p.screenshot(path=str(O/'mobile-findings.png'));size=p.evaluate('({view:innerWidth,page:document.documentElement.scrollWidth})');ck('Mobile findings fit the viewport',size['page']<=size['view']+1,size)
  br.close()
finally:stop()
ck('No page, console or asset errors',not errors,errors);report=dict(passed=sum(q['passed'] for q in checks),failed=sum(not q['passed'] for q in checks),checks=checks,errors=errors);(O/'native-report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');sys.exit(report['failed']>0)
