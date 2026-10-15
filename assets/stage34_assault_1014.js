"use strict";
/* Mike's October 14 playthrough: earned Storm, cold encounters and committed
   attacks. Existing authored plates, modular HP and weapon mounts remain owners. */
const SA14={events:[],base:{init:er26Init,tick:er26Tick,book:er26Book,set:er26Set,
 combat:er26Combat,war:er26WarTick,phase:er28PhaseCheck,draw:mr27Draw,shape:mr27Shape,
 fire:mr27Fire,blit:mr27Blit,over:mr27Over,nodes:stage4ShieldSyncNodes,
 rules:s3kOrdnanceRules,canIntercept:enemyOrdnanceCanIntercept,proof:enemyDefensiveProof,
 strike:s3ThermoStrikeTick,strikeDraw:s3ThermoStrikeDraw,bg:drawBG,
 update:updatePlay,enemy:drawEnemy,flight:air13DrawFlight,begin:beginStage,
 values:ph8Values,load:stageLoadBegin},serial:0};
const SA14_CFG={easy:{warm:1.55,lock:2.10,mg:.18,speed:4.5,waves:3,gap:.48},
 normal:{warm:1.35,lock:1.85,mg:.115,speed:5.2,waves:4,gap:.38},
 hard:{warm:1.18,lock:1.65,mg:.085,speed:5.7,waves:5,gap:.31},
 furious:{warm:1.06,lock:1.48,mg:.065,speed:6.2,waves:6,gap:.26}};
function sa14Cfg(){return SA14_CFG[diffKey==='insanity'?'furious':diffKey]||SA14_CFG.normal;}
function sa14Owns(b){return sa14Cold(b)||(run.stage===4&&!!b&&['olivewarden','stormsovereign'].includes(b._ship));}
function sa14Storm(b){return run.stage===4&&b?._ship==='stormsovereign';}
function sa14Cold(b){return run.stage===3&&!!b&&['frostcruiser','cryospear'].includes(b._ship);}
function sa14Log(event,b,data={}){SA14.events.push({event,ship:b?._ship,...data});if(SA14.events.length>240)SA14.events.shift();}
function sa14State(b){return b._sa14||(b._sa14={age:0,angle:0,scale:1,depth:false,glow:0,
 lockCd:2.5,escortCd:2.7,escortWave:0,engine:{},rumbleCd:0});}
function sa14Stop(b){if(b?._sa14)window.BOF_CHIP_PASS?.stop(b._sa14.engine);}
function sa14Earned(R){return R?.pilot==='yuri'&&!!(R._earnedUnlocks?.lightningOrb||R._earnedUnlocks?.thunderStorm);}
function sa14YuriSync(){for(const R of [run,...(coopActive()?[run2]:[])])if(sa14Earned(R)){
 R._thunderStormUnlocked=true;R._chainLightningLevel=Math.max(2,R._chainLightningLevel||1);
}}
beginStage=function(){for(const b of [boss,subBoss])sa14Stop(b);
 const result=SA14.base.begin.apply(this,arguments);sa14YuriSync();return result;};
ph8Values=function(){const q=SA14.base.values.apply(this,arguments);
 if(q.pilot==='yuri'&&run._thunderStormUnlocked)q.name=/MK II/.test(q.name)?'THUNDER STORM MK II':'THUNDER STORM';return q;};
SC_UNLOCKS[4].yuri=[['LIGHTNING ORB','micon_lightningorb_3'],['THUNDER STORM','yuri_storm_icon_0919']];
stageLoadBegin=function(n,keys){const extra=[];
 if(n===3||n===4){for(let i=0;i<16;i++)extra.push('s4w_lightning_ball_'+i);
  for(let i=0;i<4;i++)extra.push('retm_'+i,'retmb_'+i);
  extra.push('cfx_stage4_chain_lightning','mr27_corefx','efx_burst_lightning');
  if(n===4)extra.push(AM13_ART.flight_variant_4.heading.key,AM13_ART.flight_variant_4.roll.key);
  Snd.prepare?.(['lockon','chargeDash','geyserLightning','missileLaunch','expIce','gd_tankEngineLoop']);
 }return SA14.base.load.call(this,n,[...(keys||[]),...extra]);};
