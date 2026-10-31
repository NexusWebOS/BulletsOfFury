"use strict";
// Shared pixel-master baseline; existing typewriter, wrapping and audio remain authoritative.
for(const[n,a]of Object.entries(RD64_ART.banks).sort((a,b)=>a[1].height-b[1].height)){PM27_ART.banks[n]=a;XART._src[a.key]=a.path;}
PM27.ready=false;pm27Warm();
const RD64_CONTENTS=ui20PanelContents;
ui20PanelContents=function(){const old=PM27.role;PM27.role='command_dialogue';try{return RD64_CONTENTS.apply(this,arguments);}finally{PM27.role=old;}};
