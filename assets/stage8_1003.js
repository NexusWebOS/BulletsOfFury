"use strict";
/* Stage 8 authored combat reels. Each tell, beam, pose and lock shares geometry.
   Ordinary hulls keep the October 2 facing rule; only positions follow orbits. */
for(const a of Object.values(S81003_ART))XART._src[a.key]=a.path;
const S81003={beams:[],effects:[],clock:0,serial:0};
const S81003_BASE={warm:r30Warm,begin:beginStage,spawn:spawnEnemy,tick:s8MegaTick,
 drawEnemy:drawEnemy,projectile:drawCombatFinalProjectile,update:updatePlay,bullets:drawBullets,
 attack:r30Attack,attackTick:r30AttackTick,pose:r30Pose,parts:r30Parts,at:r30At,
 shield:r30ShieldBounds,draw:r30DrawBoss,clear:r30Clear,form:r30Form,
 aiEnd:ai27End,entry:enemyEntrySweep,frenzy:enemyFrenzyTick,movable:sepMovable,blit:r30Blit,targets:retinaBossTargets,damage:modularHit};
function s81003WarningWarm(){
 l23FovWarm();XART.rdy('hammer_reticle');XART.rdy('fx_ground_target_reticle');
 for(const tint of [null,'yellow','red'])hammerFrame('reticle',0,tint);
}
function s81003Warm(){for(const a of Object.values(S81003_ART))XART.rdy(a.key);s81003WarningWarm();}
r30Warm=function(){S81003_BASE.warm();s81003Warm();};
beginStage=function(n){S81003.beams.length=0;S81003.effects.length=0;S81003.clock=0;S81003.serial=0;const r=S81003_BASE.begin.apply(this,arguments);if(n===8)s81003Warm();return r;};
function s81003Cell(name,frame,x,y,w,h,alpha=1,angle=0,tint=null){
 const a=S81003_ART[name];if(!a||!XART.rdy(a.key))return false;
 const f=clamp(frame|0,0,a.frames-1);ctx.save();ctx.globalAlpha*=alpha;ctx.imageSmoothingEnabled=false;
 ctx.translate(x,y);if(angle)ctx.rotate(angle);
 ctx.drawImage(tint?xartTint(a.key,tint,1):XART.get(a.key),(f%a.cols)*a.cw,Math.floor(f/a.cols)*a.ch,a.cw,a.ch,-w/2,-h/2,w,h);ctx.restore();return true;
}
function s81003Distance(x,y,L){const dx=L.ex-L.x,dy=L.ey-L.y,d=dx*dx+dy*dy,u=d?clamp(((x-L.x)*dx+(y-L.y)*dy)/d,0,1):0;return Math.hypot(x-L.x-dx*u,y-L.y-dy*u);}
function s81003Lane(x,y,tx,ty,width=12,len=VH*1.3){const a=Math.atan2(ty-y,tx-x);return{x,y,ex:x+Math.cos(a)*len,ey:y+Math.sin(a)*len,width};}
function s81003Fov(L,p,retina=true,owner=boss){
 // Use the original renderer at the source for every caller, including Stage 7.
 // Passing the emitter preserves ordinary enemy bands versus boss FOV art.
 combatWarningDraw(owner,{x:L.x,y:L.y,ex:L.ex,ey:L.ey,len:Math.hypot(L.ex-L.x,L.ey-L.y),
  width:L.width,progress:clamp(p,0,1),fieldOnly:true});
 if(retina&&L.tx!=null)s81003Target(L.tx,L.ty,74,p);
}
function s81003Target(x,y,d,p){return groundTargetReticleDraw(x,y,d,clamp(p,0,1),.85);}
function s81003Beam(owner,L,kind,dur=.58){
 const q={...L,owner,kind,t:0,dur};S81003.beams.push(q);r30Sound('combatBeam0927');return q;
}
function s81003BeamsTick(dt){
 S81003.clock+=dt;
 for(const f of S81003.effects){f.t+=dt;if(f.kind==='shards'){f.x+=f.vx*dt;f.y+=f.vy*dt;f.a+=f.spin*dt;f.vx*=Math.exp(-.75*dt);f.vy*=Math.exp(-.75*dt);}}
 S81003.effects=S81003.effects.filter(f=>f.t<f.dur);
 S81003.beams=S81003.beams.filter(q=>!q.owner.dead&&q.owner._dyingT==null&&q.owner.hp>0&&(!q.owner._r30||q.owner._r30.mode==='fight')&&(q.t+=dt)<q.dur);
 for(const q of S81003.beams)for(const seat of seatList())withSeat(seat,()=>{
  if(!player.dead&&s81003Distance(player.x,player.y,q)<q.width*.5+3)playerHit(q.kind==='code'?'binary laser':'alien laser');
 });
}
function s81003BeamsDraw(){for(const q of S81003.beams){
 const dx=q.ex-q.x,dy=q.ey-q.y,len=Math.hypot(dx,dy),frame=(q.kind==='code'?4:0)+Math.floor(q.t*18)%4;
 // Cell origin includes 7% leading alpha: extend behind the emitter so the
 // visible laser starts at the same point as its warning and collision.
 const a=Math.atan2(dy,dx),h=len/ .91,cx=q.x+Math.cos(a)*(h*.5-h*.07),cy=q.y+Math.sin(a)*(h*.5-h*.07);
 s81003Cell('beams',frame,cx,cy,q.width*3.4,h,Math.min(1,(q.dur-q.t)/.09),a-Math.PI/2);
}}
updatePlay=function(dt){const r=S81003_BASE.update.apply(this,arguments);if(run.stage===8&&state===GS.PLAY)s81003BeamsTick(Math.min(dt,.05));else if(run.stage!==8)S81003.beams.length=0;return r;};
drawBullets=function(){const r=S81003_BASE.bullets.apply(this,arguments);s81003BeamsDraw();s81003ShieldEffectsDraw();return r;};

