"use strict";
/* Restoration is a deliberate multi-missile counter, with an honest window.
   Short real hit flashes remain native; charging alone does not wash the plate. */
const HC17={base:{damage:hammerBossDamage,recovery:hammerRecoveryTick,restore:fr27Restore,start:hammerStormStart,pose:hammerChromiumPoseDraw},hits:0};
function hc17Counter(b){const R=b?._hammer?.recovery;if(!R||R.status!=='charging')return null;
 if(!R._hc17){const rank=target17Rank();R._hc17={required:rank<1?2:rank===1?3:rank===2?4:5,hits:0,seen:new WeakSet()};R.duration=Math.max(R.duration,7+rank*.5);}
 return R._hc17;
}
hammerStormStart=function(b){const r=HC17.base.start.apply(this,arguments);hc17Counter(b);return r;};
fr27Restore=function(b){const r=HC17.base.restore.apply(this,arguments);const R=b._hammer.recovery;delete R._hc17;hc17Counter(b);return r;};
hammerRecoveryTick=function(b,dt){hc17Counter(b);return HC17.base.recovery.apply(this,arguments);};
hammerBossDamage=function(b,dmg){const h=b?._hammer,C=hc17Counter(b),q=_dmgBullet;
 if(!C)return HC17.base.damage.apply(this,arguments);
 b._hammerModuleHit=null;
 if(!(dmg>0))return 0;
 // Body and raised-hammer impacts both count: players can see the counter,
 // and a locked missile no longer has to find an invisible routing column.
 if(hammerMissile(q)&&q.kind!=='spaceVolley'&&!q._autoMissile&&!C.seen.has(q)){
  C.seen.add(q);C.hits++;HC17.hits++;markHit(b);b.flash=Math.max(b.flash||0,.14);
  const p=hammerHeadPoint(b);weaponHitSfx('normal');Audio.SFX.impactMetal?.();
  floatText(p.x,p.y-38,Math.min(C.hits,C.required)+' / '+C.required,'#9fffea');
  h.recovery.coreHP=Math.max(1,h.recovery.coreMax*(1-C.hits/C.required));
  if(C.hits>=C.required)hammerRecoveryBreak(b);
 }else{markHit(b);b.flash=Math.max(b.flash||0,.08);weaponHitSfx('normal');}
 return 0;
};
hammerChromiumPoseDraw=function(b){const h=b?._hammer,C=hc17Counter(b);if(!C)return HC17.base.pose.apply(this,arguments);
 const empowered=h.empowered,level=h.empowerLevel;
 h.empowered=C.hits>0;h.empowerLevel=C.hits/C.required;
 try{return HC17.base.pose.apply(this,arguments);}finally{h.empowered=empowered;h.empowerLevel=level;}
};
window.BOF_HAMMER_COUNTER={state:HC17,counter:hc17Counter};
