"use strict";
/* Requested roster: Siege Bomber -> 5 mini, new cargo fortress -> 6 mini,
   original flyover carrier -> 6 boss. Each weapon owns a real damage pool. */
const ROSTER17={buildingMini:false,base:{init:warhiveInit,tick:warhiveTick,draw:warhiveDraw,
 damage:warhiveDamage,hit:warhiveHitTest,targets:warhiveRetinaTargets,spawn:spawnSubBoss__inner,
 miniTick:updateSubBoss,miniDraw:drawSubBoss,miniHit:hitSubBoss,solid:subBossSolidAt,
 part:subBossHitPart,retina:retinaBossTargets,die:bossDie,open:sc13Open,begin:beginStage,partPos:whvPartPos}};
for(const a of HH21_ART.frames)XART._src[a.key]=a.path;
const roster17Load=stageLoadBegin;stageLoadBegin=function(n,keys){
 return roster17Load.call(this,n,[...(keys||[]),...(n===6?[...HH21_ART.frames.map(a=>a.key),'d27_'+DIRECTOR_ART.reels.mg.sheet]:[])]);};
SUBBOSS[5]={...SUBBOSS[5],kind:'siegebomber'};
SUBBOSS[6]={...SUBBOSS[6],kind:'siegefortress17'};
const ROSTER17_BOMBER=mr27BomberSetup;mr27BomberSetup=function(b){const r=ROSTER17_BOMBER.apply(this,arguments);
 if(run.stage===5&&b.kind==='siegebomber'&&b._bomber){b._bomber.space=false;b._bomber.skin=null;b._bomber.variant=0;b.name='ECLIPSE SIEGE BOMBER';b.h=b.w*.62;}return r;};
const ROSTER17_SAY=s6WingSay;s6WingSay=function(who,line){
 if(subBoss?._cargo17Mini){line=line.replace('TAKE OUT TWO BATTERIES! THAT WILL EXPOSE THE REACTOR.','DESTROY ALL SIX LASER BATTERIES TO OPEN THE REACTOR.');
  if(line==='REACTOR EXPOSED. KEEP THAT FIRING LANE OPEN!'&&!sc13Open(subBoss))return;}
 if(roster17Active(boss))return SC13.base.wingSay.call(this,who,line);
 return ROSTER17_SAY.call(this,who,line);
};
function roster17Active(b){return !!b?._carrier17;}
function roster17HullScale(b){return (b?._carrier17||b?._s6CarrierFall)?.hullScale||1;}
function roster17Home(b){return Math.max(WHV_HOME_Y,WHV_PLATE.h*WHV_S*roster17HullScale(b)/2+18);}
function roster17Sync(b){const C=b._carrier17,W=b._whv;
 b.hp=C.parts.reduce((s,p)=>s+Math.max(0,p.hp),0);
 W.core=W.coreMax=0;W.cx=b.x;W.cy=b.y;W.doorOpen=!!C.bayOpen;
 b._drawY=b.y;
}
function roster17Budget(b){const C=b._carrier17;if(C.budgetFinalized)return;C.budgetFinalized=true;
 // The legacy stage floor knows only the two fans and door. Reconcile our
 // complete module budget after spawnBoss has finished its modifiers.
 for(const p of C.parts){p.hp=p.maxhp;if(p.kind==='fan')p.max=p.maxhp;}
 b.maxhp=C.parts.reduce((s,p)=>s+p.maxhp,0);roster17Sync(b);
}
function roster17Mount(b,p){const k=WHV_S*roster17HullScale(b);return{x:b.x+p.dx*k,y:b.y+p.dy*k};}
whvPartPos=function(b,id){if(!b?._carrier17&&!b?._s6CarrierFall)return ROSTER17.base.partPos.apply(this,arguments);
 const W=b._whv,p=id==='door'?WHV_DOOR:WHV_NAC[id],k=WHV_S*roster17HullScale(b);
 // Native launch/death callers add W.dy themselves; keep this point hull-local.
 return{x:W.cx+p.x*k,y:W.cy+p.y*k};};
