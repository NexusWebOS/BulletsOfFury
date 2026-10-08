"use strict";
/* ============================================================================================
   1002 - Mike's Stage 5 / Stage 6 notes.
   Loaded after feedback_1001b.js (before the widescreen HUD) so each override here is the outermost
   wrapper of the function it changes.
   ============================================================================================ */

/* ---------------------------------------------------------------------------------------------
   A. STAGE 5 - THE CHROME HAMMER ARCHMAGE
   "volley missiles are still striking his hammer, which is disrupting the sequence of his
   recharge/recover ability. He is also not flashing white when taking damage until the very end.
   He should never be able to be killed before doing the circular spin rage form recovery effect."

   A1. VOLLEY MISSILES NEVER TOUCH THE HAMMER. The passive space volley locked the hammer as a
       retina piece (spaceVolleyLocks / spaceAcquire read spaceTargets, which lists it) and every
       missile kind - the passive volley included - broke the heal outright (0928). So the volley
       rack, which fires on its own every few beats, kept knocking him out of his recharge. Now the
       volley never selects the hammer, flies THROUGH it instead of striking it, and a stray hit on it
       counts as a body hit. The deliberate counter is unchanged: a manual missile (guided rocket,
       retina missile, nuke) into the raised hammer still breaks the heal.

   A2. EVERY HIT HE ABSORBS FLASHES. hitBoss runs hammerBossDamage and returns when it answers 0 -
       BEFORE markHit (0912y put markHit first; the hammer line was later inserted above it). So every
       round his Chromium armor soaked (the whole armored opening, on every difficulty), every round
       into the hammer and every round into the recovery core flashed nothing. A hit that changed
       anything - armor, hammer, chaingun, core, twirl or whirl counters, the state - now flashes.
       A round turned back by the energy wall changed nothing and still does not.

   A3. HE CANNOT DIE BEFORE THE SPIN RECOVERY. The 15% checkpoint is the fr_twirl - the hammer
       circling him, the slam, and the critical heal that turns him red if it is broken. It only fires
       from a "safe" state once his armor is down, so a burst that took him from above 15% to zero, or
       damage landing mid-move, killed him before it ever played. Until the twirl has been performed his
       HP cannot go below FB2_HAMMER_FLOOR of his max. And the recovery itself - the raised hammer charging,
       chromium radiating out of his core, then the whirlwind - must have started at least once: on Normal the
       0930 balance pre-spends the 15% twirl, so that heal is the only rage recovery a Normal/Hard fight has.
   --------------------------------------------------------------------------------------------- */
const FB2_HAMMER_FLOOR=.08;
function fb2HammerRageDone(b){
 const h=b&&b._hammer,A=typeof fr27Armor==='function'?fr27Armor(b):null;
 if(!h)return true;
 // 1) the hammer-raised recovery (storm_raise: chromium radiating from his core, then the whirlwind) has
 //    started at least once - hammerStormStart, which every recovery goes through, sets restorationSeen;
 // 2) where the 15% spin twirl is live (Furious - the 0930 balance pre-spends it on Normal/Hard), it has played.
 if(!h.restorationSeen)return false;
 if(A&&!A._fb2TwirlPreset&&!h._fb2RageDone)return false;
 return true;
}
function fb2HammerFloor(b){return Math.max(1,Math.ceil((b.maxhp||1)*FB2_HAMMER_FLOOR));}
function fb2HammerSnap(b){
 const h=b._hammer,A=typeof fr27Armor==='function'?fr27Armor(b):null,R=h.recovery;
 return [A?A.hp:0,h.hammerHP,h.chainHP,R?R.coreHP:0,R?R.status:'',h.whirlHits||0,h.frTwirlHits||0,h.state,b.hp].join('|');
}
const FB2_HDMG=hammerBossDamage;
hammerBossDamage=function(b,dmg){
 const h=b&&b._hammer;if(!h)return FB2_HDMG(b,dmg);
 // A1: a passive volley missile that reaches the hammer is a body hit, never the heal counter.
 if(_dmgBullet&&_dmgBullet.kind==='spaceVolley'&&b._hammerModuleHit==='hammer')b._hammerModuleHit=null;
 const before=fb2HammerSnap(b);
 let out=FB2_HDMG(b,dmg);
 // A2: absorbed, not rejected - show it.
 if(!(out>0)&&dmg>0&&!b._noHit&&fb2HammerSnap(b)!==before)markHit(b);
 // A3: no kill before the spin recovery.
 if(out>0&&!fb2HammerRageDone(b))out=Math.min(out,Math.max(0,b.hp-fb2HammerFloor(b)));
 return out;
};
// A1: the volley rack never selects the hammer piece.
let fb2NoHammerTarget=false;
const FB2_TARGETS=spaceTargets;
spaceTargets=function(){
 const a=FB2_TARGETS.apply(this,arguments);
 return fb2NoHammerTarget?a.filter(t=>!(t&&t._retinaId==='hammer')):a;
};
const FB2_VLOCKS=spaceVolleyLocks;
spaceVolleyLocks=function(){fb2NoHammerTarget=true;try{return FB2_VLOCKS.apply(this,arguments);}finally{fb2NoHammerTarget=false;}};
const FB2_ACQ=spaceAcquire;
spaceAcquire=function(b){const v=!!(b&&b.kind==='spaceVolley');if(v)fb2NoHammerTarget=true;try{return FB2_ACQ.apply(this,arguments);}finally{if(v)fb2NoHammerTarget=false;}};
// A1: ... and flies through it instead of striking it.
const FB2_SPACEHIT=spaceBulletHit;
spaceBulletHit=function(b){
 if(!(b&&b.kind==='spaceVolley'&&boss&&boss._hammer))return FB2_SPACEHIT.apply(this,arguments);
 if(b._target&&b._target._retinaId==='hammer')b._target=null;   // a lock taken before this layer loaded
 const test=bossHitTest;
 bossHitTest=function(x,y){const r=test(x,y);if(r&&boss&&boss._hammerModuleHit==='hammer'){boss._hammerModuleHit=null;return false;}return r;};
 try{return FB2_SPACEHIT.apply(this,arguments);}finally{bossHitTest=test;}
};
// A3: a broken recovery revokes healed HP; that alone must not end him before the spin either.
const FB2_RBREAK=hammerRecoveryBreak;
hammerRecoveryBreak=function(b){
 const r=FB2_RBREAK.apply(this,arguments);
 if(b&&b._hammer&&!fb2HammerRageDone(b)&&b.hp<fb2HammerFloor(b)&&!b.dead)b.hp=fb2HammerFloor(b);
 return r;
};
// A3: the spin only counts once it has actually played - its slam landed, or the pilot broke it with hammer hits
// (that interrupt IS the red rage form). Measured: a heal left 'charging' from earlier made the first hammer
// hit inside the twirl run the base recovery-break and swap fr_twirl for fr_stun on its first frame, which spent
// the 15% checkpoint with nothing shown. The twirl now starts clean, and any other early exit re-arms it.
const FB2_BEGIN=fr27BeginArmor;
fr27BeginArmor=function(b){const a=FB2_BEGIN.apply(this,arguments);if(a)a._fb2TwirlPreset=!!(a.checkpoints&&a.checkpoints.includes(.15));return a;};
const FB2_HSTATE=hammerState;
hammerState=function(b,state){
 const h=b&&b._hammer;
 if(h&&state==='fr_twirl'&&h.recovery&&h.recovery.status==='charging')h.recovery=null;
 // leaving the twirl - from the tick (its slam and heal) or from a hit (the pilot's break into the red rage)
 if(h&&h.state==='fr_twirl'&&state!=='fr_twirl'&&!h._fb2RageDone){
  if(h.frSlam||h.frCriticalInterrupted)h._fb2RageDone=true;
  else{const A=typeof fr27Armor==='function'?fr27Armor(b):null;if(A&&A.checkpoints){const i=A.checkpoints.indexOf(.15);if(i>=0)A.checkpoints.splice(i,1);}}
 }
 return FB2_HSTATE.apply(this,arguments);
};

