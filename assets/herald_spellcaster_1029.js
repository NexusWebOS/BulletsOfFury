'use strict';
/* HS53: drawn spell seal, skull channel, ruby penta balls and real red glass scatter. */
const HS53={base:{start:hr28Start,tell:hd1003Tell,tick:hd1003Tick,blit:hd1003Blit,draw:heraldDeathDraw,
 projectile:drawCombatFinalProjectile,update:updatePlay,effects:drawEffects,intercept:enemyOrdnanceCanIntercept,
 element:enemyOrdnanceElement,rules:s3kOrdnanceRules,load:stageLoadBegin},events:[],orbs:new Set(),fx:[]};
for(const a of Object.values(HS53_ART))XART._src[a.key]=a.path;
stageLoadBegin=function(n,keys){if(n===8)Snd.prepare(['iceOrbImpact','combatOrb0927','timedBombBlast','bossWeaponCharge','wardenScream','combatAlien0927']);return HS53.base.load.call(this,n,n===8?[...(keys||[]),...Object.values(HS53_ART).map(a=>a.key)]:keys);};
function hs53Log(event,data={}){HS53.events.push({event,time:efxClock,...data});if(HS53.events.length>900)HS53.events.shift();}
function hs53Own(b){return run.stage===8&&!b?.dead&&b?._hd1003?.mode==='er28-herald'&&b._hd1003.er28?._hs53?b._hd1003.er28:null;}
function hs53Blit(name,f,x,y,hit=false){const a=HS53_ART[name+(hit?'_hit':'')]||HS53_ART[name];if(!a||!XART.rdy(a.key))return false;f=clamp(f|0,0,a.frames-1);
 ctx.drawImage(XART.get(a.key),f%a.cols*a.cw,Math.floor(f/a.cols)*a.ch,a.cw,a.ch,Math.round(x-a.pivot[0]),Math.round(y-a.pivot[1]),a.cw,a.ch);return true;}
hr28Start=function(b,kind){HS53.base.start.apply(this,arguments);if(kind!=='pentagram')return;
 const H=b._hd1003,A=H.er28;Object.assign(A,{_hs53:true,_hh52:true,phase:'gather',warm:5.4,clip:'cast',frame:0,
  origin:{x:camLeftX()+viewW()/2,y:viewTopY()+175},lastLine:-1,burst:false,released:false,dark:0});
 // No old traveling sigil may survive entry into the replacement cast.
 for(const q of eBullets)if(q._heraldOwner1003===b&&q._er28Herald==='pentagram')q.dead=true;
 hs53Log('cast-start',{casterPhase:!!H.hs53Caster});
};
hd1003Tell=function(b){if(b===subBoss&&b?._hd1003){const H=b._hd1003;
  const stripped=['gunL','gunR','wingL','wingR'].every(id=>!hd1003Live(b,hd1003Part(b,id)));
  if(stripped&&!H.hs53Caster){H.hs53Caster=true;H.hs53Turn=0;hs53Log('caster-phase-enter',{hp:b.hp,maxhp:b.maxhp});}
  if(H.hs53Caster){const book=['pentagram','nuke','rage','storm','pentagram'],kind=book[(H.hs53Turn||0)%book.length];H.hs53Turn=(H.hs53Turn||0)+1;return hr28Start(b,kind);}
  // The seal is skull-driven, including when both claws have been destroyed.
  if((H.er28Turn||0)%10===7){H.er28Turn=(H.er28Turn||0)+1;return hr28Start(b,'pentagram');}
 }return HS53.base.tell.apply(this,arguments);};
function hs53SealPoint(b){return{x:b.x,y:b.y+82};}
function hs53Round(b,p,a,speed,kind,extra={}){if(eBullets.filter(q=>q._heraldOwner1003===b&&!q.dead).length>=128)return null;
 const q=eShootT(p.x,p.y,a,speed,'s8pair',{owner:b,noMuzzle:true,silent:true,w:kind==='orb'?34:14,h:kind==='orb'?34:14});if(!q)return null;
 Object.assign(q,{_hs53:kind,_hs53Born:efxClock,_heraldOwner1003:b,_heraldPart1003:'head',_weaponProof:true,_shootable:false,
  _s3kOriginalProof:false,_noArsenal:true,_boss:true,homing:false,...extra});delete q.hp;return q;}
