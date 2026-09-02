/* Production-browser proof for the complete Stage 7 Warden finale and Stage 8 helix-rift entry. */
const http=require('http'),fs=require('fs'),path=require('path');let playwright;
try{playwright=require('playwright');}catch(_){playwright=require(path.join(process.env.USERPROFILE,'.cache','codex-runtimes','codex-primary-runtime','dependencies','node','node_modules','playwright'));}
const {chromium}=playwright,ROOT=path.resolve(__dirname,'..'),OUT=path.join(ROOT,'docs','proofs','stage7_finale_helix_0901');
fs.mkdirSync(OUT,{recursive:true});
const MIME={'.html':'text/html','.js':'text/javascript','.css':'text/css','.png':'image/png','.jpg':'image/jpeg','.webp':'image/webp','.json':'application/json','.mp3':'audio/mpeg','.ogg':'audio/ogg'};
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
  const shot=name=>page.locator('#screen').screenshot({path:path.join(OUT,name)});
  await page.evaluate(()=>eval(`(function(){
    run.mode='campaign';beginStage(7);setState(GS.PLAY);run.pilot=Math.max(0,PILOTS.findIndex(function(p){return p.key==='lizzie';}));
    player.reset();player.invuln=999;player.x=worldWidth()/2;player.y=485;snapCamToPlayer();stagePlan=[{t:9999,fn:function(){}}];
    waveIdx=0;stageTimer=90;mapScroll=levelScrollRange();enemies.length=0;eBullets.length=0;pBullets.length=0;aiQueue.length=0;powerups.length=0;
    boss=null;bossActive=false;bossDefeated=false;subBoss=null;subBossActive=false;subBossDone=true;subBossTriggered=true;
    bossWarned=true;warnT=0;warnKind=null;story=null;if(typeof storySkip==='function')storySkip();
  })()`));
  await page.waitForFunction(()=>XART.rdy('nfx_l7portal_4'),null,{timeout:20000});
  await page.evaluate(()=>{mapScroll=levelScrollRange();});await page.waitForTimeout(240);
  await page.evaluate(()=>{mapScroll=levelScrollRange();_bossHold=1;});await page.waitForTimeout(80);await shot('01_helix_portal_waiting.png');
  await page.evaluate(()=>eval(`(function(){spawnBoss('sludgeemperor');boss.enter=false;s7WardenInit(boss);boss.x=worldWidth()/2;boss.y=84;boss.ty=178;warnT=0;warnKind=null;story=null;})()`));
  const keys=['cfx_stage7_warden_walk','cfx_stage7_warden_roar','cfx_stage7_warden_cripple','cfx_stage7_warden_laststand','cfx_stage7_warden_teleport','cfx_stage7_warden_mine'];
  await page.waitForFunction(keys=>keys.every(k=>XART.rdy(k)),keys,{timeout:25000});
  await page.waitForTimeout(420);await page.evaluate(()=>{mapScroll=levelScrollRange();_bossHold=1;});await page.waitForTimeout(80);await shot('02_portal_closing.png');
  await page.evaluate(()=>{s7WardenPhase(boss,'teleportIn');boss._s7warden.final.t=.44;});await page.waitForTimeout(180);await shot('03_portal_aperture_teleport.png');
  await page.evaluate(()=>{boss._s7warden.final.t=.82;});await page.waitForTimeout(180);await shot('04_warden_emerging.png');
  await page.evaluate(()=>{s7WardenPhase(boss,'roar');boss._s7warden.final.t=.68;boss._s7warden.final.beat=1;});await page.waitForTimeout(180);await shot('05_warden_rear_roar.png');
  await page.evaluate(()=>{s7WardenPhase(boss,'fight');boss._s7FinalNoBar=false;boss._s7warden.noHit=false;boss.y=184;});await page.waitForTimeout(220);await shot('06_reverse_scroll_fight.png');

  await page.evaluate(()=>eval(`(function(){boss.hp=boss.maxhp*.755;s7WardenHit(boss,boss.maxhp*.015,boss.x,boss.y);})()`));
  await page.waitForTimeout(520);await shot('07_stunned_exposed_cores.png');
  const coreState=await page.evaluate(()=>eval(`(function(){var out={phase:s7FinalPhase(boss),noHit:boss._s7warden.noHit,tests:[]};for(const c of boss._s7warden.final.cores){const p=s7WardenCorePos(boss,c.side);out.tests.push({p:p,at:!!s7WardenCoreAt(boss,p.x,p.y),before:c.hp});s7WardenHit(boss,c.max+5,p.x,p.y);out.tests[out.tests.length-1].after=c.hp;out.tests[out.tests.length-1].dead=c.dead;}out.cores=boss._s7warden.final.cores.map(c=>({dead:c.dead,hp:c.hp}));return out;})()`));
  await page.evaluate(()=>{boss._s7warden.final.t=3.68;});await page.waitForTimeout(150);
  await page.evaluate(()=>eval(`(function(){boss.hp=boss.maxhp*.505;s7WardenHit(boss,boss.maxhp*.015,boss.x,boss.y);})()`));
  await page.waitForTimeout(720);await shot('08_hyper_pixel_glow.png');
  await page.evaluate(()=>{boss._s7warden.final.t=1.55;});await page.waitForTimeout(150);
  await page.evaluate(()=>eval(`(function(){boss.hp=boss.maxhp*.255;s7WardenHit(boss,boss.maxhp*.015,boss.x,boss.y);})()`));
  await page.waitForTimeout(650);await shot('09_rear_leg_destruction.png');
  await page.evaluate(()=>{boss._s7warden.final.t=1.30;});await page.waitForTimeout(150);await shot('10_crippled_front_leg_crawl.png');
  await page.evaluate(()=>eval(`(function(){boss.hp=1;s7WardenHit(boss,4,boss.x,boss.y);})()`));
  await page.waitForTimeout(580);await shot('11_intact_last_stand.png');
  await page.evaluate(()=>{boss._s7warden.final.t=2.78;});await page.waitForTimeout(950);await shot('12_escape_portal_and_warning.png');
  await page.evaluate(()=>{boss._s7warden.final.t=4.08;});await page.waitForTimeout(280);await shot('13_explosion_chase_whiteout.png');
  await page.evaluate(()=>{boss._s7warden.final.t=5.22;});await page.waitForTimeout(240);
  const mapState=await page.evaluate(()=>({state:state,stageSelect:GS.STAGESEL,runStage:run.stage,pending:campaign._l78Pending||0,unlocked:campaign.unlockedMax,bossActive,
    phase:boss&&s7FinalPhase(boss),phaseT:boss&&boss._s7warden&&boss._s7warden.final.t,finished:boss&&boss._s7warden&&boss._s7warden.final.finished,whiteBlast}));

  await page.evaluate(()=>beginStage(8));
  await page.evaluate(()=>{l78entry.t=.24;});await page.waitForTimeout(160);await shot('14_stage8_white_helix_rift.png');
  await page.evaluate(()=>{l78entry.t=1.14;});await page.waitForTimeout(160);await shot('15_ship_spat_from_rift.png');
  await page.evaluate(()=>{l78entry.t=2.54;});await page.waitForTimeout(160);await shot('16_stage8_reader_warning.png');
  await page.evaluate(()=>{l78entry.radio=null;l78entry.said2=true;l78entry.t=7.28;});await page.waitForTimeout(160);await shot('17_stage8_countdown.png');
  await page.evaluate(()=>{l78entry.radio=null;l78entry.t=9.48;});await page.waitForTimeout(160);await shot('18_stage8_go_live.png');
  await page.evaluate(()=>{l78entry.t=10.18;});await page.waitForTimeout(180);
  const endState=await page.evaluate(keys=>({state:state,play:GS.PLAY,stage:run.stage,l78:run._l78Entry,playerHidden:s7WardenShipHidden(),
    assets:keys.map(k=>({key:k,ready:XART.rdy(k)}))}),keys);
  await context.close();const recorded=await video.path(),webm=path.join(OUT,'lizzie_stage7_warden_to_stage8_helix.webm');
  if(path.resolve(recorded)!==path.resolve(webm))fs.copyFileSync(recorded,webm);await browser.close();server.close();
  const report={coreState,mapState,endState,errors,missing,recording:path.relative(ROOT,webm).replace(/\\/g,'/')};
  fs.writeFileSync(path.join(OUT,'report.json'),JSON.stringify(report,null,2));console.log(JSON.stringify(report,null,2));
  const ok=coreState.cores.every(c=>c.dead)&&mapState.state===mapState.stageSelect&&mapState.pending===1&&mapState.unlocked>=8&&!mapState.bossActive&&
    endState.state===endState.play&&endState.stage===8&&!endState.l78&&endState.assets.every(a=>a.ready)&&!errors.length&&!missing.length;
  if(!ok)process.exitCode=1;
})().catch(e=>{console.error(e);server.close();process.exitCode=1;});