function s81003ShieldEffectsDraw(){for(const f of S81003.effects){
 const n=f.kind==='shatter'?16:8,frame=f.kind==='shards'?f.frame:Math.min(n-1,Math.floor(f.t/f.dur*n));
 s81003Cell(f.kind,frame,f.x,f.y,f.size,f.size,Math.min(1,(f.dur-f.t)/.25),f.a||0);
}}
function s81003ShieldShatter(b,q){
 const size=Math.min(440,Math.max(q.w,q.h)*1.4);
 S81003.effects.push({kind:'shatter',x:q.x,y:q.y,size,t:0,dur:1.0});
 // Generated crystal chunks travel through every octant; they are visual
 // fragments, not hostile projectiles or a second collision shield.
 for(let i=0;i<16;i++){const a=i*TAU/16,sp=(140+(i%3)*28)*clamp(Math.max(q.w,q.h)/240,.9,1.6);
  S81003.effects.push({kind:'shards',frame:i%4,x:q.x+Math.cos(a)*q.w*.28,y:q.y+Math.sin(a)*q.h*.28,
   vx:Math.cos(a)*sp,vy:Math.sin(a)*sp,a,spin:(i%2?-1:1)*(2+i%3),size:25+(i%3)*9,t:0,dur:1.05+(i%4)*.12});
 }
 // The old damage route already plays the shield-break cue exactly once.
 shake=Math.max(shake,7);b._r30.history.push({event:'shieldShatter1003',x:q.x,y:q.y,shards:16});
 // Replace the former short, centered disintegration cell with this reel.
 b._r30.fx=b._r30.fx.filter(f=>f.kind!=='shield');
}
modularHit=function(dmg){
 const b=boss,S=b?._r30;if(!S||S.shield<=0||!r30Live(b))return S81003_BASE.damage.apply(this,arguments);
 const before=S.shield,q=r30ShieldBounds(b),r=S81003_BASE.damage.apply(this,arguments);
 if(S.shield<before){
  if(S.wallImpactAt1003==null||S.clock-S.wallImpactAt1003>=.07){
   S.wallImpactAt1003=S.clock;
   const hx=typeof _lastHitX==='number'&&Math.abs(_lastHitX-q.x)<q.w*.5?_lastHitX:q.x;
   const hy=typeof _lastHitY==='number'&&Math.abs(_lastHitY-q.y)<q.h*.5?_lastHitY:q.y+q.h*.35;
   S81003.effects.push({kind:'impact',x:hx,y:hy,size:64,t:0,dur:.38});
   if(S.shield>0)(Audio.SFX.projectileRicochet||Audio.SFX.shieldDeflect||function(){})();
  }
  if(S.shield<=0)s81003ShieldShatter(b,q);
  if(S81003.effects.length>64)S81003.effects.splice(0,S81003.effects.length-64);
 }return r;
};

