'use strict';
/* Mike Oct25: faster Event Horizon rotation, vertical flight and an eye bomb.
   Existing whole plates, native HP, hits, attack book and defeat stay in charge. */
const EH25={events:[],owners:new Set(),base:{init:s9VoidHorizonInit,tick:s9VoidHorizonTick,set:s5924Set,eye:s5924Eye,draw:s9VoidHorizonDraw,
 hit:s9VoidHorizonHit,load:stageLoadBegin,update:updatePlay,ball:tb28BallDraw,warm:tb28Warm,projectile:drawCombatFinalProjectile,
 intercept:enemyOrdnanceCanIntercept,element:enemyOrdnanceElement,rules:s3kOrdnanceRules},
 cues:['bossWeaponCharge','combatOrb0927','warpBurst']};
function eh25Own(b){return !!(run.stage===9&&b?._s9rift?.s5924&&b===subBoss);}
function eh25Log(b,event,data={}){EH25.events.push({event,time:efxClock,...data});if(EH25.events.length>500)EH25.events.shift();}
function eh25State(b){if(!b._eh25){b._eh25={clock:0,flight:0,y:b._s9rift.core.y,rail:b._s9rift.core.y,spin:0,spinning:false,turn:0,bomb:null,impacts:[],frame:null};EH25.owners.add(b);}return b._eh25;}
s9VoidHorizonInit=function(b){const r=EH25.base.init.apply(this,arguments);if(b._s9rift)eh25State(b);return r;};
stageLoadBegin=function(n,keys){if(n===9)for(const c of EH25.cues)Snd.prepare(c);return EH25.base.load.call(this,n,[...(keys||[]),...(n===9?['bf22_water_orb',...s5924Keys()]:[])]);};
// Native manoeuvres keep their horizontal movement and attack clocks. The eye,
// physical core and renderer all use the independent vertical flight position.
s5924Eye=function(b){if(eh25Own(b)&&b._eh25&&!b.enter)return{x:b._s9rift.core.x,y:b._eh25.y};return EH25.base.eye.apply(this,arguments);};
function eh25Flight(b,dt){const H=eh25State(b),rank=bh25Rank();
 if(b.enter)return;const top=viewTopY()+170,bottom=Math.max(top+24,VH-197),mid=(top+bottom)/2,amp=(bottom-top)/2*[.65,.84,.94,1][rank];
 if(!H.bomb){H.flight+=dt;const to=mid-Math.cos(H.flight*[1.05,1.18,1.34,1.50][rank])*amp;H.y+=clamp(to-H.y,-[120,145,165,185][rank]*dt,[120,145,165,185][rank]*dt);}
}
function eh25Spin(b,dt){const H=eh25State(b),Q=b._s9rift.s5924,rps=[1.50,1.75,2,2.25][bh25Rank()],want=!b.enter&&!H.bomb&&Q.t>=Q.warm&&Q.t<Q.warm+Q.active;
 if(want){H.spin=(H.spin+rps*dt)%1;H.spinning=true;}
 else if(H.spinning){const step=rps*dt;if(1-H.spin<=step+1e-6){H.spin=0;H.spinning=false;}else H.spin+=step;}
 H.rps=rps;
}
function eh25Bomb(b,resume){const H=eh25State(b),F=b._s9rift,Q=F.s5924,rank=bh25Rank(),T=targetShip(F.core.x,H.y),warm=[2.1,1.95,1.80,1.65][rank];
 Q.mode='eh25-bomb';Q.t=0;Q.warm=warm;Q.active=0;Q.angles=[];
 const P=H.bomb={resume,t:0,phase:'charge',recover:0,locked:false,target:{x:T.x,y:T.y}};
 P.job=tb28Fire(b,{from:()=>eh25Own(b)&&!b.dead?s5924Eye(b):null,target:P.target,warm,track:.40,flight:[1.35,1.2,1.1,1][rank],mode:'direct',art:'eh25-energy',kind:'s9pair',size:92,width:42,reticle:94,splash:54,laneAlpha:.46,
  onRelease:q=>{if(H.bomb!==P||b.dead)return;const a=Math.atan2(q.ty-q.sy,q.tx-q.sx),shot=q.ball;P.phase='flight';
   Object.assign(shot,{_eh25Owner:b,_s5924Owner:b,_eh25Bomb:true,_eh25Born:efxClock,_weaponProof:true,_shootable:false,_s3kOriginalProof:false,_noArsenal:true,homing:false,w:42,h:42});delete shot.hp;
   wm26Emit(b,q.sx,q.sy,a,'orb','#69efff',{size:58,life:.24,follow:()=>!b.dead?s5924Eye(b):null});combatAudio0927(b,'combatOrb0927',.5);
   eh25Log(b,'bomb-release',{x:q.sx,y:q.sy,target:{x:q.tx,y:q.ty},vx:shot.vx,vy:shot.vy,flight:q.flight});},
  onArrive:(q,x,y)=>{if(H.bomb!==P||b.dead)return;P.phase='recover';H.impacts.push({x,y,t:0});combatAudio0927(b,'warpBurst',.5);shake=Math.max(shake,3);eh25Log(b,'bomb-impact',{x,y,radius:q.splash});}});
 combatAudio0927(b,'bossWeaponCharge',.8);eh25Log(b,'bomb-charge',{warm,eye:s5924Eye(b),target:P.target});
}
s5924Set=function(b,mode){if(eh25Own(b)&&mode!=='entry'&&!b.dead&&!b._bh25){const H=eh25State(b);H.turn++;if(H.turn%3===0){eh25Bomb(b,mode);return;}}
 return EH25.base.set.apply(this,arguments);
};
s9VoidHorizonTick=function(b,dt){if(!eh25Own(b))return EH25.base.tick.apply(this,arguments);const H=eh25State(b),F=b._s9rift,Q=F.s5924,w=F.core;
 if(b.dead)return true;dt=Math.max(0,Math.min(.05,dt));H.clock+=dt;for(const f of H.impacts)f.t+=dt;H.impacts=H.impacts.filter(f=>f.t<.42);
 eh25Flight(b,dt);
 if(H.bomb){const P=H.bomb;F.t+=dt;Q.t+=dt;Q.age+=dt;P.t+=dt;w.flash=Math.max(0,w.flash-dt);b.flash=Math.max(0,(b.flash||0)-dt);b.enter=false;b._late27=null;
  const q=P.job;if(!P.locked&&q.t>=q.warm*.40){P.locked=true;eh25Log(b,'bomb-aim-locked',{target:{x:q.tx,y:q.ty},remaining:q.warm-q.t});}
  if(q.arrived||q.dead){P.recover+=dt;if(q.dead&&!q.arrived&&!P.cleared){P.cleared=true;eh25Log(b,'bomb-defensively-cleared');}
   if(P.recover>=[1.35,1.25,1.15,1.05][bh25Rank()]){H.bomb=null;EH25.base.set.call(this,b,P.resume);eh25Log(b,'bomb-complete');}}
 }else{
  // Remove last frame's display displacement before the native orbit controller
  // runs. s5924Eye supplies the current physical firing height throughout it.
  w.y=b.y=H.rail;const entering=b.enter;EH25.base.tick.apply(this,arguments);H.rail=w.y;if(entering){H.y=w.y;}
 }
 eh25Spin(b,dt);w.y=H.y;b.x=w.x;b.y=b._drawY=w.y;b.hp=w.hp;return true;
};
function eh25Orb(x,y,size,age,alpha=1){ctx.save();ctx.globalAlpha*=alpha;const ok=bf22EffectDraw(BF22_ART.effects.water_orb,x,y,size,size,age*1.9,age);ctx.restore();return ok;}
tb28Warm=function(art){if(art==='eh25-energy'){XART.rdy('bf22_water_orb');return;}return EH25.base.warm.apply(this,arguments);};
tb28BallDraw=function(art,x,y,size,t,alpha){if(art==='eh25-energy')return eh25Orb(x,y,size,t,alpha??1);return EH25.base.ball.apply(this,arguments);};
drawCombatFinalProjectile=function(q){return q?._eh25Bomb?eh25Orb(q.x,q.y,92,efxClock-q._eh25Born):EH25.base.projectile.apply(this,arguments);};
enemyOrdnanceCanIntercept=function(q){return !q?._eh25Bomb&&EH25.base.intercept.apply(this,arguments);};
enemyOrdnanceElement=function(q){return q?._eh25Bomb?null:EH25.base.element.apply(this,arguments);};
s3kOrdnanceRules=function(q){if(q?._eh25Bomb){q._weaponProof=true;q._shootable=false;delete q.hp;return;}return EH25.base.rules.apply(this,arguments);};
function eh25Pose(b){const H=eh25State(b),Q=b._s9rift.s5924;let bank='black_drift',frame;
 if(H.spinning){bank='black_spin';frame=Math.floor(H.spin*(S5924_ART.banks.black_spin.frames.length-1));}
 else if(H.bomb?.phase==='charge'||Q.t<Q.warm){bank='black_charge';frame=Math.min(8,Math.floor(clamp(Q.t/Q.warm,0,.999)*9));}
 else frame=Math.floor(H.clock*14)%S5924_ART.banks.black_drift.frames.length;
 return{bank,frame,a:S5924_ART.banks[bank].frames[frame]};
}
s9VoidHorizonDraw=function(b){if(!eh25Own(b))return EH25.base.draw.apply(this,arguments);const F=b._s9rift,H=eh25State(b),P=eh25Pose(b),key=F.core.flash>0?P.a.hit:P.a.key;
 s5924Warning(b);if(!XART.rdy(key))return EH25.base.draw.apply(this,arguments);ctx.save();ctx.imageSmoothingEnabled=false;ctx.drawImage(XART.get(key),F.core.x-192,F.core.y-192,384,384);ctx.restore();H.frame={bank:P.bank,frame:P.frame,key};
 if(!b.dead&&H.bomb?.phase==='charge'){const u=clamp(H.bomb.t/F.s5924.warm,0,1),eye=s5924Eye(b);eh25Orb(eye.x,eye.y,18+74*u*u,H.clock,.40+.60*u);}
 for(const f of H.impacts)eh25Orb(f.x,f.y,92+f.t*155,H.clock,Math.max(0,1-f.t/.42));
 drawSubBossBar(b);return true;
};
function eh25Cancel(b,reason){const H=b?._eh25;if(!H)return;const P=H.bomb;if(P){P.job.dead=true;if(P.job.ball)P.job.ball.dead=true;H.bomb=null;eh25Log(b,'bomb-cancel',{reason});}
 for(const q of eBullets)if(q._eh25Owner===b)q.dead=true;H.impacts=[];EH25.owners.delete(b);
}
s9VoidHorizonHit=function(b){const r=EH25.base.hit.apply(this,arguments);if(b?.dead)eh25Cancel(b,'native-defeat');return r;};
function eh25Prune(){for(const b of EH25.owners)if(!eh25Own(b)||b.dead||b._s9rift.core.disabled)eh25Cancel(b,'native-owner-change');}
updatePlay=function(){eh25Prune();const r=EH25.base.update.apply(this,arguments);eh25Prune();return r;};
globalThis.BOF_HORIZON_ASSAULT_1025={state:EH25,pose:eh25Pose};
