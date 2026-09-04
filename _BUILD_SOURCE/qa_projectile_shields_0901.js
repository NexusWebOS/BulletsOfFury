/* Production-browser proof for the 0901 projectile/shield/boss correction pass. */
const http=require('http');
const fs=require('fs');
const path=require('path');
let playwright;
try{playwright=require('playwright');}
catch(_){playwright=require(path.join(process.env.USERPROFILE,'.cache','codex-runtimes','codex-primary-runtime','dependencies','node','node_modules','playwright'));}
const {chromium}=playwright;

const ROOT=path.resolve(__dirname,'..');
const OUT=path.join(ROOT,'docs','proofs','projectile_shields_0901');
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
  const page=await browser.newPage({viewport:{width:980,height:720}}),errors=[],missing=[];
  page.on('pageerror',e=>errors.push(String(e)));
  page.on('console',m=>{if(m.type()==='error'&&!/^Failed to load resource:/.test(m.text()))errors.push(m.text());});
  page.on('response',r=>{if(r.status()>=400&&!/favicon\.ico/.test(r.url()))missing.push({status:r.status(),url:r.url()});});
  await page.goto(`http://127.0.0.1:${server.address().port}/index.html`,{waitUntil:'domcontentloaded',timeout:30000});
  await page.waitForFunction(()=>window.__bofFrames>8,null,{timeout:30000});

  async function clear(stage,key){
    await page.evaluate(stage=>eval(`(function(){
      beginStage(${stage});setState(GS.PLAY);run.pilot=Math.max(0,PILOTS.findIndex(function(p){return p.key==='lizzie';}));
      player.reset();player.invuln=999;player.x=worldWidth()/2;player.y=430;snapCamToPlayer();
      stagePlan=[{t:9999,fn:function(){}}];waveIdx=0;stageTimer=0;mapScroll=levelScrollRange();
      enemies.length=0;eBullets.length=0;pBullets.length=0;aiQueue.length=0;powerups.length=0;
      boss=null;bossActive=false;subBoss=null;subBossActive=false;story=null;s5run=null;
    })()`),stage);
    if(key)await page.waitForFunction(key=>XART.rdy(key),key,{timeout:30000});
    await page.waitForTimeout(120);
  }
  async function screenshot(name){await page.locator('#screen').screenshot({path:path.join(OUT,name)});}
  async function gallery(stage,key,kinds,name){
    await clear(stage,key);
    const routed=await page.evaluate(kinds=>eval(`(function(){
      var kinds=${JSON.stringify(kinds)};
      for(var i=0;i<kinds.length;i++){
        var col=i%4,row=Math.floor(i/4),left=(typeof camX==='number'?camX:0);
        eBullets.push({x:left+65+col*120,y:135+row*190,vx:0,vy:.001,w:18,h:28,dmg:1,t:(i%4)*.035,
          kind:kinds[i],_boss:true,_noArsenal:true,_forceStageArt:true,szMul:1.45});
      }
      return kinds.map(function(k){return !!CFX_STAGE_PROJECTILE[k];});
    })()`),kinds);
    await page.waitForTimeout(180);await screenshot(name);return routed;
  }

  const galleries={};
  galleries.stage2=await gallery(2,'cfx_stage2_volcanic_projectiles',
    ['s2needle','s2rake','s2slag','s2rocket','s2bomb','s2shock','s2breath','s2mine'],'01_stage2_projectile_family.png');
  galleries.stage5=await gallery(5,'cfx_stage5_alien_projectiles_v2',
    ['s5fracture','s5split','s5prism','s5null','s5missile','s5chaos','s5halo'],'02_stage5_projectile_family.png');
  galleries.stage7=await gallery(7,'cfx_stage7_toxic_projectiles_v2',
    ['s7acid','s7sludge','s7shard','s7bio','s7laser','s7grenade'],'03_stage7_projectile_family.png');
  galleries.stage8=await gallery(8,'cfx_stage8_symbiote_projectiles',
    ['s8needle','s8rage','s8slug','s8missile','s8pair','s8blade','s8rift','s8parasite'],'04_stage8_projectile_family.png');

  const shieldCases={2:['disc','eye'],5:['s5gravity','s5satellite','s5repair','s5leech'],
    7:['s7sampler','s7skimmer'],8:['s8deathorb','s8parasite','s8scout','s8leech'],
    9:['s9beacon','s9prism','s9ring','s9singularity']};
  const shields={};
  for(const stage of [2,5,7,8,9]){
    await clear(stage,null);
    shields[stage]=await page.evaluate(types=>eval(`(function(){
      var types=${JSON.stringify(types)},out=[];
      for(var i=0;i<types.length;i++){
        var e=spawnEnemy(types[i],110+i*150,150,{inPlace:true,_noFire:true});
        if(e){e.x=110+i*150;e.y=150;e.vx=0;e.vy=0;if(e._esh){e._esh.phase='active';e._esh.animT=.16;}
          out.push({type:e.type,family:e._esh&&e._esh.family,energy:e._esh&&e._esh.max});}
      }return out;
    })()`),shieldCases[stage]);
    if(stage===8){
      await page.waitForFunction(()=>XART.rdy('nes_crimson_f_3')&&XART.rdy('nes_prism_3'),null,{timeout:30000});
      await page.waitForTimeout(150);await screenshot('05_stage8_shielded_drone_roster.png');
    }
  }

  /* Stage 4: the carrier bubble rejects a body shot, but the unlocked sub-target beneath 50%
     receives damage through the same live bubble. Include the new lightning-only shot in frame. */
  await clear(4,'cfx_stage4_chain_lightning');
  const stage4=await page.evaluate(()=>eval(`(function(){
    spawnBoss('stormsovereign');boss.enter=false;boss.x=worldWidth()/2;boss.y=138;boss.ty=138;boss.hp=boss.maxhp*.50;
    if(!boss._s4war)stage4WarfareInit(boss);stage4CoreTurretSpawnMissing(boss,.50);
    var t=boss._s4war.coreTurrets[0];t.materialize=1;t.spawnT=1;t.x=112;t.y=260;
    var before=t.shield,coreShot={x:t.x,y:t.y,vx:0,vy:-8,w:8,h:14};boss._s4CoreHit=t;boss._s4ShieldHit=null;
    var coreDeflected=stage4ShieldDeflectBullet(boss,coreShot);stage4CoreTurretAbsorbHit(boss,18);
    var bodyShot={x:boss.x,y:boss.y+boss.h*.42,vx:0,vy:-8,w:8,h:14};boss._s4CoreHit=null;boss._s4ShieldHit=null;
    var bodyDeflected=stage4ShieldDeflectBullet(boss,bodyShot);
    eBullets.push({x:boss.x+112,y:315,vx:0,vy:2.2,w:23,h:54,dmg:1,t:.12,_s4wKind:'lightning',_boss:true,szMul:1.35});
    return {coreDeflected:coreDeflected,bodyDeflected:bodyDeflected,before:before,after:t.shield,coreUnlocked:boss._s4war.coreUnlocked};
  })()`));
  await page.waitForTimeout(180);await screenshot('06_stage4_turret_window_and_chain_lightning.png');

  /* Stage 2: force the chargebeam phase. Only L/R may own beam geometry; C owns the magma orb. */
  await clear(2,'cfx_stage2_volcanic_projectiles');
  const stage2Tell=await page.evaluate(()=>eval(`(function(){
    spawnBoss('infernoreaver');boss.enter=false;boss.x=worldWidth()/2;boss.y=132;boss.ty=132;boss.hp=boss.maxhp*.35;
    boss._mwAttack=null;boss._irPass=null;boss._irRoll=null;boss._l23Beam=null;boss._orb=null;shipBossAttack(boss);
    if(boss._orb)boss._orb.t=.74;
    return {pattern:shipBossCurrentPattern(boss),beamSlots:boss._l23Beam&&boss._l23Beam.slots.slice(),orb:!!boss._orb};
  })()`));
  await page.waitForFunction(()=>XART.rdy('mwfx_fireball_charge_4'),null,{timeout:30000});
  await page.waitForTimeout(120);await screenshot('07_stage2_nose_magma_charge.png');
  const stage2Release=await page.evaluate(()=>eval(`(function(){
    var before=eBullets.length;reaverOrbTick(boss,.52);var q=eBullets.find(function(x){return x._reaverOrb;});
    return {before:before,after:eBullets.length,kind:q&&q.kind,size:q&&q.szMul,beamSlots:boss._l23Beam&&boss._l23Beam.slots.slice()};
  })()`));

  const assets=await page.evaluate(()=>[
    'cfx_stage2_volcanic_projectiles','cfx_stage4_chain_lightning','cfx_stage5_alien_projectiles_v2',
    'cfx_stage7_toxic_projectiles_v2','cfx_stage8_symbiote_projectiles'
  ].map(k=>({key:k,registered:!!XART._src[k]})));
  const report={galleries,shields,stage4,stage2Tell,stage2Release,assets,errors,missing};
  fs.writeFileSync(path.join(OUT,'report.json'),JSON.stringify(report,null,2));console.log(JSON.stringify(report,null,2));
  await browser.close();server.close();

  const galleryOk=Object.values(galleries).every(rows=>rows.every(Boolean));
  const shieldOk=Object.values(shields).every(rows=>rows.length&&rows.every(q=>q.family&&q.energy>0));
  const stage4Ok=stage4.coreUnlocked&&!stage4.coreDeflected&&stage4.bodyDeflected&&stage4.after<stage4.before;
  const stage2Ok=stage2Tell.pattern==='chargebeam'&&stage2Tell.orb&&stage2Tell.beamSlots.join(',')==='L,R'&&
    stage2Release.kind==='magma'&&stage2Release.size===2.6;
  if(!galleryOk||!shieldOk||!stage4Ok||!stage2Ok||assets.some(a=>!a.registered)||errors.length||missing.length)process.exitCode=1;
})().catch(e=>{console.error(e);server.close();process.exitCode=1;});