/* Campaign replacements ride existing wave beats rather than adding density. */
const S81003_ROLES={s8leech:'gravity',s8hunter:'stalker',s8solar:'prism',s8gravity1003:'gravity',s8stalker1003:'stalker',s8prism1003:'prism'};
spawnEnemy=function(type,x,y,opt={}){
 const role=run.stage===8?S81003_ROLES[type]:null;
 const alias={s8gravity1003:'s8leech',s8stalker1003:'s8hunter',s8prism1003:'s8solar'}[type]||type;
 const e=S81003_BASE.spawn(alias,x,y,opt);if(!e||!role)return e;
 e._alien1003=role;e.w=role==='stalker'?112:role==='prism'?86:102;e.h=role==='prism'?126:108;
 e.hp=e.maxhp=e._maxhp=EHP(role==='gravity'?28:role==='prism'?36:30);e._s8mega=alias;e.pattern='s8mega';e.shoots=false;e.spin=0;e._frFlight=false;
 e._orbit1003={id:++S81003.serial,phase:'entry',t:0,age:0,cycles:0,homeX:clamp(e.x,camLeftX()+80,camRightX()-80),homeY:viewTopY()+viewH()*.27,theta:0,side:(S81003.serial%2?1:-1),cd:.9};
 s81003Warm();return e;
};
// This controller owns its route and difficulty speed. Generic entry arcs,
// dodges and frenzied lunges would move an emitter away from its locked lane.
enemyEntrySweep=function(e,dt){if(e._alien1003)return;return S81003_BASE.entry.apply(this,arguments);};
enemyFrenzyTick=function(e,dt){if(e._alien1003)return;return S81003_BASE.frenzy.apply(this,arguments);};
ai27End=function(e,prev){if(e?._alien1003){e._frFlight=false;if(e._ai27)e._ai27.dx=0;}return S81003_BASE.aiEnd.apply(this,arguments);};
sepMovable=function(e){if(e?._alien1003&&['tell','fire'].includes(e._orbit1003.phase))return false;return S81003_BASE.movable.apply(this,arguments);};
function s81003EnemyLanes(e,A){
 const tx=player.x,ty=player.y,role=e._alien1003;
 if(role==='gravity'){
  const aim=Math.atan2(ty-e.y,tx-e.x),count=diffKey==='easy'?7:9+fr27Difficulty()*2,step=TAU/count,lanes=[];
  for(let i=0;i<count;i++){const a=aim+step*i;if(Math.abs(Math.atan2(Math.sin(a-aim),Math.cos(a-aim)))<step*1.15)continue;
   lanes.push(s81003Lane(e.x,e.y,e.x+Math.cos(a)*230,e.y+Math.sin(a)*230,12,230));
  }return lanes;
 }
 if(role==='stalker')return [-1,1].map(side=>({...s81003Lane(e.x+side*e.w*.225,e.y-e.h*.10,tx+side*28,ty,10),tx:tx+side*28,ty}));
 return [{...s81003Lane(e.x,e.y+e.h*.32,tx,ty,14),tx,ty}];
}
function s81003EnemyTick(e,dt){
 const A=e._orbit1003,n=fr27Difficulty(),easy=diffKey==='easy';A.t+=dt;A.age+=dt;e.spin=e._bank=e._frBank=0;e._s8Roll=null;e._furyMove=null;
 if(A.phase==='entry'){
  const d=A.homeY-e.y;e.y+=Math.min(d,100*dt);if(d<=1){e.y=A.homeY;A.phase='orbit';A.age=0;}return;
 }
 if(A.phase==='leave'){e.y+=115*dt;if(e.y>VH+150)e.dead=true;return;}
 if(A.phase==='orbit'){
  A.theta+=dt*(easy?.55:[.7,.9,1.05][n])*A.side;
  const radius=Math.min(68,(camRightX()-camLeftX())*.13),tx=clamp(A.homeX+Math.sin(A.theta)*radius,camLeftX()+e.w*.6,camRightX()-e.w*.6),ty=A.homeY+Math.sin(A.theta*1.35)*32;
  e.x+=clamp(tx-e.x,-100*dt,100*dt);e.y+=clamp(ty-e.y,-85*dt,85*dt);A.cd-=dt;
  // At most two simultaneous charge/fire owners on Normal/Hard (one Easy,
  // three Furious). A waiting unit continues its orbit, never fires blind.
  const busy=enemies.filter(o=>o!==e&&!o.dead&&['tell','fire'].includes(o._orbit1003?.phase)).length;
  if(A.cd<=0&&busy<(easy?1:n===2?3:2)&&e.y<player.y-85&&e.x>camLeftX()+20&&e.x<camRightX()-20){
   A.phase='tell';A.age=0;A.warm=easy?1.55:[1.30,1.10,.94][n];A.lanes=s81003EnemyLanes(e,A);A.locked=false;r30Sound('bossWeaponCharge');
  }return;
 }
 if(A.phase==='tell'){
  if(A.age<A.warm*.36)A.lanes=s81003EnemyLanes(e,A);else A.locked=true;
  combatWarningTick(e,'alien1003-'+A.id+'-'+A.cycles,A.age,A.warm);
  if(A.age>=A.warm){A.phase='fire';A.age=0;A.cycles++;
   if(e._alien1003==='gravity'){
    // Every warning spoke becomes one orb; the omitted committed lane stays open.
    for(const L of A.lanes){const a=Math.atan2(L.ey-L.y,L.ex-L.x);
     const q=eShootT(e.x,e.y,a,easy?2:[2.35,2.7,3.1][n],'s8pair',{w:19,h:19,silent:true});q._alienOrb1003=true;q._noArsenal=true;
    }r30Sound('combatAlien0927');
   }else for(const L of A.lanes)s81003Beam(e,L,e._alien1003==='prism'?'code':'alien',easy?.42:[.52,.62,.7][n]);
  }return;
 }
 if(A.phase==='fire'&&A.age>.78){A.phase=A.cycles>=(easy?2:3)?'leave':'orbit';A.age=0;A.cd=easy?3.4:[2.6,2.2,1.85][n];}
}
s8MegaTick=function(e,dt){if(e._alien1003)return s81003EnemyTick(e,Math.min(.05,dt));return S81003_BASE.tick.apply(this,arguments);};
drawEnemy=function(e){
 if(!e._alien1003)return S81003_BASE.drawEnemy.apply(this,arguments);if(e.dead)return;
 const A=e._orbit1003,phase=A.phase,f=phase==='tell'?A.age/A.warm<.55?1:2:phase==='fire'?3:0;
 if(phase==='tell')for(const L of A.lanes)s81003Fov(L,A.age/A.warm,true,e);
 // Reference sheet hull center is 44% down the padded frame. Feet/exhaust
 // extend lower; dimensions are intentionally not the full image rectangle.
 s81003Cell(e._alien1003,f,e.x,e.y+e.h*.08,e.w*1.14,e.h*1.52,1);
 if(e.flash>0)s81003Cell(e._alien1003,f,e.x,e.y+e.h*.08,e.w*1.14,e.h*1.52,Math.min(1,e.flash*9),0,'#ffffff');
};
drawCombatFinalProjectile=function(q,role){if(q._alienOrb1003)return s81003Cell('fov',8+Math.floor((q.t||S81003.clock)*16)%4,q.x,q.y,30,35,1);return S81003_BASE.projectile.apply(this,arguments);};