/* ---------------------------------------------------------------------------------------------
   B. STAGE 5 - THE HAMMER'S ARRIVAL, IN PLAY
   "generate a proper avatar box of our hammer boss, do not pause the game, just darken the arena and
   do the cinematic between both them and the player. The player should be stunned and go '...Who are
   you?' '.........' Decker or Cole will be the main point of contact from HQ"

   The 0930 Cronos scene was a LIVE director scene, which replaces updatePlay outright: the world froze
   and the dialogue played over it. This one is a beat inside ordinary play. updatePlay keeps running
   (scroll, effects, music, the volley rack's clock) while:
     - the hammer finishes unfolding and HOLDS the fully unfolded plate, untargetable (_noHit) - he
       is not attacking yet and cannot be damaged during the dialogue;
     - every seat is STUNNED through the one control gate updatePlay already has
       (s6OpeningControlsLocked, which has exactly one caller), with dizzy sparks orbiting the ship;
     - drawBG gets a dark wash on top, so the arena drops back and only the two ships stay lit;
     - the dialogue types in the in-play dlgBox with authored boxes: the pilot's own comm portrait,
       the hammer's avatar box (dispatch_1002/hammer_avatar.png) and an HQ dispatcher box.
   FIRE advances a line (the stunned pilot has nothing else to do with it); lines also advance on
   their own. The 0930 scene is retired by setting _cin30Spoke before its hook can see the boss.
   Campaign keeps the Cronos name reveal, condensed into one line; arcade keeps him silent.

   DISPATCHER (Mike): playing Decker, Cole chimes in; playing Cole, Decker does; anyone else gets one of
   the two at random. If both seats are Cole and Decker: Axel when the lead pilot is a man, the other
   woman (Lizzie <-> Falva) when she is a woman. Never a pilot who is in the air.
   --------------------------------------------------------------------------------------------- */
{const root='assets/game/shared/combat/dispatch_1002/';
 XART._src.fb2_hammer_avatar=root+'hammer_avatar.png';
 for(const p of ['cole','decker','axel','lizzie','falva'])XART._src['fb2_dispatch_'+p]=root+'dispatch_'+p+'.png';}
const FB2_FEMALE=new Set(['lizzie','falva']);
function fb2SeatPilots(){
 const a=[String(run.pilot||'').toLowerCase()];
 if(typeof coopActive==='function'&&coopActive()&&typeof run2!=='undefined'&&run2)a.push(String(run2.pilot||'').toLowerCase());
 return a;
}
function fb2Dispatcher(rand){
 const seats=fb2SeatPilots(),lead=seats[0],free=p=>!seats.includes(p),r=rand||Math.random;
 if(lead==='decker'&&free('cole'))return 'cole';
 if(lead==='cole'&&free('decker'))return 'decker';
 const hq=['cole','decker'].filter(free);
 if(hq.length)return hq[Math.floor(r()*hq.length)%hq.length];
 if(FB2_FEMALE.has(lead)){const o=lead==='lizzie'?'falva':'lizzie';if(free(o))return o;}
 for(const p of ['axel','lizzie','falva'])if(free(p))return p;
 return 'axel';
}
function fb2HammerIntroScript(lead,disp,campaign){
 const P=lead.toUpperCase(),D=disp.toUpperCase()+' - HQ',B=campaign?'CRONOS':'???';
 const L=(who,text,kind)=>({who,text,kind});
 const out=[
  L(P,'...Who are you?','pilot'),
  L('???','.........','boss'),
  L(D,P+', talk to me. What are you looking at? That signature is not in any Federation file.','hq'),
  L(P,'I don’t know. It’s not moving... it’s just staring at me.','pilot')];
 if(campaign)out.push(L(B,'I am Cronos. Your planet is precisely what interests me. Leave now, pilot.','boss'));
 else out.push(L('???','.........','boss'));
 out.push(L(D,'Its core is spiking! Snap out of it - get your hands back on the stick, NOW!','hq'));
 return out.map(l=>({...l,text:l.text.replace(/’/g,"'")}));
}
const FB2_HOLD_T=1.95;                 // the unfold reel's last frame; 2.0 is where he becomes hittable
let fb2Intro=null;
function fb2IntroActive(){return !!(fb2Intro&&!fb2Intro.done&&run&&run.stage===5&&state===GS.PLAY&&boss&&boss===fb2Intro.boss&&!boss.dead);}
function fb2IntroStart(b){
 const lead=fb2SeatPilots()[0],disp=fb2Dispatcher();
 fb2Intro={boss:b,lead,disp,lines:fb2HammerIntroScript(lead,disp,run.mode==='campaign'),i:0,t:0,shown:0,age:0,done:false,dim:0,noHit:b._noHit};
 b._noHit=true;eBullets.length=0;storySkip&&storySkip();Input.clearTaps&&Input.clearTaps();
 for(const k of ['fb2_hammer_avatar','fb2_dispatch_'+disp,'dlg_window'])try{XART.rdy(k);}catch(_w){}
 if(Audio.SFX.alertDanger)Audio.SFX.alertDanger();
}
function fb2IntroEnd(){const I=fb2Intro;if(!I||I.done)return;I.done=true;I.endT=0;
 const b=I.boss;if(b&&!b.dead){b._noHit=false;if(b._hammer&&b._hammer.state==='unfold')b._hammer.t=2;}
 Input.clearTaps&&Input.clearTaps();
}
function fb2IntroTick(dt){
 const I=fb2Intro;if(!I)return;
 if(I.done){I.dim=Math.max(0,I.dim-dt*1.6);if(I.dim<=0)fb2Intro=null;return;}
 if(!fb2IntroActive()){fb2IntroEnd();return;}
 I.age+=dt;I.dim=Math.min(1,I.dim+dt*2);eBullets.length=0;
 const L=I.lines[I.i],cps=38,full=L.text.length;
 if(I.age>.35&&(Input.tapAny?Input.tapAny(keybind.fire):Input.menuConfirm())){
  if(I.shown<full){I.shown=full;I.t=Math.max(I.t,full/cps);}else{I.i++;I.t=0;I.shown=0;}
 }else{
  I.t+=dt;const n=Math.min(full,Math.floor(I.t*cps));if(typeof dialogueLetterTicks==='function')dialogueLetterTicks(L.text,I.shown,n);I.shown=Math.max(I.shown,n);
  if(I.t>=full/cps+(L.text.replace(/\./g,'').length?1.7:1.25)){I.i++;I.t=0;I.shown=0;}
 }
 if(I.i>=I.lines.length)fb2IntroEnd();
}
const FB2_HTICK=hammerBossTick;
hammerBossTick=function(b,dt){
 const h=b&&b._hammer;
 if(!h||b._hammerTime||run.stage!==5)return FB2_HTICK.apply(this,arguments);
 b._cin30Spoke=true;                   // the 0930 live (pausing) scene never fires now
 if(!b._fb2IntroSeen&&h.state==='unfold'&&h.t>=FB2_HOLD_T-.05){b._fb2IntroSeen=true;fb2IntroStart(b);}
 if(fb2Intro&&!fb2Intro.done&&fb2Intro.boss===b){
  if(h.state==='unfold'){h.t=Math.min(h.t,FB2_HOLD_T);b._noHit=true;return;}   // hold the unfolded plate
 }
 return FB2_HTICK.apply(this,arguments);
};
const FB2_CTRL=s6OpeningControlsLocked;
s6OpeningControlsLocked=function(){return fb2IntroActive()||FB2_CTRL.apply(this,arguments);};
const FB2_UPD=updatePlay;
updatePlay=function(dt){const r=FB2_UPD.apply(this,arguments);if(fb2Intro)fb2IntroTick(dt||0);return r;};
const FB2_BG=drawBG;
drawBG=function(dt){
 const r=FB2_BG.apply(this,arguments);
 if(fb2Intro&&fb2Intro.dim>0&&run.stage===5){const a=.58*fb2Intro.dim*fb2Intro.dim*(3-2*fb2Intro.dim);
  ctx.save();ctx.setTransform(1,0,0,1,0,0);ctx.fillStyle='rgba(2,4,12,'+a.toFixed(3)+')';ctx.fillRect(0,0,ctx.canvas.width,ctx.canvas.height);ctx.restore();}
 return r;
};
function fb2StunDraw(){
 if(!fb2IntroActive())return;const t=fb2Intro.age;
 // drawn after drawWorld has returned: put the world camera back on (never a raw world x on screen)
 ctx.save();
 if(!(typeof _inWorldXform!=='undefined'&&_inWorldXform)){const z=typeof viewZoom==='function'?viewZoom():1;
  if(z!==1){ctx.translate(0,VH*(1-z));ctx.scale(z,z);}ctx.translate(-camLeftX(),0);}
 for(const n of seatList()){const S=seatShip(n);if(!S||S.dead||S.out)continue;
  // the same orbiting shield-impact plates the shared enemy shield stun uses (enemyShieldStunDraw)
  const key='nes_hit_'+Math.min(2,Math.floor((t*15)%3));const top=S.y-34,r=26;
  for(let i=0;i<3;i++){const a=t*6+i*TAU/3,x=S.x+Math.cos(a)*r,y=top+Math.sin(a)*7;
   ctx.save();ctx.translate(x,y);ctx.rotate(a);ctx.globalAlpha=.95;ctx.globalCompositeOperation='lighter';
   if(XART.rdy(key))ctx.drawImage(XART.get(key),-16,-16,32,32);
   ctx.restore();}}
 ctx.restore();
}
function fb2IntroDraw(){
 if(!fb2IntroActive())return;const I=fb2Intro,L=I.lines[I.i];if(!L)return;
 const portraitKey=L.kind==='boss'?'fb2_hammer_avatar':L.kind==='hq'?'fb2_dispatch_'+I.disp:undefined;
 const tint=L.kind==='boss'?'#c6a6ff':L.kind==='hq'?dialogueNameColor(I.disp,'#a9dcfa'):dialogueNameColor(L.who,'#cfd6e6');
 const pw=Math.round(VW*.92),ph=Math.round(VH*.25),x=Math.round((VW-pw)/2),y=Math.round(VH*.43);
 dlgBox._tw={key:String(state)+'|'+L.who+'|'+L.text,count:I.shown,at:performance.now(),auto:false};
 dlgBox({who:L.who,portrait:L.kind==='pilot'?I.lead:false,portraitKey,full:L.text,shown:L.text.slice(0,I.shown),fade:1,tint,pw,ph,x,y,emo:L.kind==='pilot'&&I.i===0?'idle':undefined});
}
// the fight clock counts the fight, not the conversation (it already skips the entry the same way)
const FB2_CLOCK=encounterClockTick;
encounterClockTick=function(b,active,dt){if(b&&fb2IntroActive()&&b===fb2Intro.boss)return;return FB2_CLOCK.apply(this,arguments);};
const FB2_WORLD=drawWorld;
drawWorld=function(dt){const r=FB2_WORLD.apply(this,arguments);if(fb2IntroActive()){fb2StunDraw();fb2IntroDraw();}return r;};

