"use strict";
/* Chronos's Stage5 counter contract. The intact actor, held tool and detached
   tool have explicit owners; ordinary damage never changes attack state. */
const C25={events:[],base:{damage:hammerBossDamage,break:hammerRecoveryBreak,module:hammerBossModuleBreak,
 restore:fr27Restore,disarm:hammerWhirlDisarm,tick:hammerBossTick,draw:hammerBossDraw,blue:ha21Blue,head:hammerHeadPoint,
 wall:hm10WallDraw,reticle:hammerGroundReticleDraw,pair:hj22PairDraw,warning:combatWarningDraw,
 stun:hammerStunEffectsDraw,armor:fr27BeginArmor,death:bossDie}};
for(const a of Object.values(C25_ART.sheets))XART._src[a.key]=a.path;
for(const [name,a]of Object.entries(C25_ART.banks))for(let f=0;f<a.count;f++){
 BOFX.cells['c25_'+name+'_'+f]=[a.sheet,f%a.cols*a.w,Math.floor(f/a.cols)*a.h,a.w,a.h];
 BOFX.cells['c25_'+name+'_'+f+'_hit']=[a.sheet+'_hit',f%a.cols*a.w,Math.floor(f/a.cols)*a.h,a.w,a.h];
}
function c25Warm(){return Object.values(C25_ART.sheets).map(a=>XART.rdy(a.key)).every(Boolean);}
const c25StageLoad=stageLoadBegin;
stageLoadBegin=function(n,keys){if(n===5)Snd.prepare(['lightning','hammerMagnet','hammerThrow','bossWeaponCharge']);return c25StageLoad.call(this,n,[...(keys||[]),...(n===5?Object.values(C25_ART.sheets).map(a=>a.key):[])]);};
function c25Own(b){return run.stage===5&&!!b?._hammer&&!b._gp4Host&&!b._hammerTime?.hama;}
function c25Depth(b){return c25Own(b)&&(b._hammer.state.startsWith('giant_')||!!b._hammer.er23DepthCombo);}
function c25Log(type,data={}){C25.events.push({type,time:efxClock,...data});if(C25.events.length>500)C25.events.shift();}
function c25Counter(b){const h=b?._hammer;if(!c25Own(b)||b.dead||b._noHit||h.recovery?.status!=='charging'||h.t<1.25)return false;const at=hammerHeadPoint(b);return at.y>=viewTopY()+55&&at.y<PLAY.y+PLAY.h-40;}
function c25Plate(b,name,u){
 const suffix=hf22Red(b)?'_red':b._hammer.c25ArmorAtDeath||fr27Armor(b)?.activated&&fr27Armor(b)?.hp>0?'_armor':'';
 if(name==='empty'){
  const a=typeof C25_ART!=='undefined'&&C25_ART.banks['empty'+suffix];if(!a)return null;
  const f=Math.min(a.count-1,Math.floor(clamp(u,0,1)*(a.count-1))),key='c25_empty'+suffix+'_'+f;
  if(!XART.rdy(key)||!XART.rdy(key+'_hit'))return null;
  return {a:{...a,key,white:key+'_hit',_hf22:true,_c25:true,_c26:true,frame:f},k:.84,rot:0,kind:'c25_empty'+suffix};
 }
 const bank='chronos_'+name+suffix,q=bi24Sample(bank,u);if(!q)return null;
 const key='bi24_'+bank+'_'+q.f;if(!XART.rdy(key))return null;
 return{a:{...q.a,key,white:'bi24_'+bank+'_hit_'+q.f,tip:q.a.tips[q.f],_hf22:true,_bi24:true},k:1,rot:0,kind:'c25_'+bank};
}
ha21Blue=function(b){
 if(!c25Own(b))return C25.base.blue.apply(this,arguments);const h=b._hammer,K=h.c25Knock;
 if(b.dead)return c25Plate(b,'empty',1-clamp((b.dying||0)/.9,0,1))||c25Plate(b,'kneel',clamp((b.dying||0)/.9,0,1));
 if(K){const u=K.t<.65?1-K.t/.65:K.t<2.8?0:clamp((K.t-2.8)/1.4,0,1);return c25Plate(b,'empty',u)||c25Plate(b,'kneel',1-u);}
 if(h.state==='unfold'&&fb2IntroActive()&&XART.rdy('c25_intro_0'))return {a:{...C25_ART.banks.intro,key:'c25_intro_0',white:'c25_intro_0_hit',_hf22:true},k:1,rot:0,kind:'c25_intro_clean'};
 if(h.state==='fr_activation')return c25Plate(b,'hold',clamp(h.t/.8,0,1))||C25.base.blue.apply(this,arguments);
 return C25.base.blue.apply(this,arguments);
};
// The displayed whole actor's measured hammer is the only counter aperture.
hammerHeadPoint=function(b){
 if(c25Own(b)&&!b._hammer.throw&&!b._hammer.hc11Counter){const q=ha21Blue(b);if(q?.a.tip)return hb20World(q.a,q.a.tip,b,q.k,q.rot);}
 return C25.base.head.apply(this,arguments);
};
// The 1002 layer rejected unguided missiles after the native component hit
// had already consumed them. Resolve a real contact at this visible aperture.
C25.base.retinaDamage=retinaMissileDamage;
retinaMissileDamage=function(t,dmg,q){
 const b=t?._retinaOwner,at=c25Own(b)&&t._retinaId==='hammer'?hammerHeadPoint(b):null;
 if(at&&c25Counter(b)&&retinaTargetValid(t)&&hammerMissile(q)&&q.kind!=='spaceVolley'&&!q._auto&&!q._autoMissile&&Math.hypot(q.x-at.x,q.y-at.y)<=48){
  const bullet=_dmgBullet,src=_dmgSrc;_dmgBullet=q;_dmgSrc='missile';b._hammerModuleHit='hammer';
  try{hitBoss(dmg);return true;}finally{_dmgBullet=bullet;_dmgSrc=src;}
 }
 return C25.base.retinaDamage.apply(this,arguments);
};
hammerBossDamage=function(b,dmg){
 if(!c25Own(b))return C25.base.damage.apply(this,arguments);const h=b._hammer,hit=b._hammerModuleHit,q=_dmgBullet;
 if(h.recovery?.status==='charging'){
  b._hammerModuleHit=null;if(!(dmg>0))return 0;markHit(b);const A=fr27Armor(b);if(A)A.flash=.12;
  if(c25Counter(b)&&hit==='hammer'&&hammerMissile(q)&&q.kind!=='spaceVolley'&&!q._autoMissile&&!q._auto&&!q._passive){
   h.c25CounterToken=true;hammerRecoveryBreak(b);c25Log('raised-hammer-missile-counter');
  }else{weaponHitSfx('shield');if(hit==='hammer')hm10ShieldImpact(b,hammerHeadPoint(b).x,hammerHeadPoint(b).y);}
  return 0;
 }
 if(hit==='hammer'&&!h.throw)b._hammerModuleHit=null;
 h.hm10BreakPending=false;
 return C25.base.damage.call(this,b,dmg);
};
hammerBossModuleBreak=function(b,which){if(c25Own(b)&&which==='hammer'){b._hammer.hm10BreakPending=false;b._hammer.hammerHP=Math.max(1,b._hammer.hammerHP);markHit(b);return;}return C25.base.module.apply(this,arguments);};
hammerWhirlDisarm=function(b){if(c25Own(b)){markHit(b);return;}return C25.base.disarm.apply(this,arguments);};
hammerRecoveryBreak=function(b){
 if(!c25Own(b))return C25.base.break.apply(this,arguments);const h=b._hammer;
 if(!h.c25CounterToken||h.recovery?.status!=='charging')return;
 delete h.c25CounterToken;const at={...hammerHeadPoint(b)},r=C25.base.break.apply(this,arguments);
 h.c25Knock={t:0,from:at,away:{x:clamp(b.x+(b.x<worldWidth()/2?180:-180),camLeftX()+45,camRightX()-45),y:viewTopY()+30}};
 h.knockedHammer=null;h.hm10BreakPending=false;h.hc11Counter=null;h.whirl=null;
 delete h._hj22Pair;delete h._hf22StormPair;delete h.er23DepthCombo;h.c25CounterState=h.state;
 b20Cue('hammerThrow');return r;
};
fr27Restore=function(b){
 const r=C25.base.restore.apply(this,arguments);
 if(c25Own(b)&&b._hammer.recovery?.status==='charging'){
  const q=typeof c26Pose==='function'?c26Pose(b,'shield',7):c25Plate(b,'hold',1),tip=q?.a.tip;
  if(tip){const top=q.a.bounds?.[1]??tip[1]-45;
   b._hammer.c25ChargeY=Math.max(b.y,viewTopY()+145-(tip[1]-q.a.pivot[1])*q.k,
    viewTopY()+132-(top-q.a.pivot[1])*q.k);}
 }
 return r;
};
hammerBossTick=function(b,dt){
 if(!c25Own(b))return C25.base.tick.apply(this,arguments);const h=b._hammer,K=h.c25Knock;h.hm10BreakPending=false;
 if(K&&!b.dead){
  K.t+=dt;h.t+=dt;h.chromiumT=(h.chromiumT||0)+dt;const A=fr27Armor(b);if(A){A.barrier=0;A.flash=Math.max(0,(A.flash||0)-dt);}
  if(K.t>=2.8&&!K.recalled){K.recalled=true;b20Cue('hammerMagnet');c25Log('hammer-magnetic-recall');}
  if(K.t>=4.3){delete h.c25Knock;h.hammerDestroyed=false;h.hammerHP=h.hammerMax;h.charged=false;h.empowered=false;h.frRecovery=false;h.frResume=null;
   if(A){A.barrier=0;if(A.stunCritical){A.stunCritical=false;A.rage=true;}}
   h.mode=h.c25CounterState==='storm_stun'?'storm':'hammer';hammerState(b,h.mode==='storm'?'storm_idle':'hammer');c25Log('hammer-caught');}
  return;
 }
 if(h.recovery?.status==='charging'&&h.c25ChargeY!=null){
  b.y+=clamp(h.c25ChargeY-b.y,-220*dt,220*dt);b._drawY=b.y;
 }
 const old=h.state,r=C25.base.tick.apply(this,arguments);
 if(h.state==='fr_activation'){
  const beat=Math.floor(Math.max(0,h.t-.4)/.48);if(h.t>=.4&&beat!==h.c25EnergyBeat){h.c25EnergyBeat=beat;b20Cue('lightning');c25Log('armor-energy-strike',{beat});}
 }
 if(old!==h.state)c25Log('state',{from:old,to:h.state});return r;
};
// Defer the native wall while older underlays draw, then HA21 flushes it once.
hm10WallDraw=function(b){if(c25Own(b)&&HA21.painting===b){HA21.deferredWall=b;return;}return C25.base.wall.apply(this,arguments);};
hammerGroundReticleDraw=function(){if(c25Own(boss))return;return C25.base.reticle.apply(this,arguments);};
hj22PairDraw=function(b,P){
 if(!c25Own(b))return C25.base.pair.apply(this,arguments);if(c25Depth(b)||b.dead)return;
 if(P.furiousMelee24)return C25.base.pair.apply(this,arguments);
 if(P.clock<1.2){const at=hammerHeadPoint(b);combatWarningDraw(P,{x:at.x,y:at.y,ex:P.target.x,ey:P.target.y,progress:clamp(P.clock/.85,0,1),width:124,fieldOnly:true});}
};
combatWarningDraw=function(owner,q){if(c25Depth(boss)&&(owner===boss||owner===boss._hammer.er23DepthCombo))return;return C25.base.warning.apply(this,arguments);};
function c25Bolt(from,to,t,width=22,alpha=1){
 const length=Math.hypot(to.x-from.x,to.y-from.y);if(!Number.isFinite(length)||length<1)return;
 const key='arch_hammer_lightning_0926';if(!XART.rdy(key))return;const im=XART.get(key),f=Math.floor(t*18)%8;
 ctx.save();ctx.translate(from.x,from.y);ctx.rotate(Math.atan2(to.y-from.y,to.x-from.x)-Math.PI/2);ctx.globalAlpha*=alpha;ctx.imageSmoothingEnabled=false;
 ctx.drawImage(im,f%4*384+78,Math.floor(f/4)*512+48,228,416,-width/2,0,width,length);ctx.restore();
}
function c25ChargeDraw(b){
 const h=b._hammer,activation=h.state==='fr_activation';if(!activation&&!c25Counter(b))return;
 const head=hammerHeadPoint(b),t=h.t;
 if(activation&&t>.35&&t<FR27_ACT.plate){
  // Alternating authored bolts converge on the actual raised hammer and then
  // conduct into shoulders/chest, rather than a detached floating core.
  const beat=Math.floor((t-.35)/.24),side=beat%2?1:-1;
  c25Bolt({x:head.x+side*130,y:viewTopY()-20},head,t,36);
  c25Bolt(head,{x:b.x+side*56,y:b.y-18},t+.2,26,.9);
  c25Bolt({x:b.x+side*56,y:b.y-18},{x:b.x+15,y:b.y-40},t+.4,18,.8);
 }
 hj22Light('blue',head);
}
function c25KnockDraw(b){
 const K=b._hammer.c25Knock;if(!K)return;const t=K.t,fly=clamp(t/.65,0,1),back=clamp((t-2.8)/1.5,0,1),a=typeof c27Row==='function'?c27Row('takeoff_'+c26Material(b),0):hf22Row('blue_jump',0),to=c35Catch(b).at;
 const u=back*back*(3-2*back),at={x:lerp(lerp(K.from.x,K.away.x,fly),to.x,u),y:lerp(lerp(K.from.y,K.away.y,fly),to.y,u)},scale=lerp(lerp(1,.16,fly),c35Catch(b).scale,u),angle=back>0?lerp(5.2,c35Catch(b).angle,u):t*8;
 if(back>0)c25Bolt(to,at,t,12,.7);
 c35Tool(at,angle,Math.max(b.flash||0,b._lastPart?.flash||0),scale);
 C25.lastTool={...at,scale,back};
}
hammerStunEffectsDraw=function(b){if(c25Own(b)){c25KnockDraw(b);return;}return C25.base.stun.apply(this,arguments);};
hammerBossDraw=function(b){
 if(!c25Own(b))return C25.base.draw.apply(this,arguments);const h=b._hammer;
 if(b.dead||h.c25Knock){const q=ha21Blue(b);if(q){hammerBossAtmosphereDraw(b);ha21Body(b,q);c25KnockDraw(b);return;}}
 if(h.state==='fr_activation'){
  const q=ha21Blue(b);if(q){hammerBossAtmosphereDraw(b);ha21Body(b,q);c25ChargeDraw(b);return;}
 }
 const r=C25.base.draw.apply(this,arguments);
 if(!b.dead&&h.state==='spell')for(const q of h.spellTargets||[]){
  combatWarningDraw(b,{x:q.x,y:PLAY.y,ex:q.x,ey:hammerWarningFloorY(),progress:clamp(h.t/2.35,0,1),width:44,fieldOnly:true});
 }
 c25ChargeDraw(b);return r;
};
bossDie=function(){const b=boss;if(c25Own(b)){b._hammer.c25ArmorAtDeath=!!(fr27Armor(b)?.activated&&fr27Armor(b)?.hp>0);delete b._hammer.c25Knock;}
 return C25.base.death.apply(this,arguments);};
