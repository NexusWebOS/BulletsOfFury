/* Browser render proof for the full-screen HQ, Xeno Regent rig and Stage-6 miniboss. */
const http=require('http');
const fs=require('fs');
const path=require('path');
let playwright;
try{playwright=require('playwright');}
catch(_){playwright=require(path.join(process.env.USERPROFILE,'.cache','codex-runtimes','codex-primary-runtime',
  'dependencies','node','node_modules','playwright'));}
const {chromium}=playwright;
const ROOT=path.resolve(__dirname,'..');
const OUT=path.join(ROOT,'docs','proofs','cinematic_boss_overhaul_0831');
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
  const page=await browser.newPage({viewport:{width:1440,height:900}});
  const errors=[];page.on('pageerror',e=>errors.push(String(e)));
  await page.goto(`http://127.0.0.1:${server.address().port}/index.html`,{waitUntil:'domcontentloaded',timeout:30000});
  await page.waitForFunction(()=>window.__bofFrames>12,null,{timeout:30000});
  await page.keyboard.press('Enter');

  await page.evaluate(()=>hqPlay('HQ_ALL_00'));
  await page.waitForFunction(()=>document.body.classList.contains('cinematic-full')&&XART.rdy('cut_furyhq_command_center'),null,{timeout:30000});
  await page.waitForTimeout(900);
  const cinematic=await page.evaluate(()=>{const c=document.getElementById('screen');return ({state,
    css:document.body.classList.contains('cinematic-full'),backing:[c.width,c.height],
    client:[c.clientWidth,c.clientHeight],viewWidth:cutsceneViewWidth()});});
  await page.screenshot({path:path.join(OUT,'01_full_browser_hq.png')});

  async function clear(stage){
    await page.evaluate(stage=>eval(`(function(){
      if(typeof hqSc!=='undefined')hqSc=null;
      beginStage(${stage});setState(GS.PLAY);player.reset();player.invuln=99999;player.x=worldWidth()/2;player.y=438;
      stagePlan=[{t:9999,fn:function(){}}];waveIdx=0;stageTimer=0;mapScroll=levelScrollRange();snapCamToPlayer();
      enemies.length=0;eBullets.length=0;pBullets.length=0;aiQueue.length=0;powerups.length=0;
      boss=null;bossActive=false;subBoss=null;subBossActive=false;story=null;
    })()`),stage);
  }

  await clear(5);
  await page.evaluate(()=>eval(`(function(){
    spawnBoss('xenoregent');boss.enter=false;boss.x=240;boss.y=128;boss.ty=128;boss.fireCd=999;
    if(boss._xenoRig){boss._xenoRig.t=2;boss._xenoRig.mother.y=36;for(var i=0;i<boss._xenoRig.helpers.length;i++)boss._xenoRig.helpers[i].y=145;}
  })()`));
  await page.waitForFunction(()=>boss&&boss._xenoRig&&XART.rdy('s5atk_twin_station_0')&&XART.rdy('s5atk_heavy_interceptor_0'),null,{timeout:30000});
  await page.waitForTimeout(700);
  const xeno=await page.evaluate(()=>({ship:boss._ship,shield:boss._xenoRig.shield,
    mother:boss._xenoRig.mother.hp,helpers:boss._xenoRig.helpers.map(x=>x.hp),targets:spaceTargets().filter(x=>x._xenoOwner).length}));
  await page.locator('#screen').screenshot({path:path.join(OUT,'02_stage5_regent_mothership_helpers.png')});

  await clear(6);
  await page.evaluate(()=>eval(`(function(){
    spawnSubBoss('blacksteel');subBoss.enter=false;subBoss.x=240;subBoss.y=128;subBoss.ty=128;subBoss.fireCd=999;
    if(subBoss._s6mini){subBoss._s6mini.mode='storm';subBoss._s6mini.t=.82;subBoss._s6mini.charge=.82;}
  })()`));
  await page.waitForFunction(()=>subBoss&&subBoss._s6mini&&XART.rdy('s6mb_cyclonemuzzle_0'),null,{timeout:30000});
  await page.waitForTimeout(450);
  const s6=await page.evaluate(()=>({ship:subBoss._ship,mode:subBoss._s6mini.mode,charge:subBoss._s6mini.charge}));
  await page.locator('#screen').screenshot({path:path.join(OUT,'03_stage6_miniboss_storm_charge.png')});

  const report={cinematic,xeno,s6,errors};
  fs.writeFileSync(path.join(OUT,'report.json'),JSON.stringify(report,null,2));
  console.log(JSON.stringify(report,null,2));
  const ok=cinematic.css&&cinematic.client[0]===1440&&cinematic.client[1]===900&&cinematic.viewWidth>=768&&
    xeno.shield&&xeno.targets===3&&s6.mode&&errors.length===0;
  await browser.close();server.close();if(!ok)process.exitCode=1;
})().catch(e=>{console.error(e);server.close();process.exitCode=1;});
