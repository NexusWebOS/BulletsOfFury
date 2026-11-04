from pathlib import Path
import json,sys
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[2];W=Path(__file__).parent;sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import TRAP_RAF
out=[]
with sync_playwright() as pw:
 for baseline in [True,False]:
  b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1280,'height':800});errors=[];p.on('pageerror',lambda e:errors.append(str(e)))
  p.route('**/assets/online-config.js',lambda r:r.fulfill(status=200,content_type='application/javascript',body='window.BOF_ONLINE_CONFIG={};'))
  if baseline:p.route('**/assets/game.js*',lambda r:r.fulfill(status=200,content_type='application/javascript',body=(W/'game-before-exit.js').read_text(encoding='utf8')))
  p.goto('http://127.0.0.1:65041/game/index.html',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5');p.evaluate(TRAP_RAF);p.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'));p.add_script_tag(path=str(W/'wave_observe_1102.js'));p.evaluate('WO16.start(1)');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(1)}',timeout=180000)
  rows=p.evaluate('''()=>{const rows=[];stagePlan=[];for(const c of [{name:'small exit',y:VH+80,h:null},{name:'visible southern edge',y:VH-8,h:null},{name:'queued north',y:-320,h:null},{name:'large hull still visible',y:VH+81,h:240},{name:'large hull fully departed',y:VH+136,h:240}]){enemies=[];const e=spawnEnemy('s1tanklight',worldWidth()/2,100,{});e.x=worldWidth()/2;e.y=c.y;e._lvlY=levelSrcY()+e.y;e._tank=true;e._phase='shift';e._phT=1000;e._spd=0;e._drawH=e.h;if(c.h)e._groundTrafficSize={w:e.w,h:c.h};_lastScrollDy=1;const score=run.score;updatePlay(1/60);rows.push({name:c.name,alive:enemies.includes(e)&&!e.dead,y:e.y,reward:run.score-score,footprint:groundTrafficFootprint(e)});}return rows;}''')
  out.append({'baseline':baseline,'rows':rows,'errors':errors});b.close()
a=out[0]['rows'];z=out[1]['rows'];assert a[0]['alive'] and not z[0]['alive'],out
assert all(z[i]['alive'] for i in [1,2,3]),out
assert not z[4]['alive'] and all(r['reward']==0 for r in z),out
assert not any(q['errors'] for q in out),out
(W/'ground-exit-probe.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
