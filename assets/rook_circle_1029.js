'use strict';
/* Rook's spin tell: full authored FOV disc behind his hull, icon above it.
   The native attack keeps its timing, guns, turning frames and missile stun. */
const RK50={base:{attack:rg4Attack,act:rg4AttackTick,tick:rebelSquadTick,ship:fr27RebelDrawShip,warning:rg4Warning,damage:rebelSquadDamage,load:stageLoadBegin,dispatch:RD42.attack},events:[],fields:0,symbols:0};
for(const role of ['field','symbol'])for(const colour of ['green','yellow','red'])XART._src['rk50_'+role+'_'+colour]='assets/game/levels/stage_06/boss/rook_circle_1029/'+role+'_'+colour+'.png';
function rk50Own(q,A=q?.rg4?.act){return rr33Group(boss)&&boss._rebels.ships.includes(q)&&q.key==='rook'&&!q.dead&&A?.kind==='rk38spin'&&A._rk50;}
function rk50Fixed(q){return rk50Own(q)&&['charge','fire'].includes(q.rg4.act.phase)&&!q._rk38Stun;}
function rk50Center(A){return{x:camLeftX()+viewW()/2,y:A?._rk50Y??VH/2};}
function rk50Hold(q,A){const c=rk50Center(A);q.x=c.x;q.y=c.y;A.ox=c.x;A.oy=c.y;A.from={...c};}
function rk50Colour(A){const p=A.phase==='fire'?1:clamp(A.t/A.warm,0,1);return p<.45?'green':p<.78?'yellow':'red';}
function rk50Blit(role,colour,x,y){const key='rk50_'+role+'_'+colour,size=role==='field'?404:48;if(!XART.rdy(key))return;ctx.drawImage(XART.get(key),Math.round(x-size/2),Math.round(y-size/2),size,size);}
stageLoadBegin=function(n,keys){return RK50.base.load.call(this,n,n===6?[...(keys||[]),...['field','symbol'].flatMap(role=>['green','yellow','red'].map(c=>'rk50_'+role+'_'+c))]:keys);};
function rk50Prepare(q){const A=q?.rg4?.act;if(rr33Group(boss)&&q?.key==='rook'&&A?.kind==='rk38spin'&&!A._rk50){A._rk50=true;A._rk50Y=VH/2;A.center=rk50Center(A);RK50.events.push({event:'spin-approach',time:rg4State()?.age||0,...A.center});}}
RD42.attack=function(q){const r=RK50.base.dispatch.apply(this,arguments);rk50Prepare(q);return r;};
rg4Attack=function(q){const r=RK50.base.attack.apply(this,arguments);if(rr33Group(boss))rk50Prepare(boss._rebels.ships.find(q=>q.key==='rook'));return r;};
rg4AttackTick=function(q,R,G,dt){const A=q.rg4?.act;if(!rk50Own(q,A))return RK50.base.act.apply(this,arguments);
 if(A.phase==='advance')A.center=rk50Center(A);else if(rk50Fixed(q))rk50Hold(q,A);
 const phase=A.phase,r=RK50.base.act.apply(this,arguments);if(q.rg4.act===A&&rk50Fixed(q))rk50Hold(q,A);
 if(phase!==A.phase)RK50.events.push({event:'spin-phase',phase:A.phase,time:G.age,x:q.x,y:q.y});if(RK50.events.length>200)RK50.events.shift();return r;
};
rebelSquadTick=function(b,dt){const r=RK50.base.tick.apply(this,arguments),q=b?._rebels?.ships.find(q=>rk50Fixed(q));if(q){rk50Hold(q,q.rg4.act);rr45Separate(b);}return r;};
// Real missile knockback still displaces him; the reservation does not erase it.
rebelSquadDamage=function(b){const q=b?._rebels?.ships[b._rebels.hit],A=q?.rg4?.act,y=q?.y,owned=rk50Own(q,A),r=RK50.base.damage.apply(this,arguments);if(owned&&q.rg4?.act===A)A._rk50Y+=q.y-y;return r;};
rg4Warning=function(q,A){if(rk50Own(q,A)&&['charge','fire'].includes(A.phase)){if(q._rk38Stun)return;rk50Blit('symbol',rk50Colour(A),q.x,q.y-78);RK50.symbols++;return;}return RK50.base.warning.apply(this,arguments);};
fr27RebelDrawShip=function(q){const A=q.rg4?.act;if(rk50Own(q,A)&&A.phase==='charge'&&!q._rk38Stun){rk50Blit('field',rk50Colour(A),q.x,q.y);RK50.fields++;}return RK50.base.ship.apply(this,arguments);};
globalThis.BOF_ROOK_CIRCLE_1029=RK50;
