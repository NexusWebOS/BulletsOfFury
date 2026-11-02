"use strict";
/* 1101 (Mike, after the Stage-7 review films): the Brood Sentinel's robot flies are larger, can be shot down and
   burst into blood; each maw attack fans flies out three times before the next state; the lunge winds both scythe
   claws outward and back, then swings them forward across the player. Late layer over stage7_amplify_1101 (S711):
   its actor, shield, HP, hit flash, death and the claw/hull art all stay with that owner. */
const BS111={blood:{key:'bs111_blood_burst',path:'assets/game/levels/stage_07/enemies/brood_1101/blood_burst.png',cell:128,frames:8,life:.42,size:76},
 fx:[],flies:[],tracked:new WeakSet(),events:[],
 base:{brood:s711Brood,proj:s711Projectile,warn:s711DrawWarning,fx:updateEffects,intercept:enemyOrdnanceCanIntercept,flashes:drawNavalFlashes,load:stageLoadBegin,begin:beginStage}};
XART._src[BS111.blood.key]=BS111.blood.path;
function bs111Log(event,data={}){BS111.events.push({event,t:efxClock,...data});if(BS111.events.length>600)BS111.events.shift();}
// Per rank (Normal/Hard/Furious): flies per fan, fan width (rad), gap between fans, fly speed, fly HP.
const BS111_FAN={n:[7,9,11],spread:[1.45,1.65,1.85],gap:[.62,.54,.46],speed:[2.4,2.6,2.8],hp:[1,1,2]};
function bs111Fan(e,k){const A=e._s711,r=s711Rank(),M=s711M(e),T=targetShip(e.x,e.y),p=s711Point(e,M.mouth);
 const n=BS111_FAN.n[r],S=BS111_FAN.spread[r],step=S/(n-1),centre=Math.atan2(T.y-p.y,T.x-p.x),off=[0,.5,-.5][k%3]*step;let made=0;
 // Consecutive fans shift by half a lane, so the safe gaps move between fans.
 for(let i=0;i<n;i++){const b=s711Shot(e,{...p,angle:centre-S/2+i*step+off},'fly',BS111_FAN.speed[r],i>0,0);if(!b)continue;made++;
  Object.assign(b,{_s711Kind:'broodfly',_shootable:true,_weaponProof:false,_energyOrdnance:true,homing:false,hp:BS111_FAN.hp[r],w:30,h:30,life:6,_bsPhase:i*1.7+k});delete b._s711Steer;}
 bs111Log('fan',{fan:k,flies:made,of:n});return made;}
s711Brood=function(e,dt){const A=e._s711;
 if(!['claw-tell','claw','recover','mouth-fire'].includes(A.phase))return BS111.base.brood.apply(this,arguments);
 const r=s711Rank(),T=targetShip(e.x,e.y),D=Math.PI/2,back=[2.25,2.35,2.45][r],strike=-.6;
 if(A.phase==='claw-tell'){
  // Wind-up: both scythes fan outward and back over the shoulders, then quiver while the warning commits.
  if(!A.target||A.t<A.warm*.55)A.target={x:T.x,y:T.y};
  const u=clamp(A.t/(A.warm*.8),0,1),ease=u*u*(3-2*u),quiver=u>=1?Math.sin(A.t*46)*.05:0;
  A.angles=[D+back*ease+quiver,D-back*ease-quiver];combatWarningTick(e,'s711-claws',A.t,A.warm);
  if(A.t>=A.warm){A.start={x:e.x,y:e.y};A.end={x:clamp(A.target.x,camLeftX()+110,camRightX()-110),y:Math.min(A.target.y-85,PLAY.y+viewH()*.65)};
   s711Phase(e,'claw');combatAudio0927(e,'combatServo0927',.4);if(typeof av3Sound==='function')av3Sound('claw_lunge',.75,.2);}
 }else if(A.phase==='claw'){
  // The body launches with the claws still drawn back; the scythes then swing forward across the target.
  const u=clamp(A.t/[.66,.6,.54][r],0,1),out=u<.45?Math.sin(u/.45*Math.PI/2):u<.75?1:Math.cos((u-.75)/.25*Math.PI/2),
   s=clamp((u-.32)/.3,0,1),sw=s*s;
  e.x=A.start.x+(A.end.x-A.start.x)*out;e.y=A.start.y+(A.end.y-A.start.y)*out;
  A.angles=[D+back+(strike-back)*sw,D-back-(strike-back)*sw];A.swing=s;
  if(s>0&&u<.8)for(let i=0;i<2;i++){const q=s711Part(e,i);for(const seat of seatList())withSeat(seat,()=>{if(!player.dead&&!player.out&&player.invuln<=0&&s81003Distance(player.x,player.y,{x:q.x,y:q.y,ex:q.tip.x,ey:q.tip.y})<16)playerHit('Brood Sentinel claw');});}
  if(u>=1){e.x=A.start.x;e.y=A.start.y;s711Phase(e,'recover');}
 }else if(A.phase==='recover'){A.angles=A.angles.map(a=>a+clamp(s1aAngle(D-a),-dt*3.5,dt*3.5));if(A.t>.7)s711Tell(e,'mouth-open',[1.1,1,.9][r]);}
 else if(A.phase==='mouth-fire'){
  // Three fans of flies, then the maw closes and the claw cycle begins again.
  if(A.round<3){if(A.beat<=0){bs111Fan(e,A.round);A.round++;A.beat=BS111_FAN.gap[r];}}
  else if(A.beat<=0)s711Phase(e,'mouth-close');
 }
 if(A.age>24){e.y-=150*dt;if(e.y<-160)e.dead=true;}
};
// The maw warning shows the fan it is about to release: both edges and the centre lane.
s711DrawWarning=function(e){const A=e._s711;if(A?.model!=='brood'||A.phase!=='mouth-open'||A.cancelled)return BS111.base.warn.apply(this,arguments);
 const M=s711M(e),r=s711Rank(),p=s711Point(e,M.mouth),T=targetShip(e.x,e.y),c=Math.atan2(T.y-p.y,T.x-p.x),S=BS111_FAN.spread[r];
 for(const a of [c-S/2,c,c+S/2])combatWarningDraw(e,{x:p.x,y:p.y,ex:p.x+Math.cos(a)*420,ey:p.y+Math.sin(a)*420,width:a===c?20:14,progress:clamp(A.t/A.warm,0,1),fieldOnly:true});};