/* ---------------------------------------------------------------------------------------------
   C. STAGE 6 - THE STEALTH FLIGHTS REPLACE THE BOMBERS
   "The bomber jets on stage 6, I dont like these type of jets. Use the stealth fighter jets that are
   blue, palette swap them to red, and another new enemy to green. The red ones shoot regular missiles
   that lock retinas on us, the green ones drop the atom bombs ... make an orange one with machine gun
   turrets ... when theyre coming left to right, we should see arrows letting us know its coming left,
   its coming right, its coming down etc with our asterisk and warning box system."

   Art: assets/game/levels/stage_06/enemies/stealth_1002/{red,green,orange}.png (cells east/west/south/north), built by
   _BUILD_SOURCE/stealth_jets_1002.py - red/green are hue rotations of the authored blue jet's paint,
   orange is a SpriteCook edit of the blue jet (wing gatlings + chin gun). Baked offline: the 1001 runtime
   swap read pixels with getImageData, which a file:// page refuses.

   Replaced: every s6bomber the stage spawns (the plan's lateral runs, both reinforcement directors) and
   the seven cardinal s6StrikeSpawn passes. Each flight is WARNED first - the warning box (the lane band
   over the strip it will fly), the impact-imminent asterisk at the edge it enters from, and the escape
   arrow plate pointing the way it travels, all stepping green -> yellow -> red with the shared warning
   beeps - and only then does the jet enter.
     RED     one retina lock on the pilot, two regular missiles off the nose (lock-bound steering;
             a roll, somersault or dash breaks it - the 0912q header rule).
     GREEN   Lizzie's atom bomb onto a committed reticle (the 0929 atomic run).
     ORANGE  wing gatlings + chin gun: short aimed bursts while it crosses.
   The opening assault squadron keeps its own gates; its jets now wear the role colour: every bomb carrier
   is GREEN, a Furious machine-gun gate ORANGE, an unarmed gate keeps the authored BLUE.
   --------------------------------------------------------------------------------------------- */
