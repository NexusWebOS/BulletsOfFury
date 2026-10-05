"use strict";
/* Original warning/Retina routing and preload now live in stage8_1003.js so
   every Stage 7/8 enemy uses them without depending on this finale overlay. */
const OW1003_BASE={draw:r30DrawBoss};
r30DrawBoss=function(b){
 const r=OW1003_BASE.draw.apply(this,arguments),S=b?._r30;
 if(!S?.finale1003b||S.mode!=='fight'||!S.attack)return r;
 const P=S.attack,K=P.k1003;let progress=null;
 if(K&&['slashTell','jumpTell','followTell'].includes(K.phase))progress=K.age/s81003KnightDur(K.phase);
 else if(!K&&P.t<P.tell)progress=P.t/P.tell;
 if(progress!=null){const Q=r30Pose(b);
  // One original green/yellow/red sign above the boss, even for multiple lanes.
  combatWarningDraw(b,{x:Q.x,y:Q.y,ex:Q.x,ey:Q.y+1,progress:clamp(progress,0,1),
   alertOnly:true,alertX:Q.x,alertY:Math.max(S.shield>0?82:L23_WARN_MINY,Q.y-b.h*.5-54)});
 }
 return r;
};
