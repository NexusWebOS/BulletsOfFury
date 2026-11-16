"use strict";
/* Conservative clipping of authored weather tiles only. Preserve native art,
   frame selection, clocks, return values and reactor draw accounting. */
const NW16={base:{weather:th114Weather,storm:th114Blit,reactor:tc119Blit},active:false,viewport:null,skipped:0};
function nw16Outside(x,y,w,h){
 const v=NW16.viewport;return !!v&&(x+w<=v.left||x>=v.right||y+h<=v.top||y>=v.bottom);
}
th114Blit=function(name,f,x,y){
 if(NW16.active){const B=THS114_ART.banks[name];if(B&&nw16Outside(Math.round(x-B.cw/2),Math.round(y-B.ch/2),B.cw,B.ch)){
  const c=B.cells[clamp(f|0,0,B.frames-1)];if(!XART.rdy(c[0]))return false;NW16.skipped++;return true;
 }}return NW16.base.storm.apply(this,arguments);
};
tc119Blit=function(name,f,x,y){
 if(NW16.active){const B=TC119_ART.banks[name],c=B?.cells[clamp(f|0,0,(B?.frames||1)-1)];if(c&&TC119.images[c[0]]&&nw16Outside(Math.round(x)-B.pivot[0]+c[5],Math.round(y)-B.pivot[1]+c[6],c[3],c[4])){
  TC119.draws[name]=(TC119.draws[name]||0)+1;NW16.skipped++;return true;
 }}return NW16.base.reactor.apply(this,arguments);
};
th114Weather=function(){const active=NW16.active,viewport=NW16.viewport,m=ctx.getTransform(),pad=ctx.imageSmoothingEnabled?1:0;NW16.active=true;
 NW16.viewport=m.b===0&&m.c===0&&m.a>0&&m.d>0&&ctx.globalCompositeOperation==='source-over'&&ctx.filter==='none'&&ctx.shadowBlur===0&&ctx.shadowOffsetX===0&&ctx.shadowOffsetY===0&&[m.a,m.d,m.e,m.f].every(Number.isFinite)?
  {left:(-pad-m.e)/m.a,right:(cv.width+pad-m.e)/m.a,top:(-pad-m.f)/m.d,bottom:(cv.height+pad-m.f)/m.d}:null;
 try{return NW16.base.weather.apply(this,arguments);}finally{NW16.active=active;NW16.viewport=viewport;}};
