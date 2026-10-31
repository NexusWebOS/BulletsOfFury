from pathlib import Path
import sys,json,math,http.server
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];W=R/'_shots/nightwing_side_facing_1030/probe';W.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import serve,TRAP_RAF,STEP
http.server.ThreadingHTTPServer.request_queue_size=256
checks=[];errors=[];http=[]
def ck(name,passed,data=None):
 checks.append(dict(name=name,passed=bool(passed),data=data));(W/'checks.json').write_text(json.dumps(dict(checks=checks,errors=errors,http=http),indent=2));assert passed,(name,data)
port,stop=serve(str(R))
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1280,'height':800})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'or'draw error'in m.text else None);p.on('response',lambda r:http.append(r.url)if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}',timeout=180000);p.wait_for_function('window.__bofFrames>5');p.mouse.click(3,3);p.evaluate('()=>{run.stage=6;stageLoadBegin(6)}');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(6)}',timeout=180000);p.evaluate(TRAP_RAF)
  def step(n):
   e=p.evaluate(STEP,n)
   if e:raise RuntimeError(e)
  p.evaluate("()=>{diffKey='furious';debugUnlocked=true;debugStartFight({stage:6,role:'boss',kind:'warhive'},{pilot:'cole',record:false});DBGT.god=true;spawnBoss('warhive');debugFight.spawned=true;warnT=0;BOFCinematicDirector.cancel();setState(GS.PLAY);bossActive=true;s6Wing.ships=[];delete boss._carrier17;boss._whv.mode='ace';whvAceSpawn(boss);}");step(450)
  # A fixture enters the actual 25% threshold. Native owners choose all three
  # routes, warnings, durations, wobble and inverted return without phase writes.
  p.evaluate('''()=>{const b=boss,A=b._whv.ace;nw30Cancel(b);A.roll=A.somer=A.dash=A.desp=null;A._nw28.mode='fight';A.st='fight';A.inverted=false;A.gunCd=A.rollCd=A.somerCd=A.dashCd=99;b._nw30.gunCd=b._nw30.windCd=99;b.hp=b.maxhp*.24;A.x=camLeftX()+viewW()/2;A.y=200;player.y=VH-95;player.x=camLeftX()+viewW()/2;nf29Sync(b);window.flightCalls=[];window.originalBlit=ctx.drawImage;ctx.drawImage=function(im,...a){for(const[k,m]of Object.entries(NW30_ART.banks))if(im===XART.get(m.key)){flightCalls.push({bank:k,frame:Math.floor(a[1]/m.ch)*m.cols+Math.floor(a[0]/m.cw),x:a[4],y:a[5],w:a[6],h:a[7]});break;}return originalBlit.apply(this,[im,...a]);};}''')
  rows=[];shots=set()
  for i in range(500):
   step(1)
   q=p.evaluate('''()=>{const b=boss,A=b._whv.ace,P=A.desp,p=nw30Pose(b);flightCalls=[];nw28DrawBody(b);return{x:A.x,y:A.y,state:P?.st,pass:P?.pass,t:P?.t,lead:P?.lead,bank:p.bank,frame:p.frame,yaw:p.meta.angle+Math.PI/2,modular:nw30Modular(b),calls:flightCalls,engines:NW30.last?.engines,left:camLeftX(),right:camRightX(),hp:b.hp};}''');rows.append(q)
   if q['state']=='cross'and q['t']>q['lead']and q['left']+140<q['x']<q['right']-140 and q['pass']not in shots:
    shots.add(q['pass']);p.evaluate('()=>{drawWorld(0);SC12.refresh();__bofFit()}');p.screenshot(path=str(W/f"side-pass-{q['pass']}.png"))
   if q['state']=='done':break
  (W/'trace.json').write_text(json.dumps(rows,indent=2))
  active=[q for q in rows if q['state']=='cross'and q['t']>q['lead']and q['left']<q['x']<q['right']]
  ck('Native low-health attack crosses all three routes and returns',len(shots)==3 and rows[-1]['state']=='done',dict(routes=sorted(shots),frames=len(rows)))
  ck('Every visible crossing uses a whole authored directional hull',all(q['bank']=='heading'and not q['modular']and any(c['bank']=='heading'and c['frame']==q['frame']for c in q['calls'])for q in active))
  errors_angle=[];directions=set();frames=set()
  for a,b in zip(rows,rows[1:]):
   if a['state']==b['state']=='cross'and a['pass']==b['pass']and a['t']>=a['lead']and b['left']<b['x']<b['right']:
    dx=b['x']-a['x'];dy=b['y']-a['y'];yaw=math.atan2(dy,dx);errors_angle.append(abs(math.atan2(math.sin(yaw-b['yaw']),math.cos(yaw-b['yaw']))));directions.add(1 if dx>0 else -1);frames.add(b['frame'])
  ck('Both side directions face the real per-frame travel vector',directions=={-1,1}and max(errors_angle)<.15,dict(maxDegrees=math.degrees(max(errors_angle)),directions=sorted(directions)))
  ck('Wavering flight advances multiple actual rotation frames',len(frames)>=8,sorted(frames))
  ck('Directional shadow and thrusters remain attached to the same heading',all(any(c['bank']=='heading_shadow'and c['frame']==q['frame']for c in q['calls'])and any(c['bank'].startswith('exhaust_boost')for c in q['calls'])for q in active))
  ck('Inverted return clears temporary side-pass poses',p.evaluate('boss._whv.ace.inverted&&!boss._whv.ace._nf29Pose&&!boss._whv.ace._nw32SidePose'))
  # Actual rotated pose must remain hittable, white flash must render and expire.
  q=p.evaluate('''()=>{const b=boss,A=b._whv.ace;nw30Cancel(b);A.desp={st:'cross',t:.9,lead:.62,dur:.95,pass:0,x0:camLeftX()-120,x1:camRightX()+120,y0:240,y1:440};A.roll=A.somer=A.dash=null;A.inverted=false;whvAceDesperation(b,A,0);A.x=camLeftX()+viewW()/2;A.y=250;nf29Sync(b);b._noHit=false;b._gp4FlashNext=0;b.flash=0;let hits=0;for(let y=A.y-80;y<A.y+80;y+=8)for(let x=A.x-80;x<A.x+80;x+=8)if(warhiveHitTest(b,x,y))hits++;markHit(b);flightCalls=[];nw28DrawBody(b);return{hits,flash:b.flash,calls:flightCalls};}''')
  ck('Rotated hull retains real alpha hits and matched white damage frame',q['hits']>30 and q['flash']>0 and any(c['bank']=='heading_hit'for c in q['calls']),q)
  p.evaluate('()=>{drawWorld(0);SC12.refresh();__bofFit()}');p.screenshot(path=str(W/'side-hit.png'));step(24);ck('Directional damage flash expires normally',p.evaluate('boss.flash===0'))
  p.evaluate('()=>{ctx.drawImage=originalBlit;run.stage=7}');ck('Other stages keep their native heading metadata',p.evaluate("nf29Art('heading')===NF29_ART.banks.heading"))
  ck('No native browser, draw or asset errors',not errors and not http,dict(errors=errors,http=http));br.close()
finally:stop()
print(len(checks),'Nightwing directional-pass checks passed')
