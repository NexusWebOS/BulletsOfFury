"use strict";
/* Current Breaker's reveal needs real regular-wave time before native mini/boss
   entry. Isolated actor behavior, encounter pools and portal owners are unchanged. */
const S9S111={plan:buildStagePlan,spawn:spawnEnemy,suppressLate:0};
spawnEnemy=function(type){if(run.stage===9&&type==='cbreak'&&S9S111.suppressLate)return null;return S9S111.spawn.apply(this,arguments);};
buildStagePlan=function(stage){const plan=S9S111.plan.apply(this,arguments);if(stage!==9||run._gp4StageX)return plan;
 const out=plan.map(w=>{if(Math.abs(w.t-38.85)>.001)return w;return{...w,fn:()=>{S9S111.suppressLate++;try{return w.fn();}finally{S9S111.suppressLate--;}}};});
 out.push({t:12.05,fn:()=>spawnEnemy('cbreak',(camLeftX()+camRightX())*.5,-124,{_stagger:.25})});return out.sort((a,b)=>a.t-b.t);
};
