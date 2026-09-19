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
  page.evaluate("() => {document.body.classList.add('fs');__bofFit();run.mode='campaign';run.pilot='yuri';run.stage=4;run.score=231450;run.lives=3;diffKey='hard';DIFF=difficultyForRun('campaign','hard');campaign.unlockedMax=5;openStageSelect(4,{});}")
  page.wait_for_timeout(1800)
  page.screenshot(path=str(root/'_shots'/'widescreen_0918'/'campaign_map_portrait_centered.png'))
  before=page.evaluate("""() => {const s=document.getElementById('screen').getBoundingClientRect(),w=cmap2World(2),c=cmap2.cam,k=s.width/480;return {x:s.left+240*k+(w.x-c.x)*c.z*k,y:s.top+218*k+(w.y-c.y)*c.z*k,frameLeft:s.left,cursor:sselCursor,stages:[1,2,3,4,5].map(i=>{const q=cmap2World(i);return [i,s.left+240*k+(q.x-c.x)*c.z*k,s.top+218*k+(q.y-c.y)*c.z*k]}),worldVisible:getComputedStyle(document.getElementById('wide-map-world')).display};}""")
  if before['x']<before['frameLeft']:
   page.mouse.click(before['x'],max(24,before['y']))
   page.wait_for_timeout(150)
  after=page.evaluate("() => ({cursor:sselCursor,focus:cmap2.focus})")
  assert before['worldVisible']=='block' and before['x']<before['frameLeft'],before
  assert after['cursor']==2 and not errors,(after,errors)
  save=page.evaluate("""() => {const r=cmap2BtnRects()[0],s=document.getElementById('screen').getBoundingClientRect(),k=s.width/480;return {x:s.left+(r.x+r.w/2)*k,y:s.top+(r.y+r.h/2)*k};}""")
  page.mouse.move(save['x'],save['y'])
  page.mouse.down()
  page.wait_for_timeout(120)
  page.mouse.up()
  page.wait_for_timeout(450)
  bar=page.evaluate("() => ({mode:campPause&&campPause.mode,top:document.getElementById('screen').getBoundingClientRect().top})")
  assert bar['mode']=='save' and bar['top']<3,(bar,save)
  print(json.dumps({'before':before,'after':after,'bar':bar,'errors':errors}))
  browser.close()
finally:stop()
