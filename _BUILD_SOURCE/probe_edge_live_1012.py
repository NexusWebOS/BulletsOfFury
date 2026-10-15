from pathlib import Path
import sys,json
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
O=R/'_shots/performance_1012/live';O.mkdir(parents=True,exist_ok=True)
port,stop=shoot.serve(str(R));errors=[];results=[]
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge',args=['--mute-audio'])
  for stage in [1,6]:
   p=b.new_page(viewport={'width':1366,'height':768})
   p.route('**/favicon.ico',lambda route:route.fulfill(status=204,body=''))
   p.on('pageerror',lambda e:errors.append(str(e)))
   p.on('console',lambda m:errors.append(m.text) if m.type=='error' else None)
   p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('window.__bofFrames>4',timeout=120000)
   p.evaluate(shoot.TRAP_RAF);p.wait_for_timeout(50)
   p.evaluate(shoot.SETUP,{'state':'PLAY','stage':stage,'pilot':'cole','invuln':True})
   p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(run.stage)&&XART.rdy(SC12_ART.key)&&bmfReady("game");}',timeout=120000)
   p.evaluate('''()=>{s6Opening=null;run._mission29OpeningDone=true;run.weapon=0;run.wlevel=6;run.wlevels=WEAPONS.map(()=>6);run._cfUnlocked=6;story=null;
    window.LP12={frames:0,dt:[],work:[],peakP:0,peakE:0,peakFx:0,active:true};const original=loop;
    loop=function(now){if(!LP12.active)return;const q=LP12;q.frames++;q.dt.push(now-last);
     for(const name of ['left','right','fire'])for(const k of keybindFor(1)[name]||[])if(!k.startsWith('pad_'))Input.keys[k]=name==='fire'||(name==='right')===(Math.floor(q.frames/60)%2===0);
     if(q.frames%60===0)for(let i=0;i<3;i++)explode(player.x+(i-1)*40,player.y-100-i*20,55,'orange',null,null,null,null,true);
     const t=performance.now();original(now);q.work.push(performance.now()-t);q.peakP=Math.max(q.peakP,pBullets.length);q.peakE=Math.max(q.peakE,eBullets.length);q.peakFx=Math.max(q.peakFx,particles.length+explosions.length);
     if(q.frames>=240){q.active=false;requestAnimationFrame=()=>0;}};
    requestAnimationFrame=__bofRealRAF;last=performance.now();requestAnimationFrame(loop);}''')
   p.wait_for_function('LP12.frames>=240',timeout=120000)
   q=p.evaluate('''()=>{const a=LP12.work.slice(20).sort((a,b)=>a-b),d=LP12.dt.slice(20);return{stage:run.stage,frames:LP12.frames,averageSubmissionMs:a.reduce((x,y)=>x+y,0)/a.length,p95SubmissionMs:a[Math.floor(a.length*.95)],rafFps:1000/(d.reduce((x,y)=>x+y,0)/d.length),peakPlayerShots:LP12.peakP,peakEnemyShots:LP12.peakE,peakEffects:LP12.peakFx,renderScale:SS,state,finite:Number.isFinite(player.x)&&Number.isFinite(player.y)};}''')
   results.append(q);print(json.dumps(q),flush=True)
   assert q['finite'] and q['peakPlayerShots']>0 and q['peakEffects']>0 and q['state']=='play',q
   p.screenshot(path=str(O/f'stage{stage}.png'));p.close()
  b.close()
finally:stop()
(O/'verification.json').write_text(json.dumps({'results':results,'errors':errors},indent=2),encoding='utf-8')
assert not errors,errors
