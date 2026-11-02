"""Real Chromium: solid Stage6 hulls, actual pixels/sockets and native sortie owners."""
from pathlib import Path
import sys,json
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import TRAP_RAF
O=R/'_shots/stage6_airframe_1101';checks=[];errors=[];runs=[]
def ck(n,v,d=None):
 checks.append(dict(name=n,passed=bool(v),data=d));(O/'edge-checks.json').write_text(json.dumps(checks,indent=2));print('PASS'if v else'FAIL',n,flush=True)
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
 for typ in['l6v_s0','l6v_r0','l6v_s1','l6v_r2']:
  p.evaluate(SETUP,next(c for c in cases if c['id']==typ));q=p.evaluate('''()=>{for(let i=0;i<350;i++){updatePlay(1/60);if(eBullets.some(b=>b._s611Owner===E&&!r46Physical(b.kind)))break;}drawWorld(0);const ev=S611.events.filter(q=>q.event==='shot');return {shots:ev.length,frame:E._s611Rendered?.frame,ordinary:eBullets.filter(b=>b._s611Owner===E&&!r46Physical(b.kind)).map(b=>({kind:b.kind,can:enemyOrdnanceCanIntercept(b),art:b._s611Ammo})),muzzles:S611.events.filter(q=>q.event==='muzzle').length};}''');ck(typ+' real rounds and separate measured muzzle reports',q['shots']>0 and q['muzzles']>0 and q['frame']==0,q);ck(typ+' ordinary rounds reject interception and use compact teal art',bool(q['ordinary'])and all(not b['can']and b['art']=='slug'for b in q['ordinary']),q['ordinary'])
 p.evaluate(SETUP,next(c for c in cases if c['id']=='l6v_r2'))
 q=p.evaluate('''()=>{const m=s611M(E),out=[];for(const gain of[.16,.52,.95]){ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);ctx.globalCompositeOperation='lighter';r46Blit(m.glow,0,Math.PI/2,300,200,192,null,gain);ctx.restore();const a=ctx.getImageData(204,104,192,192).data;let light=0,pixels=0;for(let i=0;i<a.length;i+=4){light+=a[i]+a[i+1]+a[i+2];if(a[i]+a[i+1]+a[i+2]>0)pixels++;}out.push({gain,light,pixels});}return out;}''');ck('Native1015 companion retains geometry at three brightness steps',q[0]['pixels']==q[1]['pixels']==q[2]['pixels']and q[0]['light']<q[1]['light']<q[2]['light'],q)
 for diff in['normal','hard']:
  p.evaluate('d=>{diffKey=d;DIFF=difficultyForRun(run.mode,d)}',diff)
  for typ in['l6v_s0','s6lancer']:
   p.evaluate(SETUP,next(c for c in cases if c['id']==typ));q=p.evaluate('''()=>{const hp=E.hp;for(let i=0;i<300;i++)updatePlay(1/60);drawWorld(0);return {hp,budget:E.hp,frame:E._s611Rendered?.frame,shots:S611.events.filter(q=>q.event==='shot').length};}''');ck(diff+' '+typ+' native health and launch contract',q['budget']==q['hp']and q['frame']==0 and q['shots']>0,q)
 p.evaluate(SETUP,next(c for c in cases if c['id']=='l6v_s0'))
 q=p.evaluate('''()=>{for(let i=0;i<100;i++)updatePlay(1/60);for(let n=0;n<8&&!E.dead&&E._dyingT==null;n++){hitEnemy(E,99999);for(let i=0;i<14;i++)updatePlay(1/60);}const dying=E._dyingT!=null||E.dead,before=S611.events.filter(q=>q.event==='shot').length;for(let i=0;i<200;i++)updatePlay(1/60);return {dying,dead:E.dead,fx:E._deathFxStarted,before,after:S611.events.filter(q=>q.event==='shot').length};}''');ck('Canonical jet retains native burning/crash/death and cancels guns',q['dying']and q['dead']and q['fx']and q['before']==q['after'],q)
 ck('Native page/console has no errors',not errors,errors);b.close()
(O/'edge-errors.json').write_text(json.dumps(errors,indent=2));print('SUMMARY',sum(c['passed']for c in checks),'/',len(checks),flush=True);sys.exit(0 if all(c['passed']for c in checks)else 1)
