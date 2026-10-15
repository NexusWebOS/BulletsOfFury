"""Check the frame/onion review with the real Chromium canvas and network."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import shoot,json,sys
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'_shots/playthrough_1011/review';OUT.mkdir(parents=True,exist_ok=True)
checks=[];errors=[]
def check(name,value,data=None):
 checks.append(dict(name=name,passed=bool(value),data=data));print(('PASS ' if value else 'FAIL ')+name,flush=True)
port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch();p=br.new_page(viewport=dict(width=1440,height=1000));p.set_default_timeout(60000)
  p.on('pageerror',lambda e:errors.append(str(e)))
  p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.on('response',lambda r:errors.append(f'HTTP {r.status}: {r.url}') if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/docs/previews/playthrough_1011/index.html')
  p.wait_for_function('window.reviewState?.loaded');p.locator('#play').click()
  p.evaluate('document.querySelectorAll("img").forEach(i=>i.loading="eager")')
  p.wait_for_function('Array.from(document.images).filter(i=>i.src).every(i=>i.complete&&i.naturalWidth>0)')
  keys=p.locator('#bank option').evaluate_all('(a)=>a.map(o=>o.value)')
  for key in keys:
   p.locator('#bank').select_option(key);p.wait_for_function('window.reviewState.loaded')
   count=p.evaluate('window.reviewState.count')
   p.locator('#frame').fill(str(count-1));p.locator('#frame').dispatch_event('input')
   p.wait_for_function('window.reviewState.loaded')
   q=p.evaluate('window.reviewState');check(key+' loads its complete authored bank',q['frame']==count-1 and count==(6 if key=='ice_parts' else 16),q)
   if key in ['fire_spray','sonic_pulse']:
    p.locator('#onion').check();p.locator('#pivot').check();p.locator('#animation').screenshot(path=str(OUT/(key+'-onion.png')))
  p.locator('#bank').select_option('drone_raise');p.locator('#frame').fill('8');p.locator('#frame').dispatch_event('input');p.locator('#onion').check();p.locator('#pivot').check()
  p.wait_for_function('window.reviewState.loaded');p.locator('#animation').screenshot(path=str(OUT/'drone-onion.png'))
  p.locator('#next').click();check('Next frame preserves the physical anchor',p.evaluate('window.reviewState.frame===9&&!window.reviewState.playing'))
  p.locator('#previous').click();check('Previous frame returns to the selected drawing',p.evaluate('window.reviewState.frame===8'))
  p.locator('#play').click();p.wait_for_timeout(280);check('Playback advances real frames',p.evaluate('window.reviewState.playing&&window.reviewState.frame!==8'));p.locator('#play').click()
  p.locator('#combat img').first.click();check('Capture opens at full resolution',p.locator('#lightbox').evaluate('(d)=>d.open'));p.locator('#close').click()
  for w,h in [(1440,1000),(820,900),(390,844)]:
   p.set_viewport_size(dict(width=w,height=h));p.evaluate('window.scrollTo(0,0)');p.wait_for_timeout(80)
   q=p.evaluate('({width:innerWidth,body:document.documentElement.scrollWidth})');check(f'Review fits {w}px without horizontal overflow',q['body']<=w,q)
   p.screenshot(path=str(OUT/f'review-{w}.png'))
  check('No page, console or asset errors',not errors,errors);br.close()
finally:stop()
report=dict(passed=sum(c['passed'] for c in checks),failed=sum(not c['passed'] for c in checks),checks=checks,errors=errors)
(OUT/'report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(passed=report['passed'],failed=report['failed'],errors=errors)))
sys.exit(1 if report['failed'] else 0)
