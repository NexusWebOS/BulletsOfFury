"use strict";
/* Physical claws use the same authored rig for rendering, targets and contact. */
const AP10_A={parts:r30Parts,attack:r30Attack,draw:r30DrawBoss,shot:f1003bShot,
 mega:s8MegaTick,break:r30Break,morph:j3Morph,tick:r30Tick,events:[]};
function ap10HostSwipe(b){return j3State(b)?.encounter===0&&b._r30.attack?.type==='hostClaws'&&!hf7State(b)?.sig;}
r30Parts=function(b){const out=AP10_A.parts.apply(this,arguments);if(!ap10HostSwipe(b))return out;
 const P=b._r30.attack,Q=r30Pose(b),u=clamp((P.t-P.tell)/P.active,0,1),wind=clamp(P.t/P.tell,0,1);
 for(const v of out)if(['left','right'].includes(v.p.id)){
  const side=v.p.id==='left'?-1:1,rot=side*(P.t<P.tell?-.62*wind:-.62*Math.cos(u*Math.PI)+.95*Math.sin(u*Math.PI));
  v.rot=rot;v.x=Q.x+side*78-Math.sin(rot)*v.h*.4;v.y=Q.y-43+Math.cos(rot)*v.h*.4;
 }return out;};
function ap10ClawTip(v){return{x:v.x-Math.sin(v.rot)*v.h*.36,y:v.y+Math.cos(v.rot)*v.h*.36};}
r30DrawBoss=function(b){const r=AP10_A.draw.apply(this,arguments);if(ap10HostSwipe(b)){
 const P=b._r30.attack;if(P.t<P.tell)for(const v of r30Parts(b).filter(v=>['left','right'].includes(v.p.id))){
  const tip=ap10ClawTip(v);combatWarningDraw(b,{...tip,ex:P.tx,ey:P.ty,width:44,progress:P.t/P.tell,fieldOnly:true});}
 }return r;};
f1003bShot=function(){const q=AP10_A.shot.apply(this,arguments);
 if(q&&!q.dead&&j3State(arguments[0])){AP10_A.events.push({event:'projectile',phase:j3State(arguments[0]).encounter,kind:arguments[5]});
  if(AP10_A.events.length>240)AP10_A.events.shift();}return q;};
// A surviving copy visibly ruptures when its own persistent HP is depleted;
// a healthy copy changing tactics keeps its existing transformation.
j3Morph=function(b,to){const J=j3State(b),S=b?._r30;
 if(J?.encounter===2&&J.hp[J.active]<=0&&S.mode==='fight'&&!S.ap10CopyBroken){
  S.ap10CopyBroken={to,t:0,rig:r30Parts(b).map(v=>({...v}))};b.enter=true;S.attack=null;
  for(const v of S.ap10CopyBroken.rig){const key=REALM30_ART[v.key]?'r30_'+v.key:v.key;
   if(XART.rdy(key))d27ModuleRupture(b,{...v.p,_d27Ruptured:false},{...v,debrisImage:XART.get(key)},'purple');}
  r30Sound('expBig');AP10_A.events.push({event:'copy-destroyed',form:J.active});return;
 }return AP10_A.morph.apply(this,arguments);};
r30Tick=function(b,dt){const S=b?._r30;
 if(S?.mode==='takeover'&&S.t>=3.6&&!S.ap10ConsumeShriek){
  S.ap10ConsumeShriek=true;r30Sound('dracodiaShriek');shake=Math.max(shake,10);
  AP10_A.events.push({event:'consumption-shriek'});
 }
 const Q=S?.ap10CopyBroken;if(Q){
 j3Timers(b,Math.min(.05,dt));Q.t+=dt;b.enter=true;b._noHit=true;
 if(Q.t>=1.25){delete b._r30.ap10CopyBroken;b._noHit=false;return AP10_A.morph.call(this,b,Q.to);}return;
 }return AP10_A.tick.apply(this,arguments);};
const AP10_A_BROKEN_DRAW=r30DrawBoss;
r30DrawBoss=function(b){if(b?._r30?.ap10CopyBroken)return;return AP10_A_BROKEN_DRAW.apply(this,arguments);};
// The ordinary alien fleet must participate before passing below the player.
// Keep the authored row-specific attacks, add only a second committed volley.
s8MegaTick=function(e,dt){const before=e._frRealmAI?.seq||0,r=AP10_A.mega.apply(this,arguments),A=e._frRealmAI;
 if(A&&A.seq>before){A.cd*=diffKey==='easy'?.88:diffKey==='normal'?.72:.66;
  if(fr27RealmRow(e)===0||fr27RealmRow(e)===3)A.ap10Follow={left:.35,x:e.x,y:e.y+e.h*.4,target:{x:player.x,y:player.y},row:fr27RealmRow(e)};}
 const Q=A?.ap10Follow;if(Q){Q.left-=dt;if(Q.left<=0){
  const a=Math.atan2(Q.target.y-Q.y,Q.target.x-Q.x);for(const d of [-.11,.11])fr27RealmShot(Q.x,Q.y,a+d,3.7+fr27Difficulty()*.45,Q.row===3?2:0);
  Audio.SFX.enemyHeavyLaser?.();A.ap10Follow=null;}}
 return r;};
