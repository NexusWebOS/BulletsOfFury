'use strict';
/* EH91: exact level-4 white cannon pixels and native per-pose optic masks.
   All turns, charge materials and muzzle pulses are authored fixed cells. */
const EH91={revision:1,base:{load:stageLoadBegin}};
for(const[name,a]of Object.entries(EH91_ART)){XART._src[a.key]=a.path;ER28_ART['eh57_'+name]=a;}
ER28_ART.eh57_eye_white=EH91_ART.eye_glow;ER28_ART.eh57_beam_water=EH91_ART.beam;
stageLoadBegin=function(n,keys){return EH91.base.load.call(this,n,n===9?[...(keys||[]),...Object.values(EH91_ART).map(a=>a.key)]:keys);};
globalThis.BOF_HORIZON_WHITE_OPTICS=EH91;
