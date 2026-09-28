"use strict";
/* HAMA (Mike 0928) - the second Hammer Time password, danced to the MC Hammer "U Can't Touch This"
   instrumental Mike supplied.

   "the hammer boss and his helpers will be mouthing and singing ... above them and doing the breakdown
   in sequence of the song. Everytime it goes Hammer time! he should hit the ground with his hammer twice
   in sequence of Hammer and Time ... throw his hammer up in the air behind him, grab a robot helper and
   chuck them at us while its also singing ... the breakdown where they do the lasso and turn 360 degrees
   while jumping and going OH, OH OH OH ... moon walk back and forth when he transforms as the song is
   playing and the shield rises ... When he comes to do his hammer jumps at us, he should be singing the
   song like AHHH WOOOO!"

   It is the 0927 HAMMER encounter with a different track: hammer_time_0927.js is variant-driven since
   0928 (ht27Variant), so the lock, the shield wall, the helpers, the pause/music handling and every
   cleanup path are the proven ones. Everything this file syncs to comes from HAMA_ART.audio, which
   _BUILD_SOURCE/build_hama_0928.py MEASURES off the file (tempo, beat phase, 8-bar sections, the
   "STOP!" dropouts) - nothing here is timed by ear.

   ART. Every pose is authored: the Hammer Time troupe sheet (ht27_boss / ht27_dancers: shuffles, the
   front/side/back/side 360 turn, the raised-palm STOP) and the Archmage's own hammer_throw_0926 plate,
   the only poses of this Hammer with EMPTY HANDS, which is what makes the robot toss possible without a
   second hammer appearing. HAMA_FRAMES below names every frame a beat uses; dedicated lasso / moonwalk /
   carry frames from Mike's art pass replace entries there, one line each (docs/HAMA_0928.md lists them).

   LYRICS. The captions are the song's short hooks (CAN'T TOUCH THIS, STOP, HAMMER TIME, BREAK IT DOWN,
   the OH-OH chant) and original parody lines. The verses are NOT transcribed. */
let hamaPending=false;
const HAMA_A=HAMA_ART.audio,HAMA_P=60/HAMA_A.bpm,HAMA_BAR=4*HAMA_P;
BOFA.music.hama=HAMA_A.path;
if(Snd){const m=new window.Audio();m.preload='none';m.src=HAMA_A.path;m.loop=true;Snd.music.hama=m;}

/* ---- the cue sheet, derived once from the measured track ---- */
const HAMA_CUES=(()=>{
  const secs=HAMA_A.sections,intro=secs.find(s=>s.kind==='intro');
  // the three big dropouts are the "STOP!"s; a smaller one within 12 s of the last is part of the same call
  const stops=[];for(const [t,len] of HAMA_A.stops){if(stops.length&&t-stops[stops.length-1].t<12)continue;
    stops.push({t,len,lock0:t-1.25*HAMA_P,lock1:t+3*HAMA_P});}
  const breakdowns=secs.filter(s=>s.kind==='breakdown').map(s=>{
    const cut=stops.find(q=>q.lock0>s.t0&&q.lock0<s.t1+HAMA_P);return {t0:s.t0,t1:cut?cut.lock0:s.t1};});
  return {introEnd:intro?intro.t1:14.7,stops,breakdowns,sections:secs};
})();
const HAMA_VARIANT={music:'hama',audio:HAMA_A,introEnd:HAMA_CUES.introEnd,
  wantLock(c){return HAMA_CUES.stops.some(s=>c>=s.lock0&&c<s.lock1);}};
function hamaOn(){return ht27Active&&ht27Variant===HAMA_VARIANT;}
function hamaStopAt(c){return HAMA_CUES.stops.find(s=>c>=s.lock0&&c<s.lock1)||null;}
function hamaBreakdownAt(c){return HAMA_CUES.breakdowns.find(w=>c>=w.t0&&c<w.t1)||null;}
function hamaSectionAt(c){return HAMA_CUES.sections.find(s=>c>=s.t0&&c<s.t1)||null;}
function hamaBeat(c){return (c-HAMA_A.phase)/HAMA_P;}

