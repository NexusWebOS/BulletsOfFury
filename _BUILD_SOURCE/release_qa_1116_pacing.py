from pathlib import Path
from playwright.sync_api import sync_playwright
import sys,json,time
R=Path(__file__).resolve().parents[1];O=R/'_shots/release_qa_1116/pacing';O.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
rows=[];errors=[]
with sync_playwright()as w:
 b=w.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required'])
 for stage in [5,6,8,9]:
  context=b.new_context(viewport={'width':1440,'height':1000});p=context.new_page();p.set_default_timeout(180000);local=[]
  p.on('pageerror',lambda e:local.append(str(e)));p.on('console',lambda m:local.append(m.text)if m.type=='error'else None);p.on('response',lambda r:local.append(str(r.status)+' '+r.url)if r.status>=400 else None)
  t=time.monotonic();p.goto('http://127.0.0.1:8765/index.html?release-pacing=1116',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>6');boot=time.monotonic()-t
  p.evaluate(shoot.TRAP_RAF);p.evaluate("s=>{BOFOnline.submitScore=()=>{};BOSSMODE.start(s,'boss','cole',false,'furious');player.invuln=1e8;player._spawnClearT=1e8;}",stage);p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(run.stage)}',polling=50)
  # Native entry/warning before the real-wall-clock first-form sample.
  for i in range(120):p.evaluate(shoot.STEP,6);p.wait_for_timeout(1)
  p.evaluate("()=>{window.Pace16={deltas:[],longTasks:[],start:performance.now(),old:performance.now(),frames:window.__bofFrames};try{new PerformanceObserver(l=>Pace16.longTasks.push(...l.getEntries().map(e=>e.duration))).observe({type:'longtask',buffered:false});}catch(e){};window.requestAnimationFrame=window.__bofRealRAF;last=performance.now();window.pace16Tick=t=>{if(!Pace16.end){Pace16.deltas.push(t-Pace16.old);Pace16.old=t;requestAnimationFrame(pace16Tick);}};requestAnimationFrame(pace16Tick);requestAnimationFrame(loop);}")
  p.keyboard.down('j');p.wait_for_timeout(20000);p.keyboard.up('j')
  q=p.evaluate("()=>{Pace16.end=performance.now();const ds=Pace16.deltas.slice(1).sort((a,b)=>a-b),pct=u=>ds[Math.min(ds.length-1,Math.floor(ds.length*u))]||null;return{stage:run.stage,state,kind:boss?.kind,hp:boss?.hp,dead:player.dead,frames:window.__bofFrames-Pace16.frames,wallSeconds:(Pace16.end-Pace16.start)/1000,medianMs:pct(.5),p95Ms:pct(.95),p99Ms:pct(.99),longTasks:Pace16.longTasks,resourceCount:performance.getEntriesByType('resource').length,jsRequests:performance.getEntriesByType('resource').filter(r=>/\\.js(?:[?]|$)/.test(r.name)).length};}");q.update({'coldBootSeconds':boot,'errors':local});rows.append(q);errors.extend(local);p.screenshot(path=str(O/f'furious-stage{stage}.jpg'),type='jpeg',quality=86);print(json.dumps(q),flush=True);context.close()
 b.close()
(O/'report.json').write_text(json.dumps({'rows':rows,'errors':errors,'scope':'Four fresh isolated Chromium contexts, real wall-clock native RAF first-form samples with held primary,20 seconds each after native entry. Protected stationary fixture. Headless software-rendering measurements are diagnostic, not target-hardware FPS certification or full fights.'},indent=2),encoding='utf8')
