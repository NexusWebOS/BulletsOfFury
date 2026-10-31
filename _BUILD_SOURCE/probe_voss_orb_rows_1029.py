from pathlib import Path
import sys,http.server,json,math
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];W=R/'_shots/voss_orb_rows_1029';W.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import serve,TRAP_RAF,STEP
http.server.ThreadingHTTPServer.request_queue_size=256
checks=[]
def ck(name,ok,data=None):
 checks.append(dict(name=name,passed=bool(ok),data=data));(W/'voss-checks.json').write_text(json.dumps(checks,indent=2));assert ok,(name,data)
port,stop=serve(str(R));errors=[]
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)))
  p.goto(f'http://127.0.0.1:{port}',timeout=180000);p.wait_for_function('window.__bofFrames>5');p.mouse.click(3,3)
  p.evaluate('()=>{run.stage=6;stageLoadBegin(6)}');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(6)}',timeout=180000);p.evaluate(TRAP_RAF)
  for difficulty in ['easy','normal','hard','furious']:
   p.evaluate('''d=>{diffKey=d;debugUnlocked=true;debugStartFight({stage:6,role:'boss',kind:'rebelsquad'},{pilot:'cole',record:false});DBGT.god=true;spawnBoss('rebelsquad');debugFight.spawned=true;warnT=0;BOFCinematicDirector.cancel();setState(GS.PLAY);bossActive=true;const R=boss._rebels;R.frIntro={done:true,t:0,beat:0};boss._noHit=false;if(R.rough33){R.rough33.phase='combat';R.rough33.resume=1.6;}R.h3Intro=null;R.frRadio=null;R.releaseAt=0;const G=rg4Init(boss);G.releaseAt=0;if(G.rd21)G.rd21.fleet=null;for(const q of R.ships){q.rg4.act=null;q.rg4.cd=999;q.stun=0;}const q=R.ships.find(q=>q.key==='voss');q.x=340;q.y=130;player.x=340;player.y=550;OR44.events=[];OR44.rows=OR44.rounds=0;rg4Attack(q,R,G,'turbo');}''',difficulty)
   trace=[]
   for i in range(360):
    e=p.evaluate(STEP,1)
    if e:raise RuntimeError(e)
    if i==140:p.evaluate('player.x=40')
    if i%3==0:trace.append(p.evaluate('''()=>({act:boss._rebels.ships.find(q=>q.key==='voss').rg4.act?.kind,phase:boss._rebels.ships.find(q=>q.key==='voss').rg4.act?.phase,rounds:rg4State().ord.filter(z=>z._or44&&!z.dead).map(z=>({row:z._or44Row,side:z._or44Side,x:z.x,y:z.y,vx:z.vx,vy:z.vy,r:z.r,t:z.t,original:z._or44Velocity,origin:z._or44Origin}))})'''))
    if difficulty=='furious'and i in [120,150,180]:p.screenshot(path=str(W/f'voss-probe-{i}.png'))
   events=p.evaluate('OR44.events');orbs=[e for e in events if e['event']=='orb'];pairs={e['row']for e in orbs}
   ck(difficulty+' native five rows and ten orbs',len(orbs)==10,len(orbs))
   ck(difficulty+' simultaneous pairs from two live sockets',all(len([e for e in orbs if e['row']==r])==2 for r in pairs))
   ck(difficulty+' 33 percent faster travel',all(abs(math.hypot(e['vx'],e['vy'])-240)<1e-6 for e in orbs))
   moving=[z for s in trace for z in s['rounds']]
   ck(difficulty+' constant velocity after target moves',all(abs(z['vx']-z['original']['x'])<1e-7 and abs(z['vy']-z['original']['y'])<1e-7 for z in moving))
   ck(difficulty+' columns keep their firing socket horizontal positions',all(z['vx']==0 and abs(z['x']-z['origin']['x'])<1e-6 for z in moving))
   distances=[]
   for s in trace:
    for row in set(z['row']for z in s['rounds']):
     pair=[z for z in s['rounds']if z['row']==row]
     if len(pair)==2:
      a,b=pair;distances.append(abs((a['x']-b['x'])-(a['origin']['x']-b['origin']['x']))+abs((a['y']-b['y'])-(a['origin']['y']-b['origin']['y'])))
   ck(difficulty+' pair rows never converge',len(distances)>10 and max(distances)<1e-6,dict(samples=len(distances),maxError=max(distances)))
   ck(difficulty+' continues into native turbo sequence',any(s['phase']=='turbocharge'for s in trace)and any(s['phase']=='dash'for s in trace))
   (W/(difficulty+'-voss-trace.json')).write_text(json.dumps(dict(events=events,trace=trace),indent=2))
  ck('Complete fixed-cell normal and hit atlas loaded',p.evaluate("XART.rdy('or44_orbs')&&XART.get('or44_orbs').width===384&&XART.get('or44_orbs').height===384"))
  ck('Stage X excluded',p.evaluate("(()=>{const q=boss._rebels.ships.find(q=>q.key==='voss');run._gp4StageX=true;const v=or44Own(q);run._gp4StageX=false;return !v})()"))
  ck('Rook retains existing machine gun owner',p.evaluate("!or44Own(boss._rebels.ships.find(q=>q.key==='rook'))"))
  # Inspect source frame selection in the native draw owner, including real hit response.
  ck('Native hit selects white bank and expires',p.evaluate("""(()=>{const q=boss._rebels.ships.find(q=>q.key==='voss'),G=rg4State();const o={kind:'energy',owner:q,x:340,y:260,r:13,hp:2,max:2,t:.1,life:5,flash:0,_or44:true,_vs41Orb:true,_rr26Energy:true,vx:0,vy:0};G.ord.push(o);rg4OrdnanceHit(G,o,.2);let ys=[];const draw=ctx.drawImage;ctx.drawImage=function(...a){ys.push(a[2]);};try{rg4OrdnanceDraw(o,G);o.flash=0;rg4OrdnanceDraw(o,G);}finally{ctx.drawImage=draw;o.dead=true;}return ys[0]>=192&&ys[1]<192&&o.hp<2;})()"""))
  ck('Destroyed cannon emits no orb',p.evaluate("""(()=>{const q=boss._rebels.ships.find(q=>q.key==='voss'),G=rg4State(),mods=fr27RebelModules(q);const m=mods.find(m=>m.id==='left'),hp=m.hp;m.hp=0;OR44.events=[];vs41Release(q,G,{tx:q.x,ty:500,round:0});const es=OR44.events.filter(e=>e.event==='orb');m.hp=hp;return es.length===1&&es[0].side===1;})()"""))
  ck('No native JavaScript errors',not errors,errors);br.close()
 print(json.dumps(dict(passed=len(checks),checks=checks),indent=2))
finally:stop()
