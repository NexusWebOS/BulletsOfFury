"""Native October 2 gameplay fixtures. Deliberately not campaign completion evidence."""
from pathlib import Path
import sys,json,base64,http.server
from playwright.sync_api import sync_playwright
import shoot as sh
R=Path(__file__).resolve().parents[1];O=R/'_shots/feedback_1002';O.mkdir(parents=True,exist_ok=True)
errors=[];report={'checks':[],'scenes':[]};port,stop=sh.serve(str(R))
def check(v,name):
 report['checks'].append({'ok':bool(v),'name':name});print(('OK ' if v else 'FAIL ')+name,flush=True)
SETUP="""c=>{ht27Stop();debugFight=null;coopOn=false;diffKey=c.diff||'normal';DIFF=DIFFS[diffKey];run.pilot=c.pilot||'yuri';run.mode='campaign';run._freezerL2Cleared=false;beginStage(c.stage);setState(GS.PLAY);player.reset();BOFCinematicDirector.cancel();story=null;special=null;thunderStorm=null;s6Opening=null;s6Wing=null;stagePlan=[];spawnClock=9999;waveIdx=999;enemies=[];eBullets=[];pBullets=[];powerups=[];boss=null;bossActive=false;subBoss=null;subBossActive=false;groundTargetingReset();tb28Reset();polishLanes=[];stageTimer=0;player.x=worldWidth()/2;player.y=VH-110;camX=player.x-VW/2;player.invuln=1e9;if(c.kind){if(c.mini)spawnSubBoss__inner(c.kind);else spawnBoss(c.kind);window.B=c.mini?subBoss:boss;B._be=null;B.enter=false;B._noHit=false;B.x=worldWidth()/2;B.y=B._er26?.home||B.ty||160;B._drawY=B.y;}return true;}"""
def shot(p,name,draw='drawWorld(0);'):
 p.evaluate('()=>{shake=0;ctx.setTransform(SS,0,0,SS,0,0);'+draw+'}')
 (O/(name+'.png')).write_bytes(base64.b64decode(p.evaluate('()=>cv.toDataURL().split(",")[1]')))
def frames(p,n,expr='updatePlay(1/60);drawWorld(1/60);'):
 for i in range(0,n,30):
  p.evaluate('(n)=>{for(let i=0;i<n;i++){'+expr+'}}',min(30,n-i));p.wait_for_timeout(8)
