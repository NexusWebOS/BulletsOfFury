"use strict";
/* Cole's radio conversation and route selection run above live flight.
   Preserve the scheduled wave queue; only new enemy arrivals wait. */
const RADIO17={hold:false,frames:0,base:{play:updatePlay,scene:s6q13Scene,tick:fb2TalkTick,start:fb2TalkStart,spawn:spawnEnemy}};
function radio17Live(){return state===GS.PLAY&&run.stage===6&&!run._gp4StageX&&
 (!!(fb2Talk&&!fb2Talk.done)||!!(s6Wing?.choice&&!s6Wing.route));}
fb2TalkStart=function(){
 fb2Talk={beats:fb2TeamScript(),i:0,t:0,shown:0,age:0,done:false};
 for(let i=0;i<3;i++)XART.rdy('fb2_cole_rage_'+i);
};
fb2TalkTick=function(dt){const rounds=eBullets.slice(),px=player.x,py=player.y;
 try{return RADIO17.base.tick.apply(this,arguments);}finally{
  // The old scene owner cleared this array as a pause safeguard. These live
  // rounds still own their motion, collisions and lifetime in updatePlay.
  eBullets.splice(0,0,...rounds.filter(q=>!eBullets.includes(q)));
  if(fb2Talk?.beats?.[fb2Talk.i]?.kind==='demo'){player.x=px;player.y=py;}
 }
};
s6q13Scene=function(){if(run.stage===6&&fb2Talk&&!fb2Talk.done)return null;
 return RADIO17.base.scene.apply(this,arguments);};
spawnEnemy=function(){if(RADIO17.hold||radio17Live())return null;return RADIO17.base.spawn.apply(this,arguments);};
updatePlay=function(dt){
 if(!radio17Live())return RADIO17.base.play.apply(this,arguments);
 const plan=stagePlan,time=stageTimer,wave=waveIdx,spawn=spawnClock,active=fb2TalkActive,tick=fb2TalkTick;
 const wing=s6Wing,choosing=!!(wing?.choice&&!wing.route);
 // The older pursuit owner returns before flight updates while this flag is
 // set. Poll its real menu once, then let an unconfirmed choice fly normally.
 // RADIO17.hold still blocks arrivals and the wave clock below stays parked.
 if(choosing&&!wing.autoRoute)fr27RouteInput(wing);
 if(choosing&&!wing.autoRoute)wing.choice=false;
 if(fb2Talk&&!fb2Talk.done)tick(dt);
 RADIO17.hold=true;RADIO17.frames++;stagePlan=[];
 fb2TalkActive=()=>false;fb2TalkTick=()=>{};
 try{return RADIO17.base.play.apply(this,arguments);}finally{
  fb2TalkActive=active;fb2TalkTick=tick;stagePlan=plan;stageTimer=time;waveIdx=wave;spawnClock=spawn;RADIO17.hold=false;
  if(choosing)wing.choice=true;
 }
};
window.BOF_LIVE_RADIO={state:RADIO17,active:radio17Live};
