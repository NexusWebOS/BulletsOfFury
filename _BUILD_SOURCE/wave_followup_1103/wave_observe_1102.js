/* QA-only: native Furious cadence, GOD observer, delayed input-only cleanup.
   Never loaded by production index. No enemy health/phase/attack writes. */
const WO16={units:[],byUnit:new WeakMap(),events:[],attempts:[],clock:0,stage:0,phase:'OBSERVE',lastInput:null,lastRelease:0,lastProgress:0,nextAdvance:0,nextMissile:0,firstFire:null,fireFrames:0,clearWindows:[],frames:0,frameMs:[],updateMs:[],drawMs:[],peakEnemies:0,peakBullets:0,peakClosePairs:0,peakGroundOverlap:0,earlyDamage:[],damageCalls:0,base:{spawn:spawnEnemy,hit:hitEnemy}};
function wo16Bounds(e){const w=e._drawW||e._actualDrawW||e.w||32,h=e._drawH||e._actualDrawH||e.h||32;return{x:e.x,y:e._drawY??e.y,w:Math.min(680,w),h:Math.min(900,h)};}
function wo16Combatant(e){return !!e&&!e.dead&&e._dyingT==null&&(!(e.prop||e._prop||e.pattern==='prop')||!!e._modTurret||e.type==='modturret');}
function wo16Visible(e){if(!wo16Combatant(e))return false;const r=wo16Bounds(e);return r.x+r.w*.5>=camLeftX()&&r.x-r.w*.5<=camRightX()&&r.y+r.h*.5>=viewTopY()&&r.y-r.h*.5<VH;}
function wo16Unit(e){let u=WO16.byUnit.get(e);if(!u){u={id:WO16.units.length,type:e.type,wave:WO16.active??WO16.current??null,born:WO16.clock,firstVisible:null,visible:0,lastHp:e.hp,maxHp:e.maxhp||e._maxhp||e.hp,minX:e.x,maxX:e.x,minY:e.y,maxY:e.y,firstTarget:null,lastSeen:WO16.clock,deadAt:null,lastAttack:0};WO16.units.push(u);WO16.byUnit.set(e,u);}return u;}
spawnEnemy=function(){const n=enemies.length,e=WO16.base.spawn.apply(this,arguments);if(WO16.stage)for(const a of enemies.slice(n))wo16Unit(a);return e;};
hitEnemy=function(e,dmg){const u=WO16.byUnit.get(e);if(u&&WO16.stage){WO16.damageCalls++;if(u.visible<8&&WO16.earlyDamage.length<100)WO16.earlyDamage.push({id:u.id,type:u.type,visible:u.visible,t:WO16.clock,phase:WO16.phase,bullet:typeof _dmgBullet!=='undefined'?_dmgBullet?.kind:null,dmg});}return WO16.base.hit.apply(this,arguments);};
WO16.start=function(stage,route='left'){
 ht27Stop();debugFight=null;coopOn=false;diffKey='furious';run.mode='arcade';DIFF=difficultyForRun('arcade','furious');run.pilot='yuri';pilotIndex=PILOTS.findIndex(p=>p.key==='yuri');PILOTMOD={...PILOTS[pilotIndex]};run.lives=3;run.contUsed=0;run.shield=0;
 beginStage(stage);setState(GS.PLAY);player.reset();BOFCinematicDirector.cancel();story=fb2Talk=fb2Intro=special=thunderStorm=s6Opening=null;H3.ending=null;H3.release=false;AP10_X.intro=null;P2M.active=null;FS11.pending=null;FS11.boxes=[];
 boss=null;bossActive=false;subBoss=null;subBossActive=false;subBossDone=subBossTriggered=aminiTriggered=true;bossWarned=false;warnT=0;warnKind=null;globalThis.BOF_REGULAR_WAVE_REVIEW=true;
 // Native ambient/onslaught/adaptive owners remain enabled. Preserve props,
 // orbital rocks, traffic gates, authored schedule, terrain and native timers.
 player.dead=player.out=false;player.alive=true;player.invuln=0;player.x=worldWidth()/2;player.y=VH-65;camX=player.x-VW/2;player.roll=player.somer=player._spin=player._voidDeath=null;
 run.weapon=0;run.wlevel=5;run.wlevels=WEAPONS.map(()=>5);run.bombs=40;debugUnlocked=true;DBGT.god=true;DBGT.speed=1;Input.mouse.active=false;
 Object.assign(WO16,{units:[],byUnit:new WeakMap(),events:[],attempts:[],clock:0,stage,route,phase:'OBSERVE',lastInput:null,lastRelease:0,lastProgress:0,nextAdvance:0,nextMissile:0,firstFire:null,fireFrames:0,clearWindows:[],frames:0,frameMs:[],updateMs:[],drawMs:[],peakEnemies:0,peakBullets:0,peakClosePairs:0,peakGroundOverlap:0,earlyDamage:[],damageCalls:0,active:null,allAt:null,done:false,expected:stagePlan.length,originalLength:curStage.length,baselineGodBlocks:DBGT.stats?.godBlocks||0});
 stagePlan=stagePlan.map((w,i)=>{const fn=w.fn;return{...w,fn:Object.assign(function(){WO16.active=i;const before=new Set(enemies);try{return fn.apply(this,arguments);}finally{const retry=waveIdx<i;WO16.attempts.push({i,t:stageTimer,clock:WO16.clock,retry});if(!retry&&!WO16.events.some(e=>e.i===i)){WO16.events.push({i,t:stageTimer,planned:w.t,clock:WO16.clock,video:typeof captureStart==='number'?(performance.now()-captureStart)/1000:null,map:mapScroll,meta:Object.fromEntries(Object.entries(w).filter(([k])=>k!=='fn')),types:enemies.filter(e=>!before.has(e)).map(e=>e.type),units:enemies.filter(e=>!before.has(e)).map(e=>({id:wo16Unit(e).id,type:e.type,model:e._s911?.model||e._s811?.model||e._s711?.model||e._s511?.model||e._v31?.model||e._i31?.model||e._s411?.model})),spawns:[]});WO16.lastRelease=WO16.clock;}WO16.active=null;}},fn)};});
 if(window.BOFOnline)window.BOFOnline.submitScore=()=>{};if(curStage.music)Audio.startMusic(curStage.music);return{stage,route,expected:WO16.expected,originalLength:curStage.length,minimumVisibleObservation:8,eliteObservation:18,ambientAndAdaptive:true,initialQuiet:12,nativeGod:DBGT.god};
};
function wo16Need(e,u){if(e._sc12||e._ca111||e.type==='cbreak'||e.hp>500)return 18;const a=e._ea11;if(a&&a.shots+a.beams+(a.ground||0)>0)return 8;return 12;}
function wo16Hold(K,binds,action,on){if(!on)return;const k=binds[action]?.find(k=>!k.startsWith('mouse'));if(k)K[k]=true;}
WO16.input=function(dt){
 WO16.clock+=dt;Input.clearTaps();for(const k of Object.keys(Input.keys))Input.keys[k]=false;const binds=keybindFor(1),K=Input.keys;
 if(WO16.clock>=WO16.nextAdvance&&(story||fb2Talk||fb2Intro||thaw||s6Wing?.choice&&!s6Wing.route)){if(s6Wing?.choice&&!s6Wing.route)Input.injectTap(binds[WO16.route][0]);if(story||fb2Talk||fb2Intro||thaw||s6Wing?.choice&&!s6Wing.route)Input.injectTap(binds.fire.find(k=>!k.startsWith('mouse'))||binds.fire[0]);WO16.nextAdvance=WO16.clock+2;}
 let visible=[];
 for(const e of enemies){const u=wo16Unit(e);if(e.dead||e._dyingT!=null){if(u.deadAt==null)u.deadAt=WO16.clock;continue;}u.lastSeen=WO16.clock;u.minX=Math.min(u.minX,e.x);u.maxX=Math.max(u.maxX,e.x);u.minY=Math.min(u.minY,e.y);u.maxY=Math.max(u.maxY,e.y);if(wo16Visible(e)){if(u.firstVisible==null)u.firstVisible=WO16.clock;u.visible+=dt;u.lastHp=e.hp;u.shots=e._ea11?.shots||0;u.beams=e._ea11?.beams||0;u.ground=e._ea11?.ground||0;u.actions=e._ea11?.actions||[];visible.push(e);}}
 const ready=visible.filter(e=>(WO16.mode==='CLEANUP'||wo16Unit(e).visible>=wo16Need(e,wo16Unit(e)))&&!e._noHit),targets=_lockTargets().filter(t=>t&&!t.dead&&t.hp>0&&t.y>viewTopY()+10&&t.y<VH-45&&t.x>=camLeftX()+4&&t.x<=camRightX()-4);
 const eligible=targets.filter(t=>{const e=t._retinaOwner||t._owner||t.owner||t;return ready.includes(e)||ready.some(e=>Math.abs(e.x-t.x)<Math.max(80,e.w||32)&&Math.abs(e.y-t.y)<Math.max(80,e.h||32));});
 function priority(t){return /hull|body|core/i.test(String(t.kind||t.name||''))?1:0;}eligible.sort((a,b)=>priority(a)-priority(b)||b.y-a.y);let target=eligible[WO16.targetIndex%Math.max(1,eligible.length)];if(target){const hp=target.hp;if(WO16.targetHp!=null&&hp<WO16.targetHp-.01)WO16.targetProgress=WO16.clock;if(WO16.clock-(WO16.targetProgress||0)>4&&eligible.length>1){WO16.targetIndex=(WO16.targetIndex+1)%eligible.length;target=eligible[WO16.targetIndex];WO16.targetProgress=WO16.clock;}WO16.targetHp=target.hp;}
 const tx=target?.x??(worldWidth()/2+Math.sin(WO16.clock*.23)*Math.min(165,worldWidth()*.25)),ty=VH-65;
 wo16Hold(K,binds,'left',player.x>tx+5);wo16Hold(K,binds,'right',player.x<tx-5);wo16Hold(K,binds,'up',player.y>ty+5);wo16Hold(K,binds,'down',player.y<ty-5);
 // Short, aimed cleanup pulses. Young ships in the shot corridor postpone fire.
 const young=target&&visible.some(e=>wo16Unit(e).visible<8&&Math.abs(e.x-player.x)<Math.max(42,(e.w||32)*.55)&&e.y<player.y);
 const fire=WO16.clock>=12&&!!target&&Math.abs(player.x-target.x)<22&&WO16.mode==='CLEANUP';
 WO16.phase=WO16.mode||'OBSERVE';wo16Hold(K,binds,'fire',fire);
 if(fire){WO16.fireFrames++;if(WO16.firstFire==null)WO16.firstFire=WO16.clock;const owner=target._retinaOwner||target._owner||target.owner||target,u=WO16.byUnit.get(owner);if(u&&u.firstTarget==null)u.firstTarget=WO16.clock;
  if(!WO16.clearWindows.length||WO16.clock-WO16.clearWindows.at(-1).end>.2)WO16.clearWindows.push({start:WO16.clock,end:WO16.clock,wave:u?.wave??null,type:owner.type||target.kind});else WO16.clearWindows.at(-1).end=WO16.clock;
  if((eligible.length>1||target._sc12||target._ca111||target.hp>180)&&WO16.clock>=WO16.nextMissile){wo16Hold(K,binds,'retina',true);Input.injectTap(binds.bomb.find(k=>!k.startsWith('mouse'))||binds.bomb[0]);WO16.nextMissile=WO16.clock+2;}}
 const live=visible.length,bullets=eBullets.filter(b=>!b.dead).length;WO16.peakEnemies=Math.max(WO16.peakEnemies,live);WO16.peakBullets=Math.max(WO16.peakBullets,bullets);
 const all=WO16.events.length===WO16.expected&&waveIdx>=stagePlan.length,pending=run.stage===6&&carrierAssaultPending111();if(all&&!WO16.allAt)WO16.allAt=WO16.clock;WO16.done=!!all&&!pending&&WO16.clock-WO16.allAt>24;
 WO16.lastInput={phase:WO16.phase,target:target?.type||target?.kind||null,targets:targets.length,eligible:eligible.length,visible:live,bullets,youngInCorridor:!!young,playerX:player.x,targetX:target?.x,targetHp:target?.hp,all,pending};
};
WO16.frame=function(gap,update,draw){WO16.frames++;WO16.frameMs.push(gap);WO16.updateMs.push(update);WO16.drawMs.push(draw);if(WO16.frameMs.length>600){WO16.frameMs.shift();WO16.updateMs.shift();WO16.drawMs.shift();}};
function wo16Summary(a){const s=[...a].sort((a,b)=>a-b),n=s.length;return{mean:n?a.reduce((a,b)=>a+b,0)/n:0,p95:n?s[Math.floor((n-1)*.95)]:0,p99:n?s[Math.floor((n-1)*.99)]:0,max:n?s[n-1]:0};}
WO16.snapshot=function(){return{clock:WO16.clock,stage:run.stage,state,stageTimer,waveIdx,expected:WO16.expected,events:WO16.events.length,dead:player.dead,god:DBGT.god,godBlocks:(DBGT.stats?.godBlocks||0)-WO16.baselineGodBlocks,done:WO16.done,allAt:WO16.allAt,map:mapScroll,input:WO16.lastInput,firstFire:WO16.firstFire,fireFrames:WO16.fireFrames,peakEnemies:WO16.peakEnemies,peakBullets:WO16.peakBullets,visibleUnits:WO16.units.filter(u=>u.firstVisible!=null).length,dialogs:{story:!!story,talk:!!fb2Talk,intro:!!fb2Intro,thaw:!!thaw,choice:!!s6Wing?.choice,route:s6Wing?.route},carriers:run.stage===6?[...CA111.completed]:[],assault:run.stage===6?{active:CA111.active?.key,queue:CA111.queue.map(q=>q.key),blocked:sc12Blocked(),events:CA111.events.slice(-6)}:null,mini:!!subBossActive,boss:!!bossActive,live:enemies.filter(e=>!e.dead&&e._dyingT==null).map(e=>({type:e.type,hp:e.hp,x:e.x,y:e.y,noHit:!!e._noHit})),perf:{frame:wo16Summary(WO16.frameMs),update:wo16Summary(WO16.updateMs),draw:wo16Summary(WO16.drawMs)}};};
globalThis.BOF_WAVE_OBSERVER=WO16;