const FB2_ROLES=['red','green','orange'];
for(const r of FB2_ROLES)XART._src['fb2_stealth_'+r]='assets/game/levels/stage_06/enemies/stealth_1002/'+r+'.png';
const FB2_DIR_FRAME={east:0,west:1,south:2,north:3};
const FB2_DIR_ANG={east:0,west:Math.PI,south:Math.PI/2,north:-Math.PI/2};
let fb2Flights=[],fb2RoleSerial=0;
function fb2Warm(){for(const k of ['fb2_stealth_red','fb2_stealth_green','fb2_stealth_orange','warn_escape_arrow_0916','lz_bomb','bmfx_alert_green_impact_imminent','bmfx_alert_yellow_impact_imminent','bmfx_alert_red_impact_imminent'])try{XART.rdy(k);}catch(_w){}}
function fb2FlightPlan(direction,role){
 const L=camLeftX(),R=camRightX(),T=targetShip((L+R)/2,VH/2),side=direction==='east'||direction==='west';
 const y=side?clamp(T.y-[150,130,110][fr27Difficulty()],viewTopY()+80,VH*.56):0;
 const x=side?0:clamp(T.x+(fb2RoleSerial%2?-60:60),L+60,R-60);
 const q={direction,role:role||FB2_ROLES[fb2RoleSerial++%3],x,y,t:0,warn:[1.55,1.35,1.2][fr27Difficulty()],id:'fb2flight-'+(++fb2Flights._n||(fb2Flights._n=1))};
 fb2Warm();fb2Flights.push(q);combatWarningTick(q,q.id,0,q.warn);return q;
}
fb2Flights._n=0;
function fb2FlightSpawn(q){
 const dir=q.direction,side=dir==='east'||dir==='west',L=camLeftX(),R=camRightX();
 const x=side?(dir==='east'?L-80:R+80):q.x,y=side?q.y:(dir==='south'?viewTopY()-80:VH+80);
 const e=spawnEnemy('s1jetbomber_b',x,y,{route:'straight'});if(!e)return null;
 e.x=x;e.y=y;e.t=0;e.pattern='s6strike';e.shoots=false;e.fk=null;e._atk='none';e.spin=0;e._esw=null;e._noSep=true;
 e.w=side?92:74;e.h=side?70:92;e._s6Strike={direction:dir,t:0,racks:0,cd:999};
 e._faceAng={east:Math.PI/2,west:-Math.PI/2,south:Math.PI,north:0}[dir];
 e._fb2Stealth={role:q.role,direction:dir,t:0,shots:0,cd:.35};
 e.hp=e.maxhp=[22,28,34][fr27Difficulty()];q.jet=e;
 (Audio.SFX.tlvJetEngine||Audio.SFX.enemyShoot||function(){})();
 return e;
}
function fb2FlightsTick(dt){
 if(run.stage!==6){fb2Flights.length=0;return;}
 for(const q of fb2Flights){q.t+=dt;combatWarningTick(q,q.id,q.t,q.warn);if(!q.spawned&&q.t>=q.warn){q.spawned=true;fb2FlightSpawn(q);}}
 for(let i=fb2Flights.length-1;i>=0;i--)if(fb2Flights[i].spawned)fb2Flights.splice(i,1);
}
function fb2AtomBomb(e){
 const T=targetShip(e.x,e.y),n=fr27Difficulty();
 if(groundTargetingFx.filter(q=>q._fb2Atom&&!q.dead).length>=[2,3,4][n])return;
 s67AssaultWarm&&s67AssaultWarm();
 const q=groundTargetingSpawn({kind:'missile',x:clamp(T.x,camLeftX()+42,camRightX()-42),y:clamp(T.y,viewTopY()+85,VH-48),owner:e,
  track:false,lane:false,warn:[1.75,1.6,1.45][n],radius:[32,35,38][n],size:104,active:.55,sound:'atomicDetonate',shake:12,
  onImpact:g=>{if(typeof s67AtomicImpact==='function')s67AtomicImpact(g);else explode(g.x,g.y,90,'red');}});
 if(q){q._fb2Atom=true;q._s67Atom=true;q._jetBomb={x:e.x,y:e.y};}
 (Audio.SFX.atomicLaunch||Audio.SFX.missile||function(){})();
}
function fb2Gun(e){
 const S=e._fb2Stealth,a=FB2_DIR_ANG[S.direction],T=targetShip(e.x,e.y);
 // the two wing gatlings (+-22 px across the heading) and the chin gun on the nose
 const ox=-Math.sin(a),oy=Math.cos(a),nose={x:e.x+Math.cos(a)*30,y:e.y+Math.sin(a)*30};
 const aimA=Math.atan2(T.y-e.y,T.x-e.x);
 const shot=(x,y,ang,spd,col)=>{const last=eBullets[eBullets.length-1];eMG(x,y,ang,spd,col);const b=eBullets[eBullets.length-1];
  if(b&&b!==last){b._fb2Src=e;e._fb2Rounds=(e._fb2Rounds||0)+1;}};
 for(const s of [-1,1])shot(e.x+ox*22*s+Math.cos(a)*12,e.y+oy*22*s+Math.sin(a)*12,aimA+s*.05,3.9,'#ffb347');
 shot(nose.x,nose.y,aimA,4.2,'#ffd27a');
}
function fb2FlightTick(e,dt){
 const S=e._fb2Stealth,n=fr27Difficulty();S.t+=dt;S.cd-=dt;
 const side=S.direction==='east'||S.direction==='west',speed=(side?[300,345,390]:[230,265,300])[n],a=FB2_DIR_ANG[S.direction];
 e.x+=Math.cos(a)*speed*dt;e.y+=Math.sin(a)*speed*dt;e.spin=0;e._polishBomberCD=999;   // its role is its only attack
 const inside=e.x>camLeftX()+40&&e.x<camRightX()-40&&e.y>viewTopY()+30&&e.y<VH-40;
 if(inside&&S.cd<=0){
  if(S.role==='red'&&S.shots<1){S.shots++;S.cd=99;
   // ONE retina, two regular missiles off the nose - the second queues on the same lock
   enemyLockOn(e,[1.0,.9,.8][n]);enemyLockOn(e,[1.0,.9,.8][n]+.26);}
  else if(S.role==='green'&&S.shots<[1,1,2][n]){S.shots++;S.cd=.7;fb2AtomBomb(e);}
  else if(S.role==='orange'&&S.shots<[3,4,5][n]){S.shots++;S.cd=[.42,.36,.30][n];fb2Gun(e);}
 }
 if(S.t>7||e.x<camLeftX()-140||e.x>camRightX()+140||e.y<viewTopY()-140||e.y>VH+140)e.dead=true;
}
const FB2_STRIKE_TICK=s6StrikeTick;
s6StrikeTick=function(e,dt){if(e&&e._fb2Stealth)return fb2FlightTick(e,dt);return FB2_STRIKE_TICK.apply(this,arguments);};
function fb2SheetCell(key,frame,x,y,s,e){
 if(!XART.rdy(key))return false;const im=XART.get(key),c=frame*128;
 ctx.save();ctx.imageSmoothingEnabled=false;ctx.drawImage(im,c,0,128,128,x,y,s,s);
 if(e&&e.flash>0){const t=xartTint(key,'#ffffff',1);if(t){ctx.globalAlpha=Math.min(1,e.flash*9);ctx.drawImage(t,c,0,128,128,x,y,s,s);}}
 ctx.restore();return true;
}
function fb2MissionRole(A){
 if(A.kind==='bomb'||A.direction==='east'||A.direction==='west'||A.attack===2)return 'green';
 if(A.n===2&&A.attack===1)return 'orange';
 return null;   // an unarmed gate keeps the authored blue
}
const FB2_FLEET=furyFleetDraw;
furyFleetDraw=function(e){
 if(e&&e._fb2Stealth){if(e.dead||e._dyingT!=null)return true;const s=104;
  if(!fb2SheetCell('fb2_stealth_'+e._fb2Stealth.role,FB2_DIR_FRAME[e._fb2Stealth.direction],e.x-s/2,e.y-s/2,s,e))return true;
  e._drawW=e._drawH=s;return true;}
 if(e&&e._mission29&&run.stage===6){const A=e._mission29,role=fb2MissionRole(A);
  if(role){if(e.dead||e._dyingT!=null)return true;const s=e._s67Draw||100;
   if(fb2SheetCell('fb2_stealth_'+role,FB2_DIR_FRAME[A.direction],e.x-s/2,e.y-s/2,s,e)){e._drawW=e._drawH=s;return true;}}
  /* blue: the authored sheet, unrecoloured */
  if(e.dead||e._dyingT!=null)return true;const s=e._s67Draw||100;
  if(typeof missionCell==='function'&&missionCell('bluejets',FB2_DIR_FRAME[A.direction]%3,e.x-s/2,e.y-s/2,s,s)){
   if(e.flash>0&&typeof s67CellFlash==='function')s67CellFlash('bluejets',FB2_DIR_FRAME[A.direction]%3,e.x-s/2,e.y-s/2,s,s,e);e._drawW=e._drawH=s;return true;}
 }
 return FB2_FLEET.apply(this,arguments);
};
// the replacements: the strike passes, and every s6bomber the stage asks for
s6StrikeSpawn=function(direction){fb2FlightPlan(direction);return null;};
const FB2_SPAWN=spawnEnemy;
spawnEnemy=function(type){
 if(type==='s6bomber'&&run.stage===6){
  const o=arguments[3]||{},x=arguments[1];let dir;
  if(o._side===1)dir='east';else if(o._side===-1)dir='west';
  else if(o._jetManeuver||x<camLeftX()-20||x>camRightX()+20)dir=x<(camLeftX()+camRightX())/2?'east':'west';
  else dir='south';
  fb2FlightPlan(dir);return null;
 }
 return FB2_SPAWN.apply(this,arguments);
};
// the warning: box (lane band), asterisk at the entry edge, arrow pointing the way it flies
function fb2FlightWarnDraw(){
 if(run.stage!==6||!fb2Flights.length)return;
 const L=camLeftX(),R=camRightX(),top=viewTopY(),arrow=XART.rdy('warn_escape_arrow_0916')?XART.get('warn_escape_arrow_0916'):null;
 for(const q of fb2Flights){if(q.spawned)continue;
  const p=clamp(q.t/q.warn,0,1),col=l23FovPhase(p),side=q.direction==='east'||q.direction==='west';
  const x=side?L:q.x-38,y=side?q.y-31:top,w=side?(R-L):76,h=side?62:viewH();
  const beat=Math.floor(p*L23_WARN_ARROWS),frac=p*L23_WARN_ARROWS-beat,lit=frac<.62;
  ctx.save();ctx.globalAlpha=.16+.14*p;ctx.fillStyle=col==='green'?'#32e891':col==='yellow'?'#ffd74b':'#ff4840';ctx.fillRect(x,y,w,h);
  ctx.globalAlpha=lit?.85:.45;ctx.strokeStyle=ctx.fillStyle;ctx.lineWidth=2;ctx.strokeRect(x+1,y+1,w-2,h-2);ctx.restore();
  // asterisk at the edge it enters from
  const ex=q.direction==='east'?L+26:q.direction==='west'?R-26:q.x,ey=side?q.y:(q.direction==='south'?top+30:VH-60);
  const ak='bmfx_alert_'+col+'_impact_imminent';
  if(XART.rdy(ak)){const im=XART.get(ak),s=34;ctx.save();ctx.globalAlpha=lit?1:.55;ctx.drawImage(im,ex-s/2,ey-s/2,s,s);ctx.restore();}
  // arrows along the lane, pointing the way it travels
  if(arrow&&lit){const ah=side?30:28,aw=ah*(arrow.naturalWidth||arrow.width)/Math.max(1,arrow.naturalHeight||arrow.height),a=FB2_DIR_ANG[q.direction];
   const pts=side?[.36,.56,.76].map(f=>({x:q.direction==='east'?lerp(L,R,f):lerp(R,L,f),y:q.y})):[.30,.48,.66].map(f=>({x:q.x,y:q.direction==='south'?lerp(top,VH,f):lerp(VH,top,f)}));
   for(const pt of pts){ctx.save();ctx.globalAlpha=col==='red'?.95:.78;ctx.imageSmoothingEnabled=false;ctx.translate(Math.round(pt.x),Math.round(pt.y));ctx.rotate(a);ctx.drawImage(arrow,-aw/2,-ah/2,aw,ah);ctx.restore();}}
 }
}
const FB2_S6DRAW=s6OpeningDraw;
s6OpeningDraw=function(){const r=FB2_S6DRAW.apply(this,arguments);fb2FlightWarnDraw();return r;};
const FB2_UPD2=updatePlay;
updatePlay=function(dt){const r=FB2_UPD2.apply(this,arguments);if(state===GS.PLAY&&!(BOFCinematicDirector&&BOFCinematicDirector.live))fb2FlightsTick(dt||0);return r;};
const FB2_STAGE=beginStage;
beginStage=function(){fb2Flights.length=0;return FB2_STAGE.apply(this,arguments);};