function hs53Release(b,A){const p=hs53SealPoint(b),rank=bh25Rank(),n=[3,5,6,7][rank];A.released=true;
 for(let i=0;i<n;i++){const tx=camLeftX()+54+i*(viewW()-108)/(n-1),ty=viewTopY()+viewH()*(.68+(i%2)*.11),fuse=1.35+(i%3)*.22,
  a=Math.atan2(ty-p.y,tx-p.x),speed=Math.hypot(tx-p.x,ty-p.y)/(fuse*60),q=hs53Round(b,p,a,speed,'orb',{_hs53At:efxClock+fuse,_hs53Index:i,_hs53EscapeX:player.x});
  if(q){q.vx=(tx-p.x)/(fuse*60);q.vy=(ty-p.y)/(fuse*60);q.spd=Math.hypot(q.vx,q.vy);q._hs53Target={x:tx,y:ty};
   HS53.orbs.add(q);hs53Log('penta-ball-release',{index:i,x:q.x,y:q.y,vx:q.vx,vy:q.vy,at:q._hs53At,target:q._hs53Target});}
 }
 combatAudio0927(b,'timedBombBlast',.12);hs53Log('seal-release',{count:n,x:p.x,y:p.y});
}
function hs53Shatter(q,source='contact'){if(q._hs53Burst)return;q._hs53Burst=true;q.dead=true;const b=q._heraldOwner1003;if(b!==subBoss||b.dead||run.stage!==8)return;
 const rank=bh25Rank(),n=[8,10,12,14][rank],gap=Math.atan2(VH-28-q.y,q._hs53EscapeX-q.x),phase=q._hs53Index*.21;
 HS53.fx.push({b,x:q.x,y:q.y,t:0});if(HS53.fx.length>14)HS53.fx.shift();let count=0;
 for(let i=0;i<n;i++){const a=i*TAU/n+phase;if(Math.abs(Math.atan2(Math.sin(a-gap),Math.cos(a-gap)))<.25)continue;
  if(hs53Round(b,q,a,2.35+rank*.18,'shard',{_hs53Dir:((Math.round(a*32/TAU)%32)+32)%32,_hs53Phase:i%8}))count++;
 }
 combatAudio0927(b,'iceOrbImpact',.10);hs53Log('penta-ball-shatter',{index:q._hs53Index,count,x:q.x,y:q.y,gap,source});
}
hd1003Tick=function(b,dt){const A=hs53Own(b);if(!A)return HS53.base.tick.apply(this,arguments);const H=b._hd1003;
 H.clock+=dt;H.age+=dt;H.attackAge+=dt;A.t+=dt;b.fireCd=999;b._sba=null;b._s4MiniSafe=true;
 const u=clamp(A.t/.8,0,1),k=u*u*(3-2*u);b.x=lerp(A.from.x,A.origin.x,k);b.y=lerp(A.from.y,A.origin.y,k)+Math.sin(H.clock*2)*3;b._drawY=b.y;
 A.dark=Math.min(15,Math.floor(A.t/1.0*15));
 if(A.t<.6){A.phase='gather';A.clip='cast';A.frame=Math.floor(A.t/.6*12);}
 else if(A.t<3.35){A.phase='inscribe';A.clip='cast';A.frame=12+Math.min(11,Math.floor((A.t-.6)/2.75*12));
  const line=Math.min(5,Math.floor((A.t-.6)/2.75*56/6));if(line>A.lastLine){A.lastLine=line;combatAudio0927(b,'combatAlien0927',.15);hs53Log(line<5?'seal-line':'seal-circle',{line});}}
 else if(A.t<4.55){A.phase='spin';A.clip='raised';A.frame=Math.floor(H.clock*20)%16;}
 else if(A.t<5.4){A.phase='pulse';A.clip='raised';A.frame=Math.floor(H.clock*24)%16;}
 else if(A.t<6.05){A.phase='burst';A.clip='raised';A.frame=Math.floor(H.clock*24)%16;if(!A.released)hs53Release(b,A);}
 else if(A.t<10.2){A.phase='scatter';A.clip='raised';A.frame=Math.floor(H.clock*20)%16;}
 else{A.phase='recover';A.clip='lower';A.frame=Math.min(23,Math.floor((A.t-10.2)/.65*24));A.dark=Math.max(0,15-Math.floor((A.t-10.2)*18));if(A.t>=11.3){hr28End(b);hs53Log('cast-complete');}}
 if(A.t<5.4)combatWarningTick(b,'hs53-cast-'+A.serial,A.t,5.4);
 return true;
};
hd1003Blit=function(p,P,flash=0,alpha=1){const A=hs53Own(subBoss);if(A&&A.phase!=='recover'&&p.id==='head'&&!p.dead)return hs53Blit('head_cast',Math.floor(A.t*24)%32,P.x,P.y,flash>0);return HS53.base.blit.apply(this,arguments);};
heraldDeathDraw=function(b){const A=hs53Own(b);if(!A)return HS53.base.draw.apply(this,arguments);const out=HS53.base.draw.apply(this,arguments),p=hs53SealPoint(b);
 if(A.t<5.4){const head=hd1003Pose(b,hd1003Part(b,'head'));hh52Blit('star',0,head.x,head.y-106);}
 if(A.phase==='inscribe')hs53Blit('seal_build',Math.min(55,Math.floor((A.t-.6)/2.75*56)),p.x,p.y);
 else if(A.phase==='spin')hs53Blit('seal_spin',Math.floor((A.t-3.35)/1.2*32)%32,p.x,p.y);
 else if(A.phase==='pulse')hs53Blit('seal_pulse',Math.min(23,Math.floor((A.t-4.55)/.85*24)),p.x,p.y);
 else if(A.phase==='burst')hs53Blit('seal_burst',Math.min(15,Math.floor((A.t-5.4)/.65*16)),p.x,p.y);
 return out;
};
drawCombatFinalProjectile=function(q){if(q?._hs53){const age=efxClock-q._hs53Born;
  if(q._hs53==='orb'){const remain=q._hs53At-efxClock;return remain<.35?hs53Blit('orb_hot',Math.min(15,Math.floor((.35-remain)/.35*16)),q.x,q.y):hs53Blit('orb',Math.floor(age*24)%32,q.x,q.y);}
  return hs53Blit('glass_shard',q._hs53Dir*8+(Math.floor(age*24)+q._hs53Phase)%8,q.x,q.y);
 }return HS53.base.projectile.apply(this,arguments);};
