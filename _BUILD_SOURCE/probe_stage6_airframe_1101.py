"""Real Chromium: solid Stage6 hulls, actual pixels/sockets and native sortie owners."""
from pathlib import Path
import sys,json
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import TRAP_RAF
O=R/'_shots/stage6_airframe_1101';checks=[];errors=[];runs=[]
def ck(n,v,d=None):
 checks.append(dict(name=n,passed=bool(v),data=d));(O/'checks.json').write_text(json.dumps(checks,indent=2));print('PASS'if v else'FAIL',n,flush=True)
SETUP=r'''q=>{window.fixtureSpawn=true;EA11.case(q.spec);if(q.special){for(const e of enemies)e.dead=true;enemies=[];aiQueue=[];fb2Flights=[];
 if(q.special==='dasher'){const f=cp22Free;cp22Free=()=>true;try{E=cp22DashSpawn(1,PLAY.y+165)}finally{cp22Free=f}}
 else if(q.special.startsWith('strike-'))E=fb2FlightSpawn({direction:q.special.slice(7),role:'red',x:worldWidth()/2,y:PLAY.y+150,_cp22Mode:'bomb'});
 else E=fb2FlightSpawn({direction:'south',role:'red',x:worldWidth()/2,_cp22Mode:q.special});}
 window.fixtureSpawn=false;bossWarned=false;thaw=story=fb2Talk=null;CP12.next=VP12.next=CP22.nextWave=CP22.nextFlyby=99999;_adaptiveSpawnT=99999;S611.events=[];R46.fx=[];player.invuln=40002;playerLocks=[];return {type:E.type,hp:E.hp,x:E.x,y:E.y,model:s611Name(E),pattern:E.pattern};}'''
with sync_playwright()as pw:
 b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:350])if m.type=='error'or'draw error'in m.text else None)
 p.goto('http://127.0.0.1:8805/game/index.html',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5');p.mouse.click(3,3);p.evaluate(TRAP_RAF);p.add_script_tag(path=str(R/'_BUILD_SOURCE/enemy_behaviour_lab_1011.js'));p.evaluate('EA11.setup(6,"furious")');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(6)&&Object.values(S611_ART.banks).every(B=>XART.rdy(B.key))}',timeout=180000)
 p.evaluate('()=>{const spawn=spawnEnemy;spawnEnemy=function(){if(!window.fixtureSpawn&&ai27Context!==window.E)return null;return spawn.apply(this,arguments);};}')
 specs=json.loads((R/'_shots/enemy_flight_1031/before/stage6-specs.json').read_text());cases=[]
 for typ in dict.fromkeys(s['type']for s in specs if s['type']!='modturret'):
  cases.append({'id':typ,'spec':next(s for s in specs if s['type']==typ),'special':'strike-south'if typ=='s1jetbomber_b'else None})
 for special in['dasher','bomb','rain','charge','strike-east','strike-west']:
  typ='s6dart'if special=='dasher'else's1jetbomber_b';cases.append({'id':special,'spec':next(s for s in specs if s['type']==typ),'special':special})
 (O/'cases.json').write_text(json.dumps(cases,indent=2))
 for case in cases:
  initial=p.evaluate(SETUP,case);trace=[]
  for j in range(34):
   q=p.evaluate('()=>{for(let i=0;i<24;i++){if(E.dead)break;updatePlay(1/60);}drawWorld(0);return {x:E.x,y:E.y,hp:E.hp,dead:E.dead,key:E._s611Rendered?.key,frame:E._s611Rendered?.frame,dir:E._s611Rendered?.dir,exhausts:E._s611Rendered?.exhausts,phase:E._cp22Flight?.phase||E._cp22Dash?.phase||E._phase,seen:E._ai27?.seen,finite:[E,...eBullets].every(q=>Number.isFinite(q.x)&&Number.isFinite(q.y))};}');trace.append(q);p.wait_for_timeout(3)
   if j in[4,9,16]and not q['dead']:p.screenshot(path=str(O/(case['id']+'-'+str(j)+'.png')))
   if q['dead']:break
  events=p.evaluate('S611.events');runs.append(dict(case=case,initial=initial,trace=trace,events=events));(O/'runs.json').write_text(json.dumps(runs,indent=2))
  ck(case['id']+' one canonical hull throughout native flight/attack',all(q['frame']==0 and q['key']==trace[0]['key']for q in trace if q.get('key'))and any(q.get('key')for q in trace),trace[-1])
  ck(case['id']+' native HP, finite position and real exhausts',all((q['hp']==initial['hp']or q['dead']and q['hp']==0)and q['finite']and (q.get('exhausts')or q['dead'])for q in trace),initial)
 # Actual native hit pixels, not just selected texture names.
 p.evaluate('''()=>{window.skyPixels=()=>{ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);drawEnemy(E);ctx.restore();const a=ctx.getImageData(0,0,cv.width,cv.height).data;let white=0,light=0;for(let i=0;i<a.length;i+=4){if(a[i]>235&&a[i+1]>235&&a[i+2]>235)white++;light+=a[i]+a[i+1]+a[i+2];}return {white,light};};}''')
 for typ in ['l6v_s0','l6v_s1','l6v_s2','l6v_r0','l6v_r1','l6v_r2','s6lancer','s6dart','s6turbine','s6probe']:
  case=next(c for c in cases if c['id']==typ);p.evaluate(SETUP,case);q=p.evaluate('''()=>{for(let i=0;i<90;i++)updatePlay(1/60);E.x=worldWidth()/2;E.y=220;camX=E.x-VW/2;if(E._esh){hitEnemy(E,E._esh.max+1);for(let i=0;i<25;i++)updatePlay(1/60);E.x=worldWidth()/2;E.y=220;}const clean=skyPixels(),before=E.hp;hitEnemy(E,.01);const hit=skyPixels();for(let i=0;i<30;i++)updatePlay(1/60);E.x=worldWidth()/2;E.y=220;return {clean,hit,after:skyPixels(),hpBefore:before,hp:E.hp,flash:E.flash};}''');ck(typ+' actual native damaged pixels and flash expiry',q['hit']['white']>q['clean']['white']+30 and q['after']['white']<q['hit']['white']and q['flash']<=0,q)
 q=p.evaluate('''()=>{window.fixtureSpawn=true;const ground=['mg','laser','sonic'].map(_modWeapon=>spawnEnemy('modturret',200,100,{_modStage:6,_modWeapon}));const intro=fb2FlightSpawn({direction:'south',role:'blue',x:300});window.fixtureSpawn=false;return {ground:ground.every(e=>e==null),introExists:!!intro,introPreserved:s611Name(intro)==null,nativeRole:intro?._fb2Stealth?.role};}''');ck('No sky ground turrets; native entrance stealth remains excluded',q['ground']and q['introExists']and q['introPreserved'],q)
 ck('Native page/console has no errors',not errors,errors);b.close()
(O/'errors.json').write_text(json.dumps(errors,indent=2));print('SUMMARY',sum(c['passed']for c in checks),'/',len(checks),flush=True);sys.exit(0 if all(c['passed']for c in checks)else 1)
