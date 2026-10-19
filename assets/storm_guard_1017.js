"use strict";
/* Sovereign: the warning is the actual next fan, including the pursuit volley.
   Its detached guard wing uses authored lightning aircraft and committed passes. */
const SG17={base:{set:er26Set,draw:er26Draw,shot:stage4WarfareShot,mark:s4ac13Mark,
 break:ordnanceBreak1002,core:sa14CoreTick,helper:mr27HelperDraw,gun:mr27HelperGun,
 extent:stage4HelperExtent,targets:retinaBossTargets},warnings:0,shots:0};
function sg17Protect(q){if(!q||q.dead)return q;
 q._sg17Lightning=true;q._weaponProof=true;q._shootable=false;q._s3kOriginalProof=true;delete q.hp;
 // Older family adapters must not turn a live lightning ball into missile ordnance.
 for(const [key,value] of [['_weaponProof',true],['_shootable',false]]){
  if(Object.getOwnPropertyDescriptor(q,key)?.configurable===false)continue;
  Object.defineProperty(q,key,{get:()=>value,set:()=>{},enumerable:true,configurable:true});
 }return q;
}
s4ac13Mark=function(q){return sg17Protect(SG17.base.mark.apply(this,arguments));};
stage4WarfareShot=function(b,p,a,speed,role){const q=SG17.base.shot.apply(this,arguments);
 return sa14Storm(b)&&role==='orb'?sg17Protect(q):q;};
ordnanceBreak1002=function(q){if(q&&(q._sg17Lightning||sa14Electric(q)))return;
 return SG17.base.break.apply(this,arguments);};
er26Set=function(b,mode){const r=SG17.base.set.apply(this,arguments);
 if(sa14Storm(b)&&mode==='sa14-overflight')b._er26._sa14.shot=.78;return r;};
