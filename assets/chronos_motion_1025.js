"use strict";
/* Whole-actor banks. Spin uses the original HAMMER/HAMA two-handed plates,
   with body and hammer kept together and their original head landmarks. */
const C27={events:[],base:{blue:ha21Blue,tick:hammerBossTick,state:hammerState,depth:hammerDepthScale,
 landing:ha21Landing,restore:fr27Restore,wall:hm10WallDraw,release:hammerBoomerangRelease,
 grip:hammerGripPoint,tool:hf22Tool,aura:hf22Aura,draw:hammerBossDraw,arm:hammerGiantArm}};
for(const a of Object.values(C27_ART.sheets))XART._src[a.key]=a.path;
for(const [name,a]of Object.entries(C27_ART.banks))for(let f=0;f<a.count;f++)for(const hit of ['', '_hit'])
 BOFX.cells['c27_'+name+'_'+f+hit]=[a.sheet+hit,f%a.cols*a.cell[0],Math.floor(f/a.cols)*a.cell[1],...a.cell];
function c27Warm(){return Object.values(C27_ART.sheets).map(a=>XART.rdy(a.key)).every(Boolean);}
const c27Load=stageLoadBegin;
stageLoadBegin=function(n,keys){return c27Load.call(this,n,[...(keys||[]),...(n===5?Object.values(C27_ART.sheets).map(a=>a.key):[])]);};
function c27Row(bank,f){const a=C27_ART.banks[bank];if(!a)return null;f=clamp(Math.floor(f),0,a.count-1);
 return{...a.frames[f],w:C27_ART.worldSize[0],h:C27_ART.worldSize[1],pivot:C27_ART.pixelPivot.map(v=>v*C27_ART.worldScale),
 key:'c27_'+bank+'_'+f,white:'c27_'+bank+'_'+f+'_hit',_hf22:true,_c26:true,_c27:true,frame:f,bank};}
function c27Material(b){return hf22Red(b)?'red':c26Material(b);}
function c27Pose(b,bank,u=0,k=1,mat=c27Material(b)){const name=['activation','rage_charge'].includes(bank)?bank:bank+'_'+mat,a=C27_ART.banks[name];
 const row=a&&c27Row(name,clamp(u,0,1)*(a.count-1));return row&&XART.rdy(row.key)&&XART.rdy(row.white)?{a:row,k,rot:0,kind:'c27_'+name}:null;}
