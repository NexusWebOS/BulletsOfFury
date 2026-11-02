"use strict";
/* Ice roster: actual directional hull cells, measured native launchers,
   four cardinal beams, island fixtures and a distinct mine-dropping jet. */
const I31={base:{spawn:spawnEnemy,ice:s3IceTick,draw:drawEnemy,entry:enemyEntrySweep,route:eb11OwnsRoute,aiEnd:ai27End,
 turret:modularGroundTurretTick,shot:drawCombatFinalProjectile,intercept:enemyOrdnanceCanIntercept,element:enemyOrdnanceElement,
 effects:updateEffects,flashes:drawNavalFlashes,load:stageLoadBegin,begin:beginStage,kill:killEnemy,earlyShot:ovSonicProjectileDraw},events:[],fx:[],serial:0,
 models:{sharddart:'shard',cryoeye:'eye',glaciercarrier:'carrier',s3interceptor:'interceptor',ac10icejet:'interceptor',s3mine:'mine'}};
for(const B of Object.values(I31_ART.banks))XART._src[B.key]=B.path;
const I31_ISLAND=Uint8Array.from(atob(I31_ART.islands.bits),c=>c.charCodeAt(0));
function i31Log(e,event,more={}){I31.events.push({id:e?._i31?.id,type:e?.type,event,t:efxClock,...more});if(I31.events.length>800)I31.events.shift();}
function i31Live(e){return !!e&&!e.dead&&e.hp>0&&e._dyingT==null;}
function i31M(e){return I31_ART.models[e._i31.model];}
function i31Size(e){return Math.max(e.w,e.h)*160/140;}
function i31Head(e){const A=e._i31;if(A.model==='shard')return Math.PI/2;return Math.PI/2+s1aDir(A.head,8)*TAU/8;}
function i31Blit(B,f,a,x,y,size,tint=null,alpha=1){if(!B||!XART.rdy(B.key))return false;
 const c=B.cell,d=s1aDir(a,B.dirs),cols=B.cols||B.dirs,im=tint?xartTint(B.key,tint,1):XART.get(B.key);
 ctx.save();ctx.globalAlpha*=alpha;ctx.imageSmoothingEnabled=false;ctx.drawImage(im,d%cols*c,(Math.min(B.frames-1,f|0)*(B.dirRows||1)+Math.floor(d/cols))*c,c,c,x-size/2,y-size/2,size,size);ctx.restore();return true;}
function i31Point(e,p){const a=i31Head(e)-Math.PI/2,c=Math.cos(a),s=Math.sin(a),k=i31Size(e)/160,x=(p[0]-80)*k,y=(p[1]-80)*k;
 return{x:e.x+x*c-y*s,y:e.y+x*s+y*c,angle:a+Math.PI/2};}
function i31Gun(e,n=0){const M=i31M(e),d=s1aDir(e._i31.head,8),p=M.gunPoses?.[d]?.[n];
 if(p){const k=i31Size(e)/160;return{x:e.x+(p[0]-80)*k,y:e.y+(p[1]-80)*k,angle:i31Head(e)};}return i31Point(e,M.guns[n%M.guns.length]);}
function i31Flash(e,p,size=26){I31.fx.push({owner:e,p:{...p},anchor:{x:e.x,y:e.y},t:0,life:.12,size});}
function i31Shot(e,p,kind='slug',silent=false){const mine=kind==='mine',sonic=kind==='sonic';
 const b=eShootT(p.x,p.y,p.angle,mine?.15:sonic?2.9:4.4,mine?'s3mortar':sonic?'rzbSonic':'s3tracer',{owner:e,noMuzzle:true,silent:true,w:mine?20:sonic?22:9,h:mine?20:sonic?14:20});
 if(!b||b.dead||b._ai27Held)return b;
 b._i31Kind=kind;b._i31Owner=e;b._noArsenal=true;b._weaponProof=!mine;b._shootable=mine;b._energyOrdnance=true;b.homing=false;
 if(mine){b.vx=b.vy=0;b.life=5.2;b.hp=3;}
 if(!silent){if(sonic)stageRevisionCue(e,'razorbackPressure',.12);else(mine?Audio.SFX.bombDrop:kind==='laser'?Audio.SFX.enemyHeavyLaser:Audio.SFX.enemyMachineGunHeavy)?.();}
 i31Flash(e,p,mine?30:sonic?36:23);if(e._i31)e._i31.lastShot=e._i31.age;i31Log(e,'shot',{kind,x:p.x,y:p.y,a:p.angle});return b;}