// Approved per-wave inspection pacing. Each callback/AI is native; the next
// release is held. Camera seeks between cleared groups are inspection cuts,
// not a claim of ordinary campaign timing or natural overlap balance.
const wo16Start=WO16.start,wo16Input=WO16.input;
WO16.start=function(stage,route='left'){
 const r=wo16Start(stage,route);WO16.current=0;WO16.targetIndex=0;WO16.targetProgress=0;WO16.targetHp=null;WO16.mode='PREPARE';WO16.prepare=0;WO16.phaseStart=0;WO16.waveTimes=stagePlan.map(w=>w.t);WO16.waveMeta=[];WO16.references=WO16_MAPS['stage-'+stage+(stage===6&&route==='right'?'-right':'')];
 CP12.next=VP12.next=CP22.nextWave=CP22.nextFlyby=99999;_adaptiveSpawnT=99999;tryAdaptiveReinforcement=()=>{};s6OnslaughtTick=function(W,dt){W.combatTime=(W.combatTime||0)+dt;};
 stagePlan=stagePlan.map((w,i)=>{const f=w.fn;const paced=function(){const n=WO16.events.length,result=f.apply(this,arguments);if(WO16.events.length>n){WO16.current=i;WO16.mode='OBSERVE';WO16.phaseStart=WO16.clock;const ev=WO16.events.at(-1);ev.planned=WO16.waveTimes[i];WO16.waveMeta[i]={i,start:ev.video,clock:WO16.clock,observeUntil:null,cleanup:null,end:null};}return result;};return{...w,t:Infinity,fn:Object.assign(paced,f)};});
 return{...r,pacing:'One native authored wave at a time; observation then input-only cleanup',ambientAndAdaptive:false,normalCadence:false,camera:'Native recorded release locations; camera seeks between cleared wave groups'};
};
WO16.input=function(dt){
 if(WO16.mode==='PREPARE'){
  const ref=WO16.references[String(WO16.current)];stageTimer=ref.time;mapScroll=ref.map;_prevMapScroll=mapScroll;_lastScrollDy=0;
  if(WO16.prepare++>=2)stagePlan[WO16.current].t=ref.time;
 }
 if(WO16.mode==='OBSERVE'&&s6Wing?.ships)for(const q of s6Wing.ships){q.fcd=Math.max(q.fcd||0,1);q.missileCd=Math.max(q.missileCd||0,1);q.specialCd=Math.max(q.specialCd||0,1);}
 wo16Input(dt);
 const departedFixture=e=>e.y>VH+Math.max(80,wo16Bounds(e).h*.5+16)&&(WO16.byUnit.get(e)?.firstVisible!=null||e.prop||e._prop||e._modTurret||e.type==='modturret');
 const nativeLive=enemies.filter(e=>wo16Combatant(e)&&WO16.byUnit.get(e)?.wave===WO16.current&&!departedFixture(e));
 if(WO16.mode==='OBSERVE'){
  const big=nativeLive.some(e=>e._sc12||e._ca111||e.type==='cbreak'||e.hp>500),grace=big?18:8;
  if(WO16.clock-WO16.phaseStart>=grace){WO16.waveMeta[WO16.current].observeUntil=WO16.clock;WO16.waveMeta[WO16.current].cleanup=typeof captureStart==='number'?(performance.now()-captureStart)/1000:null;WO16.mode='CLEANUP';}
 }
 if(WO16.mode==='CLEANUP'&&nativeLive.length&&WO16.clock-WO16.waveMeta[WO16.current].observeUntil>60&&!nativeLive.some(e=>e._ca111||e._sc12)){WO16.waveMeta[WO16.current].blocked=nativeLive.map(e=>({type:e.type,hp:e.hp,x:e.x,y:e.y}));WO16.resetBlocked=true;WO16.mode='TAIL';WO16.tailStart=WO16.clock;}
 if(WO16.mode==='CLEANUP'&&!nativeLive.length){WO16.mode='TAIL';WO16.tailStart=WO16.clock;}
 if(WO16.mode==='TAIL'&&WO16.clock-WO16.tailStart>=2){
  const m=WO16.waveMeta[WO16.current];m.end=typeof captureStart==='number'?(performance.now()-captureStart)/1000:null;
  if(WO16.current+1>=WO16.expected)WO16.mode='DONE';
  else{if(WO16.resetBlocked){enemies=enemies.filter(e=>WO16.byUnit.get(e)?.wave!==WO16.current);WO16.resetBlocked=false;}WO16.current++;WO16.prepare=0;WO16.targetIndex=0;WO16.targetProgress=WO16.clock;WO16.targetHp=null;WO16.mode='PREPARE';enemies=enemies.filter(e=>!departedFixture(e));pBullets=[];eBullets=[];orbBeams=[];playerLocks=[];groundTargetingReset();run.weapon=0;run.wlevel=5;player._mgMuzT=0;}
 }
 WO16.done=WO16.mode==='DONE';WO16.phase=WO16.mode;WO16.lastInput.mode=WO16.mode;WO16.lastInput.wave=WO16.current;WO16.lastInput.elapsed=WO16.clock-WO16.phaseStart;
};

// Observation holds the actual allied missile/special owner, as well as MG cadence.
const wo16WingArsenal=s6WingArsenal;
s6WingArsenal=function(q,dt){if(WO16.stage===6&&WO16.mode==='OBSERVE')return;return wo16WingArsenal.apply(this,arguments);};