warhiveInit=function(b){
 if(ROSTER17.buildingMini||run.stage!==6||run._gp4StageX)return ROSTER17.base.init.apply(this,arguments);
 SC13.base.init(b);delete b._cargo13;
 const rank=target17Rank(),mul=coopActive()?1.5:1,parts=[];
 const add=(id,kind,dx,dy,hp,w,h)=>parts.push({id,kind,dx,dy,hp:Math.ceil(hp*mul),maxhp:Math.ceil(hp*mul),w,h,dead:false,flash:0,t:0,phase:'rest',cool:1.1+parts.length*.25,serial:0});
 add('L','fan',-169.5,-10,140+rank*22,66,66);add('R','fan',169.5,-10,140+rank*22,66,66);
 // Only the outer batteries sit beside the fan nacelles. The bay stays clear.
 for(const [i,x] of [[0,-104],[3,104]])add('laser'+i,'laser',x,65,105+rank*20,38,54);
 // Four gun housings already exist on the whole authored hull. Split the
 // removed bay batteries' health between these actual, targetable sockets.
 const gunHP=105+rank*20;
 for(const [i,x,y,muzzleY,rect] of [[0,177,103,116,[168,86,18,32]],[1,211,94,110,[200,76,22,36]],
  [2,301,94,110,[290,76,22,36]],[3,335,103,116,[326,86,18,32]]]){
  add('hullGun'+i,'gun',x-256,y-144,i%2?Math.floor(gunHP/2):Math.ceil(gunHP/2),20,30);
  Object.assign(parts.at(-1),{hullGun:i,sourceRect:rect,muzzleDY:muzzleY-y,muzzleAge:99});
 }
 add('rackL','missile',-108,-34,125+rank*20,35,60);add('rackR','missile',108,-34,125+rank*20,35,60);
 b._carrier17={parts,hullScale:1.45,age:0,phase:'arrive',t:0,scale:1.8,depth:true,cycles:0,flight:13,hit:null,shots:0};
 for(const id of ['L','R']){const p=parts.find(p=>p.id===id);b._whv.parts[id]=p;p.fl=0;p.max=p.maxhp;}
 b._whv.parts.door={hp:0,max:0,dead:false,fl:0};b._whv.mode='carrier';b._whv.st='hold';b._whv.jets=[];b._whv.beam=null;
 b.name='WARHIVE HARRIER';b.enter=false;b._noHit=true;b.y=VH+210;b.x=camLeftX()+viewW()/2;
 b.w=WHV_PLATE.w*WHV_S*roster17HullScale(b);b.h=WHV_PLATE.h*WHV_S*roster17HullScale(b);
 b.maxhp=parts.reduce((s,p)=>s+p.hp,0);roster17Sync(b);sc13Warm();enc30Warm(4);whvWarm();
};
function roster17Ready(b){const C=b?._carrier17;return !!C&&!b.dead&&!C.depth&&C.phase==='fight';}
function roster17At(b,x,y){if(!roster17Ready(b))return null;const C=b._carrier17,k=roster17HullScale(b);
 for(const p of C.parts)if(!p.dead){const m=roster17Mount(b,p);if(Math.abs(x-m.x)<p.w*k/2&&Math.abs(y-m.y)<p.h*k/2)return p.id;}
 const q=whvPartPos(b,'door');if(Math.abs(x-q.x)<38*k&&Math.abs(y-q.y)<40*k)return 'armor';
 return null;
}
warhiveHitTest=function(b,x,y){if(!roster17Active(b))return ROSTER17.base.hit.apply(this,arguments);
 b._carrier17.hit=roster17At(b,x,y);return b._carrier17.hit!==null;};
