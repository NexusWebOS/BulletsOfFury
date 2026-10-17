"use strict";
/* 1017 - the Olive Warden's last stand.

   Mike: "Stage 4 miniboss, he does nothing when all his modular pieces are destroyed."

   Measured before this file: with gunL, gunR, rocketL and rocketR dead, the Warden's book still cycles
   sa14-mg and sa14-rockets, and both fire only from slots mr27CanFire allows - so every turn warned nothing
   and fired nothing. The hull did not move (x 340 / y 175 across 900 frames on Normal and Hard) and the only
   rounds on screen were his escorts'. A miniboss whose four modules are gone was a target that waited to die.

   Once every module is dead the Warden exposes his core and fights with the hull itself:
     CORE FAN  - a fan of heavy rounds from the core. Its two-lane gap is COMMITTED when the attack is chosen
                 and every wave fires the lanes the warning showed (the shared-warning rule).
     HULL RAM  - tracks the player's lane, locks it under the shared green/yellow/red warning, rams south off
                 the screen, drops back in from the top and returns to station.
   and his escorts come round sooner (Easy/Normal). Every attack warns through sa14Warning + combatWarningTick, the path
   his module attacks already use, so the last stand reads exactly like the rest of the fight.

   Mike, later on 1017: "on hard, 4 jets should appear, 2 from the south, 2 from the north, and they shouldnt fly
   off, they should kinda orbit and circle around the boss until we destroy them. Then when theyre destroyed, they
   respawn about 5 seconds later. On Insanity, 6. 2 south, 2 north, 1 east, 1 west." and "Get sounds for all his
   attacks too ... but no lightning. Hes a pure war machine of bullets and missiles and charging/ramming at you."
   So: no lightning (the borrowed Storm glow - four blue arcs and a lightning ball around his core, plus the blue
   cold-tracer art on the fan - is gone), his own sound set on every attack, and the ORBIT WING below replaces the
   fly-in escort turns from Hard up. */
const WLS17={serial:0,base:{book:er26Book,set:er26Set,mini:sa14MiniAttack,escorts:sa14Escorts,slug:sa14Slug,missiles:sa14Missiles,update:updatePlay,enemy:drawEnemy,draw:er26Draw}};
function wls17Sfx(k){try{(Audio.SFX[k]||Audio.SFX.enemyMachineGunHeavy)?.();}catch(e){}}
const WLS17_CFG={
 easy:   {fanWarm:1.40,fanWaves:2,fanGap:.46,fanSpeed:3.0,ramWarm:1.50,ramTrack:.55,ramSpeed:560,returnSpeed:220,escort:.80},
 normal: {fanWarm:1.20,fanWaves:3,fanGap:.38,fanSpeed:3.4,ramWarm:1.25,ramTrack:.55,ramSpeed:680,returnSpeed:260,escort:.70},
 hard:   {fanWarm:1.05,fanWaves:4,fanGap:.32,fanSpeed:3.8,ramWarm:1.10,ramTrack:.60,ramSpeed:800,returnSpeed:300,escort:.60},
 furious:{fanWarm:.92, fanWaves:5,fanGap:.27,fanSpeed:4.2,ramWarm:.95, ramTrack:.62,ramSpeed:920,returnSpeed:340,escort:.50}
};
function wls17Cfg(){return WLS17_CFG[diffKey==='insanity'?'furious':diffKey]||WLS17_CFG.normal;}
function wls17Exposed(b){return sa14Mini(b)&&!!b._mr27&&b._mr27.parts.length>0&&b._mr27.parts.every(p=>p.dead);}
function wls17Mode(m){return m==='sa14-corefan'||m==='sa14-ram';}
// The fan's lanes around straight down from the core: count, spacing and the committed gap.
function wls17FanLanes(b){const T=b._er26._sa14,count=9+vp12Tier()*2,out=[];
 for(let i=0;i<count;i++){if(i===T.gap||i===T.gap+1)continue;out.push(Math.PI/2+(i-(count-1)/2)*.13);}return out;}

