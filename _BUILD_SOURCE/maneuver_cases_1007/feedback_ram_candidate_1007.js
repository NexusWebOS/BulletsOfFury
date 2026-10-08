"use strict";
/* Mike's October 2 encounter notes. This is the final gameplay layer; one source
   of geometry for art, muzzles, damage and Retina. Password choreography is separate. */
for(const a of Object.values(FB1002_ART))XART._src[a.key]=a.path;
const FB1002_BASE={stage:beginStage,play:updatePlay,spawn:spawnEnemy,fleet:furyFleetDraw,drawEnemy:drawEnemy,
 formOptions:weaponBaseForms,formSelect:weaponFormSelect,forge:forgeSelect,combine:forgeCombine,icon:weaponIconKey,
 rosterOwns:mr27Owns,rosterInit:mr27Init,shape:mr27Shape,blit:mr27Blit,coreDraw:mr27CoreDraw,drawRoster:mr27Draw,
 init:er26Init,book:er26Book,set:er26Set,combat:er26Combat,shot:er26Shot,war:er26WarTick,grid:er28Grid,
 polish:polishEncounterAttack,targets:_lockTargets,retinaDamage:retinaMissileDamage,mount:shipBossMount,
 damage:mr27Damage,beamDraw:l23BossBeamDraw,groundTick:groundTargetingTick,
 hammerTick:hammerBossTick,hammerDamage:hammerBossDamage,hammerDraw:hammerBossDraw,
 hammerDeath:hammerBossDeathTick,gunDraw:hammerBlasterGunDraw,volley:spaceVolleyLocks};
function fb1002Warm(){for(const a of Object.values(FB1002_ART))XART.rdy(a.key);}
function fb1002Cell(name,frame,x,y,w,h,tint,angle=0,alpha=1){
 const a=FB1002_ART[name];if(!a||!XART.rdy(a.key))return false;
 const r=a.frames[clamp(frame|0,0,a.frames.length-1)],im=tint?xartTint(a.key,tint,.82):XART.get(a.key);
 ctx.save();ctx.globalAlpha*=alpha;ctx.imageSmoothingEnabled=false;ctx.translate(x,y);ctx.rotate(angle);
 ctx.drawImage(im,...r,-w/2,-h/2,w,h);ctx.restore();return true;
}
function fb1002FreezerLocked(){return _pilotKey()==='freezer'&&run.mode==='campaign'&&!(run._freezerL2Cleared||((run.stage|0)>2));}
function fb1002FreezerEnforce(){if(!fb1002FreezerLocked())return;run.wvars=run.wvars||WEAPONS.map(()=>null);run.wvars[4]='icebreath';if(run.forge)delete run.forge[4];}
weaponBaseForms=function(w){if(w===4&&fb1002FreezerLocked())return [{kind:'variant',id:'icebreath',name:'ICE BREATH'}];return FB1002_BASE.formOptions(w);};
weaponFormSelect=function(w,o){if(w===4&&fb1002FreezerLocked()&&!(o?.kind==='variant'&&o.id==='icebreath'))return 'locked';return FB1002_BASE.formSelect(w,o);};
forgeSelect=function(w,e){if(w===4&&e&&fb1002FreezerLocked())return 'locked';return FB1002_BASE.forge(w,e);};
forgeCombine=function(w,e){if(w===4&&fb1002FreezerLocked())return 'locked';return FB1002_BASE.combine(w,e);};
const FB1002_CLEAR=freezerStageClearDefaults;
freezerStageClearDefaults=function(n){if(n===2&&_pilotKey()==='freezer')run._freezerL2Cleared=true;FB1002_CLEAR(n);fb1002FreezerEnforce();};
weaponIconKey=function(w,lv,opt){
 if(!spaceWeaponsActive()&&w===4&&_pilotKey()==='freezer'&&(fb1002FreezerLocked()||heldVariant(4)==='icebreath')&&(!opt?.fixed||opt.fixed==='icebreath'))return 'fb1002_icebreath';
 return FB1002_BASE.icon(w,lv,opt);
};
beginStage=function(n){const r=FB1002_BASE.stage.apply(this,arguments);run._damAssault1002=null;fb1002Warm();fb1002FreezerEnforce();return r;};

/* The dam is reached on the terrain's real-time clock. Freezer slows threats,
   not the campaign clock or the chopper's entry animation. */
function damAssaultReady1002(){
 if(run.stage!==1)return true;
 const A=run._damAssault1002;if(A)return A.done;
 run._damAssault1002={t:0,next:0,waves:0,done:false};return false;
}
function damAssaultTick1002(dt){
 const A=run._damAssault1002;if(run.stage!==1||!A||A.done)return;A.t+=dt;
 const n=fr27Difficulty(),count=diffKey==='easy'?2:3+n,total=diffKey==='easy'?3:4;
 if(A.waves<total&&A.t>=A.next){
  for(let j=0;j<count;j++){
   const x=camLeftX()+viewW()*(j+.5)/count,e=spawnEnemy('s1jetbomber_b',x,viewTopY()-100-j*40,{route:'straight'});
   if(e){e._damBomber1002={t:0,cd:.5+j*.22};e.pattern='s6strike';e._s6Strike={direction:'south',t:0,cd:999};e._noSep=true;e.shoots=false;e.fk=null;e._atk='none';e.hp=e.maxhp=[20,26,32][n];}
  }
  A.waves++;A.next=A.t+[4.6,4.1,3.7][n];Audio.SFX.tlvJetEngine?.();
 }
 if(A.waves>=total&&!enemies.some(e=>e._damBomber1002&&!e.dead)&&!groundTargetingFx.some(q=>q._dam1002&&!q.dead))A.done=true;
}
const FB1002_STRIKE=s6StrikeTick;
s6StrikeTick=function(e,dt){
 const D=e._damBomber1002;if(!D)return FB1002_STRIKE(e,dt);D.t+=dt;D.cd-=dt;e.y+=([105,135,165][fr27Difficulty()])*dt;e.spin=0;e._polishBomberCD=999;
 if(D.cd<=0&&e.y>viewTopY()+25&&e.y<player.y-60){D.cd=1.3;
  const count=groundTargetingFx.filter(q=>q._dam1002&&!q.dead).length;
  if(count<6){const q=groundTargetingSpawn({kind:'missile',owner:e,x:clamp(e.x,camLeftX()+32,camRightX()-32),y:clamp(player.y+rnd(-65,25),PLAY.y+100,PLAY.y+PLAY.h-30),track:false,lane:false,warn:1.45,radius:23,size:64,active:.42,onImpact:g=>{explode(g.x,g.y,68,'red');Audio.SFX.expBig?.();}});q._dam1002=true;q._jetBomb={x:e.x,y:e.y};Audio.SFX.enemyMissile?.();}
 }
 if(e.y>VH+100)e.dead=true;
};
furyFleetDraw=function(e){
 if(!e._damBomber1002)return FB1002_BASE.fleet(e);
 const mission=e._mission29;e._mission29=null;
 try{return MISSION29_BASE.fleet(e);}finally{e._mission29=mission;}
};

