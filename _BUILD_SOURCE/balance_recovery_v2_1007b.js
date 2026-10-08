'use strict';
/* Learnable counterplay: commit, let the slowest ship escape, reward a break.
   These clocks are shared by drawing and damage. No automatic hit forgiveness. */
const BALANCE_RECOVERY_1007B={
 profiles:{easy:{furnace:.76,punish:2.0,crossGap:.75,crossTell:.75},normal:{furnace:.84,punish:1.65,crossGap:.64,crossTell:.66},hard:{furnace:.92,punish:1.30,crossGap:.56,crossTell:.58},furious:{furnace:.96,punish:1.1,crossGap:.48,crossTell:.52}},
 base:{beam:fztBeam,cross:hc1007CrossStart,whirl:hammerWhirlLane,furnace:furnaceCombat,furnaceBreak:furnaceBreak,barrier:magmaWardBarrierDamage,node:stage4ShieldDestroyNode,war:er26WarTick}
};
function balanceRecoveryProfile(){return BALANCE_RECOVERY_1007B.profiles[diffKey]||BALANCE_RECOVERY_1007B.profiles.furious;}
hc1007CrossStart=function(){
 const C=BALANCE_RECOVERY_1007B.base.cross.apply(this,arguments),P=balanceRecoveryProfile();
 C.fade=.24;C.rewarn=P.crossTell;C.cycle=Math.max(C.cycle,C.on+C.fade+C.rewarn+P.crossGap);C.duration=C.cycle*6;
 return C;
};
hammerWhirlLane=function(b){
 const r=BALANCE_RECOVERY_1007B.base.whirl.apply(this,arguments),w=b._hammer.whirl,P=MANEUVER_SAFETY_1007.profiles[diffKey]||MANEUVER_SAFETY_1007.profiles.furious;
 if(w)w.warm=Math.max(w.warm,P.reaction+(102+10+P.pad)/(MANEUVER_SAFETY_1007.slowSpeed*1.35)+.10);
 return r;
};
furnaceCombat=function(b,dt){
 // The final copy retains its late-game pace. Stage 2 teaches the same pattern
 // with room to identify the cannon, rotating flame and exposed body.
 const pace=1;
 b._fz.at=Math.max(0,b._fz.at-dt*(1-pace));
 return BALANCE_RECOVERY_1007B.base.furnace(b,dt*pace);
};
furnaceBreak=function(b,key){
 const r=BALANCE_RECOVERY_1007B.base.furnaceBreak.apply(this,arguments);
 if(run.stage===2&&key!=='head'){furnaceClear(b);b._mwStun=Math.max(b._mwStun||0,balanceRecoveryProfile().punish);}
 return r;
};
magmaWardBarrierDamage=function(b){
 const active=b?._mwBarrier?.active,r=BALANCE_RECOVERY_1007B.base.barrier.apply(this,arguments);
 if(active&&!b._mwBarrier.active&&run.stage===2)b._mwStun=Math.max(b._mwStun||0,balanceRecoveryProfile().punish);
 return r;
};
stage4ShieldDestroyNode=function(b){
 const active=b?._s4war?.shield?.active,r=BALANCE_RECOVERY_1007B.base.node.apply(this,arguments);
 if(active&&!b._s4war.shield.active&&b._mr27){
  b._mr27.stun=Math.max(b._mr27.stun||0,balanceRecoveryProfile().punish);
  b._mr27.ram1002=null;hc1007Cancel(b);b._l23Beam=null;
  groundTargetingCancel(b);er26Set(b,'recover');b._er26.dur=Math.max(b._er26.dur,b._mr27.stun);
 }
 return r;
};
er26WarTick=function(b,dt){
 if(b._ship==='stormsovereign'&&b._mr27?.stun>0&&!b.dead){
  // Weapon loss already awarded this stun, but the damaged-weapon ram director
  // ignored it. Keep the attachments alive while pausing offensive attacks.
  b._mr27.ram1002=null;hc1007Cancel(b);b._l23Beam=null;b._er26.warnings=[];
  b.x+=clamp(er26Station(b,0)-b.x,-110*dt,110*dt);b.y+=clamp(b._er26.home-b.y,-220*dt,220*dt);
  stage4ShieldTick(b,dt);stage4CoreFormationTick(b,dt);b._drawY=b.y;
  return true;
 }
 return BALANCE_RECOVERY_1007B.base.war.apply(this,arguments);
};

// Stage 2's flame visibly vents between sweeps. The shared beam list drives both
// drawing and collision, so a vanished flame cannot leave an invisible hitbox.
function balanceFlameCycle(F){
 const rank=diffKey==='easy'?0:diffKey==='normal'?1:diffKey==='hard'?2:3;
 const on=[.55,.65,.72,.78][rank],gap=[.62,.50,.44,.40][rank],warn=[.50,.45,.40,.36][rank],fade=.14;
 const t=Math.max(0,F.at-(F.attack==='sweep'?1.05:1)),cycle=on+fade+gap+warn,p=t%cycle;
 return {p,on,gap,warn,fade,cycle};
}
fztBeam=function(F,x,y,a,len,width,kind){
 if(run.stage===2&&kind==='flame'&&['spin900','sweep','rotor'].includes(F.attack)){
  const C=balanceFlameCycle(F);
  if(C.p>=C.on+C.fade){
   if(C.p>=C.on+C.fade+C.gap)fztTell(F,x,y,a,len,(C.p-C.on-C.fade-C.gap)/C.warn);
   return;
  }
  if(C.p>C.on)width*=1-(C.p-C.on)/C.fade;
 }
 return BALANCE_RECOVERY_1007B.base.beam(F,x,y,a,len,width,kind);
};