/* ---- which authored frame each beat wears. Sheet cells are named, never guessed. ----
   ht27_boss:    0-3 shuffle, 4-7 hammer-across shuffle, 8 front / 9 side / 10 back / 11 side (the turn),
                 12-15 the raised palm.  ht27_dancers: 0-3 finger-gun shuffle, 4 front / 5 side / 6 back /
                 7 side (the turn).  throw (arch_hammer_throw_0926): 0 empty hand reaching, 1 hammer in hand,
                 2 crouched strike, 3 wind-up, 4 overhead, 5 overhead follow-through, 6 empty hand out,
                 7 empty-handed stand. */
const HAMA_FRAMES={
  moonwalkBoss:{left:9,right:11},        // faces AWAY from the way it slides: that is the moonwalk
  moonwalkBot:{left:5,right:7},
  lassoBoss:[12,13,14,15],               // the raised arm circling over the head, on the beat
  lassoBot:[3,1,3,1],
  spinBoss:[8,9,10,11],                  // a full turn, one view per beat, in the air
  spinBot:[4,5,6,7],
  stopBoss:[12,13,14,15],
  slam:{windup:4,impact:2},
  toss:{windup:3,overhead:4,release:5,reach:0,hold:6,thrown:7,catch:1},
};
const HAMA_THROW=HAMA_ART.poses.throw;
/* the throw plate is drawn at the troupe sheet's body scale: its upright stand (frame 7) is 314 px of ink
   against the troupe's 252 px upright shuffle, which the troupe draws at 225/313.5 */
const HAMA_THROW_S=(252/HAMA_THROW.bodyInk)*(225/313.5);

/* ---- lyrics: short hooks + original parody lines ---- */
const HAMA_VERSE=['MY HAMMER IS CHROME','SPACE IS MY DANCE FLOOR','FEEL THE BASS IN YOUR HULL',
  'TOO SHINY FOR YOUR LASERS','CHROME PARACHUTE PANTS','ROBOTS - HIT IT','DANCE OR GET FLATTENED',
  'YO PILOT, SIT DOWN','BLUE STEEL, BIG DEAL','THE BEAT IS MY SHIELD'];
function hamaSing(d,who,text,dur,big){const H=d.hama;if(!H)return;
  H.lines=H.lines.filter(l=>l.who!==who);H.lines.push({who,text,t:0,dur:dur||HAMA_BAR*.9,big:!!big});}

/* ---- slams on HAMMER and on TIME ---- */
function hamaSlamPoint(b){return {x:b.x+30,y:b.y+100};}
function hamaSlam(b,d,word){
  const p=hamaSlamPoint(b);shake=Math.max(shake,13);explode(p.x,p.y,78,'blue');spawnShockRing(p.x,p.y,140,'comet');
  (Audio.SFX.hammerImpact||Audio.SFX.expBig||function(){})();
  d.hama.slamT=.22;hamaSing(d,'shout',word,HAMA_P*(word==='TIME!'?2.4:1.2),true);
}
function hamaStopTick(b,d,c){
  const s=hamaStopAt(c);if(!s)return;const H=d.hama,k=HAMA_CUES.stops.indexOf(s),flags=H.stopFlags[k]||(H.stopFlags[k]={});
  if(!flags.stop){flags.stop=true;hamaTossAbort(b,d);hamaThrownClear(d);H.lines=[];hamaSing(d,'shout','STOP!',s.t-c+.1,true);}
  const w=.22,t2=s.t+HAMA_P;
  H.pose=c<s.t-w?'stop':c<s.t?'windup':c<t2-w?'impact':c<t2?'windup':'impact';
  if(!flags.ham&&c>=s.t){flags.ham=true;hamaSlam(b,d,'HAMMER');}
  if(!flags.time&&c>=t2){flags.time=true;hamaSlam(b,d,'TIME!');hamaSing(d,'crew','HAMMER TIME!',HAMA_P*2);}
}

