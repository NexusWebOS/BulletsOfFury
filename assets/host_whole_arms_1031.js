'use strict';
/* RD96: complete shoulder-to-claw strikes and a current-torso shell closure. */
const RD96={base:{body:bi24Draw,vbody:v18Body,physical:rd72Physical,at:r30At,point:rb23PartPoint,root:rd72Root,port:rd72Port,rupture:v18Rupture,foldInit:rd73Init,attackTick:v18AttackTick,load:stageLoadBegin},events:[],draws:{}};
for(const a of Object.values(RD96_ART))XART._src[a.key]=a.path;
function rd96Log(event,data={}){RD96.events.push({event,clock:efxClock,...data});if(RD96.events.length>800)RD96.events.shift();}
function rd96Physical(b){const P=rd72Act(b);return P?.physical?P:null;}
function rd96Blit(n,f,x,y,hit=false){const a=RD96_ART[n+(hit?'_hit':'')]||RD96_ART[n];if(!a||!XART.rdy(a.key))return false;f=clamp(f|0,0,a.frames-1);ctx.drawImage(XART.get(a.key),f%a.cols*a.cw,Math.floor(f/a.cols)*a.ch,a.cw,a.ch,Math.round(x-a.pivot[0]),Math.round(y-a.pivot[1]),a.cw,a.ch);RD96.draws[n]=(RD96.draws[n]||0)+1;return true;}
function rd96Alpha(n,f,x,y){const a=RD96_ART[n],xx=Math.floor(x+a.pivot[0]),yy=Math.floor(y+a.pivot[1]);if(xx<0||yy<0||xx>=a.cw||yy>=a.ch)return false;const row=a.spans[clamp(f|0,0,a.frames-1)][yy];for(let i=0;i<row.length;i+=2)if(xx>=row[i]&&xx<row[i+1])return true;return false;}
function rd96Rig(b,P,f){f=clamp(f|0,0,63);const v=RD96_ART['arm_'+P.side].poses[f];P.rd96={f,lean:v.lean};P.rig={root:{x:b.x+v.root[0],y:b.y+v.root[1]},wrist:{x:b.x+v.tip[0],y:b.y+v.tip[1]},tip:{x:b.x+v.tip[0],y:b.y+v.tip[1]},nodes:[],frame:f};P.grip=v.grip;}
rd72Root=function(b,side){const P=rd96Physical(b);if(P?.side===side&&P.rig)return{...P.rig.root};return{x:b.x+(side==='left'?-84:84),y:b.y-52};};
function rd96Goal(b,P){const a=RD96_ART['arm_'+P.side].poses[27],q={x:clamp(P.target.x-a.tip[0],camLeftX()+140,camRightX()-140),y:clamp(P.target.y-a.tip[1],viewTopY()+145,VH-150)},dx=q.x-P.origin.x,dy=q.y-P.origin.y,d=Math.hypot(dx,dy),k=d>175?175/d:1;return{x:P.origin.x+dx*k,y:P.origin.y+dy*k};}
function rd96Move(b,a,z,k){k=clamp(k,0,1);k=k*k*(3-2*k);b.x=lerp(a.x,z.x,k);b.y=lerp(a.y,z.y,k);b._drawY=b.y;}
rd72Physical=function(b,P,dt){const u=P.t-P.tell,sign=P.side==='left'?-1:1;if(!P.rd96)rd96Log('whole-arm-windup',{serial:P.serial,side:P.side,kind:P.kind});
 if(u<0){P.rd96Goal=rd96Goal(b,P);b.x=P.origin.x;b.y=P.origin.y;b._drawY=b.y;rd96Rig(b,P,Math.floor(clamp(P.t/P.tell,0,1)*15));return;}
 const goal=P.rd96Goal||(P.rd96Goal=rd96Goal(b,P));
 if(!P.rd96Struck){P.rd96Struck=true;combatAudio0927(b,'combatModule0927',.15);rd96Log('whole-arm-strike',{serial:P.serial,side:P.side,target:{...P.target},advance:Math.hypot(goal.x-P.origin.x,goal.y-P.origin.y)});}
 if(P.grab?.active){const G=P.grab;G.t+=dt;const k=clamp(G.t/.65,0,1);rd96Move(b,goal,{x:goal.x+sign*8,y:goal.y-35},k);rd96Rig(b,P,48+Math.floor(k*7));
  withSeat(G.seat,()=>{player.x=P.rig.tip.x;player.y=P.rig.tip.y;player.invuln=3;player._bank=0;});if(G.t>=1.25){P.rd96Return={x:b.x,y:b.y};rd72Throw(b,P,G);}return;}
 if(P.throwAt!=null){const k=clamp((P.t-P.throwAt)/.65,0,1);rd96Move(b,P.rd96Return||goal,P.origin,k);rd96Rig(b,P,56+Math.floor(k*7));if(k>=1)rd72Finish(b,P);return;}
 let f;if(u<.30){rd96Move(b,P.origin,goal,u/.30);f=16+Math.floor(clamp(u/.30,0,1)*11);}
 else if(u<.70){b.x=goal.x;b.y=goal.y;b._drawY=b.y;f=28+Math.floor((u-.30)/.40*3);}
 else{const k=clamp((u-.70)/.85,0,1);rd96Move(b,goal,P.origin,k);f=32+Math.floor(k*15);}
 rd96Rig(b,P,f);
 if(P.kind==='grab'&&u>=.22&&u<.70)rd72Catch(b,P);
 if(P.kind==='swipe'&&u>=.22&&u<.76)for(const seat of seatList())withSeat(seat,()=>{if(!player.dead&&!P.contacts.has(seat)&&Math.hypot(player.x-P.rig.tip.x,player.y-P.rig.tip.y)<30){P.contacts.add(seat);playerHit('Dracodia whole-arm swipe');rd72Log('claw-contact',{seat,side:P.side});rd96Log('whole-arm-contact',{seat,side:P.side});}});
 if(u>=1.55&&!P.grab?.active)rd72Finish(b,P);
};
bi24Draw=function(q,b,size,rot=0){const P=rd96Physical(b);if(!P||rot)return RD96.base.body.apply(this,arguments);const f=P.rd96?.f||0,k=P.rd96?.lean||0,side=P.side,other=side==='left'?'right':'left',core=b.parts.find(p=>p.id==='core'),passive=b.parts.find(p=>p.id===other),arm=b.parts.find(p=>p.id===side);
 if(passive&&!passive.destroyed)rd96Blit('passive_'+side,k,b.x,b.y,passive.flash>0);
 rd96Blit('core_'+side,k,b.x,b.y,Math.max(core?.flash||0,b.flash||0)>0);
 if(arm&&!arm.destroyed)rd96Blit('arm_'+side,f,b.x,b.y,arm.flash>0);
 BI24.current.set(b,{...q,size:360,k:360/512,rot:0,x:b.x,y:b.y,key:q.a.key});return true;};