function roster17Damage(b,dmg){const C=b._carrier17;if(!roster17Ready(b)||!(dmg>0))return 0;
 roster17Budget(b);
 const shot=_dmgBullet,k=roster17HullScale(b);let id=C.direct??C.hit;C.direct=null;C.hit=null;
 if(id==null&&Number.isFinite(_lastHitX))id=roster17At(b,_lastHitX,_lastHitY);
 if(id==null&&shot&&Number.isFinite(shot.x)){
  if(shot.kind==='beam'||shot.kind==='flame'){
   const live=C.parts.filter(p=>!p.dead).map(p=>({p,m:roster17Mount(b,p)})).filter(q=>shot.kind==='flame'?flameHit(shot,q.m.x,q.m.y,q.p.w*k,q.p.h*k):
    Math.abs(shot.x-q.m.x)<(shot.w||1)/2+q.p.w*k/2&&q.m.y+q.p.h*k/2>shot.top&&q.m.y-q.p.h*k/2<shot.bot);
   live.sort((a,c)=>c.m.y-a.m.y);id=live[0]?.p.id;
  }else id=roster17At(b,shot.x,shot.y);
 }
 if(id==null&&!shot)id=C.parts.find(p=>!p.dead)?.id;
 {const p=C.parts.find(p=>p.id===id);if(!p||p.dead)return 0;
  p.hp=Math.max(0,p.hp-dmg);markHit(p);p.fl=.18;
  if(p.hp<=0){p.dead=true;p.phase='dead';const q=roster17Mount(b,p);unitDeathFX({...q,w:p.w*k,h:p.h*k},'turret','blue');Audio.SFX.expBig?.();}
 }
 weaponHitSfx('normal');if(typeof stageStats!=='undefined')stageStats.dmgDealt+=dmg;roster17Sync(b);
 if(C.parts.every(p=>p.dead)){b.hp=0;bossDie();}return 0;
}
warhiveDamage=function(b,dmg){return roster17Active(b)?roster17Damage(b,dmg):ROSTER17.base.damage.apply(this,arguments);};
warhiveRetinaTargets=function(b,out){if(!roster17Active(b))return ROSTER17.base.targets.apply(this,arguments);
 roster17Budget(b);
 if(!roster17Ready(b))return;const C=b._carrier17;
 for(const p of C.parts)if(!p.dead)out.push(retinaDynamicPiece(b,'harrier '+p.id,p.kind,
  ()=>({...roster17Mount(b,p),hp:p.hp,dead:p.dead||!roster17Ready(b)}),d=>{C.direct=p.id;hitBoss(d);},p.w*roster17HullScale(b),p.h*roster17HullScale(b)));
};
function roster17FlashTick(C,dt){for(const p of C.parts){p.flash=Math.max(0,(p.flash||0)-dt);p.fl=Math.max(0,(p.fl||0)-dt);}}
function roster17Muzzle(b,p){const m=roster17Mount(b,p),k=roster17HullScale(b);
 m.y+=p.kind==='gun'?p.muzzleDY*WHV_S*k:p.h*k*.35;return m;}
