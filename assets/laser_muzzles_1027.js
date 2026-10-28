"use strict";
/* Focused blue laser emitters. Beam owners retain timing, collision and sound. */
const LM27={enabled:true,draws:0,history:[],base:{beam:av3Beam,load:stageLoadBegin}};
for(const a of Object.values(LM27_ART.banks))XART._src[a.key]=a.path;
function lm27Warm(){for(const a of Object.values(LM27_ART.banks))XART.rdy(a.key);}
function lm27Laser(color){return !/fusion|helix|lightning|storm/.test(String(color))&&(typeof color==='number'?color:av3Color(color))===1;}
function lm27Muzzle(g,x,y,angle,width,t){
 const name=width<16?'small':width<24?'medium':'large',a=LM27_ART.banks[name];
 if(!XART.rdy(a.key)){lm27Warm();return false;}
 const d=((Math.round(angle*64/TAU)%64)+64)%64,f=((Math.floor(t*24)%16)+16)%16,i=f*64+d;
 g.save();g.globalAlpha=1;g.globalCompositeOperation='source-over';g.filter='none';g.shadowBlur=0;g.imageSmoothingEnabled=false;
 g.drawImage(XART.get(a.key),i%64*64,Math.floor(i/64)*64,64,64,Math.round(x-32),Math.round(y-32),64,64);g.restore();
 LM27.draws++;LM27.history.push({x,y,angle,direction:d,phase:f,size:name,width,time:t});if(LM27.history.length>120)LM27.history.shift();return true;
}
stageLoadBegin=function(n,keys){return LM27.base.load.call(this,n,[...(keys||[]),...Object.values(LM27_ART.banks).map(a=>a.key)]);};
av3Beam=function(g,x,y,angle,length,width,color,t=AV3.clock,alpha=1,muzzle=true){
 if(!LM27.enabled||!lm27Laser(color))return LM27.base.beam.apply(this,arguments);
 // False propagates through the original beam renderer, removing its ice crown.
 const result=LM27.base.beam.call(this,g,x,y,angle,length,width,color,t,alpha,false);
 if(muzzle&&alpha>0&&[x,y,angle,length,width,t].every(Number.isFinite)&&length>0&&width>=.5)lm27Muzzle(g,x,y,angle,width,t);
 return result;
};
lm27Warm();globalThis.BOF_LASER_MUZZLES_1027=LM27;
