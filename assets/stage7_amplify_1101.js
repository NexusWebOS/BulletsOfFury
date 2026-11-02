"use strict";
/* Stage7 regular roster only. Registered source hulls + articulated modules,
   real mouth/gun sockets, native absorbing shield/HP/flash/death ownership. */
const S711={base:{spawn:spawnEnemy,draw:drawEnemy,entry:enemyEntrySweep,frenzy:enemyFrenzyTick,
 beginAI:ai27Begin,endAI:ai27End,route:eb11OwnsRoute,kill:killEnemy,load:stageLoadBegin,begin:beginStage,
 early:ovSonicProjectileDraw,final:drawCombatFinalProjectile,intercept:enemyOrdnanceCanIntercept,
 effects:updateEffects,flashes:drawNavalFlashes,model:r46Model,shield:drawEnemyShieldLayer,lock:enemyLockOn},
 serial:0,events:[],fx:[],models:{s7pipe:'crawler',s7tank:'tank',ll18brood:'brood',cp22relay:'relay',cp22slime:'slime',s7missilejet:'missilejet',s7barge:'barge',s8crescent:'crescent'},
 retired:new Set(['ll18raptor','blacksteel_hunter','xelite_blacksteelhunter'])};
for(const B of Object.values(S711_ART.banks))XART._src[B.key]=B.path;
function s711Live(e){return !!e&&!e.dead&&e.hp>0&&e._dyingT==null;}
function s711M(e){return S711_ART.models[e?._s711?.model];}
function s711Log(e,event,data={}){S711.events.push({id:e?._s711?.id,type:e?.type,event,t:efxClock,...data});if(S711.events.length>1800)S711.events.shift();}
function s711Rank(){return diffKey==='furious'||diffKey==='insanity'?2:diffKey==='hard'?1:0;}
function s711Angle(a,dirs=32){return Math.PI/2+v31Dir(a,dirs)*TAU/dirs;}
function s711Point(e,p,a=null){const M=s711M(e),A=e._s711,k=(M?.spanWorld||94)/256,head=s711Angle(a??A.head),rot=head-Math.PI/2,x=(p[0]-128)*k,y=(p[1]-128)*k;
 return{x:e.x+x*Math.cos(rot)-y*Math.sin(rot),y:e.y+x*Math.sin(rot)+y*Math.cos(rot),angle:head};}
function s711Part(e,i){const A=e._s711,M=s711M(e),m=M.modules[i],p=s711Point(e,m.mount),angle=s711Angle(A.angles[i]??A.head),rot=angle-Math.PI/2,k=M.spanWorld/256,recoil=efxClock-(A.fired[i]??-99)<.09?2:0;
 return{x:p.x-Math.cos(angle)*recoil,y:p.y-Math.sin(angle)*recoil,angle,tip:{x:p.x+(m.muzzle[0]*Math.cos(rot)-m.muzzle[1]*Math.sin(rot))*k-Math.cos(angle)*recoil,y:p.y+(m.muzzle[0]*Math.sin(rot)+m.muzzle[1]*Math.cos(rot))*k-Math.sin(angle)*recoil,angle}};}
function s711Phase(e,phase){Object.assign(e._s711,{phase,t:0,beat:0,round:0});s711Log(e,phase);}
function s711Fly(e,x,y,speed,turn,dt){const A=e._s711,want=Math.atan2(y-e.y,x-e.x);A.head+=clamp(s1aAngle(want-A.head),-turn*dt,turn*dt);e.x+=Math.cos(A.head)*speed*dt;e.y+=Math.sin(A.head)*speed*dt;}
function s711MountGuns(e,dt,track=false){const A=e._s711,M=s711M(e);if(!M)return;const T=targetShip(e.x,e.y);
 M.modules.forEach((m,i)=>{const p=s711Point(e,m.mount),want=track?clamp(s1aAngle(Math.atan2(T.y-p.y,T.x-p.x)-A.head),-.55,.55)+A.head:A.head;
  A.angles[i]=(A.angles[i]??A.head)+clamp(s1aAngle(want-(A.angles[i]??A.head)),-dt*2.4,dt*2.4);});}
