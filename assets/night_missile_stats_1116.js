"use strict";
/* Credit native missile damage to boss/miniboss results without touching HP,
   shield gates, damage routing or rewards. Splash on one encounter counts once
   per projectile; an inner native credit is never counted again. */
const NMS16={base:{boss:hitBoss,mini:hitSubBoss,retina:retinaMissileDamage},shots:new WeakMap(),credited:0};
function nms16Hit(base,owner,self,args,health=owner,shot=_dmgBullet){
 const missile=!!(shot&&typeof shot==='object'&&!shot.ally&&!shot._wingKey&&['gmiss','missile','nukem','retinaMissile'].includes(shot.kind));
 if(!missile||!owner||typeof owner!=='object'||typeof stageStats==='undefined')return base.apply(self,args);
 const stats=stageStats,hp=health?.hp,dealt=stats.dmgDealt||0,hits=stats.mslHits||0;
 const result=base.apply(self,args);
 if(stageStats===stats&&((Number.isFinite(hp)&&health?.hp<hp)||(stats.dmgDealt||0)>dealt)){
  let seen=NMS16.shots.get(shot);if(!seen){seen=new WeakSet();NMS16.shots.set(shot,seen);}
  if(!seen.has(owner)){seen.add(owner);if((stats.mslHits||0)===hits){stats.mslHits=hits+1;NMS16.credited++;}}
 }
 return result;
}
hitBoss=function(){return nms16Hit(NMS16.base.boss,boss,this,arguments);};
hitSubBoss=function(){return nms16Hit(NMS16.base.mini,subBoss,this,arguments);};
retinaMissileDamage=function(t,dmg,shot){
 const owner=t?._retinaOwner||t?._xenoOwner||t?._spaceBossOwner||t?._spaceSubOwner||t;
 return nms16Hit(NMS16.base.retina,owner,this,arguments,t,shot);
};
