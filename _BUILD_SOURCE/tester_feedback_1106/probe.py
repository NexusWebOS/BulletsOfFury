from pathlib import Path
import sys, json, time, argparse
from playwright.sync_api import sync_playwright

R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury')
W=Path(__file__).resolve().parent
sys.path.insert(0,str(R/'_BUILD_SOURCE'))
import shoot
ap=argparse.ArgumentParser(); ap.add_argument('--label',default='before'); ap.add_argument('--headless',action='store_true'); a=ap.parse_args()
O=W/a.label; O.mkdir(exist_ok=True)
port,stop=shoot.serve(str(R)); results={}; errors=[]
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge',headless=a.headless,args=['--autoplay-policy=no-user-gesture-required'])
  p=b.new_page(viewport={'width':1366,'height':768}); p.on('pageerror',lambda e:errors.append(str(e)))
  p.add_init_script('''window.FB116={media:[],frames:[],long:[],last:0};
   new PerformanceObserver(l=>{for(const e of l.getEntries())FB116.long.push({at:e.startTime,ms:e.duration});}).observe({type:'longtask',buffered:true});
   const play=HTMLMediaElement.prototype.play;
   HTMLMediaElement.prototype.play=function(){const e=this,t=performance.now(),q={at:t,src:e.src.split('/').pop().slice(0,90),ready:e.readyState};FB116.media.push(q);e.addEventListener('playing',()=>{q.started=performance.now()-t;},{once:true});return play.apply(this,arguments);};
   function sample(t){if(FB116.last)FB116.frames.push({at:t,ms:t-FB116.last});FB116.last=t;requestAnimationFrame(sample);}requestAnimationFrame(sample);''')
  p.goto(f'http://127.0.0.1:{port}/index.html?quality=high',timeout=180000)
  p.wait_for_function('window.__bofFrames>4',timeout=180000); p.mouse.click(2,2)
  p.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'))
  results['boot']=p.evaluate('()=>({seconds:performance.now()/1000,SS,VW,VH,state,voices:Snd._sfxVoices.length})')
  print('BOOT',results['boot'],flush=True)
  # Native tutorial completion -> campaign map, without changing its continuations.
  results['map']=p.evaluate('''()=>{run.mode='campaign';run.pilot='axel';run.diff='normal';campaign.unlockedMax=1;
   tutStart({stage:1,lead:'axel',disp:'axel'});tutFinish(true);
   return {state,mode:run.mode,boot:typeof sselBoot==='number'?sselBoot:null,focus:typeof cmap2==='object'?cmap2.focus:null,campPause,stage:run.stage};}''')
  p.wait_for_timeout(12000)
  p.screenshot(path=str(O/'campaign.png'))
  results['mapAfterBoot']=p.evaluate('()=>({state,stateT,sselBoot,focus:cmap2.focus,bar:cmap2.bar,campPause,rects:cmap2._btnRects,mouse:Input.mouse})')
  print('MAP',results['map'],results['mapAfterBoot'],flush=True)
  # Stage 5 cold start, preserving the actual loading/launch clocks.
  client=p.context.new_cdp_session(p);client.send('Profiler.enable');client.send('Profiler.start')
  p.evaluate('''()=>{FB116.frames=[];FB116.long=[];FB116.media=[];FB116.start=performance.now();run.mode='arcade';run.pilot='axel';run.diff='furious';beginStage(5);DBGT.god=true;}''')
  p.wait_for_timeout(15000)
  results['spaceEntry']=p.evaluate('''()=>({state,time:stageTimer,load:stageLoadInfo(5),frames:FB116.frames,long:FB116.long,media:FB116.media,heap:performance.memory?.usedJSHeapSize,pBullets:pBullets.length,eBullets:eBullets.length,enemies:enemies.length,SS})''')
  profile=client.send('Profiler.stop')['profile'];(O/'space-entry.cpuprofile').write_text(json.dumps(profile),encoding='utf8')
  p.screenshot(path=str(O/'space-entry.png'))
  # Stable combat, held fire; compare a fixed native opening at SS2.
  p.evaluate('''()=>{EA11.setup(5,'furious');stagePlan=[];waveIdx=0;CP12.next=VP12.next=CP22.nextWave=CP22.nextFlyby=99999;_adaptiveSpawnT=99999;
   run.weapon=0;run.wlevel=3;run.wlevels=WEAPONS.map(()=>3);FB116.start=performance.now();FB116.frames=[];FB116.long=[];FB116.media=[];
   FB116.down=Input.down;Input.down=function(k){return keybind.fire.includes(k)||FB116.down.call(Input,k);};}''')
  p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(5)}',timeout=180000,polling=100)
  client.send('Profiler.start');p.wait_for_timeout(14000)
  results['spaceCombat']=p.evaluate('''()=>({state,time:stageTimer,frames:FB116.frames,long:FB116.long,media:FB116.media,heap:performance.memory?.usedJSHeapSize,pBullets:pBullets.length,eBullets:eBullets.length,enemies:enemies.length,SS,voices:Snd._sfxVoices.length})''')
  (O/'space-combat.cpuprofile').write_text(json.dumps(client.send('Profiler.stop')['profile']),encoding='utf8')
  p.evaluate('()=>{Input.down=FB116.down;}')
  results['errors']=errors
  (O/'results.json').write_text(json.dumps(results,indent=2),encoding='utf8')
  for name in ['spaceEntry','spaceCombat']:
   q=results[name]; ms=sorted(e['ms'] for e in q['frames']); audio=[e['started'] for e in q['media'] if 'started'in e]
   print(name,json.dumps({k:v for k,v in q.items() if k not in ['frames','long','media']}),json.dumps(dict(frames=len(ms),p50=ms[len(ms)//2],p95=ms[int(len(ms)*.95)],worst=ms[-1],longTasks=sorted(q['long'],key=lambda e:e['ms'])[-8:],audioCalls=len(q['media']),audioStarted=len(audio),audioP95=sorted(audio)[int(len(audio)*.95)] if audio else None)),flush=True)
  b.close()
finally: stop()