/* ---- the intro: ship, unfold, then the moonwalk while the shield rises ---- */
function hamaIntroTick(b,d,dt){
  const t=d.clock,home=VH*.34,H=d.hama,cx=(camLeftX()+camRightX())/2;b._noHit=true;d.shipFrame=null;
  if(t<2){const p=clamp(t/2,0,1),e=1-Math.pow(1-p,3);b.y=lerp(VH+50,home,e);b.x=cx;d.shipFrame=15;}
  else if(t<3.6){b.y=home;d.shipFrame=15-Math.min(9,Math.floor((t-2)/1.6*10));}
  else{
    // back and forth, one bar each way, gliding: position is a triangle wave of the bar clock
    const bars=hamaBeat(t)/4,ph=bars-Math.floor(bars/2)*2,tri=ph<1?ph:2-ph;
    const nx=cx+lerp(-70,70,tri);H.moonDir=nx<b.x?-1:1;b.x=nx;b.y=home+Math.sin(hamaBeat(t)*Math.PI)*2;
    H.pose='moonwalk';
    if(!H.introSummoned&&t>=6.4){H.introSummoned=true;ht27Summon(d,false);}
    if(!H.introWoo&&t>=4.2){H.introWoo=true;hamaSing(d,'boss','WOO! CHECK THE FEET',HAMA_BAR*1.6);}
  }
  d.shield=t>=7;
}
function hamaIntroEnd(b,d){
  d.shield=false;b._noHit=false;d.shipFrame=null;d.hama.pose=null;
  for(const p of [player,player2])if(p&&!p.dead)p.invuln=Math.max(p.invuln||0,60);
  Input.clearTaps();hamaSing(d,'boss','HIT IT!',HAMA_BAR);ht27DanceStart(b,d,1.2);
}

/* ---- the breakdown: shield up, the troupe lassos and jump-turns on the beat ---- */
function hamaBreakdownStart(b,d,bd){
  hamaTossAbort(b,d);hamaThrownClear(d);ht27ClearAttacks();
  d.mode='breakdown';d.t=0;d.shield=true;d.hama.bd=bd;d.hama.bdBeat=-1;d.from={x:b.x,y:b.y};
  hammerState(b,'hammer');b._noHit=false;b.enter=false;ht27Summon(d,true);
  hamaSing(d,'shout','BREAK IT DOWN!',HAMA_BAR,true);(Audio.SFX.shieldUp||Audio.SFX.select||function(){})();
}
function hamaBreakdownTick(b,d,dt){
  const H=d.hama,p=clamp(d.t/.8,0,1),e=p*p*(3-2*p),hx=(camLeftX()+camRightX())/2;
  b.x=lerp(d.from.x,hx,e);b.y=lerp(d.from.y,VH*.34,e);
  const beat=Math.floor(hamaBeat(d.clock)),inBar=((beat%4)+4)%4,bar=Math.floor(beat/4);
  H.pose=bar%2?'spin':'lasso';H.beatIn=inBar;
  if(beat!==H.bdBeat){H.bdBeat=beat;
    const chant=['OH!','OH-OH!','OH-OH-OH!','OH!'][inBar];
    hamaSing(d,inBar%2?'boss':'crew',chant,HAMA_P*.95);
    if(H.pose==='spin'&&inBar===0)(Audio.SFX.hammerWhoosh||Audio.SFX.blip||function(){})();
  }
}

