'use strict';
/* October 10: the orb rework (Mike: "all orbs in game need to be more powerful as they are the most
   underwhelming weaponry in the entire game, and some of them even break and just disappear with no
   effects, no blasts, no nothing and you just die... the ice orb pierces and damages as intended and
   shoots shards, just needs more damage. the rest, rework/balance/effects").

   This file owns the player orb (weapon slot 5, every variant and forge element) and Yuri's
   lightning orb. Measured before the rework at level 3 against a fixed six-target row
   (_BUILD_SOURCE/probe_orbs_1010.py): MG 78 dps, spread 98, laser 180, every orb 64-71 and chrome 32.

   1. Damage scales from the orb's own table (FB10_ORB) by level, not from the old flat 2-3 per hit.
      Contact hits now name the orb as the damaging round, so elemental crits and forge infusions
      apply to the orb body as well as its shards.
   2. Every orb ending detonates: a damaging blast with the element's authored burst, a flash ring,
      sound and shake. That includes orbs removed by any other system (shields, wipes, absorbers),
      which are caught after the frame and detonated where they were last seen.
   3. Each element has its own job. Ice / fire-ice / lightning / prism / chrome / dark pierce;
      fire, magma, toxic, kinetic and water burst on contact.
        ice        pierce, shard spray, frost shatter that slows what it catches
        fire-ice   Freezer's thermoshock: pierces and freezes, detonates fire and ice
        fire       contact fireball: big blast, sets everything in it burning, fire-shard ring
        magma      the forged fire orb: a larger, heavier fireball
        toxic      contact burst that leaves a poison cloud ticking for 2.6 s
        kinetic    contact sonic shockwave that knocks the formation back
        water      contact tidal splash that soaks targets and raises a water geyser
        lightning  pierce; its end discharges chain lightning through the formation
        prism      pierce; its end refracts into a radial fan of piercing rays
        chrome     pierce; mirrors enemy rounds it passes and bursts in a wide mirror shell
        dark       the existing void rift, harder, with a visible collapse blast
   4. One orb at level 1-2, two from level 3 and three at level 5, with a 0.3 s relaunch gap
      (assets/game.js pShoot).
   5. Orbs lean toward the nearest target ahead (fb10Steer), and their encounter contact searches
      the whole orb radius for a live part (fb10FindSolid), so they connect with strafing bosses
      and modular minibosses instead of sailing past them.
   Verification: docs/ORBS_1010.md and _BUILD_SOURCE/probe_orbs_1010.py.
*/
const FB10_ORB={
 // Per level-1 orb. hit = contact (every 0.16 s per target for piercing orbs), shard = each shard,
 // blast = to every enemy in the blast, boss = the blast's strike on a boss/miniboss part. Contact
 // orbs refire fast at close range, so their crowd blast is the lower figure and their boss blast
 // the higher one; piercing orbs earn their boss damage by sitting on the hull.
 //          contact  shard  blast  boss  radius  pierce
 ice:      {hit:7,  shard:2.2, blast:14, boss:16, r:70,  pierce:true},
 fireice:  {hit:8,  shard:2.4, blast:18, boss:20, r:78,  pierce:true},
 fire:     {hit:14, shard:2.0, blast:18, boss:40, r:80,  pierce:false},
 magma:    {hit:18, shard:2.4, blast:24, boss:52, r:96,  pierce:false},
 toxic:    {hit:12, shard:1.6, blast:12, boss:28, r:74,  pierce:false},
 kinetic:  {hit:14, shard:1.8, blast:15, boss:34, r:84,  pierce:false},
 water:    {hit:13, shard:1.8, blast:14, boss:32, r:86,  pierce:false},
 lightning:{hit:6,  shard:.9,  blast:14, boss:16, r:72,  pierce:true},
 prism:    {hit:7,  shard:2.0, blast:14, boss:16, r:70,  pierce:true},
 chrome:   {hit:8,  shard:2.2, blast:18, boss:20, r:84,  pierce:true},
 dark:     {hit:8,  shard:2.0, blast:20, boss:24, r:80,  pierce:true},
};
const FB10_COLOR={ice:'#bfe8ff',fireice:'#9fd8ff',fire:'#ff7331',magma:'#ff451c',toxic:'#96ec38',kinetic:'#8ab4ff',
 water:'#3fa7ff',lightning:'#ffe03a',prism:'#e0b3ff',chrome:'#d6e2ee',dark:'#b46cff'};
