from pathlib import Path
import sys,json,time
from playwright.sync_api import sync_playwright
R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');W=Path(__file__).resolve().parent
sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
port,stop=shoot.serve(str(R))
try:
 with sync_playwright()as pw:
  b=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required'])
  p=b.new_page(viewport={'width':1366,'height':768});errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
  p.goto(f'http://127.0.0.1:{port}/index.html?quality=high',timeout=180000)
  p.wait_for_function('window.__bofFrames>5',timeout=180000);p.mouse.click(2,2)
  keys=['stage6_blue_master','bg_stage05_loop_0923','ls112_stage_5','ls112_stage_6','ls112_bed_space']
  info=p.evaluate('(keys)=>({sources:Object.fromEntries(keys.map(k=>[k,XART._src[k]])),cfg:_levelCfg(5),base:LS112.base.cfg(5),ss:SS})',keys)
  print(json.dumps(info),flush=True)
  (W/'scene-inventory.json').write_text(json.dumps(info,indent=2),encoding='utf8')
  p.evaluate("()=>{run.mode='arcade';run.pilot='axel';diffKey='furious';run.gravityShipReady=false;beginStage(5);DBGT.god=true;}")
  for label,condition in [('before-ascent',"state===GS.LAUNCH&&drawLaunch._furyIntro?.t>5"),('before-assembly',"drawLaunch._furyIntro?.phase==='assembly'"),('before-space',"state===GS.PLAY&&stageLoadReady(5)")]:
   p.wait_for_function(condition,timeout=180000,polling=50)
   p.screenshot(path=str(W/(label+'.png')))
   print(label,p.evaluate('()=>({state,stateT,t:drawLaunch._furyIntro?.t,phase:gravityMode.phase,scroll:_stage5SpaceScroll})'),flush=True)
  (W/'before-errors.json').write_text(json.dumps(errors,indent=2),encoding='utf8');b.close()
finally:stop()
