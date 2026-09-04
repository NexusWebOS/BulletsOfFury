/* Browser proof for the Fury dialogue font, authored stage password face, and retired fonts. */
const http=require('http');
const fs=require('fs');
const path=require('path');
let playwright;
try{playwright=require('playwright');}
catch(_){playwright=require(path.join(process.env.USERPROFILE,'.cache','codex-runtimes','codex-primary-runtime','dependencies','node','node_modules','playwright'));}
const {chromium}=playwright;

const ROOT=path.resolve(__dirname,'..');
const OUT=path.join(ROOT,'docs','proofs','cinematic_password_fonts_0902');
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
  const page=await browser.newPage({viewport:{width:1040,height:760}}),errors=[],missing=[];
  page.on('pageerror',e=>errors.push(String(e)));
  page.on('console',m=>{if(m.type()==='error'&&!/^Failed to load resource:/.test(m.text()))errors.push(m.text());});
  page.on('response',r=>{if(r.status()>=400&&!/favicon\.ico/.test(r.url()))missing.push({status:r.status(),url:r.url()});});
  await page.goto(`http://127.0.0.1:${server.address().port}/index.html`,{waitUntil:'domcontentloaded',timeout:30000});
  await page.waitForFunction(()=>window.__bofFrames>8&&typeof bmfReady==='function'&&bmfReady('dialogue'),null,{timeout:30000});
  await page.evaluate(()=>{const f=pilotFont(6);if(f)void f.img;});
  await page.waitForFunction(()=>artReady(pilotFont(6)),null,{timeout:30000});

  const screenshot=async name=>page.locator('#screen').screenshot({path:path.join(OUT,name)});
  const password=await page.evaluate(()=>eval(`(function(){
    setState(GS.PASSWORD);pwInput='TURB';drawPassword.typing=true;drawPassword.sel=-1;
    var calls=0,orig=passwordStageText;passwordStageText=function(){calls++;return orig.apply(this,arguments);};
    drawPassword(0);passwordStageText=orig;
    var font=pilotFont(6),legacy=[];
    for(var p of ['img','cells'])for(var k in (BOFX[p]||{}))if(/^sfont[1-9]_|^ncm_font_|^bof_font/.test(k))legacy.push(p+':'+k);
    var old=bmfDraw,bmfCalls=0;bmfDraw=function(){bmfCalls++;return old.apply(this,arguments);};
    msgFaceUse('dialogue');msgText('BULLETS OF FURY!',VW/2,80,30,'#ffe082',1,1,.05);msgFaceUse(null);bmfDraw=old;
    return {stage:6,stageFontIdentity:font===ASSETS.stageArt['1'],stageFontReady:artReady(font),stageTextCalls:calls,
      legacyKeys:legacy,compactFamilyAbsent:!('bofFont' in ASSETS)&&!('bofFont' in BOF),centeredDialogueBmfCalls:bmfCalls,
      authoredStageFonts:Object.keys(ASSETS.stageArt||{})};
  })()`));
  await page.waitForTimeout(180);await screenshot('01_password_stage6_font.png');

  await page.evaluate(()=>eval(`(function(){run.mode='campaign';run.pilot='axel';hqSeen={};hqPlay('axel',function(){});hqLine=1;hqBeatT=.9;hqChars=999;})()`));
  await page.waitForFunction(()=>eval(`!!hqSc&&cinWarm(hqSc)`),null,{timeout:30000});
  await page.waitForTimeout(220);await screenshot('02_cinematic_dialogue_regular.png');

  const stress="Fury HQ confirms the dimensional corridor is destabilizing faster than predicted; maintain formation, protect the evacuation wing, and do not let the carrier cross the final beacon.";
  const hard="FURYHQDIMENSIONALOVERRIDESEQUENCEALPHAOMEGASEVEN must remain completely inside this dialogue window.";
  await page.evaluate(({stress,hard})=>eval(`(function(){
    hqSc={cast:['cole','decker'],destination:'hq',beats:[
      {who:'cole',motion:'formation',text:${JSON.stringify(stress)}},
      {who:'decker',motion:'formation',text:${JSON.stringify(hard)}}]};
    hqLine=0;hqBeatT=.9;hqChars=999;setState(GS.CUTSCENE);
  })()`),{stress,hard});
  await page.waitForFunction(()=>eval(`!!hqSc&&cinWarm(hqSc)`),null,{timeout:30000});
  await page.waitForTimeout(220);await screenshot('03_cinematic_dialogue_long_line.png');
  await page.evaluate(()=>{hqLine=1;hqBeatT=.9;hqChars=999;});
  await page.waitForTimeout(180);await screenshot('04_cinematic_dialogue_long_token.png');

  const fit=await page.evaluate(({stress,hard})=>eval(`(function(){
    msgFaceUse('dialogue');
    function cutMetrics(text){
      var CW=cutsceneViewWidth(),CH=VH,dx=Math.round(CW*.025),dy=Math.round(CH*.715),dw=Math.round(CW*.95),dh=Math.round(CH*.255);
      var padX=dw*.055,inW=dw-padX*2,room=dh*.52,maxH=Math.max(13,Math.round(CH*.031));
      var L=msgBlockLayout(text,inW,room,maxH,8,1.31,.055),widest=Math.max(0,...L.lines.map(x=>msgMeasure(x,L.H,.055)));
      return {text:text,H:L.H,rows:L.lines.length,height:L.height,room:room,widest:widest,width:inW,
        fits:L.height<=room+.01&&widest<=inW+.01};
    }
    var corpus=[];for(var pk in PILOT_OPENINGS)for(var beat of PILOT_OPENINGS[pk].beats)if(beat.text)corpus.push(beat.text);
    var storyLines=[];(function walk(v){if(!v)return;if(Array.isArray(v)){if(v.length>=2&&typeof v[0]==='string'&&typeof v[1]==='string')storyLines.push(v[1]);for(var q of v)walk(q);}else if(typeof v==='object')for(var k in v)walk(v[k]);})(BOFX.story);
    var all=corpus.concat(storyLines),checked=all.map(cutMetrics),stressRows=[cutMetrics(${JSON.stringify(stress)}),cutMetrics(${JSON.stringify(hard)})];
    msgFaceUse(null);
    return {dialogueReady:bmfReady('dialogue'),openingLines:corpus.length,storyLines:storyLines.length,
      failed:checked.filter(x=>!x.fits),stress:stressRows};
  })()`),{stress,hard});

  const retiredSheetsAbsent=Array.from({length:8},(_,i)=>path.join(ROOT,'assets','game','fonts',`bof_font${i+1}.png`)).every(p=>!fs.existsSync(p));
  const report={password,fit,retiredSheetsAbsent,errors,missing};
  fs.writeFileSync(path.join(OUT,'report.json'),JSON.stringify(report,null,2));
  console.log(JSON.stringify(report,null,2));
  await browser.close();server.close();
  const ok=password.stageFontIdentity&&password.stageFontReady&&password.stageTextCalls>=30&&password.legacyKeys.length===0&&
    password.compactFamilyAbsent&&password.centeredDialogueBmfCalls===1&&password.authoredStageFonts.length===5&&retiredSheetsAbsent&&
    fit.dialogueReady&&fit.failed.length===0&&fit.stress.every(x=>x.fits)&&
    errors.length===0&&missing.length===0;
  if(!ok)process.exitCode=1;
})().catch(e=>{console.error(e);server.close();process.exitCode=1;});
