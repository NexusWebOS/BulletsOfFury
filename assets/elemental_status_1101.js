"use strict";
/* 1101 (Mike): Forge elements must read on the enemy. Toxic poisons (slow damage) and flashes green; electric wraps
   the target in a lightning swirl, chains static damage to neighbours and flashes yellow/blue/white; wind kicks the
   target back and flashes teal; chromium adds metallic damage with gray flashes and steel sparks. Every other element
   flashes its own colour too. Late layer: the native infusionOnHit, poisonTick, chainZap, the wind gust
   (audio_wind_1010) and the chromium mirror all stay; this only adds status, colour, the swirl and chromium's bonus. */
const EL11={busy:false,events:[],
 colour:{toxic:'#5dff4a',wind:'#47e6d2',chrome:'#a9b4c2',fire:'#ff6a1e',ice:'#9fdcff',water:'#3fa7ff',kinetic:'#cfe0ff',dark:'#b46cff'},
 cycle:{lightning:['#ffe03a','#7fb4ff','#ffffff'],prism:['#ff7a9a','#ffe27a','#7affc4','#7ab8ff','#d49aff']},
 base:{hit:infusionOnHit,flash:hitFlashColor,chain:chainZap,draw:drawEnemy,fx:updateEffects}};
function el11Log(event,data={}){EL11.events.push({event,t:efxClock,...data});if(EL11.events.length>800)EL11.events.shift();}
function el11Status(e,el,lv,t){if(!e)return;const s=e._el11;if(s&&s.el===el){s.t=Math.max(s.t,t);s.lv=Math.max(s.lv,lv);}else e._el11={el,lv,t};}
function el11Colour(el){const c=EL11.cycle[el];return c?c[Math.floor(efxClock*18)%c.length]:EL11.colour[el]||null;}
// Hit flashes take the element's colour while its status is live (toxic: for as long as the poison runs).
hitFlashColor=function(t,fallback){const s=t?._el11;if(s&&s.t>0){const c=el11Colour(s.el);if(c)return c;}return EL11.base.flash.apply(this,arguments);};
infusionOnHit=function(e,b,dmg){
 const el=b?._inf,first=!EL11.busy&&!!e&&!!el,lv=first?clamp(b._infLv||((run.infusion&&run.infusion.elem===el)?run.infusion.lv:1),1,5):0;
 const r=EL11.base.hit.apply(this,arguments);if(!first)return r;
 EL11.busy=true;
 try{
  el11Status(e,el,lv,.45);
  if(el==='toxic')el11Status(e,el,lv,Math.max(.45,e._poison||0));
  else if(el==='lightning'){
   e._el11Swirl=Math.max(e._el11Swirl||0,.55+.1*lv);
   // Level 1 has no native jump (depth lv-1 = 0); static always reaches at least one neighbour.
   if(lv===1&&b.kind!=='beam'&&efxClock-(e._el11ChainAt??-9)>.2){e._el11ChainAt=efxClock;EL11.base.chain(e.x,e.y,1,[e]);}
  }else if(el==='wind'){
   // The power of wind: a level-scaled kick straight back along the round's flight, on top of the native gust.
   if(!(typeof isSetPiece==='function'&&isSetPiece(e))&&e!==boss&&e!==subBoss&&efxClock-(e._el11KickAt??-9)>.14){
    e._el11KickAt=efxClock;const a=Math.atan2(b.vy||-1,b.vx||0),f=10+5*lv;e._el11Kick={vx:Math.cos(a)*f*9,vy:Math.sin(a)*f*9,t:.22};el11Log('kick',{lv});}
  }else if(el==='chrome'&&!b._mirror&&e.hp>0){
   // Metallic damage: a bonus slug of the same hit, plus steel sparks.
   const bonus=Math.max(1,Math.round(dmg*(.15+.05*lv)*10)/10);hitEnemy(e,bonus,true);el11Log('metal',{bonus});
   for(let i=0;i<3+lv&&particles.length<600;i++){const a=rnd(0,Math.PI*2),v=rnd(1.4,3.2);particles.push({x:e.x+rnd(-6,6),y:(e._drawY??e.y)+rnd(-6,6),vx:Math.cos(a)*v,vy:Math.sin(a)*v,life:rnd(.18,.34),t:0,r:rnd(1,2),color:i%2?'#ffffff':'#a9b4c2'});}
  }
 }finally{EL11.busy=false;}
 return r;
};
// Every target the static chain jumps to is wrapped too and flashes electric.
chainZap=function(x,y,depth,hitset){const r=EL11.base.chain.apply(this,arguments);
 if(Array.isArray(hitset))for(const o of hitset)if(o&&!o.dead){o._el11Swirl=Math.max(o._el11Swirl||0,.5);el11Status(o,'lightning',1,.4);}
 return r;};
