from pathlib import Path
from playwright.sync_api import sync_playwright
import http.server,json,sys
R=Path(__file__).resolve().parents[1];W=R/'_shots/stage6_solo_miniboss_1028';W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import serve,TRAP_RAF,STEP
http.server.ThreadingHTTPServer.request_queue_size=256
checks=[];errors=[];http=[]
def ck(n,v,d=None):checks.append(dict(name=n,passed=bool(v),data=d));(W/'checks.json').write_text(json.dumps(dict(checks=checks,errors=errors,http=http),indent=2));assert v,(n,d)
port,stop=serve(str(R))
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'or'draw error'in m.text else None);p.on('response',lambda r:http.append(r.url)if r.status>=400 else None);p.goto(f'http://127.0.0.1:{port}',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5');p.mouse.click(3,3);p.evaluate('()=>{run.stage=6;stageLoadBegin(6)}');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(6)}',timeout=180000);p.evaluate(TRAP_RAF)
  def step(n):
   e=p.evaluate(STEP,n)
   if e:raise RuntimeError(e)
  for diff in ['easy','normal','hard','furious']:
   p.evaluate("d=>{diffKey=d;debugUnlocked=true;debugStartFight({stage:6,role:'mini',kind:'siegefortress17'},{pilot:'cole',record:false});DBGT.god=true;BOFCinematicDirector.cancel();setState(GS.PLAY);}",diff);step(15);ck(diff+' warning has no NPCs',p.evaluate('s6SoloActive()&&!s6Wing.ships.length&&!ally'))
   p.evaluate("()=>{spawnSubBoss('siegefortress17');debugFight.spawned=true;warnT=0;}");step(180);q=p.evaluate('''()=>({ships:s6Wing.ships.length,ally:!!ally,shots:pBullets.filter(p=>p.ally||p._wingKey).length,parts:subBoss._cargo13?.guns.length,hp:subBoss.hp,held:S6SOLO.held.ships.length,opening:s6OpeningActive(),talk:!!fb2Talk,bossTime:subBoss.t,y:subBoss.y})''');ck(diff+' actual Fortress fight is solo with native weapons/HP',q['ships']==0 and not q['ally']and q['shots']==0 and q['hp']>0 and q['parts']>=6,q);ck(diff+' Fortress entrance advances without a stuck stage opening',not q['opening']and not q['talk']and q['bossTime']>2,q)
   p.evaluate('s6WingLaunch(8,true)');step(30);ck(diff+' reinforcements cannot enter mid-fight',p.evaluate('!s6Wing.ships.length'))
  p.screenshot(path=str(W/'solo-native.png'))
  q=p.evaluate('''()=>{const old=S6SOLO.base.draw;let n=0;S6SOLO.base.draw=()=>n++;try{s6WingDraw()}finally{S6SOLO.base.draw=old}return n;}''');ck('Native ally renderer is not called during the miniboss',q==0)
  q=p.evaluate('''()=>{allyRoster=['yuri'];allyUsed=[];ally=null;const n=allyUsed.length,r=allyCall();return{r,n,used:allyUsed.length,ally:!!ally};}''');ck('Calling a rival ally is blocked without spending the favor',q['r']==False and q['used']==q['n']and not q['ally'],q)
  p.evaluate('''()=>{debugFight=null;subBoss=null;subBossActive=false;subBossDone=false;subBossTriggered=false;warnT=0;boss=null;bossActive=false;s6SoloRelease();s6WingInit();s6WingLaunch(4,true);ally=null;allyRoster=['yuri'];allyUsed=[];allyCall();window.preSolo={n:s6Wing.ships.length,hp:s6Wing.ships.map(q=>q.hp),used:allyUsed.length,player,run};pBullets.push({kind:'mg',x:1,y:1,ally:true,_wingKey:'yuri'},{kind:'mg',x:2,y:1,seat:1},{kind:'mg',x:3,y:1,seat:2});subBossTriggered=true;warnKind='sub';warnT=2;s6WingTick(1/60);}''');q=p.evaluate('''()=>({wing:s6Wing.ships.length,ally:!!ally,npc:pBullets.filter(p=>p.ally||p._wingKey).length,seats:pBullets.filter(p=>p.seat===1||p.seat===2).map(p=>p.seat),same:preSolo.player===player&&preSolo.run===run,parked:S6SOLO.held.ships.length})''');ck('Natural campaign warning parks existing support and clears NPC fire only',q['wing']==0 and not q['ally']and q['npc']==0 and q['parked']>0,q);ck('Both human-seat rounds and player state remain untouched',q['seats']==[1,2]and q['same'],q)
  p.evaluate('''()=>{subBossTriggered=true;subBossActive=false;subBossDone=true;warnT=0;s6WingTick(1/60);}''');q=p.evaluate('''()=>({restored:s6Wing.ships.length,allArriving:s6Wing.ships.every(q=>q.phase==='arrive'),ally:!!ally,used:allyUsed.length,expected:preSolo.n})''');ck('Campaign support returns after the miniboss with no duplicate favor cost',q['restored']>=q['expected']and q['allArriving']and q['ally']and q['used']==1,q)
  for kind in ['warhive','rebelsquad']:
   p.evaluate("k=>{debugStartFight({stage:6,role:'boss',kind:k},{pilot:'cole',record:false});DBGT.god=true;spawnBoss(k);debugFight.spawned=true;warnT=0;}",kind);ck(kind+' main encounter retains its allied wing',p.evaluate('!s6SoloActive()&&s6Wing.ships.length>0'),p.evaluate('s6Wing.ships.length'))
  p.evaluate("()=>{debugStartFight({stage:6,role:'mini',kind:'siegefortress17'},{pilot:'cole',record:false});debugFight=null;on5LaunchEncounter({stage:6,role:'mini',kind:'siegefortress17',code:'MINI6'});}");step(90);ck('MINI6 password/direct-inner entry is also solo',p.evaluate('subBossActive&&!s6Wing.ships.length&&!ally'))
  p.evaluate('''()=>{run.stage=7;debugFight=null;subBossActive=true;ally=null;allyRoster=['yuri'];allyUsed=[];}''');ck('Other stages can still call their allies during a miniboss',p.evaluate('!s6SoloActive()&&allyCall()&&!!ally'))
  ck('No native game, draw or asset errors',not errors and not http,dict(errors=errors,http=http));br.close()
finally:stop()
print(len(checks),'solo encounter and scope checks passed')
