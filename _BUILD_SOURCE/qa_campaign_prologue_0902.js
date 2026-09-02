/* Browser proof for the new-campaign FURY HQ prologue and its safe map handoff. */
const http=require('http');
const fs=require('fs');
const path=require('path');
let playwright;
try{playwright=require('playwright');}
catch(_){playwright=require(path.join(process.env.USERPROFILE,'.cache','codex-runtimes','codex-primary-runtime','dependencies','node','node_modules','playwright'));}
const {chromium}=playwright;

const ROOT=path.resolve(__dirname,'..');
const OUT=path.join(ROOT,'docs','proofs','campaign_prologue_0902');
fs.mkdirSync(OUT,{recursive:true});
const MIME={'.html':'text/html','.js':'text/javascript','.css':'text/css','.png':'image/png','.jpg':'image/jpeg','.json':'application/json','.ttf':'font/ttf','.wav':'audio/wav','.mp3':'audio/mpeg'};
const server=http.createServer((req,res)=>{
  const rel=decodeURIComponent((req.url||'/').split('?')[0]).replace(/^\/+/, '')||'index.html';
  const file=path.resolve(ROOT,rel);if(!file.startsWith(ROOT)){res.writeHead(403);res.end();return;}
  fs.readFile(file,(err,data)=>{if(err){res.writeHead(404);res.end();return;}
    res.writeHead(200,{'Content-Type':MIME[path.extname(file).toLowerCase()]||'application/octet-stream'});res.end(data);});
});

(async()=>{
  await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
  const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe'});
  const page=await browser.newPage({viewport:{width:1180,height:760}}),errors=[],missing=[];
  page.on('pageerror',e=>errors.push(String(e)));
  page.on('console',m=>{if(m.type()==='error'&&!/^Failed to load resource:/.test(m.text()))errors.push(m.text());});
  page.on('response',r=>{if(r.status()>=400&&!/favicon\.ico/.test(r.url()))missing.push({status:r.status(),url:r.url()});});
  await page.goto(`http://127.0.0.1:${server.address().port}/index.html`,{waitUntil:'domcontentloaded',timeout:30000});
  await page.waitForFunction(()=>window.__bofFrames>8&&typeof campaignIntroStart==='function'&&typeof bmfReady==='function'&&bmfReady('dialogue'),null,{timeout:30000});

  await page.evaluate(()=>eval(`(function(){
    run.mode='campaign';campaign._booted=true;campaignIntroPilot='maverick';
    campaignIntroStart(function(){openStageSelect(1,{boot:true});});
  })()`));
  await page.waitForFunction(()=>eval(`campaignIntroReady()`),null,{timeout:30000});

  const shots=[
    ['01_hq_aerial.png',1.5],['02_hq_beach_view.png',4.9],['03_hq_gate_view.png',8.2],
    ['04_fury_team.png',11.7],['05_command.png',15.1],['06_virus_takeover.png',18.6],
    ['07_final_dispatch.png',22.2],['08_title_seven_rounds_rng_pilot.png',26.2]
  ];
  for(const [name,t] of shots){
    await page.evaluate(t=>eval(`(function(){campaignIntro.t=${JSON.stringify(t)};campaignIntro.ready=true;campaignIntro.shotSoundN=7;})()`),t);
    await page.waitForTimeout(140);
    await page.locator('#screen').screenshot({path:path.join(OUT,name)});
  }

  const contract=await page.evaluate(()=>eval(`(function(){
    var route=cinRouteBackdrop.toString(),motion=cinDrawMotion.toString(),flow=startRun.toString();
    var oldMG=Audio.SFX.machineGun,shots=0;Audio.SFX.machineGun=function(){shots++;};
    campaignIntro.shotSoundN=0;campaignIntroFinale(campaignIntro,CAMPAIGN_INTRO_FINALE+2,cutsceneViewWidth(),VH);
    Audio.SFX.machineGun=oldMG;campaignIntro.shotSoundN=7;
    return {
      state:state,introState:GS.CAMPAIGNINTRO,beatCount:CAMPAIGN_INTRO_BEATS.length,
      closeViewsRegistered:XART._src.cinbg_hq_beach&&XART._src.cinbg_hq_gate,
      aerialOnlyRoute:route.indexOf('cinbg_hq_aerial')>=0&&route.indexOf('cinbg_hq_beach')<0&&route.indexOf('cinbg_hq_gate')<0,
      topDownApproaches:motion.indexOf("motion==='hq_approach'")>=0&&motion.indexOf("motion==='jungle_approach'")>=0,
      sevenRoundFinale:campaignIntroFinale.toString().indexOf('i<7')>=0,
      sevenShotSounds:shots,
      randomPilot:campaignIntro.pilot,
      freshRunRoutesToPrologue:flow.indexOf("campaignIntroStart(function(){ openStageSelect(fromStage,{boot:true}); })")>=0,
      dialogueReady:bmfReady('dialogue'),ready:campaignIntroReady(),canvas:[cv.width,cv.height]
    };
  })()`));

  /* A fresh Enter press skips to the same booting map and never reaches generic Back routing. */
  await page.evaluate(()=>eval(`(function(){
    globalThis.__ciDone=0;campaignIntroPilot='axel';
    campaignIntroStart(function(){globalThis.__ciDone++;openStageSelect(1,{boot:true});});
    campaignIntro.ready=true;stateT=.6;
  })()`));
  await page.keyboard.press('Enter');
  await page.waitForFunction(()=>eval(`state===GS.STAGESEL`),null,{timeout:5000});
  const skip=await page.evaluate(()=>eval(`({called:globalThis.__ciDone|0,state:state,map:state===GS.STAGESEL,boot:sselBoot})`));
  await page.evaluate(()=>eval(`(function(){sselBoot=0;sselFlagsShown=9;})()`));
  await page.waitForTimeout(180);
  await page.locator('#screen').screenshot({path:path.join(OUT,'09_campaign_map_handoff.png')});

  const report={contract,skip,errors,missing};
  fs.writeFileSync(path.join(OUT,'report.json'),JSON.stringify(report,null,2));
  console.log(JSON.stringify(report,null,2));
  await browser.close();server.close();
  const ok=contract.state===contract.introState&&contract.beatCount===7&&contract.closeViewsRegistered&&
    contract.aerialOnlyRoute&&contract.topDownApproaches&&contract.sevenRoundFinale&&contract.sevenShotSounds===7&&contract.freshRunRoutesToPrologue&&
    contract.dialogueReady&&contract.ready&&skip.called===1&&skip.map&&skip.boot===1&&errors.length===0&&missing.length===0;
  if(!ok)process.exitCode=1;
})().catch(e=>{console.error(e);server.close();process.exitCode=1;});