/* ---- the robot toss ---- */
function hamaTossStart(b,d){
  const H=d.hama;
  // "he keeps bringing his helpers to come back to help him"
  const live=d.helpers.filter(q=>!q.dead&&q.spawn>=1);
  if(live.length<2){ht27Summon(d,false);hamaSing(d,'boss','ROBOTS! BACK TO THE FLOOR',HAMA_BAR);}
  d.mode='toss';d.t=0;hammerState(b,'hammer');b._noHit=false;
  H.toss={t:0,held:null,aim:null,thrown:false,hammer:null,wait:live.length<2?.7:0};
}
function hamaTossAbort(b,d){
  const H=d.hama,T=H&&H.toss;if(!T)return;
  if(T.held&&!T.thrown){T.held.x=b.x;T.held.y=b.y;d.helpers.push(T.held);}
  H.toss=null;H.flyHammer=null;
}
function hamaHandPoint(b){return {x:b.x-78,y:b.y+2};}
function hamaThrowSpeed(){return diffKey==='insanity'?420:hammerFurious()?380:hammerHard()?340:diffKey==='easy'?260:300;}
function hamaThrownHP(){return diffKey==='insanity'?64:hammerFurious()?56:hammerHard()?44:30;}
function hamaTossTick(b,d,dt){
  const H=d.hama,T=H.toss;if(!T){ht27DanceStart(b,d,1.3);return;}
  if(T.wait>0){T.wait-=dt;H.pose='dance';return;}
  T.t+=dt;const t=T.t;
  // 0-.40 the hammer goes up and back over his shoulder
  if(t<.2)H.pose='t:windup';else if(t<.4)H.pose='t:overhead';
  else if(!T.launched){T.launched=true;H.pose='t:release';const hp={x:b.x+20,y:b.y-70};
    H.flyHammer={t:0,dur:2.55,x0:hp.x,y0:hp.y,x1:b.x-40,y1:b.y+40};(Audio.SFX.hammerWhoosh||Audio.SFX.blip||function(){})();
    hamaSing(d,'boss','HOLD MY HAMMER',HAMA_BAR*.8);}
  if(t>=.5&&t<.95){H.pose='t:reach';
    if(!T.held){const live=d.helpers.filter(q=>!q.dead&&q.spawn>=1);
      if(!live.length){if(t>.9){hamaSing(d,'boss','...NOBODY?',HAMA_BAR);H.toss=null;}return;}
      const q=live.reduce((a,c)=>Math.abs(c.x-b.x)<Math.abs(a.x-b.x)?c:a);
      T.held=q;d.helpers=d.helpers.filter(r=>r!==q);q.aim=null;q.burst=null;}
    const hand=hamaHandPoint(b),k=clamp((t-.5)/.35,0,1);T.held.x=lerp(T.held.x,hand.x,k);T.held.y=lerp(T.held.y,hand.y,k);
  }else if(t>=.95&&t<1.75&&T.held){H.pose='t:hold';
    const hand=hamaHandPoint(b);T.held.x=hand.x+Math.sin(t*38)*2;T.held.y=hand.y;
    if(!T.aim){T.aim={x:player.x,y:player.y,t:0,dur:.8};hamaSing(d,'robot','CANT TOUCH THIIIS',1.4);H.singer=T.held;}
    const A=T.aim;A.t+=dt;if(A.t<A.dur*.6){A.x=player.x;A.y=player.y;}
    combatWarningTick(b,'hama-toss',A.t,A.dur);
  }else if(t>=1.75&&!T.thrown&&T.held){T.thrown=true;H.pose='t:thrown';
    const q=T.held,A=T.aim||{x:player.x,y:player.y},a=Math.atan2(A.y-q.y,A.x-q.x),v=hamaThrowSpeed();
    const r={_hamaThrown:true,x:q.x,y:q.y,vx:Math.cos(a)*v,vy:Math.sin(a)*v,rot:0,spin:(A.x<q.x?-1:1)*9,
      hp:hamaThrownHP(),maxhp:hamaThrownHP(),w:40,h:46,t:0,flash:0,dead:false,slot:q.slot,spawn:1};
    H.thrown.push(r);H.singer=r;hamaSing(d,'robot','CANT TOUCH THIIIIIS!',2.2);
    (Audio.SFX.hammerThrow||Audio.SFX.hammerWhoosh||Audio.SFX.select||function(){})();
  }else if(t>=1.75)H.pose='t:thrown';
  if(H.flyHammer&&H.flyHammer.t>=H.flyHammer.dur){H.flyHammer=null;H.pose='t:catch';H.caught=.3;
    (Audio.SFX.hammerCatch||Audio.SFX.select||function(){})();hamaSing(d,'crew','WOO!',HAMA_P*2);}
  if(t>=1.75&&!H.flyHammer&&(H.caught||0)<=0){H.toss=null;ht27DanceStart(b,d,hammerFurious()?1.1:1.5);}
}
function hamaHammerTick(d,dt){const H=d.hama;if(H.flyHammer)H.flyHammer.t+=dt;if(H.caught>0)H.caught-=dt;if(H.slamT>0)H.slamT-=dt;}
function hamaThrownHit(r,dmg){
  if(!r||r.dead)return;r.hp-=dmg;r.flash=.12;weaponHitSfx('normal');
  if(r.hp<=0){r.dead=true;explode(r.x,r.y,52,'blue');spawnShockRing(r.x,r.y,44,'comet');Audio.SFX.expSmall();
    floatText(r.x,r.y-30,'OH NO!','#ffe98a');}
}
function hamaThrownClear(d){const H=d.hama;if(!H)return;for(const r of H.thrown)if(!r.dead){r.dead=true;explode(r.x,r.y,40,'blue');}H.thrown=[];}
function hamaThrownTick(b,d,dt){
  const H=d.hama;
  for(const r of H.thrown){if(r.dead)continue;r.t+=dt;r.x+=r.vx*dt;r.y+=r.vy*dt;r.rot+=r.spin*dt;r.flash=Math.max(0,r.flash-dt);
    for(const p of pBullets){if(p.dead||p._launchDelay>0)continue;const beam=/^(beam|firewhip|flame)$/.test(p.kind||'');
      if(beam?Math.abs(p.x-r.x)<r.w*.5+(p.w||10)*.5&&r.y>(p.top||0)&&r.y<(p.bot||player.y):Math.abs(p.x-r.x)<r.w*.5+(p.w||4)*.5&&Math.abs(p.y-r.y)<r.h*.5+(p.h||8)*.5){
        hamaThrownHit(r,(p.dmg||1)*(beam?dt*8:1));if(!beam&&!p.pierce)p.dead=true;if(r.dead)break;}}
    if(r.dead)continue;
    for(const pl of [player,player2])if(pl&&!pl.dead&&Math.abs(pl.x-r.x)<26&&Math.abs(pl.y-r.y)<30){
      r.dead=true;explode(r.x,r.y,60,'blue');spawnShockRing(r.x,r.y,60,'comet');
      if(pl===player)playerHit('hama-robot');else if(typeof withSeat==='function')withSeat(2,()=>playerHit('hama-robot'));break;}
    if(r.y>VH+70||r.y<-90||r.x<camLeftX()-90||r.x>camRightX()+90)r.dead=true;
  }
  H.thrown=H.thrown.filter(r=>!r.dead);
}

