"use strict";
/* Predict a near collision, not merely proximity. Existing authored impact
   asterisks mark only the closest approaching rounds; hit boxes stay unchanged. */
const PW5={threats:[],draws:0,aceBursts:0};
const PW5_BASE={update:updatePlay,world:drawWorld,guns:whvAceGuns,ace:whvAceTick,drawAce:whvDrawAce,missiles:whvAceFireMissiles,begin:beginStage};
beginStage=function(){PW5.threats=[];return PW5_BASE.begin.apply(this,arguments);};
function pw5Warm(){for(const c of ['yellow','red'])XART.rdy('bmfx_alert_'+c+'_impact_imminent');cf1004Warm();l23FovWarm();}
function pw5Impact(p,ship,scale=60){
 if(p.dead||ship.dead||ship.out||p.kind==='helper'||p._hammerLaser||p._frostNoseLaser||p._ovSonicWave||![p.x,p.y,p.vx,p.vy].every(Number.isFinite))return null;
 // Relative approach avoids marking rounds that the pilot already outruns.
 const dx=ship.x-p.x,dy=ship.y-p.y,vx=p.vx*scale-(ship._vx||0)*60,vy=p.vy*scale-(ship._vy||0)*60,v2=vx*vx+vy*vy;
 if(v2<25)return null;const t=(dx*vx+dy*vy)/v2;if(t<=.04||t>.72)return null;
 const miss=Math.hypot(dx-vx*t,dy-vy*t),radius=Math.max(14,Math.min(26,(p.r||Math.max(p.w||7,p.h||7)*.15)+10));
 return miss<=radius?{p,t,miss,seat:ship.seat||1}:null;
}
function pw5Collect(){PW5.threats=[];if(state!==GS.PLAY)return;pw5Warm();
 const B=boss,W=B?._whv,G=B?._rebels?.gang1004,rounds=eBullets.filter(p=>!p.dead).map(p=>[p,60]);
 for(const p of W?.shots||[])rounds.push([p,60]);for(const p of G?.ord||[])if(p.kind!=='helper')rounds.push([p,1]);
 for(const seat of seatList())withSeat(seat,()=>{const found=rounds.map(([p,s])=>pw5Impact(p,player,s)).filter(Boolean).sort((a,b)=>a.t-b.t);
  for(const q of found.slice(0,2))if(!PW5.threats.some(v=>v.p===q.p))PW5.threats.push({...q,seat});});
}
updatePlay=function(dt){const r=PW5_BASE.update.apply(this,arguments);pw5Collect();return r;};
function pw5Draw(){
 for(const q of PW5.threats){const p=q.p;if(p.dead)continue;const urgent=q.t<.30,col=urgent?'red':'yellow',key='bmfx_alert_'+col+'_impact_imminent';
  if(XART.rdy(key)){const im=XART.get(key),size=urgent?19:15;
   ctx.save();ctx.imageSmoothingEnabled=false;ctx.globalAlpha=.72+.28*(.5+.5*Math.sin(efxClock*(urgent?20:12)));
   ctx.drawImage(im,p.x-size/2,p.y-size/2,size,size);ctx.restore();PW5.draws++;}
 }
}
drawWorld=function(dt){const r=PW5_BASE.world.apply(this,arguments);if(state===GS.PLAY&&PW5.threats.length){
 ctx.save();const z=viewZoom();if(z!==1){ctx.scale(z,z);ctx.translate(0,VH*(1-z)/z);}if(worldWidth()>viewW())ctx.translate(-camX,0);
 pw5Draw();ctx.restore();}return r;};
function pw5Ace(b){return run.stage===6&&b?._whv?.ace&&!b._gp4Host&&!b.dead;}
whvAceGuns=function(b,A,spread){if(!pw5Ace(b)||A._pw5Release)return PW5_BASE.guns.apply(this,arguments);
 if(A._pw5Gun||A._pw5Recover>0)return;
 const tell=diffKey==='easy'?1.15:.9;
 A._pw5Gun={t:0,tell,next:tell,n:0,spread:spread||0,tx:player.x,ty:VH+40};A.burst=0;A.gunCd=Math.max(A.gunCd,tell+1.8);
 combatWarningTick(b,'pw5-rain',0,tell);PW5.aceBursts++;
};
whvAceFireMissiles=function(b,n){const A=b?._whv?.ace;if(pw5Ace(b)&&A._pw5Gun){A._pw5Missiles=n;return;}
 return PW5_BASE.missiles.call(this,b,pw5Ace(b)?Math.min(n,diffKey==='furious'||diffKey==='insanity'?4:2):n);};
whvAceTick=function(b,dt){const A=b?._whv?.ace;if(!pw5Ace(b))return PW5_BASE.ace.apply(this,arguments);
 pw5Warm();A._pw5Recover=Math.max(0,(A._pw5Recover||0)-dt);
 const P=A._pw5Gun;if(P){A.burst=0;A.gunCd=Math.max(A.gunCd,.4);if(A.orb)A.orb.cd=Math.max(A.orb.cd,.35);}
 const r=PW5_BASE.ace.apply(this,arguments);if(!P)return r;
 if(A.dash||A.desp&&A.desp.st!=='done'||A.roll||A.somer){A._pw5Gun=null;A._pw5Recover=.6;return r;}
 P.t+=dt;combatWarningTick(b,'pw5-rain',Math.min(P.t,P.tell),P.tell);
 if(P.t>=P.next&&P.n<4){P.next+=.17;P.n++;
  for(const side of [-1,1]){const x=A.x+side*16,y=A.y+30,a=Math.atan2(P.ty-y,P.tx+side*(P.spread?90:24)-x);
   eShootT(x,y,a,diffKey==='easy'?3.8:diffKey==='furious'||diffKey==='insanity'?5.0:4.5,'s6tracer',{owner:b,silent:side>0,w:7,h:19});}
 }
 if(P.t>=P.tell+.82){A._pw5Gun=null;A._pw5Recover=.8;A.gunCd=Math.max(A.gunCd,.8);
  if(A.orb)A.orb.cd=Math.max(A.orb.cd,.75);
  if(A._pw5Missiles){const count=A._pw5Missiles;A._pw5Missiles=0;whvAceFireMissiles(b,count);}}
 return r;
};
whvDrawAce=function(b){const r=PW5_BASE.drawAce.apply(this,arguments),A=b?._whv?.ace,P=A?._pw5Gun;
 if(P&&P.t<P.tell)for(const side of [-1,1])combatWarningDraw(b,{x:A.x+side*16,y:A.y+30,ex:P.tx+side*(P.spread?90:24),ey:P.ty,width:24,progress:P.t/P.tell,fieldOnly:true});
 return r;};
