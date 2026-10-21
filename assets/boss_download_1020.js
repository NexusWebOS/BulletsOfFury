"use strict";
/* Intact forms use the commissioned PixelLab meshes. Broken-module and
   hammerless returns trace their CURRENT authored pixels once, so a download
   cannot bring back a destroyed cannon, wing or hammer for a single frame. */
const DL20={base:dr21Download,cache:new Map(),builds:0,last:null};
function dl20Changed(b){return ph21Own(b)&&ph21State(b)?.parts.some(p=>p.destroyed)||hb20Own(b)&&hb20State(b)?.rage;}
function dl20Mesh(b){const id=b._r30.v18.form+':'+v18Size(b)+':'+b.parts.filter(p=>p.destroyed).map(p=>p.id).join(',')+':'+!!hb20State(b)?.rage;if(DL20.cache.has(id))return DL20.cache.get(id);
 const c=document.createElement('canvas');c.width=c.height=256;const g=c.getContext('2d',{willReadFrequently:true}),names=['save','restore','translate','rotate','scale','drawImage'],props=['globalAlpha','globalCompositeOperation','imageSmoothingEnabled'],saved={},pd={};g.translate(128,128);g.scale(.5,.5);g.translate(-b.x,-b.y);g.imageSmoothingEnabled=false;
 try{for(const name of props){pd[name]=Object.getOwnPropertyDescriptor(ctx,name);Object.defineProperty(ctx,name,{configurable:true,get:()=>g[name],set:v=>g[name]=v});}for(const n of names){saved[n]=ctx[n];ctx[n]=(...args)=>g[n](...args);}v19Body(b);}
 finally{for(const n of names)ctx[n]=saved[n];for(const name of props){delete ctx[name];if(pd[name])Object.defineProperty(ctx,name,pd[name]);}}
 const raw=g.getImageData(0,0,256,256),src=raw.data,out=g.createImageData(256,256),dst=out.data;let top=255,bottom=0;
 for(let y=1;y<255;y++)for(let x=1;x<255;x++){const at=(y*256+x)*4;if(src[at+3]<48)continue;top=Math.min(top,y);bottom=Math.max(bottom,y);let edge=false,crease=false;for(const d of [-4,4,-1024,1024]){edge||=src[at+d+3]<48;crease||=Math.abs(src[at]-src[at+d])+Math.abs(src[at+1]-src[at+d+1])+Math.abs(src[at+2]-src[at+d+2])>100;}
  const grid=(x+y)%7===0||(x-y+256)%11===0;if(!edge&&!crease&&!grid)continue;dst[at]=edge?219:157;dst[at+1]=edge?207:134;dst[at+2]=255;dst[at+3]=edge?220:crease?155:65;
 }
 g.setTransform(1,0,0,1,0,0);g.clearRect(0,0,256,256);g.putImageData(out,0,0);const glow=document.createElement('canvas');glow.width=glow.height=256;const gg=glow.getContext('2d');gg.drawImage(c,0,0);gg.globalCompositeOperation='source-in';gg.fillStyle='#ffffff';gg.fillRect(0,0,256,256);
 const q={c,glow,top,bottom,parts:v18Rig(b).filter(v=>!v.spec.hidden).map(v=>v.layer||v.p.id),id};DL20.cache.set(id,q);if(DL20.cache.size>6)DL20.cache.delete(DL20.cache.keys().next().value);DL20.builds++;return q;
}
dr21Download=function(b,t,duration,incoming){if(!dl20Changed(b))return DL20.base.apply(this,arguments);const a=dl20Mesh(b),u=clamp(t/duration,0,1),reveal=v19Ease(incoming?(u-.26)/.62:(u-.06)/.62),growth=incoming?lerp(.22,1,v19Ease(u/.22)):lerp(1,.22,v19Ease((u-.76)/.24)),size=512,top=b.y-size/2,cut=top+size*reveal,offsetY=Math.max(0,viewTopY()+72-(b.y+(a.top-128)*2))*(incoming?1-v19Ease((u-.88)/.12):v19Ease(u/.15));
 ctx.save();ctx.translate(0,offsetY);const wire=()=>{ctx.save();ctx.imageSmoothingEnabled=false;ctx.translate(b.x,b.y);ctx.scale(growth,growth);ctx.drawImage(a.c,-256,-256,512,512);const y=-256+((Math.floor(t/.07)%16)/15)*512;ctx.save();ctx.beginPath();ctx.rect(-256,y-12,512,24);ctx.clip();ctx.drawImage(a.glow,-256,-256,512,512);ctx.restore();ctx.restore();};
 ctx.save();ctx.beginPath();ctx.rect(b.x-size,incoming?cut:top-1,size*2,incoming?Math.max(0,top+size-cut+1):Math.max(0,cut-top+1));ctx.clip();wire();ctx.restore();
 ctx.save();ctx.beginPath();ctx.rect(b.x-size,incoming?top:cut,size*2,incoming?Math.max(0,cut-top):Math.max(0,top+size-cut));ctx.clip();v19Body(b);ctx.restore();
 if(reveal>0&&reveal<1){ctx.save();ctx.beginPath();ctx.rect(b.x-size,cut-4,size*2,8);ctx.clip();ctx.globalCompositeOperation='lighter';wire();ctx.restore();}if(incoming?u<.24:u>.76)dr21Art('download',t,b.x,b.y,70,.7);ctx.restore();DL20.last={id:a.id,parts:a.parts,incoming,u,reveal};return true;
};
globalThis.BOF_BOSS_DOWNLOAD=DL20;
