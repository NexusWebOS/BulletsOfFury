"use strict";
/* Dedicated illustrated dialogue portrait. UI concepts remain preview choices;
   the native dialogue timing, speaker selection and input keep their owners. */
const DP20={key:'dp20_dracodia_portrait',base:{portrait:dr5Portrait,warm:dr5Warm,load:stageLoadBegin},draws:0};
XART._src[DP20.key]='assets/game/levels/stage_08/cinematics/dracodia_portrait_1020/portrait.webp';
dr5Warm=function(){DP20.base.warm.apply(this,arguments);XART.rdy(DP20.key);};
stageLoadBegin=function(n,keys){return DP20.base.load.call(this,n,n===8?[...(keys||[]),DP20.key]:keys);};
dr5Portrait=function(face,talk=0){
 if(XART.rdy(DP20.key)){DP20.draws++;return XART.get(DP20.key);}
 return DP20.base.portrait.apply(this,arguments);
};
globalThis.BOF_DRACODIA_PORTRAIT=DP20;