enemyOrdnanceCanIntercept=function(b){return b?._i31Kind?b._i31Kind==='mine':I31.base.intercept.apply(this,arguments);};
enemyOrdnanceElement=function(b){return b?._i31Kind==='mine'?'ice':b?._i31Kind?null:I31.base.element.apply(this,arguments);};
function i31IslandAt(x,y){const M=I31_ART.islands,gx=Math.floor(x/M.cell),gy=Math.floor(y/M.cell),n=gy*M.gw+gx;
 return gx>=0&&gx<M.gw&&gy>=0&&gy<M.gh&&!!(I31_ISLAND[n>>3]&(1<<(7-(n&7))));}
function i31Legal(e,x,y){const r=e.w*.64,sy=levelSrcY()+y;return[-1,-.5,0,.5,1].every(a=>[-1,-.5,0,.5,1].every(b=>i31IslandAt(x+a*r,sy+b*r)));}
function i31Place(e){const born=e.y,prefer=e.x;for(let row=0;row<=960;row+=8){const y=born-row;for(let d=0;d<worldWidth();d+=8)for(const side of d?[-1,1]:[1]){
 const x=clamp(prefer+d*side,38,worldWidth()-38);if(i31Legal(e,x,y)){e.x=x;e.y=y;e._fixedX=x;e._lvlY=levelSrcY()+y;return true;}}}return false;}
spawnEnemy=function(type,x,y,opt={}){const e=I31.base.spawn.apply(this,arguments);if(!e||run.stage!==3)return e;
 if(e._modTurret&&['laser','sonic'].includes(e._modTurret.weapon)){
  e._i31Turret=true;e._i31Ground={phase:'wait',t:0,cd:.7};e._drawW=e._drawH=e.w*1.27;
  if(!i31Place(e)){e.dead=true;e.dropOk=false;return null;}i31Log(e,'island-fixture',{x:e.x,y:e.y});return e;}
 const model=I31.models[type];if(!model)return e;
 const dims={shard:[50,60],interceptor:type==='ac10icejet'?[102,90]:[84,78],carrier:[100,96],eye:[100,100],mine:[106,96]}[model];
 e.w=dims[0];e.h=dims[1];e._drawW=e.w;e._drawH=e.h;e._noSep=true;e._frFlight=false;e.pattern='s3ice';e._s3ice=type;
 e.shoots=e.armed=false;e.fireCd=999;e.fk=null;e.spin=0;
 for(const k of ['_dr','_cn','_ai','_af10Jet','_ac10Ram','_entry','_s3Act','_biomePlate','_jetManeuver','_ep13','_esh'])delete e[k];
 e._i31={id:++I31.serial,model,phase:'entry',age:0,t:0,head:Math.PI/2,side:e.x<worldWidth()/2?1:-1,homeX:e.x,homeY:PLAY.y+130,cd:.6,round:0,beams:[],sourceAI:opt.ai?.kind||'curve'};
 i31Log(e,'spawn',{model,hp:e.hp});return e;};
enemyEntrySweep=function(e){if(e?._i31)return;return I31.base.entry.apply(this,arguments);};
eb11OwnsRoute=function(e){return !!e?._i31||I31.base.route.apply(this,arguments);};
ai27End=function(e,old){if(e?._i31&&e._ai27)e._ai27.dx=0;return I31.base.aiEnd.apply(this,arguments);};
function i31Mode(e,phase){e._i31.phase=phase;e._i31.t=0;e._i31.round=0;e._i31.cd=0;i31Log(e,phase);}
function i31Fly(e,tx,ty,speed,turn,dt){const A=e._i31,want=Math.atan2(ty-e.y,tx-e.x);A.head+=clamp(s1aAngle(want-A.head),-turn*dt,turn*dt);
 const old={x:e.x,y:e.y};e.x+=Math.cos(A.head)*speed*dt;e.y+=Math.sin(A.head)*speed*dt;e.vx=(e.x-old.x)/dt/60;e.vy=(e.y-old.y)/dt/60;}
