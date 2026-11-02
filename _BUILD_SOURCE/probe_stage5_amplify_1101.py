"""Native orbital roles, current pixels, birth interception and cleanup."""
from pathlib import Path
import sys,json
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import TRAP_RAF
O=R/'_shots/stage5_amplify_1101';checks=[];errors=[];runs=[]
def ck(n,v,d=None):
 checks.append(dict(name=n,passed=bool(v),data=d));(O/'checks.json').write_text(json.dumps(checks,indent=2));print('PASS'if v else'FAIL',n,flush=True)
SETUP='''s=>{window.fixtureSpawn=true;EA11.case(s);window.fixtureSpawn=false;bossWarned=false;thaw=story=fb2Talk=null;CP12.next=VP12.next=CP22.nextWave=CP22.nextFlyby=99999;_adaptiveSpawnT=99999;S511.events=[];S511.fx=[];S511.mines.clear();player.invuln=40002;playerLocks=[];return {type:E.type,hp:E.hp,x:E.x,y:E.y,shield:E._esh?.max||0};}'''
with sync_playwright()as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:350])if m.type=='error'or'draw error'in m.text else None)
 p.goto('http://127.0.0.1:8805/game/index.html',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5');p.mouse.click(3,3);p.evaluate(TRAP_RAF);p.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'));p.evaluate('EA11.setup(5,"furious")');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(5)&&Object.values(S511_ART.banks).every(B=>XART.rdy(B.key))&&Object.values(S511_ART.models).every(m=>XART.rdy(m.bank.key))}',timeout=180000)
 p.evaluate('()=>{const spawn=spawnEnemy;spawnEnemy=function(){if(!window.fixtureSpawn&&ai27Context!==window.E)return null;return spawn.apply(this,arguments);};}')
 specs=json.loads((R/'_shots/enemy_flight_1031/before/stage5-specs.json').read_text());types=['s5frigate','s5rammer','s5skimmer','s5gravity','s5minelayer','s5satellite','s5portalmine','s5repair','s5station','s5leech']
 for diff in['normal','hard','furious']:
  p.evaluate('d=>{diffKey=d;DIFF=difficultyForRun(run.mode,d)}',diff)
  for typ in types:
   initial=p.evaluate(SETUP,next(s for s in specs if s['type']==typ));trace=[];seen=set()
   for j in range(46):
    q=p.evaluate('()=>{for(let i=0;i<24;i++){if(E.dead)break;updatePlay(1/60);}drawWorld(0);return {x:E.x,y:E.y,hp:E.hp,dead:E.dead,age:E._s511.age,phase:E._s511.phase,dir:E._s511Rendered?.dir,frame:E._s511Rendered?.frame,head:E._s511.head,shots:eBullets.filter(b=>b._s511Owner===E).length,locks:playerLocks.filter(L=>L.src===E).length,beams:E._s511.beams,finite:[E,...eBullets].every(q=>Number.isFinite(q.x)&&Number.isFinite(q.y))};}');trace.append(q);p.wait_for_timeout(3)
    if diff=='furious'and q['phase']not in seen and q['phase']in['beam','tell','lay','pass','open','pounce','lock','recover']:
     p.screenshot(path=str(O/(typ+'-'+q['phase']+'.png')));seen.add(q['phase'])
    if q['dead']:break
   events=p.evaluate('S511.events');runs.append(dict(diff=diff,type=typ,initial=initial,trace=trace,events=events));(O/'runs.json').write_text(json.dumps(runs,indent=2))
   ck(diff+' '+typ+' live owner, finite motion and native HP',all(q['finite']and q['hp']==initial['hp']for q in trace),trace[-1])
   if typ=='s5leech':ck(diff+' Leech opens/pounces and never fires',any(q['phase']=='pounce'for q in trace)and not any(e['event']=='shot'for e in events),list({q['phase']for q in trace}))
   elif typ=='s5rammer':ck(diff+' Rammer commits fast ram',any(q['phase']=='ram'for q in trace),events)
   elif typ in['s5frigate','s5repair']:ck(diff+' '+typ+' real beams',any(e['event']=='beam-release'for e in events),events[-4:])
   else:ck(diff+' '+typ+' actually launches',any(e['event']=='shot'for e in events),events[-4:])
   if diff!='normal'and typ in['s5gravity','s5portalmine']:ck(diff+' '+typ+' full radial directions',all(e['directions']==(9 if typ=='s5portalmine'else 12)for e in events if e['event']=='radial-release')and any(e['event']=='radial-release'for e in events))
   if typ=='s5satellite':ck(diff+' native Retina acquires before missiles',any(q['locks']for q in trace)and any(e['event']=='missile-release'for e in events))
   if typ=='s5station':ck(diff+' Station alternates spread and charged beam',any(e['event']=='beam-release'for e in events)and any(e['event']=='shot'and e['kind']=='laser'for e in events))
 # Compare actual ram timings/speed and Repair HP across ranks.
 rr=[next(x for x in runs if x['diff']==d and x['type']=='s5rammer')for d in['normal','hard','furious']]
 ck('Rammer acts earlier on Hard and earliest Furious',all(rr[i]['trace'][-1]['age']>rr[i+1]['trace'][-1]['age']for i in range(2)),[x['trace'][-1]['age']for x in rr])
 repair=[next(x for x in runs if x['diff']==d and x['type']=='s5repair')['initial']['hp']for d in['normal','hard','furious']];ck('Repair HP rises Hard/Furious',repair[0]<repair[1]<repair[2],repair)
 p.evaluate('''()=>{window.orbitalPixels=()=>{ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);drawEnemy(E);ctx.restore();const a=ctx.getImageData(0,0,cv.width,cv.height).data;let white=0,color=0;for(let i=0;i<a.length;i+=4){if(a[i]>235&&a[i+1]>235&&a[i+2]>235)white++;if(Math.max(a[i],a[i+1],a[i+2])-Math.min(a[i],a[i+1],a[i+2])>25)color++;}return {white,color};};}''')
 for typ in types:
  p.evaluate(SETUP,next(s for s in specs if s['type']==typ));q=p.evaluate('''()=>{for(let i=0;i<70;i++)updatePlay(1/60);E.x=worldWidth()/2;E.y=220;camX=E.x-VW/2;const clean=orbitalPixels();markHit(E);const hit=orbitalPixels();for(let i=0;i<30;i++)updatePlay(1/60);E.x=worldWidth()/2;E.y=220;return {clean,hit,expired:orbitalPixels(),flash:E.flash};}''');ck(typ+' actual marked hull pixels and expiry',q['hit']['white']>q['clean']['white']+20 and q['expired']['white']<q['hit']['white']and q['flash']<=0,q)
 p.evaluate(SETUP,next(s for s in specs if s['type']=='s5satellite'));q=p.evaluate('''()=>{for(let i=0;i<300;i++)updatePlay(1/60);const rounds=eBullets.filter(b=>b._s511Kind);return rounds.map(b=>({kind:b._s511Kind,lock:b._lockId,can:enemyOrdnanceCanIntercept(b)}));}''');ck('Satellite missiles keep actual native lock and interception',bool(q)and all(b.get('lock')and b['can']for b in q),q)
 q=p.evaluate('()=>({bullet:enemyOrdnanceCanIntercept({_s511Kind:"slug"}),mine:enemyOrdnanceCanIntercept({_s511Kind:"mine"}),orb:enemyOrdnanceCanIntercept({_s511Kind:"orb"}),void:(window.fixtureSpawn=true,spawnEnemy("xelite_voidreaver",200,-80))})');p.evaluate('window.fixtureSpawn=false');ck('Birth rules: bullets immune, plasma/mines interceptable, Voidreaver removed',not q['bullet']and q['mine']and q['orb']and q['void']is None,q)
 ck('No native page/console errors',not errors,errors);b.close()
(O/'errors.json').write_text(json.dumps(errors,indent=2));print('SUMMARY',sum(c['passed']for c in checks),'/',len(checks),flush=True);sys.exit(0 if all(c['passed']for c in checks)else 1)
