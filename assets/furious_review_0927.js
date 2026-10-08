"use strict";
/* Mike's full-game Furious review. Keep authored damage tells independent of
   difficulty-scaled aircraft movement; no additional Retina spam. */
const FR27_BASE={spawn:spawnEnemy,aiBegin:ai27Begin,aiEnd:ai27End};
function fr27Difficulty(){return diffKey==='furious'||diffKey==='insanity'?2:diffKey==='hard'?1:0;}
function fr27ArrivalReady(e){
 if(e._modJet){const gun=e._modJet==='desert'?'rotary_module_0':(e._modJet==='black'?'missile':'laser')+'_module';const a=XART.rdy('overhaul_jet_'+e._modJet+'_hull'),b=XART.rdy('overhaul_jet_'+gun);return a&&b;}
 if(run.stage===8&&e._s8mega)return XART.rdy('fr27_realm_fleet');
 return true;
}
spawnEnemy=function(type,x,y,opt){
  const count=enemies.length,result=FR27_BASE.spawn.apply(this,arguments);
  for(const e of enemies.slice(count)){
    if(!e||e.dead||e._boss||e._amini||isSetPiece(e))continue;
    // At zoomed-out resolutions y=-30 is INSIDE the viewport. Spawn beyond
    // the actual visible top, including the unit's full authored silhouette.
    if(y<=PLAY.y&&e.x>=0&&e.x<=worldWidth()){
      const top=viewTopY()-Math.max(e.h||30,e._drawH||0)*.65-28;
      const dy=Math.min(0,top-e.y);e.y+=dy;
      if(Number.isFinite(e._drawY))e._drawY+=dy;
      e._spawnY=e.y;e._frArrival=true;
    }
    if(ai27Air(e))e._frFlight=true;
    fr27ArrivalReady(e);
  }
  return result;
};
ai27Begin=function(e,dt){
  if(e&&!e.dead)e._frPrevious={x:e.x,y:e.y,dt};
  return FR27_BASE.aiBegin(e,dt);
};
ai27End=function(e,previous){
  FR27_BASE.aiEnd(e,previous);
  const p=e&&e._frPrevious;if(!p||e.dead||e._dyingT!=null)return;
  if(e._frArrival&&!fr27ArrivalReady(e)){e.x=p.x;e.y=p.y;return;}
  if(e._frFlight&&!e._frozen&&!e._mercuryLock){
    const n=fr27Difficulty(),mul=[1,1.32,1.68][n];
    let dx=(e.x-p.x)*mul,dy=(e.y-p.y)*mul;
    // The authored route may reset to a destination on its first frame. Fly
    // there at a bounded speed instead of materializing in the playfield.
    const d=Math.hypot(dx,dy),cap=[190,255,335][n]*p.dt;
    if(d>cap&&d>0){dx*=cap/d;dy*=cap/d;}
    e.x=p.x+dx;e.y=p.y+dy;
    if(Number.isFinite(e._drawY))e._drawY=e.y;
    if(e.y>viewTopY()+Math.max(e.h||30,30))e._frArrival=false;
  }
};
Object.assign(FR27_BASE,{hammerTick:hammerBossTick,hammerDraw:hammerBossDraw,hammerDamage:hammerBossDamage,recovery:hammerRecoveryTick,breakRecovery:hammerRecoveryBreak,health:bossHealthFraction,healthVisible:bossHealthVisible,gauge:hammerChromiumGaugeFill,head:hammerHeadPoint});
for(const name of ['chromium_actions','realm_terrain','realm_fleet'])XART._src['fr27_'+name]='assets/game/shared/combat/furious_review_0927/'+name+'.png';
function fr27Cell(key,col,row,x,y,w,h,alpha,tint){
 if(!XART.rdy(key))return false;const im=tint?xartTint(key,tint,1):XART.get(key);if(!im)return false;const W=im.width||im.naturalWidth,H=im.height||im.naturalHeight;
 const rows=key==='fr27_chromium_actions'?[0,345,680,986,1230]:[0,285,548,899,1254];
 const sx=Math.floor(col*W/4),ex=Math.floor((col+1)*W/4),sy=rows[row]*H/rows[4],eh=(rows[row+1]-rows[row])*H/rows[4];
 ctx.save();ctx.globalAlpha=alpha==null?1:alpha;ctx.imageSmoothingEnabled=false;ctx.drawImage(im,sx,sy,ex-sx,eh,x-w/2,y-h/2,w,h);ctx.restore();return true;
}
function fr27Armor(b){return b&&b._hammer&&b._hammer.frArmor;}
/* ⚠ 0929 - Mike: "when I shoot the hammer when he charges it to restore his energy it is still not breaking and
   bringing him to his stun state and he just keeps the shield up and keeps doing it. This is bad."
   Measured in Chromium on Hard/Furious before this pass (_BUILD_SOURCE/probe_hammer_heal_break_0929.py):
   - the energy wall swallowed 349-452 of the pilot's rounds, so held gunfire never reached the healing hammer;
   - a break sent him to fr_stun, which nothing drew as a stun - he stood in his IDLE pose holding the hammer -
     with the shield still up (barrier 3.1: every body round did 0) ...
   - ... and 2.8 s later fr_stun called fr27Restore: ANOTHER heal. Every stun ended in a heal, the disarm stun
     included, because hammer_stun/storm_stun were converted into fr_stun as well.
   Now rounds in the raised hammer's own column pass the wall while he heals, a break is the authored stun
   (the base storm stun's pose, static and core burst, same 4 s) with the shield DOWN and double body damage,
   and a broken heal is over: he gets back up and fights on. Checkpoint heals still happen once each. */
const FR27_STUN_T=4,FR27_HAMMER_LANE=40;
/* ⚠ 0928 REBUILD (Mike: "the chromium armor activate sequence was horrible and needs to be re-done").
   Measured before: 3.4 s of a SEPARATE sheet (fr27_chromium_actions row 0) - a silver robot with a
   silver hammer that is not the boss - stepped at four frames, then a pop to the real blue boss; the
   HP bar emptied and refilled as if he had healed; the caption sat in the HUD band. Now the REAL boss
   stays on screen and the engine's own chromium treatment grows the armor out from his chest reactor
   (h.empowered + empowerLevel: the pixel-stepped core mask with its bright leading ring), sparks run
   over the plating, the grey armor gauge fills as it spreads, and it LOCKS with a blue blast, a shock
   ring and shake that also cover the palette hand-off back to the plate. 2.1 s. No new art. */
