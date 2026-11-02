"use strict";
/* Stage5 orbital roles. Whole authored direction cells; native hull damage,
   absorbing shields, Retina missiles, dodge/contact and death ownership. */
const S511={base:{spawn:spawnEnemy,tick:s5SpaceTick,draw:drawEnemy,attach:r46Attach,model:r46Model,
 beginAI:ai27Begin,endAI:ai27End,entry:enemyEntrySweep,frenzy:enemyFrenzyTick,
 shot:ovSonicProjectileDraw,finalShot:drawCombatFinalProjectile,intercept:enemyOrdnanceCanIntercept,
 effects:updateEffects,flashes:drawNavalFlashes,play:updatePlay,kill:killEnemy,load:stageLoadBegin,begin:beginStage},
 serial:0,events:[],fx:[],mines:new Set(),types:new Set(['s5frigate','s5rammer','s5skimmer','s5gravity','s5minelayer','s5satellite','s5portalmine','s5repair','s5station','s5leech'])};
for(const B of [...Object.values(S511_ART.banks),...Object.values(S511_ART.models).map(m=>m.bank)])XART._src[B.key]=B.path;
function s511Own(e){return !!e?._s511;}
function s511Live(e){return !!e&&!e.dead&&e.hp>0&&e._dyingT==null;}
function s511M(e){return S511_ART.models[e._s511.model];}
function s511Log(e,event,data={}){S511.events.push({id:e?._s511?.id,type:e?.type,event,t:efxClock,...data});if(S511.events.length>1800)S511.events.shift();}
r46Attach=function(e){if(S511.types.has(e?.type))return;return S511.base.attach.apply(this,arguments);};
r46Model=function(e){return s511Own(e)?null:S511.base.model.apply(this,arguments);};
// Retired everywhere, including adaptive aces and direct preview requests.
for(const list of Object.values(DIFFICULTY_ELITE_STAGE))if(Array.isArray(list)){let i;while((i=list.indexOf('voidreaver'))>=0)list.splice(i,1);}
spawnEnemy=function(type,x,y,opt={}){
 if(type==='xelite_voidreaver'||type==='voidreaver')return null;
 const e=S511.base.spawn.apply(this,arguments);if(!e||run.stage!==5||!S511.types.has(e.type))return e;
 const model=e.type.slice(2),m=S511_ART.models[model];
 for(const k of ['_r46','_ai','_air17','_ep13','_vp12','_s5Act','_jetManeuver','_entrySweep','_af10Jet','_ac10Ram','_modJet','_r30'])delete e[k];
 e._s511={id:++S511.serial,model,phase:'entry',t:0,age:0,cd:.7,head:Math.PI/2,round:0,beat:0,beams:[],lanes:[],home:clamp(e.x,camLeftX()+95,camRightX()-95),side:e._side|| (e.x<worldWidth()/2?1:-1)};
 e._s5space=e.type;e.pattern='s5space';e._frFlight=false;e._noSep=true;e.shoots=e.armed=false;e.fireCd=e._fcd=999;e.fk=null;e.spin=0;
 if(model==='repair'){e._s511.head=e._s511.side>0?0:Math.PI;e.x=e._s511.side>0?camLeftX()-90:camRightX()+90;e.y=PLAY.y+95;}
 if(model==='repair'){const mul=DR15.keys.includes(diffKey)?1:[1,1.65,2.15][ai27Level()];e.hp*=mul;e._maxhp=e.maxhp=e.hp;}
 if(model==='station'){delete e._esh;enemyShieldEquip(e,'bubble_volt',EHP(38),{once:true,drawScale:1.48});}
 e._drawW=e._drawH=m.spanWorld;e._s511.hullHP=e.hp;s511Log(e,'spawn',{hp:e.hp,shield:e._esh?.max||0});return e;
};
enemyEntrySweep=function(e){if(s511Own(e))return;return S511.base.entry.apply(this,arguments);};
enemyFrenzyTick=function(e){if(s511Own(e))return;return S511.base.frenzy.apply(this,arguments);};
ai27End=function(e,old){if(s511Own(e)&&e._ai27)e._ai27.dx=0;return S511.base.endAI.apply(this,arguments);};
function s511Angle(e){const B=s511M(e).bank;return Math.PI/2+s1aDir(e._dyingT!=null?Math.PI/2+(e.spin||0):e._s511.head,B.dirs)*TAU/B.dirs;}
function s511Point(e,name='centre'){
 const m=s511M(e),B=m.bank,p=m.sockets[name]||m.sockets.centre||[64,64],mid=m.reuse?64:B.cell/2,
 k=m.spanWorld/m.sourceSpan,a=s511Angle(e)-Math.PI/2,c=Math.cos(a),s=Math.sin(a),x=(p[0]-mid)*k,y=(p[1]-mid)*k;
 return{x:e.x+x*c-y*s,y:e.y+x*s+y*c,angle:s511Angle(e)};
}
function s511Phase(e,phase){Object.assign(e._s511,{phase,t:0,round:0,beat:0});s511Log(e,phase);}
function s511Fly(e,x,y,sp,turn,dt){const A=e._s511,want=Math.atan2(y-e.y,x-e.x);A.head+=clamp(s1aAngle(want-A.head),-turn*dt,turn*dt);e.x+=Math.cos(A.head)*sp*dt;e.y+=Math.sin(A.head)*sp*dt;e.spin=A.head-Math.PI/2;}
function s511Flash(e,p,size=30){S511.fx.push({owner:e,p:{...p},origin:{x:e.x,y:e.y},t:0,life:.12,size});}
function s511Shot(e,p,kind,speed=3.5,silent=false){
 if(!s511Live(e))return null;const missile=kind==='missile',mine=kind==='mine',orb=kind==='orb';
 const b=eShootT(p.x,p.y,p.angle,speed,missile?'emissile':mine?'s5split':kind==='laser'?'s5prism':orb?'s5split':'s5fracture',{owner:e,noMuzzle:true,silent:true,w:mine?18:orb?16:9,h:mine?18:orb?16:24});
 if(!b||b.dead||b._ai27Held)return null;
 Object.assign(b,{_s511Kind:kind,_s511Owner:e,_noArsenal:true,_weaponProof:!(mine||missile||orb),_shootable:mine||missile||orb,_energyOrdnance:!missile,homing:false});
 if(missile){b.hp=2;b.spd=speed;b.turn=.075;b.life=8;}
 if(orb){b.hp=3;b.life=7;}
 if(mine){b.hp=3;b.vx=b.vy=b.spd=0;b.life=8;b._wardenAnchor={x:p.x,y:p.y,life:8};b._wardenAnchored=true;S511.mines.add(b);}
 if(!silent){if(missile)Audio.SFX.enemyMissile?.();else if(mine)Audio.SFX.bombDrop?.();else if(orb)Audio.SFX.magmaOrb?.();else Audio.SFX.enemyPulseLaserAlien?.();}
 if(!mine)s511Flash(e,p,orb?38:26);e._s511.lastShot=e._s511.age;s511Log(e,'shot',{kind,x:p.x,y:p.y,a:p.angle});return b;
}
enemyOrdnanceCanIntercept=function(b){return b?._s511Kind?['mine','orb','missile'].includes(b._s511Kind):S511.base.intercept.apply(this,arguments);};
function s511Tell(e,lanes,duration,phase='tell'){s511Phase(e,phase);e._s511.lanes=lanes;e._s511.warm=duration;Audio.SFX.bossWeaponCharge?.();}
function s511Lane(e,name,width=24,angle=null){const p=s511Point(e,name);return{...p,angle:angle??p.angle,width};}
function s511Beam(e,lanes,duration){const A=e._s511;s511Phase(e,'beam');A.lanes=[];A.beams=lanes.map(p=>({p:{...p},t:0,life:duration}));Audio.SFX.enemyHeavyLaser?.();s511Log(e,'beam-release',{lanes:lanes.map(p=>({...p}))});}
function s511BeamTick(e,dt){const A=e._s511;for(const b of A.beams){b.t+=dt;for(const seat of seatList())withSeat(seat,()=>{
  if(!player.dead&&!player.out&&player.invuln<=0&&ep13BeamTouches({x:b.p.x,y:b.p.y,a:b.p.angle,width:b.p.width,len:1200,active:b.t>.08&&b.t<b.life-.1},player))playerHit();});}
 A.beams=A.beams.filter(b=>b.t<b.life);
}
function s511Ready(e){return e._ai27?.visible&&e._ai27.seen>.5&&e.y>PLAY.y+24;}
s5SpaceTick=function(e,dt){if(!s511Own(e))return S511.base.tick.apply(this,arguments);if(!s511Live(e))return;
 if(e._stagger>0){e._stagger=Math.max(0,e._stagger-dt);return;}
 const A=e._s511,K=A.model,r=ai27Level(),T=targetShip(e.x,e.y);A.age+=dt;A.t+=dt;A.cd-=dt;A.beat-=dt;e._s5Act=null;e.shoots=e.armed=false;e.fireCd=e._fcd=999;
 if(e._shieldStun>0||e._frozen||e._mercuryLock>0){A.beams=[];A.lanes=[];if(['tell','beam','fire','lock'].includes(A.phase))s511Phase(e,'recover');return;}
 s511BeamTick(e,dt);
 if(K==='rammer'){
  if(A.phase==='entry'){e.y+=[115,185,240][r]*dt;if(e.y>PLAY.y+100){A.head=Math.atan2(T.y-e.y,T.x-e.x);s511Tell(e,[s511Lane(e,'centre',30)],[.64,.42,.30][r]);}}
  else if(A.phase==='tell'){combatWarningTick(e,'s511-ram',A.t,A.warm);if(A.t>=A.warm){A.lanes=[];s511Phase(e,'ram');Audio.SFX.jetDash?.();}}
  else if(A.phase==='ram'){const sp=[440,650,850][r];e.x+=Math.cos(A.head)*sp*dt;e.y+=Math.sin(A.head)*sp*dt;}
 }else if(K==='skimmer'){
  if(A.phase==='entry'){s511Fly(e,A.home,PLAY.y+110,205,3.4,dt);if(s511Ready(e)&&e.y>PLAY.y+90)s511Phase(e,'pass');}
  else if(A.phase==='pass'){
   // 1101 (Mike: fire more often): the weave alone rarely lined the nose up (one pair per ~6.6 s), so every
   // 1.5/1.25/1.0 s it banks onto the pilot for a 0.7 s strafe. It still only fires while actually facing them.
   A.strafe=(A.strafe??1.0)-dt;const strafing=A.strafe<=0;if(A.strafe<=-.7)A.strafe=[1.5,1.25,1.0][r];
   const tx=clamp(A.home+Math.sin(A.t*1.35)*175*A.side,camLeftX()+70,camRightX()-70),ty=PLAY.y+170+Math.sin(A.t*1.8)*65;
   // Strafe: the nose swings onto the pilot while the hull keeps drifting along its weave line (no closing ram).
   if(strafing){const k=Math.min(1,dt*1.6),want=Math.atan2(T.y-e.y,T.x-e.x);A.head+=clamp(s1aAngle(want-A.head),-4.2*dt,4.2*dt);e.x+=(tx-e.x)*k;e.y+=(ty-e.y)*k;e.spin=A.head-Math.PI/2;}
   else s511Fly(e,tx,ty,160,3.0,dt);
   // Nose and both fixed guns actually face the pilot before release.
   const aim=Math.atan2(T.y-e.y,T.x-e.x);if(A.cd<=0&&Math.abs(s1aAngle(aim-s511Angle(e)))<.65){for(const name of['port','starboard'])s511Shot(e,s511Point(e,name),'slug',4.8,name==='starboard');A.cd=strafing?[.24,.20,.16][r]:[.55,.42,.30][r];}
   if(A.t>7)s511Phase(e,'exit');
  }else s511Fly(e,A.home-A.side*150,VH+210,300,2.5,dt);
 }else if(K==='minelayer'){
  if(A.phase==='entry'){s511Fly(e,A.home,PLAY.y+100,235,3,dt);if(s511Ready(e))s511Phase(e,'lay');}
  else if(A.phase==='lay'){s511Fly(e,A.home+Math.sin(A.t*1.25)*145,PLAY.y+155+A.t*48,170,2.8,dt);if(A.cd<=0){s511Shot(e,s511Point(e,'centre'),'mine',0);A.cd=turretInterval15(.62,[.62,.49,.39][r]);}if(A.t>3.4){s511Phase(e,'exit');Audio.SFX.jetDash?.();}}
  else s511Fly(e,A.home+A.side*400,-250,370,4.5,dt);
 }else if(K==='repair'){
  if(A.phase==='entry'){s511Fly(e,A.home,PLAY.y+100,220,5,dt);if(s511Ready(e)&&A.age>1.1)s511Phase(e,'turn');}
  else if(A.phase==='turn'){A.head+=clamp(s1aAngle(Math.PI/2-A.head),-5*dt,5*dt);e.y+=50*dt;if(Math.abs(s1aAngle(A.head-Math.PI/2))<.05){A.head=Math.PI/2;s511Tell(e,['port','starboard'].map(n=>s511Lane(e,n,20)),[.85,.73,.65][r]);}}
  else if(A.phase==='tell'){combatWarningTick(e,'s511-tips',A.t,A.warm);if(A.t>=A.warm){s511Beam(e,A.lanes,1.35);}}
  else if(A.phase==='beam'){e.y+=[90,120,145][r]*dt;A.beams.forEach((b,i)=>Object.assign(b.p,s511Point(e,i?'starboard':'port')));if(!A.beams.length)s511Phase(e,'exit');}
  else if(A.phase==='exit')e.y+=220*dt;
 }else if(K==='leech'){
  if(A.phase==='entry'){s511Fly(e,T.x,T.y,135,2.8,dt);if(s511Ready(e)&&Math.hypot(T.x-e.x,T.y-e.y)<270)s511Tell(e,[],.82,'open');}
  else if(A.phase==='open'){s511Fly(e,T.x,T.y,45,2,dt);if(A.t>A.warm){A.target={x:T.x,y:T.y};s511Phase(e,'pounce');Audio.SFX.jetDash?.();}}
  else if(A.phase==='pounce'){s511Fly(e,T.x,T.y,[210,260,310][r],2.5,dt);if(A.t>1.3)s511Phase(e,'recover');}
  else if(A.phase==='recover'){e.x-=Math.cos(A.head)*65*dt;e.y-=Math.sin(A.head)*65*dt;if(A.t>.8)s511Phase(e,'entry');}
  // Connected front claws own a real contact volume. Native playerHit owns dodge/death.
  if(A.phase==='pounce')for(const seat of seatList())withSeat(seat,()=>{const p=s511Point(e,'centre');if(!player.dead&&!player.out&&player.invuln<=0&&Math.hypot(player.x-p.x,player.y-p.y)<25){playerHit();s511Log(e,'claw-contact',{seat:seat.id});s511Phase(e,'recover');}});
 }else{
  if(A.phase==='entry'){e.y+=(K==='station'?75:95)*dt;if(e.y>=PLAY.y+(K==='station'?110:145))s511Phase(e,'wait');}
  if(K==='portalmine')A.head+=dt*2.1;
  if(A.phase==='wait'&&A.cd<=0&&s511Ready(e)){
   if(K==='satellite'){
    s511Phase(e,'lock');for(let i=0;i<[2,3,4][r];i++)enemyLockOn(e,.95+i*.16,{fire:L=>{if(!s511Live(e))return;const p=s511Point(e,i%2?'starboard':'port'),b=s511Shot(e,p,'missile',3.5,i%2>0);if(b)s511Log(e,'missile-release',{lock:L.id,index:i});}});
   }else if(K==='frigate')s511Tell(e,[s511Lane(e,'centre',26)],[1.05,.95,.85][r]);
   else if(K==='station'){if((A.cycle||0)%3===2)s511Tell(e,[s511Lane(e,'centre',34)],[1.15,1.05,.95][r]);else{s511Tell(e,['port','starboard'].map(n=>s511Lane(e,n,34)),.72,'spread-tell');}}
   else{s511Tell(e,[],[1.0,.85,.75][r]);}
  }else if(A.phase==='lock'&&A.t>1.65){s511Phase(e,'recover');}
  else if(['tell','spread-tell'].includes(A.phase)){
   combatWarningTick(e,'s511-'+K,A.t,A.warm);
   if(A.t>=A.warm){
    if(K==='frigate'||K==='station'&&A.phase==='tell')s511Beam(e,A.lanes,K==='station'?1.55:1.2);
    else if(K==='station'){for(const name of['port','starboard']){const p=s511Point(e,name);for(let i=-1;i<=1;i++)s511Shot(e,{...p,angle:p.angle+i*.22},'laser',3.8,name==='starboard'||i!==-1);}s511Phase(e,'recover');A.cycle=(A.cycle||0)+1;}
    else{
     const n=K==='portalmine'?(r?9:6):(r?12:8),base=K==='portalmine'?s511Angle(e):A.age*.17;
     for(let i=0;i<n;i++){const angle=base+i*TAU/n,p={x:e.x+Math.cos(angle)*27,y:e.y+Math.sin(angle)*27,angle};if(!r&&K==='gravity'&&Math.abs(s1aAngle(angle-Math.PI/2))<.44)continue;s511Shot(e,p,K==='gravity'?'orb':'slug',K==='gravity'?2.1:2.9,i>0);}
     s511Log(e,'radial-release',{directions:n,kind:K==='gravity'?'orb':'slug'});s511Phase(e,'recover');
    }
   }
  }else if(A.phase==='beam'&&!A.beams.length){if(K==='station')A.cycle=(A.cycle||0)+1;s511Phase(e,'recover');}
  else if(A.phase==='recover'&&A.t>[1.0,.8,.6][r]){s511Phase(e,'wait');A.cd=turretInterval15(1.15,[1.15,.85,.65][r]);}
 }
 if(A.age>27||e.y>VH+140||e.x<camLeftX()-230||e.x>camRightX()+230||A.phase==='exit'&&e.y<-160){e.dead=true;A.beams=[];A.lanes=[];s511Log(e,'exit');}
};
function s511Draw(e){const A=e._s511,m=s511M(e),B=m.bank,a=s511Angle(e),size=m.spanWorld*B.cell/m.sourceSpan;let f=0;
 if(m.reuse){const row=m.bank.banks;f=A.phase==='beam'||efxClock-(A.lastShot??-999)<.24?row.attack.row+Math.floor(A.age*20)%row.attack.frames:row.idle.row;}
 else if(A.model==='minelayer'&&A.phase==='lay')f=Math.floor(A.age*18)%8;
 else if(A.model==='leech')f=A.phase==='open'?Math.min(7,Math.floor(A.t/.82*8)):A.phase==='pounce'?7+Math.min(5,Math.floor(A.t*6)):A.phase==='recover'?12+Math.min(3,Math.floor(A.t*5)):0;
 if(e._dyingT!=null)f=0;
 if(e._esh)drawEnemyShieldLayer(e,false);
 if(['skimmer','rammer','minelayer','repair'].includes(A.model)&&e._dyingT==null){for(const n of['exhaustPort','exhaustStarboard']){const p=s511Point(e,n);v31Blit(S511_ART.banks.thruster,Math.floor(A.age*24)%4,p.angle,p.x,p.y,34);}}
 if(m.reuse)r46Blit(B,f,a,e.x,e.y,size,e.flash>0?hitFlashColor(e):null);
 else v31Blit(B,f,a,e.x,e.y,size,e.flash>0?hitFlashColor(e):null);
 e._drawW=e._drawH=m.spanWorld;e._s511Rendered={key:B.key,frame:f,dir:s1aDir(a,B.dirs),size,phase:A.phase};
 if(e._esh){drawEnemyShieldLayer(e,true);bet24Bar?.(e);}
 if(s511Live(e)){
  for(const p of A.lanes)if(['tell','spread-tell'].includes(A.phase))combatWarningDraw(e,{...p,ex:p.x+Math.cos(p.angle)*1200,ey:p.y+Math.sin(p.angle)*1200,len:1200,progress:clamp(A.t/A.warm,0,1),width:p.width,fieldOnly:true});
  // Source beam alpha occupies18/64px across and50/64px along. Its complete
  // visible width is the same width used for FOV and contact; no invisible skirt.
  for(const b of A.beams){const p=b.p,size=p.width*64/18,step=size*48/64;for(let d=size*28/64;d<1200;d+=step){const x=p.x+Math.cos(p.angle)*d,y=p.y+Math.sin(p.angle)*d;if(x<camLeftX()-60||x>camRightX()+60||y<PLAY.y-60||y>VH+60)continue;v31Blit(S511_ART.banks.laser,Math.floor(b.t*24)%4,p.angle,x,y,size);}}
 }
}
drawEnemy=function(e){if(s511Own(e)&&!e.dead)return s511Draw(e);return S511.base.draw.apply(this,arguments);};
function s511Projectile(b){const k=b._s511Kind,B=S511_ART.banks[k==='missile'?'thunder_missile':k==='slug'?'laser':k],size=k==='mine'?38:k==='orb'?34:k==='missile'?42:38,age=projectileVisualAge(b),f=Math.floor(age*22)%B.frames,a=Math.atan2(b.vy,b.vx),r=v31Blit(B,f,a,b.x,b.y,size);
 if(k==='orb'){ctx.save();ctx.globalCompositeOperation='lighter';v31Blit(S511_ART.banks.orb_glow,f,a,b.x,b.y,size,null,pxgStep(.5+.5*Math.sin(age*9)));ctx.restore();}return r;}
