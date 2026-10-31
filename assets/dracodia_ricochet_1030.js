'use strict';
/* RD73: exposed first-host core ricochets continuously and drops committed code bombs. */
const RD73={base:{start:v18StartAttack,tick:v18AttackTick,weapon:rb23DrawWeapon},events:[],serial:0,
 specs:[{speed:255,gap:.52,cap:4},{speed:290,gap:.36,cap:5},{speed:330,gap:.24,cap:6}]};
function rd73Own(b){return b===boss&&rb23Host(b)&&!b.dead&&b._r30.mode==='fight'&&!rb23Arms(b).length;}
function rd73Attack(b){const P=b?._r30?.v18?.attack;return rd73Own(b)&&P?.type==='rb23-roll'?P:null;}
function rd73Log(event,data={}){RD73.events.push({event,clock:efxClock,...data});if(RD73.events.length>900)RD73.events.shift();}
function rd73Init(b,P){const spec=RD73.specs[d20Rank()],w=viewW(),ready=!!b._r30.v18.r25BallReady,sign=b.x-camLeftX()>w/2?-1:1;
 P.tell=ready?.25:1.2;P.active=9.6;P.beamPhase='travel';P._rd73={serial:++RD73.serial,spec,x:b.x-camLeftX(),y:b.y,vx:sign*Math.cos(.61)*spec.speed,vy:Math.sin(.61)*spec.speed,phase:'fold',phaseT:0,drop:0,cycle:0,drops:0,bounces:0};
 rd73Log('ricochet-start',{serial:P._rd73.serial,speed:spec.speed,gap:spec.gap,cap:spec.cap,hp:b.hp});return P._rd73;
}
v18StartAttack=function(b){const r=RD73.base.start.apply(this,arguments),P=rd73Attack(b);if(P)rd73Init(b,P);return r;};
// Union of all24 actual roll-frame alpha extents:118/122/105/104 around the128px pivot.
function rd73Bounds(){return{left:128,right:Math.max(129,viewW()-132),top:viewTopY()+157,bottom:Math.max(viewTopY()+158,VH-112)};}
function rd73Move(b,M,dt){const B=rd73Bounds(),speed=M.phase==='coast'?.8:1;M.x+=M.vx*dt*speed;M.y+=M.vy*dt*speed;
 for(let i=0;i<4&&(M.x<B.left||M.x>B.right);i++){const edge=M.x<B.left?'left':'right';M.x=edge==='left'?2*B.left-M.x:2*B.right-M.x;M.vx=edge==='left'?Math.abs(M.vx):-Math.abs(M.vx);M.bounces++;rd73Log('wall-rebound',{serial:M.serial,edge,vx:M.vx,vy:M.vy});}
 for(let i=0;i<4&&(M.y<B.top||M.y>B.bottom);i++){const edge=M.y<B.top?'top':'bottom';M.y=edge==='top'?2*B.top-M.y:2*B.bottom-M.y;M.vy=edge==='top'?Math.abs(M.vy):-Math.abs(M.vy);M.bounces++;rd73Log('wall-rebound',{serial:M.serial,edge,vx:M.vx,vy:M.vy});}
 b.x=camLeftX()+M.x;b.y=M.y;b._drawY=b.y;
}
function rd73Drop(b,M){const live=enemies.filter(e=>!e.dead&&e._d20?.owner===b&&e._d20.kind==='bomb'&&e._d20.phase!=='erase');if(live.length>=M.spec.cap)return false;
 const base={x:b.x,y:clamp(b.y+92,viewTopY()+145,VH-52)},offsets=[[0,0],[-84,0],[84,0],[0,-84],[-84,-84],[84,-84],[0,84],[-168,0],[168,0]],occupied=[...live.map(e=>e._d20.target),...D20.blasts.filter(q=>q.owner===b&&q.radius>0&&q.t<q.life).map(q=>({x:q.x,y:q.y}))];
 let target=null;for(let i=0;i<offsets.length;i++){const o=offsets[(i+M.drops%3)%offsets.length],q={x:clamp(base.x+o[0],camLeftX()+58,camRightX()-58),y:clamp(base.y+o[1],viewTopY()+145,VH-52)};if(!occupied.some(p=>(q.x-p.x)**2+(q.y-p.y)**2<74*74)){target=q;break;}}
 if(!target)return false;const e=d20Bomb(b,target);if(!e)return false;e.x=b.x;e.y=b.y+22;e._d20.start={x:e.x,y:e.y};e._d20._rd73=true;M.drops++;
 rd73Log('rapid-code-drop',{serial:M.serial,id:e._d20.id,x:e.x,y:e.y,target:{...target},warning:e._d20.flight+e._d20.warm,live:live.length+1});return true;
}
v18AttackTick=function(b,dt){const P=rd73Attack(b);if(!P)return RD73.base.tick.apply(this,arguments);dt=clamp(dt||0,0,.05);const M=P._rd73||rd73Init(b,P);P.t+=dt;const B=rd73Bounds();P.beamPhase='travel';
 if(P.t<P.tell){M.x+=clamp(clamp(M.x,B.left,B.right)-M.x,-160*dt,160*dt);M.y+=clamp(clamp(M.y,B.top,B.bottom)-M.y,-160*dt,160*dt);b.x=camLeftX()+M.x;b.y=M.y;b._drawY=b.y;combatWarningTick(b,'rd73-fold-'+M.serial,P.t,P.tell);return;}
 if(M.phase==='fold'){M.phase='bombing';M.phaseT=0;b._r30.v18.bi24Rolled=true;rd73Log('ricochet-release',{serial:M.serial,x:b.x,y:b.y});}
 M.phaseT+=dt;rd73Move(b,M,dt);
 if(M.phase==='bombing'){M.drop-=dt;if(M.drop<=0){M.drop=M.spec.gap;rd73Drop(b,M);}if(M.phaseT>=P.active){M.phase='coast';M.phaseT=0;j3State(b).attacks++;rd73Log('barrage-recovery',{serial:M.serial,cycle:M.cycle,drops:M.drops});}}
 else if(M.phaseT>=.7){M.phase='bombing';M.phaseT=0;M.drop=0;M.cycle++;rd73Log('barrage-resume',{serial:M.serial,cycle:M.cycle});}
 for(const seat of seatList())withSeat(seat,()=>{if(!player.dead&&Math.hypot(player.x-b.x,player.y-b.y)<62)playerHit('Dracodia rolling core');});
};
rb23DrawWeapon=function(b){const P=rd73Attack(b);if(P?._rd73&&P.t<P.tell){rd72Blit('asterisk',P.t/P.tell<2/3?0:1,b.x,Math.max(viewTopY()+78,b.y-124));return;}return RD73.base.weapon.apply(this,arguments);};
globalThis.BOF_DRACODIA_RICOCHET_1030={state:RD73};
