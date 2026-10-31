window.FURYBOT={version:'1023-1',originalHit:playerHit,events:[],samples:[],frames:0,commands:[0,0],queue:[],nextObserve:0,nextDecision:0,nextMissile:7,nextScan:4,nextEvasion:8,nextCharge:24,nextConfirm:2,owned:['w','a','s','d','j','k','c','y','h'],keyEvents:[],stats:{protectedContacts:0,distance:0,rolls:0,somersaults:0,missiles:0,shots:0},seenShots:new WeakSet(),lastPhase:'',spawnSeen:false,completed:false};
if(window.BOFOnline)BOFOnline.submitScore=()=>{};
FURYBOT.age=()=>Math.round((performance.now()-FURYBOT.started)/10)/100;
FURYBOT.targetList=function(){
 let ts=[];try{ts=_lockTargets();}catch{}
 // Arsenal elites are native enemy containers rather than boss targets.
 for(const e of enemies)if(!e.dead&&e.hp>0&&(e._amini||e._bob20)&&!ts.includes(e))ts.push(e);
 return ts.filter(t=>!t.dead&&(t.hp==null||t.hp>0)&&Number.isFinite(t.x+t.y)&&t.x>camLeftX()+4&&t.x<camRightX()-4&&(t._drawY??t.y)>PLAY.y-25&&(t._drawY??t.y)<VH-55);
};
FURYBOT.observe=function(){
 const Q=this,t=Q.age(),targets=Q.targetList().map((a,i)=>({x:a.x,y:a._drawY??a.y,id:i,w:a.w||40,h:a.h||40}));
 const below=targets.filter(a=>a.y<player.y-25),available=below.length?below:targets;
 available.sort((a,b)=>Math.abs(a.x-player.x)-Math.abs(b.x-player.x));
 // Hold an aim for a short burst, rather than switching to a different part every frame.
 let target=available[0];if(Q.aimUntil>t&&Q.aim){const p=available.find(a=>Math.hypot(a.x-Q.aim.x,a.y-Q.aim.y)<65);if(p)target=p;}
 if(target){Q.aim=target;if(!(Q.aimUntil>t))Q.aimUntil=t+1.2;}
 const bullets=eBullets.filter(b=>!b.dead&&b.x>camLeftX()-30&&b.x<camRightX()+30&&b.y>PLAY.y-30&&b.y<VH+30).map(b=>({x:b.x,y:b.y,vx:(b.vx||0)*60,vy:(b.vy||0)*60,r:Math.min(22,Math.max(5,(b.w||8)/2))}));
 const body=bossActive?boss:subBossActive?subBoss:null;
 const bodies=(body?._rebels?body._rebels.ships:body?[body]:[]).filter(b=>!b.dead&&!b.enter).map(b=>({x:b.x,y:b._drawY??b.y,w:Math.min(b.w||80,190),h:Math.min(b.h||80,200)}));
 // Only currently drawn warning geometry, never future attack selections.
 const lines=[];
 try{if(body?._hc1007){const C=hc1007CrossState(body);if(C&&!['gap','done','dissolve'].includes(C.mode))lines.push(...C.rays);else lines.push(...(body._hc1007.lines||[]));}}catch{}
 try{if(body?._r30){const H=hf7Sample(body);if(H&&['tell','fire'].includes(H.phase))lines.push(...H.lines);}}catch{}
 return{t,target,bullets,bodies,lines};
};
FURYBOT.lineDistance=function(x,y,L){const x0=L.x??L.x1,y0=L.y??L.y1,x1=L.ex??L.x2,y1=L.ey??L.y2;if(!Number.isFinite(x0+y0+x1+y1))return 9999;const dx=x1-x0,dy=y1-y0,k=clamp(((x-x0)*dx+(y-y0)*dy)/(dx*dx+dy*dy||1),0,1);return Math.hypot(x-x0-dx*k,y-y0-dy*k);};
FURYBOT.decide=function(S){
 const spd=playerBaseSpeed()*60*1.35,L=camLeftX()+24,R=camRightX()-24,top=PLAY.y+65,bottom=VH-58;
 const reach=run.weapon===4?Math.max(110,flameReach(run.wlevel)*.70):180;
 const py=S.target?clamp(Math.max(S.target.y+reach,VH-152),top,bottom):VH-125;
 let best=Infinity,choice=[0,0],danger=0;
 for(const dy of[-1,0,1])for(const dx of[-1,0,1]){const n=dx&&dy?Math.SQRT1_2:1;let c=0;
  for(const t of[.12,.28,.44]){const x=clamp(player.x+dx*n*spd*t,L,R),y=clamp(player.y+dy*n*spd*t,top,bottom);
   for(const b of S.bullets)c+=Math.max(0,22+b.r-Math.hypot(x-b.x-b.vx*t,y-b.y-b.vy*t))*4;
   for(const b of S.bodies)c+=Math.max(0,Math.min(b.w*.36+22-Math.abs(x-b.x),b.h*.36+22-Math.abs(y-b.y)))*6;
   for(const b of S.lines)c+=Math.max(0,(b.width||18)/2+18-this.lineDistance(x,y,b))*5;
  }
  if(!dx&&!dy)danger=c;
  const fx=clamp(player.x+dx*n*spd*.25,L,R),fy=clamp(player.y+dy*n*spd*.25,top,bottom);
  c+=Math.abs(fx-(S.target?.x??worldWidth()/2))*.22+Math.abs(fy-py)*.12;
  if(dx!==this.commands[0]||dy!==this.commands[1])c+=3;
  if(dy>0&&player.y>=bottom||dy<0&&player.y<=top||dx>0&&player.x>=R||dx<0&&player.x<=L)c+=140;
  if(fx<L+15||fx>R-15)c+=5;
  if(c<best){best=c;choice=[dx,dy];}
 }
 this.commands=choice;const t=this.age();
 if(danger>62&&t>this.nextEvasion&&!player.roll&&!player.somer){const key=danger>220&&this.stats.somersaults<=this.stats.rolls?'w':choice[0]<0?'a':'d';this.keyEvents.push({at:t,key},{at:t+.105,key});this.nextEvasion=t+2.8+Math.random()*1.8;}
};
FURYBOT.pre=function(now){
 const Q=this;if(!Q.started||Q.finished)return;const t=Q.age();for(const k of Q.owned)Input.keys[k]=false;
 if(state!==GS.PLAY)return;
 if(t>Q.nextConfirm){Input.injectTap('j');Q.nextConfirm=t+2.5;}
 if(t>=Q.nextObserve){Q.queue.push(Q.observe());Q.nextObserve=t+.10;}
 if(t>=Q.nextDecision){let S;while(Q.queue.length&&Q.queue[0].t<=t-.22)S=Q.queue.shift();if(S)Q.decide(S);Q.nextDecision=t+.10;}
 const[dx,dy]=Q.commands;if(dx<0)Input.keys.a=true;if(dx>0)Input.keys.d=true;if(dy<0)Input.keys.w=true;if(dy>0)Input.keys.s=true;
 if(!Q.completed)Input.keys.j=true;
 // Read the same visible charge meter a human watches, then RELEASE FIRE.
 // Fusion is a hold/release gun; permanently holding fire never launches it.
 if(spaceWeaponsActive()&&run.spaceWeapon===1){if((run._spaceShadowCharge||0)>=SPACE_SHADOW_FULL_CHARGE*.98)Q.fireReleaseUntil=t+.16;}
 else if(colePilot()&&run.wlevel>=8&&(player._fuse||0)>=FUSE_FULL*.99)Q.fireReleaseUntil=t+.16;
 if(t<Q.fireReleaseUntil)Input.keys.j=false;
 for(const e of Q.keyEvents.filter(e=>e.at<=t))Input.injectTap(e.key);Q.keyEvents=Q.keyEvents.filter(e=>e.at>t);
 if(t>Q.nextScan){Q.scanUntil=t+2.0;Q.multi=Math.floor(t/8)%2===1;if(!Q.multi)Input.injectTap('c');Q.nextScan=t+6.5;}
 if(t<Q.scanUntil)Input.keys[Q.multi?'y':'c']=true;
 if(t>Q.nextMissile&&Q.targetList().length&&run.bombs>0){Input.injectTap('k');Input.keys.k=true;Q.nextMissile=t+1.5+Math.random()*.8;}
 // H is the native pilot charge button. Never manufacture a special pickup.
 if(t>Q.nextCharge){Q.chargeUntil=t+1.1;Q.nextCharge=t+23;}
 if(t<Q.chargeUntil)Input.keys.h=true;
 // The small arsenal elites have no protected entrance. For visible review,
 // acquire the arriving hull and watch its first tell before engaging it.
 if(Q.config.role==='elite'){
  const visible=enemies.some(e=>e._amini&&!e.dead&&e.hp>0&&e.y>PLAY.y+(e.h||80)*.35);
  if(visible&&Q.eliteSeen==null)Q.eliteSeen=t;
  if(Q.eliteSeen==null||t<Q.eliteSeen+3){Input.keys.j=false;Input.keys.k=false;Input.keys.y=false;Input.keys.c=false;}
 }
};
FURYBOT.phase=function(){const b=bossActive?boss:subBossActive?subBoss:null;if(!b)return state;
 const J=b._r30?j3State(b):null;
 return [b.kind||b._ship,b._hammer?.mode,b._hammer?.state,b._hammer?.rage?'rage':null,b._whv?.mode,b._carrier17?.mode,b._er26?.mode,b._bomber?.mode,b._r30?.mode,J?`encounter${J.encounter}:form${J.active}:mimic${J.mimic}`:null,...(b._rebels?.ships||[]).map(s=>s.rg4?.act?.kind)].filter(Boolean).join('|');};
