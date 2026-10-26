'use strict';
const C42={blue:ha21Blue,hand:c30Hand,draw:hammerBossDraw,gather:c30Gather,cache:new Map()};
for(let i=0;i<8;i++)XART._src['c42_bolt_'+i]='assets/game/shared/combat/chronos_orb_1025/bolt'+i+'.png';
const c42Load=stageLoadBegin;stageLoadBegin=function(n,keys){return c42Load.call(this,n,[...(keys||[]),...(n===5?Array.from({length:8},(_,i)=>'c42_bolt_'+i):[])]);};
function c42WavePhase(b){return c30Own(b)&&['gather','thrust','beam','recover'].includes(b._hammer.c30?.phase);}
function c42Active(b){return c42WavePhase(b)&&(b._hammer.c30.cycle||0)%6<3;}
ha21Blue=function(b){if(c42Active(b))return c30Pose('cast',5,c30Scale(b));return C42.blue.apply(this,arguments);};
c30Hand=function(b,release=false){if(c42Active(b))return hb20World(c30Row('cast',5),[130,88],b,c30Scale(b),0);return C42.hand.apply(this,arguments);};
c30Gather=function(b){if(!c42Active(b))return C42.gather.apply(this,arguments);const R=b._hammer.c30,L=c30Line(b);C25.base.warning(b,{x:L.from.x,y:L.from.y,ex:L.to.x,ey:L.to.y,width:76,progress:R.phase==='thrust'?1:clamp(R.t/1.7,0,1),fieldOnly:true});};
function c42Orb(b){if(!c42Active(b))return;const R=b._hammer.c30,a=c30Row('cast',5);if(!XART.rdy(a.key))return;
 const u=R.phase==='gather'?clamp(R.t/1.35,0,1):1,step=Math.round(u*12),key=step+':'+(Math.floor(efxClock*16)%3);
 let im=C42.cache.get(key);if(!im){im=document.createElement('canvas');im.width=im.height=28;const g=im.getContext('2d');g.drawImage(XART.get(a.key),116,74,28,28,0,0,28,28);const d=g.getImageData(0,0,28,28);
 for(let i=0;i<d.data.length;i+=4){const r=d.data[i],gg=d.data[i+1],bb=d.data[i+2];if(bb>r*1.2&&gg>r*1.1){const v=step/12;d.data[i]=r+(bb-r)*v;d.data[i+1]=gg+(r-gg)*v;d.data[i+2]=bb+(r-bb)*v;}else d.data[i+3]=0;}
 g.putImageData(d,0,0);C42.cache.set(key,im);}
 const p=c30Hand(b),k=c30Scale(b);ctx.save();ctx.imageSmoothingEnabled=false;ctx.drawImage(im,p.x-14*k,p.y-14*k,28*k,28*k);ctx.restore();C42.lastOrb={...p,charge:u,phase:R.phase};}
hammerBossDraw=function(b){const r=C42.draw.apply(this,arguments);c42Orb(b);return r;};
c33Storm=function(b){if(!c42WavePhase(b)){C33.lastDraw=null;return;}const R=b._hammer.c30,level=R.phase==='gather'?clamp(R.t/.6,0,1):R.phase==='recover'?1-clamp(R.t/.7,0,1):1;
 ctx.save();ctx.beginPath();ctx.rect(camLeftX(),viewTopY(),camRightX()-camLeftX(),viewH());ctx.clip();ctx.fillStyle='rgba(2,0,8,'+(level*.72)+')';ctx.fillRect(camLeftX(),viewTopY(),camRightX()-camLeftX(),viewH());
 let bolts=0,strike=null;
 const elapsed=R.t+({gather:0,thrust:1.7,beam:2.06,recover:3.41}[R.phase]||0),beat=Math.floor(elapsed/.38),age=elapsed-beat*.38;
 if(R.phase!=='recover'&&age<.30){const key='c42_bolt_'+Math.min(7,Math.floor(age/.30*8));if(XART.rdy(key)){
 const lanes=[.18,.76,.39,.89,.58,.09,.68,.30],x=camLeftX()+(camRightX()-camLeftX())*lanes[beat%lanes.length],height=viewH(),k=height/256,head=clamp(age/.14,0,1)*height;
 ctx.save();ctx.beginPath();ctx.rect(x-32*k,viewTopY(),64*k,head);ctx.clip();ctx.globalAlpha=level;ctx.drawImage(XART.get(key),x-32*k,viewTopY(),64*k,256*k);ctx.restore();bolts=1;strike={beat,x,head,age};}}

 ctx.restore();C33.lastDraw={phase:R.phase,level,bolts,strike,pixellab:true};};
window.BOF_CHRONOS_ORB=C42;
