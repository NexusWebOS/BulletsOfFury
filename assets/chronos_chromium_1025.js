'use strict';
// Pixel replacement on authored plates: no opacity fade or new pose generation.
const C38={get:XART.get,ready:XART.rdy,blue:ha21Blue,cache:new Map(),mix:new Map()};
function c38Chrome(im){const c=document.createElement('canvas');c.width=im.width;c.height=im.height;const g=c.getContext('2d');g.drawImage(im,0,0);const d=g.getImageData(0,0,c.width,c.height),a=d.data,src=new Uint8ClampedArray(a),w=c.width,h=c.height;
 for(let y=2;y<h-2;y++)for(let x=2;x<w-2;x++){const i=(y*w+x)*4,r=src[i],v=src[i+1],b=src[i+2],l=(r+v+b)/3;if(!src[i+3]||l<62||Math.max(r,v,b)-Math.min(r,v,b)>25)continue;
 let inside=true;for(const [dx,dy]of [[-2,0],[2,0],[0,-2],[0,2]])if(!src[((y+dy)*w+x+dx)*4+3])inside=false;if(!inside)continue;
 const z=Math.min(244,95+l*.70);a[i]=Math.round(z*.95);a[i+1]=Math.round(z*.985);a[i+2]=Math.round(z);
 }g.putImageData(d,0,0);return c;}
XART.get=function(key){if(C38.mix.has(key))return C38.mix.get(key);const im=C38.get.apply(this,arguments);if(!im||typeof key!=='string'||!/^(ha21_h22_|h22_|c27_|c29_|hf22_)/.test(key)||! /(_chrome|_armor)(_|$)/.test(key)||key.includes('_hit'))return im;
 if(!C38.cache.has(key))C38.cache.set(key,c38Chrome(im));return C38.cache.get(key);};
XART.rdy=function(key){return C38.mix.has(key)||C38.ready.apply(this,arguments);};
function c38Plate(a,z,step){const key='c38_'+a.key+'_'+step;if(C38.mix.has(key))return key;if(!XART.rdy(a.key)||!XART.rdy(z.key))return a.key;
 const im=XART.get(a.key),to=XART.get(z.key),c=document.createElement('canvas');c.width=im.width;c.height=im.height;const g=c.getContext('2d');g.drawImage(im,0,0);const d=g.getImageData(0,0,c.width,c.height);g.clearRect(0,0,c.width,c.height);g.drawImage(to,0,0);const target=g.getImageData(0,0,c.width,c.height).data;
 const bayer=[0,8,2,10,12,4,14,6,3,11,1,9,15,7,13,5],u=step/24;
 for(let y=0;y<c.height;y++)for(let x=0;x<c.width;x++){const i=(y*c.width+x)*4,threshold=.72*y/c.height+.28*(bayer[(y%4)*4+x%4]+.5)/16;if(u>=threshold){for(let n=0;n<3;n++)d.data[i+n]=target[i+n];}}
 g.putImageData(d,0,0);C38.mix.set(key,c);return key;}
ha21Blue=function(b){if(c25Own(b)&&!b.dead&&b._hammer.state==='fr_activation'&&!b._hammer._ht23ArmorGun){const h=b._hammer,q=c29Hold(b,clamp(h.t/.85,0,1),'regular'),z=c29Row('hold',q.a.frame,'chrome'),u=clamp((h.t-.65)/(C27_ARMOR.plate-.65),0,1),step=Math.floor(u*24);
 return {...q,a:{...q.a,key:c38Plate(q.a,z,step)},kind:'c38_chromium_'+step};}return C38.blue.apply(this,arguments);};
window.BOF_CHRONOS_CHROMIUM=C38;