/* The binary barrier is one full rectangular wall. Height growth retains its
   bottom anchor; no floating miniature shield or elliptical hit envelope. */
r30ShieldBounds=function(b){
 if(b._r30?.attack?.type==='knight'&&b._r30.attack.k1003){const p=s81003KnightPose(b);return{x:p.x,y:p.y,w:216,h:224};}
 const q=S81003_BASE.shield(b);return{...q,w:q.w*1.06,h:q.h};
};
function s81003ShieldDraw(b){const S=b._r30;if(S.shield<=0)return;const q=r30ShieldBounds(b),age=S.wallAge1003||0;
 const f=age<.42?Math.min(3,Math.floor(age/.42*4)):S.shieldFlash>0?8:4+Math.floor(S.clock*12)%4;
 s81003Cell('wall',f,q.x,q.y,q.w,q.h,.78);
}
r30At=function(b,x,y){
 if(!b?._r30)return S81003_BASE.at(b,x,y);if(!r30Live(b))return null;
 const S=b._r30,Q=r30Pose(b);if(Q.alpha<.25||S.ghostHidden)return null;
 if(S.shield>0){const q=r30ShieldBounds(b);if(Math.abs(x-q.x)<=q.w*.5&&Math.abs(y-q.y)<=q.h*.5)return{id:'shield',hp:S.shield,dmg:true};}
 // The existing routine has an ellipse check; once our rectangle has missed,
 // temporarily omit that legacy envelope and retain authored module testing.
 const shield=S.shield;S.shield=0;try{return S81003_BASE.at(b,x,y);}finally{S.shield=shield;}
};
r30Form=function(b,n){S81003_BASE.form.apply(this,arguments);b._r30.wallAge1003=0;};
r30Clear=function(b){S81003.beams=S81003.beams.filter(q=>q.owner!==b);return S81003_BASE.clear.apply(this,arguments);};