/* Retire every runtime golem entry, including old saved/editor wave names. */
spawnEnemy=function(type,x,y,opt){
 const fire=type==='golem'||type==='firejet1002';if(fire)type='lance';
 const e=FB1002_BASE.spawn(type,x,y,opt);
 if(fire&&e){e.type='firejet1002';e._fireJet1002=true;e.w=66;e.h=70;e.hp=e.maxhp=Math.ceil(32*DIFF.eHp);e._noSep=true;}
 return e;
};
drawEnemy=function(e){if(e._fireJet1002&&!e.dead&&e._dyingT==null){fb1002Cell('firejet',0,e.x,e.y,82,82,e.flash>0?hitFlashColor(e):null);return;}return FB1002_BASE.drawEnemy.apply(this,arguments);};
function ordnanceBreak1002(q){
 if(q._fbImpact1002||!q._er26Art&&q._er26Source!=='tb28'&&!q._s4wKind)return;
 q._fbImpact1002=true;const ice=q._er26Art==='ice';
 explode(q.x,q.y,q._er26Art?46:32,ice?'blue':'red',q._er26Art?'fireball':null);
 (ice?Audio.SFX.iceOrbImpact:Audio.SFX.missileHit)?.();Audio.SFX.expSmall?.();
}

/* 27 retina impacts, three spatial groups, staged in time. Tracking ends well
   before the red warning so the player can dodge committed positions. */
function fb1002Meteor(b){
 const n=3,L=camLeftX(),W=viewW(),order=[0,1,2];
 for(let i=order.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[order[i],order[j]]=[order[j],order[i]];}
 for(let group=0;group<n;group++)for(let r=0;r<3;r++)for(let c=0;c<3;c++){
  const zone=order[group],cx=L+W*(zone+.5)/3,cy=clamp(player.y-55+rnd(-42,42),PLAY.y+140,PLAY.y+PLAY.h-90);
  const q=groundTargetingSpawn({kind:'lava',owner:b,x:cx+(c-1)*36,y:cy+(r-1)*36,warn:1.65,delay:group*1.15,active:.36,radius:16,size:46,track:false,lane:false,sound:'expBig',shake:3,onImpact:g=>explode(g.x,g.y,49,'red','fireball')});
  q._meteor1002={group,zone,c,r,cx,cy,phase:rnd(0,TAU)};
 }
 er26Sound('bossWeaponCharge','enemyBossCannon');
}
er28Grid=function(b,mode){if(b._ship==='magmaward'&&diffKey==='furious')return fb1002Meteor(b);return FB1002_BASE.grid(b,mode);};
polishEncounterAttack=function(b,dt){
 const R=b._er26;if(b._ship==='magmaward'&&R.level===2&&/mortar/.test(R.mode)){
  if(!R.groundCast){R.groundCast=true;R.dur=5.7;fb1002Meteor(b);}return true;
 }return FB1002_BASE.polish(b,dt);
};
groundTargetingTick=function(dt){
 for(const q of groundTargetingFx){const M=q._meteor1002;if(!M||q.delay>0||q.t>=q.warn*.48)continue;
  const zoneL=camLeftX()+viewW()*M.zone/3,zoneR=zoneL+viewW()/3;
  const a=M.phase+q.t*2.2,px=clamp(player.x,zoneL+44,zoneR-44);
  q.x=clamp(M.cx*.72+px*.28+(M.c-1)*36+Math.cos(a)*12,zoneL+18,zoneR-18);
  q.y=clamp(M.cy+(M.r-1)*36+Math.sin(a)*16,PLAY.y+100,PLAY.y+PLAY.h-24);
 }return FB1002_BASE.groundTick(dt);
};