ovSonicProjectileDraw=function(b){return b?._s511Kind?s511Projectile(b):S511.base.shot.apply(this,arguments);};
drawCombatFinalProjectile=function(b){return b?._s511Kind?s511Projectile(b):S511.base.finalShot.apply(this,arguments);};
updateEffects=function(dt){const r=S511.base.effects.apply(this,arguments);for(const f of S511.fx)f.t+=dt;S511.fx=S511.fx.filter(f=>f.t<f.life&&s511Live(f.owner));return r;};
drawNavalFlashes=function(){const r=S511.base.flashes.apply(this,arguments);for(const f of S511.fx)v31Blit(S511_ART.banks.muzzle,Math.floor(f.t/f.life*4),f.p.angle,f.p.x+f.owner.x-f.origin.x,f.p.y+f.owner.y-f.origin.y,f.size);return r;};
updatePlay=function(dt){const r=S511.base.play.apply(this,arguments);if(run.stage!==5)return r;
 for(const b of S511.mines){
  if(!b.dead&&b.t>.6){for(const s of seatList())withSeat(s,()=>{if(!player.dead&&!player.out&&Math.hypot(player.x-b.x,player.y-b.y)<45){b._s511Detonate=true;b.dead=true;}});}
  if(b.dead||!eBullets.includes(b)){if(b._s511Detonate){explode(b.x,b.y,90,'purple','electric');Audio.SFX.expBig?.();for(const s of seatList())withSeat(s,()=>{if(!player.dead&&!player.out&&player.invuln<=0&&Math.hypot(player.x-b.x,player.y-b.y)<65)playerHit();});s511Log(b._s511Owner,'mine-detonated',{x:b.x,y:b.y});}else if(b.t<7.8)s511Log(b._s511Owner,'mine-intercepted',{x:b.x,y:b.y});S511.mines.delete(b);}
 }return r;};
killEnemy=function(e){const r=S511.base.kill.apply(this,arguments);if(s511Own(e)&&!s511Live(e)){e._s511.beams=[];e._s511.lanes=[];playerLocks=playerLocks.filter(L=>L.src!==e);S511.fx=S511.fx.filter(f=>f.owner!==e);s511Log(e,'destroyed');}return r;};
stageLoadBegin=function(n,keys){if(n===5)keys=[...(keys||[]),...Object.values(S511_ART.banks).map(b=>b.key),...Object.values(S511_ART.models).map(m=>m.bank.key),...['green','yellow','red'].map(c=>'bmfx_fov_'+c+'_tall')];return S511.base.load.call(this,n,keys);};
beginStage=function(){S511.events=[];S511.fx=[];S511.mines.clear();return S511.base.begin.apply(this,arguments);};
globalThis.BOF_ORBITAL_REFIT={state:S511,art:S511_ART};
