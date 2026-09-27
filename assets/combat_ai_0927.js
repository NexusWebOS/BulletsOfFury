"use strict";
/* Reactions change intent and actual motion, never the player's/camera's position.
   Authored routes, ground anchors, bosses and their warning directors retain ownership. */
let ai27Context=null;
function ai27Level(){return diffKey==='furious'||diffKey==='insanity'?2:diffKey==='hard'?1:0;}
function ai27Owns(e){return !!(e&&!e.dead&&e._dyingT==null&&!e.prop&&!e._prop&&e.pattern!=='prop'&&!isSetPiece(e));}
function ai27Air(e){
  if(e._vkind==='tank'||e.ground||e.inPlace||e._tur||e._bunker||/tank|turret|barge|mine|canister|beacon|pillar|carrier|walker|pipe/.test(e.type||''))return false;
  return !!(isJetEnemy(e)||e._dr||e._droid||e._s7toxic||e._s9void||e._s8mega||e._s5space||e._s6storm||
    ['ash','skim','eye','lance'].includes(e._volc)||e.pattern==='sewer');
}
function ai27Begin(e,dt){
  const previous=ai27Context;ai27Context=ai27Owns(e)?e:null;
  if(!ai27Context)return previous;
  const n=ai27Level(),A=e._ai27||(e._ai27={seen:0,cd:.45,read:0,dodge:0,dir:0,lastHp:e.hp,flinch:0,hitCd:0,reactions:0,blocked:0,shots:0});
  const L=camLeftX(),R=camRightX(),visible=e.x>=L+12&&e.x<=R-12&&e.y>=PLAY.y+8&&e.y<VH-30;
  A.seen=visible?A.seen+dt:0;A.visible=visible;A.cd=Math.max(0,A.cd-dt);A.hitCd=Math.max(0,A.hitCd-dt);A.flinch=Math.max(0,A.flinch-dt);
  if(e.hp<A.lastHp&&A.hitCd<=0){A.flinch=[.16,.12,.09][n];A.hitCd=.85;A.reactions++;}
  A.lastHp=e.hp;A.air=ai27Air(e);A.dx=0;
  if(!A.air||!visible||e._frozen||e._mercuryLock>0||e._shieldStun>0||e._jetManeuver||e._rollT!=null||['curl','cross','flee'].includes(e._phase))return previous;
  if(A.dodge>0){const step=Math.min(dt,A.dodge);A.dodge-=step;A.dx=A.dir*(105+n*22)*step;if(A.dodge<=0)A.cd=[4.6,3.6,2.8][n];return previous;}
  if(A.read>0){A.read=Math.max(0,A.read-dt);if(A.read===0){A.dodge=.30;A.reactions++;}return previous;}
  if(A.cd>0||A.seen<.65||e.y>player.y-65)return previous;
  // Predict actual projectile interception; nearby parallel shots are not threats.
  for(const q of pBullets){
    if(!q||q.dead||q.ally||q.kind==='beam'||q.kind==='firewhip'||q._launchDelay>0)continue;
    const vy=(q.vy||0)*60;if(vy>=-20)continue;
    const t=(e.y-q.y)/vy;if(t<.10||t>[.50,.42,.34][n])continue;
    const x=q.x+(q.vx||0)*60*t;if(Math.abs(x-e.x)>(e.w||30)*.45+8)continue;
    const pad=Math.max(22,(e.w||30)*.45),roomL=e.x-(L+pad),roomR=R-pad-e.x;
    let dir=x>e.x?-1:1;if(dir<0&&roomL<48)dir=1;if(dir>0&&roomR<48)dir=-1;
    const lane=e.x+dir*42;
    if(Math.min(roomL,roomR)<-5||enemies.some(o=>o!==e&&!o.dead&&Math.abs(o.x-lane)<36&&Math.abs(o.y-e.y)<50)){A.cd=.7;break;}
    A.dir=dir;A.read=[.19,.15,.11][n];A.cd=.6;break;
  }
  return previous;
}
function ai27End(e,previous){
  const A=e&&e._ai27;
  if(A&&A.dx&&!e.dead&&e._dyingT==null){const pad=Math.max(16,(e.w||30)*.4);e.x=clamp(e.x+A.dx,pad,worldWidth()-pad);e._bank=clamp((e._bank||0)+A.dir*.10,-.35,.35);}
  ai27Context=previous;
}
function ai27ShotBlocked(){
  const e=ai27Context,A=e&&e._ai27;if(!A)return false;
  const p=targetShip(e.x,e.y),near=Math.hypot(p.x-e.x,p.y-e.y)<Math.max(66,Math.max(e.w||24,e.h||24)*.48+22);
  const blocked=e.dead||e._dyingT!=null||!A.visible||A.seen<[.50,.40,.32][ai27Level()]||A.flinch>0||near;
  if(blocked)A.blocked++;else A.shots++;
  return blocked;
}
// Field enemies only: bosses/directors and detached projectile splits have no context.
function ai27Release(fn){return function(...a){if(ai27ShotBlocked())return {x:a[0],y:a[1],vx:0,vy:0,w:0,h:0,dead:true,_ai27Held:true};return fn.apply(this,a);};}
eShootT=ai27Release(eShootT);eShoot=ai27Release(eShoot);eMG=ai27Release(eMG);eGreenLaser=ai27Release(eGreenLaser);
eMissile=ai27Release(eMissile);eMissileHoming=ai27Release(eMissileHoming);eHomingMissile=ai27Release(eHomingMissile);
droneFire=ai27Release(droneFire);ex8Fire=ai27Release(ex8Fire);

