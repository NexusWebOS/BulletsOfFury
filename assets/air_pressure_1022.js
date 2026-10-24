"use strict";
/* Bounded crossing waves and committed flyby attacks. Stage/boss/cinematic
   clocks, native projectile collision, evasions and explosion reels stay native. */
const CP22={age:0,nextWave:8,nextFlyby:5,waves:0,serial:0,pending:[],events:[],radio:0,
 base:{begin:beginStage,play:updatePlay,tick:s6StormTick,flight:fb2FlightTick,spawnFlight:fb2FlightSpawn,
  plan:fb2FlightPlan,draw:drawEnemy,entry:enemyEntrySweep,frenzy:enemyFrenzyTick,pose:bf22State,blit:af21Draw,end:ai27End,load:stageLoadBegin}};
for(const S of Object.values(CP22_ART.sheets))XART._src[S.key]=S.path;
for(const [id,M] of Object.entries(CP22_ART.models)){
 BF22_ART.models[id]=M;AF21_ART.models[id]=M;for(const alias of M.aliases)BF22.aliases.set(M.stages[0]+'|'+alias,{id,M});
}
Object.assign(BF22_ART.effects,CP22_ART.effects);
stageLoadBegin=function(n,keys){const extra=n===8?Object.values(CP22_ART.herald).map(B=>B.key):[];return CP22.base.load.call(this,n,[...(keys||[]),...extra]);};
function cp22Log(event,data={}){CP22.events.push({event,t:CP22.age,...data});if(CP22.events.length>200)CP22.events.shift();}
function cp22Rank(){return target17Rank();}
function cp22Free(){return state===GS.PLAY&&run.stage===6&&!run._gp4StageX&&!story&&!s6q13Scene()&&!radio17Live()&&!RADIO17.hold&&!bossActive&&!subBossActive&&!(warnT>0)&&!bossWarned&&!bossDefeated;}
function cp22Sound(e,cue,interval=.15){return combatAudio0927(e,cue,interval);}
const CP22_CUES=['jetDash','enemyMachineGunLight','atomicLaunch','atomicDetonate','bossWeaponCharge','combatAlien0927','combatToxic0927','bossfireVileexistence','expSmall'];
Snd.prepare?.(CP22_CUES.map(n=>{const a=CA15.aliases[n]||n;return window.BOF_CHIP_PASS?.aliases[a]||a;}));
function cp22Say(text){
 if(CP22.radio>0||!s6Wing||s6Wing.line)return;
 const allies=s6Wing.ships.filter(q=>q.phase==='fight'&&!q.dead);if(!allies.length)return;
 s6WingSay(allies[CP22.waves%allies.length].key.toUpperCase(),text);CP22.radio=8;cp22Log('ally-radio',{text});
}
function cp22DashSpawn(side,y){
 if(!cp22Free())return null;const L=camLeftX(),R=camRightX(),rank=cp22Rank(),e=spawnEnemy('s6dart',side>0?L-65:R+65,y);
 if(!e)return null;
 for(const k of ['_fb2Stealth','_s6Strike','_mission29','_jetManeuver','_esh','_entrySweep','_esw','_s6Act'])delete e[k];
 Object.assign(e,{type:'cp22dasher',pattern:'s6storm',_s6storm:'s6dart',_noSep:true,_noHit:false,_frFlight:false,
  shoots:false,fk:null,vx:0,vy:0,spin:0,w:42,h:32,_stagger:0});
 e.hp=e.maxhp=e._maxhp=EHP(6);e.score=620;
 e._cp22Dash={phase:'tell',t:0,warm:[1.18,1.02,.90,.80,.76][rank],side,y,from:e.x,end:side>0?R+50:L-50,
  a:side>0?0:Math.PI,speed:[610,720,820,900,930][rank],left:L,right:R};
 cp22Log('dasher-tell',{side,y,warm:e._cp22Dash.warm});return e;
}
function cp22DashTick(e,dt){
 const D=e._cp22Dash;if(!D||e.dead||e._dyingT!=null)return;
 e._frFlight=false;e._noHit=false;e.spin=0;e.shoots=false;D.t+=dt;
 if(D.phase==='tell'){
  combatWarningTick(e,'cp22-dash',D.t,D.warm);
  if(D.t>=D.warm){D.phase='dash';D.t=0;cp22Sound(e,'jetDash',.5);cp22Log('dasher-launch',{side:D.side,y:e.y});}
  return;
 }
 const x=e.x;e.x+=D.side*D.speed*dt;e.y=D.y;e._bf22FireAt=efxClock;
 const L={x,y:e.y,ex:e.x,ey:e.y,width:22};
 for(const seat of seatList())withSeat(seat,()=>{if(!player.dead&&s81003Distance(player.x,player.y,L)<15)playerHit('Tempest Dasher');});
 if(D.side>0?e.x>D.end:e.x<D.end){
  e.x=clamp(e.x,camLeftX()-8,camRightX()+8);e.dead=true;e.hp=0;e.shoots=false;
  groundTargetingCancel(e);unitDeathFX(e,'jet','red');cp22Sound(e,'expSmall',.2);cp22Log('dasher-edge-detonation',{side:D.side});
 }
}
s6StormTick=function(e,dt){if(e._cp22Dash)return cp22DashTick(e,dt);return CP22.base.tick.apply(this,arguments);};
enemyEntrySweep=function(e){if(e?._cp22Dash||e?._cp22Sewer)return;return CP22.base.entry.apply(this,arguments);};
enemyFrenzyTick=function(e){if(e?._cp22Dash||e?._cp22Sewer)return;return CP22.base.frenzy.apply(this,arguments);};
ai27End=function(e,previous){
 if(e?._ai27&&(e._cp22Dash||e._cp22Sewer&&['tell','fire'].includes(e._cp22Sewer.phase)||e._cp22Flight&&['tell','fire'].includes(e._cp22Flight.phase)))e._ai27.dx=0;
 return CP22.base.end.apply(this,arguments);
};
bf22State=function(e,kind,value){
 if(e?._cp22Dash)return {kind:e._cp22Dash.phase==='dash'?'attack':'idle',value:e._cp22Dash.phase==='dash'?(e._cp22Dash.t*3)%1:0};
 return CP22.base.pose.apply(this,arguments);
};
af21Draw=function(p){
 const e=BF22.actor,D=e?._cp22Dash,F=e?._cp22Flight;
 if(p?.M?._bf22&&(D||F?.mode==='charge'&&F.phase==='fire'))p={...p,rotation:(D?D.a:F.angle)-Math.PI/2};
 return CP22.base.blit.call(this,p,...Array.prototype.slice.call(arguments,1));
};
function cp22DashDraw(e){const D=e._cp22Dash;if(e.dead||e._dyingT!=null)return;
 if(D.phase==='tell'){
  const x=D.side>0?D.left+2:D.right-2,ex=D.side>0?D.right:D.left;
  combatWarningDraw(e,{x,y:D.y,ex,ey:D.y,width:64,progress:clamp(D.t/D.warm,0,1),fieldOnly:true});
 }else{
  const B=CP22_ART.effects.dasher_turbo;if(!B||!XART.rdy(B.key))return;const im=XART.get(B.key),f=Math.floor(D.t*B.fps)%B.frames;
  ctx.save();ctx.translate(e.x,e.y);ctx.rotate(D.a-Math.PI/2);ctx.imageSmoothingEnabled=false;ctx.globalAlpha=.65+.3*Math.sin(D.t*65)**2;
  ctx.drawImage(im,...B.cells[f],-24,-85,48,64);ctx.restore();
 }
}
function cp22HullDraw(e){
 const A=bf22Model(e);if(!A)return false;const oldActor=BF22.actor,oldRoot=BF22.root,oldSelection=BF22.selection,oldAlias=AF21.aliases.get(e.type);
 BF22.actor=e;BF22.root=ctx.getTransform();BF22.selection=bf22State(e,'idle',0);AF21.aliases.set(e.type,A);
 try{const p=af21Pose(e.type,'idle',0);if(!p)return false;p.rotation=e._cp22Dash?e._cp22Dash.a-Math.PI/2:e.spin||0;
  return af21Draw(p,e.x,e.y,bf22Span(e,A.M),1,e.flash>0?hitFlashColor(e):null);
 }finally{BF22.actor=oldActor;BF22.root=oldRoot;BF22.selection=oldSelection;oldAlias?AF21.aliases.set(e.type,oldAlias):AF21.aliases.delete(e.type);}
}
drawEnemy=function(e){if(e.dead)return;const r=e._cp22Dash||e._cp22Sewer?cp22HullDraw(e):CP22.base.draw.apply(this,arguments);if(e._cp22Dash)cp22DashDraw(e);else if(e._cp22Flight)cp22FlightDraw(e);return r;};
fb2FlightPlan=function(){const q=CP22.base.plan.apply(this,arguments);
 if(q&&cp22Free())q._cp22Mode=['bomb','rain','charge','rain'][CP22.serial++%4];return q;};
