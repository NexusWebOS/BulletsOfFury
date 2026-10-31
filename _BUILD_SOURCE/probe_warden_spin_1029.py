from pathlib import Path
import sys,json,http.server
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];W=R/'_shots/warden_spin_1029/probe';W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'))
from shoot import serve,STEP
from barrage_review_common_1025 import boot
http.server.ThreadingHTTPServer.request_queue_size=256;checks=[];errors=[]
def ck(n,v,d=None):checks.append(dict(name=n,passed=bool(v),data=d));(W/'checks.json').write_text(json.dumps(checks,indent=2));print('PASS'if v else'FAIL',n,str(d)[:400]if not v else'',flush=True)
def step(p,n):
 for i in range(0,n,30):
  err=p.evaluate(STEP,min(30,n-i))
  if err:raise RuntimeError(err)
  p.wait_for_timeout(1)
def snap(p,n):p.evaluate('drawWorld(0)');p.screenshot(path=str(W/(n+'.png')))
port,stop=serve(str(R))
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);bc=br.new_context(viewport={'width':1280,'height':800});p=boot(bc,port,7,errors)
  p.evaluate('()=>{run.stage=7;stageLoadBegin(7)}');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(7)}',timeout=240000)
  p.evaluate("()=>{beginStage(7);BOFCinematicDirector.cancel();story=null;diffKey='furious';debugStartFight({stage:7,role:'boss',kind:'sludgeemperor'},{pilot:'cole',record:false});spawnBoss('sludgeemperor');debugFight.spawned=true;bossActive=true;warnT=0;DBGT.god=true;player.invuln=1e9;BOFCinematicDirector.cancel();setState(GS.PLAY);window.B=boss;pBullets=[];eBullets=[];}");step(p,650)
  ck('Spin, front and shadow banks preload',p.evaluate('Object.values(WS56_ART).every(a=>XART.rdy(a.key))'))
  hazards=p.evaluate("""()=>{const d=ctx.drawImage,h=playerHit;let draws=0,hits=0;ctx.drawImage=function(){draws++;return d.apply(this,arguments)};playerHit=()=>hits++;try{for(const diff of ['easy','normal','hard','furious']){diffKey=diff;run._s7Sluices=[{live:true,t:4,side:1,row:200}];stage7SluiceTick(10);stage7SluiceDraw();}return{draws,hits,events:stage7SluiceEvents().length}}finally{ctx.drawImage=d;playerHit=h;diffKey='furious'}}""")
  ck('Pipe hazards draw nothing on every difficulty',hazards['draws']==0,hazards)
  ck('Removed pipe hazards cannot damage players or persist saved events',hazards['hits']==0 and hazards['events']==0)
  p.evaluate("s7mSet(B,'er28-guns')");step(p,20);snap(p,'front-barrels-no-pipes')
  d=p.evaluate("""()=>{const pose=s7mPose(B),f=s7mBlit,draws=[];s7mBlit=function(...a){draws.push({name:a[0],i:a[1]});return f.apply(this,a)};try{s7mDraw(B)}finally{s7mBlit=f}return{ids:pose.map(p=>p.id),draws}}""")
  ck('Both gun poses are ordered in front of the head',d['ids'][-2:]==['gunL','gunR'],d)
  guns=[i for i,q in enumerate(d['draws'])if q['name']=='warden'and q['i']==5];head=[i for i,q in enumerate(d['draws'])if q['name']=='warden'and q['i']==7]
  ck('Native renderer actually paints live guns after the face',len(guns)>=2 and head and min(guns)>max(head),d)
  p.evaluate("()=>{for(const id of ['frontL','frontR','rearL','rearR','gunL','gunR','canL','canR']){const part=B._s7mod.parts.find(p=>p.id===id)||B._s7mod.er28Canisters.find(p=>p.id===id);if(part?.hp>0)s7mHit(B,part.hp+10,0,0,id)}s7mSet(B,'ws56-spin');WS56.events=[];window.M=B._s7mod;window.core=M.core;}")
  ck('Native module destruction exposes the existing living core pool',p.evaluate('ws56Ready(B)&&M.core===M.coreMax&&s7mLive(M,\'front\').length===0&&sw28Can(M).length===0'))
  step(p,40);snap(p,'spin-warning');ck('Spin warns a committed ground landing point',p.evaluate("!!ws56Active(B)&&M.t<M.warn&&M.ws56.targets.length===5"))
  step(p,50);snap(p,'spin-airborne');ck('Spinning core rises with a ground shadow',p.evaluate("M.height>15&&M.ws56.frame>0&&M.ws56.frame<32"),p.evaluate('({height:M.height,frame:M.ws56.frame})'))
  step(p,300);snap(p,'spin-slams');ck('Spin delivers five distinct circular ground slams',p.evaluate("WS56.events.filter(e=>e.event==='slam'&&e.kind==='spin').length===5&&new Set(WS56.events.filter(e=>e.event==='slam').map(e=>Math.round(e.x))).size>=4"),p.evaluate('WS56.events'))
  ck('Slam orbs use actual unshootable toxic ordnance',p.evaluate('eBullets.some(q=>q._er28Orb&&!q.dead)&&eBullets.filter(q=>q._er28Orb).every(q=>!enemyOrdnanceCanIntercept(q))'))
  p.evaluate('window.returnDX=0;window.returnX=B.x')
  for _ in range(34):
   step(p,1);p.evaluate('()=>{returnDX=Math.max(returnDX,Math.abs(B.x-returnX));returnX=B.x}')
  ck('Circling core returns smoothly instead of snapping to native center',p.evaluate("returnDX<4&&WS56.events.some(e=>e.event==='attack-complete'&&e.kind==='spin'&&Math.abs(e.x-worldWidth()/2)<.01)"),p.evaluate('({returnDX,x:B.x,mode:M.mode})'))
  p.evaluate("s7mSet(B,'ws56-hop')");step(p,75);snap(p,'backwards-hop');step(p,215);snap(p,'forward-hop')
  ck('Backward-forward hop has three committed landings',p.evaluate("()=>{const e=WS56.events.filter(e=>e.event==='slam'&&e.kind==='hop');return e.length===3&&e[0].y<e[1].y&&e[2].y<e[1].y}"),p.evaluate('WS56.events.filter(e=>e.event===\'slam\'&&e.kind===\'hop\')'))
  ck('New attacks leave the native HP unchanged without player hits',p.evaluate('M.core===core'))
  p.evaluate("()=>{s7mSet(B,'ws56-spin');window.nativeCalls=[];window.nativeHit=playerHit;playerHit=function(...a){nativeCalls.push(a);return nativeHit.apply(this,a)};const P=M.ws56.targets[0];player.x=P.x;player.y=P.y+M.drop+40;player.invuln=0;run.shield=0;}");step(p,126)
  ck('Ground slams use actual player damage',p.evaluate("nativeCalls.some(a=>a[0]==='Warden core ground slam')"),p.evaluate('nativeCalls'));p.evaluate('()=>{playerHit=nativeHit;player.invuln=1e9}')
  px=p.evaluate("""()=>{drawWorld(0);const a=ctx.getImageData(0,0,cv.width,cv.height).data,before=M.core;s7mHit(B,5,0,0,'core');drawWorld(0);const d=ctx.getImageData(0,0,cv.width,cv.height).data;let white=0;for(let i=0;i<d.length;i+=4)if(d[i]>240&&d[i+1]>240&&d[i+2]>240&&a[i]+a[i+1]+a[i+2]<650)white++;return{white,before,hp:M.core};}""")
  ck('Actual rotating core takes damage with white hit pixels',px['white']>4 and px['hp']<px['before'],px);step(p,20);ck('Rotating core hit flash expires',p.evaluate('M.coreFlash===0'))
  p.evaluate("()=>{M.ws56Turn=0;window.book=[];for(let i=0;i<3;i++){s7mNext(B);book.push(M.mode)}}")
  ck('Exposed core naturally chooses spin, hops and mortars',p.evaluate("book.join(',')==='ws56-spin,ws56-hop,er28-mortar'"),p.evaluate('book'))
  p.evaluate("()=>{s7mSet(B,'ws56-hop');s7mHit(B,99999,0,0,'core')}");ck('Defeat retains native zero-pool and escape state',p.evaluate("M.core===0&&M.mode==='dead'"));step(p,1)
  ck('No browser exceptions',not errors,errors);(W/'events.json').write_text(json.dumps(p.evaluate('WS56.events'),indent=2));br.close()
finally:stop()
print('RESULT',sum(c['passed']for c in checks),'/',len(checks));assert all(c['passed']for c in checks)