function roster17GunConfig(){const rank=target17Rank();return{warm:[1.2,1.1,1,.85][rank],rounds:[4,5,7,9][rank],gap:[.18,.16,.125,.10][rank],speed:3.6+rank*.3,rest:[2.4,2.1,1.8,1.6][rank]};}
function roster17HullGun(b,p,dt){if(p.dead)return;
 const cfg=roster17GunConfig(),C=b._carrier17;p.t+=dt;p.cool-=dt;p.muzzleAge+=dt;
 if(p.phase==='rest'&&p.cool<=0){const m=roster17Muzzle(b,p),target=targetShip(m.x,m.y);
  p.angle=Math.atan2(target.y-m.y,target.x-m.x);p.phase='tell';p.t=0;p.serial++;p.round=0;p.shot=0;
  p.lanes=Array.from({length:cfg.rounds},(_,i)=>p.angle+(i/(cfg.rounds-1)-.5)*.24);Audio.SFX.bossWeaponCharge?.();
 }else if(p.phase==='tell'){
  combatWarningTick(p,'harrier-hull-'+p.serial,p.t,cfg.warm);
  if(p.t>=cfg.warm){p.phase='fire';p.t=0;p.shot=0;}
 }else if(p.phase==='fire'){
  p.shot-=dt;if(p.shot<=0&&p.round<cfg.rounds){const m=roster17Muzzle(b,p),a=p.lanes[p.round++];
   const q=eShootT(m.x,m.y,a,cfg.speed,'s6tracer',{owner:b,w:6,h:16,silent:true,noMuzzle:true});
   Object.assign(q,{owner:b,_carrier17Shot:true,_carrierHullGun:p.id,_shootable:false,_weaponProof:true,mg:true,homing:false,_noArsenal:true});
   p.muzzleAge=0;p.muzzleAngle=a;p.shot=cfg.gap;C.shots++;Audio.SFX.enemyMachineGunHeavy?.();
  }
  if(p.round>=cfg.rounds&&p.muzzleAge>.16){p.phase='rest';p.t=0;p.cool=cfg.rest+p.hullGun*.11;}
 }
}
function roster17Weapon(b,p,dt){const C=b._carrier17,rank=target17Rank();
 if(p.kind==='gun')return roster17HullGun(b,p,dt);
 if(p.dead)return;p.cool-=dt;p.t+=dt;
 const warm=p.kind==='laser'?1.12:1.15;
 if(p.phase==='rest'&&p.cool<=0){const m=roster17Mount(b,p),t=targetShip(m.x,m.y);p.aim={x:t.x,y:t.y};p.angle=Math.atan2(t.y-m.y,t.x-m.x);p.phase='tell';p.t=0;p.serial++;p.round=0;p.shot=0;Audio.SFX.bossWeaponCharge?.();}
 if(p.phase==='tell'){combatWarningTick(p,'harrier-'+p.serial,p.t,warm);if(p.t>=warm){p.phase='fire';p.t=0;Audio.SFX.enemyHeavyLaser?.();}}
 else if(p.phase==='fire'){
  const m=roster17Mount(b,p),k=roster17HullScale(b);m.y+=p.h*k*.35;
  if(p.kind==='laser'){
   const width=(14+rank*2)*k,open=Math.min(1,p.t/.1,(.62-p.t)/.12);
   if(open>.25)for(const s of seatList())withSeat(s,()=>{const dx=player.x-m.x,dy=player.y-m.y,along=dx*Math.cos(p.angle)+dy*Math.sin(p.angle),cross=Math.abs(-dx*Math.sin(p.angle)+dy*Math.cos(p.angle));
    if(!player.dead&&along>10&&along<900&&cross<width*open/2+6)playerHit({kind:'harrierLaser',owner:b});});
  }else{p.shot-=dt;const n=p.kind==='missile'?2+rank:3+rank;
   if(p.shot<=0&&p.round<n){const a=p.angle+(p.round-(n-1)/2)*(p.kind==='missile'?.13:.08),missile=p.kind==='missile';
    const q=eShootT(m.x,m.y,a,missile?2.6+rank*.12:3.3+rank*.2,missile?'emissile':'s6tracer',{w:missile?11:7,h:missile?22:16,silent:true});
    Object.assign(q,{owner:b,_carrier17Shot:true,_shootable:missile,_weaponProof:!missile,homing:false,_noArsenal:true});
    C.shots++;p.round++;p.shot=.16; (missile?Audio.SFX.missile:Audio.SFX.enemyMachineGunHeavy)?.();}
  }
  if(p.t>.72){p.phase='rest';p.t=0;p.cool=Math.max(.85,2.5-rank*.35)+(p.kind==='laser'?.4:0);}
 }
}
warhiveTick=function(b,dt){if(!roster17Active(b))return ROSTER17.base.tick.apply(this,arguments);
 roster17Budget(b);
 const C=b._carrier17,W=b._whv;dt=clamp(dt,0,.05);b.t+=dt;b.flash=Math.max(0,b.flash-dt);C.age+=dt;C.t+=dt;roster17FlashTick(C,dt);
 if(b.dead){b.dying+=dt;W.dy=(W.dy||0)+dt*(18+b.dying*12);C.scale=1;
  C.boom=(C.boom||0)-dt;if(C.boom<=0&&b.dying<2.5){C.boom=.18;explode(b.x+rnd(-150,150),b.y+W.dy+rnd(-70,70),68,'red',null,'nxp_barrage');}
  if(b.dying>2.5&&!C.crashed){C.crashed=true;unitDeathFX(b,'boss','red');}return;}
 const cx=camLeftX()+viewW()/2;
 if(C.phase==='arrive'||C.phase==='flyover'){
  const u=clamp(C.t/2.6,0,1),k=u*u*(3-2*u);C.depth=true;b._noHit=true;C.scale=lerp(1.8,1,k);
  b.x=cx;b.y=lerp(VH+210,roster17Home(b),k);W.fanA+=dt*20;
  if(u>=1){C.depth=false;b._noHit=false;C.scale=1;C.phase='fight';C.t=0;for(const p of C.parts)if(!p.dead){p.phase='rest';p.cool=.8+Math.abs(p.dx)/180;}Audio.SFX.bossRoar?.();}
 }else if(C.phase==='leave'){
  C.depth=true;b._noHit=true;b.y+=dt*250;W.fanA+=dt*18;
  if(C.t>2.3){C.phase='flyover';C.t=0;C.cycles++;C.flight=13;}
 }else{
  b._noHit=false;C.depth=false;b.x=cx+Math.sin(C.age*.36)*8;b.y=roster17Home(b)+Math.sin(C.age*.55)*10;
  W.fanA+=dt*10;for(const p of C.parts)roster17Weapon(b,p,dt);
  C.flight-=dt;if(C.flight<=0&&C.parts.some(p=>!p.dead)&&C.parts.every(p=>p.phase!=='fire')){
   if(C.flight>-.9)combatWarningTick(b,'harrier-flight-'+C.cycles,-C.flight,.9);
   else{C.phase='leave';C.t=0;for(const p of C.parts)p.phase='rest';Audio.SFX.chargeDash?.();}
  }
 }
 W.parts.door.fl=Math.max(0,W.parts.door.fl-dt);roster17Sync(b);
};
function roster17Draw(b,C=b._carrier17){const W=b._whv;if(C.crashed)return;
 const k=(C.scale||1)*roster17HullScale(b),cx=W.cx,cy=W.cy+(W.dy||0);ctx.save();ctx.translate(cx,cy);ctx.scale(k,k);ctx.translate(-cx,-cy);
 ctx.imageSmoothingEnabled=false;
 const hullW=WHV_PLATE.w*WHV_S,hullH=WHV_PLATE.h*WHV_S;
 if(C.depth){ctx.save();ctx.globalAlpha=.20;ctx.translate(0,42);const key='whv_closed_w';if(XART.rdy(key)){const im=xartTint(key,'#000000',1);ctx.drawImage(im,cx-hullW/2,cy-hullH/2,hullW,hullH);}ctx.restore();}
 const key=W.doorOpen?'whv_open_w':'whv_closed_w';
 const mount=p=>({x:cx+p.dx*WHV_S,y:cy+p.dy*WHV_S});
 for(const p of C.parts.filter(p=>p.kind==='fan')){const q=mount(p);
  whvSprite(p.dead?'whv_twreck':'whv_fan',q.x,q.y,p.dead?70:54,p.dead?70:54,p.dead?0:W.fanA*(p.id==='L'?1:-1),ctx.globalAlpha);
  if(!p.dead&&p.flash>0){const im=xartTint('whv_fan','#ffffff',1);if(im){ctx.save();ctx.globalAlpha=Math.min(1,p.flash*9);ctx.translate(q.x,q.y);ctx.rotate(W.fanA*(p.id==='L'?1:-1));ctx.drawImage(im,-27,-27,54,54);ctx.restore();}}
 }
 if(XART.rdy(key))ctx.drawImage(XART.get(key),cx-hullW/2,cy-hullH/2,hullW,hullH);
 for(const p of C.parts.filter(p=>p.kind!=='fan')){const q=mount(p);
  if(p.kind==='gun'){
   // Animate the existing hull pixels in place; never paste another turret on top.
   if(p.dead||p.flash>0||['tell','fire'].includes(p.phase)){
    const a=HH21_ART.frames[p.hullGun],flash=p.flash>0,im=flash?XART.get(a.key):xartTint(a.key,p.dead?'#10151f':'#70dfff',1);
    if(im){ctx.save();ctx.imageSmoothingEnabled=false;ctx.globalAlpha*=flash?1:p.dead?.74:p.phase==='fire'?.48:.18+.22*(.5+.5*Math.sin(p.t*24));
     ctx.drawImage(im,q.x-a.pivot[0]*WHV_S,q.y-a.pivot[1]*WHV_S,a.w*WHV_S,a.h*WHV_S);ctx.restore();}
   }
  }else if(p.kind==='laser'){
   if(!(typeof pf20TurretDraw==='function'&&pf20TurretDraw(p,q.x,q.y,38,47.5,p.flash||0))){
    const pose=p.dead?3:p.phase==='fire'?2:p.phase==='tell'?1:0,im=p.flash>0?xartTint('s6cargo13_turrets','#ffffff',1):XART.get('s6cargo13_turrets');
    if(im)ctx.drawImage(im,pose*128,0,128,160,q.x-19,q.y-22,38,47.5);
   }
  }else if(!p.dead)enc30Cell(p.id==='rackL'?'tank_pod_l':'tank_pod_r',0,q.x,q.y,30,54,p.flash>0?'#ffffff':null);
  else whvPartFx(b,q,0,true,.5,p.dx);
 }
 ctx.restore();
 // Draw warnings on the combat plane, from the same enlarged world sockets
 // used by damage. Scaling the whole ray with the hull displaced its endpoint.
 if(roster17Ready(b))for(const p of C.parts)if(!p.dead){const unit=roster17HullScale(b),m=roster17Muzzle(b,p);
  const angle=p.angle??Math.PI/2,ex=m.x+Math.cos(angle)*900,ey=m.y+Math.sin(angle)*900;
  if(p.kind==='gun'){
   if(p.phase==='tell'){
    // Show both edges and the centre of the committed fan without stacking
    // nine opaque fields over each gun on Furious.
    const lanes=p.lanes||[],fan=lanes.length?[lanes[0],lanes[Math.floor(lanes.length/2)],lanes.at(-1)]:[];
    for(const a of fan)combatWarningDraw(p,{x:m.x,y:m.y,ex:m.x+Math.cos(a)*900,ey:m.y+Math.sin(a)*900,progress:p.t/roster17GunConfig().warm,width:12,alpha:.32,fieldOnly:true});
    combatWarningDraw(p,{x:m.x,y:m.y,ex,ey,progress:p.t/roster17GunConfig().warm,alertOnly:true,alertX:m.x,alertY:m.y-28});
   }
   if(p.muzzleAge<.14)wm26Draw(ctx,'mg',m.x,m.y,p.muzzleAngle,p.muzzleAge/.14,42*unit);
  }else if(p.phase==='tell')combatWarningDraw(p,{x:m.x,y:m.y,ex,ey,progress:p.t/(p.kind==='laser'?1.12:1.15),width:(p.kind==='laser'?26:20)*unit});
  if(p.kind==='laser'&&p.phase==='fire'){const open=clamp(Math.min(p.t/.1,(.62-p.t)/.12),0,1);if(open>0)av3Beam(ctx,m.x,m.y,p.angle,900,(14+target17Rank()*2)*unit*open,'ice',b.t);}
 }
}
warhiveDraw=function(b){if(roster17Active(b))return roster17Draw(b);return ROSTER17.base.draw.apply(this,arguments);};

