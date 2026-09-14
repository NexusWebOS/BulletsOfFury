/* Focused browser regression: Stage 9 and its rival sequence use the approved song. */
'use strict';
const http=require('http'),fs=require('fs'),path=require('path');
let playwright;
try{playwright=require('playwright');}
catch(_){playwright=require(path.join(process.env.USERPROFILE,'.cache','codex-runtimes','codex-primary-runtime',
  'dependencies','node','node_modules','playwright'));}
const {chromium}=playwright;
const ROOT=path.resolve(__dirname,'..');
const MIME={'.html':'text/html','.js':'text/javascript','.css':'text/css','.png':'image/png',
  '.jpg':'image/jpeg','.wav':'audio/wav','.mp3':'audio/mpeg','.json':'application/json'};
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
  const page=await browser.newPage({viewport:{width:900,height:760}});
  const errors=[];page.on('pageerror',e=>errors.push(String(e)));
  await page.goto(`http://127.0.0.1:${server.address().port}/index.html`,
    {waitUntil:'domcontentloaded',timeout:30000});
  await page.waitForFunction(()=>window.__bofFrames>12&&typeof Snd!=='undefined'&&Snd&&
    Snd.music.bonus&&Snd.music.rival,null,{timeout:30000});
  await page.locator('#screen').click({position:{x:30,y:30}});

  async function playback(name){
    await page.evaluate(name=>{Audio.init();Audio.startMusic(name);},name);
    await page.waitForFunction(name=>Snd.cur===Snd.music[name]&&Snd.cur.readyState>=2,name,{timeout:30000});
    await page.waitForTimeout(420);
    return page.evaluate(name=>({
      key:name,
      src:Snd.music[name].getAttribute('src'),
      currentTime:Snd.music[name].currentTime,
      paused:Snd.music[name].paused,
      readyState:Snd.music[name].readyState,
      isCurrent:Snd.cur===Snd.music[name]
    }),name);
  }
  const bonus=await playback('bonus');
  const rival=await playback('rival');
  const report={bonus,rival,errors};
  console.log(JSON.stringify(report,null,2));
  const expected='assets/game/music/stage9_rival_dog_showdown.mp3';
  const ok=[bonus,rival].every(x=>x.src===expected&&x.currentTime>0.05&&!x.paused&&
    x.readyState>=2&&x.isCurrent)&&!errors.length;
  await browser.close();server.close();if(!ok)process.exitCode=1;
})().catch(e=>{console.error(e);server.close();process.exitCode=1;});
