"use strict";
/* Final interception invariant: cosmetic elemental art cannot make an ordinary
   gun round or sonic pressure wave into shootable ordnance. Physical missiles
   and deliberately authored boss energy-ball mechanics keep their native rules. */
const ORD1106_INTERCEPT=enemyOrdnanceCanIntercept;
enemyOrdnanceCanIntercept=function(q){
  return !enemyProjectileIsBulletOrSonic(q)&&ORD1106_INTERCEPT.apply(this,arguments);
};
