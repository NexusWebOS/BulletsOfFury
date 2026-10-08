'use strict';
/* A yellow ground reticle means its target has actually stopped moving.
   Leave a reaction plus travel budget for the slowest unboosted pilot. */
const MANEUVER_SAFETY_1007={
 profiles:Object.freeze({easy:{reaction:.45,pad:18},normal:{reaction:.38,pad:16},hard:{reaction:.32,pad:14},furious:{reaction:.28,pad:12},insanity:{reaction:.24,pad:10}}),
 slowSpeed:2.6*60*(1+Math.min(...PILOTS.map(p=>p.spd||0))),
 originalSpawn:groundTargetingSpawn,originalPhase:groundTargetingPhase
};
function maneuverWarningBudget(q){
 const P=MANEUVER_SAFETY_1007.profiles[diffKey]||MANEUVER_SAFETY_1007.profiles.normal;
 const early=run.stage<=3?(diffKey==='easy'?.05:diffKey==='normal'?.025:0):0;
 const required=P.reaction+(q.radius+P.pad)/MANEUVER_SAFETY_1007.slowSpeed+early+2/30;
 if(q.track){
  // The strike owns this clock. Linked, fixed-position boss beams keep their
  // existing authored duration; their separate collision owner is untouched.
  q.warn=Math.max(q.warn,Math.ceil((required-.08+.18)*100)/100);
  q.trackFor=Math.min(q.trackFor,.5,Math.max(0,(q.warn+.08-required)/q.warn));
 }
 q._safetyCommit=q.track?q.warn*q.trackFor:q.warn*.5;
 q._safetyBudget={reaction:P.reaction,pad:P.pad,required,speed:MANEUVER_SAFETY_1007.slowSpeed};
 return q;
}
groundTargetingSpawn=function(){return maneuverWarningBudget(MANEUVER_SAFETY_1007.originalSpawn.apply(this,arguments));};
groundTargetingPhase=function(q){
 if(q._safetyCommit==null||q._fztEye)return MANEUVER_SAFETY_1007.originalPhase(q);
 const lock=q._safetyCommit;
 return q.t<lock?clamp(q.t/Math.max(.001,lock),0,1)*.5:
  .5+.5*clamp((q.t-lock)/Math.max(.001,q.warn-lock),0,1);
};

/* Legacy movement/projectiles are expressed per 60 Hz tick. Keep them on that
   clock even when the display renders at 30, 120 or 144 Hz. Never catch up a
   background tab with a burst of unseen attacks. Rendering retains its clock. */
const BOF_COMBAT_CLOCK={step:1/60,debt:0,steps:0,total:0};
function combatClockReset(){BOF_COMBAT_CLOCK.debt=0;BOF_COMBAT_CLOCK.steps=0;}
function combatFrame(dt){
 const C=BOF_COMBAT_CLOCK;C.steps=0;
 if(state!==GS.PLAY||!Number.isFinite(dt)||dt<0||dt>.25){combatClockReset();return 0;}
 C.debt+=Math.min(dt,.05);
 while(C.debt+1e-9>=C.step&&C.steps<3&&state===GS.PLAY){
  if(C.steps)Input.clearTaps();
  C.debt=Math.max(0,C.debt-C.step);C.steps++;C.total++;
  updatePlay(C.step);
 }
 if(state!==GS.PLAY)C.debt=0;
 return C.steps;
}
const MANEUVER_SET_STATE=setState;
setState=function(next){if(next!==state)combatClockReset();return MANEUVER_SET_STATE.apply(this,arguments);};

/* Sovereign's ram must warn for the same footprint that can hit the pilot.
   Its shield is wider than the hull; weapon loss can leave that shield intact. */
function maneuverRamRadius(b){
 const S=b._s4war,H=S?.shield;
 let radius=b.w*(H&&(H.active||H.rearming) ? .67 : .5);
 if(H?.active)for(const n of H.nodes||[])if(!n.dead)radius=Math.max(radius,Math.abs(n.x-b.x)+36);
 for(const t of S?.coreTurrets||[])if(!t.dead&&t.materialize>=1)radius=Math.max(radius,Math.abs(t.x-b.x)+Math.max(36,(t.w||0)/2));
 return radius;
}
function maneuverRamWarm(b,base,E){
 const P=MANEUVER_SAFETY_1007.profiles[diffKey]||MANEUVER_SAFETY_1007.profiles.normal;
 // Near an edge, escaping inward crosses the assembly's swept horizontal span.
 const sweep=E?Math.abs(E.tx-E.ox):0;
 return Math.max(base,P.reaction+(maneuverRamRadius(b)+P.pad+sweep)/(MANEUVER_SAFETY_1007.slowSpeed*1.35)+.12);
}
function maneuverRamWidth(b){return 2*maneuverRamRadius(b)+6;}