// The new cargo fortress keeps its six independent authored laser batteries,
// but completes through the miniboss lifecycle rather than ending the stage.
spawnSubBoss__inner=function(kind){
 if(kind!=='siegefortress17')return ROSTER17.base.spawn.apply(this,arguments);
 const saved={boss,bossActive,bossWarned,bossDefeated};let b;
 ROSTER17.buildingMini=true;
 try{spawnBoss('warhive');b=boss;}finally{ROSTER17.buildingMini=false;boss=saved.boss;bossActive=saved.bossActive;bossWarned=saved.bossWarned;bossDefeated=saved.bossDefeated;}
 b.sub=true;b.kind='siegefortress17';b._cargo17Mini=true;b._s4MiniSafe=true;b.name='WARHIVE SIEGE FORTRESS';
 b.maxhp=b.hp=Math.round([1000,1350,1650,1950,2100][target17Rank()]*(coopActive()?1.5:1));
 b._cargo13.budgetFinalized=false;sc13FinalizeBudget(b);subBoss=b;subBossActive=true;subBossDone=false;continueRewardMark(b);return b;
};
sc13Open=function(b){return b?._cargo17Mini?b._cargo13.guns.every(g=>g.dead):ROSTER17.base.open.apply(this,arguments);};
bossDie=function(){if(!boss?._cargo17Mini)return ROSTER17.base.die.apply(this,arguments);
 const b=boss;if(b.dead)return;achievementEncounterDefeat(b,'miniboss');b.dead=true;b.dying=0;b.hp=0;sc13Clear(b);run.score+=9000;Audio.SFX.expBoss?.();};
