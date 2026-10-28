'use strict';
/* Approved original recordings, minus two semitones + room reverb. Native audio only. */
const chronosEnergyVolume=v=>Math.max(0,Math.min(1,v));
const CF49={base:{sfx:c46Sfx,sound:c33Sound,log:c45Log,load:stageLoadBegin,update:updatePlay,state:setState},
 owner:null,seen:new WeakMap(),events:[],keys:{},voices:2,musicDucked:false};
const CF49_SOURCES={"rage_charge":"dbz-powerup-minus2-reverb.mp3","rage_release":"saiyan-minus2-reverb.mp3","wave_charge":"kame_charge-minus2-reverb.mp3","gather_charge":"kame_charge-minus2-reverb.mp3","wave_full":"basicbeam_fire-minus2-reverb.mp3"};
for(const [role,file]of Object.entries(CF49_SOURCES)){
 const key='chronosEnergy_'+role,uri='assets/game/shared/audio/original_sfx_minus2_reverb_1026/'+file,slots=[],list=[];
 CF49.keys[role]=key;BOFA.sfx[key]=uri;
 for(let i=0;i<CF49.voices;i++)Object.defineProperty(list,i,{enumerable:true,get(){
  if(!slots[i])slots[i]={el:new window.Audio(),uri,attached:false,used:0};return Snd._touchVoice(slots[i]);}});
 Snd.pools[key]={list,slots,i:0};Snd.TAME[key]={g:['rage_charge','wave_charge','gather_charge','wave_full'].includes(role)?1.8:1.25,native:true,min:0};
}
function chronosEnergyStopRole(role){for(const v of Snd.pools[CF49.keys[role]].slots)if(v?.el){
 v.el._bofEpoch=(v.el._bofEpoch||0)+1;try{v.el.pause();v.el.loop=false;v.el.currentTime=0;}catch(e){}}}
function chronosEnergyStop(){for(const role in CF49.keys)chronosEnergyStopRole(role);CF49.owner=null;chronosEnergyMusicMix();}
function chronosEnergyPlay(b,token,role,cycle=0){
 if(!b||b.dead||!c25Own(b)||!token||state!==GS.PLAY)return false;
 if(CF49.owner&&CF49.owner!==b)chronosEnergyStop();CF49.owner=b;
 let marks=CF49.seen.get(token);if(!marks){marks=new Set();CF49.seen.set(token,marks);}
 const id=role+':'+cycle;if(marks.has(id))return false;marks.add(id);
 if(marks.size>96)marks.delete(marks.values().next().value);
 const gain=role==='wave_tail'?.60:role==='rage_release'?.88:1;
 for(const a of Snd.pools[CF49.keys[role]].list)a.loop=role.endsWith('_charge');
 const accepted=Snd.play(CF49.keys[role],gain);chronosEnergyMusicMix();
 CF49.events.push({role,cycle,time:efxClock,phase:b._hammer.c30?.phase||b._hammer.state,gain,accepted});
 if(CF49.events.length>300)CF49.events.shift();return accepted;
}
// Lightning keeps every strike; its backing level leaves room for the foreground tell.
function chronosEnergyLightningGain(b){
 if(CF49.owner!==b||Snd.vol.sfx<=0)return 1;
 const active=Object.entries(CF49.keys).some(([role,key])=>role!=='wave_tail'&&Snd.pools[key].slots.some(v=>v?.attached&&!v.el.paused&&!v.el.ended));
 return active?.24:1;
}

function chronosEnergyForeground(){return state===GS.PLAY&&Snd.vol.sfx>0&&CF49.owner&&!CF49.owner.dead&&
 Object.entries(CF49.keys).some(([role,key])=>role!=='wave_tail'&&Snd.pools[key].slots.some(v=>v?.attached&&!v.el.paused&&!v.el.ended));}
const chronosEnergyBaseMusicDuck=pauseMusicDuck;
pauseMusicDuck=function(){return chronosEnergyBaseMusicDuck()*(chronosEnergyForeground()?.22:1);};
function chronosEnergyMusicMix(){
 // Sustained charge voices must follow live SFX/master changes, not their start value.
 for(const [role,key]of Object.entries(CF49.keys))for(const v of Snd.pools[key].slots)if(v?.attached&&!v.el.paused){
  const gain=role==='wave_tail'?.60:role==='rage_release'?.88:1;
  v.el.volume=chronosEnergyVolume(gain*Snd.TAME[key].g*Snd.vol.sfx*Snd.vol.master);
 }
 const active=!!chronosEnergyForeground();
 if((active||CF49.musicDucked)&&Snd.cur)Snd.cur.volume=chronosEnergyVolume(Snd.vol.music*Snd.vol.master*pauseMusicDuck());
 CF49.musicDucked=active;
}

const chronosEnergyBaseSetVol=Snd.setVol;
Snd.setVol=function(){const out=chronosEnergyBaseSetVol.apply(this,arguments);chronosEnergyMusicMix();return out;};

c45Log=function(type,data){const b=boss,C=b?._hammer?._hf22Charge;
 if(C&&type==='strike'&&data.n===1)chronosEnergyPlay(b,C,'rage_charge');
 if(C&&type==='final'){chronosEnergyStopRole('rage_charge');chronosEnergyPlay(b,C,'rage_release');}
 return CF49.base.log.apply(this,arguments);
};
c46Sfx=function(key){const b=boss,R=b?._hammer?.c30;
 if(c46Own(b)){
  if(['warpCharge','hammerEradCharge'].includes(key)){chronosEnergyPlay(b,R,'wave_charge');return;}
  if(key==='fusionBeam'){chronosEnergyStopRole('wave_charge');chronosEnergyPlay(b,R,'wave_full');return;}
  if(key==='expBig'&&R.phase==='kame_fire')return;
  if(key==='laserBeamEnd')return; // The approved recording owns its natural reverb tail.
 }
 return CF49.base.sfx.apply(this,arguments);
};
c33Sound=function(name,b,gain){const h=b?._hammer,R=h?.c30;
 if(c25Own(b)&&!b.dead){
  if(name==='rage'&&h._hf22Charge)return true;
  if(R&&['gather','thrust','beam','recover'].includes(R.phase)){
   if(name==='charge')return chronosEnergyPlay(b,R,'gather_charge',R.cycle||0);
   if(name==='wave'){chronosEnergyStopRole('gather_charge');return chronosEnergyPlay(b,R,'wave_full',R.cycle||0);}
  }
 }
 return CF49.base.sound.apply(this,arguments);
};
stageLoadBegin=function(n,keys){if(n===5)Snd.prepare(Object.values(CF49.keys));return CF49.base.load.apply(this,arguments);};
updatePlay=function(dt){const out=CF49.base.update.apply(this,arguments),b=CF49.owner;
 if(b&&(b!==boss||b.dead||run.stage!==5||!b._hammer._hf22Charge&&!b._hammer.c30))chronosEnergyStop();
 chronosEnergyMusicMix();return out;};
setState=function(next){if(next!==GS.PLAY)chronosEnergyStop();return CF49.base.state.apply(this,arguments);};
globalThis.BOF_CHRONOS_ENERGY_AUDIO=CF49;
