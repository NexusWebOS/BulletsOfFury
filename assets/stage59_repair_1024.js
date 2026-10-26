"use strict";
/* Native health, damage, reward and sound owners remain authoritative. */
const S5924={base:{targets:siegeBomberTargets,space:spaceTargets,shield:drawEnemyShieldLayer,
 drawEnemy:drawEnemy,horizonInit:s9VoidHorizonInit,horizonTick:s9VoidHorizonTick,horizonDraw:s9VoidHorizonDraw,
 load:stageLoadBegin,warp:s9WarpDraw,warpStart:s9WarpStart,warpTick:s9WarpTick,state:setState,impact:spaceImpact,death:unitDeathFX},draws:{},shots:[]};
// A dead core used to remain first in spaceTargets, absorb the collision, then
// refuse its damage. Live weapon targets precede the broad body in space too.
siegeBomberTargets=function(b){return S5924.base.targets.apply(this,arguments)
 .filter(t=>!t.dead&&t.hp>0).sort((a,z)=>(a._retinaId==='bomber-core')-(z._retinaId==='bomber-core'));};
spaceTargets=function(){return S5924.base.space.apply(this,arguments).filter(t=>t&&!t.dead&&!(Number.isFinite(t.hp)&&t.hp<=0));};
function s5924HullExtent(e){const M=bf22Model(e)?.M;if(!M||run.stage!==9)return;
 const span=e._bf22Rendered?.scale!=null?e._bf22Rendered.scale*M.span:bf22Span(e,M)*(e._scale??1);
 if(Number.isFinite(span)&&span>0)e._drawW=e._drawH=span;
}
drawEnemy=function(e){const r=S5924.base.drawEnemy.apply(this,arguments);s5924HullExtent(e);return r;};
unitDeathFX=function(e){s5924HullExtent(e);return S5924.base.death.apply(this,arguments);};
// The old renderer inherited the legacy full-canvas dimensions, then grew them
// another 40%. Limit only Stage9 fodder's shell; energy and break clocks stay.
drawEnemyShieldLayer=function(e,front){
 if(run.stage!==9||!bf22Model(e))return S5924.base.shield.apply(this,arguments);
 const s=e._esh,name=FV21_SHIELDS[s?.family];if(!name){
  const w=e._drawW,h=e._drawH;e._drawW=Math.min(100,e.w*1.10);e._drawH=Math.min(100,e.h*1.10);
  try{return S5924.base.shield.apply(this,arguments);}finally{e._drawW=w;e._drawH=h;}
 }
 if(!front||e.dead||e._dyingT!=null)return;
 const t=s.animT||0,energy=clamp(s.energy/Math.max(1,s.max),0,1),size=Math.min(144,Math.max(e.w,e.h)*1.35);
 let alpha=.22+.16*energy;if(s.phase==='deploy')alpha*=clamp(t/.34,0,1);else if(s.phase==='broken')alpha*=clamp(1-t/.30,0,1);
 fv21Frame(name,efxClock+(e.t||0)*.1,e.x,e.y,size,alpha,false,0,s.hitT||0);
};
// Frequent space-gun contacts need compact sparks, not a field of overlapping
// explosions. This affects decoration only; damage and actual deaths remain.
spaceImpact=function(b,family,lv,size){const r=S5924.base.impact.apply(this,arguments);
 if(run.stage===9&&family!=='shadow'){
  b.w=b.h=Math.min(b.w, family==='volley'?26:20);b.life=Math.min(b.life,.14);
  const nearby=pBullets.some(q=>q!==b&&!q.dead&&q.kind==='spaceImpact'&&!q._quietVisual&&q.t<.12&&Math.hypot(q.x-b.x,q.y-b.y)<52);
  if(nearby)b._quietVisual=true;
 }return r;};
function s5924Rank(){return diffKey==='furious'||diffKey==='insanity'?2:diffKey==='hard'?1:0;}
function s5924Ready(name){return typeof S5924_ART!=='undefined'&&S5924_ART.banks[name]?.frames.every(a=>XART.rdy(a.key));}
function s5924Keys(){return typeof S5924_ART==='undefined'?[]:Object.values(S5924_ART.sheets).map(a=>a.key);}
function s5924Eye(b){return{x:b._s9rift.core.x,y:b._s9rift.core.y};}
function s5924Set(b,mode){const F=b._s9rift,Q=F.s5924,n=s5924Rank();Q.mode=mode;Q.t=0;Q.fired=0;Q.from={x:b.x,y:b.y};Q.warm=[1.18,1.04,.92][n];Q.active=mode==='spin'?1.30:1.35;Q.rest=[1.20,1.05,.90][n];Q.target={x:targetShip(b.x,b.y).x,y:targetShip(b.x,b.y).y};
 const eye=s5924Eye(b),aim=Math.atan2(Q.target.y-eye.y,Q.target.x-eye.x);Q.angles=[];
 if(mode==='spin'){
  const count=[12,14,16][n],gap=aim;
  for(let i=0;i<count;i++){const a=i*TAU/count;if(Math.abs(Math.atan2(Math.sin(a-gap),Math.cos(a-gap)))>.43)Q.angles.push(a);}
 }else if(mode==='sweep')for(const o of [-.35,-.175,0,.175,.35])Q.angles.push(Math.PI/2+o);
 else for(const o of (n===2?[-.22,-.11,0,.11,.22]:[-.16,0,.16]))Q.angles.push(aim+o);
 combatWarningTick(b,'horizon-eye-'+mode,0,Q.warm,true);
}
s9VoidHorizonInit=function(b){const r=S5924.base.horizonInit.apply(this,arguments),F=b._s9rift;
 if(F){b.w=F.core.w=248;b.h=F.core.h=284;b.name='BLACK EVENT HORIZON';F.s5924={mode:'entry',t:0,age:0,cycle:0};}
 return r;};