const FB10_PALETTE={ice:'blue',fireice:'blue',fire:'red',magma:'red',toxic:'green',kinetic:'blue',water:'blue',lightning:'orange',
 prism:'purple',chrome:'white',dark:'purple'};
const FB10_SHARD={ice:[1,.10],fireice:[1,.10],fire:[0,.10],magma:[0,.10],toxic:[.45,.23],lightning:[.7,.15],prism:[.65,.17],
 kinetic:[.85,.13],water:[.6,.19],chrome:[.6,.17],dark:[0,.24]};
let fb10Clouds=[];
function fb10Lv(b){return clamp(b.lv||1,1,5);}
function fb10K(b){return 1+.25*(fb10Lv(b)-1);}              // x1 at level 1, x1.5 at 3, x2 at 5
function fb10Kind(b){
 if(b._wvar==='magmaorb')return 'magma';
 const el=b._el||(b._ts?'fireice':b._fire?'fire':'ice');
 return FB10_ORB[el]?el:'ice';
}
function fb10Init(b){
 if(b._fb10)return b._fb10;
 const k=fb10Kind(b),S=FB10_ORB[k],K=fb10K(b),
  // Freezer's authored stage bonuses (ice breath on 2, thermoshock on 3) keep applying on top
  pre=typeof elementMultiplier==='function'?elementMultiplier(b._el,b._ts?'fireice':'orb'):1;
 b._hit||=[];b._ht??=0;b._bt??=0;b._sbt??=0;b.spin??=0;b.frame??=0;
 b.dmg=S.hit*K*pre;
 return b._fb10={k,K,S,shard:S.shard*K*pre,blast:S.blast*K*pre,boss:S.boss*K*pre,r:S.r+fb10Lv(b)*8,last:{x:b.x,y:b.y},mirrorCd:0};
}
// Every damaging touch names the orb as the live round: elemental crits and forge infusions apply.
function fb10As(b,fn){const prev=_dmgBullet;_dmgBullet=b;try{fn();}finally{_dmgBullet=prev;}}
/* Modular encounters only take damage on their live parts (the Razorback seals its centre plate
   until both gun pods break, for one). An orb is a big round, so instead of testing its centre
   point it looks for the nearest solid point anywhere inside its radius, and strikes there so
   the encounter routes the damage to that part. Measured before: the orb body never touched the
   Razorback at all (13 dps from stray shards against 942 HP). */