/* ---------------------------------------------------------------------------------------------
   D. STAGE 6 - THE HARRIER'S LAUNCHED JETS FIGHT LIKE A SQUADRON
   "those jets that come out of the harrier to attack us, needs to be more advanced AI and proper
   attacks."
   The Warhive's hivewing escorts (hivewingTick, 0918) held a slot, fired 3-round darts aimed at where the
   pilot IS, and took a strafing dive after a 0.4s nose flash aimed at where the pilot WAS - every jet on
   its own, and a tell too short to read through the carrier's own fire. On top of that base, now:
     - LEAD AIM: every burst and dive leads a moving pilot (aimPlayer's lead model), so circling in place no
       longer dodges a whole squadron for free; standing still still eats the same shots it always did;
     - A WARNED DIVE: the dive is telegraphed with the shared lane warning (green -> yellow -> red) along
       the committed vector; the vector LOCKS at 60% of the tell, so a late break still dodges it;
     - A SQUADRON BRAIN (fb2SquadTick), one call per frame, picks coordinated plays between free jets:
         PINCER   two jets break to opposite edges above the pilot, warn their crossing lanes, and fire
                  converging 6-round streams (the gap between the two lanes is the way out);
         MISSILE  one jet opens a retina lock and launches two regular missiles (lock-bound - a roll,
                  somersault or dash breaks it, 0912q);
         BRACKET  the free jets re-slot either side of the pilot's column instead of over it;
     - LANE DISCIPLINE: a jet that has sat in the pilot's fire lane for 0.35s sidesteps out of it.
   Plays get more frequent with difficulty. Nothing here touches the launch, peel or the boss's own fight.
   --------------------------------------------------------------------------------------------- */
let fb2Squad={next:3.5,serial:0};
function fb2HwFace(e,a){const fa=Math.atan2(Math.cos(a),-Math.sin(a));e._faceAng=fa;e.spin=fa-Math.PI;}
function fb2HwFree(e){return e&&e._elx==='hivewing'&&!e.dead&&e._dyingT==null&&!e._hwLaunch&&!e._hwPeel&&!e._hwD&&!e._fb2Tac&&e.y>VH*.12;}
function fb2SquadTick(dt){
 if(run.stage!==6)return;
 const jets=enemies.filter(e=>e&&e._elx==='hivewing'&&!e.dead&&e._dyingT==null);
 if(!jets.length){fb2Squad.next=Math.max(fb2Squad.next,2.5);return;}
 fb2Squad.next-=dt;if(fb2Squad.next>0)return;
 const n=fr27Difficulty(),free=jets.filter(fb2HwFree);fb2Squad.next=[6.4,5.0,3.9][n];
 if(!free.length){fb2Squad.next=1.2;return;}
 const plays=['pincer','missile','bracket'],play=plays[fb2Squad.serial++%3];
 if(play==='pincer'&&free.length>=2){
  const T=targetShip(camLeftX()+viewW()/2,VH/2),y=clamp(T.y-[190,175,160][n],VH*.18,VH*.52);
  const pair=free.slice(0,2).sort((a,b)=>a.x-b.x);
  pair.forEach((e,i)=>{e._fb2Tac={kind:'pincer',side:i?1:-1,phase:'move',t:0,x0:e.x,y0:e.y,tx:i?camRightX()-46:camLeftX()+46,ty:y+(i?18:-18),shots:0,id:'fb2pin-'+fb2Squad.serial+'-'+i};});
  return;
 }
 if(play==='missile'&&!playerLocks.some(L=>L.src&&L.src._elx==='hivewing'&&(L.state==='arming'||L.state==='locked'))){
  const e=free[0];e._fb2Tac={kind:'missile',phase:'arm',t:0};const d=[1.05,.95,.85][n];
  enemyLockOn(e,d);enemyLockOn(e,d+.28);e._muz=.2;return;
 }
 // bracket: alternate the free jets either side of the pilot's column
 free.forEach((e,i)=>{e._fb2Bracket={side:i%2?1:-1,t:[2.6,3.0,3.4][n]};});
}
function fb2HwTacTick(e,dt,X){
 const A=e._fb2Tac;A.t+=dt;const n=fr27Difficulty();
 if(A.kind==='missile'){                                  // hold steady and keep the nose on the pilot while the lock arms
  const T=targetShip(e.x,e.y);fb2HwFace(e,Math.atan2(T.y-e.y,T.x-e.x));e.y+=Math.sin(A.t*6)*.4;
  if(A.t>1.5){e._fb2Tac=null;e._faceAng=Math.PI;e.spin=0;}return true;
 }
 if(A.phase==='move'){const p=clamp(A.t/1.05,0,1),k=p*p*(3-2*p);e.x=lerp(A.x0,A.tx,k);e.y=lerp(A.y0,A.ty,k);
  fb2HwFace(e,Math.PI/2-A.side*.9*k);
  if(p>=1){A.phase='warn';A.t=0;A.warn=[.72,.62,.54][n];A.a=aimPlayer(e.x,e.y,5,.9);}return true;}
 if(A.phase==='warn'){
  if(A.t<A.warn*.6)A.a=aimPlayer(e.x,e.y,5,.9);          // tracks, then COMMITS for the last 40%
  fb2HwFace(e,A.a);combatWarningTick(e,A.id,A.t,A.warn);
  if(A.t>=A.warn){A.phase='fire';A.t=0;A.cd=0;}return true;}
 if(A.phase==='fire'){A.cd-=dt;
  if(A.cd<=0&&A.shots<6){A.shots++;A.cd=.075;eShootT(e.x+Math.cos(A.a)*20,e.y+Math.sin(A.a)*20,A.a,5.2,'dart');e._muz=.1;}
  if(A.shots>=6&&A.t>.6){A.phase='return';A.t=0;A.x0=e.x;A.y0=e.y;}return true;}
 // return to the squadron slot
 const p=clamp(A.t/.9,0,1),k=p*p*(3-2*p),sx=clamp(hivewingSlotX(e,X),28,worldWidth()-28);
 e.x=lerp(A.x0,sx,k);e.y=lerp(A.y0,VH*X.band,k);fb2HwFace(e,lerp(A.a,Math.PI/2,k));
 if(p>=1){e._fb2Tac=null;e._faceAng=Math.PI;e.spin=0;e._hwDive=Math.max(e._hwDive||0,2.2);}return true;
}
const FB2_HWTICK=hivewingTick;
hivewingTick=function(e,dt,X){
 if(e._hwLaunch||e._hwPeel)return FB2_HWTICK.apply(this,arguments);
 if(e._fb2Tac&&fb2HwTacTick(e,dt,X))return;
 const n=fr27Difficulty(),D0=e._hwD,tell0=D0&&D0.st==='tell';
 // lane discipline: out of the pilot's fire lane
 const T=targetShip(e.x,e.y);
 if(!e._hwD&&Math.abs(T.x-e.x)<e.w*.55&&T.y>e.y)e._fb2Lane=(e._fb2Lane||0)+dt;else e._fb2Lane=0;
 if(e._fb2Lane>.35&&e._rollT==null&&typeof el8Roll==='function'){el8Roll(e,e.x<T.x?-1:1);e._fb2Lane=0;}
 const burst0=e._hwBurst||0;
 if(tell0&&D0._warn)D0.t=0;                 // the base releases its dive at 0.4s of tell; this tell is ours
 FB2_HWTICK.apply(this,arguments);
 // lead aim on a new burst
 if((e._hwBurst||0)>burst0)e._hwBA=aimPlayer(e.x,e.y,4.4,[.6,.8,.95][n]);
 // bracket: bias the slot to one side of the pilot's column for a while
 if(e._fb2Bracket&&!e._hwD){const B=e._fb2Bracket;B.t-=dt;const want=clamp(T.x+B.side*[70,78,86][n],34,worldWidth()-34);
  e.x+=clamp(want-e.x,-X.spd*.8*dt,X.spd*.8*dt);if(B.t<=0)e._fb2Bracket=null;}
 // the warned, committed dive
 const D=e._hwD;
 if(D&&D.st==='tell'){
  if(!tell0){D._warn=[.78,.66,.56][n];D._fa=aimPlayer(e.x,e.y,6.3,.9);}
  if(tell0)D._t2=(D._t2||0)+dt;
  if(D._t2<D._warn*.6)D._fa=aimPlayer(e.x,e.y,6.3,.9);
  combatWarningTick(e,'fb2dive',D._t2,D._warn);
  if(D._t2>=D._warn){D.st='run';D.t=0;D.a=D._fa;D.fcd=0;(Audio.SFX.whip||function(){})();}
 }
};
// the warning lanes for dives and pincers, drawn in world space with the shared field
const FB2_S6DRAW2=s6OpeningDraw;
s6OpeningDraw=function(){
 const r=FB2_S6DRAW2.apply(this,arguments);if(run.stage!==6)return r;
 for(const e of enemies){if(!e||e._elx!=='hivewing'||e.dead||e._dyingT!=null)continue;
  const D=e._hwD,A=e._fb2Tac;let a=null,p=0,w=22;
  if(D&&D.st==='tell'&&D._warn){a=D._fa;p=clamp((D._t2||0)/D._warn,0,1);w=e.w*.7;}
  else if(A&&A.kind==='pincer'&&A.phase==='warn'){a=A.a;p=clamp(A.t/A.warn,0,1);w=18;}
  if(a==null)continue;const L=Math.max(viewW(),VH)*1.2;
  combatWarningDraw(e,{x:e.x,y:e.y,ex:e.x+Math.cos(a)*L,ey:e.y+Math.sin(a)*L,progress:p,width:w,fieldOnly:false});
 }
 return r;
};
const FB2_UPD3=updatePlay;
updatePlay=function(dt){const r=FB2_UPD3.apply(this,arguments);if(state===GS.PLAY&&!(BOFCinematicDirector&&BOFCinematicDirector.live))fb2SquadTick(dt||0);return r;};
const FB2_STAGE2=beginStage;
beginStage=function(){fb2Squad={next:3.5,serial:0};return FB2_STAGE2.apply(this,arguments);};

