"use strict";
/* Late-stage visibility, live Gang defense, proper fighter bombers and beam hull hits. */
const ON5C={storm:drawS6Storm,bomber:enc30BomberDraw,enemy:drawEnemy,round:rg4Round,gun:ra4Gun,helix:ra4Helix,
 demo:rs1004DemoTick,gang:rg4GangStart,rebelTick:rebelSquadTick,rebelDamage:rebelSquadDamage,
 ship:fr27RebelDrawShip,projectile:drawCombatFinalProjectile,shot:eShootT,attack:ht27Attack,spawn:spawnEnemy};
const ON5_BEAM_DRAW=av3Beam;
av3Beam=function(g,x,y,angle,length,width){
 // Animated nozzles can open to a positive floating-point epsilon. Tiling a
 // hundreds-pixel strip at that width would issue trillions of draw calls.
 // Subpixel beam bodies are invisible; collision/timing still owns the nozzle.
 if(![x,y,angle,length,width].every(Number.isFinite)||width<.5||length<.5)return false;
 return ON5_BEAM_DRAW.apply(this,arguments);
};
function on5Bomber(e){return run.stage===6&&(e?._s6storm==='s6bomber'||e?.type==='s6bomber'||e?.type==='s1jetbomber_b'||e?._s67Bomber||e?._fb2Stealth||e?._mission29?.kind==='bomb');}
spawnEnemy=function(){const e=ON5C.spawn.apply(this,arguments);if(on5Bomber(e))gp4BomberDurability(e);return e;};
function on5BomberDraw(e,dir){if(!on5Bomber(e))return false;if(e.dead||e._dyingT!=null)return false;
 const A=e._fb2Stealth||e._mission29||e._s6Strike||{},role=A.role==='red'||!A.role&&(e._side??e._dir??1)>0?'red':'green',direction=dir||A.direction||(e._dir<0?'west':'east');
 e._on5Bomber=role;const size=e._s67Draw||104;
 fb2Warm();if(!fb2SheetCell('fb2_stealth_'+role,FB2_DIR_FRAME[direction]??2,e.x-size/2,e.y-size/2,size,e))return true;
 e._drawW=e._drawH=size;ON5.draws['bomber-'+role]=(ON5.draws['bomber-'+role]||0)+1;return true;}
drawEnemy=function(e){if(on5BomberDraw(e))return;return ON5C.enemy.apply(this,arguments);};
drawS6Storm=function(e){if(on5BomberDraw(e,e._dir<0?'west':'east'))return true;return ON5C.storm.apply(this,arguments);};
enc30BomberDraw=function(e,dir){if(on5BomberDraw(e,dir))return true;return ON5C.bomber.apply(this,arguments);};
// A held laser is a column, not a point at the squad controller's center. Each
// real hull gets its own burn clock; cloak hides acquisition but not blind fire.
function on5RebelLaser(beam,dt,flame=false){const b=boss,R=b?._rebels;if(!b||!bossActive||b.dead||b._noHit||!R?.frIntro?.done||R.gang1004?.scene)return;
 beam._on5Burn??=new Map();for(const q of R.ships){if(q.dead||q.mode==='entry'||q.warp>0)continue;
  const old=Math.max(0,(beam._on5Burn.get(q)||0)-dt);beam._on5Burn.set(q,old);
  const hit=flame?flameHit(beam,q.x,q.y,62,70):q.y+35>=(beam.top??-20)&&q.y-35<=(beam.bot??player.y-14)&&Math.abs(beam.x-q.x)<=31+(beam.w||12)/2;
  if(!hit||old>0)continue;R.hit=q.i;R.frHit=null;_lastHitX=q.x;_lastHitY=q.y;
  hitBoss((beam.dmg||1)*(flame?elementMultiplier(attackElement('flame'),flameIsIce()?'icebreath':'flamethrower'):1));weaponHitSfx(flame?attackElement('flame'):'laser');
  beam._on5Burn.set(q,flame?FLAME_TICK:.05);on5Log('rebelLaserHit',{pilot:q.key,kind:beam.kind});
 }}
