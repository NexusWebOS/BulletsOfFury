'use strict';
/* Mike Oct25: the authored turning carrier downloads the actual final body.
   One chest anchor, native scale and completed plate continue into the speech. */
const RD25={base:{draw:rb23SceneDraw,tick:rb23SceneTick,load:stageLoadBegin},last:null,
 mainHeart:[159.52,157.02],carrierHeart:[78.26,140.97]};
stageLoadBegin=function(n,keys){if(n===8)Snd.prepare('combatEnergy0927');return RD25.base.load.apply(this,arguments);};
function rd25Own(b){return v18Owned(b)&&b._r30.mode==='dr5er23rebirth'&&!!b._r30.v18.rb23Rebirth;}
function rd25Ease(u){u=clamp(u,0,1);return u*u*(3-2*u);}
function rd25Hermite(a,velocity,z,u){return (2*u*u*u-3*u*u+1)*a+(u*u*u-2*u*u+u)*velocity+(-2*u*u*u+3*u*u)*z;}
function rd25Pose(b,t=b._r30.t){
 const size=v18Size(b),k=size/320,dx=(RD25.mainHeart[0]-160)*k,dy=(RD25.mainHeart[1]-160)*k,
  cx=(camLeftX()+camRightX())/2,cy=viewTopY()+viewH()*.38,u=rd25Ease((t-14)/11.2),
  from={x:cx+Math.sin(7*2)*70+RD25.carrierHeart[0]-128,y:cy+Math.cos(14*3)*16+RD25.carrierHeart[1]-128},
  to={x:camLeftX()+viewW()/2+dx,y:PLAY.y+168+Math.sin(b._r30.clock)*6+dy},
  x=lerp(from.x,to.x,u),y=lerp(from.y,to.y,u),progress=clamp((t-14)/11.2,0,1),
  a0=10.2*(1.8+10.2/11.2*2.2),end=TAU*Math.ceil((a0+2)/TAU),settle=clamp(t-24.2,0,1),
  angle=t>=25.2?0:t<24.2?(t-14)*(1.8+progress*2.2):rd25Hermite(a0,5.8,end,settle),
  turn=t<24.2?t*20:rd25Hermite(24.2*20,20,24*Math.ceil((24.2*20+12)/24),settle),frame=((Math.floor(turn)%24)+24)%24;
 return{x,y,dx,dy,size,k,progress,angle,frame,t,body:{x:x-dx*Math.cos(angle)+dy*Math.sin(angle),y:y-dx*Math.sin(angle)-dy*Math.cos(angle)}};
}
function rd25Clip(Q,finished,draw,scan=false){
 ctx.save();ctx.beginPath();let count=0;
 for(let y=0;y<320;y+=4){const order=((y/4)*.61803398875)%1,complete=order<=Q.progress;
  if(scan?complete&&Q.progress<1&&Math.abs(order-Q.progress)<.075:complete===finished){ctx.rect(-160*Q.k,(y-160)*Q.k,320*Q.k,4*Q.k+.01);count++;}}
 ctx.clip();if(count)draw();ctx.restore();return count;
}
function rd25Body(b,Q){
 const carrier=ER23_ART.banks.symbiote,wire=DR22_ART.forms.colossus;
 ctx.save();ctx.translate(Q.x,Q.y);ctx.rotate(Q.angle);ctx.translate(-Q.dx,-Q.dy);ctx.imageSmoothingEnabled=false;
 rd25Clip(Q,false,()=>{
  if(XART.rdy(wire.key)){const f=Math.floor(b._r30.clock/.07)%wire.frames,k=Q.size/(wire.captureSize*wire.captureScale);
   ctx.save();ctx.globalAlpha=Q.progress*.16;ctx.drawImage(XART.get(wire.key),f%wire.columns*wire.w,Math.floor(f/wire.columns)*wire.h,wire.w,wire.h,-wire.pivot[0]*k,-wire.pivot[1]*k,wire.w*k,wire.h*k);ctx.restore();}
  if(XART.rdy(carrier.key)){ctx.save();ctx.globalAlpha=1-Q.progress*.25;ctx.drawImage(XART.get(carrier.key),Q.frame%carrier.cols*carrier.w,Math.floor(Q.frame/carrier.cols)*carrier.h,carrier.w,carrier.h,
    Q.dx-RD25.carrierHeart[0],Q.dy-RD25.carrierHeart[1],carrier.w,carrier.h);ctx.restore();}
 });
 const bands=rd25Clip(Q,true,()=>{ctx.save();ctx.globalAlpha=.50+.50*Q.progress;ce20Body(b._r30.clock,0,0,Q.size);ctx.restore();});
 rd25Clip(Q,true,()=>{ctx.save();ctx.globalCompositeOperation='screen';ctx.globalAlpha=.50;ce20Body(b._r30.clock,0,0,Q.size);ctx.restore();},true);
 ctx.restore();return bands;
}
function rd25Lightning(b,Q,R){if(Q.t>=17){const n=R.bolts||0,phase=R.boltPhase||0,beats=Q.t<23?Math.min(3,1+Math.floor(Q.progress*3)):6;
 for(let i=0;i<beats;i++){const theta=(n-i)*2.399963,x=Q.x+Math.cos(theta)*viewW()*.46,y=Q.y+Math.sin(theta)*viewH()*.43;
  r25Bolt(x,y,Q.x+Math.cos(theta+.7)*25,Q.y+Math.sin(theta+.7)*25,Q.t+i*.15,Q.t<23?(.95-phase*.65)/(1+i*.4):.78);}}
}
function rd25UnderEffects(b,Q,R){}
function rd25OverEffects(b,Q,R){}
rb23SceneDraw=function(b){
 const t=b?._r30?.t;if(!rd25Own(b)||t<14)return RD25.base.draw.apply(this,arguments);
 const Q=rd25Pose(b),R=b._r30.v18.rb23Rebirth;
 if(t<25.6)er23Curtain('blackout',15);
 rd25UnderEffects(b,Q,R);const bands=rd25Body(b,Q);rd25OverEffects(b,Q,R);
 if(t<25.6){
  for(let i=0;i<7;i++){const side=i%2?-1:1,x=Q.x+side*(120+i%3*34),y=Q.y-180+((t*80+i*73)%350);v17Code(t*20+i*3,x,y,90,.23+Q.progress*.20);}
  rd25Lightning(b,Q,R);
  ctx.save();ctx.font='bold 13px monospace';ctx.textAlign='center';ctx.fillStyle=Q.progress>=1?'#fff':'#aaf6ff';ctx.fillText(Q.progress>=1?'DOWNLOAD COMPLETE':'DOWNLOADING  '+Math.floor(Q.progress*100).toString().padStart(2,'0')+'%',Q.x,Q.y+157);ctx.restore();
 }
 if(t>=25.3){const step=t<25.6?Math.floor((t-25.3)/.3*16):16-Math.floor(clamp((t-25.9)/2.6,0,1)*16);er23Curtain('whiteout',step);}
 RD25.last={...Q,bands,bolts:R.bolts,source:'native-colossus',carrier:ER23_ART.banks.symbiote.key,protected:b._noHit};S78.downloadLast=RD25.last;
};
rb23SceneTick=function(b,dt){const out=RD25.base.tick.apply(this,arguments);if(rd25Own(b)&&b._r30.t>=14){const Q=rd25Pose(b);b.x=Q.body.x;b.y=Q.body.y;}return out;};
globalThis.BOF_DRACODIA_DOWNLOAD_1025=RD25;
