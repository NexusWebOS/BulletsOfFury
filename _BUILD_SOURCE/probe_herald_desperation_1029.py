from pathlib import Path
import sys,json,http.server
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];W=R/'_shots/herald_desperation_1029/probe';W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'))
from shoot import serve,STEP
from barrage_review_common_1025 import boot
http.server.ThreadingHTTPServer.request_queue_size=256;checks=[];errors=[]
def ck(n,v,d=None):
 checks.append(dict(name=n,passed=bool(v),data=d));(W/'checks.json').write_text(json.dumps(checks,indent=2));print('PASS'if v else'FAIL',n,str(d)[:500]if not v else'',flush=True)
def step(p,n):
 for i in range(0,n,30):
  err=p.evaluate(STEP,min(30,n-i))
  if err:raise RuntimeError(err)
  p.wait_for_timeout(1)
def snap(p,name):p.evaluate('drawWorld(0)');p.screenshot(path=str(W/(name+'.png')))
port,stop=serve(str(R))
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);bc=br.new_context(viewport={'width':1280,'height':800});p=boot(bc,port,8,errors)
  p.evaluate('()=>{run.stage=8;stageLoadBegin(8)}');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(8)}',timeout=240000)
  p.evaluate("()=>{beginStage(8);BOFCinematicDirector.cancel();story=null;diffKey='furious';debugStartFight({stage:8,role:'mini',kind:'heralddeath'},{pilot:'cole',record:false});spawnSubBoss('heralddeath');debugFight.spawned=true;subBossActive=true;warnT=0;DBGT.god=true;player.invuln=1e9;BOFCinematicDirector.cancel();setState(GS.PLAY);window.B=subBoss;pBullets=[];eBullets=[];}");step(p,150)
  ck('All new authored depth and roller banks preload',p.evaluate('Object.values(HD54_ART).every(a=>XART.rdy(a.key))'))
  p.evaluate("()=>{window.full=B.hp;hd1003Hit(B,1,0,0,'core')}")
  ck('Above 20% uses the existing attack owners',p.evaluate('!B._hd1003.hd54&&B.hp===full-1'))
  p.evaluate("hd1003Hit(B,B.maxhp*10,0,0,'head')")
  ck('An oversized real native hit stops exactly at 20%',p.evaluate('!B.dead&&Math.abs(B.hp-B.maxhp*.2)<.001&&!!hd54Own(B)'),p.evaluate('({hp:B.hp,maxhp:B.maxhp,dead:B.dead,mode:B._hd1003.mode})'))
  ck('Remaining modules shed through native part breakup',p.evaluate("['wingL','wingR','gunL','gunR'].every(id=>hd1003Part(B,id).dead)"))
  ck('The protection gate rejects direct hits and Retina locks',p.evaluate("()=>{const hp=B.hp;hd1003Hit(B,999,0,0,'head');return B.hp===hp&&!retinaBossTargets(B).length&&hd1003At(B,B.x,B.y)===null}"))
  step(p,25);snap(p,'red-invulnerability-rumble')
  step(p,55);snap(p,'north-retreat');ck('Retreat really leaves the visible northern edge',p.evaluate('B.y<viewTopY()'),p.evaluate('B.y'))
  step(p,75);snap(p,'background-charge');ck('Background charge uses the smaller head animation bank',p.evaluate("hd54Own(B).phase==='charge'&&hd54Own(B).bank==='charge'"))
  p.evaluate('window.pulse0=hd54Own(B).pulse');step(p,60);p.evaluate('window.pulse1=hd54Own(B).pulse');step(p,120);p.evaluate('window.pulse2=hd54Own(B).pulse');step(p,60);p.evaluate('window.pulse3=hd54Own(B).pulse')
  ck('Charge glow accelerates toward its five-second climax',p.evaluate('pulse3-pulse2>pulse1-pulse0'),p.evaluate('({pulse0,pulse1,pulse2,pulse3})'))
  step(p,55);snap(p,'spin-barrage')
  ck('The charge lasts at least five seconds before the spinning attack',p.evaluate("()=>{const a=HD54.events.find(e=>e.event==='phase'&&e.phase==='charge'),b=HD54.events.find(e=>e.event==='phase'&&e.phase==='spin');return b.time-a.time>=4.98}"))
  ck('Spin uses generated 32-view depth frames',p.evaluate("hd54Own(B).bank==='spin'&&HD54_ART.spin.frames===32"))
  step(p,100);snap(p,'rollers-depth');ck('Both distant visual orbs and real foreground rounds exist',p.evaluate('HD54.events.some(e=>e.event===\'roller-foreground\')&&eBullets.some(q=>q._hd54&&!q.dead)'),p.evaluate('HD54.events.slice(-8)'))
  ck('Red rollers are sourced from Falva and have ten authored growth levels',p.evaluate('HD54_ART.orb_0.diameter===12&&HD54_ART.orb_9.diameter===66'))
  ck('Ordinary energy rollers cannot be shot down',p.evaluate('eBullets.filter(q=>q._hd54).every(q=>q._weaponProof&&!q._shootable&&!enemyOrdnanceCanIntercept(q))'))
  ck('Visible roller size and native collision grow together',p.evaluate('eBullets.filter(q=>q._hd54&&!q.dead).every(q=>Math.abs(q.w-HD54_ART[\'orb_\'+q._hd54Flight.level].diameter*.68)<.01)'))
  ck('Background boss remains protected while firing',p.evaluate("()=>{const hp=B.hp;hd1003Hit(B,50,0,0,'core');return B.hp===hp&&hd54Protected(B)}"))
  ck('Old full-sized hull smoke cannot obscure the protected distant skull',p.evaluate("()=>{const draw=ctx.drawImage;let n=0;ctx.drawImage=function(){n++;return draw.apply(this,arguments)};try{encounterDamageOverlay(B,true)}finally{ctx.drawImage=draw}return n===0}"))
  p.evaluate('window.contact=eBullets.find(q=>q._hd54&&!q.dead);window.calls=[];window.oldHit=playerHit;playerHit=function(...a){calls.push(a);return oldHit.apply(this,a)};contact.x=player.x=camLeftX()+viewW()/2;contact.y=player.y=VH-85;contact.vx=contact.vy=0;player.invuln=0;run.shield=0');step(p,1)
  ck('Foreground rollers use actual native player collision',p.evaluate('calls.length>0'),p.evaluate('calls'));p.evaluate('()=>{playerHit=oldHit;player.invuln=1e9}')
  step(p,480);snap(p,'fast-spin');ck('Spin cadence speeds up with the barrage',p.evaluate("()=>{const e=HD54.events.filter(e=>e.event==='roller-release');return e.length>20&&e[e.length-1].time-e[e.length-2].time<e[1].time-e[0].time}"))
  ck('Projectile count stays under the 64 round desperation budget',p.evaluate('HD54.flights.length+eBullets.filter(q=>q._hd54&&!q.dead).length<65'))
  step(p,300);snap(p,'foreground-return');ck('Boss returns to a vulnerable foreground window',p.evaluate("hd54Own(B)?.phase==='foreground'&&!hd54Protected(B)&&retinaBossTargets(B).length===2"),p.evaluate('({t:hd54Own(B)?.t,phase:hd54Own(B)?.phase})'))
  d=p.evaluate("""()=>{drawWorld(0);const a=ctx.getImageData(0,0,cv.width,cv.height).data,before=B.hp;hd1003Hit(B,5,0,0,'head');drawWorld(0);const d=ctx.getImageData(0,0,cv.width,cv.height).data;let white=0;for(let i=0;i<d.length;i+=4)if(d[i]>240&&d[i+1]>240&&d[i+2]>240&&a[i]+a[i+1]+a[i+2]<650)white++;return{white,before,hp:B.hp};}""")
  ck('Foreground takes native damage with real white hit pixels',d['white']>4 and d['hp']<d['before'],d);step(p,20)
  ck('White hit flash expires',p.evaluate("hd1003Part(B,'head').flash===0"))
  p.evaluate("hd1003Hit(B,99999,0,0,'head')");ck('The final foreground hit uses native defeat',p.evaluate("B.dead&&B._hd1003.mode==='dead'"))
  step(p,1);ck('Defeat clears the new foreground and distant projectiles',p.evaluate('!HD54.flights.length&&!eBullets.some(q=>q._hd54&&!q.dead)'))
  ck('No browser exceptions',not errors,errors);(W/'events.json').write_text(json.dumps(p.evaluate('HD54.events'),indent=2));br.close()
finally:stop()
print('RESULT',sum(c['passed']for c in checks),'/',len(checks));assert all(c['passed']for c in checks)
