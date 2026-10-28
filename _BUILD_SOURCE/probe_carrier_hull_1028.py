from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import sys,json,http.server,numpy as np
http.server.ThreadingHTTPServer.request_queue_size=256
R=Path(__file__).resolve().parents[1];W=R/'_shots/carrier_hull_1028';W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import serve,TRAP_RAF,STEP
checks=[];errors=[];http=[]
def check(n,v,d=None):
 checks.append(dict(name=n,passed=bool(v),data=d));(W/'checks.json').write_text(json.dumps(dict(checks=checks,errors=errors,http=http),indent=2));assert v,n
M=json.loads((R/'assets/game/levels/stage_06/boss/carrier_hull_1028/manifest.json').read_text())
check('All new cells are even and textures fit 4096px',all(a['cw']%2==a['ch']%2==0 and max(Image.open(R/a['path']).size)<=4096 for a in M['banks'].values()))
port,stop=serve(str(R))
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'or'draw error'in m.text else None);p.on('response',lambda r:http.append(r.url)if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5&&typeof HC32!=="undefined"');p.mouse.click(3,3);p.evaluate('()=>{run.stage=6;stageLoadBegin(6)}');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(6)&&hc32Warm()}',polling=100,timeout=180000);p.evaluate(TRAP_RAF)
  def step(n):
   err=p.evaluate(STEP,n)
   if err:raise RuntimeError(err)
  def setup(d='furious'):
   p.evaluate("d=>{run.ngplus=false;diffKey=d;debugUnlocked=true;debugStartFight({stage:6,role:'boss',kind:'warhive'},{pilot:'cole',record:false});DBGT.god=true;spawnBoss('warhive');debugFight.spawned=true;warnT=0;BOFCinematicDirector.cancel();setState(GS.PLAY);bossActive=true;s6Wing.ships=[];}",d);step(220);p.evaluate('()=>{enemies=[];powerups=[];subBoss=null;subBossActive=false;pBullets=[];eBullets=[];}')
  for diff in ['easy','normal','hard','furious']:
   setup(diff)
   if diff=='furious':p.screenshot(path=str(W/'mounted-lasers.png'))
   q=p.evaluate('''()=>{const b=boss,C=b._carrier17,S=b._hc32;return{hp:b.hp,max:b.maxhp,sum:C.parts.reduce((n,p)=>n+p.hp,0),core:S.core,coreMax:S.coreMax,targets:retinaBossTargets(b).map(t=>t._retinaId),point:roster17At(b,b.x,b.y),mounts:C.parts.filter(p=>p.kind==='laser').map(p=>({dx:p.dx,dy:p.dy,hit:roster17At(b,...Object.values(roster17Mount(b,p)))}))}}''')
   check(diff+' hull absent from targets/collision while ten modules live',len(q['targets'])==10 and 'harrier hull'not in q['targets']and q['point']is None,q)
   check(diff+' HP budget includes the protected hull reserve exactly once',q['hp']==q['max']==q['sum']+q['core']and q['core']==q['coreMax'],q)
   check(diff+' both laser bases mount on the user-selected metal wing panels and share hit sockets',q['mounts']==[dict(dx=-104,dy=20,hit='laser0'),dict(dx=104,dy=20,hit='laser3')],q['mounts'])
   q=p.evaluate('''()=>{const b=boss,C=b._carrier17,S=b._hc32,core=S.core,hp=b.hp;C.direct='hull';hitBoss(999);C.hit='armor';hitBoss(999);return{core:S.core,hp:b.hp,initialCore:core,initialHP:hp};}''');check(diff+' direct and stale hull hits cannot bypass module gate',q['core']==q['initialCore']and q['hp']==q['initialHP'],q)
   q=p.evaluate('''()=>{const b=boss,C=b._carrier17,S=b._hc32,result=[],last=C.parts.find(p=>p.id==='laser3');for(const p of C.parts.filter(p=>p!==last)){C.direct=p.id;hitBoss(p.hp+1);C.direct='hull';hitBoss(999);result.push({dead:p.dead,core:S.core,exposed:S.exposed,hull:roster17At(b,b.x,b.y),target:retinaBossTargets(b).some(t=>t._retinaId==='harrier hull')})}const before=S.core;C.direct=last.id;hitBoss(last.hp+1);return{result,before,core:S.core,exposed:S.exposed,fall:!!b._s6CarrierFall,live:C.parts.filter(p=>!p.dead).length,targets:retinaBossTargets(b).map(t=>t._retinaId),hp:b.hp};}''')
   check(diff+' hull remains protected at every partial destruction step',all(x['dead']and x['core']==q['before']and not x['exposed']and x['hull']is None and not x['target']for x in q['result']))
   check(diff+' final laser break exposes one intact hull pool before any fall',q['core']==q['before']==q['hp']and q['exposed']and not q['fall']and q['live']==0 and q['targets']==['harrier hull'],q)
  # The final Furious fixture is now in its exposed-hull phase.
  for n,label in [(12,'full-flash'),(62,'pulse-loop'),(95,'red-flash')]:
   step(n);p.screenshot(path=str(W/(label+'.png')));q=p.evaluate('()=>{roster17Draw(boss);return HC32.last}');check('Native hull selects authored '+label+' frames',q['exposed']and q['frame']<16,q)
  q=p.evaluate('''()=>{let smoke=0;const get=XART.get,draw=ctx.drawImage;let key='';XART.get=function(k){key=k;return get.apply(this,arguments)};ctx.drawImage=function(im,...a){if(key===HC32_ART.banks.smoke.key)smoke++;return draw.call(this,im,...a)};try{s6r18CarrierOverlay(boss,boss._carrier17)}finally{XART.get=get;ctx.drawImage=draw}return{smoke,fans:CR31.smoke.length,events:HC32.events.filter(e=>e.event==='hull-cookoff').map(e=>e.edge),shoot:HC32.events.filter(e=>e.event==='hull-exposed').length}}''');check('Eight bounded smoke columns cover the hull while both fans burn/smoke',q['smoke']==8 and q['fans']==2,q);check('Cookoff starts north, east, west, south before spreading',q['events'][:4]==[0,1,2,3],q['events'])
  q=p.evaluate('''()=>{const b=boss,S=b._hc32,C=b._carrier17,p=C.parts[0],hp=S.core;C.direct=p.id;hitBoss(10);return{hp,after:S.core}}''');check('A stale destroyed module target cannot damage the exposed hull',q['hp']==q['after'],q)
  q=p.evaluate('''()=>{const b=boss,S=b._hc32,prior=S.core,q={kind:'mg',x:b.x,y:b.y+b.h/2+32,vx:0,vy:-6.5,w:4,h:12,dmg:7,lv:1,t:0,seat:1};pBullets=[q];let ticks=0;while(!q.dead&&q.y>0&&ticks++<100)updatePlay(1/60);return{before:prior,after:S.core,dead:q.dead,flash:S.flash,ticks}}''');check('A real native machine-gun bullet damages the newly exposed hull',q['after']<q['before']and q['dead']and q['flash']>0,q)
  q=p.evaluate('''()=>{const b=boss,S=b._hc32;ctx.clearRect(0,0,cv.width,cv.height);const white=hc32Cell('closed',16),draw=ctx.drawImage;let drawn=0;ctx.drawImage=function(im,...a){if(im===white){drawn++;return draw.call(this,im,...a)}};try{roster17Draw(b)}finally{ctx.drawImage=draw}const d=ctx.getImageData(0,0,cv.width,cv.height).data;let lit=0,whitePixels=0;for(let i=0;i<d.length;i+=4){if(Math.max(d[i],d[i+1],d[i+2])>25){lit++;if(d[i]>245&&d[i+1]>245&&d[i+2]>245)whitePixels++;}}return{drawn,lit,whitePixels,frame:HC32.last.frame}}''');check('Accepted hull hit visibly flashes the entire actual hull white',q['drawn']==1 and q['lit']>20000 and q['whitePixels']>.99*q['lit']and q['frame']==16,q);p.evaluate('()=>{s6r18CarrierOverlay(boss,boss._carrier17)}');check('Hatch overlay uses the same whole-hull white hit frame',p.evaluate('HC32.last.frame===16'));step(20);check('Native hull hit flash expires and returns to red cookoff animation',p.evaluate('boss._hc32.flash===0&&HC32.last.frame<16'))
  q=p.evaluate('''()=>{const b=boss,S=b._hc32,C=b._carrier17,hp=S.core;_dmgBullet={kind:'beam',x:b.x,w:8,top:0,bot:VH};_lastHitX=_lastHitY=null;warhiveDamage(b,3);_dmgBullet=null;return{before:hp,after:S.core}}''');check('Held beam reaches exposed hull through its actual opaque column',q['after']==q['before']-3,q)
  p.evaluate('()=>{boss._carrier17.direct="hull";hitBoss(boss._hc32.core+1);}');check('Hull exhaustion starts the original opaque carrier fall exactly once',p.evaluate('!!boss._s6CarrierFall&&boss._hc32.final&&!boss.dead&&HC32.events.filter(e=>e.event==="hull-destroyed").length===1'));step(80);p.screenshot(path=str(W/'burning-fall.png'));check('Red glow, hull smoke and fan fires persist during native fall',p.evaluate('boss._s6CarrierFall&&HC32.last.exposed&&HC32.last.frame<16&&CR31.smoke.length===2'))
  step(520);check('Native Nightwing entrance/combat still receives its original life',p.evaluate('boss._whv.mode==="ace"&&boss._whv.ace._nw28.mode==="fight"&&boss.hp>0&&!boss.dead'))
  setup();q=p.evaluate('''()=>{const b=boss,S=b._hc32,q={kind:'mg',x:b.x,y:b.y+b.h/2+32,vx:0,vy:-6.5,w:4,h:12,dmg:7,lv:1,t:0,seat:1},hp=S.core;pBullets=[q];let n=0;while(!q.dead&&q.y>0&&n++<110){enemies=[];powerups=[];updatePlay(1/60);}return{core:hp,after:S.core,dead:q.dead,y:q.y,point:roster17At(b,q.x,q.y),test:bossHitTest(q.x,q.y)}}''');check('A real centerline bullet passes untouched through the protected hull',q['core']==q['after']and not q['dead']and q['y']<=0,q)
  check('Fans remain passive after mounted-turret and hull changes',p.evaluate('boss._carrier17.parts.filter(p=>p.kind==="fan").every(p=>p.phase==="rest"&&!p.aim)'))
  p.evaluate('()=>{for(const p of [...boss._carrier17.parts]){boss._carrier17.direct=p.id;hitBoss(p.hp+1);}}')
  frames=[]
  for i in range(48):
   p.evaluate('()=>{boss._carrier17.direct="hull";hitBoss(.01)}');step(1);frames.append(p.evaluate('HC32.last.frame'))
  check('Sustained hits retain native white flashes AND visible red palette intervals',16 in frames and sum(f!=16 for f in frames)>=16,dict(white=frames.count(16),red=sum(f!=16 for f in frames)))
  p.evaluate('run.stage=7');check('Other stages do not enter the new hull owner',p.evaluate('!hc32Own(boss)'));check('No game, draw or HTTP asset errors',not errors and not http,dict(errors=errors,http=http));br.close()
finally:stop()
print(f'{len(checks)} native/art checks passed')
