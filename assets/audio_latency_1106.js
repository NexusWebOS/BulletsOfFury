"use strict";
/* Short effects use decoded WebAudio buffers, not a new streaming decoder per
   overlap voice. Music and held loops retain their native streaming owners.
   Native Snd.play owns cue aliases, cooldowns, gains and the four volume buses. */
const AL116={cache:new Map(),queue:[],loading:0,bytes:0,limit:64*1024*1024,
 active:new Set(),maxVoices:32,epoch:0,cueEpoch:Object.create(null),clock:0,events:[],errors:[],
 base:{prepare:Snd.prepare,stop:Snd.stopCue,vol:Snd.setVol,warp:Snd.setWarpMix,state:setState,begin:beginStage},
 stats:{decoded:0,starts:0,expired:0,cancelled:0,stolen:0,echoes:0}};
function al116Log(q){AL116.events.push(q);if(AL116.events.length>256)AL116.events.shift();}
function al116Uris(name){const p=Snd.pools[name];if(!p)return [];
 if(p.uris)return p.uris;
 const raw=BOFA.sfx[name];return (Array.isArray(raw)?raw:[raw]).filter(Boolean).map(v=>v.startsWith('assets/')?v:'data:audio/mpeg;base64,'+v);
}
function al116Trim(){if(AL116.bytes<=AL116.limit)return;
 const rows=[...AL116.cache.values()].filter(q=>q.buffer).sort((a,b)=>a.used-b.used);
 for(const q of rows){if(AL116.bytes<=AL116.limit)break;AL116.bytes-=q.bytes;AL116.cache.delete(q.uri);}
}
function al116Pump(){while(AL116.loading<2&&AL116.queue.length){
 const q=AL116.queue.shift();AL116.loading++;
 fetch(q.uri).then(r=>{if(!r.ok)throw Error('SFX fetch '+r.status);return r.arrayBuffer();})
 .then(bytes=>Snd._audioCtx().decodeAudioData(bytes))
 .then(buffer=>{q.buffer=buffer;q.bytes=buffer.length*buffer.numberOfChannels*4;q.used=++AL116.clock;
  AL116.bytes+=q.bytes;AL116.stats.decoded++;q.resolve(buffer);al116Trim();})
 .catch(e=>{q.failed=true;q.resolve(null);if(AL116.errors.length<20)AL116.errors.push(String(e));})
 .finally(()=>{AL116.loading--;al116Pump();});
}}
function al116Decode(uri,urgent=false){let q=AL116.cache.get(uri);
 if(!q){q={uri,used:++AL116.clock,bytes:0,buffer:null};q.promise=new Promise(resolve=>q.resolve=resolve);AL116.cache.set(uri,q);AL116.queue.push(q);}
 q.used=++AL116.clock;
 if(urgent&&!q.buffer){const i=AL116.queue.indexOf(q);if(i>0){AL116.queue.splice(i,1);AL116.queue.unshift(q);}}
 al116Pump();return q;
}
function al116Available(){return location.protocol!=='file:'&&!!Snd._audioCtx();}
Snd.prepare=function(names){if(!al116Available())return AL116.base.prepare.apply(this,arguments);
 for(const name of Array.isArray(names)?names:[names])for(const uri of new Set(al116Uris(name)))al116Decode(uri);
};
function al116Priority(name){return Snd.VOICE_SET[name]?3:/warn|alert|lock|charge|powerup|countdown|shieldBreak/i.test(name)?2:1;}
function al116Level(v){const cfg=v.cfg,channel=Snd.VOICE_SET[v.name]?(Snd.vol.voice??1):Snd._sfxMix();
 return clamp(v.volume*(cfg?.g??1)*channel*Snd.vol.master,0,1)*(cfg?.native?1:cfg?.boost||1);
}
function al116End(v){if(!AL116.active.delete(v))return;
 for(const n of v.nodes)try{n.disconnect();}catch(_e){}
}
function al116Stop(v){try{v.src.stop();}catch(_e){}al116End(v);}
function al116Start(buffer,name,volume,cfg,born,epoch){
 if(epoch!==AL116.epoch)return false;
 const c=Snd._audioCtx();if(!c||c.state!=='running')return false;
 const priority=al116Priority(name);
 if(AL116.active.size>=AL116.maxVoices){let victim=null;
  for(const v of AL116.active)if(v.priority<=priority&&(!victim||v.priority<victim.priority||v.priority===victim.priority&&v.at<victim.at))victim=v;
  if(!victim)return false;al116Stop(victim);AL116.stats.stolen++;
 }
 const src=c.createBufferSource(),gain=c.createGain(),nodes=[src,gain];src.buffer=buffer;
 let tail=src;
 if(cfg&&!cfg.native&&cfg.lp){const lp=c.createBiquadFilter(),shelf=c.createBiquadFilter();
  lp.type='lowpass';lp.frequency.value=cfg.lp;lp.Q.value=.7;
  shelf.type='highshelf';shelf.frequency.value=2600;shelf.gain.value=-6;
  src.connect(lp);lp.connect(shelf);tail=shelf;nodes.push(lp,shelf);
 }
 const v={name,src,gain,nodes,cfg,volume,priority,at:performance.now()};gain.gain.value=al116Level(v);tail.connect(gain);
 const bus=typeof aq112Bus==='function'?aq112Bus():null;gain.connect(bus?.input||c.destination);
 src.onended=()=>al116End(v);AL116.active.add(v);src.start();AL116.stats.starts++;
 al116Log({name,delay:performance.now()-born,at:born,contextTime:c.currentTime,baseLatency:c.baseLatency||0,outputLatency:c.outputLatency||0});
 // Preserve the native portal's single throttled, slightly detuned reflection.
 // It shares the decoded sample instead of opening another streaming decoder.
 const mix=Snd.warpMix||0;
 if(mix>.04&&born-Snd._warpSfxAt>=66&&AL116.active.size<AL116.maxVoices){
  Snd._warpSfxAt=born;const echo=c.createBufferSource(),eg=c.createGain();echo.buffer=buffer;echo.playbackRate.value=.985;
  const e={name,src:echo,gain:eg,nodes:[echo,eg],cfg:{native:true,g:cfg?.g??1},volume:volume*mix*.22,priority:0,at:born,echo:true};
  eg.gain.value=al116Level(e);echo.connect(eg);eg.connect(bus?.input||c.destination);echo.onended=()=>al116End(e);
  AL116.active.add(e);echo.start(c.currentTime+(.064+mix*.034));AL116.stats.echoes++;
 }
 return true;
}
Snd.bufferPlay=function(name,volume,cfg){if(!al116Available())return null;
 const p=Snd.pools[name],uris=al116Uris(name);if(!p||!uris.length)return null;
 const uri=uris[p.i%uris.length];p.i=(p.i+1)%p.list.length;
 const q=al116Decode(uri,true),born=performance.now(),epoch=AL116.epoch,cueEpoch=AL116.cueEpoch[name]||0,level=volume==null?1:volume;
 if(q.failed)return null;
 const play=()=>{
  if(epoch!==AL116.epoch||cueEpoch!==(AL116.cueEpoch[name]||0)){AL116.stats.cancelled++;return false;}
  // A delayed gunshot or warning is misinformation. Prewarm it for the next
  // event rather than playing a stale event seconds after its visual trigger.
  if(performance.now()-born>120){AL116.stats.expired++;return false;}
  return al116Start(q.buffer,name,level,cfg,born,epoch);
 };
 const c=Snd._audioCtx();
 if(q.buffer&&c.state==='running')return play();
 const ready=q.buffer?Promise.resolve(q.buffer):q.promise;
 Promise.all([ready,c.state==='running'?null:c.resume()]).then(([buffer])=>{if(buffer)play();}).catch(()=>{});
 return true;
};
Snd.stopCue=function(name){const r=AL116.base.stop.apply(this,arguments);
 AL116.cueEpoch[name]=(AL116.cueEpoch[name]||0)+1;for(const v of AL116.active)if(v.name===name)al116Stop(v);return r;
};
Snd.setVol=function(){const r=AL116.base.vol.apply(this,arguments);
 for(const v of AL116.active){v.gain.gain.cancelScheduledValues(0);v.gain.gain.value=al116Level(v);}return r;
};
Snd.setWarpMix=function(v){const r=AL116.base.warp.apply(this,arguments);
 if(v<=.04)for(const e of [...AL116.active])if(e.echo)al116Stop(e);return r;
};
const AL116_COMMON=['blip','select','hit','machineGun','spread','laser','missile','enemyShoot','enemyMachineGunLight',
 'expSmall','expBig','mapDeploy','goodluck','bossWeaponCharge','lockAlert','powerup','dash','jetDash',
 'laserBeamStart','laserBeamEnd','flameThrowerStart','flameThrowerEnd','flameHit','enemyBossCannon','combatOrb0927'];
