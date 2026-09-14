#!/usr/bin/env node
'use strict';

const fs=require('fs');
const path=require('path');
const root=path.resolve(__dirname,'..');
const src=fs.readFileSync(path.join(root,'assets','game.js'),'utf8');

function ok(value,message){if(!value)throw new Error(message);}
function has(text,message){ok(src.includes(text),message);}

for(const file of [
  'assets/game/sounds/ice_breath_start.wav',
  'assets/game/sounds/ice_breath_loop.wav',
  'assets/game/sounds/ice_breath_release.wav',
  'assets/game/sounds/reviewed_decker_shotgun.wav',
  'assets/game/sounds/reviewed_decker_shell_eject.wav',
  'assets/game/sounds/reviewed_decker_reload.wav',
  'assets/game/sounds/nsp_bof2_charge_shot.mp3',
  'assets/game/sounds/nsp_charge_release.mp3',
]) ok(fs.existsSync(path.join(root,file)),`missing audio asset: ${file}`);

has("dkBuck:'assets/game/sounds/reviewed_decker_shotgun.wav'",'Decker blast is not on the real sample');
has("dkShell:'assets/game/sounds/reviewed_decker_shell_eject.wav'",'Decker casing cue is not registered');
has("dkReload:'assets/game/sounds/reviewed_decker_reload.wav'",'Decker approved reload cue is not registered');
has('run._dkReloadCue=0.10;','Decker reload is not scheduled after the blast');
has('Audio.SFX.dkReload) Audio.SFX.dkReload();','Decker reload event has no audible dispatch');

has("fireIceChargeStart:'assets/game/sounds/ice_breath_start.wav'",'Thermoshock charge-start cue is missing');
has("fireIceChargeLoop:'assets/game/sounds/nsp_bof2_charge_shot.mp3'",'Thermoshock charge loop is missing');
has("fireIceOrbLaunch:'assets/game/sounds/nsp_charge_release.mp3'",'Thermoshock release cue is missing');
has("Snd.loopPrepare('fireIceChargeLoop')",'Thermoshock charge loop is not warmed');
has("Audio.SFX.fireIceChargeStart||Audio.SFX.iceBreathStart",'Thermoshock charge start is not dispatched');
has("if(!_ts && Audio.SFX.nsp_charge_release)",'Thermoshock release still stacks the generic cue');
has("k==='freezer' && run && run.weapon===5",'Freezer does not own the held trigger while charging Thermoshock');

has("iceBreathLoop:       {g:0.86, boost:1.55",'Ice Breath held bed is still buried under music');
has("Snd.loopOn(n,el==='ice'?0.90:0.78)",'Ice Breath loop request remains below foreground level');

console.log(JSON.stringify({
  freezer:{iceBreath:['start','loop','end'],thermoshock:['charge-start','charge-loop','release']},
  decker:{shotgun:['blast','shell-eject','reload'],reloadDelaySeconds:0.10},
  assetsVerified:8
},null,2));
