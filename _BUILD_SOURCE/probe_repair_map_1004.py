"""Uninterrupted Chromium map animation and Stage X audio routing."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import shoot as sh
import json
R=Path(__file__).resolve().parents[1];O=R/'_shots/gameplay_audit_1004/map';O.mkdir(parents=True,exist_ok=True)
port,stop=sh.serve(str(R));errors=[];report={}
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1920,'height':1080})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('()=>window.__bofFrames>3',timeout=120000)
  p.evaluate('()=>{run.mode="campaign";run.pilot="lizzie";campaign.unlockedMax=8;campaign.rank={1:"S",2:"A",3:"B"};campaign.bonusUnlocked=false;campaign.rivalScattered=false;openStageSelect(1,{boot:true});sselUnlockCine=null;Input.mouse.moved=false;window.sselCommitted=false;cmap2Warm();mapgWarm();}')
  p.wait_for_function('()=>GP4_MAP_KEYS.every(k=>XART.rdy("gp4_island_"+k))&&bmfReady("game")&&bmfReady("dialogue")',timeout=120000)
  p.wait_for_timeout(4500);p.screenshot(path=str(O/'overview.png'))
  p.wait_for_function('()=>sselBoot===0',timeout=30000);p.wait_for_timeout(2800);p.screenshot(path=str(O/'selected-jungle.png'))
  report['firstZoom']=p.evaluate('()=>({z:cmap2.cam.z,x:cmap2.cam.x,y:cmap2.cam.y})')
  p.evaluate('()=>{sselCursor=4;Input.mouse.moved=false;}');p.wait_for_timeout(2700);p.screenshot(path=str(O/'selected-desert.png'))
  report['hover']=p.evaluate('()=>({stage:sselCursor,lift:cmap2.lift[4],camera:cmap2.cam})')
  p.set_viewport_size({'width':1000,'height':900});p.wait_for_timeout(1400);p.screenshot(path=str(O/'compact.png'))
  p.evaluate(sh.TRAP_RAF);p.wait_for_timeout(50)
  report['stagex']=[]
  for code in ['XHARR','XREBEL']:
   p.evaluate('(code)=>{pwInput=code;submitPassword();beginStage(PENDING_STAGE);setState(GS.PLAY);BOFCinematicDirector.cancel();story=null;gp4QuickEncounter();Audio.startMusic("boss6");}',code)
   p.wait_for_function('()=>Snd.cur&&Snd.cur.readyState>=2&&!Snd.cur.paused',timeout=30000)
   report['stagex'].append(p.evaluate('()=>({route:run._gp4StageX,path:Snd.cur.getAttribute("src")})'))
  b.close()
finally:stop()
report['errors']=errors;(O/'report.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