s9VoidHorizonTick=function(b,dt){const F=b?._s9rift;if(!F)return S5924.base.horizonTick.apply(this,arguments);
 if(b.dead)return true;const w=F.core,Q=F.s5924||(F.s5924={mode:'entry',t:0,age:0,cycle:0});Q.age+=dt;Q.t+=dt;F.t+=dt;b.t=(b.t||0);
 // This controller replaces the old unrelated off-wing/wardens' volley book.
 b._late27=null;w.flash=Math.max(0,w.flash-dt);b.flash=Math.max(0,(b.flash||0)-dt);
 const cx=(camLeftX()+camRightX())/2;
 if(Q.mode==='entry'){
  const u=clamp(Q.t/1.65,0,1);w.x=cx;w.y=lerp(-170,150,u*u*(3-2*u));b.enter=u<1;
  if(u===1){b.x=w.x;b.y=w.y;s5924Set(b,'aimed');}
 }else{
  b.enter=false;const fire=Q.t>=Q.warm&&Q.t<Q.warm+Q.active;
  if(Q.t<Q.warm){combatWarningTick(b,'horizon-eye-'+Q.mode,Q.t,Q.warm);}
  else if(fire){
   const u=(Q.t-Q.warm)/Q.active;
   if(Q.mode==='orbit'){w.x=Q.from.x+Math.sin(u*TAU)*72;w.y=Q.from.y+(1-Math.cos(u*TAU))*22;}
   else if(Q.mode==='sweep'){w.x=clamp(cx+Math.sin(u*Math.PI*2)*100,camLeftX()+125,camRightX()-125);w.y=150+Math.sin(u*Math.PI)*26;}
   const gap=Q.mode==='spin'?.60:.34,n=s5924Rank();
   if(u*Q.active>=Q.fired*gap&&Q.fired<(Q.mode==='spin'?2:3)){
    const eye=s5924Eye(b),kind=Q.mode==='spin'?'s9pair':'s9needle';
    Q.angles.forEach((a,i)=>{const shot=eShootT(eye.x,eye.y,a,2.7+n*.25,kind,{w:Q.mode==='spin'?14:8,h:Q.mode==='spin'?14:22,silent:i>0,noMuzzle:true});
     Object.assign(shot,{_s5924Owner:b,_bf22Theme:'water',_bf22Form:Q.mode==='spin'?'orb':'needle',_bf22Born:efxClock});S5924.shots.push({x:shot.x,y:shot.y,eye:{...eye},mode:Q.mode});if(S5924.shots.length>96)S5924.shots.shift();});
    wm26Emit(b,eye.x,eye.y,Math.PI/2,'laser','#51e7ff',{size:38,life:.16,follow:()=>!b.dead?s5924Eye(b):null});Q.fired++;
   }
  }else{
   const t=clamp((Q.t-Q.warm-Q.active)/Q.rest,0,1),goal={x:cx+Math.sin(Q.age*.65)*85,y:148+Math.sin(Q.age*1.05)*18};
   w.x=lerp(w.x,goal.x,Math.min(1,dt*4));w.y=lerp(w.y,goal.y,Math.min(1,dt*4));
   if(t===1){b.x=w.x;b.y=w.y;s5924Set(b,['aimed','orbit','sweep','spin'][++Q.cycle%4]);}
  }
 }
 w.spin=0;b.x=w.x;b.y=b._drawY=w.y;b.hp=w.hp;return true;
};
function s5924Warning(b){const Q=b._s9rift.s5924;if(!Q||Q.mode==='entry'||Q.t>=Q.warm)return;const p=s5924Eye(b);
 for(const a of Q.angles)combatWarningDraw(b,{x:p.x,y:p.y,ex:p.x+Math.cos(a)*720,ey:p.y+Math.sin(a)*720,width:Q.mode==='spin'?22:26,progress:Q.t/Q.warm,fieldOnly:true});
}
s9VoidHorizonDraw=function(b){const F=b?._s9rift;if(!F)return S5924.base.horizonDraw.apply(this,arguments);
 const Q=F.s5924,w=F.core;s5924Warning(b);
 let bank=Q?.mode==='spin'&&Q.t>=Q.warm&&Q.t<Q.warm+Q.active?'black_spin':Q?.t<Q?.warm?'black_charge':'black_drift';
 const B=typeof S5924_ART!=='undefined'&&S5924_ART.banks[bank],u=bank==='black_spin'?clamp((Q.t-Q.warm)/Q.active,0,.999):bank==='black_charge'?clamp(Q.t/Q.warm,0,.999):(efxClock*.7)%1;
 if(B&&s5924Ready(bank)){const a=B.frames[Math.floor(u*B.frames.length)%B.frames.length],im=XART.get(w.flash>0?a.hit:a.key);ctx.imageSmoothingEnabled=false;ctx.drawImage(im,w.x-192,w.y-192,384,384);S5924.draws[bank]=(S5924.draws[bank]||0)+1;}
 else{const key='ns9x_horizonblk_'+Math.floor(efxClock*10)%7;if(XART.rdy(key)){ctx.imageSmoothingEnabled=false;ctx.drawImage(w.flash>0?xartTint(key,'#ffffff',1):XART.get(key),w.x-w.w/2,w.y-w.h/2,w.w,w.h);}}
 drawSubBossBar(b);return true;};
