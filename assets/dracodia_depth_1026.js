'use strict';
/* Mike Oct26: accelerating depth loops stay incomplete until peak whiteout.
   Native rebirth owns all24 audible beats; distant strikes are visual partners. */
const RD26={base:{pose:rd25Pose,body:rd25Body,clip:rd25Clip,lightning:rd25Lightning,load:stageLoadBegin},last:null,fx:null};
for(const a of [RD26_ART.body,RD26_ART.wire])XART._src[a.key]=a.path;
function rd26Ready(){return [RD26_ART.body,RD26_ART.wire].map(a=>XART.rdy(a.key)).every(Boolean);}
stageLoadBegin=function(n,keys){return RD26.base.load.call(this,n,[...(keys||[]),...(n===8?[RD26_ART.body.key,RD26_ART.wire.key]:[])]);};
rd25Pose=function(b,t=b._r30.t){
 const Q=RD26.base.pose.apply(this,arguments);if(!rd26Ready())return Q;
 const elapsed=Math.max(0,t-14),rotationRate=20/24+.15*elapsed,
  rotationTurns=14*20/24+20/24*elapsed+.075*elapsed*elapsed,yaw=((rotationTurns%1)+1)%1,
  fullForm=t>=25.6,materialProgress=fullForm?1:Math.min(Q.progress,.86);
 return{...Q,angle:0,body:{x:Q.x-Q.dx,y:Q.y-Q.dy},depth:true,yaw:yaw*TAU,depthFrame:Math.floor(yaw*RD26_ART.frames)%RD26_ART.frames,
  frame:Math.floor(yaw*24+1e-9)%24,nativeBlend:fullForm?1:0,fullForm,materialProgress,rotationTurns,rotationRate,extent:RD26_ART.w};
};
rd25Clip=function(Q,finished,draw,scan=false){if(!Q.depth)return RD26.base.clip.apply(this,arguments);
 ctx.save();ctx.beginPath();let count=0;const w=RD26_ART.w,h=RD26_ART.h,p=RD26_ART.pivot,progress=Q.materialProgress;
 for(let y=0;y<h;y+=4){const order=((y/4)*.61803398875)%1,complete=order<=progress;
  if(scan?complete&&progress<1&&Math.abs(order-progress)<.075:complete===finished){ctx.rect(-p[0]*Q.k,(y-p[1])*Q.k,w*Q.k,4*Q.k+.01);count++;}}
 ctx.clip();if(count)draw();ctx.restore();return count;
};
function rd26Helix(Q){const points=[],count=32,phase=(Q.t-23)*8.5;
 for(let i=0;i<=count;i++){const u=i/count,theta=u*TAU*2-phase,r=Q.size*.39*(.62+.38*Math.sin(u*Math.PI));
  points.push({x:Q.body.x+Math.sin(theta)*r,y:Q.body.y+(u-.5)*Q.size*.72+Math.cos(theta)*12,z:Math.cos(theta)});}
 const arcs=[];for(let i=0;i<count;i++)arcs.push({from:points[i],to:points[i+1],front:(points[i].z+points[i+1].z)>=0,index:i});return arcs;
}
function rd26Swirl(Q,front){const warm=clamp((Q.t-23)/.35,0,1),fade=clamp((25.6-Q.t)/.3,0,1);if(!warm||!fade)return;
 for(const a of rd26Helix(Q))if(a.front===front){const alpha=warm*fade*(front?.80:.36)*(.72+.28*Math.sin(Q.t*10-a.index*.55));
  r25Bolt(a.from.x,a.from.y,a.to.x,a.to.y,Q.t+a.index*.11,alpha);RD26.fx[front?'front':'back'].push({...a,alpha});}
}
function rd26Plate(Q,wire=false){const a=wire?RD26_ART.wire:RD26_ART.body,c=RD26_ART.cells[Q.depthFrame],p=RD26_ART.pivot;
 ctx.drawImage(XART.get(a.key),...c,-p[0]*Q.k,-p[1]*Q.k,RD26_ART.w*Q.k,RD26_ART.h*Q.k);
}
rd25UnderEffects=function(b,Q,R){RD26.fx={t:Q.t,back:[],front:[],strikes:[]};if(Q.depth)rd26Swirl(Q,false);};
rd25OverEffects=function(b,Q,R){if(Q.depth)rd26Swirl(Q,true);};
rd25Body=function(b,Q){if(!Q.depth)return RD26.base.body.apply(this,arguments);
 const carrier=ER23_ART.banks.symbiote;
 ctx.save();ctx.translate(Q.x-Q.dx,Q.y-Q.dy);ctx.imageSmoothingEnabled=false;
 if(Q.fullForm){ce20Body(b._r30.clock,0,0,Q.size);ctx.restore();
  RD26.last={frame:Q.depthFrame,yaw:Q.yaw,angle:0,blend:1,bands:128,body:Q.body,t:Q.t,fullForm:true};return 128;}
 rd25Clip(Q,false,()=>{
  ctx.save();ctx.globalAlpha=Q.progress*.40;rd26Plate(Q,true);ctx.restore();
  if(XART.rdy(carrier.key)){ctx.save();ctx.globalAlpha=1-Q.progress*.40;
   if(typeof rd27Carrier==='function')ctx.drawImage(rd27Carrier(Q),Q.dx-RD25.carrierHeart[0],Q.dy-RD25.carrierHeart[1],carrier.w,carrier.h);
   else ctx.drawImage(XART.get(carrier.key),Q.frame%carrier.cols*carrier.w,Math.floor(Q.frame/carrier.cols)*carrier.h,carrier.w,carrier.h,Q.dx-RD25.carrierHeart[0],Q.dy-RD25.carrierHeart[1],carrier.w,carrier.h);ctx.restore();}
 });
 const material=()=>rd26Plate(Q);
 const bands=rd25Clip(Q,true,()=>{ctx.save();ctx.globalAlpha=.50+.50*Q.progress;material();ctx.restore();});
 rd25Clip(Q,true,()=>{ctx.save();ctx.globalCompositeOperation='screen';ctx.globalAlpha=.50;material();ctx.restore();},true);
 ctx.restore();RD26.last={frame:Q.depthFrame,yaw:Q.yaw,angle:0,blend:0,bands,body:Q.body,t:Q.t,fullForm:false};return bands;
};
function rd26StrikeClock(t,R){const u=Math.max(0,t-23),phase=5*u+3*u*u;
 return t>=23?{beat:24+Math.floor(phase),age:phase%1,rate:5+6*u}:{beat:R.bolts,age:R.boltPhase||0,rate:null};}
