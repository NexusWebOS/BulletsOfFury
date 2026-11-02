from pathlib import Path
import sys,json
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import TRAP_RAF
from stage9_cases_1101 import CASES,SETUP
O=R/'_shots/stage9_amplify_1101';checks=[];errors=[];runs=[]
def ck(n,ok,d=None):
 checks.append(dict(name=n,passed=bool(ok),data=d));(O/'checks.json').write_text(json.dumps(checks,indent=2));print('PASS'if ok else'FAIL',n,flush=True)
with sync_playwright()as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport=dict(width=1280,height=800));p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'or'draw error'in m.text else None);p.on('response',lambda r:errors.append(str(r.status)+' '+r.url)if r.status>=400 else None)
 p.add_init_script("Object.defineProperty(navigator,'getGamepads',{value:()=>[]});");p.goto('http://127.0.0.1:8805/game/index.html',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5');p.mouse.click(3,3);p.evaluate(TRAP_RAF);p.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'));p.evaluate('EA11.setup(9,"furious")');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(9)&&s911Keys().every(k=>XART.rdy(k))}',timeout=180000)
 p.evaluate('()=>{const spawn=spawnEnemy;spawnEnemy=function(){return window.allowS911?spawn.apply(this,arguments):null;};}')
 for diff in['normal','hard','furious']:
  p.evaluate('d=>{diffKey=d;DIFF=difficultyForRun(run.mode,d)}',diff)
  for cid,typ,model,role,title,seconds in CASES:
   initial=p.evaluate(SETUP,dict(type=typ,model=model,role=role));trace=[];seen=set()
   for j in range(76):
    q=p.evaluate('()=>{for(let i=0;i<24;i++){if(E.dead)break;updatePlay(1/60);}drawWorld(0);return{hp:E.hp,dead:E.dead,x:E.x,y:E.y,age:E._s911.age,phase:E._s911.phase,attack:E._s911.attack,dir:E._s911Rendered?.dir,pose:E._s911Rendered?.pose,beams:E._s911.beams.length,finite:[E,...eBullets].every(q=>Number.isFinite(q.x+q.y))};}');trace.append(q);p.wait_for_timeout(3)
    key=str(q.get('attack'))+'-'+q['phase']
    if diff=='furious'and key not in seen and q['phase']in['beam','fire','flight','transform','dash','pass']:
     p.screenshot(path=str(O/(model+'-'+key+'.png')));seen.add(key)
    if q['dead']:break
   ev=p.evaluate('S911.events');runs.append(dict(diff=diff,id=cid,type=typ,model=model,initial=initial,trace=trace,events=ev));(O/'runs.json').write_text(json.dumps(runs,indent=2))
   ck(diff+' '+model+' finite native pool',initial['model']==model and all(v['finite']and v['hp']==initial['hp']for v in trace),trace[-1]);ck(diff+' '+model+' actually attacks',any(v['event']in['shot','beam-release','wave-release']for v in ev))
   if model=='beacon':
    shots=[v for v in ev if v['event']=='shot'];ck(diff+' Beacon releases exact nine-way volleys',bool(shots)and len(shots)%9==0 and len({round(v['angle'],3)for v in shots[:9]})==9,dict(shots=len(shots),angles=[v['angle']for v in shots[:9]]));ck(diff+' Beacon spins and has a real shield',initial['shield']>0 and len({v.get('dir')for v in trace})>3)
   if model in['beamship','harrier']:ck(diff+' '+model+' exact paired/four measured beams',any(v['event']=='beam-release'and v['lanes']==(2 if model=='beamship'else 4)for v in ev),[v for v in ev if v['event']=='beam-release'])
   if model=='manta':ck(diff+' Manta has no shield',initial['shield']==0)
   if model=='current':ck(diff+' Current Breaker transforms and uses all three attacks while facing us',any(v['event']=='water-human-complete'for v in ev)and all(v.get('dir')==0 for v in trace)and {'tidal-waves','grenades','superman'}.issubset({v.get('attack')for v in trace}),dict(attacks=list({v.get('attack')for v in trace}),dirs=list({v.get('dir')for v in trace})))
   if model=='minelayer':ck(diff+' Real mines stay after the laying jet departs',any(v.get('kind')=='mine'for v in ev if v['event']=='shot')and any(v['dead']for v in trace),[v for v in ev if v['event']=='shot'])
 # Damaged pixels and actual expiry in the native renderer for all19 identities.
 p.evaluate('''()=>{window.pixels9=()=>{ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);drawEnemy(E);ctx.restore();const a=ctx.getImageData(0,0,cv.width,cv.height).data;let white=0;for(let i=0;i<a.length;i+=4)if(a[i]>235&&a[i+1]>235&&a[i+2]>235&&a[i+3]>180)white++;return white;};}''')
 for cid,typ,model,role,title,seconds in CASES:
  p.evaluate(SETUP,dict(type=typ,model=model,role=role));q=p.evaluate('''()=>{E.x=worldWidth()/2;E.y=220;camX=E.x-VW/2;const clean=pixels9();markHit(E);const hit=pixels9();for(let i=0;i<30;i++)updatePlay(1/60);E.x=worldWidth()/2;E.y=220;return{clean,hit,expired:pixels9(),flash:E.flash};}''');ck(model+' visible hit pixels and expiry',q['hit']>q['clean']+10 and q['expired']<q['hit']and q['flash']<=0,q)
 q=p.evaluate('()=>Object.fromEntries(["slug","laser-orb","mist","wave","mine","grenade"].map(k=>[k,enemyOrdnanceCanIntercept({_s911Kind:k})]))');ck('Birth rules preserve ordinary water rounds and physical mine/grenade interception',all(not q[k]for k in['slug','laser-orb','mist','wave'])and q['mine']and q['grenade'],q)
 ck('No native browser/console/asset errors',not errors,errors);b.close()
(O/'errors.json').write_text(json.dumps(errors,indent=2));print('SUMMARY',sum(v['passed']for v in checks),'/',len(checks),flush=True);sys.exit(0 if all(v['passed']for v in checks)else 1)
