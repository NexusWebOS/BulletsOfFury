/* Focused browser proof for the 0902 Stage-2 / Laser Mist / pause pass. */
const http=require('http');
const fs=require('fs');
const path=require('path');
let playwright;
try{playwright=require('playwright');}
catch(_){playwright=require(path.join(process.env.USERPROFILE,'.cache','codex-runtimes','codex-primary-runtime',
  'dependencies','node','node_modules','playwright'));}
const {chromium}=playwright;

const ROOT=path.resolve(__dirname,'..');
const OUT=path.join(ROOT,'docs','proofs','stage2_lasermist_pause_0902');
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
  const source=fs.readFileSync(path.join(ROOT,'assets','game.js'),'utf8');
  const atlasMap=JSON.parse(fs.readFileSync(path.join(ROOT,'assets','game','laser_mist','bof_laser_mist_weapon_atlas.json'),'utf8'));
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

  await page.evaluate(()=>beginStage(2));
  await page.waitForFunction(()=>stageLoadReady(2),null,{timeout:60000});
  const stage2=await page.evaluate(()=>eval(`(function(){
    run.stage=2;curStage=STAGES[1];setState(GS.PLAY);player.reset();player.dead=false;player.invuln=9999;
    player.x=VW/2;player.y=VH-52;stagePlan=[{t:9999,fn:function(){}}];waveIdx=0;stageTimer=9999;
    mapScroll=levelScrollRange();snapCamToPlayer();enemies.length=0;eBullets.length=0;pBullets.length=0;
    powerups.length=0;boss=null;bossActive=false;subBoss=null;subBossActive=false;story=null;warnT=0;stageEnding=false;
    spawnBoss('infernoreaver');boss.enter=false;boss.y=boss.ty||120;boss._drawY=boss.y;boss.fireCd=.1;
    var patrol={ampX:SHIPBOSS.infernoreaver.move.ampX,ampY:SHIPBOSS.infernoreaver.move.ampY,
      period:SHIPBOSS.infernoreaver.move.period};
    var barrier=boss._mwBarrier,bodyHp=boss.hp;
    boss._sba={kind:'chargebeam'};boss._l23Beam={};boss._orb={};boss._irPass={};boss._irRoll={};
    magmaWardBarrierDamage(boss,barrier.maxhp+1,boss.x,boss.y);
    var manoeuvre=shipBossManoeuvre(boss,1/60);
    return {patrol:patrol,bodyUnaffected:boss.hp===bodyHp,barrierActive:barrier.active,
      stun:boss._mwStun,fireCd:boss.fireCd,attacksCancelled:!boss._sba&&!boss._l23Beam&&!boss._orb&&!boss._irPass&&!boss._irRoll,
      manoeuvreOwnsFrame:manoeuvre};
  })()`));
  /* Restore an intact shield for the visual proof after validating the break state. */
  await page.evaluate(()=>{magmaWardBarrierInit(boss);boss._mwStun=0;boss.fireCd=99;explosions.length=0;});
  await page.waitForTimeout(150);
  await page.locator('#screen').screenshot({path:path.join(OUT,'01_stage2_inferno_reaver_shield.png')});

  await page.evaluate(()=>{laserMistWarm();});
  await page.waitForFunction(()=>XART.rdy('bof_laser_mist_weapon_atlas'),null,{timeout:30000});
  await page.evaluate(()=>beginStage(9));
  await page.waitForFunction(()=>stageLoadReady(9),null,{timeout:60000});
  const mist=await page.evaluate(()=>eval(`(function(){
    run.stage=9;curStage=STAGES[8];setState(GS.PLAY);player.reset();player.dead=false;player.invuln=9999;
    player.x=VW/2;player.y=VH-44;run.weapon=6;run.wlevels=[1,1,1,1,1,1,5];run.wlevel=5;
    stagePlan=[{t:9999,fn:function(){}}];waveIdx=0;stageTimer=9999;mapScroll=levelScrollRange();snapCamToPlayer();
    enemies.length=0;eBullets.length=0;pBullets.length=0;powerups.length=0;particles.length=0;pImpacts.length=0;
    boss=null;bossActive=false;bossWarned=true;subBoss=null;subBossActive=false;subBossTriggered=true;subBossDone=true;
    story=null;warnT=0;stageEnding=false;
    function step(n){for(var f=0;f<n;f++){var list=pBullets.slice();for(var i=0;i<list.length;i++)laserMistTick(list[i],1/60);
      for(var j=pBullets.length-1;j>=0;j--)if(pBullets[j].dead)pBullets.splice(j,1);}}
    laserMistFire(5);var launch=pBullets.length;step(8);var first=pBullets.length;
    step(22);var second=pBullets.length;
    var stages=[0,0,0];for(var b of pBullets)stages[b._mistStage]++;
    laserMistImpact(VW*.31,VH*.34,5,true);laserMistImpact(VW*.69,VH*.41,5,false);
    var xs=pBullets.map(function(b){return b.x;}),ys=pBullets.map(function(b){return b.y;});timeScale=0;
    return {launch:launch,first:first,second:second,stages:stages,waves:[...new Set(pBullets.map(function(b){return b._mistLedger.wave;}))].length,
      bubbles:particles.filter(function(p){return p._lmBubble;}).length,impacts:pImpacts.length,
      bounds:{minX:Math.min.apply(Math,xs),maxX:Math.max.apply(Math,xs),minY:Math.min.apply(Math,ys),maxY:Math.max.apply(Math,ys)}};
  })()`));
  await page.waitForTimeout(35);
  await page.locator('#screen').screenshot({path:path.join(OUT,'02_laser_mist_level5_split_and_impacts.png')});

  const pause=await page.evaluate(()=>eval(`(function(){
    timeScale=1;Audio.setVol('music',.5);setState('paused');
    return {state:state,screen:document.getElementById('screen').style.filter,
      hud:document.getElementById('hud').style.filter,equip:document.getElementById('equipcv').style.filter,
      lowered:Audio.getVol('music')};
  })()`));
  await page.waitForTimeout(35);
  await page.screenshot({path:path.join(OUT,'03_pause_grayscale.png')});
  const resumed=await page.evaluate(()=>{setState(GS.PLAY);return {state:state,
    filter:document.getElementById('screen').style.filter,music:Audio.getVol('music')};});

  const failure=await page.evaluate(()=>eval(`(function(){
    try{localStorage.removeItem(LASER_MIST_UNLOCK_KEY);}catch(e){}laserMistUnlocked=false;
    run.stage=9;bossDefeated=false;setState(GS.PLAY);triggerGameOver();
    return {state:state,unlocked:laserMistIsUnlocked(),stored:localStorage.getItem(LASER_MIST_UNLOCK_KEY)};
  })()`));
  const unlock=await page.evaluate(()=>eval(`(function(){
    setState(GS.PLAY);run.stage=9;laserMistUnlocked=false;try{localStorage.removeItem(LASER_MIST_UNLOCK_KEY);}catch(e){}
    var changed=laserMistUnlock();run.stage=6;run.spaceMode=false;return {changed:changed,unlocked:laserMistIsUnlocked(),stored:localStorage.getItem(LASER_MIST_UNLOCK_KEY),
      icon:weaponIconKey(6,5),name:weaponDisplayName(6)};
  })()`));

  const unlockCalls=(source.match(/laserMistUnlock\(\)/g)||[]).length;
  const staticChecks={
    atlasFrames:Object.keys(atlasMap.frames||{}).length,
    unlockCalls:unlockCalls,
    shadowImmediate:/const SPACE_SHADOW_AUDIO_DELAY=0;/.test(source),
    laserImpactAtlas:/key='laser_'\+clamp\(b\.lv\|\|1,1,5\)\+'_impact_'/.test(source),
    cutscenePilotPrewarm:/function cinPrewarmPilot\(pilot\)/.test(source)&&/cinPrewarmPilot\(run\.pilot\)/.test(source),
    selectedStagePrewarm:/warmStageSheets\([^\n]*sselCursor/.test(source),
    unlockFunction:/function laserMistUnlock\(\)/.test(source),
    stage9OnlyGrant:/if\(run\.stage===9&&typeof laserMistUnlock==='function'\)laserMistUnlock\(\)/.test(source)
  };
  const report={stage2,mist,pause,resumed,failure,unlock,staticChecks,missing,errors};
  fs.writeFileSync(path.join(OUT,'report.json'),JSON.stringify(report,null,2));
  const assert=(v,m)=>{if(!v)throw new Error(m);};
  assert(stage2.patrol.period>=5.5&&stage2.patrol.ampX<=120&&stage2.patrol.ampY<=4,
    'Stage-2 boss patrol is not slow/predictable: '+JSON.stringify(stage2.patrol));
  assert(stage2.bodyUnaffected&&!stage2.barrierActive&&stage2.stun>=.8&&stage2.fireCd>stage2.stun&&
    stage2.attacksCancelled&&stage2.manoeuvreOwnsFrame,'Stage-2 shield punish contract failed: '+JSON.stringify(stage2));
  assert(mist.launch===3&&mist.first===9&&mist.second===27&&mist.stages[2]===27&&mist.waves===1,
    'Laser Mist did not produce one 3 -> 9 -> 27 wave: '+JSON.stringify(mist));
  assert(mist.bubbles>0&&mist.bubbles<=72&&mist.impacts===4,'Water impact budget failed: '+JSON.stringify(mist));
  assert(pause.state==='paused'&&/grayscale\(1\)/.test(pause.screen)&&pause.screen===pause.hud&&pause.screen===pause.equip&&
    pause.lowered<=.141,'Pause presentation/audio failed: '+JSON.stringify(pause));
  assert(resumed.state==='play'&&resumed.filter===''&&Math.abs(resumed.music-.5)<.001,
    'Pause resume did not restore visuals/music: '+JSON.stringify(resumed));
  assert(failure.state==='riftfallback'&&!failure.unlocked&&failure.stored===null,
    'Stage-9 failure did not route to the rift without granting the reward: '+JSON.stringify(failure));
  assert(unlock.changed&&unlock.unlocked&&unlock.stored==='1'&&unlock.icon==='micon_lasermist_5'&&unlock.name==='LASER MIST',
    'Stage-9 reward persistence/icon/name failed: '+JSON.stringify(unlock));
  assert(staticChecks.atlasFrames===49&&staticChecks.shadowImmediate&&staticChecks.laserImpactAtlas&&
    staticChecks.cutscenePilotPrewarm&&staticChecks.selectedStagePrewarm&&staticChecks.unlockFunction&&staticChecks.stage9OnlyGrant,
    'Static integration contract failed: '+JSON.stringify(staticChecks));
  assert(missing.length===0,'Missing assets: '+missing.join(', '));
  assert(errors.length===0,'Page errors: '+errors.join(' | '));
  console.log(JSON.stringify(report,null,2));
  await browser.close();server.close();
})().catch(err=>{console.error(err);server.close();process.exit(1);});
