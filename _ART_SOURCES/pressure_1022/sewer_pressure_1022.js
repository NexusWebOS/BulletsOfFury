"use strict";
/* Airborne sewer slots share one toxic family. Ground machinery keeps its native
   placements, clearance and attacks. Randomness chooses the next beat, never an
   already warned trajectory. The entry cap remains part of the scrolling master. */
const SP22={events:[],base:{spawn:spawnEnemy,tick:s7ToxicTick,draw:drawEnemy,pose:bf22State,theme:bf22Theme,terrain:drawLevelMaster},
 slots:{s7skimmer:'slime',s7serpent:'slime',mm_hellhugger:'slime',mm1003_hellhugger:'slime',s7sampler:'drone',mm_riflelocust:'drone',mm1003_riflelocust:'drone',s7lamprey:'relay',mm_hellram:'relay',mm1003_hellram:'relay',s7mine:'drone',s7canister:'relay',mm1003_hexpyre:'relay',mm1003_impharrow:'drone'},
 types:{slime:'cp22slime',drone:'cp22drone',relay:'cp22relay'}};
spawnEnemy=function(type,x,y,options){
 const role=run.stage===7&&SP22.slots[type];if(!role)return SP22.base.spawn.apply(this,arguments);
 const e=SP22.base.spawn.call(this,'s7skimmer',x,y,options);if(!e)return e;
 for(const k of ['_mm1003','_mm','_toxicJet','_s7Act','_esh','_entrySweep','_s7AtkT','_s7AtkDur'])delete e[k];
 Object.assign(e,{type:SP22.types[role],pattern:'s7toxic',_s7toxic:'s7skimmer',_vkind:'air',_noSep:true,shoots:false,fk:null,spin:0,vx:0,vy:0,_frFlight:false,_stagger:0});
 const hp={slime:22,drone:14,relay:32}[role],span={slime:54,drone:42,relay:68}[role];e.w=span;e.h=span;e.hp=e.maxhp=e._maxhp=EHP(hp);
 e.score={slime:1240,drone:960,relay:1460}[role];e._cp22Sewer={role,phase:'entry',t:0,age:0,seq:0,shots:0,from:{x,y},tx:clamp(x,camLeftX()+65,camRightX()-65),ty:viewTopY()+100+Math.random()*90};return e;
};
bf22Theme=function(e){return e?._cp22Sewer?'toxic':SP22.base.theme.apply(this,arguments);};
bf22State=function(e,kind,value){const S=e?._cp22Sewer;if(!S)return SP22.base.pose.apply(this,arguments);
 if(e._air13Motion)return {kind:e._air13Motion.kind,value:clamp(e._air13Motion.t/e._air13Motion.dur,0,.999)};
 if(S.phase==='tell')return {kind:'attack',value:clamp(S.t/S.warm*.48,0,.48)};
 if(S.phase==='fire')return {kind:'attack',value:.5+Math.min(.49,S.t*1.2)};
 return {kind:S.phase==='move'?'drift':'idle',value:S.phase==='move'?(S.tx>e.x?.7:.2):efxClock*.8};
};
function sp22Log(e,event){SP22.events.push({role:e._cp22Sewer.role,event,t:e._cp22Sewer.age,attack:e._cp22Sewer.attack});if(SP22.events.length>180)SP22.events.shift();}
function sp22Tell(e){const S=e._cp22Sewer,T=targetShip(e.x,e.y),rank=target17Rank();S.phase='tell';S.t=0;S.shots=0;S.cd=0;S.seq++;
 S.warm=[1.12,.96,.86,.76,.72][rank];S.attack=S.role==='slime'&&S.seq%3===2?'hook':S.role==='relay'&&S.seq%2?'lattice':S.role==='drone'?'needle':'fan';
 S.target={x:T.x,y:T.y};S.angle=Math.atan2(T.y-e.y,T.x-e.x);S.lines=[];
 if(S.attack==='hook')S.lines.push({x:e.x,y:e.y,ex:e.x+Math.cos(S.angle)*VH,ey:e.y+Math.sin(S.angle)*VH,width:72,angle:S.angle});
 else{const offsets=S.attack==='lattice'?[-.48,-.24,.24,.48]:S.attack==='needle'?[-.055,.055]:[-.18,0,.18];
  offsets.forEach((offset,i)=>{const socket=i%2?'starboard':'port',P=bf22Mount(e,socket),a=(S.attack==='lattice'?Math.PI/2:S.angle)+offset;S.lines.push({x:P.x,y:P.y,ex:P.x+Math.cos(a)*VH*1.4,ey:P.y+Math.sin(a)*VH*1.4,width:S.attack==='needle'?14:24,angle:a,socket});});}
 combatAudio0927(e,'bossWeaponCharge',.8);sp22Log(e,'tell');
}
s7ToxicTick=function(e,dt){const S=e._cp22Sewer;if(!S)return SP22.base.tick.apply(this,arguments);if(e.dead||e._dyingT!=null)return;
 S.age+=dt;S.t+=dt;e.shoots=false;e.spin=0;e._frFlight=false;
 if(e._air13Motion){e._air13Motion.t+=dt;if(e._air13Motion.t>=e._air13Motion.dur)delete e._air13Motion;}
 if(S.phase==='entry'||S.phase==='move'){
  const dx=S.tx-e.x,dy=S.ty-e.y,dist=Math.hypot(dx,dy),speed=S.role==='drone'?135:105;
  if(dist>3){e.x+=dx/dist*Math.min(dist,speed*dt);e.y+=dy/dist*Math.min(dist,speed*dt);}else sp22Tell(e);
 }else if(S.phase==='tell'){
  combatWarningTick(e,'sewer-'+S.seq,S.t,S.warm);
  if(S.t>=S.warm){S.phase='fire';S.t=0;sp22Log(e,'release');if(S.attack==='hook')combatAudio0927(e,'jetDash',.5);}
 }else if(S.phase==='fire'){
  if(S.attack==='hook'){
   const x=e.x,y=e.y,speed=370+target17Rank()*30;e.spin=S.angle-Math.PI/2;e.x+=Math.cos(S.angle)*speed*dt;e.y+=Math.sin(S.angle)*speed*dt;
   for(const seat of seatList())withSeat(seat,()=>{if(!player.dead&&s81003Distance(player.x,player.y,{x,y,ex:e.x,ey:e.y})<24)playerHit('corrosive hook run');});
  }else{
   S.cd-=dt;if(S.cd<=0&&S.shots<(S.attack==='needle'?2:1)){
    S.cd=.22;S.shots++;for(const L of S.lines){const P=bf22Mount(e,L.socket),first=eBullets.length;
     eShootT(P.x,P.y,L.angle,S.attack==='needle'?4.1:S.attack==='lattice'?2.6:3.0,S.attack==='needle'?'s7laser':'s7sludge',{owner:e,w:S.attack==='needle'?8:15,h:S.attack==='needle'?22:15,silent:true});bf22Tag(first,e);bf22Flash(e,L.socket,L.angle,.15);}
    combatAudio0927(e,S.attack==='needle'?'enemyMachineGunLight':'combatToxic0927',.14);
   }
  }
  if(S.t>(S.attack==='hook'?.48:.46)){S.phase='recover';S.t=0;sp22Log(e,'recovery');}
 }else if(S.phase==='recover'&&S.t>.65){
  S.phase='move';S.t=0;S.tx=camLeftX()+60+Math.random()*Math.max(1,viewW()-120);S.ty=viewTopY()+90+Math.random()*Math.min(200,viewH()*.36);
  if(S.seq%3===0)e._air13Motion={kind:S.seq%2?'roll':'somer',t:0,dur:.65};
 }
 // Limited sorties keep sewer lanes clear instead of accumulating hovering turrets.
 if(S.age>15){e.y-=190*dt;if(e.y<viewTopY()-100)e.dead=true;S.phase='leave';}
};
drawEnemy=function(e){const r=SP22.base.draw.apply(this,arguments),S=e._cp22Sewer;
 if(S&&S.phase==='tell'&&!e.dead&&e._dyingT==null)for(const L of S.lines||[])combatWarningDraw(e,{...L,progress:S.t/S.warm,fieldOnly:true});return r;};
drawLevelMaster=function(dt){
 // Intro and launch render several seconds before PLAY. Hold the actual source
 // at row zero during those shots; once PLAY starts the original entrance exits
 // with world scroll, including its original alpha and parallax liquid below it.
 const hold=run.stage===7&&(state===GS.INTRO||state===GS.LAUNCH)&&!bossActive;
 if(hold)mapScroll=0;const r=SP22.base.terrain.apply(this,arguments);if(hold)mapScroll=0;return r;
};
globalThis.BOF_SEWER_PRESSURE={state:SP22,tell:sp22Tell};