/* ---------------------------------------------------------------------------------------------
   E. STAGE 6 - "WHO STAYED BEHIND AT BASE?!" AND SECRET WEAPON CALLISTO
   Mike's scene, after the fighters and the Harrier pass over the wing (the W.fake beat: "HARRIER BREAKING
   LEFT", Voss's taunt) and BEFORE the split-the-wing choice. The base flow is held at the end of that beat
   while this plays, and released into the choice exactly as before when it ends.
     - the team argument: Cole demands who defended the base; silence; "Not me", "Uhhh...", "Well...", "We
       were attacked and saw everyone was getting attacked and-";
     - Cole LOSES IT in generated shouting talk frames (dispatch_1002/cole_rage_0..2: snarl, yell, scream);
     - heads down ("Sorry boss..."); Cole calms down and lays out the split;
     - PLAYING COLE ONLY: "SECRET WEAPON CALLISTO / WEAPON STATUS = ACTIVATED" types letter by letter in the
       powerup banner face, ACTIVATED in green, flashing on five beeps; Cole explains the field tests and
       DEMONSTRATES: the fusion cannon charges and releases, then his level-7 lasers (the black four-wide rows
       and homing trident arch, coleTier 7) fire a long burst; the
       team reacts in shock, then the choice.
   It runs in play like the Stage-5 arrival - nothing pauses; the pilot's controls are held (the demo is
   scripted on the pilot's own ship), enemy rounds are cleared and nothing can hit the ship meanwhile.
   Speakers are drawn from the nine pilots in the air; nobody speaks a line as two people.
   --------------------------------------------------------------------------------------------- */
