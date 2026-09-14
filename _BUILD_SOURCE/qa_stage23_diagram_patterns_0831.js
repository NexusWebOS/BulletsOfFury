/* Browser proof for Mike's Level-2/3 hand-drawn boss lane and safe-zone diagrams. */
const http=require('http');
const fs=require('fs');
const path=require('path');
let playwright;
try{playwright=require('playwright');}
catch(_){playwright=require(path.join(process.env.USERPROFILE,'.cache','codex-runtimes','codex-primary-runtime',
  'dependencies','node','node_modules','playwright'));}
const {chromium}=playwright;
const ROOT=path.resolve(__dirname,'..');
const OUT=path.join(ROOT,'docs','proofs','stage23_diagram_patterns_0831');
fs.mkdirSync(OUT,{recursive:true});
const MIME={'.html':'text/html','.js':'text/javascript','.css':'text/css','.png':'image/png','.jpg':'image/jpeg',
  '.wav':'audio/wav','.mp3':'audio/mpeg','.json':'application/json'};
const server=http.createServer((req,res)=>{
  const rel=decodeURIComponent((req.url||'/').split('?')[0]).replace(/^\/+/, '')||'index.html',file=path.resolve(ROOT,rel);
  if(!file.startsWith(ROOT)){res.writeHead(403);res.end();return;}
  fs.readFile(file,(err,data)=>{if(err){res.writeHead(404);res.end();return;}
    res.writeHead(200,{'Content-Type':MIME[path.extname(file).toLowerCase()]||'application/octet-stream'});res.end(data);});
});

