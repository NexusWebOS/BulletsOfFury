'use strict';
/* The native debug jump enters PLAY directly, bypassing the deployment loader.
   Keep that route's simulation behind the same decoded-resource gate. The main
   frame loop still services stageLoadTick; no recording-only warm-up is needed. */
const BP119={base:{start:debugStartFight,play:updatePlay,draw:drawScene},pending:null,events:[]};
function bp119Pending(){
 if(!BP119.pending)return false;
 if(BP119.pending!==debugFight){BP119.pending=null;return false;}
 return true;
}
debugStartFight=function(entry,opts){
 const result=BP119.base.start.apply(this,arguments);
 BP119.pending=result&&debugFight&&!stageLoadReady(entry.stage)?debugFight:null;
 if(BP119.pending)BP119.events.push({type:'loading',stage:entry.stage});
 return result;
};
updatePlay=function(dt){
 if(bp119Pending()){
  if(!stageLoadReady(debugFight.stage))return;
  BP119.events.push({type:'ready',stage:debugFight.stage});BP119.pending=null;
 }
 return BP119.base.play.apply(this,arguments);
};
drawScene=function(dt){
 const result=BP119.base.draw.apply(this,arguments);
 if(state===GS.PLAY&&bp119Pending())drawStageLoadOverlay();
 return result;
};
globalThis.BOF_BOSS_PREVIEW_LOADING_1109=BP119;
