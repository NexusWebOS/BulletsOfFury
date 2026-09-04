/* Browser proof for the nine pilot-selected campaign flight openings. */
const http=require('http');
const fs=require('fs');
const path=require('path');
let playwright;
try{playwright=require('playwright');}
catch(_){playwright=require(path.join(process.env.USERPROFILE,'.cache','codex-runtimes','codex-primary-runtime','dependencies','node','node_modules','playwright'));}
const {chromium}=playwright;

const ROOT=path.resolve(__dirname,'..');
const OUT=path.join(ROOT,'docs','proofs','pilot_openings_0901');
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
  await page.waitForFunction(()=>window.__bofFrames>8&&typeof bmfReady==='function'&&bmfReady('dialogue'),null,{timeout:30000});

  const pilots=['axel','freezer','cole','falva','maverick','yuri','juggernaut','lizzie','decker'];
  const branch=[];
  for(let i=0;i<pilots.length;i++){
    const pilot=pilots[i];
    const routed=await page.evaluate(p=>eval(`(function(){
      run.mode='campaign';run.pilot=${JSON.stringify(p)};hqSeen={};var continued=false;
      var started=hqTrigger('pre',1,function(){continued=true;});
      return {started:started,continued:continued,selected:hqSc===PILOT_OPENINGS[${JSON.stringify(p)}],
        cast:(hqSc&&hqSc.cast||[]).slice(),destination:hqSc&&hqSc.destination,
        beats:hqSc&&hqSc.beats.length,dialogue:hqSc&&hqSc.beats.filter(function(b){return !!b.text;}).length};
    })()`),pilot);
    await page.waitForFunction(()=>eval(`!!hqSc&&cinWarm(hqSc)`),null,{timeout:30000});
    await page.evaluate(()=>eval(`(function(){
      var at=hqSc.beats.findIndex(function(b){return !!b.text;});hqLine=Math.max(0,at);hqBeatT=.9;hqChars=999;
    })()`));
    await page.waitForTimeout(150);
    await page.locator('#screen').screenshot({path:path.join(OUT,String(i+1).padStart(2,'0')+'_'+pilot+'_dialogue.png')});

    const audit=await page.evaluate(()=>eval(`(function(){
      msgFaceUse('dialogue');var W=cutsceneViewWidth(),H=VH,dw=Math.round(W*.95),dh=Math.round(H*.255),
        padX=dw*.055,bodyW=dw-padX*2,bodyH=dh*.52,rows=[];
      for(var b of hqSc.beats)if(b.text){
        var L=msgBlockLayout(b.text,bodyW,bodyH,Math.max(13,Math.round(H*.031)),8,1.31,.055);
        var widest=Math.max.apply(Math,[0].concat(L.lines.map(function(x){return msgMeasure(x,L.H,.055);})));
        rows.push({who:b.who,text:b.text,H:L.H,lines:L.lines.length,height:L.height,room:bodyH,widest:widest,width:bodyW,
          fits:L.height<=bodyH+.01&&widest<=bodyW+.01});
      }
      var pilotReady=cinAllPilots(hqSc).every(function(p){for(var v=1;v<=7;v++)if(!XART.rdy(cinShipKey(p,v)))return false;return true;});
      msgFaceUse(null);return {dialogueFace:bmfReady('dialogue'),pilotReady:pilotReady,rows:rows,failed:rows.filter(function(r){return !r.fits;})};
    })()`));
    branch.push(Object.assign({pilot},routed,audit));
  }

  /* Representative action states: generated airbursts/projectiles, banking, cloaking and departure. */
  const actionProofs=[
    ['cole','dogfight',.95],['maverick','missile_lock',.95],['decker','cloak',.95],['falva','duo_attack',.95],
    ['axel','hq_approach',.62],['axel','hq_approach',1.72],['axel','hq_approach',2.92],
    ['freezer','jungle_approach',1.72]
  ];
  for(let i=0;i<actionProofs.length;i++){
    const [pilot,motion,shotT]=actionProofs[i];
    await page.evaluate(({pilot,motion,shotT})=>eval(`(function(){
      run.mode='campaign';run.pilot=${JSON.stringify(pilot)};hqSeen={};hqPlay(${JSON.stringify(pilot)},function(){});
      var at=hqSc.beats.findIndex(function(b){return b.motion===${JSON.stringify(motion)};});hqLine=Math.max(0,at);hqBeatT=${JSON.stringify(shotT)};hqChars=999;
    })()`),{pilot,motion,shotT});
    await page.waitForFunction(()=>eval(`!!hqSc&&cinWarm(hqSc)`),null,{timeout:30000});
    await page.waitForTimeout(110);
    await page.locator('#screen').screenshot({path:path.join(OUT,'action_'+String(i+1).padStart(2,'0')+'_'+pilot+'_'+motion+'.png')});
  }

  const routing=await page.evaluate(()=>eval(`(function(){
    hqSc=null;run.mode='campaign';var postContinued=false,wrongStageContinued=false;
    var postStarted=hqTrigger('post',1,function(){postContinued=true;});
    var wrongStarted=hqTrigger('pre',2,function(){wrongStageContinued=true;});
    return {oldTableRemoved:typeof HQ_SCENES==='undefined',postStarted:postStarted,postContinued:postContinued,
      wrongStarted:wrongStarted,wrongStageContinued:wrongStageContinued,openingKeys:Object.keys(PILOT_OPENINGS)};
  })()`));
  const report={branch,routing,errors,missing};
  fs.writeFileSync(path.join(OUT,'report.json'),JSON.stringify(report,null,2));
  console.log(JSON.stringify(report,null,2));
  await browser.close();server.close();
  const ok=branch.length===9&&branch.every(r=>r.started&&!r.continued&&r.selected&&r.beats>=4&&r.dialogue>=2&&
      r.dialogueFace&&r.pilotReady&&r.failed.length===0)&&routing.oldTableRemoved&&
      !routing.postStarted&&routing.postContinued&&!routing.wrongStarted&&routing.wrongStageContinued&&
      routing.openingKeys.length===9&&errors.length===0&&missing.length===0;
  if(!ok)process.exitCode=1;
})().catch(e=>{console.error(e);server.close();process.exitCode=1;});