function sa14Freeze(b){if(!sa14Cold(b))return;
 // No nuclear replacement of the ice miniboss. Its authored hull/parts survive.
 if(b._ship==='frostcruiser'){S3_THERMO_STRIKE.mini=null;delete b._s3Nuclear;delete b._s3Thermo;}
 if(b._er26){b._er26.form='ice';b._er26.formBeats=0;b._er26.neutralOpening=false;}
}
er26Init=function(b){const r=SA14.base.init.apply(this,arguments);if(sa14Owns(b)){sa14State(b);sa14Freeze(b);}return r;};
s3ThermoStrikeTick=function(role,b){if(sa14Cold(b)){
 S3_THERMO_STRIKE[role]=null;sa14Freeze(b);return false;
}return SA14.base.strike.apply(this,arguments);};
s3ThermoStrikeDraw=function(role,b){if(sa14Cold(b))return false;return SA14.base.strikeDraw.apply(this,arguments);};
er28PhaseCheck=function(b){if(sa14Owns(b))return false;return SA14.base.phase.apply(this,arguments);};
er26Book=function(b){
 if(!sa14Owns(b))return SA14.base.book.apply(this,arguments);
 if(b?._ship==='cryospear')return ['sa14-mg','sa14-rockets','sa14-ice','sa14-mg','sa14-ice'];
 if(b?._ship==='olivewarden')return ['sa14-mg','sa14-rockets','sa14-mg','sa14-rockets'];
 if(sa14Storm(b))return ['sa14-drive','sa14-storm','sa14-rockets','sa14-mg','sa14-overflight'];
 return SA14.base.book.apply(this,arguments);
};
er26Set=function(b,mode){
 if(sa14Cold(b)&&['nuclear','form-change','overdrive'].includes(mode))mode='recover';
 const result=SA14.base.set.call(this,b,mode);if(!sa14Owns(b))return result;
 const A=sa14State(b),R=b._er26,c=sa14Cfg();sa14Stop(b);A.glow=0;A.depth=false;
 A.fromAngle=A.angle;A.fromScale=A.scale;
 if(!mode.startsWith('sa14-'))return result;
 R._sa14={aim:{x:player.x,y:player.y},from:{x:b.x,y:b.y},shot:0,wave:0,
  beep:0,thunder:0,released:false,moveTo:b.x,seek:null};
 R.warm=mode==='sa14-lock'?c.lock:mode==='sa14-ice'||mode==='sa14-storm'?c.warm+.55:c.warm;
 R.live=mode==='sa14-mg'?2.6:mode==='sa14-rockets'?c.waves*c.gap+.5:mode==='sa14-ice'||mode==='sa14-storm'?3.6:1.8;
 R.dur=R.warm+R.live;R.warnings=[];b._l23Beam=null;b._ap10Storm=null;
 if(b._mr27)b._mr27.ram1002=null;
 if(mode==='sa14-overflight')R.dur=10.5;
 if(mode==='sa14-lock')A.lockCd=5.2;
 sa14Log('attack',b,{mode,warm:R.warm});return result;
};
// One physical transform owns hull, attached parts, generators and Retina.
function sa14Transform(b,p){const A=b._sa14;if(!sa14Storm(b)||!A)return p;
 const angle=A.angle||0,k=A.scale||1,cy=b._drawY??b.y,c=Math.cos(angle),s=Math.sin(angle),dx=(p.x-b.x)*k,dy=(p.y-cy)*k;
 return {...p,x:b.x+dx*c-dy*s,y:cy+dx*s+dy*c,w:p.w*k,h:p.h*k,rot:(p.rot||0)+angle};
}
mr27Shape=function(b,id){let p=SA14.base.shape.apply(this,arguments);
 if(sa14Storm(b)&&id?.startsWith('rocket')&&b._er26.mode==='sa14-lock'&&b._er26.t<b._er26.warm)
  p={...p,x:p.x+Math.sin(b._er26.t*55)*1.8,y:p.y+Math.sin(b._er26.t*47)*1.2};
 return sa14Transform(b,p);};
mr27Fire=function(b,slot,angle){return SA14.base.fire.call(this,b,slot,sa14Storm(b)?angle-(b._sa14?.angle||0):angle);};
stage4ShieldSyncNodes=function(b){
 if(!sa14Storm(b)||!b._s4war?.shield)return SA14.base.nodes.apply(this,arguments);
 const H=b._s4war.shield;H.anchorX=Math.min(VW*.5-36,b.w*.67+36);H.anchorY=46;H.rowOffset=78;
 for(const n of H.nodes){const p=sa14Transform(b,{x:b.x+n.side*H.anchorX,y:(b._drawY??b.y)+H.anchorY+n.row*H.rowOffset,w:54,h:54});n.x=p.x;n.y=p.y;}
};
function sa14Electric(q){return !!q&&(q._sa14Electric||s4ac13Electric(q));}
s3kOrdnanceRules=function(q){if(sa14Electric(q)){q._weaponProof=true;q._shootable=false;q._s3kOriginalProof=true;return;}
 return SA14.base.rules.apply(this,arguments);};
