"use strict";
/* HAMMER: an isolated password encounter. Ordinary campaign Hammer is unchanged. */
let ht27Pending=false,ht27Active=false;
const HT27_BASE={submit:submitPassword,start:startRun,state:setState,tick:updatePlay,
 hammerTick:hammerBossTick,draw:hammerBossDraw,damage:hammerBossDamage,hit:bossHitTest,music:Audio.startMusic,
 hard:hammerHard,furious:hammerFurious,locks:_lockTargets,spaceTargets:spaceTargets,enemyHit:hitEnemy};
hammerHard=function(){return ht27Active?['hard','furious','insanity'].includes(diffKey):HT27_BASE.hard();};
hammerFurious=function(){return ht27Active?['furious','insanity'].includes(diffKey):HT27_BASE.furious();};
for(const [key,d]of Object.entries(HAMMER_TIME_ART.sheets))XART._src['ht27_'+key]=d.path;
BOFA.music.hammerTime=HAMMER_TIME_ART.audio.path;
if(Snd){const m=new window.Audio();m.preload='none';m.src=HAMMER_TIME_ART.audio.path;m.loop=true;Snd.music.hammerTime=m;}
/* 0928 (HAMA): the encounter is track-agnostic. A variant supplies its own song, cue windows and intro
   length; null is the original HAMMER code with Mike's remix and its 0:16-0:24 dance break. */
