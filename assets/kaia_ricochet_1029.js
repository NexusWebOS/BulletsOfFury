'use strict';
/* Stage 6 Kaia roller bursts: faster release and four-edge ricochets.
   Native ordnance still owns damage, lifespan, owner cleanup and shield returns. */
const KR48={interval:.14,speeds:[235,260,280,300],serial:0,events:[]};
function kr48Own(q){return q?.key==='kaia'&&rr33Group(boss)&&boss._rebels.ships.includes(q);}
function kr48Log(event,data){KR48.events.push({event,time:rg4State()?.age||0,...data});if(KR48.events.length>600)KR48.events.shift();}
function kr48Launch(o){o._kr48=++KR48.serial;kr48Log('shot',{id:o._kr48,x:o.x,y:o.y,speed:Math.hypot(o.vx,o.vy),interval:KR48.interval});}
function kr48Axis(position,velocity,dt,lo,hi){
 if(hi<=lo)return{position:(lo+hi)/2,velocity,bounces:[]};
 const bounces=[];
 // Keep an easing viewport edge from leaving a roller outside the playfield.
 if(position<lo){position=lo;if(velocity<0){velocity=-velocity;bounces.push('low');}}
 else if(position>hi){position=hi;if(velocity>0){velocity=-velocity;bounces.push('high');}}
 position+=velocity*dt;
 // Reflect overshoot too, so a corner hit preserves speed and remaining travel.
 while(position<lo||position>hi||(position===lo&&velocity<0)||(position===hi&&velocity>0)){
  if(position<=lo){position=lo+(lo-position);velocity=Math.abs(velocity);bounces.push('low');}
  else{position=hi-(position-hi);velocity=-Math.abs(velocity);bounces.push('high');}
 }
 return{position,velocity,bounces};
}
function kr48Move(o,dt){
 // The authored roller is 48px wide; its collision radius remains the native 16.
 const inset=24,left=camLeftX()+inset,right=camRightX()-inset,top=PLAY.y+inset,bottom=VH-inset;
 const x=kr48Axis(o.x,o.vx,dt,left,right),y=kr48Axis(o.y,o.vy,dt,top,bottom);
 o.x=x.position;o.y=y.position;o.vx=x.velocity;o.vy=y.velocity;
 for(const edge of [...x.bounces.map(e=>e==='low'?'left':'right'),...y.bounces.map(e=>e==='low'?'top':'bottom')]){
  o.bounces++;kr48Log('bounce',{id:o._kr48,edge,x:o.x,y:o.y,vx:o.vx,vy:o.vy});
 }
}
globalThis.BOF_KAIA_RICOCHET_1029=KR48;
