"use strict";
/* Stage1 missile truck: authored moving chassis and two independent launcher
   mounts. Native ground motion, damage reactions and death/reward owners stay
   in charge. All poses use registered192x256 canvases, never fitted per frame. */
const MT18={base:{spawn:spawnEnemy,tank:tankTick,mod:modularTankTick,draw:drawEnemy,hit:hitEnemy,
 targets:_lockTargets,load:stageLoadBegin},shots:0,partsDestroyed:0,draws:0,events:[]};
for(const bank of Object.values(MT18_ART))for(const a of bank.frames)XART._src[a.key]=a.path;
function mt18Keys(){return Object.values(MT18_ART).flatMap(b=>b.frames.map(a=>a.key));}
function mt18Warm(){for(const k of mt18Keys())XART.rdy(k);}
stageLoadBegin=function(n,keys){return MT18.base.load.call(this,n,n===1?[...(keys||[]),...mt18Keys()]:keys);};
function mt18Rank(){return ['furious','insanity'].includes(diffKey)?2:diffKey==='hard'?1:0;}
spawnEnemy=function(){const n=enemies.length,out=MT18.base.spawn.apply(this,arguments);
 for(const e of enemies.slice(n))if(run.stage===1&&/^s1truckmissile(?:_b|_blk)?$/.test(e.type)){
  const hp=e.maxhp||e.hp,coop=coopActive()?1.5:1;
  e._mt18={age:0,wheel:0,hull:Math.ceil(Math.max(8,hp*.75)),hullFlash:0,
   palette:/_(?:b|blk)$/.test(e.type)?'black':'olive',parts:[-1,1].map((side,i)=>({id:'rack'+(side<0?'L':'R'),
    side,dx:side*17,dy:-27,w:28,h:40,hp:Math.ceil(Math.max(4*coop,hp*.30)),flash:0,
    angle:Math.PI/2,phase:'rest',t:0,cool:1.1+i*1.3,round:0,next:0}))};
  const A=e._mt18;A.maxHull=A.hull;for(const p of A.parts)p.maxhp=p.hp;
  e.maxhp=e._maxhp=e.hp=A.hull+A.parts.reduce((s,p)=>s+p.hp,0);
  e._modTank=1;e._bodyW=76;e._bodyH=108;e.w=82;e.h=112;e._unitSquare=112;
  e._drawW=76;e._drawH=108;e.shoots=false;mt18Warm();
 }return out;
};
function mt18Mount(e,p){return{x:e.x+p.dx,y:e.y+p.dy};}
function mt18Muzzle(e,p,round=0){const m=mt18Mount(e,p),a=p.angle,dx=[-8,8,0][round%3],dy=7;
 const c=Math.cos(a-Math.PI/2),s=Math.sin(a-Math.PI/2);
 return{x:m.x+dx*c-dy*s,y:m.y+dx*s+dy*c,aim:a};}
function mt18Frame(p){if(p.phase==='tell')return 1;
 if(p.phase==='fire')return clamp(2+Math.floor(p.t/.12),2,8);
 if(p.phase==='reload')return clamp(9+Math.floor(p.t/.12),9,15);return 0;}
