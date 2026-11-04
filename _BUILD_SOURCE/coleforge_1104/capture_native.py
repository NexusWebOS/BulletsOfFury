from native_common import *
clips=json.loads((W/'capture-receipt.json').read_text())['clips']if len(sys.argv)>1 and(W/'capture-receipt.json').exists()else[];clips=[c for c in clips if c['mode']not in sys.argv[1:]];errors=[]
with sync_playwright()as pw:
 for mode in (sys.argv[1:]or['spread','plasma','effects']):
  b=pw.chromium.launch(channel='msedge',headless=True,args=['--autoplay-policy=no-user-gesture-required'])
  p=b.new_page(viewport={'width':1700,'height':1050});p.on('pageerror',lambda e:(errors.append(str(e)),print('ERROR '+str(e),flush=True)))
  p.on('console',lambda m:errors.append(m.text[:300])if m.type=='error'or'DRAW ERROR'in m.text else None)
  p.route('**/assets/online-config.js',lambda r:r.fulfill(status=200,body='window.BOF_ONLINE_CONFIG={};',content_type='application/javascript'))
  p.goto('http://127.0.0.1:65042/game/index.html?quality=high&cf114=film',wait_until='load',timeout=180000);p.wait_for_function('window.__bofFrames>4',timeout=60000);p.evaluate(TRAP_RAF)
  p.evaluate(SETUP,{'stage':5,'diff':'furious','pilot':'cole'})
  p.evaluate('''()=>{CP12.next=VP12.next=CP22.nextWave=CP22.nextFlyby=999999;_adaptiveSpawnT=999999;tryAdaptiveReinforcement=()=>{};subBossDone=subBossTriggered=aminiTriggered=true;curStage={...curStage,length:99999};gravityMode={...GRAVITY_SHIP_ACTIVE,narrative:false};furyShipWarm();run.spaceWeapon=3;run.spaceLevels=[1,1,1,1,1];sa114Warm();cfx114Warm(5);Snd.setVol('music',.22);Snd.setVol('sfx',.9);Snd.setVol('master',.9);}''')
  keys=p.evaluate('Object.values(CF114_ART.banks).map(B=>B.key)');warm(p,keys)
  p.mouse.click(700,500);p.evaluate('async()=>{await Snd._audioCtx().resume();Snd.prepare(["spaceLaserCannon","spaceLaserHit","atomicDetonate","nuclearDetonate"]);}')
  p.evaluate('''mode=>{window.qaMode=mode;window.qaStart=performance.now();window.qaNext=0;window.qaPart=-1;window.qaFilmStats={frames:0,peak:0,cues:[],parts:[],gaps:[],last:performance.now()};
   const play=Snd.play;Snd.play=function(k){qaFilmStats.cues.push(k);return play.apply(this,arguments);};
   window.qaFilm=document.createElement('canvas');qaFilm.width=1712;qaFilm.height=1112;window.qaFilmCtx=qaFilm.getContext('2d');
   window.qaBefore=function(t){const sec=(t-qaStart)/1000,part=Math.floor(sec/(mode==='effects'?2.4:2.8));
    if(mode!=='effects'){
     run.spaceWeapon=mode==='spread'?3:4;run.spaceLevels[run.spaceWeapon]=clamp(part+1,1,5);run.wlevel=spaceWeaponLevel();
     if(t>=qaNext){pShoot();qaNext=t+_weaponCadence()*1000;}
     if(part!==qaPart){powerups=[];const p={kind:'weapon',spaceType:run.spaceWeapon,wtype:run.spaceWeapon,x:player.x+115,y:player.y-120,vy:0,t:0,w:36,h:36};powerups.push(p);}
    }else if(part!==qaPart){
     CFX114.fx=[];explosions=[];smokeTrails=[];shockRings=[];_smokeRings=[];atomBooms=[];nukeImpacts=[];
     const x=player.x,y=player.y-170;
     if(part===0){explode(x,y,22,'red');spawnSmokeRing(x,y,70);spawnShockRing(x,y,70,'fire');cfx114Spawn('small',x,y,64);}
     if(part===1){cfx114Spawn('column',x,y,256);cfx114Spawn('fire',x,y,96);cfx114Spawn('smoke',x+95,y+20,96);}
     if(part===2)nukeAt(x,y);
     if(part===3)atomBlast(x,y);
     if(part===4){window.qaShield={x,y,w:62,h:62,_esh:{family:'bubble_hex',phase:'deploy',animT:0,hitT:0}};}
     if(part===5){window.qaShield={x,y,w:62,h:62,_esh:{family:'bubble_toxic',phase:'deploy',animT:0,hitT:0}};}
    }
    if(qaShield&&mode==='effects'){qaShield._esh.animT+=1/60;if(qaShield._esh.animT>.335)qaShield._esh.phase='active';}
    if(part!==qaPart){qaFilmStats.parts.push({part,sec,level:spaceWeaponLevel()});qaPart=part;}
    qaFilmStats.frames++;qaFilmStats.gaps.push(t-qaFilmStats.last);qaFilmStats.last=t;qaFilmStats.peak=Math.max(qaFilmStats.peak,pBullets.length);
   };
   window.qaShield=null;
   window.qaAfter=function(){if(qaShield){ctx.save();ctx.setTransform(SS,0,0,SS,0,0);const v=viewZoom();ctx.scale(v,v);ctx.translate(-camX,VH*(1-v)/v);drawEnemyShieldLayer(qaShield,true);ctx.restore();}
    const g=qaFilmCtx;g.fillStyle='#03080d';g.fillRect(0,0,1712,1112);g.drawImage(cv,376,88);
    g.drawImage(document.getElementById('siege-left'),0,88);g.drawImage(document.getElementById('siege-right'),1336,88);
    g.drawImage(document.getElementById('hud28-stage'),0,0);g.drawImage(document.getElementById('hud28-encounter'),1336,0);
   };
   const raf=__bofRealRAF,original=__bofPendingRAF;window.requestAnimationFrame=cb=>raf(t=>{qaBefore(t);cb(t);qaAfter();});
   const audio=Snd._audioCtx(),dest=audio.createMediaStreamDestination();aq112Tap().connect(dest);window.qaAnalyser=audio.createAnalyser();aq112Tap().connect(qaAnalyser);window.qaPeak=0;
   const stream=new MediaStream([...qaFilm.captureStream(30).getVideoTracks(),...dest.stream.getAudioTracks()]);const mime='video/webm;codecs=vp9,opus',chunks=[],rec=new MediaRecorder(stream,{mimeType:mime,videoBitsPerSecond:7000000});rec.ondataavailable=e=>{if(e.data.size)chunks.push(e.data);};window.qaRec={rec,chunks,mime};rec.start(500);original(performance.now());
  }''',mode)
  for i in range(4):
   p.wait_for_timeout(3600)
   data=p.evaluate('()=>{const a=new Float32Array(qaAnalyser.fftSize);qaAnalyser.getFloatTimeDomainData(a);qaPeak=Math.max(qaPeak,...a.map(Math.abs));return{t:stageTimer,frames:qaFilmStats.frames,level:spaceWeaponLevel(),shots:pBullets.length,error:window.__bofDrawError,peak:qaPeak};}')
   print(mode,i,data,flush=True)
   if i==1:
    (W/(mode+'-native.png')).write_bytes(base64.b64decode(p.evaluate('qaFilm.toDataURL().split(",")[1]')))
  with p.expect_download(timeout=30000)as d:
   p.evaluate('''async mode=>{const R=qaRec;await new Promise(r=>{R.rec.onstop=r;R.rec.stop();});const blob=new Blob(R.chunks,{type:R.mime}),a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download=mode+'.webm';a.click();}''',mode)
  d.value.save_as(W/(mode+'.webm'))
  receipt=p.evaluate('()=>({frames:qaFilmStats.frames,parts:qaFilmStats.parts,peakShots:qaFilmStats.peak,meanGap:qaFilmStats.gaps.reduce((a,b)=>a+b,0)/qaFilmStats.gaps.length,maxGap:Math.max(...qaFilmStats.gaps),cues:[...new Set(qaFilmStats.cues)],audioPeak:qaPeak,drawError:window.__bofDrawError,audioErrors:AQ112.errors})');receipt['mode']=mode;receipt['bytes']=(W/(mode+'.webm')).stat().st_size;clips.append(receipt);(W/'capture-receipt.json').write_text(json.dumps({'clips':clips,'errors':errors},indent=2),encoding='utf8');b.close()
