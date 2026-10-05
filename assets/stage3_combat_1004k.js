"use strict";
/* October 4 recording pass. Reuse the modular geometry, Voss dash setup,
   authored FOV/beam reels and elemental impacts; preserve encounter HP/forms. */
const S3K_BASE={book:er26Book,set:er26Set,combat:er26Combat,shot:er26Shot,
  shape:mr27Shape,tick:mr27Tick,beamStart:l23BossBeamStart,beamTick:l23BossBeamTick,
  break:ordnanceBreak1002,update:updatePlay,effects:drawEffects,thermoBurst:s3ThermoBurstOrb};
const S3K_MUZZLE=wm26Draw;
wm26Draw=function(g,family,x,y,angle,progress,size,color){
  if(family!=='spread'&&family!=='shotgun')return S3K_MUZZLE.apply(this,arguments);
  const n=WM26_REELS[family].n,fi=Math.floor(clamp(progress||0,0,.999)*n),im=wm26Art(family,fi,color),raw=wm26Art(family,fi,null);
  if(!im||!raw)return false;const p=wm26Pixels('s3k-muzzle-'+family+'-'+fi,raw),h=size||WM26_REELS[family].size,w=h*im.width/im.height;
  g.save();g.imageSmoothingEnabled=false;g.globalCompositeOperation='source-over';g.shadowBlur=0;
  g.translate(x,y);g.rotate((angle==null?-Math.PI/2:angle)+Math.PI/2);
  g.drawImage(im,-w*p.baseX,-h*p.bottom,w,h);g.restore();return true;
};
function s3kOwns(b){return !!b&&run.stage===3&&['frostcruiser','cryospear'].includes(b._ship);}
function enemyOrdnanceElement(q){
  if(!q||q._coldTracer1002||q.mg||/shard|lance|beam|laser|pellet|slug/i.test(q.kind||'')&&!q._s3LaserBall)return null;
  if(q._er26Art==='fire'||q._er26Art==='ice')return q._er26Art;
  if(q._tb28&&['magma','ice','fire'].includes(q._tb28.art))return q._tb28.art==='ice'?'ice':'fire';
  if(q._s3LaserBall)return q._s3ThermoArt==='fire'?'fire':'ice';
  if(/^(magma|fireorb|fireball|iceball|s3mortar)$/.test(q.kind||''))return /ice|s3/.test(q.kind)?'ice':'fire';
  return null;
}
function enemyOrdnanceCanIntercept(q){return !!q&&(!!enemyOrdnanceElement(q)||/missile|rocket|warhead/i.test(q.kind||''));}
function enemyDefensiveProof(q){return !!(q&&(q._s3kOriginalProof==null?q._weaponProof:q._s3kOriginalProof));}
function s3kOrdnanceRules(q){
  if(!q||q.dead)return;
  // Shootability does not revoke a bomb clear or a shield's authored reflection grant.
  if(q._s3kOriginalProof==null)q._s3kOriginalProof=!!q._weaponProof;
  const yes=enemyOrdnanceCanIntercept(q);q._weaponProof=!yes;q._shootable=yes;
  if(yes&&enemyOrdnanceElement(q)){q.hp=q.hp||1;q._energyOrdnance=true;}
}
let s3kResidue=[];
ordnanceBreak1002=function(q){
  const elem=enemyOrdnanceElement(q);if(!elem)return S3K_BASE.break(q);
  if(q._fbImpact1002)return;q._fbImpact1002=true;q._intercepted=true;
  if(q._tb28){q._tb28.dead=true;q._tb28.phase='done';}
  efxBurst(elem,q.x,q.y,Math.min(76,Math.max(38,(q._er26Draw||q.w||26)*1.1)));
  const cue=elem==='ice'?'iceOrbImpact':'fireOrbImpact';
  (Audio.SFX[cue]||Audio.SFX.expSmall)?.();
  s3kResidue.push({x:q.x,y:q.y,t:0,elem,stage:run.stage,size:clamp((q._er26Draw||34)*.6,20,38)});
  if(s3kResidue.length>24)s3kResidue.shift();
  // Chips are existing authored debris, rather than circles or new collision shards.
  if(elem==='ice')for(let i=0;i<10;i++){const a=i*TAU/10;
    particles.push({x:q.x,y:q.y,vx:Math.cos(a)*2.3,vy:Math.sin(a)*2.3,
      life:.45+i%3*.10,t:0,r:1,_iceChip:1,_icSz:4+i%3,_icRot:a,_icSpin:7,_icF:i%8,color:'#9fe4ff'});
  }
};
er26Shot=function(){const q=S3K_BASE.shot.apply(this,arguments);s3kOrdnanceRules(q);return q;};
updatePlay=function(dt){
  for(const q of eBullets)s3kOrdnanceRules(q);
  const balls=eBullets.filter(q=>!q.dead&&enemyOrdnanceElement(q));
  for(const q of s3kResidue)q.t+=dt;s3kResidue=s3kResidue.filter(q=>q.t<.65);
  const result=S3K_BASE.update.apply(this,arguments);
  for(const q of balls)if((q.dead||!eBullets.includes(q))&&!q._tb28?.arrived&&q.y>PLAY.y&&q.y<VH&&q.x>camLeftX()&&q.x<camRightX())ordnanceBreak1002(q);
  return result;
};
s3ThermoBurstOrb=function(q){if(q?._intercepted){q._s3OrbBurst=true;return;}return S3K_BASE.thermoBurst.apply(this,arguments);};
drawEffects=function(){const result=S3K_BASE.effects.apply(this,arguments);
  for(const q of s3kResidue){if(q.stage!==run.stage)continue;const key='efx_burst_'+q.elem;
    // Hold the authored scattered aftermath briefly, independent of the impact reel.
    efxFrame(key,6,q.x-q.size/2,q.y-q.size/2,q.size,q.size,.42*(1-q.t/.65));}
  return result;
};
er26Book=function(b){const book=S3K_BASE.book(b).slice();if(!s3kOwns(b))return book;
  if(b._ship==='frostcruiser')book.splice(3,0,'elite-ram1004k');
  else {book.splice(2,0,'rime-missile1004k');book.splice(5,0,'rime-orbit1004k');}
  return book;
};
er26Set=function(b,mode){S3K_BASE.set.apply(this,arguments);if(!s3kOwns(b))return;
  const R=b._er26;R.s3kAim={x:player.x,y:player.y};R.s3kLocked=false;R.s3kDash=null;
  if(/1004k$/.test(mode)){R.warm=diffKey==='easy'?1.75:1.25;R.live=mode==='elite-ram1004k'?1.55:3.1;
    R.dur=R.warm+R.live;R.shot=0;R.wave=0;
    R.s3kOrbit={x:clamp(player.x,camLeftX()+110,camRightX()-110),y:clamp(player.y-155,PLAY.y+140,VH-185)};}
};
mr27Shape=function(b,id){const q=S3K_BASE.shape.apply(this,arguments),p=mr27Part(b,id);
  if(s3kOwns(b)&&p?._s3kPos){q.x=p._s3kPos.x;q.y=p._s3kPos.y;}return q;};
