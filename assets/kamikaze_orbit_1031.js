"use strict";
/* Earth-camo rolling kamikaze. Source roll poses and source heading cells;
   bounded steering, orbit/pursuit/strike/recovery and native impact/HP/death. */
const KO31={base:{jet:jetTick,draw:drawEnemy,aiEnd:ai27End,load:stageLoadBegin},serial:0,clock:0,stamp:null,epoch:null,events:[],draws:{hull:0,thruster:0}};
XART._src[KO31_ART.key]=KO31_ART.path;XART.rdy(KO31_ART.key);
function ko31Owns(e){return run.stage===1&&!!e?._s1Kamikaze&&/^s1jetdelta(?:_b)?$/.test(rosterKey(e.type));}
function ko31Log(e,mode){KO31.events.push({mode,at:efxClock,id:e._ko31?.id,x:e.x,y:e.y});if(KO31.events.length>160)KO31.events.shift();}
function ko31Mode(e,mode){const A=e._ko31;A.mode=mode;A.modeT=0;A.committed=false;if(mode==='orbit'&&KO31.epoch==null)KO31.epoch=KO31.clock;ko31Log(e,mode);if(mode==='strike')Audio.SFX.jetDash?.();}
function ko31Init(e){
 if(e._ko31)return e._ko31;
 const rank=e._s1LeadRank??KO31.serial,base=Math.max(168,(e._jspd||104)*1.60),id=++KO31.serial;
 const neighbours=enemies.filter(q=>q!==e&&ko31Owns(q)&&s1bAlive(q)&&q._ko31);if(!neighbours.length){KO31.epoch=null;KO31.clock=0;KO31.stamp=null;}
 const preferred=clamp(Math.floor((e.x-camLeftX())/Math.max(1,camRightX()-camLeftX())*5),0,4),used=new Set(neighbours.map(q=>q._ko31.slot));
 const slot=[0,1,2,3,4].sort((a,b)=>Math.abs(a-preferred)-Math.abs(b-preferred)).find(n=>!used.has(n))??preferred;
 const A=e._ko31={id,slot,head:Math.PI/2,mode:'approach',modeT:0,age:0,roll:0,rollRate:.85,rollFrame:0,side:rank%2?-1:1,radius:130,speed:base,currentSpeed:base,attempts:0,committed:false,minDistance:1e9};
 e._s1aFlight=A;e._jet=1;e._atk='none';e.shoots=false;e.fk=null;e.impact=true;e._noSep=true;e._s1Elite=null;e._ko31ThrusterFrame=0;ko31Log(e,'approach');return A;
}
function ko31Tick(e,dt){
 if(!s1bAlive(e))return;const A=ko31Init(e);
 if((e._s1DelayFrames||0)>0){e._s1DelayFrames--;return;}
 if(e._frozen||e._mercuryLock>0)return;
 if(e._stagger>0){e._stagger=Math.max(0,e._stagger-dt);return;}
 dt=Math.max(0,dt);A.age+=dt;A.modeT+=dt;
 // Advance the formation clock once per live simulation tick, including after
 // a pause; scenery/effect time is only the identity of that tick.
 if(KO31.stamp!==efxClock){KO31.stamp=efxClock;KO31.clock+=dt;}
 const T=targetShip(e.x,e.y),distance=Math.hypot(T.x-e.x,T.y-e.y),left=camLeftX(),right=camRightX();
 const centre={x:clamp(T.x,left+145,right-145),y:clamp(T.y-65,PLAY.y+145,VH-140)},rx=e.x-centre.x,ry=e.y-centre.y,rd=Math.max(1,Math.hypot(rx,ry));
 const lead={x:T.x+clamp((T.x-(A.targetX??T.x))/Math.max(dt,.001),-210,210)*.18,y:T.y};A.targetX=T.x;
 if(A.mode==='approach'&&rd<A.radius+80)ko31Mode(e,'orbit');
 if(A.age>20&&A.mode!=='exit')ko31Mode(e,'exit');
 let vx,vy,turn=2.25,speed=A.speed;
 if(A.mode==='approach'){vx=lead.x-e.x;vy=lead.y-e.y;}
 else if(A.mode==='orbit'){
  // Shared circulating slots keep a wave flowing in one direction instead
  // of sending head-on aircraft through the same orbital path.
  const theta=-Math.PI/2+(A.slot-2)*TAU/5+(KO31.clock-(KO31.epoch??KO31.clock))*1.35;
  const px=centre.x+Math.cos(theta)*A.radius,py=centre.y+Math.sin(theta)*A.radius;
  vx=-Math.sin(theta)*A.radius*1.35+(px-e.x)*2.2;vy=Math.cos(theta)*A.radius*1.35+(py-e.y)*2.2;
  speed=clamp(Math.hypot(vx,vy),A.speed*.60,A.speed*1.08);
  if(A.modeT>2.4&&!enemies.some(q=>q!==e&&ko31Owns(q)&&s1bAlive(q)&&q._ko31?.mode==='strike'))ko31Mode(e,'strike');
 }else if(A.mode==='strike'){
  speed=A.speed*1.16;turn=2.9;
  if(A.committed){vx=Math.cos(A.commitHead);vy=Math.sin(A.commitHead);turn=0;}
  else {vx=lead.x-e.x;vy=lead.y-e.y;const aim=Math.atan2(vy,vx);
   if(distance<102&&Math.abs(s1aAngle(aim-A.head))<.40){A.committed=true;A.commitHead=A.head;A.commitT=A.modeT;ko31Log(e,'impact-commit');}}
  if(A.modeT>1.45||A.committed&&A.modeT-A.commitT>.62){A.attempts++;ko31Mode(e,'recover');}
 }else if(A.mode==='recover'){
  vx=centre.x-e.x;vy=centre.y-110-e.y;turn=2.65;
  if(A.modeT>1.25)ko31Mode(e,A.attempts>=2?'exit':'orbit');
 }else {vx=(A.side>0?right+180:left-180)-e.x;vy=VH+160-e.y;}
 // Nearby craft steer apart without a lateral position shove or a speed jump.
 if(!A.committed&&A.mode!=='exit'){
  let nx=0,ny=0;for(const q of enemies){if(q===e||!ko31Owns(q)||!s1bAlive(q))continue;
   const dx=e.x-q.x,dy=e.y-q.y,d=Math.hypot(dx,dy);if(d>235)continue;
   const rvx=Math.cos(A.head)*speed-(q.vx||0)*60,rvy=Math.sin(A.head)*speed-(q.vy||0)*60;
   const closest=clamp(-(dx*rvx+dy*rvy)/Math.max(1,rvx*rvx+rvy*rvy),0,.70),px=dx+rvx*closest,py=dy+rvy*closest,pd=Math.hypot(px,py);
   const danger=Math.max(clamp((142-d)/142,0,1),clamp((108-pd)/108,0,1));
   if(danger){const length=Math.max(1,pd),ax=pd>4?px:dx,ay=pd>4?py:dy;nx+=ax/length*danger;ny+=ay/length*danger;turn=Math.max(turn,4.1);}
  }
  const length=Math.max(.001,Math.hypot(vx,vy));vx=vx/length+nx*2.6;vy=vy/length+ny*2.6;
  // Anticipate the visible edges using the aircraft's current velocity. Bank
  // back into the field; do not clamp/teleport a pursuing plane at the edge.
  const px=e.x+Math.cos(A.head)*speed*.48,py=e.y+Math.sin(A.head)*speed*.48;
  const wallX=clamp((left+52-px)/95,0,1)-clamp((px-(right-52))/95,0,1);
  const wallY=clamp((py-(VH-58))/90,0,1);
  vx+=wallX*2.5;vy-=wallY*2.5;
  if(A.mode!=='approach')vy+=clamp((PLAY.y+48-py)/85,0,1)*2.0;
  if(wallX||wallY)turn=Math.max(turn,3.3);
 }
 const want=Math.atan2(vy,vx);A.head+=clamp(s1aAngle(want-A.head),-turn*dt,turn*dt);
 A.currentSpeed+=clamp(speed-A.currentSpeed,-190*dt,190*dt);
 const ox=e.x,oy=e.y;e.x+=Math.cos(A.head)*A.currentSpeed*dt;e.y+=Math.sin(A.head)*A.currentSpeed*dt;e.vx=(e.x-ox)/Math.max(dt,.001)/60;e.vy=(e.y-oy)/Math.max(dt,.001)/60;e.spin=0;
 A.distance=Math.hypot(T.x-e.x,T.y-e.y);A.minDistance=Math.min(A.minDistance,A.distance);
 const near=clamp((245-A.distance)/205,0,1),rate=.85+4.7*Math.pow(near,1.45);
 A.rollRate+=(rate-A.rollRate)*Math.min(1,dt*6);A.roll+=A.rollRate*dt;A.rollFrame=Math.floor(A.roll*KO31_ART.frames)%KO31_ART.frames;
 e._air13Frame=s1aDir(A.head);e._ko31ThrusterFrame=Math.floor(A.age*25)%8;
 if(A.mode==='exit'&&(e.x<left-90||e.x>right+90||e.y>VH+85))e.dead=true;
}
jetTick=function(e,dt){return ko31Owns(e)?ko31Tick(e,dt):KO31.base.jet.apply(this,arguments);};
ai27End=function(e,previous){if(ko31Owns(e)&&e._ai27)e._ai27.dx=0;return KO31.base.aiEnd.apply(this,arguments);};
function ko31Blit(e,colour=null,alpha=1,dx=0,dy=0){
 const A=e._ko31;if(!A||!XART.rdy(KO31_ART.key))return;const c=KO31_ART.cell,im=colour?xartTint(KO31_ART.key,colour,1):XART.get(KO31_ART.key),size=Math.max(e.w,e.h)*1.10;
 ctx.save();ctx.globalAlpha*=alpha;ctx.imageSmoothingEnabled=false;ctx.drawImage(im,s1aDir(A.head)*c,A.rollFrame*c,c,c,e.x-size/2+dx,e.y-size/2+dy,size,size);ctx.restore();
}
function ko31Draw(e){
 const A=e._ko31||ko31Init(e);
 ko31Blit(e,'#000000',.24,10,18);
 const angle=s1aPoseAngle(A.head)-Math.PI/2,c=Math.cos(angle),s=Math.sin(angle),scale=Math.max(e.w,e.h)*1.10/128;
 for(const [x,y]of KO31_ART.tailSockets[A.rollFrame]){const dx=(x-64)*scale,dy=(y-64)*scale;s1aBlit('thruster',e._ko31ThrusterFrame,A.head,e.x+dx*c-dy*s,e.y+dx*s+dy*c,58);KO31.draws.thruster++;}
 ko31Blit(e,tintColor(e));e._drawW=e._drawH=Math.max(e.w,e.h)*1.10;e._air13RenderedKey=KO31_ART.key;KO31.draws.hull++;
}
drawEnemy=function(e){if(ko31Owns(e)&&s1bAlive(e))return ko31Draw(e);return KO31.base.draw.apply(this,arguments);};
stageLoadBegin=function(n,keys){return KO31.base.load.call(this,n,n===1?[...(keys||[]),KO31_ART.key,S1A_ART.thruster.key]:keys);};
