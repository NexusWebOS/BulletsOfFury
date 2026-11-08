from pathlib import Path
import json,subprocess,time,statistics,sys
from playwright.sync_api import sync_playwright
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');ROOT=W/'qa/Installed BOF';Q=W/'qa/paired';Q.mkdir(exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import serve
port,stop=serve(str(ROOT/'game'));rows=[];proc=None
def measure(p,kind):
 p.wait_for_function('window.__bofFrames>5',timeout=180000);p.mouse.click(3,3);p.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'))
 p.evaluate("()=>{EA11.setup(1,'furious');let seed=1106;Math.random=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/4294967296;};stagePlan=[];waveIdx=0;CP12.next=VP12.next=CP22.nextWave=CP22.nextFlyby=99999;_adaptiveSpawnT=99999;DBGT.god=true;spawnSubBoss('razorback');}");p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(1)}',timeout=180000,polling=100);p.bring_to_front();p.wait_for_timeout(10000);samples=[]
 for _ in range(3):
  n=p.evaluate('window.__bofFrames');t=time.monotonic();p.wait_for_timeout(5000);samples.append((p.evaluate('window.__bofFrames')-n)/(time.monotonic()-t))
 row=dict(kind=kind,samplesFps=samples,medianFps=statistics.median(samples),viewport=p.evaluate('()=>({SS,VW,VH,dpr:devicePixelRatio,width:innerWidth,height:innerHeight,canvas:[cv.width,cv.height],focus:document.hasFocus()})'));rows.append(row);print(kind,json.dumps(row),flush=True)
try:
 with sync_playwright()as pw:
  proc=subprocess.Popen([str(ROOT/'Bullets of Fury.exe'),'--game','--qa-dir',str(Q),'--profile',str(Q/'profile'),'--debug-port','48975'])
  until=time.monotonic()+60
  while True:
   try:b=pw.chromium.connect_over_cdp('http://127.0.0.1:48975');break
   except:
    if time.monotonic()>until:raise
    time.sleep(.3)
  p=b.contexts[0].pages[0];measure(p,'native-fullscreen');p.evaluate('()=>window.close()');proc.wait(timeout=20);proc=None;b.close()
  b=pw.chromium.launch(channel='msedge',headless=False,args=['--autoplay-policy=no-user-gesture-required','--force-device-scale-factor=1.25']);context=b.new_context(viewport={'width':1536,'height':960},device_scale_factor=1.25);p=context.new_page();p.goto(f'http://127.0.0.1:{port}/index.html?quality=high',wait_until='load',timeout=180000);measure(p,'edge-browser-same-game');b.close()
 ratio=rows[0]['medianFps']/rows[1]['medianFps'];result=dict(rows=rows,nativeToBrowserRatio=ratio,comparableCanvas=rows[0]['viewport']['canvas']==rows[1]['viewport']['canvas'],noMaterialHostRegression=ratio>=.85,limitations='One available Windows machine, uncaptured seeded Razorback case; not every stage or an FPS guarantee.');(W/'qa/paired-performance.json').write_text(json.dumps(result,indent=2));print('PERFORMANCE_COMPARISON',json.dumps(result),flush=True)
finally:
 if proc and proc.poll()is None:proc.terminate();proc.wait(timeout=15)
 stop()
