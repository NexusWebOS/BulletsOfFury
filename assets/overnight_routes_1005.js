"use strict";
/* Six-character ceiling. Passwords use the ordinary difficulty/pilot flow. */
const ON5R={submit:submitPassword,start:startRun,state:setState};
const ON5_CODES={};
for(let n=1;n<=9;n++){
 ON5_CODES['BOSS'+n]={stage:n,role:'boss'};PASSWORDS['BOSS'+n]=n;
 if(SUBBOSS[n]?.kind){ON5_CODES['MINI'+n]={stage:n,role:'mini'};PASSWORDS['MINI'+n]=n;}
 if(ALTBOSS[n]?.kind){ON5_CODES['ALT'+n]={stage:n,role:'alt',kind:ALTBOSS[n].kind};PASSWORDS['ALT'+n]=n;}
}
for(let n=1;n<=3;n++){ON5_CODES['FINAL'+n]={stage:8,role:'boss',phase:n-1};PASSWORDS['FINAL'+n]=8;}
for(const [code,i]of Object.entries({HOST8:0,HELI8:1,FURN8:2,CRYO8:3,STORM8:4,KNIGHT:5,ACE8:6,WARD8:7})){
 ON5_CODES[code]={stage:8,role:'boss',phase:2,mimic:i};PASSWORDS[code]=8;
}
submitPassword=function(){const code=String(pwInput).toUpperCase();ON5.pending=ON5_CODES[code]?{...ON5_CODES[code],code}:null;return ON5R.submit.apply(this,arguments);};
function on5LaunchEncounter(E){
 BOFCinematicDirector.cancel();story=null;debugFight=null;storySkip();setState(GS.PLAY);
 stagePlan=[];spawnClock=9999;waveIdx=9999;fb2Talk=null;s6Opening=null;H3.release=false;
 enemies=[];eBullets=[];pBullets=[];powerups=[];groundTargetingReset();tb28Reset();warnT=0;
 boss=null;bossActive=false;bossDefeated=false;bossWarned=E.role==='boss';subBoss=null;subBossActive=false;
 subBossTriggered=true;subBossDone=E.role==='boss';_sc1=_sc2=_mc1=_mc2=true;
 const entry=debugFightFor(E.stage,E.role==='boss'?'boss':'mini');
 if(!entry&&!E.kind)throw new Error('Missing password encounter '+E.code);
 const kind=E.kind||entry.kind;
 mapScroll=E.role==='boss'?(DEBUG_BOSS_SCROLL[E.stage]||0):(SUBBOSS[E.stage]?.afterScroll||0);
 stageTimer=E.role==='boss'?curStage.length+1:curStage.length*(SUBBOSS[E.stage]?.at||.5);
 if(E.stage===6){s6WingInit();s6Wing.route='left';s6Wing.all=true;s6Wing.beats=3;s6Wing.fakeDone=true;s6Wing.supplyIndex=3;s6WingLaunch(4,true);s6Wing.line=null;}
 if(E.role==='boss')spawnBoss(kind);else spawnSubBoss__inner(kind);
 if(j3State(boss)&&E.phase!=null){j3Encounter(boss,E.phase);if(E.phase===2)bossPhaseMusic(8,3);
  if(E.mimic!=null){j3Mimic(boss,E.mimic);bossPhaseMusic(8,3);}}
 Audio.startMusic(E.role==='boss'?'boss'+E.stage:BOFA.music['mini'+E.stage]?'mini'+E.stage:'boss'+E.stage);
 // Phase music is mapped by the existing authored music registry, not aliases.
 if(j3State(boss))bossPhaseMusic(8,(E.phase??0)+1);
 Input.clearTaps?.();on5Log('passwordEncounter',{code:E.code,kind,role:E.role,stage:E.stage});return E.role==='boss'?boss:subBoss;
}
startRun=function(fromStage=1){const E=ON5.pending;ON5.pending=null;const r=ON5R.start.apply(this,arguments);
 if(E&&E.stage===fromStage)on5LaunchEncounter(E);return r;};
setState=function(next){const r=ON5R.state.apply(this,arguments);if(ON5.pending&&![GS.DIFF,GS.PILOT,GS.PILOT2,GS.INTRO,GS.PLAY,GS.LAUNCH,GS.LOADOUT].includes(state))ON5.pending=null;return r;};