const FR27_ACT={brace:.35,plate:1.75,end:2.1};
function fr27BeginArmor(b){
 const h=b._hammer,A=h.frArmor={hp:b.maxhp,max:b.maxhp,t:0,active:true,half:false,checkpoints:[],barrier:0,rage:false};
 h.throw=null;h.bombs=[];h.pillars=[];b._noHit=true;hammerState(b,'fr_activation');
 h.empowered=true;h.empowerLevel=0;h.chromiumT=.75;h.frAct={locked:false,spark:0,y0:b.y};
 if(typeof fxBurst==='function')fxBurst(b.x,b.y,70,{color:'#9fe9ff',rings:1,chunks:0,sparks:8});
 (Audio.SFX.bossWeaponCharge||Audio.SFX.lightning||function(){})();
 return A;
}
function fr27ActivationTick(b,dt){
 const h=b._hammer,A=fr27Armor(b),F=h.frAct||(h.frAct={locked:false,spark:0,y0:b.y});
 h.t+=dt;b._noHit=true;
 // hold the SILVER tone (1 of the three chromium tones): the cycle's green read as a different metal
 h.chromiumT=.75+(h.t*.45)%.6;
 const t=h.t,p=clamp((t-FR27_ACT.brace)/(FR27_ACT.plate-FR27_ACT.brace),0,1);
 // brace: a short dip, then the plate rides back up as the armor spreads
 b.y=F.y0+Math.sin(clamp(t/FR27_ACT.plate,0,1)*Math.PI)*7;
 if(!F.locked){h.empowered=true;h.empowerLevel=p*p*(3-2*p);
  F.spark-=dt;if(t>FR27_ACT.brace&&F.spark<=0&&typeof fxBurst==='function'){F.spark=.16;
   const a=h.chromiumT*5.3,r=24+62*h.empowerLevel;fxBurst(b.x+Math.cos(a)*r,b.y+Math.sin(a)*r*.9,18,{color:HAMMER_CHROMIUM_COLORS[hammerChromiumTone(b)],rings:0,chunks:0,sparks:6});}
  if(t>=FR27_ACT.plate){F.locked=true;h.empowered=false;h.empowerLevel=0;b.y=F.y0;
   if(typeof fxBurst==='function'){fxBurst(b.x,b.y,150,{color:'#dff6ff',rings:2,chunks:0,sparks:22});fxBurst(b.x,b.y-10,60,{color:'#9fe9ff',rings:1,chunks:0,sparks:10});}
   b.flash=Math.max(b.flash||0,.18);shake=Math.max(shake,9);
   (Audio.SFX.shieldUp||Audio.SFX.shieldBreakCombat||Audio.SFX.expBig||function(){})();
   if(A)A.capT=1.3;}
 }
 if(t>=FR27_ACT.end){A.activated=true;b._noHit=false;h.frAct=null;hammerState(b,'hammer');}
}
function fr27Restore(b,fraction,critical,barrier){
 const h=b._hammer,A=fr27Armor(b);
 h.frResume=h.mode;   // 0929: where the fight goes back to if the player breaks this heal (hammerStormStart makes it 'storm')
 // 0929: HAMMER draws its dance crew, not the boss, while its mode is 'dance' - so a heal that starts mid-dance hands
 // the fight back to 'attack', or the charge and the stun that follows it would be drawn as dancing.
 {const d=b._hammerTime;if(d&&d.mode==='dance'){d.mode='attack';d.t=0;}}
 hammerStormStart(b);
 h.recovery.amount=b.maxhp*fraction;h.recovery.duration=critical?5:2.25;h.recovery.elapsed=0;h.recovery.applied=0;
 h.recovery.fr=true;h.recovery.armor=!!(A&&A.hp>0);h.recovery.critical=!!critical;
 h.recovery.coreHP=critical?Math.max(36,h.hammerMax*.32):Math.max(24,h.hammerMax*.18);
 h.recovery.coreMax=h.recovery.coreHP;
 h.recovery.frDamage=0;h.recovery.granted=0;h.frRecovery=true;h.frCritical=!!critical;
 if(A)A.barrier=barrier?6:0;
 b._noHit=false;
}
function fr27Reflect(b,A,dt){
 if(A.barrier<=0)return;A.barrier=Math.max(0,A.barrier-dt);A.reflectCD=Math.max(0,(A.reflectCD||0)-dt);
 const y=b.y+85,half=150,healing=b._hammer&&b._hammer.recovery&&b._hammer.recovery.status==='charging';
 // 0929: the raised hammer's own column - the same +/-40 px bossHitTest gives the healing hammer
 const lane=healing&&hammerWeaponTargetable(b)?hammerHeadPoint(b).x:null;
 for(const q of pBullets){if(q.dead||q.y<y-26||q.y>y+26||Math.abs(q.x-b.x)>half||q.vy>=0)continue;
  // 0928: while he heals, a missile passes the wall. 0929: so does any round aimed at the hammer - shooting the
  // hammer is the counter Mike asked for; body shots beside it are still turned back.
  if(healing&&(hammerMissile(q)||(lane!=null&&Math.abs(q.x-lane)<FR27_HAMMER_LANE)))continue;
  q.dead=true;if(A.reflectCD<=0){A.reflectCD=.09;const a=Math.PI/2+clamp((q.x-b.x)/half,-1,1)*.55;
   const missile=/miss|rocket/.test(q.kind||''),z=eShootT(q.x,y+28,a,4.2,missile?'s4rocket':'eglaser',{w:missile?12:8,h:missile?28:18,silent:true});z._hammerLaser=!missile;}
 }
}
function fr27HammerAim(q,target){
 const owner=target&&(target._retinaOwner||target),A=fr27Armor(owner);
 if(!A||owner!==boss||owner.dead||A.barrier<=0||!hammerMissile(q)){
  q._frHammerRoute=null;return null;
 }
 const y=owner.y+85,half=150,margin=50;
 let route=q._frHammerRoute;
 if(!route||route.owner!==owner){
  // Keep the selected component; steer outside the wall before turning inward.
  const l=camLeftX()+20,r=camRightX()-20;
  let side=q.x<owner.x?-1:q.x>owner.x?1:(q.side<0?-1:1);
  if(owner.x+side*(half+margin)<l||owner.x+side*(half+margin)>r)side=-side;
  route=q._frHammerRoute={owner,side,phase:q.y<y-58?2:0};
 }
 const x=owner.x+route.side*(half+margin);
 if(route.phase===0&&Math.abs(q.x-x)<20)route.phase=1;
 if(route.phase===1&&q.y<y-58)route.phase=2;
 if(route.phase===2){q._frHammerFlank=owner;return null;}
 return {x,y:route.phase===0?Math.min(q.y-24,y+76):y-85};
}
hammerRecoveryTick=function(b,dt){
 const h=b._hammer,R=h.recovery,A=fr27Armor(b);if(!R||!R.fr)return FR27_BASE.recovery(b,dt);
 if(R.status!=='charging'||b.dead)return;R.elapsed=Math.min(R.duration,R.elapsed+Math.max(0,dt));
 // Only newly accrued healing is granted: body damage is real damage, never undone by a catch-up heal.
 const wanted=R.amount*R.elapsed/R.duration,gain=Math.max(0,wanted-R.applied);R.applied=wanted;
 const before=R.armor&&A?A.hp:b.hp;
 if(R.armor&&A)A.hp=Math.min(A.max,A.hp+gain);else b.hp=Math.min(b.maxhp,b.hp+gain);
 R.granted+=(R.armor&&A?A.hp:b.hp)-before;
 if(R.elapsed>=R.duration){R.status='complete';R.finishedAt=h.t;h.hammerHP=h.hammerMax;}
};
hammerRecoveryBreak=function(b){
 const h=b._hammer,R=h.recovery,A=fr27Armor(b);if(!R||!R.fr)return FR27_BASE.breakRecovery(b);
 R.status='cancelled';R.revoked=R.granted||0;
 if(R.armor&&A)A.hp=Math.max(0,A.hp-R.revoked);else b.hp=Math.max(1,b.hp-R.revoked);
 R.applied=0;h.coreBurst={...hammerHeadPoint(b),t:0};h.frCriticalInterrupted=!!R.critical;
 {const hd=hammerHeadPoint(b),first=explosions.length;explode(hd.x,hd.y,84,'blue');for(let i=first;i<explosions.length;i++)explosions[i].chromiumTone=hammerChromiumTone(b);shake=Math.max(shake,10);}
 h.hammerDestroyed=true;h.hammerHP=0;h.throw=null;h.stormWaves=[];h.frRecovery=false;
 h.empowered=false;h.empowerLevel=0;h.charged=false;   // 0929: he loses the charge, as the base break does
 if(A){A.barrier=0;A.stunCritical=!!R.critical;}      // 0929: the shield DROPS - he is stunned, not protected (was 3.1)
 hammerState(b,'fr_stun');(Audio.SFX.shieldBreakCombat||Audio.SFX.expBig||function(){})();
};
/* 0929: a broken restoration is over. He gets back up into the fight he left - he does not start another heal.
   From the storm phase that is the base stun's own get-up (the hammer re-forms from the grip); otherwise the
   base disarm stun's (leap_reset with the combo armed), which HAMMER's own tick turns into its dance. */