enemyOrdnanceCanIntercept=function(q){return !sa14Electric(q)&&SA14.base.canIntercept.apply(this,arguments);};
enemyDefensiveProof=function(q){return sa14Electric(q)||SA14.base.proof.apply(this,arguments);};
function sa14Rumble(b,strength,dt){const A=sa14State(b);A.rumbleCd-=dt;if(A.rumbleCd>0)return;A.rumbleCd=.18;
 for(const pad of navigator.getGamepads?.()||[])if(pad?.vibrationActuator?.playEffect){
  try{pad.vibrationActuator.playEffect('dual-rumble',{duration:150,strongMagnitude:strength,weakMagnitude:strength*.6}).catch(()=>{});}catch(_){}
 }}
function sa14Rev(b,progress,dt){const A=sa14State(b);shake=Math.max(shake,1.2+progress*3);
 const voice=window.BOF_CHIP_PASS?.sound(A.engine,'gd_tankEngineLoop',{loop:true,gain:1.8});
 if(voice)voice.el.playbackRate=(.8+progress*.9)*Math.max(.5,Math.min(2,timeScale));sa14Rumble(b,.15+progress*.35,dt);
}
function sa14Warning(b,point,target,width,progress){b._er26.warnings.push({x:point.x,y:point.y,
 angle:Math.atan2(target.y-point.y,target.x-point.x),width,progress});}
function sa14FanWarning(b,progress){const T=b._er26._sa14,count=7+vp12Tier()*2,gap=(T.wave%3)+2,p=shipBossMount(b,'C');
 for(let i=0;i<count;i++){if(i===gap||i===gap+1)continue;const angle=Math.PI/2+(i-(count-1)/2)*.145;
  sa14Warning(b,p,{x:p.x+Math.cos(angle)*VH,y:p.y+Math.sin(angle)*VH},16,progress);
 }}