FURYBOT.health=function(){const b=bossActive?boss:subBossActive?subBoss:null;
 if(b?._rebels)return b._rebels.ships.reduce((n,s)=>n+Math.max(0,s.hp||0),0);
 if(b)return Math.max(0,b.hp||0);
 if(this.config.role==='elite')return enemies.filter(e=>e._amini&&!e.dead).reduce((n,e)=>n+Math.max(0,e.hp),0);
 if(this.config.role==='tutorial')return Object.values(TUT?.L?.bob?.parts||{}).reduce((n,e)=>n+Math.max(0,e.hp),0);
 return null;};
FURYBOT.paint=function(){const G=this.geom,c=this.captureCtx;if(!c)return;c.imageSmoothingEnabled=false;c.fillStyle='#000';c.fillRect(0,0,G.W,G.H);
 // Use the CURRENT native layout, including the Siege Console side panels.
 // Hidden legacy HUD sources are not visible game surfaces and must not enter footage.
 for(const el of document.querySelectorAll('canvas')){const s=getComputedStyle(el),r=el.getBoundingClientRect();if(s.display==='none'||s.visibility==='hidden'||Number(s.opacity)===0||r.width<1||r.height<1||r.right<0||r.bottom<0||r.left>G.W||r.top>G.H)continue;c.drawImage(el,Math.round(r.x),Math.round(r.y),Math.round(r.width),Math.round(r.height));}
};
FURYBOT.audio=async function(){const Q=this,ac=Snd._audioCtx();await ac.resume();const dest=ac.createMediaStreamDestination(),seen=new WeakSet(),base=HTMLMediaElement.prototype.play;
 const attach=el=>{if(seen.has(el))return;seen.add(el);try{if(el._bofNode)el._bofNode.connect(dest);else{const stream=el.captureStream?.();if(stream?.getAudioTracks().length){const n=ac.createMediaStreamSource(stream);n.connect(dest);}}}catch(e){(Q.audioErrors??=[]).push(String(e));}};
 HTMLMediaElement.prototype.play=function(){const r=base.apply(this,arguments);attach(this);return r;};for(const el of Object.values(Snd.music||{}))if(el instanceof HTMLMediaElement&&!el.paused)attach(el);
 return dest.stream;};