function fr27Resume(b){
 const h=b._hammer,A=fr27Armor(b),mode=h.frResume;h.frResume=null;
 if(A)A.barrier=0;h.empowered=false;h.empowerLevel=0;h.throw=null;h.knockedHammer=null;
 if(mode==='storm'){h.mode='storm';h.hammerDestroyed=true;hammerState(b,'storm_rebuild');return;}
 h.hammerDestroyed=false;h.hammerHP=h.hammerMax;h.mode='hammer';h.followCount=0;h.comboPending=true;
 hammerState(b,'leap_reset');(Audio.SFX.bossPhase||function(){})();
}
hammerBossDamage=function(b,dmg){
 const h=b._hammer,A=fr27Armor(b);if(!A)return FR27_BASE.hammerDamage(b,dmg);
 if(h.state==='fr_activation'){b._hammerModuleHit=null;return 0;}
 const hammerHit=b._hammerModuleHit==='hammer';
 if(hammerHit&&h.recovery?.status==='charging'&&dmg>0){
  // A deliberately locked rocket is the immediate recovery counter. Passive
  // weapons still deplete the exposed core normally.
  if(hammerMissile(_dmgBullet)){   // 0928: every player missile kind, locked or not (was gmiss/nukem/retinaMissile only)
   b._hammerModuleHit=null;hammerRecoveryBreak(b);return 0;
  }
  return FR27_BASE.hammerDamage(b,dmg);
 }
 if(A.barrier>0&&!hammerHit&&_dmgBullet?._frHammerFlank!==b){b._hammerModuleHit=null;return 0;}
 if(h.state==='fr_twirl'){const hit=b._hammerModuleHit;b._hammerModuleHit=null;if(hit==='hammer'){h.frTwirlHits=(h.frTwirlHits||0)+dmg;if(h.frTwirlHits>=h.hammerMax*.30){h.frCriticalInterrupted=true;A.stunCritical=true;A.barrier=0;h.hammerDestroyed=true;hammerState(b,'fr_stun');}}return 0;}
 // 0929: the stun is the punish window - double body damage, as the base stuns give (armor still takes it first)
 const dealt=FR27_BASE.hammerDamage(b,dmg)*(h.state==='fr_stun'?2:1);
 if(A.hp>0&&dealt>0){const blocked=Math.min(A.hp,dealt);A.hp-=blocked;A.flash=.15;if(A.hp<=0){A.active=false;spawnShockRing(b.x,b.y,180,'comet');(Audio.SFX.shieldBreakCombat||Audio.SFX.expBig||function(){})();}return dealt-blocked;}
 return dealt;
};
hammerBossTick=function(b,dt){
 const h=b._hammer;let A=fr27Armor(b);
 const passwordReady=!b._hammerTime||b._hammerTime.mode==='attack';
 if(!A&&h.balance0922&&!b._noHit&&passwordReady&&!['flyby','return','unfold'].includes(h.state))A=fr27BeginArmor(b);
 if(!A)return FR27_BASE.hammerTick(b,dt);
 A.t+=dt;A.flash=Math.max(0,(A.flash||0)-dt);fr27Reflect(b,A,dt);
 if(h.state==='fr_activation'){fr27ActivationTick(b,dt);return;}
 if(A.capT>0)A.capT=Math.max(0,A.capT-dt);
 if(h.state==='fr_stun'){
  h.t+=dt;h.chromiumT=(h.chromiumT||0)+dt;A.barrier=0;
  if(h.t>=FR27_STUN_T){
   if(A.stunCritical){A.stunCritical=false;A.rage=true;A.barrier=0;h.rage=999;h.hammerDestroyed=false;h.hammerHP=h.hammerMax;h.frResume=null;h.mode='hammer';h.followCount=0;h.comboPending=false;hammerTarget(b);hammerState(b,'warn');}
   else fr27Resume(b);   // 0929: was fr27Restore(b,.10,false,true) - a second heal after every stun
  }return;
 }
 if(h.state==='fr_twirl'){
  h.t+=dt;combatWarningTick(b,'chromium-final-slam',Math.min(h.t,2.2),2.2);
  if(h.t>=2.2&&!h.frSlam){h.frSlam=true;spawnShockRing(b.x,b.y+65,190,'comet');explode(b.x,b.y+65,95,'blue');for(let i=0;i<10;i++)hammerEnergyBomb(b.x,b.y+65,TAU*i/10,4.1);(Audio.SFX.hammerImpact||function(){})();}
  if(h.t>=2.85)fr27Restore(b,.50,true,false);return;
 }
 if(h.frRecovery&&h.state==='storm_raise'){
  h.t+=dt;h.chromiumT=(h.chromiumT||0)+dt;h.empowered=true;h.empowerLevel=clamp(h.t/1.25,0,1);
  if(h.t>1.0)hammerRecoveryTick(b,dt);
  if(h.recovery.status==='complete'&&h.t-h.recovery.finishedAt>.35){h.frRecovery=false;A.barrier=0;h.mode='hammer';h.phasePending=false;hammerWhirlStart(b);}return;
 }
 /* 0929: the base stuns are no longer turned into fr_stun (which put the shield up and ended in a heal). They
    run as authored - shield down, double damage, their own get-up. In the red rage the disarm stun's get-up
    goes back to the rage jumps, as the critical stun does, instead of the base's phase-two hand-off. */
 if(['hammer_exposed','hammer_stun','storm_stun','storm_rebuild'].includes(h.state))A.barrier=0;
 if(A.rage&&((h.state==='hammer_stun'&&h.t+dt>=5)||(h.state==='hammer_exposed'&&h.t+dt>=3))){
  h.knockedHammer=null;h.hammerDestroyed=false;h.hammerHP=h.hammerMax;h.followCount=0;h.comboPending=false;hammerTarget(b);hammerState(b,'warn');return;}
 // 0929: in HAMMER only between moves of the fight itself - never inside a music break or the intro
 const safe=['hammer','shield','leap_reset','storm_idle','chain_cool','hammer_catch'].includes(h.state)&&(!b._hammerTime||['attack','dance'].includes(b._hammerTime.mode));
 if(safe&&!A.half&&A.hp>0&&A.hp<=A.max*.50){A.half=true;fr27Restore(b,.10,false,true);return;}
 if(safe&&A.hp<=0){
  const ratio=b.hp/b.maxhp,threshold=[.75,.50,.35,.15].find(v=>ratio<=v&&!A.checkpoints.includes(v));
  if(threshold!=null){A.checkpoints.push(threshold);if(threshold===.15){h.frSlam=false;h.frTwirlHits=0;hammerState(b,'fr_twirl');}else fr27Restore(b,.10,false,true);return;}
 }
 if(A.rage&&h.state==='leap_reset'){
  h.t+=dt;h.followCount=0;h.phasePending=false;
  const u=clamp(h.t/.75,0,1),ease=u*u*(3-2*u);b.x=lerp(h.ox,(camLeftX()+camRightX())/2,ease);b.y=lerp(h.oy,VH*.34,ease);
  // Hold the actual recovery pose before the next full-speed, fully warned slam.
  if(h.t>=({easy:1.5,normal:1.25,hard:1.1,furious:.95,insanity:.90}[diffKey]||1.25)){hammerTarget(b);hammerState(b,'warn');}return;
 }
 if(A.rage)h.phasePending=false;
 FR27_BASE.hammerTick(b,dt);
};
hammerHeadPoint=function(b){
 const h=b&&b._hammer;if(h&&h.state==='fr_twirl'){const f=Math.floor(h.t*(7+h.t*5))%4;return{x:b.x+[0,92,0,-92][f],y:b.y+[-112,-10,80,-10][f]};}
 return FR27_BASE.head(b);
};
hammerBossDraw=function(b){
 const h=b._hammer,A=fr27Armor(b);if(!A)return FR27_BASE.hammerDraw(b);
 const s=h.state;let drawn=false;
 if(s==='fr_activation'){ /* the real boss, in his idle pose, with the chromium spreading over it */
  /* the storm-idle reel is the standing pose that routes through hammerChromiumPoseDraw, which is
     what carries the empowered core-out armor mask; the ordinary idle pose does not */
  if(typeof repair30ChromiumActivationDraw==='function')drawn=repair30ChromiumActivationDraw(b);
  else{const mode=h.mode;h.state='storm_idle';h.mode='storm';try{FR27_BASE.hammerDraw(b);}finally{h.state='fr_activation';h.mode=mode;}drawn=true;}}
 else if(s==='fr_twirl')drawn=fr27Cell('fr27_chromium_actions',h.t<2.2?Math.floor(h.t*(7+h.t*5))%4:Math.min(3,Math.floor((h.t-2.2)/.65*4)),h.t<2.2?1:2,b.x,b.y,252,258,1);
 /* 0929: fr_stun IS his stun, so it draws as one - the base storm stun's authored pose (hit, stunned, getting up),
    its static and the hammer-core burst, on the same 4 s clock. Nothing drew fr_stun before: he stood in his
    idle pose, hammer in hand, which read as "the heal did not break". */
 else if(s==='fr_stun'){const d=b._hammerTime,dm=d&&d.mode;if(d)d.mode='attack';   // HAMMER draws the boss only in 'attack'
  h.state='storm_stun';try{FR27_BASE.hammerDraw(b);}finally{h.state='fr_stun';if(d)d.mode=dm;}drawn=true;}
 if(!drawn){ctx.save();if(A.rage)ctx.filter='sepia(1) saturate(5) hue-rotate(315deg)';FR27_BASE.hammerDraw(b);ctx.restore();}
 if(A.hp>0&&s!=='fr_activation'){ctx.save();ctx.globalCompositeOperation='lighter';ctx.globalAlpha=.13+.06*Math.sin(A.t*12);archEffectBlit(9,b.x,b.y,115,A.t*1.7,.7);ctx.restore();}
 if(A.barrier>0)fr27Cell('fr27_chromium_actions',Math.floor(A.t*14)%4,3,b.x,b.y+67,315,120,.85);
 if(s==='fr_twirl'&&h.t<2.2)combatWarningDraw(b,{x:b.x,y:b.y+65,ex:b.x,ey:VH,progress:h.t/2.2,width:260,alpha:.32});
 if(s==='fr_activation'||A.capT>0){const k=s==='fr_activation'?clamp((h.t-FR27_ACT.brace)/.4,0,1):clamp(A.capT/.4,0,1);
  campText('CHROMIUM ARMOR',b.x,Math.min(VH*.62,b.y+118),14,'#dff6ff',k);}
};
bossHealthFraction=function(b){return FR27_BASE.health(b);};   // 0928: the HP bar no longer empties and refills during the activation
// Draw a second steel fill on the very same authored gauge geometry; the base HP stays underneath.
const FR27_GAUGE=drawHealthBarArt;
drawHealthBarArt=function(kind,frac,cx,cy,w,inWorld,lagKey){
 const result=FR27_GAUGE.apply(this,arguments),A=kind==='boss'&&fr27Armor(boss);if(!result||!A)return result;
 const h=boss._hammer,ratio=h.state==='fr_activation'?clamp((h.t-FR27_ACT.brace)/(FR27_ACT.plate-FR27_ACT.brace),0,1):A.hp/A.max;
 if(ratio<=0||!XART.rdy('bmbar_fill_grey'))return result;
 const s=w/BMBAR.frameW,O=BMBAR.boss,x=Math.round(cx-w/2)+O.dx*s,y=Math.round(cy-BMBAR.frameH*s/2)+O.dy*s;
 ctx.save();if(inWorld&&typeof camX==='number')ctx.translate(camX,0);ctx.beginPath();ctx.rect(x,y,O.w*s*ratio,O.h*s);ctx.clip();ctx.drawImage(XART.get('bmbar_fill_grey'),x,y,O.w*s,O.h*s);ctx.globalCompositeOperation='lighter';ctx.globalAlpha=.12+.12*(.5+.5*Math.sin(A.t*9));ctx.drawImage(XART.get('bmbar_fill_grey'),x,y,O.w*s,O.h*s);ctx.restore();return result;
};
Object.assign(FR27_BASE,{play:updatePlay,wing:s6WingTick,rebelTick:rebelSquadTick,rebelDamage:rebelSquadDamage,rebelDraw:rebelSquadDraw,bg:drawBG,weaponTargetable:hammerWeaponTargetable});
hammerWeaponTargetable=function(b){return b?._hammer?.state==='fr_twirl'||FR27_BASE.weaponTargetable(b);};
s6WingRadioPages=function(L){return[{text:L.full,dur:L.full.length/36+2.5}];};
s6WingRadioDraw=function(){
 if(!s6WingRadioVisible())return;const L=s6Wing.line,count=Math.min(L.full.length,Math.floor(L.t*36)),key=L.who.toLowerCase();
 dlgBox({who:L.who,full:L.full,shown:L.full.slice(0,count),portrait:key,portraitKey:REBEL_KEYS.includes(key)?'rr_portrait_'+key:undefined,pw:VW*.72,tint:'#87ddff'});
};
function fr27ChooseRoute(W,route){W.autoRoute=route;W.frBank=0;W.frStory=0;W.frChoice=null;Input.clearTaps();}
function fr27RouteInput(W){
 const C=W.frChoice||(W.frChoice={side:'left',t:0,mouse:false});C.t+=1/60;
 if(Input.menuLeft()){C.side='left';Audio.SFX.blip();}if(Input.menuRight()){C.side='right';Audio.SFX.blip();}
 const m=Input.mouse||{},over=m.y>VH*.42&&m.y<VH*.61&&m.x>VW*.08&&m.x<VW*.92;
 if(m.down&&!C.mouse&&over&&C.t>.2){C.side=m.x<VW/2?'left':'right';fr27ChooseRoute(W,C.side);}
 C.mouse=!!m.down;
 if(C.t>.2&&Input.menuConfirm())fr27ChooseRoute(W,C.side);
}
s6WingChoiceDraw=function(){
 const W=s6Wing;if(!W||!W.choice||W.route)return;const C=W.frChoice||{side:'left'};
 ctx.save();worldXformEscape();ctx.fillStyle='rgba(0,3,12,.72)';ctx.fillRect(0,0,VW,VH);
 dialogueFrameDraw('FURY WING','#8edfff',VW*.06,VH*.30,VW*.88,VH*.35);
 campText('CHOOSE YOUR PURSUIT',VW/2,VH*.355,18,'#fff0b0');
 for(const [i,side,name]of [[0,'left','HARRIER'],[1,'right','REBEL FURY']]){
  const x=VW*(i?.72:.28),selected=C.side===side;
  ctx.fillStyle=selected?'rgba(53,113,159,.65)':'rgba(2,12,24,.85)';ctx.fillRect(x-VW*.185,VH*.43,VW*.37,VH*.13);
  ctx.strokeStyle=selected?'#fff0aa':'#426b88';ctx.lineWidth=selected?2:1;ctx.strokeRect(x-VW*.185,VH*.43,VW*.37,VH*.13);
  campText(name,x,VH*.485,15,selected?'#fff4b7':'#b0c8de');
  campText(side.toUpperCase(),x,VH*.535,10,'#83dbff');
 }
 controlHintRow([['pad_dpad','CHOOSE'],['pad_a','CONFIRM']],VH*.615,VW/2,VW*.8,20);ctx.restore();
};
s6WingTick=function(dt){
 const W=s6Wing;FR27_BASE.wing(dt);if(!W||!W.route)return;
 if(W.frBank!=null)W.frBank=Math.min(2.8,W.frBank+dt);
 if(W.route==='right'&&!bossActive){const t=W.routeFightT||0;
  const beats=[['DECKER','THAT IS VOSS AND HIS OLD UNIT. THEY TOOK THE GEAR WE LEFT AT THE FORWARD DEPOT.'],['COLE','HOTWIRE AND PHOENIX WARNED US ABOUT THEM BEFORE THEIR MISSION. WE NEVER HEARD FROM EITHER PILOT AGAIN.'],[_pilotKey().toUpperCase(),'THEN WE GET SOME ANSWERS. COVER ME.']];
  const at=[1,10,21],i=W.frStory||0;if(i<beats.length&&t>=at[i]){W.frStory=i+1;s6WingSay(...beats[i]);}
 }
};
updatePlay=function(dt){
 if(run.stage===6&&s6Wing?.choice&&!s6Wing.route&&!s6Wing.autoRoute){fr27RouteInput(s6Wing);if(!s6Wing.autoRoute)return;}
 return FR27_BASE.play(dt);
};
drawBG=function(dt){
 const W=run.stage===6?s6Wing:null,bank=W&&W.route&&W.frBank<2.8?Math.sin(W.frBank/2.8*Math.PI)*(W.route==='left'?1:-1)*.075:0;
 if(!bank)return FR27_BASE.bg(dt);ctx.save();ctx.translate(worldWidth()/2,VH/2);ctx.rotate(bank);ctx.scale(1.12,1.12);ctx.translate(-worldWidth()/2,-VH/2);FR27_BASE.bg(dt);ctx.restore();
};
bossHealthVisible=function(b){if(b?._rebels)return false;return FR27_BASE.healthVisible(b);};
rebelSquadTick=function(b,dt){
 const R=b._rebels;if(!R.frIntro)R.frIntro={t:0,beat:0,done:false};const I=R.frIntro;
 if(!I.done){
  I.t+=dt;b._noHit=true;eBullets.length=0;pBullets.length=0;
  for(const q of R.ships){q.x+=clamp(q.homeX-q.x,-100*dt,100*dt);q.y+=clamp(q.homeY-q.y,-95*dt,95*dt);q.mode='entry';}
  const beats=[['VOSS','THE DIVISION BETRAYED EVERY ONE OF US. THERE ARE NO ORDERS LEFT WORTH FOLLOWING.'],[_pilotKey().toUpperCase(),'WE WERE ONE UNIT ONCE. IT DOES NOT HAVE TO BE LIKE THIS. WE CAN STILL STOP THIS.'],['NYX','STOP IT? THEY BUILT THIS WORLD ON OUR BONES.'],['VOSS','LET THE WORLD BURN. GET OUT OF OUR WAY, OR BURN WITH IT.']];
  const at=[2.5,10,17.5,22.5];if(I.beat<beats.length&&I.t>=at[I.beat]){s6WingSay(...beats[I.beat++]);}
  if(I.t>=29){I.done=true;b._noHit=false;R.t=0;R.releaseAt=1.6;for(const q of R.ships){q.mode='fight';q.t=0;q.cd=1.6+q.i*.4;}}
  return;
 }
 FR27_BASE.rebelTick(b,dt);
};
rebelSquadDamage=function(b,dmg){if(!b._rebels.frIntro?.done)return;FR27_BASE.rebelDamage(b,dmg);
 if(b._rebels.ships.every(q=>q.dead)&&run.stage===6&&!Rival24.active){campaign.rivalDefeated=[true,true,true,true,true];campaign.rivalScattered=false;}
};
rebelSquadDraw=function(b){FR27_BASE.rebelDraw(b);if(!b._rebels.frIntro?.done)return;
 for(const q of b._rebels.ships){if(q.dead)continue;const w=66,y=q.y-52;
  ctx.save();ctx.fillStyle='#04080f';ctx.fillRect(q.x-w/2-2,y-2,w+4,9);ctx.fillStyle='#3a4655';ctx.fillRect(q.x-w/2,y,w,5);ctx.fillStyle=REBEL_TINT[q.i];ctx.fillRect(q.x-w/2,y,w*clamp(q.hp/q.max,0,1),5);ctx.restore();campText(q.key.toUpperCase(),q.x,y-7,7,'#e6efff');
 }
};
Object.assign(FR27_BASE,{s7Tick:s7mTick,s7Draw:s7mDraw,s7Portal:drawS7FinalPortalWorld,s7Radio:s7WardenRadioDraw,s7Finish:s7WardenFinishCampaign});
function fr27ToxicExplosion(x,y,size,serial){
 const fam=BOSS_COMBO[(serial||0)%BOSS_COMBO.length];
 explode(x,y,size,'green',null,fam,null,.8+(serial%3)*.1,true);
 const fx=explosions[explosions.length-1];if(fx)fx._frToxic=true;
 // Palette the secondary sparks too; retain their authored motion and smoke.
 for(const p of particles)if(p.t===0&&p.color!=='#1c1c1c')p.color=p.color==='#ffd36b'?'#ceff7d':'#4fbf25';
}
function fr27Exit(b,dt){
 const M=b._s7mod,F=b._s7warden.final,E=M.frExit||(M.frExit={t:0,beat:0,fx:0,startX:player.x,startY:player.y,groundY:b.y,sourceY:_masterSrcY,travel:0,serial:0,portalX:worldWidth()/2,portalY:118});
 E.t+=dt;M.t=E.t;M.clock+=dt;F.phase='escape';F.shipHidden=E.t>=17.3;F.bossHidden=E.t>=13;
 b._s7FinalNoBar=true;b._s7warden.noHit=true;bossDefeated=true;player.invuln=Math.max(player.invuln,3);eBullets.length=0;
 const name=(PILOTS.find(q=>q.key===run.pilot)?.name||run.pilot).toUpperCase();
 const beats=[{at:0,who:'',text:''},{at:1.1,who:missionRadioWho('DECKER'),text:'I AM DETECTING A SELF-DESTRUCT SEQUENCE IN THAT THING!'},{at:5.0,who:missionRadioWho('COLE'),text:"IT'S GONNA BLOW! GET OUT OF THERE, NOW!!!"},{at:15.6,who:missionRadioWho('DECKER'),text:name+', NOOOOOOOOOOOOOOO!'},{at:18.4,who:missionRadioWho('COLE'),text:'WHERE DID THEY GO? ARE THEY ALL RIGHT? CHECK THE RADAR, NOW!'}];
 if(E.beat<beats.length&&E.t>=beats[E.beat].at){const q=beats[E.beat++];F.radio=q.who?{who:q.who,full:q.text,t:0,typed:0,dur:5}:null;if(E.beat===1)s7WardenMechSound('scream');}
 if(F.radio){F.radio.t+=dt;F.radio.typed+=dt*44;if(F.radio.t>F.radio.dur)F.radio=null;}
 if(E.t>=8){
  const u=clamp((E.t-8)/9.3,0,1),ease=u*u*(3-2*u);player.y=lerp(E.startY,E.portalY,ease);player.x=lerp(E.startX,E.portalX,ease);player._thrustPower=1;
  E.travel=(E.t-8)*180;b.y=E.groundY+E.travel;M.lean=0;M.height=0;M.drop=0;
  E.fx-=dt;while(E.fx<=0){E.fx+=.11;const front=lerp(viewTopY()+viewH()+100,viewTopY()-100,clamp((E.t-8)/12,0,1));
   fr27ToxicExplosion(camLeftX()+Math.random()*viewW(),front+Math.random()*190,135+Math.random()*85,E.serial++);
   if(E.t<12)fr27ToxicExplosion(b.x+Math.sin(E.t*13)*100,b.y+Math.cos(E.t*9)*75,150,E.serial++);
  }
  E.boomCD=(E.boomCD||0)-dt;if(E.boomCD<=0){E.boomCD=Math.max(.20,.42-(E.t-8)*.02);s7mSound(E.serial%3?'expSmall':'expBig');}
  shake=Math.max(shake,7+Math.min(9,E.t-8));
  if(!E.ring&&E.t>=8.4){E.ring=true;spawnSmokeRing(b.x,b.y,220);s7mFX(b.x,b.y,260,true);s7mSound('expBig');}
  if(!E.portalSound&&E.t>=14.1){E.portalSound=true;(Audio.SFX.warpGate||Audio.SFX.teleportIn||function(){})();}
  if(E.t>=18.6){E.fillCD=(E.fillCD||0)-dt;if(E.fillCD<=0){E.fillCD=.18;for(let i=0;i<4;i++)fr27ToxicExplosion(camLeftX()+(i+.5)*viewW()/4,viewTopY()+Math.random()*viewH()-140,240,E.serial++);}}
 }
 if(E.t>=22.8){
  if(!b._forgeRewardDropped){b._forgeRewardDropped=true;forgeBossDrop(player.x,player.y);run.score+=35000;}
  for(const p of powerups)if(p.kind==='forgecombo'&&!p.dead){applyPowerup(p);p.dead=true;}
  F.finished=true;F.phase='done';F.radio=null;F.shipHidden=false;b.dead=true;bossActive=false;bossDefeated=true;whiteBlast=0;run._l78Entry=1;
  if(run.mode==='campaign')campaign._l78Pending=1;drawStageClear._init=false;drawStageClear._res=null;Audio.stopMusic();setState(GS.STAGECLEAR);
 }
 return true;
}
s7mTick=function(b,dt){if(b?._s7mod?.mode==='dead'&&!b._s7mod.tank)return fr27Exit(b,dt);return FR27_BASE.s7Tick(b,dt);};
s7mDraw=function(b){const M=b?._s7mod,E=M?.frExit;if(!E)return FR27_BASE.s7Draw(b);if(E.t>=13)return true;
 const mode=M.mode,t=M.t;try{M.mode='roar';M.t=.2;M.coreFlash=.15+Math.sin(E.t*(8+E.t*2))*.14;return FR27_BASE.s7Draw(b);}finally{M.mode=mode;M.t=t;}
};
drawS7FinalPortalWorld=function(){
 if(run.stage!==7)return;const E=boss?._s7mod?.frExit;
 // The entry floor has no giant portal prop. Only the exit vortex appears here.
 if(!E||E.t<14.1||E.t>=18.5)return;
 const age=E.t-14.1,closing=clamp((E.t-17.3)/1.2,0,1);
 // Frames 0–3 open the vortex; 4–7 are its dissipating tail, not a held opening.
 const f=closing>0?Math.min(7,4+Math.floor(closing*4)):Math.min(3,Math.floor(age*5));
 fr27ToxicPortal(f,E.portalX,E.portalY,190*(1-closing));
};
s7WardenRadioDraw=function(){FR27_BASE.s7Radio();const E=boss?._s7mod?.frExit;if(E&&E.t>21.3){ctx.save();ctx.fillStyle='rgba(0,0,0,'+clamp((E.t-21.3)/1.5,0,1)+')';ctx.fillRect(0,0,VW,VH);ctx.restore();}};
function fr27CinematicCamera(){const E=run.stage===7&&boss?._s7mod?.frExit;if(!E||E.t<8)return;const z=1+clamp((E.t-8)/6,0,1)*.18;ctx.translate(player.x,player.y);ctx.scale(z,z);ctx.translate(-player.x,-player.y);ctx.translate(0,Math.max(0,(E.startY-player.y)*.66));}
for(const name of ['stagex_card','stagex_terrain','realm_ordnance','realm_boss'])XART._src['fr27_'+name]='assets/game/shared/combat/furious_review_0927/'+name+'.png';
XART._src.r24_card=XART._src.fr27_stagex_card;
function fr27LoopTerrain(key,scroll){
 if(!XART.rdy(key))return false;const im=XART.get(key),w=worldWidth(),h=w*im.height/im.width,top=viewTopY();
 // Ping-pong addressing has identical pixels at both joins, with no stitched seam or crossfade.
 const offset=((scroll||0)%(h*2)+h*2)%(h*2);
 for(let i=-2;i<4;i++){const y=top+i*h+offset-h*2;ctx.save();if(i%2){ctx.translate(0,y+h);ctx.scale(1,-1);ctx.drawImage(im,0,0,w,h+1);}else ctx.drawImage(im,0,y,w,h+1);ctx.restore();}return true;
}
const FR27_ROUTE_BG=drawBG;
drawBG=function(dt){
 if(Rival24.active){
  // Reuse the authored ocean reel under the alpha-cut industrial terrain.
  // Independent water travel continues while the encounter holds mapScroll.
  ctx.fillStyle='#05243b';ctx.fillRect(0,viewFillY(),worldWidth(),viewFillH());
  ctx.save();ctx.globalAlpha=.42;
  drawAnimTerrain(_liquidFrames('nlq2_water'),stageTimer*42,1.35,.5,5,worldWidth());
  ctx.restore();
  fr27LoopTerrain('fr27_stagex_terrain',stageTimer*42);
  return;
 }
 if(run.stage===8){
  // The replacement renderer owns the scrolling that the old master renderer supplied.
  dt=Number.isFinite(dt)?dt:0;mapScroll=Math.min(Math.max(4096,levelScrollRange()),mapScroll+dt*40);
  run._frRealmScroll=(run._frRealmScroll||0)+dt*78;_masterSrcY=levelScrollRange()-mapScroll;
  if(fr27LoopTerrain('fr27_realm_terrain',run._frRealmScroll))return;
 }
 return FR27_ROUTE_BG(dt);
};
Object.assign(FR27_BASE,{begin:beginStage,s8Tick:s8MegaTick,s8Draw:drawS8Mega,projectile:drawCombatFinalProjectile});
beginStage=function(num){const r=FR27_BASE.begin.apply(this,arguments);if(num===8){run._frRealmScroll=0;run._l78Entry=1;l78EntryStart();setState(GS.WARPENTRY);for(const k of ['realm_terrain','realm_fleet','realm_ordnance','realm_boss'])XART.rdy('fr27_'+k);}return r;};
function fr27ToxicPortal(frame,x,y,size){
 const key='nfx_l7portal_'+clamp(frame|0,0,7);if(!size||!XART.rdy(key))return false;
 const im=xartPalette(key,'#74ee44')||XART.get(key);ctx.save();ctx.imageSmoothingEnabled=false;
 ctx.drawImage(im,x-size,y-size,size*2,size*2);ctx.restore();return true;
}
l78EntryStart=function(){l78entry={t:0,beat:0,destY:VH*.78};storySkip();player.invuln=Math.max(player.invuln||0,3);XART.rdy('fr27_realm_terrain');for(let i=0;i<8;i++)XART.rdy('nfx_l7portal_'+i);s7mWarm();};
drawL78Entry=function(dt){
 if(!l78entry)l78EntryStart();const E=l78entry;E.t+=dt;const t=E.t;
 const dest={y:E.destY},u=clamp((t-1.2)/2.1,0,1),ease=1-Math.pow(1-u,3);
 player.x=worldWidth()/2;player.y=lerp(112,dest.y,ease);_cinematicHidePlayer=t<1.2;
 const inv=player.invuln;player.invuln=0;drawWorld(0);player.invuln=inv;_cinematicHidePlayer=false;
 if(t>.7&&t<4){const age=t-.7,close=clamp((t-3)/1,0,1),f=close>0?5+Math.min(2,Math.floor(close*3)):Math.min(4,Math.floor(age*5));
  const x=(player.x-camLeftX())*viewZoom(),y=(112-viewTopY())*viewZoom();fr27ToxicPortal(f,x,y,170*viewZoom()*(1-close));
 }
 if(!E.open&&t>=.7){E.open=true;(Audio.SFX.warpGate||Audio.SFX.teleportIn||function(){})();}
 if(!E.breach&&t>=1.2){E.breach=true;(Audio.SFX.dash||function(){})();}
 const texts=['WHERE AM I? IS ANYONE THERE? I AM NOT GETTING A READ ON ANYONE! SOMEONE, PLEASE RESPOND!','NOTHING. NO FURY SIGNAL. THIS IS NOT ANYWHERE I KNOW.'];
 const idx=t>=9.5?1:0,age=t-(idx?9.5:3.8);
 if(age>=0)dlgBox({who:run.pilot.toUpperCase(),full:texts[idx],shown:texts[idx].slice(0,Math.floor(age*36)),portrait:run.pilot,pw:VW*.76,tint:'#c9a5ff'});
 if(t<1.4){ctx.fillStyle='rgba(0,0,0,'+(1-clamp(t/1.4,0,1))+')';ctx.fillRect(0,0,VW,VH);}
 if(t>=15){player.y=dest.y;player.invuln=2.5;run._l78Entry=0;l78entry=null;Audio.startMusic(curStage.music);setState(GS.PLAY);Input.clearTaps();}
};
function fr27RealmRow(e){const k=e._s8mega||e.type||'';return /carrier|solar|gunship|tentacle/.test(k)?3:/bomber|deathorb|manta/.test(k)?1:/needle|razor|leech/.test(k)?2:0;}
function fr27RealmShot(x,y,a,spd,row){const q=eShootT(x,y,a,spd,'s8pair',{w:row===0?10:row===1?26:22,h:row===0?23:row===1?26:22,silent:true});q._frRealm=row;q._boss=true;q._noArsenal=true;return q;}
s8MegaTick=function(e,dt){
 const n=fr27Difficulty(),row=fr27RealmRow(e),A=e._frRealmAI||(e._frRealmAI={t:0,cd:1.0+Math.random()*.65,shot:0,home:e.x,seq:0});A.t+=dt;A.cd-=dt;
 const turn=Math.sin(A.t*(row===2?1.5:.7))*[20,18,38,10][row];e.x=clamp(A.home+turn,camLeftX()+e.w*.5,camRightX()-e.w*.5);e.y+=dt*[66,44,92,33][row];e._frBank=Math.cos(A.t*.7)*20;
 if(e.y>player.y-65||e.y<viewTopY()+e.h*.5||A.cd>0)return;
 if(!A.tell){A.tell={t:0,x:player.x,y:player.y};combatWarningTick(e,'realm-'+A.seq,0,.8,true);}
 A.tell.t+=dt;combatWarningTick(e,'realm-'+A.seq,A.tell.t,.8);
 if(A.tell.t<.8)return;const target=A.tell,a=Math.atan2(target.y-e.y,target.x-e.x);A.tell=null;A.seq++;A.shot=.2;A.cd=[2.9,3.5,3.1,3.7][row]/[1,1.12,1.25][n];
 if(row===0)for(const o of [-.16,0,.16])fr27RealmShot(e.x,e.y+e.h*.4,a+o,3.3+n*.6,0);
 else if(row===1){for(const o of [-.23,.23]){const q=fr27RealmShot(e.x,e.y+e.h*.4,a+o,2.7+n*.45,1);q._frBurst=1.05;}}
 else if(row===2){for(const x of [-e.w*.2,e.w*.2])fr27RealmShot(e.x+x,e.y+e.h*.42,Math.PI/2,5.2+n*.5,0);}
 else for(const o of [-.30,0,.30])fr27RealmShot(e.x,e.y+e.h*.4,a+o,3.0+n*.4,2);
 (Audio.SFX.enemyHeavyLaser||Audio.SFX.enemyShoot||function(){})();
};
drawS8Mega=function(e){const A=e._frRealmAI,row=fr27RealmRow(e),f=A?.shot>0?3:Math.abs(e._frBank||0)>10?(e._frBank<0?1:2):0;
 const size=Math.max(e.w,e.h)*1.28;e._drawW=size*.82;e._drawH=size;const drawn=fr27Cell('fr27_realm_fleet',f,row,e.x,e.y,size,size,1);
 if(drawn&&e.flash>0)fr27Cell('fr27_realm_fleet',f,row,e.x,e.y,size,size,Math.min(1,e.flash*9),'#ffffff');
 if(A?.tell)combatWarningDraw(e,{x:e.x,y:e.y+e.h*.35,ex:A.tell.x,ey:A.tell.y,progress:A.tell.t/.8,width:row===0?85:row===2?30:100,alpha:.32});
 return drawn;
};
drawCombatFinalProjectile=function(b,role){if(b._frRealm==null)return FR27_BASE.projectile(b,role);return vile24Cell('fr27_realm_ordnance',4,4,Math.floor((b.t||efxClock)*12)%4+b._frRealm*4,b.x-(b._frRealm===0?10:19),b.y-(b._frRealm===0?20:19),b._frRealm===0?20:38,b._frRealm===0?40:38,1);};
const FR27_REALM_PLAY=updatePlay;
updatePlay=function(dt){const r=FR27_REALM_PLAY(dt);if(state===GS.PLAY&&run.stage===8){for(const e of enemies)if(e._frRealmAI)e._frRealmAI.shot=Math.max(0,e._frRealmAI.shot-dt);for(const q of eBullets){if(q.dead||q._frBurst==null)continue;q._frBurst-=dt;if(q._frBurst<=0){q.dead=true;for(let i=0;i<8;i++)fr27RealmShot(q.x,q.y,Math.PI/2+i*TAU/8,3.1+fr27Difficulty()*.3,0);explode(q.x,q.y,45,'blue',null,'nxp_barrage');Audio.SFX.expSmall?.();}}}return r;};