function s711Attach(e,model){
 const ground=!!e._modTurret,M=S711_ART.models[model];
 // Remove inherited movers/launchers, preserving real actor/pool/death/traffic.
 for(const k of Object.keys(e))if(/^_(?:r46|r30|ll18|cp22Sewer|s7Act|s7Atk|modTank|modJet|toxicJet|esh|entrySweep|jetManeuver|air17|air13|ep13|ap10|frFlight|fury|s8|mm1003|mutator1003|enemyShield|cn$|dr$)/.test(k))delete e[k];
 e._s711={id:++S711.serial,model,phase:'entry',age:0,t:0,beat:0,round:0,cycles:0,head:Math.PI/2,angles:[],fired:[],rotor:0,home:clamp(e.x,camLeftX()+90,camRightX()-90),side:e.x<worldWidth()/2?1:-1};
 Object.assign(e,{pattern:'s7toxic',shoots:false,armed:false,fireCd:999,_fcd:999,fk:null,_atk:'none',spin:0,vx:0,vy:0,_frFlight:false,_noSep:true,_noHit:false});
 if(model==='brood')e.name='BROOD SENTINEL';if(model==='missilejet')e.name='TOXIC MISSILE JET';if(model==='crescent')e.name='CRESCENT ESCORT';
 if(M){e.art=M.bank.key;e._drawW=e._drawH=M.spanWorld;e.w=M.spanWorld*.78;e.h=M.spanWorld*.86;}
 if(model==='brood'||model==='barge'){enemyShieldEquip(e,'bubble_volt',Math.ceil((model==='brood'?58:46)*DIFF.eHp),{once:true,regen:.025});}
 if(model==='tank'||model==='crawler'){
  e.ground=true;e._groundTraffic=true;e._groundTrafficSize={w:M.spanWorld*(model==='crawler'?.82:.64),h:M.spanWorld*.96};
  if(model==='crawler')e.x=e.x<worldWidth()/2?worldWidth()*.17:worldWidth()*.83;
  groundTrafficPlaceEntry(e);e._s711.anchor={x:e.x,y:levelSrcY()+e.y};
 }
 if(ground){e._s711.model='ground';e._s711.weapon=e._modTurret.weapon;e._s711.head=e._modTurret.angle||Math.PI/2;e._s711.anchor={x:e._modTurret.mapX??e.x,y:e._modTurret.mapY??levelSrcY()+e.y};e.w=e.h=58;e._drawW=e._drawH=76;e.art=S711_ART.banks.ground_base.key;}
 e._s711.hullHP=e.hp;s711Log(e,'spawn',{model:e._s711.model,hp:e.hp,shield:e._esh?.max||0});return e;
}
spawnEnemy=function(type,x,y,opt={}){
 if(S711.retired.has(type))return null;
 // Replace that retired campaign beat with the requested second toxic jet.
 const requested=type==='s7missilejet',e=S711.base.spawn.call(this,requested?'cp22slime':type,x,y,opt);if(!e||run.stage!==7||e._boss||e.boss||e._amini||e._mini||e.prop||e._prop)return e;
 const model=requested?'missilejet':S711.models[e.type];if(requested){e.type='s7missilejet';e.hp=e.maxhp=e._maxhp=EHP(38);}
 if(model||e._modTurret?.stage===7)s711Attach(e,model||'ground');return e;
};
const S711_PLAN=buildStagePlan;buildStagePlan=function(n){const p=S711_PLAN.apply(this,arguments);if(n!==7)return p;
 return p.map(w=>w.t===28?{...w,fn:()=>spawnEnemy('s7missilejet',worldWidth()*.60,-155,{})}:w.t===20?{...w,fn:()=>spawnEnemy('s8crescent',worldWidth()*.5,-130,{})}:w);
};
r46Model=function(e){return e?._s711?null:S711.base.model.apply(this,arguments);};
enemyEntrySweep=function(e){if(!e?._s711)return S711.base.entry.apply(this,arguments);};
enemyFrenzyTick=function(e){if(!e?._s711)return S711.base.frenzy.apply(this,arguments);};
eb11OwnsRoute=function(e){return !!e?._s711||S711.base.route.apply(this,arguments);};
ai27Begin=function(e,dt){if(!e?._s711)return S711.base.beginAI.apply(this,arguments);const previous=ai27Context;ai27Context=null;return previous;};
ai27End=function(e,old){if(e?._s711){ai27Context=old;return;}return S711.base.endAI.apply(this,arguments);};
// Slug tanks have no inherited missile locks; native missiles retain their own.
enemyLockOn=function(e){if(e?._s711&&e._s711.model!=='missilejet')return null;return S711.base.lock.apply(this,arguments);};
drawEnemyShieldLayer=function(e){if(e?._s711)return;return S711.base.shield.apply(this,arguments);};
function s711Shot(e,p,kind='slug',speed=4.5,silent=false,index=0){
 if(!s711Live(e))return null;const missile=kind==='missile',fly=kind==='fly';
 const b=eShootT(p.x,p.y,p.angle,speed,missile?'emissile':fly?'s7bio':kind==='sonic'?'rzbSonic':kind==='laser'?'s7laser':'mg',{owner:e,noMuzzle:true,silent:true,w:fly?18:missile?12:kind==='sonic'?18:7,h:fly?18:missile?26:kind==='sonic'?18:19});
 if(!b||b.dead||b._ai27Held)return null;
 Object.assign(b,{_s711Kind:kind,_s711Owner:e,_noArsenal:true,_weaponProof:!missile,_shootable:missile,_energyOrdnance:!missile,homing:false});
 if(missile){b.hp=2;b.spd=speed;b.turn=.065;b.life=8;}
 if(fly){b.life=5.5;b._s711Steer=1.15;}
 e._s711.fired[index]=efxClock;S711.fx.push({e,p:{...p},from:{x:e.x,y:e.y},kind,index,t:0,life:.10,size:kind==='fly'?40:kind==='missile'?36:28});
 if(!silent)combatAudio0927(e,missile?'enemyMissile':fly?'combatToxic0927':kind==='laser'?'enemyHeavyLaser':kind==='sonic'?'combatEnergy0927':'enemyMachineGunLight',.075);
 s711Log(e,'shot',{kind,index,x:p.x,y:p.y,angle:p.angle,phase:e._s711.phase,cadence:e._s711.cadence});return b;
}
enemyOrdnanceCanIntercept=function(b){return b?._s711Kind?b._s711Kind==='missile':S711.base.intercept.apply(this,arguments);};
function s711Ready(e){return e.y>viewTopY()+45&&e.y<VH-70&&e.x>camLeftX()+22&&e.x<camRightX()-22;}
function s711Tell(e,kind,duration){s711Phase(e,kind);e._s711.warm=duration;combatAudio0927(e,'bossWeaponCharge',.5);}
function s711Ground(e,dt){const A=e._s711,r=s711Rank(),T=targetShip(e.x,e.y);e.y=A.anchor.y-levelSrcY();e.x=A.anchor.x;
 A.head+=clamp(s1aAngle(Math.atan2(T.y-e.y,T.x-e.x)-A.head),-dt*turretSpeed15(1.6),dt*turretSpeed15(1.6));e._modTurret.angle=A.head;
 if(!s711Ready(e))return;
 if(A.phase==='entry')s711Tell(e,'tell',A.weapon==='mg'?.65:.9);
 else if(A.phase==='tell'){combatWarningTick(e,'s711-ground',A.t,A.warm);if(A.t>A.warm)s711Phase(e,'fire');}
 else if(A.phase==='fire'){
  if(A.beat<=0){const a=s711Angle(A.head),k=94/256,rot=a-Math.PI/2,ps=A.weapon==='mg'?[[98,204],[160,204]]:[[128,218]];
   ps.forEach((p,i)=>s711Shot(e,{x:e.x+((p[0]-128)*Math.cos(rot)-(p[1]-128)*Math.sin(rot))*64/256,y:e.y+((p[0]-128)*Math.sin(rot)+(p[1]-128)*Math.cos(rot))*64/256,angle:a},A.weapon==='mg'?'slug':A.weapon,A.weapon==='mg'?5.2:4.4,i>0,i));A.beat=turretInterval15(.15,[.15,.12,.095][r]);A.round++;
   if(A.round>=(A.weapon==='mg'?[6,9,12][r]:A.weapon==='laser'?3:2))s711Phase(e,'recover');}
 }else if(A.phase==='recover'&&A.t>[1.45,1.12,.85][r])s711Tell(e,'tell',A.weapon==='mg'?.58:.85);
 if(e.y>VH+110)e.dead=true;
}
function s711Tank(e,dt){const A=e._s711,r=s711Rank(),M=s711M(e);e._lvlY=(e._lvlY??levelSrcY()+e.y)+18*dt;e.y=e._lvlY-levelSrcY();
 if(!s711Ready(e))return;if(A.phase==='entry')s711Phase(e,'fire');
 if(A.phase==='fire'&&A.beat<=0){const ps=A.model==='crawler'?M.mouths:M.guns;ps.forEach((p,i)=>s711Shot(e,s711Point(e,p),'slug',5.0,i>0,i));A.beat=turretInterval15(.18,[.18,.14,.105][r]);if(++A.round>=[6,9,12][r])s711Phase(e,'recover');}
 if(A.phase==='recover'&&A.t>[1.25,1.0,.8][r])s711Phase(e,'fire');
 if(e.y>VH+130)e.dead=true;
}
function s711Brood(e,dt){const A=e._s711,r=s711Rank(),M=s711M(e),T=targetShip(e.x,e.y);
 if(A.phase==='entry'){e.y+=82*dt;if(e.y>PLAY.y+125)s711Tell(e,'claw-tell',[1.12,1.0,.9][r]);}
 else if(A.phase==='claw-tell'){
  if(!A.target||A.t<A.warm*.55)A.target={x:T.x,y:T.y};s711MountGuns(e,dt);A.angles=[Math.PI/2-.42*Math.min(1,A.t/A.warm),Math.PI/2+.42*Math.min(1,A.t/A.warm)];combatWarningTick(e,'s711-claws',A.t,A.warm);
  if(A.t>=A.warm){A.start={x:e.x,y:e.y};A.end={x:clamp(A.target.x,camLeftX()+110,camRightX()-110),y:Math.min(A.target.y-85,PLAY.y+viewH()*.65)};s711Phase(e,'claw');combatAudio0927(e,'combatServo0927',.4);}
 }else if(A.phase==='claw'){
  const u=clamp(A.t/.44,0,1),v=Math.sin(Math.PI*u);e.x=A.start.x+(A.end.x-A.start.x)*v;e.y=A.start.y+(A.end.y-A.start.y)*v;A.angles=[Math.PI/2-.42+.95*u,Math.PI/2+.42-.95*u];
  if(u>.18&&u<.85)for(let i=0;i<2;i++){const q=s711Part(e,i);for(const seat of seatList())withSeat(seat,()=>{if(!player.dead&&!player.out&&player.invuln<=0&&s81003Distance(player.x,player.y,{x:q.x,y:q.y,ex:q.tip.x,ey:q.tip.y})<16)playerHit('Brood Sentinel claw');});}
  if(u>=1){e.x=A.start.x;e.y=A.start.y;s711Phase(e,'recover');}
 }else if(A.phase==='recover'){A.angles=A.angles.map(a=>a+clamp(s1aAngle(Math.PI/2-a),-dt*2.5,dt*2.5));if(A.t>.7)s711Tell(e,'mouth-open',[1.1,1,.9][r]);}
 else if(A.phase==='mouth-open'){combatWarningTick(e,'s711-mouth',A.t,A.warm);if(A.t>=A.warm)s711Phase(e,'mouth-fire');}
 else if(A.phase==='mouth-fire'){
  if(A.beat<=0){const p=s711Point(e,M.mouth),a=Math.atan2(T.y-p.y,T.x-p.x);s711Shot(e,{...p,angle:a},'fly',2.7,false,0);A.beat=turretInterval15(.24,[.24,.20,.17][r]);if(++A.round>=[4,5,6][r])s711Phase(e,'mouth-close');}
 }else if(A.phase==='mouth-close'&&A.t>.55){A.cycles++;s711Tell(e,'claw-tell',[1.12,1.0,.9][r]);}
 if(A.age>24){e.y-=150*dt;if(e.y<-160)e.dead=true;}
}
function s711Air(e,dt){const A=e._s711,M=s711M(e),r=s711Rank(),T=targetShip(e.x,e.y),K=A.model;
 s711MountGuns(e,dt,K==='missilejet'||K==='barge');
 if(K==='barge'){
  if(A.phase==='entry'){e.y+=48*dt;if(e.y>PLAY.y+130)s711Tell(e,'tell',1.05);}
  else if(A.phase==='tell'){combatWarningTick(e,'s711-barge',A.t,A.warm);if(A.t>=A.warm)s711Phase(e,'fire');}
  else if(A.phase==='fire'){e.x+=Math.sin(A.age*.9)*16*dt;if(A.beat<=0){for(let i=A.round%2;i<4;i+=2)s711Shot(e,s711Part(e,i).tip,'slug',4.7,i!==A.round%2,i);A.beat=turretInterval15(.21,[.21,.17,.14][r]);if(++A.round>=[8,10,12][r])s711Phase(e,'recover');}}
  else if(A.phase==='recover'&&A.t>1.1)s711Tell(e,'tell',.95);
 }else if(A.phase==='entry'){
  s711Fly(e,A.home,PLAY.y+125,148,2.7,dt);if(s711Ready(e)&&e.y>PLAY.y+90)s711Tell(e,'rev',K==='relay'?1.15:.85);
 }else if(A.phase==='rev'){
  const aim=Math.atan2(T.y-e.y,T.x-e.x);A.head+=clamp(s1aAngle(aim-A.head),-1.6*dt,1.6*dt);A.rotor+=dt*(3+15*A.t/A.warm);
  combatWarningTick(e,'s711-guns',A.t,A.warm);if(A.t>=A.warm){s711Phase(e,K==='missilejet'?'lock':'fire');A.attackOrigin={x:e.x,y:e.y};A.target={x:T.x,y:T.y};
   if(K==='missilejet')for(let i=0;i<4;i++)enemyLockOn(e,.95+i*.16,{fire:L=>{if(!s711Live(e)||e._s711.phase!=='lock')return;const p=s711Part(e,i%2).tip,b=s711Shot(e,p,'missile',3.4,i%2>0,i%2);if(b)s711Log(e,'missile-release',{lock:L.id});}});}
 }else if(A.phase==='lock'){if(A.t>1.7)s711Phase(e,'recover');}
 else if(A.phase==='fire'){
  const tx=A.home+Math.sin(A.t*1.6)*115*A.side,ty=PLAY.y+175+Math.sin(A.t)*40;s711Fly(e,tx,ty,K==='relay'?88:120,1.7,dt);
  // Guns slew only within their registered trunnions; rounds leave that facing.
  s711MountGuns(e,dt,true);A.rotor+=dt*(18+Math.min(26,A.t*12));
  A.cadence=turretInterval15(Math.max(.12,.26-A.t*.055),Math.max([.12,.10,.085][r],[.26,.23,.20][r]-A.t*.055));
  if(A.beat<=0&&s711Ready(e)){for(let i=0;i<2;i++)s711Shot(e,s711Part(e,i).tip,K==='crescent'?'laser':'slug',K==='crescent'?4.3:5.4,i>0,i);A.beat=K==='crescent'?turretInterval15(.30):A.cadence;}
  if(A.t>(K==='relay'?3.2:2.25)){A.rollStart=A.head;if(M.roll)s711Phase(e,'roll');else{A.cycles++;s711Phase(e,A.cycles>=2?'exit':'recover');}combatAudio0927(e,'jetDash',.6);}
 }else if(A.phase==='roll'){
  s711Fly(e,T.x,T.y,180,1.6,dt);
  if(K==='relay'&&A.beat<=0&&M.rollBores){const f=Math.min(7,Math.floor(A.t/.72*8));M.rollBores[f].forEach((p,i)=>s711Shot(e,s711Point(e,p),'slug',5.4,i>0,i));A.beat=turretInterval15(.12);}
  if(A.t>.72){A.cycles++;s711Phase(e,A.cycles>=2?'exit':'recover');}
 }else if(A.phase==='recover'){
  s711Fly(e,A.home,PLAY.y+110,155,2.8,dt);if(A.t>1.1)s711Tell(e,'rev',.85);
 }else if(A.phase==='exit')s711Fly(e,A.home+A.side*450,-220,285,2.8,dt);
 if(A.age>22&&K==='barge')e.y-=140*dt;
 if(A.age>30||A.phase==='exit'&&(e.y<-170||e.x<camLeftX()-220||e.x>camRightX()+220))e.dead=true;
}
function s711Tick(e,dt){if(!s711Live(e))return;const A=e._s711;A.age+=dt;A.t+=dt;A.beat-=dt;e.shoots=e.armed=false;
 if(bossActive||subBossActive||bossDefeated){if(!A.cancelled){s711Cancel(e);A.cancelled=true;}if(['ground','tank','crawler'].includes(A.model)){if(A.model==='ground')e.y=A.anchor.y-levelSrcY();else e.y=(e._lvlY??levelSrcY()+e.y)-levelSrcY();}else e.y-=180*dt;if(e.y<-220||e.y>VH+160)e.dead=true;return;}
 if(A.model==='crawler'){const row=e._lvlY??levelSrcY()+e.y;A.travel=(A.travel||0)+(A.lastWalk?Math.hypot(e.x-A.lastWalk.x,row-A.lastWalk.y):0);A.lastWalk={x:e.x,y:row};}
 if(e._stagger>0){e._stagger=Math.max(0,e._stagger-dt);return;}
 if(A.model==='ground')s711Ground(e,dt);else if(A.model==='tank'||A.model==='crawler')s711Tank(e,dt);else if(A.model==='brood')s711Brood(e,dt);else s711Air(e,dt);
 if(e.dead)s711Cancel(e);
}
function s711Cancel(e){playerLocks=playerLocks.filter(L=>L.src!==e);S711.fx=S711.fx.filter(f=>f.e!==e);e._combatWarnings={};s711Log(e,'cancel');}
function s711Blit(B,f,a,p,scale,tint=null,alpha=1){return v31Blit(B,f,a,p.x,p.y,B.cell*scale,tint,alpha);}
function s711Draw(e){const A=e._s711,M=s711M(e),tint=e.flash>0?hitFlashColor(e):null;
 if(A.model==='ground'){
  const scale=64/256;s711Blit(S711_ART.banks.ground_base,0,Math.PI/2,e,76/256,tint);s711Blit(S711_ART.banks['head_'+A.weapon],0,A.head,e,scale,tint);
  if(A.weapon!=='mg'){ctx.save();ctx.globalCompositeOperation='lighter';s711Blit(S711_ART.banks['head_'+A.weapon+'_glow'],0,A.head,e,scale,null,pxgStep(.6+.4*Math.sin(A.age*9)));ctx.restore();}
  e._s711Rendered={model:A.model,dir:v31Dir(A.head),key:S711_ART.banks['head_'+A.weapon].key};
 }else{
  const k=M.spanWorld/256,dying=e._dyingT!=null,head=dying?A.head+(e.spin||0):A.head,roll=A.phase==='roll'&&M.roll&&!dying;
  if(!dying&&M.tails.length)for(const p of M.tails){const q=s711Point(e,p);s711Blit(S711_ART.banks.thruster,Math.floor(A.age*26)%S711_ART.banks.thruster.frames,q.angle,q,38/S711_ART.banks.thruster.cell);}
  const rf=roll?Math.min(7,Math.floor(A.t/.72*8)):0;
  if(roll)s711Blit(M.roll,rf,head,e,k,tint);
  else if(A.model==='crawler'){
   M.segments.forEach((m,i)=>{const p=s711Point(e,m.mount);p.x+=Math.sin((A.travel||0)*.3-i*.8)*1.5;s711Blit(m.bank,0,head,p,k,tint);});
   M.modules.forEach((m,i)=>{const p=s711Point(e,m.mount),a=head+Math.sin((A.travel||0)*.3+(i%3)*Math.PI+(i<3?0:Math.PI))*.20;s711Blit(m.bank,0,a,p,k,tint);});
  }else{
   s711Blit(M.bank,0,head,e,k,tint);
   M.modules.forEach((m,i)=>{const p=s711Part(e,i),f=m.rotary?Math.floor(A.rotor)%8:0;s711Blit(m.bank,f,p.angle,p,k,tint);});
   if(M.face){let f=A.phase==='mouth-open'?Math.min(3,Math.floor(A.t/A.warm*4)):A.phase==='mouth-fire'?4+Math.floor(A.t*14)%2:A.phase==='mouth-close'?Math.min(7,5+Math.floor(A.t/.55*3)):0;s711Blit(M.face.bank,f,head,s711Point(e,M.face.mount),k,tint);A.faceFrame=f;}
  }
  if(!tint&&!dying&&!roll&&S711_ART.banks[A.model+'_glow']){ctx.save();ctx.globalCompositeOperation='lighter';s711Blit(S711_ART.banks[A.model+'_glow'],0,head,e,k,null,pxgStep(.4+.6*Math.sin(A.age*8)**2));ctx.restore();}
  const s=e._esh;if(s&&!dying&&s.phase!=='broken'){ctx.save();ctx.globalCompositeOperation='lighter';const deploy=s.phase==='deploy'?clamp(s.animT/.34,0,1):1,alpha=deploy*(s.hitT>0?.95:pxgStep(.35+.65*Math.sin(A.age*7)**2));s711Blit(S711_ART.banks[A.model+'_shield'],0,head,e,k,null,alpha);M.modules.forEach((m,i)=>{const p=s711Part(e,i);s711Blit(m.shield,m.rotary?Math.floor(A.rotor)%8:0,p.angle,p,k,null,alpha);});ctx.restore();}
  e._s711Rendered={model:A.model,dir:v31Dir(head),frame:rf,face:A.faceFrame,key:roll?M.roll.key:M.bank.key,modules:M.modules.length};
 }
 if(s711Live(e))s711DrawWarning(e);
}
function s711DrawWarning(e){const A=e._s711,M=s711M(e);if(A.model==='missilejet'||A.cancelled||!['tell','rev','mouth-open','claw-tell'].includes(A.phase))return;
 const ps=A.phase==='claw-tell'?M.modules.map((m,i)=>s711Part(e,i).tip):A.phase==='mouth-open'?[s711Point(e,M.mouth)]:A.model==='ground'?Array.from({length:A.weapon==='mg'?2:1},(_,index)=>s711FlashPoint({e,index})):M.modules.map((m,i)=>s711Part(e,i).tip);
 for(let i=0;i<ps.length;i++){const p=ps[i],len=A.phase==='claw-tell'?150:1000,claw=A.phase==='claw-tell',end=claw&&A.target?{x:A.target.x+(i?-32:32),y:A.target.y}:{x:p.x+Math.cos(p.angle)*len,y:p.y+Math.sin(p.angle)*len};combatWarningDraw(e,{x:p.x,y:p.y,ex:end.x,ey:end.y,width:claw?38:20,progress:clamp(A.t/A.warm,0,1),fieldOnly:true});}
}
drawEnemy=function(e){if(e?._s711&&!e.dead)return s711Draw(e);return S711.base.draw.apply(this,arguments);};
function s711Projectile(b){const kind=b._s711Kind,B=S711_ART.banks[kind==='missile'?'missile':kind],age=projectileVisualAge(b),a=Math.atan2(b.vy,b.vx),f=Math.floor(age*(kind==='fly'?32:23))%B.frames,size=kind==='fly'?38:kind==='missile'?48:kind==='slug'?32:kind==='sonic'?42:46;
 const out=v31Blit(B,f,a,b.x,b.y,size);if(kind==='laser'||kind==='slug'){ctx.save();ctx.globalCompositeOperation='lighter';v31Blit(S711_ART.banks[kind+'_glow'],f,a,b.x,b.y,size,null,pxgStep(.45+.55*Math.sin(age*13)**2));ctx.restore();}return out;}