const ON5_COLE_TARGET=_coleNearest;
_coleNearest=function(x,y){if(!boss?._rebels||!bossActive)return ON5_COLE_TARGET.apply(this,arguments);
 let best=ON5_COLE_TARGET.apply(this,arguments);if(best===boss)best=null;
 let distance=best?dist2(x,y,best.x,best.y):Infinity;const R=boss._rebels;
 if(boss.dead||boss._noHit||!R.frIntro?.done||R.gang1004?.scene)return best;
 for(const q of R.ships){if(q.dead||q.mode==='entry'||q.warp>0||q.frCloak>0)continue;
  const d=dist2(x,y,q.x,q.y);if(d>=distance)continue;distance=d;
  best=retinaDynamicPiece(boss,'on5-cole-'+q.key,'rival',()=>({x:q.x,y:q.y,hp:q.hp,dead:q.dead||q.mode==='entry'||q.warp>0||q.frCloak>0}),
   dmg=>{R.hit=q.i;R.frHit=null;hitBoss(dmg);},62,70);
 }return best;
};
function on5FinaleLaser(beam,dt,flame=false){const b=boss;if(!r30Live(b)||b.enter||b._noHit||beam._bt>0)return;
 const targets=retinaBossTargets(b).filter(q=>!q.dead&&q.hp>0&&
  (flame?flameHit(beam,q.x,q.y,q.w,q.h):q.y+q.h/2>=(beam.top??-20)&&q.y-q.h/2<=beam.bot&&Math.abs(q.x-beam.x)<q.w/2+beam.w/2));
 // The foremost intersecting plate absorbs a pulse. Covered modules are not
 // hit a second time through the code shield during the same pulse.
 targets.sort((a,b)=>(b.y+b.h/2)-(a.y+a.h/2));
 // A projected shield sits in front of its owner's plate even when the whole
 // body's rectangular bounds extend below the projection's actual position.
 const q=targets.find(t=>t._retinaId?.startsWith('code-wall-1003d'))||targets[0];if(!q)return;
 q._retinaHit(beam.dmg*(flame?elementMultiplier(attackElement('flame'),flameIsIce()?'icebreath':'flamethrower'):1));
 weaponHitSfx(flame?attackElement('flame'):'laser');beam._bt=flame?FLAME_TICK:.05;
}
rg4GangStart=function(b,G){if(G.gang||b._rebels.frStageX||b._rebels.ships.length!==5)return false;
 G.gang=true;G.rescueAt=G.age+11;b._noHit=false;
 for(const q of b._rebels.ships)if(!q.dead){q._on5Guard={hp:Math.ceil(q.max*.065),max:Math.ceil(q.max*.065),t:0,flash:0};q.rg4.turbo=['rook','jace'].includes(q.key);}
 const speaker=b._rebels.ships.find(q=>q.key==='voss'&&!q.dead)||b._rebels.ships.find(q=>!q.dead);
 if(speaker)rf28Callout(b._rebels,'GANG MODE INITIATE!',speaker.x,speaker.y+62,RA4_COLORS[speaker.key],2.4,8);
 av3Sound('laser_charge',.75);rg4Log(G,'gangStart',{live:true,wounded:b._rebels.ships.filter(q=>q.hp<=q.max*.5).length});return true;
};
rebelSquadDamage=function(b,dmg){const R=b._rebels,q=R.ships[R.hit],H=q?._on5Guard;
 if(H&&H.hp>0&&!q.dead&&R.frIntro?.done&&!R.gang1004?.scene&&q.mode!=='entry'&&!(q.warp>0)&&dmg>0){
  H.hp=Math.max(0,H.hp-dmg);H.flash=.12;R.hit=-1;av3Sound('impact_energy',.55,.10);
  if(!H.hp){rg4FX(R.gang1004,3,q.x,q.y,105,.5);av3Sound('shield_break',.7);delete q._on5Guard;}return;
 }return ON5C.rebelDamage.apply(this,arguments);};
rebelSquadTick=function(b,dt){const r=ON5C.rebelTick.apply(this,arguments);for(const q of b._rebels.ships){const H=q._on5Guard;if(!H)continue;
 H.t+=dt;H.flash=Math.max(0,H.flash-dt);if(q.dead||H.t>=4.0){if(!q.dead)rg4FX(b._rebels.gang1004,3,q.x,q.y,90,.5);delete q._on5Guard;}}return r;};
fr27RebelDrawShip=function(q){const r=ON5C.ship.apply(this,arguments),H=q._on5Guard;if(H){
 rg4Cell(3,Math.floor(H.t*12)%6,q.x,q.y,98,108,.85,RA4_COLORS[q.key]);if(H.flash>0)rg4Cell(3,Math.floor(H.t*12)%6,q.x,q.y,98,108,.95,'#ffffff');}return r;};
ra4Gun=function(q,G,dt){if(G.scene||q.rg4?.act?.phase==='fire'||q.rg4?.act?.phase==='row')return;
 const before=q.rg4?.gunN,r=ON5C.gun.apply(this,arguments);if(q.rg4&&q.rg4.gunN!==before)q.rg4.gunCd=Math.max(q.rg4.gunCd,G.gang?.95:1.18);return r;};
