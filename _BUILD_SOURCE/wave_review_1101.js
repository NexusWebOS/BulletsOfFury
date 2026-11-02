/* QA-only regular-wave review, never shipped in index.html.
   Native wave callbacks, AI, ordnance, damage and authored scene art remain live.
   Encounter directors are disabled for this requested regular-wave-only film. */
globalThis.WR15={events:[],attempts:[],spawned:[],clock:0,serial:0,seen:new WeakMap(),ready:new WeakMap(),stage:0,done:false,errors:[],base:{spawn:spawnEnemy},active:null};
spawnEnemy=function(){const e=WR15.base.spawn.apply(this,arguments);if(e&&WR15.stage){WR15.spawned.push({wave:WR15.active,type:e.type,clock:WR15.clock,hp:e.hp});}return e;};
WR15.start=function(stage,route='left'){
 EA11.setup(stage,'furious');const originalLength=curStage.length,plan=stagePlan;
 Object.assign(WR15,{events:[],attempts:[],spawned:[],clock:0,serial:0,seen:new WeakMap(),ready:new WeakMap(),stage,done:false,errors:[],active:null,originalLength,expected:plan.length,lastInput:null,allAt:null,nextAdvance:0,nextMissile:0,route});
 // Suppress only encounter entry, retaining the original level duration,
 // background clock and native pressure/traffic gates. No encounter HP,
 // phase or attack clock is written by the observer.
 globalThis.BOF_REGULAR_WAVE_REVIEW=true;bossWarned=false;subBossTriggered=subBossDone=aminiTriggered=true;warnT=0;warnKind=null;
 // The requested finite wave book excludes endless adaptive reinforcements.
 // Their extra traffic would obscure each authored formation's review window.
 CP12.next=VP12.next=CP22.nextWave=CP22.nextFlyby=99999;_adaptiveSpawnT=99999;
 tryAdaptiveReinforcement=()=>{};
 s6OnslaughtTick=function(W,dt){W.combatTime=(W.combatTime||0)+dt;};
 story=thaw=fb2Talk=fb2Intro=null;BOFCinematicDirector.cancel();playerLocks=[];
 run.weapon=0;run.wlevel=5;run.wlevels=WEAPONS.map(()=>5);run.bombs=40;run.lives=20;debugUnlocked=true;DBGT.god=true;DBGT.speed=1;player.invuln=0;Input.mouse.active=false;
 stagePlan=plan.map((w,i)=>{const native=w.fn;return{...w,fn:function(){
  WR15.active=i;const before=new Set(enemies),sp=WR15.spawned.length;let out;
  try{out=native.apply(this,arguments);}finally{
   const retry=waveIdx<i;WR15.attempts.push({i,t:stageTimer,clock:WR15.clock,retry});
   if(!retry&&!WR15.events.some(q=>q.i===i))WR15.events.push({i,t:stageTimer,planned:w.t,clock:WR15.clock,video:typeof captureStart==='number'?(performance.now()-captureStart)/1000:null,map:mapScroll,meta:Object.fromEntries(Object.entries(w).filter(([k])=>k!=='fn')),fnMeta:{...native},types:enemies.filter(e=>!before.has(e)).map(e=>e.type),units:enemies.filter(e=>!before.has(e)).map(e=>({type:e.type,model:e._s911?.model||e._s811?.model||e._s711?.model||e._s511?.model||e._v31?.model||e._i31?.model||e._s411?.model})),spawns:WR15.spawned.slice(sp).map(e=>e.type)});
   WR15.active=null;
  }return out;
 }};});
 if(curStage.music)Audio.startMusic(curStage.music);return{stage,originalLength,expected:plan.length};
};
WR15.input=function(dt){
 WR15.clock+=dt;Input.clearTaps();for(const k of Object.keys(Input.keys))Input.keys[k]=false;
 if(WR15.clock>=WR15.nextAdvance&&(story||fb2Talk||fb2Intro||thaw||s6Wing?.choice&&!s6Wing.route)){const binds=keybindFor(1);if(s6Wing?.choice&&!s6Wing.route)Input.injectTap(binds[WR15.route][0]);Input.injectTap(binds.fire.find(k=>!k.startsWith('mouse'))||binds.fire[0]);WR15.nextAdvance=WR15.clock+.75;}
 const live=enemies.filter(e=>!e.dead&&e._dyingT==null&&!e.prop&&!e._prop&&e.pattern!=='prop');
 const targets=_lockTargets().filter(e=>e&&!e.dead&&e.hp>0&&e.y>PLAY.y+15&&e.y<VH-45&&e.x>=camLeftX()-10&&e.x<=camRightX()+10);
 for(const e of targets)if(!WR15.ready.has(e))WR15.ready.set(e,WR15.clock);
 const t=targets.sort((a,b)=>b.y-a.y)[0],x=t?.x??worldWidth()/2,y=VH-60,K=Input.keys;
 K.a=player.x>x+5;K.d=player.x<x-5;K.w=player.y>y+5;K.s=player.y<y-5;
 K.j=!!t&&WR15.clock-(WR15.ready.get(t)||0)>.65;
 K.c=K.j&&!!t&&(t._sc12||t._ca111||t.hp>180);
 if(K.j&&WR15.clock>=WR15.nextMissile){const binds=keybindFor(1);Input.injectTap(binds.bomb.find(k=>!k.startsWith('mouse'))||binds.bomb[0]);WR15.nextMissile=WR15.clock+.9;}
 const all=WR15.events.length===WR15.expected&&waveIdx>=stagePlan.length,pending=run.stage===6&&carrierAssaultPending111();
 if(all&&!WR15.allAt)WR15.allAt=WR15.clock;
 // A wave film reviews releases and their combat tail, rather than requiring
 // every escaped/upstream survivor to die after finite scenery stops scrolling.
 // The Stage6 assault queue still owns its complete encounter sequence.
 WR15.done=!!all&&!pending&&WR15.clock-WR15.allAt>18;
 WR15.lastInput={target:t?.type||null,targets:targets.length,live:live.length,all,pending};
};
WR15.snapshot=function(){return{clock:WR15.clock,stage:run.stage,state,stageTimer,waveIdx,expected:WR15.expected,events:WR15.events.length,dead:player.dead,done:WR15.done,allAt:WR15.allAt,map:mapScroll,input:WR15.lastInput,dialogs:{story:!!story,talk:!!fb2Talk,intro:!!fb2Intro,thaw:!!thaw,choice:!!s6Wing?.choice,route:s6Wing?.route},carriers:run.stage===6?[...CA111.completed]:[],assault:run.stage===6?{active:CA111.active?.key,queue:CA111.queue.map(q=>q.key),blocked:sc12Blocked(),events:CA111.events.slice(-8)}:null,mini:!!subBossActive,boss:!!bossActive,live:enemies.filter(e=>!e.dead&&e._dyingT==null).map(e=>({type:e.type,hp:e.hp,x:e.x,y:e.y,noHit:!!e._noHit}))};};
