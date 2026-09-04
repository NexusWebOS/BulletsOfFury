/* Deterministic browser capture for qa_pattern_lab_0901.html. */
const http=require('http');
const fs=require('fs');
const path=require('path');
let playwright;
try{playwright=require('playwright');}
catch(_){playwright=require(path.join(process.env.USERPROFILE,'.cache','codex-runtimes','codex-primary-runtime','dependencies','node','node_modules','playwright'));}
const {chromium}=playwright;

const ROOT=path.resolve(__dirname,'..');
const OUT=path.join(ROOT,'docs','proofs','pattern_lab_0901');
fs.mkdirSync(OUT,{recursive:true});
const MIME={'.html':'text/html','.js':'text/javascript','.css':'text/css','.png':'image/png','.jpg':'image/jpeg','.json':'application/json','.wav':'audio/wav','.mp3':'audio/mpeg'};
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
  const context=await browser.newContext({
    viewport:{width:600,height:640},
    recordVideo:{dir:OUT,size:{width:600,height:640}}
  });
  const page=await context.newPage();
  const video=page.video();
  const errors=[],missing=[];
  page.on('pageerror',e=>errors.push(String(e)));
  page.on('response',r=>{if(r.status()>=400)missing.push({status:r.status(),url:r.url()});});
  page.on('console',m=>{if(m.type()==='error'&&!/^Failed to load resource:/.test(m.text()))errors.push(m.text());});
  await page.goto(`http://127.0.0.1:${server.address().port}/_BUILD_SOURCE/qa_pattern_lab_0901.html`,
    {waitUntil:'domcontentloaded',timeout:30000});
  await page.waitForFunction(()=>window.__patternLabReady===true,null,{timeout:30000});

  const shots=[
    [3.8,'01_reserved_formation_tracers.png'],
    [10.9,'02_durable_anchor_cannon.png'],
    [15.8,'03_boss_reveal_recognition.png'],
    [19.0,'04_independent_hardpoint_mg.png'],
    [25.6,'05_two_lane_beam_corridor.png'],
    [31.8,'06_local_damage_state.png'],
    [35.4,'07_complete.png']
  ];
  for(const [t,name] of shots){
    await page.waitForFunction(v=>window.__patternLab&&window.__patternLab.t>=v,t,{timeout:15000});
    await page.screenshot({path:path.join(OUT,name)});
  }
  const state=await page.evaluate(()=>({
    lab:window.__patternLab,
    pilot:(typeof _pilotKey==='function')?_pilotKey():null,
    gameState:(typeof state!=='undefined')?state:null,
    gameFrames:window.__bofFrames||0
  }));
  await context.close();
  const recorded=await video.path();
  const webm=path.join(OUT,'lizzie_pattern_lab.webm');
  if(path.resolve(recorded)!==path.resolve(webm))fs.copyFileSync(recorded,webm);
  await browser.close();server.close();

  const relevantMissing=missing.filter(m=>!/favicon\.ico(?:$|\?)/.test(m.url));
  const report={...state,errors,missing:relevantMissing,recording:path.relative(ROOT,webm).replace(/\\/g,'/')};
  fs.writeFileSync(path.join(OUT,'report.json'),JSON.stringify(report,null,2));
  console.log(JSON.stringify(report,null,2));
  const ok=state.pilot==='lizzie'&&state.gameState==='play'&&state.lab&&state.lab.completed&&
    state.lab.metrics.maxShots>=18&&state.lab.metrics.intercepts>=1&&state.lab.metrics.beamDoors.every(n=>n===2)&&
    !errors.length&&!relevantMissing.length&&!(state.lab.errors||[]).length;
  if(!ok)process.exitCode=1;
})().catch(e=>{console.error(e);server.close();process.exitCode=1;});
