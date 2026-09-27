"use strict";
// Finished ElevenLabs recordings layered/mastered with Mike's ColeForge SFX engine.
// Loaded before game.js so lazy audio pools receive the final paths on first creation.
const AUDIO_0927_ROOT='assets/game/sfx_0927/';
const AUDIO_0927_GROUPS={
  missile_auto_1:['missile','spaceVolleyLaunch','volleyLaunch','nuclearLaunch','enemyMissile'],
  boss_charge:['bossWeaponCharge','chargeStart','furnaceLaserCharge','warshipCoreCharge','hammerEradCharge','quadCharge'],
  hammer_slam:['hammerImpact','groundBombImpact','bodyDrop'],
  stun:['shieldBreakCombat','enemyBossHit','combatStun0927'],
  beam:['furnaceLaserBurst','hammerEradBlast','fusionBeam','enemyHeavyLaser','combatBeam0927'],
  toxic:['enemyToxicSpit','bossfireSludgeemperor','combatToxic0927'],
  ice:['cryoOrb','iceOrbImpact','combatIce0927'],
  alien:['symbioteWarcry','wardenRoar','wardenScream','mechScream','combatAlien0927'],
  cannon:['enemyBossCannon','combatCannon0927'],
  module_break:['coreUnlocked','combatModule0927'],
  energy_release:['quadFire','combatEnergy0927'],
  servo_charge:['hammerMagnet','combatServo0927'],
  plasma_orb:['combatOrb0927']
};
function audio0927Register(){
  if(!window.BOFA)return;
  for(const [file,names] of Object.entries(AUDIO_0927_GROUPS))for(const name of names)
    BOFA.sfx[name]=file==='missile_auto_1'?[AUDIO_0927_ROOT+'missile_auto_1.mp3',AUDIO_0927_ROOT+'missile_auto_3.mp3']:AUDIO_0927_ROOT+file+'.mp3';
}
function audio0927Mix(A){
  for(const [file,names] of Object.entries(AUDIO_0927_GROUPS))for(const name of names){
    const heavy=['beam','hammer_slam','alien'].includes(file),repeat=file==='missile_auto_1';
    A.TAME[name]={g:heavy?.80:repeat?.58:.88,native:true,min:repeat?.11:file==='boss_charge'?.55:heavy?.30:.18};
  }
}
let combatAudioClock0927=0;
function combatAudioTick0927(dt){combatAudioClock0927+=Math.max(0,dt);}
function combatAudio0927(owner,cue,interval=.16){
  if(!owner||!cue||!Audio.SFX[cue])return false;
  // Wave scheduling freezes stageTimer during encounters. Audio must keep time
  // while those attacks repeat, using only elapsed combat simulation time.
  const t=combatAudioClock0927;
  const times=owner._audio0927||(owner._audio0927={});
  if(times[cue]!=null&&t-times[cue]<interval)return false;
  times[cue]=t;Audio.SFX[cue]();return true;
}
function combatAudioState0927(b,mode){
  if(/stun|knockback|exposed/.test(mode))combatAudio0927(b,'combatStun0927',.6);
  else if(/catch|rebuild|unfold|uncurl/.test(mode))combatAudio0927(b,'combatServo0927',.5);
  else if(/phantom|shadowcall|mirror|eclipse/.test(mode))combatAudio0927(b,'combatAlien0927',1.2);
}
