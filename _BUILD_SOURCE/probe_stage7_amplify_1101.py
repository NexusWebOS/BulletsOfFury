"""Native Stage7 generated modules, socket releases and actual damaged pixels."""
from pathlib import Path
import sys,json
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import TRAP_RAF
O=R/'_shots/stage7_amplify_1101';O.mkdir(exist_ok=True);checks=[];errors=[];runs=[]
def ck(n,ok,d=None):
 checks.append(dict(name=n,passed=bool(ok),data=d));print('PASS'if ok else'FAIL',n,flush=True)
 (O/'checks.json').write_text(json.dumps(checks,indent=2))
specs=json.loads((R/'_shots/enemy_flight_1031/before/stage7-specs.json').read_text())
specs=[s for s in specs if s['type']!='ll18raptor'and s['type']!='cp22drone']
specs+=[dict(type='s7missilejet',pattern='s7toxic',map=1120,x=340,y=-150,opt={}),dict(type='s8crescent',pattern='s7toxic',map=500,x=340,y=-130,opt={})]
SETUP='''s=>{window.allowS711=true;EA11.case(s);window.allowS711=false;bossWarned=false;thaw=story=fb2Talk=null;CP12.next=VP12.next=CP22.nextWave=CP22.nextFlyby=99999;_adaptiveSpawnT=99999;player.invuln=40002;playerLocks=[];S711.events=[];S711.fx=[];if(E._s711?.model==='ground'){E._s711.anchor.y=levelSrcY()+160;E._modTurret.mapY=E._s711.anchor.y;E.y=160;}return {type:E.type,hp:E.hp,x:E.x,y:E.y,model:E._s711?.model,shield:E._esh?.max||0};}'''
with sync_playwright()as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:500])if m.type=='error'or'draw error'in m.text else None)
 p.goto('http://127.0.0.1:8805/game/index.html',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5');p.mouse.click(3,3);p.evaluate(TRAP_RAF);p.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'));p.evaluate('EA11.setup(7,"furious")');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(7)&&Object.values(S711_ART.banks).every(B=>XART.rdy(B.key))}',timeout=180000)
 p.evaluate('()=>{const spawn=spawnEnemy;spawnEnemy=function(){if(!window.allowS711)return null;return spawn.apply(this,arguments);};}')
 for diff in['normal','hard','furious']:
  p.evaluate('d=>{diffKey=d;DIFF=difficultyForRun(run.mode,d)}',diff)
  for idx,s in enumerate(specs):
   initial=p.evaluate(SETUP,s);trace=[];seen=set()
   for j in range(76):
    q=p.evaluate('()=>{for(let i=0;i<24;i++){if(E.dead)break;updatePlay(1/60);}drawWorld(0);return {x:E.x,y:E.y,hp:E.hp,dead:E.dead,age:E._s711?.age,phase:E._s711?.phase,dir:E._s711Rendered?.dir,frame:E._s711Rendered?.frame,face:E._s711Rendered?.face,head:E._s711?.head,shots:eBullets.filter(b=>b._s711Owner===E).length,locks:playerLocks.filter(L=>L.src===E).length,finite:[E,...eBullets].every(q=>Number.isFinite(q.x)&&Number.isFinite(q.y))};}');trace.append(q);p.wait_for_timeout(3)
    if diff=='furious'and q.get('phase')not in seen and q.get('phase')in['fire','roll','claw','mouth-fire','lock','rev','tell']:
     p.screenshot(path=str(O/(str(idx)+'-'+s['type']+'-'+q['phase']+'.png')));seen.add(q['phase'])
    if q['dead']:break
   events=p.evaluate('S711.events');runs.append(dict(diff=diff,spec=s,initial=initial,trace=trace,events=events));(O/'runs.json').write_text(json.dumps(runs,indent=2))
   name=diff+' '+initial['type']+' '+str(idx)
   ck(name+' owns finite motion and retained hull pool',initial.get('model')is not None and all(q['finite']and q['hp']==initial['hp']for q in trace),trace[-1])
   shots=[e for e in events if e['event']=='shot'];ck(name+' launches real ordnance',bool(shots),shots[-2:])
   if initial['model']in['tank','crawler','relay','slime','barge']:
    ck(name+' only paired toxic slugs, no missile Retinas',bool(shots)and all(e['kind']=='slug'for e in shots)and not any(q['locks']for q in trace),list({e['kind']for e in shots}))
   if initial['model']=='brood':
    ck(name+' real claw contact cycle and robot-fly mouth',any(q['phase']=='claw'for q in trace)and any(e['kind']=='fly'for e in shots),list({q['phase']for q in trace}))
    ck(name+' no spawned helpers',p.evaluate('enemies.every(e=>e===E||e.dead)'),p.evaluate('enemies.map(e=>e.type)'))
   if initial['model']=='relay':ck(name+' speeds up and uses authored roll poses',len({round(e.get('cadence',0),3)for e in shots})>4 and any(q['phase']=='roll'and q.get('frame',0)>0 for q in trace))
   if initial['model']=='missilejet':ck(name+' native lock before shootable missiles',any(q['locks']for q in trace)and any(e['event']=='missile-release'for e in events))
 # Actual renderer damaged pixels, expiry and finite absorbing shield pool.
 p.evaluate('''()=>{window.sewerPixels=()=>{ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);drawEnemy(E);ctx.restore();const a=ctx.getImageData(0,0,cv.width,cv.height).data;let white=0,color=0,opaque=0;for(let i=0;i<a.length;i+=4){if(a[i]>235&&a[i+1]>235&&a[i+2]>235&&a[i+3]>200)white++;if(Math.max(a[i],a[i+1],a[i+2])-Math.min(a[i],a[i+1],a[i+2])>25)color++;if(a[i+3]>50)opaque++;}return {white,color,opaque};};}''')
 for idx,s in enumerate(specs):
  p.evaluate(SETUP,s);q=p.evaluate('''()=>{for(let i=0;i<70;i++)updatePlay(1/60);E.x=worldWidth()/2;E.y=220;camX=E.x-VW/2;const clean=sewerPixels();markHit(E);const hit=sewerPixels();for(let i=0;i<30;i++)updatePlay(1/60);E.x=worldWidth()/2;E.y=220;return {clean,hit,expired:sewerPixels(),flash:E.flash};}''');ck(str(idx)+' '+s['type']+' actual white hit pixels and expiry',q['hit']['white']>q['clean']['white']+20 and q['expired']['white']<q['hit']['white']and q['flash']<=0,q)
 for typ in['ll18brood','s7barge']:
  p.evaluate(SETUP,next(s for s in specs if s['type']==typ));q=p.evaluate('''()=>{E.y=200;for(let i=0;i<30;i++)updatePlay(1/60);const start={hp:E.hp,energy:E._esh.energy};hitEnemy(E,8);const hit={hp:E.hp,energy:E._esh.energy,flash:E.flash};for(let j=0;j<8&&E._esh.phase!=='broken';j++){for(let i=0;i<20;i++)updatePlay(1/60);hitEnemy(E,200);}return {start,hit,phase:E._esh.phase,energy:E._esh.energy,hp:E.hp,max:E.maxhp};}''');ck(typ+' native shield absorbs damage and breaks finitely',q['hit']['hp']==q['start']['hp']and q['hit']['energy']<q['start']['energy']and q['hit']['flash']>0 and q['phase']=='broken',q)
 q=p.evaluate('()=>({slug:enemyOrdnanceCanIntercept({_s711Kind:"slug"}),fly:enemyOrdnanceCanIntercept({_s711Kind:"fly"}),laser:enemyOrdnanceCanIntercept({_s711Kind:"laser"}),missile:enemyOrdnanceCanIntercept({_s711Kind:"missile"}),retired:(window.allowS711=true,spawnEnemy("ll18raptor",340,-150))})');p.evaluate('window.allowS711=false');ck('Birth immunity, physical missiles and Blacksteel retirement',not q['slug']and not q['fly']and not q['laser']and q['missile']and q['retired']is None,q)
 ck('No Chromium page/console errors',not errors,errors);b.close()
(O/'errors.json').write_text(json.dumps(errors,indent=2));print('SUMMARY',sum(c['passed']for c in checks),'/',len(checks),flush=True);sys.exit(0 if all(c['passed']for c in checks)else 1)
