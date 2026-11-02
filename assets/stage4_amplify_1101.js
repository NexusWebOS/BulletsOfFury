"use strict";
/* Mike's highway corrections. Complete authored plates/directions, fixed
   weapons, real missile locks and the shared ground-traffic owner. */
const S411={base:{spawn:spawnEnemy,chase:s4ChaseTick,draw:drawEnemy,attach:r46Attach,model:r46Model,
 beginAI:ai27Begin,endAI:ai27End,route:eb11OwnsRoute,entry:enemyEntrySweep,frenzy:enemyFrenzyTick,
 shot:ovSonicProjectileDraw,flashes:drawNavalFlashes,effects:updateEffects,kill:killEnemy,load:stageLoadBegin,begin:beginStage,death:deathClassOf},
 serial:0,fx:[],events:[],types:{s4command:'command',s4heavyjet:'heavyjet',s4missile:'missiletruck',s4tanker:'tanker',s4tractor:'tractor',s4sam:'sam'}};
for(const b of Object.values(S411_ART.banks))XART._src[b.key]=b.path;
function s411Own(e){return run.stage===4&&!!e?._s411;}
function s411Live(e){return !!e&&!e.dead&&e.hp>0&&e._dyingT==null;}
function s411M(e){return S411_ART.models[e._s411.model];}
function s411Log(e,event,more={}){S411.events.push({id:e?._s411?.id,type:e?.type,event,t:efxClock,...more});if(S411.events.length>1500)S411.events.shift();}
r46Attach=function(e){if(run.stage===4&&S411.types[e?.type])return;return S411.base.attach.apply(this,arguments);};
r46Model=function(e){return s411Own(e)?null:S411.base.model.apply(this,arguments);};
function s411Facing(e){return Math.PI/2+s1aDir(e._s411.head,16)*TAU/16;}
function s411Point(e,p){const m=s411M(e),k=m.side/192;return{x:e.x+(p[0]-96)*k,y:e.y+(p[1]-96)*k,angle:m.ground?Math.PI/2:s411Facing(e)};}
function s411Gun(e,i=0){const m=s411M(e),d=s1aDir(e._s411.head,16),points=m.ground?m.guns:m.gunPoses[d];return s411Point(e,points[i%points.length]);}
function s411Mode(e,phase){Object.assign(e._s411,{phase,t:0,beat:0,round:0});s411Log(e,phase);}
spawnEnemy=function(type,x,y,opt={}){const e=S411.base.spawn.apply(this,arguments);if(!e||run.stage!==4)return e;
 if(e._armor17){e._s411Straight=e.x;e._noSep=true;return e;}
 const model=S411.types[e.type];if(!model)return e;const m=S411_ART.models[model],hp=e.hp;
 for(const k of['_r46','_ai','_air17','_ep13','_vp12','_s4Act','_jetManeuver','_entrySweep','_af10Jet','_ac10Ram','_modJet','_modJetAngles','_r30'])delete e[k];
 e._s411={id:++S411.serial,model,ground:m.ground,head:Math.PI/2,phase:m.ground?'wait':'entry',age:0,t:0,cd:.65,round:0,beat:0,launched:0,homeX:clamp(e.x,camLeftX()+90,camRightX()-90),side:e.x<worldWidth()/2?1:-1};
 e.pattern='s4chase';e._s4chase=e.type;e._frFlight=false;e.shoots=e.armed=false;e.fireCd=e._fcd=999;e.fk=null;e.spin=0;e._noSep=true;e.ground=m.ground;
 const f=m.ground?m.footprint.map(v=>v*m.side/192):[m.side*.73,m.side*.78];
 e.w=f[0]*.9;e.h=f[1]*.9;e._drawW=f[0];e._drawH=f[1];
 if(m.ground){e._groundTraffic=true;e._groundTrafficSize={w:f[0],h:f[1]};groundTrafficPlaceEntry(e);groundTrafficReserve(e,enemies.filter(o=>o!==e&&groundTrafficVehicle(o)));e._s411.lane=e.x;e._lvlY=levelSrcY()+e.y;}
 s411Log(e,'spawn',{model,hp,footprint:f});return e;
};
eb11OwnsRoute=function(e){return s411Own(e)||!!e?._s411Straight||S411.base.route.apply(this,arguments);};
enemyEntrySweep=function(e){if(s411Own(e)||e?._s411Straight!=null)return;return S411.base.entry.apply(this,arguments);};
enemyFrenzyTick=function(e){if(s411Own(e))return;const r=S411.base.frenzy.apply(this,arguments);if(e?._s411Straight!=null)groundTrafficSet(e,e._s411Straight,e.y);return r;};
ai27Begin=function(e,dt){const old=S411.base.beginAI.apply(this,arguments);if(e?._s411Straight!=null)groundTrafficSet(e,e._s411Straight,e.y);return old;};
ai27End=function(e,old){if((s411Own(e)||e?._s411Straight!=null)&&e._ai27)e._ai27.dx=0;const r=S411.base.endAI.apply(this,arguments);
 if(e?._s411Straight!=null&&!e.dead)groundTrafficSet(e,e._s411Straight,e.y);return r;};
