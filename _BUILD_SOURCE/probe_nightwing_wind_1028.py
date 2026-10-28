from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
import sys,json,numpy as np
R=Path(__file__).resolve().parents[1];W=R/'_shots/nightwing_wind_1028';W.mkdir(exist_ok=True,parents=True);sys.path.insert(0,str(R/'_BUILD_SOURCE'));from shoot import serve,TRAP_RAF,STEP
checks=[];errors=[];http=[]
def check(n,v,d=None):
 checks.append(dict(name=n,passed=bool(v),data=d));(W/'checks.json').write_text(json.dumps({'checks':checks,'errors':errors,'http':http},indent=2));assert v,n
M=json.loads((R/'assets/game/levels/stage_06/boss/nightwing_wind_1028/manifest.json').read_text())
check('All aircraft, weapons and wind banks use even cells and bounded texture dimensions',all(b['cw']%2==0 and b['ch']%2==0 and max(Image.open(R/b['path']).size)<=4096 for b in M['banks'].values()))
port,stop=serve(str(R))
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1280,'height':800});p.on('requestfailed',lambda q:errors.append('REQUEST '+q.url+' '+str(q.failure))if q.failure!='net::ERR_ABORTED'else None);p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'or'draw error'in m.text else None);p.on('response',lambda r:http.append(r.url)if r.status>=400 else None)
  p.goto(f'http://127.0.0.1:{port}',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5&&typeof NW30!=="undefined"');p.mouse.click(3,3);p.evaluate('()=>{run.stage=6;stageLoadBegin(6)}');p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(6)}',polling=100,timeout=180000);p.evaluate(TRAP_RAF)
  def step(n):
   err=p.evaluate(STEP,n)
   if err:raise RuntimeError(err)
  p.evaluate("()=>{diffKey='furious';debugUnlocked=true;debugStartFight({stage:6,role:'boss',kind:'warhive'},{pilot:'cole',record:false});DBGT.god=true;spawnBoss('warhive');debugFight.spawned=true;warnT=0;BOFCinematicDirector.cancel();setState(GS.PLAY);bossActive=true;s6Wing.ships=[];delete boss._carrier17;boss._whv.mode='ace';whvAceSpawn(boss);NW30.events=[];}")
  step(430)
  check('Whole-aircraft palette aliases are ready across native and depth poses',p.evaluate('Object.entries(NW30_ART.aliases).every(([k,v])=>XART.rdy(k)&&XART.get(k)===NW30.base.get(NW30_ART.banks[v].key))'))
  check('Nightwing still has one native health pool and one Retina target',p.evaluate('!boss.modular&&boss.hp>0&&retinaBossTargets(boss).length===1'))
  p.evaluate('()=>{const S=nw30State(boss),A=boss._whv.ace;nw30Cancel(boss);S.gunCd=0;S.windCd=99;A.dash=A.desp=A.roll=A.somer=null;A.gunCd=A.dashCd=A.somerCd=A.rollCd=99;}');step(2)
  q=p.evaluate('()=>({action:boss._nw30.action,locks:playerLocks.filter(q=>q.src===boss).length})');check('Dual machine guns arm a real player Retina warning before release',q['action']['phase']=='warn'and q['locks']>0,q)
  p.screenshot(path=str(W/'retina-warning.png'));step(70);p.screenshot(path=str(W/'dual-guns.png'))
  q=p.evaluate('()=>({shots:NW30.events.filter(e=>e.event==="turret-shot"),bullets:eBullets.filter(q=>q._nw30Owner===boss).map(q=>({wind:q._nw30Wind,shootable:enemyOrdnanceCanIntercept(q)})),recoil:boss._nw30.recoil})');check('Both physical turret sockets release paired machine-gun bullets',len(q['shots'])>=2 and {s['side']for s in q['shots']}=={0,1},q['shots'][:4]);check('Machine-gun bullets cannot be shot down',q['bullets']and all(not b['shootable']for b in q['bullets']))
  q=p.evaluate('''()=>{const S=boss._nw30,A=boss._whv.ace;let calls=[];const draw=ctx.drawImage;ctx.drawImage=function(im,...args){if(im===XART.get(NW30_ART.banks.gun_left.key)||im===XART.get(NW30_ART.banks.gun_right.key))calls.push(args);return draw.call(this,im,...args)};try{nw28DrawBody(boss)}finally{ctx.drawImage=draw}return{calls:calls.length,modules:NW30.last.modular,engines:NW30.last.engines}}''');check('Native renderer draws exactly two separate recoil guns and two anchored exhausts',q['calls']==2 and q['modules']and len(q['engines'])==2,q)
  frames=set()
  for i in range(12):step(1);frames.add(p.evaluate('nw30Gun(boss,0).frame%4'))
  check('Gun kickback uses multiple authored recoil frames',len(frames)>=2,list(frames))
  step(160);p.evaluate('()=>{nw30Cancel(boss);const S=boss._nw30;S.windCd=0;S.gunCd=99;boss._whv.ace.dashCd=99;}');step(3);check('Wind charge starts as its own exclusive attack',p.evaluate('boss._nw30.action.kind==="wind"&&boss._nw30.action.phase==="charge"&&!boss._whv.ace._ra7Gate&&!boss._whv.ace._pw5Gun'))
  step(72);p.screenshot(path=str(W/'wind-charge.png'));check('Wind charge darkens scenery without protecting the boss',p.evaluate('NW30.dim>=8&&!whvAceInvuln(boss._whv.ace)'))
  q=p.evaluate('()=>{const hp=boss.hp;boss._gp4FlashNext=0;hitBoss(1);return{damage:hp-boss.hp,flash:boss.flash}}');check('Current complete pose retains accepted damage and hit flash while charging',q['damage']>0 and q['flash']>0,q)
  step(90);p.screenshot(path=str(W/'wind-volley.png'));q=p.evaluate('()=>({wind:eBullets.filter(q=>q._nw30Wind).map(q=>({shootable:enemyOrdnanceCanIntercept(q),element:enemyOrdnanceElement(q)})),shots:NW30.events.filter(e=>e.event==="turret-shot"&&e.kind==="wind")})');check('Animated wind rounds leave both guns and carry Wind damage',len(q['wind'])>=6 and all(x['element']=='wind'and not x['shootable']for x in q['wind'])and {x['side']for x in q['shots']}=={0,1})
  q=p.evaluate('''()=>{const q=eBullets.find(q=>q._nw30Wind),old=ctx.drawImage;let count=0;ctx.drawImage=function(im,...a){if(im===XART.get(NW30_ART.banks.wind_bullet.key))count++;return old.call(this,im,...a)};try{drawCombatFinalProjectile(q)}finally{ctx.drawImage=old}return count;}''');check('Live projectile renderer selects the generated animated wind bank',q==1)
  step(140);check('Wind volley has finite recovery and clears scenery dimming',p.evaluate('!boss._nw30.action&&NW30.dim===0'))
  p.evaluate('()=>{nw30Cancel(boss);const A=boss._whv.ace;boss._nw30.gunCd=boss._nw30.windCd=99;A.roll=A.somer=A.desp=null;A.dash={st:"warn",t:0,x0:A.x,y0:A.y};}');modes=set()
  for i in range(420):
   step(1)
   modes.add(p.evaluate('NW30.last?.throttle'))
   if i in[130,210,250]:p.screenshot(path=str(W/f'dash-{i}.png'))
  check('Cruise, boosted dash, large flyover and small approach use distinct exhaust banks',{'cruise','boost','small'}.issubset(modes)and any(str(x).startswith('large_')for x in modes),list(modes))
  check('Dashes leave bounded authored wind rings',p.evaluate('NW30.events.some(e=>e.event==="dash-wind-ring")&&boss._nw30.rings.length<=6'))
  q=p.evaluate('''()=>{const b=boss,A=b._whv.ace;nw30Cancel(b);A.dash=A.roll=A.somer=A.desp=A._nf29Pose=null;A.inverted=false;A.vx=0;A.x=camLeftX()+viewW()/2;A.y=viewTopY()+viewH()/2;b._gp4FlashNext=0;const hp=b.hp;hitBoss(1);const draw=ctx.drawImage,keys=['clean_hit','gun_left_hit','gun_right_hit'].map(k=>XART.get(NW30_ART.banks[k].key));let draws=0;ctx.clearRect(0,0,cv.width,cv.height);ctx.drawImage=function(im,...args){if(keys.includes(im)){draws++;return draw.call(this,im,...args)}};try{nw28DrawBody(b)}finally{ctx.drawImage=draw}const d=ctx.getImageData(0,0,cv.width,cv.height).data;let lit=0,neutral=0;for(let i=0;i<d.length;i+=4)if(Math.max(d[i],d[i+1],d[i+2])>25){lit++;if(Math.max(d[i],d[i+1],d[i+2])-Math.min(d[i],d[i+1],d[i+2])<2)neutral++;}return{draws,lit,neutral,damaged:b.hp<hp};}''');check('Accepted hits visibly white the whole body and both recoil modules',q['draws']==3 and q['lit']>9000 and q['neutral']>q['lit']*.99 and q['damaged'],q)
  step(20);check('The native white hit flash expires while the wind jet keeps moving',p.evaluate('boss.flash<=0'))
  p.evaluate('run.stage=7');check('Other stages keep the original aircraft sources',p.evaluate('!nw30Palette()'));check('No game, draw or asset HTTP errors',not errors and not http,{'errors':errors,'http':http});br.close()
finally:stop()
print(f'{len(checks)} native/art checks passed')