er26Book=function(b){
 if(wls17Exposed(b))return ['sa14-corefan','sa14-ram','sa14-corefan','sa14-corefan','sa14-ram'];
 return WLS17.base.book.apply(this,arguments);
};
er26Set=function(b,mode){
 if(sa14Mini(b)&&wls17Exposed(b)&&(mode==='sa14-mg'||mode==='sa14-rockets'))mode='sa14-corefan';   // a turn chosen the frame the last module died
 const r=WLS17.base.set.call(this,b,mode);
 if(!sa14Mini(b)||!wls17Mode(mode))return r;
 const R=b._er26,T=R._sa14,c=wls17Cfg();T.wls=++WLS17.serial;T.home={x:b.x,y:b.y};
 if(mode==='sa14-corefan'){
  const count=9+vp12Tier()*2;
  // the gap is deterministic (no Math.random: the wave plan's fixtures read the unseeded stream) and walks
  // across the fan from one fan to the next, so no one lane is safe twice running
  T.gap=1+((T.wls*3)%(count-3));wls17Sfx('bossWeaponCharge');
  R.warm=c.fanWarm;R.live=(c.fanWaves-1)*c.fanGap+.5;R.dur=R.warm+R.live;
 }else{
  T.phase='track';T.lane=b.x;T.v=0;wls17Sfx('razorbackCharge');R.warm=c.ramWarm;R.live=9;R.dur=R.warm+R.live;
 }
 sa14Log('last-stand',b,{mode,warm:R.warm});return r;
};
sa14MiniAttack=function(b,dt){
 const R=b._er26;
 if(!wls17Mode(R.mode))return WLS17.base.mini.apply(this,arguments);
 R.warnings=[];return R.mode==='sa14-corefan'?wls17CoreFan(b,dt):wls17Ram(b,dt);
};
function wls17CoreFan(b,dt){
 const R=b._er26,T=R._sa14,c=wls17Cfg(),A=sa14State(b),p=shipBossMount(b,'C');
 if(R.t<R.warm){
  for(const a of wls17FanLanes(b))sa14Warning(b,p,{x:p.x+Math.cos(a)*VH,y:p.y+Math.sin(a)*VH},16,R.t/R.warm);
  combatWarningTick(b,'warden-core-'+T.wls,R.t,R.warm);return true;
 }
 T.shot-=dt;
 if(T.shot<=0&&T.wave<c.fanWaves){
  for(const a of wls17FanLanes(b)){
   const q=eShootT(p.x,p.y,a,c.fanSpeed,'mg',{w:8,h:18,silent:true});
   Object.assign(q,{_boss:true,_noArsenal:true,_weaponProof:true,_shootable:false,mg:true,_er26Source:b._ship,_wls17:true});
  }
  shipBossMuzzleStart(b,['C'],{fam:'mg',life:.14,hpx:52});wls17Sfx('wardenGun');wls17Sfx('enemyMachineGunBurst');
  shake=Math.max(shake,2);R.shots=(R.shots||0)+1;T.wave++;T.shot=c.fanGap;
  sa14Log('core-fan',b,{wave:T.wave,gap:T.gap});
 }
 if(R.t>=R.dur)er26Set(b,'recover');return true;
}
function wls17Ram(b,dt){
 const R=b._er26,T=R._sa14,c=wls17Cfg(),A=sa14State(b);
 const L=camLeftX(),Rx=camRightX(),half=b.w*.42;
 if(T.phase==='track'){
  const k=clamp(R.t/R.warm,0,1);
  // green: the hull follows the player's lane; yellow and red: the lane is LOCKED and late movement cannot move it
  if(k<c.ramTrack){const tgt=targetShip(b.x,b.y),want=clamp(tgt.x,L+half,Rx-half);b.x+=clamp(want-b.x,-190*dt,190*dt);}
  T.lane=b.x;b._drawY=b.y;
  sa14Warning(b,{x:b.x,y:b.y+b.h*.2},{x:b.x,y:VH+60},b.w*.62,k);
  combatWarningTick(b,'warden-ram-'+T.wls,R.t,R.warm);
  if(R.t>=R.warm){T.phase='dive';T.v=140;shake=Math.max(shake,5);wls17Sfx('razorbackRam');wls17Sfx('tlvJetThrust');sa14Log('ram',b,{lane:T.lane});}
  return true;
 }
 if(T.phase==='dive'){
  T.v=Math.min(c.ramSpeed,T.v+c.ramSpeed*2.4*dt);b.x=T.lane;b.y+=T.v*dt;b._drawY=b.y;
  if(b.y-b.h*.5>VH+30){T.phase='drop';b._noHit=true;b.x=T.home.x;b.y=-b.h*.6;b._drawY=b.y;}
  return true;
 }
 if(T.phase==='drop'){
  b.x=T.home.x;b.y+=Math.max(60,Math.min(c.returnSpeed,(T.home.y-b.y)*3))*dt;b._drawY=b.y;
  if(b.y+b.h*.3>PLAY.y)b._noHit=false;   // hittable again as soon as the hull is on screen
  if(b.y>=T.home.y){b.y=T.home.y;b._drawY=b.y;b._noHit=false;wls17Sfx('tlvJetBrake');er26Set(b,'recover');}
  return true;
 }
 er26Set(b,'recover');return true;
}

