'use strict';
/* Depth changes happen beyond the top edge, never by shrinking in place. */
const C35={get:XART.get,tool:hf22Tool,flight:hammerFlightDraw,cache:new Map(),lastFlight:null};
function c35DepthFlight(b,R,targetScale){
 const changing=Math.abs(R.from.scale-targetScale)>.15;
 if(!changing){const u=clamp(R.t/.8,0,1),e=u*u*(3-2*u);b.x=lerp(R.from.x,R.to.x,e);b.y=lerp(R.from.y,R.to.y,e);R.scale=targetScale;return u>=1;}
 const exit=.7,enter=.85,off=viewTopY()-340;
 if(R.t<exit){const u=R.t/exit;b.x=R.from.x;b.y=lerp(R.from.y,off,u*u);R.scale=R.from.scale;}
 else{const u=clamp((R.t-exit)/enter,0,1);b.x=R.to.x;b.y=lerp(off,R.to.y,1-(1-u)*(1-u));R.scale=targetScale;}
 C35.lastFlight={phase:R.t<exit?'north-exit':'south-entry',scale:R.scale,y:b.y};
 return R.t>=exit+enter;
}
// Correct only saturated violet armor in the gun plates. Preserve highlights,
// alpha, native hit-white plates, blue ordnance and dark metal shading.
XART.get=function(key){const im=C35.get.apply(this,arguments);if(!im||typeof key!=='string'||! /^(ha21_blue_to_ball|ch23_(body|hands)|c29_(stun|recall)|c25_empty|bi24_chronos_)/.test(key)||key.includes('_hit')||key.includes('_red'))return im;
 if(!C35.cache.has(key)){const c=document.createElement('canvas');c.width=im.width;c.height=im.height;const g=c.getContext('2d');g.drawImage(im,0,0);const d=g.getImageData(0,0,c.width,c.height),p=d.data;
  for(let i=0;i<p.length;i+=4){const r=p[i],v=p[i+1],b=p[i+2];if(p[i+3]&&b>v*1.25&&r>v*1.3&&b>45&&r>b*.4){p[i]=Math.min(r,Math.round(b*.16));p[i+1]=Math.max(v,Math.round(b*.54));}}
  g.putImageData(d,0,0);C35.cache.set(key,c);
 }return C35.cache.get(key);
};
// The original authored cylindrical energy hammer has eight complete flight
// views and measured head sockets. Detached flight alone uses this sheet.
function c35Tool(at,angle,flash=0,scale=1){
 const key='arch_hammer_flight_0926';if(!XART.rdy(key))return false;
 const f=((Math.round(angle/TAU*8)%8)+8)%8,p=HAMMER_FLIGHT_HEADS[f],x=f%4*384,y=Math.floor(f/4)*512,k=.72*scale;
 const im=XART.get(key);ctx.save();ctx.translate(at.x,at.y);ctx.imageSmoothingEnabled=false;
 ctx.drawImage(im,x,y,384,512,(x-p[0])*k,(y-p[1])*k,384*k,512*k);
 if(flash>0){const id='tool-white';if(!C35.cache.has(id)){const c=document.createElement('canvas');c.width=im.width;c.height=im.height;const g=c.getContext('2d');g.drawImage(im,0,0);g.globalCompositeOperation='source-in';g.fillStyle='white';g.fillRect(0,0,c.width,c.height);C35.cache.set(id,c);}ctx.drawImage(C35.cache.get(id),x,y,384,512,(x-p[0])*k,(y-p[1])*k,384*k,512*k);}
 ctx.restore();C35.lastTool={frame:f,x:at.x,y:at.y,scale:k};return true;
}
hf22Tool=function(b,at,angle){return c25Own(b)?c35Tool(at,angle,Math.max(b.flash||0,b._lastPart?.flash||0)):C35.tool.apply(this,arguments);};
function c35Catch(b){const q=h22Blue(b,0);return {at:hb20World(q.a,q.a.tip,b,q.k,0),angle:5*Math.PI/4,scale:.687/.72};}
hammerFlightDraw=function(T,alpha){if(c25Own(boss)){
 if(alpha!=null&&alpha!==1)return false;
 const target=c35Catch(boss),u=T.phase==='return'?1-clamp(Math.hypot(T.x-target.at.x,T.y-target.at.y)/150,0,1):0;
 const turn=Math.atan2(Math.sin(target.angle-T.angle),Math.cos(target.angle-T.angle));
 return c35Tool(T,T.angle+turn*u,Math.max(boss.flash||0,boss._lastPart?.flash||0),lerp(1,target.scale,u));
 }return C35.flight.apply(this,arguments);};
c29Tool=function(b,from,to,u,scale=1,angle=0){const e=u*u*(3-2*u);return c35Tool({x:lerp(from.x,to.x,e),y:lerp(from.y,to.y,e)},angle,0,scale);};
window.BOF_CHRONOS_FLIGHT=C35;
