"""Measure current regular tank and Furious miniboss in native Chromium."""
from pathlib import Path
import sys,json,base64
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'_BUILD_SOURCE'));import shoot
OUT=ROOT/'_ART_SOURCES/siege_tanks_1010/reference';errors=[]
port,stop=shoot.serve(str(ROOT))
try:
 with sync_playwright() as pw:
  br=pw.chromium.launch(args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page();p.set_default_timeout(120000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF);p.wait_for_timeout(60)
  p.evaluate('()=>{beginStage(1);setState(GS.PLAY);story=null;BOFCinematicDirector.cancel();stagePlan=[];player.invuln=1e9;}')
  p.wait_for_function('()=>{stageLoadTick();return stageLoadInfo(1).ready;}',polling=30)
  q=p.evaluate('()=>{enemies=[];spawnEnemy("s1tankheavy",180,220);const e=enemies.at(-1);e._modAngle=Math.PI/2;ctx.setTransform(SS,0,0,SS,0,0);ctx.clearRect(0,0,cv.width,cv.height);drawEnemy(e);return {type:e.type,w:e.w,h:e.h,drawW:e._drawW,drawH:e._drawH,image:cv.toDataURL().split(",")[1]};}')
  (OUT/'regular_tank_native.png').write_bytes(base64.b64decode(q.pop('image')))
  q['furious']={'w':186,'h':186};q['errors']=errors
  (OUT/'scale_baseline.json').write_text(json.dumps(q,indent=2)+'\n');print(json.dumps(q),flush=True);br.close()
finally:stop()
if errors:sys.exit(1)
