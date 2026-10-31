'use strict';
/* Formation missile tells, one screen-wide audible warning and NPC breakaway.
   Existing authored retinas, baked ship flames and physical missile collision remain. */
const RM49={base:{fleet:rd21Fleet,rocket:ra4Rocket,tick:rebelSquadTick,wing:s6WingTick,navigate:s6WingNavigate,arsenal:s6WingArsenal,targets:ra4Targets,world:drawWorld,update:updatePlay,state:setState,load:stageLoadBegin,duck:pauseMusicDuck,block:rr26BlockShips},owner:null,events:[],keys:{},serial:0};
for(const [role,source,gain,gate]of [['seek','retinaLockBeep',.95,.07],['locked','alertLockon',.95,.9],['incoming','retinaLockBeep',.95,.09],['boost','jetDash',.7,.5]]){
 const key='riders49_'+role,uri=BOFA.sfx[source],slots=[],list=[];RM49.keys[role]=key;BOFA.sfx[key]=uri;
 for(let i=0;i<3;i++)Object.defineProperty(list,i,{enumerable:true,get(){if(!slots[i])slots[i]={el:new window.Audio(),uri:Array.isArray(uri)?uri[0]:uri,attached:false,used:0};return Snd._touchVoice(slots[i]);}});
 Snd.pools[key]={list,slots,i:0};Snd.TAME[key]={g:gain,native:true,min:gate};
}
function rr49Scope(b=boss){return state===GS.PLAY&&!!b&&!b.dead&&rr33Group(b);}
function rr49Log(event,data={}){RM49.events.push({event,time:rg4State()?.age||0,...data});if(RM49.events.length>600)RM49.events.shift();}
function rr49Warm(){Snd.prepare(Object.values(RM49.keys));}
function rr49State(b=boss){const G=b?._rebels?.gang1004;return G&&(G.rm49||(G.rm49={clock:0,beep:0,incoming:0,focus:0,fleet:null,sequence:0}));}
function rr49Sound(role){const S=rr49State();if(!S||!rr49Scope())return false;RM49.owner=boss;S.focus=.45;const accepted=Snd.play(RM49.keys[role]);rr49Log('audio',{role,accepted});return accepted;}
function rr49Players(){const out=[];for(const seat of seatList())withSeat(seat,()=>{if(!player.dead&&!player.out)out.push({key:_pilotKey(),ref:player,seat});});return out;}
function rr49Break(b,F){const S=rr49State(b);S.fleet=F;S.sequence=++RM49.serial;F._rm49=S.sequence;F._rm49Locked=false;RM49.owner=b;
 const targets=rr49Players();for(const q of b._rebels.ships){const A=q._rd21Volley;if(!A)continue;A.target=targets[q.i%Math.max(1,targets.length)]||A.target;A._rm49=S.sequence;A.phase='charge';}
 const wing=s6Wing?.ships||[];for(const q of wing){if(q.hp<=0||q.phase==='leave'||q._rm49Flight&&q._rm49Flight.phase!=='return')continue;
  q._rm49Flight={phase:'out',t:0,lane:clamp((q.x-camLeftX())/viewW(),.07,.93),homeY:q.y};q.phase='rm49-evade';q.target=null;q._rd21Intercept=null;q.dodgeT=0;q.dodgeMode=null;
 }rr49Sound('boost');rr49Log('allies-break',{sequence:S.sequence,count:wing.filter(q=>q._rm49Flight).length});
}
rd21Fleet=function(b,G,D,dt){const F=D.fleet;if(!rr49Scope(b)||!F)return RM49.base.fleet.apply(this,arguments);
 if(!F._rm49Warm){F._rm49Warm=true;rr49Warm();}const before=F.phase;
 const result=RM49.base.fleet.apply(this,arguments);
 if(F.phase==='tell'&&!F._rm49)rr49Break(b,F);
 for(const q of b._rebels.ships){const A=q._rd21Volley;if(A?._rm49){A.phase=F.phase==='tell'?'charge':'fire';if(F.phase!=='tell')A.t=A.warm+(rr49State(b).clock%1);}}
 if(before==='tell'&&F.phase==='volley'&&!F._rm49Locked){F._rm49Locked=true;rr49State(b).confirmedUntil=rr49State(b).clock+.5;rr49Sound('locked');rr49Log('locked-on',{sequence:F._rm49});}
 if(D.fleet!==F&&F._rm49){rr49Log('riders-settled',{sequence:F._rm49});}
 return result;
};
ra4Rocket=function(q,G,A){const first=eBullets.length,r=RM49.base.rocket.apply(this,arguments);
 if(rr49Scope()&&A?._rm49){for(const z of eBullets.slice(first))if(z._ra4Rocket){z._rm49=A._rm49;z._rm49Pilot=q.key;rr49Log('missile',{pilot:q.key,target:A.target.key,sequence:A._rm49,shootable:z._shootable});}}
 return r;
};
function rr49Missiles(){return eBullets.filter(m=>m._rm49&&!m.dead&&m.hp>0&&m.x>camLeftX()-60&&m.x<camRightX()+60&&m.y>PLAY.y-80&&m.y<VH+60);}
function rr49Threat(){let best=Infinity;for(const m of rr49Missiles())for(const t of rr49Players()){
 const dx=t.ref.x-m.x,dy=t.ref.y-m.y,vx=m.vx*60,vy=m.vy*60,dist=Math.hypot(dx,dy),tt=(dx*vx+dy*vy)/Math.max(1,vx*vx+vy*vy);
 if(dist<330&&tt>=-.08&&tt<1.45&&Math.hypot(dx-vx*Math.max(0,tt),dy-vy*Math.max(0,tt))<130)best=Math.min(best,dist);
 }return best;}
