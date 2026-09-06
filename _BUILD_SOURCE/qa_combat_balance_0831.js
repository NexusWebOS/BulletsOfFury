/* Focused browser proof for the 2026-08-31 combat/balance/audio correction pass. */
const http=require('http');
const fs=require('fs');
const path=require('path');
let playwright;
try{playwright=require('playwright');}
catch(_){playwright=require(path.join(process.env.USERPROFILE,'.cache','codex-runtimes','codex-primary-runtime',
  'dependencies','node','node_modules','playwright'));}
const {chromium}=playwright;

const ROOT=path.resolve(__dirname,'..');
const OUT=path.join(ROOT,'docs','proofs','combat_balance_0831');
fs.mkdirSync(OUT,{recursive:true});
const MIME={'.html':'text/html','.js':'text/javascript','.css':'text/css','.png':'image/png',
  '.jpg':'image/jpeg','.jpeg':'image/jpeg','.wav':'audio/wav','.mp3':'audio/mpeg','.json':'application/json'};
const server=http.createServer((req,res)=>{
  const rel=decodeURIComponent((req.url||'/').split('?')[0]).replace(/^\/+/, '')||'index.html';
  const file=path.resolve(ROOT,rel);
  if(!file.startsWith(ROOT)){res.writeHead(403);res.end();return;}
  fs.readFile(file,(err,data)=>{if(err){res.writeHead(404);res.end();return;}
    res.writeHead(200,{'Content-Type':MIME[path.extname(file).toLowerCase()]||'application/octet-stream'});res.end(data);});
});

