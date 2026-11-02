"""Real Chromium/native collision and pixel checks. Pinned high-HP authored
targets are diagnostic fixtures, not a fight/balance/survival certification."""
from pathlib import Path
import json,sys,http.server
from playwright.sync_api import sync_playwright
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'_BUILD_SOURCE'))
from shoot import serve,STEP,TRAP_RAF
W=R/'_shots/weapon_contacts_1031';W.mkdir(exist_ok=True)
http.server.ThreadingHTTPServer.request_queue_size=256
checks=[];errors=[]
def ck(n,v,d=None):
 checks.append(dict(name=n,passed=bool(v),data=d));(W/'checks.json').write_text(json.dumps(checks,indent=2));print('PASS'if v else'FAIL',n,str(d)[:500]if not v else'',flush=True)
def step(p,n):
 for i in range(0,n,5):
  e=p.evaluate(STEP,min(5,n-i));assert not e,e;p.wait_for_timeout(1)
port,stop=serve(str(R))
try:
 with sync_playwright()as pw:
  br=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required']);p=br.new_page(viewport={'width':1280,'height':800})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text)if m.type=='error'or'draw error'in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>5&&typeof WC1031!=="undefined"',timeout=180000);p.mouse.click(3,3)
  p.wait_for_function('()=>Object.values(WC1031_ART).every(a=>XART.rdy(a.key))',timeout=180000)
  p.evaluate(TRAP_RAF)
  p.evaluate("()=>{debugStartFight(debugFightFor(1,'boss'),{pilot:'cole'});spawnBoss(debugFightFor(1,'boss').kind);debugFight.spawned=true;warnT=0;DBGT.god=true;player.invuln=1e9;BOFCinematicDirector.cancel();setState(GS.PLAY);}")
  p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(1)}',timeout=180000);step(p,250)
  p.evaluate("()=>{boss=null;bossActive=false;subBoss=null;subBossActive=false;debugFight=null;run.mode='boss';enemies.length=0;eBullets.length=0;pBullets.length=0;player.x=worldWidth()/2;player.y=VH-65;window.E=spawnEnemy('s1tankheavy',player.x,player.y-155,{});Object.assign(E,{hp:100000,maxhp:100000,pattern:'__dummy',shoots:false,fk:null,vx:0,vy:0,_noSep:true,t:0});window.home={x:E.x,y:E.y};window.wcBooms=[];window.wcExplode=explode;explode=function(){wcBooms.push([...arguments].slice(0,5));return wcExplode.apply(this,arguments);};}")
  step(p,3);p.evaluate('drawWorld(0)');p.screenshot(path=str(W/'fixture.png'))
  ck('All34 fixed even-cell contact banks preload',p.evaluate('Object.values(WC1031_ART).length===34&&Object.values(WC1031_ART).every(a=>a.cw===96&&a.ch===96&&a.pivot[0]===48&&a.pivot[1]===48)'))
  # Native collision path: launch real rounds directly into the actual target.
  kinds=[dict(kind='mg',lv=1),dict(kind='spread',lv=3),dict(kind='lzslug',lv=2),dict(kind='chain',lv=2),dict(kind='beam',lv=3,life=.2,_hit=[],bot=500,top=-20),dict(kind='spaceLaser',lv=2),dict(kind='lasermist',lv=2,life=2,_mistStage=2,_mistAge=.1),dict(kind='mavlaser',lv=1,colorLv=3,_hit=[],_speed=4),dict(kind='venomx',lv=2,_child=True,_charged=False,ph=0,roll=0,_hs=[])]
  for i,opt in enumerate(kinds):
   p.evaluate("o=>{E.x=home.x;E.y=home.y;E.hp=100000;E.flash=0;pImpacts.length=0;pBullets.length=0;wcBooms.length=0;WC1031.events=[];WC1031.gates=new WeakMap();const b=Object.assign({x:E.x,y:E.y+5,vx:0,vy:-.1,w:8,h:16,dmg:1,t:0,seat:1},o);if(b.kind==='mavlaser'){b._bx=b.x;b._by=b.y;b._ang=-Math.PI/2;b._phase=0;}pBullets.push(b);window.Q=b;}",opt)
   if opt['kind']=='beam':p.evaluate("()=>{Input.keys.j=true;run.weapon=3;run.wlevel=3;player.x=E.x;}")
   step(p,1)
   if opt['kind']=='beam':p.evaluate('Input.keys.j=false')
   r=p.evaluate('({hp:E.hp,flash:E.flash,fx:WC1031.events,booms:wcBooms,marks:pImpacts.filter(f=>f.mark).length,state,round:Q.kind,dead:Q.dead,beam:{x:Q.x,bot:Q.bot,life:Q.life},e:{x:E.x,y:E.y,w:E.w},player:{x:player.x,y:player.y}})')
   ck(opt['kind']+' native hit uses matched contact with no generic explosion',r['hp']<100000 and len(r['fx'])>0 and not r['booms'],r)
   if i in [0,2,3,5,6]:p.screenshot(path=str(W/(f'native-{i}-{opt["kind"]}.png')))
  # Every orb has its own existing elemental bank; native AoE/shard budgets stay active.
  orb=[]
  for el in ['ice','fire','lightning','kinetic','chrome','toxic','prism','water','dark','wind']:
   r=p.evaluate("el=>{E.x=home.x;E.y=home.y;E.hp=100000;E.flash=0;pImpacts.length=0;pBullets.length=0;wcBooms.length=0;WC1031.events=[];WC1031.gates=new WeakMap();const b={kind:'orb',x:E.x,y:E.y+5,vx:0,vy:-.1,w:26,h:26,dmg:2,lv:2,t:0,life:1,seat:1,_el:el,_hit:[],shardN:7};const old=_dmgBullet;_dmgBullet=b;hitEnemy(E,2);_dmgBullet=old;fb10Blast(b,E.x,E.y,'impact');return{el,hp:E.hp,bank:WC1031.events[0]?.bank,shards:pBullets.length,booms:wcBooms.length,nativeEnded:!!b._fb10Ended,fx:pImpacts.map(f=>f.bank)};}",el)
   orb.append(r)
   ck(el+' orb uses its elemental contact and preserves native detonation',r['hp']<100000 and r['bank']=='orb_'+el and r['nativeEnded'] and r['booms']==0,r)
  (W/'orbs.json').write_text(json.dumps(orb,indent=2))
  # Compare native damage with the visual system enabled/disabled.
  r=p.evaluate("()=>{const a=[];for(const enabled of [false,true]){WC1031.enabled=enabled;E.hp=100000;E.flash=0;E._esh=null;const old=_dmgBullet;_dmgBullet={kind:'mg',x:E.x,y:E.y,w:6,h:14,dmg:3,lv:1};hitEnemy(E,3);_dmgBullet=old;a.push(100000-E.hp);}WC1031.enabled=true;return a;}")
  ck('Visual contact does not change native damage',r[0]==r[1] and r[0]>0,r)
  # Native renderer pixels, flash, moving residue and expiry (no fake ctx).
  p.evaluate("()=>{pImpacts.length=0;pBullets.length=0;fb10Clouds=[];E=spawnEnemy('s1tankheavy',home.x,home.y,{});Object.assign(E,{hp:100000,maxhp:100000,pattern:'__dummy',shoots:false,fk:null,vx:0,vy:0,_noSep:true,t:0});E._esh=null;E.flash=0;WC1031.gates=new WeakMap();window.pixelRead=()=>{ctx.save();ctx.clearRect(0,0,cv.width,cv.height);drawEnemy(E);ctx.restore();return Array.from(ctx.getImageData(Math.floor(E.x-35),Math.floor(E.y-35),70,70).data)};pixelRead();}")
  p.wait_for_timeout(150)
  p.evaluate("()=>{window.cleanPixels=pixelRead();const old=_dmgBullet;_dmgBullet={kind:'mg',x:E.x,y:E.y+4,lv:1};hitEnemy(E,1);_dmgBullet=old;window.hitPixels=pixelRead();}")
  ck('Actual authored hull pixels visibly flash on contact',p.evaluate('cleanPixels.some((v,i)=>v!==hitPixels[i])&&E.flash>0'))
  r=p.evaluate("()=>{const f=pImpacts.find(f=>f.mark);if(!f)return null;weaponFeedbackDraw(f);const old=[f.x,f.y];E.x+=31;E.y+=19;weaponFeedbackDraw(f);return{dx:f.x-old[0],dy:f.y-old[1],bank:f.bank};}")
  ck('Scorch decal follows the actual struck hull',r and r['dx']==31 and r['dy']==19,r)
  p.evaluate('E.x=home.x;E.y=home.y;E.flash=0;window.expiredPixels=pixelRead()')
  colors=p.evaluate("()=>{const whites=a=>a.reduce((n,v,i)=>n+(i%4===0&&a[i+3]>160&&v>235&&a[i+1]>235&&a[i+2]>235?1:0),0);return{clean:whites(cleanPixels),hit:whites(hitPixels),expired:whites(expiredPixels),flash:E.flash};}")
  ck('Native white damaged pixels expire back to the animated authored palette',colors['hit']>colors['clean']+20 and colors['expired']<colors['hit']*.4 and colors['flash']==0,colors)
  p.evaluate("()=>{E.x=home.x;E.y=home.y;pBullets.length=0;run.mode='campaign';setState(GS.PLAY)}");step(p,70)
  ck('Attached contact and scorch reels expire on the simulation clock',p.evaluate('!pImpacts.some(f=>f._weaponContact&&f.target===E)'),p.evaluate('({state,fx:pImpacts.filter(f=>f._weaponContact).map(f=>({t:f.t,dur:f.dur})),clock:efxClock})'))
  # Protected/reflected hits do not leave an artificial hull damage mark.
  r=p.evaluate("()=>{pImpacts.length=0;E.hp=100000;E.flash=0;E._noHit=true;const old=_dmgBullet;_dmgBullet={kind:'mg',x:E.x,y:E.y,lv:1};hitEnemy(E,3);_dmgBullet=old;E._noHit=false;return{hp:E.hp,n:pImpacts.length};}")
  ck('Untargetable units receive no false residue',r['hp']==100000 and r['n']==0,r)
  r=p.evaluate("()=>{pImpacts.length=0;E.hp=100000;E.flash=0;const s=enemyShieldEquip(E,'bubble_volt',100);s.phase='active';WC1031.gates=new WeakMap();const old=_dmgBullet;_dmgBullet={kind:'mg',x:E.x,y:E.y+4,vx:0,vy:-8,w:6,h:14,lv:1};hitEnemy(E,3);_dmgBullet=old;const r={hp:E.hp,energy:s.energy,marks:pImpacts.filter(f=>f.mark).length};E._esh=null;return r;}")
  ck('Native energy shields absorb damage without a hull scorch',r['hp']==100000 and r['energy']<100 and r['marks']==0,r)
  r=p.evaluate("()=>{pImpacts.length=0;E.hp=100000;E.flash=0;WC1031.gates=new WeakMap();for(let i=0;i<500;i++){efxClock+=.05;playerWeaponImpact({kind:'beam',x:E.x,y:E.y,lv:3},E,E.x,E.y);}return{all:pImpacts.length,marks:pImpacts.filter(f=>f.mark&&f.t<f.dur).length};}")
  ck('Continuous fire has bounded effects and at most3 live marks per hull',r['all']<=180 and r['marks']<=3,r)
  r=p.evaluate("()=>{pImpacts.length=0;wcBooms.length=0;E.hp=1;E.flash=0;WC1031.gates=new WeakMap();const old=_dmgBullet;_dmgBullet={kind:'mg',x:E.x,y:E.y,lv:1};hitEnemy(E,10);_dmgBullet=old;return{dead:E.dead,dying:E._dyingT,booms:wcBooms.length,marks:pImpacts.filter(f=>f.mark).length};}")
  ck('Lethal hits preserve native destruction explosions and leave no floating decal',bool(r.get('dead')or r.get('dying')is not None) and r['booms']>0 and r['marks']==0,r)
  p.evaluate("()=>{pBullets.length=0;enemies.length=0;eBullets.length=0;pImpacts.length=0;spawnSubBoss(debugFightFor(1,'mini').kind);subBossActive=true;setState(GS.PLAY);}");step(p,280)
  r=p.evaluate("()=>{const o=subBoss,L=livePieces(o).filter(t=>!t.dead&&t.hp>0);for(const t of L){pImpacts.length=0;WC1031.gates=new WeakMap();const hp=t.hp,ohp=o.hp,b={kind:'spaceLaser',x:t.x,y:t.y,dmg:1,lv:2};spaceDamageTarget(t,1,b);if(t.hp<hp||o.hp<ohp){const f=pImpacts.find(f=>f.mark);if(f){weaponFeedbackDraw(f);const x=f.x,y=f.y;o.x+=24;o.y+=16;weaponFeedbackDraw(f);return{hp:true,contacts:pImpacts.filter(f=>f._weaponContact&&!f.mark).length,dx:f.x-x,dy:f.y-y,target:f.target._retinaId,exact:f.target===t};}}}return{hp:false,targets:L.map(t=>({id:t._retinaId,hp:t.hp})),enter:o.enter};}")
  ck('Exact live miniboss component receives one contact through nested routers',r['hp'] and r.get('contacts')==1 and r.get('exact'),r)
  ck('Component residue follows its live native socket as the boss moves',r.get('dx')==24 and r.get('dy')==16,r)
  p.evaluate('drawWorld(0)');p.screenshot(path=str(W/'native-component.png'))
  ck('No browser/console/rendering errors',not errors,errors)
  (W/'errors.json').write_text(json.dumps(errors,indent=2));br.close()
finally:stop()
print('RESULT',sum(c['passed']for c in checks),'/',len(checks));assert all(c['passed']for c in checks)
