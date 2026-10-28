"use strict";
/* On-hull laser batteries -> every module down -> exposed burning hull.
   Native carrier fall, detonation and Nightwing handoff remain the exit. */
const HC32={drawing:null,cells:new Map(),events:[],last:null,base:{init:warhiveInit,sync:roster17Sync,budget:roster17Budget,at:roster17At,damage:warhiveDamage,targets:warhiveRetinaTargets,die:bossDie,tick:warhiveTick,draw:roster17Draw,overlay:s6r18CarrierOverlay,get:XART.get,fan:s6r18FanDraw,load:stageLoadBegin}};
for(const a of Object.values(HC32_ART.banks))XART._src[a.key]=a.path;
function hc32Own(b){return run.stage===6&&!run._gp4StageX&&!!(b?._carrier17||b?._s6CarrierFall);}
function hc32State(b){return b._hc32||(b._hc32={coreMax:Math.ceil(b._carrier17.parts.reduce((n,p)=>n+p.maxhp,0)*HC32_ART.hullRatio),core:0,initialized:false,exposed:false,t:0,flash:0,next:0,n:0,final:false});}
function hc32Log(b,event,data={}){HC32.events.push({event,time:b.t,...data});if(HC32.events.length>160)HC32.events.shift();}
function hc32Cell(name,f){const a=HC32_ART.banks[name];if(!a||!XART.rdy(a.key))return null;const id=name+':'+f;if(HC32.cells.has(id))return HC32.cells.get(id);
 const c=document.createElement('canvas');c.width=a.cw;c.height=a.ch;c.getContext('2d').drawImage(HC32.base.get.call(XART,a.key),f%a.cols*a.cw,Math.floor(f/a.cols)*a.ch,a.cw,a.ch,0,0,a.cw,a.ch);HC32.cells.set(id,c);return c;}
function hc32Warm(){let ready=true;for(const a of Object.values(HC32_ART.banks))ready=XART.rdy(a.key)&&ready;if(ready)for(const name of['closed','open'])for(let f=0;f<17;f++)hc32Cell(name,f);return ready;}
stageLoadBegin=function(n,keys){return HC32.base.load.call(this,n,n===6?[...(keys||[]),...Object.values(HC32_ART.banks).map(a=>a.key)]:keys);};
warhiveInit=function(b){const result=HC32.base.init.apply(this,arguments);if(hc32Own(b)&&b._carrier17)for(const mount of HC32_ART.laserMounts){const p=b._carrier17.parts.find(p=>p.id===mount.id);if(p){p.dx=mount.dx;p.dy=mount.dy;}}return result;};
roster17Sync=function(b){const result=HC32.base.sync.apply(this,arguments);if(!hc32Own(b)||!b._carrier17)return result;const C=b._carrier17,S=hc32State(b);if(!S.initialized){S.core=S.coreMax;S.initialized=true;}
 b.hp+=S.core;b.maxhp=C.parts.reduce((n,p)=>n+p.maxhp,0)+S.coreMax;return result;};
roster17Budget=function(b){const result=HC32.base.budget.apply(this,arguments);if(hc32Own(b)&&b._carrier17)roster17Sync(b);return result;};
function hc32HullAt(b,x,y){if(!roster17Ready(b)||!b._hc32?.exposed)return false;const W=b._whv,k=WHV_S*roster17HullScale(b),sx=Math.floor((x-W.cx)/k+256),sy=Math.floor((y-W.cy-(W.dy||0))/k+144),rows=HC32_ART.masks[W.doorOpen?'open':'closed'];
 return sx>=0&&sx<512&&sy>=0&&sy<288&&rows[sy].some(([l,r])=>sx>=l&&sx<r);}
roster17At=function(b,x,y){if(!hc32Own(b)||!b._carrier17)return HC32.base.at.apply(this,arguments);if(b._hc32?.exposed)return hc32HullAt(b,x,y)?'hull':null;
 const id=HC32.base.at.apply(this,arguments);return id==='armor'?null:id;};
warhiveRetinaTargets=function(b,out){if(!hc32Own(b)||!b._carrier17||!b._hc32?.exposed)return HC32.base.targets.apply(this,arguments);if(!roster17Ready(b))return;
 const S=b._hc32;out.push(retinaDynamicPiece(b,'harrier hull','hull',()=>({x:b.x,y:b.y,hp:S.core,dead:b.dead||S.core<=0||!roster17Ready(b)}),d=>{if(b._carrier17){b._carrier17.direct='hull';hitBoss(d);}},b.w*.9,b.h*.85));};
function hc32Open(b){const C=b._carrier17,S=hc32State(b),W=b._whv;if(S.exposed)return;S.exposed=true;S.t=0;S.next=.12;S.n=0;C.depth=false;C.scale=1;C.phase='fight';C.t=0;C.bayOpen=false;b._noHit=false;W.doorOpen=false;
 const B=s6r18State(b).bay;B.mode='cool';B.open=0;for(const p of C.parts){p.phase='dead';delete p.aim;delete p.lanes;}roster17Sync(b);showCallout('shoot',1.6);Audio.SFX.expBig?.();s6WingSay('DECKER','ALL GUNS AND PROPELLERS DOWN! HULL EXPOSED. FINISH IT!');hc32Log(b,'hull-exposed',{core:S.core,max:b.maxhp});}
