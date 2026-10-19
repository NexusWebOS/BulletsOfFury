"use strict";
/* Stage 9's authored gunships/prisms were flattened into the same fodder HP
   pool as scouts. Retain their authored weight and native difficulty ratio. */
const LE19={base:{spawn:spawnEnemy},adjusted:0};
// Normalization compares the same party in both difficulties. Reapply the
// ordinary-enemy party factor that otherwise cancels in that ratio.
function le19PartyFactor(){return window.LC19_OFF!==1&&coopActive()?COOP_EHP_MUL:1;}
function le19Pool(e){const spec=e?._s9void&&S9VOID[e._s9void];if(!spec||window.LE19_OFF===1||e._le19HP)return;
 const current=EHP(spec.hp),saved=diffKey;let normal=current;
 try{diffKey='normal';normal=EHP(spec.hp);}finally{diffKey=saved;}
 const hp=Math.max(current,Math.round(spec.hp*current/Math.max(1,normal)*le19PartyFactor()));
 e.hp=e.maxhp=e._maxhp=hp;e._le19HP=true;LE19.adjusted++;
}
spawnEnemy=function(){const first=enemies.length,r=LE19.base.spawn.apply(this,arguments);for(let i=first;i<enemies.length;i++)le19Pool(enemies[i]);return r;};
window.BOF_LATE_HULLS={state:LE19,pool:le19Pool};