(async()=>{
  await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
  const browser=await chromium.launch({headless:true,
    executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',
    args:['--autoplay-policy=no-user-gesture-required']});
  const page=await browser.newPage({viewport:{width:1100,height:820}});
  const errors=[];page.on('pageerror',e=>errors.push(String(e)));
  await page.goto(`http://127.0.0.1:${server.address().port}/index.html`,
    {waitUntil:'domcontentloaded',timeout:30000});
  await page.waitForFunction(()=>window.__bofFrames>12,null,{timeout:30000});
  await page.keyboard.press('Enter');

  async function clear(n){
    await page.evaluate(n=>eval(`(function(){
      beginStage(${n});setState(GS.PLAY);player.reset();player.invuln=99999;player.x=240;player.y=438;
      stagePlan=[{t:9999,fn:function(){}}];waveIdx=0;stageTimer=0;mapScroll=levelScrollRange();snapCamToPlayer();
      enemies.length=0;eBullets.length=0;pBullets.length=0;aiQueue.length=0;powerups.length=0;
      boss=null;bossActive=false;subBoss=null;subBossActive=false;story=null;
      if(typeof thaw!=='undefined')thaw=null;
    })()`),n);
  }

  /* Balance/data audit first, while no live encounter can mutate the sampled values. */
  const audit=await page.evaluate(()=>eval(`(function(){
    run.spaceLevels=[0,0,0];run.wlevels=[0,0,0,0,0,0];run._threatBuild=0;run._lifeThreat=0;run._lifeCombatT=0;
    var base=combatThreat(1);
    run.wlevels=[5,4,3,2,1,0];run.speedLevel=4;run.missileLevel=4;run._lifeCombatT=100;
    var hot=combatThreat(1);
    run.wlevels=[0,0,0,0,0,0];run.speedLevel=0;run.missileLevel=0;run._lifeThreat=0;run._lifeCombatT=0;run._threatBuild=0;
    var reset=combatThreat(1);
    var iconCalls=[],oldKey=weaponIconKey;
    weaponIconKey=function(w,l,o){iconCalls.push({w:w,l:l});return oldKey(w,l,o);};
    run.wlevels=[1,1,1,1,1,1];run.weapon=1;powerups=[{kind:'weapon',wtype:1,wvar:null,x:240,y:230,w:24,h:24,t:.2,dead:false}];
    drawPowerups();weaponIconKey=oldKey;
    return {base:base,hot:hot,reset:reset,pickupLevel:iconCalls.length?iconCalls[0].l:null,
      lizzieCadence:LZ_SLUG_CD,lizzieSpeed:LZ_SLUG_SPD,
      laserNative:!!(Snd&&Snd.TAME&&Snd.TAME.laserBeamLoop&&Snd.TAME.laserBeamLoop.native)};
  })()`));

  /* Stage 2 weather pressure must stop before the main boss, and both authored fire-boss rails
     must advance continuously rather than jumping between firing stations. */
  await clear(2);
  const firewaveGate=await page.evaluate(()=>eval(`(function(){
    wfxReset();wfx.fireCd=0;bossActive=false;warnKind=null;wfxUpdate(.10);
    var stagePressure=!!wfx.fseq;
    bossActive=true;wfxUpdate(.10);
    return {stagePressure:stagePressure,bossSequence:!!wfx.fseq,bossWave:!!wfx.fire,cooldown:wfx.fireCd};
  })()`));
  const level2Slide=await page.evaluate(()=>eval(`(function(){
    spawnBoss('infernoreaver');boss.enter=false;boss.x=240;boss.y=shipBossStationY(boss);boss.ty=boss.y;
    infernoReaverPassStart(boss,1);boss.x=boss._irPass.startX;boss._irPass.phase='pass';boss._irPass.t=0;
    var last=boss.x,maxStep=0,minX=boss.x,maxX=boss.x;
    for(var i=0;i<270;i++){
      infernoReaverPassTick(boss,1/60);maxStep=Math.max(maxStep,Math.abs(boss.x-last));last=boss.x;
      minX=Math.min(minX,boss.x);maxX=Math.max(maxX,boss.x);
    }
    return {maxStep:maxStep,travel:maxX-minX,phase:boss._irPass&&boss._irPass.phase};
  })()`));

  /* Level 2: boss stays on station; capture a live half-turn and its off-beat. */
  await clear(2);
  await page.evaluate(()=>{for(let i=0;i<12;i++)XART.rdy('mwfx_flamethrower_'+i);});
  await page.waitForFunction(()=>{for(let i=0;i<12;i++)if(XART.rdy('mwfx_flamethrower_'+i))return true;return false;},null,{timeout:10000});
  await page.evaluate(()=>eval(`(function(){
    spawnBoss('infernoreaver');boss.enter=false;boss.x=130;boss.y=112;boss.ty=112;boss.fireCd=999;
    infernoReaverRollStart(boss,1);boss._irRoll.phase='roll';boss._irRoll.t=.26;
  })()`));
  await page.waitForTimeout(90);
  const rollLive=await page.evaluate(()=>({y:boss.y,station:boss._irRoll.sy,flameOn:boss._irRoll.flameOn,
    angle:boss._irRoll.flameAng,phase:boss._irRoll.phase}));
  await page.locator('#screen').screenshot({path:path.join(OUT,'01_level2_bounded_180_flame.png')});
  await page.evaluate(()=>{boss._irRoll.t=.68;boss._irRoll._flameWasOn=true;});
  await page.waitForTimeout(40);
  const rollGap=await page.evaluate(()=>({y:boss.y,station:boss._irRoll.sy,flameOn:boss._irRoll.flameOn,
    phase:boss._irRoll.phase}));
  await page.locator('#screen').screenshot({path:path.join(OUT,'02_level2_flame_recovery_gap.png')});

  /* Level 3: alternate physical cannon, crisp reactor charge, then the oversized rigid orb. */
  await clear(3);
  await page.evaluate(()=>eval(`(function(){
    spawnBoss('cryospear');boss.enter=false;boss.x=240;boss.y=118;boss.ty=118;boss.fireCd=999;
    boss._s3boss={role:'wall'};
    var L=shipBossMount(boss,'L');l23BossBeamStart(boss,'rime',['L'],[aimPlayer(L.x,L.y)],.08,.62,.16,44);
    boss._l23Beam.t=.18;boss._l23Beam.released=true;boss._s3boss.cannonGlow={slot:'L',t:.40};
  })()`));
  await page.waitForTimeout(80);
  const cannon=await page.evaluate(()=>({slots:boss._l23Beam&&boss._l23Beam.slots.slice(),width:boss._l23Beam&&boss._l23Beam.width}));
  await page.locator('#screen').screenshot({path:path.join(OUT,'03_level3_left_cannon_laser.png')});

  await clear(3);
  await page.evaluate(()=>eval(`(function(){
    spawnBoss('cryospear');boss.enter=false;boss.x=240;boss.y=118;boss.ty=118;boss.fireCd=999;
    boss._s3boss.charge={t:.72,dur:1.12,slot:'C',kind:'giantOrb',released:false};
  })()`));
  await page.waitForTimeout(60);
  await page.locator('#screen').screenshot({path:path.join(OUT,'04_level3_internal_pixel_charge.png')});

  await page.evaluate(()=>eval(`(function(){
    var p=shipBossMount(boss,'C'),q=stage3BossShot(boss,'C',Math.PI/2,1.38,'s3mortar',{w:68,h:68,silent:true});
    q._s3Giant=true;q._s3StaticSpin=true;q._shootable=false;q.hp=undefined;q.x=p.x;q.y=p.y+88;
  })()`));
  await page.waitForTimeout(80);
  const giant=await page.evaluate(()=>{const q=eBullets.find(x=>x._s3Giant);return q&&{w:q.w,h:q.h,spin:q._s3StaticSpin,shootable:q._shootable};});
  await page.locator('#screen').screenshot({path:path.join(OUT,'05_level3_giant_ice_lightning_orb.png')});

  /* Stage 3: the promoted mini and boss now carry deliberate multi-layer patterns and cross the
     screen on readable rails.  Sample the director itself so a future art swap cannot hide a
     movement teleport or silently remove half the ammunition. */
  await clear(3);
  const level3Mini=await page.evaluate(()=>eval(`(function(){
    spawnSubBoss('rimewall');subBoss.enter=false;subBoss.x=126;subBoss.y=shipBossStationY(subBoss);subBoss.ty=subBoss.y;
    var minHp=subBoss.maxhp;stage3BossBeginSlide(subBoss,4.55);
    var last=subBoss.x,maxStep=0,minX=subBoss.x,maxX=subBoss.x;
    for(var i=0;i<273;i++){stage3BossSlideTick(subBoss,1/60);maxStep=Math.max(maxStep,Math.abs(subBoss.x-last));last=subBoss.x;minX=Math.min(minX,subBoss.x);maxX=Math.max(maxX,subBoss.x);}
    eBullets.length=0;subBoss._s3boss.slide=null;stage3BossAttack(subBoss,'s3spearcross',0,0,1);
    for(var j=0;j<132;j++)stage3BossTick(subBoss,1/60);
    return {hp:minHp,maxStep:maxStep,travel:maxX-minX,shots:subBoss._s3boss.shots,kinds:Object.assign({},subBoss._s3boss.kinds)};
  })()`));
  await page.waitForTimeout(40);
  await page.locator('#screen').screenshot({path:path.join(OUT,'06_level3_cryospear_crossweave.png')});

  await clear(3);
  const level3Boss=await page.evaluate(()=>eval(`(function(){
    spawnBoss('cryospear');boss.enter=false;boss.x=240;boss.y=shipBossStationY(boss);boss.ty=boss.y;boss.fireCd=999;
    var bossHp=boss.maxhp;eBullets.length=0;stage3BossAttack(boss,'s3wallhalo',0,0,1);
    for(var i=0;i<168;i++)stage3BossTick(boss,1/60);
    var giant=eBullets.filter(function(q){return !!q._s3Giant;}).length;
    return {hp:bossHp,shots:boss._s3boss.shots,kinds:Object.assign({},boss._s3boss.kinds),giant:giant,
      slideDuration:boss._s3boss.slide&&boss._s3boss.slide.dur};
  })()`));
  await page.waitForTimeout(40);
  await page.locator('#screen').screenshot({path:path.join(OUT,'07_level3_rimewall_halo.png')});

  /* Live sample playback: confirm the exact boss-family cues decode, advance and use their
     throttled mix gains.  This catches the common 'call succeeds but the element is silent'
     regression without changing or normalising the approved recordings. */
  await page.evaluate(()=>eval(`(function(){
    var names=['enemyMachineGunHeavy','enemyHeavyLaser','bossWeaponCharge','shieldHitHeavy','shieldBreakCombat'];
    Snd.prepare(names);for(var n of names){delete Snd._last[n];Snd.pools[n].i=0;}
  })()`));
  await page.waitForFunction(()=>eval(`(function(){
    var names=['enemyMachineGunHeavy','enemyHeavyLaser','bossWeaponCharge','shieldHitHeavy','shieldBreakCombat'];
    return names.every(function(n){var p=Snd&&Snd.pools&&Snd.pools[n];return p&&p.list.every(function(a){return a.readyState>=2;});});
  })()`),null,{timeout:15000});
  await page.evaluate(()=>eval(`(function(){
    Audio.resume();
    var names=['enemyMachineGunHeavy','enemyHeavyLaser','bossWeaponCharge','shieldHitHeavy','shieldBreakCombat'];
    window.__qaBossAudioRoute={};
    for(var n of names){
      var p=Snd.pools[n],idx=p.i,handle=Audio.SFX[n];
      if(handle)handle();
      window.__qaBossAudioRoute[n]={handle:typeof handle==='function',before:idx,after:p.i,
        immediate:{paused:p.list[idx].paused,currentTime:p.list[idx].currentTime,readyState:p.list[idx].readyState,volume:p.list[idx].volume}};
    }
  })()`));
  /* The real WAV elements deliberately retry after lazy decode. Give that retry window time to
     finish; sampling at 180ms caught the expected HAVE_METADATA dip and falsely read silence. */
  await page.waitForTimeout(850);
  const bossAudio=await page.evaluate(()=>{
    const names=['enemyMachineGunHeavy','enemyHeavyLaser','bossWeaponCharge','shieldHitHeavy','shieldBreakCombat'];
    const out={};for(const n of names){const p=Snd&&Snd.pools&&Snd.pools[n],a=p&&p.list.find(x=>x.currentTime>0);
      out[n]=a?{currentTime:a.currentTime,readyState:a.readyState,paused:a.paused,volume:a.volume}:null;}
    return {route:window.__qaBossAudioRoute,playback:out};
  });

  /* Held laser audio must use the native loop and advance while a real beam entity is alive. */
  await clear(1);
  await page.evaluate(()=>{Snd.loopPrepare('laserBeamLoop');});
  await page.waitForFunction(()=>{const L=Snd&&Snd.loops&&Snd.loops.laserBeamLoop;return L&&L.el.readyState>=2;},null,{timeout:15000});
  await page.evaluate(()=>eval(`(function(){
    run.pilot='axel';run.weapon=3;run.wlevels[3]=2;run.wlevel=2;
    pShoot();
    /* Reproduce a held trigger, whose .11s cadence continually refreshes the single beam. */
    window.__qaLaserHold=setInterval(function(){pShoot();},80);
  })()`));
  await page.waitForTimeout(650);
  const laserAudio=await page.evaluate(()=>{const L=Snd&&Snd.loops&&Snd.loops.laserBeamLoop;
    if(window.__qaLaserHold){clearInterval(window.__qaLaserHold);window.__qaLaserHold=null;}
    return L?{paused:L.el.paused,currentTime:L.el.currentTime,readyState:L.el.readyState,on:L.on,volume:L.el.volume}:null;});

  const report={audit,firewaveGate,level2Slide,rollLive,rollGap,cannon,giant,level3Mini,level3Boss,bossAudio,laserAudio,errors};
  fs.writeFileSync(path.join(OUT,'report.json'),JSON.stringify(report,null,2));
  console.log(JSON.stringify(report,null,2));
  const ok=audit.hot.hp>audit.base.hp&&audit.hot.spawn>audit.base.spawn&&
    Math.abs(audit.reset.hp-audit.base.hp)<.0001&&audit.pickupLevel===2&&
    Math.abs(audit.lizzieCadence-.075625)<.00001&&Math.abs(audit.lizzieSpeed-7.875)<.00001&&audit.laserNative&&
    firewaveGate.stagePressure&&!firewaveGate.bossSequence&&!firewaveGate.bossWave&&firewaveGate.cooldown>=999&&
    level2Slide.maxStep<2&&level2Slide.travel>220&&
    rollLive.flameOn&&Math.abs(rollLive.y-rollLive.station)<1&&
    !rollGap.flameOn&&Math.abs(rollGap.y-rollGap.station)<1&&
    cannon.slots&&cannon.slots[0]==='L'&&cannon.width===44&&
    giant&&giant.w===68&&giant.h===68&&giant.spin&&!giant.shootable&&
    level3Mini.hp>=1250&&level3Mini.maxStep<2&&level3Mini.travel>220&&level3Mini.shots>=19&&
    level3Mini.kinds.s3lance>=18&&level3Mini.kinds.s3mortar>=1&&
    level3Boss.hp>=1800&&level3Boss.shots>=35&&level3Boss.giant===1&&level3Boss.slideDuration>=4.3&&
    Object.values(bossAudio.route).every(a=>a.handle&&a.after!==a.before&&a.immediate.readyState>=1&&a.immediate.volume<=.69)&&
    Object.values(bossAudio.playback).every(a=>a&&a.readyState>=2&&a.currentTime>0&&a.volume<=.69)&&
    laserAudio&&laserAudio.readyState>=2&&laserAudio.on&&!errors.length;
  await browser.close();server.close();if(!ok)process.exitCode=1;
})().catch(e=>{console.error(e);server.close();process.exitCode=1;});