function fr27CoreMapPosition(){const p=cmap2World('hub');return p?cmap2ToScreen(p.x,p.y):null;}
const FR27_MAP_CAMERA=cmap2CameraTick;
cmap2CameraTick=function(dt,cine,selected){return FR27_MAP_CAMERA(dt,cine,Rival24.mapFocused?'hub':selected);};

Object.assign(FR27_BASE,{rebelHit:rebelSquadHitTest,retinaBoss:retinaBossTargets,radio:s6WingSay,radioDraw:s6WingRadioDraw,world:drawWorld});
drawWorld=function(dt){return FR27_BASE.world(run.stage===6&&s6Wing?.choice&&!s6Wing.route?0:dt);};
s6WingSay=function(who,text){
 if(s6Wing)return FR27_BASE.radio(who,text);
 if(Rival24.active&&boss?._rebels){boss._rebels.frRadio={who,full:text,t:0};XART.rdy('rr_portrait_'+who.toLowerCase());}
};
s6WingRadioDraw=function(){
 FR27_BASE.radioDraw();const L=Rival24.active&&boss?._rebels?.frRadio;if(!L)return;
 dlgBox({who:L.who,full:L.full,shown:L.full.slice(0,Math.floor(L.t*36)),portrait:L.who.toLowerCase(),portraitKey:REBEL_KEYS.includes(L.who.toLowerCase())?'rr_portrait_'+L.who.toLowerCase():undefined,pw:VW*.74,tint:'#87ddff'});
};
function fr27RebelModules(q){return q.frModules||(q.frModules=[{id:'left',hp:q.max*.20,max:q.max*.20,dx:-27},{id:'right',hp:q.max*.20,max:q.max*.20,dx:27}]);}
rebelSquadHitTest=function(b,x,y){
 if(!FR27_BASE.rebelHit(b,x,y))return false;const q=b._rebels.ships[b._rebels.hit];
 const dx=x-q.x;const id=Math.abs(dx)>18?(dx<0?'left':'right'):null;
 const p=fr27RebelModules(q).find(p=>p.id===id);if(p&&p.hp<=0){b._rebels.hit=-1;return false;}
 b._rebels.frHit=id;return true;
};
const FR27_REBEL_DAMAGE=rebelSquadDamage;
rebelSquadDamage=function(b,dmg){
 const R=b._rebels,q=R.ships[R.hit],id=R.frHit;R.frHit=null;
 if(!R.frIntro?.done||!q||q.dead||q.mode==='entry'||q.warp>0)return;
 const m=fr27RebelModules(q).find(p=>p.id===id);
 if(m){if(m.hp<=0)return;const damage=Math.min(dmg,m.hp);m.hp-=damage;dmg=damage;if(m.hp<=0){explode(q.x+m.dx,q.y,35,'red');spawnSmokeRing(q.x+m.dx,q.y,26);Audio.SFX.expBig?.();}}
 FR27_REBEL_DAMAGE(b,dmg);
};
retinaBossTargets=function(b){
 if(!b?._rebels)return FR27_BASE.retinaBoss(b);const R=b._rebels,out=[];if(!R.frIntro?.done||b.dead)return out;
 for(const q of R.ships){if(q.dead||q.mode==='entry'||q.warp>0)continue;
  for(const p of [...fr27RebelModules(q),{id:'core',dx:0,hp:q.hp}]){if(p.hp<=0)continue;
   out.push(retinaDynamicPiece(b,q.key+'-'+p.id,p.id==='core'?'rival':'module',()=>({x:q.x+p.dx,y:q.y,hp:p.id==='core'?q.hp:p.hp,dead:q.dead||q.mode==='entry'||q.warp>0||p.hp<=0}),d=>{R.hit=q.i;R.frHit=p.id==='core'?null:p.id;hitBoss(d);},p.id==='core'?34:24,64));
  }
 }return out;
};
function fr27RebelAttack(q,R){
 const live=fr27RebelModules(q).filter(p=>p.hp>0);q.frAttackN=(q.frAttackN||0)+1;
 if((q.i===1||R.frStageX)&&q.frAttackN%3===0){q.frCloak=1.8;q.cd=2.6;return true;}
 if(live.length&&q.frAttackN%2===0){q.frCast={t:0,tx:player.x,ty:player.y,kind:q.i%2?'orb':'laser'};q.cd=2.8;R.releaseAt=R.t+1.9;combatWarningTick(q,'rebel-charge',0,1.1,true);Audio.SFX.bossWeaponCharge?.();return true;}
 if(!live.length){q.cd*=1.4;return false;}return false;
}
const FR27_REBEL_TICK=rebelSquadTick;
rebelSquadTick=function(b,dt){
 const R=b._rebels;if(R.frRadio){R.frRadio.t+=dt;if(R.frRadio.t>R.frRadio.full.length/36+2.5)R.frRadio=null;}
 for(const q of R.ships){fr27RebelModules(q);q.frCloak=Math.max(0,(q.frCloak||0)-dt);
  if(q.frCast){q.cd=Math.max(q.cd,dt+.2);const C=q.frCast;C.t+=dt;combatWarningTick(q,'rebel-charge',Math.min(1.1,C.t),1.1);
   if(C.t>=1.1){for(const m of q.frModules.filter(p=>p.hp>0)){const x=q.x+m.dx,y=q.y+28,a=Math.atan2(C.ty-y,C.tx-x);for(const o of (C.kind==='orb'?[-.16,.16]:[0])){const z=eShootT(x,y,a+o,C.kind==='orb'?3.1:6.2,C.kind==='orb'?'s6orb':'eglaser',{w:C.kind==='orb'?20:9,h:C.kind==='orb'?20:32,silent:true});z._noArsenal=true;}}Audio.SFX.enemyHeavyLaser?.();q.frCast=null;}
  }
 }
 FR27_REBEL_TICK(b,dt);
 for(const q of R.ships){if(R.frStageX&&!q.dead)q.homeX=worldWidth()/2;if(q.evadeT>0&&!q.frEvading){q.frEvadeCount=(q.frEvadeCount||0)+1;q.frSomersault=q.frEvadeCount%3===0;q.frEvading=true;}if(!(q.evadeT>0))q.frEvading=false;}
};
XART._src.fr27_rebel_pitch='assets/game/shared/combat/furious_review_0927/rebel_pitch.png';
function fr27RebelDrawShip(q){
 const f=q.evadeT>0?Math.min(7,Math.floor((1-q.evadeT/.38)*8)):0,key='rr_roll_'+REBEL_SHIPS[q.i]+'_'+f;
 const k=XART.rdy(key)?key:'rr_ship_'+REBEL_SHIPS[q.i];if(!XART.rdy(k))return;
 const pitch=q.frSomersault&&q.evadeT>0&&XART.rdy('fr27_rebel_pitch');const im=XART.get(pitch?'fr27_rebel_pitch':k);
 const cw=pitch?im.width/4:im.width,ch=pitch?im.height/5:im.height,sx=pitch?Math.min(3,Math.floor(f/2))*cw:0,sy=pitch?q.i*ch:0;
 const w=SHIP_DRAW_H*1.5,h=pitch?w:w*ch/cw;ctx.save();ctx.globalAlpha=q.frCloak>0?.22+.12*Math.sin(q.t*22):1;
 for(const[a,z,id]of [[0,.33,'left'],[.33,.67,null],[.67,1,'right']]){if(id&&fr27RebelModules(q).find(p=>p.id===id).hp<=0)continue;ctx.drawImage(im,sx+a*cw,sy,(z-a)*cw,ch,q.x-w/2+a*w,q.y-h/2,(z-a)*w,h);}
 ctx.restore();if(q.frCast)combatWarningDraw(q,{x:q.x,y:q.y+28,ex:q.frCast.tx,ey:q.frCast.ty,progress:q.frCast.t/1.1,width:q.frCast.kind==='orb'?75:28,alpha:.30});
}