function s411Fly(e,tx,ty,speed,turn,dt){const A=e._s411,want=Math.atan2(ty-e.y,tx-e.x);A.head+=clamp(s1aAngle(want-A.head),-turn*dt,turn*dt);e.x+=Math.cos(A.head)*speed*dt;e.y+=Math.sin(A.head)*speed*dt;e.spin=A.head-Math.PI/2;}
function s411Flash(e,p,rocket=false){S411.fx.push({owner:e,p:{...p},origin:{x:e.x,y:e.y},age:0,life:rocket?.15:.10,rocket});}
function s411Round(e,i,missile=false){if(!s411Live(e))return null;const m=s411M(e),p=s411Gun(e,i),a=p.angle;
 const b=eShootT(p.x,p.y,a,missile?2.65:4.7,missile?'s4missile':'s4brass',{owner:e,noMuzzle:true,silent:true,w:missile?11:7,h:missile?26:16});
 if(!b||b.dead||b._ai27Held)return null;
 Object.assign(b,{_s411Art:missile?(m.ground?'rack':'jet'):'slug',_s411Owner:e,_noArsenal:true,homing:false,_shootable:missile,_weaponProof:!missile});
 if(missile){b.hp=target17Rank()>=2?2:1;b._s4Accel=1.25;b._s4Max=5.25;b.life=7;b._s411Length=m.ground?m.missileLength*m.side/192:28;}
 const f={...p};if(missile&&m.ground)f.y-=m.missileLength*m.side/192*.5;s411Flash(e,f,missile);
 if(missile)Audio.SFX.enemyMissile?.();else if(i===0)Audio.SFX.enemyMachineGunHeavy?.();
 e._s411.lastShot=e._s411.age;s411Log(e,'shot',{kind:b.kind,art:b._s411Art,index:i,x:p.x,y:p.y,a,vx:b.vx,vy:b.vy});return b;
}
function s411Salvo(e,count){const A=e._s411,rank=ai27Level(),warm=[.9,.8,.7][rank],spacing=.18;A.launched=0;A.salvo=count;
 for(let i=0;i<count;i++)enemyLockOn(e,warm+i*spacing,{fire:L=>{if(!s411Live(e))return;const b=s411Round(e,i,true);if(b){A.launched++;s411Log(e,'missile-release',{index:i,lock:L.id,x:b.x,y:b.y});}}});
 s411Mode(e,'lock');A.lockTime=warm+(count-1)*spacing+.12;s411Log(e,'retina-salvo',{count,warm,spacing});
}
function s411Visible(e){return e.x>camLeftX()+25&&e.x<camRightX()-25&&e.y>PLAY.y+40&&e.y<VH-80;}
s4ChaseTick=function(e,dt){if(!s411Own(e))return S411.base.chase.apply(this,arguments);if(!s411Live(e))return;
 if(e._stagger>0){e._stagger=Math.max(0,e._stagger-dt);return;}
 const A=e._s411,m=s411M(e),rank=ai27Level(),T=targetShip(e.x,e.y);A.age+=dt;A.t+=dt;A.cd-=dt;e.shoots=false;e._s4Act=null;e.fireCd=e._fcd=999;
 if(e._frozen||e._mercuryLock>0||e._shieldStun>0||e._stagger>0)return;
 if(m.ground){
  const speed={tanker:114,tractor:62,missiletruck:40,sam:35}[A.model],next=e.y+speed*dt;
  if(groundTrafficLegal(e,A.lane,next))groundTrafficSet(e,A.lane,next);else groundTrafficSet(e,A.lane,e.y);
  A.head=Math.PI/2;e.spin=0;
  if(A.model!=='tanker'&&s411Visible(e)&&T.y>e.y+45){
   if(A.phase==='wait'&&A.cd<=0){if(A.model==='tractor'){s411Mode(e,'tell');Audio.SFX.bossWeaponCharge?.();}else s411Salvo(e,A.model==='sam'?3:2);}
   else if(A.phase==='lock'&&A.t>A.lockTime){s411Mode(e,'recover');}
   else if(A.phase==='tell'){combatWarningTick(e,'s411-front',A.t,.62);if(A.t>=.62)s411Mode(e,'fire');}
   else if(A.phase==='fire'){if(A.beat<=0&&A.round<[3,4,5][rank]){for(let i=0;i<2;i++)s411Round(e,i);A.round++;A.beat=.12;}A.beat-=dt;if(A.round>=[3,4,5][rank]&&A.beat<=0)s411Mode(e,'recover');}
   else if(A.phase==='recover'&&A.t>[1.9,1.5,1.15][rank]){s411Mode(e,'wait');A.cd=.15;}
  }
 }else{
  const committed=['tell','fire','lock'].includes(A.phase);
  if(committed){e.x+=Math.cos(A.head)*65*dt;e.y+=Math.sin(A.head)*65*dt;}
  else if(A.age<1.8)s411Fly(e,A.homeX,PLAY.y+115,150,2.0,dt);
  else if(A.age<13){const q=(A.age-1.8)*.72,tx=clamp(A.homeX+Math.sin(q)*A.side*155,camLeftX()+85,camRightX()-85),ty=PLAY.y+155+Math.sin(q*1.45)*80;s411Fly(e,tx,ty,125,2.1,dt);}
  else{s411Fly(e,clamp(A.homeX-A.side*150,camLeftX()+40,camRightX()-40),VH+220,235,1.6,dt);A.phase='exit';}
  if(A.phase==='entry'&&A.age>1.8)s411Mode(e,'curve');
  const targetAngle=Math.atan2(T.y-e.y,T.x-e.x),facing=Math.abs(s1aAngle(targetAngle-s411Facing(e)))<.65;
  if(A.phase==='curve'&&A.age<12&&A.cd<=0&&s411Visible(e)&&T.y>e.y+65&&facing){if(A.model==='heavyjet')s411Salvo(e,2);else{s411Mode(e,'tell');Audio.SFX.bossWeaponCharge?.();}}
  else if(A.phase==='tell'){combatWarningTick(e,'s411-guns',A.t,.58);if(A.t>=.58)s411Mode(e,'fire');}
  else if(A.phase==='fire'){A.beat-=dt;if(A.beat<=0&&A.round<[4,5,6][rank]){for(let i=0;i<2;i++)s411Round(e,i);A.round++;A.beat=.10;}if(A.round>=[4,5,6][rank]&&A.beat<=0)s411Mode(e,'recover');}
  else if(A.phase==='lock'&&A.t>A.lockTime)s411Mode(e,'recover');
  else if(A.phase==='recover'&&A.t>.55){s411Mode(e,'curve');A.cd=turretInterval15(1.1,[1.1,.85,.65][rank]);}
 }
 if(e.y>VH+150||A.age>24||e.x<camLeftX()-190||e.x>camRightX()+190){e.dead=true;s411Log(e,'exit');}
};
function s411Blit(B,f,x,y,size,color=null){if(!B||!XART.rdy(B.key))return false;const r=B.cells[clamp(f|0,0,B.frames-1)],im=color?xartTint(B.key,color,1):XART.get(B.key);ctx.save();ctx.imageSmoothingEnabled=false;ctx.drawImage(im,...r,x-size/2,y-size/2,size,size);ctx.restore();return true;}
drawEnemy=function(e){if(!s411Own(e)||e.dead)return S411.base.draw.apply(this,arguments);const A=e._s411,m=s411M(e);let B=m.banks.sequence||m.banks.heading,f=0;
 if(m.ground){if(A.model==='tractor')f=A.phase==='fire'?4+Math.floor(A.t*22)%4:Math.floor(A.age*12)%4;
  else if(A.model==='tanker')f=Math.floor(A.age*14)%8;
  else if(A.model==='sam')f=A.phase==='lock'?Math.min(3,A.launched):A.phase==='recover'?Math.min(6,4+Math.floor(A.t*3)):Math.floor(A.age*8)%2?0:7;
  else f=A.phase==='lock'?Math.min(2,A.launched):A.phase==='recover'?3+Math.min(1,Math.floor(A.t*3)):5+Math.floor(A.age*10)%3;
 }else{f=s1aDir(A.head,16);if(f===0&&A.phase==='fire'){B=m.banks.attack;f=Math.floor(A.t*20)%4;}}
 if(e._dyingT!=null){B=m.banks.sequence||m.banks.heading;f=0;}
 if(e._esh)drawEnemyShieldLayer(e,false);
 if(!m.ground&&e._dyingT==null){const d=s1aDir(A.head,16),a=s411Facing(e)-Math.PI/2,c=Math.cos(a),s=Math.sin(a),k=m.side/192;
  for(let i=0;i<m.tails.length;i++){const p=m.tailPoses?.[d]?.[i]||m.tails[i],x=(p[0]-96)*k,y=(p[1]-96)*k;s1aBlit('thruster',Math.floor(A.age*24)%8,a+Math.PI/2,e.x+(m.tailPoses?x:x*c-y*s),e.y+(m.tailPoses?y:x*s+y*c),30);}}
 s411Blit(B,f,e.x,e.y,m.side,e.flash>0?hitFlashColor(e):null);e._s411Rendered={key:B.key,frame:f,phase:A.phase,dir:s1aDir(A.head,16),size:m.side};
 if(e._esh){drawEnemyShieldLayer(e,true);if(typeof bet24Bar==='function')bet24Bar(e);}
 if(A.phase==='tell')for(let i=0;i<m.guns.length;i++){const p=s411Gun(e,i);combatWarningDraw(e,{...p,ex:p.x+Math.cos(p.angle)*1000,ey:p.y+Math.sin(p.angle)*1000,progress:clamp(A.t/(m.ground?.62:.58),0,1),width:17,fieldOnly:true});}
};
ovSonicProjectileDraw=function(b){if(!b?._s411Art)return S411.base.shot.apply(this,arguments);const a=Math.atan2(b.vy,b.vx);
 if(b._s411Art==='slug'){s1aBlit('slug',Math.floor(projectileVisualAge(b)*20)%4,a,b.x,b.y,28);return true;}
 if(b._s411Art==='jet'){const B=Object.entries(R46_ORDNANCE.glyphs).find(([k])=>{const p=JSON.parse(k);return p[0]===4&&p[1]==='s4heavyjet'&&/missile/.test(p[2]);})?.[1];if(B){r46Blit(B,Math.floor(projectileVisualAge(b)*B.fps)%B.frames,a,b.x,b.y,B.cell);return true;}}
 const P=S411_ART.projectile;let d=0;for(let i=1;i<P.angles.length;i++)if(Math.abs(s1aAngle(a-P.angles[i]))<Math.abs(s1aAngle(a-P.angles[d])))d=i;
 const size=(b._s411Length||34)*P.bank.cell/P.span;s411Blit(P.bank,d,b.x,b.y,size);const back=(b._s411Length||34)*.52;s1aBlit('thruster',Math.floor(projectileVisualAge(b)*24)%8,a,b.x-Math.cos(a)*back,b.y-Math.sin(a)*back,20);return true;
};
updateEffects=function(dt){const r=S411.base.effects.apply(this,arguments);for(const f of S411.fx)f.age+=dt;S411.fx=S411.fx.filter(f=>f.age<f.life&&s411Live(f.owner));return r;};
drawNavalFlashes=function(){const r=S411.base.flashes.apply(this,arguments);for(const f of S411.fx){const k=f.rocket?'rocket_muzzle':'muzzle',B=S1A_ART[k];s1aBlit(k,Math.min(B.frames-1,Math.floor(f.age/f.life*B.frames)),f.p.angle,f.p.x+f.owner.x-f.origin.x,f.p.y+f.owner.y-f.origin.y,f.rocket?35:25);}return r;};
deathClassOf=function(e){return s411Own(e)&&e._s411.ground?'tank':S411.base.death.apply(this,arguments);};
killEnemy=function(e){const r=S411.base.kill.apply(this,arguments);if(s411Own(e)&&!s411Live(e)){playerLocks=playerLocks.filter(L=>L.src!==e);S411.fx=S411.fx.filter(f=>f.owner!==e);
 if(e._s411.model==='tanker'&&!e._s411Detonated){e._s411Detonated=true;const hits=[];for(const q of enemies.slice()){if(q===e||q.dead||q._dyingT!=null||q._boss||q._mini||q._amini)continue;const d=Math.hypot(q.x-e.x,q.y-e.y);if(d<155){const hp=q.hp;hitEnemy(q,72*(1-.55*d/155));hits.push({type:q.type,before:hp,after:q.hp});}}Audio.SFX.expSmall?.();s411Log(e,'fuel-splash',{radius:155,hits});}}
 return r;};
stageLoadBegin=function(n,keys){if(n===4)keys=[...(keys||[]),...Object.values(S411_ART.banks).map(b=>b.key),...['green','yellow','red'].map(c=>'bmfx_fov_'+c+'_tall')];return S411.base.load.call(this,n,keys);};
beginStage=function(){S411.events=[];S411.fx=[];S411.serial=0;return S411.base.begin.apply(this,arguments);};
globalThis.BOF_HIGHWAY_REFIT={state:S411,art:S411_ART};
