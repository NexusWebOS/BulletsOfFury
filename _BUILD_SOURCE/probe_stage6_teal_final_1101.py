"""Real Chromium: solid Stage6 hulls, actual pixels/sockets and native sortie owners."""
from pathlib import Path
import sys,json
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import TRAP_RAF
O=R/'_shots/stage6_airframe_1101';checks=[];errors=[];runs=[]
def ck(n,v,d=None):
 checks.append(dict(name=n,passed=bool(v),data=d));(O/'teal-final-checks.json').write_text(json.dumps(checks,indent=2));print('PASS'if v else'FAIL',n,flush=True)
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
 case=next(c for c in cases if c['id']=='l6v_s2');initial=p.evaluate(SETUP,case);trace=[];rounds=[]
 for n in range(250):
  q=p.evaluate('''()=>{const first=eBullets.length;updatePlay(1/60);drawWorld(0);return {hp:E.hp,frame:E._s611Rendered?.frame,key:E._s611Rendered?.key,rounds:eBullets.slice(first).filter(b=>b._s611Owner===E&&!b.dead).map(b=>({art:b._s611Ammo,can:enemyOrdnanceCanIntercept(b),distance:Math.hypot(b.x-r46Nearest(E,b.x,b.y).x,b.y-r46Nearest(E,b.x,b.y).y)}))};}''');trace.append(q);rounds+=q['rounds']
  if n%20==0:p.wait_for_timeout(2)
 ck('Final teal gun-pod hull retains one frame/native HP',all(q['hp']==initial['hp']and q['frame']==0 for q in trace),initial)
 ck('Final teal MG rounds leave actual gun mouths and stay unshootable',bool(rounds)and all(q['art']=='slug'and not q['can']and q['distance']<10 for q in rounds),rounds[:8])
 q=p.evaluate('''()=>{const m=s611M(E);return {guns:m.guns.length,model:E._s611.model};}''');ck('Final teal source has four measured hollow barrel mouths',q['guns']==4,q)
 p.screenshot(path=str(O/'fighter-teal-final-gun-pods.png'))
 q=p.evaluate('''()=>{E.x=worldWidth()/2;E.y=220;camX=E.x-VW/2;const px=()=>{ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);drawEnemy(E);ctx.restore();const a=ctx.getImageData(0,0,cv.width,cv.height).data;let white=0;for(let i=0;i<a.length;i+=4)if(a[i]>235&&a[i+1]>235&&a[i+2]>235)white++;return white;};const clean=px(),hp=E.hp;hitEnemy(E,.01);const hit=px();for(let i=0;i<30;i++)updatePlay(1/60);E.x=worldWidth()/2;E.y=220;return{clean,hit,expired:px(),hpBefore:hp,hp:E.hp,flash:E.flash};}''');ck('Final teal gun pods show native damaged pixels and expiry',q['hp']<q['hpBefore']and q['hit']>q['clean']+30 and q['expired']<q['hit']and q['flash']<=0,q)
 ck('Native page/console has no errors',not errors,errors);b.close()
(O/'teal-final-errors.json').write_text(json.dumps(errors,indent=2));print('SUMMARY',sum(c['passed']for c in checks),'/',len(checks),flush=True);sys.exit(0 if all(c['passed']for c in checks)else 1)
