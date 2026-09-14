/* Focused live-browser proof for the eight-gate warp, Stage-9 pressure, meteors and space missiles. */
const http=require('http');
const fs=require('fs');
const path=require('path');
let playwright;
try{playwright=require('playwright');}
catch(_){playwright=require(path.join(process.env.USERPROFILE,'.cache','codex-runtimes','codex-primary-runtime',
  'dependencies','node','node_modules','playwright'));}
const {chromium}=playwright;
const ROOT=path.resolve(__dirname,'..');
const OUT=path.join(ROOT,'docs','proofs','warp_stage9_overhaul_0831');
fs.mkdirSync(OUT,{recursive:true});
const MIME={'.html':'text/html','.js':'text/javascript','.css':'text/css','.png':'image/png',
  '.jpg':'image/jpeg','.jpeg':'image/jpeg','.wav':'audio/wav','.mp3':'audio/mpeg','.json':'application/json'};
const server=http.createServer((req,res)=>{
  const rel=decodeURIComponent((req.url||'/').split('?')[0]).replace(/^\/+/, '')||'index.html';
  const file=path.resolve(ROOT,rel);
  if(!file.startsWith(ROOT)){res.writeHead(403);res.end();return;}
  fs.readFile(file,(err,data)=>{if(err){res.writeHead(404);res.end();return;}
    res.writeHead(200,{'Content-Type':MIME[path.extname(file).toLowerCase()]||'application/octet-stream'});res.end(data);
  });
});

(async()=>{
  await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
  const browser=await chromium.launch({headless:true,
    executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',
    args:['--autoplay-policy=no-user-gesture-required']});
  const page=await browser.newPage({viewport:{width:1100,height:820}}),errors=[];
  page.on('pageerror',e=>errors.push(String(e)));
  await page.goto(`http://127.0.0.1:${server.address().port}/index.html`,{waitUntil:'domcontentloaded',timeout:30000});
  await page.waitForFunction(()=>window.__bofFrames>12,null,{timeout:30000});
  await page.keyboard.press('Enter');
  await page.evaluate(()=>{for(let i=0;i<16;i++)XART._touch('nfx_warp_tunnel_'+i);for(let i=0;i<8;i++)XART._touch('nfx_s5gate96_'+i);});
  await page.waitForFunction(()=>XART.rdy('nfx_warp_tunnel_0')&&XART.rdy('nfx_s5gate96_0'),null,{timeout:30000});

  const gate=await page.evaluate(()=>eval(`(function(){
    beginStage(5);setState(GS.PLAY);run._s9taken=0;run._s9warp=0;player.reset();player.dead=false;player.invuln=99999;
    player.y=VH*.72;enemies.length=0;eBullets.length=0;pBullets.length=0;s5RunInit();
    var frames=[];
    for(var i=0;i<S5R_N;i++){
      var g=s5run.gates[i];player.x=g.x;g.y=player.y-1;
      for(var j=i+1;j<S5R_N;j++)s5run.gates[j].y=-2000-j*100;
      s5RunTick(.02);frames.push(warpForcedRollFrame());
      if(i<S5R_N-1){s5RunTick(.08);frames.push(warpForcedRollFrame());}
    }
    return {count:S5R_N,idx:s5run.idx,armed:s5run.armed,done:s5run.done,taken:run._s9taken,
      warp:run._s9warp,speed:s5run.rollSpeed,mix:s5run.warpMix,frames:frames};
  })()`));

  await page.evaluate(()=>eval(`(function(){
    beginStage(5);setState(GS.PLAY);player.reset();player.x=worldWidth()/2;player.y=VH*.70;
    s9warp={ph:'draw',t:.62,x:player.x,y:player.y,rollPhase:2.2,rollSpeed:3.05};
  })()`));
  await page.waitForTimeout(100);
  await page.locator('#screen').screenshot({path:path.join(OUT,'warp_fullscreen_live.png')});

  const stage9=await page.evaluate(()=>eval(`(function(){
    s9warp=null;beginStage(9);setState(GS.PLAY);player.reset();player.invuln=99999;
    gravityModeRetain();spaceModeStage(9);stagePlan=buildStagePlan(9);
    var roles=[];for(var i=0;i<stagePlan.length;i++){var s=String(stagePlan[i].fn);for(var r of ['kamikaze','jumper','slider','spinner','beam','orb','laser'])if(s.indexOf(r)>=0&&roles.indexOf(r)<0)roles.push(r);}
    enemies.length=0;eBullets.length=0;pBullets.length=0;powerups.length=0;
    var a=spawnS9Meteor(worldWidth()*.38,150,4.5,95,40),b=spawnS9Meteor(worldWidth()*.62,150,4.0,-95,40);
    var before=[a._mvx,b._mvx];for(var q=0;q<16;q++){s9MeteorTick(a,.04);s9MeteorTick(b,.04);}
    var after=[a._mvx,b._mvx],bombs=run.bombs;run.spaceLevels[2]=3;var launched=spaceUseMissile();
    var seed=pBullets.find(function(x){return x.kind==='spaceVolleySeed';});if(seed)spaceBulletTick(seed,.11);
    return {plan:stagePlan.length,roles:roles,meteorScales:[a._meteorScale,b._meteorScale],
      meteorBodies:[a.w,b.w],before:before,after:after,launched:launched,bombsBefore:bombs,bombsAfter:run.bombs,
      volley:pBullets.filter(function(x){return x.kind==='spaceVolley';}).length};
  })()`));
  await page.waitForTimeout(120);
  await page.locator('#screen').screenshot({path:path.join(OUT,'stage9_giant_meteors_live.png')});

  const report={gate,stage9,errors};
  fs.writeFileSync(path.join(OUT,'report.json'),JSON.stringify(report,null,2));console.log(JSON.stringify(report,null,2));
  const frameChanged=new Set(gate.frames).size>2;
  const ok=gate.count===8&&gate.idx===8&&gate.armed&&gate.done&&gate.taken&&gate.warp&&gate.speed>2.7&&gate.mix>.85&&frameChanged&&
    stage9.plan>=28&&['kamikaze','jumper','slider','spinner','beam','orb','laser'].every(r=>stage9.roles.includes(r))&&
    stage9.meteorScales.every(s=>s>=3&&s<=5)&&stage9.meteorBodies.every(s=>s>=132)&&
    stage9.launched&&stage9.bombsAfter===stage9.bombsBefore-1&&stage9.volley===3&&!errors.length;
  await browser.close();server.close();if(!ok)process.exitCode=1;
})().catch(e=>{console.error(e);server.close();process.exitCode=1;});
