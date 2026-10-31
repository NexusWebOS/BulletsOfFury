'use strict';
/* EH85: normalized authored mint optics, explicit UFO sound events and measured
   quiet-cue corrections. Native HP, movement/hits, projectiles and victory remain EH57-owned. */
const EH85={revision:2,base:{audio:combatAudio0927,tick:s9VoidHorizonTick,clear:eh57Clear,load:stageLoadBegin,update:updatePlay,state:setState,duck:pauseMusicDuck,play:Snd.play,letters:dialogueLetterTicks},events:[],owner:null,duckUntil:0,ducked:false,keys:{},letters:new Map()};
// Radio and menu panels share a renderer. Repainting or measuring an already
// revealed line must not replay every letter, nor steal the combat voices.
dialogueLetterTicks=function(text,from,to){if(!text||!Number.isFinite(to))return;const now=performance.now(),n=clamp(Math.floor(to),0,text.length);let m=EH85.letters.get(text);
 if(!m||now-m.at>800){m={n:0,at:now};EH85.letters.set(text,m);}m.at=now;
 const start=Math.max(m.n,Number.isFinite(from)?Math.floor(from):0);m.n=Math.max(m.n,n);if(n<=start)return;
 // One tick for a revealed batch prevents catch-up frames from stacking clicks.
 for(let i=n-1;i>=start;i--)if(/[^\s]/.test(text[i])){EH85.base.letters.call(this,text,i,i+1);break;}
 if(EH85.letters.size>64)EH85.letters.delete(EH85.letters.keys().next().value);
};
if(Snd.TAME.dialogueLetter)Snd.TAME.dialogueLetter={...Snd.TAME.dialogueLetter,min:Math.max(.026,Snd.TAME.dialogueLetter.min||0)};
for(const [name,a]of Object.entries(EH85_ART)){XART._src[a.key]=a.path;ER28_ART['eh57_'+name]=a;if(name==='beam')ER28_ART.eh57_beam_water=a;}
for(const role of ['charge','release','orb','boost','half','sustain']){
 const key='horizon85_'+role,uri='assets/game/shared/audio/horizon_mix_1031/'+role+'.mp3',list=[],slots=[];EH85.keys[role]=key;BOFA.sfx[key]=uri;
 for(let i=0;i<2;i++)Object.defineProperty(list,i,{enumerable:true,get(){if(!slots[i])slots[i]={el:new window.Audio(),uri,attached:false,used:0};return Snd._touchVoice(slots[i]);}});
 Snd.pools[key]={list,slots,i:0};Snd.TAME[key]={g:role==='sustain'?.83:role==='charge'?1.16:1.12,native:true,min:role==='orb'?.12:role==='release'?.18:.15};Audio.SFX[key]=()=>Snd.play(key);
}
// Source audit at the40% cabinet mix: these existing samples were4â€“13dB
// below heavy fire. Adjust only the measured quiet families, retaining gates.
const EH85_GAINS={combatOrb0927:1.12,cfComboWater:.85,jetDash:.85,combatToxic0927:1.05,bossWeaponCharge:1.06,combatBeam0927:1.02,geyserLightning:.92};
for(const [key,g]of Object.entries(EH85_GAINS))if(Snd.TAME[key]){
 const canonical=globalThis.BOF_CHIP_PASS?.aliases[key]||key;
 for(const alias of Object.keys(Snd.pools))if(Snd.pools[alias]===Snd.pools[canonical]&&Snd.TAME[alias])Snd.TAME[alias]={...Snd.TAME[alias],g};}
function eh85Log(event,data={}){EH85.events.push({event,time:efxClock,...data});if(EH85.events.length>800)EH85.events.shift();}
function eh85Stop(){for(const key of Object.values(EH85.keys)){
 const L=Snd.loops[key];if(L){L.on=false;L.hold=0;L.lvl=0;L.playing=false;L.pending=false;L.el.pause();L.el.currentTime=0;}
 for(const v of Snd.pools[key].slots)if(v?.attached){v.el._bofEpoch=(v.el._bofEpoch||0)+1;v.el.pause();v.el.currentTime=0;}
 }EH85.owner=null;}
