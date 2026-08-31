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

  /* Held laser audio must use the native loop and advance while a real beam entity is alive. */
  await clear(1);
  await page.evaluate(()=>eval(`(function(){
    run.pilot='axel';run.weapon=3;run.wlevels[3]=2;run.wlevel=2;
    if(Snd&&Snd.loopPrepare)Snd.loopPrepare('laserBeamLoop');
    pShoot();
    /* Reproduce a held trigger, whose .11s cadence continually refreshes the single beam. */
    window.__qaLaserHold=setInterval(function(){pShoot();},80);
  })()`));
  await page.waitForTimeout(650);
  const laserAudio=await page.evaluate(()=>{const L=Snd&&Snd.loops&&Snd.loops.laserBeamLoop;
    if(window.__qaLaserHold){clearInterval(window.__qaLaserHold);window.__qaLaserHold=null;}
    return L?{paused:L.el.paused,currentTime:L.el.currentTime,readyState:L.el.readyState,on:L.on,volume:L.el.volume}:null;});

  const report={audit,rollLive,rollGap,cannon,giant,laserAudio,errors};
  fs.writeFileSync(path.join(OUT,'report.json'),JSON.stringify(report,null,2));
  console.log(JSON.stringify(report,null,2));
  const ok=audit.hot.hp>audit.base.hp&&audit.hot.spawn>audit.base.spawn&&
    Math.abs(audit.reset.hp-audit.base.hp)<.0001&&audit.pickupLevel===2&&
    Math.abs(audit.lizzieCadence-.06875)<.00001&&Math.abs(audit.lizzieSpeed-7.875)<.00001&&audit.laserNative&&
    rollLive.flameOn&&Math.abs(rollLive.y-rollLive.station)<1&&
    !rollGap.flameOn&&Math.abs(rollGap.y-rollGap.station)<1&&
    cannon.slots&&cannon.slots[0]==='L'&&cannon.width===44&&
    giant&&giant.w===68&&giant.h===68&&giant.spin&&!giant.shootable&&
    laserAudio&&laserAudio.readyState>=2&&laserAudio.on&&!errors.length;
  await browser.close();server.close();if(!ok)process.exitCode=1;
})().catch(e=>{console.error(e);server.close();process.exitCode=1;});