for(const mat of ['regular','chrome','red']){
 const suffix=mat==='chrome'?'_armor':mat==='red'?'_red':'';
 HF22_ART.banks['blue_jump'+suffix]=[...Array.from({length:17},(_,f)=>c27Row('windup_'+mat,f)),
  ...Array.from({length:16},(_,f)=>c27Row('strike_'+mat,f+1)),...Array.from({length:16},(_,f)=>c27Row('retract_'+mat,f+1))];
 HF22_ART.banks['blue_sides'+suffix]=[...[0,3,6,16,16,16,16].map(f=>c27Row('left_'+mat,f)),
  ...[0,3,6,16,16,16,16].map(f=>c27Row('right_'+mat,f)),c27Row('takeoff_'+mat,0)];
}
HF22_ART.phases.blue={...HF22_ART.phases.blue,windEnd:16,strikeEnd:32};
function c27Log(type,data={}){C27.events.push({type,time:efxClock,...data});if(C27.events.length>400)C27.events.shift();}
ha21Blue=function(b){if(!c25Own(b)||b.dead||b._hammer.c25Knock)return C27.base.blue.apply(this,arguments);
 // The music encounter owns its ship entrance, dance and STOP plates. Do not
 // paint a campaign idle/held-tool pose over those complete original frames.
 if(b._hammerTime&&b._hammerTime.mode!=='attack')return null;
 const h=b._hammer,s=h.state,t=h.t||0,R=h.c26Return;
 // Pickup owns its complete strike/toss/catch. The old slam must not keep
 // supplying a held head after the hammer has actually left his hand.
 if(h.hb20Pickup){const z=h.hb20Pickup.t,M=H22_ART.blueSlam;
  if(z>=HT23_PICKUP.toss)return null;
  const frame=z<.6?0:z<1.42?lerp(0,M.windEnd,clamp((z-.6)/.82,0,1)):
   z<HT23_PICKUP.hit?lerp(M.windEnd,M.strikeEnd,clamp((z-1.42)/.36,0,1)):M.strikeEnd;
  return h22Blue(b,frame);
 }
 // Original complete plate retains the approved hammer silhouette at rest.
 if(s==='unfold')return h22Pose('blue_slam',0,1.75);
 if(R)return c27Pose(b,'retract',R.t/R.duration,R.scale);
 if(s==='fr_activation')return h._ht23ArmorGun?null:t<C27_ARMOR.raise?c27Pose(b,'windup',t/C27_ARMOR.raise,1,'regular'):c27Pose(b,'activation',(t-C27_ARMOR.raise)/(C27_ARMOR.end-C27_ARMOR.raise));
 if(h._hf22Charge){const u=clamp(h._hf22Charge.t/1.8,0,1);
  return c27Pose(b,'windup',Math.min(1,u/.6),1,u>=.72?'red':c26Material(b));}
 if(h.recovery?.status==='charging'||s==='shield')return c27Pose(b,'windup',t/.85);
 if(h.c27Combo){const q=hf22PairPose(b,h.c27Combo);if(q)q.k=h.c27Combo.scale;return q;}
 if(['whirl_warn','whirl_turn','whirlwind','fr_twirl'].includes(s)){
  const n=C27_ART.banks.spin_regular.count,f=((Math.floor(h.c26SpinClock||0)%n)+n)%n;return c27Pose(b,'spin',f/(n-1));
 }
 if(s.startsWith('giant_')){
  const k=hammerDepthScale(b);
  if(s==='giant_idle')return h22Blue(b,0,1.75*k);
  if(s==='giant_windup')return c27Pose(b,'takeoff',t/.55*.55,k);
  if(s==='giant_rise')return c27Pose(b,'takeoff',.55+clamp(t/.8,0,1)*.45,k);
  if(s==='giant_bg_drop')return c27Pose(b,'land',t/.75,k);
  if(s==='giant_bg_land')return c27Pose(b,'land',1,k);
  if(s==='giant_bg_jump')return c27Pose(b,'windup',t/.85,k);
  if(s==='giant_warn')return c27Pose(b,'windup',1,k);
  if(s==='giant_dive')return c27Pose(b,'strike',t/.65,k);
  return c27Pose(b,'strike',1,k);
 }
 if(h._hf22StormPair||h._hj22Pair&&s==='recover')return C27.base.blue.apply(this,arguments);
 if(['warn','leap','recover','storm_warn','storm_slam','storm_split'].includes(s))return C27.base.blue.apply(this,arguments);
 if(['spin','revenge_charge'].includes(s))return c27Pose(b,'windup',t/(s==='spin'?HAMMER_SPIN_TIME:2));
 if(s==='throw')return c27Pose(b,'throw_empty',Math.min(1,t/.3));
 if(['spell','spell_blast'].includes(s)&&!h.hammerDestroyed)return c29Hold(b,s==='spell'?clamp(t/.8,0,1):1);
 if(['nova_charge','nova_release'].includes(s))return c27MissilePose(b);
 if(s==='enrage'&&!h.hammerDestroyed)return c27Pose(b,'takeoff',0);
 if(['hammer','storm_idle','hammer_catch','back','leap_reset'].includes(s)&&!h.hammerDestroyed)return h22Blue(b,0);
 return C27.base.blue.apply(this,arguments);
};
// Native collision and FOV owners use these same world-space head landmarks.
ha21Landing=function(b,target,kind,frame,scale){if(c25Own(b)&&['slam','jump'].includes(kind)){
 const a=c27Row('strike_'+c27Material(b),16),k=b._hammer.state.startsWith('giant_')?1.25:1;
 return{x:target.x-(a.tip[0]-a.pivot[0])*k,y:target.y-(a.tip[1]-a.pivot[1])*k};
 }return C27.base.landing.apply(this,arguments);};
hammerDepthScale=function(b){if(c25Own(b)){const h=b._hammer,s=h.state;
 if(h.c26Return)return h.c26Return.scale;
 if(h.c27Combo)return h.c27Combo.scale;
 if(['giant_bg_drop','giant_bg_land','giant_bg_jump','giant_warn'].includes(s))return .36;
 if(s==='giant_rise'||s==='giant_windup'||s==='giant_idle')return 1;
 if(s==='giant_dive')return lerp(.36,1.25,clamp(h.t/.65,0,1));
 if(s==='giant_sweep')return 1.25;
 }return C27.base.depth.apply(this,arguments);};
