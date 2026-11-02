"""Native paired bomber flight, mirrored landings and committed Retina checks."""
from pathlib import Path
import json,sys,http.server
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];W=R/'_shots/herald_straight_1031/probe';W.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(R/'_BUILD_SOURCE'))
from shoot import serve,STEP
from barrage_review_common_1025 import boot
http.server.ThreadingHTTPServer.request_queue_size=256
checks=[];errors=[];cases=[]
def ck(n,v,d=None):
 checks.append(dict(name=n,passed=bool(v),data=d));print('PASS'if v else'FAIL',n,json.dumps(d)[:900]if not v else'',flush=True)
 (W/'checks.json').write_text(json.dumps(checks,indent=2))
def step(p,n):
 for i in range(0,n,30):
  err=p.evaluate(STEP,min(30,n-i))
  if err:raise RuntimeError(err)
  p.wait_for_timeout(1)
def start(p,difficulty):
 p.evaluate("""d=>{diffKey=d;debugStartFight({stage:8,role:'mini',kind:'heralddeath'},{pilot:'cole',record:false});spawnSubBoss('heralddeath');debugFight.spawned=true;subBossActive=true;warnT=0;DBGT.god=true;player.invuln=1e9;BOFCinematicDirector.cancel();setState(GS.PLAY);window.B=subBoss;HB25.events=[];HL51.events=[];HH52.events=[];pBullets=[];eBullets=[];}""",difficulty)
 step(p,150);p.evaluate("()=>{HB25.events=[];HL51.events=[];HH52.events=[];hb25Flight(B,'bomber')}")
