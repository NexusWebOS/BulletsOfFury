'use strict';
/* Learnable counterplay: commit, let the slowest ship escape, reward a break.
   These clocks are shared by drawing and damage. No automatic hit forgiveness. */
const BALANCE_RECOVERY_1007B={
 profiles:{easy:{punish:2.0,crossGap:.75,crossTell:.75},normal:{punish:1.65,crossGap:.64,crossTell:.66},hard:{punish:1.30,crossGap:.56,crossTell:.58},furious:{punish:1.1,crossGap:.48,crossTell:.52}},
 base:{beam:fztBeam,cross:hc1007CrossStart,whirl:hammerWhirlLane,furnaceBreak:furnaceBreak,barrier:magmaWardBarrierDamage,node:stage4ShieldDestroyNode,war:er26WarTick}
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
furnaceBreak=function(b,key){
 const phase=b._fz?.phase,r=BALANCE_RECOVERY_1007B.base.furnaceBreak.apply(this,arguments);
 if(run.stage===2&&key!=='head'){
  // A surviving arm must begin a fresh tell after the pause, never resume an
  // already-live flame. Phase transitions already select their next attack.
  if(b._fz.phase===phase)furnaceShieldBreak(b);else furnaceClear(b);
  b._mwStun=Math.max(b._mwStun||0,balanceRecoveryProfile().punish);
 }
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
  b._er26.mode='recover';b._er26.dur=Math.max(b._er26.dur||0,b._er26.t+b._mr27.stun);
  stage4ShieldTick(b,dt);er26CoreTick(b,dt);
  for(const d of b._s4war?.coreTurrets||[])if(d._pressure1002){d._pressure1002.aim=null;d._pressure1002.cd=Math.max(1,d._pressure1002.cd);}
  b._drawY=b.y;
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

/* Earned supplies use existing collectible art and collection rules. A boss
   ledger prevents regenerating parts or revisiting forms from farming drops. */
function balanceMilestone(b,id,shield=false,defer=false){
 if(!b||b._gp4Host)return false;
 const ledger=b._balanceRewards1007||(b._balanceRewards1007=new Set());
 if(ledger.has(id))return false;ledger.add(id);
 const reward={id,shield};
 if(defer)(b._balancePending1007||(b._balancePending1007=[])).push(reward);
 else balanceDropMilestone(b,reward);
 return true;
}
function balanceDropMilestone(b,reward){
 const x=clamp(b.x,camLeftX()+70,camRightX()-70),y=clamp(b.y+65,PLAY.y+120,VH-150);
 dropPowerup(x-(reward.shield?22:0),y,'weapon',true);
 if(reward.shield)dropPowerup(x+22,y,'shield',true);
}
const BALANCE_MILESTONE_BASE={break:furnaceBreak,node:stage4ShieldDestroyNode,hammer:hammerBossDamage,recovery:hammerRecoveryBreak,final:r30Break,tick:r30Tick};
furnaceBreak=function(b,key){
 const r=BALANCE_MILESTONE_BASE.break.apply(this,arguments);
 if(run.stage===2&&key!=='head')balanceMilestone(b,'furnace-'+key,diffKey==='easy'||diffKey==='normal');
 return r;
};
stage4ShieldDestroyNode=function(b){
 const live=b?._s4war?.shield?.active,r=BALANCE_MILESTONE_BASE.node.apply(this,arguments);
 if(run.stage===4&&live&&!b._s4war.shield.active)balanceMilestone(b,'generators',diffKey==='easy'||diffKey==='normal');
 return r;
};
hammerBossDamage=function(b){
 const hp=fr27Armor(b)?.hp||0,r=BALANCE_MILESTONE_BASE.hammer.apply(this,arguments);
 if(run.stage===5&&hp>0&&fr27Armor(b)?.hp<=0)balanceMilestone(b,'chromium-armor',diffKey==='easy'||diffKey==='normal');
 return r;
};
hammerRecoveryBreak=function(b){
 const charging=b?._hammer?.recovery?.status==='charging',r=BALANCE_MILESTONE_BASE.recovery.apply(this,arguments);
 if(run.stage===5&&charging&&b._hammer.recovery?.status!=='charging')balanceMilestone(b,'recovery-interrupt',true);
 return r;
};
r30Break=function(b){
 const J=j3State(b),earned=J&&b._r30.mode==='fight'&&b.hp<=0;
 const id=J&&(J.encounter<2?'phase-'+J.encounter:'form-'+J.active);
 const r=BALANCE_MILESTONE_BASE.final.apply(this,arguments);
 if(earned)balanceMilestone(b,id,true,true);
 return r;
};
r30Tick=function(b){
 const r=BALANCE_MILESTONE_BASE.tick.apply(this,arguments);
 if(b?._balancePending1007?.length&&b._r30?.mode==='fight'&&!b.dead&&!player.dead){
  for(const reward of b._balancePending1007.splice(0))balanceDropMilestone(b,reward);
 }
 return r;
};

// Mid-campaign bosses must still finish after a weapon-loss recovery. Keep the
// complete attack/phase book and budget hull, armor and barrier consistently.
const BALANCE_HP_1007={2:{easy:1,normal:.68,hard:.68,furious:.72},4:{easy:1,normal:.76,hard:.76,furious:.80},5:{easy:1,normal:.76,hard:.72,furious:.70}};
function balanceScalePool(o,hp,max,mul){
 if(!o||!Number.isFinite(o[hp]))return;
 o[hp]=o[hp]>0?Math.max(1,Math.round(o[hp]*mul)):0;
 if(max&&Number.isFinite(o[max]))o[max]=Math.max(1,Math.round(o[max]*mul));
}
function balanceEncounterBudget(b){
 if(!b||b._balanceHealth1007!=null||b._gp4Host||b._r30)return;
 const stage=b._furnace?2:b._ship==='stormsovereign'?4:b._hammer?5:0;
 if(!stage||run.stage!==stage)return;
 const mul=BALANCE_HP_1007[stage][diffKey]||1;b._balanceHealth1007=mul;
 if(mul===1)return;
 balanceScalePool(b,'hp','maxhp',mul);
 if(b._fz?.hpSync)for(const key of ['left','right','body','head']){
  balanceScalePool(b._fz.pools,key,null,mul);balanceScalePool(b._fz.max,key,null,mul);
 }
 balanceScalePool(b._mwBarrier,'hp','maxhp',mul);
 for(const p of b._mr27?.parts||[])balanceScalePool(p,'hp',Number.isFinite(p.maxhp)?'maxhp':'max',mul);
 balanceScalePool(fr27Armor(b),'hp','max',mul);
}
const BALANCE_SPAWN_1007=spawnBoss;
spawnBoss=function(){const r=BALANCE_SPAWN_1007.apply(this,arguments);balanceEncounterBudget(boss);return r;};

// Stage 2's miniboss owns the pressure budget while it is alive. Existing warned
// firewalls/vents finish normally; only the NEXT environmental event waits.
// After victory there is a three-second breath before the next warning begins.
const BALANCE_ENVIRONMENT_BASE={weather:wfxUpdate,vents:s2VentTick};
function balanceStage2Duel(){return run.stage===2&&subBossActive&&subBoss&&!subBoss.dead;}
wfxUpdate=function(dt){
 if(balanceStage2Duel()&&wfx)wfx.fireCd=Math.max(wfx.fireCd||0,3+dt);
 return BALANCE_ENVIRONMENT_BASE.weather.apply(this,arguments);
};
s2VentTick=function(dt){
 if(balanceStage2Duel())s2VentT=Math.max(s2VentT,3+dt);
 return BALANCE_ENVIRONMENT_BASE.vents.apply(this,arguments);
};
