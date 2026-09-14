/* Focused browser regression: every SPECIAL-crate outcome produces a real audible cue. */
'use strict';
const http=require('http'),fs=require('fs'),path=require('path');
let playwright;
try{playwright=require('playwright');}
catch(_){playwright=require(path.join(process.env.USERPROFILE,'.cache','codex-runtimes','codex-primary-runtime',
  'dependencies','node','node_modules','playwright'));}
const {chromium}=playwright;
const ROOT=path.resolve(__dirname,'..');
const OUT=path.join(ROOT,'docs','proofs','special_pickup_audio_0831');
fs.mkdirSync(OUT,{recursive:true});
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
  await page.waitForFunction(()=>window.__bofFrames>12&&typeof Snd!=='undefined'&&Snd&&Snd.pools.specialAbilityPickup&&
    Snd.pools.megaShieldPickup,null,{timeout:30000});
  /* A real gesture opens the same media gate a player opens at boot. */
  await page.locator('#screen').click({position:{x:30,y:30}});
  await page.evaluate(()=>{Audio.init();Snd.prepare(['specialAbilityPickup','megaShieldPickup']);});
  await page.waitForFunction(()=>Snd.pools.specialAbilityPickup.list[0].readyState>=2&&
    Snd.pools.megaShieldPickup.list[0].readyState>=2,null,{timeout:30000});

  const routing=await page.evaluate(()=>eval(`(function(){
    beginStage(1);setState(GS.PLAY);player.reset();player.invuln=9999;
    stagePlan=[{t:9999,fn:function(){}}];waveIdx=0;enemies.length=0;eBullets.length=0;
    pBullets.length=0;powerups.length=0;boss=null;bossActive=false;subBoss=null;subBossActive=false;
    var calls=[],old=Snd.play;
    Snd.play=function(name){calls.push(name);return true;};
    var pilots=['axel','cole','decker','falva','freezer','juggernaut','lizzie','maverick','yuri'];
    var nativeRoutes={};
    for(var i=0;i<pilots.length;i++){
      run.pilot=pilots[i];special=null;startSpecial();
      nativeRoutes[pilots[i]]=calls[calls.length-1];
      if(special)endSpecial();
    }
    var before=calls.length;
    run.pilot='cole';applyPowerup({kind:'sonicbox',x:player.x,y:player.y});
    run.pilot='lizzie';applyPowerup({kind:'lzmgbox',x:player.x,y:player.y});
    run.pilot='decker';applyPowerup({kind:'dkshotbox',x:player.x,y:player.y});
    var loanRoutes=calls.slice(before);
    Snd.play=old;
    return {nativeRoutes:nativeRoutes,loanRoutes:loanRoutes,
      specialNative:Snd.TAME.specialAbilityPickup.native===true,
      axelNative:Snd.TAME.megaShieldPickup.native===true,
      specialSrc:Snd.pools.specialAbilityPickup.list[0].src,
      axelSrc:Snd.pools.megaShieldPickup.list[0].src};
  })()`));

  async function playback(name){
    const before=await page.evaluate(name=>{const p=Snd.pools[name],a=p.list[p.i];
      window.__specialQaAudio=a;Snd.play(name);return {ready:a.readyState,node:!!a._bofNode};},name);
    await page.waitForTimeout(320);
    const after=await page.evaluate(()=>({time:window.__specialQaAudio.currentTime,
      paused:window.__specialQaAudio.paused,ended:window.__specialQaAudio.ended,
      node:!!window.__specialQaAudio._bofNode,volume:window.__specialQaAudio.volume}));
    return {before,after};
  }
  const specialPlayback=await playback('specialAbilityPickup');
  await page.waitForTimeout(350); // clear the independent cue throttle
  const axelPlayback=await playback('megaShieldPickup');

  /* Visual sanity: confirm the grant leaves the player in a valid active-special play state. */
  await page.evaluate(()=>eval(`(function(){run.pilot='yuri';special=null;startSpecial();})()`));
  await page.waitForTimeout(160);
  await page.locator('#screen').screenshot({path:path.join(OUT,'01_special_pickup_active.png')});

  const report={routing,specialPlayback,axelPlayback,errors};
  fs.writeFileSync(path.join(OUT,'report.json'),JSON.stringify(report,null,2));
  console.log(JSON.stringify(report,null,2));
  const routes=Object.values(routing.nativeRoutes);
  const ok=routes.length===9&&routes[0]==='megaShieldPickup'&&routes.slice(1).every(x=>x==='specialAbilityPickup')&&
    routing.loanRoutes.length===3&&routing.loanRoutes.every(x=>x==='specialAbilityPickup')&&
    routing.specialNative&&routing.axelNative&&specialPlayback.after.time>0.05&&axelPlayback.after.time>0.05&&
    !specialPlayback.after.node&&!axelPlayback.after.node&&!errors.length;
  await browser.close();server.close();if(!ok)process.exitCode=1;
})().catch(e=>{console.error(e);server.close();process.exitCode=1;});