/* New Stage 3 miniboss: same modular rules and damage routing as the roster. */
mr27Owns=function(b){return b?._ship==='frostcruiser'||FB1002_BASE.rosterOwns(b);};
mr27Init=function(b){
 FB1002_BASE.rosterInit(b);if(b?._ship==='frostcruiser'&&b._mr27){b._mr27.skin='frost1002';XART.rdy('fb1002_frost_hull');}
 if(b?._ship==='stormsovereign'&&b._mr27&&!b._mr27.parts.some(p=>p.id==='lightning'))b._mr27.parts.push({id:'lightning',hp:b.maxhp*.09,max:b.maxhp*.09,dead:false,flash:0,recoil:0,angle:Math.PI/2});
};
const FB1002_FROST_NAMES=['frost_hull','frost_gun','frost_gun','frost_core','frost_missile','frost_missile'];
mr27Shape=function(b,id){
 if(b?._mr27?.skin==='frost1002'){
  const gun=id.startsWith('gun'),rocket=id.startsWith('rocket'),side=id.endsWith('L')?-1:1;
  const part=mr27Part(b,id),rot=part?.rot||0;
  if(id==='core')return {x:b.x,y:b.y-b.h*.05,w:b.w*.23,h:b.h*.23,cell:3,rot:0};
  return {x:b.x+side*b.w*(rocket?.36:.225),y:(b._drawY??b.y)+b.h*(rocket?.06:.015)-(part?.recoil||0)*3,w:b.w*(gun?.19:.16),h:b.h*(gun?.50:.31),cell:gun?(side<0?1:2):(side<0?4:5),rot};
 }
 if(id==='lightning')return {...FB1002_BASE.shape(b,'core'),w:b.w*.14,h:b.h*.39,cell:3};
 return FB1002_BASE.shape(b,id);
};
mr27Blit=function(skin,cell,p,flash,form,owner){
 if(skin!=='frost1002')return FB1002_BASE.blit.apply(this,arguments);
 const name=FB1002_FROST_NAMES[cell],a=FB1002_ART[name];if(!a)return false;
 if(flash>0)return fb1002Cell(name,0,p.x,p.y,p.w,p.h,hitFlashColor(owner||{}),p.rot||0);
 if(form==='fire'&&XART.rdy(a.key)){const im=xartPalette(a.key,'#ef6337');ctx.save();ctx.translate(p.x,p.y);ctx.rotate(p.rot||0);ctx.drawImage(im,...a.frames[0],-p.w/2,-p.h/2,p.w,p.h);ctx.restore();return true;}
 return fb1002Cell(name,0,p.x,p.y,p.w,p.h,null,p.rot||0);
};
mr27Draw=function(b){
 if(b._ship!=='frostcruiser')return FB1002_BASE.drawRoster(b);
 mr27Init(b);const M=b._mr27,R=b._er26,form=b._s3Nuclear?R.form:'ice';
 if(b._l23Beam)l23BossBeamDraw(b);
 mr27Blit('frost1002',0,{x:b.x,y:b.y,w:b.w,h:b.h},b.flash,form,b);
 for(const part of M.parts)if(!part.dead){const p=mr27Shape(b,part.id);mr27Blit(M.skin,p.cell,p,Math.max(part.flash,b.flash||0),form,b);}
 const core=mr27Shape(b,'core');mr27Blit(M.skin,3,core,b.flash,form,b);er26Draw(b);shipBossMuzzleDraw(b);M.draws++;return true;
};
er26Init=function(b){FB1002_BASE.init(b);if(b?._ship==='frostcruiser'){b.w=260;b.h=240;b.name=diffKey==='furious'?'THERMAL ELITE CRUISER':'ELITE FROST CRUISER';mr27Init(b);}};
er26Book=function(b){
 if(b._ship==='frostcruiser')return ['elite-ball1002','elite-beam1002','elite-missile1002','elite-strafe1002'];
 if(b._ship==='cryospear')return ['ice-battery1002','cannon-relay','ice-crossfire1002','glacier-press','ice-battery1002','cannon-relay'];
 const book=FB1002_BASE.book(b);if(b._ship==='stormsovereign')book.splice(2,0,'storm-lance1002');return book;
};
er26Set=function(b,mode){
 FB1002_BASE.set(b,mode);const R=b._er26;if(!/1002$/.test(mode))return;
 R.warm=diffKey==='easy'?1.65:[1.3,1.12,.95][R.level];R.live=mode.includes('beam')?1.1:3.0;R.dur=R.warm+R.live;R.shot=0;R.beamStarted=false;
};
er26Shot=function(b,slot,a,speed,opt={}){
 const q=FB1002_BASE.shot(b,slot,a,speed,opt);
 if(!q.dead&&b._ship==='frostcruiser'&&b._s3Nuclear&&b._er26.form==='fire'){q._er26Art='fire';q._er26Charred=true;q._weaponProof=!opt.large;}
 return q;
};
er26Combat=function(b,dt){
 const R=b._er26,mode=R.mode,n=R.level;if(!/1002$/.test(mode)||b._s4war)return FB1002_BASE.combat(b,dt);
 const fire=b._s3Nuclear&&R.form==='fire',family=fire?'inferno':'rime';
 b.x+=(er26Station(b,0)-b.x)*Math.min(1,dt*1.6);b.y+=(R.home-b.y)*Math.min(1,dt*2);b._drawY=b.y;R.warnings=[];
 if(mode==='elite-beam1002'){
  if(!R.beamStarted){const slots=['L0','L1','R0','R1'].filter(s=>mr27CanFire(b,s));l23BossBeamStart(b,family,slots,slots.map(s=>Math.PI/2+(s[0]==='L'?.14:-.14)),R.warm,1.1,.24,17);R.beamStarted=true;R.dur=R.warm+1.4;}
  l23BossBeamTick(b,dt);return;
 }
 for(const side of ['L','R'])if(mr27CanFire(b,side))er26Warning(b,side,R.angles[side==='L'?0:2],30);
 if(R.t<R.warm){combatWarningTick(b,'er26-'+R.serial,R.t,R.warm);return;}
 R.warnings=[];R.shot-=dt;if(R.shot>0)return;const wave=R.wave++,side=wave%2?'R':'L',a=R.angles[side==='L'?0:2];
 if(mode==='elite-ball1002'){
  er26Fan(b,side,a+Math.sin(wave*.8)*.14,3+n,.13,3.3+n*.55,{large:true});R.shot=[.68,.54,.42][n];
 }else if(mode==='elite-missile1002'){
  if(mr27CanFire(b,'ROCKET_'+side)){const p=shipBossMount(b,'ROCKET_'+side),q=eShootT(p.x,p.y,a+(wave%3-1)*.15,3.6+n*.6,'emissile',{w:12,h:24,silent:true});
   Object.assign(q,{_shootable:true,hp:2,homing:wave%2===0,_frostHoming:wave%2===0,turn:.014,spd:3.6+n*.6,ang:a,_boss:true,_noArsenal:true,_er26Source:'frostcruiser'});mr27Fire(b,'ROCKET_'+side,a);shipBossMuzzleStart(b,['ROCKET_'+side],{fam:'missile',life:.16,hpx:32});Audio.SFX.enemyMissile?.();}
  R.shot=[.6,.49,.39][n];
 }else {
  const p=shipBossMount(b,side);if(mr27CanFire(b,side)){
   const angle=a+(wave%7-3)*.055;
   for(const offset of (mode==='ice-crossfire1002'?[-.075,.075]:[0])){
    const q=eShootT(p.x,p.y,angle+offset,5.1+n*.55,'mg',{w:7,h:17,silent:true});Object.assign(q,{_boss:true,_noArsenal:true,_er26Source:b._ship,_coldTracer1002:true});
   }mr27Fire(b,side,angle);shipBossMuzzleStart(b,[side],{fam:'mg',life:.08,hpx:28});Audio.SFX.machineGun?.();
  }
  R.shot=wave%9===8?.48:[.115,.09,.072][n];
 }
 if(diffKey==='easy')R.shot*=1.55;R.shots++;
};
const FB1002_PROJECTILE=er26ProjectileDraw;
const FB1002_MUZZLE=er26Muzzle;
er26Muzzle=function(b,slot){if(b._ship==='frostcruiser'&&b._s3Nuclear&&b._er26.form==='fire')return shipBossMuzzleStart(b,[slot],{life:.16,hpx:44,fam:'magma'});return FB1002_MUZZLE(b,slot);};
er26ProjectileDraw=function(q){
 if(q._coldTracer1002){const key='l23fx_rime_mg_'+Math.floor((q.t||0)*18)%8;if(XART.rdy(key)){const im=XART.get(key);ctx.save();ctx.translate(q.x,q.y);ctx.rotate(Math.atan2(q.vy,q.vx)-Math.PI/2);ctx.drawImage(im,-7,-16,14,32);ctx.restore();}return true;}
 return FB1002_PROJECTILE(q);
};

