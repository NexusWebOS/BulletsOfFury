'use strict';
// Complete authored ship-to-robot plates, before the dialogue hold begins.
const C39={blue:ha21Blue,tick:hammerBossTick};
ha21Blue=function(b){if(c25Own(b)&&!b.dead){const h=b._hammer;
 if(h.state==='flyby')return ha21Pose('blue_from_ship',0,1.75,Math.PI);
 if(h.state==='return')return ha21Pose('blue_from_ship',0,1.75,0);
 if(h.state==='unfold'&&!fb2IntroActive())return ha21Pose('blue_from_ship',clamp(h.t/1.85,0,1),1.75,0);
 }return C39.blue.apply(this,arguments);};
hammerBossTick=function(b,dt){const prior=b?._hammer?.state,r=C39.tick.apply(this,arguments);
 // The whole ship must clear the upper edge before reversing its heading.
 if(c25Own(b)&&prior==='flyby'&&b._hammer.state==='return'){b.y=viewTopY()-360;b._drawY=b.y;}
 return r;};
window.BOF_CHRONOS_ARRIVAL=C39;