/* ---- his own sounds on the module attacks (wardenGun / wardenRocket / wardenRackCharge) ---- */
function wls17Swap(map,fn){const old={};for(const k in map){old[k]=Audio.SFX[k];if(Audio.SFX[map[k]])Audio.SFX[k]=Audio.SFX[map[k]];}
 try{return fn();}finally{for(const k in old)Audio.SFX[k]=old[k];}}
sa14Slug=function(b){const a=arguments;if(!sa14Mini(b))return WLS17.base.slug.apply(this,a);
 return wls17Swap({enemyMachineGunHeavy:'wardenGun'},()=>WLS17.base.slug.apply(this,a));};
sa14Missiles=function(b){const a=arguments;if(!sa14Mini(b))return WLS17.base.missiles.apply(this,a);
 return wls17Swap({missile:'wardenRocket'},()=>WLS17.base.missiles.apply(this,a));};
const WLS17_SET=er26Set;
er26Set=function(b,mode){const r=WLS17_SET.apply(this,arguments);
 if(sa14Mini(b)&&mode==='sa14-rockets'&&b._er26&&b._er26.mode==='sa14-rockets')wls17Sfx('wardenRackCharge');
 return r;};

/* ---- the ORBIT WING (Hard 4: 2 south + 2 north; Furious and Insanity 6: + east + west - Mike: "I meant 6 on Furious") ----
   Each slot enters from its own edge under a short warning, joins an ellipse around the Warden and circles
   him, firing warned bursts at the player. It never flies off. When it dies the slot waits WING17_RESPAWN
   seconds and a new jet enters from the same edge. Easy / Normal keep the fly-in escort turns. */
const WING17_RESPAWN=5.0,WING17_WARN=.8,WING17_ENTRY=1.25;
const WING17_LAYOUT={hard:['S','S','N','N'],furious:['S','S','N','N','E','W'],insanity:['S','S','N','N','E','W']};
const WING17_CFG={hard:{spin:.70,rx:205,ry:118,every:2.7,tell:.55,rounds:5,gap:.11,speed:3.9},
 furious:{spin:.82,rx:205,ry:118,every:2.3,tell:.50,rounds:6,gap:.10,speed:4.3},
 insanity:{spin:.92,rx:215,ry:124,every:2.0,tell:.45,rounds:7,gap:.09,speed:4.6}};
function wing17Layout(){return WING17_LAYOUT[diffKey]||null;}
function wing17Cfg(){return WING17_CFG[diffKey]||WING17_CFG.hard;}
function wing17State(b){
 const L=wing17Layout();if(!L)return null;
 if(!b._wing17){const n=L.length;b._wing17={t:0,slots:L.map((edge,i)=>({i,edge,e:null,wait:.4+i*.3,warn:0,phase:i/n*TAU}))};}
 return b._wing17;
}
/* The ring is centred on his STATION, not his live hull: while he rams south off the screen and drops back
   in from the top the wing keeps circling where he fights, instead of bunching at the screen edge after him. */