function mt18Log(kind,e,p){MT18.events.push({kind,side:p?.side,age:e._mt18.age});if(MT18.events.length>120)MT18.events.shift();}
function mt18Tick(e,dt){const A=e._mt18;if(e.dead||e._dyingT!=null)return;
 tankMotionTick(e,dt,TANK_SPD);A.age+=dt;A.hullFlash=Math.max(0,A.hullFlash-dt);
 if(Math.abs(e._spd||0)>.5)A.wheel+=dt*14;
 const rank=mt18Rank(),warm=[1.1,.95,.8][rank];
 for(const p of A.parts){p.flash=Math.max(0,p.flash-dt);if(p.hp<=0)continue;
  if(e._frozen||e._mercuryLock>0||e._stagger>0){p.cool=Math.max(.5,p.cool);continue;}
  p.t+=dt;p.cool-=dt;const m=mt18Mount(e,p),q=targetShip(m.x,m.y);
  if(p.phase==='rest'&&p.cool<=0&&e.y>viewTopY()+48&&e.y<q.y-60&&Math.abs(q.x-e.x)<220){
   p.phase='tell';p.t=0;p.aim={x:q.x,y:q.y};p.angle=clamp(Math.atan2(q.y-m.y,q.x-m.x),Math.PI/2-.58,Math.PI/2+.58);
   e._phase='brake';e._phT=0;p.round=0;p.next=0;mt18Log('tell',e,p);Audio.SFX.lockOn?.();
  }
  if(p.phase==='tell'){
   combatWarningTick(p,'truck-'+p.id,p.t,warm);
   if(p.t>=warm){p.phase='fire';p.t=0;mt18Log('launch',e,p);}
  }else if(p.phase==='fire'){
   p.next-=dt;
   if(p.next<=0&&p.round<3){const mz=mt18Muzzle(e,p,p.round),b=eShootT(mz.x,mz.y,mz.aim,3.05+rank*.45,'s1jungleMissile',{w:10,h:22,szMul:1.08,silent:true});
    Object.assign(b,{owner:e,_mt18Missile:true,_shootable:true,_weaponProof:false,_noArsenal:true,homing:false,hp:rank?2:1});
    wm26Emit(e,mz.x,mz.y,mz.aim,'missile',null,{size:26,life:.14});Audio.SFX.missile?.();
    p.round++;p.next=.24;MT18.shots++;
   }
   if(p.t>=.84){p.phase='reload';p.t=0;mt18Log('reload',e,p);}
  }else if(p.phase==='reload'&&p.t>=.84){p.phase='rest';p.t=0;p.cool=[4.5,3.8,3.1][rank];mt18Log('ready',e,p);}
 }
}
tankTick=function(e,dt){return e?._mt18?mt18Tick(e,dt):MT18.base.tank.apply(this,arguments);};
modularTankTick=function(e,dt){if(e?._mt18)return;return MT18.base.mod.apply(this,arguments);};
function mt18Blit(name,palette,frame,x,y,scale,flash=0,angle=0,owner=null){
 const a=MT18_ART[name+'_'+palette].frames[frame%MT18_ART[name+'_'+palette].frames.length];
 if(!XART.rdy(a.key))return false;const rect=[-a.pivot[0]*scale,-a.pivot[1]*scale,a.w*scale,a.h*scale];
 ctx.save();ctx.imageSmoothingEnabled=false;ctx.translate(Math.round(x),Math.round(y));ctx.rotate(angle);ctx.drawImage(XART.get(a.key),...rect);
 if(flash>0){const hit=xartTint(a.key,hitFlashColor(owner||{},'#ffffff'),.9);if(hit){ctx.save();ctx.globalAlpha=clamp(flash/.16,0,1)*.85;ctx.drawImage(hit,...rect);ctx.restore();}}
 ctx.restore();return true;
}
function mt18Draw(e){const A=e._mt18;if(!A)return false;
 if(!XART.rdy(MT18_ART['hull_'+A.palette].frames[0].key)){mt18Warm();return false;}
 mt18Blit('hull',A.palette,Math.floor(A.wheel)%8,e.x,e.y,.5,Math.max(e.flash||0,A.hullFlash),0,e);
 for(const p of A.parts){const m=mt18Mount(e,p);
  if(p.hp<=0){whvPartFx(e,m,0,true,.19,p.side);continue;}
  mt18Blit('launcher',A.palette,mt18Frame(p),m.x,m.y,.20,Math.max(p.flash,e.flash||0),p.angle-Math.PI/2,e);
  if(p.phase==='tell'){const q=mt18Muzzle(e,p);combatWarningDraw(p,{x:q.x,y:q.y,ex:q.x+Math.cos(p.angle)*650,ey:q.y+Math.sin(p.angle)*650,progress:clamp(p.t/[1.1,.95,.8][mt18Rank()],0,1),width:18});}
 }
 e._drawW=76;e._drawH=108;MT18.draws++;return true;
}
drawEnemy=function(e){if(e?._mt18&&!e.dead&&mt18Draw(e))return;return MT18.base.draw.apply(this,arguments);};
hitEnemy=function(e,dmg){if(!e?._mt18)return MT18.base.hit.apply(this,arguments);
 if(e.dead||e._dyingT!=null||e._noHit)return;
 const A=e._mt18,q=_dmgBullet,direct=A.direct;A.direct=null;
 let part=A.parts.find(p=>p.hp>0&&p.id===direct)||null;
 if(direct==null){const x=Number.isFinite(q?.x)?q.x:_lastHitX;
  if(Number.isFinite(x))part=A.parts.filter(p=>p.hp>0&&Math.abs(x-e.x-p.dx)<p.w/2+3).sort((a,b)=>Math.abs(x-e.x-a.dx)-Math.abs(x-e.x-b.dx))[0]||null;
 }
 const result=elementalDamageResult(e,'enemy',q,dmg,e.x,e.y);dmg=Math.max(0,result.dmg||0);if(!dmg)return;
 markHit(e); // owner flash is visible through every current hull/module pose
 if(enemyShieldIntercept(e,dmg,q))return true;
 if(q?._inf==='kinetic')dmg*=1+.15*(q._infLv||1);
 if(q?._inf==='lightning'&&e._soaked>0)dmg*=1.35;
 if(part){part.hp=Math.max(0,part.hp-dmg);markHit(part);
  if(part.hp===0){part.phase='dead';MT18.partsDestroyed++;const m=mt18Mount(e,part);unitDeathFX({...m,w:28,h:40},'turret','red');mt18Log('module-destroyed',e,part);}
 }else{A.hull=Math.max(0,A.hull-dmg);A.hullFlash=Math.max(A.hullFlash,.16);}
 weaponHitSfx('normal');if(typeof stageStats!=='undefined'){stageStats.dmgDealt+=dmg;
  if(_dmgSrc==='missile')stageStats.mslHits++;
  else if(_dmgSrc==='special'){stageStats.spHits++;stageStats.spDmg+=dmg;}
  if(stageStats.wpn){const key=scWeaponKey();stageStats.wpn[key]=(stageStats.wpn[key]||0)+dmg;}
 }
 if(q?._inf&&typeof infusionOnHit==='function')infusionOnHit(e,q,dmg);
 e.hp=A.hull+A.parts.reduce((s,p)=>s+p.hp,0);if(A.hull<=0){e.hp=0;killEnemy(e);}return true;
};
_lockTargets=function(){const all=MT18.base.targets.apply(this,arguments),out=[];
 for(const e of all){if(!e?._mt18||e.dead||e._dyingT!=null){out.push(e);continue;}
  const A=e._mt18;for(const p of A.parts)if(p.hp>0)out.push(retinaDynamicPiece(e,'missile truck '+p.id,p.id,
   ()=>({...mt18Mount(e,p),hp:p.hp,dead:e.dead||p.hp<=0}),d=>{A.direct=p.id;hitEnemy(e,d);},p.w,p.h));
  out.push(retinaDynamicPiece(e,'missile truck hull','truck hull',()=>({x:e.x,y:e.y+25,hp:A.hull,dead:e.dead}),d=>{A.direct='hull';hitEnemy(e,d);},60,52));
 }return out;
};
window.BOF_MISSILE_TRUCK={state:MT18,warm:mt18Warm,mount:mt18Mount,frame:mt18Frame};
