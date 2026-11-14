async cfg=>{
 const audio=Snd._audioCtx();await audio.resume();const mix=audio.createMediaStreamDestination(),analyser=audio.createAnalyser();analyser.fftSize=1024;const gain=audio.createGain();gain.gain.value=.5;analyser.connect(gain);gain.connect(mix);
 const seen=new WeakSet(),play=HTMLMediaElement.prototype.play;window.captureStats={peak:0,tapped:0,tapErrors:[],frames:0,playing:{},nativeCues:{},outputTaps:0};
 const graph=FILMAUDIO1111;graph.tap=analyser;for(const node of graph.before){if(node.context===audio&&!graph.seen.has(node)){graph.connect.call(node,analyser);graph.seen.add(node);captureStats.outputTaps++;}}graph.before.clear();
 HTMLMediaElement.prototype.play=function(){if(!seen.has(this)){try{if(!this._bofNode){const source=audio.createMediaElementSource(this),out=audio.createGain();out.gain.value=1;source.connect(out);out.connect(audio.destination);this._bofNode=out;}seen.add(this);captureStats.tapped++;}catch(e){captureStats.tapErrors.push(String(e));}}return play.apply(this,arguments);};
 const nativePlay=Snd.play;Snd.play=function(key){captureStats.nativeCues[key]=(captureStats.nativeCues[key]||0)+1;return nativePlay.apply(this,arguments);};
 const canvas=document.createElement('canvas');canvas.width=1280;canvas.height=844;const g=canvas.getContext('2d'),samples=new Float32Array(analyser.fftSize);window.reviewCapture=canvas;window.captureLive=true;
 const types=['video/mp4','video/mp4;codecs=avc1.42E01E,mp4a.40.2','video/webm;codecs=vp9,opus','video/webm;codecs=vp8,opus'],type=types.find(t=>MediaRecorder.isTypeSupported(t));if(!type)throw Error('No supported audible video recorder');
 const stream=canvas.captureStream(30);for(const t of mix.stream.getAudioTracks())stream.addTrack(t);window.reviewRecorder=new MediaRecorder(stream,{mimeType:type,videoBitsPerSecond:2000000,audioBitsPerSecond:128000});window.capturePending=Promise.resolve();
 reviewRecorder.onerror=e=>FILM1111.errors.push('Video recorder: '+(e.error?.message||e.message||'encoder error'));
 reviewRecorder.ondataavailable=e=>{if(!e.data.size)return;capturePending=capturePending.then(async()=>{const b=new Uint8Array(await e.data.arrayBuffer());let s='';for(let i=0;i<b.length;i+=32768)s+=String.fromCharCode(...b.subarray(i,i+32768));await saveCaptureChunk(btoa(s));captureStats.chunks=(captureStats.chunks||0)+1;});};reviewRecorder.start(1000);
 const A=FILM1111;A.config=cfg;A.start=performance.now();A.enabled=false;
 // Native run initialization occurs before this requested stage's entry. Only
 // this recording fixture seeds review equipment and native GOD assistance.
 run.mode='campaign';diffKey='furious';pilotIndex=PILOTS.findIndex(p=>p.key==='cole');startRun(1);BOFCinematicDirector.cancel();storySkip();
 run.mode='campaign';run.stage=cfg.stage;DIFF=difficultyForRun(run.mode,diffKey);run.weapon=3;run.wlevel=5;run.wlevels=WEAPONS.map(()=>5);run.spaceWeapon=0;run.spaceLevels=[5,5,5,5,5];run.bombs=40;run.missileLevel=2;debugUnlocked=true;DBGT.god=true;DBGT.speed=1;debugFight=null;Input.mouse.active=false;
 if(cfg.stage===8)run._l78Entry=1;beginStage(cfg.stage);
 // Stage entry installs its real space/ground loadout. Seed the documented
 // review equipment after that handoff, before the first recorded frame.
 if(spaceWeaponsActive()){run.spaceWeapon=0;run.spaceLevels=[5,5,5,5,5];run.wlevel=spaceWeaponLevel();}else{run.weapon=3;run.wlevel=5;run.wlevels=WEAPONS.map(()=>5);}
 const playerDamage=playerHit;playerHit=function(source){if(A.enabled&&run.stage===cfg.stage){captureStats.preventedHits=(captureStats.preventedHits||0)+1;captureStats.hitCauses??={};captureStats.hitCauses[source]=(captureStats.hitCauses[source]||0)+1;return;}return playerDamage.apply(this,arguments);};
 film1111ObservePlan();A.enabled=true;playerHit('recording-protection-check');captureStats.protectionVerified=!player.dead&&captureStats.preventedHits===1;if(!captureStats.protectionVerified)throw Error('Recording protection failed');
 function render(){if(!captureLive)return;try{film1111Input();}catch(e){if(A.errors.length<10)A.errors.push(String(e));}
  g.fillStyle=getComputedStyle(document.body).backgroundColor;g.fillRect(0,0,1280,844);for(const c of document.querySelectorAll('canvas')){if(!c.width||!c.height)continue;const r=c.getBoundingClientRect(),s=getComputedStyle(c);if(!r.width||!r.height||r.right<=0||r.left>=1280||r.bottom<=0||s.display==='none'||s.visibility==='hidden'||s.opacity==='0')continue;g.imageSmoothingEnabled=false;g.drawImage(c,r.x,r.y,r.width,r.height);}
  g.fillStyle='#07101c';g.fillRect(0,800,1280,44);g.fillStyle='#f4d380';g.font='15px sans-serif';g.textAlign='center';g.fillText('STAGE '+cfg.stage+' / FURIOUS / INVULNERABLE INPUT PILOT / NATIVE HEALTH & PROGRESSION / TIER-5 REVIEW LOADOUT',640,827);
  analyser.getFloatTimeDomainData(samples);for(const v of samples)captureStats.peak=Math.max(captureStats.peak,Math.abs(v));captureStats.frames++;requestAnimationFrame(render);
 }requestAnimationFrame(render);return{mimeType:type,difficulty:diffKey,stage:run.stage,mode:run.mode,pilot:run.pilot,god:DBGT.god,loadout:{weapon:run.weapon,level:run.wlevel,missiles:run.bombs},expected:stagePlan.length};
}
