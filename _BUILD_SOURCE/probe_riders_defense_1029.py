from pathlib import Path
import sys,http.server,json,math
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];W=R/'_shots/riders_defense_1029';W.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import serve,TRAP_RAF,STEP
http.server.ThreadingHTTPServer.request_queue_size=256;checks=[];errors=[]
def ck(n,v,d=None):
 checks.append(dict(name=n,passed=bool(v),data=d));(W/'checks.json').write_text(json.dumps(checks,indent=2));print('PASS'if v else'FAIL',n,flush=True);assert v,(n,d)
port,stop=serve(str(R))
try:
 with sync_playwright()as pw:
  b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'or'draw error'in m.text else None)
  p.goto(f'http://127.0.0.1:{port}',timeout=180000);p.wait_for_function('window.__bofFrames>5');p.mouse.click(3,3);p.evaluate('()=>{run.stage=6;stageLoadBegin(6)}');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(6)}',timeout=180000);p.evaluate(TRAP_RAF)
  setup="""()=>{diffKey='furious';debugUnlocked=true;debugStartFight({stage:6,role:'boss',kind:'rebelsquad'},{pilot:'cole',record:false});DBGT.god=true;spawnBoss('rebelsquad');debugFight.spawned=true;warnT=0;BOFCinematicDirector.cancel();setState(GS.PLAY);bossActive=true;window.R=boss._rebels;R.frIntro={done:true,t:0,beat:0};boss._noHit=false;if(R.rough33){R.rough33.phase='combat';R.rough33.resume=1.6;}R.h3Intro=null;R.frRadio=null;R.releaseAt=0;window.G=rg4Init(boss);G.releaseAt=0;G.rescueDone=true;if(G.rd21)G.rd21.fleet=null;for(const q of R.ships){q.rg4.act=null;q.rg4.cd=999;q.stun=0;}window.v=R.ships.find(q=>q.key==='voss');window.j=R.ships.find(q=>q.key==='jace');window.overlaps=()=>{const ss=R.ships.filter(q=>!q.dead&&q.y>PLAY.y-100&&q.y<VH+100);let max=0;for(let i=0;i<ss.length;i++)for(let k=i+1;k<ss.length;k++){const a=ss[i],b=ss[k],A=rr45Bounds(a),B=rr45Bounds(b),x=A.w+B.w+7-Math.abs(a.x-b.x),y=A.h+B.h+9-Math.abs(a.y-b.y);if(x>0&&y>0)max=Math.max(max,Math.min(x,y));}return max;};}"""
  p.evaluate(setup)
  ck('Authored fixed-size banks preload',p.evaluate("Object.keys(RR45_BANKS).every(k=>XART.rdy('rr45_'+k))"))
  ck('Unavailable Decker does not queue repeated charge dialogue',p.evaluate("(()=>{const ships=s6Wing.ships,done=G.rescueDone,Q=rr26State(G).queue,n=Q.length;s6Wing.ships=ships.filter(q=>q.key!=='decker');G.rescueDone=false;let started;try{started=rg4RescueStart(boss,G);}finally{s6Wing.ships=ships;G.rescueDone=done;}return !started&&Q.length===n})()"))
  q=p.evaluate("""()=>{for(const q of R.ships){q.x=340;q.y=130;q._rd21Scale=1;q.rfHeading=Math.PI/2;}rr45Separate(boss);return{max:overlaps(),ships:R.ships.map(q=>({key:q.key,x:q.x,y:q.y}))};}""");ck('Five stacked fighters separate into distinct reserved airspace',q['max']<.2,q)
  p.screenshot(path=str(W/'spacing.png'))
  q=p.evaluate("""()=>{const n=pBullets.length;releaseHelix(MAV_FULL);const mv=pBullets.slice(n).find(o=>o._isBall),before=G.ord.length;ra4Helix(j,G,{a:Math.PI/2});const o=G.ord.slice(before).find(o=>o.kind==='helix');return{maverick:Math.abs(mv.vy)*60,jace:Math.hypot(o.vx,o.vy),hp:o.hp,r:o.r};}""");ck('Jace launch speed equals actual Maverick full ball',q['maverick']==q['jace']==690,q)
  q=p.evaluate("""()=>{G.rescueDone=false;G.rr26=rr26State(G);G.rr26.wall=null;const result=rg4RescueStart(boss,G);return{result,wall:!!G.rr26.wall?._rr45,caster:G.rr26.wall?.caster?.key,crate:s6Wing?.boxes.some(q=>q._rr26Wall&&!q.dead)};}""");ck('Decker starts gold charge automatically without supply box',q['result']and q['wall']and q['caster']=='decker'and not q['crate'],q)
  p.evaluate('()=>{atomFlash=0;pBullets=[];helixBursts.length=0}')
  for name,t in [('charge',.9),('seed',1.9),('forming',2.6),('active',4)]:
   p.evaluate('t=>{G.rr26.wall.t=t}',t);p.evaluate('()=>drawWorld(0)');p.screenshot(path=str(W/(name+'.png')))
  q=p.evaluate("""()=>{const W=G.rr26.wall,r=rr26WallRect();W.t=4;const a={x:r.x+150,y:r.y-6,vx:0,vy:3,w:8,h:12,kind:'s6tracer',t:0,_noArsenal:true};eBullets.push(a);const ord=rr26Energy(v,G,Math.PI/2,false,r.x+210,r.y-5);const shot={x:r.x+160,y:r.y+r.h+4,vx:0,vy:-10,w:8,h:12,kind:'mg',dmg:1};pBullets.push(shot);rr26WallContact(G,1/60);return{bullet:a.dead,orb:ord.dead,returns:G.rr26.returns.length,friendly:!!shot.dead,angry:G.rr26.queue.some(q=>q[0]==='rook'&&/SHIELD APART/.test(q[1]))};}""");ck('Shield returns enemy bullets and energy with angry dialogue; friendly shots pass',q['bullet']and q['orb']and q['returns']>=2 and not q['friendly']and q['angry'],q)
  ck('Friendly laser retains its real range',p.evaluate("(()=>{const b={kind:'beam',x:player.x,y:player.y,w:10,h:400};const a=rr26BeamBase(b),c=playerBeamRange(b);return JSON.stringify(a)===JSON.stringify(c)})()"))
  q=p.evaluate("""()=>{const rows=h3RebelLines(R),i=rows.findIndex(q=>q.who==='KAIA'),I={rows,i,t:rows[i].text.length/32+.4};rs1004DemoTick(R,I,1/60);return{kind:rows[i].demo,count:I.showcase.fx.filter(q=>q.kind==='rr45roller').length};}""");ck('Kaia intro launches actual roller demonstration',q['kind']=='rr45roller'and q['count']==1,q)
  p.evaluate('()=>{G.rr26.wall.t=4;G.ord=[];pBullets=[];eBullets=[];for(const q of R.ships){q.rg4.act=null;q.rg4.cd=999;}v.x=340;v.y=130;rg4Attack(v,R,G,"turbo");}')
  phases=set();worst=0;worstState=None;warnings=[]
  for i in range(1400):
   p.evaluate('()=>{rg4AttackTick(v,R,G,1/60);rr45Separate(boss)}')
   if i%8==0:
    q=p.evaluate('()=>({phase:v.rg4.act?.phase,max:overlaps(),cue:v.rg4.act?.rr45Cue,scale:v._rd21Scale,ships:R.ships.map(q=>({key:q.key,x:q.x,y:q.y,b:rr45Bounds(q)}))})');phases.add(q['phase']);
    if q['max']>worst:worst=q['max'];worstState=q
    if q['cue']:warnings.append(q['cue'])
   if i in [350,570,610]:p.evaluate('()=>drawWorld(0)');p.screenshot(path=str(W/f'voss-{i}.png'))
  ck('Voss warns top, bottom and sideways entries',set(q['dir']for q in warnings)>={1,3} and any(q['dir']in[0,2]for q in warnings),warnings[::10])
  ck('Voss completes lateral pass and native recovery',{'rr45_cross','north','dash','recover'}.issubset(phases)and p.evaluate('v.rg4.act===null'),list(phases))
  ck('Fighters keep clear during complete Voss book',worst<.3,worstState)
  ck('Prior fixed Voss orb columns remain unchanged',p.evaluate('OR44.events.filter(q=>q.event==="orb").every(q=>q.vx===0&&q.vy===240)'))
  ck('Stage X retains previous behavior',p.evaluate('(()=>{run._gp4StageX=true;const v=rr45Scope();run._gp4StageX=false;return !v})()'))
  ck('No native page/draw errors',not errors,errors);b.close()
finally:stop()




