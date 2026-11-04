from pathlib import Path
import json,sys,ast
from playwright.sync_api import sync_playwright
W=Path(__file__).parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury')
sys.path.insert(0,str(R/'_BUILD_SOURCE'))
from shoot import TRAP_RAF
OBS=Path(r'C:/Users/Mike/Documents/New project/BOF-Wave-Observe-1102')
errors=[];results=[]
def stats(v):
 v=sorted(v);return {'mean':sum(v)/len(v),'p95':v[int((len(v)-1)*.95)],'max':v[-1]}
with sync_playwright() as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required','--disable-background-timer-throttling','--disable-renderer-backgrounding'])
 p=b.new_page(viewport={'width':1280,'height':800})
 p.route('**/assets/online-config.js',lambda r:r.fulfill(status=200,content_type='application/javascript',body='window.BOF_ONLINE_CONFIG={};'))
 p.on('pageerror',lambda e:errors.append(str(e)))
 p.goto('http://127.0.0.1:65041/game/index.html',wait_until='load',timeout=180000)
 p.wait_for_function('window.__bofFrames>5',timeout=60000);p.evaluate(TRAP_RAF)
 p.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'))
 p.add_script_tag(path=str(OBS/'reference_wave_maps.js'));p.add_script_tag(path=str(OBS/'wave_observe_1102.js'))
 for stage in ([5] if len(sys.argv)>1 else [1,7,5,9]):
  for scale in [1,2]:
   p.evaluate('(s)=>WO16.start(s)',stage)
   p.wait_for_function('(s)=>{stageLoadTick();return stageLoadReady(s)}',arg=stage,timeout=180000)
   cdp=p.context.new_cdp_session(p);cdp.send('Profiler.enable');cdp.send('Profiler.start')
   p.evaluate('(n)=>{setRenderScale(n);if(run.stage===5||run.stage===9){run.spaceMode=true;gravityMode={...GRAVITY_SHIP_ACTIVE,narrative:false};furyShipWarm();}window.qualityPerf={gap:[],update:[],draw:[],running:true};let prev=performance.now(),debt=0,warm=0;function f(now){if(!qualityPerf.running)return;const gap=now-prev;prev=now;debt+=Math.min(.05,gap/1000);let n=0;const a=performance.now();stageLoadTick();while(debt>=1/60&&n<3){WO16.input(1/60);stateT+=1/60;updatePlay(1/60);debt-=1/60;n++;}const b=performance.now();ctx.setTransform(SS,0,0,SS,0,0);ctx.imageSmoothingEnabled=false;drawWorld(n/60);if(warm++>120){qualityPerf.gap.push(gap);qualityPerf.update.push(b-a);qualityPerf.draw.push(performance.now()-b);}window.__bofRealRAF(f);}window.__bofRealRAF(f);}',scale)
   p.wait_for_timeout(12000)
   q=p.evaluate('()=>{qualityPerf.running=false;return {stage:run.stage,SS,perf:qualityPerf,state:WO16.snapshot()}}')
   profile=cdp.send('Profiler.stop')['profile'];(W/f'profile-{stage}-{scale}.cpuprofile').write_text(json.dumps(profile),encoding='utf8');cdp.detach()
   q['stats']={k:stats(v)for k,v in q.pop('perf').items()if isinstance(v,list) and v}
   q['fps']=1000/q['stats']['gap']['mean'];results.append(q)
   print(json.dumps({'stage':stage,'SS':scale,'fps':q['fps'],'draw':q['stats']['draw']}),flush=True)
   if scale==2:p.locator('#screen').screenshot(path=str(W/f'live-stage-{stage}.png'))
 b.close()
(W/('performance-space-isolated.json' if len(sys.argv)>1 else 'performance.json')).write_text(json.dumps({'scenes':results,'errors':errors},indent=2),encoding='utf8')
assert not errors