def snap(p):return p.evaluate("""()=>{const Q=B._hd1003._hb25;return Q?{clock:efxClock,t:Q.t,warm:Q.warm,phase:Q.phase,pass:Q.pass,total:Q.total,left:Q.planLeft??camLeftX(),width:Q.planWidth??viewW(),x:B.x,y:B.y,angle:Q.angle,escape:Q.escapeX,path:Q.path,plan:Q.plan?.map(p=>({...p,target:{...p.target}}))}:null}""")
port,stop=serve(str(R))
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);bc=br.new_context(viewport={'width':1280,'height':800});p=boot(bc,port,8,errors)
  for difficulty in ['normal','hard','furious']:
   start(p,difficulty);plans={};positions=[];screens=set();mark_checked=False;middle=[];fov=set();fields=[];body_pixels=None
   for i in range(500):
    q=snap(p)
    if q is None:break
    positions.append([q['x'],q['y'],q['clock']])
    if(q['pass']==0 and q['phase']=='strike')or(q['pass']==1 and q['phase']in ['tell','strike']):middle.append(q)
    if q['pass']==1 and q['phase']=='tell':
     fov.add('green'if q['t']/q['warm']<.55 else'yellow'if q['t']/q['warm']<.82 else'red')
     fields+=p.evaluate("""()=>{const old=combatWarningDraw,rows=[];combatWarningDraw=function(o,a){rows.push(a);return old.apply(this,arguments)};try{drawWorld(0)}finally{combatWarningDraw=old}return rows.filter(q=>q.width===80&&q.ex>q.x&&q.y===q.ey)}""")
     if body_pixels is None:
      body_pixels=p.evaluate("""()=>{ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,cv.width,cv.height);for(const part of B._hd1003.parts)if(hd1003Live(B,part))hd1003Blit(part,hd1003Pose(B,part),0,1);const d=ctx.getImageData(0,0,cv.width,cv.height).data;let n=0;for(let i=0;i<d.length;i+=4)if(d[i]||d[i+1]||d[i+2])n++;ctx.restore();drawWorld(0);return n}""")
     if difficulty=='furious'and 'warning'not in screens and q['t']/q['warm']>.55:
      p.screenshot(path=str(W/'rightward-fov.png'));screens.add('warning')
    if q['phase']=='tell'and q['pass']not in plans:
     plans[q['pass']]=q
     if q['pass']==0:p.evaluate('player.x=Math.max(camLeftX()+75,player.x-85)')
    if difficulty=='furious'and q['phase']=='strike'and q['pass']not in screens and q['left']+q['width']*.35<q['x']<q['left']+q['width']*.65:
     p.evaluate('drawWorld(0)');p.screenshot(path=str(W/f'pass-{q["pass"]}.png'));screens.add(q['pass'])
    if not mark_checked and p.evaluate('eBullets.some(q=>q._hl51&&!q.dead)'):
     marks=p.evaluate("()=>eBullets.filter(q=>q._hl51&&!q.dead).map(q=>({id:q._hl51,target:{...q._hb25Bomb.target}}))")
     p.evaluate('player.x+=20');step(p,3)
     stable=p.evaluate('(a)=>a.every(o=>{const q=eBullets.find(q=>q._hl51===o.id);return!q||q._hb25Bomb.target.x===o.target.x&&q._hb25Bomb.target.y===o.target.y})',marks)
     ck(difficulty+': released bomb targets stay fixed while player moves',stable);mark_checked=True
    step(p,3)
   ck(difficulty+': native flight makes both bomber passes',set(plans)=={0,1}and plans[0]['total']==2,list(plans))
   a,b=plans[0],plans[1]
   ck(difficulty+': leftward first pass then rightward second pass',a['path']['to']['x']<a['path']['from']['x']and b['path']['to']['x']>b['path']['from']['x'],[a['path'],b['path']])
   mirrored=len(a['plan'])==len(b['plan'])and all(any(abs((x['target']['x']-a['left'])/a['width']+(y['target']['x']-b['left'])/b['width']-1)<1e-7 and x['wave']==y['wave']and x['burst']==y['burst']and x['id']!=y['id']for y in b['plan'])for x in a['plan'])
   ck(difficulty+': mirrored landing pattern retains its wave identities',mirrored,[len(a['plan']),len(b['plan'])])
   ck(difficulty+': no upward detour between bombing passes',max(z['y']for z in middle)-min(z['y']for z in middle)<1e-6)
   ck(difficulty+': complete hull is invisible during rightward warning',body_pixels==0,body_pixels)
   ck(difficulty+': authored rightward FOV passes green yellow red',fov=={'green','yellow','red'}and len(fields)>0,dict(colours=sorted(fov),fields=len(fields)))
   waiting=[z for z in middle if z['pass']==1 and z['phase']=='tell'];ck(difficulty+': full stationary warning before flying right',len(waiting)>4 and max(z['x']for z in waiting)-min(z['x']for z in waiting)<1e-6 and waiting[-1]['t']>waiting[-1]['warm']-.10)
   ck(difficulty+': committed safe opening mirrors too',abs((a['escape']-a['left'])/a['width']+(b['escape']-b['left'])/b['width']-1)<1e-7)
   e=p.evaluate('({drops:HL51.events.filter(e=>e.event==="drop"),impacts:HL51.events.filter(e=>e.event==="impact"),flight:HH52.events})');drops=e['drops']
   ck(difficulty+': real bombs release on both passes',set(d['pass']for d in drops)=={0,1},[{k:d[k]for k in ['pass','wave','part','target']}for d in drops])
   ck(difficulty+': actual release velocities reach their exact ground Retinas',all(abs(d['x']+d['vx']*60*(d['at']-d['time'])-d['target']['x'])<1e-5 and abs(d['y']+d['vy']*60*(d['at']-d['time'])-d['target']['y'])<1e-5 for d in drops))
   ck(difficulty+': every observed impact lands on its own warning',len(e['impacts'])>0 and all(any(d['id']==z['id']and d['target']['x']==z['x']and d['target']['y']==z['y']for d in drops)for z in e['impacts']))
   jumps=[((((positions[j][0]-positions[j-1][0])**2+(positions[j][1]-positions[j-1][1])**2)**.5)/(positions[j][2]-positions[j-1][2]),j,positions[j-1],positions[j])for j in range(1,len(positions))]
   ck(difficulty+': return is continuous and completes native recovery',q is None and max(z[0]for z in jumps)<1000.01 and any(z['event']=='flight-return-complete'for z in e['flight']),dict(ended=q is None,maxPixelsPerSecond=max(z[0]for z in jumps)))
   cases.append(dict(difficulty=difficulty,plans=plans,events=e))
  # A new pair with only one surviving claw still has a mirrored second pass.
  start(p,'furious');p.evaluate("()=>{hd1003Hit(B,hd1003Part(B,'gunR').hp+1,0,0,'gunR');hb25Flight(B,'bomber')}")
  one=[]
  for i in range(1100):
   q=snap(p)
   if q is None:break
   if q['phase']=='tell'and not any(z['pass']==q['pass']for z in one):one.append(q)
   step(p,1)
  ck('One surviving claw retains both nonempty mirrored passes',len(one)==2 and all(z['plan']and all(d['id']=='gunL'for d in z['plan'])for z in one),[len(z['plan'])for z in one])
  start(p,'furious');p.evaluate("()=>{window.Q=B._hd1003._hb25}")
  for i in range(180):
   if p.evaluate('Q.phase==="tell"'):break
   step(p,1)
  p.evaluate("()=>{hd1003Hit(B,hd1003Part(B,'gunR').hp+1,0,0,'gunR');Q.pass=1;Q.path=hb25Corner(B,Q);hb25BombPlan(B,Q)}")
  ck('A claw destroyed between passes has no pending return drops',p.evaluate('Q.plan.length>0&&Q.plan.every(p=>p.id==="gunL")'))
  ck('Native ordinary bombs remain non-interceptible from release',p.evaluate("()=>{const m=hd1003Muzzle(B,'gunL');eBullets=[];hb25BombDrop(B,{escapeX:camLeftX()+40,rank:3,drops:0,pass:0},{id:'gunL',target:{x:camLeftX()+viewW()*.6,y:VH-36},burst:true,seed:1,wave:0});return eBullets.length>0&&eBullets.every(q=>!enemyOrdnanceCanIntercept(q))}"))
  ck('No native page/console errors',not errors,errors)
  (W/'cases.json').write_text(json.dumps(cases,indent=2));br.close()
finally:stop()
print('RESULT',sum(x['passed']for x in checks),'/',len(checks),flush=True)
if any(not x['passed']for x in checks):raise SystemExit(1)
