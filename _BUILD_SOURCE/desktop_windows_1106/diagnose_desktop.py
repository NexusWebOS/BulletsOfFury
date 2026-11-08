from pathlib import Path
import subprocess,time,json,urllib.request,ctypes
from playwright.sync_api import sync_playwright
W=Path(__file__).resolve().parent;EXE=W/'qa/Installed BOF/Bullets of Fury.exe';Q=W/'qa/perf';Q.mkdir(exist_ok=True);R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');port=48974
p=subprocess.Popen([str(EXE),'--game','--qa-dir',str(Q),'--profile',str(Q/'profile'),'--debug-port',str(port)])
try:
 with sync_playwright()as pw:
  until=time.monotonic()+60
  while True:
   try:b=pw.chromium.connect_over_cdp(f'http://127.0.0.1:{port}');break
   except:
    if time.monotonic()>until:raise
    time.sleep(.3)
  page=b.contexts[0].pages[0];page.wait_for_function('window.__bofFrames>10',timeout=180000);page.mouse.click(3,3);page.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'));page.evaluate("()=>{EA11.setup(1,'furious');stagePlan=[];waveIdx=0;CP12.next=VP12.next=CP22.nextWave=CP22.nextFlyby=99999;_adaptiveSpawnT=99999;DBGT.god=true;spawnSubBoss('razorback');}");page.wait_for_function('()=>{stageLoadTick();return stageLoadReady(1)}',timeout=180000)
  gpu=b.new_browser_cdp_session().send('SystemInfo.getInfo');(Q/'gpu.json').write_text(json.dumps(gpu,indent=2));print('GPU',gpu['gpu']['featureStatus'],flush=True)
  rows=[]
  for mode in ['unfocused','focused','windowed','fullscreen']:
   if mode=='focused':
    h=ctypes.windll.user32.FindWindowW(None,'Bullets of Fury');ctypes.windll.user32.ShowWindow(h,9);ctypes.windll.user32.SetForegroundWindow(h)
   if mode in ['windowed','fullscreen']:page.keyboard.press('F11');page.wait_for_timeout(1000)
   page.wait_for_timeout(1200);a=page.evaluate('window.__bofFrames');t=time.monotonic();page.wait_for_timeout(5000);fps=(page.evaluate('window.__bofFrames')-a)/(time.monotonic()-t)
   stats=page.evaluate('()=>({state,visibility:document.visibilityState,focus:document.hasFocus(),SS,VW,VH,canvas:[cv.width,cv.height],rect:cv.getBoundingClientRect().toJSON(),scale:devicePixelRatio,enemies:enemies.length,sub:subBoss?.kind,frames:window.__bofFrames})');rows.append(dict(mode=mode,fps=fps,stats=stats));print(mode,round(fps,2),stats,flush=True)
  (Q/'comparison.json').write_text(json.dumps(rows,indent=2));page.evaluate('()=>window.close()');p.wait(timeout=15);b.close()
finally:
 if p.poll()is None:p.terminate();p.wait(timeout=15)
