/* Real-browser proof for Mike's 2026-08-30 annotated Stage-1 wave map. */
const http=require('http');
const fs=require('fs');
const path=require('path');
let playwright;
try{playwright=require('playwright');}
catch(_){playwright=require(path.join(process.env.USERPROFILE,'.cache','codex-runtimes','codex-primary-runtime',
  'dependencies','node','node_modules','playwright'));}
const {chromium}=playwright;

const ROOT=path.resolve(__dirname,'..');
const OUT=path.join(ROOT,'docs','proofs','stage1_wave_map_0830');
fs.mkdirSync(OUT,{recursive:true});
const MIME={'.html':'text/html','.js':'text/javascript','.css':'text/css','.png':'image/png',
  '.jpg':'image/jpeg','.jpeg':'image/jpeg','.mp3':'audio/mpeg','.wav':'audio/wav','.ttf':'font/ttf','.json':'application/json'};
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
  const errors=[];
  page.on('pageerror',e=>errors.push(String(e)));
  await page.goto(`http://127.0.0.1:${server.address().port}/index.html`,
    {waitUntil:'domcontentloaded',timeout:30000});
  await page.waitForFunction(()=>window.__bofFrames>12,null,{timeout:30000});

  await page.evaluate(()=>eval(`
    run.pilot='cole'; beginStage(1); setState(GS.PLAY); player.reset(); player.invuln=999;
    window.__qaStage1Plan=buildStagePlan(1);
    window.__qaShowWave=function(i){
      run.stage=1;curStage=STAGES[0];state=GS.PLAY;stagePlan=[];waveIdx=0;
      enemies.length=0;eBullets.length=0;pBullets.length=0;playerLocks.length=0;
      subBoss=null;subBossActive=false;subBossTriggered=true;subBossDone=true;
      boss=null;bossActive=false;bossWarned=true;aminiTriggered=true;_sc1=_sc2=_mc1=_mc2=true;
      var w=window.__qaStage1Plan[i];mapScroll=w.fn._s1MapScroll||0;stageTimer=w.t;w.fn();
      player.x=worldWidth()/2;player.y=VH*.82;player.invuln=999;
      return enemies.map(function(e){return {type:e.type,x:e.x,y:e.y,w:e.w,h:e.h,
        bodyW:e._bodyW||e.w,bodyH:e._bodyH||e.h,unitSquare:e._unitSquare||0,
        wave:e._s1Wave||0,lead:e._s1LeadRank,kamikaze:!!e._s1Kamikaze};});
    };
  `));

  const shots=[
    {i:0,name:'01_water_left_boats'},
    {i:6,name:'02_coast_fast_jet_ripple'},
    {i:7,name:'03_land_tank_file'},
    {i:17,name:'04_dam_kamikaze_approach'}
  ];
  const shown={};
  const shownAfter={};
  for(const s of shots){
    shown[s.name]=await page.evaluate(i=>eval(`window.__qaShowWave(${i})`),s.i);
    await page.waitForTimeout(s.i===0?2200:(s.i===7?3000:(s.i===17?650:450)));
    shownAfter[s.name]=await page.evaluate(()=>eval(`enemies.map(function(e){return {type:e.type,
      x:e.x,y:e.y,w:e.w,h:e.h,bodyW:e._bodyW||e.w,bodyH:e._bodyH||e.h,
      unitSquare:e._unitSquare||0,dead:!!e.dead,beached:!!e._beached};})`));
    await page.locator('#screen').screenshot({path:path.join(OUT,s.name+'.png')});
  }

  /* Capture the actual dam rows reached by the new boss time, without spawning the boss fight. */
  const arena=await page.evaluate(()=>eval(`(function(){
    enemies.length=0;eBullets.length=0;stagePlan=[];waveIdx=0;bossWarned=true;
    mapScroll=STAGES[0].length*40;stageTimer=STAGES[0].length-1;
    return {scroll:mapScroll,sourceTop:(_levelCfg(1).h-VH)-mapScroll,length:STAGES[0].length};
  })()`));
  await page.waitForTimeout(250);
  await page.locator('#screen').screenshot({path:path.join(OUT,'05_dam_boss_arena.png')});

  const mechanics=JSON.parse(await page.evaluate(()=>eval(`(function(){
    var p=buildStagePlan(1),mapped=[];
    for(var i=0;i<p.length;i++){
      mapScroll=p[i].fn._s1MapScroll||0;enemies.length=0;p[i].fn();
      mapped.push(enemies.map(function(e){return {type:e.type,x:e.x,w:e._s1Wave||0,
        lead:e._s1LeadRank,k:!!e._s1Kamikaze};}));
    }
    var all=[].concat.apply([],mapped),water=[].concat.apply([],mapped.slice(0,6));
    var ripples={};all.filter(function(e){return e.w;}).forEach(function(e){
      (ripples[e.w]||(ripples[e.w]=[])).push({x:e.x,lead:e.lead});
    });
    var releases=[];mapScroll=p[6].fn._s1MapScroll;enemies.length=0;p[6].fn();
    var jets=enemies.slice(),y0=jets.map(function(e){return e.y;}),first=jets.map(function(){return -1;});
    for(var f=0;f<14;f++)for(var j=0;j<jets.length;j++){
      jetTick(jets[j],1/60);if(first[j]<0&&jets[j].y!==y0[j])first[j]=f;
    }
    mapScroll=p[7].fn._s1MapScroll;enemies.length=0;p[7].fn();
    var tanks=enemies.slice(),tx=tanks.map(function(e){return e.x;});
    for(var q=0;q<360;q++)for(var z=0;z<tanks.length;z++)tankTick(tanks[z],1/60);
    var tankDrift=tanks.reduce(function(m,e,i){return Math.max(m,Math.abs(e.x-tx[i]));},0);
    mapScroll=p[17].fn._s1MapScroll;enemies.length=0;p[17].fn();
    var k=enemies[0];k._s1DelayFrames=0;k._stagger=0;player.x=worldWidth()*.78;player.y=VH*.82;
    while(!k._kmLocked)jetTick(k,1/60);var a0=Math.atan2(k._kmVy,k._kmVx);
    player.x=worldWidth()*.12;for(var n=0;n<90;n++)jetTick(k,1/60);
    var a1=Math.atan2(k._kmVy,k._kmVx);
    return JSON.stringify({planCount:p.length,mapYs:p.map(function(w){return w.fn._s1MapY;}),
      waterTypes:water.map(function(e){return e.type;}),ripples:ripples,releases:first,
      tankDrift:tankDrift,kamikazes:all.filter(function(e){return e.k;}).length,
      kamikazeVectorDrift:Math.abs(a1-a0),subboss:SUBBOSS[1],stageLength:STAGES[0].length});
  })()`)));

  const report={shown,shownAfter,arena,mechanics,errors};
  const tankBoxes=shownAfter['03_land_tank_file'];
  let tankTouch=false;
  for(let a=0;a<tankBoxes.length;a++) for(let b=a+1;b<tankBoxes.length;b++){
    const A=tankBoxes[a],B=tankBoxes[b];
    if(Math.abs(A.x-B.x)<=(A.w+B.w)/2 && Math.abs(A.y-B.y)<=(A.h+B.h)/2) tankTouch=true;
  }
  report.tankFootprints={allSquare:tankBoxes.every(t=>t.w===t.h&&t.unitSquare===t.w),touching:tankTouch};
  fs.writeFileSync(path.join(OUT,'report.json'),JSON.stringify(report,null,2));
  console.log(JSON.stringify(report,null,2));
  const rippleKeys=Object.keys(mechanics.ripples);
  const leads=rippleKeys.slice(0,4).map(k=>mechanics.ripples[k].filter(e=>e.lead===0)[0].x);
  const ok=mechanics.planCount===19 && mechanics.waterTypes.length===10 &&
    mechanics.waterTypes.every(t=>/^s1boat|^s1corvette/.test(t)) && rippleKeys.length===5 &&
    new Set(leads).size===4 && mechanics.releases.join(',')==='0,2,5,7' &&
    mechanics.tankDrift<0.01 && report.tankFootprints.allSquare && !report.tankFootprints.touching &&
    mechanics.kamikazes===8 && mechanics.kamikazeVectorDrift<0.0001 &&
    mechanics.subboss.afterWaveTime===34 && arena.sourceTop>=360 && arena.sourceTop<=460 && !errors.length;
  await browser.close();server.close();
  if(!ok)process.exitCode=1;
})().catch(e=>{console.error(e);server.close();process.exitCode=1;});