function i31BeamsTick(e,dt){const A=e._i31;for(const b of A.beams){b.t+=dt;if(b.t>=b.life)continue;
 for(const seat of seatList())withSeat(seat,()=>{if(player.dead||player.out)return;const x=player.x-b.p.x,y=player.y-b.p.y,c=Math.cos(b.p.angle),s=Math.sin(b.p.angle),along=x*c+y*s,across=Math.abs(-x*s+y*c);
  if(along>0&&along<1000&&across<7+(player._hx||8))playerHit('Cryoeye ice laser');});}A.beams=A.beams.filter(b=>b.t<b.life);}
s3IceTick=function(e,dt){if(!e?._i31)return I31.base.ice.apply(this,arguments);if(!i31Live(e))return;
 const A=e._i31,r=v31Rank(),T=targetShip(e.x,e.y);A.age+=dt;A.t+=dt;A.cd-=dt;i31BeamsTick(e,dt);e.spin=0;
 if(A.model==='eye'){
  if(A.phase==='entry'){e.y+=92*dt;if(e.y>=A.homeY)i31Mode(e,'wait');}
  else if(A.phase==='wait'){e.x+=Math.sin(A.age*1.1)*12*dt;if(A.t>1.0){i31Mode(e,'tell');A.lanes=i31M(e).guns.map((_,i)=>({...i31Gun(e,i),angle:-Math.PI/2+i*Math.PI/2}));Audio.SFX.bossWeaponCharge?.();}}
  else if(A.phase==='tell'){combatWarningTick(e,'i31-cross',A.t,1.1);if(A.t>=1.1){A.beams=A.lanes.map(p=>({p:{...p},t:0,life:.8}));for(const p of A.lanes)i31Flash(e,p,40);Audio.SFX.enemyHeavyLaser?.();i31Log(e,'cross-lasers',{count:A.beams.length});i31Mode(e,'fire');}}
  else if(A.phase==='fire'&&A.t>.85)i31Mode(e,'recover');
  else if(A.phase==='recover'&&A.t>[2.3,1.9,1.6][r])i31Mode(e,A.age>11?'exit':'wait');
  else if(A.phase==='exit')e.y+=150*dt;
 }else if(A.model==='shard'){
  // Upright top-view bank poses only: no inversion, roll, or upward flip.
  e.y+=108*dt;const kind=A.sourceAI,amp=kind==='diag'?70:kind==='charge'?36:95,phase=kind==='rush'?1.5:1.05;
  const dx=Math.sin(A.age*phase)*amp*A.side;A.head=Math.PI/2-clamp(dx/160,-.45,.45);e.x+=dx*dt;
  A.phase='curve';if(A.cd<=0&&e.y>PLAY.y+40&&e.y<T.y-65){for(let i=0;i<2;i++){const p=i31Gun(e,i);p.angle=Math.PI/2;i31Shot(e,p,'slug',i>0);}A.cd=turretInterval15(.85,[.85,.65,.48][r]);}
 }else if(A.model==='carrier'){
  A.phase='sortie';e.y+=68*dt;e.x=A.homeX+Math.sin(A.age*.72)*50;
  if(A.cd<=0&&e.y>PLAY.y+45&&e.y<VH-110){for(let i=0;i<2;i++){const p=i31Gun(e,i);i31Shot(e,p,'slug',i>0);}A.cd=turretInterval15(.65,[.65,.48,.35][r]);}
 }else if(A.model==='mine'){
  if(A.phase==='entry'){i31Fly(e,A.homeX,PLAY.y+100,150,2,dt);if(e.y>=PLAY.y+80)i31Mode(e,'lay');}
  else if(A.phase==='lay'){i31Fly(e,clamp(A.homeX+A.side*200,camLeftX()+65,camRightX()-65),VH-70,112,1.6,dt);
   if(A.cd<=0){const p=i31Point(e,[80,113]);i31Shot(e,p,'mine');A.cd=.6;}if(A.t>3.3){i31Mode(e,'exit');Audio.SFX.turbo?.();}}
  else{i31Fly(e,e.x+A.side*170,VH+200,285,1.5,dt);}
 }else{
  if(A.phase==='entry'){i31Fly(e,A.homeX,A.homeY,155,1.8,dt);if(e.y>A.homeY-12)i31Mode(e,'curve');}
  else if(A.phase==='curve'){const angle=A.t*1.05*A.side,tx=A.homeX+Math.sin(angle)*135,ty=A.homeY+75+Math.sin(A.t*1.3)*65;
   i31Fly(e,clamp(tx,camLeftX()+80,camRightX()-80),ty,115,1.8,dt);
   if(A.cd<=0&&e.y<T.y-80){for(let i=0;i<2;i++)i31Shot(e,i31Gun(e,i),'slug',i>0);A.cd=turretInterval15(.72,[.72,.52,.38][r]);}
   if(A.t>7.0)i31Mode(e,'exit');
  }else i31Fly(e,A.homeX-A.side*180,VH+180,205,1.4,dt);
 }
 if(A.age>19||e.y>VH+130||e.x<camLeftX()-160||e.x>camRightX()+160){e.dead=true;A.beams=[];i31Log(e,'exit');}
};
function i31TurretGun(e){const T=e._modTurret,a=Math.PI/2+s1aDir(T.angle,64)*TAU/64,r=e.w*.96*.405;return{x:e.x+Math.cos(a)*r,y:e.y+Math.sin(a)*r,angle:a};}
modularGroundTurretTick=function(e,dt){if(!e?._i31Turret)return I31.base.turret.apply(this,arguments);if(!i31Live(e)||e.y<PLAY.y+30||e.y>VH-45)return;
 const A=e._i31Ground,T=e._modTurret,P=targetShip(e.x,e.y);A.t+=dt;A.cd-=dt;
 if(A.phase==='wait'){T.angle+=clamp(s1aAngle(Math.atan2(P.y-e.y,P.x-e.x)-T.angle),-turretSpeed15(1.4)*dt,turretSpeed15(1.4)*dt);if(A.cd<=0){A.phase='tell';A.t=0;A.target={x:P.x,y:P.y};if(T.weapon==='sonic')stageRevisionCue(e,'razorbackCharge',.16);else Audio.SFX.bossWeaponCharge?.();}}
 else if(A.phase==='tell'){combatWarningTick(e,'ice-ground',A.t,.85);if(A.t>=.85){const p=i31TurretGun(e);
  if(T.weapon==='sonic')for(const off of[-.13,0,.13])i31Shot(e,{...p,angle:p.angle+off},'sonic',off!==0);
  else i31Shot(e,p,'laser');
  A.phase='wait';A.cd=turretInterval15(T.weapon==='sonic'?3.0:2.1);A.t=0;}}
 T.mode=A.phase;};
