/* Review-only. Loaded by record.py, never by the shipping index.html.
 * Only damage immunity and isolated encounter/loadout setup are privileged.
 * During combat the pilot uses the native input layer; all enemies remain native.
 */
window.FURYBOT={version:'1023-1',originalHit:playerHit,events:[],samples:[],frames:0,commands:[0,0],queue:[],nextObserve:0,nextDecision:0,nextMissile:7,nextScan:4,nextEvasion:8,nextCharge:24,nextConfirm:2,owned:['w','a','s','d','j','k','c','y','h'],keyEvents:[],stats:{protectedContacts:0,distance:0,rolls:0,somersaults:0,missiles:0,shots:0},seenShots:new WeakSet(),lastPhase:'',spawnSeen:false,completed:false};
playerHit=function(source){if(!player.dead&&player.invuln<=0){FURYBOT.stats.protectedContacts++;if(FURYBOT.events.length<4000)FURYBOT.events.push({t:FURYBOT.age(),type:'protected-contact',source:typeof source==='string'?source:source?.kind||source?.type||'enemy',x:player.x,y:player.y});}return;};
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
FURYBOT.post=function(now){const Q=this;if(!Q.started||Q.finished)return;Q.frames++;const t=Q.age();
 const p=Q.lastPlayer;if(p)Q.stats.distance+=Math.hypot(player.x-p.x,player.y-p.y);Q.lastPlayer={x:player.x,y:player.y};
 if(player.roll&&!Q.wasRoll)Q.stats.rolls++;if(player.somer&&!Q.wasSomer)Q.stats.somersaults++;Q.wasRoll=!!player.roll;Q.wasSomer=!!player.somer;
 const bombs=run.bombs;if(Q.lastBombs!=null&&bombs<Q.lastBombs)Q.stats.missiles+=Q.lastBombs-bombs;Q.lastBombs=bombs;
 for(const b of pBullets)if(!Q.seenShots.has(b)){Q.seenShots.add(b);Q.stats.shots++;}
 const hp=Q.health();if(bossActive||subBossActive||hp>0){if(!Q.spawnSeen){Q.spawnSeen=true;Q.initialHP=hp;Q.events.push({t,type:'native-spawn',hp,diff:diffKey});}}
 const phase=Q.phase();if(phase!==Q.lastPhase){Q.events.push({t,type:'phase',phase,hp});Q.lastPhase=phase;}
 if(t>Q.nextSample||Q.nextSample==null){Q.samples.push({t,state,hp,x:Math.round(player.x),y:Math.round(player.y),diff:diffKey,weapon:run.weapon,level:run.wlevel,spaceWeapon:run.spaceWeapon,spaceLevels:run.spaceLevels,bombs,enemyBullets:eBullets.length,phase,sim:stageTimer,debug:!!debugFight});Q.nextSample=t+2;}
 let done=Q.spawnSeen&&!debugFight&&[GS.DEBUGFADE,GS.DEBUG].includes(state);
 // The native actor's removal after its death reel is also an honest finish.
 // Stage5's post-fight portal choice can otherwise hold PLAY after the fight.
 if(Q.spawnSeen&&bossDefeated&&!bossActive&&!subBossActive&&!boss&&!subBoss)done=true;
 if(Q.config.route)done=Q.spawnSeen&&(bossDefeated||[GS.STAGECLEAR,GS.STAGESEL,GS.FLYOVER].includes(state));
 if(Q.config.role==='elite')done=Q.spawnSeen&&hp===0;
 if(Q.config.role==='tutorial')done=Q.spawnSeen&&hp===0;
 if(Q.config.heart)done=Q.spawnSeen&&(bossDefeated||state==='chromeheart_result');
 if(done&&!Q.completed){Q.completed=true;Q.completedAt=t;Q.events.push({t,type:'native-defeat',hp,state});}
 if(!(Q.nextPaint>now)){Q.paint();Q.nextPaint=now+1000/30;}
 if(Q.completed&&t>Q.completedAt+5)Q.stop('native-defeat');
 else if(t>Q.config.limit)Q.stop('time-limit');
};
FURYBOT.paint=function(){const G=this.geom,c=this.captureCtx;if(!c)return;c.imageSmoothingEnabled=false;c.fillStyle='#000';c.fillRect(0,0,G.W,G.H);
 // Use the CURRENT native layout, including the Siege Console side panels.
 // Hidden legacy HUD sources are not visible game surfaces and must not enter footage.
 for(const el of document.querySelectorAll('canvas')){const s=getComputedStyle(el),r=el.getBoundingClientRect();if(s.display==='none'||s.visibility==='hidden'||Number(s.opacity)===0||r.width<1||r.height<1||r.right<0||r.bottom<0||r.left>G.W||r.top>G.H)continue;c.drawImage(el,Math.round(r.x),Math.round(r.y),Math.round(r.width),Math.round(r.height));}
};
FURYBOT.audio=async function(){const Q=this,ac=Snd._audioCtx();await ac.resume();const dest=ac.createMediaStreamDestination(),seen=new WeakSet(),base=HTMLMediaElement.prototype.play;
 const attach=el=>{if(seen.has(el))return;seen.add(el);try{if(el._bofNode)el._bofNode.connect(dest);else{const stream=el.captureStream?.();if(stream?.getAudioTracks().length){const n=ac.createMediaStreamSource(stream);n.connect(dest);}}}catch(e){(Q.audioErrors??=[]).push(String(e));}};
 HTMLMediaElement.prototype.play=function(){const r=base.apply(this,arguments);attach(this);return r;};for(const el of Object.values(Snd.music||{}))if(el instanceof HTMLMediaElement&&!el.paused)attach(el);
 return dest.stream;};