function fb10FindSolid(x,y,R,test){
 if(test(x,y))return {x,y};
 for(const f of [.35,.7,1])for(let i=0;i<12;i++){const a=i*TAU/12+f;const px=x+Math.cos(a)*R*f,py=y+Math.sin(a)*R*f;if(test(px,py))return {x:px,y:py};}
 return null;
}
function fb10SubBossAt(px,py){
 const m=subBoss;if(!m)return false;
 const sw=m._drawW||m.w,sh=m._drawH||m.h,sy=m._drawY||m.y;
 if(m._ship==='olivewarden'&&typeof stage4MiniDroneAt==='function'&&stage4MiniDroneAt(m,px,py,6))return true;
 if(Math.abs(m.x-px)>sw/2||Math.abs(sy-py)>sh/2)return false;
 const s=typeof subBossSolidAt==='function'?subBossSolidAt(px,py):null;
 return s===null||s===true;
}
function fb10BossAt(px,py){
 if(!boss)return false;
 if(typeof stage4CoreTurretAt==='function'&&stage4CoreTurretAt(boss,px,py,6))return true;
 if(typeof stage4ShieldNodeAt==='function'&&stage4ShieldNodeAt(boss,px,py,6))return true;
 if(Math.abs(boss.x-px)>boss.w/2||Math.abs((boss._drawY??boss.y)-py)>boss.h/2)return false;
 return !!bossHitTest(px,py);
}
function fb10StrikeSubBoss(b,dmg,p){fb10As(b,()=>hitSubBoss(dmg,p.x,p.y));}
function fb10StrikeBoss(b,dmg,p){
 _lastHitX=p.x;_lastHitY=p.y;
 const t4=typeof stage4CoreTurretAt==='function'?stage4CoreTurretAt(boss,p.x,p.y,6):null;
 const n4=!t4&&typeof stage4ShieldNodeAt==='function'?stage4ShieldNodeAt(boss,p.x,p.y,6):null;
 if(t4){boss._s4CoreHit=t4;_lastHitX=t4.x;_lastHitY=t4.y;}else if(n4){boss._s4ShieldHit=n4;_lastHitX=n4.x;_lastHitY=n4.y;}
 fb10As(b,()=>hitBoss(dmg));
}
function fb10HitEncounter(b,dmg,x,y,radius){
 if(subBoss&&subBossActive&&!subBoss.dead&&!subBoss.enter&&!subBoss._noHit){
  const p=fb10FindSolid(x,y,radius,fb10SubBossAt);if(p)fb10StrikeSubBoss(b,dmg,p);
 }
 if(boss&&bossActive&&!boss.dead&&!boss.enter&&!boss._noHit){
  const p=fb10FindSolid(x,y,radius,fb10BossAt);if(p)fb10StrikeBoss(b,dmg,p);
 }
}
function fb10Blast(b,x,y,why){
 if(b._fb10Ended)return;b._fb10Ended=why||true;
 const F=fb10Init(b),k=F.k,lv=fb10Lv(b),r=F.r,dmg=F.blast,col=FB10_COLOR[k];
 // the blast itself: falloff from full at the centre to 60% at the rim
 fb10As(b,()=>{for(const e of enemies){if(e.dead||e._dyingT!=null)continue;
  const d=Math.hypot(e.x-x,e.y-y);if(d>r+(e.w||20)*.3)continue;
  hitEnemy(e,dmg*(1-.4*clamp(d/r,0,1)));fb10Rider(b,k,e,lv);}});
 fb10HitEncounter(b,F.boss,x,y,r*.75);
 // what it looks like and sounds like
 const efx=k==='magma'||k==='fireice'?'fire':k;
 if(typeof efxBurst==='function')efxBurst(efx,x,y,r*1.7);
 if(k==='fireice'&&typeof tsFx==='function')tsFx(x,y,'imp',r*1.6);
 explode(x,y,Math.round(r*.55),FB10_PALETTE[k]||'red',k==='fire'||k==='magma'?'fireball':null);
 particles.push({x,y,vx:0,vy:0,t:0,life:.38,r:r*.9,flashring:true,color:col});
 if(k==='fire'||k==='magma'||k==='kinetic')spawnShockRing(x,y,r*.8,k==='kinetic'?'comet':'fire');
 shake=Math.max(shake,2.5+lv*.5+(k==='magma'?2:0));
 const S=Audio.SFX||{};
 (k==='ice'||k==='fireice'?(S.iceOrbImpact||S.shatter):k==='lightning'?(S.lightning||S.chainShoot):
  k==='water'?(S.waterSplash||S.splash):S.enemyOrbImpact||S.expBig||S.expSmall||function(){})?.();
 // and what it leaves behind
 const shardOpt={mul:F.shard,ts:b._ts,fire:b._fire,wvar:b._wvar,el:b._el||k,forge:!!b._inf,forgeLv:b._infLv||0};
 if(k==='ice'||k==='fireice')iceBurst(x,y,b.shardN||7,lv,shardOpt);
 else if(k==='fire'||k==='magma')iceBurst(x,y,Math.max(9,(b.shardN||5)*2),lv,shardOpt);
 else if(k==='toxic')fb10Clouds.push({x,y,r:64+lv*6,t:0,life:2.6,tick:0,dmg:4*F.K,owner:b});
 else if(k==='water'&&typeof geyserSpawn==='function')geyserSpawn(x,y,'water');
 else if(k==='lightning'&&typeof chainZap==='function'){chainZap(x,y,2+Math.floor(lv/2),[]);chainZap(x,y,1+Math.floor(lv/3),[]);}
 else if(k==='prism'){const n=8+lv*2;for(let i=0;i<n;i++){const a=i*TAU/n+(b.spin||0);
  pBullets.push({kind:'spread',x,y,vx:Math.cos(a)*7.5,vy:Math.sin(a)*7.5,w:5,h:12,dmg:6*F.K,lv:1,t:0,pierce:true,_hit:[],_inf:'prism',_child:true,_split:true,_prism:true});}}
 else if(k==='chrome'&&typeof chromeMirror==='function'){chromeMirror(x,y,140+lv*20,lv);iceBurst(x,y,b.shardN||7,lv,shardOpt);}
 else if(k==='dark'){const N=9+Math.min(5,lv);for(let i=0;i<N;i++)pShard(x,y,Math.PI+(i/(N-1))*Math.PI,lv,{mul:F.shard,el:'dark',wvar:'darkorb',forge:true,forgeLv:b._infLv||1});}
 else if(k==='kinetic')iceBurst(x,y,b.shardN||7,lv,shardOpt);
}
// per-target riders a blast leaves on what it caught
function fb10Rider(b,k,e,lv){
 if(k==='fire'||k==='magma'||k==='fireice'){if(typeof enemyBurnApply==='function')enemyBurnApply(e,DK_BURN_TIME*(.8+.2*lv),b);}
 if(k==='ice'||k==='fireice'){e.vx*=.5;e.vy*=.5;e._frzFlash=.18;e._frozen=(e._frozen||0)+1;}
 if(k==='toxic'){e._poison=Math.max(e._poison||0,2.6+.4*lv);e._poisonLv=Math.max(e._poisonLv|0,lv);}
 if(k==='water')e._soaked=3;
 if(k==='lightning')e._zapFlash=.2;
 if(k==='kinetic'&&!(typeof isSetPiece==='function'&&isSetPiece(e))){const d=Math.max(1,Math.hypot(e.x-b.x,e.y-b.y)),kb=10+4*lv;e.x+=(e.x-b.x)/d*kb;e.y+=(e.y-b.y)/d*kb-4;}
}
function fb10CloudTick(dt){
 for(const c of fb10Clouds){c.t+=dt;c.tick-=dt;
  if(c.tick<=0){c.tick=.25;
   for(const e of enemies){if(e.dead||e._dyingT!=null)continue;if(Math.hypot(e.x-c.x,e.y-c.y)<c.r+(e.w||20)*.25){hitEnemy(e,c.dmg);e._poison=Math.max(e._poison||0,1.4);}}
   fb10HitEncounter(c.owner,c.dmg,c.x,c.y,c.r*.6);
   for(let i=0;i<5;i++)particles.push({x:c.x+rnd(-c.r,c.r)*.7,y:c.y+rnd(-c.r,c.r)*.7,vx:rnd(-.3,.3),vy:rnd(-.6,-.1),life:rnd(.4,.8),t:0,r:rnd(3,7),color:chance(.5)?'#8de23a':'#3aff5a'});
   if(c.t<.3&&typeof efxBurst==='function')efxBurst('toxic',c.x,c.y,c.r*1.4);}
 }
 fb10Clouds=fb10Clouds.filter(c=>c.t<c.life);
}