function sa14Slug(b,slot,target,spread=0){if(!mr27CanFire(b,slot))return;
 const mount=shipBossMount(b,slot),angle=Math.atan2(target.y-mount.y,target.x-mount.x)+spread;
 mr27Fire(b,slot,angle);const p=shipBossMount(b,slot),q=eShootT(p.x,p.y,angle,sa14Cfg().speed,'mg',{w:7,h:17,silent:true});
 Object.assign(q,{_boss:true,_noArsenal:true,_weaponProof:true,_shootable:false,mg:true,_coldTracer1002:true,_er26Source:b._ship,_sa14Slug:true});
 shipBossMuzzleStart(b,[slot],{fam:'mg',life:.08,hpx:30});Audio.SFX.machineGun?.();b._er26.shots++;
}
function sa14Missiles(b,target,lock=false){let count=0;
 for(const slot of ['ROCKET_L','ROCKET_R']){if(!mr27CanFire(b,slot))continue;
  const initial=shipBossMount(b,slot),angle=Math.atan2(target.y-initial.y,target.x-initial.x);mr27Fire(b,slot,angle);
  const p=shipBossMount(b,slot);
  for(const off of (lock?[-.10,0,.10]:[-.055,.055])){
   const q=eShootT(p.x,p.y,angle+off,3.5+vp12Tier()*.45,'emissile',{w:12,h:24,silent:true});
   Object.assign(q,{_boss:true,_noArsenal:true,_shootable:true,_weaponProof:false,hp:2,homing:false,
    _er26Source:b._ship,_sa14Missile:true,_sa14Target:{...target}});count++;
  }shipBossMuzzleStart(b,[slot],{fam:'missile',life:.18,hpx:34});
 }if(count){Audio.SFX.missileLaunch?.();sa14Log('missile-volley',b,{count,lock,target:{...target}});}return count;
}
function sa14Balls(b,ice,behind=false){const R=b._er26,T=R._sa14,c=sa14Cfg(),count=7+vp12Tier()*2;
 const gap=(T.wave%3)+2,angles=[];
 for(let i=0;i<count;i++){if(i===gap||i===gap+1)continue;
  const angle=Math.PI/2+(i-(count-1)/2)*.145;
  const p=behind?{x:b.x+(i-(count-1)/2)*4,y:(b._drawY??b.y)+b.h*.35}:shipBossMount(b,'C');
  const q=ice?er26Shot(b,p,angle,2.8+vp12Tier()*.3,{large:true}):stage4WarfareShot(b,p,angle,2.8+vp12Tier()*.35,'orb',{szMul:.7});
  if(q.dead)continue;q._er26Source=b._ship;q._sa14Volley=true;
  if(!ice){s4ac13Mark(q);q._sa14Electric=true;q._weaponProof=true;q._shootable=false;q._s3kOriginalProof=true;}
  angles.push(angle);
 }T.wave++;R.shots+=angles.length;shake=Math.max(shake,ice?4:6);
 (ice?Audio.SFX.expIce:Audio.SFX.geyserLightning)?.();
 shipBossMuzzleStart(b,['C'],{fam:ice?'cryo':'lightning',life:.22,hpx:70});
 sa14Log(ice?'ice-volley':'lightning-volley',b,{wave:T.wave,gap,angles,x:b.x,y:b.y});
}
function sa14Upper(){let chosen=null;for(const seat of seatList())withSeat(seat,()=>{
 if(!player.dead&&!player.out&&player.y<PLAY.y+PLAY.h*.5&&(!chosen||player.y<chosen.player.y))chosen={seat,player};
});return chosen;}
function sa14Attack(b,dt){const R=b._er26,A=sa14State(b),T=R._sa14,c=sa14Cfg(),mode=R.mode;
 if(!T)return false;R.warnings=[];
 if(mode==='sa14-overflight')return sa14Overflight(b,dt);
 A.angle=0;A.scale=1;A.depth=false;b._s4Airborne=false;
 if(mode==='sa14-lock'){
  const upper=sa14Upper();if(!T.released&&!upper){sa14Log('lock-cancel',b);er26Set(b,'recover');A.lockCd=1.5;return true;}
  if(!T.seek&&upper)T.seek=upper.player;
  if(R.t<R.warm-.40&&T.seek&&!T.seek.dead)T.aim={x:T.seek.x,y:T.seek.y};
  if(R.t<R.warm){const progress=clamp(R.t/R.warm,0,1);sa14Warning(b,shipBossMount(b,'C'),T.aim,52,progress);
   T.beep-=dt;if(T.beep<=0){T.beep=.18;Audio.SFX.lockon?.();sa14Log('lock-beep',b,{progress});}
   sa14Rev(b,progress,dt);return true;
  }if(!T.released){T.released=true;sa14Stop(b);sa14Log('retina-lock',b,{target:{...T.aim}});}
  T.shot-=dt;if(T.wave<c.waves&&T.shot<=0){sa14Missiles(b,T.aim,true);T.wave++;T.shot=c.gap;}
  if(R.t>=R.dur)er26Set(b,'recover');return true;
 }
 if(mode==='sa14-drive'){
  if(R.t<R.warm){if(R.t<R.warm-.45)T.aim={x:player.x,y:player.y};
   sa14Warning(b,{x:b.x,y:b.y},T.aim,b.w*.48,R.t/R.warm);sa14Rev(b,R.t/R.warm,dt);return true;}
  if(!T.released){T.released=true;T.to={x:clamp(T.aim.x,camLeftX()+b.w*.28,camRightX()-b.w*.28),y:clamp(T.aim.y-36,PLAY.y+b.h*.3,VH*.78)};
   sa14Stop(b);Audio.SFX.chargeDash?.();shake=Math.max(shake,7);sa14Log('charge-release',b,{target:T.to});}
  const t=R.t-R.warm,u=clamp(t/.68,0,1),ease=u*u*(3-2*u);
  if(t<.68){b.x=lerp(T.from.x,T.to.x,ease);b.y=lerp(T.from.y,T.to.y,ease);
   for(const seat of seatList())withSeat(seat,()=>{if(!player.dead&&player.invuln<=0&&Math.abs(player.x-b.x)<b.w*.28&&Math.abs(player.y-b.y)<b.h*.28)playerHit('Warned Sovereign charge');});
  }else{const u=clamp((t-.68)/1.12,0,1),k=u*u*(3-2*u);b.x=lerp(T.to.x,er26Station(b,0),k);b.y=lerp(T.to.y,R.home,k);}
  b._drawY=b.y;if(R.t>=R.dur)er26Set(b,'recover');return true;
 }
 const charged=mode==='sa14-ice'||mode==='sa14-storm';
 if(!charged){b.x+=clamp(er26Station(b,0)-b.x,-55*dt,55*dt);b.y+=clamp(R.home-b.y,-65*dt,65*dt);}
 if(R.t<R.warm){if(R.t<R.warm-.4)T.aim={x:player.x,y:player.y};
  const slots=mode==='sa14-rockets'?['ROCKET_L','ROCKET_R']:mode==='sa14-mg'?['L','R']:['C'];
  if(charged)sa14FanWarning(b,R.t/R.warm);
  else for(const slot of slots)if(mr27CanFire(b,slot))sa14Warning(b,shipBossMount(b,slot),T.aim,28,R.t/R.warm);
  combatWarningTick(b,'sa14-'+R.serial,R.t,R.warm);
  if(charged){A.glow=R.t/R.warm;T.thunder-=dt;if(T.thunder<=0){T.thunder=.42;Audio.SFX.geyserLightning?.();sa14Log('charge-thunder',b);}}
  else if(mode==='sa14-rockets')sa14Rumble(b,.25,dt);
  b._drawY=b.y;return true;
 }
 A.glow=charged?Math.max(0,A.glow-dt*3):0;T.shot-=dt;
 if(charged){b.x+=clamp(T.moveTo-b.x,-115*dt,115*dt);
  if(T.wave>0&&T.wave<4&&T.shot>0){A.glow=clamp(1-T.shot/.82,0,1);sa14FanWarning(b,A.glow);
   combatWarningTick(b,'sa14-salvo-'+R.serial+'-'+T.wave,.82-T.shot,.82);
   T.thunder-=dt;if(T.thunder<=0&&A.glow>.35){T.thunder=.45;Audio.SFX.geyserLightning?.();}}
  if(T.wave<4&&T.shot<=0){sa14Balls(b,mode==='sa14-ice');T.shot=.82;
   A.glow=0;R.warnings=[];T.thunder=.3;
   if(mode==='sa14-ice')T.moveTo=Math.min(camRightX()-b.w*.32,b.x+20+vp12Tier()*3);
  }
 }else if(T.shot<=0){
  if(mode==='sa14-mg'){const slot=T.wave++%2?'R':'L';sa14Slug(b,slot,T.aim,(T.wave%5-2)*.025);T.shot=c.mg+(T.wave%12===0?.32:0);}
  else if(mode==='sa14-rockets'&&T.wave<c.waves){sa14Missiles(b,T.aim);T.wave++;T.shot=c.gap;}
 }b._drawY=b.y;if(R.t>=R.dur)er26Set(b,'recover');return true;
}
function sa14Overflight(b,dt){const R=b._er26,A=sa14State(b),T=R._sa14,t=R.t,top=PLAY.y+135,bottom=PLAY.y+PLAY.h+190;
 const ease=k=>{k=clamp(k,0,1);return k*k*(3-2*k);};R.warnings=[];
 if(t<1.3){A.angle=0;A.scale=1;A.depth=false;T.aim.x=player.x;sa14Warning(b,{x:b.x,y:b.y},{x:T.aim.x,y:bottom},b.w*.55,t/1.3);sa14Rev(b,t/1.3,dt);}
 else if(t<2.3){if(!T.released){T.released=true;T.exitX=clamp(T.aim.x,camLeftX()+90,camRightX()-90);sa14Stop(b);Audio.SFX.chargeDash?.();}
  b.x=lerp(T.from.x,T.exitX,ease((t-1.3)));b.y=lerp(T.from.y,bottom,ease(t-1.3));A.depth=b.y>VH+b.h*.3;
 }else if(t<2.8){b.y=bottom;A.depth=true;}
 else if(t<4.8){const u=ease((t-2.8)/2);A.angle=Math.PI;A.scale=lerp(2.05,1,u);A.depth=true;
  b.x=lerp(T.exitX,camLeftX()+viewW()*.5,u);b.y=lerp(bottom,top,u);
  sa14Rumble(b,.38,dt);
 }else{A.angle=Math.PI;A.scale=1;A.depth=false;b.y=top-(t-4.8)*9;
  b.x+=clamp(camLeftX()+viewW()*.5-b.x,-45*dt,45*dt);T.shot-=dt;
  if(T.shot<=0){sa14Balls(b,false,true);T.shot=sa14Cfg().gap*2.15;}
 }b._drawY=b.y;b._noHit=A.depth;b._s4Airborne=A.depth;
 if(t>=R.dur){sa14Log('pursuit-complete',b);er26Set(b,'recover');}return true;
}
er26Combat=function(b,dt){if(sa14Owns(b)&&b._er26.mode.startsWith('sa14-'))return sa14Attack(b,dt);
 return SA14.base.combat.apply(this,arguments);};