stageLoadBegin=function(n,keys){if([5,9].includes(n))for(const cue of ['enemyElectricBolt','combatOrb0927','bossWeaponCharge','warpBurst'])Snd.prepare(cue);return S5924.base.load.call(this,n,[...(keys||[]),...([5,9].includes(n)?s5924Keys():[])]);};
function s5924HideWarp(){if(S5924.overlay)S5924.overlay.style.display='none';}
setState=function(next){if(next!==GS.PLAY)s5924HideWarp();return S5924.base.state.apply(this,arguments);};
function s5924FullWarp(im,white){const room=document.getElementById('room');if(!room)return;
 if(!S5924.overlay){const c=document.createElement('canvas');c.id='water-warp-1024';c.setAttribute('aria-hidden','true');c.style.cssText='position:absolute;inset:0;width:100%;height:100%;pointer-events:none;z-index:1000;image-rendering:pixelated;display:none';room.appendChild(c);S5924.overlay=c;}
 const c=S5924.overlay,rect=room.getBoundingClientRect(),dpr=window.devicePixelRatio||1,w=Math.ceil(rect.width*dpr/2)*2,h=Math.ceil(rect.height*dpr/2)*2;
 if(c.width!==w||c.height!==h){c.width=w;c.height=h;}c.style.display='block';const g=c.getContext('2d'),size=Math.max(w,h);g.imageSmoothingEnabled=false;g.globalAlpha=1;g.drawImage(im,(w-size)/2,(h-size)/2,size,size);
 if(white>0){g.globalAlpha=white;g.fillStyle='#ffffff';g.fillRect(0,0,w,h);g.globalAlpha=1;}
}
s9WarpStart=function(){s5924HideWarp();const r=S5924.base.warpStart.apply(this,arguments);s5924Keys().forEach(k=>XART.rdy(k));return r;};
s9WarpTick=function(dt){const W=s9warp;
 if(W&&s5924Ready('warp_motion')&&W.ph==='draw'&&W.t>=S9W_CHARGE+.16&&!W._s5924Done){
  W._s5924Age=(W._s5924Age||0)+dt;if(W._s5924Age>=3)W._s5924Done=true;
  return S5924.base.warpTick.call(this,0);
 }const r=S5924.base.warpTick.apply(this,arguments);if(!s9warp)s5924HideWarp();return r;};
s9WarpDraw=function(){const W=s9warp;if(!W||!s5924Ready('warp_motion')){s5924HideWarp();return S5924.base.warp.apply(this,arguments);}
 // Keep the real ship capture/portal entry, then replace the old rift overlays
 // with one full-field authored water tunnel. The native map handoff stays.
 if(W.ph==='draw'&&W.t<S9W_CHARGE+.16)return S5924.base.warp.apply(this,arguments);
 const B=S5924_ART.banks.warp_motion,age=(W._s5924Age||0)+Math.max(0,W.t-S9W_CHARGE-.16),u=(age*20%(B.frames.length-1))/(B.frames.length-1),a=B.frames[Math.floor(u*(B.frames.length-1))];
 const im=XART.get(a.key);ctx.save();ctx.setTransform(SS,0,0,SS,0,0);const width=cv.width/SS,height=cv.height/SS,size=Math.max(width,height);ctx.imageSmoothingEnabled=false;ctx.drawImage(im,(width-size)/2,(height-size)/2,size,size);
 const white=W.ph==='white'?clamp(W.t/S9W_WHITE,0,1):0;if(white>0){ctx.globalAlpha=white;ctx.fillStyle='#ffffff';ctx.fillRect(0,0,width,height);}ctx.restore();s5924FullWarp(im,white);
};
globalThis.BOF_STAGE59_REPAIR=S5924;