function wing17CentreStep(b){const W=b._wing17,R=b._er26,T=R&&R._sa14,ram=R&&R.mode==='sa14-ram'&&T&&T.home;
 const x=ram?T.home.x:b.x,y=(ram?T.home.y:(b._drawY??b.y))+12;
 if(W){if(W.cx==null){W.cx=x;W.cy=y;}else{W.cx+=(x-W.cx)*.08;W.cy+=(y-W.cy)*.08;}return {x:W.cx,y:W.cy};}
 return {x,y};}
function wing17Centre(b){const W=b._wing17;return W&&W.c?W.c:{x:b.x,y:(b._drawY??b.y)+12};}
function wing17Orbit(b,s,t){const c=wing17Cfg(),C=wing17Centre(b),a=s.phase+t*c.spin,L=camLeftX(),R=camRightX();
 return {x:clamp(C.x+Math.cos(a)*c.rx,L+42,R-42),y:clamp(C.y+Math.sin(a)*c.ry,PLAY.y+40,VH-150)};}
function wing17Gate(b,s){const L=camLeftX(),R=camRightX(),C=wing17Centre(b),off=s.i%2?1:-1;
 if(s.edge==='S')return {x:clamp(C.x+off*110,L+40,R-40),y:VH+64};
 if(s.edge==='N')return {x:clamp(C.x+off*110,L+40,R-40),y:-64};
 if(s.edge==='E')return {x:R+64,y:C.y+40};
 return {x:L-64,y:C.y+40};}
