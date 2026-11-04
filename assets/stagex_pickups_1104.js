"use strict";
/* Stage X is routed through Stage6. Only its explicit route flag selects these
   authored pickups; regular Stage6 and every reward/HP owner stay native. */
const SXP114={base:{crate:drawCrate,capsule:drawCapsule,powerups:drawPowerups,begin:beginStage},
 banks:{power:{key:'stagex114_power_turn64',file:'power_turn_64.png',cell:64,idleFrames:16,hitStart:16,hitFrames:16,frameSeconds:.08},capsule:{key:'stagex114_speed64',file:'speed_64.png',cell:64},speed:{key:'stagex114_speed36',file:'speed_36.png',cell:36}},idleFrames:8,hitFrame:8,frameSeconds:.10};
for(const b of Object.values(SXP114.banks))XART._src[b.key]='assets/game/levels/stage_06/pickups/stagex_1104/'+b.file;
function sxp114Active(){return typeof stageXArenaActive==='function'&&stageXArenaActive();}
function sxp114Warm(){for(const b of Object.values(SXP114.banks))XART.rdy(b.key);}
function sxp114Draw(kind,x,y,t,flash){const b=SXP114.banks[kind];if(!XART.rdy(b.key))return false;
 const n=b.idleFrames||SXP114.idleFrames,pose=Math.floor(Math.max(0,t||0)/(b.frameSeconds||SXP114.frameSeconds))%n;
 const f=flash>0?(b.hitFrames?b.hitStart+pose:SXP114.hitFrame):pose,c=b.cell;
 ctx.save();ctx.imageSmoothingEnabled=false;ctx.globalAlpha=1;ctx.globalCompositeOperation='source-over';ctx.shadowBlur=0;
 ctx.drawImage(XART.get(b.key),f*c,0,c,c,Math.round(x-c/2),Math.round(y-c/2),c,c);ctx.restore();return true;
}
drawCrate=function(x,y,t,flash){if(sxp114Active()&&sxp114Draw('power',x,y,t,flash))return;return SXP114.base.crate.apply(this,arguments);};
drawCapsule=function(x,y,t,flash){if(sxp114Active()&&sxp114Draw('capsule',x,y,t,flash))return;return SXP114.base.capsule.apply(this,arguments);};
drawPowerups=function(){if(!sxp114Active()||!XART.rdy(SXP114.banks.speed.key))return SXP114.base.powerups.apply(this,arguments);
 const all=powerups;powerups=all.filter(p=>p.kind!=='speed');try{SXP114.base.powerups.apply(this,arguments);}finally{powerups=all;}
 for(const p of all)if(!p.dead&&p.kind==='speed')sxp114Draw('speed',p.x,p.y+Math.sin((p.t||0)*4)*2,p.t,p.flash||0);
};
beginStage=function(){const out=SXP114.base.begin.apply(this,arguments);if(run.stage===6)sxp114Warm();return out;};
globalThis.BOF_STAGE_X_PICKUPS_1104={state:SXP114,active:sxp114Active,warm:sxp114Warm};
