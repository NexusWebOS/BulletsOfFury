'use strict';
const C44={blue:ha21Blue,body:ha21Body,get:XART.get,rdy:XART.rdy,beam:hammerChromiumDraw,hit:c41Hit,cache:new Map()};
// Every rage wave keeps the authored hip gather and two-handed thrust.
c42Active=function(){return false;};
function c44BluePose(q){return {...q,a:{...q.a,key:'c44_'+q.a.key},kind:'c44_blue_wave'};}
XART.rdy=function(key){return key.startsWith('c44_')?C44.rdy.call(this,key.slice(4)):C44.rdy.apply(this,arguments);};
XART.get=function(key){if(!key.startsWith('c44_'))return C44.get.apply(this,arguments);if(C44.cache.has(key))return C44.cache.get(key);const im=C44.get.call(this,key.slice(4));if(!im)return im;const c=document.createElement('canvas');c.width=im.width;c.height=im.height;const g=c.getContext('2d');g.drawImage(im,0,0);const d=g.getImageData(0,0,c.width,c.height);for(let i=0;i<d.data.length;i+=4){const r=d.data[i],b=d.data[i+2];if(r>d.data[i+1]*1.25&&r>b*1.25){const z=.299*r+.587*d.data[i+1]+.114*b;d.data[i]=z*.90;d.data[i+1]=z*.98;d.data[i+2]=Math.min(255,z*1.08);}}g.putImageData(d,0,0);C44.cache.set(key,c);return c;};
ha21Blue=function(b){if(c25Own(b)&&['mega_charge','mega_beam'].includes(b._hammer.state)){const h=b._hammer;return c44BluePose(h.state==='mega_beam'?c30Pose('cast',5+(Math.floor(h.t*14)&1)):h.t<1.29?c30Pose('cast',Math.min(3,h.t/1.29*3)):c30Pose('thrust',(h.t-1.29)/.36*8));}return C44.blue.apply(this,arguments);};
function c44Muzzle(b){return hb20World(c30Row('cast',5),[128,110],b,1,0);}
hammerChromiumDraw=function(x,y,endY,width,t,dur){if(c25Own(boss)&&boss._hammer.state==='mega_beam')return c41Draw(c44Muzzle(boss),{x:boss.x,y:endY},t,dur,false);return C44.beam.apply(this,arguments);};
c41Hit=function(from,to,t,dur,p){if(c25Own(boss)&&boss._hammer.state==='mega_beam')from=c44Muzzle(boss);return C44.hit.call(this,from,to,t,dur,p);};
ha21Body=function(b,q){const C=b?._hammer?._hf22Charge,u=C?cgChargeU(b):0;if(!c25Own(b)||!C||u<.30)return C44.body.apply(this,arguments);
 const f=clamp((u-.30)/.62,0,1)*(C29_ART.banks.rage_regular.length-1),a=c29Pose('rage',f,'regular').a,r=c29Pose('rage',f,'red').a,step=Math.round(clamp((u-.38)/.54,0,1)*24),key='fade:'+a.key+':'+step;
 if(!XART.rdy(a.key)||!XART.rdy(r.key))return C44.body.apply(this,arguments);
 let c=C44.cache.get(key);if(!c){const im=XART.get(a.key),red=XART.get(r.key);c=document.createElement('canvas');c.width=im.width;c.height=im.height;const g=c.getContext('2d');g.drawImage(im,0,0);const d=g.getImageData(0,0,c.width,c.height);g.clearRect(0,0,c.width,c.height);g.drawImage(red,0,0);const rd=g.getImageData(0,0,c.width,c.height);for(let i=0;i<d.data.length;i+=4)for(let j=0;j<3;j++)d.data[i+j]=Math.round(lerp(d.data[i+j],rd.data[i+j],step/24));g.putImageData(d,0,0);C44.cache.set(key,c);}
 ctx.drawImage(c,b.x-a.pivot[0],b.y-a.pivot[1]);C44.lastFade={step,u};};
window.BOF_CHRONOS_KAME=C44;
