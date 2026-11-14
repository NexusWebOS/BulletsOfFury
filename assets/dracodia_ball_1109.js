'use strict';
/* Authored compact-ball counter, scoped to Dracodia's Chronos copy. */
const DB119={base:{start:hb20Start,pose:hb20Pose,tick:v19NativeTick,rig:v19HammerRig,hit:modularHit,blit:rd74Blit,draw:v19DonorDraw},events:[],radius:64};
for(const [n,a]of Object.entries(DB119_ART))for(const m of ['regular','chrome','red','hit','red_hit']){
 const bank='ba119_'+n+'_'+m,key='nca_'+bank;XART._src[key]='assets/game/shared/combat/dracodia_ball_1109/'+n+'_'+m+'.webp';BA119.keys[8].push(key);
 if(['regular','chrome','red'].includes(m))RD74_ART.banks[bank]={key,hitKey:'nca_ba119_'+n+'_hit',frames:16,cols:4,cw:a.cell[0],ch:a.cell[1],pivot:a.pivot,meta:a.meta};
}
// The visible spikes extend beyond the forgiving contact radius. Reserve
// their measured frame extents at walls rather than clipping the artwork.
{const a=DB119_ART['corrupt-roll'],p=a.pivot;DB119.pad={left:Math.ceil(Math.max(...a.meta.map(m=>p[0]-m.bounds[0])))+2,right:Math.ceil(Math.max(...a.meta.map(m=>m.bounds[2]-p[0])))+2,top:Math.ceil(Math.max(...a.meta.map(m=>p[1]-m.bounds[1])))+2,bottom:Math.ceil(Math.max(...a.meta.map(m=>m.bounds[3]-p[1])))+2};}
function db119Bounds(){const p=DB119.pad;return{left:camLeftX()+p.left,right:camRightX()-p.right,top:viewTopY()+p.top+36,bottom:VH-p.bottom-12};}
function db119HomeY(){const a=DB119_ART['corrupt-fold'];return Math.max(viewTopY()+viewH()*.30,viewTopY()+a.pivot[1]-a.meta[0].bounds[1]+46);}
function db119Own(b){return rd74Own(b)&&hb20State(b)?.action?.type==='ball';}
function db119Log(event,data={}){DB119.events.push({event,clock:efxClock,...data});if(DB119.events.length>600)DB119.events.shift();}
function db119Start(b){const Q=rd74Init(b),p=b20Target(b),dir=p.x>=b.x?1:-1;
 const A=Q.action={type:'ball',t:0,approach:.35,fold:1.25,tell:1.60,rollTime:3.85,settle:.22,unfold:1.15,duration:6.82,from:{x:b.x,y:b.y},origin:{x:b.x,y:Math.max(b.y,db119HomeY())},target:{x:p.x,y:p.y},serial:++RD74.serial,hit:new Set(),vx:150*dir,vy:165,angle:0,bounces:0,deflected:false};
 Q.shield=0;Q.previousHead=null;Q.pendingGun=Q.pendingArsenal=false;Q.parts[1].destroyed=Q.parts[2].destroyed=true;b._lastPart=Q.parts[0];b._noHit=false;
 b20Cue('bossWeaponCharge');rd74Log('attack-start',{type:'ball',hp:b.hp});db119Log('curl-start');return A;
}
hb20Start=function(b,type){if(rd74Own(b)){
 const Q=rd74Init(b),ready=Q.opening&&Q.chrome&&!Q.pendingGun&&!Q.pendingArsenal&&!Q.pendingRecall&&(Q.rage||b.hp>b.maxhp*.29);
 // Restore the ball slot that RD74 previously aliased to the standing spin.
 if(type==='ball'||type==null&&ready&&Q.seq%6===3){if(type==null)Q.seq++;return db119Start(b);}
 }return DB119.base.start.apply(this,arguments);};