ovSonicProjectileDraw=function(b){return b?._s711Kind?s711Projectile(b):S711.base.early.apply(this,arguments);};
drawCombatFinalProjectile=function(b){return b?._s711Kind?s711Projectile(b):S711.base.final.apply(this,arguments);};
updateEffects=function(dt){const r=S711.base.effects.apply(this,arguments);for(const f of S711.fx)f.t+=dt;S711.fx=S711.fx.filter(f=>f.t<f.life&&s711Live(f.e));
 for(const b of eBullets)if(b._s711Kind==='fly'&&!b.dead&&b.t<1.15){const T=targetShip(b.x,b.y),want=Math.atan2(T.y-b.y,T.x-b.x),a=Math.atan2(b.vy,b.vx),speed=Math.hypot(b.vx,b.vy),head=a+clamp(s1aAngle(want-a),-.65*dt,.65*dt);b.vx=Math.cos(head)*speed;b.vy=Math.sin(head)*speed;}
 return r;};
function s711FlashPoint(f){const e=f.e,A=e._s711,M=s711M(e);
 if(['relay','slime','crescent','missilejet','barge'].includes(A.model))return A.phase==='roll'&&M.rollBores?s711Point(e,M.rollBores[Math.min(7,Math.floor(A.t/.72*8))][f.index]):s711Part(e,f.index).tip;
 if(A.model==='tank'||A.model==='crawler')return s711Point(e,(M.guns||M.mouths)[f.index]);
 if(A.model==='brood')return s711Point(e,M.mouth);
 if(A.model==='ground'){const pp=A.weapon==='mg'?[[98,204],[160,204]][f.index]:[128,218],a=s711Angle(A.head),rot=a-Math.PI/2,k=64/256;return{x:e.x+((pp[0]-128)*Math.cos(rot)-(pp[1]-128)*Math.sin(rot))*k,y:e.y+((pp[0]-128)*Math.sin(rot)+(pp[1]-128)*Math.cos(rot))*k,angle:a};}
 return{x:f.p.x+e.x-f.from.x,y:f.p.y+e.y-f.from.y,angle:f.p.angle};}
drawNavalFlashes=function(){const r=S711.base.flashes.apply(this,arguments);for(const f of S711.fx){const p=s711FlashPoint(f);s711Blit(S711_ART.banks.muzzle,Math.min(3,Math.floor(f.t/f.life*4)),p.angle,p,f.size/S711_ART.banks.muzzle.cell);}return r;};
killEnemy=function(e){const r=S711.base.kill.apply(this,arguments);if(e?._s711&&!s711Live(e))s711Cancel(e);return r;};
stageLoadBegin=function(n,keys){if(n===7)keys=[...(keys||[]),...Object.values(S711_ART.banks).map(b=>b.key),...['green','yellow','red'].map(c=>'bmfx_fov_'+c+'_tall')];return S711.base.load.call(this,n,keys);};
beginStage=function(){S711.events=[];S711.fx=[];return S711.base.begin.apply(this,arguments);};
globalThis.BOF_SEWER_REFIT={state:S711,art:S711_ART};