rg4Round=function(q,a,speed,kind,extra){if(extra?._ra4Slug&&!extra?._ra4Gun)a=Math.PI/2;return ON5C.round.call(this,q,a,speed,kind,extra);};
ra4Helix=function(q,G,A){const r=ON5C.helix.apply(this,arguments),o=G.ord.at(-1);if(o?.kind==='helix'){o.vx=0;o.vy=380;o.life=1.15;}return r;};
rs1004DemoTick=function(R,I,dt){const r=ON5C.demo.apply(this,arguments),S=I.showcase,D=S?.current,q=D?.q;
 if(S)for(const f of S.fx){if(f.kind==='ball'){f.vx=0;f.vy=520;f.life=1.25;}if(f.kind==='slug'){f.vx=0;f.vy=640;f.life=1.0;}}
 if(D?.kind==='turbo'&&D.released&&q&&!q.dead){const after=I.rows[I.i].text.length/32+.12,t=D.t-Math.max(1.25,after);
  if(t>=.45){const span=viewW()+220,pass=Math.floor((t-.45)*1250/span),u=((t-.45)*1250)%span,dir=pass%2?-1:1;
   q.x=dir>0?camLeftX()-110+u:camRightX()+110-u;q.y=PLAY.y+100+(pass%2)*60;q.rfHeading=dir>0?0:Math.PI;
   for(const f of S.fx)if(f.kind==='dash'&&f.t<dt*1.1){f.x=q.x;f.y=q.y;f.a=q.rfHeading;}
  }}return r;};
// Readable authored rounds retain exact collision dimensions and shootability.
drawCombatFinalProjectile=function(p){if([6,7,8].includes(run.stage)&&!p.dead&&['mg','s6tracer','s7laser'].includes(p.kind)&&!p._ra4MiniBall){
 const w=p.kind==='s7laser'?10:7,h=p.kind==='s7laser'?26:19,a=Math.atan2(p.vy||0,p.vx||0)-Math.PI/2;
 if(cf1004Cell('yellow',p.t||efxClock,p.x,p.y,w,h,a)){ON5.draws.tracers=(ON5.draws.tracers||0)+1;return true;}
 }return ON5C.projectile.apply(this,arguments);};
// Reduce overlapping ordinary late-stage fire without slowing boss signatures.
eShootT=function(x,y,a,speed,kind,opt){const n=run.stage,ordinary=[6,7,8].includes(n)&&!bossActive&&!subBossActive&&['mg','s6tracer','s7laser'].includes(kind);
 if(ordinary){const owner=opt?.owner,cap=diffKey==='easy'?22:diffKey==='furious'||diffKey==='insanity'?44:32;
  if(eBullets.filter(q=>!q.dead&&['mg','s6tracer','s7laser'].includes(q.kind)).length>=cap)return{dead:true,x,y,vx:0,vy:0};
  if(owner&&owner._on5ShotAt!=null&&efxClock-owner._on5ShotAt<.08)return{dead:true,x,y,vx:0,vy:0};if(owner)owner._on5ShotAt=efxClock;
  speed*=.90;
 }return ON5C.shot.call(this,x,y,a,speed,kind,opt);};
// Both musical variants can use the campaign Hammer's gun/spell combos as well
// as boomerang, whirlwind and leap chains, while keeping their music clocks.
ht27Attack=function(b,d){const n=d.attack%6;if(n===4||n===5){d.attack++;d.mode='attack';d.t=0;const h=b._hammer;h.phasePending=false;h.comboPending=false;
  if(n===4)hammerChainStart(b);else hammerSpellStart(b);return;
 }return ON5C.attack.apply(this,arguments);};
// Restore the retained instrumental, never the premix containing robot chants.
BOFA.music.hama='assets/game/music/HAMA_Instrumental.mp3';
if(Snd?.music.hama){const m=Snd.music.hama;m.pause();m.src=BOFA.music.hama;m.preload='none';m.loop=true;}
hamaRecordedVocals1001=function(){return false;};
hamaSing=function(){};
hamaLyricsTick=function(b,d){if(d.hama)d.hama.lines=[];};
const ON5_CONTAINER=breakContainer;
breakContainer=function(p){if(!p._on5Pill)return ON5_CONTAINER.apply(this,arguments);
 p.dead=true;crateBreak(p.x,p.y,'#d3f0ff');powerups.push({kind:p._on5Content,x:p.x,y:p.y,vy:.65,t:0,w:24,h:24,bob:0});Audio.SFX.expSmall?.();};
