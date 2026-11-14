'use strict';
/* No Safe Sky. Presentation only: native final death, victory, scores, unlocks,
   saves and rewards remain with their existing owners. Authored frames blit 1:1. */
const F12={version:2,revision:3,current:null,last:null,events:[],loaded:new Set(),autoAdvance:false,
 base:{draw:drawVictory,trigger:triggerVictory,state:setState,preview:D1110.preview,previewC22:C22.preview,victoryKeys:victoryEndingKeys},
 reducedMotion:typeof matchMedia==='function'&&matchMedia('(prefers-reduced-motion: reduce)').matches,
 paused:false,audition:false,movie:false};
for(const a of Object.values(F12_ART.banks))XART._src[a.key]=a.path+'?v='+a.sha256.slice(0,12);
function f12Event(event,data={}){F12.events.push({event,...data});if(F12.events.length>500)F12.events.shift();}
const F12_ALIAS={'crew-nod':'boat-nod','cole-shit':'outdoor-crew','crew-snap':'outdoor-crew'};
function f12Name(b){return F12_ALIAS[b.visual]||b.visual;}
function f12Room(b){return /^boat|crew-nod/.test(b.visual)?'boat':/cloud|formation|approach|landing|cole-shit|run-out/.test(b.visual)?'apron':'hq';}
function f12Portrait(b){return !!b.pilot&&!['cloud-return','formation','approach','landing'].includes(b.visual);}
function f12Keys(b){
 const names=[],n=f12Name(b),panel=f12Portrait(b);if(F12_ART.banks[(panel?'panel-':'')+n])names.push((panel?'panel-':'')+n);
 if(panel)names.push('border','face-'+b.pilot,'room-'+f12Room(b));
 if(b.pilot)names.push('mini-'+f12Room(b)+'-'+b.pilot);
 if(b.avatar)names.push('avatar-'+b.avatar);
 const keys=names.map(k=>F12_ART.banks[k]?.key).filter(Boolean);
 if(b.who&&b.text){const role=b.pilot?'crew-'+b.pilot:b.avatar==='holt'||b.who==='BASE SYSTEM'?'command':b.avatar?'hostile':'narration';keys.push(CX4_ART.banks['frame-'+role].key);}
 return keys;
}
function f12Warm(s){
 const keep=new Set();for(let i=Math.max(0,s.i-1);i<Math.min(s.beats.length,s.i+3);i++)for(const k of f12Keys(s.beats[i]))keep.add(k);
 keep.add(CM3_ART.banks['ink-fade'].key);
 for(const k of keep){XART.rdy(k);if(k.startsWith('f12_'))F12.loaded.add(k);}
 for(const k of [...F12.loaded])if(!keep.has(k)){XART.releaseRoot(k);F12.loaded.delete(k);}
 return f12Keys(s.beats[s.i]).every(k=>XART.rdy(k));
}
function f12Stop(){for(const k of F12.cues||[])Snd.stopCue(k);F12.cues=new Set();F12.resume=[];}
function f12AudioPause(paused){
 if(paused){F12.resume=[];for(const k of F12.cues||[])for(const v of Snd.pools[k]?.slots||[])if(v?.attached&&!v.el.paused&&!v.el.ended){v.el._bofEpoch=(v.el._bofEpoch||0)+1;v.el.pause();F12.resume.push(v.el);}if(Snd.cur&&!Snd.cur.paused){Snd.cur.pause();F12.resume.push(Snd.cur);}}
 else{for(const el of F12.resume||[]){const q=el.play();if(q?.catch)q.catch(()=>{});}F12.resume=[];}
}
function f12Audio(){
 const urls={f12HQAlert:'hq-alert.mp3',f12HoltHelp:'holt-help.mp3',f12Phoenix:'phoenix-radio.mp3',f12VoidScream:'void-scream.mp3'};
 for(const [key,file]of Object.entries(urls)){
  const uri='assets/game/shared/cinematics/finale_1112/audio/'+file,list=[],slots=[];
  BOFA.sfx[key]=uri;for(let i=0;i<2;i++)Object.defineProperty(list,i,{enumerable:true,get(){if(!slots[i])slots[i]={el:new window.Audio(),uri,attached:false,used:0};return Snd._touchVoice(slots[i]);}});
  Snd.pools[key]={list,slots,i:0};Snd.TAME[key]={g:key==='f12VoidScream'?.8:.92,native:true,min:.4};Snd.VOICE_SET[key]=1;Audio.SFX[key]=()=>Snd.play(key);
 }
}
f12Audio();
victoryEndingKeys=function(){if(run.mode==='campaign'&&run.stage===8&&run._trueFinaleCleared)return [...new Set(F12_ART.story.slice(0,3).flatMap(b=>f12Keys(b)))];return F12.base.victoryKeys.apply(this,arguments);};
function f12Cue(s,b,key,at,previous){
 const id=s.i+':'+key+':'+at;if(s.t<at||s.cues.has(id))return;s.cues.add(id);
 if(!F12.movie&&previous<=at&&s.t-previous<.3){F12.cues.add(key);const played=Snd.play(key);f12Event('cue',{shot:b.id,key,played,at});}
}
function f12New(){
 f12Stop();D1110.ending=null;const beats=F12_ART.story.map(b=>({...b,text:b.text||''}));
 const s={id:'stage8-no-safe-sky',beats,i:0,t:0,age:0,shown:0,md:!!Input.mouse.down,cues:new Set(),phase:'film',wait:0};F12.current=s;f12Warm(s);
 Snd.prepare(['f12HQAlert','f12HoltHelp','f12Phoenix','f12VoidScream','stage3AtomicSiren','crackle','warpGate','expBig']);
 if(!F12.movie)Audio.startMusic('cinematics');f12Event('start',{pilot:run.pilot});return s;
}
function f12Frame(a,t){return a.loop?Math.floor(Math.max(0,t)*a.fps)%a.frames:Math.min(a.frames-1,Math.floor(Math.max(0,t)*a.fps));}
function f12Blit(n,f,x=0,y=0){const a=F12_ART.banks[n];if(!a||!XART.rdy(a.key))return false;f=clamp(f|0,0,a.frames-1);ctx.drawImage(XART.get(a.key),f%a.cols*a.w,Math.floor(f/a.cols)*a.h,a.w,a.h,Math.round(x),Math.round(y),a.w,a.h);return true;}
function f12Clip(x,y,w,h,fn){ctx.save();ctx.beginPath();ctx.rect(x,y,w,h);ctx.clip();fn();ctx.restore();}
function f12Mouth(b,s){return s.shown>0&&s.shown<b.text.length?[0,1,2,3,4,5,6,2,1][Math.floor(Math.max(0,s.t-.4)*9)%9]:0;}
function f12Caption(b,s){
 if(!b.who||!b.text)return;const pk=b.pilot,role=pk?'crew':b.avatar==='holt'||b.who==='BASE SYSTEM'?'command':b.avatar?'hostile':'narration';
 if(!cx4Frame(role,10,346,892,166,pk))return;const pose=f12Mouth(b,s),room=f12Room(b);
 // Portraits share one measured bay and always sit on the lower panel edge.
 if(pk)f12Blit('mini-'+room+'-'+pk,pose,30,413);
 else if(b.avatar==='holt'){
  const a=F12_ART.banks['avatar-holt'];const f=/holt-(help|extreme)/.test(b.visual)?19+Math.floor(s.t*12)%5:pose;
  f12Blit('avatar-holt',Math.min(a.frames-1,f),30,413);
 }else if(b.avatar)f12Blit('avatar-'+b.avatar,0,30,413);
 const hasFace=!!pk||!!b.avatar;msgFaceUse('dialogue');
 const layout=msgDrawBlock({text:b.text,budget:s.shown,x:hasFace?130:40,y:415,w:hasFace?730:828,h:70,maxH:16,minH:13,lineMul:1.22,color:'#fff6e6',alpha:1,outline:false,align:'left',stableCenter:false,valign:'middle'});
 const name=msgDrawBlock({text:b.who,budget:999,x:52,y:357,w:274,h:33,maxH:16,minH:12,lineMul:1,color:'#edf4ff',alpha:1,outline:false,align:'left',valign:'middle'});
 if(!F12.movie)controlHintRow([['pad_a',s.shown<b.text.length?'READ':'NEXT'],['pad_start','SKIP']],508,456,880,10);
 msgFaceUse(null);F12.caption={who:b.who,text:b.text,shown:s.shown,layout,name,avatar:pk||b.avatar||null,rect:{x:10,y:346,w:892,h:166},textRect:{x:130,y:415,w:730,h:70},avatarRect:{x:30,y:413,w:80,h:80}};
}
function f12Draw(s){
 const b=s.beats[s.i];if(!b)return;const n=f12Name(b),a=F12_ART.banks[n],face=f12Portrait(b),name=(face?'panel-':'')+n,A=F12_ART.banks[name];
 const previous=s.beats[s.i-1],fresh=!previous||previous.visual!==b.visual||previous.pilot!==b.pilot;
 d1110Viewport();ctx.save();ctx.setTransform(SS,0,0,SS,0,0);ctx.imageSmoothingEnabled=false;ctx.fillStyle='#000';ctx.fillRect(0,0,912,512);
 const readAt=.42,t=s.t,shakeShot=['skeleton-roar','skeleton-crash','transmission-blast','seeder-scream'].includes(b.visual),jitter=shakeShot&&!F12.reducedMotion?[[-3,2],[2,-2],[-1,-1],[3,2]][Math.floor(t*24)%4]:[0,0];
 let frame=A?f12Frame(A,A.loop?s.age:t):0,pose=f12Mouth(b,s);if(n==='red-alert'&&F12.reducedMotion)frame=2;
 if(b.visual==='holt-call')frame=s.shown<b.text.length&&t>readAt?Math.floor(t*10)%A.frames:0;
 if(face){
  f12Clip(0,12,600,324,()=>f12Blit(name,frame,0,0));
  const entry=fresh&&!F12.reducedMotion?Math.round(72*Math.pow(1-clamp((t-.12)/.3,0,1),3)):0;
  f12Clip(610,14,302,322,()=>{f12Blit('room-'+f12Room(b),0,604,16);f12Blit('face-'+b.pilot,pose,604+entry,16);});
  // New panels remain inked out until their own dialogue begins.
  if(fresh&&t<readAt&&!F12.reducedMotion)cm3Cover([610,14,302,322],Math.min(8,Math.floor(t/readAt*8)));
  f12Blit('border',0,0,-40);
 }else if(A)f12Blit(name,frame,jitter[0],jitter[1]);
 if(b.visual==='dead-screen'){
  msgFaceUse('dialogue');msgText('SIGNAL LOST',456,225,24,'#e77569',1,1,.02);msgFaceUse(null);
 }
 if(b.reading){msgFaceUse('dialogue');msgText(b.reading,456,b.text?332:478,13,'#e9e3b9',1,1,.02);msgFaceUse(null);}
 if(b.visual==='card'){
  msgFaceUse('dialogue');msgText('Bullets of Fury,',456,215,36,'#fff0ca',1,1,.02);msgText('will continue!',456,281,32,'#e7a76a',1,1,.02);msgFaceUse(null);
  if(!F12.movie&&s.t>3){msgFaceUse('dialogue');controlHintRow([['pad_start','TITLE']],490,456,870,14);msgFaceUse(null);}
 }
 f12Caption(b,s);
 if(fresh&&b.transition!=='cut'&&t<.32&&!F12.reducedMotion)cm3Cover([0,0,912,b.text?340:512],Math.min(8,Math.floor(t/.32*8)));
 if(b.visual==='skeleton-roar'&&t>4.45)cm3Cover([0,0,912,512],Math.max(0,8-Math.floor((t-4.45)/.55*8)));
 if(F12.paused||D1110.paused){msgFaceUse('dialogue');msgText('PAUSED',456,24,17,'#fff0ca',1,1,.02);msgFaceUse(null);}
 ctx.restore();F12.last={shot:b.id,index:s.i,visual:b.visual,bank:name,frame,pose,who:b.who,text:b.text,shown:s.shown,time:t,room:f12Room(b),portraitBottom:face?336:null,caption:b.who?F12.caption:null,allNine:['formation','landing','crew','shock','radio-crew','boat-front','crew-nod','boat-rear'].includes(b.visual)};
 D1110.last=F12.last;
}
function f12Advance(s,manual=false){
 if(s.i>=s.beats.length-1){s.phase='card';s.t=Math.max(6,s.t);s.shown=s.beats[s.i].text.length;f12Stop();return;}
 const old=s.beats[s.i];s.i++;s.t=0;s.shown=0;s.wait=0;Input.clearTaps();
 // A manually skipped shot must not leave its speech or warning playing behind the next scene.
 if(manual)for(const [at,key]of old.cue||[])if(key.startsWith('f12')||key==='stage3AtomicSiren')Snd.stopCue(key);
 if(s.beats[s.i].visual==='transmission-blast')Snd.stopCue('f12HoltHelp');
 f12Warm(s);f12Event('shot',{id:s.beats[s.i].id});
}
function f12Title(){f12Stop();F12.current=null;D1110.ending=null;drawVictory._t=0;drawVictory._ready=false;setState(GS.TITLE);menuIndex=0;Audio.startMusic('title');Input.clearTaps();}
function f12Skip(s){f12Stop();Audio.stopMusic();s.i=s.beats.length-1;s.t=0;s.shown=0;s.phase='film';s.wait=0;Input.clearTaps();f12Warm(s);f12Event('skip');}
function f12Step(s,dt){
 const paused=F12.paused||D1110.paused;if(!!paused!==!!s.audioPaused){f12AudioPause(paused);s.audioPaused=!!paused;}if(paused)return;
 const b=s.beats[s.i];s.age+=Math.max(0,dt);const click=Input.mouse.down&&!s.md;s.md=!!Input.mouse.down;
 if(s.age>.2&&Input.menuStart()){if(s.phase==='card'||b.visual==='card')f12Title();else f12Skip(s);return;}
 if(s.age>.2&&(Input.menuConfirm()||click)){
  if(s.phase==='card'||b.visual==='card'){f12Title();return;}
  if(s.shown<b.text.length){s.shown=b.text.length;}else f12Advance(s,true);return;
 }
 if(!f12Warm(s)){s.wait+=Math.max(0,dt);return;}
 const prev=s.t,before=s.shown;s.t+=Math.max(0,dt);s.shown=Math.max(s.shown,Math.min(b.text.length,Math.floor(Math.max(0,s.t-.42)*34)));
 if(!F12.movie)dialogueLetterTicks(b.text,before,s.shown);
 if(!F12.movie){
  const musicId=s.i+':music';if(Object.hasOwn(b,'music')&&!s.cues.has(musicId)){s.cues.add(musicId);if(b.music)Audio.startMusic(b.music);else Audio.stopMusic();}
  if(Snd.cur)Snd.cur.volume=clamp((b.who?.length ? .27 : .42)*Snd.vol.music*Snd.vol.master,0,1);
 }
 for(const [at,key]of b.cue||[])f12Cue(s,b,key,at,prev);
 // Dialogue waits for the player; action beats retain their authored timing.
 // Preview movie export advances explicitly using the same frame selection.
 if(s.phase!=='card'&&(!b.who||F12.autoAdvance)&&s.t>=Math.max(b.duration,b.text.length/34+.95))f12Advance(s);
}
triggerVictory=function(){F12.current=null;f12Stop();return F12.base.trigger.apply(this,arguments);};
const F12_DRAW=drawVictory;
drawVictory=function(dt){
 if(run.mode!=='campaign'||run.stage!==8||!drawVictory._trueEnding)return F12_DRAW.apply(this,arguments);
 const s=F12.current||f12New();f12Step(s,Math.min(.1,Math.max(0,dt||0)));
 if(F12.current===s){
  // Keep the previous complete shot visible while a cold next image decodes.
  if(!f12Warm(s)&&s.presented)f12Draw(s.presented);
  else{f12Draw(s);s.presented={...s,presented:null};}
 }
};Object.assign(drawVictory,F12_DRAW);
setState=function(next){if(next!==GS.VICTORY&&F12.current){f12Stop();F12.current=null;for(const k of F12.loaded)XART.releaseRoot(k);F12.loaded.clear();}return F12.base.state.apply(this,arguments);};
F12.preview=function(pilot='cole',index=0){
 BOFCinematicDirector.cancel();run.mode='campaign';run.stage=8;run.pilot=F12_ART.pilots.includes(pilot)?pilot:'cole';Input.clearTaps();Input.mouse.down=false;
 setState(GS.VICTORY);drawVictory._trueEnding=true;drawVictory._ready=true;const s=f12New();s.i=clamp(index|0,0,s.beats.length-1);f12Warm(s);return s;
};
const f12Preview=(id,p,...rest)=>id==='ending'?F12.preview(p):F12.base.preview(id,p,...rest);
D1110.preview=S113.preview=f12Preview;C22.preview=(id,p)=>id==='ending'?F12.preview(p):F12.base.previewC22(id,p);
F12.draw=f12Draw;F12.step=f12Step;F12.keys=f12Keys;F12.warm=f12Warm;F12.pause=function(v){F12.paused=!!v;if(F12.current)F12.current.audioPaused=F12.paused;f12AudioPause(F12.paused);};F12.stop=f12Stop;
window.BOF_STAGE8_FINALE_1112=F12;