function db119Phase(A){const end=A.rollEnd??A.tell+A.rollTime;return A.t<A.tell?'curl':A.t<end?'roll':A.t<end+A.settle?'settle':'unfold';}
hb20Pose=function(b){if(!db119Own(b))return DB119.base.pose.apply(this,arguments);const Q=hb20State(b),A=Q.action,phase=db119Phase(A),end=A.rollEnd??A.tell+A.rollTime;
 if(A.t<A.approach)return rd74Sample('retract_'+rd74Mat(Q),16);
 let bank='corrupt-fold',f;if(phase==='curl')f=Math.min(15,Math.floor((A.t-A.approach)/A.fold*16));
 else if(phase==='roll'||phase==='settle'){bank='corrupt-roll';let angle=A.angle;if(phase==='settle'){const u=clamp((A.t-end)/A.settle,0,1);angle=lerp(A.settleAngle??A.angle,Math.ceil((A.settleAngle??A.angle)/TAU)*TAU,u);}f=((Math.floor(angle/TAU*16)%16)+16)%16;}
 else f=15-Math.min(15,Math.floor((A.t-end-A.settle)/A.unfold*16));
 return ba119Corrupt(Q,f,bank);
};
function db119EndRoll(b,A){if(A.unfoldFrom)return;A.rollEnd=A.t;A.duration=A.t+A.settle+A.unfold;A.settleAngle=A.angle;A.unfoldFrom={x:b.x,y:b.y};db119Log('roll-end',{deflected:A.deflected,bounces:A.bounces});}
v19NativeTick=function(b,dt){const A=db119Own(b)&&hb20State(b).action;if(!A)return DB119.base.tick.apply(this,arguments);
 const out=DB119.base.tick.apply(this,arguments);if(hb20State(b).action!==A){db119Log('unfold-complete');return out;}
 dt=clamp(dt,0,.05);const phase=db119Phase(A),Q=hb20State(b);
 if(phase==='curl'){const u=v19Ease(clamp(A.t/A.approach,0,1));b.x=lerp(A.from.x,A.origin.x,u);b.y=lerp(A.from.y,A.origin.y,u);}
 else if(phase==='roll'){
  if(!A.launched){A.launched=true;A.previous={x:b.x,y:b.y};b20Cue('hammerThrow');db119Log('roll-start');}
  A.angle+=dt*9;const speed=diffKey==='furious'?1.45:diffKey==='hard'?1.15:1,prev={x:b.x,y:b.y};b.x+=A.vx*dt*speed;b.y+=A.vy*dt*speed;
  const {left:l,right,top,bottom}=db119Bounds();let edge=false;
  if(b.x<l){b.x=l;A.vx=Math.abs(A.vx);edge=true;}if(b.x>right){b.x=right;A.vx=-Math.abs(A.vx);edge=true;}
  if(b.y<top){b.y=top;A.vy=Math.abs(A.vy);edge=true;}if(b.y>bottom){b.y=bottom;A.vy=-Math.abs(A.vy);edge=true;}
  if(edge){if(A.deflected){A.vx=A.vy=0;db119EndRoll(b,A);}else{A.bounces++;A.hit=new Set();if(efxClock>=(A.nextBang||0)){A.nextBang=efxClock+.15;b20Cue('hammerImpact');}db119Log('ricochet');}}
  b20HitSegment(b,prev,b,DB119.radius-7,'Corrupted Chronos spiked ball',A.hit);
 }else{
  db119EndRoll(b,A);if(phase==='unfold'){const u=v19Ease(clamp((A.t-A.rollEnd-A.settle)/A.unfold,0,1)),home={x:(camLeftX()+camRightX())/2,y:db119HomeY()};b.x=lerp(A.unfoldFrom.x,home.x,u);b.y=lerp(A.unfoldFrom.y,home.y,u);}
 }
 Q.parts[0].hp=b.hp;Q.parts[1].destroyed=Q.parts[2].destroyed=true;b._drawY=b.y;return out;
};
v19HammerRig=function(b){if(!db119Own(b))return DB119.base.rig.apply(this,arguments);const Q=hb20State(b),q=hb20Pose(b),core=b20Piece(Q.parts[0],q.a,b,0,1,'core',1);core._rd74=true;return[core];};
modularHit=function(dmg){const b=boss;if(!db119Own(b)||!(dmg>0)||!r30Live(b)||b._noHit)return DB119.base.hit.apply(this,arguments);
 const Q=hb20State(b),A=Q.action,q=_dmgBullet,rocket=_dmgSrc==='missile'||hammerMissile(q);A.hitKind=rocket?'rocket':'projectile';b._lastPart=Q.parts[0];
 const result=DB119.base.hit.apply(this,arguments);markHit(b,.12);markHit(Q.parts[0],.12);
 // Like native Chronos's ball, physical impacts get their explicit short
 // response even when the general boss strobe gate is between pulses.
 b.flash=Math.max(b.flash||0,.12);Q.parts[0].flash=Math.max(Q.parts[0].flash||0,.12);
 if(rocket&&db119Phase(A)==='roll'){
  // Commit away from the current shooter; never home back onto the player.
  const p=targetShip(b.x,b.y),dx=b.x-p.x,dy=b.y-p.y,m=Math.hypot(dx,dy)||1;A.vx=(m===1&&dx===0?0:dx/m)*240;A.vy=(dx===0&&dy===0?-1:dy/m)*240;A.deflected=true;A.hit=new Set();b20Cue('hammerImpact');db119Log('rocket-deflect',{vx:A.vx,vy:A.vy});
 }else db119Log(rocket?'rocket-hit':'projectile-hit');return result;
};
rd74Blit=function(q,x,y,hit=false){const b=boss;if(db119Own(b)&&q?.a?.bank==='rage_flame')return true;
 if(db119Own(b)&&q?.a?.bank?.startsWith('ba119_corrupt-')&&/corrupt-(fold|roll)_/.test(q.a.bank)){
 const a=RD74_ART.banks[q.a.bank],A=hb20State(b).action,f=q.a.frame,flash=Math.max(b.flash||0,db119PartFlash(b));
 const name=q.a.bank.startsWith('ba119_corrupt-fold')?'corrupt-fold':'corrupt-roll',key=flash>0?(A.hitKind==='projectile'?'nca_ba119_'+name+'_red_hit':a.hitKey):a.key;
 if(!XART.rdy(key))return false;ctx.drawImage(XART.get(key),f%a.cols*a.cw,Math.floor(f/a.cols)*a.ch,a.cw,a.ch,Math.round(x-a.pivot[0]),Math.round(y-a.pivot[1]),a.cw,a.ch);RD74.draws[q.a.bank]=(RD74.draws[q.a.bank]||0)+1;return true;
 }return DB119.base.blit.apply(this,arguments);};
function db119PartFlash(b){return hb20State(b)?.parts?.[0]?.flash||0;}
v19DonorDraw=function(b){const out=DB119.base.draw.apply(this,arguments);if(db119Own(b)){const A=hb20State(b).action;if(A.t<A.tell){const {left:l,right,bottom}=db119Bounds(),tx=A.vx>0?(right-b.x)/A.vx:(l-b.x)/A.vx,ty=(bottom-b.y)/A.vy,t=Math.max(0,Math.min(tx>0?tx:Infinity,ty>0?ty:Infinity));
 combatWarningDraw(A,{x:b.x,y:b.y,ex:b.x+A.vx*t,ey:b.y+A.vy*t,width:DB119.radius*2,progress:clamp(A.t/A.tell,0,1),fieldOnly:true});}}return out;};
globalThis.BOF_DRACODIA_BALL=DB119;