function al116Warm(stage){Snd.prepare(AL116_COMMON);
 if(stage===5||stage===9)Snd.prepare(['spaceLaserCannon','spaceLaserHit','spaceVolleyLaunch','spaceVolleyHit','spaceShadowCharge','spaceShadowRelease',
  'enemyPulseLaserAlien','warpCharge','warpGate','warpBurst','explosionElectrical','fusionBeam']);
}
setState=function(s){if(s!==state){AL116.epoch++;
 if(s===GS.TITLE||s===GS.MODESEL||s===GS.GAMEOVER)for(const v of [...AL116.active])al116Stop(v);
 }return AL116.base.state.apply(this,arguments);};
beginStage=function(n){al116Warm(n);return AL116.base.begin.apply(this,arguments);};
// Release unused streaming clones from legacy boot preparation. Do not touch
// music, loop elements, or any voice which has actually started playing.
for(let i=Snd._sfxVoices.length-1;i>=0;i--){const v=Snd._sfxVoices[i];if(!v.el.paused)continue;
 try{v.el.removeAttribute('src');v.el.load();}catch(_e){}v.attached=false;Snd._sfxVoices.splice(i,1);
}
al116Warm(0);
globalThis.BOF_AUDIO_LATENCY_1106={state:AL116,warm:al116Warm,ready:name=>al116Uris(name).every(uri=>!!AL116.cache.get(uri)?.buffer)};
