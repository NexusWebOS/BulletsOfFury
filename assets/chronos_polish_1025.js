'use strict';
// Chronos presentation tuning. Native damage, pickups and scrolling retain ownership.
const C37={init:hammerBossInit,hit:markHit,damage:hammerBossDamage,tick:hammerBossTick,rocks:l5RocksUpdate,container:spawnContainer,queue:[],next:0,owner:null,deferred:0};
hammerBossInit=function(b){const r=C37.init.apply(this,arguments);if(c25Own(b)){const h=b._hammer;h.chainHP=h.chainMax=Math.ceil(h.chainMax*3);}return r;};
markHit=function(t,f){if(!c25Own(t))return C37.hit.apply(this,arguments);
 const now=GP4.clock;if(now<(t._gp4FlashNext||0))return t;t._gp4FlashNext=now+.42;
 return GP4_BASE.hit(t,.065);
};
hammerBossDamage=function(b,dmg){if(!c25Own(b))return C37.damage.apply(this,arguments);
 const h=b._hammer,A=fr27Armor(b),old=A?.flash||0,gun=h.ch23GunFlash||0,r=C37.damage.apply(this,arguments);
 // Accept short native flashes with a palette interval; never alter damage or white art.
 if(A&&A.flash>old){if(gp4FlashRequest(A,'c37Armor',.065))A.flash=.065;else A.flash=old;}
 if(h.ch23GunFlash>gun)h.ch23GunFlash=.065;
 return r;
};
function c37Quiet(){if(!c25Own(boss)||boss.dead)return false;const h=boss._hammer,R=h.c30;
 return !!(h._hf22Charge||h.state==='fr_activation'||h.state==='storm_raise'||h.recovery?.status==='charging'||R&&['retreat','gather','thrust','beam','volley_move','volley_warn'].includes(R.phase));
}
l5RocksUpdate=function(dt){if(c37Quiet())l5RockT=Math.max(l5RockT,dt+.05);return C37.rocks.apply(this,arguments);};
spawnContainer=function(type){if(c37Quiet()){if(C37.owner!==boss){C37.owner=boss;C37.queue=[];}C37.queue.push(type);C37.deferred++;return;}return C37.container.apply(this,arguments);};
const c37Armory=spaceArmorySupplyTick,c37Missiles=bossMissileSupplyTick,c37Bonus=missileSupplyBonusTick;
spaceArmorySupplyTick=function(dt){if(!c37Quiet())return c37Armory.apply(this,arguments);};
bossMissileSupplyTick=function(dt){if(!c37Quiet())return c37Missiles.apply(this,arguments);};
missileSupplyBonusTick=function(dt){if(!c37Quiet())return c37Bonus.apply(this,arguments);};
hammerBossTick=function(b,dt){const r=C37.tick.apply(this,arguments);if(c25Own(b)&&b===boss){
 if(C37.owner&&C37.owner!==b){C37.queue=[];C37.owner=null;}
 if(!b.dead&&!c37Quiet()&&C37.queue.length&&GP4.clock>=C37.next){C37.container(C37.queue.shift());C37.next=GP4.clock+2;}
 }return r;};
window.BOF_CHRONOS_POLISH=C37;