rb23PartPoint=function(b,p,muzzle=false){const P=rd96Physical(b);if(P?.side===p.id&&P.rig)return{...P.rig.tip};if(rd73Own(b)&&p.id==='core')return{x:b.x,y:b.y};return RD96.base.point.apply(this,arguments);};
function rd96Fold(b){const N=b?._r30?.v18,P=N?.attack;return rd73Own(b)&&!N.r25BallReady&&P?.type==='rb23-roll'?{P,f:Math.min(RD96_ART.fold.frames-1,Math.floor(P.t/P.tell*RD96_ART.fold.frames))}:null;}
r30At=function(b,x,y){const P=rd96Physical(b);if(P){if(!r30Live(b)||b._noHit)return null;const f=P.rd96?.f||0,k=P.rd96?.lean||0,other=P.side==='left'?'right':'left';for(const [id,bank,frame]of [[P.side,'arm_'+P.side,f],[other,'passive_'+P.side,k],['core','core_'+P.side,k]]){const p=b.parts.find(p=>p.id===id);if(p&&!p.destroyed&&p.hp>0&&rd96Alpha(bank,frame,x-b.x,y-b.y))return p;}return null;}
 const F=rd96Fold(b);if(F){if(!r30Live(b)||b._noHit)return null;return rd96Alpha('fold',F.f,x-b.x,y-b.y)?b.parts.find(p=>p.id==='core'):null;}
 if(rd73Own(b)&&!b._r30.v18.r25BallReady&&!b._r30.v18.attack){if(!r30Live(b)||b._noHit)return null;return rd96Alpha('armless',0,x-b.x,y-b.y)?b.parts.find(p=>p.id==='core'):null;}return RD96.base.at.apply(this,arguments);};
