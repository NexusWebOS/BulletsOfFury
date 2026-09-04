/* Stage 5 Xeno Regent fairness + bounded stage-resource loading browser proof. */
const http=require('http');
const fs=require('fs');
const path=require('path');
let playwright;
try{playwright=require('playwright');}
catch(_){playwright=require(path.join(process.env.USERPROFILE,'.cache','codex-runtimes','codex-primary-runtime',
  'dependencies','node','node_modules','playwright'));}
const {chromium}=playwright;

const ROOT=path.resolve(__dirname,'..');
const OUT=path.join(ROOT,'docs','proofs','stage5_boss_loading_0901');
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
  const errors=[],missing=[],stageRequests=[];
  page.on('pageerror',e=>errors.push(String(e)));
  page.on('response',r=>{
    if(r.status()===404)missing.push(r.url());
    if(/stage5_|combat_final|xeno|fracture|chaos_harrier/.test(r.url()))stageRequests.push({url:r.url(),at:Date.now()});
  });
  await page.goto(`http://127.0.0.1:${server.address().port}/index.html`,
    {waitUntil:'domcontentloaded',timeout:30000});
  await page.waitForFunction(()=>window.__bofFrames>12,null,{timeout:30000});
  await page.keyboard.press('Enter');

  const start=Date.now();
  await page.evaluate(()=>beginStage(5));
  const initial=await page.evaluate(()=>stageLoadInfo(5));
  let maxInflight=0;
  while(!(await page.evaluate(()=>stageLoadReady(5)))&&Date.now()-start<60000){
    maxInflight=Math.max(maxInflight,await page.evaluate(()=>_stageLoads[5].inflight.length));
    await page.waitForTimeout(25);
  }
  const loaded=await page.evaluate(()=>stageLoadInfo(5));
  if(!loaded.ready)throw new Error('Stage 5 loader did not finish in 60 seconds: '+JSON.stringify(loaded));

  await page.evaluate(()=>eval(`(function(){
    setState(GS.PLAY);player.reset();player.invuln=99999;player.x=VW/2;player.y=VH-54;
    stagePlan=[{t:9999,fn:function(){}}];waveIdx=0;stageTimer=9999;mapScroll=levelScrollRange();snapCamToPlayer();
    enemies.length=0;eBullets.length=0;pBullets.length=0;powerups.length=0;aiQueue.length=0;
    boss=null;bossActive=false;subBoss=null;subBossActive=false;story=null;warnT=0;stageEnding=false;
    run._threatBuild=0;run._lifeThreat=0;run._lifeCombatT=0;spawnBoss('xenoregent');
    boss.enter=false;boss.y=boss.ty||120;boss._drawY=boss.y;boss.fireCd=99;
    for(var i=0;i<120;i++)xenoRegentTick(boss,1/60);
  })()`));
  const bossSpawnAt=Date.now();
  await page.waitForTimeout(350);
  const fight=await page.evaluate(()=>({bossHp:boss.hp,bossMax:boss.maxhp,mother:{x:boss._xenoRig.mother.x,
    y:boss._xenoRig.mother.y,hp:boss._xenoRig.mother.hp,max:boss._xenoRig.mother.maxhp},
    shield:boss._xenoRig.shield}));
  await page.locator('#screen').screenshot({path:path.join(OUT,'01_stage5_shield_array_target.png')});

  const shield=await page.evaluate(()=>eval(`(function(){
    var R=boss._xenoRig,b0=boss.hp,m0=R.mother.hp;
    hitBoss(100);
    var bleed={bossBefore:b0,bossAfter:boss.hp,motherBefore:m0,motherAfter:R.mother.hp};
    xenoRegentPartDamage(R.mother,R.mother.hp+1,boss);
    return {bleed:bleed,shieldAfter:R.shield,motherDead:R.mother.dead};
  })()`));
  await page.locator('#screen').screenshot({path:path.join(OUT,'02_stage5_shield_broken.png')});

  const grid=await page.evaluate(()=>eval(`(function(){
    eBullets.length=0;boss._xenoGrid=null;xenoRegentGridStart(boss,2);
    var spec={gap:boss._xenoGrid.gap,gapW:boss._xenoGrid.gapW,waves:boss._xenoGrid.waves,tell:boss._xenoGrid.tell};
    for(var i=0;i<145;i++)xenoRegentGridTick(boss,1/60);
    spec.projectiles=eBullets.length;spec.finished=!boss._xenoGrid;return spec;
  })()`));
  /* Re-open the telegraph for a visible three-column proof. */
  await page.evaluate(()=>{eBullets.length=0;boss._xenoGrid=null;xenoRegentGridStart(boss,4);});
  await page.locator('#screen').screenshot({path:path.join(OUT,'03_stage5_three_column_grid_lane.png')});

  const frameTimes=await page.evaluate(()=>new Promise(resolve=>{
    const a=[];let prev=performance.now(),n=0;
    function step(t){if(n)a.push(t-prev);prev=t;n++;if(n<181)requestAnimationFrame(step);else{
      const s=a.slice().sort((x,y)=>x-y);resolve({samples:a.length,median:s[(s.length*.5)|0],
        p95:s[(s.length*.95)|0],max:s[s.length-1]});}}
    requestAnimationFrame(step);
  }));
  const renderScale=await page.evaluate(()=>SS);
  const afterSpawnRequests=stageRequests.filter(r=>r.at>=bossSpawnAt);
  const kill=await page.evaluate(()=>{const before=boss.hp;hitBoss(before+10);return {before,defeated:bossDefeated,dying:boss.dying,dead:boss.dead};});
  const release=await page.evaluate(()=>{
    const before=!!XART.img.nca_stage5_runtime_atlas;beginStage(6);
    return {before,after:!!XART.img.nca_stage5_runtime_atlas,next:stageLoadInfo(6)};
  });
  const stageRootCounts=await page.evaluate(()=>{
    const out={};for(const n of [2,3,4,6,7,8,9]){beginStage(n);out[n]=stageLoadInfo(n).total;}return out;
  });

  const report={initial,loaded,maxInflight,loadMs:Date.now()-start,fight,shield,grid,renderScale,frameTimes,
    afterSpawnStageAssetRequests:afterSpawnRequests,missing,errors,kill,release,stageRootCounts};
  fs.writeFileSync(path.join(OUT,'report.json'),JSON.stringify(report,null,2));
  const assert=(v,m)=>{if(!v)throw new Error(m);};
  assert(initial.total>=20,'Stage 5 loader did not discover a meaningful resource set');
  assert(loaded.ready&&loaded.failed===0,'Stage 5 resources did not all decode');
  assert(maxInflight<=3,'Stage loader exceeded its three-image decode budget');
  assert(fight.bossMax<=3800,'Regent still has the duplicated HP multiplier: '+fight.bossMax);
  assert(fight.mother.y>=95,'Mandatory shield array is still clipped offscreen');
  assert(shield.bleed.motherAfter<shield.bleed.motherBefore&&shield.bleed.bossAfter===shield.bleed.bossBefore,
    'Shield did not route body/special damage to its source');
  assert(shield.motherDead&&!shield.shieldAfter,'Shield source did not break the shield');
  assert(grid.gapW===3&&grid.waves===3&&grid.projectiles<=24,'Grid is still over-dense: '+JSON.stringify(grid));
  assert(afterSpawnRequests.length===0,'Boss spawn caused late Stage-5 asset requests');
  assert(missing.length===0,'Missing resources: '+missing.join(', '));
  assert(errors.length===0,'Page errors: '+errors.join(' | '));
  assert(kill.defeated||kill.dying||kill.dead,'Regent kill path did not complete');
  assert(release.before&&!release.after,'Stage-owned atlas remained decoded after the next mission began');
  assert(Object.values(stageRootCounts).every(n=>n>0&&n<80),'A stage still queues too many texture roots: '+JSON.stringify(stageRootCounts));
  console.log(JSON.stringify(report,null,2));
  await browser.close();server.close();
})().catch(err=>{console.error(err);server.close();process.exit(1);});
