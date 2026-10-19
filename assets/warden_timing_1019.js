"use strict";
/* Keep the authored Warden attacks and the shorter Furious stomp follow-ups.
   The later pose controller had reset every claw tell to Normal's 1.1 seconds. */
const WT19={baseSet:s7mSet,version:'warden-timing-1019',events:[]};
function wt19Own(b){return !window.WT19_OFF&&run.stage===7&&b?._s7mod&&!b._s7mod.tank&&!b._gp4Host&&!b._s7mod.frExit;}
s7mSet=function(b,mode){
 const follow=wt19Own(b)&&mode?.startsWith('swipe')&&(b._s7mod.s67Swat||0)>0;
 const result=WT19.baseSet.apply(this,arguments),M=b?._s7mod;
 if(!wt19Own(b))return result;
 if(mode?.startsWith('swipe'))M.warn=follow?.46:diffKey==='easy'?1.4:diffKey==='furious'||diffKey==='insanity'?.80:diffKey==='hard'?.94:1.1;
 else if(mode==='battery1009'&&diffKey!=='easy')M.warn=diffKey==='furious'||diffKey==='insanity'?1.16:diffKey==='hard'?1.4:1.65;
 else return result;
 WT19.events.push({mode,difficulty:diffKey,tell:M.warn,stompFollowup:!!follow});
 if(WT19.events.length>100)WT19.events.shift();
 return result;
};
