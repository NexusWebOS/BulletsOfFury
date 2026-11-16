"use strict";
/* Clipped bitmap dialogue follows the currently revealing line. No copy/input changes. */
const DS15={base:msgDrawBlock,columns:new Map(),last:null};
function ds15Scene(){return state===GS.CAMPAIGNINTRO?campaignIntro?.d1110:state===GS.VICTORY?D1110.ending?.scene:BOFCinematicDirector.current;}
msgDrawBlock=function(o){
 const scene=ds15Scene(),dialogue=_msgFace==='dialogue'||!!scene;
 if(!dialogue||!(o.w>0&&o.h>0))return DS15.base.apply(this,arguments);
 const text=String(o.text??''),L=msgBlockLayout(text,o.w,o.h,o.maxH,o.minH,o.lineMul,o.spacing);
 if(L.height<=o.h)return DS15.base.apply(this,arguments);
 const budget=o.budget==null?Infinity:Math.max(0,Math.floor(o.budget)),beat=scene?.beats[scene.i],key=[state,scene?.id,beat?.id,o.x,o.y,o.w,o.h,text].join('|'),now=scene?.age??stateT;
 let q=DS15.columns.get(key);if(!q||budget<q.budget){q={at:now,offset:0,budget:0};DS15.columns.set(key,q);if(DS15.columns.size>40)DS15.columns.delete(DS15.columns.keys().next().value);}
 let n=budget,cursor=0;for(let i=0;i<L.lines.length;i++){if(n<=0)break;cursor=i;n-=L.lines[i].length+1;}
 const max=Math.max(0,L.height-o.h),target=Math.min(max,Math.max(0,cursor*L.step+L.H-o.h)),dt=campPause||D1110.paused?0:Math.max(0,Math.min(.1,now-q.at));q.at=now;q.budget=budget;
 q.offset+=Math.min(1,1-Math.exp(-dt*20))*(target-q.offset);if(Math.abs(target-q.offset)<.15)q.offset=target;
 const offset=Math.round(q.offset),visible=[];let yy=o.y+L.H/2-offset,left=budget;
 ctx.save();ctx.beginPath();ctx.rect(o.x,o.y,o.w,o.h);ctx.clip();
 for(let i=0;i<L.lines.length;i++){const line=L.lines[i];if(left<=0)break;const part=left>=line.length?line:line.slice(0,left);
  if(part){let x=o.x;if(o.align==='center')x+=(o.w-msgMeasure(o.stableCenter?line:part,L.H,o.spacing))/2;
   msgTextLeft(part,x,yy,L.H,o.color||DIALOGUE_BODY_COLOR,o.tintA??1,o.alpha??1,o.spacing,o.outline||false);
   if(yy+L.H/2>o.y&&yy-L.H/2<o.y+o.h)visible.push({row:i,text:part,y:yy});}
  left-=line.length+1;yy+=L.step;
 }ctx.restore();DS15.last={text,budget,offset,target,max,rows:L.lines,visible,box:{x:o.x,y:o.y,w:o.w,h:o.h},height:L.H,step:L.step,scene:scene?.id,shot:beat?.id};return{...L,scroll:offset};
};
window.BOF_DIALOGUE_SCROLL_1115=DS15;
