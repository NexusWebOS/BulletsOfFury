from pathlib import Path
import sys,json
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import TRAP_RAF
O=R/'_shots/waves_all_1101';errors=[];rows=[];stages=[int(s)for s in sys.argv[1:]]or list(range(1,10))
with sync_playwright()as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:400])if m.type=='error'or'draw error'in m.text else None)
 p.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});");p.goto('http://127.0.0.1:8805/game/index.html',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5');p.mouse.click(3,3);p.evaluate(TRAP_RAF);p.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'));p.add_script_tag(path=str(R/'_BUILD_SOURCE/wave_review_1101.js'))
 for stage in stages:
  setup=p.evaluate('s=>WR15.start(s)',stage);p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(run.stage)}',timeout=180000);trace=[]
  for j in range(650):
   q=p.evaluate('()=>{for(let i=0;i<60;i++){WR15.input(1/60);updatePlay(1/60);if(i%2===1)drawWorld(1/30);}return WR15.snapshot();}');trace.append(q);p.wait_for_timeout(3)
   if j%30==0:print('Stage',stage,round(q['clock']),q['events'],'/',q['expected'],q['input'],flush=True)
   if q['done']or errors or q['state']!='play':break
  rows.append(dict(stage=stage,setup=setup,result=q,trace=trace,events=p.evaluate('WR15.events'),attempts=p.evaluate('WR15.attempts'),spawns=p.evaluate('WR15.spawned')));(O/'coverage.json').write_text(json.dumps(dict(rows=rows,errors=errors),indent=2));p.screenshot(path=str(O/('stage'+str(stage)+'-coverage.png')))
  print('END',stage,q,flush=True)
 b.close()
