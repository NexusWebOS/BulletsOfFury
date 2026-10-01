"use strict";
/* Portable 72-heading sprite contract. Authored roll/pitch reels stay separate.
   All atlas frames use a stable center, clockwise degrees and untrimmed bounds.
   Exporter writes the same cells to disk for engines without Canvas transforms. */
const ROT5={step:5,count:72,budget:48*1024*1024,bytes:0,serial:0,depth:0,busy:false,
  ids:new WeakMap(),names:new WeakMap(),cache:new Map(),seen:new Map(),fallbacks:0,draws:0};
const ROT5_GET=XART.get.bind(XART),ROT5_RAW=ctx.drawImage.bind(ctx);
XART.get=function(k){const im=ROT5_GET(k);if(im&&typeof im==='object')ROT5.names.set(im,k);return im;};
function rot5Index(angle){return ((Math.round(angle/(Math.PI/36))%72)+72)%72;}
function rot5Source(im,rect,w,h,flip){
 if(!im||!(im.naturalWidth||im.width))return null;
 const iw=im.naturalWidth||im.width,ih=im.naturalHeight||im.height,r=rect||[0,0,iw,ih];
 let id=ROT5.ids.get(im);if(!id){id=++ROT5.serial;ROT5.ids.set(im,id);}
 const ratio=Math.round(w/h*1000)/1000,key=id+':'+r.join(',')+':'+ratio+':'+(flip||0);
 let q=ROT5.cache.get(key);if(q){ROT5.cache.delete(key);ROT5.cache.set(key,q);return q;}
 const max=Math.min(384,Math.max(r[2],r[3])),bh=Math.max(2,Math.round(max/Math.max(1,ratio))),bw=Math.max(2,Math.round(bh*ratio));
 const c=document.createElement('canvas');c.width=bw;c.height=bh;const g=c.getContext('2d');g.imageSmoothingEnabled=false;
 if(flip){g.translate(flip&1?bw:0,flip&2?bh:0);g.scale(flip&1?-1:1,flip&2?-1:1);}
 g.drawImage(im,...r,0,0,bw,bh);
 const side=Math.ceil(Math.hypot(bw,bh))+6;
 q={key,source:c,bw,bh,side,frames:new Map(),bytes:bw*bh*4,name:ROT5.names.get(im)||im._key||im.src||'canvas',rect:r};
 ROT5.cache.set(key,q);ROT5.bytes+=q.bytes;return q;
}
function rot5Frame(q,index){
 index=((index|0)%72+72)%72;if(q.frames.has(index)){const f=q.frames.get(index);q.frames.delete(index);q.frames.set(index,f);return f;}
 const c=document.createElement('canvas');c.width=c.height=q.side;c.naturalWidth=c.naturalHeight=q.side;
 const g=c.getContext('2d');g.imageSmoothingEnabled=false;g.translate(q.side/2,q.side/2);g.rotate(index*Math.PI/36);g.drawImage(q.source,-q.bw/2,-q.bh/2);
 q.frames.set(index,c);q.bytes+=q.side*q.side*4;ROT5.bytes+=q.side*q.side*4;
 while(ROT5.bytes>ROT5.budget&&ROT5.cache.size>1){const [id,old]=ROT5.cache.entries().next().value;if(old===q){ROT5.cache.delete(id);ROT5.cache.set(id,old);continue;}ROT5.cache.delete(id);ROT5.bytes-=old.bytes;}
 while(ROT5.bytes>ROT5.budget&&q.frames.size>1){const oldest=q.frames.keys().next().value;q.frames.delete(oldest);const bytes=q.side*q.side*4;q.bytes-=bytes;ROT5.bytes-=bytes;}
 return c;
}
function rot5Draw(key,x,y,w,h,angle,alpha){
 if(!XART.rdy(key))return false;const im=XART.get(key),q=rot5Source(im,null,w,h,0);if(!q)return false;
 const f=rot5Frame(q,rot5Index(angle||0)),s=w/q.bw;
 ctx.save();ctx.globalAlpha*=alpha==null?1:alpha;ROT5.busy=true;
 try{ROT5_RAW(f,x-f.width*s/2,y-f.height*s/2,f.width*s,f.height*s);}finally{ROT5.busy=false;ctx.restore();}return true;
}
ctx.drawImage=function(im,...v){
 if(!ROT5.depth||ROT5.busy||!im)return ROT5_RAW(im,...v);
 if(v.length===2)v.push(im.naturalWidth||im.width,im.naturalHeight||im.height);
 const m=ctx.getTransform(),sx=Math.hypot(m.a,m.b),det=m.a*m.d-m.b*m.c,sy=det/(sx||1),angle=Math.atan2(m.b,m.a);
 if(Math.abs(angle)<.00001)return ROT5_RAW(im,...v);
 if(sx<.001||Math.abs(sy)<.001||Math.abs(m.a*m.c+m.b*m.d)>.002*sx*Math.abs(sy)){ROT5.fallbacks++;return ROT5_RAW(im,...v);}
 let r=null,dx,dy,dw,dh;if(v.length===8){r=v.slice(0,4);[dx,dy,dw,dh]=v.slice(4);}else [dx,dy,dw,dh]=v;
 if(!(dw&&dh))return;const w=Math.abs(dw),h=Math.abs(dh*sy/sx),flip=(dw<0?1:0)^((dh*sy<0)?2:0),q=rot5Source(im,r,w,h,flip);if(!q)return ROT5_RAW(im,...v);
 const index=rot5Index(angle),f=rot5Frame(q,index),sc=w/q.bw,cx=dx+dw/2,cy=dy+dh/2;
 ROT5.draws++;const name=q.name+'|'+q.rect.join(',')+'|'+q.bw+'x'+q.bh;
 if(!ROT5.seen.has(name))ROT5.seen.set(name,{key:q.name,rect:q.rect,w:q.bw,h:q.bh,pivot:[.5,.5],step:5,count:72});
 ctx.save();ctx.setTransform(sx,0,0,sx,m.a*cx+m.c*cy+m.e,m.b*cx+m.d*cy+m.f);ctx.imageSmoothingEnabled=false;
 ROT5_RAW(f,-f.width*sc/2,-f.height*sc/2,f.width*sc,f.height*sc);ctx.restore();
};
function rot5Scope(fn){return function(){ROT5.depth++;try{return fn.apply(this,arguments);}finally{ROT5.depth--;}};}
for(const name of ['drawEnemy','drawBoss','drawBossSprite','drawModularBoss','shipBossDraw','drawSubBoss','drawShipSprite','drawRivalShip','furyShipDrawFlight','s6WingDraw','allyDraw'])
 if(typeof window[name]==='function')window[name]=rot5Scope(window[name]);
/* Steering uses the approved neutral hull through ±15 degrees. Full roll/pitch
   are deliberate actions only; they must never be selected by a held direction. */
const ROT5_SHIP_KEY=_shipFrameKey,ROT5_PLAYER=_drawPlayerCore;
_shipFrameKey=function(pk){return !spaceShipActive()&&!player.roll&&!player.somer?'ship_'+pk:ROT5_SHIP_KEY(pk);};
_drawPlayerCore=function(){
 const steer=!spaceShipActive()&&!player.dead&&!player.roll&&!player.somer;
 const a=steer?Math.round(clamp(player._bank||0,-1,1)*3)*Math.PI/36:0;
 ROT5.depth++;ctx.save();if(a){ctx.translate(player.x,player.y);ctx.rotate(a);ctx.translate(-player.x,-player.y);}
 try{return ROT5_PLAYER.apply(this,arguments);}finally{ctx.restore();ROT5.depth--;}
};
