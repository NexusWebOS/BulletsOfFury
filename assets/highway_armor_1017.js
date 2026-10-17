"use strict";
/* Highway armor has a heavy authored hull, an aimed twin cannon and two
   separately destructible missile racks. Shells retain their release vector. */
const ARMOR17={base:{spawn:spawnEnemy,tick:modularTankTick,draw:drawModularTank,sand:sandTankTick,
 hit:hitEnemy,muzzle:modularTankMuzzle,projectile:er26ProjectileDraw},shots:0,modules:0};
function armor17Road(x,y){const s=levelSrcY()+y;
 return [-42,0,42].every(dx=>[-42,0,42].every(dy=>tankDrivable(x+dx,s+dy,false)));}
function armor17Place(e){const W=worldWidth(),c=W*.5;
 for(const x of [e.x,c,c-52,c+52,c-104,c+104,c-156,c+156])if(armor17Road(x,e.y)){e.x=x;return true;}return false;
}
spawnEnemy=function(){const start=enemies.length,r=ARMOR17.base.spawn.apply(this,arguments);
 for(const e of enemies.slice(start))if(run.stage===4&&e._modTank===4){
  delete e._r30;e.w=88;e.h=104;e._drawW=88;e._drawH=104;e._noSep=true;e.ground=true;
  e.pattern='armor17';e.shoots=false;e.vx=e.vy=0;e._kick=e._recoil=0;
  const rank=target17Rank(),mul=coopActive()?1.5:1;
  e._armor17={age:0,hull:Math.round((24+rank*6)*mul),hullFlash:0,parts:[
   {id:'turret',hp:Math.round((18+rank*5)*mul),dx:0,dy:-3,w:40,h:58,phase:'rest',t:0,cool:.9,flash:0},
   {id:'rackL',hp:Math.round((12+rank*3)*mul),dx:-32,dy:4,w:22,h:40,phase:'rest',t:0,cool:2.2,flash:0},
   {id:'rackR',hp:Math.round((12+rank*3)*mul),dx:32,dy:4,w:22,h:40,phase:'rest',t:0,cool:2.8,flash:0}]};
  for(const p of e._armor17.parts)p.maxhp=p.hp;e.maxhp=e._maxhp=e.hp=e._armor17.hull+e._armor17.parts.reduce((s,p)=>s+p.hp,0);
  e._armor17.maxHull=e._armor17.hull;e._armor17.placed=armor17Place(e);e._modAngle=Math.PI/2;
  enc30Warm(4);a17Warm(['tankHull','tankTurret','tankShell']);
 }return r;
};
function armor17Mount(e,p){return {x:e.x+p.dx,y:e.y+p.dy};}
function armor17TurretPoint(e,side=0){const a=e._modAngle??Math.PI/2,k=104/A17_ART.tankTurret.span,reach=109*k,spread=20*k*side;
 return{x:e.x+Math.cos(a)*reach+Math.cos(a-Math.PI/2)*spread,y:e.y-3+Math.sin(a)*reach+Math.sin(a-Math.PI/2)*spread,aim:a};}
function armor17Shape(e,p){if(p.id!=='turret')return {...armor17Mount(e,p),w:p.w,h:p.h,rot:0};
 const a=e._modAngle??Math.PI/2;return{x:e.x+Math.cos(a)*20,y:e.y-3+Math.sin(a)*20,w:44,h:96,rot:a-Math.PI/2};}
function armor17Touches(e,p,x,y,pad=0){const s=armor17Shape(e,p),dx=x-s.x,dy=y-s.y,c=Math.cos(s.rot),sn=Math.sin(s.rot);
 return Math.abs(dx*c+dy*sn)<s.w/2+pad&&Math.abs(-dx*sn+dy*c)<s.h/2+pad;}