hammerState=function(b,s){const r=C27.base.state.apply(this,arguments);if(!c25Own(b))return r;const h=b._hammer;
 if(s==='giant_rise')h.c27Rise={x:b.x,y:b.y};
 if(s==='giant_bg_drop'){b.y=viewTopY()-210;b._drawY=b.y;h.c27Background={x:b.x,y:viewTopY()+180};}
 if(s==='giant_dive'){h.giantFromX=b.x;h.giantFromY=b.y;}
 if(s.startsWith('giant_'))c27Log('depth-phase',{state:s,x:b.x,y:b.y,scale:hammerDepthScale(b)});
 return r;
};
hammerGiantArm=function(b){if(!c25Own(b))return C27.base.arm.apply(this,arguments);
 const h=b._hammer;h.countered=false;hammerTarget(b);h.giantFromX=b.x;h.giantFromY=b.y;hammerState(b,'giant_warn');b20Cue('bossWeaponCharge');};
hammerBossTick=function(b,dt){if(!c25Own(b)||b.dead||b._hammer.c25Knock)return C27.base.tick.apply(this,arguments);
 const h=b._hammer,s=h.state;
 if(c27RageTick(b,dt))return;
 if(['nova_charge','nova_release'].includes(s)){c27MissileTick(b,dt*(hf22Red(b)?2:1));return;}
 // Double only the hammer attack clock, never dialogue, armor activation,
 // missile-counter healing windows, ball motion, or stun/recovery timers.
 if(hf22Red(b)&&!h._hf22Charge&&!h.recovery?.status?.includes('charging')&&
  (s.startsWith('giant_')||h.c27Combo||['warn','leap','recover','storm_warn','storm_slam','hf22_storm_combo','whirl_warn','whirl_turn','whirlwind','spin','throw','hammer_catch'].includes(s)))dt*=2;
 if(h.c27Combo){const P=h.c27Combo;P.clock+=dt;h.t+=dt;c27ComboTick(b,P);
  if(P.clock>=hf22PairDuration(P)){delete h.c27Combo;hammerState(b,'giant_recover');}return;}
 if(s.startsWith('giant_')&&!h.c26Return){
  h.t+=dt;h.hitCd=Math.max(0,(h.hitCd||0)-dt);
  if(s==='giant_idle'){if(h.t>=.46)hammerState(b,'giant_windup');}
  else if(s==='giant_windup'){if(h.t>=.55){hammerState(b,'giant_rise');b._noHit=true;b20Cue('hammerLeap');}}
  else if(s==='giant_rise'){const a=h.c27Rise||{x:b.x,y:h.oy};b.x=a.x;b.y=lerp(a.y,viewTopY()-470,clamp(h.t/.8,0,1));
   if(h.t>=.95)hammerState(b,'giant_bg_drop');}
  else if(s==='giant_bg_drop'){b.y=lerp(viewTopY()-210,h.c27Background.y,clamp(h.t/.75,0,1));if(h.t>=.75)hammerState(b,'giant_bg_land');}
  else if(s==='giant_bg_land'){if(h.t>=.3){hammerState(b,'giant_bg_jump');b20Cue('hammerLeap');}}
  else if(s==='giant_bg_jump'){b.y=h.c27Background.y-Math.sin(clamp(h.t/.85,0,1)*Math.PI/2)*55;if(h.t>=.85)hammerGiantArm(b);}
  else if(s==='giant_warn'){if(h.t>=.6){hammerState(b,'giant_dive');b._noHit=false;b20Cue('hammerThrow');}}
  else if(s==='giant_dive'){const u=clamp(h.t/.65,0,1),e=u*u,to=ha21Landing(b,{x:h.tx,y:h.ty},'slam',16,1.25);
   b.x=lerp(h.giantFromX,to.x,e);b.y=lerp(h.giantFromY,to.y,e);
   if(u>=1){hammerState(b,'giant_sweep');h.c27ImpactHit=new Set();shake=Math.max(shake,12);b20Cue('hammerImpact');h.leapFx=.01;h.leapFxX=h.tx;h.leapFxY=h.ty;
    const at=hammerHeadPoint(b);b20HitSegment(b,at,at,62,'Chronos depth hammer impact',h.c27ImpactHit);}}
  else if(s==='giant_sweep'){if(h.t>=.20){
   if(['hard','furious'].includes(diffKey)){const P=hj22Pair(b,'blue',{x:h.tx,y:h.ty});P.scale=1.25;hammerState(b,'c27_depth_combo');h.c27Combo=P;c27Log('double-and-sides-start');}
   else hammerState(b,'giant_recover');}}
  else return C27.base.tick.call(this,b,dt);
  b._drawY=b.y;return;
 }
 return C27.base.tick.call(this,b,dt);
};
fr27Restore=function(b){const r=C27.base.restore.apply(this,arguments);if(c25Own(b)&&b._hammer.recovery?.status==='charging'){
 const a=c27Row('windup_'+c27Material(b),16);b._hammer.c25ChargeY=viewTopY()+160-(a.tip[1]-a.pivot[1]);
 }return r;};
