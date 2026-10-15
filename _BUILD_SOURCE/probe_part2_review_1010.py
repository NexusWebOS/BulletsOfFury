"""Verify the shipped effect-review page in real Chromium."""
from pathlib import Path
import sys,json
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
OUT=ROOT/'_shots/part2_1010/review';OUT.mkdir(parents=True,exist_ok=True)
checks=[];errors=[];port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch();p=br.new_page(viewport=dict(width=1280,height=1100))
  p.on('pageerror',lambda e:errors.append(str(e)))
  p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.on('response',lambda r:errors.append('HTTP '+str(r.status)+': '+r.url) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/docs/previews/part2_1010/index.html');p.wait_for_function('data&&Object.values(loaded).every(im=>im.complete&&im.naturalWidth>0)')
  for bank in ['atom','jace','maverick','maverick_full','fire','fire_root','fire_tip','stealth_roll','stealth_somer','stealth','shield']:
   p.select_option('#bank',bank)
   count=len(p.evaluate('artList()')); fits=[]; bad=[]
   if not count:raise AssertionError(bank+': selector returned no authored poses')
   for i in range(count):
    p.locator('#frame').evaluate('(e,i)=>{e.value=i;e.dispatchEvent(new Event("input"));}',i)
    q=p.evaluate('''()=>{const p=g.getImageData(0,0,432,432).data;let n=0,edge=0;for(let y=0;y<432;y++)for(let x=0;x<432;x++)if(p[(y*432+x)*4+3]>20){n++;if(x<10||x>=422||y<10||y>=422)edge++;}return {pixels:n,edges:edge,fit:fitBank()};}''')
    fits.append(q['fit'])
    if q['pixels']<100 or q['edges']:bad.append(dict(frame=i,**q))
   checks.append(dict(name=bank+': every pose renders with ten clear pixels on all borders',passed=not bad,data=bad))
   checks.append(dict(name=bank+': one fixed camera, scale and physical anchor across every pose',passed=all(q==fits[0] for q in fits),data=fits[0]))
   p.check('#onion');p.screenshot(path=str(OUT/(bank+'-onion.png')));p.uncheck('#onion')
   p.screenshot(path=str(OUT/(bank+'.png')))
  p.select_option('#bank','atom');p.locator('#frame').evaluate('(e)=>{e.value=18;e.dispatchEvent(new Event("input"));}');p.check('#onion')
  normal=p.evaluate('onion.checked&&index===18&&artList().length===32');checks.append(dict(name='Onion control actually overlays neighboring registered poses',passed=normal))
  p.screenshot(path=str(OUT/'atomic-registered-onion.png'))
  checks.append(dict(name='Review includes all original captures and the corrected live art evidence',passed=p.locator('figure').count()==len(p.evaluate('data.gallery')) and p.locator('figure').count()>=28))
  checks.append(dict(name='No page, console or missing asset errors',passed=not errors,data=errors));br.close()
except Exception as e:errors.append(str(e))
finally:
 stop();r=dict(passed=sum(q['passed'] for q in checks),failed=sum(not q['passed'] for q in checks),checks=checks,errors=errors)
 (OUT/'report.json').write_text(json.dumps(r,indent=2),encoding='utf-8');print(json.dumps(r),flush=True)
sys.exit(1 if r['failed'] or errors else 0)