function sg17Fan(b){const R=b._er26,T=R?._sa14;if(!T)return null;
 let progress=0,behind=false;
 if(R.mode==='sa14-storm'){
  if(R.t<R.warm)progress=R.t/R.warm;
  else if(T.wave>0&&T.wave<4&&T.shot>0)progress=1-T.shot/.82;
  else return null;
 }else if(R.mode==='sa14-overflight'&&R.t>=4.8&&T.shot>0&&T.shot<=.78){behind=true;progress=1-T.shot/.78;}
 else return null;
 const count=7+vp12Tier()*2,gap=(T.wave%3)+2,out=[];
 for(let i=0;i<count;i++){if(i===gap||i===gap+1)continue;
  const p=behind?{x:b.x+(i-(count-1)/2)*4,y:(b._drawY??b.y)+b.h*.35}:shipBossMount(b,'C');
  out.push({...p,angle:Math.PI/2+(i-(count-1)/2)*.145,progress:clamp(progress,0,1),width:22});
 }return out;
}
er26Draw=function(b){const lanes=sa14Storm(b)?sg17Fan(b):null,R=b?._er26,old=R?.warnings;
 if(lanes)R.warnings=old.filter(w=>w.helper);
 let result;try{result=SG17.base.draw.apply(this,arguments);}finally{if(lanes)R.warnings=old;}
 if(lanes){lanes.forEach((p,i)=>combatWarningDraw(b,{...p,ex:p.x+Math.cos(p.angle)*900,ey:p.y+Math.sin(p.angle)*900,fieldOnly:i>0}));SG17.warnings++;}
 return result;
};
function sg17Wing(b,d,dt){const rank=vp12Tier(),S=b._s4war;
 const C=d._sg17||(d._sg17={age:0,phase:'entry',t:0,shot:0,cycle:0,delay:d.side>0?.45:0});
 C.age+=dt;d._mrOwner=b;d.size=116;d.spawnT+=dt;
 const station=b._target17Station||{x:er26Station(b,0),y:b._er26.home};
 const tx=clamp(station.x+d.side*(viewW()*.27+Math.sin(C.age*1.35)*45),camLeftX()+55,camRightX()-55);
 const ty=PLAY.y+104+Math.sin(C.age*1.35+d.side)*43;
 d.materialize=clamp(C.age/1.1,0,1);d.flash=Math.max(0,d.flash-dt);d.deflectFlash=Math.max(0,(d.deflectFlash||0)-dt);d.deflectSfx=Math.max(0,(d.deflectSfx||0)-dt);
 const g=mr27HelperState(d);g.flash=Math.max(0,g.flash-dt);
 if(C.phase==='entry'){const u=clamp(C.age/1.1,0,1),k=u*u*(3-2*u);d.x=tx;d.y=lerp(PLAY.y-160,ty,k);d._sg17Scale=lerp(1.65,1,k);d._noHit=true;
  d.ang=Math.PI/2;if(u>=1){C.phase='recover';C.t=0;d._noHit=false;}return;}
 d.x+=clamp(tx-d.x,-145*dt,145*dt);d.y+=clamp(ty-d.y,-105*dt,105*dt);d._sg17Scale=1;d._noHit=false;
 const hidden=b.dead||b._sa14.depth||S.shield.rearming||g.dead;
 if(hidden){C.phase='recover';C.t=0;d.state='overheat';return;}
 C.t+=dt;const warm=[1.05,.92,.82,.72][rank],rest=[1.35,1.05,.80,.62][rank];
 if(C.phase==='recover'){d.state='overheat';d.vulnerable=true;
  if(C.t>=rest+C.delay){const p=targetShip(d.x,d.y);C.aim={x:p.x,y:p.y};C.angle=Math.atan2(p.y-d.y,p.x-d.x);C.phase='tell';C.t=0;C.shot=0;C.round=0;C.cycle++;C.missile=C.cycle%2===0;Audio.SFX.bossWeaponCharge?.();}
 }else if(C.phase==='tell'){d.state='windup';d.vulnerable=true;d.ang+=stage4AngleDelta(d.ang,C.angle)*Math.min(1,dt*7);
  combatWarningTick(d,'storm-jet-'+C.cycle,C.t,warm);
  const muzzle=stage4CoreTurretTip(d,1);for(const off of C.missile?[-.09,.09]:[0])
   b._er26.warnings.push({x:muzzle.x,y:muzzle.y,angle:C.angle+off,width:C.missile?24:20,progress:C.t/warm,helper:d});
  if(C.t>=warm){C.phase='fire';C.t=0;d.ang=C.angle;}
 }else{d.state='fire';C.shot-=dt;
  if(C.shot<=0&&C.round<(C.missile?[2,2,3,4][rank]:[6,8,10,12][rank])){
   const side=C.round++%2?1:-1,p=stage4CoreTurretTip(d,side);
   const angle=C.angle+(C.missile?(C.round%2?.09:-.09):0);
   const q=stage4WarfareShot(b,p,angle,C.missile?2.8+rank*.2:3.7+rank*.3,C.missile?'rocket':'lightningmg',{szMul:.70});
   Object.assign(q,{_sa14CoreShot:true,_sg17JetShot:true,_weaponProof:!C.missile,_shootable:C.missile,homing:false,_er26Source:'core',_air17Element:'lightning',_air17Missile:!!C.missile});
   if(C.missile){q.kind='emissile';q.hp=rank>=2?3:2;q.w=10;q.h=24;q._s4Accel=1.1;q._s4Max=5.8;Audio.SFX.enemyMissile?.();}
   S.coreShots++;S.coreBarrelShots[side]++;b._er26.helperShots++;SG17.shots++;
   stage4CoreTurretMuzzle(b,d,side);if(!C.missile&&C.round%3===1)Audio.SFX.enemyMachineGunHeavy?.();C.shot=C.missile?.23:[.18,.15,.12,.10][rank];
  }
  if(C.t>1.6){C.phase='recover';C.t=0;}
 }
}
sa14CoreTick=function(b,dt){if(!sa14Storm(b))return SG17.base.core.apply(this,arguments);
 if(!b._s4war.coreUnlocked)return;for(const d of b._s4war.coreTurrets)if(!d.dead)sg17Wing(b,d,dt);};
stage4HelperExtent=function(d){return d?._sg17?{x:42,y:48}:SG17.base.extent.apply(this,arguments);};
mr27HelperGun=function(b,d){if(!d?._sg17)return SG17.base.gun.apply(this,arguments);
 const a=d.ang??Math.PI/2;return{x:d.x+Math.cos(a)*26,y:d.y+Math.sin(a)*26,w:24,h:38,rot:a-Math.PI/2};};
mr27HelperDraw=function(b,d){if(!sa14Storm(b))return SG17.base.helper.apply(this,arguments);
 if(!d._sg17)return;const scale=d._sg17Scale||1,g=mr27HelperState(d);
 a17Blit('stormJet',b.t*18,d.x,d.y,116*scale,Math.max(d.flash||0,g.flash||0,d.deflectFlash||0),d.ang-Math.PI/2);
};
const SG17_AT=stage4CoreTurretAt;stage4CoreTurretAt=function(b,x,y,pad){const d=SG17_AT.apply(this,arguments);return d?._noHit?null:d;};
retinaBossTargets=function(b){const out=SG17.base.targets.apply(this,arguments);
 if(!sa14Storm(b))return out;
 // Cached target dead flags are getters. Filter airborne entries without
 // assigning to them, and leave their live moving targets reusable on landing.
 return out.filter(q=>{const d=q.part||q._part;if(!d?._sg17)return true;
  q.w=q.h=98;return !d._noHit;});};
window.BOF_STORM_GUARD={state:SG17,fan:sg17Fan};