hammerBoomerangRelease=function(b){const at=c25Own(b)?{...hammerHeadPoint(b)}:null,r=C27.base.release.apply(this,arguments),T=b?._hammer?.throw;
 if(at&&T){T.x=T.ox=at.x;T.y=T.oy=at.y;T._hf22Origin={...at};}return r;};
hammerGripPoint=function(b){if(c25Own(b)&&(b._hammer.throw||b._hammer.state==='hammer_catch')){
 return c35Catch(b).at;
 }return C27.base.grip.apply(this,arguments);};
hf22Tool=function(b,at,angle){if(c25Own(b)){const a=hf22Row('blue_tool',((Math.floor(angle/TAU*32)%32)+32)%32);
 return a&&hf22Cell(a,at.x,at.y,Math.max(b.flash||0,b._lastPart?.flash||0));}return C27.base.tool.apply(this,arguments);};
hf22Aura=function(b){if(!c25Own(b))return C27.base.aura.apply(this,arguments);};
// The native shield has its own transparent animated field, in front of the
// intact palm-projecting actor. Never repaint a different weapon in this pass.
hm10WallDraw=function(b){if(!c25Own(b))return C27.base.wall.apply(this,arguments);};
hammerBossDraw=function(b){
 if(c25Own(b)&&!b.dead&&b._hammer._hf22Charge){hammerBossAtmosphereDraw(b);const q=ha21Blue(b);if(q)ha21Body(b,q);return;}
 const r=C27.base.draw.apply(this,arguments);if(!c25Own(b)||b.dead)return r;
 const h=b._hammer;if(h.state==='shield'||h.recovery?.status==='charging'){
  const t=h.t||0,u=clamp(t/.75,0,1);if(u>0){ctx.save();ctx.translate(b.x,b.y+55);ctx.scale(1.15*u,1.15*u);
   er23DrawBank('shield_wall',Math.floor(t*16)%ER23_ART.banks.shield_wall.count,0,0,Math.max(b.flash||0,fr27Armor(b)?.flash||0)>0);ctx.restore();}
 }return r;};
window.BOF_CHRONOS_MOTION=C27;

// Keep the native combo's cadence and collision owner, using the full current
// authored banks. A depth combo stays at its landing scale until it retreats.
function c27ComboTick(b,P){
 const furious=P.furiousMelee24,T=HF22_FURIOUS_COMBO,t=P.clock,k=P.scale||1;
 const impact=furious?T.impact:1.2,sideStart=furious?T.left.start:1.36;
 if(t<sideStart){const a=c27Row('strike_'+c27Material(b),16),u=clamp(t/impact,0,1);
  const end={x:P.target.x-(a.tip[0]-a.pivot[0])*k,y:P.target.y-(a.tip[1]-a.pivot[1])*k};
  c27VisibleWindup(b,P,end,k,impact,furious?T.lock:.85);
  if(t>=impact&&!P.impact){P.impact=true;const at=hammerHeadPoint(b);b20HitSegment(b,at,at,62*k,'Hammer second downward slam',P.hit);b20Cue('hammerImpact');c27Log('second-down');}
 }else if(furious){for(const side of ['left','right']){const z=T[side];if(t<z.start||t>=z.end)continue;
   if(!P[side+'Aim']){const ship=targetShip(b.x,b.y),a=c27Row(side+'_'+c27Material(b),16);
    P[side+'Aim']={x:ship.x,y:ship.y};P[side+'Origin']={x:b.x,y:b.y};P[side+'End']={x:ship.x-(a.tip[0]-a.pivot[0])*k,y:ship.y-(a.tip[1]-a.pivot[1])*k};}
   const o=P[side+'Origin'],e=P[side+'End'],u=clamp((t-z.start)/(z.hit-z.start),0,1);
   b.x=lerp(o.x,e.x,u*u*(3-2*u));b.y=lerp(o.y,e.y,u*u*(3-2*u));
   const at=hammerHeadPoint(b),previous=P[side+'Prev']||at;P[side+'Prev']=at;
   if(t>=z.hit){b20HitSegment(b,previous,at,30*k,'Hammer '+side+' sweep',P[side+'Hit']);
    if(!P[side+'Cue']){P[side+'Cue']=true;b20Cue('hammerThrow');c27Log(side+'-swing');}}
  }}
 b._drawY=b.y;
}
const c27OldFuriousPose=hf22FuriousPose;
hf22FuriousPose=function(b,P){if(!c25Own(b))return c27OldFuriousPose.apply(this,arguments);
 const T=HF22_FURIOUS_COMBO,t=P.clock;
 for(const side of ['left','right']){const z=T[side];if(t>=z.start&&t<z.end){
  const u=clamp((t-z.start)/(z.hit-z.start),0,1);
  return c27Pose(b,side,u,P.scale||1);}}
 return c27OldFuriousPose.apply(this,arguments);
};
const c27OldPose=hf22Pose,c27OldRow=hf22Row;
hf22Pose=function(b,bank,f){if(c25Own(b)&&['blue_jump','blue_sides'].includes(bank)){
 const mat=c27Material(b),rows=HF22_ART.banks[bank+(mat==='red'?'_red':mat==='chrome'?'_armor':'')],a=rows[clamp(Math.floor(f),0,rows.length-1)];
 return {a,k:1,rot:0,kind:bank+'_'+mat};}return c27OldPose.apply(this,arguments);};
