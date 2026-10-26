"use strict";
/* Absorptive Chromium, clear counter cues, and bounded stage-native ambushes. */
const CP12={events:[],age:0,stage:0,next:12,serial:0,base:{tick:hammerBossTick,draw:hammerBossDraw,damage:hammerBossDamage,update:updatePlay,enemy:drawEnemy}};
function cp12Log(event,data={}){CP12.events.push({event,...data});if(CP12.events.length>180)CP12.events.shift();}
function cp12Caption(b,text){b._hammer.cp12Caption={text,t:2.5};cp12Log('caption',{text});}
function cp12Absorb(b,q){q.dead=true;const h=b._hammer;h.cp12Hit=.18;if((h.cp12Sound||0)<=0){h.cp12Sound=.09;Audio.SFX.shieldHitCombat?.();hm10ShieldImpact?.(b,q.x,q.y);cp12Log('shield-absorb');}}
hammerBossTick=function(b,dt){const h=b._hammer;h.cp12Sound=Math.max(0,(h.cp12Sound||0)-dt);h.cp12Hit=Math.max(0,(h.cp12Hit||0)-dt);if(h.cp12Caption)h.cp12Caption.t-=dt;
 const old=h.cp12State,wall=hm10WallActive(b)||b._hammerTime?.shield;
 if(wall){const healing=h.recovery?.status==='charging',head=healing?hammerHeadPoint(b):null;
  for(const q of pBullets){if(q.dead||q.vy>=0)continue;const y=b._hammerTime?.shield?ht27WallBounds(b._hammerTime).y:b.y+85;
   if(Math.abs(q.y-y)>30||Math.abs(q.x-b.x)>150)continue;
   if(healing&&(hammerMissile(q)||Math.abs(q.x-head.x)<FR27_HAMMER_LANE))continue;cp12Absorb(b,q);}
  if(b._hammerTime)b._hammerTime.reflections=[];
 }
 const r=CP12.base.tick.apply(this,arguments);
 if(h.state!==old){if(h.state==='storm_raise')cp12Caption(b,'Gotta Recharge!');else if(h.state==='shield'||h.state==='fr_activation')cp12Caption(b,'Chromium Shield, Activate!');else if(h.state==='uncurl')cp12Caption(b,"Is that the best you've got, mortal?");}
 h.cp12State=h.state;return r;};
const cp12TimeTick=ht27Tick;
ht27Tick=function(b,dt){const d=b._hammerTime;if(d?.shield){d.cp12Sound=Math.max(0,(d.cp12Sound||0)-dt);const wall=ht27WallBounds(d);
 for(const q of pBullets){if(q.dead||q.vy>=0||q.y<wall.y-26||q.y>wall.y+26)continue;q.dead=true;if(d.cp12Sound<=0){d.cp12Sound=.09;Audio.SFX.shieldHitCombat?.();hm10ShieldImpact(b,q.x,q.y);cp12Log('password-shield-absorb');}}
 d.reflections=[];}return cp12TimeTick.apply(this,arguments);};
hammerBossDamage=function(b,dmg){if(hm10WallActive(b)&&b._hammer?.recovery?.status!=='charging'){b._hammer.cp12Hit=.18;if((b._hammer.cp12Sound||0)<=0){b._hammer.cp12Sound=.09;Audio.SFX.shieldHitCombat?.();}return 0;}return CP12.base.damage.apply(this,arguments);};
hammerBossDraw=function(b){CP12.base.draw.apply(this,arguments);if(b.dead)return;const h=b._hammer;
 if(h.recovery?.status==='charging'&&!(typeof c25Own==='function'&&c25Own(b))){const q=hammerHeadPoint(b),x=clamp(q.x,camLeftX()+45,camRightX()-45),y=clamp(q.y-40,PLAY.y+65,PLAY.y+PLAY.h-50);bossShootGraphic(x,y+14);}
 if(h.cp12Caption?.t>0){ctx.save();const x=clamp(b.x,camLeftX()+150,camRightX()-150),y=Math.max(PLAY.y+26,b.y-125);ctx.fillStyle='rgba(3,8,17,.9)';ctx.fillRect(x-148,y-17,296,31);bmfDrawOn(ctx,window.BOF_UI_FACE||'game',h.cp12Caption.text.toUpperCase(),x,y-6,10,'center');ctx.restore();}
};
/* Owned flame recording: override the later chip alias and stretched chip variants. */
if(window.BOF_CHIP_PASS){const a=window.BOF_CHIP_PASS;a.bank.cues.firewallLaunch.file='../sounds/firewall_flamethrower_1012.mp3';
 a.firewall=function(w){if(!w||player.dead)return null;const v=a.sound(w,'firewallLaunch',{gain:1,loop:true,offset:0});if(v){v.owner=w;v.seconds=10;}return v;};}