/* Stage 4: a fifth destroyable weapon, guided interception, and a weaponless
   berserk ram. Surviving helpers have independent committed attack cycles. */
const FB1002_CAN_FIRE=mr27CanFire;
mr27CanFire=function(b,slot){if(b?._ship==='stormsovereign'&&['C','CORE','CL','CR'].includes(slot)&&b._mr27?.parts.find(p=>p.id==='lightning')?.dead)return false;return FB1002_CAN_FIRE(b,slot);};
mr27CoreDraw=function(b,q){
 if(b._ship!=='stormsovereign')return FB1002_BASE.coreDraw(b,q);
 // Generator/helper centres use their own geometry and flash, never the hull weapon.
 if(q.id!=='core')return mr27Blit('storm',3,q,q.flash||0,null,b);
 const part=b._mr27?.parts.find(p=>p.id==='lightning');if(part?.dead)return;
 const B=b._l23Beam,charge=B?clamp(B.t/B.warm,0,1):0,p=mr27Shape(b,'lightning');
 fb1002Cell('lightning_gun',Math.min(3,Math.floor(charge*4)),p.x,p.y,p.w,p.h,part?.flash>0?hitFlashColor(b):null);
};
shipBossMount=function(b,slot){if(b?._ship==='stormsovereign'&&slot==='C'&&b._mr27){const p=mr27Shape(b,'lightning');return {x:p.x,y:p.y+p.h*.41};}return FB1002_BASE.mount.apply(this,arguments);};
mr27Damage=function(b,dmg,x,y){
 if(b?._ship==='stormsovereign'&&b._mr27){const p=b._mr27.parts.find(p=>p.id==='lightning'),q=mr27Shape(b,'lightning');
  if(p&&!p.dead&&Number.isFinite(x+y)&&Math.abs(x-q.x)<q.w/2&&Math.abs(y-q.y)<q.h/2){
   const hit=Math.min(p.hp,dmg);p.hp-=hit;p.flash=.18;if(p.hp<=0){p.dead=true;b._l23Beam=null;d27ModuleRupture(b,p,q,'blue');Audio.SFX.shieldBreakCombat?.();}return hit;
  }
 }return FB1002_BASE.damage.apply(this,arguments);
};
function fb1002MissileTarget(q){if(q._fbRetina1002)return q._fbRetina1002;
 q._fbRetina1002=retinaDynamicPiece(q,'missile1002','hostile missile',()=>({x:q.x,y:q.y,hp:q.hp||1,dead:q.dead}),d=>{q.hp=(q.hp||1)-d;if(q.hp<=0){q.dead=true;ordnanceBreak1002(q);}},q.w||12,q.h||24);return q._fbRetina1002;
}
_lockTargets=function(){const a=FB1002_BASE.targets();if(run.stage===4)for(const q of eBullets)if(!q.dead&&q._shootable&&(q._s4wKind||q._er26Source==='stormsovereign'))a.push(fb1002MissileTarget(q));return a;};
function fb1002Helpers(b,dt){
 const S=b._s4war;if(!S?.coreUnlocked)return;
 for(const d of S.coreTurrets){if(d.dead||d.materialize<.9||b._mr27&&mr27HelperState(d).dead)continue;
  d._pressure1002=d._pressure1002||{t:0,cd:1.4+Math.random(),aim:null,burst:0};const P=d._pressure1002;P.t+=dt;P.cd-=dt;
  if(!P.aim&&P.cd<=0){P.aim={x:player.x,y:player.y,t:0};P.burst=0;}
  if(!P.aim)continue;P.aim.t+=dt;const warm=[1.0,.85,.72][fr27Difficulty()],a=Math.atan2(P.aim.y-d.y,P.aim.x-d.x);
  if(P.aim.t<warm){combatWarningTick(d,'helper1002',P.aim.t,warm);b._er26.warnings.push({x:d.x,y:d.y,angle:a,width:28,progress:P.aim.t/warm});continue;}
  if(P.burst<3&&P.aim.t>=warm+P.burst*.21){const p=stage4CoreTurretTip(d,P.burst%2?-1:1),q=stage4WarfareShot(b,p,a,4.1+fr27Difficulty()*.65,'rocket',{shootable:true,hp:2,accel:.6,max:6.5,szMul:.72});q._er26Source='stormsovereign';stage4CoreTurretMuzzle(b,d,P.burst%2?-1:1);P.burst++;Audio.SFX.enemyMissile?.();}
  if(P.aim.t>warm+1.0){P.aim=null;P.cd=[3.3,2.7,2.2][fr27Difficulty()];}
 }
}
er26WarTick=function(b,dt){
 if(b._ship!=='stormsovereign'||!b._mr27)return FB1002_BASE.war(b,dt);
 const R=b._er26,M=b._mr27,n=R.level,alive=M.parts.filter(p=>!p.dead),missing=M.parts.length-alive.length;
 // Custom lances and rams still advance the shared shield/helper rig. Leaving
 // these clocks in the base controller stranded helper muzzles offscreen.
 if(!b._s4war.shield.rearming&&((missing>=2&&!b.enter)||R.mode==='storm-lance1002')){
  R.warnings=[];stage4ShieldTick(b,dt);er26CoreTick(b,dt);
 }
 if(missing>=2&&!b.enter&&!b._s4war.shield.rearming){
  const E=M.ram1002||(M.ram1002={t:0,state:'tell',ox:b.x,oy:b.y,tx:player.x,ty:player.y-32});E.t+=dt;
  const noWeapons=alive.length===0;
  if(noWeapons){b._s4war.shield.active=false;b.flash=.10;b._hitFlashColor='#ff3737';if((E.t*12|0)!==E.smoke){E.smoke=E.t*12|0;addTrail(b.x+rnd(-b.w*.2,b.w*.2),b.y+b.h*.22,null,'missile');}}
  const baseWarm=diffKey==='easy'?1.4:[1.05,.9,.78][n],warm=typeof maneuverRamWarm==='function'?maneuverRamWarm(b,baseWarm,E):baseWarm;
  if(E.state==='tell'){combatWarningTick(b,'ram1002',E.t,warm);R.warnings=[{x:b.x,y:b.y,angle:Math.atan2(E.ty-b.y,E.tx-b.x),width:typeof maneuverRamWidth==='function'?maneuverRamWidth(b):b.w*.55,laneShape:'line',progress:E.t/warm}];
   if(E.t>=warm){E.state='drive';E.t=0;E.ox=b.x;E.oy=b.y;Audio.SFX.bossRoar?.();}}
  else if(E.state==='drive'){const p=clamp(E.t/.6,0,1),u=p*p*(3-2*p);b.x=lerp(E.ox,clamp(E.tx,camLeftX()+b.w*.4,camRightX()-b.w*.4),u);b.y=lerp(E.oy,Math.min(E.ty,VH*.72),u);
   if(player.invuln<=0&&!player.dead&&Math.hypot(player.x-b.x,player.y-b.y)<b.w*.42)playerHit();
   if(!noWeapons){E.cd=(E.cd||0)-dt;if(E.cd<=0){E.cd=.13;for(const side of ['L','R'])if(mr27CanFire(b,side))er26WarShot(b,side,aimPlayer(b.x,b.y),5.7,'lightningmg');for(const side of ['L','R'])if(mr27CanFire(b,'ROCKET_'+side))er26WarShot(b,side,aimPlayer(b.x,b.y),5.0,'rocket',{shootable:true,hp:2});}}
   if(p>=1){E.state='return';E.t=0;E.ox=b.x;E.oy=b.y;}}
  else{const p=clamp(E.t/1.2,0,1),u=p*p*(3-2*p);b.x=lerp(E.ox,er26Station(b,0),u);b.y=lerp(E.oy,R.home,u);if(E.t>2){M.ram1002=null;er26Set(b,'recover');}}
  b._drawY=b.y;fb1002Helpers(b,dt);return true;
 }
 if(R.mode==='storm-lance1002'&&!b._s4war.shield.rearming){
  if(!R.beamStarted){const slots=mr27CanFire(b,'C')?['C']:[];l23BossBeamStart(b,'rime',slots,[Math.PI/2],1.75,1.2,.25,35,{sweepArc:.26,sweepRate:1.6});if(b._l23Beam)b._l23Beam._fb1002=true;R.beamStarted=true;R.dur=3.3;Audio.SFX.warshipCoreCharge?.();}
  l23BossBeamTick(b,dt);if(R.t>=R.dur&&!b._l23Beam)er26Set(b,'recover');fb1002Helpers(b,dt);return true;
 }
 const result=FB1002_BASE.war(b,dt);fb1002Helpers(b,dt);return result;
};
l23BossBeamDraw=function(b){
 const B=b._l23Beam;if(!B?._fb1002)return FB1002_BASE.beamDraw(b);
 const p=shipBossMount(b,'C'),a=B.angles[0],end=PLAY.y+PLAY.h;
 if(B.t<B.warm){combatWarningDraw(b,{x:p.x,y:p.y,ex:p.x+Math.cos(a)*(end-p.y),ey:end,progress:B.t/B.warm,width:44});return;}
 const age=B.t-B.warm;if(age>B.active)return;
 const len=VH*1.1;ctx.save();ctx.translate(p.x,p.y);ctx.rotate(a-Math.PI/2);fb1002Cell('lightning_beam',1+(age*14|0)%2,0,len/2,42,len,null,0,.92);ctx.restore();
};