// The old special death renderer bypassed hammerBossDraw entirely.
C25.base.drawBoss=drawBoss;
drawBoss=function(){if(c25Own(boss)&&boss.dead)return hammerBossDraw(boss);return C25.base.drawBoss.apply(this,arguments);};
window.BOF_CHRONOS_CONTRACT=C25;

/* GPT authored whole plates: one material-specific actor for the full attack,
   fixed pivots, real hammer landmarks, and continuous retreat ownership. */
const C26={base:{blue:ha21Blue,paint:b20Image,flash:ha21Flash,state:hammerState,tick:hammerBossTick,
 draw:hammerBossDraw,head:hammerHeadPoint,landing:ha21Landing,giant:hammerGiantArm,
 at:bossHitTest,damage:hammerBossDamage,retina:retinaMissileDamage,wall:hm10WallDraw},events:[]};
for(const a of Object.values(C26_ART.sheets))XART._src[a.key]=a.path;
for(const [name,a]of Object.entries(C26_ART.banks))for(let f=0;f<a.count;f++)for(const hit of ['', '_hit'])
 BOFX.cells['c26_'+name+'_'+f+hit]=[a.sheet+hit,f%a.cols*a.w,Math.floor(f/a.cols)*a.h,a.w,a.h];
function c26Warm(){return Object.values(C26_ART.sheets).map(a=>XART.rdy(a.key)).every(Boolean);}
const c26Load=stageLoadBegin;
stageLoadBegin=function(n,keys){if(n===5)Snd.prepare(['enemyLaser','enemyPulseLaserAlien','hammerMagnet','hammerThrow','hammerLeap','hammerImpact']);return c26Load.call(this,n,[...(keys||[]),...(n===5?Object.values(C26_ART.sheets).map(a=>a.key):[])]);};
function c26Material(b){return fr27Armor(b)?.activated&&fr27Armor(b)?.hp>0?'chrome':'regular';}
function c26Row(bank,f){const a=C26_ART.banks[bank];if(!a)return null;f=Math.min(a.count-1,Math.max(0,Math.floor(f)));return {...a,...a.frames[f],key:'c26_'+bank+'_'+f,white:'c26_'+bank+'_'+f+'_hit',_hf22:true,_c26:true,frame:f,bank};}
function c26Pose(b,bank,f,k=1,material=c26Material(b)){const a=c26Row(bank+'_'+material,f);return a&&XART.rdy(a.key)&&XART.rdy(a.white)?{a,k,rot:0,kind:'c26_'+bank+'_'+material}:null;}
// Native double/side swings consume the same measured plates as the renderer.
for(const material of ['regular','chrome']){
 const suffix=material==='chrome'?'_armor':'';
 HF22_ART.banks['blue_jump'+suffix]=Array.from({length:8},(_,i)=>c26Row('jump_'+material,i));
 HF22_ART.banks['blue_sides'+suffix]=[0,0,1,2,3,4,4,4,4,3,2,1,0,0,0].map(i=>c26Row('spin_'+material,i));
}
HF22_ART.phases.blue={...HF22_ART.phases.blue,windEnd:2,strikeEnd:4};
C26.base.row=hf22Row;C26.base.furiousPose=hf22Pose;
hf22Row=function(bank,f){if(c25Own(boss)&&['blue_jump','blue_sides'].includes(bank)){
 const rows=HF22_ART.banks[bank+(c26Material(boss)==='chrome'?'_armor':'')];return rows[Math.min(rows.length-1,Math.max(0,Math.floor(f)))];}
 return C26.base.row.apply(this,arguments);};
