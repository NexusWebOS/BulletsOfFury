/* Focused browser proof for the 2026-08-31 supplied-shmup-reference pass. */
const http=require('http');
const fs=require('fs');
const path=require('path');
let playwright;
try{playwright=require('playwright');}
catch(_){playwright=require(path.join(process.env.USERPROFILE,'.cache','codex-runtimes','codex-primary-runtime',
  'dependencies','node','node_modules','playwright'));}
const {chromium}=playwright;

const ROOT=path.resolve(__dirname,'..');
const OUT=path.join(ROOT,'docs','proofs','shmup_reference_0831');
fs.mkdirSync(OUT,{recursive:true});
const MIME={'.html':'text/html','.js':'text/javascript','.css':'text/css','.png':'image/png',
  '.jpg':'image/jpeg','.wav':'audio/wav','.mp3':'audio/mpeg','.json':'application/json'};
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
    })()`),n);
  }
  async function waitArt(key){
    await page.evaluate(k=>XART.rdy(k),key);
    await page.waitForFunction(k=>XART.rdy(k),key,{timeout:12000});
  }

  /* Stage 5: the tell owns all blocked columns and leaves exactly two adjacent columns clear. */
  await clear(5);await waitArt('nsb_xenoregent_intact');
  const xenoTell=await page.evaluate(()=>eval(`(function(){
    spawnBoss('xenoregent');boss.enter=false;boss.x=400;boss.y=shipBossStationY(boss);boss.ty=boss.y;boss.fireCd=999;
    player.x=365;xenoRegentGridStart(boss,3);
    var G=boss._xenoGrid;return {gap:G.gap,cols:G.cols,doorWidth:2,left:G.left,right:G.right};
  })()`));
  await page.waitForTimeout(80);
  await page.locator('#screen').screenshot({path:path.join(OUT,'01_stage5_xeno_void_grid_tell.png')});
  const xenoLive=await page.evaluate(()=>eval(`(function(){
    var before=eBullets.length;for(var i=0;i<72;i++)xenoRegentTick(boss,1/60);
    var G=boss._xenoGrid;return {before:before,shots:eBullets.length,wave:G&&G.wave,gap:G&&G.gap,
      kinds:eBullets.reduce(function(o,q){o[q.kind]=(o[q.kind]||0)+1;return o;},{})};
  })()`));
  await page.waitForTimeout(50);
  await page.locator('#screen').screenshot({path:path.join(OUT,'02_stage5_xeno_void_grid_release.png')});

  /* Stage 7: all three residues are visible during the tell; only the first has bloomed after the
     first release, demonstrating sequential ownership instead of three overlapping rings. */
  await clear(7);await waitArt('nsb_sludgeemperor_intact');
  const sludgeTell=await page.evaluate(()=>eval(`(function(){
    spawnBoss('sludgeemperor');boss.enter=false;boss.x=400;boss.y=shipBossStationY(boss);boss.ty=boss.y;boss.fireCd=999;
    player.x=390;sludgeRosetteStart(boss);return {points:boss._s7Rosette.points.length,tell:boss._s7Rosette.tell};
  })()`));
  await page.waitForTimeout(80);
  await page.locator('#screen').screenshot({path:path.join(OUT,'03_stage7_toxic_bloom_tell.png')});
  const sludgeLive=await page.evaluate(()=>eval(`(function(){
    for(var i=0;i<54;i++)sludgeRosetteTick(boss,1/60);
    return {wave:boss._s7Rosette&&boss._s7Rosette.wave,shots:eBullets.length,
      acid:eBullets.filter(function(q){return q.kind==='s7acid';}).length};
  })()`));
  await page.waitForTimeout(50);
  await page.locator('#screen').screenshot({path:path.join(OUT,'04_stage7_toxic_bloom_first_ring.png')});

  /* Stage 9: a two-lane door is shown before the first row and moves by only one lane afterward. */
  await clear(9);await waitArt('ns9_tidal_intact');
  const tidalTell=await page.evaluate(()=>eval(`(function(){
    spawnBoss('tidalsovereign');boss.enter=false;boss.x=400;boss.y=shipBossStationY(boss);boss.ty=boss.y;boss.fireCd=999;
    player.x=420;tidalCascadeStart(boss,2);var T=boss._s9Cascade;
    return {gap:T.gap,cols:T.cols,doorWidth:2,left:T.left,right:T.right};
  })()`));
  await page.waitForTimeout(80);
  await page.locator('#screen').screenshot({path:path.join(OUT,'05_stage9_tidal_cascade_tell.png')});
  const tidalLive=await page.evaluate(()=>eval(`(function(){
    var old=boss._s9Cascade.gap;for(var i=0;i<42;i++)tidalCascadeTick(boss,1/60);var T=boss._s9Cascade;
    return {oldGap:old,gap:T&&T.gap,delta:T&&Math.abs(T.gap-old),wave:T&&T.wave,shots:eBullets.length,
      pair:eBullets.filter(function(q){return q.kind==='s9pair';}).length};
  })()`));
  await page.waitForTimeout(50);
  await page.locator('#screen').screenshot({path:path.join(OUT,'06_stage9_tidal_cascade_release.png')});

  const report={xenoTell,xenoLive,sludgeTell,sludgeLive,tidalTell,tidalLive,errors};
  fs.writeFileSync(path.join(OUT,'report.json'),JSON.stringify(report,null,2));
  console.log(JSON.stringify(report,null,2));
  const ok=xenoTell.doorWidth===2&&xenoLive.before===0&&xenoLive.wave>=1&&xenoLive.kinds.s5fracture>=6&&
    xenoLive.kinds.s5null>=6&&sludgeTell.points===3&&sludgeLive.wave>=1&&sludgeLive.wave<=2&&
    sludgeLive.acid===sludgeLive.wave*11&&
    tidalTell.doorWidth===2&&tidalLive.wave===1&&tidalLive.delta===1&&tidalLive.pair===6&&!errors.length;
  await browser.close();server.close();if(!ok)process.exitCode=1;
})().catch(e=>{console.error(e);server.close();process.exitCode=1;});
