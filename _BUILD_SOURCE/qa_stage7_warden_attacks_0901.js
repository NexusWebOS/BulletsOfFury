/* Production-browser proof for the scaled Toxic Portal Warden attack-art pass. */
const http=require('http'),fs=require('fs'),path=require('path');let playwright;
try{playwright=require('playwright');}catch(_){playwright=require(path.join(process.env.USERPROFILE,'.cache','codex-runtimes','codex-primary-runtime','dependencies','node','node_modules','playwright'));}
const {chromium}=playwright,ROOT=path.resolve(__dirname,'..'),OUT=path.join(ROOT,'docs','proofs','stage7_warden_attacks_0901');
fs.mkdirSync(OUT,{recursive:true});
const MIME={'.html':'text/html','.js':'text/javascript','.css':'text/css','.png':'image/png','.jpg':'image/jpeg','.json':'application/json'};
const server=http.createServer((req,res)=>{const rel=decodeURIComponent((req.url||'/').split('?')[0]).replace(/^\/+/, '')||'index.html',file=path.resolve(ROOT,rel);
  if(!file.startsWith(ROOT)){res.writeHead(403);res.end();return;}fs.readFile(file,(err,data)=>{if(err){res.writeHead(404);res.end();return;}
    res.writeHead(200,{'Content-Type':MIME[path.extname(file).toLowerCase()]||'application/octet-stream'});res.end(data);});});
(async()=>{
  await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
  const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe'});
  const context=await browser.newContext({viewport:{width:980,height:720},recordVideo:{dir:OUT,size:{width:980,height:720}}});
  const page=await context.newPage(),video=page.video(),errors=[],missing=[];
  page.on('pageerror',e=>errors.push(String(e)));page.on('console',m=>{if(m.type()==='error'&&!/^Failed to load resource:/.test(m.text()))errors.push(m.text());});
  page.on('response',r=>{if(r.status()>=400&&!/favicon\.ico/.test(r.url()))missing.push({status:r.status(),url:r.url()});});
  await page.goto(`http://127.0.0.1:${server.address().port}/index.html`,{waitUntil:'domcontentloaded',timeout:30000});
  await page.waitForFunction(()=>window.__bofFrames>10,null,{timeout:30000});await page.keyboard.press('Enter');
  await page.evaluate(()=>eval(`(function(){
    beginStage(7);setState(GS.PLAY);run.pilot=Math.max(0,PILOTS.findIndex(function(p){return p.key==='lizzie';}));
    player.reset();player.invuln=999;player.x=worldWidth()/2;player.y=485;snapCamToPlayer();stagePlan=[{t:9999,fn:function(){}}];
    waveIdx=0;stageTimer=0;mapScroll=levelScrollRange();enemies.length=0;eBullets.length=0;pBullets.length=0;aiQueue.length=0;powerups.length=0;
    boss=null;bossActive=false;subBoss=null;subBossActive=false;story=null;spawnBoss('sludgeemperor');boss.enter=false;
    boss.x=worldWidth()/2;boss.y=178;boss.ty=178;s7WardenInit(boss);boss._s7warden.mt=-999;
  })()`));
  const assetKeys=['cfx_stage7_warden_walk','cfx_stage7_warden_cannon','cfx_stage7_warden_rail','cfx_stage7_warden_shell','cfx_stage7_warden_mine','cfx_stage7_warden_spear'];
  await page.waitForFunction(keys=>keys.every(k=>XART.rdy(k)),assetKeys,{timeout:20000});
  await page.evaluate(()=>eval(`(function(){boss.x=worldWidth()/2;boss._s7warden.mode='burst';boss._s7warden.mt=-999;boss._s7warden.travel=0;eBullets.length=0;})()`));
  const shot=async name=>page.locator('#screen').screenshot({path:path.join(OUT,name)});
  await page.waitForTimeout(180);await shot('01_scaled_lane_fit.png');
  async function attack(mode,mt,wait,name){
    await page.evaluate(({mode,mt})=>eval(`(function(){eBullets.length=0;_navalFlashes.length=0;boss.x=worldWidth()/2;s7WardenMode(boss,'${mode}');boss._s7warden.mt=${mt};})()`),{mode,mt});
    await page.waitForTimeout(wait);await shot(name);return page.evaluate(()=>eBullets.map(b=>b.kind));
  }
  const burst=await attack('burst',.45,760,'02_alternating_cannon_barrage.png');
  await attack('rail',.30,260,'03_reactor_rail_charge.png');
  const rail=await attack('rail',.82,360,'04_rift_rail_spear_volley.png');
  const mine=await attack('minefield',.68,1200,'05_portal_minefield.png');
  const state=await page.evaluate(keys=>({pilot:_pilotKey(),boss:boss.name,w:boss.w,h:boss.h,mode:boss._s7warden.mode,
    assets:keys.map(k=>({key:k,ready:XART.rdy(k)}))}),assetKeys);
  await context.close();const recorded=await video.path(),webm=path.join(OUT,'lizzie_toxic_portal_warden_attacks.webm');
  if(path.resolve(recorded)!==path.resolve(webm))fs.copyFileSync(recorded,webm);await browser.close();server.close();
  const report={state,projectileKinds:{burst:[...new Set(burst)],rail:[...new Set(rail)],mine:[...new Set(mine)]},errors,missing,
    recording:path.relative(ROOT,webm).replace(/\\/g,'/')};
  fs.writeFileSync(path.join(OUT,'report.json'),JSON.stringify(report,null,2));console.log(JSON.stringify(report,null,2));
  const ok=state.pilot==='lizzie'&&state.boss==='TOXIC PORTAL WARDEN'&&state.w===300&&state.h===230&&state.assets.every(a=>a.ready)&&
    burst.includes('s7wardenShell')&&rail.includes('s7wardenRail')&&mine.includes('s7wardenMine')&&!errors.length&&!missing.length;
  if(!ok)process.exitCode=1;
})().catch(e=>{console.error(e);server.close();process.exitCode=1;});