// Stage 8 first shell: an authored alien hull with binary cannons and dark matter.
Object.assign(FR27_BASE,{vileAttack:vile24Attack,vileTick:vile24Tick,vileDraw:vile24DrawBoss});
vile24Attack=function(b){
 if(b._vForm!==0)return FR27_BASE.vileAttack(b);const S=b._v24;if(!S||S.pattern)return;
 const type=['binary-fan','binary-bombs','dark-matter'][S.seq++%3];
 S.pattern={type,t:0,tell:1.05,tx:player.x,ty:player.y,released:false,fr:true};b.fireCd=2.8;
 combatWarningTick(b,type,0,1.05,true);(Audio.SFX.bossWeaponCharge||Audio.SFX.enemyBossCannon)?.();
};
vile24Tick=function(b,dt){
 const S=b._v24,P=S?.pattern;if(b._vForm!==0||!P?.fr)return FR27_BASE.vileTick(b,dt);
 P.t+=dt;combatWarningTick(b,P.type,Math.min(P.t,P.tell),P.tell);
 if(!P.released&&P.t>=P.tell){P.released=true;const n=fr27Difficulty();
  for(const side of [-1,1]){if(!vile24Part(b,side<0?'left_systems':'right_systems'))continue;
   const x=b.x+side*b.w*.30,y=b.y+b.h*.21,a=Math.atan2(P.ty-y,P.tx-x);
   if(P.type==='binary-fan')for(let j=-2;j<=2;j++)fr27RealmShot(x,y,a+j*.14,3.7+n*.55,0);
   else if(P.type==='binary-bombs')for(const o of [-.21,.21]){const q=fr27RealmShot(x,y,a+o,2.3+n*.3,1);q._frBurst=1.1;}
   else for(const o of [-.28,0,.28])fr27RealmShot(x,y,a+o,2.6+n*.25,2);
  }
  (Audio.SFX.enemyHeavyLaser||Audio.SFX.enemyBossCannon)?.();
 }
 if(P.t>=P.tell+1.25){S.pattern=null;b.fireCd=.7;}
};
XART._src.fr28_mutated_vessel='assets/game/shared/combat/stage678_repair_0928/mutated_vessel.png';
function fr28VesselPlate(b,alpha){
 if(!XART.rdy('fr28_mutated_vessel'))return false;const im=XART.get('fr28_mutated_vessel'),w=b.w*1.12,h=b.h*1.12;
 ctx.save();ctx.imageSmoothingEnabled=false;ctx.globalAlpha=alpha==null?1:alpha;
 for(const[a,z,id]of [[0,.28,'left_systems'],[.28,.72,null],[.72,1,'right_systems']]){
  if(id&&!vile24Part(b,id))continue;ctx.drawImage(im,im.width*a,0,im.width*(z-a),im.height,b.x-w/2+w*a,b.y-h/2,w*(z-a),h);
 }
 if(b.flash>0){const flash=xartTint('fr28_mutated_vessel',hitFlashColor(b,'#fff'),.74);if(flash){ctx.globalAlpha*=Math.min(.6,b.flash*4);ctx.drawImage(flash,b.x-w/2,b.y-h/2,w,h);}}
 ctx.restore();return true;
}
vile24DrawBoss=function(b){
 if(b._vForm!==0||b._symEntry||b._morphT!=null||!XART.rdy('fr28_mutated_vessel'))return FR27_BASE.vileDraw(b);
 fr28VesselPlate(b);const P=b._v24?.pattern;
 if(P?.fr&&!P.released)for(const side of [-1,1])if(vile24Part(b,side<0?'left_systems':'right_systems'))combatWarningDraw(b,{x:b.x+side*b.w*.30,y:b.y+b.h*.21,ex:P.tx,ey:P.ty,progress:P.t/P.tell,width:85,alpha:.34});
};
const FR28_VILE_BUILD=vile24BuildForm;
vile24BuildForm=function(b,idx){const r=FR28_VILE_BUILD.apply(this,arguments);if(idx===0){b.name='MUTATED DATA VESSEL';b.ty=Math.max(b.ty||0,b.h*.56+62);XART.rdy('fr28_mutated_vessel');}return r;};