updateSubBoss=function(dt){const b=subBoss;if(!b?._cargo17Mini)return ROSTER17.base.miniTick.apply(this,arguments);
 warhiveTick(b,dt);
 if(b.dead&&b.dying>=2.8){continueRewardResolve(b,b.x,b.y,'miniboss');subBoss=null;subBossActive=false;subBossDone=true;dropPowerup(b.x,b.y,'weapon');}
};
drawSubBoss=function(){if(!subBoss?._cargo17Mini)return ROSTER17.base.miniDraw.apply(this,arguments);warhiveDraw(subBoss);drawSubBossBar(subBoss);};
subBossSolidAt=function(x,y){return subBoss?._cargo17Mini?sc13At(subBoss,x,y)!==null:ROSTER17.base.solid.apply(this,arguments);};
subBossHitPart=function(x,y){return subBoss?._cargo17Mini?sc13At(subBoss,x,y):ROSTER17.base.part.apply(this,arguments);};
hitSubBoss=function(dmg,x,y){const b=subBoss;if(!b?._cargo17Mini)return ROSTER17.base.miniHit.apply(this,arguments);
 if(Number.isFinite(x))b._cargo13.directId=sc13At(b,x,y);
 const old=boss;boss=b;try{return warhiveDamage(b,dmg);}finally{boss=old;}
};
retinaBossTargets=function(b){if(!b?._cargo17Mini)return ROSTER17.base.retina.apply(this,arguments);
 const out=[],C=b._cargo13;if(b.dead||C.mode==='arrive')return out;
 for(const g of C.guns)if(!g.dead)out.push(retinaDynamicPiece(b,'fortress gun '+g.id,'laser battery',()=>({...sc13Mount(b,g.id),hp:g.hp,dead:g.dead||b.dead}),d=>{C.directId=g.id;hitSubBoss(d);},38,56));
 if(sc13Open(b))out.push(retinaDynamicPiece(b,'fortress reactor','reactor',()=>({...sc13Core(b),hp:C.core,dead:b.dead}),d=>{C.directId='core';hitSubBoss(d);},68,96));return out;
};
const ROSTER17_CONTACT=target17BossContact;target17BossContact=function(b,x,y){
 if(!roster17Active(b))return ROSTER17_CONTACT.apply(this,arguments);if(!roster17Ready(b))return false;
 const dx=Math.abs(x-b.x)/(b.w*.49),dy=Math.abs(y-b.y)/(b.h*.43);return dx+dy*.8<1&&dy<1;
};
window.BOF_ROSTER17={state:ROSTER17,at:roster17At,mount:roster17Mount,ready:roster17Ready};