combatAudio0927=function(b,cue,interval){if(eh57Own(b)&&b._eh57){const H=b._eh57;
 const role=cue==='bossWeaponCharge'?(H.mode==='half'?'half':'charge'):cue==='jetDash'?'boost':cue==='combatOrb0927'?'orb':cue==='combatBeam0927'?'release':null;
 if(role){const key=EH85.keys[role],before=EH85.events.length;const r=EH85.base.audio.call(this,b,key,interval);if(r)eh85Log('attack-cue',{mode:H.mode,phase:H.phase,role,key});return r;}}
 return EH85.base.audio.apply(this,arguments);};
const EH85_PRIORITY=new Set(['bossWeaponCharge','combatBeam0927','combatOrb0927','combatToxic0927','geyserLightning','tidalWaterWave','tidalWallAlert','cfComboWater','enemyHeavyLaser','chargeDash','rd27Lightning']);
Snd.play=function(key,volume){const accepted=EH85.base.play.apply(this,arguments);
 if(accepted&&Snd.vol.sfx>0&&(EH85_PRIORITY.has(key)||key.startsWith('horizon85_'))&&state===GS.PLAY&&run.stage>=5)EH85.duckUntil=Math.max(EH85.duckUntil,performance.now()+(/Charge|charge/.test(key)?900:420));
 return accepted;};
function eh85Foreground(){const b=EH85.owner,H=b?._eh57;return state===GS.PLAY&&Snd.vol.sfx>0&&!!b&&b===subBoss&&!b.dead&&run.stage===9&&H&&['charge','fire','edge-charge','dash','water-charge'].includes(H.phase);}
pauseMusicDuck=function(){return EH85.base.duck()*(eh85Foreground()?.48:state===GS.PLAY&&performance.now()<EH85.duckUntil?.68:1);};
function eh85Mix(){const active=eh85Foreground()||state===GS.PLAY&&performance.now()<EH85.duckUntil;if(Snd.cur&&(active||EH85.ducked))Snd.cur.volume=clamp(Snd.vol.music*Snd.vol.master*pauseMusicDuck(),0,1);EH85.ducked=!!active;}
s9VoidHorizonTick=function(b,dt){const out=EH85.base.tick.apply(this,arguments);if(eh57Own(b)&&!b.dead){EH85.owner=b;const H=b._eh57;
 if(H.beams.length&&(H.phase==='fire'||H.phase==='dash'))Snd.loopOn(EH85.keys.sustain,.85);
 if(H.phase==='edge-charge'&&H._eh85Edge!==H.dashTurn){H._eh85Edge=H.dashTurn;combatAudio0927(b,'bossWeaponCharge',.3);}
 if(H.phase==='return'&&H._eh85Return!==H.dashTurn){H._eh85Return=H.dashTurn;combatAudio0927(b,'jetDash',.3);}
 }return out;};
eh57Clear=function(b){if(EH85.owner===b)eh85Stop();return EH85.base.clear.apply(this,arguments);};
stageLoadBegin=function(n,keys){if(n===9){Snd.prepare(Object.values(EH85.keys));Snd.loopPrepare(EH85.keys.sustain);}return EH85.base.load.call(this,n,n===9?[...(keys||[]),...Object.values(EH85_ART).map(a=>a.key)]:keys);};
updatePlay=function(dt){const out=EH85.base.update.apply(this,arguments);if(EH85.owner&&(EH85.owner!==subBoss||EH85.owner.dead||run.stage!==9))eh85Stop();eh85Mix();return out;};
setState=function(next){if(next!==GS.PLAY){eh85Stop();EH85.duckUntil=0;}const out=EH85.base.state.apply(this,arguments);eh85Mix();return out;};
globalThis.BOF_HORIZON_AUDIO=EH85;