er26WarTick=function(b,dt){if(!sa14Owns(b)||!['olivewarden','stormsovereign'].includes(b?._ship))return SA14.base.war.apply(this,arguments);
 const A=sa14State(b),R=b._er26,S=b._s4war;A.lockCd=Math.max(0,A.lockCd-dt);
 if(!S.mini){stage4ShieldTick(b,dt);stage4ShieldSyncNodes(b);
  if(S.shield.rearming){sa14Stop(b);R.warnings=[];A.glow=.5;b.x+=clamp(er26Station(b,0)-b.x,-100*dt,100*dt);b.y+=clamp(R.home-b.y,-100*dt,100*dt);b._drawY=b.y;stage4ShieldSyncNodes(b);R.wasRearming=true;return true;}
  if(R.wasRearming){R.wasRearming=false;er26Set(b,'recover');}
  if(S._pt11Chase&&!S._pt11Chase.done){S._pt11Chase.done=true;er26Set(b,'sa14-overflight');}
  if(A.lockCd<=0&&sa14Upper()&&(mr27CanFire(b,'ROCKET_L')||mr27CanFire(b,'ROCKET_R'))&&!['sa14-lock','sa14-drive','sa14-overflight'].includes(R.mode))er26Set(b,'sa14-lock');
 }else sa14Escorts(b,dt);
 if(R.mode==='recover'){A.depth=false;b._noHit=false;b._s4Airborne=false;A.angle=(A.fromAngle||0)*(1-clamp(R.t/R.dur,0,1));A.scale=1;R.warnings=[];
  er26Move(b,R,R.t/R.dur);if(R.t>=R.dur)er26Next(b);
 }else if(!R.mode.startsWith('sa14-'))er26Set(b,'recover');else sa14Attack(b,dt);
 if(!S.mini){stage4ShieldSyncNodes(b);for(const d of S.coreTurrets){if(d.dead)continue;const p=stage4CoreTurretTarget(b,d.side);
  d.x=p.x;d.y=p.y;d.spawnT+=dt;d.materialize=clamp(d.spawnT/.8,0,1);d.state='overheat';d.vulnerable=true;d.spin=(d.spin+dt*9)%8;d.flash=Math.max(0,d.flash-dt);
 }}return true;
};
er26Tick=function(b,dt){if(sa14Owns(b)){sa14State(b).age+=dt;sa14Freeze(b);b._l23Beam=null;}
 const r=SA14.base.tick.apply(this,arguments);if(sa14Storm(b)){b._drawY=b.y;stage4ShieldSyncNodes(b);}return r;};