FURYBOT.start=async function(c){this.config=c;
 const audio=await this.audio();
 diffKey='furious';run.mode='campaign';pilotIndex=PILOTS.findIndex(p=>p.key==='maverick');
 debugUnlocked=true;DBGT.god=false;DBGT.hud=false;DBGT.speed=1;
 startRun(1);
 this.loadout={pilot:run.pilot,diff:diffKey,mode:run.mode,weapon:run.weapon,level:run.wlevel,bombs:run.bombs,grants:[]};
 this.geom={W:innerWidth,H:innerHeight};const G=this.geom;this.capture=document.createElement('canvas');this.capture.width=G.W;this.capture.height=G.H;this.captureCtx=this.capture.getContext('2d');this.paint();
 const stream=this.capture.captureStream(30);for(const tr of audio.getAudioTracks())stream.addTrack(tr);
 const mime=['video/webm;codecs=vp8,opus','video/webm'].find(m=>MediaRecorder.isTypeSupported(m));this.rec=new MediaRecorder(stream,{mimeType:mime,videoBitsPerSecond:3000000});this.writeQueue=Promise.resolve();this.bytes=0;this.chunks=[];const endpoint=location.origin+'/__capture/'+c.id;
 const write=async(blob,offset)=>{let error;for(let i=0;i<4;i++){const ac=new AbortController(),timer=setTimeout(()=>ac.abort(),15000);try{const r=await fetch(endpoint,{method:'POST',headers:{'X-Capture-Offset':String(offset)},body:blob,signal:ac.signal});if(!r.ok)throw Error('capture write '+r.status);return;}catch(e){error=e;await new Promise(r=>setTimeout(r,350*(i+1)));}finally{clearTimeout(timer);}}throw error;};
 this.rec.ondataavailable=e=>{if(e.data.size){const offset=this.bytes;this.bytes+=e.data.size;this.writeQueue=this.writeQueue.then(async()=>{if(this.writeError)return;try{await write(e.data,offset);}catch(error){this.writeError=String(error);}});}};
 this.rec.onstop=async()=>{await this.writeQueue;if(!this.writeError){this.saved=true;this.chunks=[];}else{const blob=new Blob(this.chunks,{type:this.rec.mimeType});this.downloadURL=URL.createObjectURL(blob);const a=document.createElement('a');a.href=this.downloadURL;a.download=c.id+'.webm';document.body.append(a);a.click();a.remove();this.downloadFallback=true;}stream.getTracks().forEach(t=>t.stop());};
 this.started=performance.now();this.rec.start(1000);
 // Wrap only the browser adapter. The native engine still owns the single RAF,
 // real elapsed time, fixed simulation steps, all rendering and native audio.
 const raf=window.requestAnimationFrame.bind(window);window.requestAnimationFrame=cb=>raf(now=>{if(cb!==loop)return cb(now);try{this.pre(now);cb(now);this.post(now);}catch(e){this.error=String(e.stack||e);this.stop('error');throw e;}});
 return{loadout:this.loadout,geometry:{w:G.W,h:G.H}};
};
FURYBOT.stop=function(reason){if(this.finished)return;this.finished=true;this.reason=reason;this.elapsed=this.age();for(const k of this.owned)Input.keys[k]=false;if(this.rec?.state==='recording')this.rec.stop();};
FURYBOT.report=function(){return{version:this.version,config:this.config,loadout:this.loadout,elapsed:this.elapsed??this.age(),frames:this.frames,fps:this.frames/(this.elapsed??this.age()),initialHP:this.initialHP,finalHP:this.health(),completed:this.completed,reason:this.reason,stats:this.stats,samples:this.samples,events:this.events,error:this.error,audioErrors:this.audioErrors,bytes:this.bytes,saved:this.saved,writeError:this.writeError,state,playerDead:player.dead,lifeStock:run.lives,difficulty:diffKey};};

