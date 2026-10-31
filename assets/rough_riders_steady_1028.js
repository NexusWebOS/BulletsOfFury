'use strict';
/* The Stage6 Rough Riders encounter holds the playfield steady. Physical
   recoil, ships, FOVs, collisions, flashes and the simulation remain native. */
const RR43={base:{world:drawWorld,camera:updateCamX,music:Audio.startMusic,rebelMusic:h3RebelMusic,warm:h3RebelAudioWarm},frames:0,dt:1/60,key:'roughriders6',scope(){return run.stage===6&&!run._gp4StageX&&!!boss?._rebels&&!boss._rebels.frStageX&&boss._rebels.ships.length===5;}};
// A separate event key avoids the legacy all-rebels-to-StageX remapper. Its
// source is the original Gasline file explicitly approved on October30; Harrier and current StageX remain separate.
BOFA.music[RR43.key]='assets/game/levels/stage_x/audio/music/LevelX.mp3';
function rr43Music(){if(!Snd.music[RR43.key]){const m=new window.Audio();m.preload='none';m.src=BOFA.music[RR43.key];m.loop=true;Snd.music[RR43.key]=m;}return Snd.music[RR43.key];}
Audio.startMusic=function(name){if(RR43.scope()&&!boss.dead&&state===GS.PLAY&&/^(boss\d+(mus)?|stagex|rival|roughriders6)$/.test(name)){
  const m=rr43Music();name=RR43.key;if(m&&Snd.cur===m&&!m.error){if(m.paused)try{m.play()?.catch(()=>{});}catch(_){}return;}}
 return RR43.base.music.call(this,name);};
h3RebelAudioWarm=function(){if(!RR43.scope())return RR43.base.warm.apply(this,arguments);const m=rr43Music();
 if(m){m.preload='auto';if(m.readyState<3&&m.networkState!==2)try{m.load();}catch(_){}}
 for(const name of ['av3_laser_charge','av3_laser_release','av3_fusion_cannon','av3_target_acquire','av3_teleport_out','av3_teleport_in','av3_impact_metal','av3_impact_energy','av3_gravity_pulse','chargeDash','enemyMachineGunHeavy','enemyShoot','missile','maverickHelixRelease','shieldUp','shieldBreak']){
  const p=Snd.pools[name],a=p?.list?.[0];if(a&&a.readyState<3&&a.networkState!==2)try{a.preload='auto';a.load();}catch(_){}
 }H3_REBEL_AUDIO.warmed=true;};
h3RebelMusic=function(){if(!RR43.scope())return RR43.base.rebelMusic.apply(this,arguments);
 if(state!==GS.PLAY||boss.dead)return;const A=H3_REBEL_AUDIO,m=rr43Music(),now=performance.now(),changed=A.owner!==boss;
 if(changed){A.owner=boss;A.time=0;A.next=0;h3RebelAudioWarm();}if(now<A.next||document.hidden)return;A.next=now+500;
 if(Snd.cur===m&&!m.paused&&!m.error){A.time=m.currentTime;try{if(Snd._ctx&&Snd._ctx.state!=='running')Snd._ctx.resume()?.catch(()=>{});}catch(_){}return;}
 const interrupted=Snd.cur!==m,restore=changed?0:interrupted?A.time:m.currentTime;if(interrupted&&restore>0&&m){Snd.stopMusic();Snd.cur=m;}
 Audio._h3RebelMusic=boss;Audio.resume();Audio.startMusic(RR43.key);if(interrupted&&restore>0&&Snd.cur===m)try{m.currentTime=restore;}catch(_){}if(!changed)A.recoveries++;
};
updateCamX=function(){if(!RR43.scope())return RR43.base.camera.apply(this,arguments);
 WORLD_W=worldWidth();const width=viewW(),max=Math.max(0,WORLD_W-width);if(!max){camX=0;return;}
 camX=clamp(camX,0,max);const want=clamp(player.x-width/2,0,max),delta=want-camX;
 // Ignore tiny pilot bobs; larger tracking moves ease with elapsed time and
 // cannot jump by more than180world pixels/second. The full arena stays reachable.
 const zone=want===0||want===max?0:12;if(Math.abs(delta)<=zone)return;if(zone===0&&Math.abs(delta)<.01){camX=want;return;}
 const dt=clamp(RR43.dt||1/60,0,.05),error=delta-Math.sign(delta)*zone;
 camX=clamp(camX+clamp(error*(1-Math.exp(-dt*5)),-180*dt,180*dt),0,max);
};
drawWorld=function(dt){if(!RR43.scope())return RR43.base.world.apply(this,arguments);
 const saved=shake,oldDT=RR43.dt;RR43.dt=dt>0?dt:1/60;shake=0;try{RR43.frames++;return RR43.base.world.apply(this,arguments);}finally{shake=saved;RR43.dt=oldDT;}};
globalThis.BOF_ROUGH_RIDERS_STEADY_1028=RR43;