(async()=>{
  await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
  const browser=await chromium.launch({headless:true,executablePath:'C:/Program Files/Google/Chrome/Application/chrome.exe',
    args:['--autoplay-policy=no-user-gesture-required']});
  const page=await browser.newPage({viewport:{width:1100,height:820}}),errors=[];
  page.on('pageerror',e=>errors.push(String(e)));
  await page.goto(`http://127.0.0.1:${server.address().port}/index.html`,{waitUntil:'domcontentloaded',timeout:30000});
  await page.waitForFunction(()=>window.__bofFrames>12,null,{timeout:30000});await page.keyboard.press('Enter');
  async function clear(n){await page.evaluate(n=>eval(`(function(){
    beginStage(${n});setState(GS.PLAY);player.reset();player.invuln=99999;player.x=240;player.y=438;
    stagePlan=[{t:9999,fn:function(){}}];waveIdx=0;stageTimer=0;mapScroll=levelScrollRange();snapCamToPlayer();
    enemies.length=0;eBullets.length=0;pBullets.length=0;aiQueue.length=0;powerups.length=0;
    boss=null;bossActive=false;subBoss=null;subBossActive=false;story=null;
  })()`),n);}
  await page.evaluate(()=>{for(let i=0;i<12;i++){XART.rdy('l23fx_inferno_laser_'+i);XART.rdy('l23fx_rime_laser_'+i);XART.rdy('mwfx_flamethrower_'+i);}});
  await page.waitForFunction(()=>XART.rdy('l23fx_inferno_laser_4')&&XART.rdy('l23fx_rime_laser_4')&&XART.rdy('mwfx_flamethrower_4'),null,{timeout:15000});

  /* Boss1: left-to-right, one vertical laser per station. */
  await clear(2);
  await page.evaluate(()=>eval(`(function(){
    spawnBoss('infernoreaver');boss.enter=false;boss.x=worldWidth()/2;boss.y=112;boss.ty=112;boss.fireCd=999;
    infernoReaverPassStart(boss,1);boss._irPass.phase='pass';boss._irPass.t=.01;boss.x=boss._irPass.startX;
  })()`));
  await page.waitForTimeout(250);
  const forward=await page.evaluate(()=>({dir:boss._irPass.dir,index:boss._irPass.index,x:boss.x,
    angle:boss._l23Beam&&boss._l23Beam.angles[0],slot:boss._l23Beam&&boss._l23Beam.slots[0]}));
  await page.locator('#screen').screenshot({path:path.join(OUT,'01_level2_forward_vertical_station.png')});

  /* Boss2: exact mirrored return pass. */
  await clear(2);
  await page.evaluate(()=>eval(`(function(){
    spawnBoss('infernoreaver');boss.enter=false;boss.x=worldWidth()/2;boss.y=112;boss.ty=112;boss.fireCd=999;
    infernoReaverPassStart(boss,2);boss._irPass.phase='pass';boss._irPass.t=.01;boss.x=boss._irPass.startX;
  })()`));
  await page.waitForTimeout(250);
  const reverse=await page.evaluate(()=>({dir:boss._irPass.dir,index:boss._irPass.index,x:boss.x,
    angle:boss._l23Beam&&boss._l23Beam.angles[0],slot:boss._l23Beam&&boss._l23Beam.slots[0]}));
  await page.evaluate(()=>{story=null;});
  await page.locator('#screen').screenshot({path:path.join(OUT,'02_level2_reverse_vertical_station.png')});

  /* Flame1: centred +/-45-degree douse and analytically verified corner safety corridors. */
  await clear(2);
  await page.evaluate(()=>eval(`(function(){
    spawnBoss('magmaward');shipBossInit(boss,'magmaward');boss.enter=false;boss.x=worldWidth()/2;boss.y=112;boss.ty=112;boss.fireCd=999;
    magmaWardStartAttack(boss,'magmaflame',1,1);boss.x=boss._mwAttack.homeX;boss.y=boss._mwAttack.homeY;
    boss._mwAttack.t=boss._mwAttack.tell+.28;
  })()`));
  await page.waitForTimeout(120);
  const douse=await page.evaluate(()=>eval(`(function(){
    const A=boss._mwAttack,left=camX,corners=[[left+34,280],[left+VW-34,280],[left+34,VH-54],[left+VW-34,VH-54]],saved=A.poseRot;
    function touched(pt){for(let i=0;i<=180;i++){const rel=-L2_DOUSE_ARC+2*L2_DOUSE_ARC*i/180;
      A.poseRot=rel;const C=shipBossMount(boss,'C'),a=Math.PI/2+rel;
      const h=magmaWardPointSegment(pt[0],pt[1],C.x,C.y,C.x+Math.cos(a)*240,C.y+Math.sin(a)*240);
      if(h.d<=lerp(11,36,h.u)+10)return true;}return false;}
    const cornerSafe=corners.map(p=>!touched(p));A.poseRot=saved;
    return {angle:Math.PI/2+A.poseRot,arc:L2_DOUSE_ARC,cornerSafe:cornerSafe,x:boss.x,y:boss.y};
  })()`));
  await page.locator('#screen').screenshot({path:path.join(OUT,'03_level2_centered_safe_douse.png')});

  /* Basic blue pattern: Cryo Spear's L/C/R lanes are separately timed and straight. */
  await clear(3);
  await page.evaluate(()=>eval(`(function(){
    spawnBoss('rimewall');shipBossInit(boss,'rimewall');boss.enter=false;boss.x=worldWidth()/2;boss.y=112;boss.ty=112;boss.fireCd=999;
    stage3BossAttack(boss,'s3spearburst',1,0,1);stage3BossTick(boss,.02);
  })()`));
  await page.waitForTimeout(250);
  const spear=await page.evaluate(()=>({order:boss._s3boss.cannonSeq&&boss._s3boss.cannonSeq.slots.slice(),
    angle:boss._l23Beam&&boss._l23Beam.angles[0],slot:boss._l23Beam&&boss._l23Beam.slots[0]}));
  await page.evaluate(()=>{story=null;thaw=null;});
  await page.locator('#screen').screenshot({path:path.join(OUT,'04_level3_miniboss_first_vertical_lane.png')});

  /* Rime Wall uses the longer mirrored five-lane sequence before its giant centre orb. */
  await clear(3);
  await page.evaluate(()=>eval(`(function(){
    spawnBoss('cryospear');boss.enter=false;boss.x=worldWidth()/2;boss.y=112;boss.ty=112;boss.fireCd=999;
    stage3BossAttack(boss,'s3wallcannons',2,0,1);stage3BossTick(boss,.02);
  })()`));
  await page.waitForTimeout(320);
  const wall=await page.evaluate(()=>({order:boss._s3boss.cannonSeq&&boss._s3boss.cannonSeq.slots.slice(),
    angle:boss._l23Beam&&boss._l23Beam.angles[0],slot:boss._l23Beam&&boss._l23Beam.slots[0],
    giantAfter:boss._s3boss.cannonSeq&&boss._s3boss.cannonSeq.finishCharge}));
  await page.evaluate(()=>{story=null;thaw=null;});
  await page.locator('#screen').screenshot({path:path.join(OUT,'05_level3_boss_first_vertical_lane.png')});

  const report={forward,reverse,douse,spear,wall,errors};
  fs.writeFileSync(path.join(OUT,'report.json'),JSON.stringify(report,null,2));console.log(JSON.stringify(report,null,2));
  const vertical=x=>x&&Math.abs(x.angle-Math.PI/2)<.00001;
  const ok=forward&&forward.dir===1&&vertical(forward)&&reverse&&reverse.dir===-1&&vertical(reverse)&&
    douse&&Math.abs(douse.angle-Math.PI/2)<=douse.arc+.00001&&douse.cornerSafe.every(Boolean)&&
    spear&&spear.order.join(',')==='L,C,R'&&vertical(spear)&&wall&&wall.order.join(',')==='R,C,L,C,R'&&vertical(wall)&&wall.giantAfter&&!errors.length;
  await browser.close();server.close();if(!ok)process.exitCode=1;
})().catch(e=>{console.error(e);server.close();process.exitCode=1;});