// Toxic field ordnance is ammunition, never a construction barricade plate.
const FR27_ORDNANCE_DRAW=drawCombatFinalProjectile;
drawCombatFinalProjectile=function(b,role){
 if(b.kind==='s7shard'||b.kind==='s7acid')return s7mBlit('orb',Math.floor((b.t||0)*12)%8,b.x,b.y,32,32,0,1);
 return FR27_ORDNANCE_DRAW(b,role);
};

const FR28_OLD_ALIEN_OBJECTS=l8ObjsDraw;
l8ObjsDraw=function(){if(run.stage===8&&XART.rdy('fr27_realm_terrain'))return;return FR28_OLD_ALIEN_OBJECTS.apply(this,arguments);};

// Stage 7's replacement cap connects to the existing master with an exact source seam.
XART._src.fr28_sewer_connector='assets/game/shared/combat/stage678_repair_0928/sewer_connector.png';
XART._src.fr28_lamprey='assets/game/shared/combat/stage678_repair_0928/lamprey.png';
let fr28SewerPlate=null;
function fr28SewerMaster(){
 if(fr28SewerPlate)return fr28SewerPlate;
 if(!XART.rdy('nst7_master_v3')||!XART.rdy('fr28_sewer_connector'))return null;
 const original=XART.get('nst7_master_v3'),cap=XART.get('fr28_sewer_connector'),c=document.createElement('canvas');
 c.width=original.width;c.height=original.height;const g=c.getContext('2d');g.imageSmoothingEnabled=false;g.drawImage(original,0,0);
 g.clearRect(0,0,c.width,928);g.drawImage(cap,0,0,cap.width,928,0,0,c.width,928);
 // Only a narrow floor overlap blends; the exact original remains below row 1024.
 for(let y=928;y<1024;y+=4){g.globalAlpha=(1024-y)/96;g.drawImage(cap,0,y,cap.width,4,0,y,c.width,4);}g.globalAlpha=1;
 return fr28SewerPlate=c;
}
const FR28_BG=drawBG,FR28_BEGIN=beginStage,FR28_SEWER_ENEMY=drawS7Toxic;
beginStage=function(num){const r=FR28_BEGIN.apply(this,arguments);if(num===7){XART.rdy('fr28_sewer_connector');XART.rdy('fr28_lamprey');for(let i=0;i<8;i++)XART.rdy('nfx_l7portal_'+i);}return r;};
drawBG=function(dt){
 if(run.stage!==7)return FR28_BG(dt);const E=boss?._s7mod?.frExit;
 FR28_BG(E?0:dt);const im=fr28SewerMaster();if(!im)return;
 if(!E&&_masterSrcY>=1024)return;
 const sy=E?E.sourceY-E.travel:_masterSrcY;
 _masterSrcY=sy;ctx.fillStyle='#232b12';ctx.fillRect(0,viewFillY(),worldWidth(),viewFillH());
 drawAnimTerrain(_liquidFrames('nlq_sludgeF'),oozeScroll+(E?E.travel:mapScroll),1.5,.5,5,worldWidth());
 // Continue north beyond the old cap. Mirrored addressing joins identical edge pixels.
 const cap=XART.get('fr28_sewer_connector');for(let i=1;i<=4;i++){const y=-sy-i*1024;ctx.save();if(i%2){ctx.translate(0,y+1024);ctx.scale(1,-1);ctx.drawImage(cap,0,0,680,1024);}else ctx.drawImage(cap,0,y,680,1024);ctx.restore();}
 ctx.drawImage(im,0,-sy,680,im.height);return;
};
drawS7Toxic=function(e){
 if(e._s7toxic!=='s7lamprey')return FR28_SEWER_ENEMY(e);if(!XART.rdy('fr28_lamprey'))return true;
 const im=XART.get('fr28_lamprey'),h=e.h*1.72,w=h*im.width/im.height;e._drawW=w;e._drawH=h;
 ctx.save();ctx.translate(e.x,e.y);if(e.spin)ctx.rotate(e.spin);ctx.imageSmoothingEnabled=false;ctx.drawImage(frenzyPlate(e,'fr28_lamprey')||im,-w/2,-h/2,w,h);
 drawS7DamageOverlay(e,clamp(e.hp/(e._maxhp||e.maxhp||e.hp||1),0,1),w,h);
 if(e.flash>0){const tint=xartTint('fr28_lamprey',hitFlashColor(e,'#fff'),.74);if(tint)ctx.drawImage(tint,-w/2,-h/2,w,h);}ctx.restore();return true;
};

// Restore the authored Stage 8 track rather than the historical Egypt-key alias.
BOFA.music.realm8='assets/game/levels/stage_08/audio/music/Level8.mp3';
STAGES[7].music='realm8';
if(Snd?.music&&!Snd.music.realm8&&typeof window.Audio==='function'){const track=new window.Audio();track.preload='none';track.src=BOFA.music.realm8;track.loop=true;Snd.music.realm8=track;}

const FR28_LEVEL_CFG=_levelCfg;
_levelCfg=function(){const cfg=FR28_LEVEL_CFG.apply(this,arguments);return run.stage===8?{...cfg,master:'fr27_realm_terrain',h:4096,scrollLen:4096,loopMaster:true,continuousBoss:true}:cfg;};