rd25Lightning=function(b,Q,R){if(!Q.depth)return RD26.base.lightning.apply(this,arguments);if(Q.t<17||!R.bolts)return;
 const storm=Q.t>=23,clock=rd26StrikeClock(Q.t,R),pulse=.95*clamp(1-clock.age/.72,0,1),count=storm?2:1;
 RD26.fx.clock=clock;
 for(let i=0;i<count;i++){
  const x=camLeftX()+viewW()/2+(i?36:-28),
   from={x,y:viewTopY()-30},chest={x:x+(i?-9:9),y:viewTopY()+viewH()*.34},to={x:x+(i?7:-7),y:viewTopY()+viewH()+24};
  r25Bolt(from.x,from.y,chest.x,chest.y,Q.t+i*.17,pulse);r25Bolt(chest.x,chest.y,to.x,to.y,Q.t+.13+i*.17,pulse*.90);
  RD26.fx?.strikes.push({kind:'core',from,chest,to,beat:clock.beat,alpha:pulse});
 }
 rd26AmbientLightning(Q,R,pulse,storm);
};
function rd26AmbientLightning(Q,R,pulse,storm){
 const beat=rd26StrikeClock(Q.t,R).beat,ambientCount=storm?3:Q.t>=21?2:1,lanes=[0,7,3,8,1,5,2,6,4],
  top=viewTopY()-30,bottom=viewTopY()+viewH()+24;
 for(let i=0;i<ambientCount;i++){
  const lane=lanes[(beat+i*3)%9],x=camLeftX()+viewW()*(.06+lane*.11),jitter=(beat*17+i*13)%29-14,
   from={x:x+jitter,y:top},chest={x:x-jitter,y:lerp(top,bottom,.48)},to={x:x+jitter*.5,y:bottom},
   alpha=pulse*(storm?.78:.66);
  r25Bolt(from.x,from.y,chest.x,chest.y,Q.t+i*.19+.41,alpha);r25Bolt(chest.x,chest.y,to.x,to.y,Q.t+i*.19+.61,alpha);
  RD26.fx?.strikes.push({kind:'ambient',lane,from,chest,to,beat,alpha});
 }
}
globalThis.BOF_DRACODIA_DEPTH_1026=RD26;