fb2FlightSpawn=function(q){const e=CP22.base.spawnFlight.apply(this,arguments);
 if(e&&q._cp22Mode)e._cp22Flight={mode:q._cp22Mode,phase:'entry',t:0,age:0,shots:0,cd:0,id:++CP22.serial};return e;};
function cp22FlightTell(e,F){
 const T=targetShip(e.x,e.y);F.phase='tell';F.t=0;F.warm=F.mode==='charge'?.98:.80;F.target={x:T.x,y:T.y};
 F.angle=F.mode==='rain'?Math.PI/2:Math.atan2(T.y-e.y,T.x-e.x);F.origin={x:e.x,y:e.y};
 cp22Sound(e,'bossWeaponCharge',.8);cp22Log('flyby-tell',{mode:F.mode});
}
fb2FlightTick=function(e,dt){
 const F=e._cp22Flight;if(!F)return CP22.base.flight.apply(this,arguments);if(e.dead||e._dyingT!=null)return;
 const S=e._fb2Stealth,a=FB2_DIR_ANG[S.direction],rank=cp22Rank();F.t+=dt;F.age+=dt;S.t+=dt;e._frFlight=false;e._polishBomberCD=999;
 const inside=e.x>camLeftX()+40&&e.x<camRightX()-40&&e.y>viewTopY()+35&&e.y<VH-55;
 if(F.phase==='entry'){
  e.x+=Math.cos(a)*260*dt;e.y+=Math.sin(a)*260*dt;if(inside)cp22FlightTell(e,F);
 }else if(F.phase==='tell'){
  combatWarningTick(e,'cp22-flight-'+F.id,F.t,F.warm);
  if(F.t>=F.warm){F.phase='fire';F.t=0;F.cd=0;if(F.mode==='charge')cp22Sound(e,'jetDash',.5);}
 }else if(F.phase==='fire'){
  if(F.mode==='charge'){
   const x=e.x,y=e.y;e.x+=Math.cos(F.angle)*(540+rank*55)*dt;e.y+=Math.sin(F.angle)*(540+rank*55)*dt;
   for(const seat of seatList())withSeat(seat,()=>{if(!player.dead&&s81003Distance(player.x,player.y,{x,y,ex:e.x,ey:e.y})<26)playerHit('turbo attack run');});
   if(F.t>.95){F.phase='leave';F.t=0;}
  }else{
   e.x+=Math.cos(a)*170*dt;e.y+=Math.sin(a)*170*dt;F.cd-=dt;
   if(F.cd<=0){F.cd=F.mode==='rain'?.12:.48;F.shots++;
    if(F.mode==='bomb'){
     const T=F.target,offset=(F.shots-1)*40;
     const q=groundTargetingSpawn({kind:'missile',owner:e,x:clamp(T.x+(F.shots%2?offset:-offset),camLeftX()+42,camRightX()-42),y:clamp(T.y,viewTopY()+100,VH-42),track:false,lane:false,warn:1.5,radius:30,size:92,active:.40,sound:'atomicDetonate',shake:5,onImpact:g=>{if(typeof s67AtomicImpact==='function')s67AtomicImpact(g);else explode(g.x,g.y,90,'red');}});
     if(q){q._fb2Atom=true;q._jetBomb={x:e.x,y:e.y};}cp22Sound(e,'atomicLaunch',.4);
    }else{
     const p=bf22Mount(e,F.shots%2?'port':'starboard',true),first=eBullets.length;
     eShootT(p.x,p.y,F.angle+(F.shots%2?.045:-.045),4.7,'s6tracer',{w:7,h:14,owner:e,silent:true});bf22Tag(first,e);cp22Sound(e,'enemyMachineGunLight',.12);
    }
   }
   if(F.shots>=(F.mode==='rain'?6+Math.min(3,rank):2)){F.phase='leave';F.t=0;}
  }
 }else{e.x+=Math.cos(a)*300*dt;e.y+=Math.sin(a)*300*dt;}
 if(F.age>9||e.x<camLeftX()-170||e.x>camRightX()+170||e.y<viewTopY()-170||e.y>VH+170)e.dead=true;
};
function cp22FlightDraw(e){const F=e._cp22Flight;if(e.dead||F.phase!=='tell'||F.mode==='bomb')return;
 const angle=F.angle,len=F.mode==='charge'?viewW()*1.5:VH*1.5;
 const heading=FB2_DIR_ANG[e._fb2Stealth.direction],travel=F.mode==='rain'?(6+Math.min(3,cp22Rank()))*.12*170:0;
 for(const t of F.mode==='rain'?[0,.5,1]:[0]){const x=e.x+Math.cos(heading)*travel*t,y=e.y+Math.sin(heading)*travel*t;
  for(const a of F.mode==='rain'?[angle-.06,angle+.06]:[angle])combatWarningDraw(e,{x,y,ex:x+Math.cos(a)*len,ey:y+Math.sin(a)*len,width:F.mode==='charge'?72:54,progress:F.t/F.warm,fieldOnly:true});}
}
function cp22Wave(){
 const rank=cp22Rank(),count=[4,6,7,8,8][rank],ys=[.82,.48,.67,.88,.36,.73,.55,.84],gap=[1.25,1.12,1.02,.96,.94][rank];
 for(let i=0;i<count;i++)CP22.pending.push({delay:i*gap,side:(i+CP22.waves)%2?1:-1,y:clamp(viewTopY()+viewH()*ys[(i+CP22.waves*2)%ys.length],viewTopY()+80,VH-48)});
 CP22.waves++;cp22Say(CP22.waves===1?'DASHERS ON BOTH SIDES! CLIMB OR DIVE BETWEEN THE PASSES!':'KEEP MOVING! ROLL OR SOMERSAULT THROUGH A CROSSING. WE HAVE YOUR BACK!');cp22Log('dasher-wave',{count});
}
function cp22Tick(dt){
 if(run.stage!==6)return;CP22.radio=Math.max(0,CP22.radio-dt);
 if(!cp22Free()){
  if(story||s6q13Scene()||bossActive||subBossActive||warnT>0){CP22.pending=[];for(const e of enemies)if(e._cp22Dash)e.dead=true;}
  return;
 }
 CP22.age+=dt;
 if(CP22.waves<3&&CP22.age>=CP22.nextWave&&stageTimer<curStage.length-5){cp22Wave();CP22.nextWave+=18;}
 for(const q of CP22.pending)q.delay-=dt;
 const due=CP22.pending.filter(q=>q.delay<=0);CP22.pending=CP22.pending.filter(q=>q.delay>0);
 for(const q of due)if(enemies.filter(e=>e._cp22Dash&&!e.dead).length<3)cp22DashSpawn(q.side,q.y);
 if(CP22.age>=CP22.nextFlyby){CP22.nextFlyby=CP22.age+9;
  if(enemies.filter(e=>!e.dead&&e._dyingT==null).length<10&&eBullets.length<120)fb2FlightPlan(CP22.serial%2?'east':'west');
 }
}
beginStage=function(){CP22.age=0;CP22.nextWave=8;CP22.nextFlyby=5;CP22.waves=0;CP22.serial=0;CP22.pending=[];CP22.events=[];CP22.radio=0;return CP22.base.begin.apply(this,arguments);};
updatePlay=function(dt){const r=CP22.base.play.apply(this,arguments);cp22Tick(Math.min(.05,Math.max(0,dt)));return r;};
globalThis.BOF_AIR_PRESSURE={state:CP22,spawn:cp22DashSpawn,wave:cp22Wave,free:cp22Free};
