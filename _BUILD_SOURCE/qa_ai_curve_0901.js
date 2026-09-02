/* Browser proof for the 2026-09-01 enemy-AI and campaign pressure pass. */
const http=require('http');
const fs=require('fs');
const path=require('path');
let playwright;
try{playwright=require('playwright');}
catch(_){playwright=require(path.join(process.env.USERPROFILE,'.cache','codex-runtimes','codex-primary-runtime',
  'dependencies','node','node_modules','playwright'));}
const {chromium}=playwright;

const ROOT=path.resolve(__dirname,'..');
const OUT=path.join(ROOT,'docs','proofs','ai_curve_0901');
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
  await page.keyboard.press('Enter');

  async function clear(stage){
    await page.evaluate(stage=>eval(`(function(){
      beginStage(${stage});setState(GS.PLAY);player.reset();player.invuln=99999;player.x=240;player.y=438;
      stagePlan=[{t:9999,fn:function(){}}];waveIdx=0;stageTimer=0;mapScroll=levelScrollRange();snapCamToPlayer();
      enemies.length=0;eBullets.length=0;pBullets.length=0;aiQueue.length=0;powerups.length=0;
      boss=null;bossActive=false;subBoss=null;subBossActive=false;story=null;warnT=0;stageEnding=false;
      run._threatBuild=0;run._lifeThreat=0;run._lifeCombatT=0;
    })()`),stage);
  }

  await clear(1);
  await page.evaluate(()=>eval(`(function(){
    var xs=[76,188,292,404];
    for(var i=0;i<xs.length;i++){
      var e=spawnEnemy(i===2?'s1jetbomber':'s1jetdelta',xs[i],44,{route:'straight',_s1Rush:true,_s1Wave:901,_s1LeadRank:i});
      e.y=44;e._s1DelayFrames=i*2;e._stagger=0;
    }
  })()`));
  await page.waitForTimeout(1500);
  const jets=await page.evaluate(()=>{
    const a=enemies.filter(e=>e._s1Wave===901&&!e.dead).map(e=>({x:e.x,y:e.y,rank:e._s1LeadRank,
      phase:e._s1RunPhase,target:e._s1RunTarget,bank:e.spin||0,wing:e._s1Wing})).sort((x,y)=>x.x-y.x);
    let min=999;for(let i=1;i<a.length;i++)min=Math.min(min,a[i].x-a[i-1].x);
    const active=a.filter(e=>e.target!=null),orderedTargets=[-1,1].every(side=>{
      const g=active.filter(e=>e.wing===side).sort((p,q)=>p.x-q.x);
      return g.every((e,i)=>!i||e.target>=g[i-1].target);
    });
    return {units:a,minSpacing:min,shots:eBullets.length,phases:[...new Set(a.map(e=>e.phase))],
      committed:a.filter(e=>e.target!=null).length,orderedTargets};
  });
  await page.locator('#screen').screenshot({path:path.join(OUT,'01_stage1_bracket_attack_run.png')});

  await clear(1);
  await page.evaluate(()=>XART.rdy('nef_s1_jungle_tank_intact'));
  await page.waitForFunction(()=>XART.rdy('nef_s1_jungle_tank_intact'),null,{timeout:10000});
  const tanks=await page.evaluate(()=>eval(`(function(){
    mapScroll=1200;var e=spawnEnemy('s1tankheavy',240,124,{_order:2,_atk:'cannon'});e.y=124;e._lvlY=null;_lastScrollDy=0;
    tankInit(e);e._shotCd=0;e._spd=22;e._phase='drive';e._phT=2;
    var before=eBullets.length;tankTick(e,1/60);
    var brake={shots:eBullets.length-before,phase:e._phase,queued:!!e._tankFireQueued,speed:e._spd};
    var firedAt=null;
    for(var i=0;i<180&&firedAt===null;i++){
      var n=eBullets.length;tankTick(e,1/60);if(eBullets.length>n)firedAt={frame:i,speed:e._spd,phase:e._phase};
    }
    return {brake:brake,firedAt:firedAt,kind:eBullets.length?eBullets[eBullets.length-1].kind:null,
      heading:e._tankPathDir,x:e.x,y:e.y,atk:e._atk,pattern:e.pattern,queueY:e._tankQueueY};
  })()`));
  await page.waitForTimeout(80);
  await page.locator('#screen').screenshot({path:path.join(OUT,'02_stage1_tank_brake_fire.png')});

  await clear(2);
  await page.evaluate(()=>eval(`(function(){
    encounterRipple([{type:'ash',fx:.31},{type:'ash',fx:.69}],.24);
    encounterRipple([
      {type:'cinderwasp',fx:.22,ai:{kind:'curve',dir:1,slowY:VH*.24}},
      {type:'cinderwasp',fx:.50,ai:{kind:'rush',slowY:VH*.32}},
      {type:'cinderwasp',fx:.78,ai:{kind:'curve',dir:-1,slowY:VH*.40}}
    ],.24);
  })()`));
  await page.waitForTimeout(1500);
  const volcano=await page.evaluate(()=>{
    const a=enemies.filter(e=>e._squadId&&!e.dead).map(e=>({type:e.type,x:e.x,y:e.y,squad:e._squadId,
      rank:e._squadRank,side:e._squadSide,ai:e._ai&&e._ai.kind,entry:e._ai&&e._ai.entry,bank:e._bank||0}));
    const wasps=a.filter(e=>e.type==='ash').sort((x,y)=>x.x-y.x);
    return {units:a,waspSpacing:wasps.length===2?wasps[1].x-wasps[0].x:null,shots:eBullets.length,
      support:adaptiveSpawnSlots(2,adaptiveSpawnPressure(2)),pressure:adaptiveSpawnPressure(2)};
  });
  await page.locator('#screen').screenshot({path:path.join(OUT,'03_stage2_squad_pressure.png')});

  const curve=await page.evaluate(()=>eval(`(function(){
    run._threatBuild=0;run._lifeThreat=0;run._lifeCombatT=0;
    var out=[];for(var s=1;s<=9;s++){var A=stageAiProfile(s),T=combatThreat(s);out.push({stage:s,move:A.move,
      formation:A.formation,waveGap:A.waveGap,cap:A.cap,fire:T.fire,bullet:T.bullet,bossRate:T.bossRate,spawn:T.spawn});}
    return out;
  })()`));
  const monotonic=curve.every((v,i)=>!i||(v.move>=curve[i-1].move&&v.formation>=curve[i-1].formation&&
    v.waveGap<=curve[i-1].waveGap&&(i===1||v.cap>=curve[i-1].cap)&&v.fire>=curve[i-1].fire&&
    v.bullet>=curve[i-1].bullet&&v.bossRate>=curve[i-1].bossRate));
  const report={jets,tanks,volcano,curve,monotonic,errors,missing:[...new Set(missing)]};
  fs.writeFileSync(path.join(OUT,'report.json'),JSON.stringify(report,null,2));
  console.log(JSON.stringify(report,null,2));
  const ok=jets.units.length===4&&jets.minSpacing>30&&jets.committed>=3&&jets.orderedTargets&&
    tanks.brake.shots===0&&tanks.brake.phase==='brake'&&tanks.brake.queued&&tanks.firedAt&&tanks.firedAt.speed<=1.8&&
    volcano.units.length>=5&&volcano.waspSpacing>60&&volcano.shots>0&&volcano.support===1&&
    monotonic&&!errors.length&&!missing.length;
  await browser.close();server.close();if(!ok)process.exitCode=1;
})().catch(e=>{console.error(e);server.close();process.exitCode=1;});
