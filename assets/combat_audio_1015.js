"use strict";
/* Complete missing combat cue names using the approved recordings. Aliases
   share the original pool, mixer, retrigger gate and voice budget. No new bus,
   per-frame projectile scan, synthetic sound or media allocation is needed. */
const CA15={requests:0,aliases:{},base:{shot:enemyShotSfx,release:tb28Release,arrive:tb28Arrive,fire:tb28Fire}};
const CA15_ALIASES={
 shieldHitCombat:'shieldBossAbsorb',shieldRestore:'shieldUp',
 turbo:'jetDash',boost:'jetDash',enemyMachineGun:'enemyMachineGunLight',
 hammerWhoosh:'hammerSpin',somersault:'dash',falvaRelease:'falvaBurst',
 playerHit:'hit',warp:'warpGate',sludge:'enemyToxicSpit',lightning:'explosionElectrical',
 flameIgnite:'flameThrowerStart',fireOrbLaunch:'magmaOrb',iceOrbLaunch:'cryoOrb',
 enemyOrbImpact:'fireIceOrbImpact',laserCharge:'bossWeaponCharge'
};
for(const [alias,key]of Object.entries(CA15_ALIASES)){
 if(typeof Audio.SFX[alias]==='function'||typeof Audio.SFX[key]!=='function')continue;
 Audio.SFX[alias]=(...args)=>Audio.SFX[key](...args);CA15.aliases[alias]=key;
 if(Snd.pools[key]){Snd.pools[alias]=Snd.pools[key];Snd.TAME[alias]=Snd.TAME[key];BOFA.sfx[alias]=BOFA.sfx[key];}
}
// The callback on a targeted ball may already report a release or impact.
// Count requests (including mixer-gated ones), so cooldown never causes a
// second fallback sound and a multi-projectile volley still speaks once.
const CA15_PLAY=Snd.play;
Snd.play=function(name,...args){CA15.requests++;return CA15_PLAY.call(this,CA15.aliases[name]||name,...args);};

function ca15ShotCue(kind){
 const k=String(kind||'').toLowerCase();
 // Elemental comets are not rockets; explicit ammunition precedes families.
 if(/frostcomet|frostnoselaser|^tlv|^xorb_cryo$/.test(k))return 'enemyIceBolt';
 if(/lavacomet|^fztfireball|molten|solar/.test(k))return 'enemyFlameBolt';
 if(/missile|rocket|warhead|seeker|^emr$|^s6omega$|^homing$/.test(k))return 'missile';
 if(/^s2/.test(k))return 'enemyFlameBolt';
 if(/warpshard|crystal/.test(k))return 'enemyElectricBolt';
 if(/rail/.test(k))return 'enemyRailCannon';
 if(/shell|cannon|mortar|grenade|bomb|flak|cluster|mechshot|^xlz_rock$|kinetic_rock|^blast$/.test(k))return 'enemyBossCannon';
 if(/wind|cyclone|turbo/.test(k))return 'windGust';
 if(/^s4(brass|steel)$|^s8slug$|^s8nf_(gunship|scout)$|^kingpellet$|^embullet$|^eshot$|^eg$|^dart$|minigun/.test(k))return 'enemyMachineGunLight';
 if(/acid|toxic|venom|sludge|spore|^blob$|^s7(bio|shard|wardenmine)$/.test(k))return 'enemyToxicSpit';
 if(/sonic/.test(k))return 'razorbackPressure';
 if(/tesla|lightning|electric|^s6bolt$/.test(k))return 'enemyElectricBolt';
 if(/^s5|^s8|^s9pair$|^s6(gravity|orb)$|^orb$|^gravity$|^jchelix$|antimatter|^xlz_(burst|shadow)$|^xorb_/.test(k))return 'combatOrb0927';
 if(/^s9comet$/.test(k))return 'enemyPulseLaserAlien';
 return null;
}
enemyShotSfx=function(kind){const cue=ca15ShotCue(kind);if(cue&&Audio.SFX[cue])return Audio.SFX[cue]();return CA15.base.shot.apply(this,arguments);};
function ca15BallCue(q){
 const art=q.art==='charred'?'magma':q.art==='storm'?'lightning':q.art;
 return art==='shell'?'shell':art==='rime'||art==='cryo'?'ice':art;
}
function ca15BallImpact(q){
 const k=ca15BallCue(q);
 if(/magma|molten|solar/.test(k))return 'fireOrbImpact';
 if(/rime|cryo|ice/.test(k))return 'iceOrbImpact';
 if(/lightning/.test(k))return 'explosionElectrical';
 if(k==='shell')return 'grenadeHit';
 return 'fireIceOrbImpact';
}
tb28Fire=function(owner,o){const q=CA15.base.fire.apply(this,arguments);
 if(!q.silent){const kind=ca15BallCue(q),cue=ca15ShotCue(kind)||(/ice/.test(kind)?'enemyIceBolt':/magma|molten|solar/.test(kind)?'enemyFlameBolt':'combatOrb0927');Snd.prepare([cue,ca15BallImpact(q)]);}
 return q;
};
tb28Release=function(q){const prior=CA15.requests,eligible=q.phase==='warn'&&!q.dead&&!q.silent&&!(q.owner?.dead||q.owner?.hp<=0),r=CA15.base.release.apply(this,arguments);
 if(eligible&&CA15.requests===prior)enemyShotSfx(ca15BallCue(q));return r;
};
tb28Arrive=function(q){const prior=CA15.requests,eligible=!q.arrived&&!q.dead&&!q.silent,r=CA15.base.arrive.apply(this,arguments);
 if(eligible&&CA15.requests===prior)Audio.SFX[ca15BallImpact(q)]?.();return r;
};
