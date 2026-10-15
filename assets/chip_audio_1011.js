/* Mike's approved ColeForge chip library. Load after encounter/audio extensions.
 * One canonical pool/gate per cue. Owned sustained audio follows live actions.
 */
(function(root){
 'use strict';
 const bank=root.BOF_CHIP_AUDIO;
 if(!bank||typeof Snd==='undefined'||!Snd)return;
 const A=root.BOF_CHIP_PASS={bank,aliases:{},stats:{},failures:[],owned:new Map(),cache:new Map(),suspended:false,previous:{}};
 const clamp01=n=>Math.max(0,Math.min(1,n));
 const mix=()=>Snd.vol.master*Snd._sfxMix()*(Audio.isMuted?.()?0:1);
 const tuned={forgeWeld:[.50,0],forgeComplete:[.64,.5],weaponFound:[.62,.16],loadoutSelect:[.48,.06],loadoutEquip:[.58,.12],loadoutLaunch:[.64,.6],
  error:[.55,.35],enemyDie:[.58,.09],alert:[.6,1.2],element_lightning_hit:[.48,.10],geyserLightning:[.62,.45],
  stylishDodge:[.55,.3],furiousCoin:[.55,.12],achievement:[.6,.45],timedBombBeep:[.52,.04],timedBombBlast:[.76,.4],
  firewallLaunch:[.64,.2],bossShieldStatic:[.26,.3],gd_tankEngineLoop:[.10,0],gd_tankTreadLoop:[.20,0],gd_turretTraverse:[.16,0],
  gd_tankCannon:[.68,.10],gd_shellImpact:[.6,.10],expBoss:[.8,.6],expIce:[.67,.1]};
 const priorPlay=Snd.play;
 for(const [key,d] of Object.entries(bank.cues)){
  const aliases=[...(d.aliases||[]),d.sourceKey];if(key.startsWith('gd_'))aliases.push(key.slice(3));
  const prior=Snd.TAME[key]||aliases.map(k=>Snd.TAME[k]).find(Boolean);
  const t=tuned[key]||[prior?.g??.60,Math.max(prior?.min||0,/^scoreBullet/.test(key)?.10:.08)];
  const cfg={g:t[0],min:t[1],native:true},uri=bank.base+d.file,list=[],slots=[];
  for(let i=0;i<3;i++)Object.defineProperty(list,i,{enumerable:true,get(){
   if(!slots[i]){const el=new root.Audio();el.addEventListener('error',()=>A.failures.push({key,code:el.error?.code}));slots[i]={el,uri,attached:false,used:0};}
   return Snd._touchVoice(slots[i]);
  }});
  const pool={list,slots,i:0};
  for(const name of [key,...aliases]){
   A.previous[name]=BOFA.sfx[name]||null;A.aliases[name]=key;BOFA.sfx[name]=uri;Snd.pools[name]=pool;Snd.TAME[name]=cfg;
   Audio.SFX[name]=()=>Snd.play(key);
  }
 }
 Snd.play=function(name,volume){const key=A.aliases[name]||name,r=priorPlay.call(this,key,volume);if(r&&bank.cues[key])A.stats[key]=(A.stats[key]||0)+1;return r;};
 // The realm director used to collapse distinct named releases to one generic
 // laser sample before reaching Audio.SFX. Preserve the approved named cue here.
 const realmSound=r30Sound;
 r30Sound=function(key){return A.aliases[key]?Snd.play(A.aliases[key]):realmSound.apply(this,arguments);};
 // Only these aliases are approved; enemyMissile, ordinary explosions, generic
 // UI blips, voices, music and unapproved element grants retain their recordings.
 A.stop=function(token){const v=A.owned.get(token);if(!v)return;v.active=false;v.el.pause();A.owned.delete(token);};
 A.stopAll=function(){for(const token of [...A.owned.keys()])A.stop(token);};
 A.sound=function(token,key,{gain=1,loop=false,seconds=null,offset=0}={}){
  if(A.suspended||document.hidden)return null;
  let v=A.owned.get(token);if(v?.key!==key){A.stop(token);v=null;}
  if(!v){
   const d=bank.cues[key];if(!d||A.owned.size>=8)return null;
   const variant=seconds?bank.firewallVariants.reduce((a,b)=>Math.abs(Math.log(a.duration/seconds))<Math.abs(Math.log(b.duration/seconds))?a:b):null;
   const file=bank.base+(variant?.file||d.file),cacheKey=key+':'+(variant?.duration||0);
   let el=A.cache.get(cacheKey);if(!el){el=new root.Audio();el.preload='auto';el.src=file;el.addEventListener('error',()=>A.failures.push({key,code:el.error?.code}));A.cache.set(cacheKey,el);}
   // Each sustained cue has one voice. Multiple tank motors share one quiet bed.
   for(const [id,q] of A.owned)if(q.el===el)A.stop(id);
   el.pause();el.loop=loop;el.preservesPitch=true;
   v={el,key,active:true,rate:variant?variant.duration/seconds:1,gain,offset,started:false,seeked:false};A.owned.set(token,v);
   A.stats[key]=(A.stats[key]||0)+1;
  }
  v.gain=gain;v.el.volume=clamp01((Snd.TAME[key]?.g||.5)*gain*mix());
  v.el.playbackRate=v.rate*Math.max(.5,Math.min(2,typeof timeScale==='number'?timeScale:1));
  if(!v.seeked&&v.el.readyState>=1){try{v.el.currentTime=v.offset*v.rate;v.seeked=true;}catch(_){}}
  if(!v.started){v.started=true;try{const p=v.el.play();if(p?.catch)p.catch(e=>{v.started=false;if(e.name!=='AbortError'&&e.name!=='NotAllowedError')A.failures.push({key,error:e.name});});}catch(e){v.started=false;}}
  return v;
 };
 A.firewall=function(w){
  if(!w||player.dead)return null;
  const speed=(VH+300)/FIRE_CROSS,seconds=(VH+180+140)/speed;
  const v=A.sound(w,'firewallLaunch',{seconds,offset:w.t||0});if(v){v.owner=w;v.seconds=seconds;}
  return v;
 };
 // Arrival is emitted by the existing weather controller. No generic launcher
 // one-shot is stacked on top of the stretched, wave-owned recording.
 Audio.SFX.firewallArrive=function(){return wfx?.fseq?.wave?A.firewall(wfx.fseq.wave):Snd.play('firewallLaunch');};
 const weather=wfxUpdate;
 wfxUpdate=function(dt){const r=weather.apply(this,arguments),w=wfx?.fseq?.wave;
  for(const [token,v] of A.owned)if(v.key==='firewallLaunch'&&token!==w)A.stop(token);
  if(w&&state===GS.PLAY&&!player.dead)A.firewall(w);return r;
 };
 const infusion=infusionOnHit;
 infusionOnHit=function(e,b,dmg){const eligible=!_infBusy&&e&&b?._inf==='lightning',r=infusion.apply(this,arguments);if(eligible)Audio.SFX.element_lightning_hit();return r;};
 const geyser=geyserSpawn;
 geyserSpawn=function(x,y,kind){const r=geyser.apply(this,arguments);if(r&&kind==='lightning')Audio.SFX.geyserLightning();return r;};
 root.addEventListener('bof-achievement',()=>Audio.SFX.achievement());
 const convert=furiousConvertLevel;
 furiousConvertLevel=function(){const r=convert.apply(this,arguments);if(r?.fp>0)Audio.SFX.furiousCoin();return r;};
 // Forge and tank beds are outside Snd's held-player-gun loops so menus cannot
 // accidentally stop welding, and welding cannot keep playing behind a menu.
 const forgingDraw=drawForging;
 drawForging=function(dt){const r=forgingDraw.apply(this,arguments),f=forging;
  if(state===GS.FORGING&&f&&f.t>=FORGE_WELD_T0&&f.t<FORGE_WELD_T0+FORGE_WELD_T)A.sound('forge','forgeWeld',{loop:true});else A.stop('forge');return r;};
 const visible=b=>b&&!b.dead&&(b.y+(b.h||120)/2>0)&&(b.y-(b.h||120)/2<VH)&&b.x+(b.w||120)/2>camLeftX()&&b.x-(b.w||120)/2<camRightX();
 const positions=new WeakMap();
 A.tick=function(){
  if(A.suspended||document.hidden||state!==GS.PLAY||player.dead){if(state!==GS.FORGING)A.stopAll();return;}
  const tanks=[subBoss,boss].filter(b=>visible(b)&&(b._sg10||b.kind==='razorback'));
  let moving=false,turning=false;
  for(const b of tanks){const old=positions.get(b),aim=b._sg10?.attack?.target?Math.atan2(b._sg10.attack.target.y-b.y,b._sg10.attack.target.x-b.x):(b._turretAng??b.turretAng??0);
   if(old){moving ||= Math.hypot(b.x-old.x,b.y-old.y)>.02;turning ||= Math.abs(aim-old.aim)>.004;}
   positions.set(b,{x:b.x,y:b.y,aim});
  }
  for(const [token,key,on] of [['tank-engine','gd_tankEngineLoop',tanks.length],['tank-treads','gd_tankTreadLoop',moving],['tank-servo','gd_turretTraverse',turning]]){
   if(on)A.sound(token,key,{loop:true});else A.stop(token);
  }
  for(const [token,v] of A.owned){if(v.key==='firewallLaunch'&&token!==wfx?.fseq?.wave)A.stop(token);else v.el.volume=clamp01((Snd.TAME[v.key]?.g||.5)*v.gain*mix());}
 };
 const play=updatePlay;
 updatePlay=function(dt){const r=play.apply(this,arguments);A.tick();return r;};
 const stateChange=setState;
 setState=function(next){if(next!==state)A.stopAll();return stateChange.apply(this,arguments);};
 const loopsStop=Snd.loopStopAll;
 Snd.loopStopAll=function(){if(state!==GS.FORGING)A.stopAll();return loopsStop.apply(this,arguments);};
 // Contextual tank substitutions preserve the Sonic weapon's existing sonic
 // pressure/charge identity. Devastator shells and Deviator missiles get their
 // own releases and impact cues; the engine bed covers all three password rigs.
 const siege=sg10Sfx;
 sg10Sfx=function(b,cue,gap){if(cue==='razorbackRocket'&&b?._sg10?.unit==='deviator')return stageRevisionCue(b,'missileLaunch',gap);
  if(cue==='razorbackPressure'&&b?._sg10?.unit==='devastator')return stageRevisionCue(b,'gd_tankCannon',gap);return siege.apply(this,arguments);};
 const detonate=sg10Detonate;
 sg10Detonate=function(q){if(q._sg10Done)return detonate.apply(this,arguments);const original=sg10Sfx;
  sg10Sfx=function(b,k,gap){return q._sg10Unit==='sonic'?original.apply(this,arguments):stageRevisionCue(b,q._sg10Unit==='deviator'?'missileHit':'gd_shellImpact',gap);};
  try{return detonate.apply(this,arguments);}finally{sg10Sfx=original;}
 };
 root.addEventListener('blur',()=>{A.suspended=true;A.stopAll();});
 root.addEventListener('focus',()=>{A.suspended=false;});
 document.addEventListener('visibilitychange',()=>{A.suspended=document.hidden;if(document.hidden)A.stopAll();});
})(window);
