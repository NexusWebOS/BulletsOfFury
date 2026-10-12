"use strict";
// Actual drawn rotational views. No scale-X squash, shear or top-plate warp.
const P2MC={base:{ace:whvDrawAce,key:whvAceKey,coilUnder:drawMavCoilUnder,coilOver:drawMavCoilOver,
 lance:drawHelixLance,balls:helixBallsDraw,bursts:helixBurstsDraw},views:new Map(),draws:{}};
for(const motion of ['roll','somer'])for(const a of P2_ART['stealth_'+motion])P2MC.views.set(a.role+'|'+motion+'|'+a.pose,a);
function p2StealthMotion(role,motion,progress,dir=1){
 const f=Math.min(15,Math.floor(clamp(progress,0,1)*16+1e-9)),i=dir<0?(16-f)%16:f;
 const a=P2MC.views.get(role+'|'+motion+'|'+i);return a&&XART.rdy(a.key)?a:null;
}
function p2StealthActorPose(e,role,A){
 if(A.somer)return p2StealthMotion(role,'somer',A.somer.t/(A.somer.dur||.62));
 if(A.roll)return p2StealthMotion(role,'roll',A.roll.t/(A.roll.dur||.46),A.roll.dir||1);
 if(e._s8Roll)return p2StealthMotion(role,'roll',e._s8Roll.t/e._s8Roll.dur,e._s8Roll.dir);
 if(e._rollT!=null)return p2StealthMotion(role,'roll',e._rollT/(typeof EL8_ROLL==='number'?EL8_ROLL:.55),e._rollDir||1);
 return null;
}
function p2AceView(b,A){
 if(A.somer){const f=Math.min(15,Math.floor(clamp(A.somer.t/.62,0,1)*16+1e-9)),i=(f+(A.inverted?8:0))%16;
  const a=P2MC.views.get('blue|somer|'+i);return a&&XART.rdy(a.key)?a:null;}
 if(A.roll)return p2StealthMotion('blue','roll',A.roll.t/.46,A.roll.dir);
 if(A.inverted){const a=P2MC.views.get('blue|roll|8');return a&&XART.rdy(a.key)?a:null;}
 if(Math.abs(A.vx)>170){const a=P2MC.views.get('blue|roll|'+(A.vx>0?1:15));return a&&XART.rdy(a.key)?a:null;}
 return null;
}
whvAceKey=function(b,A){return p2AceView(b,A)?.key||P2MC.base.key.apply(this,arguments);};
whvDrawAce=function(b){const A=b._whv?.ace,a=A&&!b.dead&&p2AceView(b,A);
 if(!a)return P2MC.base.ace.apply(this,arguments);
 const w=184,h=192;
 if(A.dash?.st==='warn')combatWarningDraw(b,{x:A.x,y:A.y,ex:A.dash.ex,ey:A.dash.ey,progress:A.dash.t/.95,width:w*.65});
 const P=A.desp;
 if(P?.st==='warn')combatWarningDraw(b,{x:A.x,y:A.y,ex:A.x,ey:VH+60,progress:P.t/.8,width:w*.65});
 if(P?.st==='cross'&&P.t<P.lead){combatWarningDraw(b,{x:P.x0,y:P.y0,ex:P.x1,ey:P.y1,progress:P.t/P.lead,width:95,fieldOnly:true});return;}
 // The original whole-view branch also preserves independent module health.
 const size=h*256/204,im=b.flash>0?xartTint(a.key,hitFlashColor(b),.84):XART.get(a.key);
 ctx.save();ctx.imageSmoothingEnabled=false;ctx.translate(A.x,A.y);if(A.inverted&&A.somer)ctx.rotate(Math.PI);
 ctx.drawImage(im||XART.get(a.key),-size/2,-size/2,size,size);ctx.restore();
 P2MC.draws.ace=(P2MC.draws.ace||0)+1;A._p2MotionKey=a.key;
 const r=b.hp/b.maxhp;whvPartFx(b,{x:A.x-58,y:A.y},r,false,.8,5);whvPartFx(b,{x:A.x+58,y:A.y},r,false,.8,6.3);
};
s6OpeningDraw=function(){const O=s6Opening;if(!O)return;ctx.save();ctx.imageSmoothingEnabled=false;
 if(O.phase==='flyover'&&XART.rdy('whv_closed')){
  const {x,y,w,h,sc}=s6OpeningCarrierPose(O),open=O.t>=1.55&&O.t<6.8&&XART.rdy('whv_open');
  const hullKey=open?'whv_open':'whv_closed',c=XART.get(hullKey),shadow=xartTint(hullKey,'#01030a',1);
  ctx.save();ctx.translate(x+24,y+72);ctx.rotate(Math.PI);ctx.globalAlpha=.55;if(shadow)ctx.drawImage(shadow,-w/2,-h/2,w,h);ctx.restore();
  ctx.save();ctx.translate(x,y);ctx.rotate(Math.PI);ctx.drawImage(c,-w/2,-h/2,w,h);
  if(XART.rdy('whv_fan')){const fan=XART.get('whv_fan');for(const side of [-1,1]){
   ctx.save();ctx.translate(side*169.5*sc,-10*sc);ctx.rotate(O.t*12*side);ctx.drawImage(fan,-53*sc,-53*sc,106*sc,106*sc);ctx.restore();}}
  ctx.restore();for(const j of O.carrierJets){const roll=clamp((j.age-.31)/.52,0,1),a=roll>0&&roll<1?p2StealthMotion('blue','roll',roll,j.side):null;
   const key=a?.key||'whv_ace';if(!XART.rdy(key))continue;const im=XART.get(key),hh=lerp(28,61,clamp(j.age/.55,0,1))*(a?256/204:1),ww=hh*im.width/im.height;
   ctx.save();ctx.translate(j.x,j.y);ctx.rotate(Math.PI);ctx.drawImage(im,-ww/2,-hh/2,ww,hh);ctx.restore();j._p2MotionKey=key;}
 }else if(!['countdown','flyover'].includes(O.phase)&&XART.rdy('whv_ace')){
  const im=XART.get('whv_ace'),alpha=O.phase==='cloak'?.035+.065*clamp((O.t-19.5)/2.5,0,1):O.phase==='reveal'?.10+.90*clamp(O.t/2.8,0,1):1;
  for(const j of O.jets){ctx.save();ctx.translate(j.x,j.y);ctx.globalAlpha=alpha;ctx.rotate(Math.PI);
   const hh=74,ww=hh*im.width/im.height;ctx.drawImage(im,-ww/2,-hh/2,ww,hh);ctx.restore();}
 }ctx.restore();if(O.phase==='countdown'){ctx.save();worldXformEscape();msgText(O.t<3?String(3-Math.floor(O.t)):'GO!',VW/2,VH*.40,58,'#ffffff',0,1,.07);ctx.restore();}
};
function p2MaverickBall(x,y,size,t,full,alpha=1){
 // The last authored pose is not identical to the first. Reverse the reel at
 // its endpoints instead of snapping 31 -> 0 once per second.
 const phase=Math.floor(Math.max(0,t)*24)%62,frame=phase<32?phase:62-phase;
 const a=P2_ART[full?'maverick_full':'maverick'][frame];
 if(!XART.rdy(a.key))return false;const k=size/256;
 ctx.save();ctx.imageSmoothingEnabled=false;ctx.globalAlpha*=alpha;
 ctx.drawImage(XART.get(a.key),x-a.pivot[0]*k,y-a.pivot[1]*k,a.w*k,a.h*k);ctx.restore();
 P2MC.draws.maverick=(P2MC.draws.maverick||0)+1;return true;
}
drawMavCoilUnder=function(){const p=_mavP();if(p<0)return;
 if(!P2_ART.maverick.every(a=>XART.rdy(a.key))||!P2_ART.maverick_full.every(a=>XART.rdy(a.key)))return P2MC.base.coilUnder.apply(this,arguments);
};
drawMavCoilOver=function(){P2MC.base.coilOver.apply(this,arguments);const p=_mavP();if(p<0)return;
 p2MaverickBall(player.x,player.y-28-24*p,24+90*p,efxClock,p>=.999,.6+.4*p);
};
drawHelixLance=function(x,y,len,full,phase,alpha,m,isBall){
 if(isBall&&p2MaverickBall(x,y,44+86*clamp(m||0,0,1),efxClock,full,alpha??1))return true;
 return P2MC.base.lance.apply(this,arguments);
};
helixBallsDraw=function(){for(const q of helixBalls){const p=clamp(q.t/q.life,0,1);
 if(!p2MaverickBall(q.x,q.y,96*(q.sc||1)*(.55+p*2.4),q.t,q.full,1-p*p))return P2MC.base.balls.apply(this,arguments);}
};
helixBurstsDraw=function(){if(typeof helixBallsDraw==='function')helixBallsDraw();
 for(const q of helixBursts){const p=clamp(q.t/q.life,0,1);p2MaverickBall(q.x,q.y,96*(q.sc||1)*(.55+p*2.4),q.t,q.full,1-p*p);}
};
