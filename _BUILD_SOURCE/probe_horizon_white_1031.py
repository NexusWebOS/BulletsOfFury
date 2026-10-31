from pathlib import Path
import sys,json,http.server,math,hashlib
from playwright.sync_api import sync_playwright
R=Path(r'C:\Users\Mike\Desktop\Github Coding\BulletsOfFury');W=R/'_shots/horizon_white_optics_1031';W.mkdir(parents=True,exist_ok=True);O=W/'probe';O.mkdir(exist_ok=True)
sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import serve,STEP
from barrage_review_common_1025 import boot
http.server.ThreadingHTTPServer.request_queue_size=256;checks=[];errors=[]
def ck(name,v,data=None):
 checks.append(dict(name=name,passed=bool(v),data=data));(W/'checks.json').write_text(json.dumps(checks,indent=2));print('PASS'if v else'FAIL',name,(' '+str(data)[:300])if not v else'',flush=True)
def step(p,n):
 for i in range(0,n,20):
  e=p.evaluate(STEP,min(20,n-i));assert not e,e;p.wait_for_timeout(1)
def snap(p,name):p.evaluate('drawWorld(0)');p.screenshot(path=str(O/(name+'.png')))
port,stop=serve(str(R))
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=boot(br.new_context(viewport={'width':1280,'height':800}),port,9,errors)
  p.wait_for_function('()=>{stageLoadTick();return Object.values(EH91_ART).every(a=>XART.rdy(a.key))}',timeout=120000)
  p.evaluate("()=>{diffKey='furious';debugStartFight({stage:9,role:'mini',kind:'voidhorizon'},{pilot:'cole',record:false});DBGT.god=true;DBGT.speed=1;player.invuln=1e9;spawnSubBoss('voidhorizon');debugFight.spawned=true;warnT=0;subBossActive=true;setState(GS.PLAY);window.B=subBoss;window.H=eh57State(B);window.full=B.hp;pBullets=[];eBullets=[];BOFCinematicDirector.cancel();story=null;}")
  ck('Native Furious core health is intact and matches its hull',p.evaluate("diffKey==='furious'&&B.hp===B.maxhp&&B.hp===B._s9rift.core.maxhp&&B.hp>9000"),p.evaluate('B.maxhp'))
  ck('White cannon banks are fully ready before firing',p.evaluate('Object.values(EH91_ART).every(a=>XART.rdy(a.key))'))
  # Actual render instrumentation records only native blits, then restores the API.
  calls="""()=>{const old=eh57Blit,out=[];eh57Blit=function(...a){out.push(a);return old.apply(this,a)};try{s9VoidHorizonDraw(B)}finally{eh57Blit=old}return out;}"""
  p.evaluate('()=>{window.entryTrace=[];window.__qaTick=()=>entryTrace.push({a:H.angle,t:H.clock})}');step(p,125);p.evaluate('window.__qaTick=null');tr=p.evaluate('entryTrace');ck('Hull rotation runs continuously through the entry',all(abs((y['a']-x['a'])-(y['t']-x['t'])*math.tau*.6)<.00001 for x,y in zip(tr,tr[1:]))and tr[-1]['a']>tr[0]['a'],tr[:2])
  ck('Core and hull share one pose index',p.evaluate("()=>{const old=eh57Blit,out=[];eh57Blit=(...a)=>out.push(a);try{s9VoidHorizonDraw(B)}finally{eh57Blit=old}const hull=out.find(a=>a[0].startsWith('ship')),eye=out.find(a=>a[0].startsWith('eye'));return Math.floor(eye[1]/8)===hull[1]&&eye[2]===hull[2]&&eye[3]===hull[3];}"))
  p.evaluate("eh57Set(B,'spiral')");step(p,64);snap(p,'01-charge');d=p.evaluate(calls)
  ck('Core white charge brightens at the physical optic',any(q[0]=='eye_glow'and q[1]%8>=5 and abs(q[2]-p.evaluate('B.x'))<.01 for q in d),d[:4])
  step(p,18);snap(p,'02-release');ck('Native release produces two core-rooted spirals',p.evaluate('H.beams.length===48&&[0,24].every(i=>Math.hypot(H.beams[i].x-B.x,H.beams[i].y-B.y)<.001)'))
  d=p.evaluate(calls);ck('White cannon muzzle appears only when the core fires',any(q[0]=='muzzle'for q in d)and not any(q[0]in['orb','orb_water']for q in d),[q for q in d if q[0]in['muzzle','orb','orb_water']])
  ck('All beam states resolve to the level-4 white cannon sheet',p.evaluate('ER28_ART.eh57_beam.key===EH91_ART.beam.key&&ER28_ART.eh57_beam_water.key===EH91_ART.beam.key'))
  d=p.evaluate("()=>{const a=H.angle,r=Math.atan2(H.beams[0].ey-B.y,H.beams[0].ex-B.x);return{a,r,frame:H.frame}}")
  step(p,18);e=p.evaluate("()=>({a:H.angle,r:Math.atan2(H.beams[0].ey-B.y,H.beams[0].ex-B.x),frame:H.frame})")
  delta=lambda x,y:math.atan2(math.sin(x-y),math.cos(x-y))
  ck('Spiral and hull turn at exactly the same angular speed',abs(delta(e['r'],d['r'])-(e['a']-d['a']))<.001,[d,e])
  p.evaluate('window.trace=[]');
  for i in range(125):
   step(p,1);p.evaluate('trace.push({a:H.angle,f:H.frame,t:H.t,mode:H.mode,phase:H.phase})')
  trace=p.evaluate('trace');ck('Rotation never stalls or resets across wraps',all(abs(y['a']-x['a']-math.tau*.6/60)<.00001 for x,y in zip(trace,trace[1:]))and any(x['f']==31 and y['f']==0 for x,y in zip(trace,trace[1:])))
  for mode in['beam','sweep','spin','orb']:
   p.evaluate('(m)=>eh57Set(B,m)',mode);a=p.evaluate('H.angle');step(p,100);d=p.evaluate('({a:H.angle,mode:H.mode,phase:H.phase,beams:H.beams.length})')
   ck(mode+' uses the same uninterrupted rotation',abs(d['a']-a-100/60*math.tau*.6)<.001,d)
   if mode in['beam','sweep']:
    d=p.evaluate('({a:H.angle,ray:H.beams[0].a})');step(p,8);e=p.evaluate('({a:H.angle,ray:H.beams[0].a})');ck(mode+' firing line is locked to the hull clock',abs((e['a']-d['a'])-(e['ray']-d['ray']))<.00001)
  ck('Projectiles remain native unshootable ordnance',p.evaluate('eBullets.some(q=>q._eh57Owner===B)&&eBullets.filter(q=>q._eh57Owner===B).every(q=>!enemyOrdnanceCanIntercept(q)&&q._weaponProof&&!q._shootable)'))
  # User asked to retire bullet stars, while authored attack tells remain.
  ck('All wrapped near-collision predictors return no bullet markers',p.evaluate("()=>[{}, {_eh57Owner:B}, {_jr36Bullet:true}, {_nx37Laser:true}, {_rr26KaiaRoller:true}, {kind:'helix',owner:{key:'jace'}}].every(q=>pw5Impact({...q,x:player.x,y:player.y-50,vx:0,vy:3},player)===null)"))
  noDraw=p.evaluate("()=>{PW5.threats=[{p:{x:100,y:100},t:.1}];const before=PW5.draws,di=ctx.drawImage;let imgs=0;ctx.drawImage=function(){imgs++;return di.apply(this,arguments)};try{pw5Draw();}finally{ctx.drawImage=di;}return {imgs,before,after:PW5.draws,fn:pw5Draw.toString()};}")
  ck('Even stale bullet-marker state cannot draw an asterisk',noDraw['imgs']==0 and noDraw['before']==noDraw['after'],noDraw);step(p,1);ck('Native update discards obsolete marker state',p.evaluate('PW5.threats.length===0'))
  p.evaluate("eh57Set(B,'beam')");step(p,12);ck('Authored filled rotation warning is retained',p.evaluate("()=>{const old=rk50Blit,out=[];rk50Blit=(...a)=>out.push(a);try{eh57Warning(B,H)}finally{rk50Blit=old}return out.some(a=>a[0]==='field')&&out.some(a=>a[0]==='symbol');}"))
  # Native damaged pixels, not just a flash timer assertion.
  step(p,80);d=p.evaluate("""()=>{drawWorld(0);const a=ctx.getImageData(0,0,cv.width,cv.height).data,hp=B.hp;s9VoidHorizonHit(B,5,B.x,B.y);drawWorld(0);const b=ctx.getImageData(0,0,cv.width,cv.height).data;let n=0;for(let i=0;i<b.length;i+=4)if(b[i]>240&&b[i+1]>240&&b[i+2]>240&&a[i]+a[i+1]+a[i+2]<650)n++;return{white:n,hp,after:B.hp};}""")
  ck('Native damage and visible white hull feedback work',d['after']<d['hp']and d['white']>5,d);step(p,18);ck('Hit flash expires normally',p.evaluate('B._s9rift.core.flash===0'))
  # Native beam collision at its actual current geometry.
  d=p.evaluate("""()=>{const L=H.beams[0],old=playerHit;let calls=0;playerHit=()=>calls++;DBGT.god=false;player.invuln=0;player.x=L.x+Math.cos(L.a)*90;player.y=L.y+Math.sin(L.a)*90;H.hit.clear();try{eh57Touch(B,H)}finally{playerHit=old;DBGT.god=true;player.invuln=1e9}return calls;}""")
  ck('White beam still calls native player damage on contact',d==1,d)
  p.evaluate('s9VoidHorizonHit(B,999999,B.x,B.y)');ck('Oversized hit preserves the exact half-health gate',p.evaluate("H.half&&H.mode==='half'&&B.hp===B.maxhp*.5&&!B.dead"))
  ck('Half transformation rejects damage and Retina targets',p.evaluate('()=>{const hp=B.hp;s9VoidHorizonHit(B,40,B.x,B.y);return B.hp===hp&&!retinaBossTargets(B).length}'))
  a=p.evaluate('H.angle');step(p,150);ck('Half-health charge and return never interrupt rotation',abs(p.evaluate('H.angle')-a-150/60*math.tau*.6)<.001)
  p.evaluate("eh57Set(B,'dash')");step(p,200);snap(p,'03-half-edge-charge');step(p,40);snap(p,'04-half-dash')
  ck('Dash retains the physical three-way spinning laser paths',p.evaluate("H.phase==='dash'&&H.beams.length===3&&!H.protected"),p.evaluate('({phase:H.phase,t:H.t,beams:H.beams.length})'))
  a=p.evaluate('H.angle');step(p,200);ck('Dash exit and return keep the same rotation speed',abs(p.evaluate('H.angle')-a-200/60*math.tau*.6)<.001)
  p.evaluate("eh57Set(B,'spiral')");step(p,105);snap(p,'05-half-white-spirals');d=p.evaluate(calls)
  ck('Half-health optics still use white cannon and core muzzle',any(q[0]=='muzzle'for q in d)and any(q[0]=='eye_white'for q in d))
  ck('All owned rounds remain within their budget',p.evaluate('eBullets.filter(q=>q._eh57Owner===B&&!q.dead).length<=120'))
  a=p.evaluate('H.angle');p.evaluate('setState(GS.PAUSE)');step(p,60);ck('Pause freezes the shared simulation rotation',p.evaluate('H.angle')==a);p.evaluate('setState(GS.PLAY)')
  p.evaluate('s9VoidHorizonHit(B,999999,B.x,B.y)');step(p,1);ck('Native defeat clears beams and owned projectiles',p.evaluate('B.dead&&B.hp===0&&!H.beams.length&&!eBullets.some(q=>q._eh57Owner===B&&!q.dead)'))
  ck('Browser has no page or render exceptions',not errors,errors);br.close()
finally:stop()
print('RESULT',sum(c['passed']for c in checks),'/',len(checks));assert all(c['passed']for c in checks)
