"use strict";
/* Current Breaker keeps his frontal cast/reveal identity. Actual authored
   overhead flight views and perspective tilt are a separate animation bank. */
const CF111={visual:s911Visual,guns:s911Guns,finish:s911Finish,draw:s911Draw};
function cf111Plate(e){if(e?._s911?.model!=='current'||!e._s911.human)return null;const A=e._s911,M=s911M(e),k=M.span/256;let B,G,f,angle=Math.PI/2,points,view;
 if(A.phase==='tell'&&A.attack==='superman'&&A.t>A.warm-.20){B=M.flightLaunch;G=M.flightLaunchGlow;f=Math.min(3,Math.floor((A.t-(A.warm-.20))/.20*4));points=M.launchPalms[f];view='tilt';}
 else if(A.phase==='flight'&&A.t<.22){B=M.flightLaunch;G=M.flightLaunchGlow;f=Math.min(7,4+Math.floor(A.t/.22*4));points=M.launchPalms[f];view='tilt';}
 else if(A.phase==='flight'){B=M.flight;G=M.flightGlow;f=0;const settle=clamp((A.t-1.55)/.25,0,1);angle=A.head+s1aAngle(Math.PI/2-A.head)*settle;points=M.flightPalms[v31Dir(angle,8)];view='overhead';}
 else if(A.phase==='recover'&&A.flightRecoveryAt!=null&&efxClock-A.flightRecoveryAt<.32){B=M.flightReturn;G=M.flightReturnGlow;f=Math.min(7,Math.floor((efxClock-A.flightRecoveryAt)/.32*8));points=M.returnPalms[f];view='tilt';}
 else return null;
 return{B,f,p:e,angle,scale:k,glow:G,shield:null,points,view,dir:view==='overhead'?v31Dir(angle,8):0};
}
s911Visual=function(e){const p=cf111Plate(e);return p?[p]:CF111.visual.apply(this,arguments);};
s911Guns=function(e){const p=cf111Plate(e);return p?p.points.map((v,i)=>({...s911Point(e,v,Math.PI/2),angle:e._s911.head,index:i})):CF111.guns.apply(this,arguments);};
s911Finish=function(e){if(e?._s911?.model==='current'&&e._s911.phase==='flight')e._s911.flightRecoveryAt=efxClock;return CF111.finish.apply(this,arguments);};
s911Draw=function(e){const r=CF111.draw.apply(this,arguments);if(e?._s911?.model==='current'){const p=cf111Plate(e);Object.assign(e._s911Rendered,{view:p?.view||'front',dir:p?.dir||0,flightBank:p?.B.key||null,flightFrame:p?.f??null});}return r;};
