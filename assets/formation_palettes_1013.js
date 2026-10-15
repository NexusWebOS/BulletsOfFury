"use strict";
/* Stage liveries for the existing authored mini-aircraft. Palette substitution
   happens once per decoded sheet; no geometry, alpha, ordnance or poses change. */
const FBP13={cache:new Map(),builds:0,bytes:0,keys:new Map(),
 ramps:{
  1:[[0,0,0],[30,35,41],[77,86,95],[139,151,163],[197,210,220],[245,249,252]],
  4:[[0,0,0],[17,25,15],[39,56,26],[70,87,43],[116,134,69],[195,204,142]],
  6:[[0,0,0],[5,9,21],[9,20,43],[17,38,75],[38,78,136],[126,178,226]]
 }};
for(const stage of [1,4,6]){
 const a=VP12_ART[stage],d=AM13_ART['flight_variant_'+stage];
 for(const key of [a.key,a.rollKey,d.heading.key,d.roll.key])FBP13.keys.set(key,stage);
}
function fbp13Color(r,g,b,stage){
 const hi=Math.max(r,g,b),lo=Math.min(r,g,b);
 // Keep black outlines and the authored emitter/cockpit highlights intact.
 if(hi<=16)return [r,g,b];
 if(stage===1&&g>95&&g>r*1.5&&g>b*1.25)return [r,g,b];
 if(stage===4&&r>150&&r>g*1.8&&r>b*2.2)return [r,g,b];
 if(stage===6&&g>135&&b>175&&r<g*.75)return [r,g,b];
 let light=.2126*r+.7152*g+.0722*b;
 if(stage===1)light=Math.min(255,light*2.0);
 // Cobalt panels retain their hue hierarchy but the hull is now dark navy.
 if(stage===6)light=Math.min(255,light+(hi-lo)*.20);
 const ramp=FBP13.ramps[stage],v=light/255*(ramp.length-1),i=Math.min(ramp.length-2,Math.floor(v)),t=v-i;
 return ramp[i].map((c,k)=>Math.round(c+(ramp[i+1][k]-c)*t));
}
const FBP13_GET=XART.get;
XART.get=function(key){
 const source=FBP13_GET.apply(this,arguments),stage=FBP13.keys.get(key);
 if(!stage||!source||!source.width||!source.height)return source;
 const old=FBP13.cache.get(key);if(old?.source===source)return old.canvas;
 const canvas=document.createElement('canvas');canvas.width=source.width;canvas.height=source.height;
 const c=canvas.getContext('2d');c.drawImage(source,0,0);
 const pixels=c.getImageData(0,0,canvas.width,canvas.height),p=pixels.data;
 for(let i=0;i<p.length;i+=4){if(!p[i+3])continue;const color=fbp13Color(p[i],p[i+1],p[i+2],stage);p[i]=color[0];p[i+1]=color[1];p[i+2]=color[2];}
 c.putImageData(pixels,0,0);FBP13.builds++;FBP13.bytes+=canvas.width*canvas.height*4-(old?old.canvas.width*old.canvas.height*4:0);
 FBP13.cache.set(key,{source,canvas,stage});return canvas;
};
function fbp13Clear(){FBP13.cache.clear();FBP13.bytes=0;}
const FBP13_RETIRE=bofDerivedCachesRetire;
bofDerivedCachesRetire=function(){fbp13Clear();return FBP13_RETIRE.apply(this,arguments);};
const FBP13_BEGIN=beginStage;
beginStage=function(){fbp13Clear();return FBP13_BEGIN.apply(this,arguments);};
const FBP13_READY=stageLoadReady;
stageLoadReady=function(n){const ready=FBP13_READY.apply(this,arguments);if(ready){const stage=n||run.stage;for(const [key,s]of FBP13.keys)if(s===stage&&XART.rdy(key))XART.get(key);}return ready;};
window.BOF_FORMATION_PALETTES={stats:FBP13,source:key=>FBP13_GET.call(XART,key)};