mr27Tick=function(b,dt){S3K_BASE.tick.apply(this,arguments);if(!s3kOwns(b)||!b._mr27)return;
  const R=b._er26;if(!R)return;
  if(R.t<(R.warm||0)-.4)R.s3kAim={x:player.x,y:player.y};
  const target=R.s3kAim||R.target||player;
  for(const p of b._mr27.parts){if(p.dead)continue;
    const base=S3K_BASE.shape(b,p.id),orbit=R.mode==='rime-orbit1004k'&&p.id.startsWith('gun');
    if(orbit){const a=R.t*.9+(p.id==='gunL'?Math.PI:0),C=R.s3kOrbit;
      const to={x:clamp(C.x+Math.cos(a)*105,camLeftX()+45,camRightX()-45),y:clamp(C.y+Math.sin(a)*68,PLAY.y+70,VH-115)};
      p._s3kPos=p._s3kPos||{x:base.x,y:base.y};p._s3kPos.x=lerp(p._s3kPos.x,to.x,Math.min(1,dt*4));p._s3kPos.y=lerp(p._s3kPos.y,to.y,Math.min(1,dt*4));
    }else if(p._s3kPos){p._s3kPos.x=lerp(p._s3kPos.x,base.x,Math.min(1,dt*7));p._s3kPos.y=lerp(p._s3kPos.y,base.y,Math.min(1,dt*7));
      if(Math.hypot(p._s3kPos.x-base.x,p._s3kPos.y-base.y)<1)delete p._s3kPos;}
    const q=mr27Shape(b,p.id),B=b._l23Beam,slot=p.id==='gunL'?'L0':'R0',idx=B?B.slots.indexOf(slot):-1;
    const a=idx>=0?B.angles[idx]-Math.PI/2:Math.atan2(target.y-q.y,target.x-q.x)-Math.PI/2;
    const da=Math.atan2(Math.sin(a-p.rot),Math.cos(a-p.rot));p.rot+=clamp(da,-dt*2.8,dt*2.8);
  }
};
l23BossBeamStart=function(b,family,slots,angles){
  if(s3kOwns(b))angles=slots.map(s=>{const p=shipBossMount(b,s),T=b._er26.s3kAim||b._er26.target;return Math.atan2(T.y-p.y,T.x-p.x);});
  const args=Array.from(arguments);args[3]=angles;return S3K_BASE.beamStart.apply(this,args);
};
l23BossBeamTick=function(b,dt){const B=b._l23Beam;
  if(s3kOwns(b)&&B&&!B.released&&B.t<B.warm-.4){for(let i=0;i<B.slots.length;i++){
    const p=shipBossMount(b,B.slots[i]),a=Math.atan2(player.y-p.y,player.x-p.x);B.angles[i]=a;if(B.baseAngles)B.baseAngles[i]=a;}}
  return S3K_BASE.beamTick.apply(this,arguments);
};
function s3kMG(b,slot,a){if(!mr27CanFire(b,slot))return;mr27Fire(b,slot,a);const p=shipBossMount(b,slot);
  const q=eShootT(p.x,p.y,a,5.3,'mg',{w:7,h:17,silent:true});Object.assign(q,{_boss:true,_noArsenal:true,_coldTracer1002:true,_er26Source:b._ship,_weaponProof:true});
  shipBossMuzzleStart(b,[slot],{fam:'mg',life:.08,hpx:28});Audio.SFX.machineGun?.();b._er26.shots++;
}
er26Combat=function(b,dt){if(!s3kOwns(b))return S3K_BASE.combat.apply(this,arguments);
  const R=b._er26,mode=R.mode;
  // Existing attacks use the same committed target as their FOV warning.
  if(!/1004k$/.test(mode)){
    if(R.t<R.warm-.4)R.angles=['L','C','R'].map(s=>{const p=shipBossMount(b,s),T=R.s3kAim||player;return Math.atan2(T.y-p.y,T.x-p.x);});
    return S3K_BASE.combat.apply(this,arguments);
  }
  R.warnings=[];
  if(mode==='elite-ram1004k'){
    const T=R.s3kAim||R.target,a=Math.atan2(T.y-b.y,T.x-b.x);
    if(R.t<R.warm){er26Warning(b,{x:b.x,y:b.y},a,b.w*.45);combatWarningTick(b,'s3k-ram-'+R.serial,R.t,R.warm);return;}
    if(!R.s3kDash){const A={target:{ref:T}};ra4DashSetup(b,A);A.distance=Math.min(A.distance,Math.hypot(A.tx-A.ox,A.ty-A.oy)+20);R.s3kDash=A;
      Audio.SFX.chargeDash?.();weaponFeedbackBurst('ram',b.x,b.y,88,.24,a);}
    const A=R.s3kDash,u=clamp((R.t-R.warm)/.62,0,1),e=u*u*(3-2*u);
    if(u<1){b.x=clamp(A.ox+Math.cos(A.a)*A.distance*e,camLeftX()+b.w*.3,camRightX()-b.w*.3);b.y=clamp(A.oy+Math.sin(A.a)*A.distance*e,PLAY.y+b.h*.3,VH-b.h*.22);
      for(const s of seatList())withSeat(s,()=>{if(!player.dead&&player.invuln<=0&&Math.hypot(player.x-b.x,player.y-b.y)<b.w*.29)playerHit('Frost Cruiser charge');});
    }else {b.x=lerp(b.x,er26Station(b,0),Math.min(1,dt*3));b.y=lerp(b.y,R.home,Math.min(1,dt*3));}
    b._drawY=b.y;return;
  }
  const rockets=mode==='rime-missile1004k',slots=rockets?['ROCKET_L','ROCKET_R']:['L','R'];
  for(const s of slots)if(mr27CanFire(b,s)){const p=shipBossMount(b,s),T=R.s3kAim||R.target;er26Warning(b,s,Math.atan2(T.y-p.y,T.x-p.x),rockets?32:26);}
  if(R.t<R.warm){combatWarningTick(b,'s3k-'+R.serial,R.t,R.warm);return;}R.warnings=[];
  R.shot-=dt;if(R.shot>0)return;
  if(rockets){if(R.wave>=3)return;for(const s of slots){if(!mr27CanFire(b,s))continue;
    const p=shipBossMount(b,s),T=R.s3kAim,a=Math.atan2(T.y-p.y,T.x-p.x);mr27Fire(b,s,a);
    const tip=shipBossMount(b,s);for(const off of [-.09,.09]){const q=eShootT(tip.x,tip.y,a+off,3.7,'emissile',{w:12,h:24,silent:true});
      Object.assign(q,{_boss:true,_noArsenal:true,_shootable:true,_weaponProof:false,_er26Source:b._ship,hp:2,homing:false});}
    shipBossMuzzleStart(b,[s],{fam:'missile',life:.16,hpx:30});Audio.SFX.enemyMissile?.();}
    R.wave++;R.shot=.7;
  }else {const side=R.wave++%2?'R':'L',p=shipBossMount(b,side),T=R.s3kAim;
    s3kMG(b,side,Math.atan2(T.y-p.y,T.x-p.x));R.shot=R.wave%8===0?.48:diffKey==='furious'?.12:.18;
  }
};
// Warm the actual effect strips before the first interception.
for(const k of ['efx_burst_fire','efx_burst_ice','nfb_decal',...Array.from({length:8},(_,i)=>'ndbr_'+i)])XART.rdy(k);
