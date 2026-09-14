/* Focused proof for game-wide life scaling and the cleaned Stage-9 runtime roster. */
const http=require('http');
const fs=require('fs');
const path=require('path');
let playwright;
try{playwright=require('playwright');}
catch(_){playwright=require(path.join(process.env.USERPROFILE,'.cache','codex-runtimes','codex-primary-runtime',
  'dependencies','node','node_modules','playwright'));}
const {chromium}=playwright;

const ROOT=path.resolve(__dirname,'..');
const OUT=path.join(ROOT,'docs','proofs','gamewide_scaling_stage9_0831');
fs.mkdirSync(OUT,{recursive:true});
const MIME={'.html':'text/html','.js':'text/javascript','.css':'text/css','.png':'image/png',
  '.jpg':'image/jpeg','.jpeg':'image/jpeg','.wav':'audio/wav','.mp3':'audio/mpeg','.json':'application/json'};
const server=http.createServer((req,res)=>{
  const rel=decodeURIComponent((req.url||'/').split('?')[0]).replace(/^\/+/, '')||'index.html';
  const file=path.resolve(ROOT,rel);
  if(!file.startsWith(ROOT)){res.writeHead(403);res.end();return;}
  fs.readFile(file,(err,data)=>{if(err){res.writeHead(404);res.end();return;}
    res.writeHead(200,{'Content-Type':MIME[path.extname(file).toLowerCase()]||'application/octet-stream'});
    res.end(data);
  });
});