try:
 with sync_playwright() as pw:
  b=pw.chromium.launch(args=['--no-sandbox','--autoplay-policy=no-user-gesture-required']);p=b.new_page(viewport={'width':1100,'height':900})
  p.on('pageerror',lambda e:errors.append(str(e)));p.on('console',lambda m:errors.append(m.text[:600]) if m.type=='error' or 'draw error' in m.text else None)
  p.goto(f'http://127.0.0.1:{port}/index.html',timeout=120000);p.wait_for_function('()=>window.__bofFrames>4',timeout=120000);p.evaluate(sh.TRAP_RAF);p.mouse.click(500,500)
  p.wait_for_timeout(50)
  p.evaluate('()=>{fb1002Warm();er26Warm();missionWarm();for(const k of Object.keys(MR27_ART))XART.rdy("mr27_"+k);}')
  p.wait_for_function('()=>Object.values(FB1002_ART).every(a=>XART.rdy(a.key))&&XART.rdy("mr27_storm")',timeout=120000,polling=50)
  p.evaluate(SETUP,{'stage':1,'pilot':'freezer'})
  check(p.evaluate('()=>weaponIconKey(4,5)==="fb1002_icebreath"&&weaponDisplayName(4)==="ICE BREATH"&&weaponBaseForms(4).length===1'),'Freezer locked Ice Breath name/icon')
  check(p.evaluate('()=>weaponFormSelect(4,{kind:"variant",id:"flamethrower"})==="locked"&&forgeCombine(4,"fire")==="locked"'),'cannot change Ice Breath before Level2 clear')
  p.evaluate('()=>startSpecial()')
  before=p.evaluate('()=>({t:stageTimer,map:mapScroll,x:player.x,y:player.y})');frames(p,60)
  after=p.evaluate('()=>({t:stageTimer,map:mapScroll,x:player.x,y:player.y})');report['clock']=[before,after]
  check(after['t']-before['t']>.98,'Freezer special does not halve campaign progression')
  p.evaluate('()=>{timeScale=1;special=null;freezerStageClearDefaults(1);loadoutStart(()=>{});}')
  frames(p,1,'drawLoadout(1/60);');shot(p,'freezer-loadout','drawLoadout(0);')
  p.evaluate('()=>freezerStageClearDefaults(2)');check(p.evaluate('()=>weaponBaseForms(4).length>=2'),'Ice Breath form lock opens after Level2')
  p.evaluate(SETUP,{'stage':1});p.evaluate('()=>{subBossDone=true;subBossTriggered=true;stageTimer=curStage.length;damAssaultReady1002();}');frames(p,140)
  check(p.evaluate('()=>!bossWarned&&run._damAssault1002.waves>0&&enemies.some(e=>e._damBomber1002)'),'dam bombers precede chopper')
  shot(p,'dam-bombers')
  frames(p,1500)
  check(p.evaluate('()=>run._damAssault1002.done&&run._damAssault1002.waves===4&&bossWarned'),'all four dam waves release the chopper warning')
  shot(p,'dam-chopper-arrival')
  p.evaluate(SETUP,{'stage':2});p.evaluate('()=>{player.x=worldWidth()/2;window.boxes=["ultra","uber"].map((tier,i)=>{const q={kind:"missileupbox_"+tier,x:player.x+i*90,y:player.y-100,vy:0,t:0,w:60,h:60,hp:3};powerups.push(q);pBullets.push({kind:"mg",x:q.x,y:q.y+1,vx:0,vy:0,w:5,h:12,dmg:3,t:0});return q;});}');frames(p,2)
  check(p.evaluate('()=>boxes.every(q=>q.dead)&&powerups.some(q=>q.kind==="missileup_ultra")&&powerups.some(q=>q.kind==="missileup_uber")'),'Ultra/Uber crates open from actual ordinary bullets')
  p.evaluate('()=>window.jet=spawnEnemy("golem",worldWidth()/2,180,{})');check(p.evaluate('()=>jet.type==="firejet1002"&&jet._fireJet1002'),'retired golem resolves to generated fire jet');shot(p,'replacement-firejet')
  p.evaluate(SETUP,{'stage':2,'kind':'magmaward','mini':True,'diff':'furious'});p.evaluate('()=>fb1002Meteor(B)')
  check(p.evaluate('()=>groundTargetingFx.length===27&&new Set(groundTargetingFx.map(q=>q._meteor1002.zone)).size===3'),'Furious magma retina pattern has three groups of nine')
  frames(p,55);shot(p,'magma-retina-groups')
  p.evaluate('()=>{groundTargetingReset();er26Shot(B,"L",Math.PI/2,2,{large:true});const q=eBullets.at(-1);q.x=player.x;q.y=player.y-90;window.magma=q;pBullets.push({kind:"mg",x:q.x,y:q.y,vx:0,vy:0,w:8,h:12,dmg:5,t:0});}')
  frames(p,1);check(p.evaluate('()=>magma.dead&&magma._fbImpact1002'),'shooting magma ball invokes authored explosion/audio');shot(p,'magma-shotdown')
  for diff in ['normal','hard','furious']:
   for kind,mini in [('frostcruiser',True),('cryospear',False),('stormsovereign',False)]:
    p.evaluate(SETUP,{'stage':4 if kind=='stormsovereign' else 3,'kind':kind,'mini':mini,'diff':diff})
    p.evaluate('()=>{B._er26.neutralOpening=false;B._er26.nuclearRevealed=true;B._er26.form="ice";if(run.stage===3&&diffKey==="furious")B._s3Nuclear={mode:"ice",introDone:true};if(B._s4war){B._s4war.shield.active=false;B._s4war.shield.rearming=false;}er26Set(B,B._ship==="frostcruiser"?"elite-beam1002":B._ship==="cryospear"?"ice-battery1002":"storm-lance1002");storySkip();BOFCinematicDirector.cancel();thaw=null;}')
    frames(p,40,'storySkip();BOFCinematicDirector.cancel();updatePlay(1/60);drawWorld(1/60);');shot(p,kind+'-'+diff+'-charge');frames(p,70,'storySkip();BOFCinematicDirector.cancel();updatePlay(1/60);drawWorld(1/60);');shot(p,kind+'-'+diff+'-attack')
    check(p.evaluate('()=>B._mr27&&B._mr27.parts.length>0'),kind+' modular weapons '+diff)
    if kind=='frostcruiser':
     check(p.evaluate('()=>B._mr27.skin==="frost1002"'),'new generated miniboss hull '+diff)
     check(p.evaluate('()=>["L0","L1","R0","R1"].every(s=>{const p=shipBossMount(B,s);return Number.isFinite(p.x+p.y);})'),'finite modular barrel mounts '+diff)
    if kind=='cryospear':check(p.evaluate('()=>eBullets.some(q=>q._coldTracer1002)'),'rapid visible cold bullets '+diff)
    if kind=='stormsovereign':
     check(p.evaluate('()=>B._mr27.parts.some(q=>q.id==="lightning")'),'lightning barrel destroyable '+diff)
     p.evaluate('()=>{stage4CoreTurretSpawnMissing(B,.5);B._s4war.coreTurrets.forEach(d=>{d.materialize=1;d._pressure1002={t:0,cd:0,aim:null,burst:0};});window.helperShots=0;}')
     frames(p,170,'storySkip();BOFCinematicDirector.cancel();updatePlay(1/60);helperShots=Math.max(helperShots,eBullets.filter(q=>q._s4wKind==="rocket").length);drawWorld(1/60);')
     check(p.evaluate('()=>helperShots>0&&B._s4war.coreTurrets.some(d=>d._pressure1002.burst>0)'),'materialized boss helpers release real rockets '+diff)
     shot(p,'stage4-helper-burst-'+diff)
     p.evaluate('()=>{const q=stage4WarfareShot(B,"ROCKET_L",Math.PI/2,3,"rocket",{shootable:true,hp:2});window.rocket=q;window.target=fb1002MissileTarget(q);}')
     check(p.evaluate('()=>_lockTargets().includes(target)&&retinaMissileDamage(target,3,{kind:"gmiss"})&&rocket.dead'),'Retina destroys boss missile '+diff)
     p.evaluate('()=>{B._mr27.parts.forEach(q=>q.dead=true);B._s4war.shield.rearming=false;B._s4war.shield.active=false;}');frames(p,110)
     check(p.evaluate('()=>!!B._mr27.ram1002'),'weaponless boss rams '+diff);shot(p,'stage4-ram-'+diff)
  # Arrival fixtures preserve the real neutral/bomb/new-form sequence and actor.
  for kind,mini in [('frostcruiser',True),('cryospear',False)]:
   p.evaluate(SETUP,{'stage':3,'kind':kind,'mini':mini,'diff':'furious'})
   p.evaluate('()=>{thaw=null;window.originalActor=B;window.originalHP=B.hp;storySkip();}')
   frames(p,120);shot(p,kind+'-nuclear-impact');frames(p,250)
   check(p.evaluate('()=>B===originalActor&&B.hp===originalHP&&B._s3Nuclear?.introDone&&!B._er26.neutralOpening'),'one continuous neutral/bomb/new form '+kind)
   shot(p,kind+'-post-nuclear')
  for diff in ['normal','hard','furious']:
   for stage,kind in [(7,'s7lamprey'),(7,'s7serpent'),(7,'s7sampler'),(8,'s8interceptor'),(8,'s8bomber'),(8,'s8needlejet'),(8,'s8gunship')]:
    p.evaluate(SETUP,{'stage':stage,'diff':diff})
    p.evaluate('(kind)=>{window.E=spawnEnemy(kind,player.x,130,{});E._s8Roll=null;E._furyMove=null;storySkip();E.hp=E.maxhp=1000;window.maxStep=0;window.peakShots=0;window.finiteShots=true;window.prev={x:E.x,y:E.y};}',kind)
    flight='storySkip();BOFCinematicDirector.cancel();updatePlay(1/60);peakShots=Math.max(peakShots,eBullets.length);finiteShots=finiteShots&&eBullets.every(q=>Number.isFinite(q.x+q.y+q.vx+q.vy));maxStep=Math.max(maxStep,Math.hypot(E.x-prev.x,E.y-prev.y));prev={x:E.x,y:E.y};drawWorld(1/60);'
    frames(p,90,flight);shot(p,kind+'-'+diff+'-warning')
    frames(p,75,flight);shot(p,kind+'-'+diff+'-burst')
    check(p.evaluate('()=>E.spin===0&&E._bank===0&&E._frBank===0&&maxStep<6'),'straight smooth '+kind+' '+diff)
    check(p.evaluate('()=>peakShots>0&&finiteShots'),'finite real attack '+kind+' '+diff)
    report['scenes'].append(p.evaluate('()=>({kind:E.type,diff:diffKey,peakShots,maxStep,ai:E._straight1002||E._frRealmAI})'))
    p.evaluate('()=>{window.hullAngles=[];const draw=ctx.drawImage;ctx.drawImage=function(...a){const w=a.length===5?a[3]:a[7],h=a.length===5?a[4]:a[8];if(w*h>3000){const m=this.getTransform();hullAngles.push(Math.atan2(m.b,m.a));}return draw.apply(this,a);};try{drawEnemy(E);}finally{ctx.drawImage=draw;}}')
    check(p.evaluate('()=>hullAngles.length>0&&hullAngles.every(a=>Math.abs(a)<.001)'),'actual straight hull blits '+kind+' '+diff)
  # Other rotating render paths must also obey the hull rule. The independent
  # weapon rig is intentionally outside this transform check.
  p.evaluate(SETUP,{'stage':1})
  p.evaluate('()=>{window.D=spawnEnemy("s1jetdelta",player.x,160,{});droidMake(D);D._rot=1.7;D._twist=.55;window.angles=[];const draw=ctx.drawImage;ctx.drawImage=function(...a){const m=this.getTransform();angles.push(Math.atan2(m.b,m.a));return draw.apply(this,a);};try{drawEnemy(D);}finally{ctx.drawImage=draw;}}')
  check(p.evaluate('()=>angles.length>0&&angles.every(a=>Math.abs(a)<.001)&&D._rot===1.7&&D._twist===.55'),'other droid hulls draw straight without losing independent state')
  shot(p,'ordinary-straight-droid')
  p.evaluate(SETUP,{'stage':5,'diff':'normal'})
  p.evaluate('()=>{spawnBoss(curStage.boss);B=boss;B._be=null;B.enter=false;B._noHit=false;B.x=worldWidth()/2;B.y=VH*.34;const h=B._hammer;h.balance0922=true;h.mode="hammer";h.intro1002=true;h.frArmor={hp:1,max:1,t:0,barrier:0,rage:false,half:true,checkpoints:[.75,.5,.35,.15]};hammerState(B,"hammer");window.regularStates=[];}')
  for n in range(6):
   frames(p,900,'updatePlay(1/60);if(regularStates.at(-1)!==B._hammer.state)regularStates.push(B._hammer.state);drawWorld(1/60);')
   if p.evaluate('()=>["spin","throw","giant_dive","ball"].every(s=>regularStates.includes(s))'):break
  check(p.evaluate('()=>["spin","throw","giant_dive","ball"].every(s=>regularStates.includes(s))'),'ordinary Normal fight naturally uses throws orbital jumps and spiked ball')
  report['regularHammer']=p.evaluate('()=>regularStates');shot(p,'hammer-ordinary-book')
  p.evaluate(SETUP,{'stage':5,'diff':'hard'})
  # Real Stage5 spawn uses its authored current boss kind (not the stage1 fixture).
  p.evaluate('()=>{boss=null;spawnBoss(curStage.boss);B=boss;B._be=null;B._noHit=true;B.enter=true;B._hammer.state="unfold";B._hammer.t=1.99;B.x=worldWidth()/2;B.y=VH*.34;}');frames(p,2)
  check(p.evaluate('()=>BOFCinematicDirector.current?.id==="hammer-trap1002"'),'regular Hammer taunt follows transformation');frames(p,150);shot(p,'hammer-taunt')
  p.evaluate('()=>BOFCinematicDirector.finish()');check(p.evaluate('()=>B._hammer.state==="warn"'),'dialogue immediately begins jump attack')
  p.evaluate('()=>{B._noHit=false;B._hammerModuleHit="hammer";window.hh=B._hammer.hammerHP;_dmgBullet={kind:"spaceVolley"};window.loss=hammerBossDamage(B,50);_dmgBullet=null;}')
  check(p.evaluate('()=>loss===0&&B._hammer.hammerHP===hh'),'passive volley cannot damage hammer')
  p.evaluate('()=>{B._hammerModuleHit="hammer";_dmgBullet={kind:"gmiss",tgt:null};window.loss=hammerBossDamage(B,50);_dmgBullet=null;}')
  check(p.evaluate('()=>loss===0&&B._hammer.hammerHP===hh'),'unguided manual missile cannot damage hammer')
  p.evaluate('()=>{hammerState(B,"whirl_turn");B._hammerModuleHit="hammer";_dmgBullet={kind:"gmiss"};hammerBossDamage(B,999);_dmgBullet=null;}');check(p.evaluate('()=>B._hammer.state==="whirl_turn"'),'whirlwind windup cannot be stunned')
  p.evaluate('()=>{hammerState(B,"hammer");B._hammer.regularBook1002=1;B._hammer.t=2;B._hammer.balance0922=true;B._hammer.frArmor=null;}');frames(p,2);shot(p,'hammer-regular-throw')
  p.evaluate('()=>{B._hammer.stormTarget={x:player.x,y:player.y};B._hammer.stormBounds={l:0,r:worldWidth(),bottom:hammerStormFloorY()};hammerStormImpact(B);}');check(p.evaluate('()=>B._hammer.stormWaves.every(q=>q.height===PLAY.h&&q.y>VH-80)'),'Hammer bottom row spans full play height');frames(p,230);shot(p,'hammer-fullheight-spikes')
  # Fire a real locked missile from an offset. Hold a legal targetable pose;
  # the real missile update, steering, target routing and damage stay active.
  p.evaluate('()=>{B._hammer.frArmor={hp:1,max:1,t:0,barrier:0,rage:false,half:true,checkpoints:[.75,.50,.35,.15]};B._hammer.mode="hammer";B._hammer.recovery=null;B._hammer.hammerHP=B._hammer.hammerMax;B._noHit=false;B._hammer.phasePending=false;B._hammer.hammerDestroyed=false;hammerState(B,"hammer");window.lockedHammer=_lockTargets().find(t=>t.kind==="hammer");window.preLockHP=B._hammer.hammerHP;run.bombs=3;player.x=B.x-100;useBomb(lockedHammer);window.curvedMissile=pBullets.at(-1);window.maxMissileVx=0;}')
  frames(p,140,'B._hammer.state="hammer";B._hammer.t=-100;updatePlay(1/60);maxMissileVx=Math.max(maxMissileVx,Math.abs(curvedMissile.vx||0));drawWorld(1/60);')
  check(p.evaluate('()=>curvedMissile.tgt===lockedHammer&&curvedMissile.dead&&maxMissileVx>1&&B._hammer.hammerHP<preLockHP'),'real curved Retina missile damages the hammer')
  p.evaluate('()=>{B._hammer.mode="chaingun";B._hammer.chainDestroyed=false;B._hammer.frRecovery=false;B._hammer.recovery=null;hammerChainStart(B);window.chainFrames=0;window.chainShots=0;for(let i=0;i<8;i++)XART.rdy("arch_blaster_body_"+i);}')
  p.wait_for_function('()=>XART.rdy("arch_blaster_body_5")',timeout=120000,polling=50)
  frames(p,120,'updatePlay(1/60);if(B._hammer.state==="chaingun")chainFrames++;chainShots=Math.max(chainShots,eBullets.filter(q=>q._archBlaster).length);drawWorld(1/60);');shot(p,'hammer-new-chaingun')
  check(p.evaluate('()=>chainFrames>30&&chainShots>=4'),'new modular chaingun plays a sustained real attack')
  p.evaluate('()=>{B._hammer.frArmor.rage=true;B._hammer.frArmor.barrier=0;B._hammer.mode="hammer";B._hammer.phasePending=false;B._hammer.ragePair1002=0;B._hammer.comboPending=false;hammerTarget(B);hammerState(B,"warn");window.rageStates=[];window.rageRest=0;}')
  frames(p,720,'updatePlay(1/60);if(rageStates.at(-1)!==B._hammer.state)rageStates.push(B._hammer.state);if(B._hammer.state==="recharge1002")rageRest+=1/60;drawWorld(1/60);')
  check(p.evaluate('()=>rageStates.filter(s=>s==="leap").length===2&&rageStates.includes("recharge1002")&&rageRest>=Math.max(BR_COOL,SS_COOL)'),'rage uses two jumps then a full evasion recharge window')
  report['rage']=p.evaluate('()=>({states:rageStates,rest:rageRest,roll:BR_COOL,somersault:SS_COOL})');shot(p,'hammer-rage-recovery')
  p.evaluate('()=>{B.dead=true;B.dying=0;B._hammer.deathFx1002=null;}')
  for n in range(7):
   frames(p,48,'hammerBossDeathTick(B,1/60);drawWorld(1/60);');shot(p,'hammer-death-'+str(n))
  check(p.evaluate('()=>B._hammer.deathEvents1002.includes("hammer-core")&&B._hammer.deathEvents1002.includes("scream")&&B._hammer.deathEvents1002.filter(s=>s.startsWith("ring")).length===5'),'unique Hammer death event sequence')
  check(not errors,'no page or console errors');b.close()
finally:
 stop();report['errors']=errors;(O/'verification.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
sys.exit(0 if report['checks'] and all(c['ok'] for c in report['checks']) and not errors else 1)