/* Ordinary Hammer fights keep every authored technique in their regular book.
   Password HAMA/HAMMER intros and dance/audio clocks are left authoritative. */
function fb1002NormalHammer(b){return b?._hammer&&!b._hammerTime&&!b._hama;}
function fb1002Guided(q){return !!q&&['gmiss','retinaMissile'].includes(q.kind)&&q.tgt?.kind==='hammer';}
hammerBossDamage=function(b,dmg){
 const h=b._hammer,q=_dmgBullet;
 if(b._hammerModuleHit==='hammer'&&hammerMissile(q)&&!fb1002Guided(q)){b._hammerModuleHit=null;return 0;}
 if(['whirl_warn','whirl_turn'].includes(h.state)&&b._hammerModuleHit==='hammer'){b._hammerModuleHit=null;return 0;}
 return FB1002_BASE.hammerDamage(b,dmg);
};
retinaMissileDamage=function(t,dmg,q){if(t?.kind==='hammer'&&hammerMissile(q)&&!fb1002Guided(q))return false;return FB1002_BASE.retinaDamage(t,dmg,q);};
spaceVolleyLocks=function(){return FB1002_BASE.volley.apply(this,arguments).filter(t=>t?.kind!=='hammer');};
function fb1002HammerDialogue(b){
 const h=b._hammer;h.intro1002=true;b._noHit=true;b.enter=false;
 BOFCinematicDirector.play('hammer-trap1002',[
  {who:'CHROME HAMMER',art:'fb1002_hammer_portrait',text:'Coming up here was merely a trap. The Legion has already launched its attack down on Earth.'},
  {who:'CHROME HAMMER',art:'fb1002_hammer_portrait',text:'Such a foolish mortal. This is the fate of the one who dances to their death. Now, let us dance!'}
 ],()=>{if(b!==boss||b.dead)return;b._noHit=false;hammerTarget(b);hammerState(b,'warn');Input.clearTaps();},true);
}
hammerBossTick=function(b,dt){
 if(!fb1002NormalHammer(b))return FB1002_BASE.hammerTick(b,dt);
 const h=b._hammer,prior=h.state,A=fr27Armor(b);
 // Replace the older conversation in the middle of unfolding. Speak once,
 // after the transformation completes and the whole boss is visible.
 b._cin30Spoke=true;
 if(A?.rage&&h.state==='recover'){
  h.t+=dt;if(h.t>=.35){if((h.ragePair1002||0)<2){h.comboPending=false;hammerTarget(b);hammerState(b,'warn');h.fastSecond1002=true;}else{h.ragePair1002=0;h.fastSecond1002=false;hammerState(b,'recharge1002');}}return;
 }
 if(h.state==='recharge1002'){
  h.t+=dt;const p=clamp(h.t/1.15,0,1),u=p*p*(3-2*p);b.x=lerp(h.ox,(camLeftX()+camRightX())/2,u);b.y=lerp(h.oy,VH*.34,u);
  if(h.t>1.8&&h.t<3.3){h.restShot1002=(h.restShot1002||0)-dt;if(h.restShot1002<=0){h.restShot1002=.48;for(const off of [-.18,.18])hammerEnergyBomb(b.x,b.y+30,Math.PI/2+off,3.6);}}
  if(h.t>=Math.max(BR_COOL,SS_COOL)+.65){h.restShot1002=0;hammerTarget(b);hammerState(b,'warn');}return;
 }
 if(h.fastSecond1002&&h.state==='warn'){h.t+=dt*.8;/* base warning arrives faster, never instant */}
 if(h.state==='hammer'&&h.t+dt>=hammerIdleDuration(false)&&!h.comboPending&&!h.phasePending&&!A?.rage){
  const next=(h.regularBook1002||0)%5;h.regularBook1002=(h.regularBook1002||0)+1;
  if(next===1){hammerBoomerangStart(b);return;}
  if(next===2){h.giantLeft=hammerHard()?2:1;hammerState(b,'giant_idle');return;}
  if(next===4){hammerBallArm(b);hammerState(b,'curl');return;}
 }
 // Orbital dives are available in Normal too; keep a pause after the pair.
 if(h.state==='giant_recover'&&h.t+dt>=.8&&h.giantLeft<=1){h.t+=dt;b._noHit=false;hammerState(b,'leap_reset');h.attackCycle++;h.comboPending=false;h.t=-1.4;return;}
 const result=FB1002_BASE.hammerTick(b,dt);
 if(prior==='unfold'&&h.state==='hammer'&&!h.intro1002)fb1002HammerDialogue(b);
 if(A?.rage&&prior==='leap'&&h.state==='recover'){h.ragePair1002=(h.ragePair1002||0)+1;h.fastSecond1002=false;}
 return result;
};
hammerBlasterGunDraw=function(b,alpha=1){
 const h=b._hammer,m=hammerBlasterMount(b),f=h.chainDestroyed?7:h.state==='chain_cool'?7:h.chainMuzzle>0?5+((h.chainSpin|0)&1):(h.chainHeat>.72?4:(h.chainSpin|0)%4);
 const a=FB1002_ART.chaingun;if(!XART.rdy(a.key))return FB1002_BASE.gunDraw(b,alpha);
 const r=a.frames[f],y=m.y-20,s=(m.muzzleY-y)/(a.muzzle[1]-a.pivot[1]),im=b.flash>0?xartTint(a.key,hitFlashColor(b),1):XART.get(a.key);
 ctx.save();ctx.globalAlpha*=alpha;ctx.drawImage(im,...r,m.x-a.pivot[0]*s,y-a.pivot[1]*s,r[2]*s,r[3]*s);ctx.restore();
};
hammerBossDraw=function(b){
 if(fb1002NormalHammer(b)&&b.dead)return fb1002HammerDeathDraw(b);
 if(b._hammer?.state==='recharge1002'){hammerOrbitalPose(b,11,1,b.flash>0?'white':null);return;}
 return FB1002_BASE.hammerDraw(b);
};
function fb1002HammerDeathDraw(b){
 const t=b.dying||0;if(t>=6.5)return;
 const j=t>2.5?Math.sin(t*93)*Math.min(5,(t-2.5)*2):Math.sin(t*35)*1.8;
 ctx.save();ctx.translate(j,Math.cos(t*67)*Math.min(3,t));
 fb1002Cell('deathbody',0,b.x+17,b.y+28,190,240,null,Math.sin(t*19)*.012);
 const head=t<.6?0:t<1.45?1:t<2.0?2:t<2.5?3:1;
 fb1002Cell('death_head',head,b.x+17,b.y-82,61,45,null,Math.sin(t*26)*(t>2.5?.07:.012));
 const arm=FB1002_ART.death_arm,f=t<2.45?0:Math.min(3,1+Math.floor((t-2.45)/.65)),r=arm.frames[f],s=.20;
 ctx.save();ctx.translate(b.x-39,b.y-55);ctx.scale(-1,1);ctx.rotate(t>=2.45?Math.sin(t*43)*.04:0);
 if(XART.rdy(arm.key))ctx.drawImage(XART.get(arm.key),...r,-arm.pivot[0]*s,-arm.pivot[1]*s,r[2]*s,r[3]*s);ctx.restore();
 if(t<.65)archBlit('hammer_spin',0,b.x-91,b.y+22,95,null,.5,1);
 ctx.restore();
 for(const q of b._hammer.deathFx1002||[]){const age=t-q.at;if(age>=0&&age<.9)fb1002Cell('electrical',Math.min(15,Math.floor(age/.9*16)),q.x,q.y,q.size,q.size,null,0,1-age*.2);}
}
hammerBossDeathTick=function(b,dt){
 if(!fb1002NormalHammer(b))return FB1002_BASE.hammerDeath(b,dt);
 b.dying+=dt;const t=b.dying,h=b._hammer;
 if(!h.deathFx1002){h.deathFx1002=[];h.deathEvents1002=[];groundTargetingCancel(b);eBullets=eBullets.filter(q=>!q._boss);h.stormWaves=[];h.throw=null;}
 const event=(id,at,fn)=>{if(t>=at&&!h.deathEvents1002.includes(id)){h.deathEvents1002.push(id);fn();}};
 event('hammer-core',.65,()=>{const p={x:b.x-91,y:b.y+22};h.deathFx1002.push({...p,at:t,size:130});explode(p.x,p.y,65,'blue');Audio.SFX.shieldBreakCombat?.();});
 event('scream',2.55,()=>{Audio.SFX.bossRoar?.();Audio.SFX.hammerImpact?.();});
 for(let i=0;i<5;i++)event('ring'+i,2.8+i*.32,()=>{_smokeRings.push({x:b.x,y:b.y,t:0,life:1.5,size:150+i*20,angle:i*Math.PI/4,flat:.35,still:true,front:true});Audio.SFX.expSmall?.();});
 h.deathCd=(h.deathCd||0)-dt;
 if(t>3.65&&t<6.45&&h.deathCd<=0){h.deathCd=t<4.65?.23:.08;const x=b.x+rnd(-66,66),y=b.y+rnd(-76,80);h.deathFx1002.push({x,y,at:t,size:rnd(80,150)});if(t>4.5)explode(x,y,rnd(45,85),'blue');Audio.SFX.expBig?.();}
 h.deathFx1002=h.deathFx1002.filter(q=>t-q.at<1);
 whiteBlast=t<5.5?0:t<6.05?(t-5.5)/.55:t<6.5?1:Math.max(0,1-(t-6.5)/1.2);shake=Math.max(shake,t<6.5?Math.min(16,t*2.2):0);
};
const FB1002_DRAW_BOSS=drawBoss,FB1002_POLISH_TICK=polishCombatTick;
const FB1002_DEATH_FX=unitDeathFX;
unitDeathFX=function(e){if(fb1002NormalHammer(e)&&e.dead)return;return FB1002_DEATH_FX.apply(this,arguments);};
drawBoss=function(){if(fb1002NormalHammer(boss)&&boss.dead){fb1002HammerDeathDraw(boss);return;}return FB1002_DRAW_BOSS();};
polishCombatTick=function(dt){if(fb1002NormalHammer(boss)&&boss.dead)boss._polishDeath=true;return FB1002_POLISH_TICK(dt);};
const FB1002_SNAPSHOT=campSnapshot,FB1002_APPLY=campApply;
campSnapshot=function(){const s=FB1002_SNAPSHOT();s.freezerL2Cleared=!!run._freezerL2Cleared;return s;};
campApply=function(s){const r=FB1002_APPLY(s);if(r){run._freezerL2Cleared=!!s.freezerL2Cleared||!!s.rank?.[2]||(s.stage|0)>2;fb1002FreezerEnforce();}return r;};
updatePlay=function(dt){if(!BOFCinematicDirector.live)damAssaultTick1002(dt);const r=FB1002_BASE.play(dt);fb1002FreezerEnforce();return r;};