// South-origin escorts own their movement and real MG shots, without a hidden
// second cannon controller. The renderer uses the actual authored camo bank.
function sa14Escorts(b,dt){const A=sa14State(b);A.escortCd-=dt;if(A.escortCd>0||b.dead)return;
 const live=enemies.filter(e=>e._sa14Escort?.owner===b&&!e.dead&&e._dyingT==null),limit=diffKey==='easy'?2:vp12Tier()+2;
 if(live.length<limit)for(const side of [-1,1]){
  if(live.length>=limit)break;const e=spawnEnemy('drone',camLeftX()+viewW()*(side<0?.22:.78),VH+65,{pattern:'sa14-escort',shoots:false,hp:Math.max(8,vp12FamilyHealth(4).hp),w:64});
  if(!e)continue;delete e._cn;e.shoots=false;e._mini=true;e._noSep=true;e._bodShadow=true;e.w=e.h=64;
  e._sa14Escort={owner:b,t:0,side,scale:1.95,angle:-Math.PI/2,shot:.3,shots:0,serial:SA14.serial++};live.push(e);
 }A.escortCd=[9,7,6,5][vp12Tier()];A.escortWave++;sa14Log('south-escorts',b,{count:live.length});}
function sa14EscortTick(e,dt){const A=e._sa14Escort;if(!A)return;if(A.owner.dead||A.owner.dying||run.stage!==4){e.dead=true;return;}
 A.t+=dt;const t=A.t,L=camLeftX(),W=viewW();A.scale=lerp(1.95,1,clamp(t/1.6,0,1));
 const x=L+W*(A.side<0?.22:.78)+A.side*Math.sin(t*2.0)*W*.18,y=t<1.6?lerp(VH+65,PLAY.y+PLAY.h*.34,t/1.6):PLAY.y+PLAY.h*.34+Math.sin((t-1.6)*1.7)*PLAY.h*.20;
 if(t<1.6)A.angle=Math.atan2(y-e.y,x-e.x);
 else{const target=targetShip(x,y),wanted=Math.atan2(target.y-y,target.x-x);A.angle+=clamp(stage4AngleDelta(A.angle,wanted),-5*dt,5*dt);}
 e.x=x;e.y=y;e._noHit=t<1.6;e.fireCd=999;e.vx=e.vy=0;
 if(t>1.7&&t<7.5){A.shot-=dt;if(A.shot<=0){const target=targetShip(e.x,e.y),a=Math.atan2(target.y-e.y,target.x-e.x),p={x:e.x+Math.cos(a)*24,y:e.y+Math.sin(a)*24};
  if(Math.abs(stage4AngleDelta(A.angle,a))>.7)return;
  const q=eShootT(p.x,p.y,a,4.8+vp12Tier()*.25,'mg',{w:6,h:14,silent:true});Object.assign(q,{_sa14EscortShot:true,_sa14EscortOwner:e,mg:true,_weaponProof:true,_shootable:false});
  A.shots++;A.shot=A.shots%6===0?.65:sa14Cfg().mg;Audio.SFX.machineGun?.();
 }}if(t>7.5){e.y-=Math.min(1,(t-7.5)/1.4)*220;A.angle=-Math.PI/2;}if(t>9)e.dead=true;
}
updatePlay=function(dt){sa14YuriSync();for(const e of enemies)if(e._sa14Escort&&!e.dead&&e._dyingT==null)sa14EscortTick(e,dt);
 const r=SA14.base.update.apply(this,arguments);for(const b of [boss,subBoss])if(b?._sa14&&(b.dead||b.dying))sa14Stop(b);return r;};