FURYBOT.start=async function(c){this.config=c;diffKey='furious';run.mode='arcade';DIFF=difficultyForRun('arcade','furious');debugMenu.autoRec=false;
 const audio=await this.audio();
 if(c.route){pilotIndex=PILOTS.findIndex(p=>p.key==='cole');GP4.route=c.route;GP4.stage6Only=!c.stageX;startRun(6);}
 else if(c.heart){pilotIndex=PILOTS.findIndex(p=>p.key==='cole');CH21.pending=true;startRun(5);}
 else if(c.song){pilotIndex=PILOTS.findIndex(p=>p.key==='cole');hamaPending=c.song==='hama';ht27Variant=hamaPending?HAMA_VARIANT:null;ht27Pending=true;ht27Warm();startRun(5);debugFight={...c,t:0,spawned:true};}
 else if(c.alternate){pilotIndex=PILOTS.findIndex(p=>p.key==='cole');startRun(c.stage);on5LaunchEncounter({stage:c.stage,role:'alt',kind:c.kind,code:'ALT'+c.stage});debugFight={...c,role:'mini',t:0,spawned:true};}
 else if(c.role==='tutorial'){pilotIndex=PILOTS.findIndex(p=>p.key==='cole');tutStart({stage:1,lead:'cole',disp:'decker'});setState(GS.PLAY);TUT.i=TUT_LESSONS.findIndex(d=>d.id==='exam')-1;tutNext();const L=TUT.L;L.wave=2;sg20ExamWave(L);}
 else {debugStartFight(c,{pilot:'cole'});if(c.role==='elite'){warnT=0;bossWarned=false;stageTimer=curStage.length*ARSENAL_MINI_DEF[c.kind].at;subBossDone=subBossTriggered=true;bossActive=false;boss=null;stagePlan=[];spawnArsenalMini(c.kind);debugFight=null;}}
 // A disclosed normal weapon loadout; enemy health, parts and AI untouched.
 run.weapon=0;run.wlevel=c.level??3;run.wlevels=WEAPONS.map(()=>c.level??3);run.spaceWeapon=0;run.spaceLevels=[c.level??3,c.level??3,c.level??3];run.speed=2;run.speedLevel=2;run.missileLevel=1;
 this.loadout={pilot:run.pilot,weapon:run.weapon,level:run.wlevel,spaceLevels:run.spaceLevels.slice(),speed:run.speed,missileLevel:run.missileLevel,bombs:run.bombs,diff:diffKey};
 this.geom={W:innerWidth,H:innerHeight};const G=this.geom;this.capture=document.createElement('canvas');this.capture.width=G.W;this.capture.height=G.H;this.captureCtx=this.capture.getContext('2d');this.paint();
 const stream=this.capture.captureStream(30);for(const tr of audio.getAudioTracks())stream.addTrack(tr);
 const mime=['video/webm;codecs=vp8,opus','video/webm'].find(m=>MediaRecorder.isTypeSupported(m));this.rec=new MediaRecorder(stream,{mimeType:mime,videoBitsPerSecond:4000000});this.writeQueue=Promise.resolve();this.bytes=0;this.chunks=[];const endpoint=location.origin+'/__capture/'+c.id;
 const write=async(blob,offset)=>{let error;for(let i=0;i<4;i++){const ac=new AbortController(),timer=setTimeout(()=>ac.abort(),15000);try{const r=await fetch(endpoint,{method:'POST',headers:{'X-Capture-Offset':String(offset)},body:blob,signal:ac.signal});if(!r.ok)throw Error('capture write '+r.status);return;}catch(e){error=e;await new Promise(r=>setTimeout(r,350*(i+1)));}finally{clearTimeout(timer);}}throw error;};
 this.rec.ondataavailable=e=>{if(e.data.size){const offset=this.bytes;this.bytes+=e.data.size;this.chunks.push(e.data);this.writeQueue=this.writeQueue.then(async()=>{if(this.writeError)return;try{await write(e.data,offset);}catch(error){this.writeError=String(error);}});}};
 this.rec.onstop=async()=>{await this.writeQueue;if(!this.writeError){this.saved=true;this.chunks=[];}else{const blob=new Blob(this.chunks,{type:this.rec.mimeType});this.downloadURL=URL.createObjectURL(blob);const a=document.createElement('a');a.href=this.downloadURL;a.download=c.id+'.webm';document.body.append(a);a.click();a.remove();this.downloadFallback=true;}stream.getTracks().forEach(t=>t.stop());};
 this.started=performance.now();this.rec.start(1000);
 // Wrap only the browser adapter. The native engine still owns the single RAF,
 // real elapsed time, fixed simulation steps, all rendering and native audio.
 const raf=window.requestAnimationFrame.bind(window);window.requestAnimationFrame=cb=>raf(now=>{if(cb!==loop)return cb(now);try{this.pre(now);cb(now);this.post(now);}catch(e){this.error=String(e.stack||e);this.stop('error');throw e;}});
 return{loadout:this.loadout,geometry:{w:G.W,h:G.H}};
};
FURYBOT.stop=function(reason){if(this.finished)return;this.finished=true;this.reason=reason;this.elapsed=this.age();for(const k of this.owned)Input.keys[k]=false;if(this.rec?.state==='recording')this.rec.stop();};
FURYBOT.report=function(){return{version:this.version,config:this.config,loadout:this.loadout,elapsed:this.elapsed??this.age(),frames:this.frames,fps:this.frames/(this.elapsed??this.age()),initialHP:this.initialHP,finalHP:this.health(),completed:this.completed,reason:this.reason,stats:this.stats,samples:this.samples,events:this.events,error:this.error,audioErrors:this.audioErrors,bytes:this.bytes,saved:this.saved,writeError:this.writeError,state,playerDead:player.dead,lifeStock:run.lives,difficulty:diffKey};};