hf22Row=function(bank,f){if(c25Own(boss)&&['blue_jump','blue_sides'].includes(bank))return hf22Pose(boss,bank,f).a;return c27OldRow.apply(this,arguments);};

// Hit feedback uses the same authored alpha mask; no replacement ball sprite.
C27.base.damage=hammerBossDamage;C27.base.paint=c26Paint;C27.tintCache=new Map();
hammerBossDamage=function(b,dmg){if(c25Own(b)&&b._hammer.state==='ball'&&dmg>0){b._hammer.c27BallMissile=hammerMissile(_dmgBullet);markHit(b);b.flash=Math.max(b.flash||0,.12);}
 return C27.base.damage.apply(this,arguments);};
c26Paint=function(a,x,y,k=1,rot=0,flash=0){
 if(c25Own(boss)&&boss._hammer.state==='ball'&&flash>0&&!boss._hammer.c27BallMissile){
  if(!XART.rdy(a.white))return false;let im=C27.tintCache.get(a.white);
  if(!im){const source=XART.get(a.white);im=document.createElement('canvas');im.width=source.width;im.height=source.height;const c=im.getContext('2d');c.drawImage(source,0,0);c.globalCompositeOperation='source-in';c.fillStyle='#ff3030';c.fillRect(0,0,im.width,im.height);C27.tintCache.set(a.white,im);}
  ctx.save();ctx.translate(x,y);ctx.rotate(rot);ctx.imageSmoothingEnabled=false;ctx.drawImage(im,-a.pivot[0]*k,-a.pivot[1]*k,a.w*k,a.h*k);ctx.restore();return true;
 }return C27.base.paint.apply(this,arguments);
};

