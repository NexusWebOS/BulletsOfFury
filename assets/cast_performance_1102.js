'use strict';
/* Expanded cutscene library; gameplay input/combat/death owners stay native. */
for(const [pilot,bank]of Object.entries(CP112_ART.pilots))Object.assign(C112.art.pilots[pilot],bank);
Object.assign(C112.art.chronos,CP112_ART.chronos);
const CP112={metadata:CP112_ART.metadata,shipScenes:CP112_ART.shipScenes,draw:C112.draw};
C112.draw=function(pilot,pose,x,ground,height=512){
  const key=C112.key(pilot,pose),m=CP112.metadata[key];
  if(!m)return CP112.draw.apply(this,arguments);
  if(!XART.rdy(key))return false;
  const scale=height/m.cell[1];
  ctx.drawImage(XART.get(key),x-m.pivot[0]*scale,ground-m.pivot[1]*scale,m.cell[0]*scale,m.cell[1]*scale);
  return true;
};
C112.stride=function(pilot,kind,time,x,ground,height=512){
  const gait=kind==='run'?'run':'walk',frame=Math.floor(Math.max(0,time)*(gait==='run'?10:6))%4;
  return C112.draw(pilot,gait+'_'+frame,x,ground,height);
};
window.BOF_CAST_PERFORMANCE=CP112;