function i31Draw(e){const A=e._i31,M=i31M(e),size=i31Size(e),age=A.age;let B=M.banks.heading||M.banks.idle,f=0,head=A.head;
 if(A.model==='eye'){B=M.banks.sequence;head=Math.PI/2;f=A.phase==='tell'?4+Math.min(3,Math.floor(A.t/1.1*4)):A.phase==='fire'?8+Math.min(3,Math.floor(A.t/.85*4)):A.phase==='recover'?12+Math.min(3,Math.floor(A.t/.9*4)):Math.floor(age*4)%4;}
 else if(A.model==='carrier'){B=M.banks.idle;f=Math.floor(age*10)%4;head=Math.PI/2;}
 else if(A.model==='shard'){B=M.banks.drift;f=A.head>Math.PI/2?0:1;head=Math.PI/2;}
 else if(A.model==='mine'&&A.phase==='lay'&&Math.abs(s1aAngle(A.head-Math.PI/2))<.3){B=M.banks.charge;f=Math.floor(age*10)%4;head=Math.PI/2;}
 if(e._dyingT!=null&&M.banks.roll){B=M.banks.roll;f=Math.floor(e._dyingT*14)%B.frames;head=Math.PI/2;}
 i31Blit(B,f,head,e.x+7,e.y+15,size,'#000000',.24);
 if(M.tails.length&&e._dyingT==null)for(const p of M.tails){const q=i31Point(e,p);i31Blit(I31_ART.banks.thruster,Math.floor(age*24)%4,q.angle,q.x,q.y,28);}
 i31Blit(B,f,head,e.x,e.y,size,e.flash>0?hitFlashColor(e):null);e._i31Rendered={key:B.key,frame:f,dir:s1aDir(head,B.dirs),size,head};
 if(A.model==='eye'&&A.phase==='tell')for(const p of A.lanes)combatWarningDraw(e,{...p,ex:p.x+Math.cos(p.angle)*1000,ey:p.y+Math.sin(p.angle)*1000,progress:A.t/1.1,width:16,fieldOnly:true});
 for(const b of A.beams){const step=38;for(let d=step/2;d<1000;d+=step){const x=b.p.x+Math.cos(b.p.angle)*d,y=b.p.y+Math.sin(b.p.angle)*d;
  if(x<camLeftX()-40||x>camRightX()+40||y<PLAY.y-40||y>VH+40)continue;i31Blit(I31_ART.banks.laser,Math.floor(b.t*24)%4,b.p.angle,x,y,56);}}
}
drawEnemy=function(e){if(e?._i31&&!e.dead)return i31Draw(e);
 if(e?._i31Turret&&!e.dead){const key='overhaul_ground_base_3',s=e.w*1.27,im=e.flash>0?xartTint(key,hitFlashColor(e),1):XART.get(key);if(im)ctx.drawImage(im,e.x-s/2,e.y-s/2,s,s);
  i31Blit(I31_ART.banks['turret_'+e._modTurret.weapon],0,e._modTurret.angle,e.x,e.y,e.w*.96,e.flash>0?hitFlashColor(e):null);
  const A=e._i31Ground;if(A.phase==='tell'){const p=i31TurretGun(e);combatWarningDraw(e,{...p,ex:A.target.x,ey:A.target.y,progress:A.t/.85,width:e._modTurret.weapon==='sonic'?40:16,fieldOnly:true});}return;}
 return I31.base.draw.apply(this,arguments);};
