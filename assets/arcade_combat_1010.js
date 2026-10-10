"use strict";
/* Shieldless small flyers commit to a readable ram; large jets keep gun lanes. */
const AC10={base:{spawn:spawnEnemy,volc:volcTick,ice:s3IceTick,shield:enemyShieldAutoEquip,begin:beginStage,
 ventSpawn:s2VentSpawn,ventTick:s2VentTick,ventDraw:s2VentDraw,geyser:geyserTick,fx:efxDraw,draw:drawEnemy},
 small:{2:new Set(['ash','skim','disc','eye','lance']),3:new Set(['s3mine','s3interceptor'])},load:stageLoadBegin};
for(const bank of Object.values(AC10_JET_ART))for(const a of bank)XART._src[a.key]=a.path;
stageLoadBegin=function(n,keys){const bank=n===2?AC10_JET_ART.fire:n===3?AC10_JET_ART.ice:[];
 return AC10.load.call(this,n,[...(keys||[]),...bank.map(a=>a.key),...(n===2?['efx_geyser_fire']:[])]);};
function ac10Small(e){return !!AC10.small[run.stage]?.has(e.type)&&!e._af10Jet;}
enemyShieldAutoEquip=function(e){if(ac10Small(e)){delete e._esh;return null;}return AC10.base.shield.apply(this,arguments);};
function ac10Ram(e,dt){delete e._esh;delete e._s2Act;delete e._s3Act;e.armed=false;e.shoots=false;e.fireCd=999;
 const q=e._ac10Ram||(e._ac10Ram={phase:'entry',t:0,speed:90});q.t+=dt;e._bank=0;e.spin=0;
 if(q.phase==='entry'){e.y+=100*dt;if(e.y>=PLAY.y+PLAY.h*.25){q.phase='tell';q.t=0;const p=targetShip(e.x,e.y);q.x=p.x;q.y=p.y;q.angle=Math.atan2(p.y-e.y,p.x-e.x);}}
 else if(q.phase==='tell'){e._chg=1;if(q.t>=.6){q.phase='ram';q.t=0;e._chg=0;Audio.SFX.turbo?.();}}
 else{q.speed=Math.min(diffKey==='furious'?350:300,q.speed+460*dt);e.x+=Math.cos(q.angle)*q.speed*dt;e.y+=Math.sin(q.angle)*q.speed*dt;
  let contact=false;for(const seat of seatList())withSeat(seat,()=>{if(player.dead||player.out)return;
   if(Math.abs(e.x-player.x)<e.w/2+(player._hx??9)-1&&Math.abs(e.y-player.y)<e.h/2+(player._hy??10)-2){contact=true;playerHit('Kamikaze impact');}});
  if(contact){e.hp=0;e.score=0;e.dropOk=false;killEnemy(e);return;}
  if(e.y>VH+80||e.y<PLAY.y-100||e.x<camLeftX()-100||e.x>camRightX()+100)e.dead=true;}
}
volcTick=function(e,dt){if(ac10Small(e))return ac10Ram(e,dt);if(e._af10Jet)return ac10Jet(e,dt);return AC10.base.volc.apply(this,arguments);};
s3IceTick=function(e,dt){if(ac10Small(e))return ac10Ram(e,dt);if(e._af10Jet)return ac10Jet(e,dt);return AC10.base.ice.apply(this,arguments);};
spawnEnemy=function(type,x,y,opt){const jet=type==='ac10firejet'?'fire':type==='ac10icejet'?'ice':null;
 const before=enemies.length,r=AC10.base.spawn.call(this,jet==='fire'?'cruc':jet==='ice'?'s3interceptor':type,x,y,opt),e=enemies.length>before?enemies.at(-1):null;
 if(e&&jet){e.type=type;e._af10Jet={element:jet,t:0,phase:'entry',cd:1.3};delete e._esh;e.armed=false;e.fireCd=999;
  e.w=84;e.h=88;e.hp=e.maxhp=e._maxhp=EHP(44);e.score=1300;e._drawW=108;e._drawH=112;}
 else if(e&&ac10Small(e)){delete e._esh;e.armed=false;e.shoots=false;e.fireCd=999;}
 return r;};
