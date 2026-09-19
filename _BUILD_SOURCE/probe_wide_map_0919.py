import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import shoot
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1]
port,stop=shoot.serve(str(root))
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(args=['--disable-gpu','--no-sandbox','--mute-audio'])
  page=browser.new_page(viewport={'width':1920,'height':1080})
  errors=[]
  page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load',timeout=60000)
  page.wait_for_function("typeof ASSETS!=='undefined' && (window.__bofFrames|0)>4",timeout=45000)
  page.evaluate("() => {document.body.classList.add('fs');__bofFit();run.mode='campaign';run.pilot='yuri';run.stage=4;campaign.unlockedMax=5;openStageSelect(4,{});}")
  page.wait_for_timeout(1800)
  page.screenshot(path=str(root/'_shots'/'widescreen_0918'/'campaign_map_full_world.png'))
  before=page.evaluate("""() => {const s=document.getElementById('screen').getBoundingClientRect(),w=cmap2World(2),c=cmap2.cam,k=s.width/480;return {x:s.left+240*k+(w.x-c.x)*c.z*k,y:s.top+218*k+(w.y-c.y)*c.z*k,frameLeft:s.left,cursor:sselCursor,worldVisible:getComputedStyle(document.getElementById('wide-map-world')).display};}""")
  if before['x']<before['frameLeft'] and before['y']>0:
   page.mouse.click(before['x'],before['y'])
   page.wait_for_timeout(150)
  after=page.evaluate("() => ({cursor:sselCursor,focus:cmap2.focus})")
  assert before['worldVisible']=='block' and before['x']<before['frameLeft'],before
  assert after['cursor']==2 and not errors,(after,errors)
  print(json.dumps({'before':before,'after':after,'errors':errors}))
  browser.close()
finally:stop()