(async()=>{
  await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
  const browser=await chromium.launch({headless:true,
    executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',
    args:['--autoplay-policy=no-user-gesture-required']});
  const page=await browser.newPage({viewport:{width:1100,height:820}});
  const errors=[];
  page.on('pageerror',error=>errors.push(String(error)));
  await page.goto(`http://127.0.0.1:${server.address().port}/index.html`,
    {waitUntil:'domcontentloaded',timeout:30000});
  await page.waitForFunction(()=>window.__bofFrames>12,null,{timeout:30000});
  await page.keyboard.press('Enter');

  const scaling=await page.evaluate(()=>eval(`(function(){
    var roster={};for(var key in ADAPTIVE_REINFORCEMENT_ROSTER)roster[key]=ADAPTIVE_REINFORCEMENT_ROSTER[key].slice();
    var stages=[];
    function weak(){
      run.wlevels=[0,0,0,0,0,0];run.spaceLevels=[0,0,0];run.wlevel=0;
      run.speedLevel=0;run.missileLevel=0;run.shield=0;
      run._lifeThreat=0;run._lifeCombatT=0;run._threatBuild=0;
    }
    function strong(){
      run.wlevels=[5,4,3,2,1,0];run.spaceLevels=[5,4,3];run.wlevel=5;
      run.speedLevel=4;run.missileLevel=4;run.shield=1;
      run._lifeThreat=0;run._lifeCombatT=100;run._threatBuild=0;
    }
    player.dead=false;player.invuln=99999;
    for(var stage=1;stage<=9;stage++){
      run.stage=stage;curStage=STAGES[stage-1];
      weak();var base=combatThreat(stage),baseHp=EHP(100),baseP=adaptiveSpawnPressure(stage);
      enemies.length=0;stageTimer=10;_adaptiveSpawnT=0;_adaptiveSpawnSeq=0;
      boss=null;bossActive=false;bossDefeated=false;subBoss=null;subBossActive=false;
      warnT=0;stageEnding=0;_waveGap=0;
      var baseSpawn=tryAdaptiveReinforcement(stage,{t:9999,fn:function(){}},0,stage===1?11:6);
      weak();strong();var hot=combatThreat(stage),hotHp=EHP(100),hotP=adaptiveSpawnPressure(stage);
      enemies.length=0;stageTimer=10;_adaptiveSpawnT=0;_adaptiveSpawnSeq=0;
      var hotSpawn=tryAdaptiveReinforcement(stage,{t:9999,fn:function(){}},0,stage===1?11:6);
      var spawned=enemies[0]||null;
      stages.push({stage:stage,base:{hp:base.hp,spawn:base.spawn,eHp:baseHp,pressure:baseP,
                    reinforcement:baseSpawn},
                   hot:{hp:hot.hp,spawn:hot.spawn,eHp:hotHp,pressure:hotP,
                    reinforcement:hotSpawn,type:spawned&&spawned.type,marked:!!(spawned&&spawned._adaptiveReinforcement)},
                   roster:roster[stage]||[]});
    }

    /* A real death clears the life meter and the reinforcement clock. */
    run.stage=4;curStage=STAGES[3];strong();run.shield=0;special=null;gravityMode=false;
    player.dead=false;player.invuln=0;run.lives=3;_adaptiveSpawnT=.1;_adaptiveSpawnSeq=9;
    playerHit();
    var death={dead:player.dead,lifeT:run._lifeCombatT,lifeThreat:run._lifeThreat,
               build:run._threatBuild,reinforcementT:_adaptiveSpawnT,reinforcementSeq:_adaptiveSpawnSeq};
    /* Even a retained/restored loadout cannot rebuild pressure during the death timer. */
    run.wlevels=[5,5,5,5,5,5];run.spaceLevels=[5,5,5];run._lifeThreat=0;run._threatBuild=0;
    var deadThreat=combatThreat(4);death.deadBuild=deadThreat.build;death.deadSurvived=deadThreat.survived;
    return {stages:stages,death:death};
  })()`));

  /* Render all cleaned live Stage-9 silhouettes together on the actual canvas. */
  await page.evaluate(()=>eval(`(function(){
    beginStage(9);setState(GS.PLAY);player.reset();player.invuln=999999;
    stagePlan=[{t:9999,fn:function(){}}];waveIdx=0;stageTimer=0;mapScroll=1200;
    enemies.length=0;eBullets.length=0;pBullets.length=0;powerups.length=0;
    boss=null;bossActive=false;subBoss=null;subBossActive=false;story=null;timeScale=0;
    var types=Object.keys(S9VOID),W=worldWidth();
    for(var i=0;i<types.length;i++){
      var e=spawnEnemy(types[i],W*(.14+(i%4)*.24),86+Math.floor(i/4)*145,{});
      e.x=W*(.14+(i%4)*.24);e.y=86+Math.floor(i/4)*145;e.enter=false;e.spin=0;e._stagger=999;
    }
  })()`));
  await page.waitForTimeout(500);
  await page.locator('#screen').screenshot({path:path.join(OUT,'stage9_clean_runtime_roster.png')});

  const spriteAudit=JSON.parse(fs.readFileSync(path.join(ROOT,'_BUILD_SOURCE','stage9_enemy_cleanup',
    'stage9_enemy_cleanup.json'),'utf8'));
  const report={scaling,spriteAudit,errors};
  fs.writeFileSync(path.join(OUT,'report.json'),JSON.stringify(report,null,2));
  console.log(JSON.stringify(report,null,2));

  const stageChecks=scaling.stages.every(row=>{
    if(row.stage===1)return !row.base.reinforcement&&!row.hot.reinforcement;
    return row.hot.hp>row.base.hp&&row.hot.eHp>row.base.eHp&&row.hot.spawn>row.base.spawn&&
      !row.base.reinforcement&&row.hot.reinforcement&&row.hot.marked&&row.roster.includes(row.hot.type);
  });
  const death=scaling.death;
  const ok=stageChecks&&death.dead&&death.lifeT===0&&death.lifeThreat===0&&death.build===0&&
    death.reinforcementT===6.5&&death.reinforcementSeq===0&&death.deadBuild===0&&death.deadSurvived===0&&
    spriteAudit.changed_frames===24&&spriteAudit.removed_pixels>0&&spriteAudit.added_pixels===0&&!errors.length;
  await browser.close();server.close();if(!ok)process.exitCode=1;
})().catch(error=>{console.error(error);server.close();process.exitCode=1;});