function cp12Ambush(){const stage=run.stage,side=CP12.serial++%3,fromSouth=side===0,left=side===1,x=fromSouth?camLeftX()+VW*.72:left?camLeftX()-35:camRightX()+35,y=fromSouth?PLAY.y+PLAY.h+28:PLAY.y+PLAY.h*.52;
 // Depth is an entrance animation, not extra armour. Let the same family
 // constructor own health, including its difficulty and co-op adjustments.
 const e=spawnEnemy(stage===1?'s1jetDelta':'ash',x,y,{pattern:'straight'});if(!e)return;const t={t:0,ox:x,oy:y,tx:camLeftX()+VW*(fromSouth?.84:left?.12:.88),ty:PLAY.y+PLAY.h*(fromSouth?.80:.64),scale:1.6,round:0,side};e._cp12=t;e.x=x;e.y=y;e.pattern='straight';e.shoots=false;e.vx=e.vy=0;e._noSep=true;cp12Log('ambush',{stage,side});}
updatePlay=function(dt){const r=CP12.base.update.apply(this,arguments);if(![1,2].includes(run.stage)||state!==GS.PLAY)return r;
 if(CP12.stage!==run.stage||stageTimer<CP12.lastTimer){CP12.stage=run.stage;CP12.age=0;CP12.next=12;}CP12.lastTimer=stageTimer;CP12.age+=dt;
 const blocked=bossActive||subBossActive||warnT>0||player.dead||debugFight||wfx?.fseq;
 const high=diffKey==='furious'||diffKey==='insanity',powered=(run.shield>=3&&run.speedLevel>=3);
 if(!blocked&&CP12.age>=CP12.next&&(high||powered)&&enemies.filter(e=>e._cp12&&!e.dead).length<1&&eBullets.length<90){cp12Ambush();CP12.next=CP12.age+(high?10:16);}
 for(const e of enemies){const q=e._cp12;if(!q||e.dead||e._dyingT!=null)continue;q.t+=dt;e.shoots=false;e.vx=e.vy=0;const k=clamp(q.t/1.15,0,1),ease=1-(1-k)**3;e.x=lerp(q.ox,q.tx,ease);e.y=lerp(q.oy,q.ty,ease);q.scale=lerp(1.6,1,k);
  if(q.t>=1.15&&q.t<2.2){if(!q.aim)q.aim={x:player.x,y:player.y};combatWarningTick(e,'cp12-rocket',q.t-1.15,1.05);}
  const count=high?3:2;if(!blocked&&q.aim&&q.round<count&&q.t>=2.2+q.round*.28){const angle=Math.atan2(q.aim.y-e.y,q.aim.x-e.x);for(const off of [-.20,0,.20]){eShoot(e.x,e.y,angle+off,high?4.1:3.2,'missile');const b=eBullets[eBullets.length-1];if(b)b._cp12=true;}q.round++;Audio.SFX.enemyMissile?.();cp12Log('rocket-volley',{stage:run.stage,round:q.round});}
  if(q.t>3.6){e.y=q.ty-(q.t-3.6)*190;if(e.y<PLAY.y-60)e.dead=true;}
 }return r;};
drawEnemy=function(e){if(!e._cp12||e.dead)return CP12.base.enemy.apply(this,arguments);const q=e._cp12;ctx.save();ctx.translate(e.x,e.y);ctx.scale(q.scale,q.scale);ctx.translate(-e.x,-e.y);CP12.base.enemy.apply(this,arguments);ctx.restore();if(q.aim&&q.t>=1.15&&q.t<2.2)combatWarningDraw(e,{x:e.x,y:e.y,ex:q.aim.x,ey:q.aim.y,progress:(q.t-1.15)/1.05,width:26});};