/* Ordinary enemy hulls keep their authored forward pose. Motion and attack aim
   are independent: sidesteps remain real, while turrets still swivel. Death
   spins, player evasions, bosses and cardinal bomber headings keep ownership. */
function fb1002Straight(e){return !!e&&!e.dead&&e._dyingT==null&&!e._prop&&!e.prop&&!isSetPiece(e);}
const FB1002_AI_END=ai27End,FB1002_HARDPOINT=combatHardpoint;
ai27End=function(e,previous){const r=FB1002_AI_END(e,previous);if(fb1002Straight(e)){e.spin=0;e._bank=0;e._frBank=0;e._spinA=0;e._rot=0;}return r;};
combatHardpoint=function(e,ox,oy){
 if(!fb1002Straight(e))return FB1002_HARDPOINT(e,ox,oy);
 return {x:e.x+(e._bodyW||e.w||40)*(ox||0),y:e.y+(e._bodyH||e.h||40)*(oy||0)};
};
const FB1002_STRAIGHT_DRAW=drawEnemy;
drawEnemy=function(e){
 if(!fb1002Straight(e))return FB1002_STRAIGHT_DRAW(e);
 fb1002SewerWarning(e);
 const keys=['spin','_bank','_frBank','_spinA','_rot','_twist','_roll','_rollT','_faceAng','_travelAng','_furyMove','_s8Roll','_s8RollT','_phase'],saved=keys.map(k=>e[k]);
 e.spin=e._bank=e._frBank=e._spinA=e._rot=e._twist=0;e._roll=e._rollT=e._furyMove=e._s8Roll=e._s8RollT=null;
 if(!e._hwLaunch&&!e._hwPeel&&e.pattern!=='s6strike'){e._faceAng=Math.PI;e._travelAng=Math.PI;}
 if(e.pattern==='kamikaze')e._phase='straight';
 try{return FB1002_STRAIGHT_DRAW(e);}finally{keys.forEach((k,i)=>{if(saved[i]===undefined)delete e[k];else e[k]=saved[i];});}
};

