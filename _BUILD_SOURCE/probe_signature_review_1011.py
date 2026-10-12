"""Check the portable special review's controls, images and narrow layout."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import sys,json
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
OUT=ROOT/'_shots/signature_specials_1011';checks=[];errors=[]
def check(name,yes):checks.append(dict(name=name,passed=bool(yes)));print(('PASS ' if yes else 'FAIL ')+name,flush=True)
port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch();p=br.new_page(viewport=dict(width=1280,height=950))
  p.on('pageerror',lambda e:errors.append(str(e)))
  p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.on('response',lambda r:errors.append('HTTP '+str(r.status)+': '+r.url) if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}/docs/previews/signature_specials_1011/index.html');p.wait_for_function('ready===true')
  check('Review lists nine upgrades and five enemy signatures',p.locator('#upgrades tr').count()==9 and p.locator('#rebel option').count()==5)
  good=[]
  for pk in p.evaluate('review.pilots.map(p=>p.key)'):
   p.select_option('#pilot',pk)
   for phase in ['incoming','base','enhanced']:
    p.locator('button[data-phase="'+phase+'"]').click()
    p.wait_for_function('s=>{const i=document.querySelector("#pilotShot");return i.complete&&i.naturalWidth>0&&i.getAttribute("src")===s}',arg=pk+'-'+phase+'.webp')
    good.append(pk+'-'+phase)
  check('All27 pilot pictures load through the actual selector and buttons',len(good)==27)
  for pk in p.evaluate('review.rebels.map(r=>r.key)'):
   p.select_option('#rebel',pk);p.wait_for_function('s=>{const i=document.querySelector("#rebelShot");return i.complete&&i.naturalWidth>0&&i.getAttribute("src")===s}',arg='rebel-'+pk+'.webp')
  check('All five enemy capture selections load',True)
  p.wait_for_function('()=>[...document.images].every(i=>i.complete&&i.naturalWidth>0)')
  check('Stage X reward and co-op evidence images also load',True)
  p.select_option('#pilot','cole');p.select_option('#rebel','voss');p.locator('button[data-phase="enhanced"]').click();p.screenshot(path=str(OUT/'review-desktop.png'),full_page=True)
  p.set_viewport_size(dict(width=480,height=900));p.wait_for_timeout(80)
  check('The complete review fits a narrow viewport',p.evaluate('document.documentElement.scrollWidth<=innerWidth'))
  p.screenshot(path=str(OUT/'review-mobile.png'),full_page=True)
  check('No preview page, console or missing-asset errors',not errors);br.close()
except Exception as e:
 errors.append(type(e).__name__+': '+str(e));print(errors[-1],flush=True)
finally:
 stop();report=dict(passed=sum(q['passed'] for q in checks),failed=sum(not q['passed'] for q in checks),checks=checks,errors=errors)
 (OUT/'preview-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report),flush=True)
sys.exit(1 if errors or report['failed'] else 0)
