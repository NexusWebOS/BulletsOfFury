"use strict";
/* A standalone Stage6 encounter preview owns its warning, not the regular
   carrier prologue/pursuit selector. Campaign and Arcade launches are unchanged. */
const ENTRY16={base:debugJump,events:[]};
debugJump=function(entry){const out=ENTRY16.base.apply(this,arguments);
 if(entry?.stage===6){
  BOFCinematicDirector.cancel();story=null;s6Opening=null;fb2Talk=fb2Intro=null;if(typeof AP10_X!=='undefined')AP10_X.intro=null;
  s6WingInit();s6Wing.route='left';s6Wing.all=true;s6Wing.beats=3;
  s6Wing.fakeDone=true;s6Wing.supplyIndex=3;s6Wing.line=null;H3.release=false;
  ENTRY16.events.push({stage:6,role:entry.role,kind:entry.kind});
 }
 return out;
};