drawEnemy=function(e){if(!e._sa14Escort){const flash=e.flash;if(e._vp12)e.flash=0;
 try{return SA14.base.enemy.apply(this,arguments);}finally{e.flash=flash;}}
 if(e.dead)return;
 const A=e._sa14Escort,p=air13Pose('flight_variant_4','heading',A.angle);if(!p)return;
 drawUnitShadow(e.x,e.y+18,64*A.scale,64*A.scale,.34,e);air13Blit(p,e.x,e.y,64*A.scale*p.d.referenceRatio,1,null);
 e._air13RenderedKey=p.key;e._air13Frame=p.f;
};
air13DrawFlight=function(e){const flash=e.flash;if(e._vp12)e.flash=0;
 try{return SA14.base.flight.apply(this,arguments);}finally{e.flash=flash;}};
mr27Blit=function(skin,cell,p,flash,form,owner){
 const A=owner?._sa14,r=SA14.base.blit.call(this,skin,cell,p,owner?._ship==='olivewarden'?0:flash,form,owner);
 if(r&&A&&A.glow>.50){const color=Math.floor(A.age*22)%2?'#83d9ff':'#ffffff',im=mr27Cell(skin,cell,color);
  if(im){ctx.save();ctx.globalAlpha=(A.glow-.50)*.95;ctx.translate(p.x,p.y);ctx.rotate(p.rot||0);ctx.drawImage(im,-p.w/2,-p.h/2,p.w,p.h);ctx.restore();}}
 return r;
};
mr27Draw=function(b){if(!sa14Storm(b))return SA14.base.draw.apply(this,arguments);mr27Init(b);const M=b._mr27;
 if(!XART.rdy('mr27_'+M.skin))return false;const A=sa14State(b),shape=MR27_ART[M.skin].cells[0],k=Math.min(b.w/shape[2],b.h/shape[3])*A.scale;
 if(A.depth){const im=mr27Cell(M.skin,0,'#050713');if(im){ctx.save();ctx.globalAlpha=.35;ctx.translate(b.x+10,b.y+25);ctx.rotate(A.angle);ctx.drawImage(im,-shape[2]*k*.42,-shape[3]*k*.42,shape[2]*k*.84,shape[3]*k*.84);ctx.restore();}}
 mr27Blit(M.skin,0,{x:b.x,y:b.y,w:shape[2]*k,h:shape[3]*k,rot:A.angle},b.flash,null,b);
 for(const part of M.parts)if(!part.dead){const p=mr27Shape(b,part.id);mr27Blit(M.skin,p.cell,p,Math.max(part.flash,b.flash||0),null,b);}
 mr27CoreDraw(b,mr27Shape(b,'core'));mr27Over(b);sa14Draw(b);shipBossMuzzleDraw(b);M.draws++;return true;
};
mr27Over=function(b){if(!sa14Storm(b)||!b._sa14)return SA14.base.over.apply(this,arguments);
 const H=b._s4war.shield,A=b._sa14;stage4ShieldSyncNodes(b);
 if(H&&(H.active||H.rearming)){for(const n of H.nodes)if(!n.dead){mr27Blit('storm',5,{x:n.x,y:n.y,w:54*A.scale,h:54*A.scale,rot:A.angle},n.flash,null,b);
  mr27CoreDraw(b,{x:n.x,y:n.y,w:15*A.scale,h:34*A.scale,rot:(n.spin||0)/16*TAU});
  av3Beam(ctx,n.x,n.y,Math.atan2(b.y-n.y,b.x-n.x),Math.hypot(b.x-n.x,b.y-n.y),7,'lightning',b._mr27.clock,.65,false);
 }}if(!A.depth)for(const d of b._s4war.coreTurrets)if(!d.dead&&d.materialize>.1)mr27HelperDraw(b,d);
};
function sa14BlueArc(x,y,angle,length,clock,alpha){if(!XART.rdy('cfx_stage4_chain_lightning'))return;
 const im=XART.get('cfx_stage4_chain_lightning'),f=Math.floor(clock*18)%8,w=length*256/384;
 ctx.save();ctx.translate(x,y);ctx.rotate(angle-Math.PI/2);ctx.globalCompositeOperation='lighter';ctx.globalAlpha=alpha;
 ctx.drawImage(im,(f%4)*256,Math.floor(f/4)*384,256,384,-w/2,0,w,length);ctx.restore();
}
function sa14Draw(b){const R=b._er26,A=b._sa14;if(!A||b.dead||b.enter)return;
 if(R.mode.startsWith('sa14-')){
  for(const w of R.warnings){const p={x:w.x,y:w.y};combatWarningDraw(b,{...p,ex:p.x+Math.cos(w.angle)*VH,ey:p.y+Math.sin(w.angle)*VH,
   width:w.width,progress:w.progress,fieldOnly:true});}
  if(R.warnings.length)combatWarningDraw(b,{x:b.x,y:b.y,ex:b.x,ey:VH,width:1,progress:R.warnings[0].progress,alertOnly:true,
   alertX:b.x,alertY:Math.max(PLAY.y+24,b.y-b.h*.46-22)});
 }
 if(A.glow>.02){const p=shipBossMount(b,'C'),t=R.clock;
  for(let i=0;i<4;i++){const angle=t*1.5+i*TAU/4;sa14BlueArc(p.x,p.y,angle,50+A.glow*85,t+i*.13,.4+A.glow*.4);}
  const key='s4w_lightning_ball_'+Math.floor(t*18)%16;if(XART.rdy(key)){const size=24+A.glow*42;ctx.save();ctx.globalCompositeOperation='lighter';ctx.drawImage(XART.get(key),p.x-size/2,p.y-size/2,size,size);ctx.restore();}
 }
 if(R.mode==='sa14-lock'&&R.t<R.warm){const T=R._sa14,k=clamp(R.t/R.warm,0,1),orbit=R.t<R.warm-.4?(1-k)*22:0;
  const x=T.aim.x+Math.cos(R.t*TAU*1.4)*orbit,y=T.aim.y+Math.sin(R.t*TAU*1.4)*orbit;
  ph8Icon(ctx,(orbit?'retm_':'retmb_')+Math.floor(R.t*16)%4,x,y,56);
  for(const id of ['rocketL','rocketR']){const p=mr27Part(b,id);if(p&&!p.dead){const q=mr27Shape(b,id);av3Muzzle(ctx,q.x+Math.sin(R.t*55)*2,q.y,24+k*16,'mg',R.t);}}
 }
}
const SA14_ER_DRAW=er26Draw;
er26Draw=function(b){const r=SA14_ER_DRAW.apply(this,arguments);if(sa14Owns(b)&&!sa14Storm(b))sa14Draw(b);return r;};
drawBG=function(){const r=SA14.base.bg.apply(this,arguments),b=sa14Owns(boss)&&bossActive?boss:sa14Owns(subBoss)&&subBossActive?subBoss:null,A=b?._sa14;
 if(A&&A.glow>.02&&!b.dead){ctx.save();ctx.fillStyle='rgba(1,4,17,'+(A.glow*.72)+')';ctx.fillRect(camLeftX()-40,viewFillY(),viewW()+80,viewFillH());ctx.restore();}return r;};
window.BOF_STAGE34_ASSAULT={stats:SA14,config:sa14Cfg,attack:sa14Attack};
const SA14_OVERFLIGHT_DRAW=stage4OverflightDraw;
stage4OverflightDraw=function(){if(sa14Storm(boss)&&!boss.dead&&boss._sa14?.depth)return mr27Draw(boss);
 return SA14_OVERFLIGHT_DRAW.apply(this,arguments);};
const SA14_FLIGHT_TIMING=vp12FireTiming;
vp12FireTiming=function(g,q){if(g.type==='peel-bomb')return{tell:.75,release:1.95+q.slot*.34,gap:.55};
 return SA14_FLIGHT_TIMING.apply(this,arguments);};
