"use strict";
/* The Herald fights as a flying predator. Every committed body pass and feather
   lane is warned. Native joints, part damage, retina targets, hit flashes and
   breakup continue to own the same module objects. */
const HP22={events:[],base:{tell:hd1003Tell,tick:hd1003Tick,pose:hd1003Pose,blit:hd1003Blit,draw:heraldDeathDraw,projectile:ovSonicProjectileDraw},cfg:[
 {warm:1.35,speed:620,recover:1.05,feathers:3},{warm:1.15,speed:710,recover:.90,feathers:5},
 {warm:1.02,speed:790,recover:.80,feathers:5},{warm:.94,speed:850,recover:.72,feathers:7},{warm:.90,speed:880,recover:.68,feathers:7}]};
function hp22Log(b,event,data={}){HP22.events.push({event,time:b._hd1003.clock,...data});if(HP22.events.length>200)HP22.events.shift();}
function hp22Cfg(){return HP22.cfg[target17Rank()];}
function hp22Start(b,kind){const H=b._hd1003,C=hp22Cfg();H.seq++;H._hd19=null;H.mode='predator';H.age=0;H.attackAge=0;H.lanes=[];H.flashes=[];
 const low=b.hp/b.maxhp<.35,side=H.seq%2?-1:1;b._s4MiniSafe=true;
 H._hp22={kind,phase:'perch',t:0,warm:C.warm,angle:0,passes:0,total:low&&kind!=='feathers'?2:1,side,from:{x:b.x,y:b.y},
  perch:{x:clamp(camLeftX()+viewW()*(kind==='swoop'?(side<0?.17:.83):.5),camLeftX()+65,camRightX()-65),y:viewTopY()+110}};
 if(b._hc1007)b._hc1007.cross=null;S81003.beams=S81003.beams.filter(q=>q.owner!==b);
 H.history.push(kind);if(H.history.length>30)H.history.shift();hp22Log(b,'predator-start',{kind,low});
}
hd1003Tell=function(b){const H=b._hd1003;
 // Teach the original skull and lance tells, then mix dives with the existing
 // rotating eclipse instead of stacking two controllers on the same boss.
 if(H.seq<2)return HP22.base.tell.apply(this,arguments);
 const book=['talon-dive','feathers','swoop','native','feathers','swoop'],kind=book[(H.seq-2)%book.length];
 if(kind==='native'&&!hd19Disarmed(b))return HP22.base.tell.apply(this,arguments);
 return hp22Start(b,kind==='native'?'talon-dive':kind);
};
function hp22Lock(b){const H=b._hd1003,P=H._hp22,T=targetShip(b.x,b.y);P.phase='tell';P.t=0;P.target={x:T.x,y:T.y};P.origin={x:b.x,y:b.y};P.angle=0;
 const a=Math.atan2(T.y-b.y,T.x-b.x);P.flightAngle=a;P.end={x:b.x+Math.cos(a)*VH*1.30,y:b.y+Math.sin(a)*VH*1.30};P.lines=[];
 if(P.kind==='feathers'){
  let ids=['wingL','wingR'].filter(id=>hd1003Live(b,hd1003Part(b,id)));if(!ids.length)ids=['head'];
  const n=hp22Cfg().feathers;for(const id of ids){const Q=hd1003Muzzle(b,id),aim=Math.atan2(T.y-Q.y,T.x-Q.x);
   for(let i=0;i<n;i++){const angle=aim+(i-(n-1)/2)*.14;P.lines.push({x:Q.x,y:Q.y,ex:Q.x+Math.cos(angle)*VH*1.4,ey:Q.y+Math.sin(angle)*VH*1.4,width:18,aim:angle,id,issued:false});}}
 }else P.lines.push({x:b.x,y:b.y+30,ex:P.end.x,ey:P.end.y,width:160});
 combatAudio0927(b,'bossWeaponCharge',.8);combatAudio0927(b,'combatAlien0927',1);hp22Log(b,'predator-tell',{kind:P.kind,warm:P.warm,target:P.target});
}
hd1003Tick=function(b,dt){const H=b._hd1003,P=H._hp22;if(!P)return HP22.base.tick.apply(this,arguments);
 if(b.dead){b._s4MiniSafe=false;delete H._hp22;return true;}H.clock+=dt;H.age+=dt;H.attackAge+=dt;P.t+=dt;b.fireCd=999;b._sba=null;
 // This encounter owns swept talon/head contact during its dive. Suppress the
 // generic whole-silhouette overlap, which would also make harmless wings and
 // the return flight lethal outside the announced corridor.
 b._s4MiniSafe=true;
 const C=hp22Cfg();
 if(P.phase==='perch'){
  P.angle*=Math.max(0,1-dt*9);const dx=P.perch.x-b.x,dy=P.perch.y-b.y,d=Math.hypot(dx,dy),speed=285;
  if(d>3){b.x+=dx/d*Math.min(d,speed*dt);b.y+=dy/d*Math.min(d,speed*dt);}else hp22Lock(b);
 }else if(P.phase==='tell'){
  P.angle=0;combatWarningTick(b,'predator-'+H.seq+'-'+P.passes,P.t,P.warm);
  if(P.t>=P.warm){P.phase='strike';P.t=0;P.previous={x:b.x,y:b.y};combatAudio0927(b,P.kind==='feathers'?'bossfireVileexistence':'jetDash',.5);hp22Log(b,'predator-release',{kind:P.kind});}
 }else if(P.phase==='strike'){
  if(P.kind==='feathers'){
   for(const L of P.lines)if(!L.issued){L.issued=true;const part=hd1003Part(b,L.id);if(!hd1003Live(b,part))continue;
    const Q=hd1003Muzzle(b,L.id),q=eShootT(Q.x,Q.y,L.aim,3.25+target17Rank()*.22,'s8pair',{owner:b,w:12,h:22,silent:true});
    if(q){q._heraldOwner1003=b;q._heraldPart1003=L.id;q._noArsenal=true;q._hp22Feather=true;q._hp22Born=efxClock;part.kick=3;}H.flashes.push({id:L.id,x:Q.x,y:Q.y,t:0});}
   if(P.t>.32){P.phase='recover';P.t=0;hp22Log(b,'predator-recovery',{seconds:C.recover});}
  }else{
   // Swept native part centres prevent fast dives tunnelling through a plane.
   // Head remains dangerous when the two claw modules have been destroyed.
   const ids=['gunL','gunR','head'].filter(id=>hd1003Live(b,hd1003Part(b,id))),before=ids.map(id=>hd1003Center(b,hd1003Part(b,id)));
   P.angle=clamp(P.flightAngle-Math.PI/2,-.70,.70);b.x+=Math.cos(P.flightAngle)*C.speed*dt;b.y+=Math.sin(P.flightAngle)*C.speed*dt;
   ids.forEach((id,i)=>{const Q=hd1003Center(b,hd1003Part(b,id)),A=before[i];for(const seat of seatList())withSeat(seat,()=>{
    if(!player.dead&&s81003Distance(player.x,player.y,{x:A.x,y:A.y,ex:Q.x,ey:Q.y})<(id==='head'?20:24))playerHit('Herald talon dive');});});
   if(P.t>VH*1.30/C.speed||b.y>VH+150||b.x<camLeftX()-200||b.x>camRightX()+200){P.phase='recover';P.t=0;hp22Log(b,'predator-recovery',{seconds:C.recover});}
  }
 }else{
  // Return is visibly separate and harmless; it is not another unannounced ram.
  P.angle*=Math.max(0,1-dt*7);b.x+=clamp(P.perch.x-b.x,-420*dt,420*dt);b.y+=clamp(P.perch.y-b.y,-460*dt,460*dt);
  if(P.t>C.recover&&Math.hypot(P.perch.x-b.x,P.perch.y-b.y)<4){
   if(++P.passes<P.total){P.perch.x=clamp(camLeftX()+viewW()*(P.side<0?.83:.17),camLeftX()+65,camRightX()-65);P.phase='perch';P.t=0;P.warm=C.warm;}
   else{b._s4MiniSafe=false;delete H._hp22;H.mode='rest';H.age=.40;H.lanes=[];}
  }
 }
 b._drawY=b.y;return true;
};
hd1003Pose=function(b,p){const Q=HP22.base.pose.apply(this,arguments),a=b?._hd1003?._hp22?.angle||0;if(!a)return Q;
 const x=Q.x-b.x,y=Q.y-b.y;return {...Q,x:b.x+x*Math.cos(a)-y*Math.sin(a),y:b.y+x*Math.sin(a)+y*Math.cos(a),a:Q.a+a};};