for(let i=0;i<3;i++)XART._src['fb2_cole_rage_'+i]='assets/game/shared/combat/dispatch_1002/cole_rage_'+i+'.png';
let fb2Talk=null;
function fb2TalkActive(){return !!(fb2Talk&&!fb2Talk.done&&run.stage===6&&state===GS.PLAY);}
function fb2TeamPool(){
 const W=s6Wing,seen=new Set(),out=[];const add=k=>{k=String(k||'').toLowerCase();if(k&&k!=='cole'&&!seen.has(k)){seen.add(k);out.push(k);}};
 add(run.pilot);if(W&&W.ships)for(const q of W.ships)if(q.phase!=='leave')add(q.key);
 for(const k of ['decker','axel','lizzie','falva','yuri','freezer','juggernaut','maverick'])if(out.length<8)add(k);
 return out;
}
function fb2TeamScript(){
 const T=fb2TeamPool(),C='COLE',P=k=>k.toUpperCase(),cole=String(run.pilot).toLowerCase()==='cole';
 const L=(who,text,emo,extra)=>Object.assign({who,text,emo},extra||{});
 const r=k=>L(C,k,'rage',{rage:true});
 const s=[
  L(C,'DAMMIT! WHO STAYED BEHIND AT BASE TO DEFEND IT?!','anger'),
  L(P(T[0]),'........','sad'),L(P(T[1]),'......','sad'),
  L(P(T[2]),'NOT ME.','sad'),L(P(T[3]),'UHHH....','crash'),L(P(T[4]),'WELL...','sad'),
  L(P(T[5%T.length]),'WE WERE ATTACKED, AND WE SAW EVERYONE WAS GETTING ATTACKED, AND-','crash'),
  r('I SPECIFICALLY TOLD ALL OF YOU TO LEAVE AT LEAST ONE OR TWO BEHIND SO THAT WOULD NOT HAPPEN!'),
  r('DO YOU HAVE ANY IDEA WHAT DECKER WAS WORKING ON?! THEY STOLE OUR SECRET WEAPONS - THE ONES WE NEED TO DESTROY WHATEVER IS ATTACKING US!'),
  r('YOU FOOLS!'),
  L(P(T[0]),'......','sad'),L(P(T[1]),'.....','sad'),L(P(T[2]),'SORRY, BOSS...','sad'),
  L(C,'...IT IS OKAY. I HAVE AN IDEA.','idle'),
  L(C,'SINCE WE ARE ALL HERE, WE CAN SPLIT UP. WHOEVER COMES WITH ME, WE ARE GOING TO GO GET OUR TECH BACK.','idle'),
  L(C,'THE REST OF YOU - DO NOT LET THAT HARRIER GET TO THE CITY!','anger')];
 if(cole){
  s.push({kind:'callisto'});
  s.push(L(C,'WHAT WE DID NOT TELL YOU GUYS IS THAT DECKER LET ME DO A COUPLE OF PRIVATE FIELD TESTS. ALLOW ME TO DEMONSTRATE.','idle'));
  s.push({kind:'demo'});
  s.push(L(P(T[0]),'OH....','crash'),L(P(T[1]),'OMG...','crash'),L(P(T[2]),'.......','crash'),
   L(P(T[3]),'THEY ARE GOING TO PAY. YOU ARE RIGHT. LET US GET EM!','anger'));
 }
 return s;
}
function fb2TalkStart(){
 fb2Talk={beats:fb2TeamScript(),i:0,t:0,shown:0,age:0,done:false};
 eBullets.length=0;Input.clearTaps&&Input.clearTaps();
 for(let i=0;i<3;i++)try{XART.rdy('fb2_cole_rage_'+i);}catch(_w){}
}
function fb2TalkNext(){const S=fb2Talk;S.i++;S.t=0;S.shown=0;S.ph=null;if(S.i>=S.beats.length){S.done=true;Input.clearTaps&&Input.clearTaps();}}
const FB2_CALLISTO=['SECRET WEAPON CALLISTO','WEAPON STATUS = ','ACTIVATED'];
function fb2CallistoTick(S,B,dt){
 const cps=26,l1=FB2_CALLISTO[0].length/cps,l2=(FB2_CALLISTO[1].length+FB2_CALLISTO[2].length)/cps;
 // five beeps on the flash, after the second line has typed
 const beats=[0,1,2,3,4].map(k=>l1+.25+l2+.15+k*.24);
 for(const b of beats)if(S.t-dt<b&&S.t>=b){try{(Audio.SFX.retinaLockBeep||Audio.SFX.blip||function(){})();}catch(_b){}}
 if(S.t>=beats[4]+1.0)fb2TalkNext();
}
function fb2CallistoDraw(S){
 const art=typeof uiFontArt==='function'?uiFontArt():null;if(!art||!artReady(art))return;
 const cps=26,t=S.t,[a,b,c]=FB2_CALLISTO,l1=a.length/cps,t2=t-l1-.25;
 const eq=stageGlyph(art,'=')?b:b.replace('= ',': ');
 let H=Math.max(15,Math.round(VH*.047));while(H>11&&stageWidth(art,eq+c,H,.07)>VW-26)H--;
 ctx.save();worldXformEscape();
 const y1=Math.round(VH*.33),y2=y1+H+12;
 const s1=a.slice(0,Math.floor(t*cps));stageText(art,s1,VW/2-stageWidth(art,a,H,.07)/2+stageWidth(art,s1,H,.07)/2,y1,H,null,0,1,.07);
 if(t2>0){const full=eq+c,n=Math.floor(t2*cps),shown=full.slice(0,n),w=stageWidth(art,full,H,.07),x0=VW/2-w/2;
  const pre=shown.slice(0,eq.length),act=shown.slice(eq.length);
  stageText(art,pre,x0+stageWidth(art,pre,H,.07)/2,y2,H,null,0,1,.07);
  if(act){const done=n>=full.length,since=t2-full.length/cps,lit=!done||since<.15||Math.floor((since-.15)/.12)%2===0;
   const ax=x0+stageWidth(art,eq,H,.07);
   if(lit)stageText(art,act,ax+stageWidth(art,act,H,.07)/2,y2,H,'#39ff5a',.95,1,.07);}}
 ctx.restore();
}
function fb2DemoTick(S,dt){
 const D=S.demo||(S.demo={t:0,save:{w:run.weapon,lv:run.wlevel,lvs:(run.wlevels||[]).slice()},fired:0});D.t+=dt;
 player.x+=clamp(camLeftX()+viewW()/2-player.x,-160*dt,160*dt);
 if(D.t<1.35){run.weapon=0;run.wlevel=8;if(run.wlevels)run.wlevels[0]=8;coleFuseTick(dt,true);}        // the fusion cannon charges...
 else if(!D.released){D.released=true;run.weapon=0;run.wlevel=8;coleFuseTick(dt,false);shake=Math.max(shake,6);}   // ...and releases
 else if(D.t>2.1&&D.t<4.4){run.weapon=0;run.wlevel=7;if(run.wlevels)run.wlevels[0]=7;                  // then his level-7 lasers:
  D.cd=(D.cd||0)-dt;if(D.cd<=0){D.cd=.085;                                                                   // the black four-wide rows + trident arch
   // a timed Sonic Boom (stage 6 grants abilities at random) claims the trigger; suspend it for the shot only
   const before=pBullets.length,son=run.sonicT;run.sonicT=0;try{pShoot();}catch(_p){}finally{run.sonicT=son;}
   if(pBullets.length>before)D.fired+=pBullets.length-before;}}
 else if(D.t>=4.9){run.weapon=D.save.w;run.wlevel=D.save.lv;if(run.wlevels)D.save.lvs.forEach((v,i)=>run.wlevels[i]=v);fb2TalkNext();}
}
function fb2TalkTick(dt){
 const S=fb2Talk;if(!S||S.done)return;if(!fb2TalkActive()){S.done=true;return;}
 S.age+=dt;S.t+=dt;eBullets.length=0;
 const B=S.beats[S.i];if(!B)return fb2TalkNext();
 if(B.kind==='callisto')return fb2CallistoTick(S,B,dt);
 if(B.kind==='demo')return fb2DemoTick(S,dt);
 const cps=38,full=B.text.length;
 if(S.age>.35&&(Input.tapAny?Input.tapAny(keybind.fire):Input.menuConfirm())){
  if(S.shown<full){S.shown=full;S.t=Math.max(S.t,full/cps);}else fb2TalkNext();return;}
 const n=Math.min(full,Math.floor(S.t*cps));if(typeof dialogueLetterTicks==='function')dialogueLetterTicks(B.text,S.shown,n);S.shown=Math.max(S.shown,n);
 if(S.t>=full/cps+(B.text.replace(/[.\s]/g,'').length?1.6:1.05))fb2TalkNext();
}
function fb2TalkDraw(){
 if(!fb2TalkActive())return;const S=fb2Talk,B=S.beats[S.i];if(!B)return;
 if(B.kind==='callisto')return fb2CallistoDraw(S);
 if(B.kind==='demo')return;
 const pk=B.who.toLowerCase(),typing=S.shown<B.text.length;
 let portraitKey,emo=B.emo,portrait=pk;
 if(B.rage){portraitKey='fb2_cole_rage_'+(typing?[0,1,2,1][Math.floor(performance.now()/110)%4]:2);portrait=false;}
 const pw=Math.round(VW*.92),ph=Math.round(VH*.25),x=Math.round((VW-pw)/2),y=Math.round(VH*.30);
 dlgBox._tw={key:String(state)+'|'+B.who+'|'+B.text+'|'+S.i,count:S.shown,at:performance.now(),auto:false};
 dlgBox({who:B.who,portrait,portraitKey,emo:emo==='idle'?undefined:emo,full:B.text,shown:B.text.slice(0,S.shown),fade:1,
  tint:dialogueNameColor(B.who,'#cfd6e6'),pw,ph,x,y});
}
const FB2_WING=s6WingTick;
s6WingTick=function(dt){
 const W=s6Wing;
 if(W&&W.fake&&!W._fb2Talked&&W.fake.t>=5.5){
  if(!fb2Talk){fb2TalkStart();W.line=null;}             // the Voss taunt's radio box gives way to the scene
  if(!fb2Talk.done)W.fake.t=5.5-dt;                      // hold the beat; the base adds dt back
  else{W._fb2Talked=true;fb2Talk=null;}                  // released: the base runs on into the choice
 }
 return FB2_WING.apply(this,arguments);
};
const FB2_CTRL2=s6OpeningControlsLocked;
s6OpeningControlsLocked=function(){return fb2TalkActive()||FB2_CTRL2.apply(this,arguments);};
const FB2_PHIT=playerHit;
playerHit=function(){if(fb2TalkActive()||fb2IntroActive())return;return FB2_PHIT.apply(this,arguments);};
const FB2_UPD4=updatePlay;
updatePlay=function(dt){const r=FB2_UPD4.apply(this,arguments);if(fb2Talk&&state===GS.PLAY)fb2TalkTick(dt||0);return r;};
const FB2_WORLD2=drawWorld;
drawWorld=function(dt){const r=FB2_WORLD2.apply(this,arguments);if(fb2TalkActive())fb2TalkDraw();return r;};
const FB2_STAGE3=beginStage;
beginStage=function(){fb2Talk=null;return FB2_STAGE3.apply(this,arguments);};