/* An orb leans toward the nearest target ahead of it. Measured: against the Stage 1 boss, which
   strafes, 4 of 9 contact orbs flew straight past it and off the top, and a missed orb also holds
   the launch cap until it leaves. The lean is lateral only and rate-limited (a curve, not a
   homing missile); the paired launch spread still owns the first 0.15 s. */
function fb10Steer(b,dt){
 b._steerAge=(b._steerAge||0)+dt;if(b._steerAge<.15)return;
 b._steerCd=(b._steerCd||0)-dt;
 if(b._steerCd<=0){b._steerCd=.1;let best=null,score=1e9;
  const look=(x,y,wt)=>{if(!Number.isFinite(x+y))return;const ahead=b.y-y;if(ahead<-10||ahead>320)return;
   const s=Math.abs(x-b.x)*wt+ahead*.35;if(Math.abs(x-b.x)<240&&s<score){score=s;best=x;}};
  for(const e of enemies)if(!e.dead&&e._dyingT==null&&!(typeof isSetPiece==='function'&&isSetPiece(e)))look(e.x,e.y,1);
  // an encounter is aimed at its live parts (a sealed centre plate is not a target), else its hull
  for(const E of [subBoss&&subBossActive?subBoss:null,boss&&bossActive?boss:null]){
   if(!E||E.dead||E.enter)continue;let parts=[];
   try{parts=typeof retinaBossTargets==='function'?retinaBossTargets(E).filter(q=>q&&!q.dead&&Number.isFinite(q.x+q.y)):[];}catch(_){parts=[];}
   if(parts.length)for(const q of parts)look(q.x,q.y,.6);else look(E.x,E._drawY??E.y,.6);
  }
  b._steerX=best;}
 if(b._steerX==null)return;
 const want=clamp((b._steerX-b.x)*.045,-2.6,2.6);
 b.vx+=clamp(want-b.vx,-.14,.14)*dt*60;
}
playerOrbTick=function(b,dt){
 if(b.kind!=='orb')return false;
 if(b._fb10Ended){b.dead=true;return true;}
 const F=fb10Init(b),k=F.k,S=F.S,lv=fb10Lv(b),born=pBullets.length;
 b.life-=dt;b.spin+=dt*((k==='magma'||k==='kinetic')?18:7);b.t=(b.t||0);
 /* Dark Void travels first, then blossoms into a stationary, hungry rift. */
 if(k==='dark'){
  b._voidAge=(b._voidAge||0)+dt;
  if(b._voidAge>.85){b.vx=0;b.vy=0;b.w=Math.min(96,b.w+dt*46);b.h=b.w;
   fb10As(b,()=>{for(const e of enemies){if(e.dead||e._dyingT!=null||(typeof isSetPiece==='function'&&isSetPiece(e)))continue;
    const d=Math.hypot(e.x-b.x,e.y-b.y),pull=90+Math.min(40,b._voidAge*26);
    if(d<pull&&d>2){e.x+=(b.x-e.x)/d*Math.min(3.6*dt*60,d*.1);e.y+=(b.y-e.y)/d*Math.min(3.6*dt*60,d*.1);}
    if(d<b.w*.34){e._voidT=(e._voidT||0)-dt;if(e._voidT<=0){e._voidT=.16;hitEnemy(e,(4+2*lv)*F.K);}}}});
   b._voidHit=(b._voidHit||0)-dt;if(b._voidHit<=0){b._voidHit=.16;fb10HitEncounter(b,(5+2*lv)*F.K,b.x,b.y,b.w*.34);}
   if(b._voidAge>2.6)b.life=0;
  }
 }
 b.frame=(b.frame+dt*12)%4;
 if(!(k==='dark'&&(b._voidAge||0)>.85))fb10Steer(b,dt);
 b.x+=b.vx*dt*60;b.y+=b.vy*dt*60;
 if(b.vy<0)b.vy=Math.min(-3.2,b.vy*Math.pow(.9985,dt*60));
 F.last.x=b.x;F.last.y=b.y;
 // shard spray
 const P=FB10_SHARD[k]||[1,.1],sopt={mul:F.shard,ts:b._ts,fire:b._fire,wvar:b._wvar,el:b._el||k,forge:!!b._inf,forgeLv:b._infLv||0};
 b.shardCd-=dt;
 if(b.shardCd<=0){b.shardCd=P[1];const n=Math.max(2,Math.round((b.shardN||3)*P[0]));
  if(P[0]>0)for(let i=0;i<n;i++)pShard(b.x,b.y,b.spin+i*(TAU/n),lv,sopt);
  if(k==='kinetic'||k==='magma'){b._burstBeat=(b._burstBeat||0)+1;if(b._burstBeat%2===1)efxBurst(k==='kinetic'?'kinetic':'fire',b.x,b.y,Math.min(56,b.w*1.5));}
  b.sfxCd=(b.sfxCd||0)-1;if(P[0]>0&&b.sfxCd<=0){b.sfxCd=3;if(Audio.SFX.spread)Audio.SFX.spread();}}
 // chrome: the orb's shell turns enemy rounds it passes back up the screen
 if(k==='chrome'){F.mirrorCd-=dt;if(F.mirrorCd<=0){F.mirrorCd=.18;if(typeof chromeMirror==='function'&&chromeMirror(b.x,b.y,58+lv*6,lv))particles.push({x:b.x,y:b.y,vx:0,vy:0,t:0,life:.2,r:26,flashring:true,color:'#ffffff'});}}
 // contact
 b._ht-=dt;if(b._ht<=0){b._hit.length=0;b._ht=.16;}
 fb10As(b,()=>{for(const e of enemies){if(e.dead||e._dyingT!=null)continue;
  if(Math.abs(e.x-b.x)<(e.w/2+b.w/2)&&Math.abs(e.y-b.y)<(e.h/2+b.h/2)&&b._hit.indexOf(e)<0){
   b._hit.push(e);hitEnemy(e,b.dmg);
   if(b._ts){e._frozen=(e._frozen||0)+1;e._frzFlash=.18;}
   if(k==='toxic')e._poison=Math.max(e._poison||0,2.2);
   if(!S.pierce)b._impact=true;}}});
 // encounters: the same authored miniboss parts and boss hit tests the old orb used
 // encounters: anywhere inside the orb's radius that is a live, solid part counts as contact
 const reach=Math.max(b.w,b.h)*.5;
 if(subBoss&&subBossActive&&!subBoss.dead&&!subBoss.enter){b._sbt-=dt;
  if(b._sbt<=0){const p=fb10FindSolid(b.x,b.y,reach,fb10SubBossAt);if(p){b._sbt=.16;fb10StrikeSubBoss(b,b.dmg,p);if(!S.pierce)b._impact=true;}}}
 if(boss&&bossActive&&!boss.dead&&!boss.enter){b._bt-=dt;
  if(b._bt<=0){const p=fb10FindSolid(b.x,b.y,reach,fb10BossAt);if(p){b._bt=.16;fb10StrikeBoss(b,b.dmg,p);if(!S.pierce)b._impact=true;}}}
 // every ending detonates, on screen; one that leaves off the top just goes
 if(b._impact||b.life<=0||b.y<-40){
  if(b.y>=-40)fb10Blast(b,b.x,b.y,b._impact?'impact':'expire');else b._fb10Ended='offscreen';
  b.dead=true;
 }
 if(b._wingKey)for(let i=born;i<pBullets.length;i++){pBullets[i]._wingKey=b._wingKey;pBullets[i].ally=true;}
 return true;
};

