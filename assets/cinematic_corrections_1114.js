"use strict";
/* Mike rejected the pasted portrait/airframe composite and the Chronos comic finale. */
const FIXC14={base:{keys:d1110Keys,visual:d1110Visual},last:null};
// Restore the exact pre-comic native death renderer, including its ignition,
// committed missile, breakup, flight home and native continuation.
h3EndingDraw=CB1110.base.endingDraw;
hf17Warm=CB1110.base.warm;
XART._src.fury14_jungle_comic='assets/game/shared/cinematics/opening_1114/jungle-flight.png';
d1110Keys=function(rows,p=run.pilot){const keys=FIXC14.base.keys.apply(this,arguments);if(rows.some(b=>b.fury14)){
 keys.push('fury14_jungle_comic',S113_ART.banks['cockpit-'+p].key,CM3_ART.banks['caption-0'].key,D1110_ART.banks['native-'+p+'-rear'].key);
 }return [...new Set(keys)];};
function fixc14Image(key,box,pan=.5,zoom=1){if(!XART.rdy(key))return;const im=XART.get(key),[x,y,w,h]=box,k=Math.max(w/im.width,h/im.height)*zoom,dw=im.width*k,dh=im.height*k;
 ctx.drawImage(im,Math.round(x-(dw-w)*pan),Math.round(y-(dh-h)*.42),Math.round(dw),Math.round(dh));}
function fixc14Panel(n,time,b,s){const x=n*940,box=[x+12,12,888,488];
 c16Clip(box,()=>{ctx.save();ctx.translate(x,0);
  if(n===1){
   // A complete authored cockpit plate: pilot, body, controls and cabin share
   // one perspective. Never insert a detached head into an aircraft sprite.
   const a=S113_ART.banks['cockpit-'+run.pilot];fixc14Image(a.key,[12,12,888,488],.5,1);
  }else{
   const zoom=n===2?1.28:1.02,pan=n===2?.83:clamp(.15+time*.006,.15,.55);
   fixc14Image('fury14_jungle_comic',[12,12,888,488],pan,zoom);
   if(n===0){const u=clamp(time/34,0,1);d1110Native(run.pilot,'rear',390+u*80,245-u*45,390-u*55);}
   if(n===2&&b.shot==='boom'&&s.t>1.15){const age=s.t-1.15;if(age<1.4)cinFx('airburst',655,257,140,age);const im=XART.get('fury14_boom');if(im)ctx.drawImage(im,510,90,340,170);}
   if(n===2&&b.shot==='resolve')d1110Native(run.pilot,'rear',370,265,260);
  }
 ctx.restore();});
 ctx.strokeStyle='#0b0a0a';ctx.lineWidth=10;ctx.strokeRect(x+8,8,896,496);
 ctx.strokeStyle='#f5dfaf';ctx.lineWidth=3;ctx.strokeRect(x+3,3,906,506);
}
function fixc14Caption(b,s){
 if(!b.text){msgFaceUse('dialogue');controlHintRow([['pad_start','SKIP']],730,493,880,10);msgFaceUse(null);return;}
 const a=CM3_ART.banks['caption-0'];if(XART.rdy(a.key))ctx.drawImage(XART.get(a.key),31,382,850,116);
 msgFaceUse('dialogue');msgText(b.who,155,397,14,'#16131a',1,1);
 msgDrawBlock({text:b.text,budget:s.shown,x:75,y:423,w:762,h:53,maxH:18,minH:16,lineMul:1.25,color:'#fff1d3',valign:'middle',align:'left'});
 controlHintRow([['pad_a',s.shown<b.text.length?'READ':'NEXT'],['pad_start','SKIP']],723,505,887,8);msgFaceUse(null);
}
d1110Visual=function(b,s){
 if(!b.fury14)return FIXC14.base.visual.apply(this,arguments);
 const idx=s.i,targets=[0,940,1880,940,1880,1880],to=targets[idx],from=idx?targets[idx-1]:0,u=clamp(s.t/1.65,0,1),ease=u*u*(3-2*u),camera=lerp(from,to,ease);
 const time=s.beats.slice(0,idx).reduce((v,q)=>v+q.duration,0)+s.t;
 ctx.save();ctx.setTransform(SS,0,0,SS,0,0);ctx.imageSmoothingEnabled=false;ctx.fillStyle='#f0d9a5';ctx.fillRect(0,0,912,512);
 ctx.save();ctx.translate(-Math.round(camera),0);for(let n=0;n<3;n++)fixc14Panel(n,time,b,s);ctx.restore();
 if(b.shot==='boom'&&s.t>=1.15&&s.t<1.5){ctx.fillStyle='rgba(255,237,188,'+(.6*(1-(s.t-1.15)/.35))+')';ctx.fillRect(460,12,440,360);}
 fixc14Caption(b,s);
 const fade=b.shot==='fade'?clamp(s.t/b.duration,0,1):idx===0?1-clamp(s.t/.7,0,1):0;
 if(fade>0){ctx.fillStyle='rgba(0,0,0,'+fade+')';ctx.fillRect(0,0,912,512);}
 FIXC14.last={kind:'comic-strip',pilot:run.pilot,shot:b.shot,time:s.t,panel:Math.round(camera/940),camera,wholeCockpit:true,detachedPortrait:false,text:b.text};FURY14.last=FIXC14.last;ctx.restore();
};
window.BOF_CINEMATIC_CORRECTIONS_1114=FIXC14;
