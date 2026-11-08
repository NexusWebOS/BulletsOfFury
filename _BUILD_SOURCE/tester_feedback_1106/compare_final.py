from pathlib import Path
import sys,json,time,statistics
from playwright.sync_api import sync_playwright
R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');W=Path(__file__).resolve().parent
sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
port,stop=shoot.serve(str(R));out=[]
def metrics(ms):
 ms=sorted(ms);return dict(frames=len(ms),p50=ms[len(ms)//2],p95=ms[int(len(ms)*.95)],p99=ms[int(len(ms)*.99)],worst=ms[-1],over50=sum(x>50 for x in ms),averageFps=1000/statistics.mean(ms))
try:
 with sync_playwright()as pw:
  for label in ['baseline','repaired']:
   b=pw.chromium.launch(channel='msedge',args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1366,'height':768});errors=[]
   if label=='baseline':
    for f in ['assets/game.js','assets/pixel_glow_1015.js','assets/campaign_controls_1004h.js']:
     p.route('**/'+f+'*',lambda route,request,f=f:route.fulfill(path=str(W/'original'/f),content_type='text/javascript'))
    p.route('**/assets/space_pages_art_1106.js*',lambda route:route.fulfill(status=200,body='',content_type='text/javascript'))
    p.route('**/assets/space_pages_1106.js*',lambda route:route.fulfill(status=200,body='',content_type='text/javascript'))
    p.route('**/assets/audio_latency_1106.js*',lambda route:route.fulfill(status=200,body='',content_type='text/javascript'))
   p.on('pageerror',lambda e:errors.append(str(e)))
   p.add_init_script('''window.P116={ms:[],long:[],at:0,last:0,active:false};new PerformanceObserver(l=>{if(P116.active)for(const q of l.getEntries())P116.long.push(q.duration);}).observe({type:'longtask'});
    function tick(t){if(P116.active&&P116.last)P116.ms.push(t-P116.last);P116.last=t;requestAnimationFrame(tick);}requestAnimationFrame(tick);''')
   p.goto(f'http://127.0.0.1:{port}/index.html?quality=high',timeout=180000);p.wait_for_function('window.__bofFrames>5',timeout=180000);p.mouse.click(2,2)
   setup=p.evaluate('''()=>{run.mode='arcade';run.pilot='axel';diffKey='furious';run.gravityShipReady=false;P116.ms=[];P116.last=0;P116.long=[];P116.active=true;P116.at=performance.now();const t=performance.now();beginStage(5);DBGT.god=true;return performance.now()-t;}''')
   p.wait_for_function('state===GS.PLAY&&stageLoadReady(5)',timeout=180000,polling=100)
   entry=p.evaluate('()=>({ms:P116.ms,long:P116.long,elapsed:performance.now()-P116.at,load:stageLoadInfo(5),ss:SS})')
   p.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'))
   p.evaluate('''()=>{EA11.setup(5,'furious');run.pilot='axel';pilotIndex=0;PILOTMOD={...PILOTS[0]};let seed=116;Math.random=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/4294967296;};
    run.spaceWeapon=0;run.spaceLevels=[3,1,1,0,0];run.weapon=0;run.wlevel=3;P116.ms=[];P116.last=0;P116.long=[];P116.active=true;P116.at=performance.now();
    P116.down=Input.down;Input.down=function(k){return keybind.fire.includes(k)||P116.down.call(Input,k);};
    if(typeof AL116!=='undefined')AL116.events=[];
   }''')
   p.wait_for_timeout(22000)
   combat=p.evaluate('''()=>({ms:P116.ms,long:P116.long,time:stageTimer,enemies:enemies.length,enemyShots:eBullets.length,playerShots:pBullets.length,heap:performance.memory?.usedJSHeapSize,voices:Snd._sfxVoices.length,
    paging:typeof SP116==='undefined'?null:{draws:SP116.draws,misses:SP116.misses,fallbacks:SP116.fallbacks,bytes:SP116.bytes},sound:typeof AL116==='undefined'?null:{events:AL116.events,stats:AL116.stats,errors:AL116.errors,bytes:AL116.bytes},ss:SS})''')
   row=dict(label=label,setupMs=setup,entry=metrics(entry.pop('ms')),entryInfo=entry,combat=metrics(combat.pop('ms')),combatInfo=combat,errors=errors)
   out.append(row);(W/'comparison-final.json').write_text(json.dumps(out,indent=2),encoding='utf8');print(label,json.dumps({k:v for k,v in row.items()if k not in ['combatInfo','entryInfo']}),flush=True)
   p.screenshot(path=str(W/(label+'-space.png')));b.close()
finally:stop()