function s81003KnightEnter(b,phase){
 const P=b._r30.attack,K=P.k1003;K.phase=phase;K.age=0;K.hit=false;
 b._r30.history.push({event:'knight1003',phase});
 if(phase==='guard'){const S=b._r30;S.shield=S.shieldMax=Math.ceil(S.base*.035);S.wallAge1003=0;r30Sound('combatEnergy0927');}
 if(phase==='slashTell'||phase==='jumpTell'){
  K.from={x:K.x,y:K.y};K.target={x:clamp(player.x,camLeftX()+85,camRightX()-85),y:clamp(player.y,viewTopY()+180,bottomHudLayout().rail.y-35)};
  if(phase==='slashTell')b._r30.shield=0;r30Sound('bossWeaponCharge');
 }
 if(phase==='slash'||phase==='sweep')r30Sound('combatModule0927');
 if(phase==='land'){shake=Math.max(shake,8);r30Sound('hammerImpact');r30FX(b,K.target.x,K.target.y,92);}
 if(phase==='out'||phase==='in')r30Sound('teleportIn');
}
function s81003KnightStart(b){
 const P=b._r30.attack;P.k1003={phase:'morph',age:0,x:b.x,y:b.y,home:{x:b.x,y:b.y},target:{x:b.x,y:b.y+80},hit:false};
 P.tell=.8;P.active=20;b._r30.shield=0;b._r30.ghostHidden=false;
}
function s81003KnightDur(phase){const n=fr27Difficulty(),easy=diffKey==='easy';return {
 morph:.8,guard:.85,slashTell:easy?1.0:[.78,.65,.56][n],slash:.24,slashRecover:.42,
 jumpTell:easy?1.15:[.95,.80,.70][n],jump:.68,land:.16,followTell:easy?.48:[.36,.30,.26][n],sweep:.22,
 recover:easy?2.1:[1.7,1.5,1.35][n],out:.42,in:.42
 }[phase];}