drawCombatFinalProjectile=function(b){if(!b?._i31Kind)return I31.base.shot.apply(this,arguments);const k=b._i31Kind,B=I31_ART.banks[k==='laser'?'laser':k],size=k==='mine'?36:k==='sonic'?52:k==='laser'?54:34;
 return i31Blit(B,Math.floor((b.t||0)*22)%B.frames,Math.atan2(b.vy,b.vx),b.x,b.y,size);};
// Sonic's older red pressure renderer precedes the final projectile pass.
ovSonicProjectileDraw=function(b){if(b?._i31Kind)return drawCombatFinalProjectile(b);return I31.base.earlyShot.apply(this,arguments);};
updateEffects=function(dt){const r=I31.base.effects.apply(this,arguments);for(const f of I31.fx)f.t+=dt;I31.fx=I31.fx.filter(f=>f.t<f.life&&i31Live(f.owner));return r;};
drawNavalFlashes=function(){const r=I31.base.flashes.apply(this,arguments);for(const f of I31.fx)i31Blit(I31_ART.banks.muzzle,Math.floor(f.t/f.life*4),f.p.angle,f.p.x+f.owner.x-f.anchor.x,f.p.y+f.owner.y-f.anchor.y,f.size);return r;};
stageLoadBegin=function(n,keys){if(n===3)keys=[...(keys||[]),...Object.values(I31_ART.banks).map(b=>b.key),'overhaul_ground_base_3',...['green','yellow','red'].map(c=>'bmfx_fov_'+c+'_tall')];return I31.base.load.call(this,n,keys);};
beginStage=function(){I31.events=[];I31.fx=[];return I31.base.begin.apply(this,arguments);};
killEnemy=function(e){if(e?._i31){e._i31.beams=[];e._i31.lanes=[];I31.fx=I31.fx.filter(f=>f.owner!==e);i31Log(e,'destroyed');}return I31.base.kill.apply(this,arguments);};
globalThis.BOF_ICE_REFIT={state:I31,art:I31_ART};
