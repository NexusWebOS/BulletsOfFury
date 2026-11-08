from pathlib import Path
import sys,json
from playwright.sync_api import sync_playwright
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import serve
port,stop=serve(str(R));errors=[]
try:
 with sync_playwright()as pw:
  b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required','--disable-background-timer-throttling','--disable-renderer-backgrounding','--disable-backgrounding-occluded-windows']);p=b.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)))
  p.goto(f'http://127.0.0.1:{port}/index.html?quality=high',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5');p.mouse.click(3,3)
  p.evaluate("()=>{diffKey='furious';DIFF=difficultyForRun('arcade',diffKey);run.stage=7;stageLoadBegin(7);}");p.wait_for_function('()=>{stageLoadTick();return sj98Ready()&&stageLoadReady(7)}',timeout=180000)
  p.evaluate("()=>{debugUnlocked=true;debugStartFight({stage:7,role:'mini',kind:'dualscoopdredger',name:'SUMPJAW PAIR'},{pilot:'cole',record:false});DBGT.god=true;DBGT.speed=1;player.invuln=0;run.weapon=3;run.wlevel=5;run.wlevels=WEAPONS.map(()=>5);run.bombs=40;spawnSubBoss('dualscoopdredger');debugFight.spawned=true;warnT=0;s6Opening=null;fb2Talk=fb2Intro=null;H3.release=false;story=null;BOFCinematicDirector.cancel();setState(GS.PLAY);}")
  p.wait_for_timeout(2000);a=p.evaluate('({t:performance.now(),f:__bofFrames})');p.wait_for_timeout(20000);z=p.evaluate('({t:performance.now(),f:__bofFrames})');observation=(z['f']-a['f'])*1000/(z['t']-a['t'])
  p.evaluate("()=>{function input(){if(subBoss&&!subBoss.dead){const g=retinaBossTargets(subBoss)[0];Input.keys.j=true;Input.keys.a=g&&player.x>g.x+5;Input.keys.d=g&&player.x<g.x-5;}requestAnimationFrame(input)}requestAnimationFrame(input);}");a=p.evaluate('({t:performance.now(),f:__bofFrames})');p.wait_for_timeout(20000);z=p.evaluate('({t:performance.now(),f:__bofFrames})');firing=(z['f']-a['f'])*1000/(z['t']-a['t']);b.close()
finally:stop()
out=dict(observationFps=observation,firingFps=firing,errors=errors);(W/'performance.json').write_text(json.dumps(out,indent=2));print(json.dumps(out))