/* ---- singing, on the bar ---- */
function hamaLyricsTick(b,d,c,dt){
  const H=d.hama;for(const l of H.lines)l.t+=dt;H.lines=H.lines.filter(l=>l.t<l.dur);
  if(d.mode==='break'||d.mode==='breakdown')return;
  const beat=Math.floor(hamaBeat(c)),bar=Math.floor(beat/4);if(bar===H.lastBar)return;H.lastBar=bar;
  const s=hamaSectionAt(c);if(!s)return;const k=bar-s.bar0;
  if(s.kind==='intro'){if(d.mode==='intro'&&c>=6.4&&k%2)hamaSing(d,'crew',k%4===1?'OH-OH!':'YEAH!',HAMA_BAR*.8);}
  else if(s.kind==='chorus'){hamaSing(d,k%2?'boss':'crew','CANT TOUCH THIS',HAMA_BAR*.85);}
  else if(s.kind==='verse'){
    if(k%2===0&&d.mode!=='toss'){hamaSing(d,'boss',HAMA_VERSE[H.verse++%HAMA_VERSE.length],HAMA_BAR*1.8);}
    else if(k%2===1)hamaSing(d,'crew',['HEY!','UH!','WOO!','HO!'][(H.verse+k)%4],HAMA_P*1.5);}
}

/* ---- tick ---- */
const HAMA_BASE={tick:ht27Tick,draw:ht27Draw,attack:ht27Attack,start:ht27Start,warm:ht27Warm,wall:ht27WallBounds,
  targets:ht27HelperTargets,submit:submitPassword,state:setState,hit:hitEnemy};
