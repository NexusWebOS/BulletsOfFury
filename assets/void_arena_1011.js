"use strict";
/* Mike: Phase 3 is an open alien hell void, with no walls or sides. All light
   comes from authored atmosphere/code. This layer owns no combat geometry. */
const AV11={base:{load:stageLoadBegin,warm:aa5Warm,encounter:j3Encounter,tick:r30Tick},
 draws:{back:0,near:0,code:0},last:null,
 nodes:[
  {x:.13,y:.18,depth:.10,size:160,speed:4,phase:0},
  {x:.53,y:.78,depth:.10,size:140,speed:-3,phase:5},
  {x:.86,y:.43,depth:.10,size:155,speed:4,phase:11},
  {x:.33,y:.39,depth:.23,size:210,speed:-7,phase:8},
  {x:.74,y:.94,depth:.23,size:196,speed:6,phase:3},
  {x:.06,y:.87,depth:.38,size:242,speed:10,phase:13}
 ]};
for(const bank of Object.values(AV11_ART))for(const a of bank)XART._src[a.key]=a.path;
function av11Warm(){for(const bank of Object.values(AV11_ART))for(const a of bank)XART.rdy(a.key);}
aa5Warm=function(){const r=AV11.base.warm.apply(this,arguments);av11Warm();return r;};
stageLoadBegin=function(n,keys){return AV11.base.load.call(this,n,
 n===8?[...(keys||[]),...Object.values(AV11_ART).flat().map(a=>a.key)]:keys);};
j3Encounter=function(b,n){const previous=j3State(b)?.encounter,r=AV11.base.encounter.apply(this,arguments),J=j3State(b);
 if(J){if(n!==2)J.av11=null;else if(previous!==2||!J.av11)J.av11={t:0,combat:0};}
 return r;};
r30Tick=function(b,dt){const J=j3State(b);
 if(aa5Arena(b)){
  const Q=J.av11??={t:0,combat:0},step=clamp(dt||0,0,.05);
  Q.t+=step;if(b._r30.mode==='fight')Q.combat+=step;
 }
 return AV11.base.tick.apply(this,arguments);};
function av11Plate(name,f,x,y,size,alpha=1,rot=0){
 const bank=AV11_ART[name],a=bank[((f|0)%bank.length+bank.length)%bank.length];
 if(alpha<=0||!XART.rdy(a.key))return false;
 const im=XART.get(a.key);if(!im)return false;
 const k=size/a.w;
 ctx.save();ctx.globalAlpha*=alpha;ctx.translate(x,y);ctx.rotate(rot);ctx.imageSmoothingEnabled=false;
 ctx.drawImage(im,-a.pivot[0]*k,-a.pivot[1]*k,a.w*k,a.h*k);ctx.restore();return true;
}
function av11ArenaDraw(b){
 if(!aa5Arena(b))return false;
 const J=j3State(b),S=b._r30,Q=J.av11||{t:0,combat:0},t=Q.t;
 const fade=S.mode==='voidIntro1005'?clamp((S.t-1.4)/1.6,0,1):1;
 const left=camLeftX(),top=viewTopY(),w=viewW(),h=viewH(),world=worldWidth(),mid=world/2;
 const cam=left-(world-w)/2,awake=clamp(Q.combat/4,0,1),a=AV11_ART.back[0];
 // Cover the entire visible band, including camera shake margins. One common
 // scale preserves the plate's proportions at both fit and scrolling zoom.
 const cover=Math.max((world+120)/a.w,(h+120)/a.h),size=a.w*cover;
 const dx=Math.sin(t*.11)*10+cam*.08,dy=Math.cos(t*.09)*8;
 const P=S.attack,release=P?Math.max(0,1-Math.abs(P.t-P.tell)/.6):0;
 const power=.22+.78*awake,points=[];
 ctx.save();ctx.beginPath();ctx.rect(left-16,top-16,w+32,h+32);ctx.clip();ctx.globalAlpha*=fade;
 // Opaque clear also serves as a dark fallback while local art decodes. The
 // retired cathedral/ribs are never used as the fallback for this arena.
 ctx.fillStyle='#000';ctx.fillRect(left-16,top-16,w+32,h+32);
 if(av11Plate('back',0,mid+dx,top+h/2+dy,size,.88))AV11.draws.back++;
 ctx.save();ctx.globalCompositeOperation='screen';
 if(av11Plate('back',0,mid-cam*.12+Math.sin(t*.17)*24,top+h/2+Math.cos(t*.14)*17,
   size*1.36,.18+awake*.06,Math.sin(t*.045)*.025))AV11.draws.near++;
 ctx.restore();
 for(const n of AV11.nodes){
  const span=h+n.size*2,travel=((n.y*h+t*n.speed+n.size)%span+span)%span;
  const x=world*n.x+cam*n.depth+Math.sin(t*.19+n.phase)*9;
  const y=top+travel-n.size,frame=(Math.floor(t*16)+n.phase)%16;
  const breath=.76+.24*Math.sin(t*.8+n.phase),alpha=(.12+n.depth*.52)*power*breath+release*.035;
  if(av11Plate('code',frame,x,y,n.size,alpha))AV11.draws.code++;
  points.push({x,y,size:n.size,depth:n.depth,frame,alpha});
 }
 ctx.restore();J.aa5ArenaDrawn=true;
 AV11.last={t,combat:Q.combat,awake,fade,cover,size,left,top,w,h,dx,dy,points};
 return true;
}
// The existing drawBG chain already places this call below bosses, projectiles,
// warnings and HUD. Change the environment without another world draw wrapper.
aa5ArenaDraw=av11ArenaDraw;
