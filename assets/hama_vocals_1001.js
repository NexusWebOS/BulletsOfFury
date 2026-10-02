"use strict";
/* Mike's recorded performance is premixed to the existing song length. One
   HTMLAudioElement owns music, vocals, pause, looping, mute and cleanup. */
const HAMA_VOICE_BASE_1001={sing:hamaSing,lyrics:hamaLyricsTick,vocal:hama29Vocal,clock:ht27Clock,draw:drawBossSprite,lines:hamaLinesDraw};
let hamaVoicePainted1001=false;
BOFA.music.hama=HAMA_VOCALS_1001.music;
if(Snd&&Snd.music.hama){const m=Snd.music.hama;m.pause();m.preload='none';m.src=HAMA_VOCALS_1001.music;m.loop=true;}
function hamaRecordedVocals1001(){return hamaOn()&&!!HAMA_VOCALS_1001.captions.length;}
hamaSing=function(d,who,text,dur,big){
 // Gameplay still raises its event cues, but silent placeholder lyrics must not
 // overwrite the words Mike is actually singing on the recording.
 if(hamaRecordedVocals1001())return;
 return HAMA_VOICE_BASE_1001.sing.apply(this,arguments);
};
hamaLyricsTick=function(b,d,c,dt){
 if(!hamaRecordedVocals1001())return HAMA_VOICE_BASE_1001.lyrics.apply(this,arguments);
 const H=d.hama;if(!H)return;
 if(H.vocalClock1001!=null&&c<H.vocalClock1001-.5){H.stopFlags={};H.bdBeat=-1;H.lastBar=null;}
 H.vocalClock1001=c;H.lines=[];
 for(const cue of HAMA_VOCALS_1001.captions){
  if(c<cue.t)break;if(c>=cue.end)continue;
  let who=cue.who;
  if(who==='crew'&&/SOLO|UNION/.test(cue.text)&&H.singer&&!H.singer.dead)who='robot';
  H.lines=H.lines.filter(l=>l.who!==who);
  H.lines.push({who,text:cue.text,t:c-cue.t,dur:cue.end-cue.t,big:who==='shout',recorded:true});
 }
};
hama29Vocal=function(d,who){
 const line=HAMA_VOICE_BASE_1001.vocal.apply(this,arguments);
 return line||(hamaRecordedVocals1001()&&who==='boss'?d.hama.lines.find(l=>l.who==='shout'&&l.t<l.dur):null);
};
ht27Clock=function(d,dt){
 const c=HAMA_VOICE_BASE_1001.clock.apply(this,arguments);
 // Armor/stun controllers may temporarily own the boss tick. The recording
 // still advances, so its caption clock must remain outside those controllers.
 if(hamaRecordedVocals1001()&&boss&&d.hama)hamaLyricsTick(boss,d,c,dt);
 return c;
};
hamaLinesDraw=function(){hamaVoicePainted1001=true;return HAMA_VOICE_BASE_1001.lines.apply(this,arguments);};
drawBossSprite=function(b){
 hamaVoicePainted1001=false;const r=HAMA_VOICE_BASE_1001.draw.apply(this,arguments);
 if(hamaRecordedVocals1001()&&b&&b._hammerTime&&!hamaVoicePainted1001)hamaLinesDraw(b,b._hammerTime);
 return r;
};