let ht27Variant=null;
function ht27A(){return ht27Variant?ht27Variant.audio:HAMMER_TIME_ART.audio;}
function ht27SongName(){return ht27Variant?ht27Variant.music:'hammerTime';}
function ht27Song(){return Snd&&Snd.music[ht27SongName()];}
function ht27IntroEnd(){return ht27Variant?ht27Variant.introEnd:HAMMER_TIME_ART.audio.breakStart;}
function ht27WantLock(c){return ht27Variant?ht27Variant.wantLock(c):c>=HAMMER_TIME_ART.audio.breakStart&&c<HAMMER_TIME_ART.audio.breakEnd;}
function ht27Warm(){for(const k of Object.keys(HAMMER_TIME_ART.sheets))XART.rdy('ht27_'+k);XART.rdy('arch_ship_transform');XART.rdy('arch_orbital_sweep_0926');for(let i=0;i<8;i++)XART.rdy('nsr_comet_'+i);furyShipWarm();const m=ht27Song();if(m&&m.preload==='none'){m.preload='auto';m.load();}}
function ht27Begin(d){
 if(d.musicStarted)return true;
 const m=ht27Song();
 if(!m||m.readyState<2||!XART.rdy('arch_ship_transform')||!XART.rdy('arch_orbital_sweep_0926')||!furyShipReady()||!Object.keys(HAMMER_TIME_ART.sheets).every(k=>XART.rdy('ht27_'+k)))return false;
 // The first visible ship frame and the soundtrack share this start gate.
 d.musicStarted=true;d.clock=0;HT27_BASE.music(ht27SongName());return true;
}
function ht27Data(){return ht27Active&&boss&&!boss.dead?boss._hammerTime:null;}
function ht27CombatSequence(b){const h=b&&b._hammer;return !!(h&&(['fr_activation','fr_stun','fr_twirl'].includes(h.state)||h.frRecovery));}
function ht27Locked(){const d=ht27Data();if(!d)return false;const m=ht27Song(),t=m&&m.readyState>=2&&!m.paused?m.currentTime:d.clock;return d.mode==='intro'||d.locked||(!ht27CombatSequence(boss)&&ht27WantLock(t));}
function ht27ClearAttacks(){
 pBullets=[];eBullets=[];enemies=[];playerLocks=[];rollers=[];zaps=[];wm26Releases=[];
 l5Rocks=[];
 if(typeof groundTargetingReset==='function')groundTargetingReset();
 const h=boss&&boss._hammer;if(h){h.throw=null;h.bombs=[];h.pillars=[];h.ballWarn=false;h.recovery=null;h.coreBurst=null;h.chainMuzzle=0;h.leapFx=0;}
 if(Snd)Snd.loopStopAll();
}
function ht27Clock(d,dt){
 const m=ht27Song();
 // Use the playing soundtrack, not accumulated combat time. Muting keeps its clock alive.
 if(m&&m.readyState>=2&&!m.paused&&Number.isFinite(m.currentTime))d.clock=m.currentTime;
 else if(d.mode!=='intro')d.clock=(d.clock+dt)%ht27A().seconds;
 const a=ht27A();
 d.energy=a.envelope[Math.min(a.envelope.length-1,Math.floor(d.clock*a.envelopeFPS))]||0;
 return d.clock;
}
function ht27DanceEffects(dt){
 // Advance visual tails without updateEffects(), which also advances damaging bombs.
 for(const ex of explosions){ex.t+=dt;ex.r=lerp(0,ex.max,Math.min(1,ex.t/(ex.dur*.4)));}
 explosions=explosions.filter(ex=>!ex.dead&&ex.t<ex.dur);
 for(const p of particles){p.t+=dt;p.x+=(p.vx||0)*dt*60;p.y+=(p.vy||0)*dt*60;}
 particles=particles.filter(p=>!p.dead&&p.t<p.life);
 for(const p of pImpacts)p.t+=dt;pImpacts=pImpacts.filter(p=>p.t<p.dur);
 for(const s of sprAnims)s.t+=dt;sprAnims=sprAnims.filter(s=>s.t<s.dur);
 for(const s of smokeTrails)s.t+=dt;smokeTrails=smokeTrails.filter(s=>s.t<s.life);
 for(const s of efxBursts)s.t+=dt;efxBursts=efxBursts.filter(s=>s.t<EFX_BURST_T);
 for(const f of floaters)f.t+=dt;floaters=floaters.filter(f=>f.t<f.life);
 for(const f of fadeOuts)f.t+=dt;fadeOuts=fadeOuts.filter(f=>f.t<f.dur);
 updateShockRings(dt);
 shake=Math.max(0,shake-dt*24);flashScreen=Math.max(0,flashScreen-dt*3);
}
function ht27DanceStart(b,d,duration){d.mode='dance';d.t=0;d.duration=duration||1.8;hammerState(b,'hammer');b._noHit=false;b.enter=false;b._hammer.phasePending=false;}
function ht27LockStart(b,d){
  // Finish armor/restoration counterplay before a music cue resets combat state.
  if(ht27CombatSequence(b))return;
 d.mode='break';d.t=0;d.locked=true;d.shield=true;d.savedSpecial=special;special=null;
 d.savedSpeed=timeScale;timeScale=1;{const m=ht27Song();if(m){m.playbackRate=1;m.preservesPitch=true;}}
 d.reflections=pBullets.filter(q=>!q.dead).slice(0,16).map((q,i)=>({x:q.x,y:Math.min(q.y,b.y+100),vx:(i%2?1:-1)*(130+i*3),vy:75,t:0,w:8,h:20,kind:'eglaser',_hammerLaser:true}));
 ht27ClearAttacks();hammerState(b,'hammer');b._noHit=false;b.enter=false;
 for(const p of [player,player2])if(p){p.roll=null;p.somer=null;p._thrustPower=0;}
 d.homeX=(camLeftX()+camRightX())/2;d.homeY=VH*.34;d.from={x:b.x,y:b.y};
 ht27Summon(d,true);(Audio.SFX.shieldUp||Audio.SFX.bossWeaponCharge||Audio.SFX.select)();
}
function ht27LockEnd(b,d){
 d.locked=false;d.shield=false;d.reflections=[];special=d.savedSpecial||null;d.savedSpecial=null;timeScale=d.savedSpeed||1;
 for(const p of [player,player2])if(p&&!p.dead)p.invuln=Math.max(p.invuln||0,48);
 Input.clearTaps();ht27DanceStart(b,d,2.1);(Audio.SFX.shieldBreak||Audio.SFX.select)();
}
function ht27Summon(d,full){
 const count=4;
 const spots=[-130,130,-70,70];
 for(let i=0;i<count;i++)if(!d.helpers.some(q=>q.slot===i&&!q.dead)){
  const hp=diffKey==='insanity'?76:hammerFurious()?64:44;
  const q={_ht27Helper:true,slot:i,x:(camLeftX()+camRightX())/2+spots[i],y:VH*.34+(i>1?64:12),hp,maxhp:hp,w:42,h:54,dead:false,flash:0,spawn:0,age:0,arrival:full?0:i*.16,shotCd:1.8+i*.55};
  d.helpers.push(q);
 }
}
function ht27HelperHit(q,dmg){
 const d=ht27Data();if(!d||ht27Locked()||!hammerHard()||q.dead||q.spawn<1)return;
 q.hp-=dmg;q.flash=.12;weaponHitSfx('normal');
 if(q.hp<=0){q.dead=true;q.aim=null;q.burst=null;explode(q.x,q.y,45,'blue');spawnShockRing(q.x,q.y,36,'comet');Audio.SFX.expSmall();}
}
function ht27HelperFire(q,angle,count){
 const speed=diffKey==='insanity'?4.6:hammerFurious()?4.1:3.3;
 for(let i=0;i<count;i++){hammerLaser(q.x,q.y+20,angle+(i-(count-1)/2)*.16,speed,i>0);eBullets[eBullets.length-1]._ht27Helper=true;}
 wm26Emit(q,q.x,q.y+20,angle,'laser',null);q.muzzle=.13;q.angle=angle;
}
function ht27HelperTargets(){const d=ht27Data();return d&&!ht27Locked()&&hammerHard()?d.helpers.filter(q=>!q.dead&&q.spawn>=1):[];}
_lockTargets=function(){return HT27_BASE.locks().concat(ht27HelperTargets());};
spaceTargets=function(){return ht27HelperTargets().concat(HT27_BASE.spaceTargets());};
hitEnemy=function(e,dmg){if(e&&e._ht27Helper)return ht27HelperHit(e,dmg);return HT27_BASE.enemyHit.apply(this,arguments);};
function ht27Helpers(b,d,dt){
 d.helperGap=Math.max(0,(d.helperGap||0)-dt);
 for(const q of d.helpers){if(q.dead)continue;q.age+=dt;if(q.age<q.arrival)continue;
  if(!q.arrived){q.arrived=true;explode(q.x,q.y+16,34,'blue');spawnShockRing(q.x,q.y+24,38,'comet');Audio.SFX.expSmall();}
  q.spawn=Math.min(1,q.spawn+dt*1.7);q.flash=Math.max(0,q.flash-dt);q.shotCd-=dt;q.muzzle=Math.max(0,(q.muzzle||0)-dt);
  const slots=[-130,130,-70,70],tx=(camLeftX()+camRightX())/2+slots[q.slot],ty=VH*.34+(q.slot>1?64:12);
  q.x+=clamp(tx-q.x,-120*dt,120*dt);q.y+=clamp(ty-q.y,-100*dt,100*dt);
  if(!ht27Locked()&&hammerHard()&&q.spawn>=1){
   for(const p of pBullets){if(p.dead||p._launchDelay>0||/^space/.test(p.kind||''))continue;const beam=/^(beam|firewhip|flame)$/.test(p.kind||'');
    if(beam?Math.abs(p.x-q.x)<q.w*.5+(p.w||10)*.5&&q.y>(p.top||0)&&q.y<(p.bot||player.y):Math.abs(p.x-q.x)<q.w*.5+(p.w||4)*.5&&Math.abs(p.y-q.y)<q.h*.5+(p.h||8)*.5){
     ht27HelperHit(q,(p.dmg||1)*(beam?dt*8:1));if(!beam&&!p.pierce)p.dead=true;
     if(q.dead)break;
    }
   }
   if(q.dead)continue;
   // One warned helper attack at a time, during the boss's quieter beats.
   const quiet=d.mode==='dance'||['recover','back','hammer_stun'].includes(b._hammer.state);
   if(quiet&&q.shotCd<=0&&d.helperGap<=0&&!d.helpers.some(r=>r.aim||r.burst)){
    q.aim={x:player.x,y:player.y,t:0,dur:diffKey==='insanity'?.62:hammerFurious()?.72:.95};
    q.shotCd=hammerFurious()?3.3:4.4;d.helperGap=hammerFurious()?.7:1.1;
   }
   if(q.aim){const a=q.aim;a.t+=dt;combatWarningTick(q,'hammer-backup-'+q.slot,a.t,a.dur);if(a.t>=a.dur){
    const angle=Math.atan2(a.y-q.y-20,a.x-q.x);q.aim=null;
    if(q.slot%2)ht27HelperFire(q,angle,diffKey==='insanity'?5:3);
    else{ht27HelperFire(q,angle,1);q.burst={angle,left:2,cd:.16};}
    d.helperGap=hammerFurious()?.7:1.1;
   }}
   if(q.burst){q.burst.cd-=dt;if(q.burst.cd<=0){ht27HelperFire(q,q.burst.angle,1);q.burst.cd=.16;if(--q.burst.left<=0)q.burst=null;}}
  }else{q.aim=null;q.burst=null;}
 }
 d.helpers=d.helpers.filter(q=>!q.dead);
}
function ht27IntroTick(b,d){
 const t=d.clock,home=VH*.34;b._noHit=true;d.shipFrame=null;
 if(t<2){const p=clamp(t/2,0,1),e=1-Math.pow(1-p,3);b.y=lerp(VH+50,home,e);d.shipFrame=15;}
 else if(t<3.6){b.y=home;d.shipFrame=15-Math.min(9,Math.floor((t-2)/1.6*10));}
 else if(t<4.2)d.introFrame=0;
 else if(t<5.35)d.introFrame=Math.min(3,Math.floor((t-4.2)/1.15*4));
 else if(t<5.75)d.introFrame=3;
 else if(t<6.15)d.introFrame=Math.min(7,4+Math.floor((t-5.75)/.4*4));
 else{
  if(!d.slammed){d.slammed=true;d.slamAt=t;shake=Math.max(shake,14);explode(b.x,b.y+88,90,'blue');spawnShockRing(b.x,b.y+88,150,'comet');(Audio.SFX.hammerImpact||Audio.SFX.expBig)();}
  d.introFrame=t<7.05?Math.min(11,7+Math.floor((t-6.15)/.9*5)):0;
  if(t>=6.4&&!d.summoned){d.summoned=true;ht27Summon(d,false);}
 }
 d.shield=t>=7;
 // No combat interval between the entrance and the 0:16 dance cue.
}
function ht27Attack(b,d){
 d.mode='attack';d.t=0;const h=b._hammer;h.phasePending=false;h.comboPending=false;h.mode='hammer';h.followCount=hammerFurious()?5:hammerHard()?3:1;
 const which=d.attack++%4;
 if(which===1)hammerBoomerangStart(b);
 else if(which===2)hammerWhirlStart(b);
 else if(which===3&&b.hp<b.maxhp*.65){hammerBallArm(b);hammerState(b,'curl');}
 else{hammerTarget(b);hammerState(b,'warn');}
}
function ht27Tick(b,dt){
 const d=b._hammerTime;if(!d||b.dead)return;
 d.t+=dt;ht27Helpers(b,d,dt);b.flash=Math.max(0,(b.flash||0)-dt);
 if(d.mode==='intro'){
  ht27IntroTick(b,d);return;
 }
 if(d.mode==='break'){
  const p=clamp(d.t/.7,0,1),e=p*p*(3-2*p);b.x=lerp(d.from.x,d.homeX,e);b.y=lerp(d.from.y,d.homeY,e);
  for(const r of d.reflections){r.x+=r.vx*dt;r.y+=r.vy*dt;r.t+=dt;}d.reflections=d.reflections.filter(r=>r.t<.8);
  return;
 }
 if(d.mode==='dance'){
  const hx=(camLeftX()+camRightX())/2,hy=VH*.34;
  b.x+=clamp(hx+Math.sin(d.clock*ht27A().bpm/60*Math.PI)*22-b.x,-135*dt,135*dt);
  b.y+=clamp(hy-b.y,-160*dt,160*dt);
  if(d.t>=d.duration)ht27Attack(b,d);return;
 }
 if(['hammer','shield','leap_reset','storm_idle'].includes(b._hammer.state)){ht27DanceStart(b,d,hammerFurious()?1.35:1.9);return;}
 if(b._hammer.state==='hammer_stun'&&b._hammer.t+dt>=5){const h=b._hammer;h.knockedHammer=null;h.hammerDestroyed=false;h.hammerHP=h.hammerMax;ht27DanceStart(b,d,1.9);return;}
 HT27_BASE.hammerTick(b,dt);
}
function ht27Sprite(key,frame,x,footY,height,alpha,flash){
 if(!XART.rdy('ht27_'+key))return false;
 const d=HAMMER_TIME_ART.sheets[key],r=d.frames[((frame|0)%d.frames.length+d.frames.length)%d.frames.length],s=height/d.cellHeight;
 ctx.save();ctx.imageSmoothingEnabled=false;ctx.globalAlpha=alpha==null?1:alpha;
 ctx.drawImage(flash?xartTint('ht27_'+key,'#ffffff',.78):XART.get('ht27_'+key),r[0],r[1],r[2],r[3],x-r[4]*s,footY-r[5]*s,r[2]*s,r[3]*s);ctx.restore();return true;
}
function ht27WallBounds(d){const rise=d&&d.mode==='intro'?clamp((d.clock-7)/(ht27IntroEnd()-7),0,1):1;return{x:-8,y:VH*.64-VH*.48*rise,w:worldWidth()+16,h:VH*.48,alpha:.5,rise};}
function ht27Draw(b){
 const d=b._hammerTime;if(!d||b.dead)return HT27_BASE.draw(b);
 const beat=d.clock*ht27A().bpm/60,step=Math.floor(beat*2),twirl=d.mode==='break'&&Math.floor(d.t/2)%2===1;
 for(const q of d.helpers){
  if(q.spawn<=0)continue;
  ht27Sprite('dancers',d.mode==='intro'?0:(twirl?4:0)+(step+q.slot)%4,q.x,q.y+32,116*q.spawn,1,q.flash>0);
  if(q.aim)combatWarningDraw(q,{x:q.x,y:q.y+20,ex:q.aim.x,ey:q.aim.y,progress:clamp(q.aim.t/q.aim.dur,0,1),width:18,alertX:q.x,alertY:q.y-40});
 }
 if(d.mode==='attack')HT27_BASE.draw(b);
 else if(d.mode==='intro'){
  if(d.musicStarted){if(d.shipFrame!=null)archBlit('ship_transform',d.shipFrame,b.x,b.y,d.shipFrame===15?192:206);else hammerOrbitalPose(b,d.introFrame,.84);}
 }
 else{
  const stop=d.mode==='break'&&d.t<1.3;
  const f=stop?12+Math.min(3,Math.floor(d.energy*3.9)):twirl?8+step%4:(Math.floor(beat/4)%2?4:0)+step%4;
  ht27Sprite('boss',f,b.x,b.y+94,225,b.flash>0?.58:1);
  if(stop){const tx=clamp(b.x,camLeftX()+128,camRightX()-128),ty=Math.max(90,b.y-100);ctx.save();ctx.font='bold 14px BOFmil,monospace';ctx.textAlign='center';ctx.lineWidth=4;ctx.strokeStyle='#07131f';ctx.fillStyle='#dff9ff';ctx.strokeText('STOP, HAMMER TIME!',tx,ty);ctx.fillText('STOP, HAMMER TIME!',tx,ty);ctx.restore();}
 }
 if(d.shield){
  const sd=HAMMER_TIME_ART.sheets.wall,r=sd.frames[Math.floor(d.clock*16)%8],wall=ht27WallBounds(d);
  if(XART.rdy('ht27_wall')){ctx.save();ctx.globalAlpha=wall.alpha;ctx.imageSmoothingEnabled=false;
   ctx.beginPath();ctx.rect(wall.x,VH*.16,wall.w,wall.h);ctx.clip();
   ctx.drawImage(XART.get('ht27_wall'),r[0],r[1],r[2],r[3],wall.x,wall.y,wall.w,wall.h);ctx.restore();}
  for(const r of d.reflections)hammerLaserDraw(r);
 }
}
function ht27Start(){
 ht27Active=true;run.mode='arcade';run._hammerTime=true;run._s9taken=1;run._s9warp=0;
 story=null;s6Opening=null;debugFight=null;_coleScene=0;stagePlan=[];waveIdx=999;spawnClock=9999;stageTimer=9999;
 enemies=[];eBullets=[];pBullets=[];powerups=[];subBoss=null;subBossDone=true;subBossTriggered=true;subBossActive=false;aminiTriggered=true;_sbMusicResumed=true;
 bossWarned=true;warnT=0;stageEnding=0;
 run.spaceMode=true;run.gravityShipReady=true;gravityMode=GRAVITY_SHIP_ACTIVE;run.spaceWeapon=0;run.spaceLevels=[3,3,3];
 run.wlevel=3;run.wlevels=WEAPONS.map(()=>3);run.bombs=Math.max(run.bombs,12);run.lives=Math.max(run.lives,5);
 player.x=worldWidth()/2;player.y=PLAY.y+PLAY.h-100;player.invuln=180;camX=player.x-VW/2;
 spawnBoss('chromehammer');bossActive=true;boss._be=null;boss._symEntry=null;boss.enter=false;boss.x=worldWidth()/2;boss.y=VH+50;boss._noHit=true;
 boss.name='HAMMER TIME';boss.hp=boss.maxhp=Math.round(hammerFurious()?9800:hammerHard()?8400:diffKey==='easy'?4800:6800);
 boss._hammer.balance0922=true;boss._hammerTime={mode:'intro',t:0,clock:0,energy:0,attack:0,helpers:[],reflections:[],locked:false,shield:false,introFrame:0,shipFrame:15,musicStarted:false};hammerState(boss,'hammer');
 ht27ClearAttacks();special=null;for(const p of [player,player2])if(p){p.roll=null;p.somer=null;p._thrustPower=0;}
 ht27Warm();HT27_BASE.state(GS.PLAY);Snd.stopMusic();
}
function ht27Stop(){
 const d=boss&&boss._hammerTime;if(d&&d.savedSpecial){special=d.savedSpecial;d.savedSpecial=null;}
 ht27Active=false;ht27Pending=false;run._hammerTime=false;timeScale=1;if(d){d.locked=false;d.shield=false;d.helpers=[];}
 if(Snd&&Snd.cur&&Snd.cur===ht27Song())Snd.stopMusic();
 ht27Variant=null;
}
submitPassword=function(){
 if(String(pwInput).trim().toUpperCase()==='HAMMER'){
  ht27Variant=null;ht27Pending=true;ht27Warm();pwInput='';PENDING_STAGE=5;_coleScene=0;run.mode='arcade';passwordDifficulty=true;
  menuIndex=Math.max(0,diffList().indexOf(diffKey||'normal'));Audio.SFX.select();setState(GS.DIFF);return;
 }
 ht27Pending=false;return HT27_BASE.submit.apply(this,arguments);
};
startRun=function(){const launch=ht27Pending;ht27Pending=false;if(ht27Active)ht27Stop();const r=HT27_BASE.start.apply(this,arguments);if(launch)ht27Start();return r;};
setState=function(s){
 if(ht27Locked()&&s==='paused')return;
 if(ht27Active){
  if([GS.STAGECLEAR,GS.OUTBOUND,GS.STAGESEL,GS.VICTORY,GS.GAMEOVER,GS.RIVAL,GS.WARPENTRY].includes(s)){ht27Stop();s=GS.TITLE;}
  else if(s===GS.TITLE||s===GS.MODESEL||s===GS.CAMPHUB)ht27Stop();
  else if(s==='paused'){const m=ht27Song();if(m)m.pause();}
  else if(s===GS.PLAY&&state==='paused'){const m=ht27Song();if(m)m.play().catch(()=>{});}
 }
 if(ht27Pending&&[GS.TITLE,GS.PASSWORD,GS.MODESEL].includes(s))ht27Pending=false;
 return HT27_BASE.state.call(this,s);
};
Audio.startMusic=function(name){return HT27_BASE.music.call(this,ht27Active&&boss&&!boss.dead&&/^(boss5|mini5|lvl5|stage|hammerTime|hama)$/.test(name)?ht27SongName():name);};
updatePlay=function(dt){
 const d=ht27Data();if(d){
  if(d.mode==='intro'&&!ht27Begin(d)){Input.clearTaps();return;}
  const c=ht27Clock(d,dt),want=ht27WantLock(c);
  if(d.mode==='intro'&&c<ht27IntroEnd()){ht27Tick(boss,dt);ht27DanceEffects(dt);efxClock+=dt;mapScroll+=dt*12;Input.clearTaps();return;}
  if(want&&!d.locked&&!ht27CombatSequence(boss))ht27LockStart(boss,d);else if(!want&&d.locked)ht27LockEnd(boss,d);
  if(d.locked){ht27Tick(boss,dt);ht27DanceEffects(dt);efxClock+=dt;mapScroll+=dt*12;Input.clearTaps();return;}
 }
 return HT27_BASE.tick.apply(this,arguments);
};
hammerBossTick=function(b,dt){if(b._hammerTime)return ht27Tick(b,dt);return HT27_BASE.hammerTick(b,dt);};
hammerBossDraw=function(b){return b._hammerTime?ht27Draw(b):HT27_BASE.draw(b);};
hammerBossDamage=function(b,dmg){if(b._hammerTime){if(b._hammerTime.shield||b._hammerTime.mode==='intro')return 0;if(b._hammerTime.mode==='attack')return HT27_BASE.damage(b,dmg);b._hammerModuleHit=null;return dmg;}return HT27_BASE.damage(b,dmg);};
bossHitTest=function(x,y){if(boss&&boss._hammerTime&&boss._hammerTime.mode!=='attack'){boss._hammerModuleHit=null;return !boss.dead&&dist2(x,y,boss.x,boss.y)<72*72;}return HT27_BASE.hit(x,y);};
// All release entry points stay inert during the locked dance, including automatic racks.
function ht27Gate(fn){return function(){if(ht27Locked())return;return fn.apply(this,arguments);};}
pShoot=ht27Gate(pShoot);useBomb=ht27Gate(useBomb);autoFireMissiles=ht27Gate(autoFireMissiles);
spaceLaserFire=ht27Gate(spaceLaserFire);spaceVolleyLaunchRack=ht27Gate(spaceVolleyLaunchRack);
spaceShadowRelease=ht27Gate(spaceShadowRelease);startSpecial=ht27Gate(startSpecial);
