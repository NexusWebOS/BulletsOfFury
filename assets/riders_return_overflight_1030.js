'use strict';
/* Clarification: TEAL ENERGY BALLS continue over the Riders, not ally hulls. */
const RR75={base:{tick:rr26WallTick,draw:rebelSquadDraw,world:drawWorld,load:stageLoadBegin},events:[],painting:null,orbs:0,shadows:0};
for(const a of Object.values(RR75_ART))XART._src[a.key]=a.path;
stageLoadBegin=function(n,keys){return RR75.base.load.call(this,n,n===6?[...(keys||[]),...Object.values(RR75_ART).map(a=>a.key)]:keys);};
function rr75Own(){return state===GS.PLAY&&rr45Scope()&&!boss.dead;}
function rr75Log(event,data={}){RR75.events.push({event,clock:efxClock,...data});if(RR75.events.length>500)RR75.events.shift();}
rr26WallTick=function(G,dt){if(!rr75Own())return RR75.base.tick.apply(this,arguments);const S=rr26State(G),old=S.returns;S.returns=[];let fresh;
 try{RR75.base.tick.apply(this,arguments);}finally{fresh=S.returns;S.returns=old.concat(fresh);}
 for(const o of S.returns){o.t+=dt;const M=o._rr75??={phase:'approach',size:30,distance:0};
  if(M.phase==='approach'){
   if(!rd21Live(o.target)){o.target=boss._rebels.ships.find(rd21Live);if(!o.target){o.dead=true;continue;}}
   const dx=o.target.x-o.x,dy=o.target.y-o.y,d=Math.hypot(dx,dy)||1,step=430*dt;M.size=30+12*clamp(1-d/80,0,1);o.x+=dx/d*step;o.y+=dy/d*step;
   if(d<step+20){rr26Damage(o.target,12);M.phase='overflight';M.vx=dx/d*430;M.vy=dy/d*430;M.hit={x:o.x,y:o.y};M.size=42;M.hitAge=o.t;rg4FX(G,2,o.x,o.y,65,.4);rr26Log('reflection-hit',{target:o.target.key});rr75Log('pass-over',{target:o.target.key,x:o.x,y:o.y});}
  }else{
   o.x+=M.vx*dt;o.y+=M.vy*dt;M.distance+=430*dt;const u=clamp(M.distance/250,0,1);M.size=42-28*u*u*(3-2*u);
   if(o.x<camLeftX()-40||o.x>camRightX()+40||o.y<viewTopY()-40||o.y>VH+40){o.dead=true;rr75Log('edge-exit',{x:o.x,y:o.y,age:o.t});}
  }
  if(o.t>5){o.dead=true;rr75Log('finite-expiry');}
 }
 S.returns=S.returns.filter(o=>!o.dead);
};
function rr75Blit(o,role){const a=RR75_ART[role],m=o._rr75,depth=clamp(Math.round(((m?.size||30)-14)/2),0,16),f=role==='orb'?depth*8+Math.floor(o.t*16)%8:depth;if(!XART.rdy(a.key))return;const offset=role==='shadow'?20+(m?.phase==='overflight'?Math.max(0,20-m.distance*.06):0):0;
 ctx.drawImage(XART.get(a.key),f%a.cols*64,Math.floor(f/a.cols)*64,64,64,Math.round(o.x-32+(role==='shadow'?6:0)),Math.round(o.y-32+offset),64,64);RR75[role==='orb'?'orbs':'shadows']++;
}
rebelSquadDraw=function(b){if(RR75.painting)for(const o of RR75.painting)rr75Blit(o,'shadow');return RR75.base.draw.apply(this,arguments);};
drawWorld=function(dt){if(!rr75Own())return RR75.base.world.apply(this,arguments);const S=rg4State()?.rr26;if(!S?.returns?.length)return RR75.base.world.apply(this,arguments);const all=S.returns;S.returns=[];RR75.painting=all;let r;
 try{r=RR75.base.world.apply(this,arguments);}finally{S.returns=all;RR75.painting=null;}
 ctx.save();try{const z=viewZoom();if(z!==1){ctx.scale(z,z);ctx.translate(0,VH*(1-z)/z);}if(worldWidth()>viewW())ctx.translate(-camX,0);ctx.beginPath();ctx.rect(camLeftX(),0,viewW(),VH);for(const p of RR66.panels)ctx.rect(camLeftX()+p.x,p.y,p.w,p.h);ctx.clip('evenodd');for(const o of all)rr75Blit(o,'orb');}finally{ctx.restore();}return r;
};
globalThis.BOF_RIDERS_RETURN_OVERFLIGHT_1030=RR75;