function ally27Tick(q,dt){
  q.rollCool=Math.max(0,(q.rollCool||0)-dt);q.somerCool=Math.max(0,(q.somerCool||0)-dt);
  const old=q.dodgeT||0;q.dodgeT=Math.max(0,old-dt);
  if(old>0&&q.dodgeT===0){if(q.dodgeMode==='somer')q.somerCool=SS_COOL;else q.rollCool=BR_COOL;}
  q.dodgeCd=q.dodgeT>0?q.dodgeT:Math.min(q.rollCool,q.somerCool);
}
function ally27Dodge(q,danger,left,right,top,bottom){
  if(q.dodgeT>0)return false;
  const preferred=q.slot%3===0?'somer':'roll',ready=m=>!(m==='somer'?q.somerCool:q.rollCool);
  const mode=ready(preferred)?preferred:ready(preferred==='roll'?'somer':'roll')?(preferred==='roll'?'somer':'roll'):null;
  if(!mode)return false;
  let dir=q.x<danger.x?-1:1;if(q.x<left+65)dir=1;if(q.x>right-65)dir=-1;
  q.dodgeMode=mode;q.dodgeDuration=mode==='somer'?SS_DUR:BR_DUR;q.dodgeT=q.dodgeDuration;
  q.evadeX=clamp(q.x+(mode==='roll'?dir*BR_DASH:0),left,right);
  q.evadeY=clamp(q.y-(mode==='somer'?SS_SURGE:0),top,bottom);
  q.dodgeCd=q.dodgeDuration;
  if(Audio.SFX){const f=mode==='roll'?Audio.SFX.arcBarrelRoll:Audio.SFX.somersault||Audio.SFX.dash;if(f)f();}
  return true;
}
// Wing support reduces pressure; eight friendly pilots are not a difficulty multiplier.
s6PressureMultiplier=function(){const n=s6Wing?s6Wing.ships.filter(q=>q.phase==='fight').length:0;return [ .88,.96,1 ][ai27Level()]-(n>=6?.16:n>=3?.10:n>0?.04:0);};
s6OnslaughtTick=function(W,dt){
  // Encounter timers pause wave progress; ally weapons still recharge in combat.
  W.combatTime=(W.combatTime||0)+dt;
  if(bossActive||subBossActive||s6OpeningActive()||W.choice||W.fake)return;
  W.reinforce=(W.reinforce||0)-dt;
  const live=enemies.filter(e=>!e.dead&&e._dyingT==null&&!e.prop&&!e._prop).length,n=ai27Level();
  if(W.reinforce<=0&&live<[2,3,4][n]){W.reinforce=[8.5,7.5,6.5][n];const i=(W.reinforceSerial=(W.reinforceSerial||0)+1);
    spawnEnemy(i%4===0?'s6bomber':'s6dart',camLeftX()+45+((i*.618)%1)*(viewW()-90),-75,{});}
};
function ally27ArsenalTurn(q){
  const W=s6Wing;if(!W)return true;
  const t=W.combatTime||0;if((W.heavyUntil||0)>t)return false;
  W.heavyOwner=q.key;W.heavyUntil=t+.70;return true;
}
// The Rival squad shares a release window too. Five independent clocks used to
// stack a dash, lightning circles and two fan volleys on the same frame.
function rival27Turn(R,q){
  if((R.releaseAt||0)>R.t||R.ships.some(s=>!s.dead&&s!==q&&s.mode==='charge'))return false;
  const start=((R.lastRelease==null?-1:R.lastRelease)+1)%R.ships.length;
  let next=null;for(let i=0;i<R.ships.length;i++){const s=R.ships[(start+i)%R.ships.length];if(!s.dead&&s.mode==='fight'&&!(s.stun>0)&&s.cd<=0){next=s;break;}}
  if(next!==q)return false;
  R.lastRelease=q.i;R.releaseAt=R.t+[.92,.76,.60][ai27Level()];return true;
}
function rival27Warning(q,dt){
  if(q.mode!=='charge')return;
  combatWarningTick(q,'rival27-dash-'+q.i,Math.min(q.t,.90),.90);
}
function rival27Draw(b,front){
  for(const q of b._rebels.ships){
    if(q.dead||q.mode!=='charge'||q.t>=.90)continue;
    combatWarningDraw(q,{x:q.chargeX,y:q.homeY,ex:q.chargeX,ey:VH,progress:q.t/.90,width:72,fieldOnly:!front,alertOnly:front});
  }
}
