/* Real-browser regression for the 2026-08-30 Stage 1 gameplay notes.
   Boots the shipped index, runs the live launch state, and samples the actual ship draw pose. */
const http = require('http');
const fs = require('fs');
const path = require('path');
let playwright;
try{ playwright=require('playwright'); }
catch(_){ playwright=require(path.join(process.env.USERPROFILE,'.cache','codex-runtimes','codex-primary-runtime',
  'dependencies','node','node_modules','playwright')); }
const { chromium } = playwright;

const ROOT = path.resolve(__dirname, '..');
const OUT = path.join(ROOT, 'docs', 'proofs', 'stage1_0830_fix');
fs.mkdirSync(OUT, { recursive: true });

const MIME = {'.html':'text/html','.js':'text/javascript','.css':'text/css','.png':'image/png',
  '.jpg':'image/jpeg','.jpeg':'image/jpeg','.mp3':'audio/mpeg','.wav':'audio/wav','.ttf':'font/ttf','.json':'application/json'};
const server = http.createServer((req,res)=>{
  const rel=decodeURIComponent((req.url||'/').split('?')[0]).replace(/^\/+/, '')||'index.html';
  const file=path.resolve(ROOT,rel);
  if(!file.startsWith(ROOT)){res.writeHead(403);res.end();return;}
  fs.readFile(file,(err,data)=>{if(err){res.writeHead(404);res.end();return;}
    res.writeHead(200,{'Content-Type':MIME[path.extname(file).toLowerCase()]||'application/octet-stream'});res.end(data);});
});

(async()=>{
  await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
  const port=server.address().port;
  const browser=await chromium.launch({headless:true,
    executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe'});
  const page=await browser.newPage({viewport:{width:1100,height:820}});
  const consoleErrors=[];
  page.on('pageerror',e=>consoleErrors.push(String(e)));
  await page.goto(`http://127.0.0.1:${port}/index.html`,{waitUntil:'domcontentloaded',timeout:30000});
  await page.waitForFunction(()=>window.__bofFrames>8,null,{timeout:30000});
  await page.evaluate(()=>eval(`
    window.__qaLastShip=null;
    window.__qaOriginalShip=drawShipSprite;
    drawShipSprite=function(x,y,h,s){
      if(state===GS.LAUNCH) window.__qaLastShip={x:x,y:y,h:h,phase:drawLaunch._phase,scroll:mapScroll,t:stateT};
      return window.__qaOriginalShip(x,y,h,s);
    };
    run.pilot='cole'; beginStage(1); setState(GS.LAUNCH); drawLaunch._phase=undefined;
  `));

  const samples=[]; let priorPhase='';
  for(let i=0;i<180;i++){
    await page.waitForTimeout(100);
    const q=await page.evaluate(()=>eval(`({state:state,phase:(drawLaunch._phase||''),ship:window.__qaLastShip,
      mapScroll:mapScroll,dist:(drawLaunch._dist||0)})`));
    if(q.ship) samples.push(q);
    if(q.phase!==priorPhase && q.phase){
      priorPhase=q.phase;
      await page.locator('#screen').screenshot({path:path.join(OUT,`launch_${q.phase}.png`)});
    }
    if(q.state==='play') break;
  }

  const ground=samples.filter(s=>s.ship&&['run','brake','settle','cd'].includes(s.phase));
  let reversals=0,maxDownStep=0;
  for(let i=1;i<ground.length;i++){
    const dy=ground[i].ship.y-ground[i-1].ship.y;
    if(dy>0.75){reversals++;maxDownStep=Math.max(maxDownStep,dy);}
  }
  const crawl=samples.filter(s=>s.phase==='settle'||s.phase==='cd');
  const crawlAdvance=crawl.length>1?crawl[crawl.length-1].mapScroll-crawl[0].mapScroll:0;

  const unit=await page.evaluate(()=>eval(`(function(){
    run.stage=1;
    const road=tankRoadOK; tankRoadOK=function(){return true;};
    const e={type:'s1tankheavy',pattern:'s1tank',x:173,y:90,w:47,h:64,t:0,dead:false};
    const xs=[]; for(let i=0;i<720;i++){tankMotionTick(e,1/60,TANK_SPD);xs.push(e.x);}
    tankRoadOK=road;
    const before=eBullets.length,b=eShootT(200,90,Math.PI/2,3.05,'s1jungleMissile',{});
    const navy=nefArtFor({_nef:'nef_s1_river_patrol_boat',type:'s1boatpatrol',pattern:'naval',hp:1,maxhp:100,_blk:false});
    return {tankMinX:Math.min.apply(null,xs),tankMaxX:Math.max.apply(null,xs),tankVx:e.vx,
      missileKind:b.kind,missileShootable:b._shootable,missileHp:b.hp,
      fixedBullet:FIRETYPES.s1bullet.art({t:9}),navyArt:navy,bulletCount:eBullets.length-before};
  })()`));

  const report={launch:{samples:ground.length,reversals,maxDownStep,crawlAdvance,
    reachedPlay:samples.some(s=>s.state==='play'),phases:[...new Set(samples.map(s=>s.phase))]},unit,consoleErrors};
  fs.writeFileSync(path.join(OUT,'report.json'),JSON.stringify(report,null,2));
  console.log(JSON.stringify(report,null,2));
  await browser.close();server.close();
  if(reversals||crawlAdvance<=0||!report.launch.reachedPlay||unit.tankMinX!==unit.tankMaxX||
     !unit.missileShootable||unit.missileHp!==1||unit.fixedBullet!=='mgcf_1_5'||
     unit.navyArt!=='nef_s1_river_patrol_boat_intact'||consoleErrors.length) process.exitCode=1;
})().catch(e=>{console.error(e);server.close();process.exitCode=1;});