// One Stage5 owner for the two power-ups and the three physical missile slams.
const C27_ARMOR={raise:.65,plate:2.9,end:3.35};
C27.base.beginRage=hf22BeginBlueRage;
hf22BeginBlueRage=function(b){
 if(!c25Own(b))return C27.base.beginRage.apply(this,arguments);
 const h=b._hammer;if(h._hf22Red||h._hf22Charge||!h.c27RagePending&&b.hp>b.maxhp*.15)return;
 h.c27RagePending=false;h._hf22Charge={t:0,resume:'hammer'};h.state='hf22_rage_charge';h.t=0;
 h.phasePending=false;h.hammerDestroyed=false;h.hammerHP=h.hammerMax;b._noHit=true;
 const A=fr27Armor(b);if(A){A.rage=false;A.stunCritical=false;A.checkpoints=[.75,.5,.35,.15];}
 hf22WarmRed(b);b20Cue('shadowCharge');c27Log('rage-charge-start',{hp:b.hp/b.maxhp});
};
function c27RageTick(b,dt){const h=b._hammer,A=fr27Armor(b);
 if(!h._hf22Red&&b.hp<=b.maxhp*.15)h.c27RagePending=true;
 if(A){A.rage=false;A.stunCritical=false;} // Retire the old two-hit/seven-second-rest rage controller.
 if(h.c27RagePending&&!h._hf22Charge&&!h.hb20Pickup&&!h.c25Knock&&!h.hc11Counter&&!h.c26Return&&
  h.recovery?.status!=='charging'&&['hammer','storm_idle','leap_reset','hammer_catch','fr_twirl','chain_cool','core_orbit'].includes(h.state))hf22BeginBlueRage(b);
 const C=h._hf22Charge;if(!C)return false;
 C.t+=dt;h.t+=dt;b._noHit=true;b._drawY=b.y;
 if(C.t>=1.8&&hf22WarmRed(b)){delete h._hf22Charge;h._hf22Red=true;h.rage=999;h.mode='hammer';h.phasePending=false;
  h._fb2RageDone=true;if(A){A.rage=false;A.stunCritical=false;}b._noHit=false;hammerState(b,'hammer');b20Cue('bossPhase');c27Log('rage-permanent',{hp:b.hp/b.maxhp});}
 return true;
}
C27.base.beginArmor=fr27BeginArmor;C27.base.activation=fr27ActivationTick;
fr27BeginArmor=function(b){const r=C27.base.beginArmor.apply(this,arguments);if(r&&c25Own(b)&&!b._hammer._ht23ArmorGun){
 const row=c27Row('activation',0),y=viewTopY()+122-(row.tip[1]-row.pivot[1]);
 const hArmor=b._hammer.frAct;hArmor.from={x:b.x,y:b.y};hArmor.y0=y;b._hammer.c27ArmorY=y;
 }return r;};
fr27ActivationTick=function(b,dt){if(!c25Own(b)||b._hammer._ht23ArmorGun)return C27.base.activation.apply(this,arguments);
 const h=b._hammer,A=fr27Armor(b),F=h.frAct||(h.frAct={from:{x:b.x,y:b.y},y0:b.y});
 h.t+=dt;b._noHit=true;h.empowered=false;h.empowerLevel=0;h.chromiumT=.85;
 const u=clamp(h.t/C27_ARMOR.raise,0,1),e=u*u*(3-2*u);b.y=lerp(F.from?.y??F.y0,F.y0,e);b._drawY=b.y;
 if(!F.locked&&h.t>=C27_ARMOR.plate){F.locked=true;A.activated=true;b20Cue('shieldUp');shake=Math.max(shake,5);c27Log('chromium-plated');}
 if(h.t>=C27_ARMOR.end){A.activated=true;b._noHit=false;h.frAct=null;hammerState(b,'hammer');}
};
C27.base.chargeDraw=c25ChargeDraw;
c25ChargeDraw=function(b){if(!c25Own(b)||b._hammer.state!=='fr_activation')return C27.base.chargeDraw.apply(this,arguments);
 if(b._hammer._ht23ArmorGun)return;
 const t=b._hammer.t,head=hammerHeadPoint(b);if(t>=C27_ARMOR.raise&&t<C27_ARMOR.plate){
 const side=Math.floor(t/.24)%2?1:-1;c25Bolt({x:head.x+side*130,y:viewTopY()-20},head,t,30);
 c25Bolt(head,{x:b.x-56,y:b.y-18},t+.2,20,.7);c25Bolt({x:b.x-56,y:b.y-18},{x:b.x+15,y:b.y-40},t+.4,14,.6);hj22Light('blue',head);}
};
const C27_MISSILE={wind:.70,impact:.95,cycle:1.40,count:3};
function c27MissilePose(b){const h=b._hammer;
 if(h.state==='nova_charge')return c27Pose(b,'takeoff',0);
 const t=Math.min(C27_MISSILE.cycle-.001,h.t%C27_MISSILE.cycle);
 if(t<C27_MISSILE.wind)return c27Pose(b,'windup',t/C27_MISSILE.wind);
 if(t<C27_MISSILE.impact)return c27Pose(b,'strike',(t-C27_MISSILE.wind)/(C27_MISSILE.impact-C27_MISSILE.wind));
 return c27Pose(b,'retract',(t-C27_MISSILE.impact)/(C27_MISSILE.cycle-C27_MISSILE.impact));
}
function c27MissileRing(b,index){const a=c27Row('strike_'+c27Material(b),16),at=hb20World(a,a.tip,b,1,0),count=hammerFurious()?16:12;
 for(let i=0;i<count;i++){const angle=TAU*(i+index*.5)/count;
  hammerLaser(at.x+Math.cos(angle)*12,at.y+Math.sin(angle)*12,angle,3.0,true);
  const shot=eBullets[eBullets.length-1];shot._owner=b;shot._c34Chromium=true;shot._c27Volley=index;}
 b._hammer.c27Impact={at,t:0};b20Cue('hammerImpact');b20Cue('enemyPulseLaserAlien');shake=Math.max(shake,6);
 c27Log('hammer-chromium-laser-impact',{index:index+1,count,at});
}
function c27MissileTick(b,dt){const h=b._hammer;h.t+=dt;h.hitCd=Math.max(0,(h.hitCd||0)-dt);
 if(h.c27Impact)h.c27Impact.t+=dt;
 if(h.state==='nova_charge'){
  const x=(camLeftX()+camRightX())/2,y=viewTopY()+260;
  b.x+=clamp(x-b.x,-260*dt,260*dt);b.y+=clamp(y-b.y,-260*dt,260*dt);
  if(h.t>=.8){h.novaShots=0;hammerState(b,'nova_release');}b._drawY=b.y;return;
 }
 while(h.novaShots<C27_MISSILE.count&&h.t>=h.novaShots*C27_MISSILE.cycle+C27_MISSILE.impact){c27MissileRing(b,h.novaShots);h.novaShots++;}
 if(h.t>=C27_MISSILE.count*C27_MISSILE.cycle){h.attackCycle++;h.c27Impact=null;hammerState(b,'hammer');}
 b._drawY=b.y;
}
C27.base.finalDraw=hammerBossDraw;
hammerBossDraw=function(b){const h=b?._hammer;
 if(c25Own(b)&&!b.dead&&['nova_charge','nova_release'].includes(h.state)){
  hammerBossAtmosphereDraw(b);hf22Aura(b);const q=ha21Blue(b);if(q)ha21Body(b,q);
  const t=h.t%C27_MISSILE.cycle;
  if(h.state==='nova_release'&&t<C27_MISSILE.wind){const a=hammerHeadPoint(b),p=targetShip(b.x,b.y);
   combatWarningDraw(b,{x:a.x,y:a.y,ex:p.x,ey:p.y,width:125,progress:t/C27_MISSILE.wind,fieldOnly:true});}
  if(h.c27Impact&&h.c27Impact.t<.18)hj22Light('blue',h.c27Impact.at);return;
 }return C27.base.finalDraw.apply(this,arguments);
};
C27.base.plane=hammerOnPlayerPlane;
hammerOnPlayerPlane=function(b){return c25Own(b)&&b._hammer.c27Combo?false:C27.base.plane.apply(this,arguments);};
const c27Sounds=stageLoadBegin;
stageLoadBegin=function(n,keys){if(n===5)Snd.prepare(['enemyPulseLaserAlien','hammerImpact','bossPhase','shieldUp']);return c27Sounds.apply(this,arguments);};

