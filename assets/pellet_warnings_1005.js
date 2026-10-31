"use strict";
/* Bullet-attached collision asterisks retired globally at Mike's request.
   Keep the PW5 API for downstream combat wrappers and retain Nightwing's gun logic. */
const PW5={threats:[],draws:0,aceBursts:0};
const PW5_BASE={update:updatePlay,world:drawWorld,guns:whvAceGuns,ace:whvAceTick,drawAce:whvDrawAce,missiles:whvAceFireMissiles,begin:beginStage};
beginStage=function(){PW5.threats=[];return PW5_BASE.begin.apply(this,arguments);};
function pw5Warm(){cf1004Warm();l23FovWarm();}
function pw5Impact(){return null;}
function pw5Collect(){PW5.threats.length=0;}
updatePlay=function(dt){const r=PW5_BASE.update.apply(this,arguments);pw5Collect();return r;};
function pw5Draw(){}
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
