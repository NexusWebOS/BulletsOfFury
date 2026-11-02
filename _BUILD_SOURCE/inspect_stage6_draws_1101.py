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
 p.evaluate(SETUP,next(c for c in cases if c['id']=='l6v_s0'))
 q=p.evaluate('''()=>{for(let i=0;i<120;i++)updatePlay(1/60);const old=ctx.drawImage,rows=[];ctx.drawImage=function(im,...a){const tag=R46.tags.get(im)||AF21.tags.get(im)||PXG.tags.get(im)||{};rows.push({key:tag.key,args:a.slice(-4),op:this.globalCompositeOperation});return old.call(this,im,...a)};try{drawEnemy(E)}finally{ctx.drawImage=old}return rows; }''');print(json.dumps(q,indent=2),flush=True)
 ck('Native page/console has no errors',not errors,errors);b.close()
(O/'errors.json').write_text(json.dumps(errors,indent=2));print('SUMMARY',sum(c['passed']for c in checks),'/',len(checks),flush=True);sys.exit(0 if all(c['passed']for c in checks)else 1)
