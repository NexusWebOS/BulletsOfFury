from pathlib import Path
from playwright.sync_api import sync_playwright
import ast,sys,json,http.server
R=Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury');sys.path.insert(0,str(R/'_BUILD_SOURCE'));import shoot
O=R/'_shots/final_version_1021';SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text(encoding='utf-8')).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets));rows=[];errors=[];http.server.ThreadingHTTPServer.request_queue_size=128;port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(channel='msedge');p=b.new_page();p.set_default_timeout(180000);p.on('pageerror',lambda e:errors.append(str(e)));p.goto(f'http://127.0.0.1:{port}');p.wait_for_function('window.__bofFrames>4');p.evaluate(shoot.TRAP_RAF)
  for diff in ['easy','normal','hard','furious']:
   p.evaluate(SETUP,dict(stage=6,kind='rebelsquad',pilot='cole',diff=diff));p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(6)}')
   row=p.evaluate('''()=>{const R=B._rebels;rf28Init(B,R);R.frIntro={done:true};const G=rg4Init(B);G.gang=true;G.scene=null;G.rescueDone=true;G.rescueAt=Infinity;G.releaseAt=999;rd21State(B).next=999;for(const q of R.ships){q.rg4.cd=q.rg4.gunCd=999;q.rg4.act=null;}H3.release=false;H3.ending=null;fb2Talk=fb2Intro=thaw=s6Opening=null;BOFCinematicDirector.cancel();AP10_X.intro=null;story=null;P2M.active=null;stagePlan=[];spawnClock=999999;subBossTriggered=aminiTriggered=true;VP12.next=CP12.next=EP13.next=SEWER17.next=HM17.next=TARGET17.nextTank=999999;s6WingInit();s6WingLaunch(4,true);const W=s6Wing;W.beats=3;W.all=W.fakeDone=true;W.route='right';W.supplyIndex=3;W.boxes=[];for(const [i,q]of W.ships.entries()){q.phase='fight';q.t=3;q.x=worldWidth()/2+(i-1)*60;q.y=VH-100;q.fcd=0;q.missileCd=q.specialCd=999;q.dodgeCd=999;q.dodgeT=0;q.think=0;}pBullets=[];eBullets=[];player.fireCd=999999;player.invuln=999;for(const key of Object.keys(Input.keys))delete Input.keys[key];Input.mouse.down=false;const q=W.ships[0],A={shot:0,target:{key:q.key,ref:q},locked:true};ra4Rocket(R.ships[0],G,A);const m=eBullets.at(-1);m.x=q.x;m.y=q.y-150;m.vx=0;m.vy=3;m.lock=null;let shots=0,targeted=false;for(let i=0;i<100&&!m.dead;i++){updatePlay(1/60);shots=Math.max(shots,pBullets.filter(p=>p.ally&&p._wingKey).length);targeted||=W.ships.some(q=>q._rd21Intercept===m);}return{diff:diffKey,alliedShots:shots,targeted,intercepted:!!m.dead||!eBullets.includes(m)};}''');rows.append(row);print(json.dumps(row),flush=True)
  b.close()
finally:stop()
(O/'ally-defense.json').write_text(json.dumps(dict(rows=rows,errors=errors),indent=2));assert not errors and all(r['targeted'] and r['alliedShots']>0 and r['intercepted'] for r in rows)
