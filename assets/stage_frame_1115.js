"use strict";
/* Generated map briefing frames and native PixelMap glyph reveals.
   Message selection, stage locks, reward receipts and map inputs retain owners. */
const MBR15={base:{open:openStageSelect,theater:window.drawTheaterProgression1003g},typing:null,last:null,events:[],charsPerSecond:32};
for(const a of Object.values(MBR15_ART.images))XART._src[a.key]=a.path+'?v='+a.sha256.slice(0,12);
function mb15Warm(){return Object.values(MBR15_ART.images).map(a=>XART.rdy(a.key)).every(Boolean);}
function mb15Variant(copy){const s=String(copy.key)+' '+String(copy.title);return /clear|unlock|reward|earned|mk2|enhanced|superiority/i.test(s)?'clear':/required|cf4-x|rival|contact|pursuit|harrier|storm cannon|city rescue|fate/i.test(s)?'priority':'mission';}
function mb15Text(s){return pm27Text(String(s??'')).replace(/\s+/g,' ').trim().toUpperCase();}
function mb15Layout(text,width,height,title=false){
 const choices=title?[['fury_strike',16],['fury_strike',14],['command',14],['command',12],['command',10],['command',8]]:[['command',12],['command',10],['command',8]];
 let result;
 for(const[family,h]of choices){const bank=pm27Bank(family,h),step=bank.height+4,lines=pm27Wrap(text,width,bank.height,family);let at=0;
  const rows=lines.map(full=>{const start=Math.max(at,text.indexOf(full,at));at=start+full.length;return{full,start};}),used=bank.height+Math.max(0,rows.length-1)*step;
  result={family,height:bank.height,step,rows,used,width,available:height,fontKey:bank.key};if(used<=height)return result;
 }return result;
}
function mb15Reveal(copy,ready){const title=mb15Text(copy.title),body=mb15Text(copy.body),key=String(copy.key)+'|'+title+'|'+body,now=Number.isFinite(stateT)?stateT:0;
 if(!MBR15.typing||MBR15.typing.key!==key){MBR15.typing={key,last:now,elapsed:0,count:0};MBR15.events.push({event:'briefing-changed',key:String(copy.key),variant:mb15Variant(copy)});if(MBR15.events.length>120)MBR15.events.shift();}
 const t=MBR15.typing,dt=Math.max(0,Math.min(.25,now-t.last));t.last=now;if(ready&&!campPause)t.elapsed+=dt;
 t.count=ready?Math.min(title.length+body.length,Math.floor(t.elapsed*MBR15.charsPerSecond)):0;return{title,body,count:t.count,total:title.length+body.length};
}
function mb15Lines(layout,budget,box,center,palette){const[x,y,w,h]=box,top=y+Math.round((h-layout.used)/2),visible=[];
 for(let i=0;i<layout.rows.length;i++){const row=layout.rows[i],text=row.full.slice(0,Math.max(0,budget-row.start)),cy=top+layout.height/2+i*layout.step,xx=center?x+Math.round((w-pm27Width(row.full,layout.height,layout.family))/2):x;
  if(text)pm27Draw(ctx,text,xx,cy,layout.height,{family:layout.family,palette,align:'left',width:w});visible.push(text);
 }return visible;
}
function mb15BriefingDraw(copy){if(state!==GS.STAGESEL)return false;const ready=mb15Warm()&&pm27Live(),reveal=mb15Reveal(copy,ready);if(!ready)return false;
 const variant=mb15Variant(copy),a=MBR15_ART.images[variant],r={x:12,y:VH-174,w:456,h:150},safe=MBR15_ART.textSafe,tbox=[r.x+safe.title[0],r.y+safe.title[1],safe.title[2],safe.title[3]],bbox=[r.x+safe.body[0],r.y+safe.body[1],safe.body[2],safe.body[3]],title=mb15Layout(reveal.title,tbox[2],tbox[3],true),body=mb15Layout(reveal.body,bbox[2],bbox[3]);
 ctx.save();ctx.imageSmoothingEnabled=false;ctx.globalAlpha=1;ctx.filter='none';ctx.shadowBlur=0;
 ctx.drawImage(XART.get(a.key),r.x,r.y,a.w/2,a.h/2);
 const visibleTitle=mb15Lines(title,Math.min(reveal.count,reveal.title.length),tbox,true,variant==='mission'?'signal':'gold'),visibleBody=mb15Lines(body,Math.max(0,reveal.count-reveal.title.length),bbox,false,'chrome');ctx.restore();
 MBR15.last={key:String(copy.key),variant,rect:r,count:reveal.count,total:reveal.total,title:reveal.title,body:reveal.body,titleLayout:title,bodyLayout:body,visibleTitle,visibleBody,font:'PixelMap',frameKey:a.key};return true;
}
openStageSelect=function(){MBR15.typing=null;mb15Warm();return MBR15.base.open.apply(this,arguments);};
// Retain the optional renderer entry point; the removed strip draws no pixels.
window.drawTheaterProgression1003g=function(){return false;};
mb15Warm();window.BOF_STAGE_BRIEFING_1115=MBR15;
