"use strict";
/* One compact portrait chat plate. Fixed authored pixels; no runtime frame stretching. */
const CD27={base:{dlg:dlgBox,panel:ui20Panel,contents:ui20PanelContents,caption:inv20Text,load:stageLoadBegin},height:84,inDlg:0,last:null,history:[],pages:new Map()};
for(const [k,path]of Object.entries(CD27_ART.assets))XART._src[k]=path;
function cd27Width(available){return CD27_ART.widths.find(w=>w<=available)||CD27_ART.widths.at(-1);}
function cd27Key(who,w){const name=String(who||'neutral').toLowerCase(),key='cd27_'+name+'_'+w;return CD27_ART.assets[key]?key:'cd27_neutral_'+w;}
function cd27Warm(){for(const name of ['cole','neutral','dracodia','chronos'])for(const w of CD27_ART.widths)XART.rdy(cd27Key(name,w));}
cd27Warm();
stageLoadBegin=function(n,keys){return CD27.base.load.call(this,n,[...(keys||[]),...Object.keys(CD27_ART.assets)]);};
function cd27View(){if(CD27.viewport)return CD27.viewport.w;return state===GS.CUTSCENE||state===GS.CAMPAIGNINTRO?cutsceneViewWidth():VW;}
ui20Panel=function(who,x,y,w,h,portrait){
 if(!CD27.inDlg&&(!portrait||w<220||h<70))return CD27.base.panel.apply(this,arguments);
 const width=cd27Width(Math.min(w,cd27View()-16)),height=CD27.height;
 x=Math.round(x+(w-width)/2);y=Math.round(y+h-height);x=clamp(x,8,Math.max(8,cd27View()-width-8));y=clamp(y,8,(CD27.viewport?.h||VH)-height-8);
 const key=cd27Key(who,width);if(!XART.rdy(key)){cd27Warm();return CD27.base.panel.call(this,who,x,y,width,height,portrait);}
 ctx.save();ctx.imageSmoothingEnabled=false;ctx.drawImage(XART.get(key),x,y);ctx.restore();
 const r={cd27:true,x,y,w:width,h:height,key,bw:100,name:{x:x+106,y:y+10,w:68,h:12},text:{x:x+104,y:y+32,w:width-122,h:38},portraitRect:{x:x+15,y:y+8,w:74,h:68}};
 CD27.last=r;return r;
};
function cd27Page(who,full,shown,r,maxH){
 const t=r.text,fit=msgBlockLayout(full,t.w,t.h,Math.min(maxH||11,11),8,1.25);
 if(fit.height<=t.h)return {text:full,budget:shown,H:fit.H,index:0,count:1};
 const rows=msgWrap(full,t.w,8),capacity=Math.max(1,Math.floor((t.h-8)/10)+1),pages=[];let offset=0;
 for(let i=0;i<rows.length;i+=capacity){const text=rows.slice(i,i+capacity).join(' ');pages.push({text,start:offset,end:offset+text.length});offset+=text.length+1;}
 const key=who+'|'+full;let p=CD27.pages.get(key);
 if(!p){p={at:performance.now(),instant:shown>=full.length};if(CD27.pages.size>80)CD27.pages.clear();CD27.pages.set(key,p);}
 let index;
 if(p.instant){const elapsed=(performance.now()-p.at)/1000,durations=pages.map(p=>Math.max(1.2,p.text.length/34)),total=durations.reduce((a,b)=>a+b,0);let age=elapsed%total;index=0;while(index<pages.length-1&&age>=durations[index])age-=durations[index++];}
 else index=Math.max(0,pages.findIndex(p=>shown<=p.end));
 if(!p.instant&&shown>=pages.at(-1).end)index=pages.length-1;
 const page=pages[index];return {text:page.text,budget:p.instant?page.text.length:Math.max(0,shown-page.start),H:8,index,count:pages.length};
}
ui20PanelContents=function(who,full,shown,port,r,maxH=11,nameH=10){
 if(!r?.cd27)return CD27.base.contents.apply(this,arguments);
 const portraitDraw=ui20Portrait(ctx,port,r.portraitRect),n=r.name,t=r.text;
 ui20Text(ctx,who,n.x+n.w/2,n.y+n.h/2,Math.min(nameH,10),n.w,'center',UI20.color(who));
 const page=cd27Page(who,String(full),shown,r,maxH),layout=msgDrawBlock({text:page.text,budget:page.budget,x:t.x,y:t.y,w:t.w,h:t.h,maxH:page.H,minH:page.H,lineMul:1.25,color:'#fff9eb',alpha:1,outline:false,align:'center',stableCenter:true,valign:'middle'});
 const result={portrait:port,name:n,text:t,portraitRect:r.portraitRect,portraitDraw,layout,page:{index:page.index,count:page.count,text:page.text}};
 CD27.history.push({who,w:r.w,h:r.h,x:r.x,y:r.y,port,layout,page:result.page});if(CD27.history.length>100)CD27.history.shift();return result;
};
dlgBox=function(o){
 if(state===GS.PLAY&&typeof fb2TalkActive==='function'&&fb2TalkActive()){
  const beat=fb2Talk?.beats?.[fb2Talk.i];
  if(!beat||beat.kind==='demo'||beat.kind==='callisto'||String(o.full||'').toUpperCase()!==String(beat.text||'').toUpperCase())return;
 }
 const width=cd27Width(cd27View()-20),height=CD27.height,inPlay=state===GS.PLAY;
 const x=o.x==null?(inPlay?PLAY.x+8:Math.round((cd27View()-width)/2)):clamp(o.x,8,Math.max(8,cd27View()-width-8));
 CD27.inDlg++;try{return CD27.base.dlg.call(this,{...o,pw:width,ph:height,fixedHeight:true,forceShown:o.shown!=null?true:o.forceShown,x});}finally{CD27.inDlg--;}
};
inv20Text=function(who,text,W,H,shown=text.length,alpha=1){
 const width=cd27Width(W-20),p=UI20.pilot(who),port=p?commPortrait(p.key,shown<text.length?'talk':'idle'):/DRACODIA/i.test(who)?DP20.key:null;
 const old=CD27.viewport;CD27.viewport={w:W,h:H};CD27.inDlg++;ctx.save();ctx.globalAlpha*=alpha;msgFaceUse('dialogue');
 try{const r=ui20Panel(who,Math.round((W-width)/2),H-CD27.height-13,width,CD27.height,true);if(r){const content=ui20PanelContents(who,String(text).toUpperCase(),shown,port,r);INV20.caption={who,text,x:r.x,y:r.y,w:r.w,h:r.h,shown,...content};}}
 finally{msgFaceUse(null);ctx.restore();CD27.inDlg--;CD27.viewport=old;}
};
// The recovered HQ opening has its own caption entry point; use the same plate.
cinDialogue=function(beat,budget,W,H){if(!beat.text)return false;inv20Text(cinPilotName(beat.who),beat.text,W,H,budget);
 if(budget>=beat.text.length&&hqHoldT>=HQ_HOLD&&Math.floor(hqBeatT*2.2)%2){const r=CD27.last;msgFaceUse('dialogue');msgTextLeft('NEXT',r.x+r.w-48,r.y+15,7,'#ffe082',1,1,0,false);msgFaceUse(null);}return true;};
globalThis.BOF_COMPACT_DIALOGUE_1026=CD27;
