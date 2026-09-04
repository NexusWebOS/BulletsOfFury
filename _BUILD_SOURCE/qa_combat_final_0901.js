/* Browser proof for the 0901 Stage 5-7 combat-final pass. Runs the production page and records
   three short Lizzie combat scenes; no test-only code is added to assets/game.js. */
const http=require('http');
const fs=require('fs');
const path=require('path');
let playwright;
try{playwright=require('playwright');}
catch(_){playwright=require(path.join(process.env.USERPROFILE,'.cache','codex-runtimes','codex-primary-runtime','dependencies','node','node_modules','playwright'));}
const {chromium}=playwright;

const ROOT=path.resolve(__dirname,'..');
const OUT=path.join(ROOT,'docs','proofs','combat_final_0901');
fs.mkdirSync(OUT,{recursive:true});
const MIME={'.html':'text/html','.js':'text/javascript','.css':'text/css','.png':'image/png','.jpg':'image/jpeg','.json':'application/json','.wav':'audio/wav','.mp3':'audio/mpeg'};
const server=http.createServer((req,res)=>{
  const rel=decodeURIComponent((req.url||'/').split('?')[0]).replace(/^\/+/, '')||'index.html';
  const file=path.resolve(ROOT,rel);if(!file.startsWith(ROOT)){res.writeHead(403);res.end();return;}
  fs.readFile(file,(err,data)=>{if(err){res.writeHead(404);res.end();return;}
    res.writeHead(200,{'Content-Type':MIME[path.extname(file).toLowerCase()]||'application/octet-stream'});res.end(data);});
});