updateEffects=function(dt){const r=EL11.base.fx.apply(this,arguments);
 // Bosses and minibosses can carry an element status too, so their timers run down here as well.
 if(state===GS.PLAY)for(const e of [...enemies,boss,subBoss]){if(!e||e.dead)continue;
  // A fresh hit of another element shows its own colour; a running poison takes the colour back afterwards.
  const s=e._el11;if(s){if(s.el==='toxic'&&e._poison>0)s.t=Math.max(s.t,e._poison);s.t-=dt;if(s.t<=0)e._el11=null;}else if(e._poison>0)e._el11={el:'toxic',lv:e._poisonLv||1,t:e._poison};
  if(e._el11Swirl>0)e._el11Swirl-=dt;
  const k=e._el11Kick;if(k&&e._dyingT==null){e.x+=k.vx*dt;e.y+=k.vy*dt;k.vx*=.82;k.vy*=.82;k.t-=dt;if(k.t<=0)e._el11Kick=null;}
  // A kicked unit stops at the top edge instead of being blown out of the playfield (where it would be culled).
  if((e._el11Kick||e._ap10Gust)&&e._dyingT==null){const top=viewTopY()+(e._drawH||e.h||28)*.45+8;if(e.y<top)e.y=top;}}
 return r;};
function el11Swirl(e,bank){if(!(e._el11Swirl>0)||typeof l21Draw!=='function')return;
 const size=Math.min(300,Math.max(e._drawW||e.w||28,e._drawH||e.h||28)*1.7),alpha=clamp(e._el11Swirl/.3,0,1)*(bank==='wrap_back'?.6:1);
 l21Draw(bank,efxClock+(e._el11Seed??(e._el11Seed=Math.random()*3)),e.x,e._drawY??e.y,size,0,alpha);}
drawEnemy=function(e){if(!e||e.dead)return EL11.base.draw.apply(this,arguments);
 el11Swirl(e,'wrap_back');const r=EL11.base.draw.apply(this,arguments);el11Swirl(e,'wrap_front');return r;};
/* Bosses and minibosses: the native element hook only runs for regular enemies (_hitEnemyCore), so a Forge element
   did nothing to them. They get a boss-safe version: colour, toxic poison ticks, the electric swirl plus a static
   chain into nearby enemies, chromium's metallic bonus. Wind only flashes (an encounter's choreography is never
   knocked around), and ice/fire keep their colour without the small-enemy freeze/burn branches. */
EL11.base.boss=hitBoss;EL11.base.sub=hitSubBoss;EL11.base.drawBoss=drawBoss;EL11.base.drawSub=drawSubBoss;
function el11BossHit(b,which,amount){const save=_dmgBullet;_dmgBullet=null;EL11.busy=true;
 try{if(which==='sub')EL11.base.sub(amount,b.x,b._drawY??b.y);else EL11.base.boss(amount);}finally{_dmgBullet=save;EL11.busy=false;}}