/* Sewer flyers: one frozen aim per warning, then a short staggered burst.
   Shared toxic art, real barrel flashes, and pauses preserve readable lanes. */
const FB1002_TOXIC_TICK=s7ToxicTick;
s7ToxicTick=function(e,dt){
 if(!['s7lamprey','s7serpent','s7sampler'].includes(e._s7toxic))return FB1002_TOXIC_TICK(e,dt);
 const n=fr27Difficulty(),A=e._straight1002||(e._straight1002={t:0,cd:1.1,phase:'approach',seq:0});A.t+=dt;e._s7t=(e._s7t||0)+dt;
 const top=viewTopY(),home=top+viewH()*.25;
 if(A.t>12&&A.phase==='rest'){e.y+=110*dt;if(e.y>VH+100)e.dead=true;return;}
 if(e.y<home){e.y+=Math.min(home-e.y,80*dt);return;}
 if(A.home==null)A.home=e.x;
 e.x+=clamp(A.home-e.x,-65*dt,65*dt);A.cd-=dt;
 if(A.phase==='approach'){A.phase='rest';A.cd=.7;}
 if(A.phase==='rest'&&A.cd<=0&&e.y<player.y-70){
  A.phase='tell';A.age=0;A.aim={x:player.x,y:player.y};A.warm=diffKey==='easy'?1.25:[.92,.78,.65][n];A.fired=0;A.seq++;
 }
 if(A.phase==='tell'||A.phase==='burst'){
  A.age+=dt;combatWarningTick(e,'sewer1002-'+A.seq,Math.min(A.age,A.warm),A.warm);
  if(A.age>=A.warm){A.phase='burst';
   if(A.fired<3&&A.age>=A.warm+A.fired*.19){
    const side=A.fired%2?-1:1,p=combatHardpoint(e,side*.22,.35),a=Math.atan2(A.aim.y-p.y,A.aim.x-p.x);
    const laser=e._s7toxic==='s7sampler',kind=laser?'s7laser':e._s7toxic==='s7serpent'?'s7bio':'s7sludge';
    const q=eShootT(p.x,p.y,a+(A.fired-1)*.06,laser?4.2+n*.35:2.85+n*.35,kind,{w:laser?8:17,h:laser?30:20,silent:true});q._noArsenal=true;
    if(kind==='s7bio'){q._s7Accel=.6;q._s7Max=4.8;}
    stage7Muzzle(e,side*.22,.35,.75,.14);(laser?Audio.SFX.enemyHeavyLaser:Audio.SFX.combatOrb0927)?.();A.fired++;
   }
   if(A.age>A.warm+.75){A.phase='rest';A.cd=(diffKey==='easy'?3.6:[2.8,2.3,1.9][n]);A.home=clamp(e.x+(A.seq%2?48:-48),camLeftX()+e.w*.6,camRightX()-e.w*.6);}
  }
 }
 e.spin=0;
};
function fb1002SewerWarning(e){const A=e._straight1002;if(A?.phase==='tell')combatWarningDraw(e,{x:e.x,y:e.y+e.h*.35,ex:A.aim.x,ey:A.aim.y,progress:A.age/A.warm,width:52,alpha:.26});}

