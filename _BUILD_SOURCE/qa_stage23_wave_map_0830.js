/* Real-browser proof for the 2026-08-30 Stage-2 and Stage-3 annotated encounter maps. */
const http=require('http');
const fs=require('fs');
const path=require('path');
let playwright;
try{playwright=require('playwright');}
catch(_){playwright=require(path.join(process.env.USERPROFILE,'.cache','codex-runtimes','codex-primary-runtime',
  'dependencies','node','node_modules','playwright'));}
const {chromium}=playwright;

const ROOT=path.resolve(__dirname,'..');
const OUT=path.join(ROOT,'docs','proofs','stage23_wave_map_0830');
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
  const errors=[];page.on('pageerror',e=>errors.push(String(e)));
  await page.goto(`http://127.0.0.1:${server.address().port}/index.html`,
    {waitUntil:'domcontentloaded',timeout:30000});
  await page.waitForFunction(()=>window.__bofFrames>12,null,{timeout:30000});

  const audit=JSON.parse(await page.evaluate(()=>eval(`(function(){
    function inspect(n){
      run.pilot='cole';beginStage(n);setState(GS.PLAY);player.reset();player.invuln=999;
      var plan=buildStagePlan(n),out=[];
      for(var wi=0;wi<plan.length;wi++){
        enemies.length=0;aiQueue.length=0;
        var clock=0,seen=[],original=spawnEnemy;
        spawnEnemy=function(type,x,y,opt){
          var e=original(type,x,y,opt||{});
          if(e)seen.push({type:type,t:+clock.toFixed(2),x:+e.x.toFixed(1),y:+e.y.toFixed(1),w:e.w,h:e.h});
          return e;
        };
        plan[wi].fn();
        for(var q=0;q<360;q++){clock+=1/120;aiQueueTick(1/120);}
        spawnEnemy=original;
        var touch=false;
        for(var a=0;a<seen.length;a++)for(var b=a+1;b<seen.length;b++){
          var A=seen[a],B=seen[b];
          /* Only simultaneous births can be fused.  Ordered ripples may reuse a lane safely. */
          if(Math.abs(A.t-B.t)<.02 && Math.abs(A.x-B.x)<(A.w+B.w)/2 && Math.abs(A.y-B.y)<(A.h+B.h)/2)touch=true;
        }
        out.push({at:plan[wi].t,spawns:seen,touchingAtBirth:touch});
      }
      return {stage:n,length:curStage.length,subboss:SUBBOSS[n],waves:out};
    }
    return JSON.stringify({s2:inspect(2),s3:inspect(3)});
  })()`)));

  async function show(stage,index,name,wait){
    await page.evaluate(({stage,index})=>eval(`(function(){
      beginStage(${stage});setState(GS.PLAY);player.reset();player.invuln=999;
      player.x=worldWidth()/2;player.y=VH*.82;mapScroll=levelScrollRange();snapCamToPlayer();
      stagePlan=[];waveIdx=0;subBossTriggered=true;subBossDone=true;aminiTriggered=true;
      bossWarned=true;enemies.length=0;eBullets.length=0;aiQueue.length=0;
      story=null;if(typeof thaw!=='undefined')thaw=null;
      var p=buildStagePlan(${stage});p[${index}].fn();
    })()`),{stage,index});
    await page.waitForTimeout(wait);
    await page.locator('#screen').screenshot({path:path.join(OUT,name+'.png')});
  }
  await show(2,2,'01_stage2_volcanic_ripple',360);
  await show(2,11,'02_stage2_volcano_crown',520);
  await show(3,0,'03_stage3_red_ice_jet_file',1150);
  await show(3,3,'04_stage3_cryo_support_file',520);
  await show(3,2,'05_stage3_green_cryo_naval_lanes',2600);

  const s2Types=[...new Set(audit.s2.waves.flatMap(w=>w.spawns.map(s=>s.type)))];
  const s3Types=[...new Set(audit.s3.waves.flatMap(w=>w.spawns.map(s=>s.type)))];
  const s2Allowed=new Set(['ash','skim','cinderwasp','lance','eye','magmaorb','basaltbomber','cruc',
    'crawl','miner','lavamaw','pod','carrier','golem','disc']);
  const s3Allowed=new Set(['sharddart','cryoeye','glaciercarrier','s3interceptor','s3barge']);
  const readiness=await page.evaluate(()=>['ndr_cinderwasp_idle_0','ndr_basaltbomber_idle_0',
    'ndr_magmaorb_idle_0','ndr_sharddart_idle_0','s3atk_barge_0'].reduce((o,k)=>(o[k]=XART.rdy(k),o),{}));
  const report={audit,s2Types,s3Types,readiness,errors};
  fs.writeFileSync(path.join(OUT,'report.json'),JSON.stringify(report,null,2));
  console.log(JSON.stringify(report,null,2));
  const gaps=audit.s2.waves.concat(audit.s3.waves).flatMap(w=>w.spawns.slice(1).map((s,i)=>s.t-w.spawns[i].t));
  const ok=audit.s2.waves.length===15 && audit.s3.waves.length===12 &&
    s2Types.every(t=>s2Allowed.has(t)) && s3Types.every(t=>s3Allowed.has(t)) &&
    s3Types.includes('sharddart')&&s3Types.includes('s3barge')&&s3Types.includes('cryoeye')&&
    s3Types.includes('glaciercarrier') &&
    audit.s2.waves.every(w=>!w.touchingAtBirth) && audit.s3.waves.every(w=>!w.touchingAtBirth) &&
    gaps.every(g=>g>=.15) && audit.s2.subboss.at===.45 && audit.s3.subboss.at===.45 && !errors.length;
  await browser.close();server.close();if(!ok)process.exitCode=1;
})().catch(e=>{console.error(e);server.close();process.exitCode=1;});
