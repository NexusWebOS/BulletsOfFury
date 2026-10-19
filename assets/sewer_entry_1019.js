"use strict";
/* The 24-second toxic skimmer starts above the playfield. Its crossing route
   must first descend into the fight; side entries retain their native passes. */
const SE19={base:{spawn:spawnEnemy,tick:s7ToxicTick},entries:0};
spawnEnemy=function(){const first=enemies.length,r=SE19.base.spawn.apply(this,arguments);
 if(window.SE19_OFF!==1&&run.stage===7)for(let i=first;i<enemies.length;i++){
  const e=enemies[i];if(e._s7toxic!=='s7skimmer'||e.y>=PLAY.y||e.x<0||e.x>worldWidth())continue;
  e._dir=e._side||((e.x>=worldWidth()/2)?-1:1);
  e._se19Entry={target:PLAY.y+110};SE19.entries++;
 }return r;
};
s7ToxicTick=function(e,dt){const entry=e?._se19Entry;
 if(!entry||window.SE19_OFF===1)return SE19.base.tick.apply(this,arguments);
 if(e.dead||e._dyingT!=null)return;
 if((e._stagger||0)>0){e._stagger=Math.max(0,e._stagger-dt);return;}
 e._s7t=(e._s7t||0)+dt;e.y=Math.min(entry.target,e.y+180*dt);
 e.x+=e._dir*28*dt;e.spin=-e._dir*.18;
 if(e.y>=entry.target){e._se19Entry=null;e._fcd=.2;}
};
window.BOF_SEWER_ENTRY={state:SE19};