function ac10Jet(e,dt){const q=e._af10Jet;q.t+=dt;e.spin=0;
 if(e.y<PLAY.y+PLAY.h*.22){e.y+=95*dt;return;}
 e.x+=Math.sin(q.t*1.4)*32*dt;q.cd-=dt;
 if(q.phase==='entry'&&q.cd<=0){q.phase='tell';q.cd=.7;q.aim=aimPlayer(e.x,e.y);}
 else if(q.phase==='tell'&&q.cd<=0){q.phase='burst';q.cd=.16;q.left=3;}
 else if(q.phase==='burst'&&q.cd<=0){q.cd=.16;q.left--;
  for(const side of [-1,1]){const p={x:e.x+side*27,y:e.y+30};eShootT(p.x,p.y,q.aim+side*.08,q.element==='fire'?3.0:3.25,q.element==='fire'?'s2needle':'s3shard',{silent:side>0});
   if(q.element==='fire')stage2Muzzle(e,side*.32,.34,.75,.12);else stage3Muzzle(e,side*.32,.34,.75,.12);}
  if(q.left<=0){q.phase='entry';q.cd=2.2;}}
 if(q.t>12){e.y+=145*dt;if(e.y>VH+100)e.dead=true;}
}
beginStage=function(n){const r=AC10.base.begin.apply(this,arguments);if(n===2||n===3){for(const at of [12,25,38])
 stagePlan.push({t:at,fn:()=>{if(run.stage!==n||bossActive||subBossActive)return;spawnEnemy(n===2?'ac10firejet':'ac10icejet',worldWidth()/2+(at===25?100:-100),-110);}});stagePlan.sort((a,b)=>a.t-b.t);
 for(const a of n===2?AC10_JET_ART.fire:AC10_JET_ART.ice)XART.rdy(a.key);}return r;};
drawEnemy=function(e){const q=e._af10Jet;if(q&&!e.dead&&e._dyingT==null){const bank=AC10_JET_ART[q.element],a=bank[Math.floor((e.t||0)*16)%16];
 if(XART.rdy(a.key)){ctx.save();ctx.imageSmoothingEnabled=false;const s=140/Math.max(a.w,a.h),im=e.flash>0?xartTint(a.key,'#ffffff',1):XART.get(a.key);
 ctx.drawImage(im,e.x-a.pivot[0]*s,e.y-a.pivot[1]*s,a.w*s,a.h*s);ctx.restore();
 if(q.phase==='tell')drawBossRetina(e,e.x+Math.cos(q.aim)*160,e.y+Math.sin(q.aim)*160,q.cd/.7*TAU,1);return;}}
 const r=AC10.base.draw.apply(this,arguments);const z=e._ac10Ram;
 if(z?.phase==='tell')drawBossRetina(e,z.x,z.y,(1-z.t/.6)*TAU,1);
 if(q?.phase==='tell')drawBossRetina(e,e.x+Math.cos(q.aim)*160,e.y+Math.sin(q.aim)*160,q.cd/.7*TAU,1);return r;};
/* Only mountain vents become horizontal. Player/weapon geysers retain their
   original vertical damage volumes and rendering. Upper-side launch is fixed. */
s2VentSpawn=function(side,y){const v=AC10.base.ventSpawn.call(this,side,y??PLAY.y+PLAY.h*.20);v._ac10Side=true;v.x=side<0?camLeftX()+8:camRightX()-8;return v;};
s2VentTick=function(dt){const release=s2Vents.filter(v=>v._ac10Side&&!v.done&&v.t+dt>=S2VENT.warn),before=new Set(geysers);
 const r=AC10.base.ventTick.apply(this,arguments);for(const v of release){const g=geysers.find(g=>!before.has(g)&&g.hostile&&Math.abs(g.x-v.x)<1&&Math.abs(g.y-v.y)<1);
  if(g){g.horizontal=true;g.side=v.side;}}
 return r;};
geyserTick=function(dt){const horiz=geysers.filter(g=>g.horizontal),vertical=geysers.filter(g=>!g.horizontal);geysers=vertical;
 const r=AC10.base.geyser.apply(this,arguments);for(const g of horiz){g.t+=dt;g.h=Math.min(GEYSER_H,g.h+GEYSER_GROW*dt);
  const end=g.x-g.side*g.h,l=Math.min(g.x,end),right=Math.max(g.x,end),lane=geyserLane(g)*.75;
  if(g.t<g.life)for(const seat of seatList())withSeat(seat,()=>{if(!player.dead&&player.x>l&&player.x<right&&Math.abs(player.y-g.y)<lane)playerHit('Mountain fire geyser');});}
 geysers.push(...horiz.filter(g=>g.t<g.life+.2));return r;};
efxDraw=function(){const all=geysers,horiz=all.filter(g=>g.horizontal);geysers=all.filter(g=>!g.horizontal);
 try{AC10.base.fx.apply(this,arguments);}finally{geysers=all;}
 for(const g of horiz){const key='efx_geyser_fire';if(!XART.rdy(key))continue;const im=XART.get(key),fw=im.width/8,fh=im.height,frac=Math.max(.02,g.h/GEYSER_H),sh=fh*frac,w=GEYSER_H*fw/fh;
  ctx.save();ctx.translate(g.x,g.y);ctx.rotate(g.side<0?Math.PI/2:-Math.PI/2);ctx.imageSmoothingEnabled=false;
  ctx.drawImage(im,Math.floor(g.t*14)%8*fw,fh-sh,fw,sh,-w/2,-g.h,w,g.h);ctx.restore();}
};
