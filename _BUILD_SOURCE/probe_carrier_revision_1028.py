from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import sys,json,numpy as np
R=Path(__file__).resolve().parents[1];W=R/'_shots/carrier_revision_1028';W.mkdir(parents=True,exist_ok=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import serve,TRAP_RAF,STEP
checks=[];errors=[];http=[]
def check(n,v,d=None):
 checks.append(dict(name=n,passed=bool(v),data=d));(W/'checks.json').write_text(json.dumps(dict(checks=checks,errors=errors,http=http),indent=2));assert v,n
M=json.loads((R/'assets/game/levels/stage_06/boss/carrier_revision_1028/manifest.json').read_text())
pairs=[(np.array(Image.open(R/b['path']).convert('RGBA')),np.array(Image.open(R/next(p for p in M['sources']if Path(p).stem==k.replace('laser_','ice_laser_')or Path(p).stem==k.replace('muzzle_',''))).convert('RGBA')))for k,b in M['banks'].items()if k!='fan_smoke'];check('Palette variants preserve exact alpha and source dimensions',all(a.shape==b.shape and np.array_equal(a[:,:,3],b[:,:,3])for a,b in pairs))
port,stop=serve(str(R))
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1280,'height':800});p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'or'draw error'in m.text else None);p.on('response',lambda r:http.append(r.url)if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5&&typeof CR31!=="undefined"');p.mouse.click(3,3);p.evaluate('()=>{run.stage=6;stageLoadBegin(6)}');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(6)}',polling=100,timeout=180000);p.evaluate(TRAP_RAF)
  def step(n):
   err=p.evaluate(STEP,n)
   if err:raise RuntimeError(err)
  p.evaluate("()=>{diffKey='furious';debugUnlocked=true;debugStartFight({stage:6,role:'boss',kind:'warhive'},{pilot:'cole',record:false});DBGT.god=true;spawnBoss('warhive');debugFight.spawned=true;warnT=0;BOFCinematicDirector.cancel();setState(GS.PLAY);bossActive=true;s6Wing.ships=[];}");step(220)
  q=p.evaluate('''()=>{const b=boss,C=b._carrier17;let targets=0,shots=0;const aim=targetShip,shoot=eShootT;targetShip=function(){targets++;return aim.apply(this,arguments)};eShootT=function(){shots++;return shoot.apply(this,arguments)};try{for(const fan of C.parts.filter(p=>p.kind==='fan'))for(const phase of ['rest','tell','fire']){Object.assign(fan,{phase,t:.4,cool:-1,aim:{x:player.x,y:player.y},angle:1,lanes:[1]});for(let i=0;i<300;i++)roster17Weapon(b,fan,1/60)}}finally{targetShip=aim;eShootT=shoot}return{targets,shots,fans:C.parts.filter(p=>p.kind==='fan').map(p=>({phase:p.phase,aim:p.aim,angle:p.angle,hp:p.hp}))};}''')
  check('Both fans never acquire a target, warning or shot in any former attack phase',q['targets']==q['shots']==0 and all(f['phase']=='rest'and f.get('aim')is None and f.get('angle')is None for f in q['fans']),q)
  check('All ten native modules and both fan HP pools remain intact',p.evaluate('boss._carrier17.parts.length===10&&boss._carrier17.parts.filter(p=>p.kind==="fan").every(p=>p.hp>0)&&boss.hp===boss.maxhp'))
  q=p.evaluate('retinaBossTargets(boss).map(t=>({id:t._retinaId,name:t.name,hp:t.hp}))');check('Players can still Retina-target both fan objectives',len(q)==10 and sum('harrier L'in str(t)or'harrier R'in str(t)for t in q)==2,q)
  q=p.evaluate('''()=>{const b=boss,C=b._carrier17,hp=b.hp;C.direct='armor';hitBoss(40);return{hp,after:b.hp,fanCenters:C.parts.filter(p=>p.kind==='fan').map(p=>roster17At(b,...Object.values(roster17Mount(b,p))))};}''');check('Protected body ignores damage while fan sockets remain hittable',q['after']==q['hp']and set(q['fanCenters'])=={'L','R'},q)
  # Fixture-only force a native laser fire sample; no phase writes in film.
  p.evaluate('''()=>{const b=boss,C=b._carrier17;for(const p of C.parts){p.phase=p.kind==='laser'?'fire':'rest';p.t=.3;p.cool=99;if(p.kind==='laser'){p.angle=p.er28Bearing=Math.PI/2+(p.id==='laser0'?.35:-.35);p.muzzleAge=99;}}}''')
  q=p.evaluate('''()=>{const get=XART.get;let keys=[];XART.get=function(k){const name=CR31.drawing&&CR31_ART.aliases[k];if(name)keys.push(name);return get.apply(this,arguments)};try{roster17Draw(boss)}finally{XART.get=get}return{keys,scope:CR31.drawing};}''');check('Actual carrier renderer resolves red beam and focused muzzle sheets',any(k.startswith('laser_')for k in q['keys'])and any(k.startswith('muzzle_')for k in q['keys'])and q['scope']==0,q)
  p.evaluate('()=>{drawScene(0);}');p.screenshot(path=str(W/'red-lasers.png'))
  check('Blue lasers outside the carrier draw retain their original sources',p.evaluate('XART.get("ap10_ice_laser_06")===CR31.base.get("ap10_ice_laser_06")&&XART.get("lm27_large")===CR31.base.get("lm27_large")'))
  for name,x,scale in [('left',-42,1),('moved',42,.72)]:
   if name=='left':
    p.evaluate('()=>{const C=boss._carrier17;for(const p of C.parts){p.phase="rest";p.cool=99;}C.direct="L";hitBoss(10000);}');step(16)
   p.evaluate('(v)=>{const C=boss._carrier17;boss.x+=v.x;boss.y+=12;C.scale=v.scale;roster17Sync(boss);}',dict(x=x,scale=scale))
   q=p.evaluate('''()=>{let calls=[],key='';const get=XART.get,draw=ctx.drawImage;XART.get=function(k){key=k;return get.apply(this,arguments)};ctx.drawImage=function(im,...a){if(key===CR31_ART.banks.fan_smoke.key){const t=this.getTransform();calls.push({args:a,transform:[t.a,t.b,t.c,t.d,t.e,t.f]})}return draw.call(this,im,...a)};try{s6r18CarrierOverlay(boss,boss._carrier17)}finally{XART.get=get;ctx.drawImage=draw}const C=boss._carrier17,W=boss._whv,p=C.parts.find(p=>p.id==='L'),k=C.scale*roster17HullScale(boss);return{calls,smoke:CR31.smoke,expected:{x:W.cx+p.dx*WHV_S*k,y:W.cy+(W.dy||0)+p.dy*WHV_S*k},fanDead:p.dead};}''')
   a=q['calls'][0];ar=a['args'];t=a['transform'];anchorX=t[0]*(ar[4]+64)+t[4];anchorY=t[3]*(ar[5]+144)+t[5]
   check(f'Destroyed left fan smoke stays anchored during {name} carrier position/depth',q['fanDead']and len(q['calls'])==1 and abs(anchorX-q['expected']['x'])<2 and abs(anchorY-q['expected']['y'])<2,q)
   p.evaluate('()=>{drawScene(0);}');p.screenshot(path=str(W/f'fan-smoke-{name}.png'))
  p.evaluate('()=>{const C=boss._carrier17;C.scale=1;C.direct="R";hitBoss(10000);}');step(30)
  q=p.evaluate('()=>{s6r18CarrierOverlay(boss,boss._carrier17);return CR31.smoke}');check('Both destroyed fans render separate looping smoke columns',len(q)==2 and q[0]['x']!=q[1]['x'],q)
  p.evaluate('()=>drawScene(0)');p.screenshot(path=str(W/'both-fans-smoke.png'))
  q=p.evaluate('''()=>{const C=boss._carrier17,p=C.parts.find(p=>!p.dead);C.direct=p.id;const hp=p.hp;hitBoss(1);return{damage:hp-p.hp,flash:p.flash,id:p.id};}''');check('Live weapon modules retain native damage and white hit timers',q['damage']>0 and q['flash']>0,q);step(20)
  p.evaluate('()=>{const b=boss;for(const p of [...b._carrier17.parts])if(!p.dead){b._carrier17.direct=p.id;hitBoss(10000);}if(b._carrier17&&b._hc32?.exposed){b._carrier17.direct="hull";hitBoss(b._hc32.core+1);}}');step(45)
  check('Fan smoke remains attached to native falling carrier',p.evaluate('!!boss._s6CarrierFall&&boss._whv.mode!=="ace"&&CR31.smoke.length===2'))
  step(520);check('Original full-module defeat still reaches native Nightwing entrance/combat',p.evaluate('boss._whv.mode==="ace"&&!!boss._whv.ace&&!boss.dead&&boss.hp>0'))
  p.evaluate('run.stage=7');check('Fan change is isolated from other encounters',p.evaluate('!cr31Own(boss)'));check('No game, draw or HTTP asset errors',not errors and not http,dict(errors=errors,http=http));br.close()
finally:stop()
print(f'{len(checks)} native/art checks passed')