enemyOrdnanceCanIntercept=function(b){return b?._s711Kind==='broodfly'?true:BS111.base.intercept.apply(this,arguments);};
s711Projectile=function(b){if(b?._s711Kind!=='broodfly')return BS111.base.proj.apply(this,arguments);
 const B=S711_ART.banks.fly,age=projectileVisualAge(b),a=Math.atan2(b.vy,b.vx);return v31Blit(B,Math.floor(age*32)%B.frames,a,b.x,b.y,64,b._bsHit>0?'#ffffff':null);};
function bs111OnScreen(x,y){return y>viewTopY()-6&&y<VH+6&&x>camLeftX()-6&&x<camRightX()+6;}
updateEffects=function(dt){const r=BS111.base.fx.apply(this,arguments);
 for(const f of BS111.fx)f.t+=dt;BS111.fx=BS111.fx.filter(f=>f.t<BS111.blood.life);
 // A fly that dies before its lifetime ends (shot down, cleared, or striking the pilot) bursts into blood.
 const live=new Set(eBullets);
 BS111.flies=BS111.flies.filter(b=>{if(!b.dead&&live.has(b)){b._bsLast={x:b.x,y:b.y};return true;}
  const q=b._bsLast||b;if((b.t||0)<(b.life||6)-.06&&bs111OnScreen(q.x,q.y)){BS111.fx.push({x:q.x,y:q.y,t:0,flip:Math.random()<.5});
   if(typeof av3Sound==='function')av3Sound('impact_flesh',.55,.05);bs111Log('blood',{x:Math.round(q.x),y:Math.round(q.y),t:+(b.t||0).toFixed(2)});}
  return false;});
 for(const b of eBullets)if(b?._s711Kind==='broodfly'&&!b.dead){
  if(!BS111.tracked.has(b)){BS111.tracked.add(b);BS111.flies.push(b);b._bsHp=b.hp;}
  if(b.hp<b._bsHp){b._bsHit=.07;b._bsHp=b.hp;}b._bsHit=Math.max(0,(b._bsHit||0)-dt);
  // Wing-beat wobble keeps the fan alive without steering it at the pilot.
  const a=Math.atan2(b.vy,b.vx)+Math.sin((b.t||0)*9+b._bsPhase)*.55*dt,v=Math.hypot(b.vx,b.vy);b.vx=Math.cos(a)*v;b.vy=Math.sin(a)*v;}
 return r;};
drawNavalFlashes=function(){const r=BS111.base.flashes.apply(this,arguments),B=BS111.blood;if(!BS111.fx.length||!XART.rdy(B.key))return r;
 const im=XART.get(B.key);ctx.save();ctx.imageSmoothingEnabled=false;
 for(const f of BS111.fx){const fr=Math.min(B.frames-1,Math.floor(f.t/B.life*B.frames));ctx.save();ctx.translate(Math.round(f.x),Math.round(f.y));if(f.flip)ctx.scale(-1,1);
  ctx.drawImage(im,fr*B.cell,0,B.cell,B.cell,-B.size/2,-B.size/2,B.size,B.size);ctx.restore();}
 ctx.restore();return r;};
stageLoadBegin=function(n,keys){if(n===7)keys=[...(keys||[]),BS111.blood.key];return BS111.base.load.call(this,n,keys);};
beginStage=function(){BS111.fx=[];BS111.flies=[];BS111.events=[];return BS111.base.begin.apply(this,arguments);};
globalThis.BOF_BROOD_SENTINEL=BS111;