modularTankMuzzle=function(e){return e?._armor17?armor17TurretPoint(e):ARMOR17.base.muzzle.apply(this,arguments);};
sandTankTick=function(e){if(e?._armor17)return;return ARMOR17.base.sand.apply(this,arguments);};
function armor17Tick(e,dt){const A=e._armor17,rank=target17Rank();A.age+=dt;
 if(!A.placed){A.placed=armor17Place(e);if(!A.placed){e.y+=24*dt;return;}}
 const speed=e.y<PLAY.y+100?35:14,next=e.y+speed*dt;
 if(armor17Road(e.x,next))e.y=next;
 A.hullFlash=Math.max(0,A.hullFlash-dt);e._recoil=Math.max(0,(e._recoil||0)-dt);if(Number.isFinite(A.poseAge))A.poseAge+=dt;
 for(const p of A.parts){p.flash=Math.max(0,p.flash-dt);if(p.hp<=0)continue;
  if(e._stagger>0||e._frozen||e._mercuryLock>0||e.y<PLAY.y+40||e.y>VH-45){p.phase='rest';p.cool=Math.max(.5,p.cool);continue;}
  p.t+=dt;p.cool-=dt;const turret=p.id==='turret',warm=turret?[1,.9,.8,.72,.68][rank]:1.1;
  if(p.phase==='rest'&&p.cool<=0){const m=armor17Mount(e,p),q=targetShip(m.x,m.y);p.aim={x:q.x,y:q.y};p.angle=Math.atan2(q.y-m.y,q.x-m.x);p.phase='tell';p.t=0;p.round=0;p.shot=0;Audio.SFX.bossWeaponCharge?.();}
  if(p.phase==='tell'){
   if(turret)e._modAngle+=clamp(stage4AngleDelta(e._modAngle,p.angle),-dt*1.8,dt*1.8);
   combatWarningTick(p,'armor-'+Math.floor(A.age),p.t,warm);
   if(p.t>=warm){p.phase='fire';p.t=0;if(turret){p.angle=e._modAngle;p.aim={x:e.x+Math.cos(p.angle)*900,y:e.y+Math.sin(p.angle)*900};}}
  }else if(p.phase==='fire'){
   p.shot-=dt;const n=turret?2:rank<2?1:2;
   if(p.shot<=0&&p.round<n){const m=turret?armor17TurretPoint(e,p.round%2?1:-1):armor17Mount(e,p),a=turret?p.angle:p.angle+(p.round? .06:-.06);
    const q=eShootT(m.x,m.y,a,turret?3.4+rank*.2:2.45+rank*.13,turret?'s4brass':'emissile',{w:turret?8:11,h:turret?18:24,silent:true});
    Object.assign(q,{owner:e,_armor17Shell:turret,_armor17Missile:!turret,_weaponProof:turret,_shootable:!turret,homing:false,_noArsenal:true});
    if(!turret)q.hp=2;else if(p.round===0)A.poseAge=0;ARMOR17.shots++;p.round++;p.shot=.23;e._recoil=.25;
    wm26Emit(e,m.x,m.y,a,turret?'mg':'missile',null,{size:turret?36:28,life:.14});(turret?Audio.SFX.tankCannon:Audio.SFX.missile)?.();
   }
   if(p.t>.6){p.phase='rest';p.t=0;p.cool=turret?[2.2,1.8,1.4,1.1,.95][rank]:[4,3.4,2.8,2.3,2.1][rank];}
  }
 }
}
modularTankTick=function(e,dt){return e?._armor17?armor17Tick(e,dt):ARMOR17.base.tick.apply(this,arguments);};
drawModularTank=function(e){if(!e?._armor17)return ARMOR17.base.draw.apply(this,arguments);
 if(e.dead||e._dyingT!=null)return false;const A=e._armor17;
 a17Blit('tankHull',A.age*18,e.x,e.y,104,A.hullFlash);
 for(const p of A.parts){const m=armor17Mount(e,p);if(p.hp<=0){whvPartFx(e,m,0,true,.28,p.dx);continue;}
  if(p.id==='turret')a17Blit('tankTurret',A.poseAge<1?Math.min(15,Math.floor(A.poseAge*16)):12,m.x,m.y,104,p.flash,e._modAngle-Math.PI/2);
  else enc30Cell(p.id==='rackL'?'tank_pod_l':'tank_pod_r',0,m.x,m.y,22,40,p.flash>0?'#ffffff':null);
  if(p.phase==='tell'){const q=p.id==='turret'?armor17TurretPoint(e):m;combatWarningDraw(p,{x:q.x,y:q.y,ex:p.aim.x,ey:p.aim.y,progress:clamp(p.t/(p.id==='turret'?[1,.9,.8,.72,.68][target17Rank()]:1.1),0,1),width:p.id==='turret'?14:22});}
 }return true;
};
hitEnemy=function(e,dmg){if(!e?._armor17)return ARMOR17.base.hit.apply(this,arguments);
 if(e.dead||e._dyingT!=null||e._noHit)return;const A=e._armor17,q=_dmgBullet;
 const direct=A.direct;A.direct=null;
 let part=A.parts.find(p=>p.hp>0&&p.id===direct)||null;if(direct==null&&q&&Number.isFinite(q.x)&&Number.isFinite(q.y)){
  part=A.parts.find(p=>p.hp>0&&armor17Touches(e,p,q.x,q.y,3));
  if(q.kind==='beam'||q.kind==='flame')part=A.parts.find(p=>p.hp>0&&Math.abs(q.x-(e.x+p.dx))<(q.w||12)/2+p.w/2);
 }
 const result=elementalDamageResult(e,'enemy',q,dmg,e.x,e.y);dmg=Math.max(0,result.dmg||0);if(!dmg)return;
 if(part){part.hp=Math.max(0,part.hp-dmg);markHit(part);if(part.hp<=0){part.phase='dead';ARMOR17.modules++;const m=armor17Mount(e,part);unitDeathFX({...m,w:part.w,h:part.h},'turret','red');}}
 else{A.hull=Math.max(0,A.hull-dmg);markHit(e);A.hullFlash=Math.max(A.hullFlash,.16);}
 weaponHitSfx('normal');if(typeof stageStats!=='undefined')stageStats.dmgDealt+=dmg;
 e.hp=A.hull+A.parts.reduce((s,p)=>s+p.hp,0);if(A.hull<=0){e.hp=0;killEnemy(e);}return true;
};
er26ProjectileDraw=function(q){if(!q?._armor17Shell)return ARMOR17.base.projectile.apply(this,arguments);
 a17Blit('tankShell',(q.t||0)*20,q.x,q.y,26,0,Math.atan2(q.vy,q.vx)-Math.PI/2);return true;};
