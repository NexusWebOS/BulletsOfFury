// Restore the actual spawn/entry pose after the isolated fixture prepares loadout.
const BAL7_ENTRY_SETUP=BAL7.setup;
BAL7.setup=function(c){
 let entry=null;const base=spawnSubBoss__inner;
 spawnSubBoss__inner=function(){const r=base.apply(this,arguments);const b=subBoss;entry={x:b.x,y:b.y,enter:b.enter,_noHit:b._noHit,_be:b._be,_drawY:b._drawY};return r;};
 let result;try{result=BAL7_ENTRY_SETUP(c);}finally{spawnSubBoss__inner=base;}
 if(c.naturalEntry&&entry){Object.assign(B,entry);result.nativeEntry={x:entry.x,y:entry.y,enter:entry.enter,noHit:entry._noHit};}
 if(c.ownedWeapon){
  if(c.weapon===8&&c.pilot!=='yuri')throw new Error('Lightning Orb is Yuri-only');
  run._earnedUnlocks=Object.assign({},run._earnedUnlocks,{mist:c.weapon===6,chaingun:c.weapon===7,lightningOrb:c.weapon===8});
  laserMistUnlocked=c.weapon===6;chaingunUnlocked=c.weapon===7;yuriLightningOrbUnlocked=c.weapon===8;
 }
 if(c.p2Out){player2.out=true;player2.dead=true;run2.lives=0;}
 return result;
};