hd1003Blit=function(p,P,flash=0,alpha=1){
 const b=subBoss,B=CP22_ART.herald[p.id];if(!B||p.dead||!b?._hd1003||!XART.rdy(B.key))return HP22.base.blit.apply(this,arguments);
 const H=b._hd1003,mode=H._hp22?.phase,rate=mode==='strike'?22:mode==='tell'?12:7,
  f=Math.floor(H.clock*rate)%B.frames,c=B.cells[f],s=P.s/B.sourceScale;
 ctx.save();ctx.translate(P.x,P.y);ctx.rotate(P.a);ctx.globalAlpha*=alpha;ctx.imageSmoothingEnabled=false;
 ctx.drawImage(XART.get(B.key),...c,-B.pivot[0]*s,-B.pivot[1]*s,B.w*s,B.h*s);
 if(flash>0){const im=xartTint(B.key,'#ffffff',1);if(im){ctx.globalAlpha*=Math.min(1,flash*9);ctx.drawImage(im,...c,-B.pivot[0]*s,-B.pivot[1]*s,B.w*s,B.h*s);}}
 ctx.restore();return true;
};
heraldDeathDraw=function(b){const P=b?._hd1003?._hp22;
 if(P&&P.phase==='tell'&&!b.dead)for(const L of P.lines)if(!L.id||hd1003Live(b,hd1003Part(b,L.id)))combatWarningDraw(b,{...L,progress:P.t/P.warm,fieldOnly:true});
 return HP22.base.draw.apply(this,arguments);
};
ovSonicProjectileDraw=function(b){if(b?._hp22Feather){const B=CP22_ART.effects.soul_feather;if(B)return bf22EffectDraw(B,b.x,b.y,20,30,Math.atan2(b.vy,b.vx)-Math.PI/2,efxClock-b._hp22Born);}return HP22.base.projectile.apply(this,arguments);};
globalThis.BOF_HERALD_PREDATOR={state:HP22,start:hp22Start,lock:hp22Lock};