hf22Pose=function(b,bank,f){if(c25Own(b)&&['blue_jump','blue_sides'].includes(bank)){
 const rows=HF22_ART.banks[bank+(c26Material(b)==='chrome'?'_armor':'')],a=rows[Math.min(rows.length-1,Math.max(0,Math.floor(f)))];
 if(XART.rdy(a.key)&&XART.rdy(a.white))return{a,k:1,rot:0,kind:bank+'_'+c26Material(b)};
 }return C26.base.furiousPose.apply(this,arguments);};
function c26Paint(a,x,y,k=1,rot=0,flash=0){const key=flash>0?a.white:a.key;if(!XART.rdy(key))return false;
 ctx.save();ctx.translate(x,y);ctx.rotate(rot);ctx.imageSmoothingEnabled=false;
 ctx.drawImage(XART.get(key),-a.pivot[0]*k,-a.pivot[1]*k,a.w*k,a.h*k);ctx.restore();return true;}
b20Image=function(a,x,y,k=1,rot=0,flash=0){return a?._c26?c26Paint(a,x,y,k,rot,flash):C26.base.paint.apply(this,arguments);};
ha21Flash=function(b,q){if(q?.a?._c26)return c26Paint(q.a,b.x,b.y,q.k,q.rot,Math.max(b.flash||0,b._lastPart?.flash||0));return C26.base.flash.apply(this,arguments);};
ha21Blue=function(b){if(!c25Own(b)||b.dead||b._hammer.c25Knock)return C26.base.blue.apply(this,arguments);
 const h=b._hammer,s=h.state,t=h.t||0,R=h.c26Return;
 if(s==='unfold')return c26Pose(b,'shield',0,1,'regular');
 if(R)return c26Pose(b,'jump',5+Math.min(2,Math.floor(R.t/R.duration*3)),R.scale);
 if(s==='uncurl'){const u=clamp(t/1.65,0,1),q=c26Pose(b,'unfold',Math.min(3,Math.floor(u*4)),lerp(.48,1,u));if(q)q.a.pivot=[288,lerp(288,328,u)];return q;}
 if(s==='curl'){const u=clamp(t/HAMMER_BALL_WARN,0,1),q=c26Pose(b,'unfold',3-Math.min(3,Math.floor(u*4)),lerp(1,.48,u));if(q)q.a.pivot=[288,lerp(328,288,u)];return q;}
 if(s==='ball'){const q=c26Pose(b,'unfold',0,.48);if(q){q.a.pivot=[288,288];q.rot=h.angle||0;}return q;}
 if(s==='fr_activation')return c26Pose(b,'activation',Math.min(7,Math.floor(clamp(t/FR27_ACT.end,0,1)*8)),1,'regular');
 if(h.recovery?.status==='charging'||s==='shield')return c26Pose(b,'shield',Math.min(7,Math.floor(t/(s==='shield'?.95:1.4)*8)));
 if(['whirl_warn','whirl_turn','whirlwind','fr_twirl'].includes(s))return c26Pose(b,'spin',((Math.floor(h.c26SpinClock||0)%8)+8)%8);
 if(s.startsWith('giant_')){const f=s==='giant_idle'?0:s==='giant_windup'?Math.min(2,Math.floor(t/.48*3)):s==='giant_rise'||s==='giant_warn'?2:s==='giant_dive'?2+Math.min(2,Math.floor(t/.52*3)):4;return c26Pose(b,'jump',f,hammerDepthScale(b));}
 if(['hammer','storm_idle','hammer_catch','leap_reset','back'].includes(s)&&!h.hammerDestroyed)return c26Pose(b,'shield',0);
 return C26.base.blue.apply(this,arguments);
};
ha21Landing=function(b,target,kind,frame,scale){if(c25Own(b)&&['slam','jump'].includes(kind)){
 const q=c26Pose(b,'jump',4,b._hammer.state.startsWith('giant_')?1.65:1);if(q)return hb20World(q.a,q.a.pivot,{x:target.x-(q.a.tip[0]-q.a.pivot[0])*q.k,y:target.y-(q.a.tip[1]-q.a.pivot[1])*q.k},1,0);
 }return C26.base.landing.apply(this,arguments);};