window.BOF_HIGHWAY_ARMOR={state:ARMOR17,road:armor17Road,mount:armor17Mount};
const ARMOR17_BULLETS=drawBullets;drawBullets=function(){const all=eBullets,own=all.filter(q=>q._armor17Shell&&!q.dead);
 eBullets=all.filter(q=>!q._armor17Shell);try{ARMOR17_BULLETS.apply(this,arguments);}finally{eBullets=all;}
 for(const q of own)er26ProjectileDraw(q);
};
const ARMOR17_TARGETS=_lockTargets;_lockTargets=function(){const all=ARMOR17_TARGETS.apply(this,arguments),out=[];
 for(const e of all){if(!e?._armor17||e.dead||e._dyingT!=null){out.push(e);continue;}
  const A=e._armor17;
  for(const p of A.parts)if(p.hp>0){const s=armor17Shape(e,p),w=Math.abs(Math.cos(s.rot))*s.w+Math.abs(Math.sin(s.rot))*s.h,h=Math.abs(Math.sin(s.rot))*s.w+Math.abs(Math.cos(s.rot))*s.h;
   out.push(retinaDynamicPiece(e,'armor '+p.id,p.id,()=>({...armor17Shape(e,p),hp:p.hp,dead:e.dead||p.hp<=0}),d=>{A.direct=p.id;hitEnemy(e,d);},w,h));}
  out.push(retinaDynamicPiece(e,'armor hull','tank hull',()=>({x:e.x,y:e.y+30,hp:A.hull,dead:e.dead}),d=>{A.direct='hull';hitEnemy(e,d);},52,36));
 }return out;
};
