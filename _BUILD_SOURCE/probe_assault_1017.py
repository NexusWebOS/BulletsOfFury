"""Native Chromium regression: sovereign tells/guards, Hammer counter, roster,
live radio, compact wind art, highway modules and central Stage7 pressure.
"""
from pathlib import Path
import ast,json,sys,traceback,http.server,argparse,hashlib
from urllib.parse import urlparse
from playwright.sync_api import sync_playwright
import shoot
R=Path(__file__).resolve().parents[1];ap=argparse.ArgumentParser();ap.add_argument('--candidate',type=Path);args=ap.parse_args()
O=R/'_shots/assault_revision_1017'/('candidate' if args.candidate else 'native');O.mkdir(parents=True,exist_ok=True)
checks=[];errors=[];rows={}
SETUP=next(ast.literal_eval(n.value) for n in ast.parse((R/'_BUILD_SOURCE/probe_feedback_1002.py').read_text()).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
def check(name,ok,data=None):
 checks.append(dict(name=name,passed=bool(ok),data=data));print(('PASS ' if ok else 'FAIL ')+name+((' '+json.dumps(data)) if not ok else ''),flush=True)
http.server.ThreadingHTTPServer.request_queue_size=128
port,stop=shoot.serve(str(R))
try:
 with sync_playwright() as pw:
  browser=pw.chromium.launch(channel='msedge',args=['--mute-audio']);p=browser.new_page(viewport=dict(width=1440,height=1000));p.set_default_timeout(150000)
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:750]) if m.type=='error' or 'draw error' in m.text else None)
  p.on('response',lambda r:errors.append(str(r.status)+' '+r.url) if r.status>=400 else None)
  if args.candidate:
   overrides={'/'+f.relative_to(args.candidate).as_posix():f.read_bytes() for f in args.candidate.rglob('*') if f.is_file()}
   def route(rt,rq):
    name=urlparse(rq.url).path
    if name in overrides:rt.fulfill(body=overrides[name],content_type='text/html' if name.endswith('.html') else 'application/javascript')
    else:rt.continue_()
   for name in overrides:p.route('**'+name+'*',route)
  p.goto(f'http://127.0.0.1:{port}/index.html');p.wait_for_function('window.__bofFrames>4&&typeof ROSTER17!=="undefined"');p.evaluate(shoot.TRAP_RAF)
  p.evaluate('''()=>{window.art17={};window.poses17=new Set();const di=ctx.drawImage;ctx.drawImage=function(im){const tag=PXG.tags.get(im);if(tag?.key)art17[tag.key]=(art17[tag.key]||0)+1;if(tag?.key==='a17_tankTurret'&&arguments.length===9)poses17.add(Math.floor(arguments[2]/256)*4+Math.floor(arguments[1]/256));return di.apply(this,arguments)};}''')
  p.evaluate('''()=>{window.pixels17=function(draw){ctx.canvas.width=ctx.canvas.width;ctx.setTransform(1,0,0,1,0,0);ctx.translate(-camX,0);draw();return new Uint8ClampedArray(ctx.getImageData(0,0,ctx.canvas.width,ctx.canvas.height).data);};
   window.changed17=function(a,b){let n=0;for(let i=0;i<a.length;i+=4)if(a[i]!==b[i]||a[i+1]!==b[i+1]||a[i+2]!==b[i+2])n++;return n;};}''')
  def setup(stage,kind=None,mini=False,diff='hard',pilot='cole'):
   p.evaluate(SETUP,dict(stage=stage,kind=kind,mini=mini,diff=diff,pilot=pilot));p.wait_for_function('()=>{stageLoadTick();return stageLoadReady(run.stage)&&bmfReady("game")}')
   p.evaluate('''()=>{story=fb2Talk=null;BOFCinematicDirector.cancel();warnT=0;warnKind=null;stagePlan=[];VP12.next=CP12.next=EP13.next=9999;Input.keys={};Input.mouse.down=false;
    subBossTriggered=true;player.invuln=1e9;powerups=[];TARGET17.nextTank=9999;SEWER17.next=9999;
    if(window.B){B._noHit=false;B._jcGhost=false;B._phaseInvuln=0;if(B._er26){B._er26.engaged=false;er26Tick(B,0);}}art17={};}''')
  def frames(n,expr='updatePlay(1/60);drawWorld(1/60);'):
   for i in range(0,n,24):p.evaluate('({n,expr})=>{for(let i=0;i<n;i++){'+expr+'}}',dict(n=min(24,n-i),expr=expr));p.wait_for_timeout(5)
  def snap(name):
   p.evaluate('()=>{shake=0;ctx.setTransform(SS,0,0,SS,0,0);drawWorld(0);SC12.refresh();window.__bofFit()}');p.screenshot(path=str(O/(name+'.png')))
  for diff in ['normal','hard','furious']:
   setup(4,'stormsovereign',diff=diff)
   row=p.evaluate('''()=>{er26Set(B,'sa14-storm');B._er26.t=B._er26.warm*.65;B._er26._sa14.wave=0;
    const lanes=sg17Fan(B);er26Draw(B);return{count:lanes.length,progress:lanes[0].progress,angles:lanes.map(l=>l.angle),draws:SG17.warnings};}''')
   check(diff+' lightning fan uses regular native FOV lanes',row['count']>=5 and row['progress']>.6 and row['draws']>0,row)
   snap('sovereign-'+diff+'-lightning-fov')
   row=p.evaluate('''()=>{eBullets=[];sa14Balls(B,false);const balls=eBullets.slice(),angles=balls.map(q=>Math.atan2(q.vy,q.vx));
    return{count:balls.length,angles,proof:balls.every(q=>q._weaponProof&&!q._shootable&&!enemyOrdnanceCanIntercept(q)),lanes:sg17Fan(B)};}''')
   check(diff+' lightning balls cannot be intercepted',row['proof'] and row['count']>=5,row)
   for weapon in ['mg','spread','beam','orb','gmiss']:
    row=p.evaluate('''kind=>{eBullets=[];const q=stage4WarfareShot(B,{x:worldWidth()/2,y:320},Math.PI/2,0,'orb',{szMul:.7});window.ball17=q;q.vx=q.vy=0;q.x=worldWidth()/2;q.y=320;_dmgBullet=null;
     pBullets=[{kind,x:q.x,y:q.y,vx:0,vy:0,w:18,h:26,r:24,dmg:99,t:0,life:1,top:240,bot:390,_bt:0,_hit:[],spd:0,ang:-Math.PI/2}];updatePlay(0);
     return{alive:!q.dead,proof:q._weaponProof,shootable:q._shootable,intercepted:!!q._intercepted};}''',weapon)
    check(diff+' actual '+weapon+' collision leaves lightning intact',row['alive'] and row['proof'] and not row['shootable'] and not row['intercepted'],row)
   row=p.evaluate('''()=>{er26Set(B,'sa14-overflight');const T=B._er26._sa14;B._er26.t=4.8;const initial=T.shot;sa14Overflight(B,1/60);return{initial,warning:sg17Fan(B)?.length||0,wave:T.wave};}''')
   check(diff+' first overhead-return volley has a warning window',row['initial']>=.7 and row['warning']>=5 and row['wave']==0,row)
   p.evaluate('''()=>{er26Set(B,'recover');B._s4war.shield.rearming=false;B._s4war.shield.active=false;stage4CoreTurretSpawnMissing(B,.5);}''')
   frames(240)
   row=p.evaluate('''()=>({jets:B._s4war.coreTurrets.filter(d=>!d.dead).map(d=>({size:d.size,entry:d._noHit,phase:d._sg17?.phase,age:d._sg17?.age})),shots:SG17.shots,art:art17.a17_stormJet||0})''')
   check(diff+' lightning guards use compact authored116px aircraft',len(row['jets'])==2 and all(j['size']==116 for j in row['jets']) and row['art']>0,row)
   check(diff+' guards finish entry and fire independently',all(not j['entry'] for j in row['jets']) and row['shots']>0,row)
   snap('sovereign-'+diff+'-large-lightning-guards')
   if diff=='hard':
    row=p.evaluate('''()=>{const d=B._s4war.coreTurrets[0];d.shield=0;d.flash=d.deflectFlash=0;mr27HelperState(d).flash=0;const a=pixels17(()=>mr27HelperDraw(B,d)),hp=d.hp;
     _lastHitX=d.x;_lastHitY=d.y;stage4CoreTurretDamage(B,d,1);const c=pixels17(()=>mr27HelperDraw(B,d)),pixels=changed17(a,c),flash=d.flash;sg17Wing(B,d,.3);
     return{pixels,flash,damage:hp-d.hp,expired:d.flash<=0&&mr27HelperState(d).flash<=0};}''')
    check('Large lightning guard damage changes native pixels and expires',row['pixels']>30 and row['damage']>0 and row['flash']>0 and row['expired'],row)
  for diff in ['normal','hard','furious']:
   setup(5,'chromehammer',diff=diff)
   p.evaluate('''()=>{B.x=worldWidth()/2;B.y=B._drawY=235;B.enter=false;B._noHit=false;B.hp=B.maxhp*.6;fr27BeginArmor(B);B._hammer.frArmor.activated=true;B._noHit=false;fr27Restore(B,.1,false,false);B.flash=0;}''')
   frames(95)
   row=p.evaluate('''()=>{const h=B._hammer,C=hc17Counter(B),state=h.state;
    _dmgBullet={kind:'mg',x:B.x,y:B.y};B._hammerModuleHit='hammer';hammerBossDamage(B,999);_dmgBullet=null;
    return{required:C.required,hits:C.hits,charging:h.recovery.status==='charging',duration:h.recovery.duration,state,flash:B.flash};}''')
   check(diff+' charge stays up against bullets and lasts for a missile volley',row['required']>=3 and row['duration']>=7 and row['charging'] and row['hits']==0,row)
   snap('hammer-'+diff+'-charge-before-missiles')
   row=p.evaluate('''()=>{const h=B._hammer,C=hc17Counter(B),counts=[];window.counter17=C;
    for(let i=0;i<C.required-1;i++){_dmgBullet={kind:'gmiss',x:B.x,y:B.y};B._hammerModuleHit='body';hammerBossDamage(B,20);hammerBossDamage(B,20);counts.push(C.hits);}_dmgBullet=null;
    return{counts,hits:C.hits,required:C.required,status:h.recovery.status,flash:B.flash};}''')
   check(diff+' multiple unique missile impacts are required; one missile cannot double count',row['hits']==row['required']-1 and row['counts']==list(range(1,row['required'])) and row['status']=='charging',row)
   snap('hammer-'+diff+'-missile-hit-charge')
   row=p.evaluate('''()=>{_dmgBullet={kind:'retinaMissile',x:B.x,y:B.y};B._hammerModuleHit='hammer';hammerBossDamage(B,20);_dmgBullet=null;return{status:B._hammer.recovery.status,state:B._hammer.state,hits:counter17.hits,required:counter17.required};}''')
   check(diff+' final missile interrupts the heal and opens a punish window',row['status']=='cancelled' and row['state']=='fr_stun',row)
   frames(28);check(diff+' Hammer actual hit flash expires',p.evaluate('B.flash<=0'))
  setup(5,'siegebomber',True)
  frames(180);row=p.evaluate('()=>({kind:B.kind,space:B._bomber.space,name:B.name,parts:B._bomber.parts.length})')
  check('Stage5 now fields the Earth Siege Bomber with its modular weapons',not row['space'] and row['parts']>=4,row);snap('stage5-siege-bomber')
  setup(6,'siegefortress17',True)
  frames(240);row=p.evaluate('()=>({kind:B.kind,cargo:!!B._cargo13,mini:B._cargo17Mini,boss:!!boss,hp:B.maxhp,guns:B._cargo13.guns.length})')
  check('Stage6 new fortress is a true miniboss with six batteries',row['mini'] and row['guns']==6 and not row['boss'] and row['hp']<2200,row);snap('stage6-fortress-mini')
  row=p.evaluate('''()=>{const C=B._cargo13,core=C.core;for(const g of C.guns.slice(0,5)){C.directId=g.id;hitSubBoss(1e6);}C.directId='core';hitSubBoss(1e6);
   const locked=C.core===core&&!sc13Open(B);C.directId=5;hitSubBoss(1e6);const opened=sc13Open(B);C.directId='core';hitSubBoss(1e6);
   return{locked,opened,dead:B.dead,bossDefeated,active:subBossActive};}''')
  check('Fortress reactor stays locked through five broken batteries and opens on sixth',row['locked'] and row['opened'],row)
  check('Defeating fortress does not finish Stage6',row['dead'] and not row['bossDefeated'],row)
  frames(190);check('Fortress death releases the native miniboss progression',p.evaluate('subBossDone&&!subBossActive&&!subBoss'))
  for diff in ['normal','hard','furious']:
   setup(6,'warhive',diff=diff);frames(240)
   row=p.evaluate('()=>({old:!!B._carrier17,cargo:!!B._cargo13,parts:B._carrier17.parts.map(p=>({id:p.id,kind:p.kind})),ready:roster17Ready(B),targets:retinaBossTargets(B).length})')
   check(diff+' original flyover Harrier has fan, laser and missile targets',row['old'] and not row['cargo'] and len(row['parts'])==8 and row['targets']==8,row);snap('harrier-'+diff+'-modules')
   if diff=='hard':
    for ident in ['L','laser0','rackL']:
     row=p.evaluate('''id=>{const C=B._carrier17,p=C.parts.find(p=>p.id===id);p.flash=p.fl=0;const a=pixels17(()=>roster17Draw(B)),hp=p.hp;C.direct=id;warhiveDamage(B,1);const c=pixels17(()=>roster17Draw(B)),pixels=changed17(a,c),flash=p.flash;roster17Weapon(B,p,.3);
      return{pixels,flash,damage:hp-p.hp,expired:p.flash<=0};}''',ident)
     check('Harrier '+ident+' hit changes actual module pixels and expires',row['pixels']>10 and row['damage']>0 and row['flash']>0 and row['expired'],row)
   row=p.evaluate('''()=>{const C=B._carrier17,hp=C.reactor;C.direct='reactor';warhiveDamage(B,1e6);const locked=C.reactor===hp;
    for(const part of C.parts.filter(p=>p.kind==='laser')){C.direct=part.id;warhiveDamage(B,1e6);}C.direct='reactor';warhiveDamage(B,1e6);
    return{locked,lasersGone:C.parts.filter(p=>p.kind==='laser').every(p=>p.dead),stillLocked:C.reactor===hp,open:B._whv.doorOpen};}''')
   check(diff+' lasers alone do not expose reactor while fans or racks survive',row['locked'] and row['lasersGone'] and row['stillLocked'] and not row['open'],row)
   p.evaluate('''()=>{const C=B._carrier17;for(const part of C.parts.filter(p=>!p.dead)){C.direct=part.id;warhiveDamage(B,1e6);}}''');snap('harrier-'+diff+'-reactor-open')
   row=p.evaluate('''()=>{const C=B._carrier17,targets=retinaBossTargets(B);C.direct='reactor';warhiveDamage(B,30);const damaged=C.reactor<C.maxReactor;C.direct='reactor';warhiveDamage(B,1e6);return{open:B._whv.doorOpen,targets:targets.map(p=>p.kind),quick:C.maxReactor<600,damaged,dead:B.dead,defeated:bossDefeated};}''')
   check(diff+' all modules open a short final reactor phase and native boss defeat',row['open'] and row['quick'] and row['damaged'] and row['dead'] and row['defeated'],row)
  setup(6,'warhive')
  row=p.evaluate('''()=>{const C=B._carrier17;C.phase='flyover';C.t=1;C.depth=true;B._noHit=true;player.x=B.x;player.y=B.y+6;player.invuln=0;run.shield=0;updatePlay(0);return{dead:player.dead,contact:target17BossContact(B,B.x,B.y)};}''')
  check('Harrier overhead pass cannot cause contact death',not row['dead'] and not row['contact'],row)
  setup(6)
  row=p.evaluate('''()=>{subBossDone=true;subBossActive=false;subBoss=null;boss=null;bossActive=false;s6WingInit();s6Wing.fakeDone=true;s6Wing.choice=false;s6Wing.reinforce=999;
   window.liveEnemy17=spawnEnemy('s6lancer',worldWidth()/2,140,{});liveEnemy17._fcd=999;
   window.liveRound17=eShootT(worldWidth()/2+80,220,Math.PI/2,2,'s6tracer');window.radioBefore17={x:player.x,map:mapScroll,y:liveEnemy17.y,round:liveRound17.y,time:stageTimer};
   stagePlan=[{at:0,t:0,fn:()=>spawnEnemy('s6lancer',200,100,{})}];window.plan17=stagePlan;fb2TalkStart();Input.keys[keybind.right]=true;return {live:enemies.length};}''')
  p.keyboard.down('ArrowRight');frames(60);p.keyboard.up('ArrowRight')
  row=p.evaluate('''()=>({moving:player.x-radioBefore17.x,scroll:mapScroll-radioBefore17.map,enemyMoved:liveEnemy17.y-radioBefore17.y,roundMoved:liveRound17.y-radioBefore17.round,roundAlive:eBullets.includes(liveRound17),stageTimer,saved:radioBefore17.time,plan:stagePlan===plan17,active:fb2TalkActive(),hold:RADIO17.frames,spawn:spawnEnemy('s6lancer',200,100,{})===null})''')
  check('Cole radio keeps flight, map, existing enemies and rounds running',abs(row['moving'])>5 and row['scroll']>0 and abs(row['roundMoved'])>50,row)
  check('Radio holds new spawns and preserves scheduled wave queue',row['spawn'] and row['plan'] and row['stageTimer']==row['saved'] and row['active'],row);snap('stage6-live-radio')
  p.evaluate('()=>{Input.keys={};fb2Talk.done=true;s6Wing.choice=true;s6Wing.route=null;}');frames(12)
  check('Route selection continues the spawn hold',p.evaluate('radio17Live()&&spawnEnemy("s6lancer",200,100,{})===null'))
  p.evaluate('()=>{s6Wing.route="left";s6Wing.choice=false;fb2Talk=null;}')
  check('Choosing a route releases enemy spawning',p.evaluate('!!spawnEnemy("s6lancer",worldWidth()/2,100,{})'))
  setup(4)
  row=p.evaluate('''()=>{window.tank17=spawnEnemy('sandtank',worldWidth()/2,PLAY.y+110,{});return{size:[tank17.w,tank17.h],mod:!!tank17._armor17,parts:tank17._armor17.parts.length,hp:tank17.maxhp,paved:armor17Road(tank17.x,tank17.y)};}''')
  check('Stage4 tanks are larger, modular and stronger than Stage1 armor',row['mod'] and row['size'][0]>=88 and row['size'][1]>=104 and row['parts']==3 and row['hp']>55 and row['paved'],row)
  frames(210);snap('stage4-heavy-modular-tank')
  row=p.evaluate('''()=>({shots:ARMOR17.shots,shells:eBullets.filter(q=>q._armor17Shell).map(q=>({homing:q.homing,proof:q._weaponProof,a:Math.atan2(q.vy,q.vx)})),art:{hull:art17.a17_tankHull||0,turret:art17.a17_tankTurret||0,shell:art17.a17_tankShell||0}})''')
  check('Heavy tanks release real cannon shells and authored modular art',row['shots']>0 and row['art']['hull']>0 and row['art']['turret']>0 and row['art']['shell']>0,row)
  check('Heavy cannon plays all sixteen authored recoil/reload poses',p.evaluate('poses17.size===16'),p.evaluate('[...poses17]'))
  row=p.evaluate('''()=>{const p=tank17._armor17.parts[0],hp=p.hp,hull=tank17._armor17.hull,m=armor17TurretPoint(tank17,-1);_dmgBullet={kind:'mg',x:m.x,y:m.y-5};hitEnemy(tank17,1);_dmgBullet=null;return{damage:hp-p.hp,hull:tank17._armor17.hull===hull,mount:Math.hypot(m.x-tank17.x,m.y-tank17.y)};}''')
  check('Metal shells originate at actual cannon tips and incoming fire hits that module',row['damage']>0 and row['hull'] and row['mount']>55,row)
  row=p.evaluate('''()=>{const p=tank17._armor17.parts[1],hp=p.hp,hull=tank17._armor17.hull;p.flash=0;const a=pixels17(()=>drawModularTank(tank17));_dmgBullet={kind:'mg',x:tank17.x+p.dx,y:tank17.y+p.dy};hitEnemy(tank17,2);_dmgBullet=null;const c=pixels17(()=>drawModularTank(tank17));return{part:p.hp<hp,hull:tank17._armor17.hull===hull,flash:p.flash,pixels:changed17(a,c),dead:tank17.dead,y:tank17.y};}''')
  check('Tank rack damage stays on its own pool and visibly flashes native pixels',row['part'] and row['hull'] and row['flash']>0 and row['pixels']>10,row)
  row=p.evaluate('''()=>{const p=tank17._armor17.parts[2],hp=p.hp,targets=_lockTargets(),t=targets.find(q=>q._retinaOwner===tank17&&q._retinaId==='armor rackR');const hit=retinaMissileDamage(t,2,{kind:'gmiss',x:t.x,y:t.y});return{count:targets.filter(q=>q._retinaOwner===tank17).length,hit,damage:hp-p.hp};}''')
  check('Tank racks and cannon support separate native Retina missile locks',row['count']==4 and row['hit'] and row['damage']>0,row)
  setup(1)
  p.wait_for_function('()=>{a17Warm();return Object.values(A17_ART).every(a=>XART.rdy(a.key))}')
  row=p.evaluate('''()=>{const out=[];for(const kind of ['mg','spread','heavy','beam']){
    const family=kind==='heavy'?'heavy':kind==='beam'?'laser':kind==='mg'?'bullets':kind;
    const b={kind:kind==='heavy'?'mg':kind,_cal50:kind==='heavy',_inf:'wind',_infLv:3,x:worldWidth()/2,y:350,vx:0,vy:-8,w:12,h:24,top:80,bot:400,t:0};
    ctx.canvas.width=ctx.canvas.width;ctx.setTransform(1,0,0,1,0,0);const cw=ctx.canvas.width,ch=ctx.canvas.height;const n=wp11Paint(ctx,AP10_FX_ART['wind_'+family],wp11Resolve,b,0),data=ctx.getImageData(0,0,cw,ch).data;
    let minX=1e9,maxX=0,minY=1e9,maxY=0;for(let y=0;y<ch;y++)for(let x=0;x<cw;x++){const j=(y*cw+x)*4;if(data[j+3]>70&&data[j]+data[j+1]+data[j+2]>75){minX=Math.min(minX,x);maxX=Math.max(maxX,x);minY=Math.min(minY,y);maxY=Math.max(maxY,y);}}
    out.push({kind,n,w:maxX-minX+1,h:maxY-minY+1});
   }return out;}''')
  for q in row:check(q['kind']+' wind draws a compact authored projectile or single continuous laser',q['n']==1 and (q['w']<45 and q['h']<30 if q['kind']!='beam' else q['h']>280 and q['w']<45),q)
  p.evaluate('''()=>{pBullets=['mg','spread','heavy','beam'].map((kind,i)=>({kind:kind==='heavy'?'mg':kind,_cal50:kind==='heavy',_inf:'wind',_infLv:3,x:worldWidth()/2-120+i*75,y:330,vx:0,vy:-8,w:12,h:24,top:90,bot:410,t:.5,dmg:1}));}''');snap('compact-wind-family')
  check('Maverick homing lasers remain excluded from Wind',p.evaluate('wp11Family({kind:"mavlaser",_inf:"wind"})===null'))
  pressure=[]
  for diff in ['normal','hard','furious']:
   setup(7,diff=diff);p.evaluate('()=>{subBossDone=true;SEWER17.next=.01;SEWER17.spawned=0;TARGET17.nextTank=9999;}')
   row=p.evaluate('''()=>{window.centerTanks17=[.08,.92].map(f=>spawnEnemy('s7tank',worldWidth()*f,130,{}));return centerTanks17.map(e=>({x:e.x,...sewer17Band(e)}));}''')
   check(diff+' Stage7 tanks spawn inside the middle floor strip',all(q['l']<=q['x']<=q['r'] for q in row),row)
   frames(1200)
   row=p.evaluate('''()=>({spawns:SEWER17.spawned,shots:enemies.reduce((s,e)=>s+(e._eb11?.attacks||0),0),tanks:centerTanks17.map(e=>({x:e.x,...sewer17Band(e)})),rounds:eBullets.length,profile:eb11Profile()})''')
   pressure.append(row['spawns']);check(diff+' Stage7 has active attacks and sustained complementary waves',row['spawns']>=2 and row['shots']>2,row)
   check(diff+' Stage7 tanks remain central after motion and separation',all(q['l']<=q['x']<=q['r'] for q in row['tanks']),row);snap('stage7-'+diff+'-pressure')
  check('Stage7 reinforcement pressure increases Normal -> Hard -> Furious',pressure[0]<pressure[1]<pressure[2],pressure)
  row=p.evaluate('''()=>{const before=SEWER17.spawned;stageTimer=curStage.length-2;SEWER17.next=0;sewer17Wave(10);return{before,after:SEWER17.spawned};}''')
  check('Extra Stage7 pressure releases the authored boss approach instead of refilling its crowd gate',row['before']==row['after'],row)
  check('No page, console or missing-asset errors',not errors,errors);browser.close()
except Exception as e:
 errors.append(str(e));print(traceback.format_exc(),flush=True)
finally:
 stop();report=dict(passed=sum(c['passed'] for c in checks),failed=sum(not c['passed'] for c in checks),checks=checks,errors=errors,scope='Actual Chromium/index.html, native actors, update/collision paths and authored-pixel screenshots. Controlled fixtures; not a full human campaign balance certification.')
 (O/'verification.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:v for k,v in report.items() if k!='checks'}),flush=True)
if errors or report['failed']:sys.exit(1)
