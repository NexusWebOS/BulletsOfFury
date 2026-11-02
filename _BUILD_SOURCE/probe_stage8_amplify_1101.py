from pathlib import Path
import sys,json
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import TRAP_RAF
O=R/'_shots/stage8_amplify_1101';checks=[];errors=[];runs=[]
CASES=[('s8interceptor','interceptor'),('mm1003_impharrow','imp'),('mm1003_hexpyre','hexpyre'),('s8voidjet','voidjet'),('s8laserharrier','harrier'),('s8hellwing','hellwing'),('s8parasite','parasite'),('s8crescent','crescent'),('s8hunter','hunter'),('s8skull','skull'),('s8symbiote','symbiote'),('s8warpsentinel','warp'),('s8carrier','carrier'),('s8deathorb','deathorb'),('mm1003_bluehybrid','blue'),('mm1003_furnacemaw','furnacemaw'),('s8bomber','bomber'),('s8tentacle','tentacle')]
SETUP='''t=>{for(const e of enemies)e.dead=true;enemies=[];eBullets=[];pBullets=[];playerLocks=[];S811.events=[];S811.fx=[];S811.blasts=[];S811.bombs.clear();S811.heavy=null;stagePlan=[];waveIdx=999;stageTimer=0;bossWarned=bossDefeated=bossActive=subBossActive=false;thaw=story=fb2Talk=null;CP12.next=VP12.next=CP22.nextWave=CP22.nextFlyby=99999;_adaptiveSpawnT=99999;player.invuln=40002;window.allowS811=true;window.E=spawnEnemy(t,worldWidth()/2,-150,{});window.allowS811=false;return {type:E?.type,hp:E?.hp,model:E?._s811?.model,shield:E?._esh?.max||0};}'''
def ck(n,ok,d=None):checks.append(dict(name=n,passed=bool(ok),data=d));(O/'checks.json').write_text(json.dumps(checks,indent=2));print('PASS'if ok else'FAIL',n,flush=True)
with sync_playwright()as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport=dict(width=1280,height=800));p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:500])if m.type=='error'or'draw error'in m.text else None)
 p.goto('http://127.0.0.1:8805/game/index.html',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5');p.mouse.click(3,3);p.evaluate(TRAP_RAF);p.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'));p.evaluate('EA11.setup(8,"furious")');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(8)&&s811Keys().every(k=>XART.rdy(k))}',timeout=180000)
 p.evaluate('()=>{const spawn=spawnEnemy;spawnEnemy=function(){if(!window.allowS811&&!(window.E?._s811?.phase==="bay"&&arguments[0]==="s8interceptor"))return null;return spawn.apply(this,arguments);};}')
 for diff in['normal','hard','furious']:
  p.evaluate('d=>{diffKey=d;DIFF=difficultyForRun(run.mode,d)}',diff)
  for typ,model in CASES:
   initial=p.evaluate(SETUP,typ);trace=[];seen=set()
   for j in range(64):
    q=p.evaluate('()=>{for(let i=0;i<24;i++){if(E.dead)break;updatePlay(1/60);}drawWorld(0);return {hp:E.hp,dead:E.dead,x:E.x,y:E.y,age:E._s811.age,phase:E._s811.phase,attack:E._s811.attack,dir:E._s811Rendered?.dir,frame:E._s811Rendered?.frame,finite:[E,...eBullets].every(q=>Number.isFinite(q.x)&&Number.isFinite(q.y)),locks:playerLocks.filter(q=>q.src===E).length,beams:E._s811.beams.length};}');trace.append(q);p.wait_for_timeout(3)
    key=str(q.get('attack'))+'-'+q['phase']
    if diff=='furious'and key not in seen and q['phase']in['beam','spin','strike','fire','bay','bombing','lock']:
     p.screenshot(path=str(O/(model+'-'+key+'.png')));seen.add(key)
    if q['dead']:break
   ev=p.evaluate('S811.events');runs.append(dict(diff=diff,type=typ,model=model,initial=initial,trace=trace,events=ev));(O/'runs.json').write_text(json.dumps(runs,indent=2))
   ck(diff+' '+model+' finite native owner/pool',initial['model']==model and all(q['finite']and q['hp']==initial['hp']for q in trace),trace[-1])
   attacked=any(q['phase']in['fire','beam','strike','bay','bombing','lock']for q in trace);ck(diff+' '+model+' actually attacks',attacked,list({q['attack']for q in trace if q.get('attack')}))
   if model=='hexpyre':ck(diff+' Hexpyre only fire arsenal',any(e['event']=='beam-release'and e['flame']for e in ev)and all(e['kind']=='fire-orb'for e in ev if e['event']=='shot')and any(e['event']=='beam-release'and not e['flame']and e['theme']=='fire'for e in ev),[e for e in ev if e['event']=='beam-release'])
   if model=='imp':ck(diff+' Imp uses multiple real depth poses and audible release route',len({q.get('frame')for q in trace if q['phase']=='spin'})>=3 and any(e['event']=='shot'for e in ev))
   if model=='hunter':ck(diff+' Hunter eye beams and actual lash',any(q['phase']=='strike'and q['attack']=='lash'for q in trace)and any(e['event']=='beam-release'and e['theme']=='blue'for e in ev))
   if model=='tentacle':ck(diff+' Tentacle grasps with a real shield and never fires',initial['shield']>0 and any(q['phase']=='strike'for q in trace)and not any(e['event']=='shot'for e in ev))
   if model=='bomber':ck(diff+' Bomber drops physical warned bombs to actual impacts',any(e['event']=='bomb-drop'for e in ev)and any(e['event']=='bomb-impact'for e in ev))
   if model=='hellwing':ck(diff+' Hellwing commits turbo dash',any(q['phase']=='strike'and q['attack']=='turbo'for q in trace))
   if model=='carrier':ck(diff+' Carrier visibly opens and launches distinct aircraft',any(e['event']=='fighter-launch'for e in ev),[e for e in ev if e['event']=='fighter-launch'])
 # Native damaged pixels across every new body/module family, including shields.
 p.evaluate('''()=>{window.alienPixels=()=>{ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);drawEnemy(E);ctx.restore();const a=ctx.getImageData(0,0,cv.width,cv.height).data;let white=0,color=0;for(let i=0;i<a.length;i+=4){if(a[i]>235&&a[i+1]>235&&a[i+2]>235&&a[i+3]>180)white++;if(Math.max(a[i],a[i+1],a[i+2])-Math.min(a[i],a[i+1],a[i+2])>25)color++;}return {white,color};};}''')
 for typ,model in CASES:
  p.evaluate(SETUP,typ);q=p.evaluate('''()=>{for(let i=0;i<80;i++)updatePlay(1/60);E.x=worldWidth()/2;E.y=220;camX=E.x-VW/2;const clean=alienPixels();markHit(E);const hit=alienPixels();for(let i=0;i<30;i++)updatePlay(1/60);E.x=worldWidth()/2;E.y=220;return {clean,hit,expired:alienPixels(),flash:E.flash};}''');ck(model+' actual damaged pixels and expiry',q['hit']['white']>q['clean']['white']+20 and q['expired']['white']<q['hit']['white']and q['flash']<=0,q)
 p.evaluate(SETUP,'s8tentacle');q=p.evaluate('''()=>{for(let i=0;i<30;i++)updatePlay(1/60);const hp=E.hp,energy=E._esh.energy;hitEnemy(E,5);return{hp,after:E.hp,energy,afterEnergy:E._esh.energy,flash:E.flash};}''');ck('Tentacle aura really absorbs damage and flashes',q['hp']==q['after']and q['afterEnergy']<q['energy']and q['flash']>0,q)
 q=p.evaluate('()=>({slug:enemyOrdnanceCanIntercept({_s811Kind:"hell-slug"}),bone:enemyOrdnanceCanIntercept({_s811Kind:"bone"}),laser:enemyOrdnanceCanIntercept({_s811Kind:"laser"}),orb:enemyOrdnanceCanIntercept({_s811Kind:"dark-orb"}),bomb:enemyOrdnanceCanIntercept({_s811Kind:"bomb"}),missile:enemyOrdnanceCanIntercept({_s811Kind:"missile"})})');ck('Birth interception contracts preserve bullets and physical ordnance',not q['slug']and not q['bone']and not q['laser']and q['orb']and q['bomb']and q['missile'],q)
 q=p.evaluate('()=>{window.allowS811=true;const retired=[...S811.retired].map(t=>[t,spawnEnemy(t,340,-150)]);const sonic=spawnEnemy("modturret",340,-80,{_modWeapon:"sonic",_modStage:8});const laser=spawnEnemy("modturret",340,-80,{_modWeapon:"laser",_modStage:8});window.allowS811=false;return {retired:retired.map(([t,e])=>[t,!!e]),sonic:!!sonic,laser:laser?._s811?.model};}');ck('Rejected enemies and ground sonic removed; laser role flies',all(not e[1]for e in q['retired'])and not q['sonic']and q['laser']=='harrier',q)
 ck('No native page/console errors',not errors,errors);b.close()
(O/'errors.json').write_text(json.dumps(errors,indent=2));print('SUMMARY',sum(q['passed']for q in checks),'/',len(checks),flush=True);sys.exit(0 if all(q['passed']for q in checks)else 1)