/* Yuri's lightning orb: harder bolts, and it discharges instead of vanishing when it spends itself */
const FB10_YURI={fire:yuriLightningOrbFire,tick:yuriLightningOrbTick};
yuriLightningOrbFire=function(lv){
 const n=pBullets.length,r=FB10_YURI.fire.apply(this,arguments);
 for(let i=n;i<pBullets.length;i++){const q=pBullets[i];if(q&&q.kind==='yuriLightningOrb'&&!q._fb10){q._fb10=1;q.dmg*=2.2;q.w+=6;q.h+=6;}}
 return r;
};
yuriLightningOrbTick=function(b,dt){
 const n=pBullets.length,r=FB10_YURI.tick.apply(this,arguments);
 for(let i=n;i<pBullets.length;i++){const q=pBullets[i];if(q&&q.kind==='yuriLightningBolt'&&!q._fb10){q._fb10=1;q.dmg*=1.8;}}
 if(b&&b.kind==='yuriLightningOrb'&&b.dead&&!b._fb10Ended&&b.y>-40)fb10YuriDischarge(b);
 return r;
};
function fb10YuriDischarge(b){
 b._fb10Ended=true;const lv=clamp(b.lv||1,1,5),r=62+lv*8,dmg=(6+3*lv);
 fb10As(b,()=>{for(const e of enemies){if(e.dead||e._dyingT!=null)continue;if(Math.hypot(e.x-b.x,e.y-b.y)<r+(e.w||20)*.3){hitEnemy(e,dmg);e._zapFlash=.2;}}});
 fb10HitEncounter(b,dmg,b.x,b.y,r*.75);
 if(typeof chainZap==='function')chainZap(b.x,b.y,1+Math.floor(lv/2),[]);
 for(let i=0;i<6;i++){const a=i*TAU/6+rnd(-.3,.3);zaps.push({x1:b.x,y1:b.y,x2:b.x+Math.cos(a)*r,y2:b.y+Math.sin(a)*r,t:.12,_blue:!!run._thunderStormUnlocked});}
 explode(b.x,b.y,Math.round(r*.5),'orange');particles.push({x:b.x,y:b.y,vx:0,vy:0,t:0,life:.34,r:r*.85,flashring:true,color:'#ffe03a'});
 if(typeof efxBurst==='function')efxBurst('lightning',b.x,b.y,r*1.5);
 shake=Math.max(shake,3);(Audio.SFX.lightning||Audio.SFX.chainShoot||Audio.SFX.expSmall||function(){})();
}

