/* Focused live-browser QA for the 0902 Gravity Mode weapon contract:
   - Volley Missiles are passive auto-fire, never a selectable primary.
   - Missile pickups upgrade the passive without replacing Laser/Shadow.
   - A death resets every ground and space weapon bank to level 1. */
const http=require('http');
const fs=require('fs');
const path=require('path');
let playwright;
try{playwright=require('playwright');}
catch(_){playwright=require(path.join(process.env.USERPROFILE,'.cache','codex-runtimes','codex-primary-runtime',
  'dependencies','node','node_modules','playwright'));}
const {chromium}=playwright;

const ROOT=path.resolve(__dirname,'..');
const OUT=path.join(ROOT,'docs','proofs','space_passive_death_0902');
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
  const errors=[],missing=[];
  page.on('pageerror',e=>errors.push(String(e)));
  page.on('response',r=>{if(r.status()===404)missing.push(r.url());});
  await page.goto(`http://127.0.0.1:${server.address().port}/index.html`,
    {waitUntil:'domcontentloaded',timeout:30000});
  await page.waitForFunction(()=>window.__bofFrames>12,null,{timeout:30000});
  /* XART.rdy intentionally returns false on the first touch. Poll the actual Gravity atlas before
     the screenshot so the proof cannot mistake lazy-loading black frames for gameplay. */
  await page.evaluate(()=>eval("spaceAtlasCanvas('ship_base','axel')"));
  await page.waitForFunction(()=>eval("!!spaceAtlasCanvas('ship_base','axel')"),null,{timeout:30000});

  const pickup=await page.evaluate(()=>eval(`(function(){
    run.stage=5;run.spaceMode=true;run.spaceWeapon=0;run.spaceLevels=[4,3,1];
    player.dead=false;player.invuln=999;special=null;
    applyPowerup({kind:'weapon',wtype:2,x:player.x,y:player.y});
    return {active:run.spaceWeapon,primary:spaceWeaponName(),primaryLevel:spaceWeaponLevel(),
      passiveLevel:spaceVolleyLevel(),levels:run.spaceLevels.slice(),primaryIcon:spaceWeaponIconKey(),
      passiveIcon:spaceVolleyIconKey()};
  })()`));

  const automatic=await page.evaluate(()=>eval(`(function(){
    run.stage=5;run.spaceMode=true;run.spaceWeapon=0;run.spaceLevels=[2,1,5];run._spaceVolleyCd=0;
    player.dead=false;special=null;pBullets.length=0;stageStats.missiles=0;
    var first=spaceVolleyAutoTick(1/60,true),afterFirst=pBullets.filter(function(b){return b.kind==='spaceVolleySeed';}).length;
    var blocked=spaceVolleyAutoTick(1/60,true),afterBlocked=pBullets.filter(function(b){return b.kind==='spaceVolleySeed';}).length;
    spaceVolleyAutoTick(1,false);
    var second=spaceVolleyAutoTick(1/60,true),afterSecond=pBullets.filter(function(b){return b.kind==='spaceVolleySeed';}).length;
    pBullets.length=0;spaceVolleyFire();
    return {first:first,blocked:blocked,second:second,afterFirst:afterFirst,afterBlocked:afterBlocked,
      afterSecond:afterSecond,defaultVolleyTier:pBullets[0]&&pBullets[0].lv,stats:stageStats.missiles};
  })()`));

  const migration=await page.evaluate(()=>eval(`(function(){
    run.stage=5;run.spaceMode=true;run.spaceWeapon=2;run.spaceLevels=[1,1,4];spaceModeStage(5);
    return {active:run.spaceWeapon,name:spaceWeaponName(),icon:spaceWeaponIconKey(),passive:spaceVolleyLevel()};
  })()`));

  const groundDeath=await page.evaluate(()=>eval(`(function(){
    run.stage=3;run.spaceMode=false;run._groundLoadout=null;run.weapon=4;
    run.wlevels=[5,4,3,2,5,4];run.wlevel=5;run.wvars=[null,null,null,null,'flamethrower','fireorb'];
    run.missileLevel=5;run.shield=0;special=null;player.dead=false;player.alive=true;player.invuln=0;
    playerHit();return {weapon:run.weapon,wlevel:run.wlevel,wlevels:run.wlevels.slice(),
      missileLevel:run.missileLevel,variant:run.wvars[4],dead:player.dead};
  })()`));

  const spaceDeath=await page.evaluate(()=>eval(`(function(){
    run.stage=5;run.spaceMode=true;run.spaceWeapon=1;run.spaceLevels=[5,4,5];run._spaceVolleyCd=.2;
    run._groundLoadout={weapon:4,wlevel:5,wlevels:[5,4,3,2,5,4],wvars:[null,null,null,null,'flamethrower','fireorb'],missileLevel:5};
    run.weapon=0;run.wlevels=[0,0,0,0,0,0];run.wvars=[null,null,null,null,null,null];run.wlevel=4;
    run.missileLevel=0;run.shield=0;special=null;player.dead=false;player.alive=true;player.invuln=0;
    playerHit();return {active:run.spaceWeapon,spaceLevels:run.spaceLevels.slice(),missileLevel:run.missileLevel,
      groundWeapon:run._groundLoadout.weapon,groundLevel:run._groundLoadout.wlevel,
      groundLevels:run._groundLoadout.wlevels.slice(),groundMissile:run._groundLoadout.missileLevel,
      volleyCooldown:run._spaceVolleyCd,dead:player.dead};
  })()`));

  /* Visual proof: one Laser Cannon burst plus the separately spawned level-V passive volley. */
  await page.evaluate(()=>eval(`(function(){
    run.stage=5;curStage=STAGES[4];setState(GS.PLAY);gravityMode={phase:'active',t:0,age:0,retained:true};
    player.reset();player.dead=false;player.invuln=0;player.x=VW/2;player.y=VH-64;
    run.spaceMode=true;run.gravityShipReady=true;run.spaceWeapon=0;run.spaceLevels=[3,1,5];run._spaceVolleyCd=0;
    _arcBan=null;stagePlan=[{t:9999,fn:function(){}}];waveIdx=0;stageTimer=0;stageEnding=false;story=null;
    enemies.length=0;eBullets.length=0;pBullets.length=0;powerups.length=0;explosions.length=0;
    particles.length=0;pImpacts.length=0;sprAnims.length=0;fadeOuts.length=0;boss=null;bossActive=false;
    spaceVolleyAutoTick(1/60,true);
    for(var f=0;f<30;f++){var list=pBullets.slice();for(var i=0;i<list.length;i++)spaceBulletTick(list[i],1/60);}
    pBullets=pBullets.filter(function(b){return !b.dead;});
    spaceLaserFire();
    for(var lf=0;lf<5;lf++){var lasers=pBullets.filter(function(b){return b.kind==='spaceLaser';});
      for(var li=0;li<lasers.length;li++)spaceBulletTick(lasers[li],1/60);}
  })()`));
  await page.waitForTimeout(60);
  await page.locator('#screen').screenshot({path:path.join(OUT,'01_laser_plus_passive_volley.png')});

  const report={pickup,automatic,migration,groundDeath,spaceDeath,missing,errors};
  fs.writeFileSync(path.join(OUT,'report.json'),JSON.stringify(report,null,2));
  const assert=(v,m)=>{if(!v)throw new Error(m);};
  assert(pickup.active===0&&pickup.primary==='LASER CANNON'&&pickup.primaryLevel===4,
    'Passive pickup replaced or altered the selected primary: '+JSON.stringify(pickup));
  assert(pickup.passiveLevel===2&&pickup.levels.join()==='4,3,2',
    'Passive pickup did not level only Volley Missiles: '+JSON.stringify(pickup));
  assert(automatic.first&&!automatic.blocked&&automatic.second&&automatic.afterFirst===1&&
    automatic.afterBlocked===1&&automatic.afterSecond===2&&automatic.defaultVolleyTier===5&&automatic.stats===2,
    'Passive cadence/level contract failed: '+JSON.stringify(automatic));
  assert(migration.active===0&&migration.name==='LASER CANNON'&&migration.passive===4,
    'Legacy selectable-Volley state was not migrated: '+JSON.stringify(migration));
  assert(groundDeath.weapon===4&&groundDeath.wlevel===1&&groundDeath.wlevels.every(v=>v===1)&&
    groundDeath.missileLevel===1&&groundDeath.variant==='flamethrower'&&groundDeath.dead,
    'Ground death did not preserve type/variant and reset every tier to 1: '+JSON.stringify(groundDeath));
  assert(spaceDeath.active===1&&spaceDeath.spaceLevels.every(v=>v===1)&&spaceDeath.missileLevel===1&&
    spaceDeath.groundWeapon===4&&spaceDeath.groundLevel===1&&spaceDeath.groundLevels.every(v=>v===1)&&
    spaceDeath.groundMissile===1&&spaceDeath.volleyCooldown===0&&spaceDeath.dead,
    'Space death did not reset both live and stored loadouts to 1: '+JSON.stringify(spaceDeath));
  assert(missing.length===0,'Missing assets: '+missing.join(', '));
  assert(errors.length===0,'Page errors: '+errors.join(' | '));
  console.log(JSON.stringify(report,null,2));
  await browser.close();server.close();
})().catch(err=>{console.error(err);server.close();process.exit(1);});
