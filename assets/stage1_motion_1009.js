"use strict";
/* Current Stage 1 roster, not the obsolete plates in the supplied passover.
   Authored moving parts supplement live controllers, independent gun aim and
   destructible boat modules. Props, damage, speeds and projectile art survive. */
const S1M={version:1,draws:{},shots:[],actor:null,base:{begin:beginStage,load:stageLoadBegin,
 enemy:drawEnemy,tankDraw:drawModularTank,tankTick:tankTick,jetTick:jetTick,navalTick:navalTick,
 shot:eShootT,flash:navalFlash}};
for(const frames of Object.values(S1M_ART))for(const a of frames)XART._src[a.key]=a.path;
for(let i=0;i<4;i++){XART._src['s1m_kinetic_'+i]=S1M_ART.muzzle[i].path;XART._src['s1m_rocket_'+i]=S1M_ART.muzzle[i+4].path;}
function s1mKeys(){return [...Object.values(S1M_ART).flat().map(a=>a.key),...Array.from({length:4},(_,i)=>'s1m_kinetic_'+i),...Array.from({length:4},(_,i)=>'s1m_rocket_'+i)];}
function s1mWarm(){for(const k of s1mKeys())XART.rdy(k);}
stageLoadBegin=function(n,keys){return S1M.base.load.call(this,n,n===1?[...(keys||[]),...s1mKeys()]:keys);};
beginStage=function(n){const r=S1M.base.begin.apply(this,arguments);if(n===1){s1mWarm();S1M.shots=[];S1M.draws={};}return r;};
function s1mLive(e){return run.stage===1&&e&&!e.dead&&e._dyingT==null&&
 /^(?:s1tank(?:heavy|light|apc)(?:_b)?|s1truckmissile|s1boat(?:gun|patrol)|s1corvette|s1landingcraft|s1jet(?:delta|bomber)(?:_b)?)$/.test(e.type||'');}
function s1mIdle(e){const fps=e.type==='s1tanklight'?12:10;return Math.floor((e.t||0)*fps)%8;}
function s1mFire(e){return e._s1mFired==null?-1:Math.floor(((e.t||0)-e._s1mFired)/.065);}
function s1mDraw(bank,f,x,y,w,h,rot=0,tint=null){const a=S1M_ART[bank]?.[f];if(!a||!XART.rdy(a.key))return false;
 const im=tint?xartTint(a.key,tint,tint==='#ffffff'?1:.55):XART.get(a.key);if(!im)return false;
 ctx.save();ctx.translate(x,y);ctx.rotate(rot);ctx.imageSmoothingEnabled=false;
 ctx.drawImage(im,-a.pivot[0]/a.w*w,-a.pivot[1]/a.h*h,w,h);ctx.restore();
 S1M.draws[bank]=(S1M.draws[bank]||0)+1;return true;}
function s1mTick(fn,e,dt){const old=S1M.actor;if(s1mLive(e))S1M.actor=e;
 try{return fn(e,dt);}finally{S1M.actor=old;}}
tankTick=function(e,dt){return s1mTick(S1M.base.tankTick,e,dt);};
jetTick=function(e,dt){return s1mTick(S1M.base.jetTick,e,dt);};
navalTick=function(e,dt){return s1mTick(S1M.base.navalTick,e,dt);};
eShootT=function(x,y,ang,spd,kind,opts){const e=S1M.actor;
 if(s1mLive(e)){
  // The buggy's physical roof tube, not its bumper, owns the rocket origin.
  if(e.type==='s1truckmissile'){x=e.x-11;y=e.y-20;}
  // Each controller already owns its physical authored muzzle. Do not layer
  // the generic automatic muzzle over the new fire reel as well.
  opts={...(opts||{}),noMuzzle:true};
 }
 const shot=S1M.base.shot.call(this,x,y,ang,spd,kind,opts);
 if(s1mLive(e)&&shot&&!shot.dead&&!shot._ai27Held){
  e._s1mFired=e.t||0;
  S1M.shots.push({type:e.type,kind,x,y,t:e.t||0});if(S1M.shots.length>160)S1M.shots.shift();
 }
 return shot;
};
navalFlash=function(e,mz,scale,fam,opts){const owner=e||S1M.actor;
 if(!s1mLive(owner))return S1M.base.flash.apply(this,arguments);
 const f=s1mFire(owner);
 if(f>=0&&f<4&&(owner._modTank===1||owner.type==='s1truckmissile')&&
  XART.rdy(S1M_ART[owner._modTank===1?'turret':'buggy_fire'][0].key))return;
 const rocket=fam===S1_MUZZLE_MILITARY,name=rocket?'s1m_rocket':'s1m_kinetic';
 if(!XART.rdy(name+'_0'))return S1M.base.flash.apply(this,arguments);
 // Existing live hardpoint/follow, angle, size and lifetime stay authoritative.
 return S1M.base.flash.call(this,e,mz,scale,name,{...(opts||{}),n:4,anchor:24/416});
};
drawModularTank=function(e){
 if(!s1mLive(e)||e._modTank!==1||!XART.rdy(S1M_ART.hull[0].key)||!XART.rdy(S1M_ART.turret[3].key))return S1M.base.tankDraw.apply(this,arguments);
 const size=e.w*1.05,raw=s1mFire(e),f=raw>=0&&raw<4?raw:3,angle=(e._modAngle||Math.PI/2)-Math.PI/2,tint=tintColor(e);
 e._drawW=e.w;e._drawH=e.h;
 s1mDraw('hull',s1mIdle(e),e.x,e.y,size,size,0,tint);
 s1mDraw('turret',f,e.x,e.y,size,size,angle,tint);
 return true;
};
function s1mBuggy(e){const raw=s1mFire(e),fire=raw>=0&&raw<4,bank=fire?'buggy_fire':'buggy_idle',f=fire?raw:s1mIdle(e);
 if(!XART.rdy(S1M_ART[bank][f].key))return false;
 const w=55,h=w*328/220;e._drawW=w;e._drawH=h;
 s1mDraw(bank,f,e.x,e.y,w*256/220,h*384/328,(e.spin||0)+(e._navLean||0),tintColor(e));return true;}
function s1mWake(e){const fleet=e.type==='s1boatpatrol'||e.type==='s1boatgun',draw=fleet?Math.max(e.w,e.h)*1.10:e._drawH||e.h,
 w=fleet?(e.type==='s1boatgun'?draw*.55:draw*.92):(e._drawW||e.w)*1.42,h=fleet?draw*1.40:draw*1.45;
 s1mDraw('wake',s1mIdle(e),e.x,e.y+(e._navBob||0),w,h,(e.spin||0)+(e._navLean||0));}
function s1mExhaust(e){if(e._furyMove)return;const v=furyJetVariant(e);if(v<0)return;
 const size=Math.max(e.w,e.h)*1.10,k=size/128,f=s1mIdle(e);
 // Measured tail exhaust sockets in the approved south-facing native plates.
 const sockets=v===0||v===3?[[50,12],[78,12]]:v===1?[[50,12],[78,12]]:[[53,18],[73,18]];
 for(const [x,y] of sockets)s1mDraw('exhaust',f,e.x+(x-64)*k,e.y+(y-64)*k,15*k,38*k);
}
drawEnemy=function(e){
 if(!s1mLive(e))return S1M.base.enemy.apply(this,arguments);
 if(/^s1(?:boat|corvette|landingcraft)/.test(e.type))s1mWake(e);
 if(/^s1jet/.test(e.type))s1mExhaust(e);
 if(e.type==='s1truckmissile'&&s1mBuggy(e))return;
 return S1M.base.enemy.apply(this,arguments);
};