/* The catch-all: an orb that any other system deletes (a shield, a wipe, an absorber, a pBullets
   filter) still detonates where it was last seen, instead of silently vanishing. */
const FB10_UPDATE=updatePlay;
updatePlay=function(dt){
 const live=[];for(const q of pBullets)if(q&&!q.dead&&(q.kind==='orb'||q.kind==='yuriLightningOrb'))live.push([q,q.x,q.y]);
 const r=FB10_UPDATE.apply(this,arguments);
 if(state===GS.PLAY){
  fb10CloudTick(dt||1/60);
  if(player._orbCd>0)player._orbCd=Math.max(0,player._orbCd-(dt||1/60));
  for(const [q,x,y] of live){
   if(q._fb10Ended)continue;
   if(q.dead||pBullets.indexOf(q)<0){
    if(y<-40||y>VH+40)continue;
    if(q.kind==='orb')fb10Blast(q,Number.isFinite(q.x)?q.x:x,Number.isFinite(q.y)?q.y:y,'external');
    else{q.x=Number.isFinite(q.x)?q.x:x;q.y=Number.isFinite(q.y)?q.y:y;fb10YuriDischarge(q);}
   }
  }
 }
 return r;
};
const FB10_BEGIN=beginStage;
beginStage=function(){fb10Clouds=[];return FB10_BEGIN.apply(this,arguments);};