enemyOrdnanceCanIntercept=function(q){return q?._hs53?false:HS53.base.intercept.apply(this,arguments);};
enemyOrdnanceElement=function(q){return q?._hs53?null:HS53.base.element.apply(this,arguments);};
s3kOrdnanceRules=function(q){if(q?._hs53){q._weaponProof=true;q._shootable=false;delete q.hp;return;}return HS53.base.rules.apply(this,arguments);};
updatePlay=function(dt){const orbs=[...HS53.orbs];
 for(const q of orbs){const b=q._heraldOwner1003;if(b!==subBoss||b.dead||run.stage!==8){q.dead=true;HS53.orbs.delete(q);continue;}
  if(!q.dead&&efxClock>=q._hs53At){q.x=q._hs53Target.x;q.y=q._hs53Target.y;hs53Shatter(q,'fuse');}}
 for(const q of eBullets)if(q._hs53&&(q._heraldOwner1003!==subBoss||subBoss?.dead||run.stage!==8||efxClock-q._hs53Born>(q._hs53==='orb'?3:3.0)))q.dead=true;
 const out=HS53.base.update.apply(this,arguments);
 for(const q of orbs){if(q.dead&&q._heraldOwner1003===subBoss&&!subBoss.dead&&run.stage===8)hs53Shatter(q);if(q.dead||!eBullets.includes(q))HS53.orbs.delete(q);}
 for(const F of HS53.fx)F.t+=dt;HS53.fx=HS53.fx.filter(F=>F.t<.65&&F.b===subBoss&&!F.b.dead&&run.stage===8);
 return out;
};
drawEffects=function(){const out=HS53.base.effects.apply(this,arguments);for(const F of HS53.fx)hs53Blit('orb_shatter',Math.min(15,Math.floor(F.t/.65*16)),F.x,F.y);return out;};
globalThis.BOF_HERALD_SPELLCASTER_1029={state:HS53,start:b=>hr28Start(b,'pentagram')};
