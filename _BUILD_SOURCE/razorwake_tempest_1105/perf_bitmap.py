from pathlib import Path
import json,sys
from playwright.sync_api import sync_playwright
W=Path(__file__).resolve().parent;R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import serve
setup="""()=>{diffKey='furious';DIFF=difficultyForRun('arcade',diffKey);run.stage=6;debugUnlocked=true;debugStartFight({stage:6,role:'mini',kind:'razorwake',name:'RAZORWAKE'},{pilot:'cole',record:false});DBGT.god=true;DBGT.speed=1;player.invuln=0;run.weapon=3;run.wlevel=5;run.wlevels=WEAPONS.map(()=>5);run.bombs=40;if(s6Wing)Object.assign(s6Wing,{route:'left',choice:false,fake:null,fakeDone:true,_fb2Talked:true,beats:2,all:true,line:null});spawnSubBoss('razorwake');debugFight.spawned=true;warnT=0;s6Opening=null;fb2Talk=fb2Intro=null;H3.release=false;story=null;BOFCinematicDirector.cancel();setState(GS.PLAY);}"""
port,stop=serve(str(R));out=[]
try:
 with sync_playwright()as pw:
  for mode in ['firing']:
   b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required','--disable-background-timer-throttling','--disable-renderer-backgrounding','--disable-backgrounding-occluded-windows']);p=b.new_page(viewport={'width':1280,'height':800})
   if mode=='prior':p.route('**/assets/razorwake_tempest*',lambda r:r.fulfill(body='"use strict";',content_type='application/javascript'))
   p.goto(f'http://127.0.0.1:{port}/index.html?quality=high',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5');p.mouse.click(3,3);p.evaluate("()=>{diffKey='furious';DIFF=difficultyForRun('arcade',diffKey);run.stage=6;stageLoadBegin(6);}");p.wait_for_function('()=>{stageLoadTick();return fb112Ready()&&stageLoadReady(6)}',timeout=180000);p.evaluate(setup);p.wait_for_timeout(3500)
   p.evaluate("()=>{window.PQA={};for(const n of ['drawWorld','updatePlay','fb112Tick','fb112Draw','rw118Blit','rw117Blit','rw117Weather']){const f=window[n];if(typeof f!=='function')continue;const q=PQA[n]={n:0,ms:0,max:0};window[n]=function(...a){const t=performance.now();try{return f.apply(this,a);}finally{const d=performance.now()-t;q.n++;q.ms+=d;q.max=Math.max(q.max,d);}};}}")
   p.evaluate("()=>{function input(){if(subBoss&&!subBoss.dead){const g=retinaBossTargets(subBoss)[0];Input.keys.j=true;Input.keys.a=g&&player.x>g.x+5;Input.keys.d=g&&player.x<g.x-5;}requestAnimationFrame(input)}requestAnimationFrame(input);}");c=p.context.new_cdp_session(p);c.send('Profiler.enable');c.send('Profiler.start');a=p.evaluate('({t:performance.now(),f:__bofFrames})');p.wait_for_timeout(22000);z=p.evaluate('({t:performance.now(),f:__bofFrames,SS,functions:PQA,memory:performance.memory?{used:performance.memory.usedJSHeapSize,total:performance.memory.totalJSHeapSize}:null})');profile=c.send('Profiler.stop')['profile'];(W/'bitmap-firing.cpuprofile').write_text(json.dumps(profile));row=dict(mode=mode,fps=(z['f']-a['f'])*1000/(z['t']-a['t']),data=z);out.append(row);print(json.dumps(row),flush=True);b.close()
finally:stop()
(W/'bitmap-firing-performance.json').write_text(json.dumps(out,indent=2))
