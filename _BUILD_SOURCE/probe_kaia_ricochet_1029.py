from pathlib import Path
import sys,json,http.server
from playwright.sync_api import sync_playwright
R=Path(r'C:/Users/Mike/Desktop/Github Coding/BulletsOfFury');W=Path(__file__).resolve().parent;sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import serve,TRAP_RAF,STEP
http.server.ThreadingHTTPServer.request_queue_size=256;checks=[];errors=[]
def ck(n,v,d=None):
 checks.append(dict(name=n,passed=bool(v),data=d));(W/'checks.json').write_text(json.dumps(checks,indent=2));print('PASS'if v else'FAIL',n,flush=True);assert v,(n,d)
port,stop=serve(str(R))
try:
 with sync_playwright()as pw:
  b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.goto(f'http://127.0.0.1:{port}',timeout=180000);p.wait_for_function('window.__bofFrames>5');p.mouse.click(3,3);p.evaluate('()=>{run.stage=6;stageLoadBegin(6)}');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(6)}',timeout=180000);p.evaluate(TRAP_RAF)
  p.evaluate("""()=>{diffKey='furious';debugUnlocked=true;debugStartFight({stage:6,role:'boss',kind:'rebelsquad'},{pilot:'cole',record:false});DBGT.god=true;spawnBoss('rebelsquad');debugFight.spawned=true;warnT=0;BOFCinematicDirector.cancel();setState(GS.PLAY);bossActive=true;window.R=boss._rebels;R.frIntro={done:true,t:0,beat:0};boss._noHit=false;if(R.rough33){R.rough33.phase='combat';R.rough33.resume=1.6;}R.h3Intro=null;R.frRadio=null;R.releaseAt=0;window.G=rg4Init(boss);G.rescueDone=true;G.releaseAt=999;G.rd21.fleet=null;G.rd21.next=999;for(const q of R.ships){q.rg4.act=null;q.rg4.cd=999;q.stun=0;q.x=70+q.i*60;q.y=100;}window.n=R.ships.find(q=>q.key==='nyx');n.x=400;n.y=170;ny46Cloak(n);player.x=400;player.y=440;run.bombs=40;}""")
  p.evaluate("()=>{window.k=R.ships.find(q=>q.key==='kaia');pBullets=[];G.ord=[];G.rr26.wall=null;}")
  ck('Only Stage 6 Kaia owns the new roller behavior',p.evaluate("(()=>{const a=kr48Own(k)&&!kr48Own(n);run._gp4StageX=true;const b=!kr48Own(k);run._gp4StageX=false;return a&&b})()"))
  # Step for the whole burst, not only half a second.
  result=p.evaluate("""()=>{const out=[];for(const rank of ['easy','normal','hard','furious']){diffKey=rank;G.ord=[];k.rg4.act=null;rg4Attack(k,R,G,'roller');const A=k.rg4.act;A.phase='fire';A.t=0;A.cd=0;A.launch={x:300,y:150};A.launchAngle=1.1;const at=[];for(let i=0;i<1200&&k.rg4.act?.phase==='fire';i++){const count=G.ord.length;rg4AttackTick(k,R,G,1/600);if(G.ord.length>count)at.push(i/600);}out.push({rank,shots:G.ord.length,at,rounds:G.ord.map(o=>({marker:!!o._kr48,speed:Math.hypot(o.vx,o.vy),hp:o.hp,life:o.life,split:o.split})),phase:k.rg4.act.phase});}diffKey='furious';return out;}""")
  ck('All difficulties retain ten-round bursts and native recovery',all(q['shots']==10 and q['phase']=='recover'for q in result),result)
  ck('All four difficulty speeds increased by about one third',all(abs(o['speed']-v)<.001 for q,v in zip(result,[235,260,280,300])for o in q['rounds']))
  ck('Release gaps shorten from .20s to .14s',all(.139<=b-a<=.142 for q in result for a,b in zip(q['at'],q['at'][1:])))
  ck('Three HP, four-second lifetime and no child split preserved',all(o['marker']and o['hp']==3 and o['life']==4 and o['split']for q in result for o in q['rounds']))
  physics=p.evaluate("""()=>{const rows=[];for(const dt of[1/144,1/60,.05])for(const edge of['left','right','top','bottom','corner']){const L=camLeftX()+24,H=camRightX()-24,T=PLAY.y+24,B=VH-24,o={x:edge==='left'?L+1:edge==='right'||edge==='corner'?H-1:(L+H)/2,y:edge==='top'?T+1:edge==='bottom'||edge==='corner'?B-1:(T+B)/2,vx:edge==='left'?-300:edge==='right'||edge==='corner'?300:0,vy:edge==='top'?-300:edge==='bottom'||edge==='corner'?300:0,_kr48:999,bounces:0};const speed=Math.hypot(o.vx,o.vy);kr48Move(o,dt);rows.push({dt,edge,bounces:o.bounces,inside:o.x>=L&&o.x<=H&&o.y>=T&&o.y<=B,speedOK:Math.abs(speed-Math.hypot(o.vx,o.vy))<1e-8,vx:o.vx,vy:o.vy});}return rows;}""")
  ck('Top, bottom and both sides reflect at 144, 60 and 20fps',all(q['inside']and q['bounces']==(2 if q['edge']=='corner'else 1)for q in physics),physics)
  ck('Ricochets and corners preserve travel speed',all(q['speedOK']for q in physics))
  ck('Overshoot travels its remaining distance after reflection',p.evaluate('(()=>{const a=kr48Axis(99,300,.05,0,100);return a.position===86&&a.velocity===-300})()'))
  ck('Multiple rebounds in one step are resolved',p.evaluate('(()=>{const a=kr48Axis(50,1000,1,0,100);return a.position===50&&a.velocity===1000&&a.bounces.length===10})()'))
  ck('Moving viewport cannot strand a roller outside a screen edge',p.evaluate('(()=>{const a=kr48Axis(-20,-300,.05,10,100);return a.position===25&&a.velocity===300&&a.bounces.length===1})()'))
  base="{kind:'roller',_rr26KaiaRoller:true,_kr48:999,owner:k,x:300,y:200,vx:180,vy:240,r:16,hp:3,max:3,t:0,life:4,bounces:0,split:true,flash:0}"
  p.evaluate("()=>{G.ord=["+base+"];G.ord[0].t=3.99;rg4OrdnanceTick(boss,G,.02)}")
  ck('Native lifetime still expires ricochets',p.evaluate('G.ord.length===0'))
  p.evaluate("()=>{G.ord=["+base+"];k.dead=true;rg4OrdnanceTick(boss,G,.02);k.dead=false}")
  ck('Native owner defeat clears its rollers',p.evaluate('G.ord.length===0'))
  p.evaluate("()=>{G.ord=["+base+"];pBullets=[{x:303,y:204,w:8,h:12,dmg:3}];rg4OrdnanceTick(boss,G,1/60);pBullets=[]}")
  ck('Native player bullets can still destroy rollers',p.evaluate('G.ord.length===0'))
  p.evaluate("()=>{G.ord=["+base+"];G.ord[0].x=camRightX()-25;G.ord[0].y=VH-25;rg4OrdnanceTick(boss,G,.05)}")
  ck('Native ordnance owner runs the new corner rebound',p.evaluate('G.ord.length===1&&G.ord[0].bounces===2&&G.ord[0].vx<0&&G.ord[0].vy<0'))
  p.evaluate("()=>{G.ord=["+base+"];const old=camX;camX+=80;rg4OrdnanceTick(boss,G,.05);camX=old}")
  ck('No native errors',not errors,errors)
  (W/'physics.json').write_text(json.dumps(physics,indent=2));b.close()
finally:stop()