hammerState=function(b,s){const h=b?._hammer,own=c25Own(b),from=h?.state,point=own?{x:b.x,y:b.y}:null,scale=own?(ha21Blue(b)?.k||1):1;
 const r=C26.base.state.apply(this,arguments);if(!own)return r;
 if(['back','leap_reset','giant_recover'].includes(s))h.c26Return={t:0,duration:1.05,from:point,fromScale:scale,scale,state:s};
 else if(s!=='giant_warn')delete h.c26Return;
 if(s==='ball')h.c26Ball={t:0,volley:0,next:.9,aim:null};
 if(s==='uncurl')b20Cue('bossWeaponCharge');
 if(['whirl_warn','whirl_turn'].includes(s)&&!['whirlwind','whirl_warn','whirl_turn'].includes(from))h.c26SpinClock=0;
 return r;
};
// Retain the physical departure point; the old arm routine snapped to a new X/Y.
hammerGiantArm=function(b){if(!c25Own(b))return C26.base.giant.apply(this,arguments);const h=b._hammer;
 h.countered=false;b._noHit=false;hammerTarget(b);h.giantFromX=b.x;h.giantFromY=b.y;hammerState(b,'giant_warn');
 b20Cue('bossWeaponCharge');};
function c26Recoil(b){const h=b._hammer,T=h.throw;markHit(b);if((h.c26HitGate||0)>0)return false;
 h.c26HitGate=.16;if(T){T.er23Direction=-(T.er23Direction||1);T.er23ReflectCd=.16;T.hitCd=.16;}
 else{h.c26Backspin=.48;h.c26SpinClock=(h.c26SpinClock||0)-.7;}
 b20Cue('hammerMagnet');C26.events.push({type:'hammer-reversed',time:efxClock,detached:!!T,state:h.state});return true;
}
function c26Shootable(b){return c25Own(b)&&!b.dead&&!b._noHit&&b._hammer.recovery?.status!=='charging'&&
 (!!b._hammer.throw||['whirl_warn','whirl_turn','whirlwind','fr_twirl'].includes(b._hammer.state));}
