"use strict";
/* Death-reference soul bomb: authored PixelLab charge, skull comet and rupture.
   The ghost's existing soulBurst slot owns the entire committed attack. */
const SOUL19={events:[],serial:0,draws:{charge:0,flight:0,burst:0},base:{start:v18StartAttack,tick:v18AttackTick,warnings:v18Warnings,draw:r30DrawBoss,rig:v18Rig,clear:v18Clear,keys:v18Keys,warm:v18Warm,load:stageLoadBegin,sound:r30Sound}};
for(const a of Object.values(SOUL19_ART.banks).flat())XART._src[a.key]=a.path;
function soul19Keys(){return Object.values(SOUL19_ART.banks).flat().map(a=>a.key);}
function soul19Warm(){if(typeof Snd!=='undefined'&&Snd.prepare)for(const cue of ['bossWeaponCharge','spaceShadowRelease','fireIceOrbImpact'])Snd.prepare(cue);let ready=true;for(const k of soul19Keys())if(!XART.rdy(k))ready=false;return ready;}
v18Keys=function(){return [...SOUL19.base.keys(),...soul19Keys()];};
v18Warm=function(){const ready=SOUL19.base.warm();return soul19Warm()&&ready;};
stageLoadBegin=function(n,keys){return SOUL19.base.load.call(this,n,[...(keys||[]),...(n===8?soul19Keys():[])]);};
function soul19Log(event,data={}){SOUL19.events.push({event,...data});if(SOUL19.events.length>120)SOUL19.events.shift();}
function soul19Rank(){return diffKey==='furious'?3:diffKey==='hard'?2:diffKey==='normal'?1:0;}
function soul19Cue(key){if(typeof Snd!=='undefined')Snd.play(key);}
function soul19Begin(b,P){const d=soul19Rank(),choices=[];
 for(const seat of seatList())withSeat(seat,()=>{if(!player.dead&&!player.out)choices.push({x:player.x,y:player.y,seat});});
 const target=choices[SOUL19.serial++%Math.max(1,choices.length)]||{x:P.tx,y:P.ty,seat:1};
 const cast={x:b.x,y:b.y+90*v18Size(b)/320},dx=target.x-cast.x,dy=target.y-cast.y,distance=Math.hypot(dx,dy),speed=[185,205,225,245][d];
 Object.assign(P,{type:'soulBomb',tell:[1.85,1.65,1.45,1.30][d],cast,target:{...target},speed,travel:Math.max(.40,distance/speed),radius:22,burstRadius:43,burstLive:.18,burstLife:.65,hit:new Set(),started:false,phase:'charge',x:cast.x,y:cast.y});
 P.active=P.travel+P.burstLife+.30;P.t=0;b._r30.attack=P;
 soul19Cue('bossWeaponCharge');soul19Log('charge',{difficulty:diffKey,target:P.target,tell:P.tell});return P;
}
r30Sound=function(key){if(SOUL19.choosing&&key==='shadowCharge'){SOUL19.queuedCharge=true;return;}return SOUL19.base.sound.apply(this,arguments);};
v18StartAttack=function(b){const ghost=v19Organic(b)&&v18Model(b)==='ghost';SOUL19.choosing=ghost;SOUL19.queuedCharge=false;let r;
 try{r=SOUL19.base.start.apply(this,arguments);}finally{SOUL19.choosing=false;}
 const P=b?._r30?.v18?.attack;
 if(P?.type==='soulBurst'&&ghost)soul19Begin(b,P);else if(SOUL19.queuedCharge)SOUL19.base.sound('shadowCharge');
 SOUL19.queuedCharge=false;return r;
};
function soul19Hit(P,from,to,radius){const L={x:from.x,y:from.y,ex:to.x,ey:to.y};
 for(const seat of seatList())withSeat(seat,()=>{if(!P.hit.has(seat)&&!player.dead&&!player.out&&player.invuln<=0&&s81003Distance(player.x,player.y,L)<radius){P.hit.add(seat);playerHit('spectral soul bomb');soul19Log('contact',{seat,phase:P.phase});}});
}
v18AttackTick=function(b,dt){const N=b?._r30?.v18,P=N?.attack;if(P?.type!=='soulBomb')return SOUL19.base.tick.apply(this,arguments);
 if(b.dead||b._r30.mode!=='fight'){v18Clear(b);return;}
 const before=P.t;P.t+=clamp(dt||0,0,.05);combatWarningTick(b,'soul-bomb-'+N.seq,Math.min(P.t,P.tell),P.tell);
 if(P.t<P.tell)return;
 if(!P.started){P.started=true;P.phase='flight';soul19Cue('spaceShadowRelease');soul19Log('release',{target:P.target});}
 const u=P.t-P.tell,old={x:P.x,y:P.y},progress=clamp(u/P.travel,0,1);
 P.x=lerp(P.cast.x,P.target.x,progress);P.y=lerp(P.cast.y,P.target.y,progress);
 if(u<P.travel){P.phase='flight';soul19Hit(P,old,P,P.radius);}
 else {P.phase='burst';if(!P.exploded){P.exploded=true;soul19Cue('fireIceOrbImpact');shake=Math.max(shake,4);soul19Log('burst',{x:P.x,y:P.y});}
  // A large update cannot skip the last segment into the visible burst.
  if(before<P.tell+P.travel)soul19Hit(P,old,P,P.radius);
  if(u<P.travel+P.burstLive)soul19Hit(P,P,P,P.burstRadius);
 }
 if(u>=P.active){N.attack=null;N.acting=null;b._r30.attack=null;b._r30.cd=[1.15,1.0,.85,.70][soul19Rank()];j3State(b).attacks++;soul19Log('complete');}
};
v18Warnings=function(b){const P=b?._r30?.v18?.attack;if(P?.type!=='soulBomb')return SOUL19.base.warnings.apply(this,arguments);
 const progress=clamp(P.t/P.tell,0,1);
 if(P.t<P.tell){combatWarningDraw(b,{x:P.cast.x,y:P.cast.y,ex:P.target.x,ey:P.target.y,width:P.radius*2+16,progress,fieldOnly:true});groundTargetReticleDraw(P.target.x,P.target.y,P.burstRadius*2+14,progress,.90);}
 else if(P.phase==='flight')groundTargetReticleDraw(P.target.x,P.target.y,P.burstRadius*2+14,1,.90);
};
function soul19Blit(bank,age,x,y,size,alpha=1,once=false){const rows=SOUL19_ART.banks[bank],f=once?Math.min(rows.length-1,Math.floor(clamp(age/.65,0,.999)*rows.length)):Math.floor(age*20)%rows.length,a=rows[f];
 if(!a||!XART.rdy(a.key))return;const k=size/a.w;ctx.save();ctx.globalAlpha*=alpha;ctx.imageSmoothingEnabled=false;
 ctx.drawImage(XART.get(a.key),x-a.pivot[0]*k,y-a.pivot[1]*k,a.w*k,a.h*k);ctx.restore();SOUL19.draws[bank]++;
}
function soul19Draw(b){const P=b?._r30?.v18?.attack;if(P?.type!=='soulBomb'||b.dead||b._r30.mode!=='fight')return;
 const u=P.t-P.tell;if(u<0){const p=clamp(P.t/P.tell,0,1);soul19Blit('charge',P.t,P.cast.x,P.cast.y,lerp(30,112,p));}
 else if(u<P.travel){
  // Sparse authored spectral afterimages are harmless; collision follows the head.
  for(const back of [.16,.08]){const t=Math.max(0,u-back),p=clamp(t/P.travel,0,1);soul19Blit('flight',t,lerp(P.cast.x,P.target.x,p),lerp(P.cast.y,P.target.y,p),192,back===.16?.10:.18);}
  soul19Blit('flight',u,P.x,P.y,192);
 }else if(u<P.travel+P.burstLife)soul19Blit('burst',u-P.travel,P.target.x,P.target.y,280,1,true);
}
r30DrawBoss=function(b){const r=SOUL19.base.draw.apply(this,arguments);soul19Draw(b);return r;};
v18Rig=function(b){const rig=SOUL19.base.rig.apply(this,arguments),P=b?._r30?.v18?.attack;if(P?.type!=='soulBomb'||v18Model(b)!=='ghost')return rig;
 const hold=P.t<P.tell?clamp(P.t/.4,0,1):1-clamp((P.t-P.tell)/.35,0,1);
 return rig.map(v=>{if(!['left','right'].includes(v.p.id)||!v.anchor)return v;const rot=v.rot+(v.p.id==='left'?-.55:.55)*hold,a=v.a,k=v.k,dx=((a.bounds[0]+a.bounds[2])/2-v.anchor[0])*k,dy=((a.bounds[1]+a.bounds[3])/2-v.anchor[1])*k;
  return {...v,rot,x:v.ax+dx*Math.cos(rot)-dy*Math.sin(rot),y:v.ay+dx*Math.sin(rot)+dy*Math.cos(rot)};});
};
v18Clear=function(b){const P=b?._r30?.v18?.attack;if(P?.type==='soulBomb')soul19Log('cancel',{phase:P.phase});return SOUL19.base.clear.apply(this,arguments);};
window.BOF_SOUL_BOMB={state:SOUL19,begin:soul19Begin,draw:soul19Draw,warm:soul19Warm};