ht27Tick=function(b,dt){
  const d=b&&b._hammerTime;if(!hamaOn()||!d||b.dead||!d.hama)return HAMA_BASE.tick(b,dt);
  const c=d.clock;hamaLyricsTick(b,d,c,dt);hamaThrownTick(b,d,dt);hamaHammerTick(d,dt);
  if(d.mode==='intro'){
    if(c>=HAMA_CUES.introEnd)hamaIntroEnd(b,d);
    else{d.t+=dt;ht27Helpers(b,d,dt);hamaIntroTick(b,d,dt);return;}
  }
  if(d.mode==='break'){hamaStopTick(b,d,c);return HAMA_BASE.tick(b,dt);}
  d.hama.pose=null;
  const bd=hamaBreakdownAt(c);
  if(bd&&!['breakdown','break','intro'].includes(d.mode)&&!ht27CombatSequence(b))hamaBreakdownStart(b,d,bd);
  if(d.mode==='breakdown'){
    if(!bd){d.shield=false;ht27DanceStart(b,d,1.4);}
    else{d.t+=dt;ht27Helpers(b,d,dt);hamaBreakdownTick(b,d,dt);return;}
  }
  if(d.mode==='toss'){d.t+=dt;ht27Helpers(b,d,dt);b.flash=Math.max(0,(b.flash||0)-dt);hamaTossTick(b,d,dt);return;}
  const prev=b._hammer.state,r=HAMA_BASE.tick(b,dt),now=b._hammer.state;
  if(now!==prev){if(now==='leap')hamaSing(d,'boss','AHHH-WOOO!',HAMA_P*3);else if(prev==='leap')hamaSing(d,'crew','HEY!',HAMA_P*2);}
  return r;
};
ht27Attack=function(b,d){
  if(!hamaOn()||!d.hama)return HAMA_BASE.attack(b,d);
  // every other attack is the robot toss; the rest is the proven HAMMER rotation (jumps, throw, whirl, ball)
  if((d.hama.attacks++)%2===0)return hamaTossStart(b,d);
  return HAMA_BASE.attack(b,d);
};
ht27HelperTargets=function(){const d=ht27Data(),base=HAMA_BASE.targets();
  if(!hamaOn()||!d||!d.hama)return base;
  const bd=d.mode==='breakdown';return (bd?[]:base).concat(d.hama.thrown.filter(r=>!r.dead));};
hitEnemy=function(e,dmg){if(e&&e._hamaThrown)return hamaThrownHit(e,dmg);
  if(e&&e._ht27Helper&&hamaOn()){const d=ht27Data();if(d&&d.mode==='breakdown')return;}
  return HAMA_BASE.hit.apply(this,arguments);};
ht27WallBounds=function(d){const w=HAMA_BASE.wall(d);if(!hamaOn()||!d||d.mode!=='breakdown')return w;
  const rise=clamp(d.t/.9,0,1);return Object.assign(w,{y:VH*.64-VH*.48*rise,rise});};
ht27Warm=function(){HAMA_BASE.warm();if(ht27Variant===HAMA_VARIANT){XART.rdy(HAMA_THROW.key);XART.rdy('arch_hammer_spin');}};
ht27Start=function(){
  const hama=hamaPending;hamaPending=false;if(hama)ht27Variant=HAMA_VARIANT;
  HAMA_BASE.start.apply(this,arguments);
  if(hama&&boss&&boss._hammerTime){boss.name='HAMA';
    boss._hammerTime.hama={lines:[],thrown:[],stopFlags:{},toss:null,flyHammer:null,pose:null,verse:0,attacks:0,lastBar:null,moonDir:1};}
};

/* ---- draw ---- */
function hamaThrowSprite(frame,x,footY,flash){
  if(!XART.rdy(HAMA_THROW.key))return false;const r=HAMA_THROW.frames[frame],s=HAMA_THROW_S;
  const im=flash?xartTint(HAMA_THROW.key,'#ffffff',.78):XART.get(HAMA_THROW.key);
  ctx.save();ctx.imageSmoothingEnabled=false;
  ctx.drawImage(im,r[0],r[1],r[2],r[3],x-r[4]*s,footY-r[5]*s,r[2]*s,r[3]*s);ctx.restore();return true;
}
/* ⚠ the dialogue face is drawn at its own sizes only: scaled mid-"pop" it threw stray bar/bracket glyphs at
   both ends of a line (seen in the probe frames, never in a number), so a sung line pops by ALPHA, not size.
   A shout is fitted to the camera with stageFitH - BREAK IT DOWN! ran off both edges at the nominal size. */