bossDie=function(){const b=boss;if(hc32Own(b)&&b._carrier17){const S=hc32State(b);if(b._carrier17.parts.some(p=>!p.dead)){roster17Sync(b);return;}if(S.core>0){hc32Open(b);return;}if(!S.final){S.final=true;hc32Log(b,'hull-destroyed');}}
 return HC32.base.die.apply(this,arguments);};
warhiveDamage=function(b,dmg){if(!hc32Own(b)||!b._carrier17)return HC32.base.damage.apply(this,arguments);const C=b._carrier17,S=hc32State(b);
 if(!S.exposed){if(['hull','armor'].includes(C.direct)||['hull','armor'].includes(C.hit)){C.direct=C.hit=null;return 0;}return HC32.base.damage.apply(this,arguments);}
 if(!roster17Ready(b)||!(dmg>0)||S.core<=0)return 0;const id=C.direct??C.hit;C.direct=C.hit=null;if(id&&id!=='hull')return 0;
 const shot=_dmgBullet;let accepted=id==='hull';
 if(!accepted&&Number.isFinite(_lastHitX)&&Number.isFinite(_lastHitY))accepted=hc32HullAt(b,_lastHitX,_lastHitY);
 if(!accepted&&shot){if(shot.kind==='beam'||shot.kind==='flame'){
  if(shot.kind==='flame')accepted=flameHit(shot,b.x,b.y,b.w*.6,b.h*.85);
  else for(let y=Math.max(shot.top,b.y-b.h/2);y<=Math.min(shot.bot,b.y+b.h/2)&&!accepted;y+=8)accepted=hc32HullAt(b,shot.x,y);
 }else if(Number.isFinite(shot.x+shot.y))accepted=hc32HullAt(b,shot.x,shot.y);}
 if(!accepted)return 0;const actual=Math.min(S.core,dmg);S.core-=actual;markHit(b);S.flash=Math.max(S.flash,b.flash||0);weaponHitSfx('normal');if(typeof stageStats!=='undefined')stageStats.dmgDealt+=actual;roster17Sync(b);if(S.core<=0)bossDie();return 0;};
function hc32Cook(b,dt){const S=b._hc32;if(!S?.exposed)return;S.t+=dt;S.flash=Math.max(0,S.flash-dt);if(S.t>8||S.t<S.next)return;S.next+=.34;const anchors=[[0,-118],[220,0],[-220,0],[0,120],[-105,-45],[105,-45],[-65,63],[65,63]],q=anchors[S.n++%anchors.length],W=b._whv,k=WHV_S*roster17HullScale(b);
 const x=W.cx+q[0]*k,y=W.cy+(W.dy||0)+q[1]*k;explode(x,y,50+(S.n%3)*16,'red',null,S.n%2?'nxp_dense':'nxp_barrage',null,.45,true);hc32Log(b,'hull-cookoff',{x,y,edge:(S.n-1)%8});}
warhiveTick=function(b,dt){if(hc32Own(b)&&b._carrier17&&b._hc32?.exposed){const C=b._carrier17,W=b._whv;dt=clamp(dt,0,.05);b.t+=dt;b.flash=Math.max(0,b.flash-dt);C.age+=dt;C.t+=dt;
 b.x=camLeftX()+viewW()/2+Math.sin(C.age*.36)*8;b.y=roster17Home(b)+Math.sin(C.age*.55)*10;s6r18FanTick(b,C,dt);roster17FlashTick(C,dt);roster17Sync(b);hc32Cook(b,dt);return;}
 const result=HC32.base.tick.apply(this,arguments);if(hc32Own(b)&&b._s6CarrierFall)hc32Cook(b,clamp(dt,0,.05));return result;};
XART.get=function(key){const b=HC32.drawing,S=b?._hc32,name=HC32_ART.aliases[key];if(name&&S?.exposed){const f=S.flash>0?16:S.t<2.4?Math.min(11,Math.floor(S.t/.2)):12+Math.floor(S.t*8)%4,c=hc32Cell(name,f);if(c){HC32.last={key,name,frame:f,exposed:S.exposed};return c;}}return HC32.base.get.apply(this,arguments);};
roster17Draw=function(b){const old=HC32.drawing;if(hc32Own(b))HC32.drawing=b;try{return HC32.base.draw.apply(this,arguments);}finally{HC32.drawing=old;}};
s6r18CarrierOverlay=function(b){const old=HC32.drawing;if(hc32Own(b))HC32.drawing=b;try{return HC32.base.overlay.apply(this,arguments);}finally{HC32.drawing=old;}};
s6r18FanDraw=function(b,C){const result=HC32.base.fan.apply(this,arguments);if(!hc32Own(b)||!b._hc32?.exposed)return result;const a=HC32_ART.banks.smoke;if(!XART.rdy(a.key))return result;
 const S=b._hc32,W=b._whv,anchors=[[-75,-67],[75,-67],[-122,-12],[122,-12],[-52,54],[52,54],[0,100],[0,-110]];
 for(let i=0;i<anchors.length;i++){if(S.t<i*.13)continue;const q=anchors[i],x=W.cx+q[0]*WHV_S,y=W.cy+(W.dy||0)+q[1]*WHV_S,f=(Math.floor(S.t*12)+i*3)%8;ctx.drawImage(XART.get(a.key),f*a.cw,0,a.cw,a.ch,Math.round(x-32),Math.round(y-72),a.cw,a.ch);}
 return result;};
globalThis.BOF_CARRIER_HULL_1028=HC32;