function c26BallLaser(x,y,angle,speed,silent){
 // Use the approved enemy-laser chip cue by its warmed owner key, independent
 // of player weapons and historical aliases. Volley partners remain silent.
 const r=hammerLaser(x,y,angle,speed,true);if(!silent)Snd.play('enemyLaser');return r;
}
bossHitTest=function(x,y){const b=boss;if(c26Shootable(b)){const at=hammerHeadPoint(b);if(Math.hypot(x-at.x,y-at.y)<43){b._hammerModuleHit='hammer';return true;}}
 return C26.base.at.apply(this,arguments);};
hammerBossDamage=function(b,dmg){if(c26Shootable(b)&&b._hammerModuleHit==='hammer'){b._hammerModuleHit=null;if(dmg>0)c26Recoil(b);return 0;}return C26.base.damage.apply(this,arguments);};
retinaMissileDamage=function(t,dmg,q){const b=t?._retinaOwner;if(t?._retinaId==='hammer'&&c26Shootable(b)&&retinaTargetValid(t)){
 const at=hammerHeadPoint(b);if(q&&Math.hypot(q.x-at.x,q.y-at.y)<48){c26Recoil(b);return true;}}
 return C26.base.retina.apply(this,arguments);};
hammerBossTick=function(b,dt){if(!c25Own(b)||b.dead)return C26.base.tick.apply(this,arguments);const h=b._hammer;
 h.c26HitGate=Math.max(0,(h.c26HitGate||0)-dt);h.c26Backspin=Math.max(0,(h.c26Backspin||0)-dt);
 h.c26SpinClock=(h.c26SpinClock||0)+dt*(h.c26Backspin>0?-12:12);
 const R=h.c26Return;if(R){R.t+=dt;h.t+=dt;const u=clamp(R.t/R.duration,0,1),e=u*u*(3-2*u);
 b.x=lerp(R.from.x,(camLeftX()+camRightX())/2,e);b.y=lerp(R.from.y,VH*.34,e);b._drawY=b.y;R.scale=lerp(R.fromScale,1,e);
 if(u>=1){delete h.c26Return;b._noHit=false;if(R.state==='giant_recover'&&--h.giantLeft>0)hammerState(b,'giant_idle');else{if(R.state!=='leap_reset')h.attackCycle++;hammerState(b,h.mode==='storm'?'storm_idle':'hammer');}}
 return;}
 if(h.state==='ball'){
  const B=h.c26Ball||(h.c26Ball={t:0,volley:0,next:.9,aim:null});B.t+=dt;h.t+=dt;h.angle=(h.angle||0)+dt*9;h.rage=0;
  const speed=hammerFurious()?1.45:1;b.x+=(h.vx||150)*dt*speed;b.y+=(h.vy||165)*dt*speed;
  const l=camLeftX()+56,r=camRightX()-56,t=viewTopY()+56,bt=hammerWarningFloorY()-56;
  if(b.x<l){b.x=l;h.vx=Math.abs(h.vx||150);}if(b.x>r){b.x=r;h.vx=-Math.abs(h.vx||150);}
  if(b.y<t){b.y=t;h.vy=Math.abs(h.vy||165);}if(b.y>bt){b.y=bt;h.vy=-Math.abs(h.vy||165);}b._drawY=b.y;
  // Ball mode is a physical ricochet attack, never a laser launcher.
  B.aim=null;
  if(B.t>=3.85){hammerState(b,'uncurl');C26.events.push({type:'ball-unfold',volleys:0,time:efxClock});}return;
 }
 if(h.state==='uncurl'){h.t+=dt;if(h.t>=1.65){h.novaShots=0;hammerState(b,'nova_charge');b20Cue('bossWeaponCharge');}return;}
 return C26.base.tick.apply(this,arguments);
};
// The generated foreground shield is part of the complete plate. Do not stack
// a second wall over it, or let an older underlay repaint the counter objective.
hm10WallDraw=function(b){if(c25Own(b)&&!b.dead&&['shield'].includes(b._hammer.state)||c25Own(b)&&b._hammer.recovery?.status==='charging')return;return C26.base.wall.apply(this,arguments);};
hammerBossDraw=function(b){if(!c25Own(b))return C26.base.draw.apply(this,arguments);const h=b._hammer;
 if(!b.dead&&['ball','curl','uncurl'].includes(h.state)){
  hammerBossAtmosphereDraw(b);const q=ha21Blue(b);if(q)ha21Body(b,q);
  const B=h.c26Ball;if(h.state==='ball'&&B?.aim){combatWarningDraw(b,{x:b.x,y:b.y,ex:B.aim.x,ey:B.aim.y,width:65,progress:clamp((B.t-B.next+.45)/.45,0,1),fieldOnly:true});}return;
 }
 const r=C26.base.draw.apply(this,arguments);
 if(c25Counter(b)){
  const q=ha21Blue(b),head=hammerHeadPoint(b),top=q?b.y+((q.a.headBounds||q.a.bounds)[1]-q.a.pivot[1])*q.k:head.y-45;
  const im=XART.rdy('boss_shoot_prompt')?XART.get('boss_shoot_prompt'):null;
  if(im){const scale=.65,w=im.width*scale,h=im.height*scale,x=clamp(head.x,camLeftX()+w/2+4,camRightX()-w/2-4),y=Math.max(viewTopY()+50,top-h-10);
   ctx.drawImage(im,Math.round(x-w/2),Math.round(y),w,h);C26.objective={x,y,bottom:y+h,hammerTop:top};}
 }return r;
};
window.BOF_CHRONOS_FRAMES=C26;

C26.base.combat=hammerCombatTick;
hammerCombatTick=function(b,dt){if(!c25Own(b)||b._hammer.state!=='whirlwind')return C26.base.combat.apply(this,arguments);
 const h=b._hammer,previous={...hammerHeadPoint(b)},cd=h.hitCd;h.hitCd=99;
 const r=C26.base.combat.apply(this,arguments);h.hitCd=cd;
 if(h.state==='whirlwind'&&h.hitCd<=0){const at=hammerHeadPoint(b),cycle=Math.floor((h.c26SpinClock||0)/8);
  if(h.c26SweepCycle!==cycle){h.c26SweepCycle=cycle;h.c26SweepHits=new Set();}
  b20HitSegment(b,previous,at,34,'Chronos extended hammer rotation',h.c26SweepHits);
 }return r;
};