(async()=>{
  await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
  const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',
    args:['--autoplay-policy=no-user-gesture-required']});
  const context=await browser.newContext({viewport:{width:980,height:720},recordVideo:{dir:OUT,size:{width:980,height:720}}});
  const page=await context.newPage(),video=page.video(),errors=[],missing=[];
  page.on('pageerror',e=>errors.push(String(e)));page.on('console',m=>{if(m.type()==='error'&&!/^Failed to load resource:/.test(m.text()))errors.push(m.text());});
  page.on('response',r=>{if(r.status()>=400&&!/favicon\.ico/.test(r.url()))missing.push({status:r.status(),url:r.url()});});
  await page.goto(`http://127.0.0.1:${server.address().port}/index.html`,{waitUntil:'domcontentloaded',timeout:30000});
  await page.waitForFunction(()=>window.__bofFrames>10,null,{timeout:30000});
  await page.keyboard.press('Enter');

  async function clear(stage){
    await page.evaluate(stage=>eval(`(function(){
      beginStage(${stage});setState(GS.PLAY);run.pilot=Math.max(0,PILOTS.findIndex(function(p){return p.key==='lizzie';}));
      player.reset();player.invuln=999;player.x=worldWidth()/2;player.y=430;snapCamToPlayer();
      stagePlan=[{t:9999,fn:function(){}}];waveIdx=0;stageTimer=0;mapScroll=levelScrollRange();
      enemies.length=0;eBullets.length=0;pBullets.length=0;aiQueue.length=0;powerups.length=0;
      boss=null;bossActive=false;subBoss=null;subBossActive=false;story=null;s5run=null;
    })()`),stage);
    await page.waitForTimeout(120);
  }
  async function shot(name){await page.locator('#screen').screenshot({path:path.join(OUT,name)});}

  /* Stage 5: Mike's eight-node route plus the animated Xeno carrier language. */
  await clear(5);
  await page.evaluate(()=>eval(`(function(){
    s5RunInit();s5run.armed=true;s5run.idx=2;s5run.t=3.4;
    for(var i=0;i<s5run.gates.length;i++){s5run.gates[i].y=-170+i*118;s5run.gates[i].py=s5run.gates[i].y-2;}
    spawnBoss('xenoregent');boss.enter=false;boss.x=worldWidth()/2;boss.y=125;boss.ty=125;boss.fireCd=.08;
    if(boss._xenoRig)boss._xenoRig.fireBeat=0;
  })()`));
  for(let i=0;i<18;i++)await page.waitForTimeout(80);
  await shot('01_stage5_warp_route_and_xeno_carrier.png');

  /* Stage 6: standing field, reflected-warhead break, then exposed bay-window damage. */
  await clear(6);
  await page.evaluate(()=>eval(`(function(){
    spawnBoss('doomsdaycarriermk2');boss.enter=false;boss.x=worldWidth()/2;boss.y=150;boss.ty=150;carrierInit(boss);boss.fireCd=999;
    boss._bayShield.hp=1;boss._lc.cd=999;
  })()`));
  await page.waitForTimeout(900);await shot('02_stage6_carrier_energy_shield.png');
  const shieldResult=await page.evaluate(()=>eval(`(function(){
    var q={x:boss.x,y:boss.y+boss.h*.64,vx:0,vy:-4,ang:-Math.PI/2,spd:4,w:34,h:76,t:0,kind:'omegawarhead',
      _ref:true,_carrierWarhead:true,_drawW:68,_drawH:108,_boss:true,_noArsenal:true};eBullets.push(q);
    return {before:boss._bayShield.hp};
  })()`));
  await page.waitForTimeout(500);await shot('03_stage6_reflected_break_and_window.png');
  const bayResult=await page.evaluate(()=>eval(`(function(){
    var box=carrierBayBox(boss,'L'),x=(box.x0+box.x1)/2,y=(box.y0+box.y1)/2,before=boss._bay.L;
    carrierPlayerHit(boss,115,x,y);return {before:before,after:boss._bay.L,shieldUp:boss._bayShield.up,window:boss._bayShield.window};
  })()`));
  await page.waitForTimeout(350);await shot('04_stage6_exposed_bay_damage.png');

  /* Stage 7: planted gait, authored teleport and post-arrival toxic attack language. */
  await clear(7);
  await page.evaluate(()=>eval(`(function(){
    spawnBoss('sludgeemperor');boss.enter=false;boss.x=worldWidth()*.30;boss.y=178;boss.ty=178;s7WardenInit(boss);s7WardenMode(boss,'teleport');
  })()`));
  await page.waitForTimeout(520);await shot('05_stage7_portal_warden_teleport.png');
  await page.waitForTimeout(1250);
  await page.evaluate(()=>eval(`(function(){s7WardenMode(boss,'minefield');boss._s7warden.mt=.75;})()`));
  await page.waitForTimeout(650);await shot('06_stage7_portal_warden_minefield.png');
  await page.evaluate(()=>eval(`(function(){s7WardenMode(boss,'burst');boss._s7warden.mt=.46;})()`));
  await page.waitForTimeout(1050);await shot('07_stage7_portal_warden_cannon_burst.png');

  const state=await page.evaluate(()=>eval(`(function(){return{
    pilot:_pilotKey(),stage:run.stage,boss:boss&&boss.name,warden:boss&&boss._s7warden?boss._s7warden.mode:null,
    stage5Route:S5R_ROUTE.slice(),stage6:{shield:!!(boss&&boss._bayShield)},
    assets:['cfx_stage5_xeno_projectiles','cfx_stage6_carrier_shield','cfx_stage7_warden_walk','cfx_stage7_warden_teleport','cfx_stage7_warden_projectiles'].map(function(k){return{k:k,ready:XART.rdy(k)};})
  };})()`));
  await context.close();const recorded=await video.path();const webm=path.join(OUT,'lizzie_stage5_7_combat_final.webm');
  if(path.resolve(recorded)!==path.resolve(webm))fs.copyFileSync(recorded,webm);
  await browser.close();server.close();
  const report={state,shieldResult,bayResult,errors,missing,recording:path.relative(ROOT,webm).replace(/\\/g,'/')};
  fs.writeFileSync(path.join(OUT,'report.json'),JSON.stringify(report,null,2));console.log(JSON.stringify(report,null,2));
  const routeOk=JSON.stringify(state.stage5Route)===JSON.stringify([.28,.54,.76,.23,.54,.29,.69,.18]);
  const ok=state.pilot==='lizzie'&&state.boss==='TOXIC PORTAL WARDEN'&&routeOk&&shieldResult.before===1&&
    bayResult.after<bayResult.before&&bayResult.shieldUp===false&&!errors.length&&!missing.length;
  if(!ok)process.exitCode=1;
})().catch(e=>{console.error(e);server.close();process.exitCode=1;});
