/* Focused real-browser regression proof for the 2026-08-30 Stage 3/4 corrections. */
const http=require('http');
const fs=require('fs');
const path=require('path');
let playwright;
try{playwright=require('playwright');}
catch(_){playwright=require(path.join(process.env.USERPROFILE,'.cache','codex-runtimes','codex-primary-runtime',
  'dependencies','node','node_modules','playwright'));}
const {chromium}=playwright;

const ROOT=path.resolve(__dirname,'..');
const OUT=path.join(ROOT,'docs','proofs','stage34_corrections_0830');
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
    executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe'});
  const page=await browser.newPage({viewport:{width:1100,height:820}});
  const errors=[];page.on('pageerror',e=>errors.push(String(e)));
  await page.goto(`http://127.0.0.1:${server.address().port}/index.html`,
    {waitUntil:'domcontentloaded',timeout:30000});
  await page.waitForFunction(()=>window.__bofFrames>12,null,{timeout:30000});
  /* The generated arsenal plates are lazy XART entries.  Wait for the two exact hulls used by
     the hit-flash proof so the audit tests their real custom renderers rather than the generic
     loading fallback. */
  await page.waitForFunction(()=>window.XART && XART.rdy('ndr_sharddart_idle_0') &&
    XART.rdy('nef_s3_elite_ice_interceptor_intact'),null,{timeout:30000});

  const audit=await page.evaluate(()=>eval(`(function(){
    run.pilot='cole';
    function quietStage(n){
      beginStage(n);setState(GS.PLAY);player.reset();player.invuln=99999;
      stagePlan=[{t:9999,fn:function(){}}];waveIdx=0;stageTimer=0;mapScroll=levelScrollRange();
      enemies.length=0;eBullets.length=0;pBullets.length=0;aiQueue.length=0;
      boss=null;bossActive=false;subBoss=null;subBossActive=false;story=null;
      if(typeof thaw!=='undefined')thaw=null;
    }
    quietStage(3);
    var types=[];
    var plan=buildStagePlan(3),originalSpawn=spawnEnemy;
    spawnEnemy=function(type,x,y,opt){types.push(type);return originalSpawn(type,x,y,opt||{});};
    for(var wi=0;wi<plan.length;wi++){
      plan[wi].fn();for(var q=0;q<400;q++)aiQueueTick(1/120);
    }
    spawnEnemy=originalSpawn;
    var volcanic=types.filter(function(t){return ['cinderwasp','basaltbomber','magmaorb','ash','skim','lavamaw'].indexOf(t)>=0;});

    quietStage(3);
    var dr=spawnEnemy('sharddart',240,150,{}),nativeIce=spawnEnemy('s3interceptor',360,150,{});
    dr.flash=.12;nativeIce.flash=.12;
    var oldTint=xartTint,tintKeys=[];
    xartTint=function(k,c,s){tintKeys.push(k);return oldTint(k,c,s);};
    drawEnemy(dr);drawEnemy(nativeIce);xartTint=oldTint;

    quietStage(3);spawnBoss('cryospear');boss.enter=false;boss.x=240;boss.y=128;boss.ty=128;
    var orb=stage3BossShot(boss,'C',Math.PI/2,2.5,'s3mortar',{shootable:true,hp:4});
    var orbAudit={staticSpin:orb._s3StaticSpin===true,shootable:orb._shootable===true,hp:orb.hp,
      frame0:('l23fx_'+orb._l23fx+'_0'),family:orb._l23fx};

    quietStage(4);
    var barrel=spawnEnemy('s4barrel',205,210,{}),bx=barrel.x,by=barrel.y;
    for(var i=0;i<180;i++)s4ChaseTick(barrel,1/120);
    var barrelAudit={x0:bx,x1:barrel.x,y0:by,y1:barrel.y,spin:barrel.spin,vx:barrel.vx,vy:barrel.vy};

    quietStage(4);spawnBoss('stormsovereign');boss.enter=false;boss.x=240;boss.y=135;boss.ty=135;
    var hpAudit={mul:SHIPBOSS.stormsovereign.hpMul,maxhp:boss.maxhp};
    eBullets.length=0;stormMgStart(boss);for(var j=0;j<20;j++)stormMgTick(boss,.04);
    var mg=eBullets.filter(function(b){return b._stormMg;});
    _shipShot(240,180,2.4,1.1,10,boss);var general=eBullets[eBullets.length-1];
    var bulletAudit={mgCount:mg.length,mgStraight:mg.every(function(b){return Math.abs(b.vx)<.0001&&b.vy>0;}),
      generalStraight:Math.abs(general.vx)<.0001&&general.vy>0};
    return {types:Array.from(new Set(types)),volcanic:volcanic,tintKeys:tintKeys,
      orb:orbAudit,barrel:barrelAudit,hp:hpAudit,bullets:bulletAudit};
  })()`));

  async function clear(n){await page.evaluate(n=>eval(`(function(){
    beginStage(${n});setState(GS.PLAY);player.reset();player.invuln=99999;player.x=240;player.y=438;
    stagePlan=[{t:9999,fn:function(){}}];waveIdx=0;stageTimer=0;mapScroll=levelScrollRange();snapCamToPlayer();
    enemies.length=0;eBullets.length=0;pBullets.length=0;aiQueue.length=0;
    boss=null;bossActive=false;subBoss=null;subBossActive=false;story=null;
    if(typeof thaw!=='undefined')thaw=null;
  })()`),n);}

  await clear(3);
  await page.evaluate(()=>eval(`(function(){
    var a=spawnEnemy('sharddart',205,150,{}),b=spawnEnemy('s3interceptor',330,150,{});
    a.hp=Math.max(2,a.hp-2);b.hp=Math.max(2,b.hp-2);
    window.__qaHit=setInterval(function(){if(a&&!a.dead)a.flash=.12;if(b&&!b.dead)b.flash=.12;},16);
  })()`));
  await page.waitForTimeout(700);
  await page.locator('#screen').screenshot({path:path.join(OUT,'01_stage3_ice_hit_flash.png')});
  await page.evaluate(()=>clearInterval(window.__qaHit));

  await clear(3);
  await page.evaluate(()=>eval(`(function(){
    spawnBoss('cryospear');boss.enter=false;boss.x=240;boss.y=118;boss.ty=118;boss.fireCd=999;
    for(var i=-2;i<=2;i++)stage3BossShot(boss,'C',Math.PI/2+i*.12,2.15,'s3mortar',{shootable:true,hp:4});
  })()`));
  await page.waitForTimeout(850);
  await page.locator('#screen').screenshot({path:path.join(OUT,'02_stage3_static_spinning_orbs.png')});

  await clear(4);
  await page.evaluate(()=>eval(`(function(){
    var e=spawnEnemy('s4barrel',240,215,{});e._lane=240;e.spin=0;e._fcd=999;
  })()`));
  await page.waitForTimeout(500);
  await page.locator('#screen').screenshot({path:path.join(OUT,'03_stage4_fixed_barrel.png')});

  await clear(4);
  await page.evaluate(()=>eval(`(function(){
    spawnBoss('stormsovereign');boss.enter=false;boss.x=240;boss.y=130;boss.ty=130;boss.fireCd=999;
    stormMgStart(boss);stormMgTick(boss,.40);
    for(var k=0;k<5;k++)_shipShot(160+k*40,245,0,3.35,10,boss);
  })()`));
  await page.waitForTimeout(520);
  await page.locator('#screen').screenshot({path:path.join(OUT,'04_stage4_forward_bullet_columns.png')});

  const report={audit,errors};
  fs.writeFileSync(path.join(OUT,'report.json'),JSON.stringify(report,null,2));
  console.log(JSON.stringify(report,null,2));
  const ok=!audit.volcanic.length && audit.tintKeys.some(k=>k.indexOf('ndr_sharddart')===0) &&
    audit.tintKeys.some(k=>k.indexOf('nef_s3_elite_ice_interceptor')===0) && audit.orb.staticSpin &&
    !audit.orb.shootable && audit.orb.hp==null && Math.abs(audit.barrel.x1-audit.barrel.x0)<.001 &&
    audit.barrel.spin===0 && audit.barrel.vx===0 && audit.barrel.vy===0 &&
    audit.hp.mul===1.05 && audit.bullets.mgCount===12 && audit.bullets.mgStraight &&
    audit.bullets.generalStraight && !errors.length;
  await browser.close();server.close();if(!ok)process.exitCode=1;
})().catch(e=>{console.error(e);server.close();process.exitCode=1;});