v18Rupture=function(b,p){const P=rd96Physical(b);if(!P||P.side!==p.id)return RD96.base.rupture.apply(this,arguments);rd72Cancel(b,'grabbing-arm-destroyed');const v=RD96_ART['arm_'+P.side].poses[P.rd96?.f||0],points=[v.root,v.elbow,v.tip];RD71.breaks.push({b,origin:{x:b.x,y:b.y},points,t:0,next:0,side:p.id});if(RD71.breaks.length>2)RD71.breaks.shift();r30Sound('expBig');shake=Math.max(shake,8);rd71Log(b,'whole-shoulder-arm-break',{part:p.id,points});rd96Log('whole-arm-break',{side:p.id,frame:P.rd96?.f||0});return;};
rd73Init=function(b,P){const ready=!!b._r30.v18.r25BallReady,r=RD96.base.foldInit.apply(this,arguments);if(!ready){P.tell=1.50;P._rd96Fold=true;b._r30.v18.bi24Rolled=false;combatAudio0927(b,'combatEnergy0927',.2);rd96Log('current-torso-fold-start',{hp:b.hp,tell:P.tell});}return r;};
v18AttackTick=function(b,dt){const out=RD96.base.attackTick.apply(this,arguments),N=b?._r30?.v18,P=N?.attack;if(rd73Own(b)&&P?._rd96Fold&&!N.r25BallReady&&P.t>=P.tell){N.r25BallReady=true;N._rd96RollAt=b._r30.clock;N.bi24Rolled=true;combatAudio0927(b,'combatOrb0927',.16);rd96Log('sphere-closed',{startFrame:RD96_ART.fold.ballStartFrame,hp:b.hp});}return out;};
v18Body=function(b){if(!rd73Own(b))return RD96.base.vbody.apply(this,arguments);const N=b._r30.v18,core=b.parts.find(p=>p.id==='core'),hit=Math.max(core?.flash||0,b.flash||0)>0,F=rd96Fold(b);
 if(F){N.bi24Rolled=false;return rd96Blit('fold',F.f,b.x,b.y,hit);}
 if(!N.r25BallReady){N.bi24Rolled=false;return rd96Blit('armless',0,b.x,b.y,hit);}
 const a=ER23_ART.banks.roll,key=a.key+(hit?'_hit':''),f=(RD96_ART.fold.ballStartFrame+Math.floor(Math.max(0,b._r30.clock-(N._rd96RollAt||b._r30.clock))*30))%a.count;if(!XART.rdy(key))return false;N.bi24Rolled=true;ctx.drawImage(XART.get(key),f%a.cols*a.w,Math.floor(f/a.cols)*a.h,a.w,a.h,Math.round(b.x-a.pivot[0]),Math.round(b.y-a.pivot[1]),a.w,a.h);RD96.draws.roll=(RD96.draws.roll||0)+1;return true;};
stageLoadBegin=function(n,keys){if(n===8)Snd.prepare(['combatModule0927','combatEnergy0927','combatOrb0927']);return RD96.base.load.call(this,n,n===8?[...(keys||[]),...Object.values(RD96_ART).map(a=>a.key)]:keys);};
globalThis.BOF_HOST_WHOLE_ARMS=RD96;
