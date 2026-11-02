from pathlib import Path
import json,sys
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import TRAP_RAF
from stage9_cases_1101 import SETUP
O=R/'_shots/current_flight_1101';checks=[];errors=[]
def ck(n,ok,d=None):
 checks.append(dict(name=n,passed=bool(ok),data=d));(O/'checks.json').write_text(json.dumps(checks,indent=2));print('PASS'if ok else'FAIL',n,flush=True)
with sync_playwright()as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport=dict(width=1280,height=800));p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'or'draw error'in m.text else None);p.on('response',lambda r:errors.append(str(r.status)+' '+r.url)if r.status>=400 else None)
 p.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});");p.goto('http://127.0.0.1:8805/game/index.html',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5');p.mouse.click(3,3);p.evaluate(TRAP_RAF);p.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'));p.evaluate('EA11.setup(9,"furious")');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(9)&&s911Keys().every(k=>XART.rdy(k))}',timeout=180000)
 p.evaluate('()=>{const spawn=spawnEnemy;spawnEnemy=function(){return window.allowS911?spawn.apply(this,arguments):null;};}')
 for diff in['normal','hard','furious']:
  p.evaluate('d=>{diffKey=d;DIFF=difficultyForRun(run.mode,d)}',diff);init=p.evaluate(SETUP,dict(type='cbreak',model='current',role=None));rows=[];seen=set()
  for j in range(85):
   q=p.evaluate('''()=>{for(let i=0;i<24;i++)updatePlay(1/60);drawWorld(0);return{hp:E.hp,x:E.x,y:E.y,phase:E._s911.phase,attack:E._s911.attack,render:E._s911Rendered,finite:[E,...eBullets].every(e=>Number.isFinite(e.x+e.y))};}''');rows.append(q);p.wait_for_timeout(3)
   tag=q['render'].get('view','front')+'-'+q['phase']
   if diff=='furious'and tag not in seen:
    p.screenshot(path=str(O/(tag+'.png')));seen.add(tag)
  ck(diff+' actual native flight uses overhead body and perspective transitions',any(q['render'].get('view')=='overhead'for q in rows)and any(q['render'].get('view')=='tilt'for q in rows)and all(q['finite']and q['hp']==init['hp']for q in rows),dict(views=sorted({q['render'].get('view')for q in rows}),hp=init['hp']))
  ck(diff+' standing transformation and casts remain frontal',all(q['render']['dir']==0 and q['render'].get('view')=='front'for q in rows if q['phase']in['transform','fire']),None)
  ev=p.evaluate('S911.events');ck(diff+' native wave/grenade/mist attack book remains complete',any(v['event']=='wave-release'for v in ev)and any(v.get('kind')=='grenade'for v in ev)and any(v.get('kind')=='mist'for v in ev))
 # Actual hand pixels and whole-bank damage/expiry in all eight authored views.
 p.evaluate(SETUP,dict(type='cbreak',model='current',role=None));p.evaluate('''()=>{E.x=worldWidth()/2;E.y=230;Object.assign(E._s911,{human:true,phase:'flight',t:.7,attack:'superman',start:{x:E.x,y:E.y},target:{x:E.x,y:VH-65}});camX=E.x-VW/2;window.flightWhite=()=>{ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);drawEnemy(E);ctx.restore();const a=ctx.getImageData(0,0,cv.width,cv.height).data;let white=0;for(let i=0;i<a.length;i+=4)if(a[i]>235&&a[i+1]>235&&a[i+2]>235&&a[i+3]>180)white++;return white;};}''')
 for d in range(8):
  q=p.evaluate('''d=>{E._s911.head=Math.PI/2+d*TAU/8;E._s911.t=.7;E.flash=0;const p=cf111Plate(E),guns=s911Guns(E),on=guns.map(g=>s911OpaqueAt(E,g.x,g.y,1)),clean=flightWhite(),hp=E.hp;hitEnemy(E,1);const hit=flightWhite();return{d:p.dir,key:p.B.key,on,clean,hit,hp,after:E.hp};}''',d);ck('Direction'+str(d)+' selects its authored body and real palm sockets',q['d']==d and all(q['on']),q);ck('Direction'+str(d)+' actual damage visibly flashes the new body',q['after']<q['hp']and q['hit']>q['clean']+20,q)
 q=p.evaluate('''()=>{const M=s911M(E),a=s811Alpha({B:M.flightLaunch,f:0,angle:Math.PI/2}),b=s811Alpha({B:M.bank,f:4,angle:Math.PI/2}),c=s811Alpha({B:M.flightLaunch,f:7,angle:Math.PI/2}),d=s811Alpha({B:M.flight,f:0,angle:Math.PI/2}),r=s811Alpha({B:M.flightReturn,f:7,angle:Math.PI/2}),idle=s811Alpha({B:M.bank,f:0,angle:Math.PI/2});return{launch:a.every((v,i)=>v===b[i]),overhead:c.every((v,i)=>v===d[i]),idle:r.every((v,i)=>v===idle[i]),dirs:M.flight.dirs,authored:M.flight.authoredDirections};}''');ck('Launch, overhead and recovery endpoints share exact actual pixels',q['launch']and q['overhead']and q['idle']and q['authored']and q['dirs']==8,q)
 q=p.evaluate('''()=>{for(let i=0;i<40;i++)updatePlay(1/60);return E.flash;}''');ck('Flight hit flash expires through the native updater',q<=0,q)
 q=p.evaluate('''()=>{E._s911.phase='flight';E._s911.t=.6;const before=cf111Plate(E).view;bossActive=true;for(let i=0;i<20;i++)updatePlay(1/60);bossActive=false;return{before,cancelled:E._s911.cancelled,beams:E._s911.beams.length};}''');ck('Native encounter handoff still cancels the flight owner',q['before']=='overhead'and q['cancelled']and q['beams']==0,q)
 ck('No native browser/asset/console errors',not errors,errors);b.close()
a=json.load(open(O/'art-before.json'));z=json.load(open(R/'assets/game/levels/stage_09/enemies/amplify_1101/manifest.json'));ck('Other18 enemy banks and canonical standing/morph art are unchanged',all(a['models'][n]==z['models'][n]for n in a['models']if n!='current')and all(a['models']['current'][k]==z['models']['current'][k]for k in['bank','glow','morph','poseGuns']),None)
print('SUMMARY',sum(v['passed']for v in checks),'/',len(checks));sys.exit(0 if all(v['passed']for v in checks)else 1)