/* Review-only adapter. No shipping dependency, forced kills, enemy edits or loadout grants.
 * Combat reads native state and writes native Input keys (not a physical human test).
 * Menu navigation is sent by the host with actual CDP keyboard events.
 */
FURYBOT.version='1024-campaign-1';
FURYBOT.health=function(){const b=bossActive?boss:subBossActive?subBoss:null;return b?Math.max(0,b.hp||0):null;};
const betaInput=FURYBOT.pre;
FURYBOT.nextConfirm=Infinity;
FURYBOT.pre=function(now){
 if(state!==GS.PLAY){for(const k of this.owned)Input.keys[k]=false;
  if(state===GS.STAGESEL&&sselBoot===0&&!sselUnlockCine&&this.age()>(this.nextMapFire||0)){cmap2.focus='map';Input.injectTap('j');this.nextMapFire=this.age()+8;}
  return;}
 betaInput.call(this,now);
 // Keep complete naturally timed cinematics. Only advance ordinary portrait lines
 // after five seconds when no cinematic director owns the scene.
 if(BOFCinematicDirector.current){Input.keys.j=false;delete Input.taps?.j;}
 if(run.stage===6&&s6Wing?.choice&&!s6Wing.route){Input.keys.j=false;Input.injectTap('d');}
};
const betaHit=playerHit;
playerHit=function(source){
 const q=FURYBOT;if(q.started&&state===GS.PLAY&&!player.dead&&player.invuln<=0){
  q.stats.contactAttempts=(q.stats.contactAttempts||0)+1;
  if(q.events.length<20000)q.events.push({t:q.age(),type:DBGT.god?'god-contact':'hit-attempt',source:typeof source==='string'?source:source?.kind||'contact',stage:run.stage,x:player.x,y:player.y});
 }
 return betaHit.apply(this,arguments);
};
FURYBOT.post=function(now){const Q=this;if(!Q.started||Q.finished)return;Q.frames++;const t=Q.age();
 const delta=Q.lastNow?now-Q.lastNow:0;Q.lastNow=now;if(delta>0)(Q.frameTimes??=[]).push(delta);
 if(Q.frameTimes?.length>600000)Q.frameTimes.shift();
 if(player.dead&&!Q.wasDead){
  Q.stats.deaths=(Q.stats.deaths||0)+1;Q.events.push({t,type:'native-player-death',stage:run.stage,lives:run.lives});
  if(!DBGT.god){DBGT.god=true;Q.godAt=t;Q.events.push({t,type:'god-enabled',reason:'Native bot death; user-authorized completion fallback. No loadout/ammo/HP changes.'});}
 }Q.wasDead=!!player.dead;
 if(player.roll&&!Q.wasRoll)Q.stats.rolls++;if(player.somer&&!Q.wasSomer)Q.stats.somersaults++;
 Q.wasRoll=!!player.roll;Q.wasSomer=!!player.somer;
 if(Q.lastBombs!=null&&run.bombs<Q.lastBombs)Q.stats.missiles+=Q.lastBombs-run.bombs;Q.lastBombs=run.bombs;
 for(const b of pBullets)if(!Q.seenShots.has(b)){Q.seenShots.add(b);Q.stats.shots++;}
 const phase=Q.phase(),hp=Q.health(),label=run._gp4StageX?'X-HARRIER':String(run.stage);
 const scene=BOFCinematicDirector.current;
 const chapter=[state,label,bossActive?'BOSS':subBossActive?'MINIBOSS':'',scene?.id||''].join('|');
 if(chapter!==Q.chapter){Q.events.push({t,type:'chapter',chapter,hp,stageTime:stageTimer,score:run.score});Q.chapter=chapter;}
 if(phase!==Q.lastPhase){Q.events.push({t,type:'phase',phase,hp,stage:label});Q.lastPhase=phase;}
 if(t>(Q.nextSample||0)){
  Q.samples.push({t,state,stage:label,stageTime:stageTimer,hp,phase,x:Math.round(player.x),y:Math.round(player.y),god:DBGT.god,lives:run.lives,score:run.score,weapon:run.weapon,level:run.wlevel,bombs:run.bombs,enemyBullets:eBullets.length,enemies:enemies.length,music:Audio.currentMusic||Snd.currentMusic||null});Q.nextSample=t+2;
 }
 if(!(Q.nextPaint>now)){Q.paint();Q.nextPaint=now+1000/30;}
 if(state===GS.VICTORY&&run._trueFinaleCleared){
  Q.victoryAt??=t;
  if((drawVictory._t||0)>VICTORY_CARD_AT+7){Q.completed=true;Q.stop('native-campaign-victory-and-ending');}
 }
 if(t>Q.config.limit)Q.stop('time-limit');
};
// Southern strategy after immunity; track aim horizontally. Pursue pickups
// only when visible and close, preserving ordinary progression/pickup rewards.
const betaDecide=FURYBOT.decide;
FURYBOT.decide=function(S){
 betaDecide.call(this,S);
 if(DBGT.god){
  const y=VH-74,target=S.target;
  this.commands=[target?Math.abs(target.x-player.x)<12?0:Math.sign(target.x-player.x):Math.abs(player.x-worldWidth()/2)<15?0:Math.sign(worldWidth()/2-player.x),Math.abs(player.y-y)<9?0:Math.sign(y-player.y)];
  const pickup=powerups.filter(p=>!p.dead&&p.y>VH*.55&&p.y<VH-30&&Math.abs(p.x-player.x)<120).sort((a,b)=>Math.hypot(a.x-player.x,a.y-player.y)-Math.hypot(b.x-player.x,b.y-player.y))[0];
  if(pickup&&Math.hypot(pickup.x-player.x,pickup.y-player.y)<145)this.commands=[Math.abs(pickup.x-player.x)>9?Math.sign(pickup.x-player.x):0,Math.abs(pickup.y-player.y)>9?Math.sign(pickup.y-player.y):0];
 }
};
FURYBOT.report=function(){const a=[...(this.frameTimes||[])].sort((a,b)=>a-b),pct=p=>a[Math.min(a.length-1,Math.floor(a.length*p))];return{version:this.version,config:this.config,loadout:this.loadout,elapsed:this.elapsed??this.age(),frames:this.frames,fps:this.frames/(this.elapsed??this.age()),completed:this.completed,reason:this.reason,stats:this.stats,godEnabledAt:this.godAt,frameMs:{p50:pct(.5),p95:pct(.95),p99:pct(.99),max:a.at(-1)},samples:this.samples,events:this.events,error:this.error,audioErrors:this.audioErrors,bytes:this.bytes,saved:this.saved,writeError:this.writeError,state,stage:run.stage,score:run.score,playerDead:player.dead,lifeStock:run.lives,difficulty:diffKey,proof:P2M.proof,campaign:{rank:campaign.rank,bonusUnlocked:campaign.bonusUnlocked,stageX:campaign.stageX1004},trueFinale:run._trueFinaleCleared};};

FURYBOT.audio=async function(){
 const Q=this,ac=Snd._audioCtx();await ac.resume();const dest=ac.createMediaStreamDestination();Q.audioDest=dest;
 const attached=new WeakSet(),streams=new WeakMap(),base=HTMLMediaElement.prototype.play;
 function attach(el){
  if(attached.has(el))return;
  try{
   if(el._bofNode){el._bofNode.connect(dest);attached.add(el);return;}
   let st=streams.get(el);if(!st){st=el.captureStream();streams.set(el,st);st.addEventListener('addtrack',()=>attach(el));el.addEventListener('playing',()=>attach(el));}
   if(st.getAudioTracks().length){const src=ac.createMediaStreamSource(st);src.connect(dest);(Q.audioNodes??=[]).push(src);attached.add(el);}
  }catch(e){(Q.audioErrors??=[]).push(String(e));}
 }
 HTMLMediaElement.prototype.play=function(){const r=base.apply(this,arguments);attach(this);if(r?.then)r.then(()=>attach(this)).catch(()=>{});return r;};
 for(const el of Object.values(Snd.music||{}))if(el instanceof HTMLMediaElement&&!el.paused)attach(el);
 return dest.stream;
};
