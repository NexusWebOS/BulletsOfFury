"""Check the interactive candidate viewer; this is not a gameplay recording."""
from pathlib import Path
import sys,json,io
from PIL import Image
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'))
import shoot
port,shutdown=shoot.serve(str(ROOT))
out=ROOT/'_shots/furyship_0914';errors=[]
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(args=['--no-sandbox'])
  page=browser.new_page(viewport={'width':1100,'height':1000})
  page.on('pageerror',lambda e:errors.append(str(e)))
  page.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  page.goto(f'http://127.0.0.1:{port}/assets/game/furyship_0914/preview.html',wait_until='networkidle')
  for name in ['nose','hull','wing_left','wing_right','engine_left','engine_right','assembly','veil','speed','thrusters','roll','somersault']:
   page.select_option('#family',name)
   page.wait_for_timeout(100)
   assert page.locator('#frames button').count() == (5 if name in ['nose','hull','wing_left','wing_right','engine_left','engine_right'] else (12 if name=='somersault' else 8))
  page.click('#pause')
  first=page.locator('#counter').inner_text();page.wait_for_timeout(200)
  assert first==page.locator('#counter').inner_text(),'pause must freeze the reel'
  page.locator('#frames button').nth(4).click()
  page.wait_for_timeout(30)
  assert page.locator('#counter').inner_text()=='Frame 5 / 12'
  page.select_option('#scale','1')
  page.screenshot(path=str(out/'viewer.png'))
  page.select_option('#family','somersault')
  captured=[]
  for i in range(12):
   page.locator('#frames button').nth(i).click();page.wait_for_timeout(35)
   captured.append(Image.open(io.BytesIO(page.locator('#preview').screenshot())).convert('RGB'))
  captured[0].save(out/'somersault_preview.gif',save_all=True,append_images=captured[1:],duration=100,loop=0)
  browser.close()
finally:shutdown()
assert not errors,errors
(out/'viewer_results.json').write_text(json.dumps({'families':12,'pause':True,'frameSelection':True,'errors':errors,'scope':'standalone asset viewer only'},indent=2)+'\n')
print('12 reels, pause and frame selection verified; zero browser errors.')