/* Stage 8 retains the existing four authored hull roles, with fixed facing.
   Each release is committed before its burst; larger attacks leave a gap. */
s8MegaTick=function(e,dt){
 const n=fr27Difficulty(),row=fr27RealmRow(e),A=e._frRealmAI||(e._frRealmAI={t:0,cd:1.0+Math.random()*.65,shot:0,home:e.x,seq:0});
 A.t+=dt;A.cd-=dt;A.shot=Math.max(0,A.shot-dt);e._frBank=0;e.spin=0;
 e.x+=clamp(A.home-e.x,-75*dt,75*dt);
 if(A.seq>=2){e.y+=100*dt;if(e.y>VH+100)e.dead=true;return;}
 // A charging gunship must not drift into point-blank range while its own
 // firing gate suppresses the release. Hold the pocket through the tell.
 const pocket=viewTopY()+viewH()*.39;
 if(!A.tell&&e.y<pocket)e.y+=Math.min(pocket-e.y,dt*[55,37,76,28][row]);
 if(e.y>player.y-65||e.y<viewTopY()+e.h*.5||e.x<camLeftX()+12||e.x>camRightX()-12)return;
 const warm=diffKey==='easy'?1.25:[1.0,.85,.72][n];
 if(A.cd<=0&&!A.tell)A.tell={t:0,x:player.x,y:player.y,fired:0};
 if(!A.tell)return;const T=A.tell;T.t+=dt;combatWarningTick(e,'realm-'+A.seq,Math.min(T.t,warm),warm);
 if(T.t<warm)return;
 if(T.fired<3&&T.t>=warm+T.fired*.18){
  const side=T.fired%2?-1:1,p=combatHardpoint(e,side*.20,.4),a=Math.atan2(T.y-p.y,T.x-p.x);
  if(row===0){for(const o of [-.09,.09])fr27RealmShot(p.x,p.y,a+o,3.4+n*.55,0);}
  else if(row===1){const q=fr27RealmShot(p.x,p.y,a+side*.22,2.65+n*.4,1);q._frBurst=1.15;}
  else if(row===2){fr27RealmShot(p.x,p.y,a+(T.fired-1)*.06,4.7+n*.5,0);}
  else{const count=9,step=TAU/count;for(let i=0;i<count;i++){const angle=i*step,d=Math.abs(Math.atan2(Math.sin(angle-a),Math.cos(angle-a)));if(d<step*1.25)continue;fr27RealmShot(p.x,p.y,angle,2.6+n*.25,2);}T.fired=2;}
  s8Muzzle(e,side*.2,.4,.8,.14);Audio.SFX.enemyHeavyLaser?.();T.fired++;A.shot=.2;
 }
 if(T.t>=warm+.8){A.tell=null;A.seq++;A.cd=(diffKey==='easy'?4.2:[3.0,2.65,2.3][n]);}
};
const FB1002_REALM_DRAW=drawS8Mega;
drawS8Mega=function(e){const A=e._frRealmAI,bank=e._frBank,tell=A?.tell;e._frBank=0;
 // Base warning uses a fixed .8 second clock. Draw with the actual difficulty
 // clock here and temporarily hide its warning to avoid doubling the field.
 if(tell){const warm=diffKey==='easy'?1.25:[1,.85,.72][fr27Difficulty()];if(tell.t<warm)combatWarningDraw(e,{x:e.x,y:e.y+e.h*.35,ex:tell.x,ey:tell.y,progress:tell.t/warm,width:fr27RealmRow(e)===2?34:82,alpha:.28});A.tell=null;}
 try{return FB1002_REALM_DRAW(e);}finally{e._frBank=bank;if(A)A.tell=tell;}
};
