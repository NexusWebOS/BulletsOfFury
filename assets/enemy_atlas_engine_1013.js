/* Read-only field guide adapter. Gameplay code and artwork remain the actual game. */
(()=>{'use strict';
 const clock=window.BOF_ATLAS_CLOCK;if(!clock)return;
 const A={entry:null,actor:null,seen:new Map(),error:null,started:0,difficulty:'normal',autoReplay:true,serial:0,muted:true};
 function mute(on){A.muted=!!on;try{Audio.setVol('master',on?0:.65);Snd.setVol('master',on?0:.65);}catch(_){} }
 function healthControl(){const b=A.actor;return !!(b?.maxhp&&!['_cargo13','_s7mod','_s7warden','_mr27','_xenoRig','_fz','_rebels','_mm1003','_s9fusion','_v24'].some(k=>b[k]));}
 // The musical password fights retain their native cue table and attack owner.
 // Preview time owns the soundtrack cursor so pausing/stepping cannot skip cues.
 const nativeHammerClock=ht27Clock,nativeHammerLocked=ht27Locked;
 ht27Clock=function(d,dt){if(!A.entry)return nativeHammerClock.apply(this,arguments);const a=ht27A();d.clock=((d.clock||0)+dt)%a.seconds;d.energy=a.envelope[Math.min(a.envelope.length-1,Math.floor(d.clock*a.envelopeFPS))]||0;return d.clock;};
 ht27Locked=function(){if(!A.entry)return nativeHammerLocked.apply(this,arguments);const d=ht27Data();return d?d.mode==='intro'||d.locked||(!ht27CombatSequence(boss)&&ht27WantLock(d.clock)):false;};
 function syncMusic(){const d=ht27Data();if(!d?.musicStarted)return;const m=ht27Song();if(!m)return;if(clock.paused||A.muted){if(!m.paused)m.pause();return;}m.playbackRate=clock.speed;if(Number.isFinite(m.duration)&&Math.abs(m.currentTime-d.clock)>.2)m.currentTime=d.clock;if(m.paused)m.play()?.catch(()=>{});}
 function isolate(){
  BOFCinematicDirector.cancel();story=null;debugFight=null;stagePlan=[];spawnClock=9999;waveIdx=9999;stageTimer=1;
  warnT=0;subBossTriggered=true;subBossDone=true;stageEnding=false;bossDefeated=false;bossWarned=true;
  fb2Talk=null;s6Opening=null;if(typeof wfx!=='undefined'&&wfx)wfx.fseq=null;
  if(typeof VP12!=='undefined')VP12.next=99999;if(typeof CP12!=='undefined')CP12.next=99999;
  if(typeof EP13!=='undefined'){EP13.owner=null;EP13.next=0;EP13.clock=2;}
  player.invuln=1e9+2;player.dead=false;player.out=false;player.x=camLeftX()+viewW()*.5;player.y=PLAY.y+PLAY.h*.84;
  setState(GS.PLAY);
 }
 const sleep=ms=>new Promise(r=>setTimeout(r,ms));
 function finishRadio(b){
  story=null;fb2Talk=null;H3.release=false;
  if(b?._hammer){b._fb2IntroSeen=true;if(typeof fb2Intro!=='undefined'&&fb2Intro&&!fb2Intro.done)fb2IntroEnd();}
  if(b?._rebels){const R=b._rebels;if(!R.rf)rf28Init(b,R);R.frIntro={done:true,t:30,beat:99};R.frRadio=null;b._noHit=false;}
  if(b?._s7mod&&!b._s7mod.tank){const M=b._s7mod;if(!M._mission29IntroDone){M._mission29IntroDone=true;M.t=0;if(b._s7warden?.final)b._s7warden.final.radio=null;}}
 }
 async function start(entry,difficulty='normal',preserveSound=false){
  const ticket=++A.serial;A.entry=entry;A.error=null;A.actor=null;A.seen.clear();A.difficulty=difficulty;A.loading=true;A.elapsed=0;if(!preserveSound)clock.paused=false;
  const s=entry.spawn||{},stage=s.stage||entry.stages?.[0]||1;
  try{
   BOFDEBUG.lab.on(Math.min(9,stage),'cole',difficulty);isolate();boss=null;subBoss=null;bossActive=false;subBossActive=false;
   if(stage===10){run.stage=10;curStage=STAGES.find(v=>v.n===10)||curStage;}
   mute(preserveSound?A.muted:true);ep13Warm?.();const artKeys=(entry.artKeys||[]).filter(k=>XART._src[k]||BOFX.cells[k]||BOFX.img[k]);for(const k of artKeys)XART.rdy(k);
   if(s.kind==='warhive'&&typeof SC13!=='undefined')for(const k of SC13.keys)XART.rdy(k);
   for(let n=0;n<160;n++){stageLoadTick?.();if(stageLoadReady?.()!==false)break;await sleep(40);if(ticket!==A.serial)return;}
   for(let n=0;n<240&&artKeys.some(k=>!XART.rdy(k));n++){await sleep(25);if(ticket!==A.serial)return;}
   if(ticket!==A.serial)return;
   isolate();BOFDEBUG.clear();
   if(s.method==='enemy'){
    A.actor=BOFDEBUG.spawn(s.type,camLeftX()+viewW()*.5,PLAY.y+PLAY.h*.24,s.options||{});
    if(A.actor?.err)throw new Error(A.actor.err);
    A.actor._ai27={seen:1,visible:true,flinch:0};
    if(A.actor._mm1003){A.actor._mm1003.phase='rest';A.actor._mm1003.stagger=0;}
   }else if(s.method==='encounter'||s.method==='rebel'){
    A.actor=on5LaunchEncounter({stage:Math.min(9,stage),role:s.role||'boss',kind:s.method==='rebel'?'rebelsquad':s.kind,phase:s.phase,mimic:s.mimic});
    if(s.method==='rebel'){
     const key=s.pilot||s.key||s.type;
     for(const q of A.actor._rebels.ships){if(q.key!==key){q.dead=true;q.hp=0;}else{q.x=camLeftX()+viewW()*.5;q.y=q.homeY=140;q.mode='fight';q.cd=.6;}}
    }
   }else if(s.method==='password'){
    pwInput=s.password||s.code;submitPassword();diffKey=difficulty;startRun(stage);isolate();A.actor=bossActive?boss:subBossActive?subBoss:null;
    if(['HARR6','REBEL6','XHARR','XREBEL'].includes(s.password)){GP4.route=s.password.includes('REBEL')?'right':'left';GP4.stage6Only=!s.password.startsWith('X');GP4.routeReady=true;gp4QuickEncounter();A.actor=boss;
     for(let n=0;n<240&&!A.actor;n++){await sleep(50);if(ticket!==A.serial)return;A.actor=bossActive?boss:subBossActive?subBoss:null;}
    }
    if(!A.actor&&s.kind)A.actor=on5LaunchEncounter({stage,role:s.role||'boss',kind:s.kind,phase:s.phase,mimic:s.mimic});
    if(!A.actor)throw new Error('Password encounter did not create an opponent: '+(s.password||s.code));
   }else throw new Error('No BOF scene adapter for '+s.method);
   if(ticket!==A.serial)return;
   finishRadio(A.actor);
   A.started=stateT;A.elapsed=0;A.lastT=stateT;player.invuln=1e9+2;mute(A.muted);return snapshot();
  }catch(e){A.error=String(e.message||e);return {error:A.error};}finally{if(ticket===A.serial)A.loading=false;}
 }
 function snapshot(){const b=A.actor;return {ready:!!ASSETS.ready,entry:A.entry?.id,error:A.error,elapsed:A.elapsed||0,frames:clock.frames,paused:clock.paused,speed:clock.speed,muted:A.muted,healthControl:healthControl(),
  actor:b?{type:b.type||b.kind,hp:b.hp,maxhp:b.maxhp,dead:!!b.dead,x:b.x,y:b.y,phase:b._ep13?.phase||b.phase,pattern:b._ep13?.kind||b._cargo13?.mode||b._er26?.mode||b._s7mod?.mode||b._hammer?.state||b._mm1003?.phase||b._r30?.mode||b._sbPat||b._pat||b.pat}:null,
  projectiles:[...A.seen.keys()],liveProjectiles:eBullets.length,activeBeams:b?._cargo13?.lasers?.filter(l=>l.t>=l.warm&&l.t<l.warm+l.fire).length||0,stage:run.stage};}
 function after(){if(!A.entry||A.error||A.loading)return;
  A.elapsed=(A.elapsed||0)+Math.max(0,stateT-(A.lastT||stateT));A.lastT=stateT;
  if(A.entry.spawn.method!=='enemy'){if(!A.actor)A.actor=bossActive?boss:subBossActive?subBoss:null;finishRadio(A.actor);}
  player.invuln=1e9+2;stageTimer=Math.min(stageTimer,2);waveIdx=999;spawnClock=9999;
  syncMusic();
  for(const b of eBullets)if(!b.dead&&!A.seen.has(b.kind)){A.seen.set(b.kind,{...b,owner:null,_owner:null});}
  if(A.autoReplay&&A.entry.spawn.method==='enemy'&&A.elapsed>4&&(!enemies.includes(A.actor)||A.actor.dead||A.actor.y>VH+100||A.actor.y< -150)){start(A.entry,A.difficulty,true);}
 }
 clock.after=after;
 function pattern(kind){if(!A.actor||!EP13.families[run.stage]?.[A.actor.type])return false;if(A.actor._ep13)ep13Cancel(A.actor,'guide selection');A.actor._ep13Cycles=0;A.actor.x=camLeftX()+viewW()*.5;A.actor.y=PLAY.y+PLAY.h*.24;ep13Start(A.actor,kind);return true;}
 function image(key,target){if(!XART.rdy(key))return false;const im=XART.get(key),c=target.getContext('2d');c.clearRect(0,0,target.width,target.height);c.imageSmoothingEnabled=false;const z=Math.min(target.width/im.width,target.height/im.height);c.drawImage(im,(target.width-im.width*z)/2,(target.height-im.height*z)/2,im.width*z,im.height*z);return true;}
 const backup=document.createElement('canvas');
 function projectiles(tiles){if(!tiles?.length)return;const source=document.getElementById('screen');if(!source)return;
  if(backup.width!==source.width||backup.height!==source.height){backup.width=source.width;backup.height=source.height;}backup.getContext('2d').drawImage(source,0,0);
  const oldE=eBullets,oldP=pBullets;
  try{pBullets=[];
   for(const {kind,canvas}of tiles){
    let b=A.seen.get(kind);if(!b){eBullets=[];b=eShootT(VW/2,VH/2,Math.PI/2,2,kind,{silent:true,noMuzzle:true});if(!b)continue;if(typeof S9A!=='undefined'&&S9A[kind]){b._s9a=kind;b._noArsenal=true;}}
    eBullets=[{...b,x:VW/2,y:VH/2,t:stateT,_ph:0,dead:false,_launchDelay:0}];
    ctx.save();ctx.setTransform(SS,0,0,SS,0,0);ctx.clearRect(0,0,VW,VH);drawBullets();ctx.restore();
    const c=canvas.getContext('2d');c.imageSmoothingEnabled=false;c.clearRect(0,0,canvas.width,canvas.height);c.drawImage(source,(VW/2-40)*SS,(VH/2-40)*SS,80*SS,80*SS,0,0,canvas.width,canvas.height);
   }
  }finally{eBullets=oldE;pBullets=oldP;ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.clearRect(0,0,source.width,source.height);ctx.drawImage(backup,0,0);ctx.restore();}
 }
 window.BOF_ENEMY_ATLAS={start,snapshot,pattern,image,projectiles,mute,
  pause(on){clock.paused=!!on;syncMusic();},speed(n){clock.speed=Math.max(.25,Math.min(2,+n||1));syncMusic();},step(){clock.paused=true;clock.steps++;syncMusic();},
  target(x,y){player.x=camLeftX()+clamp(x,0,1)*viewW();player.y=PLAY.y+clamp(y,0,1)*PLAY.h;},
  hp(ratio){const b=A.actor;if(healthControl())b.hp=Math.max(1,b.maxhp*clamp(ratio,.01,1));},
  get patterns(){return A.actor?EP13.families[run.stage]?.[A.actor.type]||[]:[];},
  get entry(){return A.entry;},get ready(){return !!ASSETS.ready;}
 };mute(true);
})();