rebelSquadTick=function(b,dt){const result=RM49.base.tick.apply(this,arguments);if(!rr49Scope(b))return result;const S=rr49State(b);if(!S)return result;S.clock+=dt;S.beep-=dt;S.incoming-=dt;
 const F=b._rebels.gang1004?.rd21?.fleet;if(F?._rm49&&F.phase==='tell'){
  if(S.beep<=0){const progress=clamp(F.t/2.1,0,1);rr49Sound('seek');S.beep=lerp(.32,.10,progress);}
 }else S.beep=0;
 const near=rr49Threat();if(Number.isFinite(near)&&S.clock>=(S.confirmedUntil||0)){if(S.incoming<=0){rr49Sound('incoming');S.incoming=lerp(.10,.28,clamp(near/330,0,1));rr49Log('incoming',{distance:near});}}else S.incoming=0;
 return result;
};
// NPCs retain their own ships/HP. Player and co-op seats never enter this state.
ra4Targets=function(){const targets=RM49.base.targets.apply(this,arguments);return rr49Scope()?targets.filter(t=>!t.ref?._rm49Flight):targets;};
s6WingNavigate=function(q,W,dt){const P=q._rm49Flight;if(!P)return RM49.base.navigate.apply(this,arguments);
 q.target=null;q._rd21Intercept=null;q.dodgeT=0;q.dodgeMode=null;P.t+=dt;
 const S=rr49State(),F=boss?._rebels?.gang1004?.rd21?.fleet,active=rr49Scope()&&F===S?.fleet;
 if(P.phase==='out'){q.vx=0;q.vy=-(760+Math.min(340,P.t*1000));q.y+=q.vy*dt;if(q.y<-90){q.y=-90;P.phase='hold';rr49Log('ally-offscreen',{pilot:q.key});}}
 if(P.phase==='hold'){q.vx=q.vy=0;q.y=-90;if(!active){P.phase='return';P.t=0;q.x=camLeftX()+viewW()*P.lane;q.y=VH+85;rr49Log('ally-return',{pilot:q.key});}}
 if(P.phase==='return'){
  const tx=camLeftX()+viewW()*P.lane,ty=clamp(P.homeY,VH*.69,VH-48),dx=tx-q.x,dy=ty-q.y,d=Math.hypot(dx,dy),speed=Math.min(500,d*4+50),step=Math.min(d,speed*dt);
  q.vx=d?dx/d*speed:0;q.vy=d?dy/d*speed:0;q.x+=d?dx/d*step:0;q.y+=d?dy/d*step:0;
  if(d<=step+.01){delete q._rm49Flight;q.phase='fight';q.t=Math.max(1,q.t);q.think=0;q.fcd=Math.max(.35,q.fcd||0);q.target=null;q.vx=q.vy=0;rr49Log('ally-restored',{pilot:q.key});}
 }return null;
};
s6WingArsenal=function(q){if(q._rm49Flight)return;return RM49.base.arsenal.apply(this,arguments);};
// Golden Aegis is a friendly barrier; it cannot pin the departing wing below it.
rr26BlockShips=function(G){if(!rr49Scope())return RM49.base.block.apply(this,arguments);const saved=[];
 for(const q of s6Wing?.ships||[])if(q._rm49Flight){saved.push([q,q.out]);q.out=true;}
 try{return RM49.base.block.apply(this,arguments);}finally{for(const [q,out]of saved)q.out=out;}
};

function rr49Stop(){for(const key of Object.values(RM49.keys))for(const s of Snd.pools[key].slots)if(s?.attached){s.el._bofEpoch=(s.el._bofEpoch||0)+1;try{s.el.pause();s.el.currentTime=0;}catch(_){}}
 const S=RM49.owner?._rebels?.gang1004?.rm49;if(S)S.focus=0;RM49.owner=null;}
function rr49Reset(){rr49Stop();for(const q of s6Wing?.ships||[])if(q._rm49Flight){delete q._rm49Flight;q.phase='arrive';q.y=VH+85;q.vx=q.vy=0;q.target=null;}}
pauseMusicDuck=function(){return RM49.base.duck()*(rr49Scope()&&rr49State()?.focus>0?.60:1);};
updatePlay=function(dt){if(RM49.owner&&(!rr49Scope()||RM49.owner!==boss))rr49Reset();const r=RM49.base.update.apply(this,arguments),S=rr49State();if(S)S.focus=Math.max(0,S.focus-dt);
 if(Snd.cur&&(S?.focus>0||RM49.mixed)){Snd.cur.volume=clamp(Snd.vol.music*Snd.vol.master*pauseMusicDuck(),0,1);RM49.mixed=S?.focus>0;}return r;};
setState=function(s){if(s!==GS.PLAY)rr49Stop();return RM49.base.state.apply(this,arguments);};
stageLoadBegin=function(n){rr49Reset();if(n===6)rr49Warm();return RM49.base.load.apply(this,arguments);};
drawWorld=function(dt){const r=RM49.base.world.apply(this,arguments);if(!rr49Scope())return r;const seen=new Set();ctx.save();const z=viewZoom();if(z!==1){ctx.scale(z,z);ctx.translate(0,VH*(1-z)/z);}if(worldWidth()>viewW())ctx.translate(-camX,0);
 for(const m of rr49Missiles()){const target=m.lock?.ref;if(!target||target.dead||target.out||seen.has(target)||m.owner?._rd21Volley)continue;seen.add(target);ra4LockWarning({locked:true,t:1+(rr49State().clock%1),warm:1,target:{ref:target}},m._rm49Pilot);}
 ctx.restore();return r;
};
globalThis.BOF_RIDERS_MISSILE_WARNING_1029=RM49;
