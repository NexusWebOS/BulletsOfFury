'use strict';
/* Source/export owner: _BUILD_SOURCE/build_cast_cinematics_1102.py.
   Cutscene poses are opt-in. Only Chronos's existing avatar aliases change. */
const C112={art:C112_ART,baseTouch:XART._touch,baseLoad:stageLoadBegin,
  poses:['neutral','speaking','salute','walk_left','look_back','back']};
C112.key=function(pilot,pose='neutral'){
  const bank=C112.art.pilots[String(pilot).toLowerCase()];
  return bank&&(bank[pose]||bank.neutral)||null;
};
C112.draw=function(pilot,pose,x,ground,height=512){
  const key=C112.key(pilot,pose);
  if(!key||!XART.rdy(key))return false;
  const scale=height/1024;
  ctx.drawImage(XART.get(key),x-256*scale,ground-976*scale,512*scale,1024*scale);
  return true;
};
XART._touch=function(key){
  if(['fb2_hammer_avatar','fb1002_hammer_portrait','h3_hammer_portrait','cin30_cronos'].includes(key))
    return C112.baseTouch.call(this,C112.art.chronos.neutral);
  return C112.baseTouch.apply(this,arguments);
};
stageLoadBegin=function(stage,keys){
  return C112.baseLoad.call(this,stage,[...(keys||[]),...(stage===5?Object.values(C112.art.chronos):[])]);
};
window.BOF_CUTSCENE_CAST=C112;