C27.base.materialPose=c26Pose;
c26Pose=function(b,bank,f,k=1,material=c26Material(b)){
 if(c25Own(b)&&hf22Red(b)&&C26_ART.banks[bank+'_red'])material='red';
 return C27.base.materialPose.call(this,b,bank,f,k,material);
};

// Keep the overhead wind-up inside the playfield, then connect that visible
// pose to the measured impact point. The previous arc lifted the second
// wind-up (and most of the hammer) completely behind the top HUD.
function c27VisibleWindup(b,P,end,k,impact,lock){const t=P.clock,u=clamp(t/impact,0,1);
 b.x=lerp(P.origin.x,end.x,u);
 if(t<lock){const q=hf22PairPose(b,P),a=q?.a,low=a?viewTopY()+64-(a.bounds[1]-a.pivot[1])*k:P.origin.y;
  b.y=Math.max(lerp(P.origin.y,end.y,u),low);P.c27StrikeFrom={x:b.x,y:b.y};
 }else{const from=P.c27StrikeFrom||P.origin,v=clamp((t-lock)/(impact-lock),0,1);b.x=lerp(from.x,end.x,v);b.y=lerp(from.y,end.y,v);}
 b._drawY=b.y;
}
C27.base.furiousTick=hf22FuriousTick;
hf22FuriousTick=function(b,P){const r=C27.base.furiousTick.apply(this,arguments);
 if(c25Own(b)&&P.clock<HF22_FURIOUS_COMBO.impact){const a=c27Row('strike_'+c27Material(b),16),end={x:P.target.x-a.tip[0]+a.pivot[0],y:P.target.y-a.tip[1]+a.pivot[1]};
  c27VisibleWindup(b,P,end,1,HF22_FURIOUS_COMBO.impact,HF22_FURIOUS_COMBO.lock);}
 return r;
};

