from pathlib import Path
from playwright.sync_api import sync_playwright
import sys,json
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
OUT=ROOT/'_shots/element_arsenal_1011/review';OUT.mkdir(parents=True,exist_ok=True)
errors=[];checks=[]
port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch();p=b.new_page(viewport=dict(width=1360,height=1020));p.set_default_timeout(120000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.on('response',lambda r:errors.append(f'HTTP {r.status}: {r.url}') if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/docs/previews/element_arsenal_1011/index.html');p.wait_for_function('ready');p.wait_for_timeout(1200)
  for el in ['fire','kinetic','lightning','water','ice','chrome','toxic','dark','wind']:
   p.locator('[data-element="'+el+'"]').click();p.wait_for_timeout(450)
   for slot in range(9):
    p.locator('[data-weapon="'+str(slot)+'"]').click();p.wait_for_timeout(120)
    q=p.evaluate('()=>({ready,el:selected,slot,err:engine.eval("ARSENAL_PREVIEW.err"),pixels:[...document.querySelector("#live").getContext("2d").getImageData(0,0,360,470).data].filter((v,i)=>i%4!==3&&v>100).length})')
    checks.append(dict(element=el,slot=slot,passed=q['ready'] and q['pixels']>500 and not q.get('err')))
   p.locator('[data-weapon="0"]').click();p.wait_for_timeout(300)
   p.screenshot(path=str(OUT/(el+'.png')),full_page=True)
  p.locator('[data-element="fire"]').click();p.locator('#pause').click();p.locator('#onion').check();p.locator('#frame').fill('8');p.wait_for_timeout(150)
  checks.append(dict(name='Frame scrubbing and onion skin',passed=p.evaluate('paused&&frame===8&&document.querySelector("#onion").checked')))
  p.locator('.ammo').screenshot(path=str(OUT/'onion.png'))
  p.set_viewport_size(dict(width=390,height=844));p.wait_for_timeout(250);p.screenshot(path=str(OUT/'mobile.png'),full_page=True)
  checks.append(dict(name='Mobile no horizontal overflow',passed=p.evaluate('document.documentElement.scrollWidth<=window.innerWidth')))
  b.close()
finally:stop()
(OUT/'checks.json').write_text(json.dumps(dict(checks=checks,errors=errors),indent=2),encoding='utf-8')
print(json.dumps(dict(checks=len(checks),failed=[q for q in checks if not q['passed']],errors=errors)))
sys.exit(1 if errors or any(not q['passed'] for q in checks) else 0)
