/* Production-browser proof for the Toxic Portal Warden's articulated crawl. The test keeps the
   boss in patrol long enough to cross the arena, records Lizzie underneath it, and samples the
   actual runtime gait state instead of inferring animation from elapsed time. */
const http=require('http');
const fs=require('fs');
const path=require('path');
let playwright;
try{playwright=require('playwright');}
catch(_){playwright=require(path.join(process.env.USERPROFILE,'.cache','codex-runtimes','codex-primary-runtime','dependencies','node','node_modules','playwright'));}
const {chromium}=playwright;
const ROOT=path.resolve(__dirname,'..'),OUT=path.join(ROOT,'docs','proofs','stage7_warden_crawl_0901');
fs.mkdirSync(OUT,{recursive:true});
const MIME={'.html':'text/html','.js':'text/javascript','.css':'text/css','.png':'image/png','.jpg':'image/jpeg','.json':'application/json'};
const server=http.createServer((req,res)=>{
  const rel=decodeURIComponent((req.url||'/').split('?')[0]).replace(/^\/+/, '')||'index.html';
  const file=path.resolve(ROOT,rel);if(!file.startsWith(ROOT)){res.writeHead(403);res.end();return;}
  fs.readFile(file,(err,data)=>{if(err){res.writeHead(404);res.end();return;}
    res.writeHead(200,{'Content-Type':MIME[path.extname(file).toLowerCase()]||'application/octet-stream'});res.end(data);});
});

(async()=>{
  await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
  const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe'});
  const context=await browser.newContext({viewport:{width:980,height:720},recordVideo:{dir:OUT,size:{width:980,height:720}}});
  const page=await context.newPage(),video=page.video(),errors=[],missing=[];
  page.on('pageerror',e=>errors.push(String(e)));
  page.on('console',m=>{if(m.type()==='error'&&!/^Failed to load resource:/.test(m.text()))errors.push(m.text());});
  page.on('response',r=>{if(r.status()>=400&&!/favicon\.ico/.test(r.url()))missing.push({status:r.status(),url:r.url()});});
  await page.goto(`http://127.0.0.1:${server.address().port}/index.html`,{waitUntil:'domcontentloaded',timeout:30000});
  await page.waitForFunction(()=>window.__bofFrames>10,null,{timeout:30000});await page.keyboard.press('Enter');
  const bounds=await page.evaluate(()=>eval(`(function(){
    beginStage(7);setState(GS.PLAY);run.pilot=Math.max(0,PILOTS.findIndex(function(p){return p.key==='lizzie';}));
    player.reset();player.invuln=999;player.x=worldWidth()/2;player.y=470;snapCamToPlayer();
    stagePlan=[{t:9999,fn:function(){}}];waveIdx=0;stageTimer=0;mapScroll=levelScrollRange();
    enemies.length=0;eBullets.length=0;pBullets.length=0;aiQueue.length=0;powerups.length=0;
    boss=null;bossActive=false;subBoss=null;subBossActive=false;story=null;
    spawnBoss('sludgeemperor');boss.enter=false;boss.y=178;boss.ty=178;s7WardenInit(boss);
    var S=boss._s7warden,left=camLeftX()+boss.w*.26,right=camRightX()-boss.w*.26;
    boss.x=right;S.mode='patrol';S.mt=-999;S.targetX=left;S.dir=-1;S.crawlClock=0;S.crawlPhase=0;S.plants=0;
    return {left:left,right:right};
  })()`));
  await page.waitForFunction(()=>XART.rdy('cfx_stage7_warden_walk'),null,{timeout:15000});
  await page.evaluate(()=>eval(`(function(){
    var S=boss._s7warden;boss.x=camRightX()-boss.w*.26;S.targetX=camLeftX()+boss.w*.26;S.dir=-1;
    S.crawlClock=0;S.crawlPhase=0;S.crawlFrame=7;S.plants=0;S.plantedLeg=null;_navalFlashes.length=0;
  })()`));
  const samples=[];
  await page.waitForTimeout(200);await page.locator('#screen').screenshot({path:path.join(OUT,'01_crawl_start.png')});
  for(let i=0;i<60;i++){
    await page.waitForTimeout(100);
    samples.push(await page.evaluate(()=>({x:boss.x,frame:boss._s7warden.crawlFrame,phase:boss._s7warden.crawlPhase,
      plants:boss._s7warden.plants||0,leg:boss._s7warden.plantedLeg,drop:boss._s7warden.bodyDrop})));
    if(i===28)await page.locator('#screen').screenshot({path:path.join(OUT,'02_crawl_mid_stride.png')});
  }
  await page.locator('#screen').screenshot({path:path.join(OUT,'03_crawl_opposite_edge.png')});
  const state=await page.evaluate(()=>({pilot:_pilotKey(),boss:boss.name,mode:boss._s7warden.mode,
    plants:boss._s7warden.plants,asset:XART.rdy('cfx_stage7_warden_walk')}));
  await context.close();const recorded=await video.path(),webm=path.join(OUT,'lizzie_toxic_portal_warden_crawl.webm');
  if(path.resolve(recorded)!==path.resolve(webm))fs.copyFileSync(recorded,webm);
  await browser.close();server.close();
  const xs=samples.map(s=>s.x),frames=[...new Set(samples.map(s=>s.frame))].sort((a,b)=>a-b),
    phases=[...new Set(samples.map(s=>s.phase))].sort((a,b)=>a-b);
  const report={state,bounds,distance:Math.max(...xs)-Math.min(...xs),frames,phases,
    plantOrder:samples.filter((s,i)=>i===0||s.plants!==samples[i-1].plants).map(s=>s.leg),errors,missing,
    recording:path.relative(ROOT,webm).replace(/\\/g,'/')};
  fs.writeFileSync(path.join(OUT,'report.json'),JSON.stringify(report,null,2));console.log(JSON.stringify(report,null,2));
  const ok=state.pilot==='lizzie'&&state.boss==='TOXIC PORTAL WARDEN'&&state.mode==='patrol'&&state.asset&&
    report.distance>250&&frames.length===8&&phases.length===8&&state.plants>=20&&!errors.length&&!missing.length;
  if(!ok)process.exitCode=1;
})().catch(e=>{console.error(e);server.close();process.exitCode=1;});