/* ---------------------------------------------------------------------------------------------
   F. STAGE 6 - TURBULENCE
   "we also need turbulance noises generated for the harrier and them going over us and stuff."
   Two generated cues (ElevenLabs text-to-sound v2; mastered by _BUILD_SOURCE/turbulence_1002.py):
     turbCarrier1002  heavy buffeting LOOP, layered under the carrier turbine wherever the Harrier passes over
                      (the opening flyover and the "Harrier breaking left" beat) - it rides carrierTurbine's own
                      loopOn/loopOff calls, so it starts, holds and fades exactly with the turbine;
     jetWash1002      a fighter's wake slamming the cockpit, ONE per jet, the first time a Stage-6 jet (stealth
                      flights, the assault squadron, Harrier escorts, the opening's launched fighters) passes within
                      reach of the pilot, with a small shake.
   This layer loads after game.js has built its audio pools from BOFA.sfx, so it registers its own pools the
   same lazy way (voices created on first use) plus their TAME rows - every sound needs one (0912j).
   --------------------------------------------------------------------------------------------- */
function fb2AddSfx(name,uri,tame){
 if(typeof Snd==='undefined'||!Snd||!Snd.pools)return false;
 if(typeof BOFA!=='undefined'&&BOFA.sfx)BOFA.sfx[name]=uri;
 if(!Snd.pools[name]){const list=[],slots=[];
  for(let i=0;i<3;i++)Object.defineProperty(list,i,{enumerable:true,get:function(){
   if(!slots[i])slots[i]={el:new window.Audio(),uri,attached:false,used:0};return Snd._touchVoice(slots[i]);}});
  Snd.pools[name]={list,slots,i:0};}
 if(Snd.TAME)Snd.TAME[name]=tame;
 if(Audio&&Audio.SFX&&!Audio.SFX[name])Audio.SFX[name]=function(){return Snd.play(name);};
 return true;
}
fb2AddSfx('turbCarrier1002','assets/game/shared/audio/sounds/turbulence_carrier_1002.mp3',{g:0.62,native:true,min:0.00});
fb2AddSfx('jetWash1002','assets/game/shared/audio/sounds/jetwash_1002.mp3',{g:0.72,native:true,min:0.28});
if(typeof Snd!=='undefined'&&Snd&&Snd.loopOn){
 const FB2_LOOPON=Snd.loopOn,FB2_LOOPOFF=Snd.loopOff;
 Snd.loopOn=function(name,vol){const r=FB2_LOOPON.apply(this,arguments);if(name==='carrierTurbine')FB2_LOOPON.call(this,'turbCarrier1002',vol==null?1:Math.min(1,vol*1.25));return r;};
 Snd.loopOff=function(name){const r=FB2_LOOPOFF.apply(this,arguments);if(name==='carrierTurbine')FB2_LOOPOFF.call(this,'turbCarrier1002');return r;};
}
function fb2Wash(x,y){
 if(typeof Snd!=='undefined'&&Snd.play)Snd.play('jetWash1002');
 shake=Math.max(shake,1.3);
}
function fb2WashTick(){
 if(run.stage!==6||player.dead)return;
 for(const e of enemies){
  if(!e||e.dead||e._dyingT!=null||e._fb2Wash)continue;
  if(!(e._fb2Stealth||e._mission29||e._s6Strike||e._elx==='hivewing'))continue;
  if(Math.abs(e.x-player.x)<Math.max(60,(e.w||60)*.8)&&Math.abs(e.y-player.y)<Math.max(56,(e.h||60)*.75)){e._fb2Wash=1;fb2Wash(e.x,e.y);}
 }
 const O=s6Opening;
 if(O&&O.carrierJets)for(const j of O.carrierJets){
  if(j._fb2Wash)continue;
  if(Math.abs(j.x-player.x)<90&&Math.abs(j.y-player.y)<70){j._fb2Wash=1;fb2Wash(j.x,j.y);}
 }
}
const FB2_UPD5=updatePlay;
updatePlay=function(dt){const r=FB2_UPD5.apply(this,arguments);if(state===GS.PLAY)fb2WashTick();return r;};

/* ---------------------------------------------------------------------------------------------
   G. THE FUSION BEAM IS A SOLID PLASMA COLUMN, AND EVERY ICON KEEPS ONE SIZE
   "the fusion cannon beams. they should not be spikey lasers, that makes no sense at all. solid pink beams like
   falva's laser beams, but more 'Fusion' energy like while still pinkishpurple. also, their weapon pick up icons
   are very small in game..not sure why. we should be keeping a unified system of h/w for each icon as an engine
   rule."

   BEAM. Both fusion weapons drew a branching lightning lance: the space-slot Fusion (fusion_0930/beam.png) and
   Cole's level-8 fusion cannon (the green enemy laser, hue-rotated with a CSS filter). Both now draw
   assets/game/shared/player_weapons/fusion_1002/beam.png - a SpriteCook edit of Falva's own solid laser plate into a pink-violet
   plasma column with a white-hot core and a contained double helix - animated by
   _BUILD_SOURCE/fusion_beam_1002.py so the helix flows up the beam while the silhouette stays fixed. Damage,
   speed, hit width and charge scaling are unchanged; the column fills the width the round already hits with.

   ICONS - THE ENGINE RULE. iconBlit draws at a requested HEIGHT, and each art family carries its own transparent
   margin inside its cell: measured in Chromium through iconBlit itself, the space Fusion badges put only 65-77 px
   of ink on a 100 px request (and a different amount per tier) where the volley badges put 100, Thermoshock 72.
   Now every icon with a measured ink box (assets/icon_ink_1002.js, built by _BUILD_SOURCE/icon_ink_1002.py from
   the RAW draw) is drawn so its INK fills one unified box: ink height = the requested height, never wider than
   FB2_ICON_U x height, centred in that box - and every icon reports the same box width back to its caller.
   An icon with no entry draws exactly as before; add new families by re-running the measuring script.
   --------------------------------------------------------------------------------------------- */
XART._src.fb2_fusion_beam='assets/game/shared/player_weapons/fusion_1002/beam.png';
const FB2_BEAM={key:'fb2_fusion_beam',path:'assets/game/shared/player_weapons/fusion_1002/beam.png',frames:[0,1,2,3,4,5,6,7].map(k=>[k*25,0,25,147]),fps:14};
if(typeof FUSION30_ART!=='undefined')FUSION30_ART.beam=FB2_BEAM;   // fusion30Cell reads the table at call time
function fb2BeamDraw(x,y,w,h,t){
 if(!XART.rdy(FB2_BEAM.key))return false;const r=FB2_BEAM.frames[Math.floor((t||0)*FB2_BEAM.fps)%8];
 ctx.save();ctx.imageSmoothingEnabled=false;ctx.drawImage(XART.get(FB2_BEAM.key),r[0],r[1],r[2],r[3],x-w/2,y-h/2,w,h);ctx.restore();return true;
}
coleFuseDraw=function(b){
 // the two piercing lances keep their hit box (14 x 56); the column is drawn a touch wider so its sheath reads
 return fb2BeamDraw(b.x,b.y,b.w*1.35,b.h*1.15,(typeof efxClock==='number'?efxClock:performance.now()/1000)+b.x*.01);   // a draw never advances the round's own clock
};
const FB2_ICON_U=0.93;      // the unified icon box: height H, width 0.93 H (the badge family's own 104:112)
const FB2_ICONBLIT=iconBlit;
iconBlit=function(g,key,x,y,h,centred){
 const I=typeof ICON_INK_1002!=='undefined'&&key?ICON_INK_1002[key]:null;
 if(!I||!g||!(h>0))return FB2_ICONBLIT.apply(this,arguments);
 const [ix,iy,iw,ih,asp]=I,boxW=h*FB2_ICON_U;
 // the request height h2 at which the INK is exactly h tall, unless that ink would be wider than the box
 let h2=h/Math.max(.05,ih);if(iw*asp*h2>boxW)h2=boxW/Math.max(.05,iw*asp);
 const w2=asp*h2,dx=(ix+iw/2-.5)*w2,dy=(iy+ih/2-.5)*h2;
 const cx=centred?x:x+boxW/2,cy=centred?y:y+h/2;
 const r=FB2_ICONBLIT.call(this,g,key,cx-dx,cy-dy,h2,true);
 return r?boxW:r;
};