function el11BossProc(b,which,dmg){const q=_dmgBullet,el=q&&q._inf;if(!b||b.dead||!el||!INFUSIONS[el]||EL11.busy||!(dmg>0))return;
 if(efxClock-(b._el11ProcAt??-9)<.1)return;b._el11ProcAt=efxClock;const lv=clamp(q._infLv||1,1,5),y=b._drawY??b.y;
 el11Status(b,el,lv,.45);el11Log('boss-hit',{el,which});
 if(typeof efxBurst==='function'&&efxClock-(b._efxAt??-9)>.12){b._efxAt=efxClock;efxBurst(el,b.x+rnd(-14,14),y+rnd(-14,14),30+lv*9);}
 if(el==='toxic'){b._el11Poison=Math.max(b._el11Poison||0,2.2+.6*lv);b._el11PoisonLv=lv;}
 else if(el==='lightning'){b._el11Swirl=Math.max(b._el11Swirl||0,.55+.1*lv);
  if(efxClock-(b._el11ChainAt??-9)>.28){b._el11ChainAt=efxClock;EL11.busy=true;try{EL11.base.chain(b.x,y,Math.max(1,lv-1),[b]);}finally{EL11.busy=false;}}}
 else if(el==='chrome'&&!q._mirror){const bonus=Math.max(1,Math.round(dmg*(.15+.05*lv)*10)/10);el11BossHit(b,which,bonus);el11Log('metal',{bonus,boss:true});
  for(let i=0;i<3+lv&&particles.length<600;i++){const a=rnd(0,Math.PI*2),v=rnd(1.4,3.2);particles.push({x:b.x+rnd(-10,10),y:y+rnd(-10,10),vx:Math.cos(a)*v,vy:Math.sin(a)*v,life:rnd(.18,.34),t:0,r:rnd(1,2),color:i%2?'#ffffff':'#a9b4c2'});}}
}
hitBoss=function(dmg){const b=boss,r=EL11.base.boss.apply(this,arguments);if(!EL11.busy)el11BossProc(b,'boss',dmg);return r;};
// Space stages (5, 9) swap the gun for the space weapons, whose rounds were not element carriers, so a Forge element
// did nothing there at all. They carry it now, like every other Forge weapon.
if(typeof INFUSION_CARRIERS==='object'&&!Object.isFrozen(INFUSION_CARRIERS))Object.assign(INFUSION_CARRIERS,{spaceLaser:1,spaceVolley:1,spaceShrapnel:1,spaceFusion:1});
// The Hammer family (Chronos, the Stage-8 Hammer form) also takes rounds through hammerBossDamage directly.
EL11.base.hammer=hammerBossDamage;
hammerBossDamage=function(b,dmg){const r=EL11.base.hammer.apply(this,arguments);if(!EL11.busy&&b)el11BossProc(b,b===subBoss?'sub':'boss',dmg);return r;};
hitSubBoss=function(dmg){const b=subBoss,r=EL11.base.sub.apply(this,arguments);if(!EL11.busy)el11BossProc(b,'sub',dmg);return r;};
EL11.base.fx2=updateEffects;
updateEffects=function(dt){const r=EL11.base.fx2.apply(this,arguments);
 if(state===GS.PLAY)for(const [b,which] of [[boss,'boss'],[subBoss,'sub']]){if(!b||b.dead||!(b._el11Poison>0))continue;
  b._el11Poison-=dt;if(!b._el11||b._el11.el==='toxic')el11Status(b,'toxic',b._el11PoisonLv||1,Math.max(.2,b._el11Poison));b._el11PoisonT=(b._el11PoisonT||0)-dt;
  if(b._el11PoisonT<=0){b._el11PoisonT=.4;el11BossHit(b,which,1+(b._el11PoisonLv||1));el11Log('boss-poison',{which});
   if(particles.length<600)particles.push({x:b.x+rnd(-20,20),y:(b._drawY??b.y)+rnd(-20,20),vx:rnd(-.3,.3),vy:rnd(-.9,-.2),life:rnd(.3,.6),t:0,r:rnd(1.4,2.6),color:'#5dff4a'});}}
 return r;};
drawBoss=function(){const b=boss;if(b&&!b.dead)el11Swirl(b,'wrap_back');const r=EL11.base.drawBoss.apply(this,arguments);if(b&&!b.dead)el11Swirl(b,'wrap_front');return r;};
drawSubBoss=function(){const b=subBoss;if(b&&!b.dead)el11Swirl(b,'wrap_back');const r=EL11.base.drawSub.apply(this,arguments);if(b&&!b.dead)el11Swirl(b,'wrap_front');return r;};
globalThis.BOF_ELEMENTAL_STATUS=EL11;
