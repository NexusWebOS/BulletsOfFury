'use strict';
/* Nyx fires only while fully visible in the current viewport. One socket map
   owns FOV, emitted shots and attached muzzle effects for every firing pose. */
const NY47={base:{socket:nx37Socket,attack:rg4Attack,act:rg4AttackTick,tick:rebelSquadTick,warning:rg4Warning,dispatch:RD42.attack},events:[]};
function ny47Log(event,data={}){NY47.events.push({event,time:rg4State()?.age||0,...data});if(NY47.events.length>300)NY47.events.shift();}
function ny47Rect(){const W=rg4State()?.rr26?.wall,wall=W&&W.t>=W.cast+W.build&&W.t<W.dur-W.fade;return{left:camLeftX()+82,right:camRightX()-82,top:PLAY.y+72,bottom:Math.max(PLAY.y+72,Math.min(VH*.48,wall?rr26WallRect().y-78:VH*.48))};}
function ny47Visible(q){const r=ny47Rect();return q.x>=r.left-.01&&q.x<=r.right+.01&&q.y>=r.top-.01&&q.y<=r.bottom+.01&&!ny46Hidden(q);}
function ny47Point(p){const r=ny47Rect();return{x:clamp(p.x,r.left,r.right),y:clamp(p.y,r.top,r.bottom)};}
function ny47Hold(q,A){const p=ny47Point(A.from||q);A.from={x:p.x,y:p.y};q.x=p.x;q.y=p.y;A.a=clamp(A.a??Math.PI/2,.95,2.19);q.rfHeading=A.a;q.evadeT=0;q.frSomersault=false;}
nx37Socket=function(q,side){if(!ny46Own(q))return NY47.base.socket.apply(this,arguments);
 const p=rr26AnimatedPose(q)||rr26Pose(q),B=p&&NY47_SOCKETS[p.key];if(!B)return NY47.base.socket.apply(this,arguments);
 const xy=B.points[p.f%B.points.length][side<0?0:1],k=p._af21?SHIP_DRAW_H*1.5*p.M.referenceRatio/p.M.span:SHIP_DRAW_H*1.5*p.d.referenceRatio/p.m.span;
 return{x:q.x+(xy[0]-B.pivot[0])*k,y:q.y+(xy[1]-B.pivot[1])*k,side,key:p.key,frame:p.f,angle:q.rg4?.act?.a??q.rfHeading??Math.PI/2};
};
rg4Attack=function(q){const r=NY47.base.attack.apply(this,arguments),A=q.rg4?.act;if(ny46Own(q)&&A?.kind==='nx37ambush'){A.home=ny47Point(A.home);A.near=ny47Point(A.near);}return r;};
RD42.attack=function(q){if(ny46Own(q)&&ny46Hidden(q)){q.rg4.cd=Math.max(.4,q.rg4.cd);return;}return NY47.base.dispatch.apply(this,arguments);};
rg4AttackTick=function(q,R,G,dt){const A=q.rg4?.act;if(!ny46Own(q)||A?.kind!=='nx37ambush')return NY47.base.act.apply(this,arguments);
 if(A.home)A.home=ny47Point(A.home);if(A.near)A.near=ny47Point(A.near);
 if(['charge','fire'].includes(A.phase)&&!ny46Hidden(q))ny47Hold(q,A);
 const first=eBullets.length,r=NY47.base.act.apply(this,arguments);
 if(q.rg4?.act===A&&['charge','fire'].includes(A.phase)&&!ny46Hidden(q))ny47Hold(q,A);
 for(const z of eBullets.slice(first))if(z._nx37Laser&&z.owner===q){
  const ports=[nx37Socket(q,-1),nx37Socket(q,1)],p=ports.reduce((a,b)=>Math.hypot(a.x-z.x,a.y-z.y)<Math.hypot(b.x-z.x,b.y-z.y)?a:b);
  z._ny47Socket={x:p.x,y:p.y,key:p.key,frame:p.frame,side:p.side};ny47Log('shot',{visible:ny47Visible(q),x:z.x,y:z.y,socket:{...z._ny47Socket},angle:A.a});
 }return r;
};
rebelSquadTick=function(b,dt){const before=b?._rebels?.ships.find(q=>ny46Own(q,b)&&!q.dead);
 if(before&&b._rebels.frIntro?.done&&before._ny46Hidden===false){before._rd21Visible=999;before._rd21Cloak=false;before.frCloak=0;}
 const r=NY47.base.tick.apply(this,arguments),q=b?._rebels?.ships.find(q=>ny46Own(q,b)&&!q.dead),A=q?.rg4?.act;
 if(A?.kind==='nx37ambush'&&['charge','fire'].includes(A.phase)&&!ny46Hidden(q)){
  if(!ny47Visible(q)){ny47Hold(q,A);rr45Separate(b);if(!ny47Visible(q))ny47Hold(q,A);}
 }return r;};
rg4Warning=function(q,A){if(!ny46Own(q)||A?.kind!=='nx37ambush')return NY47.base.warning.apply(this,arguments);
 if(A.phase==='charge'&&!ny46Hidden(q)){for(const side of[-1,1]){const p=nx37Socket(q,side),dx=Math.cos(A.a),dy=Math.sin(A.a),spans=[];
  if(dy>0)spans.push((VH-p.y)/dy);if(dx>0)spans.push((camRightX()-p.x)/dx);else if(dx<0)spans.push((camLeftX()-p.x)/dx);
  const len=Math.max(36,Math.min(...spans.filter(n=>n>0)));combatWarningDraw(A,{x:p.x,y:p.y,ex:p.x+dx*len,ey:p.y+dy*len,len,width:18,progress:A.t/A.warm,fieldOnly:true,laneShape:'line'});
 }}};
globalThis.BOF_NYX_FIRING_1029=NY47;