function s81003KnightPose(b){
 const K=b._r30.attack.k1003,phase=K.phase,u=clamp(K.age/s81003KnightDur(phase),0,1);
 let x=K.x,y=K.y,alpha=1,scale=1,frame=0;
 const frames={morph:0,guard:b._r30.shieldFlash>0?2:1,slashTell:3,slash:4,slashRecover:5,jumpTell:6,jump:u<.58?7:8,land:9,followTell:9,sweep:10,recover:11,out:0,in:0};frame=frames[phase];
 if(phase==='morph')alpha=clamp((u-.35)/.4,0,1);
 if(phase==='slash'){const k=1-(1-u)**3;x=lerp(K.from.x,K.target.x,k);y=lerp(K.from.y,K.target.y-62,k);}
 if(phase==='jump'){x=lerp(K.from.x,K.target.x,u);y=lerp(K.from.y,K.target.y-70,u)-Math.sin(u*Math.PI)*140;scale=1+.28*Math.sin(u*Math.PI);}
 // Step forward into the follow-up; the horizontal blade's painted height
 // is the body's center. Use that very same row for warning and damage.
 if(phase==='followTell')y=lerp(K.y,K.target.y-16,u*u*(3-2*u));
 if(phase==='out')alpha=1-u;
 if(phase==='in'){x=b.x;y=b.y;alpha=u;}
 return{x,y,alpha,angle:0,shape:'knight',frame,scale};
}
r30Pose=function(b){return b._r30?.attack?.k1003?s81003KnightPose(b):S81003_BASE.pose.apply(this,arguments);};
r30Parts=function(b){if(!b._r30?.attack?.k1003)return S81003_BASE.parts.apply(this,arguments);
 const Q=s81003KnightPose(b);return [{p:b.parts.find(p=>!p.destroyed)||b.parts[0],x:Q.x,y:Q.y,w:158*Q.scale,h:194*Q.scale,rot:0,key:'s81003_knight',alpha:Q.alpha}];
};
retinaBossTargets=function(b){if(b?._r30?.attack?.k1003&&s81003KnightPose(b).alpha<.25)return [];return S81003_BASE.targets.apply(this,arguments);};
function s81003KnightHit(b,kind){
 const K=b._r30.attack.k1003,Q=s81003KnightPose(b);if(K.hit)return;K.hit=true;
 const L=kind==='sweep'?{x:Q.x-98,y:Q.y,ex:Q.x+98,ey:Q.y,width:32}:null;
 for(const seat of seatList())withSeat(seat,()=>{
  const hit=L?s81003Distance(player.x,player.y,L)<19:Math.hypot(player.x-K.target.x,player.y-K.target.y)<(kind==='land'?43:38);
  if(hit)playerHit('void knight '+kind);
 });
}
function s81003KnightTick(b,dt){
 const S=b._r30,P=S.attack,K=P.k1003;P.t+=dt;K.age+=dt;S.wallAge1003=(S.wallAge1003||0)+dt;
 const phase=K.phase,dur=s81003KnightDur(phase);
 if(['slashTell','jumpTell','followTell'].includes(phase))combatWarningTick(b,'knight1003-'+S.seq+'-'+phase,K.age,dur);
 if(phase==='slash'&&K.age>=.13)s81003KnightHit(b,'slash');
 if(phase==='land'&&K.age>=.02)s81003KnightHit(b,'land');
 if(phase==='sweep'&&K.age>=.04)s81003KnightHit(b,'sweep');
 if(K.age<dur)return;
 const pose=s81003KnightPose(b);K.x=pose.x;K.y=pose.y;
 const phases=['morph','guard','slashTell','slash','slashRecover','jumpTell','jump','land','followTell','sweep','recover','out','in'],next=phases[phases.indexOf(phase)+1];
 if(next){s81003KnightEnter(b,next);return;}
 S.attack=null;S.shield=0;S.ghostHidden=false;S.cd=1.2;S.returning={t:0,from:'knight'};r30FX(b,b.x,b.y,260,'morph');S.history.push({event:'recover'});
}
r30Attack=function(b){S81003_BASE.attack.apply(this,arguments);const P=b._r30.attack;
 // Retire the little lane shields from the live attack book. All code-wall
 // beats now raise the same full-body barrier, in every boss form.
 if(P&&['datawall','binarywall'].includes(P.type))P.type='shield';
 if(P?.type==='knight')s81003KnightStart(b);
 if(P?.type==='cannons'){P.type='codeLance1003';P.tell=diffKey==='easy'?1.6:[1.3,1.1,.96][fr27Difficulty()];P.active=.82;P.lanes=[-1,1].map(side=>({...s81003Lane(b.x+side*65,b.y+50,player.x+side*45,player.y,14),tx:player.x+side*45,ty:player.y}));}
};
r30AttackTick=function(b,dt){
 const S=b._r30,P=S.attack;if(P?.type==='knight'){if(!P.k1003)s81003KnightStart(b);return s81003KnightTick(b,dt);}
 const before=S.shield;
 if(P?.type==='codeLance1003'){
  P.t+=dt;combatWarningTick(b,'code-lance1003-'+S.seq,P.t,P.tell);
  if(P.t>=P.tell&&!P.started){P.started=true;for(const L of P.lanes)s81003Beam(b,L,'code',.65);}
  if(P.t>P.tell+P.active){S.attack=null;S.cd=1.35;S.history.push({event:'recover'});}return;
 }
 const r=S81003_BASE.attackTick.apply(this,arguments);if(S.shield>0){if(before<=0)S.wallAge1003=0;else S.wallAge1003=(S.wallAge1003||0)+dt;}return r;
};
function s81003KnightDraw(b){
 const P=b._r30.attack,K=P.k1003,Q=s81003KnightPose(b),phase=K.phase,u=clamp(K.age/s81003KnightDur(phase),0,1);
 if(phase==='slashTell'||phase==='jumpTell')s81003Target(K.target.x,K.target.y,phase==='jumpTell'?98:86,u);
 if(phase==='followTell')s81003Fov({x:Q.x-98,y:K.target.y-16,ex:Q.x+98,ey:K.target.y-16,width:32},u,false);
 if(phase==='out'||phase==='in')s81003Cell('teleport',Math.min(7,Math.floor((phase==='out'?1-u:u)*7)),Q.x,Q.y,190,280,.9);
 const size=320*Q.scale;s81003Cell('knight',Q.frame,Q.x,Q.y,size,size,Q.alpha);
 if(b.flash>0)s81003Cell('knight',Q.frame,Q.x,Q.y,size,size,Q.alpha*Math.min(1,b.flash*9),0,hitFlashColor(b,'#ffffff'));
 if(phase==='morph')s81003Cell('morph',Math.min(11,Math.floor(u*12)),Q.x,Q.y,260,270,1);
 s81003ShieldDraw(b);
}
r30DrawBoss=function(b){
 const S=b._r30,P=S.attack;if(P?.k1003&&S.mode==='fight')s81003KnightDraw(b);
 else{
  const fx=S.fx,shield=S.shield,attack=S.attack;
  S.fx=fx.filter(f=>!['morph','shield'].includes(f.kind));S.shield=0;
  if(P?.type==='codeLance1003')S.attack=null;
  try{S81003_BASE.draw(b);}finally{S.fx=fx;S.shield=shield;S.attack=attack;}
  s81003ShieldDraw(b);
  if(P?.type==='codeLance1003'&&P.t<P.tell)for(const L of P.lanes)s81003Fov(L,P.t/P.tell,true);
  if(S.mode==='reform'){const u=clamp(S.t/3.4,0,1);s81003Cell('morph',Math.min(11,Math.floor(u*12)),b.x,b.y,320,340,1);}
 }
 for(const f of S.fx){if(f.kind==='morph'&&!P?.k1003)s81003Cell('morph',Math.min(11,Math.floor(f.t/.7*12)),f.x,f.y,f.size,f.size,1);
  if(f.kind==='shield')s81003Cell('wall',9+Math.min(2,Math.floor(f.t/.7*3)),f.x,f.y,f.size,b.h,1-f.t/.7);}
};
r30Blit=function(key,x,y,w,h,a,alpha){
 const P=boss?._r30?.attack;
 if(key==='vile25_phantom_ground_portal'&&P?.type==='ghost'){
  const u=Math.max(0,P.t-P.tell)%P.cycleTime,f=Math.min(7,Math.floor(u/P.cycleTime*8));
  return s81003Cell('teleport',f,x,y-28,170,250,.8);
 }
 return S81003_BASE.blit.apply(this,arguments);
};