// Retire the pre-refit loose hammer fallbacks beneath a current whole plate.
// The canonical HF22 plasma hammer still owns every real throw and recall.
C27.base.frame=hammerFrame;
hammerFrame=function(key){const im=C27.base.frame.apply(this,arguments);if(im)HA21.tags.set(im,'hammer_'+key);return im;};
C27.base.completeDraw=hammerBossDraw;
hammerBossDraw=function(b){if(!c25Own(b)||!ha21Blue(b)?.a?._c27)return C27.base.completeDraw.apply(this,arguments);
 const draw=ctx.drawImage;ctx.drawImage=function(im,...args){const key=HA21.tags.get(im);
  if(key&&/^(?:arch_hammer(?:_spin|_flight_0926)?|hammer_boomerang_hammer)$/.test(key))return;
  return draw.call(this,im,...args);};
 try{return C27.base.completeDraw.apply(this,arguments);}finally{ctx.drawImage=draw;}
};

// Aura is a traced derivative of the current authored plate. It shares the
// exact frame, pivot, rotation and depth scale; no freestanding flame sprite.
// Keep a small LRU: a full fight visits many different 448px poses.
C27.auraCache=new Map();C27.auraDraws=0;
function c27AuraStencil(key){if(C27.auraCache.has(key)){const a=C27.auraCache.get(key);C27.auraCache.delete(key);C27.auraCache.set(key,a);return a;}
 if(!XART.rdy(key))return null;const im=XART.get(key),pad=16,w=im.width+pad*2,h=im.height+pad*2;
 const make=()=>{const c=document.createElement('canvas');c.width=w;c.height=h;return c;},solid=make(),s=solid.getContext('2d');
 s.drawImage(im,pad,pad);s.globalCompositeOperation='source-in';s.fillStyle='#ffffff';s.fillRect(0,0,w,h);
 const rim=(radius,color)=>{const c=make(),g=c.getContext('2d');for(let i=0;i<12;i++){const a=i*TAU/12;g.drawImage(solid,Math.round(Math.cos(a)*radius),Math.round(Math.sin(a)*radius));}
  g.globalCompositeOperation='destination-out';g.drawImage(solid,0,0);g.globalCompositeOperation='source-in';g.fillStyle=color;g.fillRect(0,0,w,h);return c;};
 const a={pad,sourceW:im.width,sourceH:im.height,edge:rim(1,'#ffd0ca'),red:rim(3,'#ff2444'),outer:rim(6,'#b90027')};
 C27.auraCache.set(key,a);while(C27.auraCache.size>32)C27.auraCache.delete(C27.auraCache.keys().next().value);return a;
}
function c27TraceAura(b,q,x=b.x,y=b.y){if(!c25Own(b)||b.dead||!q?.a||!hf22Red(b)&&!b._hammer._hf22Charge)return;
 const a=q.a,m=c27AuraStencil(a.key);if(!m)return;const k=q.k??1,rx=a.w/m.sourceW,ry=a.h/m.sourceH;
 const charge=b._hammer._hf22Charge,amount=charge?clamp(charge.t/1.25,0,1):1,t=efxClock;
 ctx.save();ctx.translate(x,y);ctx.rotate(q.rot||0);ctx.scale(k,k);ctx.imageSmoothingEnabled=false;
 const paint=(im,alpha,up=0,expand=1)=>{ctx.save();ctx.globalAlpha*=alpha*amount;ctx.scale(expand,expand);
  ctx.drawImage(im,-a.pivot[0]-m.pad*rx,-a.pivot[1]-m.pad*ry-up,im.width*rx,im.height*ry);ctx.restore();};
 // Short upward-moving contour echoes leave the shoulders, arms and boots.
 // They stay within 18 world pixels of the authored silhouette at full scale.
 for(let i=0;i<3;i++){const u=(t*2.4+i/3)%1;paint(m.outer,.24*(1-u),u*8,1+u*.012);}
 paint(m.red,.62+.12*Math.sin(t*17));paint(m.edge,.66+.16*Math.sin(t*23));ctx.restore();C27.auraDraws++;
}
C27.base.traceBody=ha21Body;
ha21Body=function(b,q){c27TraceAura(b,q);return C27.base.traceBody.apply(this,arguments);};
