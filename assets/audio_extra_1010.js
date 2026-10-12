"use strict";
/* Stolen overdrive, acted assembly and four authored homecoming cutaways. */
const AP10_EXTRA={load:stageLoadBegin,demo:rs1004DemoDraw,demoTick:rs1004DemoTick,ball:rs1004Ball,
 phase:furyShipDrawPhase,part:furyPartPose,ending:victoryRestoration,draws:{}};
for(const bank of Object.values(AP10_EXTRA_ART))for(const a of bank)XART._src[a.key]=a.path;
stageLoadBegin=function(n,keys){return AP10_EXTRA.load.call(this,n,[...(keys||[]),...(n>=5?Object.values(AP10_EXTRA_ART).flat().map(a=>a.key):[])]);};
function ap10ExtraCell(name,f,x,y,w,rot=0){const bank=AP10_EXTRA_ART[name],a=bank[clamp(f|0,0,bank.length-1)];
 if(!XART.rdy(a.key))return false;const k=w/a.w;ctx.save();ctx.imageSmoothingEnabled=false;ctx.translate(x,y);ctx.rotate(rot);
 ctx.drawImage(XART.get(a.key),-a.pivot[0]*k,-a.pivot[1]*k,a.w*k,a.h*k);ctx.restore();
 AP10_EXTRA.draws[name]=(AP10_EXTRA.draws[name]||0)+1;return true;}
rs1004Ball=function(x,y,size,t){return AP10_EXTRA.ball.call(this,x,y,size,t);};
rs1004DemoDraw=function(R){const D=R.h3Intro?.showcase?.current,q=D?.q;
 if(q&&D.kind==='turbo'&&!D.released&&AP10_EXTRA_ART.turbo.every(a=>XART.rdy(a.key))){
  D.released=true;try{AP10_EXTRA.demo.apply(this,arguments);}finally{D.released=false;}
  const warm=Math.max(1.25,R.h3Intro.rows[R.h3Intro.i].text.length/32+.12),f=Math.min(11,Math.floor(D.t/warm*12));
  ap10ExtraCell('turbo',f,q.x,q.y,122);return;
 }
 const r=AP10_EXTRA.demo.apply(this,arguments);
 for(const f of R.h3Intro?.showcase?.fx||[])if(f.kind==='ap10-turbo-snap')
  ap10ExtraCell('turbo',12+Math.min(3,Math.floor(f.t/.20*4)),f.x,f.y,122);
 return r;};
rs1004DemoTick=function(R,I,dt){const before=new Set(I.showcase?.fx||[]),r=AP10_EXTRA.demoTick.apply(this,arguments),S=I.showcase,D=S?.current,q=D?.q;
 for(const f of S?.fx||[])if(!before.has(f)&&(f.kind==='ball'||f.kind==='slug')){f.vx=0;f.vy=f.kind==='ball'?690:660;}
 if(q&&D.kind==='turbo'&&D.released){const warm=Math.max(1.25,I.rows[I.i].text.length/32+.12),t=D.t-warm;
  if(!D.ap10Snap){D.ap10Snap=true;S.fx.push({kind:'ap10-turbo-snap',x:D.ox,y:D.oy,t:0,life:.20});}
  if(t>=1.25){const x=camRightX()+90,y=PLAY.y+110,d=Math.hypot(D.ox-x,D.oy-y),u=clamp((t-1.25)*1250/Math.max(1,d),0,1);
   q.x=lerp(x,D.ox,u);q.y=lerp(y,D.oy,u);q.rfHeading=u<1?Math.atan2(D.oy-y,D.ox-x):null;}
 }return r;};
furyPartPose=function(){const p=AP10_EXTRA.part.apply(this,arguments);if(p)p.rotation=0;return p;};
furyShipDrawPhase=function(G,x,y,size,planeH,pilot){
 // Cole's generated plate contains Cole. Other pilots retain their own authored
 // cockpit and separate mounting pieces, now without artificial whole-part spins.
 if(pilot==='cole'&&(['charge','scatter','snap','pixelglow'].includes(G.phase)||G.phase==='drift'&&G.partStartAge!=null)){
  const f=G.phase==='drift'?Math.floor(Math.max(0,(G.age||0)-G.partStartAge)*8)%4:
   G.phase==='charge'?4+Math.min(3,Math.floor(G.t/GRAVITY_CHARGE_DUR*4)):
   G.phase==='scatter'?8+Math.min(1,Math.floor(G.t/GRAVITY_SCATTER_DUR*2)):
   G.phase==='snap'?10+Math.min(3,Math.floor(G.t/GRAVITY_SNAP_DUR*4)):14+Math.min(1,Math.floor(G.t/GRAVITY_PIXEL_DUR*2));
  // The 352px cell includes incoming hardware. Its original aircraft is 192px
  // high: match that aircraft to the launch hull, then tuck only during snap.
  const aircraftH=gravityPlaneH(planeH,size,G.phase,G.t);
  if(ap10ExtraCell('assembly',f,x,y,AP10_EXTRA_ART.assembly[0].w*aircraftH/192))return;
 }return AP10_EXTRA.phase.apply(this,arguments);};
victoryRestoration=function(t,W,H,pk){
 const f=Math.min(3,Math.floor(t/(VICTORY_DISH_AT/4))),a=AP10_EXTRA_ART.ending[f];
 if(!XART.rdy(a.key))return AP10_EXTRA.ending.apply(this,arguments);
 const im=XART.get(a.key),k=Math.max(W/a.w,H/a.h);ctx.save();ctx.imageSmoothingEnabled=false;
 ctx.drawImage(im,(W-a.w*k)/2,(H-a.h*k)/2,a.w*k,a.h*k);ctx.restore();
 const lines=['FURY FLIGHT, CAN ANYONE HEAR ME?','WE HAVE YOU. HOLD THAT CHANNEL. WE ARE BRINGING YOU HOME.',
  'FURY HQ IN SIGHT. IT IS GOOD TO BE HOME.','WELCOME HOME. EVERY SURVIVING PILOT IS WITH YOU.'];
 victoryCaption(f%2?'FURY FLIGHT':pk.toUpperCase(),lines[f],W,H,1);
 AP10_EXTRA.draws.ending=(AP10_EXTRA.draws.ending||0)+1;
};