function wing17Spawn(b,s){
 const g=wing17Gate(b,s),e=spawnEnemy('drone',g.x,g.y,{pattern:'sa14-escort',shoots:false,hp:vp12FamilyHealth(4).hp,w:96});
 if(!e)return null;delete e._cn;e.shoots=false;e._mini=true;e._noSep=true;e._bodShadow=true;e._noHit=true;e.w=e.h=96;e.vx=e.vy=0;e.fireCd=999;
 const C=wing17Centre(b);
 e._wing17={owner:b,slot:s,t:0,from:g,angle:Math.atan2(C.y-g.y,C.x-g.x),shot:0,shots:0,shotSerial:0,next:1.2+s.i*.45,phase:'enter',serial:++WLS17.serial};
 wls17Sfx('tlvJetThrust');sa14Log('wing-spawn',b,{edge:s.edge,slot:s.i});return e;
}
function wing17Tick(b,dt){
 const W=wing17State(b);if(!W)return false;W.t+=dt;W.c=wing17CentreStep(b);
 for(const s of W.slots){
  if(s.e&&(s.e.dead||s.e._dyingT!=null||!enemies.includes(s.e))){ /* culled or cleared without a death counts too */s.e=null;s.wait=WING17_RESPAWN;s.warn=0;s.gen=(s.gen||0)+1;}
  if(s.e)continue;
  s.wait-=dt;
  if(s.wait<=WING17_WARN){s.warn=clamp(1-Math.max(0,s.wait)/WING17_WARN,0,1);combatWarningTick(b,'wing-entry-'+s.i+'-'+(s.gen||0),WING17_WARN-Math.max(0,s.wait),WING17_WARN,true);}
  if(s.wait<=0){s.e=wing17Spawn(b,s);s.warn=0;if(!s.e)s.wait=1;}
 }
 return true;
}
function wing17JetTick(e,dt){
 const A=e._wing17,b=A.owner;
 if(!b||b.dead||b.dying||!subBossActive||subBoss!==b){e.dead=true;return;}
 const c=wing17Cfg(),W=b._wing17;A.t+=dt;e.fireCd=999;e.vx=e.vy=0;
 const px=e.x,py=e.y,o=wing17Orbit(b,A.slot,W.t);
 if(A.t<WING17_ENTRY){const u=clamp(A.t/WING17_ENTRY,0,1),k=u*u*(3-2*u);
  // The enlarged fly-in is above the combat plane for its ENTIRE scaling pass.
  // North/south/side entries and respawns share this gate; orbit restores contact.
  e.x=lerp(A.from.x,o.x,k);e.y=lerp(A.from.y,o.y,k);e._noHit=true;A.phase='enter';}
 else{e.x=o.x;e.y=o.y;e._noHit=false;if(A.phase==='enter')A.phase='orbit';}
 const mv=Math.hypot(e.x-px,e.y-py);
 if(A.phase!=='warn'&&A.phase!=='fire'&&mv>.05)A.angle=Math.atan2(e.y-py,e.x-px);
 if(A.t<WING17_ENTRY)return;
 A.next-=dt;
 if(A.phase==='orbit'&&A.next<=0){const t=targetShip(e.x,e.y);A.aim={x:t.x,y:t.y};A.phase='warn';A.wt=0;A.shots=0;A.shot=0;A.shotSerial++;}
 if(A.phase==='warn'){A.wt+=dt;A.angle+=clamp(stage4AngleDelta(A.angle,Math.atan2(A.aim.y-e.y,A.aim.x-e.x)),-12*dt,12*dt);
  combatWarningTick(e,'wing-fire-'+A.serial+'-'+A.shotSerial,A.wt,c.tell);
  if(A.wt>=c.tell)A.phase='fire';return;}
 if(A.phase==='fire'){A.shot-=dt;
  if(A.shot<=0&&A.shots<c.rounds){const a=Math.atan2(A.aim.y-e.y,A.aim.x-e.x),p={x:e.x+Math.cos(a)*34,y:e.y+Math.sin(a)*34};
   const q=eShootT(p.x,p.y,a,c.speed,'mg',{w:6,h:14,silent:true});
   Object.assign(q,{_wing17Shot:true,mg:true,_weaponProof:true,_shootable:false});
   if(typeof wm26Emit==='function')wm26Emit(e,p.x,p.y,a,'mg',null,{size:34,life:.12});
   wls17Sfx('enemyMachineGunLight');A.shots++;A.shot=c.gap;}
  if(A.shots>=c.rounds){A.phase='orbit';A.next=c.every+(A.slot.i%3)*.35;}}
}
sa14Escorts=function(b,dt){
 if(sa14Mini(b)&&wing17Layout())return wing17Tick(b,dt);   // Hard and up: the orbit wing owns his escorts
 const r=WLS17.base.escorts.apply(this,arguments);
 if(wls17Exposed(b)){const A=sa14State(b);if(!A.escortTurn)A.escortCd=Math.min(A.escortCd,[8,6,5,4][vp12Tier()]*wls17Cfg().escort);}
 return r;
};
updatePlay=function(dt){for(const e of enemies)if(e._wing17&&!e.dead&&e._dyingT==null)wing17JetTick(e,dt);return WLS17.base.update.apply(this,arguments);};
drawEnemy=function(e){if(!e._wing17)return WLS17.base.enemy.apply(this,arguments);
 if(e.dead)return;const A=e._wing17,p=air13Pose('flight_variant_4','heading',A.angle);if(!p)return;
 const s=A.t<WING17_ENTRY?lerp(1.45,1,clamp(A.t/WING17_ENTRY,0,1)):1;
 drawUnitShadow(e.x,e.y+18,96*s,96*s,.34,e);
 air13Blit(p,e.x,e.y,96*s*p.d.referenceRatio,1,e.flash>0?hitFlashColor(e,'#ffffff'):null);
 if(A.phase==='warn')combatWarningDraw(e,{x:e.x,y:e.y,ex:A.aim.x,ey:A.aim.y,width:30,progress:clamp(A.wt/wing17Cfg().tell,0,1),alertX:e.x,alertY:e.y-56});
 e._air13RenderedKey=p.key;e._air13Frame=p.f;
};
er26Draw=function(b){const r=WLS17.base.draw.apply(this,arguments);
 const W=b&&b._wing17;if(W&&sa14Mini(b)&&!b.dead)for(const s of W.slots)if(!s.e&&s.warn>0){
  const g=wing17Gate(b,s),o=wing17Orbit(b,s,W.t),x=clamp(g.x,camLeftX()+24,camRightX()-24),y=clamp(g.y,PLAY.y+20,VH-14);
  combatWarningDraw(b,{x,y,ex:o.x,ey:o.y,width:80,progress:s.warn,alertX:x,alertY:s.edge==='N'?y+44:s.edge==='S'?y-40:y-44});}
 return r;};