function hamaTextDraw(text,x,y,h,col,big){
  if(big&&typeof stageText==='function'&&typeof curFontArt==='function'){const art=curFontArt();
    if(art&&art.font){const vw=camRightX()-camLeftX()-24,fh=stageFitH(art,text,vw,h,8),w=stageWidth(art,text,fh);
      stageText(art,text,clamp(x,camLeftX()+12+w/2,camRightX()-12-w/2),y,fh,col,1,1,null,true);return;}}
  const w=typeof msgMeasure==='function'?msgMeasure(text,h):text.length*h*.66,cx=clamp(x,camLeftX()+8+w/2,camRightX()-8-w/2);
  // msgText draws on every path but returns a width on only one of them - never draw a second copy after it
  if(typeof msgText==='function'){msgText(text,cx,y,h,col,1,1);return;}
  ctx.save();ctx.font='bold '+h+'px BOFmil,monospace';ctx.textAlign='center';ctx.lineWidth=4;ctx.strokeStyle='#07131f';ctx.fillStyle=col;
  ctx.strokeText(text,cx,y+h*.35);ctx.fillText(text,cx,y+h*.35);ctx.restore();
}
function hamaLinesDraw(b,d){
  const H=d.hama;
  for(const l of H.lines){
    const fade=Math.min(clamp(l.t/.08,0,1),clamp((l.dur-l.t)/.25,0,1)),bob=Math.round(Math.sin(l.t*14)*1.5),kick=l.t<.1?-3:0;
    ctx.save();ctx.globalAlpha=fade;
    if(l.who==='shout')hamaTextDraw(l.text,(camLeftX()+camRightX())/2,VH*.18+bob,26,l.text==='STOP!'?'#ff4a4a':'#ffffff',true);
    else if(l.who==='boss')hamaTextDraw(l.text,b.x,b.y-128+bob+kick,13,'#bff4ff',false);
    else if(l.who==='robot'){const r=H.singer;if(r&&!r.dead)hamaTextDraw(l.text,r.x,r.y-52+bob+kick,11,'#ffe98a',false);}
    else for(const q of d.helpers)if(!q.dead&&q.spawn>=1)hamaTextDraw(l.text,q.x,q.y-50+bob+kick,10,'#ffe98a',false);
    ctx.restore();
  }
}
function hamaBotFrame(d,q,beatF){
  const H=d.hama,step=Math.floor(beatF*2);
  if(d.mode==='intro')return HAMA_FRAMES.moonwalkBot[H.moonDir<0?'left':'right'];
  if(d.mode==='breakdown')return H.pose==='spin'?HAMA_FRAMES.spinBot[H.beatIn]:HAMA_FRAMES.lassoBot[(H.beatIn+q.slot)%4];
  return (step+q.slot)%4;
}
function hamaHop(d){const H=d.hama;if(d.mode!=='breakdown'||H.pose!=='spin')return 0;const f=hamaBeat(d.clock)%1;return -Math.sin(clamp(f,0,1)*Math.PI)*28;}
ht27Draw=function(b){
  const d=b&&b._hammerTime;if(!hamaOn()||!d||b.dead||!d.hama)return HAMA_BASE.draw(b);
  const H=d.hama,beatF=hamaBeat(d.clock),step=Math.floor(beatF*2),hop=hamaHop(d);
  for(const q of d.helpers){if(q.spawn<=0)continue;
    ht27Sprite('dancers',hamaBotFrame(d,q,beatF),q.x,q.y+32+hop,116*q.spawn,1,q.flash>0);
    if(q.aim)combatWarningDraw(q,{x:q.x,y:q.y+20,ex:q.aim.x,ey:q.aim.y,progress:clamp(q.aim.t/q.aim.dur,0,1),width:18,alertX:q.x,alertY:q.y-40});}
  const foot=b.y+94,throwFoot=b.y+105,flash=b.flash>0;
  if(d.mode==='attack')HAMA_BASE.draw(b);
  else if(d.mode==='intro'&&d.shipFrame!=null){if(d.musicStarted)archBlit('ship_transform',d.shipFrame,b.x,b.y,d.shipFrame===15?192:206);}
  else if(d.mode==='intro')ht27Sprite('boss',HAMA_FRAMES.moonwalkBoss[H.moonDir<0?'left':'right'],b.x,foot,225,1,flash);
  else if(d.mode==='breakdown'){const f=H.pose==='spin'?HAMA_FRAMES.spinBoss[H.beatIn]:HAMA_FRAMES.lassoBoss[H.beatIn];ht27Sprite('boss',f,b.x,foot+hop,225,1,flash);}
  else if(d.mode==='break'){
    if(H.pose==='windup')hamaThrowSprite(HAMA_FRAMES.slam.windup,b.x,throwFoot,flash);
    else if(H.pose==='impact')hamaThrowSprite(HAMA_FRAMES.slam.impact,b.x,throwFoot+(H.slamT>0?4:0),flash);
    else ht27Sprite('boss',HAMA_FRAMES.stopBoss[Math.min(3,Math.floor(d.energy*3.9))],b.x,foot,225,1,flash);
  }
  else if(d.mode==='toss'&&H.pose&&H.pose.startsWith('t:'))hamaThrowSprite(HAMA_FRAMES.toss[H.pose.slice(2)],b.x,throwFoot,flash);
  else{const f=(Math.floor(beatF/4)%2?4:0)+step%4;ht27Sprite('boss',f,b.x,foot,225,flash?.58:1);}
  // the carried robot, the hammer in the air, the thrown robots
  const T=H.toss;if(T&&T.held&&!T.thrown)ht27Sprite('dancers',1,T.held.x,T.held.y+32,104,1,false);
  if(T&&T.aim&&!T.thrown)combatWarningDraw(b,{x:T.held?T.held.x:b.x,y:T.held?T.held.y:b.y,ex:T.aim.x,ey:T.aim.y,progress:clamp(T.aim.t/T.aim.dur,0,1),width:44,alertX:b.x,alertY:b.y-150});
  const F=H.flyHammer;if(F){const p=clamp(F.t/F.dur,0,1);
    archBlit('hammer_spin',Math.floor(F.t*14)%8,lerp(F.x0,F.x1,p),lerp(F.y0,F.y1,p)-Math.sin(p*Math.PI)*190,92,null,0,1);}
  for(const r of H.thrown){if(r.dead)continue;ctx.save();ctx.translate(r.x,r.y);ctx.rotate(r.rot);
    ht27Sprite('dancers',(Math.floor(r.t*8))%4,0,32,104,1,r.flash>0);ctx.restore();}
  if(d.shield&&d.mode!=='break'){const sd=HAMMER_TIME_ART.sheets.wall,fr=sd.frames[Math.floor(d.clock*16)%8],wall=ht27WallBounds(d);
    if(XART.rdy('ht27_wall')){ctx.save();ctx.globalAlpha=wall.alpha;ctx.imageSmoothingEnabled=false;
      ctx.beginPath();ctx.rect(wall.x,VH*.16,wall.w,wall.h);ctx.clip();
      ctx.drawImage(XART.get('ht27_wall'),fr[0],fr[1],fr[2],fr[3],wall.x,wall.y,wall.w,wall.h);ctx.restore();}
    for(const r of d.reflections)hammerLaserDraw(r);}
  hamaLinesDraw(b,d);
};

/* ---- the password ---- */
submitPassword=function(){
  if(String(pwInput).trim().toUpperCase()==='HAMA'){
    hamaPending=true;ht27Variant=HAMA_VARIANT;ht27Pending=true;ht27Warm();pwInput='';PENDING_STAGE=5;_coleScene=0;run.mode='arcade';
    passwordDifficulty=true;menuIndex=Math.max(0,diffList().indexOf(diffKey||'normal'));Audio.SFX.select();setState(GS.DIFF);return;
  }
  hamaPending=false;return HAMA_BASE.submit.apply(this,arguments);
};
/* backing out of the route drops it; a state change INSIDE startRun must not (it runs before ht27Start) */
setState=function(s){const r=HAMA_BASE.state.apply(this,arguments);
  if(hamaPending&&!ht27Active&&[GS.TITLE,GS.PASSWORD,GS.MODESEL,GS.CAMPHUB].includes(s)){hamaPending=false;if(ht27Variant===HAMA_VARIANT)ht27Variant=null;}return r;};
